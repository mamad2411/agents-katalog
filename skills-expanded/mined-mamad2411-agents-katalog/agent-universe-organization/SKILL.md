---
name: agent-universe-organization
description: "Structure, conventions, and integration patterns for the agent-universe monorepo — a 10-team, 69-agent multi-agent framework spanning OSINT, offensive security, defensive, fraud ops, legal, infra, recon, logistics, and swarm operations."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [agent-universe, monorepo, organization, agent-framework, team-structure, codebase-integration]
    triggers: [agent-universe, monorepo-organization, team-structure, codebase-integration, folder-organization, reorganize, restructure-directory, integrate-codebase]
    related_skills: [subagent-driven-development, project-inventory]
---

# Agent-Universe Organization

Conventions and working patterns for the agent-universe monorepo — a multi-team, multi-agent framework at `${MY_REPOS}\Documents\github\agent-universe\`.

This is not about the content of any one agent. It's about how the monorepo is structured, how new agents are added, how external code is integrated, and what conventions must be followed for cross-team consistency.

## Monorepo Structure

```
agent-universe/
├── AGENT_UNIVERSE.md          # Master index — all teams, all agents, shared components
├── README.md                  # Project overview
├── .github/workflows/         # CI/CD
├── orchestrator/              # Team 00 — meta-coordination (single agent)
│   ├── AGENTS.md              # YAML frontmatter + role/capabilities/workflow
│   ├── README.md              # Quick-start overview
│   ├── config/config.yaml     # Agent config (name, log_level, mcp_servers)
│   └── .env.example           # Environment variables template
├── teams/
│   ├── 01-osint-recon/        # Numbered teams (01-09)
│   │   ├── TEAM.md            # Team overview + agent table + data flow
│   │   └── {agent-name}/      # Agent directories
│   │       ├── AGENTS.md      # Frontmatter + role, capabilities, tools, MCP servers
│   │       ├── README.md      # Prerequisites, quick start, workflow, see also
│   │       ├── config/config.yaml
│   │       ├── .env.example
│   │       ├── tooling/       # Python/PowerShell scripts the agent runs
│   │       ├── templates/     # File templates (.gitkeep if empty)
│   │       ├── docs/          # Agent-specific docs (.gitkeep if empty)
│   │       └── tests/         # Test cases (.gitkeep if empty)
│   ├── 02-offensive-security/
│   ├── 03-defensive-security/
│   ├── 04-fraud-operations/
│   │   └── new/               # ⚠️ Experimental sub-projects live here (not standard structure)
│   ├── 05-legal-counsel/
│   ├── 06-infrastructure-support/
│   ├── 07-recon-team/
│   │   └── shared/            # Shared components scoped to this team
│   │       ├── slow-roll-proxy/
│   │       ├── tech-to-cve/
│   │       ├── knowledge-graph/
│   │       └── orchestrator/  # Hermes Agent skill files
│   ├── 08-infrastructure-logistics/
│   └── 09-swarm-operations/
├── infrastructure/            # Cross-cutting operational infrastructure
│   ├── README.md
│   ├── docker-compose.yml
│   ├── mcp-servers/           # MCP server implementations (12+ servers)
│   │   ├── INDEX.md
│   │   ├── hermes-config.yaml # Ready-to-use Hermes MCP configuration
│   │   ├── src/               # Python implementations (*_server.py)
│   │   └── docs/              # Server documentation
│   ├── gateway/               # Traffic routing, logging, killswitch
│   ├── network/               # VPN, WireGuard, network isolation
│   ├── fingerprint/           # Browser fingerprint management
│   ├── swarm-configs/         # NATS, Redis, Prometheus, Grafana configs
│   ├── deploy/                # Ansible, Docker Compose, scripts, WireGuard configs
│   └── docs/
│       ├── architecture/      # Swarm architecture, comm protocols, deployment topology
│       ├── frameworks/        # Tool-specific guides (CrewAI, LangGraph, vLLM, etc.)
│       └── guides/            # Workstation security, onboarding, etc.
├── shared/
│   ├── skills/                # Cross-team skill implementations
│   │   ├── INDEX.md
│   │   ├── src/               # Python skill implementations
│   │   └── docs/              # Skill docs + BUILD_RATIONALE.md
│   ├── tools/                 # Cross-team tool wrappers
│   │   ├── INDEX.md
│   │   ├── src/               # Python tool wrappers (extend BaseTool)
│   │   └── docs/              # Tool-specific docs
│   ├── knowledge-manager/     # Cross-session knowledge ingestion + search
│   ├── cost-tracking/         # Per-operation expense/revenue tracking
│   └── templates/agent-scaffold/  # Template for new agents
├── docs/                      # Project-level docs
│   ├── protocols/             # Cross-team comms, emergency, disaster recovery, compartmentalization
│   └── guides/                # Agent onboarding, full-stack quick-start, CI testing, upgrade/migration
├── .github/workflows/         # CI/CD (agent-validation.yml)
└── voice-agent/               # Standalone voice agent system
```

## Per-Agent Conventions

Every agent directory follows this exact structure:

| File | Required? | Purpose | Format |
|------|-----------|---------|--------|
| `AGENTS.md` | ✅ Yes | Agent profile — YAML frontmatter (name, team, repo, version, status) + markdown body (Role, Key Capabilities, Data Sources, Tooling, MCP Servers) | YAML + Markdown |
| `README.md` | ✅ Yes | Quick-start — overview, prerequisites, usage examples, workflow, output, cross-references | Markdown |
| `config/config.yaml` | ✅ Yes | Agent config — name, version, log_level, output_dir, mcp_servers | YAML |
| `.env.example` | ✅ Yes | Environment variables — commented, with placeholder values | Key=Value |
| `tooling/` | ✅ Yes | Runnable scripts — Python (.py) or PowerShell (.ps1). Include `__init__.py` if Python package. | Source code |
| `templates/` | 🔶 Optional | Starter files meant to be copied/modified | Any |
| `docs/` | 🔶 Optional | Agent-specific documentation | Markdown |
| `tests/` | 🔶 Optional | Test cases (pytest preferred) | Python |

### AGENTS.md Frontmatter Fields

```yaml
---
name: agent-name            # Lowercase, hyphens
team: "NN — Team Name"      # Numbered team reference
repo: agent-name-agent      # GitHub repo name
version: 0.1.0              # Semantic version
status: seed                # seed | active | stable | deprecated
---
```

### AGENTS.md Body Structure

1. **Role** — One-paragraph mission statement
2. **Key Capabilities** — Numbered list of 5-15 capabilities
3. **Data Sources** — Lists of APIs, databases, tools the agent queries
4. **Tooling** — Tools the agent uses (for AGENTS.md) or custom scripts in tooling/
5. **MCP Servers** — MCP servers the agent connects to
6. **Workflow** — ASCII diagram or numbered steps (for README.md)

### Team TEAM.md Structure

```markdown
# Team NN — Team Name

