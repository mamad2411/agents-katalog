---
name: "air-gap-deployment"
description: "Deploy UitKit stacks and infrastructure in air-gapped environments: audit MCP dependencies, replace with local equivalents, configure DISABLE_EXTERNAL_MCP"
---

# Air-Gap Deployment Skill

Deploy UitKit stacks, skills, and infrastructure in fully offline, air-gapped environments. This skill covers auditing external dependencies, replacing them with local equivalents, configuring offline modes, and validating zero external calls.

---

## When to activate

- Deploying Claude Code and UitKit stacks in air-gapped networks
- Migrating from internet-connected to fully isolated infrastructure
- Auditing which skills require network access (MCP servers, APIs, cloud services)
- Replacing external dependencies with local equivalents (git mirrors, package caches, local LLMs)
- Configuring offline-first stacks for government, financial, or security-critical environments
- Validating infrastructure has zero external connectivity

## When NOT to use

- Debugging connectivity issues (use network troubleshooting skills instead)
- Setting up local development (for that, see local-development skills)
- General cloud deployment (use cloud-specific skills)
- Container orchestration (use Kubernetes or Docker Compose skills)

---

## Instructions

### Step 1: Audit Stack Dependencies

Every UitKit stack has external dependencies. Map them before going air-gap.

**Create a dependency audit script:**

```bash
#!/bin/bash
# scripts/audit-stack-dependencies.sh
# Usage: bash audit-stack-dependencies.sh <stack-name>

STACK=$1
UITKIT_PATH=${UITKIT_PATH:-.}

if [[ -z "$STACK" ]]; then
  echo "Usage: bash audit-stack-dependencies.sh <stack-name>"
  echo "Available stacks:"
  ls "$UITKIT_PATH" | grep -E "_stack$" | sed 's/_stack//'
  exit 1
fi

STACK_DIR="$UITKIT_PATH/${STACK}_stack"

if [[ ! -d "$STACK_DIR" ]]; then
  echo "[ERROR] Stack not found: $STACK_DIR"
  exit 1
fi

echo "[*] Auditing dependencies for stack: $STACK"
echo ""

# 1. Find all CLAUDE.md files
echo "=== CLAUDE.md Files ==="
find "$STACK_DIR" -name "CLAUDE.md" -type f

# 2. Extract MCP references
echo ""
echo "=== External MCP Servers ==="
grep -r "mcp:" "$STACK_DIR" | grep -oE "mcp:[a-zA-Z0-9_-]+" | sort -u

# 3. Extract API calls
echo ""
echo "=== External API References ==="
grep -r -E "anthropic\.com|github\.com/api|aws\.amazonaws\.com|gcp|azure\.com" "$STACK_DIR" | grep -v ".git" | head -20

# 4. Extract package dependencies
echo ""
echo "=== Package Registry References ==="
grep -r -E "npm install|pip install|cargo add|go get" "$STACK_DIR" | grep -v ".git" | head -20

# 5. Find all skills and classify them
echo ""
echo "=== Skill Classification ==="
for skill_file in "$STACK_DIR"/skills/*.md; do
  skill_name=$(basename "$skill_file" .md)
  
  # Check for external indicators
  has_api=$(grep -c "API\|api\.anthropic\|cloud\|https://" "$skill_file" 2>/dev/null || echo 0)
  has_mcp=$(grep -c "mcp:" "$skill_file" 2>/dev/null || echo 0)
  
  if [[ "$has_api" -gt 0 ]] || [[ "$has_mcp" -gt 0 ]]; then
    echo "  [$skill_name] REQUIRES_NETWORK"
  else
    echo "  [$skill_name] OFFLINE_SAFE"
  fi
done
```

Run the audit:

```bash
bash scripts/audit-stack-dependencies.sh backend

# Output:
# [*] Auditing dependencies for stack: backend
# === CLAUDE.md Files ===
# ./guides/CLAUDE.md
#
# === External MCP Servers ===
# mcp:github
#
# === Skill Classification ===
#   [golang] OFFLINE_SAFE
#   [codebase-onboarding] REQUIRES_NETWORK
#   [docker] OFFLINE_SAFE
```

