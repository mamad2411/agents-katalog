---
name: gitclaw-agent
description: Create, configure, and run AI agents using the GitAgent spec and GitClaw runtime. Use when the user wants to build an AI agent, scaffold an agent folder, write SOUL.md/RULES.md/skills, run agents with GitClaw, export agents, set up compliance, connect external apps, create workflows, configure hooks, manage sub-agents, or anything related to GitAgent/GitClaw.
---

# GitClaw + GitAgent — Complete Agent Builder

You help the user create and manage AI agents using the GitAgent specification and GitClaw runtime.

## What is what

- **GitAgent** — a spec/standard that defines how an AI agent is structured as a folder of files. Like HTML for agents.
- **GitClaw** — the runtime engine that reads a GitAgent folder and runs it. Like Chrome for HTML. Available as CLI + Node.js SDK.
- **gitagent** (CLI) — scaffolds, validates, imports, exports, and manages agent folders
- **gitclaw** (CLI) — runs agents, manages sessions, commits memory, connects to external apps

## Prerequisites

```bash
# Option 1: npm
npm install -g gitclaw                      # runtime engine
npm install -g @open-gitagent/gitagent      # spec CLI (validate/export/import)

# Option 2: one-command bash installer
bash <(curl -fsSL "https://raw.githubusercontent.com/open-gitagent/gitclaw/main/install.sh?$(date +%s)")
```

---

# PART 1: CREATING AGENTS

## Step 1: Initialize

Three template options:

```bash
gitagent init --template minimal    # agent.yaml + SOUL.md only
gitagent init --template standard   # + RULES.md, AGENTS.md, skills/, knowledge/, tools/
gitagent init --template full       # + memory/, hooks/, examples/, agents/, compliance/, config/
```

Or use GitClaw directly (also scaffolds + starts interactive session):
```bash
gitclaw init
```

## Step 2: Configure agent.yaml (the manifest)

```yaml
spec_version: "0.1.0"
name: my-agent                          # kebab-case, required
version: 1.0.0                          # semver, required
description: "What this agent does"     # required
author: "name"
license: "MIT"
tags: [tag1, tag2]

model:
  preferred: "anthropic:claude-sonnet-4-6"
  fallback: ["openai:gpt-4o", "google:gemini-2.0-flash"]
  constraints:
    temperature: 0.7
    max_tokens: 4096
    top_p: 0.9

tools: [cli, read, write, memory]

skills:
  - skills/skill-name

agents:
  sub-agent-name:
    delegation:
      mode: auto            # or manual
      triggers: ["review", "audit"]

extends: "https://github.com/org/base-agent.git"   # inherit from parent agent

dependencies:
  - name: fact-checker
    source: https://github.com/org/fact-checker.git
    version: "^1.0.0"
    mount: agents/fact-checker

runtime:
  max_turns: 50
  timeout: 120

# Compliance (see Part 6)
compliance:
  risk_level: medium
  human_in_the_loop: conditional

# A2A protocol
a2a:
  url: https://api.example.com/agent
  capabilities: [review, summarize]
  authentication: bearer
  protocols: ["a2a/1.0"]

# Plugins
plugins:
  plugin-name:
    enabled: true
    source: "https://github.com/org/plugin.git"
    version: "main"
    config:
      api_key: "${MY_API_KEY}"
```

## Step 3: Write SOUL.md (agent identity — MOST IMPORTANT FILE)

SOUL.md is the system prompt. It defines WHO the agent is. Tips:
- Be specific, not vague. Vague instructions = vague behavior.
- Tell the agent HOW to use tools: "Run `ls memory/` then read recent files"
- Tell the agent HOW to get the date: "Run `date +%Y-%m-%d`"
- Tell the agent to append, not overwrite: "Read existing files before writing"
- Include: identity, purpose, behavior rules, tool usage instructions

## Step 4: Write RULES.md (hard boundaries)

Non-negotiable constraints the agent must NEVER break.
- What to never do (delete files, run destructive commands, fabricate data)
- What to always do (check date, append to files, use structured format)

## Step 5: Write DUTIES.md (segregation of duties — for compliance)

Defines role separation for regulated environments:
```markdown
# Duties
- Role: analyst — can research, draft reports
- Role: reviewer — can approve, reject, escalate
- Conflict: analyst and reviewer must be different agents
```

