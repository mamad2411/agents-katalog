# SAP-047: CapabilityServer-Template - Agent Quick Reference

**SAP ID**: SAP-047
**Name**: CapabilityServer-Template
**Version**: 1.0.0
**Status**: Pilot
**Created**: 2025-11-12
**Last Updated**: 2025-11-12

---

## Purpose

This quick reference guide helps AI agents (Claude Code, Claude Desktop, etc.) use SAP-047 (CapabilityServer-Template) to generate new capability servers quickly and consistently.

**Core Principle**: "Start right, stay right" - generate production-ready capability servers in minutes, not weeks.

---

## 📖 Quick Reference

### When to Use This SAP

**Use SAP-047 when you need to**:
- Create a new capability server from scratch
- Ensure consistency with established patterns (SAP-042 through SAP-046)
- Bootstrap a project with multi-interface support (CLI, REST, MCP)
- Integrate with service registry, bootstrap, and composition patterns automatically
- Accelerate onboarding for new developers (pre-configured structure)

**Don't use SAP-047 when**:
- Adding features to existing capability server (just extend current code)
- Creating non-capability services (templates are specific to capability servers)
- Building one-off scripts or tools (template is overkill)

---

## 🚀 5-Minute Quick Start

### 1. Install Jinja2 (if needed)

```bash
pip install jinja2
```

### 2. Generate Project

```bash
python scripts/create-capability-server.py \
    --name "Analyzer" \
    --namespace chora \
    --description "AI code analysis service" \
    --author "Infrastructure Team" \
    --python-version 3.11 \
    --enable-mcp \
    --enable-saga \
    --enable-circuit-breaker \
    --output ~/projects/analyzer
```

### 3. Navigate to Project

```bash
cd analyzer
```

### 4. Setup Development Environment

```bash
./scripts/dev-setup.sh

# This will:
# 1. Install Poetry (if not installed)
# 2. Install dependencies
# 3. Setup pre-commit hooks
# 4. Create virtual environment
```

### 5. Run Tests

```bash
pytest tests/ --cov=src/

# Expected: All tests pass, ≥80% coverage
```

### 6. Run Locally

```bash
docker-compose up

# Services available at:
# - REST API: http://localhost:8080
# - Health: http://localhost:8080/health
```

**You now have**:
- ✅ Multi-interface capability server (CLI, REST, MCP)
- ✅ Manifest registry integration
- ✅ Bootstrap startup sequence
- ✅ Saga orchestration (if enabled)
- ✅ Circuit breakers (if enabled)
- ✅ Test suite (≥80% coverage)
- ✅ CI/CD pipelines
- ✅ Documentation (AGENTS.md, API.md, CLI.md)

---

## 🎯 Common Workflows

### Workflow 1: Generate New Capability Server

**Scenario**: Create a new "Storage" capability server for data persistence.

**Steps**:

```bash
# 1. Generate project
python scripts/create-capability-server.py \
    --name "Storage" \
    --namespace chora \
    --description "Data persistence service" \
    --enable-mcp \
    --enable-circuit-breaker \
    --output ~/projects/storage
    # Note: --enable-saga omitted (no multi-step workflows needed)

# 2. Navigate to project
cd ~/projects/storage

# 3. Implement core logic
# Edit: src/chora/storage/core/capability.py

# 4. Add business logic
# Example: implement execute() method for storage operations

# 5. Run tests
pytest tests/

# 6. Deploy
./scripts/deploy.sh staging
```

**Generated Files**:
- `src/chora/storage/core/capability.py` - Core business logic
- `src/chora/storage/interfaces/cli.py` - CLI interface
- `src/chora/storage/interfaces/rest.py` - REST API
- `src/chora/storage/interfaces/mcp.py` - MCP server
- `tests/test_core/test_capability.py` - Unit tests
- `config/manifest.yaml` - Service manifest
- `Dockerfile` - Production-ready image

---

### Workflow 2: Customize Generated Project

**Scenario**: Customize the generated "Analyzer" project for specific needs.

**Steps**:

```bash
# 1. Edit core capability
# File: src/chora/analyzer/core/capability.py

class AnalyzerCapability(BaseCapability):
    async def execute(self, input_data: CapabilityInput) -> CapabilityOutput:
        """
        Analyze code (custom implementation).
        """
        # Your custom logic here
        code = input_data.get("code")
        language = input_data.get("language", "python")

        # Call your analysis logic
        analysis_result = await self._analyze_code(code, language)

        return CapabilityOutput(
            status="success",
            result={"analysis": analysis_result}
        )

    async def _analyze_code(self, code: str, language: str):
        """Custom analysis logic."""
        # TODO: Implement your analysis logic
        return {"issues": [], "suggestions": []}

# 2. Add dependencies to pyproject.toml
# [tool.poetry.dependencies]
# tree-sitter = "^0.20.0"  # For code parsing
# pylint = "^3.0.0"       # For Python analysis

# 3. Update tests
# File: tests/test_core/test_capability.py

async def test_analyze_python_code(capability):
    """Test Python code analysis."""
    result = await capability.execute({
        "code": "print('hello')",
        "language": "python"
    })
    assert result.status == "success"
    assert "analysis" in result.result

# 4. Run tests
pytest tests/ --cov=src/
```

---

### Workflow 3: Add Saga Orchestration

**Scenario**: Add multi-step workflow to "Deployment" capability server.

**Steps**:

```bash
# 1. Enable saga during generation
python scripts/create-capability-server.py \
    --name "Deployment" \
    --namespace chora \
    --enable-saga \
    --output ~/projects/deployment

# 2. Define saga in config/sagas.yaml
sagas:
  deploy_application:
    name: "Deploy Application"
    timeout: 600
    steps:
      - id: "validate_config"
        operation: "validate_config"
        compensation: "none"  # Validation has no side effects

      - id: "build_image"
        operation: "build_docker_image"
        compensation: "delete_image"
        depends_on: ["validate_config"]

      - id: "push_image"
        operation: "push_to_registry"
        compensation: "delete_from_registry"
        depends_on: ["build_image"]

      - id: "deploy_containers"
        operation: "deploy_to_cluster"
        compensation: "rollback_deployment"
        depends_on: ["push_image"]

# 3. Implement saga steps
# File: src/chora/deployment/composition/saga.py

from chora_compose.composition import Saga, SagaStep

class DeploymentSaga:
    """Deployment saga with rollback."""

    def __init__(self):
        self.saga = Saga("deploy_application")

        # Add steps
        self.saga.add_step(SagaStep(
            "validate_config",
            self.validate_config,
            lambda _: None  # No compensation needed
        ))

        self.saga.add_step(SagaStep(
            "build_image",
            self.build_docker_image,
            self.delete_image
        ))

        # ... add other steps

    async def validate_config(self, data):
        """Validate deployment config."""
        # Validation logic
        return {"validated": True}

    async def build_docker_image(self, data):
        """Build Docker image."""
        # Build logic
        return {"image_id": "img_123"}

    async def delete_image(self, data):
        """Compensation: delete Docker image."""
        image_id = data["image_id"]
        # Delete logic

# 4. Use saga in capability
# File: src/chora/deployment/core/capability.py

async def execute(self, input_data):
    """Execute deployment saga."""
    saga = DeploymentSaga()
    result = await saga.execute(input_data)

    if result["status"] == "failed":
        # Saga failed, compensation ran
        return CapabilityOutput(
            status="failed",
            result={"error": result["error"], "compensated": True}
        )

    return CapabilityOutput(status="success", result=result)
```

---

### Workflow 4: Add Circuit Breaker for External Services

**Scenario**: Protect "Notifier" service from cascading failures when email service is down.

**Steps**:

```bash
# 1. Enable circuit breaker during generation
# enable_circuit_breaker: yes

# 2. Configure circuit breaker
# File: config/circuit_breakers.yaml

circuit_breakers:
  email_service:
    failure_threshold: 5
    success_threshold: 3
    timeout: 30
    exceptions:
      - ConnectionError
      - TimeoutError

# 3. Use circuit breaker in capability
# File: src/chora/notifier/core/capability.py

from chora_compose.composition import CircuitBreaker

class NotifierCapability(BaseCapability):
    def __init__(self, config):
        super().__init__(config)
        self.email_cb = CircuitBreaker.from_config(
            "email_service",
            config_file="config/circuit_breakers.yaml"
        )

    async def execute(self, input_data):
        """Send notification with circuit breaker."""
        try:
            # Call email service through circuit breaker
            result = await self.email_cb.call(
                self._send_email,
                to=input_data["to"],
                subject=input_data["subject"],
                body=input_data["body"]
            )
            return CapabilityOutput(status="success", result=result)

        except CircuitOpenError:
            # Circuit open, email service unavailable
            # Use fallback: queue for later
            await self._queue_for_later(input_data)
            return CapabilityOutput(
                status="queued",
                result={"message": "Email service unavailable, queued for later"}
            )

    async def _send_email(self, to, subject, body):
        """Send email via external service."""
        # Email sending logic
        pass

    async def _queue_for_later(self, input_data):
        """Queue notification for later delivery."""
        # Queueing logic
        pass
```

---

### Workflow 5: Deploy Generated Project

**Scenario**: Deploy generated "Analyzer" project to staging environment.

**Steps**:

```bash
# 1. Build Docker image
docker build -t chora/analyzer:1.0.0 .

# 2. Tag for registry
docker tag chora/analyzer:1.0.0 registry.example.com/chora/analyzer:1.0.0

# 3. Push to registry
docker push registry.example.com/chora/analyzer:1.0.0

# 4. Deploy to staging
kubectl apply -f kubernetes/staging/

# Or use provided deployment script:
./scripts/deploy.sh staging

# 5. Verify deployment
curl http://staging.example.com/analyzer/health

# Expected: {"status": "healthy"}
```

---

### Workflow 6: Extend Template with Custom Features

**Scenario**: Add custom authentication middleware to generated project.

**Steps**:

```bash
# 1. Create middleware module
# File: src/chora/analyzer/middleware/auth.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    """JWT authentication middleware."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health checks
        if request.url.path in ["/health", "/ready"]:
            return await call_next(request)

        # Validate JWT token
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        # Validate token (your logic here)
        # ...

        response = await call_next(request)
        return response

# 2. Add middleware to REST API
# File: src/chora/analyzer/interfaces/rest.py

from chora.analyzer.middleware.auth import AuthMiddleware

app.add_middleware(AuthMiddleware)

# 3. Add tests
# File: tests/test_middleware/test_auth.py

async def test_auth_middleware_blocks_unauthorized():
    """Test that requests without token are blocked."""
    client = TestClient(app)
    response = client.post("/api/v1/execute", json={"input_data": {}})
    assert response.status_code == 401

async def test_auth_middleware_allows_health_check():
    """Test that health checks bypass auth."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
```

---

## 🔧 Template Variables Reference

### Core Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `project_name` | MyCapability | Human-readable project name | Analyzer, Storage, Notifier |
| `project_slug` | (derived) | URL/CLI-friendly name | analyzer, storage, notifier |
| `namespace` | chora | Python namespace | chora, mycompany |
| `project_description` | A capability server | Short description | AI code analysis service |
| `author_name` | Your Name | Author name | Infrastructure Team |
| `author_email` | your.email@example.com | Author email | infra@example.com |
| `python_version` | 3.11 | Python version | 3.9, 3.10, 3.11 |

### Feature Flags

| Variable | Default | Description | When to Enable |
|----------|---------|-------------|----------------|
| `enable_mcp` | yes | Generate MCP server interface | AI agent integration needed |
| `enable_saga` | yes | Include Saga orchestration | Multi-step workflows with rollback |
| `enable_circuit_breaker` | yes | Include circuit breaker | External service calls |
| `enable_event_bus` | no | Include event bus integration | Pub/sub messaging needed |

---

## 🎨 Project Structure Reference

