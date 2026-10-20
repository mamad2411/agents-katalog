# SAP-043: Multi-Interface Capability Servers - Agent Awareness Guide

**SAP ID**: SAP-043
**Quick Read Time**: 7-9 minutes
**For**: AI agents, Claude Code, autonomous developers

---

## 📖 Quick Reference

**Purpose**: Build capability servers with 4 standardized interfaces (Native API, CLI, REST, MCP)

**Key Principle**: **Core + Adapters** - implement business logic once, expose via thin interface adapters

**TL;DR**:
1. Implement core logic in interface-agnostic module (no Flask/Click/FastMCP imports)
2. Create thin adapters for each interface (Native, CLI, REST, MCP)
3. Adapters parse inputs, call core, format outputs (no business logic)
4. Core exceptions → interface-specific errors (HTTP 400, CLI exit 1, MCP ValueError)
5. Consistency tests verify all interfaces produce identical results

**Time Savings**: 75% faster vs implementing 4 interfaces independently (1 week vs 4 weeks)

---

## 🎯 When to Use This SAP

**Use SAP-043 when**:
- ✅ Building a capability server (Orchestrator, Manifest, Gateway, etc.)
- ✅ User asks for "multi-interface support" or "CLI + API + MCP"
- ✅ Need consistency across multiple access methods
- ✅ Want to avoid duplicating business logic
- ✅ Adding interfaces to existing capability server

**Don't use SAP-043 for**:
- ❌ Single-interface tool (e.g., CLI-only script)
- ❌ Prototype/throwaway code
- ❌ Non-Python projects (this SAP is Python-specific)
- ❌ When interfaces have fundamentally different operations (not same capability)

---

## 🚀 Quick Start Workflow

### Step 1: Implement Core Module (30-60 min)

**Goal**: Interface-agnostic business logic

```python
# core/service.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class Deployment:
    env_id: str
    service: str
    replicas: int
    deployment_id: str = ""

class ValidationError(Exception):
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field

class OrchestratorService:
    def create_deployment(self, env_id: str, config: Dict[str, Any]) -> Deployment:
        """Core business logic (no interface dependencies)."""
        # Validate
        if config["replicas"] < 1:
            raise ValidationError("replicas must be >= 1", field="replicas")

        # Business logic
        deployment = Deployment(
            env_id=env_id,
            service=config["service"],
            replicas=config["replicas"],
            deployment_id=f"deploy-{generate_id()}"
        )

        # Persist
        repository.create(deployment)
        return deployment
```

**Key Rules**:
- ✅ No Flask, Click, FastAPI, FastMCP imports
- ✅ Use dict/list/dataclass (not Request/Response objects)
- ✅ Define domain exceptions (not HTTP exceptions)
- ✅ Testable without any interface framework

### Step 2: Add Native API Adapter (5 min)

**Goal**: Re-export core for programmatic use

```python
# api/native.py or __init__.py
from core.service import OrchestratorService, Deployment, ValidationError

__all__ = ["OrchestratorService", "Deployment", "ValidationError"]

# Usage:
# from orchestrator import OrchestratorService
# service = OrchestratorService()
# deployment = service.create_deployment("prod", {"service": "web", "replicas": 3})
```

### Step 3: Add CLI Adapter (15-30 min)

**Goal**: Parse CLI args, call core, format terminal output

```python
# api/cli.py
import click, sys
from core.service import OrchestratorService, ValidationError

service = OrchestratorService()

@click.command()
@click.option("--env", required=True)
@click.option("--service", required=True)
@click.option("--replicas", type=int, required=True)
def create(env, service, replicas):
    """Create deployment."""
    try:
        # ✅ Parse → core call → format
        deployment = service.create_deployment(
            env_id=env,
            config={"service": service, "replicas": replicas}
        )
        click.echo(f"✓ Deployment {deployment.deployment_id} created")
    except ValidationError as e:
        click.echo(f"Error: {e.message}", err=True)
        sys.exit(1)
```