### Step 2: Classify Dependencies

Create a classification matrix:

```json
{
  "backend_stack": {
    "skills": {
      "golang": {
        "status": "OFFLINE_SAFE",
        "external_calls": [],
        "local_equivalent": "golang compiler (local)"
      },
      "dockerfile": {
        "status": "OFFLINE_SAFE",
        "external_calls": ["docker-hub-registry"],
        "local_equivalent": "docker load <image.tar>"
      },
      "codebase-onboarding": {
        "status": "REQUIRES_NETWORK",
        "external_calls": ["mcp:github", "anthropic-api"],
        "local_equivalent": "local git clone + offline CLAUDE.md"
      },
      "aws-architect": {
        "status": "REQUIRES_NETWORK",
        "external_calls": ["aws-api"],
        "local_equivalent": "CloudFormation templates + local schema validation"
      }
    },
    "offline_safe_skills": ["golang", "dockerfile", "testing"],
    "requires_network_skills": ["codebase-onboarding", "aws-architect", "cicd"],
    "offline_percentage": "33%"
  }
}
```

### Step 3: Replace External MCPs with Local Equivalents

**Mapping external MCPs to offline alternatives:**

| External MCP | Use Case | Offline Replacement |
|---|---|---|
| `mcp:github` | Clone repos, read PRs | `mcp:filesystem` + local git clone |
| `mcp:slack` | Notifications | `syslog` or local message queue |
| `mcp:linear` | Issue tracking | Local JSON file or SQLite |
| `mcp:aws` | Cloud operations | CloudFormation templates + validation |
| `mcp:stripe` | Payment processing | No offline equivalent — skip |

**Configuration for offline MCPs:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp",
      "args": ["server", "filesystem"],
      "disabled": false
    },
    "git": {
      "command": "mcp",
      "args": ["server", "git"],
      "disabled": false,
      "env": {
        "GIT_REPO_PATH": "/opt/repos"
      }
    },
    "bash": {
      "command": "mcp",
      "args": ["server", "bash"],
      "disabled": false,
      "env": {
        "ALLOWED_COMMANDS": "cd,ls,find,grep,git,npm,pip,python"
      }
    },
    "postgres": {
      "command": "mcp",
      "args": ["server", "postgres"],
      "disabled": false,
      "env": {
        "DATABASE_URL": "postgresql://localhost/offline_db"
      }
    }
  },
  "disableExternalMcp": true,
  "blockExternalApiCalls": true
}
```

### Step 4: Configure DISABLE_EXTERNAL_MCP Environment Variable

Set environment variables to force offline mode:

```bash
#!/bin/bash
# .claude/hooks/offline-mode.sh

export DISABLE_EXTERNAL_MCP=true
export OFFLINE_MODE=true
export MCP_SERVERS=filesystem,git,bash,postgres
export MCP_TIMEOUT=5000  # 5 second timeout instead of 30
export NETWORK_UNAVAILABLE=true

# Force local model serving
export API_URL=http://127.0.0.1:11434/v1
export MODEL=ollama:llama2

# Disable all cloud integrations
export AWS_ENDPOINT_URL=http://127.0.0.1:9000  # LocalStack
export AZURE_STORAGE_ACCOUNT_URL=http://127.0.0.1:10000
export GCP_EMULATOR_HOST=127.0.0.1:4222

echo "[*] Offline mode enabled"
```

Hook in `.claude/settings.json`:

```json
{
  "hooks": {
    "before:startup": {
      "command": "bash",
      "args": ["./.claude/hooks/offline-mode.sh"]
    }
  }
}
```

### Step 5: Audit External Calls (Detection)

Create a hook to detect and reject external network calls:

```bash
#!/bin/bash
# .claude/hooks/audit-external-calls.sh
# Runs after every bash command to check for external connectivity

COMMAND="$1"

