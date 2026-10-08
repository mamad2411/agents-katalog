---
name: n8n-creator
description: "Full-cycle secure n8n workflow builder: env config → threat model → design → build → security audit → validate & test → harden → git save → tdd-audit. Works WITH or WITHOUT MCP. Reads .env for server/creds/secrets. Auto-saves workflows to ./workflows/<project>/. Covers credential handling, webhook auth, SSRF, input validation, expression injection, rate limiting, error handling. tdd-audit runs at end of EVERY build."
risk: low
source: local
date_added: "2026-03-23"
---

# n8n Creator — Secure Workflow Builder

Full-cycle protocol for building production-ready, security-tight n8n workflows.
Works with **MCP tools OR direct REST API**. Reads config from `.env`. Saves all
workflows to a git-tracked folder structure for rollback.

## Use this skill when

- Building any new n8n workflow
- Reviewing or auditing an existing workflow for security
- Adding nodes or integrations to a workflow
- Troubleshooting workflow failures or execution errors
- Hardening a workflow before production deployment
- Any task that produces or modifies n8n workflow JSON

## Do not use this skill when

- Working on non-n8n automation
- Pure research about n8n with no workflow output

---

## Related Skills — Load as Needed

| Skill | Load When |
|-------|-----------|
| `n8n-mcp-tools-expert` | Using MCP: search_nodes, validate_node, n8n_update_partial_workflow |
| `n8n-node-configuration` | Configuring specific node operations and property dependencies |
| `n8n-validation-expert` | Interpreting errors from validate_node / validate_workflow |
| `n8n-workflow-patterns` | Choosing architectural pattern (webhook, API, DB, AI, scheduled) |
| `n8n-expression-syntax` | Writing `{{}}` expressions, `$json.body`, `$node` references |
| `n8n-code-javascript` | JavaScript Code nodes: `$input.all()`, return format, helpers |
| `n8n-code-python` | Python Code nodes |

---

## ⚠ All 7 Stages Are MANDATORY

Every workflow task — no matter how small — must complete all seven stages.
A patch to a single node still requires stages 3–7.

```
Stage 0 — Load .env & detect mode   → REQUIRED: config loaded, MCP or REST confirmed
Stage 1 — Threat Model & Design     → REQUIRED: Design Plan confirmed by user
Stage 2 — Build                      → REQUIRED: working workflow (MCP or REST)
Stage 3 — Security Audit             → REQUIRED: Audit Report, all 10 checks
Stage 4 — Validate & Test            → REQUIRED: validation results + test scenarios
Stage 5 — Harden & Git Save          → REQUIRED: hardened workflow committed to ./workflows/
Stage 6 — /tdd-audit                 → REQUIRED: clean audit before marking done
```

---

## Stage 0 — Load .env & Detect Mode

**Always first.** Never hardcode server URLs, API keys, or credentials.

### .env file (place in project/working directory)

```bash
# n8n instance
N8N_API_URL=http://localhost:5678        # Base URL of your n8n instance
N8N_API_KEY=your-api-key-here           # Settings > n8n API > Create API key
N8N_WEBHOOK_BASE_URL=https://n8n.example.com  # Public URL for webhooks (if proxied)

# Optional self-hosted config
N8N_ENCRYPTION_KEY=64-hex-chars         # CRITICAL — never auto-generated in prod
N8N_BASIC_AUTH_ACTIVE=false
N8N_BLOCK_ENV_ACCESS_IN_NODE=true       # Security: block $env in Code nodes
N8N_PAYLOAD_SIZE_MAX=16                 # MiB

# Database (self-hosted PostgreSQL recommended for prod)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=secret

# Git workflow storage
WORKFLOWS_DIR=./workflows               # Where to save workflow JSON + docs
```

### Load .env at skill start

```bash
# Shell
set -a && source .env && set +a
echo "Connecting to: $N8N_API_URL"

# Node.js
import 'dotenv/config';
const { N8N_API_URL, N8N_API_KEY } = process.env;

# Python
from dotenv import load_dotenv; import os
load_dotenv()
api_url = os.getenv('N8N_API_URL', 'http://localhost:5678')
api_key = os.getenv('N8N_API_KEY')
```

