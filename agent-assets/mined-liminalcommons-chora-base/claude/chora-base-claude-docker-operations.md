---
sap_id: SAP-011
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-110"    # Quick Start + Containerize Workflow
  phase_2: "lines 111-200"  # docker-compose + Debugging Workflows
  phase_3: "full"           # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 12000
---

# Docker Operations (SAP-011) - Claude-Specific Awareness

**SAP ID**: SAP-011
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-011?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - 5 commands to build and deploy in 2 minutes
- 📚 **CLI Commands** - 8 docker-related justfile recipes
- 🎯 **Multi-Stage Builds** - 40% smaller images with wheel distribution
- ⚡ **CI Optimization** - 6x faster builds with layer caching
- 🔧 **Troubleshooting** - 4 common problems with solutions

**This CLAUDE.md provides**: Claude Code-specific workflows using Read, Edit, Bash, and Write tools for Docker operations.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for Docker operations.

### First-Time Docker Setup

1. Read [AGENTS.md](AGENTS.md) for generic Docker workflows
2. Use this file for Claude Code tool integration (Read, Edit, Bash, Write for Docker operations)
3. Follow 3-step process: Copy Docker files → Customize → Test locally → Deploy

### Session Resumption

- Check Dockerfile, Dockerfile.test, docker-compose.yml for existing Docker configuration
- Use Bash tool for docker commands (build, run, logs, inspect)
- Use Edit tool to update Dockerfiles (multi-stage, security, optimization)
- Use Read tool to debug container issues (read logs, inspect configuration)

---

## Claude Code Docker Workflows

### Workflow 1: Containerizing a Project with Claude Code

```markdown
User: "Containerize this Python project for production"

Claude (Phase 1: Check Existing - 0-5k tokens):
1. Check existing Docker files:
   Bash: ls Dockerfile Dockerfile.test docker-compose.yml .dockerignore
2. Read project structure:
   Bash: ls -la src/ tests/
3. Read pyproject.toml (identify package name, dependencies):
   Read pyproject.toml

Claude (Phase 2: Copy Docker Files - 5-15k tokens):
4. If Docker files missing, copy from static-template:
   Bash: cp /path/to/static-template/Dockerfile .
   Bash: cp /path/to/static-template/Dockerfile.test .
   Bash: cp /path/to/static-template/docker-compose.yml .
   Bash: cp /path/to/static-template/.dockerignore .
5. List copied files:
   Bash: ls -la Dockerfile* docker-compose.yml .dockerignore

Claude (Phase 3: Customize Dockerfile - 15-30k tokens):
6. Read Dockerfile to identify customization points:
   Read Dockerfile
7. Edit Dockerfile to update project name:
   Edit Dockerfile
   # old_string: LABEL org.opencontainers.image.title="{{ project_slug }}"
   # new_string: LABEL org.opencontainers.image.title="chora-utils"
8. Edit Dockerfile CMD to match project entrypoint:
   Edit Dockerfile
   # old_string: CMD ["{{ project_slug }}"]
   # new_string: CMD ["chora-utils"]
9. Verify customization:
   Read Dockerfile (check project name, CMD)

Claude (Phase 4: Build and Test - 30-50k tokens):
10. Build production image:
    Bash: docker build -t chora-utils:latest .
11. Check image size:
    Bash: docker images chora-utils:latest --format "{{.Size}}"
    # Target: ≤250MB
12. Test image (MCP server example):
    Bash: docker run --rm chora-utils:latest chora-utils --version
13. Verify output (should show version)

Claude (Phase 5: Optimize if Needed - 50-70k tokens):
14. If image >250MB, check .dockerignore:
    Read .dockerignore
15. If .dockerignore missing entries, edit:
    Edit .dockerignore
    # Add missing exclusions: venv/, docs/, .git/
16. Rebuild with optimizations:
    Bash: docker build --no-cache -t chora-utils:latest .
17. Verify size reduction:
    Bash: docker images chora-utils:latest --format "{{.Size}}"

Claude (response to user):
"Containerized chora-utils for production:

✅ Docker files created:
   - Dockerfile (multi-stage: builder + runtime, 180MB)
   - Dockerfile.test (CI-optimized with dev dependencies)
   - docker-compose.yml (orchestration with volumes)
   - .dockerignore (build context optimization)

✅ Production image built:
   - Image: chora-utils:latest
   - Size: 180MB ✅ (target ≤250MB)
   - Security: Non-root user (UID 1000) ✅
   - Health check: Import-based ✅

✅ Image tested:
   - Command: chora-utils --version
   - Output: chora-utils 1.0.0 ✅

Next: Deploy with docker-compose up -d"

Result: Production-ready Docker image (180MB, multi-stage, secure)
```

