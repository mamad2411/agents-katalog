# /test-mvp-production — Final MVP Validation Before Close

The last script you run before closing an ANIMA module MVP and moving to the next one. Performs code review, full E2E testing, Docker validation, manifest checks, and generates a definitive pass/fail report. Nothing gets left behind.

## When to Use

- Before marking any ANIMA module as "MVP complete"
- Before pushing a module to production status
- As the final gate before moving to the next module in the sprint
- When you need a definitive "is this module done?" answer

## Usage

```
/test-mvp-production                    # Asks which folder to check
/test-mvp-production project_hermes     # Check specific module
/test-mvp-production 01-LLMDet          # Check by folder name (R&D)
/test-mvp-production all                # Batch: validate ALL modules in projects/ folder
```

## Folder Locations

Modules live in TWO places:
- **R&D (in progress)**: `/Users/ilessio/Development/AIFLOWLABS/R&D/` — modules being built
- **Production (MVP complete)**: `/Users/ilessio/Development/AIFLOWLABS/projects/` — validated modules

When a module name is given, check BOTH locations. Production folder takes priority.
When `all` is given, scan `/Users/ilessio/Development/AIFLOWLABS/projects/` and validate every `project_*` folder.

**MONAD reference** (for ROS2): `/Users/ilessio/Development/AIFLOWLABS/projects/project_monad`

## Instructions

When invoked, ask the user which module folder to validate if not provided. Then execute ALL phases below sequentially. Do NOT skip phases. Report results as you go.

**ROS2 is MANDATORY (D-034).** Every module MUST have a ROS2 node. If it doesn't, this is a CRITICAL failure that must be fixed before the module passes.

---

### PHASE 0: DISCOVERY (30 seconds)

Read the module folder and build a mental map:

```bash
# Identify the module
MODULE_DIR="<provided path or ask user>"
MODULE_NAME="<extract from pyproject.toml or folder name>"
```

**Read these files first** (skip if missing, note as gap):
1. `pyproject.toml` — dependencies, test config, metadata
2. `README.md` or `ARCHITECTURE.md` — what this module does
3. `Dockerfile` — build configuration
4. `docker-compose.yml` — service orchestration
5. `anima_module.yaml` — ANIMA manifest (if exists)
6. `src/*/server.py` or `src/*/api/` — API endpoints
7. `tests/` directory — test inventory
8. `CLAUDE.md` or `.claude/CLAUDE.md` — project instructions
9. `next_steps.md` or `TODO.md` — known gaps
10. `DEPLOYMENT_CHECKLIST.md` — if exists

**Output**: Module profile card:
```
MODULE: HERMES (project_hermes)
TYPE: Python/FastAPI microservice
CATEGORY: perception.communication
SOURCE: src/hermes/
TESTS: tests/ (N files)
DOCKER: [exists/missing]
MANIFEST: [exists/missing]
```

---

### PHASE 1: CODE REVIEW (deep)

Perform a thorough code review of ALL source files. Check:

#### 1.1 Code Quality
- [ ] No hardcoded secrets, tokens, or API keys
- [ ] No `print()` statements (should use logging)
- [ ] No `TODO`/`FIXME`/`HACK` comments left unresolved (list them all)
- [ ] No unused imports
- [ ] No dead code (unreachable functions, commented-out blocks)
- [ ] Consistent naming conventions (snake_case for Python)
- [ ] Type hints on all public functions
- [ ] Docstrings on all public classes and functions

#### 1.2 Security
- [ ] No SQL injection vectors (parameterized queries)
- [ ] No path traversal vulnerabilities
- [ ] Input validation on all API endpoints
- [ ] No hardcoded credentials or secrets
- [ ] Dependencies don't have known CVEs (check pyproject.toml)

#### 1.3 Architecture
- [ ] Single responsibility — each file under 500 lines
- [ ] No circular imports
- [ ] Clean separation: API layer / business logic / data layer
- [ ] Error handling with proper exception hierarchy
- [ ] Logging with structured output (not bare print)
- [ ] Configuration via environment variables or config files (not hardcoded)

#### 1.4 ANIMA-Specific
- [ ] Health endpoint exists at `/health` returning `{"status": "ok"}`
- [ ] Metrics endpoint exists at `/metrics` (Prometheus format) — optional but preferred
- [ ] API versioning or clear endpoint structure
- [ ] FastAPI with proper Pydantic models for request/response
- [ ] Async where appropriate (I/O-bound operations)

