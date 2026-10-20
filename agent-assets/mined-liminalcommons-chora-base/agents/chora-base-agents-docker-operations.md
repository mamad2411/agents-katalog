---
sap_id: SAP-011
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 15
progressive_loading:
  phase_1: "lines 1-120"    # Quick Reference + Core Workflows
  phase_2: "lines 121-280"  # Advanced Workflows + Integration
  phase_3: "full"           # Complete including troubleshooting
phase_1_token_estimate: 3000
phase_2_token_estimate: 6500
phase_3_token_estimate: 10000
---

# Docker Operations (SAP-011) - Agent Awareness

**SAP ID**: SAP-011
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-011?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - 5 commands to build and deploy in 2 minutes
- 📚 **5 Docker Artifacts** - Dockerfile, Dockerfile.test, docker-compose.yml, .dockerignore, best practices
- 🎯 **Multi-Stage Builds** - 40% smaller images (150-250MB vs 500MB+)
- ⚡ **6x Faster CI** - Layer caching optimization patterns
- 🔧 **Troubleshooting** - Common problems and solutions

**This AGENTS.md provides**: Agent-specific patterns for Docker workflows, CI/CD integration, and container debugging.

---

## Overview

Use Docker Operations SAP when containerizing projects for production deployment, CI/CD testing, or multi-architecture builds. This SAP provides multi-stage Dockerfiles (150-250MB images), CI-optimized test environments (6x faster with cache), and docker-compose orchestration.

**When to Use**:
- Production deployment (MCP servers, web services)
- CI/CD testing (isolated environments, reproducible builds)
- Multi-architecture builds (ARM64 + AMD64)
- Local integration testing (docker-compose orchestration)

**Don't Use For**:
- Local development (use venv instead for faster iteration)
- Quick prototyping (Docker overhead not justified)
- Simple scripts (containerization adds complexity)

---

## User Signal Patterns

Recognize these user requests as Docker operations tasks:

| User Signal | Intent | Primary Workflow |
|-------------|--------|------------------|
| "build Docker image" | Containerize project | Build Production Image (Workflow 1) |
| "containerize this project" | Add Docker support | Build Production Image (Workflow 1) |
| "run tests in Docker" | CI environment testing | Run Tests in Docker (Workflow 2) |
| "deploy with docker-compose" | Local deployment | Deploy with docker-compose (Workflow 3) |
| "image too large" | Optimize image size | Optimize Image Size (Workflow 4) |
| "Docker build failing" | Debug build issues | Debug Container Issues (Workflow 5) |
| "support ARM64" | Multi-architecture | Multi-Architecture Builds (Workflow 6) |
| "CI builds slow" | Optimize CI cache | Enable GitHub Actions Cache (Workflow 7) |

---

## Quick Reference

### Common Commands

**Build**:
```bash
docker build -t <project-slug>:latest .
docker build -t <project-slug>:test -f Dockerfile.test .
```

**Run**:
```bash
docker run -d --name <project-slug> -p 8000:8000 <project-slug>:latest
docker run --rm <project-slug>:test  # Run tests
```

**docker-compose**:
```bash
docker-compose up -d       # Start services
docker-compose ps          # Check status
docker-compose logs -f     # View logs
docker-compose down        # Stop services
```

**Debug**:
```bash
docker logs <container>                   # View logs
docker exec -it <container> /bin/bash     # Interactive shell
docker inspect <container>                # Full config
```

### Key Patterns

**Multi-Stage Build** (Production):
- Stage 1 (builder): Build wheel distribution
- Stage 2 (runtime): Install wheel, non-root user (UID 1000)
- Result: 150-250MB images (vs 500MB+ single-stage)

**Test Dockerfile** (CI):
- Single-stage editable install
- GitHub Actions cache integration (6x faster)
- Coverage extraction patterns

**Security**:
- Non-root user (UID 1000)
- Minimal base (`python:3.11-slim`)
- No secrets in images (use `.env` files)
- `.dockerignore` excludes: `.git`, `.env`, `*.pem`, `*.key`

---

## Common Workflows

### Workflow 1: Build Production Docker Image

**Context**: User requests "build Docker image" or "containerize this project"