If `.env` not present → prompt user for `N8N_API_URL` and `N8N_API_KEY` before continuing.

See `references/env-config.md` for the complete variable reference.

### Detect build mode

```
MCP tools available?  (search_nodes responds without error)
  YES → MCP path  (search_nodes, validate_node, n8n_update_partial_workflow)
  NO  → REST API path  (curl / fetch against $N8N_API_URL/api/v1)
```

Both paths produce the same workflow JSON and go through all security stages.

---

## Stage 1 — Threat Model & Design

**No workflow code during this stage.**

### 1a. Clarify requirements (one question per message)

| Question | Why it matters |
|----------|----------------|
| What does the workflow do end-to-end? | Sets attack surface |
| What triggers it? (webhook / schedule / manual / event) | Auth requirements |
| What external services does it call? | SSRF / credential scope |
| Where does user-controlled input enter? | Input validation strategy |
| What data is sensitive? (PII, tokens, financial) | Logging / masking |
| Who may trigger this? | Webhook auth + RBAC |
| What is the failure behaviour? | Error handling strategy |

### 1b. Choose workflow pattern

| Pattern | Trigger | Use when |
|---------|---------|----------|
| **Webhook Processing** | Webhook | Receiving events from external systems |
| **HTTP API Integration** | Schedule/Manual | Fetching / syncing with REST APIs |
| **Database Operations** | Schedule | ETL, sync, backup, data pipelines |
| **AI Agent Workflow** | Webhook/Manual | Conversational AI, tool-using agents |
| **Scheduled Tasks** | Schedule | Reports, digests, recurring automation |
| **Saga / Multi-step** | Webhook/Event | Distributed transactions needing rollback |
| **Fan-Out / Fan-In** | Any | Parallel processing with result aggregation |

See `references/workflow-design-patterns.md` for detailed pattern guidance.

### 1c. Design Lock — wait for user confirmation

Output this block and **wait for user confirmation before Stage 2**:

```
## Workflow Design Plan: <name>

Pattern:        <from table above>
Trigger:        <webhook path + method | cron | manual>
Auth:           <Header Auth | Basic Auth | JWT | None — justify if None>
External calls: <service → credential type>
Sensitive data: <field names>
Error strategy: <Stop and Error | continueOnFail | Error Trigger workflow>
Git path:       ./workflows/<project-name>/

## Node Plan
<nodes in execution order with brief purpose>

## Threat Surface
<top 3 risks>

## Decision Log
| Decision | Alternatives | Rationale |
```

---

## Stage 2 — Build

### MCP path

```javascript
// 1. Find nodes
search_nodes({query: "keyword"})

// 2. Understand config
get_node({nodeType: "nodes-base.X"})          // standard detail (default)

// 3. Validate before adding
validate_node({nodeType, config, profile: "runtime"})

// 4. Create and iterate
n8n_create_workflow({name, nodes: [], connections: {}, settings: {}})
n8n_update_partial_workflow({id, intent: "...", operations: [...]})

// nodeType formats:
//   search/validate tools → "nodes-base.slack"
//   workflow ops          → "n8n-nodes-base.slack"
```

### REST API path

```bash
BASE="${N8N_API_URL}/api/v1"
AUTH="X-N8N-API-KEY: ${N8N_API_KEY}"

# Create workflow
curl -s -X POST "$BASE/workflows" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "My Workflow",
    "nodes": [],
    "connections": {},
    "settings": {"executionOrder": "v1", "saveManualExecutions": true}
  }'

# Update workflow (full replace)
curl -s -X PUT "$BASE/workflows/$WORKFLOW_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d @workflow.json

# Activate / Deactivate
curl -s -X POST "$BASE/workflows/$WORKFLOW_ID/activate" -H "$AUTH"
curl -s -X POST "$BASE/workflows/$WORKFLOW_ID/deactivate" -H "$AUTH"

# List, get, delete
curl -s "$BASE/workflows?active=true" -H "$AUTH"
curl -s "$BASE/workflows/$WORKFLOW_ID" -H "$AUTH"
curl -s -X DELETE "$BASE/workflows/$WORKFLOW_ID" -H "$AUTH"

# Executions
curl -s "$BASE/executions?workflowId=$WORKFLOW_ID&limit=20" -H "$AUTH"
curl -s "$BASE/executions/$EXEC_ID" -H "$AUTH"
```

