# Project Name

## Development
<!-- Build, test, and run commands. Tool preferences agents can't discover from code. -->
<!-- Example: "Use pnpm, not npm. Use oxlint for linting, not ESLint." -->

## Test quirks
<!-- Non-obvious testing behavior that causes false passes or confusing failures. -->
<!-- Example: "Run integration tests with --no-cache or flaky tests pass incorrectly." -->

## Legacy traps
<!-- Code that looks correct but isn't. Patterns to avoid. -->
<!-- Example: "Don't use the v1 auth middleware — it stores tokens non-compliantly." -->

<!-- dev-team:begin -->

## Dev Team

This project uses [dev-team](https://github.com/dev-team) — adversarial AI agents that enforce quality through productive friction.

### Agents

Available agents: `@dev-team-hopper`, `@dev-team-szabo`, `@dev-team-knuth`, `@dev-team-deming`, `@dev-team-tufte`, `@dev-team-brooks`, `@dev-team-conway`, `@dev-team-drucker`, `@dev-team-turing`, `@dev-team-rams`, `@dev-team-borges`. See `.claude/agents/` for full definitions, roles, and when to use each agent.

### Capabilities

For automatic delegation, use `@dev-team-drucker` — it analyzes the task and routes to the right specialist.

For non-trivial work: explore the area first, then implement, then review.

**Automatic invocation (hooks):** Agents are auto-spawned based on changed file patterns. See `.dev-team/hooks/` for the watch-list patterns that determine which agents are triggered. Turing is on-demand only (spawned by Drucker for research tasks).

**End-of-workflow agents:** Borges is mandatory at end of every `dev-team-task`, `dev-team-review`, `dev-team-audit`, and `dev-team-retro` (invoked via `dev-team-extract`).

**Orchestration:** Drucker delegates tasks to the right implementing agent and spawns reviewers. Szabo, Knuth, and Brooks review all code changes.

**CRITICAL: Always run agents in the background.** When spawning Drucker or any agent for tasks that take more than a few seconds, use `run_in_background: true`. The main conversation loop must remain interactive.

Agents challenge each other using classified findings:
- `[DEFECT]` blocks progress. `[RISK]`, `[QUESTION]`, `[SUGGESTION]` are advisory.
- When agents disagree, they escalate to the human after one exchange each. Human decides.

See `.claude/rules/dev-team-process.md` for orchestration protocol, parallel execution, and agent naming conventions.

### Hook directives are MANDATORY

When a dev-team hook outputs `ACTION REQUIRED — spawn these agents`, you MUST:
1. Spawn each listed agent as a **background** subagent using the Agent tool with `subagent_type: "general-purpose"`
2. Include the agent's full definition by reading from `.claude/agents/<agent>.agent.md`
3. Include the changed file path and instruction to produce classified findings

Do NOT skip this. Do NOT treat hook output as optional. If you believe a review is unnecessary for trivial changes, explain why to the user.

### Skills

**Framework skills** (installed automatically, updated with `dev-team update`):
- `dev-team-challenge` — critically examine a proposal or implementation
- `dev-team-implement` — implement a task on a feature branch with pre-assessment and validation
- `dev-team-task` — start an iterative task loop with adversarial review gates
- `dev-team-review` — orchestrated multi-agent parallel review of changes
- `dev-team-audit` — full codebase security + quality + tooling audit
- `dev-team-retro` — audit knowledge base health (learnings, agent memory, CLAUDE.md)
- `dev-team-extract` — Borges memory extraction, metrics verification, and memory formation gates
- `dev-team-scorecard` — audit process conformance for a completed task
- `dev-team-pr` — create a well-formatted PR from the current branch using project config

> **Non-JS/TS projects:** Hooks detect the ecosystem and delegate language-specific reasoning to agents. The review skill selects the appropriate specialist agents based on changed file domains. Agents apply their built-in knowledge for language-specific test naming, build tools, and framework structures (see ADR-034).

> **Multi-runtime support:** Use `--runtime` flag during `dev-team init` to target additional runtimes (e.g., `--runtime claude,copilot` or `--runtime codex`). Each runtime adapter generates native configuration files. Run `dev-team update` after changing runtimes to regenerate all adapter output.

### Model configuration

Configure per-agent model tiers and alloy multi-model reviews in `.dev-team/config.json`:

```json
{
  "models": {
    "default": "opus",
    "agents": {
      "szabo": ["opus", "sonnet"],
      "knuth": ["opus", "sonnet"],
      "brooks": ["opus"],
      "hopper": "sonnet"
    }
  }
}
```

- `default` — model tier for agents not listed in the `agents` map
- String value (e.g., `"sonnet"`) — single model, no fallback
- Array value (e.g., `["opus", "sonnet"]`) — ordered: first is primary, rest are shadow models for alloy multi-model reviews
- Agent names are lowercase without the `dev-team-` prefix
- Available tiers: `opus`, `sonnet`, `haiku`

**Alloy tiers** (used by `dev-team-review`): LIGHT uses primary only. FULL uses primary + first shadow. DEEP uses all models. When alloy is active, the same agent runs on multiple models in parallel, and findings are deduplicated.

### Project-specific customization

`.dev-team/` is managed by dev-team and updated by `dev-team update`. Do not add project-specific files here.

Project-specific customization belongs in `.claude/`:

| What | Where |
|------|-------|
| Custom hooks (linting, workflow enforcement) | `.claude/hooks/` |
| Project-specific skills (merge, deploy, etc.) | `.claude/skills/` |
| Path-scoped instructions loaded automatically into agent context | `.claude/rules/` |
| Claude Code settings and hook wiring | `.claude/settings.json` |

Rules files (`.claude/rules/*.md`) are loaded automatically by all agents including subagents. Use them for project-specific behavioral context that should be shared across all agent sessions.

`.claude/hooks/` and `.claude/skills/` are not overwritten by `dev-team update` — your project-specific customizations are safe. Only `.claude/settings.json` is merged additively (new product hooks are added, but user-added entries are never removed).

### Memory architecture (two-tier)

All project and process learnings MUST go to in-repo files, NOT to machine-local memory (`~/.claude/projects/`). Machine-local memory is invisible to other developers, agents, and sessions.

**Tier 1 — Shared team memory** (`.claude/rules/dev-team-learnings.md`):
Project facts, overruled challenges, cross-agent decisions, process rules. Loaded automatically by all agents via rules.

**Tier 2 — Agent calibration memory** (`.claude/agent-memory/<agent>/MEMORY.md`):
Domain-specific findings, known patterns, active watch lists. Each agent owns its own file. Entries include `Last-verified` dates for temporal decay.

| What | Where |
|------|-------|
| Project patterns, process rules, tech debt, overruled challenges | `.claude/rules/dev-team-learnings.md` (Tier 1) |
| Agent-specific calibration | `.claude/agent-memory/<agent>/MEMORY.md` (Tier 2) |
| Formal architecture decisions | `docs/adr/` |
| User-specific preferences only | Machine-local memory |

**Memory evolution:** New entries trigger re-evaluation of related existing entries. Duplicates are merged, contradictions are superseded, and 3+ overrules on the same tag generate calibration rules.

**Temporal decay:** Entries have `Last-verified` dates. Borges flags entries not verified in 30+ days and archives entries over 90 days to the `## Archive` section.

When the human gives feedback about process, coding style, or tool behavior: write it to `.claude/rules/dev-team-learnings.md`. Only use machine-local memory for things that are truly personal and would not apply to another developer on the same project.

<!-- dev-team:end -->