**Run linter**: Execute `ruff check src/` and `ruff format --check src/` to verify code style.

**Output**: List of issues found, categorized as CRITICAL / WARNING / INFO.

---

### PHASE 1.5: ASSET & DEPENDENCY CHECK (models, datasets, checkpoints)

Before running any tests, check if the module needs external assets that must be downloaded. These are NOT shipped in the repo (too large for git).

#### 1.5.1 Scan for Required Downloads

Look for these patterns in the codebase:
```bash
# Search for model/checkpoint/dataset references
rg -i "(huggingface|hf_hub|from_pretrained|load_model|download|checkpoint|ckpt|\.pt$|\.pth$|\.onnx$|\.safetensors$|weights)" src/ --type py
rg -i "(dataset|data_dir|data_path|download_data|DROID|BridgeData|OXE)" src/ configs/ --type-add 'cfg:*.{toml,yaml,yml,json}' --type cfg --type py
```

#### 1.5.2 Check if Assets Exist Locally

Common asset locations (check if populated or empty):
- `models/` or `checkpoints/` or `weights/` — model files
- `data/` or `datasets/` — training/eval data
- `configs/*.toml` or `configs/*.yaml` — may reference model paths
- Environment vars like `MODEL_PATH`, `HF_HOME`, `DATA_DIR`

#### 1.5.3 Report Missing Assets

If ANY required model, checkpoint, or dataset is missing, **STOP and tell the user**:

```
⚠️  MISSING ASSETS DETECTED — Cannot run full E2E without these:

MODELS/CHECKPOINTS:
  ❌ models/owlv2-base.safetensors — Required for inference
     Download: huggingface-cli download iSEE-Laboratory/llmdet_tiny --local-dir models/
     Size: ~450MB

  ❌ checkpoints/sam_vit_h.pth — Required for segmentation
     Download: wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O checkpoints/sam_vit_h.pth
     Size: ~2.4GB

DATASETS:
  ❌ data/eval_set/ — Required for benchmark tests
     Download: python scripts/download_eval_data.py
     Size: ~1.2GB

ACTION REQUIRED: Download these assets, then re-run /test-mvp-production
Alternatively: Tests will run in DEMO/MOCK mode (limited coverage)
```

**Key rules:**
- NEVER silently skip tests because assets are missing — always tell the user
- Check `pyproject.toml` optional deps (e.g., `[project.optional-dependencies.paper]`) — these often indicate heavy model deps
- Check if there's a `download_*.sh` or `download_*.py` script in the repo
- Check if `demo` mode exists (many ANIMA modules have a lightweight demo backend that works without weights)
- If demo mode exists, run tests in demo mode BUT flag that full E2E requires real weights
- Check `.gitignore` for patterns like `*.pt`, `*.pth`, `models/`, `data/` — these confirm assets are expected but not committed

#### 1.5.4 Decide Test Mode

Based on asset availability:
- **FULL mode**: All models + data present → run everything including inference tests
- **DEMO mode**: No models but demo backend exists → run with mocked/demo inference
- **SKIP mode**: Critical assets missing, no demo fallback → skip inference tests, warn user

Always report which mode was used in the final report.

---

### PHASE 2: TEST EXECUTION (full)

#### 2.1 Inventory Existing Tests
```bash
# Count and categorize tests
find tests/ -name "test_*.py" -o -name "*_test.py" | sort
```

Categorize each test file:
- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test module interactions (API + backend)
- **E2E tests**: Test full request→response flow
- **Smoke tests**: Basic "does it start?" tests
- **Health tests**: Health endpoint verification
- **Performance tests**: Benchmarking

#### 2.2 Run ALL Tests
```bash
python -m pytest tests/ -v --tb=short --cov=<module_name> --cov-report=term-missing 2>&1
```

**Record**:
- Total tests: N
- Passed: N
- Failed: N (list each)
- Skipped: N (list each with reason)
- Coverage: X%

#### 2.3 Missing Test Coverage
If coverage < 80%, identify the uncovered files/functions and create the missing tests. Priority order:
1. API endpoints (every route must have at least one test)
2. Core business logic (engine, pipeline, processing)
3. Error paths (what happens when things fail)
4. Configuration loading
5. Edge cases

