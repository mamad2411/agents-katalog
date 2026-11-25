---
name: plan-optimizer
description: >-
  Iteratively optimize a plan by scoring it against a rubric, critiquing it, and
  rewriting it until the score plateaus. Use this skill whenever the user wants
  to refine, improve, harden, stress-test, or "make the best possible" version
  of a plan of any kind — project plans, execution/rollout plans, code
  implementation plans, research plans, strategy memos, study plans, training
  plans, go-to-market plans, or proposals. Trigger it when the user says things
  like "improve this plan", "iterate on this until it can't get better", "score
  and refine my approach", "find the holes in this plan", "make this plan
  bulletproof", or describes wanting an automatic improve-and-score loop. Also
  use it proactively when the user shares a draft plan and asks "is this good?"
  or "what would make this better?" — the loop produces a measurably stronger
  plan than a single critique pass.
---

# Plan Optimizer

This skill turns plan-writing into a search problem. Instead of producing one
plan and hoping it's good, you generate a plan, **score it numerically against
an explicit rubric**, **critique it**, **rewrite it to fix the weaknesses**, and
repeat — keeping the best version seen so far — until the score stops improving.
That plateau is your signal that further iteration is just noise, and you stop.

The reason this works is that scoring and rewriting are *separate* acts.
Generating a plan and judging a plan use different cognitive muscles; forcing an
explicit critique between revisions converts blind rewriting into directed
search that climbs toward a target rather than drifting sideways.

## When to use this

Use it whenever there's a plan that should be as good as it can reasonably get
and the cost of a weak plan is real. If the user just wants a quick first draft,
don't impose the whole loop — offer it. If they want the *best* plan, run the
loop.

## The loop at a glance

```
plan        = generate the initial plan from the task
best        = plan
best_score  = score(plan)            # 0-100, against the rubric
history     = [best_score]

repeat:
    candidate = improve(best)        # critique -> targeted rewrite
    s         = score(candidate)
    if s > best_score + MARGIN:      # require a real margin, not noise
        best, best_score = candidate, s
    history.append(best_score)
until plateau(history)               # no real gain over the last K rounds
return best, history
```

Run this in your head / in the conversation, not as code — the "functions" are
reasoning steps you perform. Keep all intermediate plans and scores so you can
show the trajectory at the end.

## Step 1 — Build the rubric first

Before writing any plan, write the rubric. **The rubric is the ceiling**: the
loop can only climb as high as the rubric lets it perceive quality, so a vague
rubric gives you a low, noisy ceiling. Spend real effort here.

A good rubric is domain-adapted, weighted, and as objective as possible. Derive
the criteria from what would actually make *this* plan succeed or fail, not from
a generic checklist. Most strong plans, whatever the domain, are graded on some
mix of:

- **Goal clarity** — is the objective and definition of "done" unambiguous and measurable?
- **Completeness** — are the necessary steps/workstreams present, with nothing load-bearing missing?
- **Sequencing & dependencies** — is the order right; are prerequisites identified?
- **Feasibility & resourcing** — is it realistic given time, people, budget, constraints?
- **Risks & mitigations** — are the real failure modes named, with contingencies?
- **Success metrics** — are there concrete signals that tell you it's working?
- **Specificity** — is it actionable (owners, dates, concrete first step) rather than vague aspiration?

Assign each criterion a weight that reflects its importance for this task, and
state, briefly, what a low/medium/high score looks like for each. Prefer
criteria you can check against something objective (does the plan name a first
action? does every phase have an exit condition?) over purely subjective taste —
objective criteria resist gaming.

Show the rubric to the user before you start iterating if there's any ambiguity
about what "good" means for them; their priorities (speed vs. thoroughness,
risk-aversion vs. ambition) should shape the weights.

## Step 2 — Generate the initial plan

Write a genuine first attempt at the plan that addresses the task. Don't
sandbag it to make the loop look impressive — a strong starting point reaches a
higher final ceiling. Then score it against the rubric (Step 3).

## Step 3 — Score

