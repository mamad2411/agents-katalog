---
name: team-protocols
description: Use this skill when authoring or auditing a multi-agent skill that spawns named subagents — shared protocols for multi-agent team coordination covering the execution model, named subagent spawning via the Agent tool, file conflict prevention, developer/reviewer/lead protocols, role selection table, and G7 spawn payload + return contract schemas. Referenced by multi-agent workflow skills (`/develop`, `/team-bugfix`, `/feature-design`). Not directly user-invoked.
disable-model-invocation: true
---

# Multi-Agent Orchestration

Base protocols for coordinating a team of named subagents in Claude Code. This skill is not invoked directly — it is referenced by workflow skills via `@team-protocols`.

## CRITICAL — orchestration skills MUST NOT use `context: fork`

Per Anthropic Claude Code docs, "subagents cannot spawn other subagents." Any skill that spawns Developer / Reviewer / QA via the `Agent` tool MUST NOT declare `context: fork` — forking pushes the skill body into a subagent that has no `Agent` tool, and the pipeline collapses (alpha.25). Only single-agent fallbacks like `feature-dev` can keep `context: fork`.

## Execution Model

You are the Lead. You run in the main conversation thread and coordinate the team by spawning named subagents via the **`Agent` tool** (Claude Code's canonical primitive for delegating work to an isolated context).

**Hard invariant**: every agent role MUST run as a NAMED subagent spawned via `Agent`, with its own isolated context. The Lead (main thread) NEVER executes Developer / Reviewer / QA work inline with `Bash`/`Read`/`Edit`. If you skip the spawn and do the work directly in the main thread, you have violated this protocol — the user loses the ability to inspect each role independently and the pipeline gates collapse to procedural-only enforcement.

> Observed alpha.23 failure mode: the skill describes roles in prose but never issues a literal `Agent(...)` call and proceeds inline. Every role-spawn step MUST execute an explicit `Agent({...})` call, not paraphrase it. Literal templates + G7 payload + role-by-role spawn map live in [`spawn-pattern.md`](./spawn-pattern.md) — load it before the first spawn.

## Pre-flight (Path B) — tool load · wave sizing · brief-from-source · file-channel

Before issuing the Path B team-create prompt the Lead runs four pre-flight checks. **Read `lead-protocol.md` "Pre-flight — wave sizing and brief-from-source" and "File-channel transport — first-class, not fallback" and apply them verbatim** — the summary below is the trigger, not the full procedure:

1. **Tool load (v0.3.9)**: if `TeamCreate`/`TaskCreate`/`TaskUpdate`/`SendMessage`/`TeamDelete`/`TaskStop`/`Monitor` are not in the active toolset, batch-load them once via `ToolSearch(query: "select:TeamCreate,TaskCreate,TaskUpdate,SendMessage,TeamDelete,TaskStop,Monitor")` (harness defers tool schemas — an unloaded tool raises `InputValidationError`). Skip if already loaded.
2. **Wave sizing (F8)**: plans with >6 WPs split into 3-6 WP waves with a checkpoint between waves (one team-create reliably converges on 3-6 WPs, not 38).
3. **Brief-from-source (F4)**: every spawn payload's `goal` + `constraints` are assembled by `Read` of the source design/PRD VERBATIM, never paraphrased from Lead context.
4. **File-channel transport (v0.3.11)**: wire `.ai-skills-memory/sessions/<sid>/team-envelopes/` as the canonical liveness signal at team-create. `team-gate-reconciliation.py` writes a snapshot envelope on every `TaskCompleted`/`TeammateIdle`; teammates write G7 envelopes there too (per `developer-protocol.md` / `reviewer-protocol.md` "File-channel envelopes"); the Lead `Monitor`s the directory so silent-bus failures (alpha.36) do not stall the pipeline.

## Two Paths — Subagents OR Agent Teams

Two execution paths are supported. Both preserve the DEV → REVIEW → QA gate semantics — only the execution mechanism differs.

**MANDATORY default: Path B (Agent Teams).** Path B MUST be selected for every multi-agent workflow. It gives the user a visual team panel, Shift+↓ to switch context into any teammate, dedicated transcript per role, and a shared task list with `dependsOn`. Path A is **fallback-only** and may be selected ONLY when Path B Step 1 returns a hard technical block (defined below). Any other downgrade is a protocol violation — there is **no silent fallback** for non-technical reasons.

**Hard technical block** = a documented Path A trigger in `path-selection-rules.md`: (1) team-create returns "Agent Teams not enabled" / equivalent (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` unset or Lead inside a subagent); (2) Pre-spawn tool-capability check (alpha.32) shows every writing role lacks `Write`/`Edit` AND Lead-writes-file restructure is unsafe. Partial mismatches are handled per role per alpha.32. In these cases only, fall back silently to Path A.

**Invalid reasons to downgrade Path B → Path A are protocol violations** — "sequential pipeline / parallelism doesn't help", "Path A is simpler/fewer tools", "no tmux/iTerm2", "Windows / no WSL / no Unix tools", "small or simple feature", and "single-stack project" are ALL invalid (Path B's value is UX visibility, not parallelism; `in-process` display mode is platform-independent; size and stack count are irrelevant to path selection). The full anti-rationalization checklist with each invalid trigger and the observed failure modes (alpha.26 / alpha.27 / alpha.30) lives in [`path-selection-rules.md`](./path-selection-rules.md) — **read it and apply every invalid-trigger rule verbatim** before any path downgrade.

**Detection is implicit, not explicit.** Do NOT run an explicit env-var check (no `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` Bash call) — that triggers a tool-permission prompt for the user without adding value. Just attempt Path B Step 1 directly. If it succeeds you're in Teams mode. If it returns "Agent Teams not enabled" or similar, fall back to Path A immediately and proceed.

### Path B — Agent Teams (MANDATORY default — try this FIRST)

Lead drives via natural language. Each teammate is a full Claude Code session with switchable context. User can Shift+↓ to switch teammates, Enter for transcripts, and Ctrl+T for the shared task list. This is the path the workflow MUST use unless a hard technical block at Step 1 forces Path A.

**Path B Liveness — Explicit Hand-off + Watchdog (v0.3.7).** Any teammate (Developer, Reviewer, QA) can silently idle in alpha `in-process` mode — including the Developer's "silent-but-complete" sub-flake where edits land on disk and acceptance criteria appear met but the G7 envelope never arrives. The Lead MUST push an explicit hand-off message at every stage transition (Developer included), run a ~90 s watchdog with up to 2 retry nudges, perform a read-only disk-state reconciliation when the silent role is the Developer, and escalate to the user after 3 nudges with a role-specific menu (per `lead-protocol.md` "Path B Liveness — Explicit Hand-off + Watchdog"). Per-task `Agent` fallback is permitted **only** on user-approved escalation, never as silent session-wide downgrade. The Lead MUST NEVER synthesize a G7 envelope on a teammate's behalf, even when disk state proves the work is done.

**Pre-spawn tool-capability check (v0.3.8, alpha.32).** Before team-create, the Lead verifies each teammate's `subagent_type` has tools sufficient for its workflow output. As of v0.3.8 ten producer roles ship with `Write` / `Edit` so the check almost always passes — it remains mandatory to catch the two intentional read-only patterns: `eval-judge` (verdict-in-response) and `software-engineer` spawned as Reviewer with `disallowedTools: ["Write","Edit"]` at spawn time. Full procedure + role-capability cache: `path-selection-rules.md` "Pre-spawn tool-capability check".

### Path A — Subagents (technical-block fallback only, sequential)

Fallback path used ONLY when Path B Step 1 returns a hard technical block. Per role, the Lead invokes `Agent({...})` and waits for return. Sequential by default; lower token cost; works in every Claude Code environment. Never selected as a primary choice — only on documented technical failure of Path B.

> The full Path A / Path B body (team-create natural-language template, task-list dependency graph, gate enforcement, the `in-process` vs `tmux` display-mode rules, and the comprehensive "no silent fallback" anti-rationalization checklist with all invalid Path A triggers) lives in [`path-selection-rules.md`](./path-selection-rules.md). Load it when authoring a workflow skill that supports both paths or auditing one for compliance with the dual-path rules.

### Hard rule for both paths

Whichever path is active, the Lead NEVER does Developer/Reviewer/QA work inline with `Bash`/`Read`/`Edit`. The role-isolation invariant applies in both modes — only the spawn mechanism differs.

## Communication Rules

- Every agent reply is the literal return value of an `Agent` tool call. **Never paraphrase or simulate an agent's response.**
- The Lead orchestrates, tracks progress, prints status tables, enforces gates. The Lead does NOT do Developer / Reviewer / QA work itself.
- If a return contract is missing fields required by the next role's protocol — reject it and re-spawn the originating role with a corrected prompt before the next role starts.
- All HANDOFF data flows through the return contract's `result` field as structured JSON, not as free-form prose.

## G7 Contracts and File Conflict Prevention

Every spawn embeds a JSON payload conforming to `plugin/schemas/spawn-payload.schema.json`. Every return embeds a JSON contract conforming to `plugin/schemas/return-contract.schema.json`. The `subagent-start-budget.py` hook validates the spawn payload + enforces budget; the `subagent-stop-learnings.py` hook validates the return.

**Single instance per role** — except Developers, where one instance per affected subproject stack is allowed. Do NOT spawn multiple Reviewers or multiple QA agents.

**Only ONE agent may edit files at any time.** Multiple Developers get `isolation: "worktree"`. Reviewer is always read-only (`disallowedTools: ["Write", "Edit"]`).

> The full G7 spawn-payload + return-contract JSON examples, the `needs_clarification` halting protocol, and the file-conflict prevention rules (writing-agent queueing, Lead enforcement, multi-Developer worktree merge order) live in [`g7-contracts.md`](./g7-contracts.md). Load it when authoring a workflow that needs the literal contract shapes or the conflict-prevention sequencing rules.

## Protocols

Apply these protocols to all agents in the team:

- **Developer protocol**: [`developer-protocol.md`](./developer-protocol.md) — task implementation, self-verification, handoff format, review iterations
- **Reviewer protocol**: [`reviewer-protocol.md`](./reviewer-protocol.md) — independent verification, ghost change detection, issue reporting
- **Lead protocol**: [`lead-protocol.md`](./lead-protocol.md) — orchestration, progress tracking, escalation, final summary
- **Role selection**: [`role-selection-table.md`](./role-selection-table.md) — subproject-to-developer mapping and spawning rules

## Integration

- **Used by**: `/develop`, `/team-bugfix`, `/feature-design` (multi-agent workflows)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json` (G7 contracts)
- **Hooks**: `subagent-start-budget.py` (validates spawn payload + enforces budget), `subagent-stop-learnings.py` (validates return contract + opt-in learnings capture)
- **Rules**: `subagent-isolation` (delegation patterns + bounded recursion), `untrusted-content-wrapping` (G1 wrap on subagent returns)
- **Reference**: [Anthropic Claude Code subagents documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)
