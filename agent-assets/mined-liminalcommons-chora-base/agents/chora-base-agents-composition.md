# SAP-046: Composition - Agent Quick Reference

**SAP ID**: SAP-046
**Name**: Composition
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This quick reference guide helps AI agents (Claude Code, Claude Desktop, etc.) work with SAP-046 (Composition) patterns for orchestrating multiple capability servers into reliable workflows.

**Core Principle**: "Orchestrate what you control, choreograph what you don't."

---

## 📖 Quick Reference

### When to Use This SAP

**Use SAP-046 when you need to**:
- Orchestrate multi-step workflows across multiple services (environment deployment, data pipelines)
- Implement distributed transactions with rollback capability (Saga pattern)
- Prevent cascading failures between services (circuit breakers)
- Manage service dependencies and startup ordering
- Ensure idempotent operations for retries
- Coordinate event-driven interactions (pub/sub messaging)

**Don't use SAP-046 for**:
- Single-service operations (no composition needed)
- Simple sequential scripts (use shell scripts instead)
- Synchronous request-response calls without failure handling (use direct HTTP calls)

---

## 🚀 5-Minute Quick Start

### 1. Install Dependencies

```bash
pip install chora-compose[composition]  # Includes saga, event bus, circuit breaker
```

### 2. Create Configuration

Create `composition.yaml`:

```yaml
version: "1.0"

sagas:
  definitions_file: "saga_definitions.yaml"
  persistence:
    backend: "sqlite"
    connection_string: "saga_state.db"

event_bus:
  backend: "memory"  # Use "redis" in production

circuit_breakers:
  definitions_file: "circuit_breakers.yaml"
```

### 3. Define a Saga

Create `saga_definitions.yaml`:

```yaml
sagas:
  deploy_environment:
    name: "Deploy Environment"
    timeout: 600
    steps:
      - id: "register_manifest"
        service: "manifest"
        operation: "register"
        timeout: 30
        compensation: "deregister"
        idempotent: true

      - id: "deploy_containers"
        service: "container-engine"
        operation: "deploy"
        timeout: 120
        compensation: "stop"
        idempotent: true
        depends_on: ["register_manifest"]

      - id: "configure_gateway"
        service: "gateway"
        operation: "add_routes"
        timeout: 30
        compensation: "remove_routes"
        idempotent: true
        depends_on: ["deploy_containers"]
```

### 4. Execute Saga

```python
from chora_compose.composition import SagaOrchestrator

orchestrator = SagaOrchestrator(
    definitions_file="saga_definitions.yaml",
    persistence_backend="sqlite"
)

saga_instance = await orchestrator.execute(
    saga_name="deploy_environment",
    input_data={
        "environment_id": "env_prod_001",
        "services": [...]
    }
)

print(f"Saga started: {saga_instance.id}")
```

### 5. Check Status

```bash
chora-compose saga status saga_abc123
```

**You now have**:
- Saga orchestration with automatic rollback
- Event bus for pub/sub messaging
- Circuit breakers for fault tolerance
- Dependency resolution for service ordering

---

## 🎯 Common Workflows

### Workflow 1: Orchestrate Multi-Step Deployment

**Scenario**: Deploy environment with manifest registration → container deployment → gateway configuration.

**Implementation**:

```python
# Define saga (saga_definitions.yaml)
sagas:
  deploy_environment:
    steps:
      - id: "register_manifest"
        service: "manifest"
        operation: "register"
        compensation: "deregister"

      - id: "deploy_containers"
        service: "container-engine"
        operation: "deploy"
        compensation: "stop"
        depends_on: ["register_manifest"]

      - id: "configure_gateway"
        service: "gateway"
        operation: "add_routes"
        compensation: "remove_routes"
        depends_on: ["deploy_containers"]

# Execute saga
orchestrator = SagaOrchestrator(definitions_file="saga_definitions.yaml")
saga_instance = await orchestrator.execute("deploy_environment", input_data={...})

# If any step fails, compensation automatically runs in reverse order
```