In agent.yaml:
```yaml
compliance:
  segregation_of_duties:
    roles:
      - id: maker
        permissions: [draft, submit]
      - id: checker
        permissions: [review, approve]
    conflicts: [[maker, checker]]
    assignments:
      maker: agent-a
      checker: agent-b
    isolation: full         # full, shared, or none
    enforcement: strict     # strict or advisory
    handoffs:
      regulatory_filing:
        requires: [analyst, reviewer]
```

## Step 6: Add .env for API keys

```
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
GEMINI_API_KEY=xxx
COMPOSIO_API_KEY=ak_xxx
COMPOSIO_USER_ID=default
GITHUB_TOKEN=ghp_xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_ALLOWED_USERS=user1,user2
LYZR_API_KEY=xxx
```

Always add `.env` to `.gitignore`.

---

# PART 2: SKILLS

## Creating skills

Each skill lives in `skills/<name>/SKILL.md`:

```markdown
---
name: skill-name
description: When to use this skill — one line (max 1024 chars)
license: MIT
allowed-tools: cli read write
metadata:
  author: your-name
  version: 1.0.0
  category: development
  risk_tier: low
  regulatory_frameworks: []
---

# Skill Name

When the user asks to <trigger condition>:

1. Step one
2. Step two
3. Step three

## Output Format
<define expected output structure>
```

Skill folder can include:
```
skills/my-skill/
├── SKILL.md          # instructions (required)
├── scripts/          # executable implementations
├── references/       # supplementary docs
├── assets/           # static resources
└── agents/           # skill-specific sub-agents
```

## Skill discovery priority (first match wins)

1. `<agent>/skills/`
2. `<agent>/.agents/skills/`
3. `<agent>/.claude/skills/`
4. `<agent>/.github/skills/`
5. `~/.agents/skills/` (user global)

## Installing skills from registries

```bash
gitagent skills search "code review"              # search registries
gitagent skills install <skill-id>                 # install
gitagent skills install <skill-id> --global        # install globally
gitagent skills list                               # list installed
gitagent skills list --local                       # list local only
gitagent skills info <skill-id>                    # inspect details
```

Or via skills.sh:
```bash
npx skills add open-gitagent/enterprise-skills --skill contract-review-analysis
```

## Invoking skills at runtime

Use the `/skill:` prefix to invoke a skill directly in a GitClaw session:
```bash
/skill:code-review Review the auth module
/skill:bug-triage Investigate the crash in payments
```

---

# PART 3: TOOLS

## Built-in GitClaw tools

- `cli` — execute shell commands
- `read` — read files with pagination
- `write` — write/create files
- `memory` — load/save git-committed memory

## Custom declarative tools

Define in `tools/<name>.yaml`:

```yaml
name: search_docs
description: "Search the documentation"
version: 1.0.0
input_schema:
  properties:
    query: { type: string, description: "Search query" }
    limit: { type: number, description: "Max results" }
  required: [query]
output_schema:
  properties:
    results: { type: array }
implementation:
  script: scripts/search.sh
  runtime: bash           # or node (default)
  timeout: 120
annotations:
  requires_confirmation: false
  read_only: true
  cost: low
```

Tool scripts receive JSON via stdin, return JSON via stdout. 120-second timeout.

## Tool metadata

Each tool can declare:
- `isConcurrencySafe` — can run in parallel (default: false)
- `isReadOnly` — only reads (default: false)
- `isDestructive` — irreversible action (default: false)
- `maxResultSizeChars` — truncate output (default: 50000)

## Tool control via SDK

```typescript
query({
  tools: [customTool],          // add custom tools
  replaceBuiltinTools: true,    // skip cli/read/write/memory
  allowedTools: ["read"],       // allowlist
  disallowedTools: ["cli"],     // denylist
})
```

---

# PART 4: RUNNING AGENTS

## GitClaw CLI

```bash
# Run with a message
gitclaw --dir ./my-agent "your message"

# Run interactively (REPL)
gitclaw --dir ./my-agent

# Short flag
gitclaw -d ./my-agent -p "your message"

# Override model
gitclaw --dir ./my-agent --model anthropic:claude-sonnet-4-6 "message"

# Run on a GitHub repo (clones, creates session branch, auto-commits)
gitclaw --repo https://github.com/org/repo --pat ghp_xxx "Fix the login bug"

# Resume an existing session
gitclaw --session gitclaw/session-a1b2c3d4 --repo https://github.com/org/repo "Continue"

# Run in sandbox
gitclaw --dir ./my-agent --sandbox "message"

# Use environment config
gitclaw --dir ./my-agent --env production "message"
```

