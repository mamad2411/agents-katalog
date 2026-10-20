# Agent Awareness Guide: Capability Registry & Service Discovery

**Capability ID**: SAP-048
**Modern Namespace**: chora.awareness.capability_registry_discovery
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Quick Start for Agents

This guide provides agent-specific patterns for discovering and querying capabilities from the Chora distributed registry. If you're an AI agent (Claude Code, Claude Desktop, etc.), start here.

**What You'll Learn**:
- How to list all available capabilities
- How to check if a service is healthy
- How to resolve dependency chains
- How to search capability documentation
- How to monitor registry changes in real-time

**Prerequisites**:
- etcd cluster running at `localhost:2379` (or custom host)
- GitOps sync service populating registry
- Heartbeat service monitoring Service-type capabilities
- Python with `etcd3` library installed (`pip install etcd3`)

---

## Common Agent Workflows

### Workflow 1: Discover Available Capabilities

**User Request**: "What capabilities are available?"

**Agent Action**:

```python
import etcd3
import json

# Connect to registry
etcd = etcd3.client(host='localhost', port=2379)

# List all capabilities
print("Available Capabilities:\n")

capabilities = []
prefix = '/chora/capabilities/'

for value, meta in etcd.get_prefix(prefix):
    key_str = meta.key.decode('utf-8')

    # Only process metadata keys
    if not key_str.endswith('/metadata'):
        continue

    namespace = key_str.split('/')[3]
    metadata = json.loads(value)

    capabilities.append({
        'namespace': namespace,
        'title': metadata['dc_title'],
        'type': metadata['dc_type'],
        'status': metadata['chora_status'],
        'description': metadata.get('dc_description', 'N/A')
    })

# Sort by namespace
capabilities.sort(key=lambda c: c['namespace'])

# Group by type
services = [c for c in capabilities if c['type'] == 'Service']
patterns = [c for c in capabilities if c['type'] == 'Pattern']

print(f"Service-Type Capabilities ({len(services)}):")
for svc in services:
    print(f"  - {svc['namespace']}")
    print(f"    {svc['description']}")
    print(f"    Status: {svc['status']}\n")

print(f"\nPattern-Type Capabilities ({len(patterns)}):")
for pat in patterns:
    print(f"  - {pat['namespace']}")
    print(f"    {pat['description']}")
    print(f"    Status: {pat['status']}\n")
```

**Agent Response Template**:
```
I found 45 capabilities in the registry:

Service-Type Capabilities (9):
- chora.devex.registry: Distributed capability registry with etcd backend
  Status: production
- chora.devex.bootstrap: Project bootstrapping and scaffolding
  Status: draft
...

Pattern-Type Capabilities (36):
- chora.infrastructure.sap_framework: Skilled Awareness Package framework
  Status: production
- chora.awareness.task_tracking: Persistent task tracking with beads
  Status: pilot
...
```

---

### Workflow 2: Check Service Health

**User Request**: "Is the registry service healthy?"

**Agent Action**:

```python
import etcd3
import json
import datetime

def check_service_health(namespace: str) -> dict:
    """Check health of a Service-type capability"""
    etcd = etcd3.client(host='localhost', port=2379)

    health_key = f'/chora/capabilities/{namespace}/health'
    health_json, meta = etcd.get(health_key)

    if not health_json:
        return {
            'healthy': False,
            'reason': 'No health key (lease expired or service not running)'
        }

    health = json.loads(health_json)

    # Calculate age
    timestamp = datetime.datetime.fromisoformat(health['timestamp'].replace('Z', '+00:00'))
    age = (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds()

    # Get lease TTL
    ttl = None
    if meta.lease_id:
        try:
            lease = etcd.Lease(meta.lease_id)
            ttl = lease.ttl
        except:
            pass

    # Determine health
    healthy = (age < 30 and ttl is not None and ttl > 0)

    return {
        'healthy': healthy,
        'age': age,
        'ttl': ttl,
        'heartbeat_count': health['heartbeat_count'],
        'last_heartbeat': health['timestamp'],
        'reason': f"Last heartbeat {age:.1f}s ago, TTL {ttl}s remaining" if healthy else f"Stale heartbeat (age: {age:.1f}s)"
    }

# Check registry service health
result = check_service_health('chora.devex.registry')

if result['healthy']:
    print(f"✓ Service is healthy")
    print(f"  Last heartbeat: {result['last_heartbeat']}")
    print(f"  Heartbeat count: {result['heartbeat_count']}")
    print(f"  TTL remaining: {result['ttl']}s")
else:
    print(f"✗ Service is unhealthy")
    print(f"  Reason: {result['reason']}")
```

