# SAP-042: Interface Design Patterns - Agent Awareness Guide

**SAP ID**: SAP-042
**Quick Read Time**: 5-7 minutes
**For**: AI agents, Claude Code, autonomous developers

---

## 📖 Quick Reference

**Purpose**: Design consistent, clean interfaces (REST, CLI, gRPC, MCP) for capability servers

**Key Principle**: **Contract-first** design with **core-interface separation**

**TL;DR**:
1. Define interface contract (OpenAPI, proto, CLI spec) BEFORE coding
2. Keep core logic interface-agnostic
3. Use thin adapters to translate between protocols
4. Map errors consistently across all interfaces
5. Version explicitly (`/api/v1/`), never break backward compatibility without warning

---

## 🎯 When to Use This SAP

**Use SAP-042 when**:
- ✅ Creating a new capability server (Orchestrator, Manifest, Gateway, etc.)
- ✅ Adding new interface to existing capability (e.g., adding REST API to CLI-only tool)
- ✅ Refactoring interfaces to fix inconsistencies
- ✅ Designing error handling for multi-interface system
- ✅ Planning API versioning strategy

**Don't use SAP-042 for**:
- ❌ Internal-only functions (no external interface)
- ❌ Prototype/throwaway code
- ❌ Single-interface, single-consumer tools

---

## 🚀 Quick Start Workflow

### 1. Define Domain Concepts (5 min)

List key concepts for your capability (nouns and verbs):

**Example** (Orchestrator):
- **Nouns**: Environment, Deployment, ServiceInstance
- **Verbs**: Create, Scale, Rollback, List, Delete

**Consistency Check**: Use SAME terminology across ALL interfaces

### 2. Write Interface Contract (15-30 min)

**REST**: Create `openapi.yaml`
```yaml
paths:
  /environments/{envId}/deployments:
    post:
      summary: Create deployment
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                service: {type: string}
                replicas: {type: integer, minimum: 1}
```

**CLI**: Document commands in `cli-spec.md`
```bash
chora-orch deployment create --env <id> --service <name> --replicas <count>
```

### 3. Implement Core Logic (30-60 min)

**Core module** (interface-agnostic):
```python
# core/orchestrator.py
def create_deployment(env_id: str, config: dict) -> Deployment:
    # Validation
    if config["replicas"] < 1:
        raise ValidationError("replicas must be >= 1", field="replicas")

    # Business logic
    deployment = Deployment(...)
    return deployment_repo.create(deployment)
```

### 4. Implement Interface Adapters (15-30 min per interface)

**REST adapter**:
```python
# api/rest.py
@app.route("/environments/<env_id>/deployments", methods=["POST"])
def create_deployment_endpoint(env_id):
    data = request.get_json()
    try:
        result = orchestrator.create_deployment(env_id, data)
        return jsonify(result.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": e.message}}), 400
```

**CLI adapter**:
```python
# cli/commands.py
@click.command()
@click.option("--env", required=True)
@click.option("--service", required=True)
@click.option("--replicas", type=int, required=True)
def deployment_create(env, service, replicas):
    try:
        result = orchestrator.create_deployment(env, {"service": service, "replicas": replicas})
        click.echo(f"✓ Deployment {result.id} created")
    except ValidationError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)
```

### 5. Test Contract and Consistency (15 min)

```python
# Test REST matches OpenAPI contract
validate_response_against_openapi(response, "POST /environments/{id}/deployments")

# Test REST and CLI produce same result
assert rest_result["replicas"] == cli_result["replicas"]
```

---

## 📋 Interface Design Checklist

### Essential Tier (Must Have)

- [ ] **Domain concepts documented** (glossary of terms)
- [ ] **OpenAPI spec written** (before coding REST API)
- [ ] **CLI spec documented** (commands, flags, help text)
- [ ] **Core logic interface-agnostic** (no HTTP codes, CLI args in core)
- [ ] **Error mapping consistent** (same exception → same error code across interfaces)
- [ ] **Help documentation complete** (OpenAPI UI, `--help` text)

### Recommended Tier (Should Have)

- [ ] **Versioning strategy defined** (`/api/v1/`, deprecation warnings)
- [ ] **Correlation IDs implemented** (`X-Request-ID` header)
- [ ] **Structured logging** (JSON format with request_id)
- [ ] **Backward compatibility tests** (old clients still work after updates)
- [ ] **Consistency tests** (REST and CLI produce same results)

### Advanced Tier (Nice to Have)

- [ ] **gRPC interface** (for high-performance needs)
- [ ] **MCP integration** (for AI agent access)
- [ ] **SDK generation** (auto-generate Python/TS clients from OpenAPI)
- [ ] **Shell autocompletion** (CLI tab-completion)
- [ ] **Hypermedia links** (HATEOAS for REST APIs)