## GitAgent run (auto-detects adapter)

```bash
gitagent run --dir ./my-agent --prompt "message"
gitagent run --repo https://github.com/org/agent-repo --prompt "message"
gitagent run --adapter claude --dir ./my-agent            # force specific adapter
gitagent run --repo https://github.com/org/repo --refresh # pull latest
gitagent run --repo https://github.com/org/repo --no-cache # fresh clone
```

## SDK usage (Node.js — in-process, no subprocess)

```typescript
import { query } from "gitclaw";

const q = query({
  prompt: "Review this codebase",
  dir: "./my-agent",
  model: "anthropic:claude-sonnet-4-6",
  maxTurns: 30,
  systemPrompt: "Override the full system prompt",    // optional
  systemPromptSuffix: "Append to system prompt",      // optional
  constraints: { temperature: 0.7, maxTokens: 4096 },
  abortController: new AbortController(),             // for cancellation
  hooks: { /* see hooks section */ },
});

for await (const msg of q) {
  if (msg.type === "delta") process.stdout.write(msg.content);
  if (msg.type === "tool_use") console.log(`Tool: ${msg.toolName}`);
  if (msg.type === "tool_result") console.log(`Result: ${msg.content}`);
  if (msg.type === "assistant") console.log("\nDone.");
  if (msg.type === "system") console.log(`System: ${msg.subtype}`);
}

// Helper methods on the query object
q.abort();                  // cancel execution
q.steer("new message");    // inject message mid-stream
q.sessionId();             // get session ID
q.manifest();              // get loaded manifest
q.messages();              // get all messages
q.costs();                 // get token/cost tracking
```

## SDK message types

| Type | Description | Key Fields |
|---|---|---|
| `delta` | Streaming text chunk | `deltaType` (text/thinking), `content` |
| `assistant` | Complete LLM response | `content`, `model`, `provider`, `usage`, `thinking`, `stopReason` |
| `tool_use` | Tool invocation | `toolName`, `args`, `toolCallId` |
| `tool_result` | Tool output | `content`, `isError`, `toolCallId` |
| `system` | Lifecycle events | `subtype` (session_start/end, hook_blocked, error) |
| `user` | User message | `content` |

## Custom tools via SDK

```typescript
import { query, tool } from "gitclaw";

const weatherTool = tool(
  "get_weather",
  "Get current weather for a city",
  { properties: { city: { type: "string" } }, required: ["city"] },
  async ({ city }) => `Weather in ${city}: 72°F, sunny`
);

for await (const msg of query({
  prompt: "What's the weather in NYC?",
  dir: "./my-agent",
  tools: [weatherTool],
})) { ... }
```

---

# PART 5: WORKFLOWS, HOOKS, MEMORY, KNOWLEDGE

## Workflows

Multi-step YAML playbooks in `workflows/<name>.yaml`:

```yaml
name: deploy-flow
description: "Deploy to production"
version: 1.0.0
inputs:
  - name: branch
    type: string
    required: true
    default: main
outputs:
  - name: deploy_url
    type: string
steps:
  - id: review
    action: "Review changes on branch"
    skill: code-review
    inputs:
      branch: "${{ inputs.branch }}"
    outputs: [review_result]
  - id: deploy
    action: "Deploy to staging"
    skill: deploy
    depends_on: [review]
    inputs:
      branch: "${{ inputs.branch }}"
      review: "${{ steps.review.outputs.review_result }}"
    conditions:
      - "${{ steps.review.outputs.review_result }} == 'approved'"
    compliance:
      audit_level: full
      requires_approval: true
error_handling:
  on_step_failure: escalate
  escalation_target: engineering-lead
```

Trigger workflows with `@flow_name` syntax in GitClaw.

## Hooks (lifecycle control)

### Script-based hooks (`hooks/hooks.yaml`)

```yaml
on_session_start:
  - script: hooks/scripts/init.sh
    timeout: 10
    description: "Initialize session"
    fail_open: true           # continue on failure

pre_tool_use:
  - script: hooks/scripts/guard.sh
    timeout: 10
    description: "Block dangerous commands"
    fail_open: false          # halt on failure

post_response:
  - script: hooks/scripts/log.sh

on_error:
  - script: hooks/scripts/on-error.sh
```

