# Claude Docker Assistance Patterns

**Purpose:** Claude-specific patterns for Docker containerization and deployment assistance.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic Docker guide.

---

## Claude's Docker Strengths

Claude excels at Docker tasks because:

- **Multi-stage build optimization** - Understands layer caching and size reduction
- **Dockerfile best practices** - Applies security and efficiency patterns
- **Troubleshooting** - Excellent at diagnosing container issues
- **docker-compose orchestration** - Can design complex service interactions
- **Documentation** - Generates clear deployment documentation

---

## Dockerfile Generation with Claude

### Complete Dockerfile Request Pattern

```markdown
# Dockerfile Generation Request

## Application Context
- **Language:** Python {{ python_version }}
- **Framework:** FastMCP / MCP Server
- **Dependencies:** [from pyproject.toml]
- **Entry point:** `python -m {{ package_name }}.server`

## Requirements
- Multi-stage build (builder + runtime)
- Minimal final image size
- Non-root user
- Health check
- Labels for metadata

## Security Requirements
- No root user in final image
- Minimal attack surface
- Only necessary dependencies in runtime
- Pinned base image versions

## Example Pattern
Follow Dockerfile patterns in this project or similar chora-base projects.

---

Claude, generate optimized Dockerfile:
1. Use multi-stage build
2. Optimize layer caching
3. Minimize final image size
4. Include security best practices
5. Add comprehensive comments
6. Include health check
```

### Expected Dockerfile Pattern

```dockerfile
# syntax=docker/dockerfile:1
# Multi-stage build for {{ project_name }}

#################################################################
# Stage 1: Builder
#################################################################
FROM python:{{ python_version }}-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements first (layer caching)
COPY pyproject.toml README.md ./
COPY src/ src/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

#################################################################
# Stage 2: Runtime
#################################################################
FROM python:{{ python_version }}-slim

# Create non-root user
RUN groupadd -r {{ package_name }} && \
    useradd -r -g {{ package_name }} {{ package_name }}

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown={{ package_name }}:{{ package_name }} src/ /app/src/

# Set environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    {{ package_name | upper }}_LOG_LEVEL=INFO

# Switch to non-root user
USER {{ package_name }}
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import {{ package_name }}; print('healthy')" || exit 1

# Run application
CMD ["python", "-m", "{{ package_name }}.server"]

# Labels
LABEL org.opencontainers.image.title="{{ project_name }}" \
      org.opencontainers.image.description="{{ description }}" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.authors="{{ author_email }}"
```

---

## docker-compose Generation

### docker-compose Request Pattern

```markdown
# docker-compose.yml Generation

## Services Needed
1. **{{ package_name }}** - Main MCP server
2. **[dependency]** - If external dependencies needed (Redis, PostgreSQL, etc.)

## Requirements
- Development and production profiles
- Volume mounts for development
- Environment variable configuration
- Health checks
- Network isolation

## Example
Reference docker-compose patterns in chora-base projects.

---

Claude, generate docker-compose.yml:
1. Development profile with hot reload
2. Production profile optimized
3. Proper volume mounts
4. Environment variables from .env
5. Health checks for all services
6. Depends_on with conditions
```

---

## Docker Build Optimization

### Layer Caching Optimization

**Request pattern:**
```markdown
"Optimize Dockerfile for layer caching:

Current Dockerfile:
[Paste current Dockerfile]

Problems:
- Dependencies reinstalled on code changes
- Large intermediate layers
- No caching of pip packages

Optimize by:
1. Copy requirements before code
2. Use --mount=type=cache for pip
3. Minimize layer count
4. Order from least to most frequently changed
```

### Image Size Reduction

**Request pattern:**
```markdown
"Reduce Docker image size:

Current image: XXX MB (too large)
Target: < XXX MB

Analyze and optimize:
1. Use smaller base image (alpine or slim)
2. Multi-stage build to exclude build tools
3. Remove unnecessary files
4. Combine RUN commands to reduce layers
5. Use .dockerignore

Show before/after size comparison."
```

---

