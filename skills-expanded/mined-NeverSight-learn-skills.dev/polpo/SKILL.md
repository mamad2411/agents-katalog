---
name: polpo
description: Build production AI agents with Polpo — the open composable backend for agents with integrated sandbox runtime, tasks and workflows, and AI Gateway. Use this skill whenever working with Polpo projects, .polpo/ directories, agent configuration, tools, memory, vault, teams, tasks, missions, skills, deployments, or the Polpo CLI/API. Triggers on "polpo", "agent", ".polpo/", "polpo.json", "agents.json", "polpo deploy", "polpo create", "polpo link", "polpo install", agent tools, agent memory, agent vault, system prompt design, multi-agent architecture, or any mention of Polpo.
---

# Polpo

Open composable backend for agents with integrated sandbox runtime, tasks and workflows, and AI Gateway. Agents are defined as config, deployed to isolated sandboxes, and called via an OpenAI-compatible API.

Never guess about Polpo internals — use this skill and reference files. When this skill doesn't cover something, follow the lookup chain at the bottom.

## Project Filesystem

Every Polpo project lives in a `.polpo/` directory. Three separate config files:

```
.polpo/
├── polpo.json              # Project link config (name, slug, projectId)
├── agents.json             # Agent definitions (array of wrapped configs)
├── teams.json              # Team definitions (array of {name, description})
├── memory.md               # Project-level shared memory (all agents read this)
├── memory/                 # Per-agent memory files
│   └── <agent-name>.md
├── skills/                 # Project-local skill packs
│   └── my-skill/
│       └── SKILL.md
├── playbooks/              # Reusable mission templates (YAML)
├── missions/               # Mission definitions
└── .env.local.example      # Env template (POLPO_API_KEY, POLPO_API_URL)
```

### polpo.json — Project link

Created by `polpo create` or `polpo link`. Links the local folder to a cloud project:

```json
{
  "project": "My Project",
  "projectSlug": "k7m2xpg9tn4bqw8e1jrf",
  "projectId": "3d606bce-73a4-49a2-9e6e-72883ecacaa5"
}
```

### agents.json — Agent definitions

Array of wrapped agent configs. Each entry pairs an agent with a team:

```json
[
  {
    "agent": {
      "name": "coder",
      "role": "Senior Engineer",
      "model": "xai/grok-4-fast",
      "systemPrompt": "You are a senior engineer. Write clean, tested code.",
      "allowedTools": ["bash", "read", "write", "edit", "glob", "grep"],
      "reasoning": "medium"
    },
    "teamName": "default"
  }
]
```

For the complete AgentConfig field reference, read [references/agent-config.md](references/agent-config.md).

### teams.json — Team definitions

```json
[
  { "name": "default", "description": "Default team" }
]
```

## Core Concepts

| Concept | What it is |
|---------|-----------|
| **Agent** | AI entity with model, tools, prompt, identity. Defined in `agents.json`. |
| **Team** | Named group of agents. Defined in `teams.json`. |
| **Task** | Unit of work assigned to an agent. Status lifecycle, expectations, retry policy. |
| **Mission** | Multi-task workflow. Can be scheduled (cron), has checkpoints and quality gates. |
| **Memory** | Persistent text context. Project-level (`memory.md`) or agent-level (`memory/<name>.md`). Auto-injected into system prompt. |
| **Vault** | Encrypted per-agent credential store. Agents access via `vault_get` tool. |
| **Skill** | A SKILL.md file teaching an agent domain knowledge. Injected into system prompt. |
| **Tool** | A capability an agent can invoke. Must be whitelisted in `allowedTools`. |

## Model Selection

Format: `provider/model-name`.

| Use Case | Model | Why |
|----------|-------|-----|
| Fast coding | `xai/grok-4-fast` | Fast, strong tool use |
| Complex reasoning | `anthropic/claude-sonnet-4` | Best reasoning |
| Budget tasks | `xai/grok-3-mini-fast` | Cheap, fast |
| Vision/multimodal | `openai/gpt-4o` | Strong multimodal |

## Tools