Hook scripts receive JSON via stdin, return `{ "action": "allow" }`, `{ "action": "block", "reason": "..." }`, or `{ "action": "modify", "args": {...} }`.

### SDK programmatic hooks

```typescript
query({
  hooks: {
    sessionStart: async (ctx) => { console.log("Session started"); },
    preToolUse: async (ctx) => {
      if (ctx.toolName === "cli" && ctx.args.command?.includes("rm -rf"))
        return { action: "block", reason: "Destructive command blocked" };
      return { action: "allow" };
    },
    postResponse: async (ctx) => { /* log response */ },
    onError: async (ctx) => { /* handle errors */ },
  },
})
```

## Memory

Memory persists across sessions via git commits.

```
memory/
├── MEMORY.md           # working memory (200-line max, auto-included in prompt)
└── runtime/
    ├── dailylog.md     # daily activity log
    ├── context.md      # session context
    └── key-decisions.md
```

Optional `memory/memory.yaml` for config:
```yaml
retention: 30d
embedding: true
retrieval: semantic
```

GitClaw auto-commits memory changes to git after each session.

## Knowledge

Reference documents the agent can consult. Define in `knowledge/index.yaml`:

```yaml
entries:
  - path: docs/architecture.md
    tags: [architecture, design]
    priority: high
    always_load: true       # injected into system prompt
  - path: docs/api-reference.md
    tags: [api]
    priority: medium        # available on-demand via read tool
```

## Few-shot examples

Put example interactions in `examples/` as markdown files. They're loaded alphabetically and injected into the system prompt as `<example>` blocks for in-context learning.

---

# PART 6: COMPLIANCE & AUDIT

## Compliance config in agent.yaml

```yaml
compliance:
  risk_level: high               # low, medium, high, critical
  human_in_the_loop: always      # always, conditional, advisory, none

  supervision:
    designated_supervisor: "compliance-officer"
    review_cadence: weekly
    escalation_triggers:
      confidence_threshold: 0.6
      action_types: [financial, regulatory]
      error_patterns: ["compliance*"]
    override_capability: true
    kill_switch: true

  recordkeeping:
    audit_logging: true
    log_format: structured_json
    retention_period: "7y"
    log_contents: [decisions, tool_calls, reasoning]
    immutable: true

  model_risk:                     # SR 11-7
    inventory_id: "MRM-2024-001"
    validation_cadence: quarterly
    validation_type: independent
    conceptual_soundness: true
    ongoing_monitoring: true
    outcomes_analysis: true
    drift_detection: true

  data_governance:
    pii_handling: redact          # redact, encrypt, prohibit, allow
    data_classification: confidential
    consent_required: true
    cross_border: false
    bias_testing: true

  communications:                 # FINRA 2210
    type: retail
    pre_review_required: true
    fair_balanced: true
    no_misleading: true
    disclosures_required: true

  segregation_of_duties:          # see DUTIES.md section
    roles: [...]
    conflicts: [...]

  vendor_management:              # SR 23-4
    due_diligence_complete: true
    soc_report_required: true
```

## Supported regulatory frameworks

FINRA (3110, 4511, 2210, 2010, 2111, 3120, 4370), Federal Reserve (SR 11-7, SR 23-4, SR 21-8), SEC (Reg S-P, Rule 17a-4), CFPB (Circular 2022-03), OCC, FDIC, BSA/AML, EU AI Act, UK FCA, GDPR, MiCA

## Compliance artifacts

```
compliance/
├── risk-assessment.md
├── regulatory-map.yaml
└── validation-schedule.yaml
```

Audit logs are written to `.gitagent/audit.jsonl` (structured JSON, one entry per line).

## Commands

```bash
gitagent validate --compliance    # validate compliance rules
gitagent audit                    # generate full compliance report
```

---

# PART 7: SUB-AGENTS

## Directory format (full agent)

```
agents/
└── reviewer/
    ├── agent.yaml
    ├── SOUL.md
    ├── skills/
    └── ...
```

## File format (lightweight)

```
agents/reviewer.md
```

With YAML frontmatter:
```markdown
---
name: reviewer
description: Reviews code for quality
model: anthropic:claude-sonnet-4-6
---

You are a code reviewer. Focus on correctness, security, and readability.
```

## Delegation config in parent agent.yaml

