---
name: loop-review
description: Adversarial review loop. Use when an implementation is ready for review before merge — dispatch a fresh-context reviewer on the diff and criteria, gate on verdicts, and iterate fixes until no blockers remain.
---

# Review Loop

A model reviewing its own work in the same context inherits every assumption that
produced the bug. This loop gets an *independent* verdict: a fresh-context reviewer
that sees only the diff and the acceptance criteria, with verdict gates that drive fix
iterations until the work is clean.

## When to reach for this

- An implementation is complete and about to be merged or handed off
- The change is risky enough that self-review isn't sufficient
- A fix round has finished and the fixes themselves need review
- Multiple workers' output needs an integration-quality gate (`loop-parallel`)

## Iron law

**The reviewer never grades its own work.** Fresh context, the diff, the task
statement, the acceptance criteria — and nothing else. No implementation narration, no
"I chose this approach because": that is anchoring, and an anchored reviewer approves.

## The loop

1. **Package the review input**: the diff, the task statement, the acceptance
   criteria, and how to run the checks. Exclude the conversation that produced the code.
2. **Dispatch a fresh-context reviewer** (a subagent, or the `pr-code-reviewer` agent
   for a full-dimension pass) scoped to **correctness first** — does the diff do what
   the task claims, and what breaks?
3. **Collect verdicts** using the shared labels from `code-review-checklist`:
   `[BLOCKER]` / `[CONCERN]` / `[NIT]` / `[QUESTION]`, ending in a verdict.
4. **Fix blockers**, re-running the real checks after each fix (`loop-verify`).
5. **Re-review the fix diff only** — a fresh dispatch, not a continuation of the
   reviewer's context.
6. **Exit** when a pass reports zero blockers and every concern is either fixed or
   explicitly deferred with a written reason.

## Loop guards

- **Scope creep guard.** An open-ended reviewer always finds "gaps", and each round of
  appeasement adds defensive code. Scope reviews to correctness (plus the dimensions
  the change actually touches); style rounds are separate and optional.
- **Iteration cap.** Two full review→fix rounds; a third disagreement is a design
  question for the human, not another round.
- **Severity honesty.** Re-labeling a correctness bug `[NIT]` to exit the loop is
  gaming the gate.

## Rationalizations

| Excuse | Reality |
|---|---|
| "I just wrote it, I know it's right" | The author's context is the one context guaranteed to share the bug's assumptions |
| "Explaining my approach helps the reviewer" | It anchors the reviewer to the author's framing — send the diff, not the story |
| "The concern is theoretical" | Then defer it *in writing* with the reason; silent dismissal is how theoretical becomes production |
| "One more fix round will satisfy it" | Past two rounds the loop is diverging — escalate |

## Pitfalls

- Reviewing in the same context that wrote the code (the whole loop's point is lost)
- Feeding the reviewer the full session transcript "for context"
- Fixing blockers without re-running the checks, then re-reviewing stale claims
- Letting the reviewer's suggestions expand the diff beyond the task's scope

---
*Related: `code-review-checklist` (dimensions and severity labels), `loop-verify`
(evidence for each fix), `loop-parallel` (reviewing integrated parallel work) · full
review pass: the `pr-code-reviewer` agent · output/ADR format: `playbook-conventions`*