58 tools across 10 categories. Agents have NO tools by default — each must be explicitly listed in `allowedTools`. Use glob patterns for categories: `"browser_*"`, `"email_*"`.

**Coding:** `bash`, `read`, `write`, `edit`, `glob`, `grep`
**Files/HTTP:** `ls`, `http_fetch`, `http_download`, `register_outcome`
**Documents:** `pdf_*` (4), `excel_*` (4), `docx_*` (2)
**Communication:** `email_*` (8), `phone_*` (7)
**Browser:** `browser_*` (17 — full Playwright automation)
**Media:** `image_generate`, `image_analyze`, `video_generate`, `audio_transcribe`, `audio_speak`
**Search:** `search_web`, `search_find_similar`
**Agent systems:** `vault_get`, `vault_list`, `memory_*` (4)

For the complete tool catalog with descriptions, read [references/tools.md](references/tools.md).

## System Prompt

Keep it focused — Claude is already smart.

```
You are {name}, a {role}.
{Core instructions — what to do, how to approach it}
{Constraints — what NOT to do}
{Output format if relevant}
```

## CLI Commands

| Command | What it does |
|---------|-------------|
| `polpo login` | Authenticate (device-code browser flow) |
| `polpo logout` | Sign out |
| `polpo create` | Interactive wizard: create project + scaffold .polpo/ |
| `polpo link --project-id <uuid>` | Bind current directory to existing project |
| `polpo deploy` | Push .polpo/ to the cloud |
| `polpo install --client <agents>` | Install Polpo skills for coding agents (auth + skills) |
| `polpo status` | Deployment status |
| `polpo logs` | Cloud execution logs |
| `polpo models` | List available models |
| `polpo byok` | Bring-your-own-key for LLM providers |
| `polpo projects` | List/manage projects |
| `polpo orgs` | Organization management |
| `polpo whoami` | Show authenticated user |
| `polpo update` | Self-update CLI |

## Deployment Flow

1. Edit `.polpo/agents.json` (agent definitions)
2. Edit `.polpo/teams.json` (team structure)
3. `polpo deploy` → validates + pushes to cloud
4. Cloud provisions isolated sandbox + per-project database
5. Call agents via `POST {slug}.polpo.cloud/v1/chat/completions`

```bash
# One-time setup
polpo login
polpo link --project-id <uuid>

# Edit → deploy cycle
vim .polpo/agents.json
polpo deploy
```

## Calling Agents

API is OpenAI-compatible. Two modes:

**Agent-direct** (specify which agent):
```bash
curl https://{slug}.polpo.cloud/v1/chat/completions \
  -H "Authorization: Bearer $POLPO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model": "polpo", "agent": "coder", "stream": true,
        "messages": [{"role":"user","content":"Hello"}] }'
```

**Orchestrator** (let Polpo route to the right agent): omit the `"agent"` field.

## Detailed References

Read only when you need depth on a specific topic:

- **[Agent Config Schema](references/agent-config.md)** — every field in AgentConfig
- **[Tool Catalog](references/tools.md)** — all 58 tools with descriptions
- **[Memory System](references/memory.md)** — project vs agent memory, API, auto-accumulation
- **[Vault System](references/vault.md)** — credential types, scoping, resolution chain
- **[Teams](references/teams.md)** — team structure, multi-team, volatile agents
- **[Tasks & Missions](references/tasks-missions.md)** — lifecycle, expectations, retry, scheduling
- **[Agent Patterns](references/patterns.md)** — multi-agent architectures, specialization
- **[API Endpoints](references/api-endpoints.md)** — all server routes

## Information Lookup Chain

When this skill doesn't answer:

1. **Search the source code** first — grep/read in the Polpo OSS repo. Core types: `packages/core/src/types.ts`. Tools: `packages/tools/src/`. Routes: `packages/server/src/routes/`. CLI: `packages/cli/src/commands/`.
2. **Check docs.polpo.sh** only if source doesn't answer — crawl structure first (`/docs/`, `/api-reference/`), then follow relevant links.
3. **Never guess** about Polpo internals. If unsure, say so.