## Troubleshooting with Claude

### Container Build Issues

**Request pattern:**
```markdown
# Docker Build Failure

Error:
```
[Paste full build error]
```

Context:
- Dockerfile: [paste Dockerfile]
- Building for: [platform - amd64/arm64]
- Base image: [image:tag]
- Recent changes: [what changed]

Claude, diagnose and fix:
1. Identify root cause
2. Explain why error occurs
3. Provide corrected Dockerfile
4. Suggest prevention strategy
```

### Runtime Container Issues

**Request pattern:**
```markdown
# Container Runtime Issue

Problem: [Container exits immediately / Not responding / etc.]

Logs:
```bash
$(docker logs container-name)
```

Inspect:
```bash
$(docker inspect container-name)
```

Context:
- Image: [image:tag]
- Platform: [amd64/arm64]
- Environment vars: [relevant vars]

Claude, diagnose:
1. Analyze logs and inspect output
2. Identify issue
3. Suggest fix
4. Provide corrected configuration
```

---

## Security Best Practices

### Security Audit Request

```markdown
"Audit Dockerfile for security issues:

Current Dockerfile:
[Paste Dockerfile]

Check for:
- [ ] Running as non-root user
- [ ] No secrets in layers
- [ ] Minimal attack surface
- [ ] Pinned base image versions
- [ ] No unnecessary tools in runtime
- [ ] Security updates applied
- [ ] Principle of least privilege

Provide security report and recommendations."
```

### Expected Security Patterns

```dockerfile
# Security best practices Claude should apply:

# 1. Pinned base images
FROM python:3.11.5-slim AS builder  # Specific version, not 'latest'

# 2. Non-root user
RUN useradd -r -u 1000 appuser
USER appuser

# 3. No secrets in build
# Use build args or runtime secrets, never COPY secrets

# 4. Minimal runtime dependencies
# Only install what's needed for runtime, not build tools

# 5. Read-only filesystem where possible
VOLUME /app/data
# Application code read-only, only data directory writable
```

---

## Multi-Platform Builds

### Multi-Platform Request

```markdown
"Configure multi-platform Docker build:

Target platforms:
- linux/amd64 (Intel/AMD servers)
- linux/arm64 (ARM servers, Apple Silicon)

Requirements:
1. Use buildx for multi-platform
2. Handle platform-specific dependencies
3. Test both platforms
4. Push to registry with manifest

Provide:
- Updated Dockerfile (if platform-specific changes needed)
- Build command for both platforms
- Testing strategy
```

### Build Command Pattern

```bash
# Multi-platform build
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t {{ project_slug }}:latest \
  --push \
  .
```

---

## Development Workflow with Docker

### Development Container Pattern

```markdown
"Create development Docker setup:

Requirements:
1. Hot reload for code changes
2. Volume mount source code
3. Debugger support
4. Development dependencies included
5. Fast iteration cycle

docker-compose.dev.yml should enable:
- Mount ./src:/app/src
- Install dev dependencies
- Expose debug ports
- Keep container running for iterative development
```

### Expected dev docker-compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  {{ package_name }}-dev:
    build:
      context: .
      target: builder  # Use builder stage with dev tools
    volumes:
      - ./src:/app/src:ro  # Mount source for hot reload
      - ./tests:/app/tests:ro
    environment:
      - {{ package_name | upper }}_DEBUG=1
      - {{ package_name | upper }}_LOG_LEVEL=DEBUG
    ports:
      - "5678:5678"  # debugpy port
    command: >
      sh -c "pip install -e .[dev] &&
             python -m debugpy --listen 0.0.0.0:5678 -m {{ package_name }}.server"
```

---

## CI/CD Integration

### GitHub Actions Docker Build

```markdown
"Generate GitHub Actions workflow for Docker:

Triggers:
- Push to main → build and push latest
- Tag push → build and push versioned tag
- PR → build only (no push)

Requirements:
1. Multi-platform build
2. Layer caching for faster builds
3. Security scanning (trivy/snyk)
4. Push to Docker Hub / GHCR

