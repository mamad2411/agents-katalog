---
name: panel-plan-loop
description: >
  Harden a written plan by iterating it through an independent agent panel until
  it converges. Use this skill whenever the user wants a plan repeatedly
  reviewed and improved — phrasings like "panel plan loop", "iterate on this
  plan with the panel", "harden this plan", "keep running the panel on my plan
  until it's solid", "loop the panel on this plan", "panel-review this plan and
  fix it", "review and iterate my plan", or any request implying more than one
  review pass with edits in between. It runs the panel-plan skill each round (a
  fresh no-shared-state panel over the plan), then synthesizes, applies the
  clear uncontested fixes to the plan directly, raises genuine judgment calls
  and open questions to the user, updates the plan, logs the round, and re-runs
  the panel — looping until a round surfaces no new must/should-fix concerns
  (then asks the user) or a round cap is hit. This is the planning-time analog
  of iterating a PR through repeated review. For a SINGLE review pass with no
  edits, use panel-plan instead. Do NOT use for code diffs / PRs (that is
  panel-review).
---

# panel-plan-loop

Iterates a written plan through multiple rounds of independent panel review,
editing the plan between rounds, until it stops attracting significant concerns.
Built **on top of** `panel-plan`: each round is one invocation of that skill (a
fresh, no-shared-state panel that reads the plan + the repo it targets and
returns synthesized findings + open questions). This skill owns everything a
single pass does not — the loop, the triage of which fixes to apply vs. raise,
the plan edits, the cross-round log, and the convergence decision.

**Division of labor.** `panel-plan` reviews and reports (read-only). This skill
_acts on_ those reports: it edits the plan and decides when to stop. Keeping the
review primitive dumb and read-only is what lets the panel stay genuinely
independent each round — the memory lives here, in the coordinator, never in the
panelists.

## When to use

- User has a written plan and wants it _hardened_ — reviewed, fixed, and
  re-reviewed until solid, not just looked at once.
- User says "iterate this plan with the panel", "keep running the panel until
  it's clean", "panel plan loop", "review and fix my plan", or similar.

When _not_ to use:

- User wants a single review pass with no edits → use `panel-plan`.
- Reviewing a code diff or PR → use `panel-review`.
- The plan does not exist yet → brainstorming / `writing-plans` first.

## Pre-flight (before round 1)