### Step 4: Add REST API Adapter (15-30 min)

**Goal**: Parse JSON, call core, return JSON + HTTP status

```python
# api/http.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.service import OrchestratorService, ValidationError

app = FastAPI()
service = OrchestratorService()

class CreateRequest(BaseModel):
    service: str
    replicas: int

@app.post("/api/v1/environments/{env_id}/deployments", status_code=201)
def create_deployment(env_id: str, request: CreateRequest):
    """Create deployment."""
    try:
        # ✅ Parse JSON → core call → format JSON
        deployment = service.create_deployment(
            env_id=env_id,
            config=request.model_dump()
        )
        return deployment.to_dict()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
```

### Step 5: Add MCP Adapter (15-30 min)

**Goal**: Define MCP tools, call core, return JSON

```python
# api/mcp.py
from fastmcp import FastMCP
from core.service import OrchestratorService, ValidationError

mcp = FastMCP("Orchestrator")
service = OrchestratorService()

@mcp.tool()
def create_deployment(env_id: str, service_name: str, replicas: int) -> dict:
    """Create deployment (MCP tool for AI assistants).

    Args:
        env_id: Environment ID
        service_name: Service to deploy
        replicas: Replica count (>=1)

    Returns:
        Deployment details
    """
    try:
        # ✅ Parse MCP args → core call → format JSON
        deployment = service.create_deployment(
            env_id=env_id,
            config={"service": service_name, "replicas": replicas}
        )
        return {"status": "created", "deployment": deployment.to_dict()}
    except ValidationError as e:
        raise ValueError(f"{e.message} (field: {e.field})")

if __name__ == "__main__":
    mcp.run()
```

### Step 6: Add Consistency Tests (15 min)

**Goal**: Verify all interfaces produce identical results

```python
# tests/test_consistency.py
def test_create_deployment_consistency():
    """All 4 interfaces should produce same deployment."""
    # Core
    core_result = OrchestratorService().create_deployment(
        "prod", {"service": "web", "replicas": 3}
    )

    # CLI (mocked)
    # cli_result = ...

    # REST (mocked)
    # rest_result = ...

    # MCP
    mcp_result = create_deployment(
        env_id="prod", service_name="web", replicas=3
    )

    # Assert consistency
    assert core_result.service == "web"
    assert core_result.replicas == 3
    assert mcp_result["deployment"]["replicas"] == 3
```

**Total Time**: 1.5-3 hours for all 4 interfaces + tests

---

## 📋 Multi-Interface Implementation Checklist

### Essential Tier (Must Have)

- [ ] **Core module exists** (core/service.py or core/__init__.py)
- [ ] **Core has zero interface imports** (no Flask, Click, FastMCP)
- [ ] **Domain exceptions defined** (ValidationError, NotFoundError, etc.)
- [ ] **Native API adapter** (re-export core in __init__.py)
- [ ] **CLI adapter implemented** (Click-based, calls core)
- [ ] **REST API adapter implemented** (FastAPI-based, calls core)
- [ ] **MCP adapter implemented** (FastMCP-based, calls core)
- [ ] **Error mapping documented** (core exception → interface errors)
- [ ] **Consistency tests pass** (all interfaces produce same results)
- [ ] **README with all 4 usage examples** (Native, CLI, REST, MCP)

### Recommended Tier (Should Have)

- [ ] **Correlation IDs propagate** (X-Request-ID through all layers)
- [ ] **Structured logging** (JSON logs with request_id, operation, interface)
- [ ] **Versioned APIs** (REST: /api/v1/, MCP: namespaced tools)
- [ ] **Backward compatibility tests** (old clients still work)
- [ ] **Interface-specific features documented** (e.g., CLI: --json flag, REST: pagination)
- [ ] **Performance baseline measured** (adapter overhead <10ms)

### Advanced Tier (Nice to Have)