# List of banned patterns indicating external calls
BLOCKED_PATTERNS=(
  "curl http"
  "wget http"
  "npm install.*--registry"
  "pip install.*--index-url"
  "docker pull"
  "aws s3"
  "gcloud"
  "az storage"
  "ssh.*external"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ $pattern ]]; then
    echo "[AUDIT] EXTERNAL_CALL_DETECTED: $COMMAND"
    # Log to audit trail
    echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"command\": \"$COMMAND\", \"type\": \"external_call_attempted\"}" >> /var/log/uitkit-audit.jsonl
    
    if [[ "${BLOCK_EXTERNAL_CALLS:-true}" == "true" ]]; then
      echo "[BLOCKED] Command blocked by air-gap policy"
      exit 1
    fi
  fi
done

exit 0
```

### Step 6: Create Offline-Safe Stack Profile

Document which parts of each stack work offline:

```markdown
# Backend Stack — Air-Gap Profile

## Offline-Safe Skills (Full Functionality)

### golang
- Build and test Go binaries locally
- No external calls
- Uses: local compiler, standard library
- Status: ✅ 100% offline

### dockerfile
- Build Docker images locally
- Requires: pre-cached base images (docker load)
- Status: ✅ 100% offline (with cached images)

### testing
- Run unit tests locally
- Status: ✅ 100% offline

## Partially Offline Skills (Limited Functionality)

### cicd
- Local GitHub Actions runners can work offline
- Cloud-based runners require network
- Status: ⚠️ 50% offline (requires GitHub Enterprise Server)

### aws-architect
- CloudFormation templates work offline
- AWS API calls require network
- Workaround: use LocalStack for local AWS emulation
- Status: ⚠️ 30% offline

## Network-Required Skills (Skip Offline)

### codebase-onboarding
- Requires GitHub API
- Requires Anthropic API
- Workaround: Use local git clone + local LLM
- Status: ❌ 0% offline

## Offline Deployment Instructions

```bash
# 1. Pre-cache Docker images
docker pull golang:1.21
docker pull ubuntu:22.04
docker save golang:1.21 -o golang.tar

# Transfer golang.tar to air-gapped network
docker load < golang.tar

# 2. Deploy backend stack with offline mode
export DISABLE_EXTERNAL_MCP=true
export API_URL=http://localhost:11434/v1

claude --stack backend-offline \
       --project /opt/uitkit \
       "Build and test a Go service"
```

## Limitations

- No live codebase onboarding from GitHub
- No Anthropic API for advanced LLM features
- Limited to local LLM quality (Llama 2, Mistral)
```

### Step 7: Test Offline Deployment

Create a test suite to validate air-gap readiness:

```bash
#!/bin/bash
# scripts/test-offline-deployment.sh

echo "[*] Testing offline deployment readiness..."

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Network isolation
echo -n "[TEST 1] Network isolation... "
if ! ping -c 1 8.8.8.8 &>/dev/null 2>&1; then
  echo "PASS"
  ((TESTS_PASSED++))
else
  echo "FAIL (external network reachable)"
  ((TESTS_FAILED++))
fi

# Test 2: Local MCP servers
echo -n "[TEST 2] Local MCP running... "
if curl -s http://127.0.0.1:8000/health 2>/dev/null | grep -q "ok"; then
  echo "PASS"
  ((TESTS_PASSED++))
else
  echo "FAIL (MCP server not responding)"
  ((TESTS_FAILED++))
fi

# Test 3: Offline mode env vars
echo -n "[TEST 3] Offline env vars set... "
if [[ "$DISABLE_EXTERNAL_MCP" == "true" ]] && [[ "$OFFLINE_MODE" == "true" ]]; then
  echo "PASS"
  ((TESTS_PASSED++))
else
  echo "FAIL (env vars not set)"
  ((TESTS_FAILED++))
fi

# Test 4: No external calls in audit log
echo -n "[TEST 4] No external calls attempted... "
if ! grep -q "external_call_attempted" /var/log/uitkit-audit.jsonl 2>/dev/null; then
  echo "PASS"
  ((TESTS_PASSED++))
else
  echo "FAIL (external calls detected in audit)"
  ((TESTS_FAILED++))
fi