---

### Workflow 2: Setting Up docker-compose with Claude Code

```markdown
User: "Set up docker-compose for local deployment"

Claude (Phase 1: Check Existing - 0-5k tokens):
1. Check docker-compose.yml exists:
   Bash: ls docker-compose.yml
2. Read current configuration:
   Read docker-compose.yml

Claude (Phase 2: Customize docker-compose - 5-15k tokens):
3. Edit service name:
   Edit docker-compose.yml
   # old_string: {{ project_slug }}:
   # new_string: chora-utils:
4. Edit environment variables:
   Edit docker-compose.yml
   # old_string: {{ PACKAGE_NAME_UPPER }}_LOG_LEVEL
   # new_string: CHORA_UTILS_LOG_LEVEL
5. Verify customization:
   Read docker-compose.yml (check service name, env vars)

Claude (Phase 3: Create .env File - 15-25k tokens):
6. Check if .env.example exists:
   Bash: ls .env.example
7. If exists, copy to .env:
   Bash: cp .env.example .env
8. If not exists, create .env with defaults:
   Write .env
   # Content:
   LOG_LEVEL=INFO
   PORT=8000
   # Add project-specific env vars

Claude (Phase 4: Set Up Volumes - 25-35k tokens):
9. Create volume directories:
   Bash: mkdir -p logs data .chora/memory/events .chora/memory/knowledge
10. Set correct permissions (UID 1000 for container):
    Bash: sudo chown -R 1000:1000 logs/ data/ .chora/memory/
11. Verify ownership:
    Bash: ls -lan logs/
    # Should show UID 1000

Claude (Phase 5: Start and Verify - 35-50k tokens):
12. Start services:
    Bash: docker-compose up -d
13. Check service status:
    Bash: docker-compose ps
    # Should show "Up" or "Up (healthy)"
14. View logs:
    Bash: docker-compose logs -f chora-utils
    # Check for startup messages, no errors
15. Test health check:
    Bash: docker inspect --format='{{json .State.Health}}' chora-utils | jq
    # Should show "healthy"

Claude (response to user):
"Set up docker-compose for local deployment:

✅ docker-compose.yml customized:
   - Service: chora-utils
   - Ports: 8000:8000
   - Volumes: logs/, data/, .chora/memory/
   - Health check: Import-based (30s interval)
   - Restart: unless-stopped

✅ Environment configured:
   - .env file created with defaults
   - LOG_LEVEL=INFO
   - PORT=8000

✅ Volumes set up:
   - logs/ (UID 1000) ✅
   - data/ (UID 1000) ✅
   - .chora/memory/ (UID 1000) ✅

✅ Service running:
   - Status: Up (healthy) ✅
   - Logs: No errors ✅

Access: http://localhost:8000"

Result: docker-compose deployment with health checks and persistence
```

---

### Workflow 3: Debugging Container Issues with Claude Code