**Research First** (Optional but recommended):
```bash
# Research Docker best practices before building
just research "Docker best practices: multi-stage builds, security, image optimization"

# Use research to inform Dockerfile design:
# - Multi-stage patterns → reduce image size by 60%
# - Security practices → non-root user, minimal base images
# - Anti-patterns → avoid secrets in layers, large build contexts
```

**Steps**:

1. **Verify Dockerfile exists**:
   ```bash
   ls Dockerfile
   ```
   If missing → copy from [static-template/Dockerfile](../../../static-template/Dockerfile)

2. **Verify .dockerignore exists** (critical for build speed):
   ```bash
   ls .dockerignore
   ```
   If missing → copy from [static-template/.dockerignore](../../../static-template/.dockerignore)

3. **Build production image**:
   ```bash
   docker build -t <project-slug>:latest .
   ```
   Replace `<project-slug>` with actual project name

4. **Verify build success and size**:
   ```bash
   docker images <project-slug>:latest --format "{{.Size}}"
   ```
   Target: ≤250MB (alert user if >250MB)

5. **Test image**:
   ```bash
   # MCP Server (STDIO)
   docker run --rm <project-slug>:latest <command> --version

   # Web Service
   docker run --rm -p 8000:8000 <project-slug>:latest
   ```

**Success Criteria**:
- Image builds without errors
- Size ≤250MB
- Container starts and responds

**Common Issues**:
- "Module not found" → Verify `pyproject.toml` package name matches `src/<package>/`
- Image >500MB → Check `.dockerignore`, ensure multi-stage build
- Permission errors → Ensure UID 1000 (non-root user)

---

### Workflow 2: Run Tests in Docker (CI Environment)

**Context**: User requests "run tests in Docker" or CI build failing

**Steps**:

1. **Verify Dockerfile.test exists**:
   ```bash
   ls Dockerfile.test
   ```
   If missing → copy from [static-template/Dockerfile.test](../../../static-template/Dockerfile.test)

2. **Build test image**:
   ```bash
   docker build -t <project-slug>:test -f Dockerfile.test .
   ```

3. **Run tests**:
   ```bash
   docker run --rm <project-slug>:test
   ```
   This runs `pytest` with coverage (default CMD)

4. **Extract coverage** (if needed):
   ```bash
   container_id=$(docker create <project-slug>:test)
   docker cp $container_id:/app/coverage.xml ./coverage.xml
   docker rm $container_id
   ```

**Success Criteria**:
- Tests pass (100% pass rate in isolated environment)
- Coverage report generated

**Common Issues**:
- Tests pass locally but fail in Docker → System dependency missing in Dockerfile.test
- Coverage not extracted → Ensure tests ran (check `docker logs`)

---

### Workflow 3: Deploy with docker-compose

**Context**: User requests "deploy locally" or "run with docker-compose"

**Steps**:

1. **Verify docker-compose.yml exists**:
   ```bash
   ls docker-compose.yml
   ```
   If missing → copy from [static-template/docker-compose.yml](../../../static-template/docker-compose.yml)

2. **Create .env file** (if not exists):
   ```bash
   cp .env.example .env
   # Remind user to edit .env with actual values
   ```

3. **Set up volume directories and permissions**:
   ```bash
   mkdir -p logs data .chora/memory
   sudo chown -R 1000:1000 logs/ data/ .chora/memory/
   ```
   Critical: UID 1000 matches container user

4. **Start services**:
   ```bash
   docker-compose up -d
   ```

5. **Verify health**:
   ```bash
   docker-compose ps
   # Check "State" column: should be "Up" or "Up (healthy)"
   ```

6. **View logs** (if issues):
   ```bash
   docker-compose logs -f <project-slug>
   ```

**Success Criteria**:
- All services start (`docker-compose ps` shows "Up")
- Health checks pass
- Application accessible

**Common Issues**:
- Port conflicts → Change host port in docker-compose.yml (`8001:8000`)
- Volume permission errors → Verify UID 1000 ownership (`ls -lan logs/`)
- Health check failing → Check logs, verify health check command

---

### Workflow 4: Optimize Image Size

**Context**: User reports "image too large" or requests optimization

**Steps**:

1. **Check current size**:
   ```bash
   docker images <project-slug>:latest --format "{{.Size}}"
   ```