**Agent Response Template**:
```
The registry service (chora.devex.registry) is healthy:
- Last heartbeat: 2025-11-15T22:30:15Z (5.2s ago)
- Heartbeat count: 142
- Lease TTL: 24s remaining

The service is actively sending heartbeats and should be operational.
```

---

### Workflow 3: Resolve Dependencies

**User Request**: "What are the dependencies for task-tracking (SAP-015)?"

**Agent Action**:

```python
import etcd3
import json

def resolve_dependencies(namespace: str, visited=None, depth=0):
    """Recursively resolve dependencies for a capability"""
    etcd = etcd3.client(host='localhost', port=2379)

    if visited is None:
        visited = set()

    if namespace in visited:
        return []  # Cycle detection

    visited.add(namespace)
    resolved = []

    # Get dependencies
    deps_key = f'/chora/capabilities/{namespace}/dependencies'
    deps_json, _ = etcd.get(deps_key)

    if not deps_json:
        return resolved

    dependencies = json.loads(deps_json)

    for dep in dependencies:
        target = dep['capability']
        relationship = dep['relationship']

        # Check if target exists
        metadata_key = f'/chora/capabilities/{target}/metadata'
        metadata_json, _ = etcd.get(metadata_key)

        if not metadata_json:
            resolved.append({
                'capability': target,
                'relationship': relationship,
                'exists': False,
                'depth': depth
            })
            continue

        metadata = json.loads(metadata_json)

        resolved.append({
            'capability': target,
            'title': metadata['dc_title'],
            'relationship': relationship,
            'exists': True,
            'depth': depth
        })

        # Recurse
        sub_deps = resolve_dependencies(target, visited.copy(), depth + 1)
        resolved.extend(sub_deps)

    return resolved

# Resolve dependencies
namespace = 'chora.awareness.task_tracking'
deps = resolve_dependencies(namespace)

print(f"Dependencies for {namespace}:\n")

if not deps:
    print("No dependencies")
else:
    # Group by depth
    by_depth = {}
    for dep in deps:
        depth = dep['depth']
        if depth not in by_depth:
            by_depth[depth] = []
        by_depth[depth].append(dep)

    # Print by depth
    for depth in sorted(by_depth.keys()):
        print(f"Level {depth + 1} (Direct):" if depth == 0 else f"Level {depth + 1} (Transitive):")
        for dep in by_depth[depth]:
            if dep['exists']:
                print(f"  - {dep['capability']} ({dep['relationship']})")
                print(f"    {dep['title']}")
            else:
                print(f"  - {dep['capability']} ({dep['relationship']}) [MISSING]")
        print()
```

**Agent Response Template**:
```
Dependencies for chora.awareness.task_tracking:

Level 1 (Direct):
- chora.infrastructure.sap_framework (prerequisite)
  Skilled Awareness Package framework

Level 2 (Transitive):
- chora.devex.documentation_framework (runtime)
  Documentation framework for structured docs

All dependencies are satisfied and available in the registry.
```

---

### Workflow 4: Search Documentation

**User Request**: "Find documentation about health monitoring"

**Agent Action**:

```python
import etcd3

def search_artifacts(query: str, limit: int = 10):
    """Search artifacts by keyword (case-insensitive)"""
    etcd = etcd3.client(host='localhost', port=2379)

    results = []
    prefix = '/chora/artifacts/'

    for value, meta in etcd.get_prefix(prefix):
        key_str = meta.key.decode('utf-8')

        # Only search content, not metadata
        if not key_str.endswith('/content'):
            continue

        content = value.decode('utf-8')

        # Simple keyword search (case-insensitive)
        if query.lower() in content.lower():
            # Extract namespace and artifact type from key
            parts = key_str.split('/')
            if len(parts) >= 5:
                namespace = parts[3]
                artifact_type = parts[4]

                # Find first occurrence for preview
                idx = content.lower().find(query.lower())
                start = max(0, idx - 100)
                end = min(len(content), idx + 100)
                preview = content[start:end]

                results.append({
                    'namespace': namespace,
                    'artifact_type': artifact_type,
                    'preview': preview,
                })

                if len(results) >= limit:
                    break

    return results

# Search for "health monitoring"
results = search_artifacts("health monitoring", limit=5)

print(f"Found {len(results)} matching artifact(s):\n")

for i, result in enumerate(results, 1):
    print(f"{i}. {result['namespace']}/{result['artifact_type']}")
    print(f"   ...{result['preview']}...\n")
```