0. **Re-entry guard — check for a prior verdict first.** Before doing anything
   else, look for an existing `<plan-dir>/<plan-basename>.review.md`. If it
   exists and its last entry is a `## FINALIZED` marker (or otherwise shows the
   plan already converged), the plan has already been hardened — **do not
   auto-start a round.** Report the prior verdict ("this plan converged at round
   N on <date>; last verdict: …") and **ask** whether the user is re-opening it
   for another round. Only proceed when the user (in _this_ invocation)
   explicitly asks for another round / to re-open it. This exists because a
   stray re-trigger — e.g. a leftover scheduled wakeup, a fat-fingered re-run —
   must not silently relaunch the panel on a plan the user already finalized.
1. **Resolve the plan file** (same priority as `panel-plan`: explicit path →
   most recent plan in the conversation → ask). It must be a markdown file on
   disk; write it out first if it only lives in the conversation. You own this
   path for the whole loop — every round reviews and edits the same file.
2. **Pick panelists** (default: all of codex/claude/opencode on `PATH`; user may
   subset) and **capture optional focus**. Hold these fixed across rounds so
   rounds are comparable.
3. **Name the review-notes file:** `<plan-dir>/<plan-basename>.review.md`. You
   append one entry per round here; the plan file itself stays free of review
   chatter.

## Each round

### Step 1 — Run one panel review

Invoke the **`panel-plan` skill** on the resolved plan file (passing the same
`--panelist` / `--focus` choices). It launches the panel, streams progress, and
returns a synthesized report: findings bucketed by severity (must-fix /
should-fix / polish), each with `<plan>:LINE` + a suggested `Fix:`, plus an
`### Open questions` section and a `### Risk` read. Let it run to completion —
all of its background-Bash / heartbeat / streaming behavior is its own concern;
you consume its synthesized output.

### Step 2 — Triage every item: auto-fix vs. raise to the user

This is the heart of the loop. Sort every finding and every open question from
the round into exactly one path:

- **Auto-fix — edit the plan directly.** Clear, uncontested improvements that do
  not change _what the plan is trying to do_: filling an obvious gap, correcting
  a verified-wrong assumption about the codebase, fixing step ordering, adding a
  missing error / rollback / verification step, tightening a vague step into a
  specific one.
- **Raise to the user — ask before editing.** Anything that needs a human
  decision: every **open question**, any trade-off with no clear winner, any
  scope expansion or reduction, product/UX decisions, panelist disagreements you
  could not resolve, and any edit that would change the plan's intent or success
  criteria. Surface these with `AskUserQuestion` (or prose if open-ended), and
  apply the user's decisions afterward.

**When in doubt, raise it.** The point of the loop is that anything worth a
human's attention reaches the human. Better to ask one extra question than to
silently bake a debatable decision into the plan.

Present the round to the user as a compact summary that clearly separates "I'm
fixing these directly" from "I need you to decide these."

### Step 3 — Update the plan and the review-notes file

- Apply the auto-fixes and the user's decisions to the plan `.md`.
- Append a round entry to `<plan>.review.md` (shape below): the concerns + who
  flagged them + how each was resolved, the open questions + the user's answers,
  and the concrete edits applied.

### Step 4 — Convergence check

- **If this round surfaced no new CRITICAL/HIGH/MEDIUM findings** (only LOW /
  nitpicks, or `NO_FINDINGS` across the board), the plan has converged. Tell the
  user, summarize the plan's current state, and **ask whether to stop here or
  run another round.** Do not silently keep looping past convergence.
- **Otherwise**, automatically start the next round (back to Step 1) against the
  _updated_ plan. Briefly tell the user you're iterating again and why.
- **Safety cap: 4 rounds.** If you reach round 4 without convergence, stop,
  report the remaining open items, and ask the user how to proceed rather than
  looping indefinitely.

**Whenever the loop ends** — convergence, the user choosing to stop, or the
round cap — append a `## FINALIZED — round N (<verdict>)` marker as the last
entry in `<plan>.review.md` (verdict = `converged` / `stopped by user` /
`round cap reached, open items remain`). This marker is what the Step 0 re-entry
guard reads to avoid relaunching the panel on an already-finalized plan, so it
is mandatory, not optional.

**Never wait by re-invoking yourself.** Do not arm a `ScheduleWakeup` / cron
whose payload re-runs `/panel-plan-loop` or `/panel-plan` between rounds or as a
"fallback heartbeat." Each round is a harness-tracked `panel-plan` invocation
that returns control to you when it finishes — there is nothing to poll for with
a timer. A stale self-re-invoking wakeup is exactly how an extra, unwanted round
got launched after a user finalized; the loop advances only by your own control
flow, never by a scheduled re-trigger.

Because each round is a fresh `panel-plan` invocation against the current plan,
panelists always judge the latest version with no cross-round contamination —
the only thing carried forward is your edits and the notes file.

## Review-notes file shape

`<plan-basename>.review.md`, alongside the plan:

```markdown
# Panel review log — docs/specs/2026-05-29-foo-design.md

## Round 1 — codex (gpt-5.5), claude (opus-4.7), opencode (qwen3.6)

### Concerns

- [HIGH] foo-design.md:42 — migration step runs before the table is created.
  Flagged by 2: codex, claude. Resolution: reordered steps 3↔4 in the plan.
- [MEDIUM] foo-design.md:88 — no rollback described for the data backfill.
  Flagged by: codex. Resolution: added a rollback note to §6.

### Open questions raised to user

- Q: Per-tenant or global cache? → A (user): per-tenant. Plan §5 updated.

### Edits applied

- Reordered §3 steps; added rollback note to §6; specified cache scope in §5.

## Round 2 — …

## FINALIZED — round 2 (converged)

No new CRITICAL/HIGH/MEDIUM in round 2; user confirmed stop. Plan is
implementation-ready.
```

The trailing `## FINALIZED` line is the signal the Step 0 re-entry guard looks
for on a later invocation.

## Notes

- **Don't re-implement the review.** The panel run, the synthesis, and the
  finding shape all belong to `panel-plan`. If you find yourself parsing raw
  panelist output here, you've crossed the boundary — invoke `panel-plan` and
  consume its synthesis instead.
- Carry each panelist's self-reported model through your round summaries and the
  notes file (`Flagged by: codex (gpt-5.5)`), as `panel-plan` does.
- A round where the panel returns `NO_FINDINGS` everywhere is the cleanest
  convergence signal — report it and ask whether to stop.