See `references/api-reference.md` for the complete REST endpoint catalog.

### Workflow JSON skeleton

```json
{
  "name": "Workflow Name",
  "active": false,
  "nodes": [],
  "connections": {},
  "settings": {
    "executionOrder": "v1",
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner",
    "errorWorkflow": ""
  },
  "tags": []
}
```

### Webhook trigger — security-first default

```json
{
  "id": "uuid",
  "name": "Receive Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "position": [240, 300],
  "parameters": {
    "httpMethod": "POST",
    "path": "your-unique-path",
    "authentication": "headerAuth",
    "responseMode": "lastNode",
    "options": {}
  }
}
```

`authentication` must be `"headerAuth"`, `"basicAuth"`, or `"jwtAuth"`.
`"none"` is never acceptable for production.

---

## Stage 3 — Security Audit

Run all 10 checks. Report each as ✅ PASS / ⚠️ WARN / ❌ FAIL.
Do not proceed to Stage 4 until all CRITICAL and HIGH items are PASS.

See `references/security-checklist.md` for full detail and remediation steps.

| # | Check | Sev | Common Failure |
|---|-------|-----|----------------|
| 1 | Webhook authentication | CRIT | `authentication: "none"` on production endpoint |
| 2 | No hardcoded credentials | CRIT | API keys in node params or expressions |
| 3 | Input validation | HIGH | Unvalidated body field in DB query / outbound URL |
| 4 | SSRF protection | HIGH | `{{$json.body.url}}` passed to HTTP Request node |
| 5 | Expression injection | HIGH | User input unsanitized in Code node or system call |
| 6 | Error response sanitization | HIGH | Stack traces or paths in Respond to Webhook |
| 7 | Sensitive data in logs | MED | Passwords/tokens in execution data |
| 8 | Rate limiting & retry | MED | No `retryOnFail` on external API calls |
| 9 | Least-privilege credentials | MED | Admin cred where read-only suffices |
| 10 | Error handling completeness | MED | No Error Trigger or continueOnFail strategy |

**Required output:**

```
## Security Audit: <workflow name>

| # | Check | Status | Finding | Remediation |
|---|-------|--------|---------|-------------|
| 1 | Webhook auth | ✅ PASS | Header auth set | — |
| 2 | Hardcoded creds | ❌ FAIL | API key in header param | Move to n8n credential |
...

Overall: X CRITICAL  X HIGH  X MEDIUM
```

---

## Stage 4 — Validate & Test

### Validate nodes

```javascript
// MCP
validate_node({nodeType: "nodes-base.X", config: {...}, profile: "runtime"})
// 2-3 fix cycles is normal

// REST — inspect execution logs
curl -s "$BASE/executions?workflowId=$ID&limit=1" -H "$AUTH"
```

### Validate full workflow

```javascript
// MCP
n8n_validate_workflow({id: "workflow-id"})

// Clean stale connections
n8n_update_partial_workflow({id, operations: [{type: "cleanStaleConnections"}]})
```

### Required test scenarios

| Scenario | Input | Expected |
|----------|-------|----------|
| Happy path | Valid complete payload | Correct output, 200 |
| Missing required field | `{}` | Safe error, no crash |
| Malformed JSON | `"not json"` | Caught at boundary |
| Auth failure | Wrong/missing header | 401, no data leak |
| Oversized payload | >16MB | Rejected |
| Expression injection | `{{$env.SECRET}}` in body | Literal string only |
| External timeout | Mock 30s+ delay | Timeout fires, handled |

See `references/testing-guide.md` for data pinning, partial execution, log analysis.

---

## Stage 5 — Harden & Git Save

### Harden: Respond to Webhook

```json
{"respondWith": "json", "responseBody": "={\"status\": \"received\"}"}
```
Never expose `$json`, error stacks, or internal paths.

### Harden: HTTP Request nodes

```json
{
  "timeout": 30000,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000,
  "authentication": "predefinedCredentialType"
}
```