```yaml
agents:
  reviewer:
    delegation:
      mode: auto
      triggers: ["review", "check code", "audit"]
```

---

# PART 8: PLUGINS

Plugins extend agents with tools, hooks, skills, and prompt content.

## Plugin CLI

```bash
gitclaw plugin install https://github.com/org/my-plugin.git
gitclaw plugin list
gitclaw plugin enable my-plugin
gitclaw plugin disable my-plugin
gitclaw plugin remove my-plugin
gitclaw plugin init my-plugin       # scaffold a new plugin
```

## Plugin locations

1. `<agent>/plugins/<name>/` (local)
2. `~/.gitclaw/plugins/<name>/` (global)
3. `<agent>/.gitagent/plugins/<name>/` (installed from remote)

## Plugin manifest (`plugin.yaml`)

```yaml
id: my-plugin
name: My Plugin
version: 1.0.0
description: "What this plugin does"
author: "name"
license: "MIT"
provides:
  tools: true
  hooks:
    on_session_start: [{ script: "scripts/init.sh", description: "..." }]
    pre_tool_use: [{ script: "scripts/guard.sh" }]
  skills: true
  prompt: "prompt.md"       # extra system prompt content
config:
  properties:
    api_key: { type: string, env: "MY_API_KEY" }
  required: [api_key]
entry: "index.ts"           # programmatic entry point
engine: ">=0.3.0"           # minimum gitclaw version
```

Enable/disable per plugin in agent.yaml:
```yaml
plugins:
  my-plugin:
    enabled: true
    config:
      api_key: "${MY_PLUGIN_KEY}"
```

## Programmatic plugin API (entry: `index.ts`)

Methods available inside the plugin entry point:
- `registerTool(tool)` — add a custom tool
- `registerHook(event, handler)` — add a lifecycle hook
- `addPrompt(text)` — inject content into system prompt
- `registerMemoryLayer(layer)` — add a custom memory layer
- `logger.info/warn/error(msg)` — structured logging
- `pluginId` — the plugin's ID string
- `pluginDir` — absolute path to the plugin folder
- `config` — resolved config values (from `plugin.yaml` + agent.yaml overrides)

---

# PART 9: COMPOSIO INTEGRATIONS (500+ external apps)

Connect agents to Gmail, Slack, Google Calendar, Notion, Jira, GitHub, and 500+ more.

## Setup

1. Get API key from https://composio.dev
2. Add to `.env`:
```
COMPOSIO_API_KEY=ak_xxx
COMPOSIO_USER_ID=default
```
3. Connect apps through Composio's OAuth flow
4. GitClaw auto-discovers connected tools

## How it works

- Tools appear as `composio_<toolkit>_<action>` (e.g., `composio_gmail_SEND_EMAIL`)
- Semantic tool matching — GitClaw picks relevant tools per query
- OAuth handled by Composio's `initiateConnection()` with redirect URLs

## SOUL.md tip

```markdown
# Integrations
You are connected to Gmail and Slack via Composio.
- Use Gmail to send emails and read inbox
- Use Slack to post messages to channels
Always confirm with the user before sending external messages.
```

---

# PART 10: MESSAGING INTEGRATIONS

## Telegram

Set in `.env`:
```
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_ALLOWED_USERS=user1,user2
```

Supports file/photo upload and download (50MB limit).

## WhatsApp

Uses Baileys library with QR authentication. Tools available:
- `send_whatsapp_message` (by name or phone)
- `save_whatsapp_contact`
- `list_whatsapp_contacts`

## Message triggers

Auto-reply patterns for specific contacts/platforms:
- `create_trigger`, `list_triggers`, `delete_trigger`, `toggle_trigger`
- Regex or substring pattern matching
- Approval gates: pause workflows, await yes/no via Telegram/WhatsApp (5-min timeout)

---

# PART 11: SCHEDULES (Cron Jobs)

Define in `schedules/<name>.yaml`:

```yaml
id: daily-report
prompt: "Generate a daily summary report"
cron: "0 9 * * *"           # every day at 9am
mode: repeat                 # or "once"
enabled: true
```

For one-time execution:
```yaml
id: migration-check
prompt: "Verify the database migration"
mode: once
runAt: "2026-04-10T09:00:00Z"
enabled: true
```

Results logged to `.gitagent/schedule-logs/`.

---

# PART 12: SESSIONS & SANDBOX

## Sessions

