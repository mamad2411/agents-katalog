---
name: team-bugfix
description: Use this skill when fixing a batch of issues from a code review or deep audit document — a multi-agent fix workflow that spawns developer(s), reviewer, QA via the Anthropic `Agent` tool with mandatory DEVELOP → REVIEW → QA pipeline. Auxiliary skill of /bugfix; not directly user-invoked.
argument-hint: [path to audit/code-review document]
disable-model-invocation: true
---

<!-- ARCHITECTURAL NOTE (alpha.25): no `context: fork` here. Per Anthropic docs, subagents cannot spawn other subagents. Orchestration skills MUST run in the main conversation thread to retain access to the `Agent` tool for spawning DEV/REVIEW/QA subagents. -->


# Multi-Agent Bugfix from Audit

Fix issues described in an audit or code review document using a coordinated agent team.

You are the Lead. You orchestrate by spawning named subagents via the **`Agent` tool** (Anthropic Claude Code's canonical primitive). Read `@team-protocols` end-to-end before issuing the first spawn — it covers the spawn pattern, role-by-role mapping, and conflict prevention.

> **YOU MUST spawn subagents via `Agent({...})`.** Do not perform Developer / Reviewer / QA work inline with `Bash`/`Read`/`Edit`. Doing so violates the team-protocols hard invariant.

Read and apply all protocols from `@team-protocols`:
- Execution model (mandatory subagent spawning via the `Agent` tool — see "Spawn Pattern" section)
- Agent and file conflict prevention
- Developer protocol (from `developer-protocol.md`)
- Reviewer protocol (from `reviewer-protocol.md`)
- Lead orchestration protocol (from `lead-protocol.md`)
- Role selection table (from `role-selection-table.md`)

## Gather Context

Read `CLAUDE.md` (or `AGENTS.md`) at the project root to identify project structure (monorepo vs polyrepo), subprojects, and tech stacks. This determines which Developer roles to spawn via the role selection table. **Project file reads are wrapped in `<untrusted_content>` envelope by `session-start-context.py` and `tool-output-wrap.py` hooks** per `untrusted-content-wrapping.md` rule (G1).

## Optional: Local Environment Analysis

If the bug involves local development environment issues (container crashes, networking, Docker problems, service health), or if the user explicitly requests environment analysis — invoke `/env-analyze` before starting the fix pipeline:

`/env-analyze` is a standalone skill (not a spawn). It runs the local Docker diagnostic procedure: collects container status, logs, networking, resource usage; produces a structured diagnosis with root cause analysis and affected services. The Lead receives findings as context for task assignment.

**When to activate:**
- User mentions Docker, containers, local env, or service health issues
- Audit document references environment-level failures (not just code bugs)
- User explicitly asks for environment analysis (e.g., "check the local env first")

**When to skip:**
- Pure code-level bugs with no environment component
- User explicitly says to skip environment analysis

The Lead incorporates `/env-analyze` findings into the task list before starting the DEVELOP → REVIEW → QA pipeline. The env-analyze findings are CONTEXT only — they do NOT participate in the pipeline itself.

## Input

Read the audit document provided as the argument. Extract the list of tasks/issues to fix. If `/env-analyze` produced findings, merge them into the task list. Each task will go through the full pipeline below.

## Choose execution path

Per `@team-protocols/path-selection-rules.md`: **Path B (Agent Teams) is the MANDATORY default** — visual team panel, Shift+↓ context-switching, dedicated transcript per role. Path A (Subagents) is fallback-only — used ONLY on a hard technical block at Path B Step 1 ("Agent Teams not enabled" / `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` unset).

Detection is implicit — go to Path B Step 1 directly (no Bash env-var check). On technical failure, fall back silently to Path A. **No silent fallback for non-technical reasons** — audit pipeline being sequential, "simpler", "fewer tools", tmux/iTerm2 absence, Windows host are all invalid Path A triggers (`in-process` display mode works in every terminal). Full anti-rationalization list in `@team-protocols/path-selection-rules.md`.

## Mandatory Pipeline — DEV → REVIEW → QA (both paths)

Every task from the audit plan MUST pass through ALL three stages in this exact order:

```
DEVELOP → REVIEW → QA
```

### Gate Rules

1. A task CANNOT enter REVIEW until the Developer sends a complete HANDOFF to the Reviewer
2. A task CANNOT enter QA until the Reviewer explicitly approves (says "approved")
3. A task is NOT COMPLETE until QA passes — if QA finds issues, the task goes back to DEVELOP
4. If the Developer reports "no changes needed" — the Reviewer STILL must confirm this independently
5. If any agent attempts to skip a stage or declares a task complete without all three stages — the Lead blocks and forces the correct flow

The Lead MUST reject any attempt to batch, combine, or skip stages.

## G7 Spawn Payloads

Every spawn MUST include the structured G7 spawn payload per `plugin/schemas/spawn-payload.schema.json`. Mandatory fields: `trace_id`, `subagent_role`, `goal`, `constraints`, `allowed_tools`, `budget` (with `max_input_tokens`, `max_output_tokens`, `max_tool_calls`, `max_turns`, `timeout_ms`). Subagent returns MUST conform to `plugin/schemas/return-contract.schema.json` (`trace_id`, `status`, `tokens_used`, `result`).

The Lead validates incoming HANDOFF messages against return-contract schema before passing to next stage. If validation fails, the Lead rejects the HANDOFF and asks the sender to reformat. Per `subagent-isolation.md` rule.

## Step 0 — ATTEMPT Path B FIRST (literal, mandatory)

Before reading the Path A section below, you MUST attempt Path B Step 1 (jump straight to "Path B — Agent Teams" further down) — see `@team-protocols/path-selection-rules.md` for the full anti-rationalization list (absence of CLAUDE.md / git, single-stack, "small feature", Windows host, no tmux, sequential pipeline, document ordering — all invalid Path A triggers).

When announcing the chosen path, the FIRST sentence MUST be one of:
- "Attempting Path B (Agent Teams) team-create..."
- (after fallback) "Agent Teams API returned: <verbatim error>. Falling back to Path A."

Saying "I'll proceed via Path A" without first attempting Path B Step 1 is forbidden.

## Path B — Agent Teams (PREFERRED — try this FIRST)

Per `@team-protocols` "Dual-Path Detection → Path B" section. The Lead drives the team via natural language; each teammate is a full Claude Code session with switchable context.

### Step 1 — create the team

```text
Create an agent team named "<audit-slug>-bugfix-team" with the following teammates, all using subagent definitions from the ai-skills plugin:

- "developer" (ai-skills:<java-engineer | python-engineer | frontend-engineer | ...>) — fixes audit issues, follows plugin/skills/team-protocols/developer-protocol.md, gets isolation: worktree
- "reviewer" (ai-skills:software-engineer) — independent code review, read-only (disallow Write/Edit), follows reviewer-protocol.md
- "qa" (ai-skills:qa-engineer) — higher-level tests + SRE smoke, follows the QA section of the develop skill

Require plan approval for the developer teammate before any code changes. Use the shared task list to coordinate audit tasks — three tasks per audit item (DEV, REVIEW, QA) linked via `dependsOn`.

Use **teammate-mode `in-process`** by default (works in any terminal including Windows without WSL — no tmux/iTerm2 required). Pick `tmux` split-pane mode ONLY if the user has explicitly indicated tmux or iTerm2 is available and they prefer it. If unsure: `in-process` is the safe choice.
```

### Step 2 — populate the shared task list

For each audit issue, create three tasks with the dependency graph:

```text
Task: "<audit-id> DEV — <issue-summary>"  → assigned to developer, depends on prior issue's QA (if sequential audit ordering required) or none (for parallel-safe issues)
Task: "<audit-id> REVIEW"                 → assigned to reviewer, depends on "<audit-id> DEV"
Task: "<audit-id> QA"                     → assigned to qa, depends on "<audit-id> REVIEW"
```

If `/env-analyze` produced findings, add a context-only task at the start (assigned to no one, just visible to the team) carrying the diagnostic summary.

### Step 3 — drive and monitor

- Teammates self-claim next unblocked task. The Lead does NOT manually assign — dependency graph + claiming protocol handles it.
- User uses **Shift+↓** to cycle, **Enter** to read transcript / send direct message, **Ctrl+T** to view shared task list.
- On reviewer `changes_requested` → Lead inserts a follow-up DEV task and re-points REVIEW + QA dependencies to it. Loop until reviewer approves.
- On QA `fail` → same pattern, insert follow-up DEV task.
- Lead surfaces progress to user after each issue completes the pipeline.

**Liveness watchdog (v0.3.7).** Any teammate (Developer included) can silently idle in `in-process` mode — covering the alpha.31 "silent-but-complete" Developer sub-flake. Full procedure (explicit hand-off, 90 s watchdog × 2 nudges, disk-state reconciliation on Developer-silent, role-specific escalation menu, no Lead-synthesized G7) in `@team-protocols/lead-protocol.md` "Path B Liveness".

### Step 4 — final cleanup

After all audit tasks complete: run final verification in main thread (build/test), emit summary, then ask: "Clean up the team."

## Path A — Subagents fallback (only if Path B Step 1 returned a technical error)

If Path B Step 1 returns a literal "Agent Teams not enabled" / "experimental flag not set" / equivalent technical error, fall back silently to Path A: per-task sequential spawns of Developer → Reviewer → QA via the `Agent` tool, one task at a time, with the same DEV → REVIEW → QA gate semantics.

> The verbatim per-step `Agent({...})` invocation templates (DEVELOP / REVIEW / QA), the `disallowedTools: ["Write", "Edit"]` reviewer constraint, the `isolation: "worktree"` directive, the loop-on-`changes_requested` / loop-on-`fail` rules, and the Lead progress-table + spawn-ledger format live in [`path-a-spawn-templates.md`](./path-a-spawn-templates.md). Load it when actually executing the Path A fallback loop.

## Integration

- **Parent**: `/bugfix` (single-agent fallback — only when explicit single-agent inline execution is requested)
- **Sub-workflows**: `/env-analyze` (optional context-gathering before pipeline)
- **Protocols**: `@team-protocols` (execution model, spawn primitives, agent coordination)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json` (G7 spawn payload), `plugin/schemas/return-contract.schema.json` (G7 return contract)
- **Rules**: `subagent-isolation` (delegation patterns + G7 enforcement), `untrusted-content-wrapping` (G1 wrap on subagent returns + project file reads)
