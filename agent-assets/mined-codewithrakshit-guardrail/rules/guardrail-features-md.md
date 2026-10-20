# GuardRail AI — Features & Hackathon Roadmap

## Strategic Direction
**Developer-first SOAR for the SDLC.**
Detect in the IDE → respond in the pipeline → notify the team.
Not a SOC tool. Not just a scanner. A full detect-respond-notify loop inside the developer workflow.

---

## ✅ Implemented

### Detection
- Hardcoded secrets & API keys (CWE-798)
- SQL injection (CWE-89)
- XSS (CWE-79)
- Path traversal (CWE-22)
- Insecure cryptography
- Command injection
- Insecure HTTP (CWE-319)
- 50+ vulnerability types via Bedrock Nova Lite

### Response / Remediation
- Production-ready patch generation
- AWS Secrets Manager provisioning with 24h TTL
- Least-privilege IAM policy generation
- Per-session resource isolation

### Ingest Paths
- Web UI — manual paste
- File upload
- VS Code / Kiro / Cursor / Windsurf extension (Ctrl+Shift+G)

### Platform
- Next.js 14 web UI — scan, results, dashboard, demo
- Express REST API
- DynamoDB audit trail + CloudWatch logging
- Docker support

---

## 🚧 In Progress — SOAR Buildout

### Phase 1 — GitHub Webhook (Priority: CRITICAL)
> Makes it SOAR, not just a scanner

- [ ] `POST /api/webhook/github` — receive PR events
- [ ] Validate `X-Hub-Signature-256` on all webhook payloads
- [ ] `api/services/github-client.js` — fetch PR diff via GitHub API
- [ ] Post PR status check (pass/fail) back to GitHub
- [ ] Post inline PR comments on vulnerable lines
- [ ] Wire route into `api/server.js`

### Phase 2 — Notification Actions (Priority: HIGH)
> The "response" in SOAR — must have 2-3 actions to credibly claim SOAR

- [ ] `api/services/notifier.js` — severity-based routing
- [ ] AWS SES email notifications (critical + high)
- [ ] Slack incoming webhook (critical only)
- [ ] Add `SLACK_WEBHOOK_URL`, `NOTIFICATION_EMAIL`, `GITHUB_TOKEN` to `.env.example`

**Severity → Action matrix:**
| Severity | Email | Slack | Block PR | PR Comment |
|----------|-------|-------|----------|------------|
| critical | ✅ | ✅ | ✅ | ✅ |
| high | ✅ | ❌ | ✅ | ✅ |
| medium | ❌ | ❌ | ❌ | ✅ |
| low | ❌ | ❌ | ❌ | dashboard only |

### Phase 3 — CI/CD Integration (Priority: HIGH)
- [ ] `.github/workflows/guardrail.yml` — scan on push/PR via hosted API
- [ ] Fail workflow on critical/high findings
- [ ] Post commit comment with scan summary
- [ ] Stretch: package as reusable GitHub Action (`uses: guardrail-ai/scan@v1`)

### Phase 4 — CLI Ingest (Priority: MEDIUM)
> Most visual demo moment — `npx guardrail scan ./src` in terminal
- [ ] `cli/` — thin Node.js CLI, calls existing `/api/scan`
- [ ] Glob file discovery, language detection
- [ ] Colored terminal output with severity breakdown
- [ ] Exit code 1 on critical/high (CI-friendly)

---

## 🔲 Remaining Improvements

### Web UI
- [ ] Real-time scan progress (SSE)
- [ ] One-click "Apply All Fixes"
- [ ] Scan history with diff comparison
- [ ] Export report as PDF/JSON
- [ ] Shareable scan result links

### Security Fixes (do before demo)
- [ ] Strip debug logs from secret-lifecycle-manager.js
- [ ] Sanitize filename before injecting into Bedrock prompt (prompt injection)
- [ ] Add request-level HTTP logging middleware (Morgan)
- [ ] Set CloudWatch log retention policy (30 days)
- [ ] Scrub stack traces before DynamoDB writes

---

## 🏆 Hackathon Demo Flow (Updated)

1. Developer pushes code with a hardcoded secret to a GitHub PR
2. GuardRail webhook fires automatically — no manual action
3. PR gets a failing status check within 3 seconds
4. Inline PR comment shows the exact vulnerable line + explanation
5. Developer gets an email with the patch
6. They apply the fix — PR turns green
7. AWS secret was auto-provisioned in the background

**Backup demo (if webhook infra isn't live):**
- VS Code extension: red squiggly → lightbulb → fixed in one click

**Key differentiator to say out loud:**
> "Traditional SOAR responds to threats in production. GuardRail shifts that left — detect and remediate before code ever ships, automatically."