- [ ] **SDKs auto-generated** (OpenAPI → Python/TS clients)
- [ ] **Shell autocompletion** (CLI tab-completion)
- [ ] **Gateway integration** (unified access via gateway)
- [ ] **Multi-protocol load testing** (verify interface parity under load)
- [ ] **Interface usage metrics** (track which interfaces are popular)

---

## 🔧 Common Patterns

### Pattern 1: Error Mapping (Core → Interfaces)

**Core Exception** → **Interface-Specific Error**:

```python
# Core
raise ValidationError("replicas must be >= 1", field="replicas")

# ↓ Adapters translate ↓

# CLI
click.echo("Error: replicas must be >= 1\n  Field: replicas", err=True)
sys.exit(1)

# REST
raise HTTPException(
    status_code=400,
    detail={"error": "VALIDATION_ERROR", "message": "replicas must be >= 1", "field": "replicas"}
)

# MCP
raise ValueError("replicas must be >= 1 (field: replicas)")
```

**Error Mapping Table**:

| Core Exception | CLI | REST | MCP |
|----------------|-----|------|-----|
| ValidationError | Exit 1 + stderr | HTTP 400 | ValueError |
| NotFoundError | Exit 1 + stderr | HTTP 404 | ValueError |
| ConflictError | Exit 1 + stderr | HTTP 409 | ValueError |
| OperationError | Exit 1 + stderr | HTTP 500 | RuntimeError |

### Pattern 2: Core-Interface Separation

```
┌─────────────────────────────────────┐
│  Native  CLI  REST  MCP             │ ← Thin adapters (parse, format)
└──────────────┬──────────────────────┘
               │
         ┌─────▼─────┐
         │   Core    │ ← Business logic (interface-agnostic)
         └───────────┘
```

**Key Rule**: Core never imports interface frameworks.

### Pattern 3: Consistent Naming Across Interfaces

| Concept | Core | Native API | CLI | REST API | MCP Tool |
|---------|------|------------|-----|----------|----------|
| Create deployment | `create_deployment()` | `service.create_deployment()` | `orch create` | `POST /api/v1/environments/{env_id}/deployments` | `orchestrator:create_deployment` |
| Replica count | `replicas` field | `config["replicas"]` | `--replicas` flag | `replicas` JSON field | `replicas` arg |

### Pattern 4: Interface-Specific Features (Documented)

**CLI-specific**: `--json` flag for machine-readable output
```bash
orch list --json | jq '.[] | select(.status=="running")'
```

**REST-specific**: Pagination headers
```http
GET /api/v1/deployments?page=2&page_size=50
Link: </api/v1/deployments?page=3>; rel="next"
```

**MCP-specific**: Resources for AI-readable documentation
```python
@mcp.resource(uri="orchestrator://docs/quickstart.md")
def get_quickstart() -> str:
    return "# Quickstart Guide\n..."
```

### Pattern 5: Observability (Correlation IDs)

**Request flow with X-Request-ID**:
```
Claude Desktop → MCP → Core → Database
(X-Request-ID: abc123)
         ↓
All logs: {"request_id": "abc123", "operation": "create_deployment", "interface": "mcp"}
```

**Implementation**:
```python
# MCP adapter
@mcp.tool()
def create_deployment(...):
    request_id = generate_request_id()
    logger.info("create_deployment called", extra={"request_id": request_id, "interface": "mcp"})
    try:
        result = service.create_deployment(..., request_id=request_id)
        logger.info("create_deployment succeeded", extra={"request_id": request_id})
        return result
    except Exception as e:
        logger.error("create_deployment failed", extra={"request_id": request_id, "error": str(e)})
        raise
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Business Logic in Interface Layer

**Bad**:
```python
@app.post("/deployments")
def create_deployment(request: CreateRequest):
    # ❌ Validation in interface layer
    if request.replicas < 1:
        raise HTTPException(400, "Invalid replicas")
    # ❌ Business logic in interface layer
    deployment = Deployment(...)
    db.session.add(deployment)
    db.session.commit()