- Each `--repo` run creates a session branch: `gitclaw/session-<8-char-hex>`
- Resume with `--session <branch>`
- Auto-commits changes, supports push

## Sandbox modes

**E2B sandbox (cloud VM):**
```bash
gitclaw --dir ./my-agent --sandbox "message"
```

**NVIDIA OpenShell (Docker + Landlock):**
- Read-only system dirs, read-write `/sandbox` and `/tmp`
- Network allowlist (default deny)
- GPU support with `--gpu` flag
- Audit or enforce modes

---

# PART 13: ENVIRONMENTS & INHERITANCE

## Environment configs

```
config/
├── default.yaml        # base config (always loaded)
├── staging.yaml        # staging overrides
└── production.yaml     # production overrides
```

```bash
gitclaw --dir ./my-agent --env production "message"
```

Deep-merges environment over default.

## Agent inheritance

```yaml
# child agent.yaml
extends: "https://github.com/org/base-agent.git"
```

Clones parent, deep-merges manifests (child overrides), combines RULES.md from both.

## Dependencies

```bash
gitagent install    # resolves semver, clones dependencies to mount paths
```

---

# PART 14: EXPORTING & IMPORTING

## Export formats (12 targets)

```bash
gitagent export --format <format> --output <file>
```

| Format | Output |
|---|---|
| `system-prompt` | Single markdown for any LLM |
| `claude-code` | `CLAUDE.md` |
| `cursor` | `.mdc` rule files |
| `openai` | Python source for OpenAI Agents SDK |
| `crewai` | YAML config with role/goal/backstory |
| `lyzr` | JSON payload for Lyzr Studio |
| `github` | GitHub Models API payload |
| `git` | Git-native execution format |
| `gemini` | Google Gemini CLI (`GEMINI.md` + `settings.json`) |
| `openclaw` | OpenClaw workspace |
| `opencode` | OpenCode instructions + config |
| `nanobot` | `config.json` + `system-prompt.md` |

## Import from existing tools

```bash
gitagent import --from claude <path>     # imports CLAUDE.md + .claude/skills/
gitagent import --from cursor <path>     # imports .cursorrules or AGENTS.md
gitagent import --from crewai <path>     # imports CrewAI YAML config
gitagent import --from opencode <path>   # imports OpenCode config
```

---

# PART 15: VALIDATION & OTHER COMMANDS

```bash
gitagent validate                  # validate spec structure
gitagent validate --compliance     # + compliance rules
gitagent info                      # display agent summary
gitagent audit                     # generate compliance report

# Lyzr Studio integration
gitagent lyzr create               # create agent on Lyzr Studio
gitagent lyzr update               # push updates
gitagent lyzr info                 # show linked agent ID
gitagent lyzr run --prompt "msg"   # clone + create + chat
```

---

# PART 16: AVAILABLE MODELS

- `openai:gpt-4o-mini`, `openai:gpt-4o`, `openai:o3`
- `anthropic:claude-sonnet-4-6`, `anthropic:claude-opus-4-6`
- `google:gemini-pro`, `google:gemini-2.0-flash`
- `groq:llama-3.3-70b-versatile`
- `mistral:mistral-large-latest`
- `xai` models (via pi-ai multi-model layer)
- Custom endpoints via `@baseUrl` syntax or env vars
- Local models via Ollama

---

# PART 17: GIT-NATIVE PATTERNS

- **Agent versioning** — git tags = agent versions (semver)
- **Branch-based deployment** — dev → staging → main
- **Human-in-the-loop** — agents open PRs for review before merging skills/memory
- **Agent forking** — fork a repo = fork an agent
- **Agent diff/audit** — `git diff` shows exactly what changed
- **CI/CD for agents** — GitHub Actions for validation, export, deployment
- **Secret management** — env vars, never committed

---

# PART 18: ENTERPRISE SKILLS (AUTO-MATCHING)

When creating a new agent, ALWAYS check if any pre-built enterprise skills from `open-gitagent/enterprise-skills` match the agent's purpose. If they do, install them automatically into the agent's `skills/` folder.

## How to install enterprise skills

Three ways to install — pick the best fit:

```bash
# Install an entire vertical (all skills for an industry)
npx skills add open-gitagent/enterprise-skills --vertical <vertical-name>

# Install a specific skill
npx skills add open-gitagent/enterprise-skills --skill <skill-id>

# Install ALL enterprise skills
npx skills add open-gitagent/enterprise-skills
```