**Mission:** One-line mission statement.

## Agents

| Agent | Path | Role |
|-------|------|------|
| **Agent Name** | `agent-dir/` | One-line role description |

## Data Flow
How this team interacts with other teams.

## Dependencies
External dependencies, tools, API keys, infrastructure requirements.
```

## Creating a New Agent (Scaffold)

### Step-by-Step Agent Creation

1. `mkdir -p teams/{NN}-{team-name}/{agent-name}/{config,tooling,templates,docs,tests}`
2. Create `AGENTS.md` with YAML frontmatter + role/capabilities/tooling
3. Create `README.md` — overview, prerequisites, quick start
4. Create `config/config.yaml` — agent config with MCP server references
5. Create `.env.example` — env vars (no real secrets)
6. If tooling exists, copy Python/PowerShell files into `tooling/`
7. Update the team's `TEAM.md` to include the new agent in the table
8. Update `AGENT_UNIVERSE.md`: bump total agent count, add agent to team's table, update summary table

### Agent Scaffold Template

```markdown
# agent-name/

├── AGENTS.md          # YAML frontmatter + markdown (role, capabilities, tooling, MCP)
├── README.md          # Usage overview, prerequisites, quick start, see-also
├── config/
│   └── config.yaml    # Agent config (name, version, log_level, output_dir, mcp_servers)
├── .env.example       # Environment variables (NO real secrets)
├── tooling/
│   ├── script.py      # (optional) Python/PowerShell tooling
│   └── .gitkeep       # (if dir is empty)
├── templates/
│   └── .gitkeep
├── docs/
│   └── .gitkeep
└── tests/
    └── .gitkeep