**Key Points**:
- Steps execute sequentially (respecting `depends_on`)
- If step fails, compensation runs in reverse order (gateway → containers → manifest)
- Each operation MUST be idempotent

---

### Workflow 2: Implement Circuit Breaker for Service Calls

**Scenario**: Protect analyzer service from cascading failures.

**Implementation**:

```python
from chora_compose.composition import CircuitBreaker

# Initialize circuit breaker
analyzer_cb = CircuitBreaker(
    name="analyzer_service",
    failure_threshold=5,  # Open after 5 failures
    timeout=30,           # Wait 30s before retry
    success_threshold=3   # Close after 3 successes in half-open
)

# Call service through circuit breaker
try:
    result = await analyzer_cb.call(
        analyzer_client.analyze,
        prompt="Analyze this code..."
    )
except CircuitOpenError:
    # Circuit open, use fallback
    logger.warning("Analyzer unavailable, using cached result")
    result = get_cached_result()
```

**States**:
- **Closed**: Normal operation, requests pass through
- **Open**: Service unavailable, requests fail immediately (no cascading)
- **Half-Open**: Testing recovery, allow limited requests

---

### Workflow 3: Publish and Subscribe to Events

**Scenario**: Notify logging service when environment is deployed (choreography pattern).

**Implementation**:

**Publisher** (Orchestrator):

```python
from chora_compose.composition import EventBus

event_bus = EventBus(backend="redis")

# Publish event after deployment
await event_bus.publish(
    type="environment.lifecycle.created",
    source="orchestrator",
    data={
        "environment_id": "env_prod_001",
        "services": ["analyzer", "executor"]
    },
    metadata={"trace_id": "trace_xyz789"}
)
```

**Subscriber** (Logging Service):

```python
# Subscribe to environment events
async def handle_environment_created(event):
    logger.info(f"Environment created: {event.data['environment_id']}")
    # Log to central logging system

await event_bus.subscribe(
    channels=["environment.lifecycle.*"],
    handler=handle_environment_created
)
```

**Key Points**:
- Use pub/sub for cross-cutting concerns (logging, monitoring, notifications)
- Subscribers are decoupled from publishers (no tight coupling)
- Events follow CloudEvents standard

---

### Workflow 4: Resolve Service Dependencies

**Scenario**: Determine startup order for services with dependencies.

**Implementation**:

```bash
# Define dependencies in manifest.yaml (per service)
service:
  name: "executor"
  dependencies:
    - name: "analyzer"
      version: ">=1.2.0"
      required: true
    - name: "storage"
      version: ">=2.0.0"
      required: true

# Resolve dependencies (topological sort)
chora-compose deps resolve --manifest services/*/manifest.yaml

# Output (startup order):
# 1. analyzer (no dependencies)
# 2. storage (no dependencies)
# 3. executor (depends on: analyzer, storage)
```

**Python API**:

```python
from chora_compose.composition import DependencyResolver

resolver = DependencyResolver()

# Resolve dependencies
sorted_services = resolver.resolve(services)

# Validate (raises CircularDependencyError if cycle detected)
resolver.validate(services)
```

---

### Workflow 5: Retry with Exponential Backoff

**Scenario**: Retry analyzer call with exponential backoff on transient failures.

**Implementation**:

```python
from chora_compose.composition import retry

@retry(
    max_attempts=5,
    initial_delay=1,  # 1s, 2s, 4s, 8s, 16s
    backoff_factor=2,
    retryable_errors=(ConnectionError, TimeoutError)
)
async def call_analyzer(prompt: str) -> str:
    """Call analyzer service (with automatic retry)."""
    response = await http_client.post(
        "http://analyzer:8080/analyze",
        json={"prompt": prompt}
    )
    return response.json()["result"]

# Usage (retry is transparent)
result = await call_analyzer("Analyze this code...")
```

**Retry Delays**:
- Attempt 1: 0s (immediate)
- Attempt 2: 1s
- Attempt 3: 2s
- Attempt 4: 4s
- Attempt 5: 8s