# Test 5: Skill execution (offline-safe skill)
echo -n "[TEST 5] Offline-safe skill execution... "
if claude "list your available skills" 2>/dev/null | grep -q "golang\|dockerfile"; then
  echo "PASS"
  ((TESTS_PASSED++))
else
  echo "FAIL (skill not available)"
  ((TESTS_FAILED++))
fi

echo ""
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"

if [[ $TESTS_FAILED -eq 0 ]]; then
  echo "[OK] Offline deployment is ready"
  exit 0
else
  echo "[FAIL] Offline deployment has issues"
  exit 1
fi
```

### Step 8: Document Offline Stack List

Create a whitelist of approved stacks for air-gap deployment:

```markdown
# Air-Gap Approved Stacks

## Fully Offline (100% functionality)

- **Backend (Go, Rust, C++)** — Local compilation, testing, Docker build
- **Data/ML** — Local feature engineering, model training, evaluation
- **Frontend** — Local build, SSG generation, component testing
- **Database** — Local SQL, querying, migrations
- **Git Workflows** — Local version control, branching
- **Productivity/Automation** — Local scripts, shell workflows

## Partially Offline (30-70% functionality)

- **DevOps/Infra** — IaC works offline; cloud deployment requires network
- **Computer Use** — Desktop automation works; cloud services don't

## Network-Required (0% offline functionality)

- **GTM/Growth** — Requires analytics, market data
- **Finance** — Requires banking APIs, payment processors
- **Legal/Compliance** — Requires regulatory databases
- **AI-Engineering (partial)** — Local models only; cloud inference unavailable

## Recommended Offline Stack Set

For air-gapped teams, use these stacks:

1. backend
2. data-ml
3. frontend
4. database
5. devops-infra (with limitations)
6. productivity
```

---

## Example: Deploy Backend Stack Offline

```bash
#!/bin/bash
# Scenario: Deploy backend stack in air-gapped environment

# 1. Set offline mode
export DISABLE_EXTERNAL_MCP=true
export OFFLINE_MODE=true

# 2. Configure local model
export API_URL=http://localhost:11434/v1
export MODEL=ollama:llama2

# 3. Verify MCP servers are local
echo "Verifying offline MCPs..."
curl -s http://localhost:8000/health | jq .

# 4. Load backend stack and execute offline
claude --stack backend \
       --project /opt/uitkit \
       --offline \
       <<'EOF'

Create a Go REST API with the following:
- HTTP server listening on :8080
- GET /api/users endpoint
- Unit tests using testify
- Docker image for deployment
- All code should be self-contained (no external packages)

Use only what's available offline.
EOF

# 5. Verify no external calls
tail -20 /var/log/uitkit-audit.jsonl | grep "external_call"
echo "If no output above, air-gap deployment successful."
```

---

## Troubleshooting

**Issue: "MCP server not found" error**

```bash
# Verify all MCPs are local
grep -r "mcp:" ~/.claude/settings.json | grep -v "filesystem\|git\|bash\|postgres"

# If external MCP referenced, disable it
export DISABLE_EXTERNAL_MCP=true
```

**Issue: "API call to anthropic.com" detected**

```bash
# Check for hardcoded API URLs
grep -r "anthropic\.com" --include="*.md" .

# Verify local model is configured
echo $API_URL
```

**Issue: "Package download failed"**

```bash
# Use offline package cache
npm ci --prefer-offline --no-audit
pip install --no-index --find-links ./packages -r requirements.txt
```

---

## Summary

**Air-gap deployment steps:**

1. **Audit** — Map external dependencies (audit-stack-dependencies.sh)
2. **Classify** — Mark skills as offline-safe or network-required
3. **Replace** — Swap external MCPs for local equivalents
4. **Configure** — Set DISABLE_EXTERNAL_MCP, OFFLINE_MODE env vars
5. **Detect** — Hook audit calls to detect and block external network
6. **Document** — Create offline-safe stack whitelist
7. **Test** — Validate zero external connectivity (test-offline-deployment.sh)
8. **Deploy** — Use offline-approved stacks only

For enterprise air-gap deployment, see `enterprise/AIR_GAP.md`.

For offline-first patterns, see `guides/offline-local-first.md`.
