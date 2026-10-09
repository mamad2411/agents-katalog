---
name: n8n-pipeline
description: Top-level orchestrator skill for the full n8n workflow pipeline — build, deploy, test, fix, rollback. Trigger when the user asks to build/deploy/debug/fix/test/rollback an n8n workflow on the production host ($N8N_HOST), or refers to workflows under their n8n workspace directory ($N8N_WORKSPACE). Routes the request to the correct slash command and enforces the safety gates (template-first, local validate, backup, confirm, test gate, git commit).
---

# n8n Pipeline Orchestrator

You are the entry point for n8n workflow automation. When triggered, you route the user's request to the right slash command and enforce safety rules across the whole pipeline.

## Setup before first use

Before this skill is useful, set the env var pointing at your n8n workspace:

```bash
# Unix / macOS / Git Bash
export N8N_WORKSPACE="/path/to/your/n8n-workflow-projects"

# Windows PowerShell
$env:N8N_WORKSPACE = "D:\path\to\your\n8n-workflow-projects"
```

Reference workspace in this skill is `${N8N_WORKSPACE}` (placeholder). The author of this skill keeps theirs at `D:/Projects/work/build-workflow/` — adjust to your reality.

## When to trigger
- User says "build/tạo workflow", "deploy wf", "test wf", "fix wf", "rollback wf"
- User references a workflow file under `${N8N_WORKSPACE}/`
- User asks to push a workflow to n8n production
- User reports an n8n execution error and wants it fixed

## Pipeline map

| Intent | Slash command | Notes |
|---|---|---|
| Create new workflow JSON | `/n8n-build <desc> [--tier=...] [--project=...]` | Template-first, local validate |
| Update existing + push to n8n | `/n8n-deploy <file> [--activate]` | Backup + confirm + test gate |
| Run workflow once to verify | `/n8n-test <workflowId> [--payload=...]` | Read-only, gate check |
| Fix broken workflow (auto loop) | `/n8n-fix <workflowId>` | 3 retries → escalate Opus thinking |
| Revert to last backup | `/n8n-rollback <workflowId>` | Confirmed rollback |

## Safety rules (non-negotiable)

0. **Preflight** — run `n8nctl doctor` at start of every pipeline run. Bail if any check fails.
1. **Production only** — `$N8N_HOST` is production. No staging exists. Treat every call as production-touching.
2. **Template-first build** — never generate workflow JSON from blank. Always copy from `_templates/`.
3. **Local validator before any deploy** — `n8nctl workflow validate <file> --strict`. Must pass.
4. **Diff preview before any update** — `n8nctl workflow diff <id> <file>` to confirm minimal changes.
5. **Backup before any update** — `n8nctl workflow backup <id> -o <projectDir>/_backups/` before `workflow update`.
6. **Confirm before activate** — always ask the user before flipping `active: true`.
7. **Test gate before activate** — execution must pass `_pipeline/test-gate.js` CẦN tier at minimum.
8. **Git commit after successful deploy** — commit the JSON to the project repo, do NOT push unless asked.
9. **Self-healing loop caps at 3** — after 3 failed fix attempts, escalate with max thinking budget, then STOP and report.
10. **Never touch credentials** — credential issues require user intervention.
11. **Never skip hooks** — no `--no-verify`, no `--force` except when user explicitly requests.

## Primary tool: n8nctl CLI

**Preferred for ALL API interactions**. Package `@trngthnh369/n8nctl` (installed globally). Wraps REST API with:
- Layered auth (env > keyring > config file)
- Retry + exponential backoff + Retry-After handling
- `--dry-run` preview for destructive ops
- `--json` / `--jq` / `--template` output formats
- Typed exit codes (0 OK, 1 API, 2 auth, 3 validation, 4 network, 5 internal)

Full command reference: run `n8nctl --help` or see `n8nctl (skill)` skill.

## Supporting skills to delegate into

- **n8nctl (skill)** — CLI command reference + raw API fallback (has `n8nctl` quick reference)
- **n8n-patterns** — workflow pattern library
- **n8n-node-configuration** — correct node types + typeVersion (offline catalog)
- **n8n-expression-syntax** — expression syntax correctness
- **n8n-validation-expert** — interpret n8n validation errors
- **n8n-integrations** — Meta/Sheets/TikTok/Claude API patterns
- **n8n-code-javascript** / **n8n-code-python** — Code node content
- **n8n-workflow-patterns** — proven architectural patterns
- **wiki-query** — if the user maintains `n8n-wiki` at `${N8N_WORKSPACE}/n8n-wiki/`

## Supporting agents to delegate into

- **n8n-builder** — structured workflow JSON construction
- **n8n-debugger** — execution error → root cause → patch loop
- **architect** — escalation step when self-healing fails

## Directory layout

```
${N8N_WORKSPACE}/
├── _pipeline/
│   ├── validate.js      # Local schema validator (Layer 1 gate)
│   ├── test-gate.js     # Execution gate checker
│   └── backup.js        # Workflow export/restore helper
├── _templates/
│   ├── orchestrator.template.json
│   ├── hub.template.json
│   ├── utility.template.json
│   └── project-bootstrap/     # Claude Code context templates
│       ├── CLAUDE.md.template
│       ├── .claudeignore.template
│       └── README.md
├── _fixtures/           # Per-workflow test payloads (build on-demand)
└── <project-name>/      # Each = its own git repo
    ├── CLAUDE.md        # Project context (from project-bootstrap template)
    ├── .claudeignore    # Project-scoped ignore (from project-bootstrap template)
    ├── workflow/
    │   └── <name>.json
    └── _backups/
        └── <name>_<timestamp>.json
```

## Project bootstrap (new project)

When creating a new n8n project folder, bootstrap Claude Code context:
```bash
PROJECT="new-project-name"
cp _templates/project-bootstrap/CLAUDE.md.template <project>/CLAUDE.md
cp _templates/project-bootstrap/.claudeignore.template <project>/.claudeignore
# Then edit CLAUDE.md → fill {{PLACEHOLDERS}}
```

See `_templates/project-bootstrap/README.md` for placeholder table.

## Safety hooks (auto-enforced via ~/.claude/settings.json)

- **`pre-bash-n8n-deploy-validate`** — blocks `n8nctl workflow update/create/import` nếu local validate.js fail
- **`post-bash-n8nctl-diagnose`** — nếu n8nctl exec error → auto-suggest `/n8n-fix`
- **`pre-write-n8n-secret`** — blocks hardcoded JWT/API key/token vào workflow JSON

Hooks in files: `~/.claude/hooks/*.cjs`. Errors logged to `~/.claude/hooks/logs/errors.log`.

## Default routing logic

```
if intent = "build/tạo mới" → /n8n-build
if intent = "deploy/push/update" + file given → /n8n-deploy
if intent = "test/chạy thử/verify" + id given → /n8n-test
if intent = "fix/sửa/debug" + id given → /n8n-fix
if intent = "rollback/revert" + id given → /n8n-rollback
if intent unclear → ask user + show the pipeline map above
```

## Tier selection heuristic (for /n8n-build)

- **utility**: single external API call, single transform, reused by multiple workflows, max 10-15 nodes
- **hub**: domain logic combining multiple utilities, has validation + error handling, orchestrates 2-5 utilities
- **orchestrator**: routes incoming requests (webhook/schedule) to the right hub, has switching logic, thin

If the user's description fits 2 tiers, prefer the smaller one (utility > hub > orchestrator). Smaller is easier to test and reuse.