```
{{project_slug}}/
├── src/{{namespace}}/{{project_slug}}/
│   ├── core/                  # Business logic (SAP-042)
│   │   ├── capability.py      # ← Implement your logic here
│   │   ├── models.py          # Pydantic models
│   │   └── exceptions.py      # Custom exceptions
│   │
│   ├── interfaces/            # Multi-interface (SAP-043)
│   │   ├── cli.py             # ← Extend CLI commands here
│   │   ├── rest.py            # ← Extend REST endpoints here
│   │   └── mcp.py             # ← Extend MCP tools here
│   │
│   ├── registry/              # Registry integration (SAP-044)
│   │   └── client.py          # Manifest client (ready-to-use)
│   │
│   ├── bootstrap/             # Bootstrap patterns (SAP-045)
│   │   └── startup.py         # Startup sequence (ready-to-use)
│   │
│   └── composition/           # Composition patterns (SAP-046)
│       ├── saga.py            # ← Define sagas here
│       ├── circuit_breaker.py # ← Configure circuit breakers here
│       └── events.py          # ← Implement event handlers here
│
├── tests/                     # ← Add your tests here
│   ├── test_core/
│   ├── test_interfaces/
│   └── test_integration/
│
├── config/                    # ← Update configurations here
│   ├── manifest.yaml          # Service manifest
│   ├── config.yaml            # Runtime config
│   └── sagas.yaml             # Saga definitions
│
└── docs/                      # ← Update documentation here
    ├── AGENTS.md              # Agent awareness guide
    ├── API.md                 # REST API documentation
    └── CLI.md                 # CLI reference
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Not Running dev-setup.sh

**Problem**: Dependencies not installed, pre-commit hooks missing, tests fail.

**Fix**: Always run `./scripts/dev-setup.sh` after generating project.

```bash
cd {{project_slug}}
./scripts/dev-setup.sh
```

---

### Pitfall 2: Forgetting to Implement Core Logic

**Problem**: Generated project runs but does nothing useful (returns placeholder responses).

**Fix**: Implement `execute()` method in `core/capability.py`.

```python
# ❌ Bad: Leaving placeholder
async def execute(self, input_data):
    return {"status": "success", "result": "..."}  # Placeholder

# ✅ Good: Implementing actual logic
async def execute(self, input_data):
    # Your business logic here
    result = await self._process_input(input_data)
    return CapabilityOutput(status="success", result=result)
```

---

### Pitfall 3: Not Updating manifest.yaml

**Problem**: Service registry doesn't know about your service, bootstrap fails.

**Fix**: Update `config/manifest.yaml` with correct service information.

```yaml
service:
  name: "analyzer"  # ← Update with actual service name
  dependencies:
    - name: "storage"  # ← Add actual dependencies
      required: true
```

---

### Pitfall 4: Skipping Tests

**Problem**: Generated tests pass, but actual functionality broken.

**Fix**: Write tests for your custom logic, not just placeholders.

```python
# ❌ Bad: Only testing placeholder
async def test_execute(capability):
    result = await capability.execute({})
    assert result.status == "success"  # Meaningless test

# ✅ Good: Testing actual behavior
async def test_analyze_code(capability):
    result = await capability.execute({
        "code": "def foo(): pass",
        "language": "python"
    })
    assert result.status == "success"
    assert "analysis" in result.result
    assert len(result.result["analysis"]["issues"]) == 0
```

---

### Pitfall 5: Not Enabling Required Features

**Problem**: Need Saga support but generated project without it.

**Fix**: Enable features during generation (or add manually later).

```bash
# If you forgot to enable saga:
# 1. Manually copy saga template from:
#    docs/skilled-awareness/composition/examples/saga.py

# 2. Add saga dependency to pyproject.toml:
#    sqlalchemy = "^2.0.0"

# 3. Create config/sagas.yaml

# Better: Re-generate with correct flags:
python scripts/create-capability-server.py \
    --name "YourProject" \
    --enable-saga \
    --output ~/projects/your-project
# Note: Will need to manually merge any custom changes
```

---

### Pitfall 6: Not Customizing Documentation

**Problem**: Generated docs still have template placeholders, confusing for users.

**Fix**: Update `docs/AGENTS.md`, `docs/API.md`, `docs/CLI.md` with actual info.

```markdown
# ❌ Bad: Leaving template placeholders
## Quick Reference
[Update with your commands here]

