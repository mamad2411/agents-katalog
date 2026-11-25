---
name: infrastructure-reconstruction-guide
description: "Author step-by-step disaster recovery reconstruction guides (RECONSTRUCTION.md) for complex multi-service ecosystems — audit every component, categorize by dependency, produce a rebuild-from-bare-metal playbook."
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [disaster-recovery, reconstruction, documentation, playbook, rebuild, restore, infrastructure, migration]
    triggers: [reconstruction guide, rebuild from scratch, disaster recovery playbook, step by step rebuild, RECONSTRUCTION.md, ecosystem rebuild, bare metal restore, rebuild everything, restore from backup doc, build recovery docs]
    related_skills: [hermes-system-backup, hermes-operational-audit, project-documentation-standards, repo-sanitization]
    summary: >-
      A structured methodology for producing a RECONSTRUCTION.md — a step-by-step disaster recovery
      playbook that assumes the old machine is gone and nothing exists but the config repo.
      Covers inventorying all components (profiles, MCP servers, scripts, cron, Docker, services),
      categorizing by dependency order, writing copy-pasteable recovery commands for each phase,
      building tiered verification checkpoints, and producing appendices (quick-start checklist,
      file reference, port allocation map).
      Complementary to hermes-system-backup (file backup + quick restore) — this skill covers the
      deeper rebuild-from-scratch documentation its restore guide assumes is already in place.
---

# Infrastructure Reconstruction Guide

> **Skill class:** Authoring a RECONSTRUCTION.md — a disaster recovery playbook that lets someone rebuild the entire ecosystem from a bare OS machine.

This is distinct from a **restore guide** (copy files back from a backup — assumes the backup medium exists and works) and from an **architecture document** (structural overview — assumes the system is running). A reconstruction guide assumes **nothing exists but the config repo** and steps through the rebuild in dependency order.

## When to Use

- **New machine / OS reinstall** — write the guide during initial setup, before the old machine dies
- **Ecosystem expansion** — profiles go from 10→30, MCPs from 5→20, services multiply
- **First-time documentation** — nothing written down, capture the rebuild process as you audit
- **Outgoing maintainer** — document the ecosystem for the person inheriting it
- **"How do I rebuild this?"** — the fact that someone is asking means the guide doesn't exist
- **After major architectural changes** — add new services, remove old ones, update the guide

## Core Methodology: 10-Phase Reconstruction Guide

### Phase 1 — Prerequisites

Catalog every dependency upfront in tables:

**Required software table:**
| Dependency | Version | Install Command |
|---|---|---|
| Git | Latest | `winget install Git.Git` |
| Python | 3.11+ | `winget install Python.Python.3.11` |
| Docker Desktop | Latest | `winget install Docker.DockerDesktop` |

**Accounts & access table:**
| Service | Required For | Signup URL |
|---|---|---|
| GitHub | Config repo, tokens | https://github.com |
| OpenRouter | LLM API fallback | https://openrouter.ai |

Scan for everything the reader needs before they can run the first command. A guide that starts with "clone the repo" but doesn't tell the reader to install Git first is incomplete.

### Phase 2 — Clone & Restore Config

- Clone the config repo with exact URL
- Clone every supporting repo (MCP server projects, agent repos, infrastructure repos)
- **Path migration audit**: grep the config repo for old usernames, old drive letters, old directory paths that will need updating on the new machine
- Run the setup script

```bash
# Find all paths that need updating
grep -rn "yourdata\|/<you>/\\|E:/" ~/Documents/github/hermes-config/config/ 2>/dev/null
grep -rn "yourdata\|<you>" ~/Documents/github/hermes-config/.hermes/ 2>/dev/null
```

### Phase 3 — Install Core Application

- Install command
- Verification: `app --version`, `app doctor`, `app doctor --fix`
- Copy every config file from the repo to runtime locations:
  - `config/config.yaml` → `~/AppData/Local/hermes/config.yaml`
  - `.hermes/config.yaml` → `~/AppData/Local/hermes/.hermes/config.yaml`
  - `config/jobs.json.example` → `~/AppData/Local/hermes/jobs.json`
  - `config/model_config.json` → `~/AppData/Local/hermes/model_config.json`

### Phase 4 — .env Construction