```markdown
User: "Container keeps crashing after startup"

Claude (Phase 1: Check Container Status - 0-5k tokens):
1. List containers:
   Bash: docker-compose ps
   # Or: docker ps -a
2. Check exit code:
   Bash: docker inspect --format='{{.State.ExitCode}}' chora-utils
   # Non-zero = crash

Claude (Phase 2: Read Logs - 5-20k tokens):
3. View container logs:
   Bash: docker-compose logs --tail=100 chora-utils
   # Or: docker logs chora-utils
4. Identify error type:
   # "Module not found" → Import issue
   # "Permission denied" → Volume permission issue
   # "No such file" → Missing file in container
   # "Address already in use" → Port conflict

Claude (Phase 3: Diagnose Issue - 20-40k tokens):
# Scenario A: Module not found
5. Run interactive shell:
   Bash: docker run -it --rm chora-utils:latest /bin/bash
6. Test import manually:
   Bash: docker run -it --rm chora-utils:latest python -c "import chora_utils; print(chora_utils.__version__)"
7. If import fails, read Dockerfile to check wheel build:
   Read Dockerfile
8. Verify package name in pyproject.toml:
   Read pyproject.toml
   # Check: name = "chora-utils" (should match src/chora_utils/)

# Scenario B: Permission denied
5. Check volume permissions:
   Bash: docker exec chora-utils ls -la /app/logs
   # Should show UID 1000, not root (0)
6. Check host permissions:
   Bash: ls -lan logs/
   # Should show UID 1000
7. If wrong UID, fix on host:
   Bash: sudo chown -R 1000:1000 logs/ data/ .chora/memory/

# Scenario C: Health check failing
5. Test health check command manually:
   Bash: docker exec chora-utils python -c "import chora_utils; assert chora_utils.__version__"
6. If fails, check if __version__ defined:
   Read src/chora_utils/__init__.py
   # Should have: __version__ = "1.0.0"

Claude (Phase 4: Fix Issue - 40-60k tokens):
# Fix based on diagnosis
9. If module issue, rebuild with correct package name:
   Edit Dockerfile
   # Verify wheel build step
10. If permission issue, set correct ownership:
    Bash: sudo chown -R 1000:1000 logs/ data/ .chora/memory/
11. If health check issue, add __version__:
    Edit src/chora_utils/__init__.py
    # Add: __version__ = "1.0.0"

Claude (Phase 5: Rebuild and Test - 60-75k tokens):
12. Rebuild image:
    Bash: docker-compose build
13. Restart service:
    Bash: docker-compose up -d
14. Monitor logs in real-time:
    Bash: docker-compose logs -f chora-utils
15. Verify container stays up:
    Bash: docker-compose ps
    # Should show "Up (healthy)"

Claude (response to user):
"Fixed container crash issue:

Issue: ModuleNotFoundError: No module named 'chora_utils'
Root cause: Package name mismatch (pyproject.toml vs src/)

Fix:
  - Verified pyproject.toml name = "chora-utils" ✅
  - Verified src/chora_utils/ directory ✅
  - Rebuilt image with --no-cache
  - Container now starts successfully ✅

Status:
  - Container: Up (healthy) ✅
  - Health check: Passing ✅
  - Logs: No errors ✅"

Result: Container runs successfully after fix
```

---

## Claude-Specific Tips

### Tip 1: Use Read Before Edit for Dockerfiles

**Pattern**:
```bash
# ALWAYS read Dockerfile before editing
Read Dockerfile

# Then edit specific sections (not full rewrite)
Edit Dockerfile
# old_string: CMD ["{{ project_slug }}"]
# new_string: CMD ["chora-utils"]
```

**Why**: Dockerfiles have complex multi-stage structure; Read ensures you understand current state before editing

---

### Tip 2: Use Bash for All docker Commands

**Pattern**:
```bash
# Build
Bash: docker build -t myproject:latest .

# Run
Bash: docker run --rm myproject:latest --version

# docker-compose
Bash: docker-compose up -d
Bash: docker-compose logs -f myproject

# Debug
Bash: docker logs myproject
Bash: docker exec -it myproject /bin/bash
Bash: docker inspect myproject
```

**Why**: Bash tool executes docker/docker-compose commands for container management

---

### Tip 3: Check Image Size After Build

**Pattern**:
```bash
# After building, ALWAYS check size
Bash: docker build -t myproject:latest .
Bash: docker images myproject:latest --format "{{.Size}}"

# Alert user if >250MB
# If too large, check .dockerignore:
Read .dockerignore
```

**Why**: Large images (>500MB) indicate missing .dockerignore or single-stage build; early detection prevents deployment issues

---

### Tip 4: Verify Volume Permissions Before Starting

**Pattern**:
```bash
# BEFORE docker-compose up, set permissions:
Bash: mkdir -p logs data .chora/memory
Bash: sudo chown -R 1000:1000 logs/ data/ .chora/memory/

# Verify:
Bash: ls -lan logs/
# Should show UID 1000

# THEN start:
Bash: docker-compose up -d
```

**Why**: Wrong UID causes "Permission denied" errors; fixing permissions first prevents runtime issues

---

### Tip 5: Test Locally Before Pushing to CI

**Pattern**:
```bash
# BEFORE committing Dockerfile changes:

# 1. Build locally
Bash: docker build -t test:latest .

# 2. Test image
Bash: docker run --rm test:latest python --version

# 3. Run tests in Docker
Bash: docker build -t test:test -f Dockerfile.test .
Bash: docker run --rm test:test

# 4. If all pass, THEN commit
Bash: git add Dockerfile Dockerfile.test
Bash: git commit -m "feat: Add Docker support"
```