**Agent Response Template**:
```
I found 5 documents mentioning "health monitoring":

1. chora.devex.registry/capability-charter
   ...health monitoring via etcd TTL leases. Service-type capabilities report health status every 10 seconds...

2. chora.awareness.capability_registry_discovery/protocol-spec
   ...Pattern 4: Check Service Health. Goal: Determine if a Service-type capability is healthy...

3. chora.devex.registry/protocol-spec
   ...Heartbeat Service implements health monitoring for Service-type capabilities using etcd leases...

Would you like me to read the full content of any of these documents?
```

---

### Workflow 5: Monitor Registry Changes

**User Request**: "Watch for new capabilities being added"

**Agent Action**:

```python
import etcd3
import json

def watch_registry(watch_prefix='/chora/capabilities/'):
    """Watch for registry changes in real-time"""
    etcd = etcd3.client(host='localhost', port=2379)

    print(f"Watching {watch_prefix} for changes...\n")

    for event in etcd.watch_prefix(watch_prefix):
        key_str = event.key.decode('utf-8')

        if event.type == 'PUT':
            # Key created or updated
            if '/health' in key_str:
                namespace = key_str.split('/')[3]
                health = json.loads(event.value)
                print(f"[HEARTBEAT] {namespace}: count={health['heartbeat_count']}, status={health['status']}")

            elif '/metadata' in key_str:
                namespace = key_str.split('/')[3]
                metadata = json.loads(event.value)
                print(f"[UPDATE] Capability updated: {namespace}")
                print(f"  Title: {metadata['dc_title']}")
                print(f"  Type: {metadata['dc_type']}")
                print(f"  Version: {metadata['chora_version']}\n")

            else:
                print(f"[PUT] {key_str}")

        elif event.type == 'DELETE':
            # Key deleted
            if '/health' in key_str:
                namespace = key_str.split('/')[3]
                print(f"[FAILURE] Service unhealthy: {namespace} (lease expired)\n")

            elif '/metadata' in key_str:
                namespace = key_str.split('/')[3]
                print(f"[REMOVED] Capability removed: {namespace}\n")

            else:
                print(f"[DELETE] {key_str}")

# Start watching (runs indefinitely)
watch_registry()
```

**Agent Response Template**:
```
I'm now watching the registry for changes. I'll notify you when:
- New capabilities are added
- Existing capabilities are updated
- Service health changes
- Services become unhealthy

Press Ctrl+C to stop watching.

[HEARTBEAT] chora.devex.registry: count=142, status=healthy
[HEARTBEAT] chora.devex.bootstrap: count=89, status=healthy
[UPDATE] Capability updated: chora.awareness.task_tracking
  Title: Task Tracking & Persistent Memory
  Type: Pattern
  Version: 2.1.0
```

---

## Quick Reference Patterns

### Pattern: List Service-Type Capabilities

```python
import etcd3
import json

etcd = etcd3.client(host='localhost', port=2379)

services = []
for value, meta in etcd.get_prefix('/chora/capabilities/'):
    key_str = meta.key.decode('utf-8')
    if key_str.endswith('/metadata'):
        metadata = json.loads(value)
        if metadata['dc_type'] == 'Service':
            services.append(metadata)

for svc in services:
    print(f"{svc['dc_identifier']}: {svc['dc_title']}")
```

---

### Pattern: Get Capability Version

```python
namespace = 'chora.devex.registry'
version_key = f'/chora/capabilities/{namespace}/version'
version, _ = etcd.get(version_key)

print(f"Version: {version.decode('utf-8')}")
```

---

### Pattern: Check if Capability Exists

```python
namespace = 'chora.awareness.task_tracking'
metadata_key = f'/chora/capabilities/{namespace}/metadata'
metadata_json, _ = etcd.get(metadata_key)

if metadata_json:
    print(f"Capability exists: {namespace}")
else:
    print(f"Capability not found: {namespace}")
```

---

### Pattern: Get Artifact Content

```python
namespace = 'chora.infrastructure.sap_framework'
artifact_type = 'capability-charter'

content_key = f'/chora/artifacts/{namespace}/{artifact_type}/content'
content, _ = etcd.get(content_key)

if content:
    print(content.decode('utf-8'))
else:
    print(f"Artifact not found: {namespace}/{artifact_type}")
```

