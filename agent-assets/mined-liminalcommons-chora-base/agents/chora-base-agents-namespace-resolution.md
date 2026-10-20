# Agent Awareness Guide: Namespace Resolution & Ontology Navigation

**Capability ID**: SAP-049
**Modern Namespace**: chora.awareness.namespace_resolution
**Type**: Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-16

---

## Quick Start for Agents

This guide provides agent-specific patterns for resolving legacy SAP-XXX identifiers to modern `chora.domain.capability` namespaces. If you're an AI agent (Claude Code, Claude Desktop), start here.

**What You'll Learn**:
- How to detect legacy SAP-XXX identifiers in user input
- How to resolve SAP-XXX to modern namespaces
- How to provide deprecation warnings
- How to navigate the ontology by domain
- How to guide users through migration

**Prerequisites**:
- Alias redirect service running at `localhost:8001` (optional - can use local file)
- [alias-mapping.json](../../../capabilities/alias-mapping.json) available locally

---

## Common Agent Workflows

### Workflow 1: Detect and Resolve Legacy Identifiers

**User Request**: "I want to install SAP-015"

**Agent Action**:

```python
import re
import requests

def detect_and_resolve_legacy_ids(user_input: str) -> list:
    """Detect SAP-XXX identifiers and resolve to modern namespaces"""
    # Regex to detect SAP-XXX pattern
    sap_pattern = r'SAP-(\d{3})'
    matches = re.findall(sap_pattern, user_input)

    resolutions = []

    for match in matches:
        sap_id = f"SAP-{match}"

        # Call alias API
        response = requests.get(f"http://localhost:8001/api/v1/resolve/{sap_id}")

        if response.status_code == 200:
            result = response.json()
            resolutions.append(result)

    return resolutions

# Usage
user_input = "I want to install SAP-015 and SAP-001"
resolutions = detect_and_resolve_legacy_ids(user_input)

for res in resolutions:
    print(f"⚠️ {res['deprecation_warning']}")
    print(f"   Modern namespace: {res['namespace']}\n")
```

**Agent Response Template**:
```
⚠️ I noticed you're using legacy identifiers. These are deprecated and will stop working on 2026-06-01 (197 days):

- SAP-015 → chora.awareness.task_tracking
- SAP-001 → chora.infrastructure.inbox

I'll install the capabilities using their modern namespaces instead.
```

---

### Workflow 2: Resolve Single Identifier

**User Request**: "What is SAP-015?"

**Agent Action**:

```python
import requests

def resolve_sap_id(sap_id: str) -> dict:
    """Resolve single SAP-XXX identifier"""
    # Normalize input (handle "15", "SAP-15", "SAP-015")
    if not sap_id.startswith("SAP-"):
        sap_id = f"SAP-{sap_id.zfill(3)}"

    response = requests.get(f"http://localhost:8001/api/v1/resolve/{sap_id}")

    if response.status_code == 404:
        return None

    return response.json()

# Usage
result = resolve_sap_id("SAP-015")

if result:
    print(f"Legacy: {result['sap_id']}")
    print(f"Modern: {result['namespace']}")
    print(f"Status: {'Deprecated' if result['deprecated'] else 'Active'}")
    print(f"Days until sunset: {result['days_until_sunset']}")
else:
    print("SAP-XXX not found")
```

**Agent Response Template**:
```
SAP-015 refers to **Task Tracking** (modern namespace: `chora.awareness.task_tracking`).

⚠️ Note: SAP-015 is deprecated and will stop working on 2026-06-01 (197 days). Please use the modern namespace instead.

Would you like me to help you install it?
```

---

### Workflow 3: Fallback to Local File (Service Unavailable)

**Problem**: Alias redirect service is down or not deployed

**Agent Action**:

```python
import json
import requests
from datetime import datetime, date

def resolve_with_fallback(sap_id: str) -> dict:
    """Resolve with fallback to local alias-mapping.json"""
    # Try API first
    try:
        response = requests.get(
            f"http://localhost:8001/api/v1/resolve/{sap_id}",
            timeout=2
        )

        if response.status_code == 200:
            return response.json()

    except requests.exceptions.RequestException:
        # Fallback to local file
        pass

    # Use local alias-mapping.json
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    if sap_id not in mapping['aliases']:
        return None

    alias_info = mapping['aliases'][sap_id]

    # Calculate days until sunset
    sunset_date = datetime.strptime(mapping['sunset_date'], '%Y-%m-%d').date()
    days_until_sunset = (sunset_date - date.today()).days

    return {
        'sap_id': sap_id,
        'namespace': alias_info['namespace'],
        'deprecated': alias_info['status'] == 'deprecated',
        'days_until_sunset': max(0, days_until_sunset),
        'source': 'local_fallback'
    }

# Usage
result = resolve_with_fallback("SAP-015")
```

---

### Workflow 4: Find Capabilities by Domain

**User Request**: "What capabilities are available in the devex domain?"