#### 2.4 Run Linter
```bash
ruff check src/ tests/ 2>&1
```

If errors found, FIX THEM. Then re-run to confirm clean.

**Output**: Test results table + coverage report.

---

### PHASE 3: DOCKER VALIDATION

#### 3.1 Check Dockerfile Exists
If no Dockerfile exists, CREATE ONE following this template:

```dockerfile
# ─── ANIMA Module: {MODULE_NAME} ───
# Build: docker build -t anima-{module}:latest .
# Run:   docker run -p {PORT}:8000 anima-{module}:latest

FROM python:3.12-slim AS base

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git && \
    rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first (cache layer)
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project 2>/dev/null || uv sync --no-dev --no-install-project

# Copy source code
COPY src/ src/
COPY configs/ configs/ 2>/dev/null || true

# Install the project
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

# Create non-root user
RUN useradd -m -u 1000 {module} && chown -R {module}:1000 /app
USER {module}

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uv", "run", "uvicorn", "{module}.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 3.2 Check docker-compose.yml Exists
If no docker-compose.yml exists, CREATE ONE following this template:

```yaml
# ANIMA Module: {MODULE_DISPLAY_NAME}
# Usage:
#   docker compose up              # CPU mode
#   docker compose --profile gpu up  # GPU mode

services:
  anima_{module}:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: anima-{module}
    ports:
      - "{PORT}:8000"
    environment:
      - DEVICE=cpu
      - LOG_LEVEL=info
    volumes:
      - {module}-data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      start_period: 30s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
    restart: unless-stopped
    networks:
      - anima-net

  anima_{module}_gpu:
    extends:
      service: anima_{module}
    container_name: anima-{module}-gpu
    profiles: ["gpu"]
    environment:
      - DEVICE=cuda:0
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: "4.0"
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  {module}-data:

networks:
  anima-net:
    name: anima-net
    external: true
```

**Port Assignment Convention** (check main docker-compose.yml for conflicts):
- Core 6: 8001-8006 (AZOTH, MONAD, LOCI, LOGOS, GNOMON, OSIRIS)
- Wave 4: 8010+ (allocate next free)
- Wave 5: 8030+ (allocate next free)

#### 3.3 Validate Dockerfile Builds
```bash
docker build -t anima-{module}:test . 2>&1
```

If build fails, fix the Dockerfile and retry. Common issues:
- Missing system dependencies
- Wrong Python package names
- Permission issues
- Missing files in COPY

#### 3.4 Validate Container Starts
```bash
docker run -d --name anima-{module}-test -p {PORT}:8000 anima-{module}:test
sleep 5
curl -f http://localhost:{PORT}/health
docker logs anima-{module}-test --tail 20
docker stop anima-{module}-test && docker rm anima-{module}-test
```

#### 3.5 Clean Up Test Artifacts
```bash
docker rmi anima-{module}:test 2>/dev/null || true
```

**Output**: Docker build status + health check result.

---

### PHASE 4: MANIFEST VALIDATION

#### 4.1 Check anima_module.yaml
If it doesn't exist, CREATE it using the ANIMA manifest standard. Use information gathered from the code:

```yaml
schema_version: "1.0"

module:
  name: {module}
  version: {from pyproject.toml}
  display_name: "{MODULE_DISPLAY_NAME}"
  description: "{from README or code}"
  category: {perception|control|planning|navigation|fleet|world_model|edge}.{subcategory}
  license: Apache-2.0
  paper: "{if applicable}"

capabilities:
  provides:
    - type: {capability_type}
      subtype: {specific_capability}

interface:
  inputs:
    - name: {input_name}
      ros2_type: {msg_type}
      encoding: [{formats}]
      min_hz: {rate}
  outputs:
    - name: {output_name}
      ros2_type: {msg_type}
      typical_hz: {rate}
  parameters:
    - name: {param}
      type: {type}
      required: {bool}
      default: {value}

hardware:
  platforms:
    - name: linux_x86
      backends: [onnxruntime_cpu]
    - name: apple_silicon
      backends: [mlx, coreml]

performance:
  profiles:
    - platform: linux_x86_cpu
      model: {default_model}
      backend: onnxruntime_cpu
      fps: {estimated}
      latency_p50_ms: {estimated}

safety:
  failure_mode: returns_empty
  timeout_ms: {appropriate_value}
  health_topic: /anima/{module}/health