2. **Verify multi-stage build**:
   ```bash
   grep "FROM.*as builder" Dockerfile
   ```
   If missing → Add builder stage (see [protocol-spec.md](protocol-spec.md) §11.1)

3. **Check .dockerignore coverage**:
   ```bash
   cat .dockerignore | grep -E "^\.git$|^venv/|^docs/"
   ```
   Should exclude: `.git`, `venv/`, `docs/`, `.vscode/`, `*.md` (except README)

4. **Check build context size**:
   ```bash
   docker build --no-cache -t test . 2>&1 | grep "Sending build context"
   ```
   Target: <20MB (with .dockerignore: 81% reduction)

5. **Rebuild and verify**:
   ```bash
   docker build --no-cache -t <project-slug>:latest .
   docker images <project-slug>:latest
   ```

**Success Criteria**:
- Image size ≤250MB
- Build context <20MB
- Multi-stage build verified

**Common Fixes**:
- Add missing .dockerignore entries
- Convert single-stage to multi-stage
- Use `--no-cache-dir` in `pip install` commands

---

### Workflow 5: Debug Container Issues

**Context**: Container crashes, health check fails, or unexpected behavior

**Steps**:

1. **Check container logs first** (reveals most issues):
   ```bash
   docker logs <container-name>
   # or
   docker-compose logs -f <service-name>
   ```

2. **Run interactive shell** (if logs unclear):
   ```bash
   docker run -it --rm <project-slug>:latest /bin/bash
   ```
   Test commands manually inside container

3. **Check health status**:
   ```bash
   docker inspect --format='{{json .State.Health}}' <container-name> | jq
   ```

4. **Verify environment variables**:
   ```bash
   docker exec <container-name> env
   ```

5. **Check file permissions**:
   ```bash
   docker exec <container-name> ls -la /app/logs
   # Should be owned by appuser (UID 1000)
   ```

**Common Issues**:

| Issue | Diagnosis Command | Fix |
|-------|-------------------|-----|
| "Module not found" | `docker run -it <image> python -c "import <pkg>"` | Rebuild with correct package name |
| "Permission denied" on /app/logs | `docker exec <container> ls -la /app/logs` | `chown -R 1000:1000 ./logs` on host |
| Health check failing | `docker exec <container> python -c "import <pkg>; print(<pkg>.__version__)"` | Add `__version__` to `__init__.py` |
| Container exits immediately | `docker logs <container>` | Check CMD, verify entrypoint |

---

## Advanced Workflows

### Workflow 6: Multi-Architecture Builds (ARM64 + AMD64)

**Context**: User requests "build for ARM64" or "support Apple Silicon"

**Steps**:

1. **Set up buildx** (one-time):
   ```bash
   docker buildx create --use
   docker buildx inspect --bootstrap
   ```