**Agent Action**:

```python
import json

def find_capabilities_by_domain(domain: str) -> list:
    """Find all capabilities in a domain"""
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    capabilities = []

    for sap_id, info in mapping['aliases'].items():
        namespace = info['namespace']

        # Extract domain (chora.DOMAIN.capability)
        parts = namespace.split('.')
        if len(parts) >= 3 and parts[1] == domain:
            capabilities.append({
                'sap_id': sap_id,
                'namespace': namespace,
                'status': info['status']
            })

    return sorted(capabilities, key=lambda c: c['namespace'])

# Usage
devex_caps = find_capabilities_by_domain('devex')

print(f"Found {len(devex_caps)} capabilities in 'devex' domain:\n")
for cap in devex_caps:
    print(f"- {cap['namespace']} (legacy: {cap['sap_id']})")
```

**Agent Response Template**:
```
Found 14 capabilities in the 'devex' domain:

- chora.devex.bootstrap (legacy: SAP-045)
- chora.devex.capability_server_template (legacy: SAP-047)
- chora.devex.documentation_framework (legacy: SAP-007)
- chora.devex.interface_design (legacy: SAP-043)
- chora.devex.manifest_registry (legacy: SAP-044)
- chora.devex.multi_interface (legacy: SAP-040)
- chora.devex.registry (legacy: SAP-047)
...

All legacy SAP-XXX identifiers are deprecated. Please use modern namespaces.
```

---

### Workflow 5: Generate Migration Report

**User Request**: "Show me all SAP-XXX identifiers that need migration"

**Agent Action**:

```python
import json
from collections import defaultdict

def generate_migration_report() -> dict:
    """Generate migration report by domain"""
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    by_domain = defaultdict(list)
    total = 0

    for sap_id, info in mapping['aliases'].items():
        namespace = info['namespace']

        # Extract domain
        parts = namespace.split('.')
        domain = parts[1] if len(parts) >= 3 else 'unknown'

        by_domain[domain].append({
            'sap_id': sap_id,
            'namespace': namespace
        })

        total += 1

    return {
        'total': total,
        'sunset_date': mapping['sunset_date'],
        'by_domain': dict(by_domain)
    }

# Usage
report = generate_migration_report()

print(f"Migration Report: {report['total']} capabilities")
print(f"Sunset Date: {report['sunset_date']}\n")

for domain, caps in sorted(report['by_domain'].items()):
    print(f"{domain}: {len(caps)} capabilities")
    for cap in caps:
        print(f"  - {cap['sap_id']} → {cap['namespace']}")
    print()
```

---

## Quick Reference Patterns

### Pattern: Normalize SAP-XXX Input

```python
def normalize_sap_id(input_id: str) -> str:
    """Normalize to SAP-XXX format"""
    import re

    # Extract number
    match = re.search(r'(\d+)', input_id.upper())
    if not match:
        raise ValueError(f"Invalid SAP ID: {input_id}")

    number = match.group(1).zfill(3)
    return f"SAP-{number}"

# Examples
assert normalize_sap_id("SAP-015") == "SAP-015"
assert normalize_sap_id("sap-15") == "SAP-015"
assert normalize_sap_id("15") == "SAP-015"
```

---

### Pattern: Reverse Lookup (Namespace → SAP-XXX)

```python
def reverse_lookup(namespace: str) -> str:
    """Find SAP-XXX for a modern namespace"""
    import json
    with open('capabilities/alias-mapping.json', 'r') as f:
        mapping = json.load(f)

    for sap_id, info in mapping['aliases'].items():
        if info['namespace'] == namespace:
            return sap_id

    return None

# Example
sap_id = reverse_lookup("chora.awareness.task_tracking")
print(f"chora.awareness.task_tracking → {sap_id}")  # SAP-015
```

---

### Pattern: Extract Domain from Namespace

```python
def extract_domain(namespace: str) -> str:
    """Extract domain from namespace"""
    parts = namespace.split('.')
    if len(parts) >= 3 and parts[0] == 'chora':
        return parts[1]
    return None

# Examples
assert extract_domain("chora.devex.registry") == "devex"
assert extract_domain("chora.awareness.task_tracking") == "awareness"
```

---

### Pattern: Check if Sunset Passed

```python
from datetime import datetime, date

def is_sunset_passed(sunset_date_str: str) -> bool:
    """Check if sunset date has passed"""
    sunset_date = datetime.strptime(sunset_date_str, '%Y-%m-%d').date()
    return date.today() > sunset_date

# Example
if is_sunset_passed("2026-06-01"):
    print("Legacy identifiers no longer supported")
else:
    print("Legacy identifiers still supported (transition period)")
```

---

## Common Agent Pitfalls

### Pitfall 1: Not Detecting Legacy Identifiers

**Problem**: Agent doesn't detect SAP-XXX in user input

**Impact**: Users continue using deprecated identifiers without warning

**Solution**: Always scan user input for SAP-XXX pattern

