---
name: configuration-file-parsing
description: >
  Use this skill when the task involves parsing, validating, or editing configuration files for cloud deployments,
  including render.yaml, Dockerfile, docker-compose.yml, JSON config files, and shell scripts like entrypoint.sh.
  
  Use when: A render.yaml needs to be created or modified for Render deployment; a Dockerfile requires dependency
  updates (e.g., adding curl, git, jq); an entrypoint.sh script needs health check improvements or syntax fixes;
  JSON/YAML configuration files need validation or structure changes; environment-specific config files need to be
  generated from templates.
  
  Don't use when: The task is about runtime environment variable access (use environment-variable-access instead);
  the task requires database schema or SQL work (use database-infraforge-database-infrastructure).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Configuration File Parsing Skill

## Overview

The Configuration File Parsing skill enables the Render Deployment Specialist agent to effectively parse, validate, modify, and generate configuration files essential for cloud deployments. This skill covers Render-specific YAML, Docker configurations, shell scripts, and general structured data formats.

## Capabilities

### YAML Configuration (render.yaml)
- **Service Definition**: Define web services, background workers, and cron jobs
- **Environment Variables**: Configure env vars, secrets, and build-time variables
- **Build & Start Commands**: Set up build pipelines and runtime commands
- **Scaling & Resources**: Configure instance types, autoscaling, and resource limits

### Docker Configuration (Dockerfile)
- **Base Image Selection**: Choose appropriate base images for the runtime
- **System Dependencies**: Install required packages (curl, git, jq, build-essential)
- **Multi-stage Builds**: Optimize image size with multi-stage builds
- **Health Check Integration**: Add Dockerfile HEALTHCHECK instructions

### Shell Scripts (entrypoint.sh)
- **Process Management**: Start multiple processes and keep container alive
- **Health Checks**: Implement curl-based health check loops with timeouts
- **Error Handling**: Add trap handlers, set -euo pipefail, and exit code management
- **Logging**: Prefix logs by process (e.g., `[API]`, `[WORKER]`) for clarity

### JSON Configuration
- **API Config Files**: Parse and generate API server configuration
- **Package Files**: Read and update package.json, requirements.txt, etc.
- **Secret Management**: Handle encrypted or templated JSON configs

## Common Patterns

### render.yaml Template
```yaml
services:
  - type: web
    name: paperclip-app
    runtime: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 8000
      - key: HERMES_MODE
        value: both
      - key: OPENROUTER_API_KEY
        fromSecret: openrouter_api_key
      - key: SUPABASE_URL
        fromSecret: supabase_url
      - key: SUPABASE_SERVICE_ROLE_KEY
        fromSecret: supabase_service_role_key
      - key: GITHUB_TOKEN
        fromSecret: github_token
    healthCheckPath: /health
    disk:
      name: tmp
      mountPath: /tmp
      sizeGB: 1
```

### Dockerfile with All Dependencies
```dockerfile
FROM python:3.11-slim

# Install system dependencies required for health checks and git operations
RUN apt-get update && apt-get install -y \
    curl \
    git \
    jq \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x docker/entrypoint.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["./docker/entrypoint.sh"]
```

### entrypoint.sh with Dual Process Management
```bash
#!/bin/bash
set -euo pipefail

# Configuration
API_PORT="${API_PORT:-8000}"
API_HOST="${API_HOST:-0.0.0.0}"
HEALTH_CHECK_URL="http://${API_HOST}:${API_PORT}/health"
MAX_HEALTH_CHECK_ATTEMPTS=30
HEALTH_CHECK_INTERVAL=5

# Log helper
log() {
  echo "[$(date -Iseconds)] $1"
}

# Check required environment variables
log "Checking required environment variables..."
required_vars=("OPENROUTER_API_KEY" "GITHUB_TOKEN" "SUPABASE_URL" "SUPABASE_SERVICE_ROLE_KEY")
missing_vars=()
for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    missing_vars+=("$var")
  fi
done

if [[ ${#missing_vars[@]} -gt 0 ]]; then
  log "ERROR: Missing required environment variables: ${missing_vars[*]}"
  exit 1
fi

log "All required environment variables are present."

# Start API server in background
log "Starting API server on ${API_HOST}:${API_PORT}..."
hermes serve --host "$API_HOST" --port "$API_PORT" &
API_PID=$!

# Wait for API server to be ready
log "Waiting for API server to be ready..."
attempt=0
while [ $attempt -lt $MAX_HEALTH_CHECK_ATTEMPTS ]; do
  if curl -sf "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
    log "API server is healthy."
    break
  fi
  attempt=$((attempt + 1))
  log "Health check attempt $attempt/$MAX_HEALTH_CHECK_ATTEMPTS failed. Retrying in ${HEALTH_CHECK_INTERVAL}s..."
  sleep "$HEALTH_CHECK_INTERVAL"
done

if [ $attempt -eq $MAX_HEALTH_CHECK_ATTEMPTS ]; then
  log "ERROR: API server failed to start after $MAX_HEALTH_CHECK_ATTEMPTS attempts."
  kill "$API_PID" 2>/dev/null || true
  exit 1
fi

# Start worker process
log "Starting worker process..."
python -m worker.main &
WORKER_PID=$!

# Trap signals to gracefully shut down
shutdown() {
  log "Shutting down..."
  kill "$API_PID" 2>/dev/null || true
  kill "$WORKER_PID" 2>/dev/null || true
  wait
  log "Shutdown complete."
  exit 0
}
trap shutdown SIGTERM SIGINT

# Keep container alive
log "All processes started. Waiting for signals..."
wait
```

## Validation Procedures

### YAML Validation
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('render.yaml'))"

# Or use yamllint if available
yamllint render.yaml
```

### Dockerfile Validation
```bash
# Build and check for errors
docker build -t test-build .

# Lint with hadolint if available
hadolint Dockerfile
```

### Shell Script Validation
```bash
# Syntax check
bash -n entrypoint.sh

# Run shellcheck if available
shellcheck entrypoint.sh
```

## Success Metrics

- **Syntax Accuracy**: 100% of generated config files pass validation on first attempt
- **Completeness**: All required environment variables and dependencies documented
- **Security**: No secrets hardcoded in configuration files
- **Compatibility**: Configurations work with target deployment platform (Render, Docker, etc.)

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