---

### Workflow 6: Implement Idempotency with Request IDs

**Scenario**: Ensure environment deployment can be retried safely.

**Implementation**:

**Server** (Orchestrator):

```python
from chora_compose.composition import idempotent_handler

@app.post("/api/v1/environments/deploy")
@idempotent_handler  # Automatically handles X-Idempotency-Key
async def deploy_environment(request):
    env_id = request.json["environment_id"]
    # Deploy environment (safe to call multiple times)
    return {"status": "success", "env_id": env_id}
```

**Client**:

```python
import uuid

# Generate idempotency key
idempotency_key = str(uuid.uuid4())

# Make request with idempotency key
response = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001"},
    headers={"X-Idempotency-Key": idempotency_key}
)

# Retry (safe, will return same response)
response2 = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={"environment_id": "env_prod_001"},
    headers={"X-Idempotency-Key": idempotency_key}  # Same key
)

assert response == response2  # Guaranteed same response
```

---

## 🔧 CLI Commands

### Saga Management

```bash
# Execute saga
chora-compose saga execute deploy_environment \
  --input '{"environment_id":"env_prod_001","services":[...]}' \
  --timeout 600

# Get saga status
chora-compose saga status saga_abc123

# Cancel saga (with rollback)
chora-compose saga cancel saga_abc123 --compensate

# List running sagas
chora-compose saga list --state running

# Saga history
chora-compose saga history --saga-name deploy_environment --days 7
```

### Event Bus

```bash
# Publish event
chora-compose events publish \
  --type environment.lifecycle.created \
  --source orchestrator \
  --data '{"environment_id":"env_prod_001"}'

# Subscribe to events (blocks, prints events)
chora-compose events subscribe --channels "environment.*,saga.*"

# View event log
chora-compose events log --tail 100 --follow
```

### Circuit Breakers

```bash
# List circuit breakers
chora-compose circuit-breaker list

# Get status
chora-compose circuit-breaker status analyzer_service

# Reset (manually close)
chora-compose circuit-breaker reset analyzer_service --force-state closed
```

### Dependencies

```bash
# Resolve dependencies (show startup order)
chora-compose deps resolve --manifest services/*/manifest.yaml

# Validate (check for circular dependencies)
chora-compose deps validate --manifest services/*/manifest.yaml

# Generate dependency graph (DOT format)
chora-compose deps graph --output deps.dot --format dot
```

---

## 🎨 Patterns & Best Practices

### Pattern 1: Orchestrate What You Control, Choreograph What You Don't

**Orchestration** (Central Control):
- Use for multi-step workflows YOU control (environment deployment)
- Saga pattern with compensation
- Explicit sequencing (step 1 → step 2 → step 3)

**Choreography** (Event-Driven):
- Use for cross-cutting concerns (logging, monitoring, notifications)
- Pub/sub messaging
- Services react independently to events

**Example**:

```python
# Orchestration: Deploy environment (you control the workflow)
saga = await orchestrator.execute("deploy_environment", {...})

# Choreography: Notify logging service (logging reacts to event)
await event_bus.publish("environment.lifecycle.created", {...})
```

---

### Pattern 2: All Operations MUST Be Idempotent

**Guideline**: Design operations so calling them multiple times has the same effect as calling once.

**Idempotent Operations**:
```python
# ✅ Idempotent: Setting value to X
PUT /api/v1/config/max_workers
{"value": 4}

# ✅ Idempotent: Deleting resource
DELETE /api/v1/environments/env_prod_001

# ✅ Idempotent: Deploying with same config
POST /api/v1/containers/deploy
{"name": "analyzer", "image": "chora/analyzer:1.2.0"}
# If container exists with same image, return existing
```

**Non-Idempotent Operations** (Avoid):
```python
# ❌ NOT idempotent: Incrementing counter
POST /api/v1/metrics/increment
{"metric": "request_count"}

# Fix: Use idempotent "set" operation
PUT /api/v1/metrics/request_count
{"value": 42}
```

