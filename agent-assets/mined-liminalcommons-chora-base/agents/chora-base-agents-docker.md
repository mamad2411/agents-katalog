# Docker Operations for {{ project_name }}

**Purpose**: Docker containerization guide for deployment and development.

**Parent**: See [../AGENTS.md](../AGENTS.md) for project overview and other topics.

**For Claude users**: See [CLAUDE.md](CLAUDE.md) for Claude-specific Docker assistance patterns.

---

## Quick Reference

- **Build image**: `{% if include_justfile %}just docker-build{% else %}docker build -t {{ project_slug }}:latest .{% endif %}`
- **Verify image**: `{% if include_justfile %}just docker-verify{% else %}docker run --rm {{ project_slug }}:latest python -c "import {{ package_name }}"{% endif %}`
- **Start services**: `{% if include_justfile %}just docker-compose-up{% else %}docker-compose up -d{% endif %}`
- **View logs**: `{% if include_justfile %}just docker-logs{% else %}docker-compose logs -f{% endif %}`

---

## Docker Operations

**When enabled** (`include_docker: true`), {{ project_name }} includes production-ready Docker support with ergonomic commands.

### Discovery

```bash
{% if include_justfile -%}
# List all Docker commands
just --list | grep docker

{% endif -%}# Available commands:
# - docker-build [TAG]          Build production image
# - docker-build-multi [TAG]    Build for amd64 + arm64
# - docker-verify [TAG]          Smoke test image health
# - docker-shell [TAG]           Interactive debugging shell
# - docker-test                  Run tests in isolated container
# - docker-compose-up            Start all services
# - docker-compose-down          Stop all services
# - docker-logs                  View service logs
# - docker-clean                 Remove images and containers
{% if docker_strategy == 'production' -%}
# - docker-push REGISTRY TAG     Push to container registry
# - docker-release VERSION REG   Full release workflow
{% endif -%}
```

### Common Workflows

```bash
{% if include_justfile -%}
# Build and verify image
just docker-build
just docker-verify

# Run services locally
just docker-compose-up
just docker-logs

# Stop services
just docker-compose-down

# Clean up
just docker-clean
{% else -%}
# Build and verify image
docker build -t {{ project_slug }}:latest .
docker run --rm {{ project_slug }}:latest python -c "import {{ package_name }}; assert {{ package_name }}.__version__"

# Run services
docker-compose up -d
docker-compose logs -f

# Stop services
docker-compose down
{% endif -%}
```

---

## Detailed Documentation

**For comprehensive Docker workflows:** See {% if include_docker %}[DOCKER_BEST_PRACTICES.md](../DOCKER_BEST_PRACTICES.md){% else %}project documentation{% endif %}

---

## Adopter Responsibilities (Wiring Required)

{% if project_type == 'web_service' -%}
- [ ] Implement `/health` endpoint in your application
- [ ] Test health check returns 200 OK when healthy
{% elif project_type == 'mcp_server' -%}
- [ ] Ensure `{{ package_name }}.__version__` is defined
- [ ] Test import-based health check works
{% endif -%}
- [ ] Configure project-specific environment variables in `.env`
- [ ] Set service dependencies in `docker-compose.yml` (if using multiple services)
{% if docker_strategy == 'production' -%}
- [ ] Configure registry credentials for `docker-push` (if publishing)
- [ ] Test multi-architecture builds (if deploying to ARM64)
{% endif -%}

---

## Image Optimization Results

**Expected metrics (wheel builds):**
- **Size**: 150-250MB (40% smaller than naive builds)
- **Build time**: ~2-3 minutes (first build), ~30 seconds (cached)
- **Health check**: <100ms (import-based validation)
- **Multi-arch**: Native ARM64 support (Apple Silicon)

---

## Related Documentation

- **[Main AGENTS.md](../AGENTS.md)** - Project overview, architecture, common tasks
- **[Testing AGENTS.md](../tests/AGENTS.md)** - Testing instructions
{% if include_memory -%}
- **[Memory System AGENTS.md](../.chora/memory/AGENTS.md)** - Cross-session learning
{% endif -%}
- **[scripts/AGENTS.md](../scripts/AGENTS.md)** - Automation scripts reference

---

**End of Docker Operations Guide**

For questions or issues not covered here, see the main [AGENTS.md](../AGENTS.md) or [DOCKER_BEST_PRACTICES.md](../DOCKER_BEST_PRACTICES.md).