### Harden: Code nodes

```javascript
// Sanitize all external inputs
const raw = ($input.first().json?.body?.field ?? '').toString().trim().slice(0, 512);
const safe = raw.replace(/[<>"'`;]/g, '');

// Null guards
const email = $input.first().json?.body?.email ?? null;
if (!email?.includes('@')) return [{json: {error: 'invalid_email'}}];

// Never log sensitive values
// ❌ console.log('token:', item.json.token);
// ✅ console.log('Processing item:', item.json.id);
```

### Git Save (every workflow, every change)

Save to the git-tracked folder structure **before** marking Stage 5 complete:

```
./workflows/
  <project-name>/
    workflow.json          ← exported workflow JSON from n8n API
    README.md              ← purpose, trigger URL, credentials needed, env vars
    deploy.sh              ← import/activate script (see below)
    rollback.sh            ← deactivate + import previous version
```

**Export workflow to file:**

```bash
PROJECT="my-project"
mkdir -p "./workflows/$PROJECT"

# Export via REST API
curl -s "$N8N_API_URL/api/v1/workflows/$WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  | jq '.' > "./workflows/$PROJECT/workflow.json"

echo "Saved workflow $WORKFLOW_ID to ./workflows/$PROJECT/workflow.json"
```

**deploy.sh template:**

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../.env"

WORKFLOW_FILE="$(dirname "$0")/workflow.json"
BASE="$N8N_API_URL/api/v1"
AUTH="X-N8N-API-KEY: $N8N_API_KEY"

echo "Deploying workflow from $WORKFLOW_FILE..."

# Check if workflow already exists (by name)
NAME=$(jq -r '.name' "$WORKFLOW_FILE")
EXISTING_ID=$(curl -s "$BASE/workflows" -H "$AUTH" \
  | jq -r --arg n "$NAME" '.data[] | select(.name==$n) | .id' | head -1)

if [ -n "$EXISTING_ID" ]; then
  echo "Updating existing workflow $EXISTING_ID..."
  curl -s -X PUT "$BASE/workflows/$EXISTING_ID" \
    -H "$AUTH" -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE"
  curl -s -X POST "$BASE/workflows/$EXISTING_ID/activate" -H "$AUTH"
else
  echo "Creating new workflow..."
  NEW_ID=$(curl -s -X POST "$BASE/workflows" \
    -H "$AUTH" -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE" | jq -r '.id')
  curl -s -X POST "$BASE/workflows/$NEW_ID/activate" -H "$AUTH"
  echo "Created workflow $NEW_ID"
fi
echo "Done."
```

**rollback.sh template:**

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../../.env"

WORKFLOW_ID="${1:?Usage: rollback.sh <workflow-id>}"
BASE="$N8N_API_URL/api/v1"
AUTH="X-N8N-API-KEY: $N8N_API_KEY"

# Deactivate
curl -s -X POST "$BASE/workflows/$WORKFLOW_ID/deactivate" -H "$AUTH"

# Restore previous git version
git checkout HEAD~1 -- "$(dirname "$0")/workflow.json"

# Re-import
curl -s -X PUT "$BASE/workflows/$WORKFLOW_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d @"$(dirname "$0")/workflow.json"

curl -s -X POST "$BASE/workflows/$WORKFLOW_ID/activate" -H "$AUTH"
echo "Rolled back workflow $WORKFLOW_ID"
```

**Launch multiple workflows at once (launch-all.sh):**

```bash
#!/usr/bin/env bash
# ./workflows/launch-all.sh — activate all workflows in all project folders
set -euo pipefail
source "$(dirname "$0")/../.env"

BASE="$N8N_API_URL/api/v1"
AUTH="X-N8N-API-KEY: $N8N_API_KEY"

for deploy_script in "$(dirname "$0")"/*/*/deploy.sh; do
  if [ -f "$deploy_script" ]; then
    echo "==> Deploying: $deploy_script"
    bash "$deploy_script"
  fi
done
echo "All workflows deployed."
```

**Commit after save:**

```bash
cd ./workflows
git add .
git commit -m "workflow: <project-name> — <brief description of change>"
```

**README.md template for each workflow:**

```markdown
# <Workflow Name>

