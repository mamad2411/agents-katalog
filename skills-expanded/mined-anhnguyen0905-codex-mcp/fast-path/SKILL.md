---
name: fast-path
description: Route small or read-only codex-flow work through a lite lane instead of the full six-phase flow — analysis-lane and small-change-lane eligibility, the always-full-flow exclusions, each lane's workflow, the mechanical scope trip-wire, the durable fastpath.log record, and the escalation rule.
---

# Fast-path gate — small and analysis-only tasks

**Helpers**: required — none; optional — none.

The full six-phase flow is for multi-task feature work; route small or read-only work through one
of these lite lanes. Evaluate this gate after the preflight resume check and BEFORE the first
`mcp__codex__codex_health` call, before writing control files.

**Eligibility** — the task must fit ONE of these lanes, and NONE of the exclusions:

- **Analysis lane**: the deliverable is an answer, report, or data readout; no tracked project
  file is created or modified. Examples: "why is X slow", "analyze this export", "compare these
  two builds", "review this module's structure".
- **Small-change lane**: a well-specified change touching ≤ 2 files with unambiguous requirements
  and a checkable outcome. Examples: a config flag, a copy fix, a single-function bug fix with a
  known repro.

**Exclusions (always full flow)**: security-sensitive changes (auth, payments, secrets,
migrations, input handling), changes spanning components or contracts, ambiguous requirements
that need real elicitation, anything the user explicitly asked to run as the full flow. When
unsure, ask the user one question: fast path or full flow.

Optional Jev assist (off by default): load `codex-flow:jev-assist`.

**Analysis lane workflow**: Claude works directly — read code, run read-only commands, query
data — and delivers the findings with a short "what I verified" note. No Codex session is
required (this lane is exempt from the Codex health gate): call `mcp__codex__codex_health` with
`{ deep: true }` only when the user requests an independent second opinion, and then use a single
read-only `mcp__codex__codex_execute` only when that opinion adds value AND Codex is healthy. When that second opinion fails, is refused by a `quota`/`model` `execProbe`, or times out,
the analysis is delivered Claude-only and the failure is named in the "what I verified" note (for
example "Codex second opinion unavailable: quota") — never silently drop it and never present a
single-reviewer readout as dual-verified. For any data-analysis work, follow the Data tooling rules in
`codex-flow:exec-deliverable` (measure input sizes first, ingest-once columnar tooling,
sample-first iteration) — never row-by-row scripts over large raw files.

**Small-change lane workflow**: first run the project's test command once and note any
pre-existing failures as the lane's known-red list — only failures NOT on that list count against
the change. Then, after the one `mcp__codex__codex_health { deep: true }` call this lane shares with the full
flow, one `mcp__codex__codex_execute` carrying the same embedded blocks
Phase 4 would use (`codex-flow:exec-coding-standards`, `codex-flow:exec-self-testing`, the
project-language skill), then ONE Claude review pass in Phase 5 order (conformance → quality →
security triggers, per `codex-flow:review-conformance`, `codex-flow:review-quality`,
`codex-flow:review-security`) plus running the relevant tests yourself against that known-red
list. Skip the dual `codex_review`, backlog, reports, and improvement gate. Route fixes back via
`mcp__codex__codex_continue`, up to 3 rounds as usual. Do not commit unless the user asks.

**Scope trip-wire (mechanical, not judgment)**: after each small-change `codex_execute` or
`codex_continue` returns, diff the actual changed files (the returned `diff` plus
`git status --porcelain`) against the ≤ 2 files the lane was entered with. ANY extra changed
file — excluding generated lockfiles — triggers the escalation rule automatically; do not review
the oversized diff in-lane and do not re-argue eligibility after the fact.

**Fast-path log**: append one line per fast-path run to `.codex-flow/notes/fastpath.log`:
`<ISO 8601> <analysis|small-change> <one-line task> session=<sessionId or -> outcome=<delivered|done|escalated|failed> evidence=<pass|fail|off>`; see profile-pilot's Fast-path analysis lane for evidence rules.
The recorded sessionId is what later `codex_continue` fix rounds attach to; the log is the only
durable trace a fast-path run leaves, so write it even on escalation or failure.
Append the matching `fast-path-analysis` or `fast-path-small` run-ledger line at the terminal outcome.

**Escalation rule**: the moment fast-path work reveals the task is bigger than its lane — more
files than declared (the trip-wire), architectural impact, hidden ambiguity — STOP, log
`outcome=escalated` with a note of any partial work that exists, tell the user what changed,
and restart at Phase 1 with the full flow. A wrong up-front size estimate is not a failure;
stretching the lane to avoid the restart is. Never stretch a lane.