```

### AGENTS.md Frontmatter Fields

```yaml
---
name: agent-name            # Lowercase, hyphens
team: "NN — Team Name"      # Numbered team reference
repo: agent-name-agent      # GitHub repo name
version: 0.1.0              # Semantic version
status: seed                # seed | active | stable | deprecated
---
```

### Pitfalls in Agent Creation

- **Nesting agents too deep**: Agents go directly under the team dir, NOT under `agents/` subdirectory. `teams/NN-name/swarm-orchestrator/AGENTS.md` ✓ — `teams/NN-name/agents/swarm-orchestrator/AGENTS.md` ✗
- **AGENT_UNIVERSE.md table formatting**: Each row MUST start with a single `|`. Triple pipes (`|||`) or extra spaces break markdown rendering.
- **Orchestrator team reference**: The orchestrator's AGENTS.md says `team: "00 — Orchestrator"`. Verify team numbers in master index vs each agent's frontmatter.
- **Dependency count in orchestrator**: After adding/removing agents, update the `"All XX specialist agents"` line in `orchestrator/AGENTS.md`.
- **TEAM.md must exist**: Every team needs a TEAM.md. Missing TEAM.md causes integration gaps.
- **Agent count verification**: `find teams/*/ -maxdepth 2 -name "AGENTS.md" | wc -l` must match the header count in AGENT_UNIVERSE.md.

## Foreign Codebase Integration (e.g., ShadowForge Swarm)

When a 400+ file external codebase needs mapping into the agent-universe structure, use this phased pattern:

### Phase 1: Full Inventory
```bash
find /source/path -type f | sort
find /source/path -name "*.py" -not -path "*__pycache__*" | sort
```

### Phase 2: Categorize Components

| Category | Destination | Example |
|----------|-------------|---------|
| Agent designs/descriptions | New `teams/{NN}-{team}/` | Crew-level agents |
| Executable code (Python) | Destination agent's `tooling/` | C2 modules |
| MCP server code | `infrastructure/mcp-servers/src/` | Server implementations |
| Skill implementations | `shared/skills/src/` | Skills with BaseSkill pattern |
| Tool wrappers | `shared/tools/src/` | Tools with BaseTool pattern |
| Infrastructure configs | `infrastructure/deploy/`, `swarm-configs/` | Docker, Ansible, NATS |
| Assessment docs | `infrastructure/docs/` | Build matrices, READMEs |

### Phase 3: Build Matrix (Security-Related Codebases)

Use this methodology to determine what gets built:

| Icon | Meaning | Action |
|------|---------|--------|
| ✅ **Build** | Legitimate technology | Full implementation with docs |
| ⚠️ **Reframe** | Tech is legitimate, context/intent is not | Build with DEFENSIVE framing |
| ❌ **Won't Build** | Directly implements illegal activity | Document why with legal/ethical rationale |

**Criteria for ❌:**
- Unauthorized computer access (CFAA §1030)
- Identity theft, fraud, or money laundering
- Evading detection for criminal purposes
- Automation of exploitation without authorization
- Covert criminal communications

### Phase 4: Parallel Integration Waves

Use `delegate_task(tasks=[...])` for heavy lifting:
- **Wave 1** — Create all new agent dirs with AGENTS.md/README.md/config
- **Wave 2** — Copy MCP servers, skills, tools to shared dirs with INDEX.md
- **Wave 3** — Copy infrastructure configs, framework docs, architecture guides
- **Wave 4** — Update master index, all TEAM.md files, create BUILD_RATIONALE.md

### Phase 5: Verify Integration

```bash
# Every team has TEAM.md
for d in teams/*/; do [ -f "$d/TEAM.md" ] && echo "✅ $(basename $d)" || echo "❌ $(basename $d)"; done