```

**Good**:
```python
@app.post("/deployments")
def create_deployment(request: CreateRequest):
    # ✅ Thin adapter: parse → core → format
    try:
        deployment = service.create_deployment(env_id, request.model_dump())
        return deployment.to_dict()
    except ValidationError as e:
        raise HTTPException(400, e.message)
```

### Pitfall 2: Interface-Specific Features Not Available Elsewhere

**Problem**: CLI has `--dry-run`, but REST API doesn't support preview mode.

**Fix**: Add `dry_run` parameter to core, expose via all interfaces:
```python
# Core
def create_deployment(self, env_id: str, config: Dict, dry_run: bool = False) -> Deployment:
    if dry_run:
        return Deployment(...)  # Don't persist

# CLI
@click.option("--dry-run", is_flag=True)
def create(..., dry_run):
    deployment = service.create_deployment(..., dry_run=dry_run)

# REST
@app.post("/deployments?dry_run={dry_run}")
def create_deployment(env_id: str, request: CreateRequest, dry_run: bool = False):
    deployment = service.create_deployment(..., dry_run=dry_run)

# MCP
@mcp.tool()
def create_deployment(..., dry_run: bool = False):
    deployment = service.create_deployment(..., dry_run=dry_run)
```

### Pitfall 3: Inconsistent Error Messages

**Problem**: CLI says "Invalid replicas", REST says "replicas must be >= 1", MCP says "bad replica count".

**Fix**: Core defines canonical error message, all interfaces use it:
```python
# Core
raise ValidationError("replicas must be >= 1", field="replicas")

# All interfaces translate consistently (same message, different format)
```

### Pitfall 4: No Consistency Tests

**Problem**: Interfaces drift over time (CLI adds feature, REST doesn't).

**Fix**: Add consistency tests to CI/CD:
```python
def test_all_interfaces_support_dry_run():
    """Verify dry_run parameter works in all interfaces."""
    # Core
    core_result = service.create_deployment(..., dry_run=True)
    assert core_result.deployment_id == ""  # Not persisted

    # CLI
    # ... test CLI with --dry-run

    # REST
    # ... test REST with ?dry_run=true

    # MCP
    mcp_result = create_deployment(..., dry_run=True)
    assert mcp_result["deployment"]["id"] == ""
```

### Pitfall 5: Thick Adapters

**Problem**: Adapter has 200+ lines, complex logic.

**Fix**: Move logic to core, keep adapter <100 lines:
```python
# If adapter is >100 lines, ask:
# - Is validation in adapter? → Move to core
# - Is business logic in adapter? → Move to core
# - Is data transformation complex? → Move to core helper
# Adapter should be: parse input → core.method() → format output
```

---

## 🤖 AI Agent Integration Notes

**For AI Agents** implementing multi-interface capability servers:

1. **Read SAP-042 first**: Foundation for contract-first, core-interface separation
2. **Start with core**: Implement business logic without thinking about interfaces
3. **Add interfaces incrementally**: Native (5 min) → CLI (30 min) → REST (30 min) → MCP (30 min)
4. **Test as you go**: Core tests first, then consistency tests
5. **Use templates**: SAP-043 provides complete code examples (copy-paste)

---

## 📚 Code Examples

### Example 1: Complete Orchestrator Service (4 Interfaces)

See [protocol-spec.md](./protocol-spec.md) for:
- Complete core module (service, models, exceptions, validators)
- All 4 interface adapters (Native, CLI, REST, MCP)
- Error handling patterns
- Testing strategies

### Example 2: Quick Decision Tree

**Question**: Which interfaces should I implement?

```
Does the capability need programmatic access (Python scripts)?
├─ Yes → Implement Native API (Essential)
└─ No → Skip to CLI

Do humans need to operate the service via command line?
├─ Yes → Implement CLI (Essential)
└─ No → Skip to REST

Do external systems need to integrate via HTTP?
├─ Yes → Implement REST API (Essential)
└─ No → Skip to MCP