---

### Pattern: List All Service Health Statuses

```python
import json

etcd = etcd3.client(host='localhost', port=2379)

health_statuses = []
for value, meta in etcd.get_prefix('/chora/capabilities/'):
    key_str = meta.key.decode('utf-8')

    if key_str.endswith('/health'):
        namespace = key_str.split('/')[3]
        health = json.loads(value)
        health_statuses.append({
            'namespace': namespace,
            'status': health['status'],
            'timestamp': health['timestamp'],
            'count': health['heartbeat_count']
        })

for status in health_statuses:
    print(f"{status['namespace']}: {status['status']} (count: {status['count']})")
```

---

## Bash Quick Reference (Using etcdctl)

### List All Capabilities

```bash
# List all metadata keys
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | grep /metadata

# Count capabilities
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only | grep /metadata | wc -l
```

---

### Check Service Health

```bash
namespace="chora.devex.registry"

# Get health status
docker-compose exec etcd1 etcdctl get "/chora/capabilities/${namespace}/health"

# Check if health key exists (exit code 0 = healthy)
if docker-compose exec etcd1 etcdctl get "/chora/capabilities/${namespace}/health" > /dev/null 2>&1; then
    echo "Service healthy"
else
    echo "Service unhealthy"
fi
```

---

### Get Capability Metadata

```bash
namespace="chora.awareness.task_tracking"

# Get metadata
docker-compose exec etcd1 etcdctl get "/chora/capabilities/${namespace}/metadata"

# Get type
docker-compose exec etcd1 etcdctl get "/chora/capabilities/${namespace}/type"

# Get version
docker-compose exec etcd1 etcdctl get "/chora/capabilities/${namespace}/version"
```

---

### Search Artifacts

```bash
# Search for keyword in all artifacts
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix | grep -i "health monitoring"

# List all artifact content keys
docker-compose exec etcd1 etcdctl get /chora/artifacts/ --prefix --keys-only | grep /content
```

---

### Watch for Changes

```bash
# Watch all capabilities
docker-compose exec etcd1 etcdctl watch /chora/capabilities/ --prefix

# Watch specific capability
docker-compose exec etcd1 etcdctl watch /chora/capabilities/chora.devex.registry/ --prefix

# Watch for health changes only
docker-compose exec etcd1 etcdctl watch /chora/capabilities/ --prefix | grep health
```

---

## Common Agent Pitfalls

### Pitfall 1: Not Checking Service Health Before Use

**Problem**: Agent uses a Service-type capability without checking health

**Impact**: Operations fail because service is unhealthy

**Solution**: Always check health before using Service-type capabilities

```python
# Bad
result = use_capability('chora.devex.registry')

# Good
health = check_service_health('chora.devex.registry')
if health['healthy']:
    result = use_capability('chora.devex.registry')
else:
    print(f"Cannot use capability: {health['reason']}")
```

---

### Pitfall 2: Ignoring Missing Dependencies

**Problem**: Agent installs a capability without resolving dependencies

**Impact**: Capability doesn't work because prerequisites are missing

**Solution**: Resolve and validate dependencies before installation

```python
# Bad
install_capability('chora.awareness.task_tracking')

# Good
deps = resolve_dependencies('chora.awareness.task_tracking')
missing = [d for d in deps if not d['exists']]

if missing:
    print(f"Missing dependencies: {[d['capability'] for d in missing]}")
    print("Install dependencies first")
else:
    install_capability('chora.awareness.task_tracking')
```

---

### Pitfall 3: Hardcoding Capability Lists

**Problem**: Agent has hardcoded list of capabilities instead of querying registry

**Impact**: Agent doesn't discover new capabilities added to registry

**Solution**: Always query registry dynamically

```python
# Bad
CAPABILITIES = ['chora.devex.registry', 'chora.awareness.task_tracking', ...]

# Good
capabilities = list_all_capabilities()  # Query registry
```

---

### Pitfall 4: Not Handling Connection Errors

**Problem**: Agent doesn't handle etcd connection failures gracefully

**Impact**: Agent crashes when etcd is unavailable

**Solution**: Use try/except for connection errors

```python
# Bad
etcd = etcd3.client(host='localhost', port=2379)
metadata, _ = etcd.get(key)

# Good
try:
    etcd = etcd3.client(host='localhost', port=2379)
    etcd.status()  # Test connection
    metadata, _ = etcd.get(key)
except Exception as e:
    print(f"ERROR: Cannot connect to registry: {e}")
    print("Ensure etcd cluster is running (docker-compose up -d)")
    # Graceful fallback
```