This is the most delicate phase because secrets aren't in the config repo. The guide must:

1. **Extract all env var references** from configs and scripts — not just what's in `.env.example`:

```bash
# Find every env var reference in config files
grep -roh '\${[A-Z_]*}' config/ | sort -u

# Find every getenv call in scripts
grep -roh 'os\.getenv([^)]*' scripts/*.py 2>/dev/null | sort -u
grep -roh 'environ\.get([^)]*' scripts/*.py 2>/dev/null | sort -u

# Cross-reference with .env.example — anything in configs that's NOT in the example is a gap
```

2. **Build a complete variable table**:

| Variable | Required? | Source URL |
|---|---|---|
| `OPENROUTER_API_KEY` | YES | https://openrouter.ai/keys |
| `DEEPSEEK_API_KEY` | YES | https://platform.deepseek.com |
| `TRILIUM_TOKEN` | YES | http://localhost:8090 → Options → Advanced → ETAPI |

3. **Provide a full template** with placeholder values — the reader should be able to copy-paste the template, fill in their keys, and go.

### Phase 5 — Infrastructure Services

For each non-MCP service, document:

| Field | Example |
|---|---|
| Service name | OmniRoute (model routing) |
| Start command | `npx omniroute@latest --port 20128` |
| Port | 20128 |
| Health check | `curl -s http://localhost:20128/v1/models` |
| Config wiring | Provider `custom:omniroute` in profile configs |

Common services: OmniRoute (model routing), Trilium Notes (Docker :8090), Postgres (Docker :33443), Buzz Nostr relay (:3000), Logseq graph (file-based), Camoufox (stealth browser binary), FAL.ai (API key only), MemPalace (pip install).

### Phase 6 — MCP Server Recovery

Group by category. For each server, produce a table row:

| Server | Type | Dependency | Restore Command |
|---|---|---|---|
| `logseq` | Python | `pip install mcp` | `python scripts/mcp_logseq_file_server.py` |
| `trilium` | Python | `pip install mcp httpx` | `python scripts/mcp_trilium_server.py` |

Include: command+args, workdir, timeout, env vars required, which profile configs define this server.