```python
# Bad: Direct use without detection
install_capability("SAP-015")

# Good: Detect and resolve first
resolved = detect_and_resolve_legacy_ids(user_input)
if resolved:
    for res in resolved:
        print(f"⚠️ {res['deprecation_warning']}")
    # Use modern namespace
    install_capability(resolved[0]['namespace'])
```

---

### Pitfall 2: Not Providing Migration Guidance

**Problem**: Agent resolves identifier but doesn't explain why it's deprecated

**Impact**: Users confused about why identifiers changed

**Solution**: Always include deprecation warning and days until sunset

```python
# Bad: Silent resolution
namespace = resolve_sap_id("SAP-015")['namespace']

# Good: Explain deprecation
result = resolve_sap_id("SAP-015")
print(f"⚠️ {result['deprecation_warning']}")
print(f"   Please update references to: {result['namespace']}")
```

---

### Pitfall 3: Not Handling Fallback

**Problem**: Agent fails when alias service is unavailable

**Impact**: Agent cannot resolve identifiers if service is down

**Solution**: Always implement fallback to local file

```python
# Bad: No fallback
result = requests.get("http://localhost:8001/api/v1/resolve/SAP-015").json()

# Good: Fallback to local file
result = resolve_with_fallback("SAP-015")
```

---

### Pitfall 4: Case Sensitivity

**Problem**: Agent fails to resolve "sap-015" vs "SAP-015"

**Impact**: Users get different results based on capitalization

**Solution**: Always normalize input to uppercase

```python
# Bad: Case-sensitive
sap_id = user_input  # "sap-015" won't match "SAP-015"

# Good: Normalize
sap_id = user_input.upper()  # "SAP-015"
```

---

## Integration with Other SAPs

### SAP-048 (Registry Discovery)

**Use Case**: Resolve legacy identifier, then query registry

```python
# 1. Resolve SAP-XXX to modern namespace
result = resolve_sap_id("SAP-015")
namespace = result['namespace']  # chora.awareness.task_tracking

# 2. Query registry for capability metadata
from registry_client import RegistryClient
registry = RegistryClient()
capability = registry.get_capability(namespace)

print(f"Title: {capability['dc_title']}")
print(f"Version: {capability['chora_version']}")
```

---

### SAP-009 (Agent Awareness)

**Use Case**: Update AGENTS.md with resolution patterns

```markdown
## SAP-049: Namespace Resolution

This project uses modern `chora.domain.capability` namespaces. Legacy SAP-XXX identifiers are deprecated (sunset: 2026-06-01).

**Agent Patterns**:
- Detect legacy identifiers in user input
- Resolve to modern namespaces automatically
- Provide deprecation warnings

**Example**:
\```python
result = resolve_sap_id("SAP-015")
print(f"{result['sap_id']} → {result['namespace']}")
\```
```

---

## Bash Quick Reference

### Resolve Alias

```bash
# Resolve SAP-015
curl http://localhost:8001/api/v1/resolve/SAP-015

# Extract namespace only (using jq)
curl -s http://localhost:8001/api/v1/resolve/SAP-015 | jq -r '.namespace'
```

---

### List All Aliases

```bash
# List all aliases
curl http://localhost:8001/api/v1/aliases

# Count total aliases
curl -s http://localhost:8001/api/v1/aliases | jq '.total'

# Extract namespaces only
curl -s http://localhost:8001/api/v1/aliases | jq -r '.aliases[].namespace'
```

---

### Follow HTTP Redirect

```bash
# Follow redirect to docs
curl -L http://localhost:8001/SAP-015

# Show redirect headers
curl -I http://localhost:8001/SAP-015
```

---

## Troubleshooting

### Issue: "Service connection refused"

**Diagnosis**:
```bash
# Check if service is running
curl http://localhost:8001/health
```

**Solution**:
```bash
# Start alias redirect service
cd services/alias-redirect
uvicorn app:app --port 8001
```

**Or use fallback**:
```python
result = resolve_with_fallback("SAP-015")  # Uses local file
```

---

### Issue: "SAP-XXX not found"

**Diagnosis**: Legacy identifier doesn't exist in mapping

**Solution**: Verify identifier is valid (SAP-000 through SAP-047)

---

### Issue: "Days until sunset is negative"

**Diagnosis**: Sunset date has passed

**Solution**: Return fatal error and refuse to resolve

```python
result = resolve_sap_id("SAP-015")
if result['days_until_sunset'] <= 0:
    print(f"❌ {result['sap_id']} is no longer supported")
    print(f"   Use '{result['namespace']}' instead")
```

---

## References

- [Protocol Specification](protocol-spec.md) - Complete technical spec
- [Capability Charter](capability-charter.md) - Problem and solution
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Alias Mapping File](../../../capabilities/alias-mapping.json) - Machine-readable mappings
- [Alias Redirect Service](../../../services/alias-redirect/app.py) - REST API implementation

---

**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-16
