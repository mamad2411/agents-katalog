---
name: designing-loops
description: Design the right loop for agentic work — choose between a plain prompt, a goal loop, a scheduled loop, or a proactive routine, then write stop conditions, intervals, and token budgets that actually hold. Use whenever the user wants recurring or long-running agent work: "keep doing X until Y", "babysit this PR", "check X every N minutes", "run this overnight", "set up a loop / routine / schedule", "fix all N errors", or asks whether something should be a loop at all. Also use before writing any /goal, /loop, or /schedule prompt, and when auditing why an existing loop overran, stalled, or burned tokens.
---

# Designing loops

A loop is an agent repeating cycles of work until a stop condition is met.
Every loop design answers three questions:

1. **What triggers a cycle?** (you, a goal not yet met, a clock, an event)
2. **What stops the whole thing?** (your judgment, verifiable criteria, cancellation)
3. **What keeps quality and cost bounded while it runs?**

Most loops fail on question 2, not question 1. People spend their effort
picking the trigger mechanism and one sentence on "until it's done" — then the
loop either quits early or runs all night doing nothing useful. So this skill
front-loads the stop condition.

The four-type taxonomy below comes from the Claude Code team's article
*Getting started with loops*. The guardrails and the runbook pattern come from
running real multi-hour autonomous loops and auditing what they claimed
afterwards.

## Step 0 — Does this need a loop at all?

Take the lowest rung on this ladder that solves the problem:

```
better prompt  <  verification skill  <  goal loop  <  scheduled loop  <  proactive routine
```

Each rung up adds token cost, latency, and new failure modes. Concretely:

- If one turn keeps failing because the agent can't tell whether its work is
  correct, the fix is a **verification skill** (encode how to check the work:
  run the app, click the thing, read the console), not a loop. A loop around
  an agent that can't self-verify just repeats the blindness N times.
- If the task is one-shot and merely large, use subagents or a workflow, not
  a loop. Loops are for *repeated cycles*, not *big batches*.
- Reach for a loop when iteration is essential (the goal takes several
  attempts) or the work genuinely recurs (new inputs keep arriving).

If the answer is "no loop", say so and stop here. Recommending against a loop
is a valid, complete outcome of this skill.

## Step 1 — Classify the loop

Ask two questions: **what triggers a cycle** and **what stops it**.

| Type | Trigger | Stop | Primitive | Best for |
|---|---|---|---|---|
| **Turn-based** | Your next prompt | Model judges it's done | Plain prompt + verification skill | Exploration, one-off tasks where you're deciding as you go |
| **Goal-based** | One prompt, now | Criteria met OR turn cap | `/goal` | Tasks with a verifiable exit condition ("0 failing tests") |
| **Time-based** | Clock interval | You cancel, or the work dries up (PR merged, queue empty) | `/loop` (runs locally), `/schedule` (runs in cloud) | Recurring work; watching external systems (CI, reviews, feeds) |
| **Proactive** | Event or schedule, no human present | Each task exits on its own goal; the routine runs until turned off | `/schedule` + `/goal` + workflows + auto mode | Well-defined recurring streams: triage, migrations, dependency bumps |

Not every install has every primitive — check what's available before
prescribing one. Every row has a prompt-level fallback:

- No `/goal` → put explicit criteria and a cap in the prompt: *"Keep going
  until all tests pass. Stop after 5 attempts and report what's blocked."*
- No `/loop` or `/schedule` → an agent that can schedule its own wake-ups can
  self-pace; otherwise cron + a headless invocation does the same job.

Mixed cases resolve by the *stop* question. "Fix CI on this PR" sounds
goal-based, but CI keeps re-triggering as reviewers push — the loop stops when
the PR merges, not when a criterion is met once. That's time-based.

## Step 2 — Write the stop condition first

Write the stop condition before the work description. Rules that hold up:

**A number beats an adjective.** "Get Lighthouse to 90+", "RSS under 80MB",
"0 strict-mode errors" — these let an evaluator or the agent itself decide
mechanically. "Make it faster", "clean up the errors" force the agent to
judge "good enough", and under pressure it will judge generously. Vague done
criteria is how a loop turns into a space heater.

**Always dual-stop.** Success condition OR bounded failure — never just one:

```
Stop when: all 47 strict errors are fixed and tests pass
OR: 5 consecutive attempts produce no reduction in error count
```

A success-only stop runs forever when the goal is unreachable. A cap-only
stop does five sloppy attempts and quits with the goal in reach.

**Per-item failure policy for multi-item loops.** The same failure three
times → mark that item BLOCKED with the reason and move to the next item.
All items blocked → report and stop (or drop to a slow heartbeat). Without
this, one poisoned item eats the whole night's budget.