Score the current plan from 0 to 100. Do this as a deliberate, separate pass:
go criterion by criterion, assign each a sub-score, note *why*, then combine by
the weights. Always write a one-line rationale per criterion — the rationale is
what feeds the next critique, and it's what keeps scoring honest rather than a
gut number.

Two guards against noisy scoring:

- **Require a margin to accept.** Only replace the current best if the new score
  beats it by a meaningful margin (e.g. +2 on a 100 scale), not by a fraction.
  Scoring has noise; without a margin you'll "improve" into a worse plan.
- **Re-anchor occasionally.** Every few rounds, re-read the *original* rubric
  fresh rather than drifting toward whatever the latest plan happens to do well.
  This catches reward-hacking, where revisions start optimizing for a score the
  rubric didn't really intend.

## Step 4 — Improve (critique, then rewrite)

This is the engine. Do **not** just say "make it better" and rewrite — that
produces lateral drift. Instead, in two explicit moves:

1. **Critique.** Against the rubric, list the specific weaknesses of the current
   best plan, ordered by how much they cost in score. Be concrete: "no rollback
   step for the migration", not "could be more robust". Name the lowest-scoring
   criteria and why they're low.
2. **Rewrite.** Produce a new full version of the plan that directly fixes the
   critique's top items, while preserving what already scored well. Don't
   regress strengths to chase a weakness.

### Two search strategies — pick one, switch when stuck

- **Hill-climb (default).** One critique→rewrite candidate per round. Fast and
  cheap. Use this unless told otherwise. Its weakness is local optima — small
  fixes that can't reach a fundamentally better structure.
- **Best-of-N.** When hill-climbing stalls (see plateau, Step 5) but you suspect
  the plan needs a structural rethink, generate **N** genuinely different
  candidates in one round — not minor variants, but different framings or
  architectures of the plan — score all N, and keep the best. This widens the
  search and is how you break through a ceiling that incremental edits can't.
  N=3 is a sensible default; more candidates cost more.

A good automatic policy: hill-climb until you hit a plateau, then do **one
best-of-N round** to try to escape the local optimum. If best-of-N also fails to
beat the ceiling by the margin, you've genuinely converged — stop.

If the user has access to a stronger model than the one running the loop, note
that running the *improve* and *score* steps on a stronger model is the single
biggest lever: a stronger model proposes structurally better rewrites and also
perceives flaws a weaker scorer misses, which raises the ceiling itself.

## Step 5 — Stop on plateau

Track the best score over a sliding window of the last K rounds (K=3 is
reasonable). Stop when **the best score has not improved by more than the margin
over the last K rounds** — that's the "iterations have become noise" point.
Also stop if you hit a sensible max rounds (e.g. 6–8) regardless, so the loop
always terminates. Before declaring convergence on a hill-climb plateau, try the
one best-of-N escape round described above.

## Step 6 — Output

Return:

1. **The best plan**, clean and ready to use — this is the deliverable, lead with it.
2. **Its final score** with the per-criterion breakdown.
3. **The score trajectory** (e.g. `62 → 74 → 81 → 83 → 83`) so the user sees the
   climb and the plateau.
4. **A short note on what the loop changed** — the 2–3 biggest improvements made
   from first draft to final, so the user understands *why* it's better.

Keep the process visible but concise. The user cares most about the final plan;
the trajectory and rationale are evidence that it's been genuinely hardened, not
just reformatted.

## Pitfalls to watch

- **Reward hacking the rubric.** If scores climb but the plan doesn't feel
  better, the rewrites are gaming the metric. Re-anchor on the original intent,
  and prefer objective criteria.
- **A weak rubric capping everything.** If you plateau low, suspect the rubric
  before the plan. A ceiling that feels too low often means the rubric can't see
  the dimension that matters — add or reweight a criterion.
- **Reformatting masquerading as improvement.** Bigger/prettier ≠ better.
  Improvements should change substance (a missing risk, a fixed dependency), not
  just structure. The margin guard helps; so does an honest critique.
- **Never stopping.** Respect the plateau and the max-rounds cap. Past the
  plateau you're spending effort to move noise around.
