# GuardRail AI — Tech Stack

## Backend (`api/`)
- **Runtime**: Node.js
- **Framework**: Express 4.x
- **Entry point**: `api/server.js`
- **Port**: 3001

### Middleware
- `helmet` — security headers
- `cors` — frontend at `http://localhost:3000`
- `express-rate-limit` — 50 req/hour default
- `compression` — gzip
- `joi` — request validation (`api/middleware/validation.js`)

### AWS SDKs (v3)
| SDK | Usage |
|-----|-------|
| `@aws-sdk/client-bedrock-runtime` | AI vulnerability analysis via Amazon Bedrock Nova Lite |
| `@aws-sdk/client-secrets-manager` | Secret provisioning with 24h TTL |
| `@aws-sdk/client-dynamodb` | Scan results + audit logs |
| `@aws-sdk/client-s3` | Patched code storage |
| `@aws-sdk/client-cloudwatch-logs` | Event logging |

### API Routes
| Method | Path | File |
|--------|------|------|
| POST | `/api/scan` | `routes/scan.js` |
| GET | `/api/result/:id` | `routes/result.js` |
| GET | `/api/logs` | `routes/logs.js` |
| POST | `/api/demo` | `routes/demo.js` |
| POST/GET | `/api/session` | `routes/session.js` |
| GET | `/health` | inline in `server.js` |

### Core Services (`api/services/`)
- `security-orchestrator.js` — main workflow coordinator
- `bedrock-client.js` — Bedrock Nova Lite AI calls
- `patch-generator.js` — produces patched code
- `secret-lifecycle-manager.js` — Secrets Manager + 24h TTL
- `session-manager.js` — per-scan session isolation
- `event-logger.js` — DynamoDB + CloudWatch audit trail
- `remediation-engine.js` — vulnerability remediation logic
- `s3-storage.js` — S3 upload/download

## Frontend (`web/`)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Port**: 3000

### Key Dependencies
- `axios` — API calls to backend
- `lucide-react` — icons
- `prismjs` — code syntax highlighting
- `react-diff-viewer-continued` — before/after patch diffs

### Pages (`web/app/`)
- `/` — landing page (`page.tsx`)
- `/scan` — code submission
- `/results` — vulnerability report + patch viewer
- `/dashboard` — scan history
- `/demo` — guided demo

## IDE Extension (`extensions/vscode/`)
- Built with VS Code Extension API
- Works on: VS Code, Kiro, Cursor, Windsurf
- Trigger: `Ctrl+Shift+G`
- Features: inline diagnostics, quick-fix lightbulb, auto-scan on save
- Packaged as `.vsix`

## Infrastructure
- **Config**: `config/aws-config.json`
- **Docker**: `api/Dockerfile`, `web/Dockerfile`, `docker-compose.yml`
- **Deploy script**: `scripts/deploy-infra.js`
- **Env**: `api/.env` (copy from `api/.env.example`)

## Supported Languages for Scanning
JavaScript, TypeScript, Python, Java, Go, Ruby, PHP