composability:
  pairs_well_with:
    - category: {related_category}
  conflicts_with: []

container:
  image: ghcr.io/aiflowlabs/anima-{module}:{version}
```

#### 4.2 Validate Manifest Consistency
- Module name matches folder/pyproject.toml
- Version matches pyproject.toml
- Interfaces match actual API endpoints
- Health endpoint matches safety.health_topic pattern
- Container image tag matches version

**Output**: Manifest status (created/validated/needs-update).

---

### PHASE 5: DOCUMENTATION CHECK

#### 5.1 Required Files Checklist
- [ ] `README.md` — What it does, how to run, API docs
- [ ] `ARCHITECTURE.md` — Technical design (can be section in README)
- [ ] `pyproject.toml` — Complete with all metadata fields
- [ ] `LICENSE` — Must exist (Apache-2.0 for ANIMA modules)
- [ ] `.gitignore` — Python + Docker patterns

#### 5.2 README Quality
The README must contain at minimum:
- One-sentence description
- What problem it solves
- Quick start (how to run)
- API endpoints list
- Configuration options
- Docker usage

If README is missing or incomplete, CREATE/UPDATE it.

#### 5.3 API Documentation
Every endpoint must be documented. Check if FastAPI auto-docs work:
- `/docs` — Swagger UI
- `/redoc` — ReDoc
- Both should be accessible when the server runs

**Output**: Documentation completeness score.

---

### PHASE 6: INTEGRATION CHECK

#### 6.1 Main docker-compose.yml Reference
Check if this module is referenced in the main ANIMA orchestration file:
`/Users/ilessio/Development/AIFLOWLABS/R&D/docker-compose.yml`

If not, note it as "not yet integrated into ANIMA suite" (this is OK for Wave 4/5 modules).

#### 6.2 Network Compatibility
- Uses `anima-net` network (or can be added)
- Port doesn't conflict with existing services
- Health check format matches ANIMA convention

#### 6.3 Data Flow
- Input/output topics documented
- Compatible with upstream/downstream modules (if applicable)

**Output**: Integration readiness status.

---

### PHASE 7: FINAL REPORT

Generate a comprehensive MVP report. This is the artifact that proves the module is done.

```markdown
# MVP VALIDATION REPORT
## Module: {MODULE_NAME} ({display_name})
## Date: {date}
## Validator: Claude (/test-mvp-production)

### SUMMARY
| Phase | Status | Score |
|-------|--------|-------|
| Code Review | PASS/FAIL | X/10 |
| Tests | PASS/FAIL | X passed, Y failed |
| Coverage | PASS/FAIL | X% |
| Docker | PASS/FAIL | builds + runs |
| Manifest | PASS/FAIL | complete/partial |
| Documentation | PASS/FAIL | X/5 required files |
| Integration | PASS/FAIL | ready/not-ready |

### OVERALL VERDICT: ✅ MVP COMPLETE / ❌ NEEDS WORK

### Issues Found (CRITICAL)
{list critical issues that MUST be fixed}