---

### Pattern 3: Compensations Run in Reverse Order

**Guideline**: When a saga fails, compensations execute in reverse order of completed steps.

**Example**:

```python
# Saga steps:
# 1. register_manifest ✅ (completed)
# 2. deploy_containers ✅ (completed)
# 3. configure_gateway ❌ (failed)

# Compensations (reverse order):
# 1. compensate deploy_containers (stop containers)
# 2. compensate register_manifest (deregister)
# 3. (configure_gateway never ran, no compensation needed)
```

**Best Practice**: Write compensations that are also idempotent.

---

### Pattern 4: Circuit Breakers Prevent Cascading Failures

**Guideline**: Wrap all external service calls in circuit breakers.

**Anti-Pattern**:
```python
# ❌ No circuit breaker: One slow service brings down entire system
result = await analyzer_client.analyze(prompt)  # Hangs if analyzer is slow
```

**Best Practice**:
```python
# ✅ Circuit breaker: Fail fast if analyzer is unavailable
cb = CircuitBreaker("analyzer_service", failure_threshold=5, timeout=30)
try:
    result = await cb.call(analyzer_client.analyze, prompt)
except CircuitOpenError:
    # Use fallback (cached result, default response, or queue for later)
    result = get_cached_result()
```

---

### Pattern 5: Use Request IDs for Idempotency

**Guideline**: Include `X-Idempotency-Key` header for non-idempotent operations.

**Example**:

```python
import uuid

# Generate unique key (or hash of request data)
idempotency_key = str(uuid.uuid4())

# Include in request
response = await http_client.post(
    "http://orchestrator:8080/api/v1/environments/deploy",
    json={...},
    headers={"X-Idempotency-Key": idempotency_key}
)

# Server caches response by key, safe to retry
```

---

### Pattern 6: Validate Dependencies Before Deployment

**Guideline**: Resolve and validate service dependencies before starting deployment.

**Example**:

```python
from chora_compose.composition import DependencyResolver

resolver = DependencyResolver()

# Validate dependencies
try:
    sorted_services = resolver.resolve(services)
except CircularDependencyError as e:
    logger.error(f"Circular dependency detected: {e}")
    return {"error": "Cannot deploy due to circular dependency"}

# Deploy in dependency order
for service in sorted_services:
    await deploy_service(service)
```

---

### Pattern 7: Use CloudEvents Standard for Events

**Guideline**: Follow CloudEvents 1.0 specification for event format.

**Event Structure**:

```json
{
  "specversion": "1.0",
  "type": "environment.lifecycle.created",
  "source": "orchestrator",
  "id": "evt_abc123",
  "time": "2025-11-12T10:15:00Z",
  "data": {
    "environment_id": "env_prod_001",
    "services": ["analyzer", "executor"]
  },
  "traceparent": "00-trace_xyz789-span_123-01"
}
```

**Benefits**:
- Standard format (interoperable with other systems)
- Includes tracing context (traceparent)
- Supports schema validation

---

## ⚠️ Common Pitfalls

### Pitfall 1: Not Implementing Compensation Logic

**Problem**: Saga steps have no compensation, leaving system in inconsistent state on failure.

**Fix**: Every Saga step MUST have a compensation operation.

```yaml
# ❌ Bad: No compensation
steps:
  - id: "deploy_containers"
    service: "container-engine"
    operation: "deploy"

# ✅ Good: With compensation
steps:
  - id: "deploy_containers"
    service: "container-engine"
    operation: "deploy"
    compensation: "stop"  # Rollback operation
```

---

### Pitfall 2: Non-Idempotent Operations in Saga Steps

**Problem**: Retrying non-idempotent operations causes duplicate effects.

**Example**:
```python
# ❌ Bad: Incrementing counter (non-idempotent)
async def increment_deployment_count():
    count = await db.get_count()
    await db.set_count(count + 1)  # Retry causes double increment
```

**Fix**: Make operations idempotent.