# Every agent has AGENTS.md
for d in teams/*/; do
  count=$(find "$d" -maxdepth 2 -name "AGENTS.md" | wc -l)
  echo "$(basename $d): $count agents"
done

# Master index matches reality
find . -path "./.git" -prune -o -name "AGENTS.md" -print | wc -l
```

### Phase 6: Update AGENT_UNIVERSE.md

The master index has these sections that need updating:
1. **Header**: `**XX specialist agents · NN teams · one monorepo**` — update counts
2. **Summary table**: Agent counts and domain descriptions per team
3. **Per-team agent tables**: Agent name → path → role
4. **Shared components**: MCP servers, skills, tools (if new)
5. **Footer**: unchanged

After any update, verify with `find teams/*/ -maxdepth 2 -name "AGENTS.md" | wc -l` against the header.

### Reference Files

- `references/agent-scaffold.md` — The canonical agent directory template with file contents (moved from absorbed agent-universe-engineering skill)
- `references/codebase-integration-checklist.md` — Step-by-step checklist for foreign codebase integration (moved from absorbed agent-universe-engineering skill)

## Adding a New Agent

1. Create directory: `teams/{NN}-{team-name}/{agent-name}/`
2. Create `config/`, `tooling/`, `templates/`, `docs/`, `tests/` subdirs
3. Write `AGENTS.md` with frontmatter + role/capabilities/tooling
4. Write `README.md` with overview, prerequisites, quick start, cross-references
5. Write `config/config.yaml` with MCP server references
6. Write `.env.example` with all required env vars
7. Create at least one tool script in `tooling/` (or placeholder)
8. Update team's `TEAM.md` to include new agent
9. Update `AGENT_UNIVERSE.md` master index

## Integrating External Codebases (Codebase Integration Pattern)

When an external codebase needs to be mapped into the agent-universe structure (e.g., a 428-file swarm framework like ShadowForge), use this pattern:

### Step 1: Full Inventory

Before moving anything, get a complete picture:

```bash
# Full file tree
find /source/path -type f | sort

# Python files only
find /source/path -name "*.py" -not -path "*__pycache__*" | sort
```

### Step 2: Categorize Each Component

Partition into destination categories:

| Category | Destination | Example |
|----------|-------------|---------|
| Agent designs/descriptions | New `teams/{NN}-{team}/` | Crew-level agents |
| Executable code (Python) | Destination agent's `tooling/` | Red team C2 modules |
| MCP server code | `infrastructure/mcp-servers/src/` | Server implementations |
| Skill implementations | `shared/skills/src/` | Skills with BaseSkill pattern |
| Tool wrappers | `shared/tools/src/` | Tools with BaseTool pattern |
| Infrastructure configs | `infrastructure/deploy/`, `infrastructure/swarm-configs/` | Docker, Ansible, NATS |
| Reference docs | Target team's `docs/` or `infrastructure/docs/` | Architecture guides |
| Assessment/evaluation docs | `infrastructure/docs/` | Build matrices, READMEs |

### Step 3: Determine What to Build vs. What Not to Build

For security-related codebases, use the **build matrix methodology** (✅/⚠️/❌):

| Icon | Meaning | Action |
|------|---------|--------|
| ✅ **Build** | Fully legitimate technology. No concerns. | Build full implementation with docs. |
| ⚠️ **Reframe** | Technology is legitimate; the *context/intent* is not. | Build with DEFENSIVE framing — describe the legitimate use case (security testing, compliance monitoring, privacy research) and strip offensive context. |
| ❌ **Won't Build** | Directly implements illegal activity (fraud, money laundering, identity theft, unauthorized access). | Do NOT build. Document why with specific legal/ethical rationale and link to legitimate alternatives. |

Criteria for ❌:
- Implements unauthorized computer access (CFAA 18 U.S.C. § 1030)
- Directly facilitates identity theft, fraud, or money laundering
- Evades detection for criminal purposes
- Automates exploitation of vulnerabilities without authorization
- Enables covert criminal communications

### Step 4: Launch Parallel Integration Waves

Use `delegate_task(tasks=[...])` for the heavy lifting. Each wave handles a category.

**Wave 1 — Agent directories:** Create all new agent dirs with full AGENTS.md/README.md/config/.env.example. Copy source tooling.

**Wave 2 — Infrastructure:** Copy MCP servers, skills, tools to shared dirs. Create INDEX.md files.

**Wave 3 — Docs:** Copy infrastructure configs, framework docs, architecture guides.

**Wave 4 — Finalize:** Update master index, all TEAM.md files, create BUILD_RATIONALE.md for ❌ items.

### Step 5: Verify Integration

```bash
# Check: every team has TEAM.md
for d in teams/*/; do [ -f "$d/TEAM.md" ] && echo "✅ $(basename $d)" || echo "❌ $(basename $d)"; done

# Check: every agent has AGENTS.md
for d in teams/*/; do 
  count=$(find "$d" -maxdepth 2 -name "AGENTS.md" | wc -l)
  echo "$(basename $d): $count agents"