## Available verticals (install by industry)

When the agent clearly belongs to one industry, use `--vertical` to install all skills for that vertical at once:

| Vertical | Command | Skills |
|---|---|---|
| Procurement | `--vertical procurement` | 23 skills (vendor management, invoicing, supplier risk, etc.) |
| Insurance | `--vertical insurance` | 20 skills (underwriting, claims, actuarial, etc.) |
| Banking | `--vertical banking` | 20 skills (lending, credit risk, trade finance, etc.) |
| Healthcare | `--vertical healthcare` | 20 skills (claims processing, medical coding, etc.) |
| CFO Office | `--vertical cfo-office` | 20 skills (budgeting, financial close, variance, etc.) |
| HR | `--vertical hr` | 20 skills (onboarding, performance, talent, workforce, etc.) |
| Sales | `--vertical sales` | 20 skills (lead qualification, forecasting, account planning, etc.) |
| Marketing | `--vertical marketing` | 20 skills (demand gen, attribution, brand, product marketing, etc.) |
| Legal & Compliance | `--vertical legal-compliance` | 20 skills (contract review, KYC, regulatory, governance, etc.) |
| IT & Operations | `--vertical it-operations` | 20 skills (incident management, change management, etc.) |

## Available individual skills (43 published, 203 total)

### Finance & Accounting
| Skill ID | Use when the agent needs to... |
|---|---|
| `budgeting-forecasting` | Create budgets, rolling forecasts, scenario planning |
| `financial-close-process` | Manage month-end/year-end close, reconciliations, journal entries |
| `variance-analysis` | Compare actuals vs budgets, identify performance gaps |
| `tax-compliance` | Handle income tax, sales tax, transfer pricing, multi-jurisdiction filing |
| `board-reporting` | Prepare board packages, KPI dashboards, governance reporting |

### Banking & Lending
| Skill ID | Use when the agent needs to... |
|---|---|
| `commercial-loan-underwriting` | Analyze financials, model cash flow, evaluate collateral, structure credit |
| `credit-risk-assessment` | Evaluate default probability under Basel III, CECL, fair lending |
| `mortgage-processing` | Process residential mortgage applications, documentation, closing |
| `trade-finance` | Handle letters of credit, documentary collections, supply chain financing |

### Insurance
| Skill ID | Use when the agent needs to... |
|---|---|
| `actuarial-analysis` | Loss reserving, rate making, experience rating, predictive modeling |
| `claims-adjudication` | Investigate claims, analyze coverage, determine liability, settle |
| `cyber-insurance-underwriting` | Assess cyber risk, evaluate security posture, structure coverage |
| `insurance-underwriting-commercial-property` | Evaluate commercial property risk, occupancy, loss history, pricing |
| `personal-lines-underwriting` | Underwrite homeowners, auto, umbrella policies |
| `policy-administration` | Manage policy lifecycle — issuance, endorsements, renewals, cancellations |
| `subrogation` | Manage recovery, demand preparation, negotiation, arbitration |

### Healthcare
| Skill ID | Use when the agent needs to... |
|---|---|
| `healthcare-claims-processing` | Process medical claims, adjudication rules, denial management |
| `medical-coding-icd10-cpt` | ICD-10 diagnosis coding, CPT procedure coding, compliance |

### Legal & Compliance
| Skill ID | Use when the agent needs to... |
|---|---|
| `contract-review-analysis` | Review contracts, identify risks, prepare markups, recommend changes |
| `corporate-governance` | Manage board procedures, committee charters, fiduciary duties |
| `intellectual-property-management` | Manage patents, trademarks, trade secrets, licensing |
| `kyc-aml-compliance` | Customer due diligence, transaction monitoring, SAR filing |
| `regulatory-compliance-monitoring` | Track regulatory changes, gap analysis, compliance reporting |

### Sales
| Skill ID | Use when the agent needs to... |
|---|---|
| `account-planning` | Stakeholder mapping, opportunity identification, competitive positioning |
| `competitive-intelligence` | Collect and analyze competitor intelligence, improve win rates |
| `lead-qualification` | Qualify leads using BANT, MEDDIC, CHAMP frameworks |
| `sales-forecasting` | Predict revenue from pipeline data, historical performance, market signals |