```python
# ✅ Good: Set to specific value (idempotent)
async def set_deployment_timestamp(env_id: str):
    timestamp = datetime.utcnow()
    await db.set_timestamp(env_id, timestamp)  # Safe to retry
```

---

### Pitfall 3: Ignoring Circuit Breaker State

**Problem**: Continuing to call service even when circuit is open.

**Example**:
```python
# ❌ Bad: Ignoring circuit breaker
try:
    result = await cb.call(analyzer_client.analyze, prompt)
except CircuitOpenError:
    # Still try to call analyzer directly (defeats circuit breaker)
    result = await analyzer_client.analyze(prompt)
```

**Fix**: Respect circuit breaker state, use fallback.

```python
# ✅ Good: Use fallback when circuit open
try:
    result = await cb.call(analyzer_client.analyze, prompt)
except CircuitOpenError:
    # Use cached result or default
    result = get_cached_result()
```

---

### Pitfall 4: Not Resolving Dependencies Before Deployment

**Problem**: Deploying services in wrong order causes failures.

**Example**:
```python
# ❌ Bad: Deploy executor before analyzer (dependency missing)
await deploy_service("executor")  # Fails: analyzer not available
await deploy_service("analyzer")
```

**Fix**: Resolve dependencies first, deploy in order.

```python
# ✅ Good: Resolve dependencies, deploy in order
sorted_services = resolver.resolve([executor, analyzer])
for service in sorted_services:  # analyzer → executor
    await deploy_service(service)
```

---

### Pitfall 5: No Timeout for Saga Execution

**Problem**: Saga runs indefinitely if step hangs.

**Fix**: Always set timeout for sagas and steps.

```yaml
sagas:
  deploy_environment:
    timeout: 600  # Saga-level timeout (10 minutes)
    steps:
      - id: "deploy_containers"
        timeout: 120  # Step-level timeout (2 minutes)
```

---

### Pitfall 6: Not Using Distributed Tracing

**Problem**: Cannot correlate saga steps with logs/metrics.

**Fix**: Propagate trace context (W3C Trace Context).

```python
# Include traceparent header in all service calls
response = await http_client.post(
    "http://analyzer:8080/analyze",
    json={...},
    headers={
        "traceparent": f"00-{trace_id}-{span_id}-01"
    }
)
```

---

## 🔗 Integration with Other SAPs

### SAP-042 (InterfaceDesign)

**Integration**: Composition uses standardized capability interfaces.

**Pattern**: Saga steps call capabilities via interfaces defined in SAP-042.

```python
# Saga step calls capability through interface
manifest_client = CapabilityClient("manifest", interface_version="1.0")
result = await manifest_client.call("register", service_config)
```

---

### SAP-044 (Registry)

**Integration**: Composition queries Manifest Registry for service discovery.

**Pattern**: Circuit breaker discovers service endpoints from registry.

```python
# Discover service from registry
analyzer_url = await registry.discover("analyzer", version=">=1.2.0")
cb = CircuitBreaker("analyzer", url=analyzer_url)
```

---

### SAP-045 (Bootstrap)

**Integration**: Bootstrap uses Composition for phased deployment orchestration.

**Pattern**: Bootstrap phases are implemented as Sagas.

```yaml
# bootstrap_saga.yaml
sagas:
  bootstrap_phase_1:
    steps:
      - deploy_manifest_registry
      - wait_for_manifest_health
```

---

### SAP-010 (A-MEM)

**Integration**: Composition emits events to A-MEM for audit/replay.

**Pattern**: Saga events are recorded in A-MEM.

```python
# Saga execution generates A-MEM events
await amem.record_event({
    "type": "saga.execution.started",
    "saga_instance_id": "saga_abc123"
})
```

---

### SAP-015 (Beads Task Tracking)

**Integration**: Composition sagas can be managed via Beads tasks.

**Pattern**: Create bead for saga execution.

```bash
bd create "Execute deploy_environment saga" \
  --epic "Environment Deployment" \
  --meta '{"saga":"deploy_environment","env":"prod"}'
```

