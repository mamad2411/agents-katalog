# Copilot Agent Suite — Installation & Usage Guide

## Prerequisites

- **VS Code** 1.99+ (February 2026 or later)
- **GitHub Copilot** extension installed and active (requires Copilot Individual, Business, or Enterprise)
- **Node.js** 18+ (for MCP servers that use `npx`)

## Installation

### Step 1: Copy the files to your repository

The agent suite lives entirely in version-controlled files. Copy the following structure into your project root:

```
your-project/
├── .github/
│   ├── copilot-instructions.md        # Always-on global instructions
│   ├── instructions/
│   │   ├── python.instructions.md     # Auto-applied to *.py files
│   │   ├── vue.instructions.md        # Auto-applied to *.vue, *.ts files
│   │   ├── react.instructions.md      # Auto-applied to *.tsx, *.jsx files
│   │   ├── testing.instructions.md    # Auto-applied to *.test.*, *.spec.* files
│   │   └── security.instructions.md   # Auto-applied to ALL files
│   ├── agents/
│   │   ├── orchestrator.agent.md      # Triage & delegate (Claude Sonnet 4.5)
│   │   ├── planner.agent.md           # Architecture & design (Claude Sonnet 4.5)
│   │   ├── implementer.agent.md       # Code generation (GPT-5.1-Codex)
│   │   ├── reviewer.agent.md          # Code review (Claude Opus 4.6)
│   │   ├── tester.agent.md            # Test generation (GPT-5.1-Codex)
│   │   ├── documenter.agent.md        # Documentation (Claude Haiku 4.5)
│   │   └── security.agent.md          # Security audit (Claude Opus 4.6)
│   └── prompts/
│       ├── new-feature.prompt.md      # /new-feature slash command
│       ├── new-endpoint.prompt.md     # /new-endpoint slash command
│       ├── new-component.prompt.md    # /new-component slash command
│       ├── security-audit.prompt.md   # /security-audit slash command
│       └── add-tests.prompt.md        # /add-tests slash command
├── .vscode/
│   └── mcp.json                       # MCP server configuration
├── AGENTS.md                          # Codex cloud sandbox instructions
└── ...your project files
```

### Step 2: Enable custom agents in VS Code

1. Open VS Code Settings (`Cmd+,` on macOS)
2. Search for `chat.agents.enabled`
3. Ensure it is set to `true`
4. Search for `chat.promptFiles`
5. Ensure it is set to `true`

### Step 3: Install MCP server dependencies (optional)

If you want to use the MCP servers (database queries, Docker management, package lookups):

```bash
# Test that MCP servers are available (they auto-install via npx)
npx -y @anthropic/mcp-server-postgres --help
npx -y mcp-server-docker --help
npx -y mcp-server-pacman --help
```

VS Code will prompt you to start MCP servers when an agent needs them. You can also start them manually via the Command Palette: `MCP: List Servers`.

### Step 4: Reload VS Code

After adding the files, reload the window (`Cmd+Shift+P` → `Developer: Reload Window`) to pick up the new agents and instructions.

---

## How to Use

### Using Custom Agents

1. Open the **Chat panel** (`Cmd+Shift+I` or click the Chat icon in the sidebar)
2. At the top of the chat input, click the **agent dropdown** (shows "Copilot" by default)
3. Select one of the custom agents from the list:
   - **Orchestrator** — Start here for complex or multi-step requests
   - **Planner** — Architecture design and implementation planning
   - **Implementer** — Writing production code
   - **Reviewer** — Code review (read-only)
   - **Tester** — Test generation
   - **Documenter** — Documentation writing
   - **Security Auditor** — Security vulnerability analysis (read-only)
4. Type your message and press Enter
5. After the agent responds, use the **handoff buttons** at the bottom of the response to route work to the next specialist

### Using Prompt Files (Slash Commands)

Type `/` in the chat input to see available prompts:

| Command | What It Does | Routes To |
|---------|-------------|-----------|
| `/new-feature` | Plan a new feature end-to-end | Orchestrator → specialists |
| `/new-endpoint` | Scaffold a FastAPI endpoint (schema → service → route → tests) | Implementer |
| `/new-component` | Scaffold a Vue/React component with types and tests | Implementer |
| `/security-audit` | Run OWASP Top 10 security analysis | Security Auditor |
| `/add-tests` | Generate comprehensive tests for existing code | Tester |

Prompts will ask for input variables (feature name, file path, etc.) before running.

### Auto-Applied Instructions

These files are automatically included in context when you work with matching files — no action needed:

| Instructions File | Applied When |
|------------------|-------------|
| `copilot-instructions.md` | Every chat request (global) |
| `security.instructions.md` | Every chat request (global security checklist) |
| `python.instructions.md` | Editing `*.py` files |
| `vue.instructions.md` | Editing `*.vue` or `*.ts` files |
| `react.instructions.md` | Editing `*.tsx` or `*.jsx` files |
| `testing.instructions.md` | Editing `*.test.*` or `*.spec.*` files |