---

## 🔧 Common Patterns

### Pattern 1: Error Mapping

**Core Exception** → **REST** → **CLI** → **gRPC**

```python
# Core
class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field

# REST: HTTP 400
{"error": {"code": "VALIDATION_ERROR", "message": "replicas must be >= 1", "field": "replicas"}}

# CLI: Exit code 1
Error: Invalid deployment config: replicas must be >= 1 (field: replicas)

# gRPC: INVALID_ARGUMENT
context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
context.set_details("replicas must be >= 1")
```

### Pattern 2: Core-Interface Separation

```
┌─────────────────────────────┐
│   REST    CLI    gRPC   MCP │ ← Thin adapters (parse, translate)
└──────────────┬──────────────┘
               │
         ┌─────▼─────┐
         │   Core    │ ← Business logic (interface-agnostic)
         └───────────┘
```

**Key Rule**: Core never imports Flask, Click, grpc, or any interface framework

### Pattern 3: Consistent Naming

| Concept | REST | CLI | Docs | Logs |
|---------|------|-----|------|------|
| Create deployment | `POST /deployments` | `deployment create` | "create deployment" | "Creating deployment" |
| Replica count | `replicas` field | `--replicas` flag | "replicas" | `replicas=3` |
| Environment | `/environments/{envId}` | `--env <id>` | "environment" | `env_id=prod` |

**Anti-Pattern**: REST calls it "instances", CLI calls it "replicas" ❌

### Pattern 4: Observability

**Request Flow with Correlation ID**:
```
Client Request (X-Request-ID: 3f8e9a7b)
    ↓
REST API (log: "Request 3f8e9a7b: POST /deployments")
    ↓
Core Logic (log: "Request 3f8e9a7b: Validating config")
    ↓
Manifest Call (header: X-Request-ID: 3f8e9a7b)
    ↓
Response (header: X-Request-ID: 3f8e9a7b)
```

### Pattern 5: Versioning

**REST API**: `/api/v1/` in URL
```
/api/v1/deployments  ← Version 1
/api/v2/deployments  ← Version 2 (breaking changes)
```

**gRPC**: Package versioning
```protobuf
package chora.orchestrator.v1;  // Version 1
package chora.orchestrator.v2;  // Version 2
```

**CLI**: Deprecation warnings
```
Warning: --count is deprecated, use --replicas instead
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Leaking Implementation Details

**Bad**:
```json
POST /deployments
{"docker_image": "nginx", "docker_network": "bridge"}
```
→ Locks interface to Docker, can't switch to Kubernetes without breaking

**Good**:
```json
POST /deployments
{"container_image": "nginx", "network_mode": "default"}
```
→ Abstract container runtime, internal implementation can change

### Pitfall 2: Inconsistent Errors

**Bad**:
- REST: `{"error": "Internal server error"}` (generic)
- CLI: `Traceback (most recent call last)...` (stack trace)
- Different messages for same error condition ❌

**Good**:
- REST: `{"error": {"code": "VALIDATION_ERROR", "message": "replicas must be >= 1"}}`
- CLI: `Error: Invalid config: replicas must be >= 1`
- Same core message, consistently translated ✅

### Pitfall 3: Business Logic in Interface Layer

**Bad**:
```python
# api/rest.py
@app.route("/deployments", methods=["POST"])
def create_deployment():
    data = request.get_json()
    if data["replicas"] < 1:  # ❌ Validation in interface layer
        return jsonify({"error": "Invalid replicas"}), 400
    # ... create deployment
```

**Good**:
```python
# core/orchestrator.py
def create_deployment(config):
    if config["replicas"] < 1:  # ✅ Validation in core
        raise ValidationError("replicas must be >= 1", field="replicas")
    # ... create deployment