## Purpose
<One sentence: what this workflow does and why>

## Trigger
- Type: Webhook / Schedule / Manual
- URL: $N8N_WEBHOOK_BASE_URL/webhook/<path>
- Auth: Header auth — requires `X-Webhook-Token` header

## Required Credentials
- `httpHeaderAuth` — API key for <service>
- `postgresDb` — read-only access to <database>

## Required Environment Variables
- `N8N_API_URL`
- `N8N_API_KEY`

## Data Flow
<Brief: input → transform → output>

## Security Notes
<Any known risks or compensating controls>

## Deploy
```bash
bash deploy.sh
```

## Rollback
```bash
bash rollback.sh <workflow-id>
```
```

---

## Stage 6 — /tdd-audit (MANDATORY, every time)

`@lhi/tdd-audit` is a hard dependency — it is installed via `setup.sh` / `npm install`
and **must run after every workflow build, patch, or modification**.

### Run the audit

```bash
# From the n8n-creator project root:
npm run tdd-audit

# Or directly (after npm install):
npx tdd-audit

# Or via the Claude Code skill:
/tdd-audit
```

### What it scans

Scans all Code nodes, expression fields, and workflow JSON for:
injection, IDOR, XSS, path traversal, broken auth, hardcoded secrets, SSRF,
insecure deserialization, prototype pollution, unvalidated input.

Runs full **Red → Green → Refactor** cycle for each finding.

### First-time setup check

```bash
# Verify tdd-audit is installed
ls node_modules/.bin/tdd-audit || { echo "Run: bash setup.sh"; exit 1; }
```

If `node_modules/.bin/tdd-audit` is missing, direct the user to run `bash setup.sh` first.

**Do not mark the workflow task complete until `tdd-audit` returns clean.**

---

## Troubleshooting

See `references/troubleshooting-guide.md` for full detail.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot read property X of undefined` | Webhook data at root | `$json.body.X` not `$json.X` |
| Expression shows as literal | Missing `{{}}` | Wrap in double curly braces |
| Node not found in validate_node | Wrong prefix | `nodes-base.*` not `n8n-nodes-base.*` |
| Broken connection error | Stale reference | `cleanStaleConnections` operation |
| 401 on webhook | No auth / wrong header | Check `authentication` field |
| Connection refused | Service down / wrong URL | Check URL and firewall |
| Invalid JSON between nodes | Data mismatch | JSON linter + check Set node mappings |
| API key rejected by n8n API | Wrong header name | Must be `X-N8N-API-KEY` |
| Workflow crashes on community node | Version mismatch | Disable via Cloud Admin Panel |

---

## Core Nodes Reference

**Triggers**: Webhook, Schedule, Manual, Chat, Email IMAP, Error, Execute Sub-workflow, Local File, MCP Server, n8n Form, RSS, Workflow Trigger

**Data**: Aggregate, AI Transform, Code, Compare Datasets, Crypto, Date & Time, Edit Fields (Set), Filter, HTML, IF, JWT, Limit, Merge, Remove Duplicates, Sort, Split in Batches, Split Out, Stop and Error, Summarize, Switch, XML

**Integration**: HTTP Request, FTP, Git, GraphQL, LDAP, Read/Write Files, Respond to Webhook, Send Email, SSH, TOTP, Wait

400+ app integrations — use `search_nodes({query: "..."})` (MCP) or browse the n8n UI.

---

## Security Anti-Patterns — Never

```javascript
// ❌ Hardcoded credential
{"headers": {"Authorization": "Bearer sk-abc123"}}

// ❌ User-controlled URL (SSRF)
{"url": "={{$json.body.callback_url}}"}

// ❌ Raw internals to caller
{"responseBody": "={{$json.error.stack}}"}

// ❌ Unauthenticated production webhook
{"authentication": "none", "path": "payment-webhook"}

// ❌ Unvalidated input in expression/query
{"query": "SELECT * FROM users WHERE id={{$json.body.id}}"}

// ❌ Reading secrets in Code node
const key = process.env.N8N_ENCRYPTION_KEY; // set N8N_BLOCK_ENV_ACCESS_IN_NODE=true
```