---

## 📊 Success Criteria

**Adoption is successful when**:
- ✅ 100% of Sagas have compensation logic defined
- ✅ All services declare dependencies in manifest
- ✅ All inter-service calls are idempotent
- ✅ ≥95% Saga success rate (failure rate <5%)
- ✅ <4 hours integration time (75% faster than ad-hoc integration)
- ✅ Circuit breakers prevent >90% of cascading failures
- ✅ Dependency resolution catches 100% of circular dependencies

---

## 📚 Additional Resources

**Detailed Documentation**:
- [capability-charter.md](capability-charter.md) - Problem statement, solution design, ROI
- [protocol-spec.md](protocol-spec.md) - Complete technical specification
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step installation guide
- [ledger.md](ledger.md) - Adoption tracking, metrics, feedback

**Related SAPs**:
- SAP-042 (InterfaceDesign) - Capability interface patterns
- SAP-043 (MultiInterface) - Multi-protocol support
- SAP-044 (Registry) - Service discovery and health
- SAP-045 (Bootstrap) - Phased deployment orchestration
- SAP-010 (A-MEM) - Event-sourced memory
- SAP-015 (Beads) - Task tracking

**Standards**:
- CloudEvents 1.0: https://cloudevents.io/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- Saga Pattern: https://microservices.io/patterns/data/saga.html
- Circuit Breaker: https://martinfowler.com/bliki/CircuitBreaker.html

---

## 🆘 Troubleshooting

### Issue 1: Saga Stuck in "running" State

**Symptom**: Saga status shows "running" for hours, no progress.

**Diagnosis**:
```bash
chora-compose saga status saga_abc123
# Check current_step and last update time
```

**Fix**:
```bash
# Cancel saga (with compensation)
chora-compose saga cancel saga_abc123 --compensate
```

---

### Issue 2: Circuit Breaker Always Open

**Symptom**: Circuit breaker never closes, all requests fail.

**Diagnosis**:
```bash
chora-compose circuit-breaker status analyzer_service
# Check failure_count, last_failure_time
```

**Fix**:
```bash
# Manually reset circuit breaker
chora-compose circuit-breaker reset analyzer_service --force-state closed
```

---

### Issue 3: Circular Dependency Error

**Symptom**: Dependency resolution fails with circular dependency error.

**Diagnosis**:
```bash
chora-compose deps validate --manifest services/*/manifest.yaml
# Error: Circular dependency detected involving: [executor, analyzer]
```

**Fix**: Remove circular dependency from manifest files.

```yaml
# Before: executor → analyzer → executor (circular)
# After: executor → analyzer (no circular)
```

---

### Issue 4: Event Not Delivered

**Symptom**: Published event never reaches subscriber.

**Diagnosis**:
```bash
# Check event log
chora-compose events log --tail 100 | grep "environment.lifecycle.created"

# Check subscriber is running
ps aux | grep "chora-compose events subscribe"
```

**Fix**:
```bash
# Restart subscriber with correct channels
chora-compose events subscribe --channels "environment.lifecycle.*"
```

---

## 🎓 Learning Path

**Beginner** (1-2 hours):
1. Read this AGENTS.md file (quick reference)
2. Follow 5-Minute Quick Start
3. Implement Workflow 1 (multi-step deployment)
4. Implement Workflow 2 (circuit breaker)

**Intermediate** (4-6 hours):
1. Read [protocol-spec.md](protocol-spec.md) (complete specification)
2. Implement Workflow 3 (pub/sub events)
3. Implement Workflow 4 (dependency resolution)
4. Read [adoption-blueprint.md](adoption-blueprint.md) (implementation guide)

**Advanced** (8-12 hours):
1. Read [capability-charter.md](capability-charter.md) (design rationale)
2. Implement all 6 common workflows
3. Integrate with SAP-045 (Bootstrap)
4. Configure monitoring (Prometheus, OpenTelemetry)

---

**Document Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12