**Source of truth:** Scan `mcp_servers` in every config file (main config.yaml, .hermes/config.yaml, every profile's config.yaml).

### Phase 7 — Profile Restoration

- List all profiles from `find profiles/ -name "config.yaml" | wc -l`
- Categorize by priority tier:
  - **CRITICAL**: default, development-lead (must work first)
  - **COUNCIL**: chief-of-staff, treasury-lead, operations-lead, etc.
  - **TEAM**: dev-lead, docs-lead, qa-lead, etc.
  - **SPECIALIST**: all specialized agents
- Document per-profile: config.yaml, AGENTS.md, SOUL.md
- Provide bulk creation commands

### Phase 8 — Scripts Restoration

Script dependency mapping table:

| Script | Purpose | pip install | Config Deps |
|---|---|---|---|
| `cron-guardian.py` | Cron lifecycle | `requests` | `model_config.json`, `.env` |
| `model_watchdog.py` | Provider health | stdlib only | `.env` |

Include: bulk install command, note which scripts are no_agent cron vs agent-driven.

### Phase 9 — Cron Jobs & Watchdogs

Table with registration commands:

| Cron Job | Schedule | Script | Registration |
|---|---|---|---|
| model-watchdog | Every 10 min | `model_watchdog.py` | `hermes cron add --name model-watchdog --schedule "*/10 * * * *" --command "python ..." --no-agent` |

### Phase 10 — Verification Checklist

Build a tiered verification flow that catches failures at exactly one layer:

| Tier | What It Verifies | Command |
|---|---|---|
| 1 | System health | `hermes doctor`, `hermes config`, `hermes profile list` |
| 2 | API connectivity | `curl -s https://api.deepseek.com/v1/models -H "Authorization: Bearer $KEY"` |
| 3 | Docker services | `docker ps`, `curl` health endpoints |
| 4 | MCP connectivity | `hermes mcp list`, `hermes mcp test <name>` |
| 5 | Knowledge bases | Logseq graph exists, Trilium responds |
| 6 | Cron jobs | `hermes cron list` |
| 7 | Profile switching | `hermes --profile development-lead --command "hello"` |
| 8 | Skills | `hermes skills list` |
| 9 | Script health | `python -m py_compile script.py` |
| 10 | End-to-end | Full conversation flow |
| 11 | VPS (if deployed) | SSH + docker compose ps |

### Appendices

| Appendix | Content |
|---|---|
| Quick-start checklist | Numbered boxes in rebuild order |
| File reference | Every important path and what lives there |
| Port allocation table | Service → port → purpose mapping |

## Scanning for Env Var Gaps

The #1 gap in reconstruction guides is missing environment variables — variables referenced in configs or scripts that aren't in the .env.example.

```bash
# Find all ${VAR} references in config files
grep -rohP '\$\{[A-Z_]+}' config/ scripts/ --include='*.yaml' --include='*.py' --include='*.sh' --include='*.json' 2>/dev/null | sort -u

# Find all getenv() calls in Python scripts
grep -rohP 'os\.getenv\(['\"]([A-Z_]+)['\"]' scripts/*.py 2>/dev/null | sort -u

# Find all os.environ.get() calls
grep -rohP 'environ(?:ment)?\.get\(['\"]([A-Z_]+)['\"]' scripts/*.py 2>/dev/null | sort -u

# Find hardcoded fallback patterns like getenv("VAR", "literal")
grep -rnP 'os\.getenv\(['\"][A-Z_]+['\"],\s*['\"][A-Za-z0-9_]+['\"]' scripts/*.py 2>/dev/null
```

Any var found by these scans that doesn't appear in `.env.example` is a gap the guide must document.

## Scanning for Path Dependencies

```bash
# Find absolute paths in configs that reference old user/drive
grep -rn 'yourdata\|/<you>/\\|E:/\|${USER_HOME}' config/ scripts/ --include='*.yaml' --include='*.py' --include='*.sh' --include='*.json' 2>/dev/null | head -50

# Find all workdir references in MCP server configs
grep -rn 'workdir:' config/ 2>/dev/null

# Find all args with absolute paths
grep -rnP 'args:.*\[.*[A-Z]:/' config/ 2>/dev/null
```

Document every path that needs rewriting for a new machine.

## Port Conflict Detection

```bash
# Scan for all port bindings in configs and scripts
grep -rohP 'port[=: ]\s*\d+' config/ scripts/ 2>/dev/null | sort -u

# Scan Docker compose files
grep -rohP '\d+:\d+' ~/Documents/github/hermes-config/vps/docker-compose.yml 2>/dev/null

# Scan docker run commands in scripts
grep -rnP '\-p \d+' scripts/*.sh scripts/*.py 2>/dev/null
```

Build the port allocation appendix from these scans.

## Authoring Rules

1. **Read before you write.** Inventory every component before writing a single line of the guide. The reconstruction guide is only as good as the audit that feeds it.

2. **Commands must be copy-pasteable.** Use exact absolute paths. No "replace with your own" without a clear example.

3. **Assume the old machine is gone.** Don't write "you can get this from the old install" unless it's truly irreplaceable.

4. **Every phase ends with a verification step.** The reader should never wonder if a phase worked.

5. **Profile priority matters.** List profiles in rebuild order — core first, council next, then team, then specialist. The earlier profiles must restore MCP connectivity for the later ones.

6. **Dependency order is sacred.** Don't list cron jobs before MCP servers, or profiles before the .env file. Each phase should only depend on phases above it.

7. **Appendices are for scanning, not reading.** The quick-start checklist, file reference, and port map are what someone glances at during a rebuild — they must be accurate at a glance.

8. **Windows path mangling is a real risk.** MSYS2 bash strips backslashes. Use `MSYS_NO_PATHCONV=1` for Docker commands with Windows paths, or POSIX-style `/c/Users/...` paths in bash scripts.

## Related Skills

- `hermes-system-backup` — File backup + quick restore (complementary: this skill covers the deeper rebuild documentation its restore guide doesn't)
- `hermes-operational-audit` — Running-system health audit (complementary: run before writing the guide to inventory the live system)
- `project-documentation-standards` — README/ROADMAP standards (narrower: project docs, not recovery docs)
- `repo-sanitization` — Sanitize for sharing (useful if the config repo will be shared with a new maintainer)
