---
name: managing-bentoml
description: |
  Use when working with Bentoml — bentoML model serving and packaging
  management. Covers service management, model packaging, deployment status, API
  testing, Bento building, and runner configuration. Use when packaging ML
  models for serving, deploying BentoML services, debugging inference issues, or
  managing model artifacts.
connection_type: bentoml
preload: false
---

# BentoML Management Skill

Manage and monitor BentoML model packaging, serving, and deployments.

## MANDATORY: Discovery-First Pattern

**Always list existing models, bentos, and deployments before creating or modifying anything.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== BentoML Version ==="
bentoml --version 2>/dev/null

echo ""
echo "=== Local Models ==="
bentoml models list 2>/dev/null | head -15

echo ""
echo "=== Local Bentos ==="
bentoml list 2>/dev/null | head -15

echo ""
echo "=== Running Services ==="
bentoml serve --help >/dev/null 2>&1
# Check for running bentoml processes
ps aux | grep -E 'bentoml|bento' | grep -v grep | awk '{print $2"\t"$11" "$12" "$13}' | head -10

echo ""
echo "=== BentoCloud Deployments (if available) ==="
bentoml deployment list 2>/dev/null | head -10 || echo "BentoCloud not configured"
```

## Core Helper Functions

```bash
#!/bin/bash

# BentoML CLI wrapper
bml() {
    bentoml "$@" 2>/dev/null
}

# BentoCloud API helper (if using BentoCloud)
bentocloud_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $BENTOCLOUD_API_TOKEN" \
            -H "Content-Type: application/json" \
            "${BENTOCLOUD_ENDPOINT}/api/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $BENTOCLOUD_API_TOKEN" \
            "${BENTOCLOUD_ENDPOINT}/api/v1/${endpoint}"
    fi
}

# Test a running BentoML service endpoint
bento_test() {
    local url="${1:-http://localhost:3000}"
    local endpoint="${2:-/healthz}"
    curl -s -w "\nHTTP_STATUS:%{http_code}\nTIME:%{time_total}s\n" "${url}${endpoint}"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use CLI commands with structured output where available
- Never dump full Bento build files -- extract key configurations
- Test endpoints with concise request/response pairs

## Common Operations

### Model Management

```bash
#!/bin/bash
echo "=== All Models ==="
bentoml models list 2>/dev/null

MODEL_TAG="${1:-}"
if [ -n "$MODEL_TAG" ]; then
    echo ""
    echo "=== Model Details: $MODEL_TAG ==="
    bentoml models get "$MODEL_TAG" 2>/dev/null

    echo ""
    echo "=== Model Metadata ==="
    bentoml models get "$MODEL_TAG" -o json 2>/dev/null | jq '{
        tag: .tag,
        module: .module,
        creation_time: .creation_time,
        labels: .labels,
        metadata: .metadata,
        context: .context
    }' | head -30
fi
```

### Bento Build and Packaging

```bash
#!/bin/bash
echo "=== All Bentos ==="
bentoml list 2>/dev/null

BENTO_TAG="${1:-}"
if [ -n "$BENTO_TAG" ]; then
    echo ""
    echo "=== Bento Details: $BENTO_TAG ==="
    bentoml get "$BENTO_TAG" 2>/dev/null

    echo ""
    echo "=== Bento Info (JSON) ==="
    bentoml get "$BENTO_TAG" -o json 2>/dev/null | jq '{
        tag: .tag,
        service: .entry_service,
        models: [.models[]? | .tag],
        apis: .apis,
        size: .size,
        creation_time: .creation_time
    }' | head -30
fi
```

### Deployment Status

```bash
#!/bin/bash
echo "=== BentoCloud Deployments ==="
bentoml deployment list 2>/dev/null | head -15

DEPLOYMENT="${1:-}"
if [ -n "$DEPLOYMENT" ]; then
    echo ""
    echo "=== Deployment Detail: $DEPLOYMENT ==="
    bentoml deployment get "$DEPLOYMENT" 2>/dev/null | head -30

    echo ""
    echo "=== Deployment Logs ==="
    bentoml deployment logs "$DEPLOYMENT" --tail 20 2>/dev/null
fi
```

### API Testing

```bash
#!/bin/bash
SERVICE_URL="${1:-http://localhost:3000}"

echo "=== Health Check ==="
curl -s "${SERVICE_URL}/healthz" | head -5

echo ""
echo "=== Service Metadata ==="
curl -s "${SERVICE_URL}/docs.json" 2>/dev/null | jq '{
    title: .info.title,
    version: .info.version,
    endpoints: [.paths | keys[]]
}' 2>/dev/null || echo "OpenAPI docs not available"

echo ""
echo "=== Readiness Check ==="
curl -s -o /dev/null -w "Status: %{http_code}\nResponse Time: %{time_total}s\n" "${SERVICE_URL}/readyz"

echo ""
echo "=== Metrics (if available) ==="
curl -s "${SERVICE_URL}/metrics" 2>/dev/null | grep -E '^(bentoml_|HELP|TYPE)' | head -20
```

### Runner Configuration Inspection

```bash
#!/bin/bash
BENTO_TAG="${1:?Bento tag required}"

echo "=== Service Configuration ==="
bentoml get "$BENTO_TAG" -o json 2>/dev/null | jq '{
    runners: [.runners[]? | {
        name: .name,
        runnable_type: .runnable_type,
        models: .models,
        resource_config: .resource_config
    }],
    apis: [.apis[]? | {
        name: .name,
        input_type: .input_type,
        output_type: .output_type,
        route: .route
    }]
}' | head -40

echo ""
echo "=== Docker Configuration ==="
bentoml get "$BENTO_TAG" -o json 2>/dev/null | jq '.docker // "not configured"'
```

## Safety Rules

- **NEVER delete models or bentos** that are referenced by active deployments -- causes immediate serving failures
- **NEVER update production deployments** without testing the new Bento version first
- **Always health-check endpoints** after deployment changes -- verify `/healthz` and `/readyz` respond
- **Test with sample input** before routing production traffic -- schema mismatches cause 500 errors
- **Back up model artifacts** before deleting old versions -- BentoML model store deletion is permanent

## Output Format

Present results as a structured report:
```
Managing Bentoml Report
═══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Model tag versioning**: Tags use `name:version` format -- omitting version uses "latest" which may not be what you expect
- **Runner resource allocation**: Runners run in separate processes -- GPU allocation must be explicit in runner config
- **Build context size**: Large files in the build directory slow down `bentoml build` -- use `.bentoignore` to exclude unnecessary files
- **Python version mismatch**: Bento Python version must match the serving environment -- mismatches cause import errors
- **Containerization**: `bentoml containerize` requires Docker -- ensure Docker daemon is running
- **Adaptive batching**: Batch size tuning affects latency vs throughput tradeoff -- monitor p99 latency after changes
- **Service dependencies**: Multi-service bentos require all dependent services to be healthy -- partial failures cascade
- **Port conflicts**: Default port 3000 may conflict with other services -- use `--port` flag to specify alternate ports