---

### Pitfall 5: Inefficient Queries

**Problem**: Agent uses prefix queries when direct key reads would suffice

**Impact**: Slow query performance (20ms vs 5ms)

**Solution**: Use direct key reads when namespace is known

```python
# Bad (slow: 20ms)
for value, meta in etcd.get_prefix('/chora/capabilities/'):
    key_str = meta.key.decode('utf-8')
    if 'chora.devex.registry' in key_str:
        ...

# Good (fast: 5ms)
key = '/chora/capabilities/chora.devex.registry/metadata'
metadata, _ = etcd.get(key)
```

---

## Integration with Other SAPs

### SAP-015 (Task Tracking)

**Use Case**: Tag beads tasks with capability namespaces

```bash
# Create task for installing capability
bd init "Install SAP-048" \
    --tags capability:chora.awareness.capability_registry_discovery \
    --priority high

# Query tasks by capability
bd list --tags capability:chora.awareness.capability_registry_discovery
```

---

### SAP-049 (Namespace Resolution)

**Use Case**: Resolve legacy SAP-XXX identifiers to modern namespaces

```python
# Resolve legacy identifier
legacy_id = 'SAP-015'
namespace = resolve_namespace(legacy_id)  # Returns 'chora.awareness.task_tracking'

# Then query registry
metadata_key = f'/chora/capabilities/{namespace}/metadata'
metadata, _ = etcd.get(metadata_key)
```

---

### SAP-009 (Agent Awareness)

**Use Case**: Update AGENTS.md files when adopting registry patterns

```markdown
## SAP-048: Capability Registry Discovery

This project uses the distributed capability registry for service discovery.

**Agent Patterns**:
- Query registry for available capabilities
- Check service health before use
- Resolve dependencies automatically

**Example**:
\```python
from registry import list_capabilities, check_health

capabilities = list_capabilities()
health = check_health('chora.devex.registry')
\```
```

---

## Troubleshooting

### Issue: "Cannot connect to etcd"

**Symptoms**: `etcd3.client()` raises connection error

**Diagnosis**:
```bash
# Check if etcd is running
docker-compose ps

# Check etcd logs
docker-compose logs etcd1

# Test connectivity
ping localhost
telnet localhost 2379
```

**Solution**:
```bash
# Start etcd cluster
cd infrastructure/etcd
docker-compose up -d

# Wait for cluster to be healthy
docker-compose exec etcd1 etcdctl endpoint health
```

---

### Issue: "Capability not found"

**Symptoms**: `etcd.get()` returns `None` for capability metadata

**Diagnosis**:
```bash
# Check if GitOps sync is running
docker-compose logs gitops-sync

# Manually check etcd
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix --keys-only
```

**Solution**:
```bash
# Run manual sync
python scripts/gitops-sync-registry.py --sync-once

# Or restart GitOps sync
docker-compose restart gitops-sync
```

---

### Issue: "Service always shows unhealthy"

**Symptoms**: Health check always returns `healthy=False`

**Diagnosis**:
```bash
# Check if heartbeat service is running
docker-compose logs heartbeat

# Check if health keys exist
docker-compose exec etcd1 etcdctl get /chora/capabilities/ --prefix | grep health
```

**Solution**:
```bash
# Restart heartbeat service
docker-compose restart heartbeat

# Check heartbeat logs for errors
docker-compose logs heartbeat | grep ERROR
```

---

## Performance Tips

1. **Cache Metadata**: Cache capability metadata client-side (60s TTL) to reduce queries
2. **Use Direct Reads**: Use direct key reads instead of prefix queries when namespace is known
3. **Batch Queries**: Use etcd transactions for batch operations
4. **Parallel Queries**: Query multiple capabilities in parallel using async/await
5. **Watch Once**: Use watch mode instead of polling for real-time updates

---

## References

- [Protocol Specification](protocol-spec.md) - Complete technical spec
- [Capability Charter](capability-charter.md) - Problem statement and solution design
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [etcd Python Client Docs](https://python-etcd3.readthedocs.io/) - etcd3 library documentation
- [etcd v3 API](https://etcd.io/docs/v3.5/learning/api/) - etcd API reference

---

**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-16
**Next Review**: After initial agent adoption (2 weeks)
