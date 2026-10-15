---
name: panel-plan
description: >
  Run a single independent panel review of a written plan (a design /
  implementation markdown file), before any code is written. Use this skill
  whenever the user asks to "panel plan" / "panel-plan", "have the panel review
  my plan", "panel-review this plan", "get second opinions on this plan", "get
  the panel's take on this plan", "fan out a plan review", or any similar
  phrasing asking for one independent multi-agent review pass over a plan. Fans
  the plan out to multiple local CLI coding agents (codex, claude, opencode),
  each in a fresh non-interactive subprocess with no shared state, reading the
  plan + the repo it targets read-only, then synthesizes their findings (gaps,
  wrong assumptions, infeasible steps, risks) and open questions into one
  report. This is the planning-time analog of panel-review (which reviews
  shipped code). It is ONE pass and does NOT edit the plan — for the
  iterate-edit-re-review loop to convergence, use panel-plan-loop. Do NOT use
  for reviewing a code diff or PR (that is panel-review), or when the user just
  wants this session to critique the plan itself.
---

# panel-plan

Fans a written plan out to multiple independent local CLI agents in parallel and
synthesizes their findings into one report. Each panelist runs in its own
subprocess with no shared conversation state — they see only the plan, the repo
it targets (read-only), and the review prompt. That no-shared-state property is
the whole point: genuinely independent second opinions on the plan.

This is **one review pass**, the planning-time sibling of `panel-review`. It
reports; it does **not** edit the plan. For the iterate → edit → re-review loop
that hardens a plan to convergence, use **`panel-plan-loop`**, which calls this
skill each round.

## When to use

- User has a written plan (a design / implementation `.md`, e.g. from
  brainstorming or `writing-plans`) and wants an independent panel to look at
  it.
- User says "panel plan", "have the panel review my plan", "get the panel's take
  on this plan", or similar — a single pass.

When _not_ to use:

- User wants the plan iterated / hardened / "kept running until it's solid" →
  use `panel-plan-loop`.
- Reviewing a code diff or PR → use `panel-review`.
- User wants _this_ session to critique the plan → just do it inline; no
  fan-out.
- The plan does not exist yet → brainstorming / `writing-plans` first.

## Steps

1. **Resolve the plan file.** In priority order: an explicit path given (as an
   argument or in the request) → the most recent plan/spec produced in this
   conversation → ask the user which file. The plan must be a markdown file that
   exists on disk. If the plan only lives in the conversation, write it to a
   file first (confirm the path with the user).
2. **Pick panelists.** Default: every supported CLI on `PATH` (codex, claude,
   opencode). The user (or the caller) may name a subset via `--panelist`.