---

## Recommended Workflows

### 🚀 New Feature (Full Lifecycle)

```
1. /new-feature → Orchestrator analyzes scope
2. → 📐 Plan Architecture (handoff to Planner)
3. → 🔨 Implement Code (handoff to Implementer)
4. → 🧪 Generate Tests (handoff to Tester)
5. → 🔍 Review Code (handoff to Reviewer)
6. → 📝 Write Documentation (handoff to Documenter)
7. → 🛡️ Security Audit (handoff to Security Auditor)
```

### ⚡ Quick Endpoint

```
1. /new-endpoint → Implementer creates schema + service + route + tests
2. → 🔍 Request Review (handoff to Reviewer)
```

### 🛡️ Security Check

```
1. /security-audit → Security Auditor scans codebase
2. → 🔨 Fix Security Issues (handoff to Implementer)
3. → 🧪 Add Security Tests (handoff to Tester)
```

### 🧪 Improve Coverage

```
1. /add-tests → Tester generates tests for target file
2. → 🔍 Review Tests (handoff to Reviewer)
```

---

## Agent Reference

### Model Assignments & Token Optimization

Each agent is pinned to a model optimized for its task — expensive models are reserved for complex reasoning, cheap models handle routine work:

| Agent | Model | Input / Output | Why This Model |
|-------|-------|---------------|----------------|
| **Orchestrator** | Claude Sonnet 4.5 | 128K / 32K | Strong reasoning for triage at moderate cost |
| **Planner** | Claude Sonnet 4.5 | 128K / 32K | Architectural planning needs good reasoning, not code gen |
| **Implementer** | GPT-5.1-Codex | 128K / 128K | Purpose-built for agentic code generation; massive output window |
| **Reviewer** | Claude Opus 4.6 | 128K / 64K | Deepest reasoning catches subtle bugs (read-only keeps cost bounded) |
| **Tester** | GPT-5.1-Codex | 128K / 128K | Efficient at formulaic test generation at scale |
| **Documenter** | Claude Haiku 4.5 | 128K / 32K | Cheapest model — more than sufficient for prose and docstrings |
| **Security Auditor** | Claude Opus 4.6 | 128K / 64K | Security analysis demands the deepest reasoning available |

### Token-Saving Design Decisions

1. **Scoped instructions** — Language-specific rules only attach when matching files are edited, not on every request
2. **Read-only agents** — Reviewer and Security Auditor have no edit tools, preventing expensive iterative edits
3. **Cheap delegation** — Orchestrator uses Sonnet (not Opus) because it only analyzes and routes, never generates code
4. **Haiku for docs** — Documentation writing doesn't need frontier reasoning
5. **Codex for code** — Codex models are optimized for code generation with lower per-token costs than chat models

---

## MCP Servers

The `.vscode/mcp.json` file configures external tool servers that agents can use:

| Server | What It Does | Used By |
|--------|-------------|---------|
| **postgres** | Query PostgreSQL databases (schema inspection, data queries) | Implementer, Tester |
| **docker** | Manage Docker containers (build, run, logs, inspect) | Implementer |
| **pacman** | Query PyPI and npm registries for package info and versions | Planner, Implementer |
| **git** | Extended git operations (log, diff, blame beyond VS Code built-ins) | All agents |
| **sequential-thinking** | Dynamic problem-solving with reflective reasoning | Planner, Orchestrator |

MCP servers start on-demand when an agent first needs them. VS Code will prompt for any required credentials (like the PostgreSQL connection string).

---

## Customization

### Adding a New Agent

Create a new file in `.github/agents/` with the `.agent.md` extension:

```markdown
---
name: My Agent
description: What this agent does
tools:
  - codebase
  - search
model: Claude Sonnet 4.5
---

# My Agent

System prompt and instructions here...
```

### Adding a New Prompt

Create a new file in `.github/prompts/` with the `.prompt.md` extension:

```markdown
---
name: my-prompt
description: What this prompt does
agent: implementer
model: GPT-5.1-Codex
tools:
  - editFiles
  - codebase
---

# My Prompt

Instructions with ${input:variableName:placeholder} variables...
```

### Modifying Instructions

Edit any `.instructions.md` file to change coding standards. Changes take effect immediately — no reload needed.

### Adding MCP Servers

Edit `.vscode/mcp.json` to add new servers. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for configuration format.

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Agents don't appear in dropdown | Ensure `chat.agents.enabled` is `true` in settings; reload window |
| Prompts don't appear with `/` | Ensure `chat.promptFiles` is `true` in settings; reload window |
| MCP server fails to start | Run the `npx` command manually in terminal to see error; ensure Node.js 18+ |
| Agent uses wrong model | Check model name matches exactly (e.g., `Claude Sonnet 4.5` not `claude-sonnet-4.5`) |
| Instructions not applied | Check `applyTo` glob pattern matches your file path; reload window |
| Agent can't find tools | Verify tool names in the `tools` array match VS Code built-in tool IDs |