# ✅ Good: Actual documentation
## Quick Reference
**Execute Analysis**:
- CLI: `analyzer execute code.py --language python`
- REST: `POST /api/v1/execute {"code": "...", "language": "python"}`
- MCP: `execute(code="...", language="python")`
```

---

## 📚 Additional Resources

**Template Documentation**:
- [capability-charter.md](capability-charter.md) - Problem statement, ROI
- [protocol-spec.md](protocol-spec.md) - Complete specification
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step guide
- [ledger.md](ledger.md) - Adoption tracking, feedback

**Related SAPs** (Implemented in Template):

**Required Dependencies** (Automatically included):
- **SAP-042 (InterfaceDesign)** - Core/interface separation (REQUIRED)
  - Ensures clean architecture with business logic separated from interfaces
  - Reduces coupling by 80%, enables independent interface evolution

- **SAP-043 (MultiInterface)** - CLI, REST, MCP interfaces (REQUIRED)
  - Provides unified interface pattern for all access methods
  - Supports --enable-mcp flag for optional MCP interface
  - Saves 75% setup time vs manual multi-interface configuration

**Optional Dependencies** (Configurable via flags):
- **SAP-044 (Registry)** - Manifest integration (OPTIONAL)
  - Enable with --enable-registry flag
  - Adds service discovery and health monitoring
  - Required for service mesh architectures

- **SAP-045 (Bootstrap)** - Startup sequencing (OPTIONAL)
  - Enable with --enable-bootstrap flag
  - Adds dependency-ordered initialization
  - Reduces startup failures by 90%

- **SAP-046 (Composition)** - Saga, circuit breaker, events (OPTIONAL)
  - Enable saga: --enable-saga
  - Enable circuit breaker: --enable-circuit-breaker
  - Enable event bus: --enable-event-bus
  - Required for distributed transaction patterns

**Deprecates**:
- **SAP-014 (mcp-server-development)** - MCP-only approach (DEPRECATED)
  - SAP-047 supersedes SAP-014 with multi-interface capability
  - Migration: Use `--enable-mcp` flag for MCP interface support

**Examples**:
- `examples/analyzer/` - Complete analyzer service example
- `examples/storage/` - Storage service example
- `examples/notifier/` - Notification service example

---

## 🆘 Troubleshooting

### Issue 1: Template Generation Fails

**Symptom**: `python scripts/create-capability-server.py` fails with error.

**Diagnosis**:
```bash
# Check Jinja2 installed
python -c "import jinja2; print(jinja2.__version__)"
# Should be ≥3.0.0

# Check script exists
ls scripts/create-capability-server.py
```

**Fix**:
```bash
# Install Jinja2
pip install jinja2

# Or if in chora-base development:
poetry install
```

---

### Issue 2: Tests Fail After Generation

**Symptom**: `pytest tests/` fails with import errors.

**Diagnosis**:
```bash
# Check if dependencies installed
poetry show
```

**Fix**:
```bash
# Run dev-setup script
./scripts/dev-setup.sh

# Or manually:
poetry install
```

---

### Issue 3: Docker Build Fails

**Symptom**: `docker build .` fails with dependency errors.

**Diagnosis**:
```bash
# Check pyproject.toml for missing dependencies
cat pyproject.toml
```

**Fix**:
```bash
# Update poetry.lock
poetry lock --no-update

# Rebuild Docker image
docker build --no-cache -t {{project_slug}}:latest .
```

---

### Issue 4: Service Won't Register with Manifest

**Symptom**: Service starts but not visible in manifest registry.

**Diagnosis**:
```bash
# Check manifest URL
echo $MANIFEST_URL

# Test manifest health
curl http://manifest:8080/health
```

**Fix**:
```bash
# Update config/config.yaml
registry:
  manifest_url: "http://manifest:8080"  # ← Correct URL

# Restart service
docker-compose restart {{project_slug}}
```

---

## 🎓 Learning Path

**Beginner** (1-2 hours):
1. Read this AGENTS.md file
2. Generate a test project (Workflow 1)
3. Run tests and explore structure
4. Implement simple execute() method

**Intermediate** (4-6 hours):
1. Customize generated project (Workflow 2)
2. Add saga orchestration (Workflow 3)
3. Add circuit breakers (Workflow 4)
4. Deploy to staging (Workflow 5)

**Advanced** (8-12 hours):
1. Extend template with custom features (Workflow 6)
2. Add authentication middleware
3. Integrate with external services
4. Deploy to production with monitoring

---

**Document Version**: 1.0.0
**Status**: Pilot
**Last Updated**: 2025-11-12