3. **Capture optional focus.** If context was given ("focus on the migration
   strategy"), pass `--focus`.
4. **Run the panel.** Run `skills/panel-plan/panel-plan.sh --plan <file>` (plus
   `--focus` / `--panelist` as chosen). Launch and monitor it **exactly** the
   way `panel-review` does — those operational rules apply verbatim:
   - Launch as a **background Bash** (`run_in_background: true`) and poll with
     `BashOutput` on the returned `bash_id` **every 10 seconds** until every
     panelist has emitted its `done (exit N)` heartbeat. This overrides the
     default "don't poll background tasks" guidance — the heartbeats and
     per-section streaming exist precisely so you can show live progress.
   - Do **not** launch via the `Agent` tool / `TaskCreate` / any subagent
     mechanism (no streaming-output API for in-flight subagents). Do **not**
     poll via `sleep N && grep`. `BashOutput` is the only correct progress
     mechanism.
   - A quiet `BashOutput` is **not** a hang. The only stderr signals are
     `panel-plan: <name> started` and
     `panel-plan: <name> (<model>) done (exit N)`; between them a panelist can
     go many minutes silent. The script enforces a per-panelist `timeout`
     (default 600s); your job is to wait it out. Intervene only if the `bash_id`
     itself exits, an obvious failure surfaces (panic / OOM / CLI-not-found), or
     the run vastly exceeds `timeout × panelists` with zero `done` heartbeats.
   - **Live progress UX (same as panel-review):** `TodoWrite` one todo per
     panelist (`Review: codex`, …) plus a `Synthesize findings` todo; flip each
     to `in_progress` on its `started` heartbeat and `completed` on its `done`
     heartbeat; post a one-line status including the self-reported model
     (`✓ codex (gpt-5.5) — N findings, M open questions`); and **stream each
     panelist's full `## <name> / <model>` section to chat the moment it
     lands**. A panelist that failed — non-zero exit **or** empty output (e.g. a
     provider quota / usage-limit / auth error, or a timeout) — is reported by
     the script as `done (exit N) — FAILED: <reason>`; surface it as
     `✗ <name> (<model>) FAILED (exit N): <reason>` and treat that panelist as
     having contributed **nothing**.
   - **If you cannot use `run_in_background` / `BashOutput` is unavailable in
     this harness:** run the script in the **foreground** with `timeout: 600000`
     (10 min) — the default 2-minute Bash timeout will kill the call before
     Codex returns. You lose live progress; warn the user. Do **not** improvise
     a waiting mechanism: no `sleep N && grep` loops against the output file,
     and **never** arm a `ScheduleWakeup` / cron whose payload re-invokes
     `/panel-plan` or this script as a "fallback heartbeat." Harness-tracked
     background Bash already re-invokes you when it completes, so a fallback
     timer is never needed — and a stale one fires later and re-runs the whole
     skill as a stray action (this has happened: a fallback wakeup re-triggered
     an extra round after the user had finalized). The only sanctioned ways to
     wait are `BashOutput` polling (preferred) or a single foreground call with
     a long timeout.
5. **Synthesize** (see below). Wait for **all** panelists to finish before
   synthesizing; partial output is fine to _show_ during the wait, but consensus
   / disagreement analysis needs every panelist's verdict.

## Synthesis

Read the script's combined output (one section per panelist + a tempdir path),
then produce the report:

- **Dedup findings** across panelists by `<plan>:LINE` (or overlapping ranges)
  AND substantively-same claim; list every panelist on a `Flagged by:` line and
  prefix with the count when ≥2 raised it. Use the higher severity when they
  differ and note it inline.
- **Bucket by severity:** `### must-fix` (CRITICAL/HIGH), `### should-fix`
  (MEDIUM), `### polish` (LOW). Omit empty buckets — no "none" placeholders.
- **Collect the union of `Open questions`** from every panelist; dedup; surface
  them in an `### Open questions` section. These are decisions only the plan's
  author can make — the primary thing a single pass surfaces for a human.
- **Verify questionable findings before surfacing them.** Same discipline as
  panel-review: a unique CRITICAL/HIGH claim, a `Fix:` that doesn't address the
  issue, a suspicious line reference, panelist disagreement, or reasoning that
  depends on codebase behavior the panelist didn't actually check — open the
  plan and/or the referenced code (`Read`/`Grep`) and confirm before surfacing
  it. Drop what you can falsify; note the correction.
- **Misinterpretation check.** If a panelist's `Goal:` line disagrees with what
  the plan actually says, call it out and treat that panelist's findings with
  extra skepticism — a misread goal produces confidently-wrong findings.

Section order: `### Overview` (one line naming the plan + a sentence of what it
aims to do; lead with the goal only when panelists agreed on it) → `### Risk`
(LOW/MEDIUM/HIGH/CRITICAL on the plan, one-sentence justification) →
`### must-fix` / `### should-fix` / `### polish` (omit empties) →
`### Open questions` → `### Disagreements` (only when panelists actually
contradict each other; omit otherwise).

**Per-finding shape:**

```
- [SEVERITY] <plan>:LINE — one-sentence issue.
  Fix: one-sentence suggested change to the plan.
  Flagged by: codex (gpt-5.5)
```

## Output discipline

- **Carry the panelist's self-reported model everywhere** you name a panelist
  (`Flagged by: codex (gpt-5.5)`), exactly as panel-review does. Surface
  `(unknown)` rather than omitting it.
- **Don't paraphrase or invent.** Surface what the panelists actually said;
  correct an obviously-wrong line reference, but never fabricate one to satisfy
  the format. A `NO_FINDINGS` panelist is still reported, not dropped.
- **This skill is read-only.** Report the findings and open questions; do not
  edit the plan file. (Editing across rounds is `panel-plan-loop`'s job.)
- The synthesized report is the deliverable — most readers won't scroll up to
  the raw per-panelist sections, so put the substance there.

## Reference

CLI flags and env vars: run `bash skills/panel-plan/panel-plan.sh --help`.

The script:

- Embeds the plan file (with line numbers via `nl`) into the prompt so panelists
  can cite `<plan>:LINE`.
- Runs every panelist **read-only** against the working tree (codex
  `--sandbox read-only`, claude `--permission-mode plan`, opencode `plan` agent)
  — they can read the codebase the plan targets to check feasibility but cannot
  modify anything. No diff, no git worktrees, no `gh`.
- Emits stderr heartbeats and `## <name> / <model> (exit N)` section headings
  identical in shape to panel-review, so the progress / streaming logic is the
  same.
- If a panelist times out or fails, the others' output is kept and the script
  exits 2 — surface the failure rather than dropping the panelist.
- Panelists pick up the project's `AGENTS.md` / `CLAUDE.md` — intentional, but
  worth knowing if those would bias the review.
