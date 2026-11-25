---
name: feature-design
description: Use this skill when starting a new feature from concept — to convert a 1–3 sentence feature idea into a complete design pack (PRD, ARCHITECTURE, UX-FLOW, DATA-MODEL, RISKS, IMPLEMENTATION-PLAN, REVIEW-LOG) via a multi-agent three-wave pipeline orchestrated by feature-design-lead. Not for refactors (use /refactor), bugfixes (use /bugfix), or refining existing PRDs (use /develop directly).
argument-hint: "<idea, 1-3 sentences>"
---

<!-- ARCHITECTURAL NOTE (alpha.25): no `context: fork` here. Per Anthropic docs, subagents cannot spawn other subagents. The three-wave orchestration pipeline requires the `Agent` tool, which is only available in the main thread. -->


# /feature-design — Multi-Agent Design Pack

Three-wave parallel-then-sequential pipeline that turns a feature idea into a versioned design pack ready for `/develop` to execute. Orchestrated by `feature-design-lead` (the only plugin agent with `tools: Task`). Conceptually aligned with [Shape Up](https://basecamp.com/shapeup): the idea is a shaped pitch; the output is a betting-ready package — fixed-time variable-scope.

## When to use

- Starting a new feature: `/feature-design "live collaborative cursors in markdown editor"`
- Validating a customer ask: `/feature-design "subscription tier with usage metering"`

## Not for

- Internal refactors → `/refactor`
- Hotfixes → `/bugfix`
- **Complete** existing PRD that just needs implementation → `/develop`

If the target repo already has a **partial** design pack (PRD exists but no design/AC/data-model), `/feature-design` still applies — see "Repo-local conventions + partial-pack mode" in Step 0.

## Invocation

```
/feature-design "Users can see where teammates are typing in real-time"
/feature-design "We need to limit API calls per month for non-paying users"
```

## Output (versioned with code, not with project memory)

Files written to **`<repo>/docs/features/<feature-id>/`** — INSIDE the target repo's `docs/`, NOT inside `.ai-skills-memory/`. Reason: design packs are intended to be VERSIONED IN GIT as project documentation, reviewed by the team, and live across many sprints.

| File | Producer | Notes |
|---|---|---|
| `PRD.md` | product-manager | Vision, success metrics, acceptance criteria |
| `MARKET-ANALYSIS.md` | marketing-strategist | Competitive snapshot, GTM angle (optional if not public-facing) |
| `ARCHITECTURE.md` | system-architect | System design, component diagram, dependency list |
| `UX-FLOW.md` | ui-ux-designer | User journeys, interaction flows, accessibility notes |
| `DATA-MODEL.md` | db-engineer | Schema, migrations, data flow (if relevant) |
| `IMPLEMENTATION-PLAN.md` | feature-design-lead | Work packages per stack, engineer role assignments, estimated effort |
| `RISKS.md` | security-engineer + qa-engineer | Identified risks, mitigation strategies, rollback plan |
| `REVIEW-LOG.md` | eval-judge | Auto-generated trace showing all review cycles and score deltas |

`<feature-id>` auto-generated from first 3 words of idea.

### Templates (`assets/`)

Concrete starter templates with worked examples (Two-factor auth feature). Producers copy + adapt rather than draft from scratch:

| Template | Used by | Purpose |
|---|---|---|
| `assets/prd-template.md` | product-manager (Wave 1) | PRD scaffold — TL;DR, problem, ICP+JTBD, solution, user stories, metrics, scope, open Qs |
| `assets/risks-template.md` | security-engineer + qa-engineer (Wave 2) | Risk register with 3×3 P×I heatmap and seeded example rows |
| `assets/implementation-plan-template.md` | feature-design-lead | Work-package decomposition with three-point estimates + mandatory Walking Skeleton WP-1 |
| `assets/review-log-template.md` | feature-design-lead (Wave 2/3 collation) | Multi-reviewer rounds, per-finding severity, signoff block |

## Agent roster

| Agent | Model | Wave | Tools | Writes its own file? |
|---|---|---|---|---|
| `feature-design-lead` | Opus | (orchestrator) | Task | — |
| `product-manager` | inherit | 1 | Read, Grep, Glob, Write, Edit | YES — writes `PRD.md` |
| `marketing-strategist` | inherit | 1 | Read, Grep, Glob, Write, Edit | YES — writes `MARKET-ANALYSIS.md` (skip if not public-facing) |
| `system-architect` | inherit | 1 | + Bash | YES — writes `ARCHITECTURE.md` |
| `ui-ux-designer` | inherit | 2 | Read, Grep, Glob, Write, Edit | YES — writes `UX-FLOW.md` |
| `db-engineer` | inherit | 2 | + Bash | YES — writes `DATA-MODEL.md` |
| `security-engineer` | sonnet | 2 | + Bash | YES — writes its section of `RISKS.md` |
| `qa-engineer` | inherit | 2 | + Bash | YES — writes its acceptance-criteria section |
| `product-manager` (reviewer) | inherit | 3 | (same as Wave 1) | YES — writes `feedback.md` |
| `system-architect` (reviewer) | inherit | 3 | (same as Wave 1) | YES — writes `architecture-review.md` |
| `eval-judge` | haiku | 3 | Read, Grep, Glob (intentionally read-only) | NO — returns verdict; Lead writes `REVIEW-LOG.md` from the structured return |

**Capability note (v0.3.8):** 9 of 10 producer roles ship with `Write` / `Edit` (Write scope = docs/design only). They write design artefacts directly — only `eval-judge` is verdict-in-response. Full cache: `@team-protocols/path-selection-rules.md`. Verbatim team-create prompt: [`path-b-team-create.md`](./path-b-team-create.md).

## Step 0a — Repo-local conventions + partial-pack mode (MANDATORY pre-pipeline)

Before announcing the path, the Lead detects (a) repo-local feature-doc conventions (`features/CLAUDE.md`, `docs/CLAUDE.md` overriding the default `docs/features/<id>/` layout), (b) any pre-existing PRD that puts the run into partial-pack mode, and (c) whether the repo requires a single consolidated `design.md` instead of separate `ARCHITECTURE/UX-FLOW/DATA-MODEL/RISKS` files. Full procedure including the mode-decision table, consolidate-vs-split rules, and judge-optional rules: [`step-0a-conventions.md`](./step-0a-conventions.md). Load it when actually running `/feature-design` against any non-trivial repo.

Announce: `"Step 0a: <path-pattern>; Mode: <standard | partial-pack | partial-pack-realign | consolidated | route-to-develop>; Input PRD: <path | none>; Judge: <required | optional | skipped>."`

## Choose execution path (Step 0 — Pre-spawn check + path selection)

Per `@team-protocols/path-selection-rules.md`: Path B (Agent Teams) is the default; Path A is selected on a hard technical block. The 3-wave pipeline maps to a shared task list with `dependsOn` enforcing wave gates structurally.

**Pre-spawn tool-capability check (MANDATORY):** read `plugin/agents/<role>.md` frontmatter `tools:` for every roster member AT AUDIT TIME (not from cache) — stale-cache alpha.32 has been observed. Confirm `eval-judge` is verdict-in-response and the team-create prompt is `path-b-team-create.md` verbatim.

Detection of Path B availability is implicit — no Bash env-var check. Announce one of:

- "Attempting Path B (Agent Teams) team-create..."
- (after fallback) "Agent Teams API returned: <verbatim error>. Falling back to Path A."
- (alpha.33-fast-fail — `TeamCreate` ok, total team silent ≥ 90 s) "Path B team-wide silent idle. Falling back to Path A per alpha.33 escape valve."

Invalid Path A triggers (sequential waves, tmux/iTerm2 absence, Windows host, single-stack, small feature) remain forbidden — **no silent fallback for non-technical reasons**. Full list + alpha.33 procedure: `@team-protocols/path-selection-rules.md`.

## Pipeline (Path B — Agent Teams, PREFERRED — try this FIRST)

Per `@team-protocols` "Dual-Path Detection → Path B" section. The Lead drives via natural language; each role-teammate is a full Claude Code session.

### Step 1 — create the team

The verbatim team-create prompt lives in [`path-b-team-create.md`](./path-b-team-create.md). Load it when actually executing Path B Step 1 — copy the verbatim prompt and substitute `<feature-slug>`. Do NOT shorten or paraphrase: the prompt encodes the v0.3.8 producer-writes-its-own-file pattern, the `eval-judge` verdict-in-response pattern, and the HTML-escape forbidance clause.

### Step 2 — populate the shared task list with wave gates

Wave-2 tasks `dependsOn` all wave-1 tasks. Wave-3 tasks `dependsOn` all wave-2 tasks. The dependency graph enforces the wave gates structurally — no manual gate-checking needed.

### Step 3 — drive and monitor

- Wave-1 teammates self-claim their task immediately and work in parallel.
- When all wave-1 tasks complete, wave-2 teammates auto-claim. The user uses Shift+↓ to peek into any role's transcript.
- Wave-3 runs sequentially because the three tasks share `dependsOn` chains pm-review → sysarch-review → judge.
- If `judge` returns rubric score < 4.0 or any dimension < 3 → Lead inserts wave-2 follow-up tasks ("re-prompt with feedback") and re-points wave-3 dependencies. RALF caps from `ralph-budget.md` apply (5 iter / 250K tokens / 60 min).

### Step 4 — finalize + cleanup

After the judge returns a verdict the Lead MUST:

1. **Post-judge reconciliation** per `@team-protocols/lead-protocol.md`. Judge findings against files Lead-edited since the judge's read must be reconciled; re-spawn judge if ≥ 2 stale findings or the verdict would flip.
2. On PASS: write IMPLEMENTATION-PLAN.md in main thread (not a teammate task); record L4 memory write.
3. **Team cleanup** per `@team-protocols/lead-protocol.md`: `shutdown_request` to every teammate, then `TeamDelete`. Skipping `TeamDelete` strands the team in `~/.claude/teams/<team-name>/`.

## Pipeline (Path A — Subagents fallback, only if Path B Step 1 returned a technical error)

Three-wave pipeline with parallel Wave-1 / Wave-2 spawns and a sequential Wave-3 cross-check + eval. The full wave-by-wave ASCII tree (per-agent context-load, gate checks between waves, RALF retry hookup, and the final IMPLEMENTATION-PLAN.md handoff) lives in [`wave-protocol.md`](./wave-protocol.md). Load it when actually executing Path A.

## G7 spawn payloads

Every spawn embeds a structured payload per `plugin/schemas/spawn-payload.schema.json`. Lead validates returns against `plugin/schemas/return-contract.schema.json` (via `subagent-stop-learnings.py` hook).

Trace IDs follow pattern `wf-<YYYYMMDD>-<feature-id>-spawn-<seq>`. Allows span tracing across all 9+ spawns per design.

## Eval, RALF, memory, observability

The 6-dimension eval rubric (pass: avg ≥ 4.0, no dimension < 3), RALF caps (5 iter / 250K tokens / 60 min, kill-on `regex:RUBRIC_FAILED_3X`), memory-write layers (L4 wave1-summary + L4 final + opt-in L4 committed), failure modes (timeouts, oscillation, oracle crashes, budget hits), and observability events written to `runs.jsonl` all live in [`eval-and-ralf.md`](./eval-and-ralf.md). Load it when running the Wave-3 → RALF retry loop, validating rubric scores, or diagnosing why a design didn't converge.

## Integration

- **Orchestrator agent**: `feature-design-lead` (Opus, `tools: Task`, only plugin agent allowed to spawn)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Companions**: `/context-load` (per-role context slices), `/subagent-spawn` (G7 payload helper), `/ralph` (RALF segment)
- **Followed by**: `/develop` (consumes IMPLEMENTATION-PLAN.md to execute work packages)
- **Rules**: `subagent-isolation` (G7 + bounded recursion + sequential code-mod gate), `untrusted-content-wrapping` (G1 wrap on subagent returns + project file reads), `ralph-budget` (caps), `geo-content` (if public-facing — applied during MARKET-ANALYSIS step), `humanize-content` (applied to all public-facing copy), `memory-discipline` (memory writes per layer)
- **Hooks**: `tool-output-wrap.py` + `tool-output-normalize.py` (G1+G2 on tool outputs), `subagent-start-budget.py` (G7 spawn validation + budget enforcement), `subagent-stop-learnings.py` (G7 return validation)