Do AI assistants need direct access?
├─ Yes → Implement MCP (Recommended)
└─ No → AI can use REST via Gateway (Optional)
```

---

## 🔗 Related SAPs

**Directly Related**:
- **SAP-042** (InterfaceDesign): Foundational principles for contract-first, core-interface separation, error mapping, versioning
- **SAP-014** (mcp-server-development): MCP interface patterns (FastMCP, Chora MCP Conventions v1.0)

**Foundation**:
- **SAP-004** (testing-framework): pytest patterns for consistency tests, mocking strategies
- **SAP-012** (development-lifecycle): DDD principles for core module design, BDD for interface parity

**Integration**:
- **SAP-044** (Registry): Service registration via multiple interfaces
- **SAP-047** (CapabilityServer-Template): Scaffolding generates multi-interface structure

---

## 📊 Adoption Metrics

**Essential Tier Success** (1-2 weeks adoption):
- Core module exists with 0 interface imports
- All 4 interfaces implemented (Native, CLI, REST, MCP)
- 100% feature parity (all operations in all interfaces)
- Consistency tests passing
- <5% code duplication (business logic in core only)

**Recommended Tier Success** (2-4 weeks adoption):
- Correlation IDs in 100% of requests
- Structured logging (JSON format)
- APIs versioned (REST: /api/v1/, MCP: namespaced)
- Backward compatibility tests passing
- <10ms adapter overhead

**Advanced Tier Success** (4-8 weeks adoption):
- 3+ SDKs auto-generated (Python, TypeScript, Go)
- Shell autocompletion working for CLI
- Gateway integration (unified access)
- Multi-protocol load testing passing

---

## 🆘 Getting Help

**Questions?**
1. Read [capability-charter.md](./capability-charter.md) - Problem statement and solution design
2. Read [protocol-spec.md](./protocol-spec.md) - Complete technical specification
3. Follow [adoption-blueprint.md](./adoption-blueprint.md) - Step-by-step guide
4. Check [ledger.md](./ledger.md) - Adoption examples and feedback

**Common Questions**:

**Q**: Do I need ALL 4 interfaces (Native, CLI, REST, MCP)?
**A**: Minimum: Native + 1 other. Recommended: All 4 for full capability server functionality. MCP is essential for AI assistant access.

**Q**: Can I add a 5th interface (e.g., gRPC)?
**A**: Yes! Add new adapter (api/grpc.py), follow same pattern: parse inputs → call core → format outputs. Update consistency tests.

**Q**: How do I handle interface-specific features (e.g., CLI progress bars)?
**A**: Core provides hooks (e.g., yield progress events), adapters consume appropriately. Document interface-specific features in README.

**Q**: What if core logic is complex (long-running operations)?
**A**: Core can be async (`async def` methods), adapters handle appropriately:
- CLI: Show progress bar (consume async generator)
- REST: Return operation ID, provide status endpoint
- MCP: Return immediately with "in_progress" status

---

## ✅ Success Criteria Summary

**You've successfully adopted SAP-043 when**:

Essential:
- [ ] Core module implemented (interface-agnostic)
- [ ] All 4 interfaces implemented (Native, CLI, REST, MCP)
- [ ] Same operations in all interfaces (100% parity)
- [ ] Consistency tests passing
- [ ] Error handling consistent

Recommended:
- [ ] Correlation IDs propagate
- [ ] APIs versioned
- [ ] Backward compatibility maintained
- [ ] <10ms adapter overhead

Advanced:
- [ ] SDKs auto-generated
- [ ] Shell autocompletion working
- [ ] Gateway integration complete

---

**Next Steps**:
1. Read [adoption-blueprint.md](./adoption-blueprint.md) for step-by-step implementation
2. Use checklist above to track progress
3. Log adoption in [ledger.md](./ledger.md)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Feedback**: Submit to ledger.md or via SAP-019 self-evaluation