**Why**: Local Docker testing provides instant feedback (30s vs 5min CI); catches errors before pushing

---

## Common Pitfalls for Claude Code

### Pitfall 1: Overwriting Dockerfile Instead of Editing

**Problem**: Using Write tool to replace Dockerfile, losing multi-stage structure and security configuration

**Fix**: Use Edit tool for incremental changes

```bash
# BAD
Write Dockerfile  # Overwrites entire file, loses builder stage

# GOOD
Read Dockerfile  # Check current structure
Edit Dockerfile  # Modify specific sections (CMD, LABEL, etc.)
```

---

### Pitfall 2: Not Creating .dockerignore Before Building

**Problem**: Building without .dockerignore, sending 850MB build context (includes .git/, venv/, docs/)

**Fix**: Create .dockerignore FIRST, then build

```bash
# BEFORE building:
Bash: ls .dockerignore
# If missing:
Bash: cp /path/to/static-template/.dockerignore .

# THEN build:
Bash: docker build -t myproject:latest .
```

**Why**: Build context affects build speed (5min vs 30s) and image size (81% reduction)

---

### Pitfall 3: Not Setting Volume Permissions (UID 1000)

**Problem**: Starting docker-compose without setting UID 1000 on volumes, container can't write

**Fix**: Set permissions BEFORE starting

```bash
# BEFORE docker-compose up:
Bash: mkdir -p logs data .chora/memory
Bash: sudo chown -R 1000:1000 logs/ data/ .chora/memory/

# THEN start:
Bash: docker-compose up -d
```

**Why**: Container runs as UID 1000 (non-root), host directories must match to allow writes

---

### Pitfall 4: Not Reading Logs for Crash Diagnosis

**Problem**: Container crashes, but not reading logs to understand why

**Fix**: ALWAYS read logs first

```bash
# ALWAYS read logs for crashed containers:
Bash: docker logs myproject
# Or:
Bash: docker-compose logs myproject

# Look for: ModuleNotFoundError, Permission denied, Address in use
```

**Why**: Logs reveal root cause immediately; saves 10-30 minutes of guessing

---

### Pitfall 5: Not Testing Health Check Command

**Problem**: Health check failing, container marked unhealthy, but didn't test health check command manually

**Fix**: Test health check command in running container

```bash
# Test health check manually:
Bash: docker exec myproject python -c "import mypackage; assert mypackage.__version__"

# If fails, check if __version__ defined:
Read src/mypackage/__init__.py
# Should have: __version__ = "1.0.0"
```

**Why**: Health checks fail silently; manual testing reveals missing __version__ or import issues

---

## Support & Resources

**SAP-011 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic Docker workflows (8 workflows)
- [Capability Charter](capability-charter.md) - Design principles, ROI (39x-47x)
- [Protocol Spec](protocol-spec.md) - Multi-stage builds, CI cache, security contracts
- [Awareness Guide](awareness-guide.md) - Agent workflows, decision trees, common pitfalls
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Docker adoption tracking

**External Resources**:
- [Docker Documentation](https://docs.docker.com/) - Official docs
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Compose reference
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Official best practices
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/) - Dockerfile syntax

**Related SAPs**:
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - GitHub Actions Docker integration
- [SAP-008 (automation-scripts)](../automation-scripts/) - `just docker-*` commands
- [SAP-010 (memory-system)](../memory-system/) - A-MEM volume mounts

**Templates**:
- `static-template/Dockerfile` - Production multi-stage image
- `static-template/Dockerfile.test` - CI test image
- `static-template/docker-compose.yml` - Orchestration template
- `static-template/.dockerignore` - Build optimization template

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-011
  - Claude Code workflows (containerize, docker-compose setup, debugging)
  - Tool usage patterns (Read Dockerfiles, Edit incremental, Bash for docker commands)
  - Claude-specific tips (Read before Edit, check size, verify permissions, test locally)
  - Common pitfalls (overwrite vs edit, .dockerignore, UID 1000, read logs, test health checks)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic Docker workflows
2. Review [protocol-spec.md](protocol-spec.md) for multi-stage builds and security contracts
3. Check [capability-charter.md](capability-charter.md) for design principles
4. Containerize project: Copy Docker files → Customize → Test locally → Deploy