Generate .github/workflows/docker.yml"
```

---

## Docker Compose Service Orchestration

### Complex Service Setup

```markdown
"Design docker-compose for services:

Services:
1. {{ package_name }} - MCP server
2. [dependency-1] - [description]
3. [dependency-2] - [description]

Requirements:
- Proper startup order (depends_on with healthchecks)
- Network isolation
- Shared volumes where needed
- Environment configuration
- Resource limits

Include:
- Service definitions
- Networks
- Volumes
- Health checks
- Restart policies
```

---

## Performance Optimization

### Build Performance

```markdown
"Optimize Docker build performance:

Current build time: XX minutes (too slow)

Optimize:
1. Use BuildKit features (--mount=type=cache)
2. Optimize layer caching
3. Parallel multi-stage builds
4. Minimal base images
5. .dockerignore to exclude unnecessary files

Target: < X minutes build time"
```

### Runtime Performance

```markdown
"Optimize container runtime performance:

Issues:
- [Slow startup / High memory / etc.]

Profile and optimize:
1. Analyze resource usage
2. Optimize entrypoint
3. Configure resource limits appropriately
4. Use appropriate base image
5. Minimize runtime overhead
```

---

## Common Docker Patterns for {{ project_name }}

### Pattern: MCP Server Container

```dockerfile
# MCP server specific patterns
# - Expose stdio for MCP protocol
# - No need for network ports usually
# - Handle graceful shutdown
# - Logging to stdout/stderr

FROM python:{{ python_version }}-slim
# ... build stages ...

# MCP servers typically use stdio, not network
# So no EXPOSE needed unless providing HTTP interface

# Handle signals for graceful shutdown
STOPSIGNAL SIGTERM

CMD ["python", "-m", "{{ package_name }}.server"]
```

### Pattern: Development Debugging

```yaml
# docker-compose.debug.yml
services:
  app-debug:
    build:
      target: builder
    volumes:
      - ./src:/app/src
    ports:
      - "5678:5678"  # debugpy
    environment:
      - PYTHONBREAKPOINT=debugpy.breakpoint
    command: >
      python -m debugpy --wait-for-client --listen 0.0.0.0:5678
      -m {{ package_name }}.server
```

---

## Troubleshooting Common Issues

### Issue: "exec format error" on Different Architecture

**Diagnosis:**
```markdown
"Getting 'exec format error':

Cause: Image built for different architecture (amd64 vs arm64)

Solutions:
1. Build for correct platform: --platform linux/amd64
2. Use multi-platform build
3. Use platform-agnostic base images

Which approach for this project?"
```

### Issue: Container Exits Immediately

**Diagnosis:**
```markdown
"Container exits with code X:

Check:
1. CMD/ENTRYPOINT syntax
2. Application startup errors (check logs)
3. Signal handling
4. Dependencies available
5. User permissions

Logs:
[Paste docker logs output]

Claude, diagnose exit cause and fix."
```

---

## Best Practices for Claude Docker Requests

### ✅ Do's

1. **Provide context** - Base images, dependencies, requirements
2. **Specify platform** - amd64, arm64, or both
3. **Include errors** - Full error messages, logs
4. **Reference patterns** - Point to example Dockerfiles
5. **State constraints** - Size limits, security requirements
6. **Request optimization** - Ask for layer caching, size reduction

### ❌ Don'ts

1. **Don't omit details** - "Make a Dockerfile" vs detailed requirements
2. **Don't skip security** - Always request security best practices
3. **Don't ignore platform** - Specify target architectures
4. **Don't forget .dockerignore** - Exclude unnecessary files
5. **Don't use latest tags** - Pin versions for reproducibility

---

**See Also:**
- [../CLAUDE.md](../CLAUDE.md) - Project-level Claude patterns
- [AGENTS.md](AGENTS.md) - Generic Docker guide
- [../../claude/FRAMEWORK_TEMPLATES.md](../../claude/FRAMEWORK_TEMPLATES.md) - Task templates in pattern library

---

**Version:** 3.3.0
**Last Updated:** 2025-10-26