2. **Build for multiple platforms**:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 \
     -t <project-slug>:latest --load .
   ```
   Note: `--load` loads single platform locally; use `--push` for multi-platform registry push

3. **Verify platforms**:
   ```bash
   docker buildx imagetools inspect <project-slug>:latest
   ```
   Should show: `linux/amd64`, `linux/arm64`

**Success Criteria**:
- Image builds for both amd64 and arm64
- No architecture-specific dependencies

**Common Issues**:
- "multiple platforms feature is not supported" → Run `docker buildx create --use`
- Build fails for ARM64 → Check for x86-only dependencies (rare in Python)

---

### Workflow 7: Enable GitHub Actions Cache (6x Speedup)

**Context**: CI builds slow (2-3 minutes), user requests optimization

**Steps**:

1. **Check current workflow**:
   ```yaml
   # .github/workflows/test.yml (current - slow)
   - name: Build
     run: docker build -t test -f Dockerfile.test .
   ```

2. **Add buildx setup**:
   ```yaml
   - name: Set up Docker Buildx
     uses: docker/setup-buildx-action@v3
   ```

3. **Replace docker build with build-push-action**:
   ```yaml
   - name: Build test image
     uses: docker/build-push-action@v5
     with:
       file: ./Dockerfile.test
       tags: ${{ github.repository }}:test
       cache-from: type=gha
       cache-to: type=gha,mode=max
       load: true
   ```

4. **Run workflow and verify speedup**:
   - First build: 2-3 minutes (populates cache)
   - Subsequent builds: ~30 seconds (6x faster)

**Success Criteria**:
- First build completes (cache populated)
- Second build shows "CACHED" in logs
- Build time <45 seconds (cached)

**Common Issues**:
- No speedup → Ensure `cache-to: type=gha,mode=max` (not just `cache-from`)
- Cache misses → Check layer ordering (dependencies before code)

---

### Workflow 8: Troubleshoot Volume Mounts

**Context**: Data not persisting, config changes not reflected

**Steps**:

1. **Check volume mounts** (docker-compose.yml):
   ```yaml
   volumes:
     - ./logs:/app/logs
     - ./data:/app/data
     - ./.chora/memory:/app/.chora/memory
   ```

2. **Verify directories exist on host**:
   ```bash
   ls -la logs/ data/ .chora/memory/
   ```
   If missing → `mkdir -p logs data .chora/memory/{events,knowledge}`

3. **Check ownership** (UID 1000):
   ```bash
   ls -lan logs/
   # Should show UID 1000, not 0 (root) or your user ID
   ```

4. **Fix ownership** (if needed):
   ```bash
   sudo chown -R 1000:1000 logs/ data/ .chora/memory/
   ```

5. **Test persistence**:
   ```bash
   docker-compose up -d
   docker exec <project-slug> sh -c "echo 'test' > /app/logs/test.log"
   docker-compose down
   docker-compose up -d
   docker exec <project-slug> cat /app/logs/test.log
   # Should output: "test"
   ```

**Success Criteria**:
- Data persists across container restarts
- Files owned by UID 1000 inside container

---

## Integration Points

### SAP-005 (ci-cd-workflows)

Docker testing in GitHub Actions workflows:
```yaml
# .github/workflows/test.yml
- name: Build test image
  uses: docker/build-push-action@v5
  with:
    file: ./Dockerfile.test
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

See: [ci-cd-workflows/AGENTS.md](../ci-cd-workflows/AGENTS.md)

### SAP-008 (automation-scripts)

Use `just` commands for Docker operations:
```bash
just docker-build         # Build production image
just docker-test          # Build and run tests in Docker
just docker-run           # Run via docker-compose
just docker-clean         # Clean up images/containers
```

See: [automation-scripts/AGENTS.md](../automation-scripts/AGENTS.md)

### SAP-010 (memory-system)

Enable A-MEM volume mounts in docker-compose.yml:
```yaml
volumes:
  - ./.chora/memory/events:/app/.chora/memory/events
  - ./.chora/memory/knowledge:/app/.chora/memory/knowledge
```

See: [memory-system/AGENTS.md](../memory-system/AGENTS.md)

---

## Decision Trees

### When to use Dockerfile vs Dockerfile.test?

```
Is this for production deployment?
├─ Yes → Use Dockerfile (multi-stage, wheel build)
└─ No → Is this for CI/CD testing?
    ├─ Yes → Use Dockerfile.test (editable install, dev deps)
    └─ No → Use Dockerfile (safer default)
```

### When to use docker-compose vs docker run?

```
Does the project need multiple services (e.g., n8n, nginx)?
├─ Yes → Use docker-compose (orchestration)
└─ No → Does it need volume persistence?
    ├─ Yes → Use docker-compose (easier volume management)
    └─ No → Use docker run (simpler for single service)
```

### When to enable multi-architecture builds?

```
Will this run on Apple Silicon (M1/M2)?
├─ Yes → Enable multi-arch (amd64 + arm64)
└─ No → Will this run on AWS Graviton (ARM64)?
    ├─ Yes → Enable multi-arch
    └─ No → Single-arch (amd64) sufficient
```

---

## Common Pitfalls

### Pitfall 1: Building Without .dockerignore

**Scenario**: Agent builds Docker image without creating `.dockerignore`, sends huge build context (includes .git/, venv/, docs/).

**Impact**: Build context 850MB (instead of 15MB), build takes 5 minutes (instead of 30 seconds).

**Fix**: Create .dockerignore BEFORE building:
```bash
cat > .dockerignore <<EOF
.git/
venv/
__pycache__/
*.pyc
.pytest_cache/
docs/
*.md
!README.md
node_modules/
.DS_Store
.vscode/
.idea/
EOF
```

**Why it matters**: Build context affects build speed and image size. Without .dockerignore, builds take 5-10 minutes instead of 30-60 seconds (81% size reduction).

