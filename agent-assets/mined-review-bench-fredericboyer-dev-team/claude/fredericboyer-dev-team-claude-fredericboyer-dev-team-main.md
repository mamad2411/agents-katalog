# dev-team

Adversarial AI agent team for any project. Installs Claude Code agents, hooks, and skills that enforce quality through productive friction.

## Project structure

- `bin/` — CLI entry point shim (`npx dev-team init`)
- `src/` — TypeScript source (compiled to `dist/` via `tsc`)
- `templates/` — Agent definitions, hook scripts, skills, and CLAUDE.md template that get copied into target projects
- `docs/adr/` — Architecture Decision Records. Every non-trivial decision gets an ADR.
- `tests/` — Unit, integration, and scenario tests
- `.claude/agents/` — Our own agent definitions (`.agent.md` files, not shipped to users)
- `.claude/agent-memory/` — Agent calibration memory (not shipped to users)
- `.dev-team/` — Hooks, config, metrics, and research (not shipped to users)

## Workflow

- **Every piece of work starts with a GitHub Issue.** No exceptions.
- Branch naming: `feat/123-description` or `fix/456-description`
- Commits reference issues: `fixes #123` or `refs #123`
- All merges via PR. No direct pushes to main.
- **Aggressively parallelize independent work.** When multiple issues touch independent files, work them simultaneously — do NOT work sequentially on issues that can be parallelized. Only sequence issues that have file conflicts.
  - **Agent teams** (preferred for multi-issue batches): The main conversation loop acts as Drucker (team lead). Spawn implementation teammates via agent teams, each on its own branch. Never delegate to a Drucker subagent — the main loop IS Drucker. *(This is specific to the dev-team repo itself. The template section below has different guidance for user projects, where `@dev-team-drucker` can be used as a subagent.)*
  - **Worktree subagents** (fallback when agent teams are unavailable): Use the Agent tool with `isolation: "worktree"` to spawn parallel workstreams in separate worktrees.
  - The main loop must stay interactive at all times. All implementation happens via background teammates or subagents.

## Development

- `npm test` — run all tests
- `node bin/dev-team.js init --all` — test the installer locally
- TypeScript source, compiled to CommonJS. Node.js 22+, zero runtime dependencies.
- Use oxlint for linting, oxfmt for formatting (not ESLint/Prettier). See ADR-007.
- Version bumps: use `npm version <version> --no-git-tag-version` to update both `package.json` and `package-lock.json` atomically. Do not edit `package-lock.json` manually.

## Template design principles

Templates, agent definitions, skills, and hooks ship to all projects. They must remain:
- **Workflow-agnostic** — don't assume PRs, specific branch naming, or any particular development workflow
- **GitHub-first** — `gh` CLI, GitHub Actions, and GitHub GraphQL API are first-class (ADR-040). Review handling is reviewer-agnostic (works for Copilot, human reviewers, bots) via GraphQL `reviewThreads`
- **Language-neutral** — don't encode language conventions (test patterns, linter commands, file extensions) that the agent already knows. Hooks detect the ecosystem; agents apply their built-in knowledge
- **Discoverable-only** — if the agent can learn it by reading the codebase, don't put it in a template. Include only what agents can't discover: tool preferences, legacy traps, process decisions
- **Process-driven** — agent definitions describe *capabilities* (what the agent can do), not *steps* (how a specific project uses them). Workflow steps (release process, review requirements, integration rules) belong in `.claude/rules/dev-team-process.md`, which each project customizes. Agents receive it automatically via rules — no explicit "read this file" needed.
- **Rules for shared context** — `.claude/rules/` files are loaded automatically by all agents including subagents (ADR-033). Use rules for shared behavioral context (process, learnings). Use `.dev-team/` for non-context files (agent memory, metrics, config).
- **Skill invocation control** — orchestration skills (task, review, audit, retro) must have `disable-model-invocation: true` to prevent accidental autonomous firing. Advisory/read-only skills (scorecard, challenge) can be autonomous.

Project-specific conventions belong in `.claude/rules/dev-team-process.md` (workflow) or `.claude/rules/dev-team-learnings.md` (organic findings) — not in templates.

## Architecture decisions

Stored in `docs/adr/`. Read before making changes to foundational patterns. ADRs are immutable records — if a decision changes, write a new ADR that supersedes the original. Do not edit existing ADRs.

<!-- dev-team:begin -->

## Dev Team

This project uses [dev-team](https://github.com/dev-team) — adversarial AI agents that enforce quality through productive friction.

### Agents

Available agents: `@dev-team-voss`, `@dev-team-hamilton`, `@dev-team-mori`, `@dev-team-szabo`, `@dev-team-knuth`, `@dev-team-deming`, `@dev-team-tufte`, `@dev-team-brooks`, `@dev-team-conway`, `@dev-team-drucker`, `@dev-team-turing`, `@dev-team-rams`, `@dev-team-borges`. See `.claude/agents/` for full definitions, roles, and when to use each agent.

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

> **Non-JS/TS projects:** Hooks detect the ecosystem and delegate language-specific reasoning to agents. The review skill selects the appropriate specialist agents based on changed file domains. Agents apply their built-in knowledge for language-specific test naming, build tools, and framework structures (see ADR-034).

> **Multi-runtime support:** Use `--runtime` flag during `dev-team init` to target additional runtimes (e.g., `--runtime claude,copilot` or `--runtime codex`). Each runtime adapter generates native configuration files. Run `dev-team update` after changing runtimes to regenerate all adapter output.

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