### Issues Found (WARNING)
{list warnings that should be fixed but don't block MVP}

### Issues Found (INFO)
{list informational notes}

### Test Results
{full test output}

### Coverage Report
{coverage summary}

### Files Created/Modified
{list all files touched during validation}

### Remaining TODOs
{anything that should be done post-MVP}
```

Save this report to: `{MODULE_DIR}/MVP_VALIDATION_REPORT.md`

---

### PHASE 8.5: CREATE MODULE RUN SKILL (/{module}-run)

**CRITICAL**: If a `/{module}-run` skill does NOT already exist, CREATE IT. This skill is a one-command launcher for the full E2E experiment. It saves hours every time you come back to a module.

#### 8.5.1 Check If Skill Exists

```bash
ls ~/.claude/skills/{module}-run/SKILL.md 2>/dev/null
```

If it exists, skip to Phase 8.5.3 (validate it). If not, create it.

#### 8.5.2 Create the Skill

Create `~/.claude/skills/{module}-run/SKILL.md` with this structure:

```markdown
# /{module}-run — Run {MODULE_DISPLAY_NAME} Full E2E

One-command launcher for the {MODULE_DISPLAY_NAME} module. Starts services, runs tests, demos inference, and tears down cleanly.

## Usage

\```
/{module}-run                  # Full E2E: start → test → demo → stop
/{module}-run start            # Just start the services
/{module}-run test             # Run all tests (assumes already started)
/{module}-run demo             # Run a demo inference
/{module}-run stop             # Tear down everything
/{module}-run status           # Check what's running
/{module}-run ros2             # Start with ROS2 profile
\```

## Instructions

### Module Info
- **Path**: {FULL_MODULE_PATH}
- **Source**: src/{module}/
- **Engine**: src/{module}/engine.py (or wherever the core class is)
- **Port**: {PORT} (FastAPI)
- **Docker service**: anima_{module}
- **ROS2 service**: anima_{module}_ros2 (profile: ros2)

### START Mode
```bash
cd {FULL_MODULE_PATH}

# Option 1: Docker (recommended)
docker compose up -d anima_{module}
# Wait for health
until curl -sf http://localhost:{PORT}/health; do sleep 1; done
echo "✅ {MODULE_UPPER} is healthy"

# Option 2: Local (for development)
uv run uvicorn {module}.server:app --host 0.0.0.0 --port {PORT} --reload

# Option 3: ROS2 mode
docker compose --profile ros2 up -d anima_{module}_ros2
```

### TEST Mode
```bash
cd {FULL_MODULE_PATH}

# Unit + integration tests
uv run pytest tests/ -v --tb=short --cov={module} --cov-report=term-missing

# Linter
uv run ruff check src/ tests/

# Health check (if Docker running)
curl -sf http://localhost:{PORT}/health | python3 -m json.tool
```

### DEMO Mode
```bash
cd {FULL_MODULE_PATH}

# {DEMO_DESCRIPTION — module-specific}
# Example for perception modules:
curl -X POST http://localhost:{PORT}/infer \
  -H "Content-Type: application/json" \
  -d '{DEMO_PAYLOAD}'

# Or for modules with a demo script:
uv run python -m {module}.demo
```

### STOP Mode
```bash
cd {FULL_MODULE_PATH}
docker compose down
docker compose --profile ros2 down 2>/dev/null || true
```

### STATUS Mode
```bash
cd {FULL_MODULE_PATH}
docker compose ps
curl -sf http://localhost:{PORT}/health 2>/dev/null && echo "✅ Healthy" || echo "❌ Not running"
```

### Full E2E (default — runs all steps)
1. Start services (Docker)
2. Wait for health check
3. Run all tests
4. Run demo inference
5. Print results summary
6. Stop services

### Required Assets
{LIST_ASSETS — models, checkpoints, datasets with download commands}

### Quick Reference
| Item | Value |
|------|-------|
| Path | `{FULL_MODULE_PATH}` |
| Port | {PORT} |
| Health | `http://localhost:{PORT}/health` |
| Docs | `http://localhost:{PORT}/docs` |
| Docker | `docker compose up -d anima_{module}` |
| ROS2 | `docker compose --profile ros2 up -d` |
| Tests | `uv run pytest tests/ -v` |
| Lint | `uv run ruff check src/` |
```

#### 8.5.3 Validate the Skill

If the skill already existed, READ it and check:
- [ ] Path is correct
- [ ] Port is correct and doesn't conflict
- [ ] Docker service name matches docker-compose.yml
- [ ] Demo command actually works with current API
- [ ] Required assets list is up to date
- [ ] ROS2 section exists (D-034)

Fix any stale information.

#### 8.5.4 Register in Module README

Add a section to the module's README.md:

```markdown
## Quick Run

```bash
# Inside Claude Code:
/azoth-run              # Full E2E
/azoth-run start        # Start services
/azoth-run test         # Run tests
/azoth-run demo         # Demo inference
```
```

**Output**: Skill created at `~/.claude/skills/{module}-run/SKILL.md`

---

### PHASE 8.7: ROS2 VALIDATION (MANDATORY — D-034)

**This phase is NOT optional.** Every ANIMA module must be a ROS2 node. If the ROS2 layer is missing, this is a CRITICAL failure.

#### 8.7.1 Check ROS2 Packages Exist

```bash
ls {module}_msgs/ 2>/dev/null && echo "✅ msgs package" || echo "❌ NO msgs package"
ls {module}_node/ 2>/dev/null && echo "✅ node package" || echo "❌ NO node package"
ls Dockerfile.ros2 2>/dev/null && echo "✅ Dockerfile.ros2" || echo "❌ NO Dockerfile.ros2"
```

#### 8.7.2 If ROS2 Missing → Build It

If ANY of the above are missing, run `/ros2-node` logic inline:
1. Analyze the module (inputs, outputs, services)
2. Create `{module}_msgs/` with message/service definitions
3. Create `{module}_node/` with node wrapper, conversions, QoS, launch file
4. Create `Dockerfile.ros2` with CycloneDDS + CLI tools
5. Add `ros2` and `ros2-test` profiles to `docker-compose.yml`
6. Create conversion tests in `tests/test_ros2_conversions.py`

Reference: `/Users/ilessio/Development/AIFLOWLABS/projects/project_monad/monad_node/`

#### 8.7.3 Validate ROS2 Tests Pass

```bash
# Run conversion tests (no rclpy needed)
python -m pytest tests/test_ros2_conversions.py -v 2>&1
```

#### 8.7.4 Validate Docker ROS2 Build

```bash
# Build the ROS2 container
docker compose --profile ros2-test build anima_{module}_ros2_test 2>&1
```

If build fails, fix and retry.

#### 8.7.5 Run Docker ROS2 Smoke Test

```bash
# One-command verification (no local ROS2 needed)
docker compose --profile ros2-test run --rm anima_{module}_ros2_test
```

This checks: node alive, topics exist, status publishing, services registered.

#### 8.7.6 ROS2 Verdict

```
ROS2 VALIDATION:
  msgs package:     [PASS/FAIL]
  node package:     [PASS/FAIL]
  Dockerfile.ros2:  [PASS/FAIL]
  Conversion tests: [PASS/FAIL]
  Docker build:     [PASS/FAIL]
  Smoke test:       [PASS/FAIL]

  ROS2 STATUS: ✅ PASS / ❌ FAIL (CRITICAL — must fix before MVP closes)
```

**If ROS2 fails, the overall MVP verdict is FAIL.** No exceptions. D-034 is locked.

---

### PHASE 8: CLEANUP & SIGN-OFF

#### 8.1 Clean Up
- Remove any test containers
- Remove any test images
- Ensure no temp files left behind

#### 8.2 Git Status
```bash
git status
```
Show the user what changed. Do NOT commit — let the user decide.

#### 8.3 Final Verdict
Based on all phases, give a clear verdict:

**If ALL phases pass:**
```
✅ MVP COMPLETE — {MODULE_NAME} is ready for production status.
   Tests: {N}/{N} passing
   Coverage: {X}%
   Docker: builds + runs + healthy
   Manifest: complete

   Next: Move to the next module in the sprint.
```

**If ANY critical issue remains:**
```
❌ MVP NOT READY — {MODULE_NAME} has {N} critical issues:
   1. {issue}
   2. {issue}

   Fix these, then run /test-mvp-production again.
```

---

## Scoring Rubric

| Category | Weight | Criteria for PASS |
|----------|--------|-------------------|
| Code Review | 25% | No critical issues, ruff clean |
| Tests | 25% | All tests pass |
| Coverage | 15% | ≥70% line coverage |
| Docker | 15% | Builds + starts + health check OK |
| Manifest | 10% | anima_module.yaml exists and valid |
| Documentation | 10% | README + pyproject.toml complete |

**MVP PASS threshold**: Score ≥ 80% AND zero critical issues.

---

## What This Skill Creates (if missing)

| File | When Created |
|------|-------------|
| `Dockerfile` | If no Dockerfile exists |
| `docker-compose.yml` | If no docker-compose exists |
| `anima_module.yaml` | If no manifest exists |
| `README.md` | If missing or empty |
| `LICENSE` | If missing (Apache-2.0) |
| Missing test files | If coverage < 70% |
| `MVP_VALIDATION_REPORT.md` | Always (the final report) |
| **`~/.claude/skills/{module}-run/SKILL.md`** | **If no /{module}-run skill exists** |

---

## Important Notes

- This skill FIXES issues it finds (linter errors, missing files, incomplete configs)
- It does NOT skip phases — every check runs every time
- It creates Docker artifacts with `anima_` prefix for consistency
- Container names follow: `anima-{module}` (hyphenated)
- Service names follow: `anima_{module}` (underscored, docker-compose convention)
- All created Dockerfiles use `uv` for package management (project convention)
- Non-root users in containers (security requirement)
- Health checks are mandatory (ANIMA architecture requirement)