### Pitfall 2: Not Using Multi-Stage Builds

**Scenario**: Agent uses single-stage Dockerfile, includes build tools in production image, creates 500MB+ images.

**Impact**: Image 520MB (includes gcc, build-essential), 3x larger than necessary.

**Fix**: Use multi-stage build (builder + runtime):
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels .

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*
CMD ["<project-slug>"]
```

**Why it matters**: Multi-stage builds separate build tools from runtime. Single-stage images are 2-3x larger, slower to pull, larger attack surface (65% reduction).

### Pitfall 3: Running as Root User

**Scenario**: Agent creates Dockerfile without non-root user, container runs as root (UID 0), security issue.

**Impact**: If container compromised, attacker has root access. Volume permissions fail (root writes, user can't read).

**Fix**: Create and use non-root user (UID 1000):
```dockerfile
# Create non-root user
RUN useradd --create-home --uid 1000 appuser

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

**Why it matters**: Running as root violates security best practices. Root containers have full system access if compromised.

### Pitfall 4: Not Testing Locally Before CI

**Scenario**: Agent pushes Dockerfile changes to GitHub, CI fails, wastes 5-10 minutes waiting for CI feedback.

**Impact**: 10-15 minutes wasted per iteration (5 min CI wait × 2-3 iterations).

**Fix**: Test Docker build LOCALLY before pushing:
```bash
# 1. Build locally (30 seconds)
docker build -t test:latest .

# 2. Test image
docker run --rm test:latest python --version

# 3. Run tests in Docker
docker build -t test:test -f Dockerfile.test .
docker run --rm test:test

# 4. NOW commit and push (CI will pass)
git add Dockerfile
git commit -m "update: upgrade Python to 3.12"
git push origin feature-branch
```

**Why it matters**: Local Docker testing provides instant feedback (30-60 seconds vs 5-10 minutes CI).

### Pitfall 5: Forgetting Volume Permissions (UID Mismatch)

**Scenario**: Agent uses docker-compose with volume mounts, container can't write to volumes because of UID mismatch.

**Impact**: "Permission denied writing to /app/logs/app.log" errors. Host directory owned by user (UID 501), container runs as appuser (UID 1000).

**Fix**: Set correct permissions on host volumes BEFORE starting:
```bash
# 1. Create directories
mkdir -p logs data .chora/memory

# 2. Set ownership to UID 1000 (container user)
sudo chown -R 1000:1000 logs/ data/ .chora/memory/

# 3. Verify
ls -lan logs/
# drwxr-xr-x  2 1000 1000  64 Nov 4 12:00 logs/

# 4. NOW start containers
docker-compose up -d
```

**Why it matters**: UID mismatch breaks volume writes. Setting permissions correctly takes 1 minute, debugging permission errors takes 10-30 minutes.

---

## Related Documents

**This SAP (docker-operations)**:
- [capability-charter.md](capability-charter.md) - Problem statement, ROI (39x-47x)
- [protocol-spec.md](protocol-spec.md) - Multi-stage builds, CI cache, security
- [awareness-guide.md](awareness-guide.md) - 8 agent workflows, decision trees
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adoption tracking

**Docker Artifacts** (static-template):
- [Dockerfile](../../../static-template/Dockerfile) - Production multi-stage image
- [Dockerfile.test](../../../static-template/Dockerfile.test) - CI test image
- [docker-compose.yml](../../../static-template/docker-compose.yml) - Orchestration
- [.dockerignore](../../../static-template/.dockerignore) - Build optimization
- [DOCKER_BEST_PRACTICES.md](../../../static-template/DOCKER_BEST_PRACTICES.md) - Guidance

**Related SAPs**:
- [SAP-003: project-bootstrap](../project-bootstrap/AGENTS.md) - Project generation with Docker
- [SAP-005: ci-cd-workflows](../ci-cd-workflows/AGENTS.md) - GitHub Actions Docker integration
- [SAP-008: automation-scripts](../automation-scripts/AGENTS.md) - `just docker-*` commands
- [SAP-010: memory-system](../memory-system/AGENTS.md) - A-MEM volume mounts

---

**Version History**:
- **1.0.0** (2025-11-04): Initial AGENTS.md with 8 workflows, progressive loading, research integration
