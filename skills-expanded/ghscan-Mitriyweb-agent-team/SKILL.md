---
name: agent-team
description: Use this skill when working on the agent-team repository — adding agents,
  modifying orchestration logic, updating CLAUDE.md configs, extending memory patterns,
  or debugging multi-agent flows. Covers: Claude SDK query() loop, YAML frontmatter
  agent configs, memory.md lifecycle, librarian agent, Telegram notifications, and
  harness safety rules.
---

# agent-team Skill

## When to activate

- Adding or modifying agent roles and their instructions (`CLAUDE.md` files).
- Modifying the core orchestration logic in `lib/run.ts` or `lib/sdk/`.
- Extending the memory curation patterns in `lib/memory.ts` or `lib/templates/librarian.md`.
- Debugging multi-agent communication flows or the delegation protocol.
- Adding new tools or modifying safety hooks in `lib/sdk/hooks.ts`.
- Updating the CLI interface in `bin/init.ts` or common utilities in `lib/common.ts`.

## Repository map

- `bin/init.ts` — CLI entry point (init, run, plan, update, reconfigure).
- `lib/run.ts` — Core `TaskRunner` orchestrating the task lifecycle.
- `lib/sdk/agent-runner.ts` — Wrapper for the Anthropic Claude Agent SDK `query()` API.
- `lib/sdk/hooks.ts` — Pre/Post tool use hooks and safety sanitization.
- `lib/memory.ts` — Logic for memory curation, capping, and rotation.
- `lib/notify.ts` — Telegram notification module.
- `agents/` — Source of truth for team definitions and protocols.
- `.claude/agents/` — Deployed agent definitions (Markdown + YAML frontmatter).
- `.claude-loop/` — Runtime artifacts: `memory.md`, logs, and reports.

## Core patterns

### query() API usage pattern

The system uses the programmatic SDK to stream agent interactions:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({ prompt, options })) {
  if (message.type === "result" && message.subtype === "success") {
    const output = message.result; // Final agent response
  }
}
```

### CLAUDE.md YAML frontmatter schema

Agent definitions use YAML frontmatter to configure the SDK session:

```yaml
---
name: sw-developer
role: developer
model: claude-3-5-sonnet-latest
tools: Read, Edit, Bash, Glob, Grep
permission_mode: acceptEdits
allow_sub_agents: false
---
```

### memory.md write contract

- **Librarian-only**: Agents should generally not write to `.claude-loop/memory.md` directly.
- **Append-only**: The `librarian` agent appends concise bullets extracted from task reports.
- **Capping**: `memory.md` is capped to the last 30 tasks in prompts to maintain context efficiency.

## How to add a new agent

1. **Create Source**: Add a Markdown file in `agents/{team}/{role}.md` (or `agents/{team}/{role}/CLAUDE.md`).
2. **Define Frontmatter**: Set `role`, `model`, and `tools`.
3. **Protocol**: Reference the new agent in `agents/{team}/PROTOCOL.md` communication graph.
4. **Deploy**: Run `agent-team reconfigure` or `agent-team init` to deploy it to `.claude/agents/`.

## Non-negotiable rules

See [docs/ARCHITECTURE.md#non-negotiable-rules](docs/ARCHITECTURE.md#non-negotiable-rules) for the full list of invariants.

## Gotchas

- **Never write to memory directly**: Always let the `librarian` curate it to avoid fragmentation.
- **Tool Names**: Use exact SDK tool names (e.g., `Bash`, not `shell`).
- **Pathing**: Always use relative paths from the project root when defining agent file locations.
- **Login Shells**: Setup commands in `run.ts` are executed in a login/interactive shell to ensure tools like `nvm` are available.