done

# Check: master index agent count matches reality
find . -path "./.git" -prune -o -name "AGENTS.md" -print | wc -l
```

## Cross-Team Component Registration

### MCP Servers

All MCP servers live in `infrastructure/mcp-servers/`. Each server is documented in `INDEX.md`:

| Server | Source File | Purpose | Tools |
|--------|-------------|---------|-------|
| document-mcp | `src/document_server.py` | Document processing | extract_entities, classify_document |
| threat-intel-mcp | `src/threat_intel_server.py` | CTI aggregation | check_ip, check_domain, check_hash |

### Skills

All shared skills in `shared/skills/` with INDEX.md listing:
- Skill name, source file, primary MCP server, key tools, output
- Dependency graph showing skill interactions

### Tools

All shared tool wrappers in `shared/tools/` with INDEX.md listing:
- Tool name, source file, role, domain, integration targets

## Pitfalls

- **Don't leave agents in `agents/` subdirs** — Team 09's agents were created under `agents/swarm-orchestrator/` by some scaffold tools. Agent directories must be directly under the team directory: `teams/09-swarm/agents/swarm-orchestrator/` → `teams/09-swarm/swarm-orchestrator/`.
- **Don't mismatch team numbers** — The orchestrator's AGENTS.md originally said `"07 — Command & Orchestration"` when 07 was the Recon Team. The orchestrator is `"00 — Orchestrator"`. Verify team numbers in master index vs. each agent's frontmatter.
- **Don't declare agents in master index that don't exist on disk** — Team 05 had "Criminal Defense Intelligence" in AGENT_UNIVERSE.md but the directory was never created. Always cross-reference.
- **TEAM.md agent counts must match master index counts.** If they diverge, update both.
- **MASTER INDEX MUST BE UPDATED whenever agents are added or removed.** The AGENT_UNIVERSE.md counts and table of contents are the single source of truth.
- **`__pycache__/` and `*.pyc` files should not be tracked.** Already in `.gitignore`.
- **Commit frequently after each integration wave** — file moves and copies are hard to reverse.
- **Leave source directories intact** when integrating — copy, don't move, so reference provenance is preserved.

## Verification Steps

- [ ] Every team has a `TEAM.md` file
- [ ] Every agent has `AGENTS.md` + `README.md` + `config/config.yaml` + `.env.example`
- [ ] Agent count in `AGENT_UNIVERSE.md` matches `find . -name "AGENTS.md" | wc -l`
- [ ] Agent count in each team's `TEAM.md` matches the directory listing
- [ ] All MCP servers are documented in `infrastructure/mcp-servers/INDEX.md`
- [ ] All shared skills are documented in `shared/skills/INDEX.md`
- [ ] All shared tools are documented in `shared/tools/INDEX.md`
- [ ] ❌ items have BUILD_RATIONALE.md with specific legal/ethical rationale
- [ ] `new/` experimental directories have a README explaining their status
- [ ] Orchestrator's dependency count (`"All N specialist agents in Teams 01-M"`) is accurate