### Marketing
| Skill ID | Use when the agent needs to... |
|---|---|
| `brand-management` | Brand architecture, guidelines, equity measurement, crisis response |
| `demand-generation` | Inbound/outbound programs, lead nurturing, funnel optimization |
| `marketing-attribution` | Multi-touch attribution modeling (first-touch, last-touch, data-driven) |
| `product-marketing` | Positioning, messaging, launch playbooks, sales enablement |

### HR
| Skill ID | Use when the agent needs to... |
|---|---|
| `employee-onboarding` | Design onboarding programs, pre-boarding, 90-day integration |
| `performance-management` | Define expectations, measure outputs, provide feedback |
| `talent-acquisition` | End-to-end recruiting — sourcing, evaluating, converting candidates |
| `workforce-planning` | Scenario modeling, skills gap analysis, succession planning |

### Procurement & Vendor Management
| Skill ID | Use when the agent needs to... |
|---|---|
| `invoice-capture-agent` | OCR extraction from invoices, validation, ERP integration |
| `performance-review-agent` | Track vendor KPIs, SLA compliance, quality metrics |
| `qualification-scoring-agent` | Score vendor capabilities, financial health, references |
| `supplier-communication-agent` | Manage vendor communications, escalation workflows |
| `supplier-risk-agent` | Monitor vendor financial stability, geopolitical risk, ESG |
| `two-way-three-way-matching-agent` | Match invoices against POs and receipts, exception routing |
| `vendor-discovery-agent` | Find vendors by requirements, capability matching, market intelligence |
| `vendor-onboarding-agent` | Automate supplier registration, compliance verification |

## Auto-matching rules

When creating a new agent, follow this decision process:

### Step 1: Does the agent clearly belong to ONE vertical?

If yes → install the entire vertical:
```bash
npx skills add open-gitagent/enterprise-skills --vertical <vertical-name>
```

| If the agent is about... | Install vertical |
|---|---|
| Procurement, vendors, suppliers, invoicing | `--vertical procurement` |
| Insurance, claims, underwriting, policies | `--vertical insurance` |
| Banking, loans, credit, lending, trade finance | `--vertical banking` |
| Healthcare, medical, claims processing, coding | `--vertical healthcare` |
| Finance, budgeting, accounting, CFO, close | `--vertical cfo-office` |
| HR, hiring, onboarding, performance, workforce | `--vertical hr` |
| Sales, leads, pipeline, forecasting, accounts | `--vertical sales` |
| Marketing, demand gen, brand, attribution | `--vertical marketing` |
| Legal, compliance, contracts, regulatory, KYC | `--vertical legal-compliance` |
| IT, operations, incidents, change management | `--vertical it-operations` |

### Step 2: Does the agent span multiple verticals?

If yes → install specific skills that match:
```bash
npx skills add open-gitagent/enterprise-skills --skill <skill-id>
```

### Step 3: Is the agent not enterprise-related?

If it's a dev tool, personal agent, or non-enterprise use case → skip enterprise skills entirely. Write custom skills instead.

### After installing, always:
1. Add installed skills to `agent.yaml` under `skills:`
2. Tell the user which enterprise skills were added and why

### Examples

- "Create a procurement agent" → `npx skills add open-gitagent/enterprise-skills --vertical procurement` (all 23 procurement skills)
- "Create an insurance claims agent" → `npx skills add open-gitagent/enterprise-skills --vertical insurance` (all insurance skills)
- "Create a KYC compliance agent" → install specific: `kyc-aml-compliance`, `regulatory-compliance-monitoring`, `contract-review-analysis`
- "Create a sales pipeline agent" → `npx skills add open-gitagent/enterprise-skills --vertical sales` (all sales skills)
- "Create an HR onboarding agent" → `npx skills add open-gitagent/enterprise-skills --vertical hr` (all HR skills)
- "Create a CFO reporting agent" → `npx skills add open-gitagent/enterprise-skills --vertical cfo-office` (all CFO skills)
- "Create a DevLog agent" → skip enterprise skills (not enterprise-related)
- "Create a code review agent" → skip enterprise skills (dev tool)

---

# KEY PRINCIPLES

- Agent = folder of markdown files, not code
- Only `agent.yaml` + `SOUL.md` are required, everything else is optional
- Change behavior by editing a markdown file — no redeploy needed
- Memory is persisted via git commits automatically
- Skills are loaded dynamically at runtime
- Write once (GitAgent spec) → export to 14+ runtimes
- Compliance is built-in, not bolted on