**Guard against goal redefinition.** Long loops under pressure quietly
redefine "done". Real example from a 15-iteration overnight run: the original
target was "release-build peak memory ≤ 500MB"; the release benchmark
wouldn't compile, so the loop re-scoped the goal to "long-term memory health"
and reported ✅. The redefinition was even reasonable — but ✅ no longer meant
what the human thought it meant. Defense: pin original metrics in writing
where the loop can't edit their meaning (the runbook's goal table), and audit
claimed ✅ against the *original* numbers afterwards (Step 6).

## Step 3 — Match the interval to the watched thing

For time-based loops, the interval is a property of the world, not a
preference:

- Ask: **how fast does the watched thing actually change?** Reviews arrive
  over hours → 15–30 min. A CI run takes ~8 min → check twice at ~4 min, not
  every 60 s. A nightly feed → daily.
- Prefer the longest interval that still catches the change in useful time.
  Every wake-up replays context; too-frequent polling is pure token burn.
- For agents that schedule their own wake-ups: prompt caches typically have a
  ~5-minute TTL. Waking inside that window is cheap; just past it is the
  worst of both worlds. Cluster wake-ups (stay under the TTL while actively
  working; commit to a much longer sleep when idle) rather than picking round
  numbers like "every 5 minutes".
- If the system emits events (webhooks, notifications), react to events and
  keep only a slow heartbeat as fallback.

## Step 4 — Bound the cost

Put these in the loop prompt itself, not in your intentions:

- **Pilot first.** Run one slice before the full run — one file, one report,
  one iteration — and gauge tokens before committing to 200 items overnight.
- **Route by difficulty.** Mechanical steps go to a cheaper, faster model;
  reserve the top model for judgment calls and final review.
- **Script the deterministic parts.** If every iteration re-derives the same
  transformation, write the script once and have the loop call it.
- **State the budget.** "Stop and report if you exceed N turns / roughly N
  tokens" gives the loop permission to stop, which it otherwise lacks.

## Step 5 — Heavy tier: give the loop a runbook file

When a loop will run many iterations unattended (overnight, multi-hour,
high-risk changes), do not stuff the design into the prompt. Create a
**runbook file** in the repo that the loop re-reads at the start of every
iteration and updates at the end. Template and instructions:
`references/runbook-template.md`.

A runbook contains: a goals table with quantified metrics and the dual stop
("all achieved or all blocked"), tiered guardrails (allowed / red lines /
conditional), a work queue with per-item risk labels, an iteration protocol,
and an append-only ledger ending in a human-readable report.

Why a file instead of a long prompt: each wake-up may start with thin
context, so durable state must live outside the conversation. The ledger
makes every decision auditable afterwards — it is the thing you reconcile
against in Step 6. And committing the runbook each iteration means a crashed
loop can resume exactly where it stopped.

## Step 6 — Audit after the loop

The loop's final report is a claim, not a fact. Budget a reconciliation pass
after any substantial run:

- **Re-measure the headline metrics yourself.** Same real overnight run as
  above: the loop self-reported 122MB; independent measurement said 79MB —
  better than claimed, but only the audit made the number trustworthy either
  way.
- **Check each ✅ against the goal's original wording**, not the wording in
  the final report (see goal redefinition, Step 2).
- **Adversarially verify before trusting fixes.** In that same run, 40
  candidate fixes went through skeptic review; only 15 survived. If the loop
  merges its own work, the merge gate (tests + independent review + no
  observable regression) belongs in the runbook's guardrails.
- **Keep the vetoed list.** What the loop tried and rejected — with reasons —
  prevents the next loop from re-attempting known dead ends. Rejections are
  results too.

## Output format

When this skill designs a loop, deliver all of:

1. **Type + one-line justification** (or "no loop needed, here's the simpler fix")
2. **The ready-to-run prompt or command**, verbatim
3. **Stop conditions** — success, failure cap, per-item policy
4. **Cost bounds** — interval justification, model routing, budget line
5. **Heavy tier only**: the runbook file, written to the repo

## Worked examples

**"Babysit PR #142 until it merges"** → Time-based. Reviews and CI change on
the scale of tens of minutes:

```
/loop 15m check PR #142: address new review comments, fix failing CI.
Stop when the PR is merged. If the same CI failure persists after 3
consecutive fixes, stop and summarize what's blocked.
```

**"Fix all 47 TypeScript strict errors"** → Goal-based. Verifiable exit,
bounded failure:

```
/goal tsc --strict reports 0 errors and the test suite passes. Work in
batches of ~10 errors, run tests after each batch. Stop after 6 attempts
or if two consecutive batches reduce the error count by zero.
```

**"Keep memory under 200MB, run overnight"** → Heavy tier. Multi-hour
autonomous run touching risky code: write a runbook
(`references/runbook-template.md`), then start a self-pacing session pointed
at it. Plan the Step 6 audit for the morning.

**"Translate the README to Japanese"** → No loop. One turn, verifiable by
reading. Recommending against the loop is the correct output.