# api/rest.py
@app.route("/deployments", methods=["POST"])
def create_deployment():
    try:
        result = orchestrator.create_deployment(request.get_json())  # ✅ Thin adapter
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": {"message": e.message}}), 400
```

### Pitfall 4: Code-First (No Contract)

**Bad Workflow**:
1. Write Flask routes
2. Implement logic
3. *"TODO: write docs later"*
4. Docs never written or lag reality ❌

**Good Workflow** (Contract-First):
1. Write OpenAPI spec
2. Review with team
3. Generate stubs from spec
4. Implement logic
5. Validate against spec ✅

---

## 🤖 AI Agent Integration Notes

**For AI Agents** reading this SAP:

1. **Prefer JSON Output**: When calling CLI, use `--json` flag for parseable output
   ```bash
   chora-orch deployment list --env prod --json
   ```

2. **Check Error Codes**: Look for structured error codes, not just HTTP status
   ```json
   {"error": {"code": "VALIDATION_ERROR", "message": "...", "field": "replicas"}}
   ```

3. **Use Correlation IDs**: Include `X-Request-ID` in requests for tracing
   ```python
   headers = {"X-Request-ID": str(uuid.uuid4())}
   ```

4. **Respect Versioning**: Pin to specific API version for stability
   ```
   /api/v1/deployments  ← Stable
   ```

5. **Expect Consistent Terms**: Same concept uses same name across interfaces
   - If REST says "replicas", CLI will say `--replicas`

---

## 📚 Code Examples

### Example 1: Complete Interface Implementation

See [protocol-spec.md](./protocol-spec.md) for:
- Full OpenAPI specification
- gRPC proto definition
- CLI command documentation
- Error handling code examples
- Observability patterns

### Example 2: Quick Decision Tree

**Question**: Which interface types should I implement?

```
Do you need service-to-service communication?
├─ Yes → Implement REST API (Essential)
└─ No → Skip to CLI

Do humans need to operate the service?
├─ Yes → Implement CLI (Essential)
└─ No → API-only is fine

Do you need high-performance streaming?
├─ Yes → Consider gRPC (Advanced)
└─ No → REST is sufficient

Do AI agents need direct access?
├─ Yes → Integrate with MCP Gateway (Recommended)
└─ No → Agents can use REST via Gateway
```

---

## 🔗 Related SAPs

**Directly Related**:
- **SAP-043** (multi-interface): Implements core + adapters pattern using SAP-042 principles
- **SAP-044** (registry): Manifest API designed following SAP-042 patterns
- **SAP-047** (template): Scaffolding tool generates interfaces using SAP-042 patterns

**Foundation**:
- **SAP-000** (sap-framework): Provides 5-artifact structure for this SAP

---

## 📊 Adoption Metrics

**Essential Tier Success** (1-2 weeks adoption):
- OpenAPI spec exists before REST implementation
- CLI spec documented with all commands
- Core logic has 0 imports of Flask/Click/grpc
- Error mapping table documented and implemented

**Recommended Tier Success** (2-4 weeks adoption):
- All APIs versioned (`/api/v1/`)
- Correlation IDs in 100% of requests
- Consistency tests passing (REST == CLI results)
- Structured logging (JSON format)

**Advanced Tier Success** (4-8 weeks adoption):
- gRPC interface implemented
- MCP integration via Gateway
- SDK auto-generated from specs
- Shell autocompletion working

---

## 🆘 Getting Help

**Questions?**
1. Read [capability-charter.md](./capability-charter.md) - Problem statement and solution design
2. Read [protocol-spec.md](./protocol-spec.md) - Complete technical specification
3. Follow [adoption-blueprint.md](./adoption-blueprint.md) - Step-by-step guide
4. Check [ledger.md](./ledger.md) - Adoption examples and feedback

**Common Questions**:

**Q**: Do I need ALL interface types (REST, CLI, gRPC, MCP)?
**A**: No. Essential tier = REST + CLI. gRPC and MCP are optional (Advanced tier).

**Q**: Can I do code-first instead of contract-first?
**A**: Not recommended. Contract-first prevents interface drift and enables collaboration. If rapid prototyping, write contract after first iteration.

**Q**: How do I handle async operations (long-running tasks)?
**A**: Return operation ID immediately, provide status endpoint for polling. Example:
```
POST /deployments → {"operation_id": "op-123", "status": "in_progress"}
GET /operations/op-123 → {"status": "completed", "result": {...}}
```

**Q**: What if I need to break backward compatibility?
**A**: Increment major version (`/api/v2/`), support v1 for ≥6 months, provide migration guide.

---

## ✅ Success Criteria Summary

**You've successfully adopted SAP-042 when**:

Essential:
- [ ] Interface contracts written before implementation
- [ ] Same terminology across all interfaces
- [ ] Core logic is interface-agnostic
- [ ] Errors map consistently (REST 400 = CLI exit 1)

Recommended:
- [ ] APIs versioned explicitly
- [ ] Correlation IDs in all requests
- [ ] Backward compatibility maintained
- [ ] Consistency tests passing

Advanced:
- [ ] gRPC/MCP interfaces implemented
- [ ] SDKs auto-generated
- [ ] Shell autocompletion working

---

**Next Steps**:
1. Read [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step implementation
2. Use checklist above to track progress
3. Log adoption in [ledger.md](./ledger.md)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Feedback**: Submit to ledger.md or via SAP-019 self-evaluation
