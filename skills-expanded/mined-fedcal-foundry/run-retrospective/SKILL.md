---
name: run-retrospective
description: Facilitate a retrospective that ends with one owned, dated change instead of a list of observations — evidence gathered from the board before opinions are collected, a format chosen for the situation rather than by habit, blameless framing that attacks the system, and a check that last cycle's action actually happened. Use at the end of a Sprint or iteration, after a painful delivery, or when the same complaint keeps returning. Not for production incident postmortems, not for evaluating people, and not for deciding scope.
argument-hint: "[--format timeline|starfish|5whys|sailboat] [--check-previous] [--dry-run]"
user-invocable: true
agent: foundry-pmo:scrum-facilitator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "tracker-item.v1 + team input -> review.v1 with one owned action"
license: Apache-2.0
---

# Run retrospective

A retrospective succeeds when something changes. Insight without an owner is entertainment, and a
team that produces insight without change learns, correctly, that the meeting does not matter.

The output of this skill is **one** improvement with a name and a date. Not five. One that
happens beats five that are listed.

## Step 0 — Check the previous action first

Always start here. `--check-previous` is implied, never optional.

Read the prior `review.v1` from `.foundry/blackboard/`. State plainly whether last cycle's action
was done, partly done, or not started. If it was not started, that is the first topic of this
retrospective and it outranks anything new — a team that repeatedly fails to execute its own
improvements has a capacity or authority problem, and generating a sixth action is avoidance.

## Step 1 — Bring evidence before opinion

Collect facts from the board before anyone speaks, so the discussion argues with data rather than
with whoever remembers most vividly. From `tracker-item.v1` via `foundry-pmo:tracker-operator`:

- items completed, cancelled and returned;
- cycle time p50 and p85 this cycle against the previous three;
- items that aged past p85, by name;
- blocked days and where the blocks originated;
- scope added after the cycle started.

Recency bias is the default failure of an unprepared retrospective: the last two days dominate a
two-week window. A timeline of what actually happened, posted before the conversation, is the
cheapest correction available.

## Step 2 — Choose the format for the situation

Rotating formats for novelty is fine. Choosing one that fits is better.

| Situation | Format | Why |
|---|---|---|
| Ordinary cycle, no crisis | `starfish` — start, stop, continue, more, less | fast, low ceremony |
| Something went visibly wrong | `timeline` — reconstruct events, then mark surprises | separates what happened from how it felt |
| The same problem keeps returning | `5whys` on that one problem | the recurrence is the signal; stop generating breadth |
| Team is disengaged or the meeting has gone stale | `sailboat` — wind, anchors, rocks, destination | metaphor lowers the cost of naming an anchor |
| Trust is low or the topic is charged | `timeline`, facts only, no interpretation round | interpretation is where blame enters |

Refuse to run a generative retrospective when the team already knows the problem and has said so
twice. Go straight to `5whys` on it.

## Step 3 — Blameless framing

Blameless does not mean consequence-free or vague. It means the object of analysis is the system
that let a person's reasonable action produce a bad outcome.

Rewrite as you go:

| Said | Recorded |
|---|---|
| "X broke the build" | "a change reached main without the test that would have caught it" |
| "we were sloppy about reviews" | "review latency p85 was 3.2 days; there is no WIP limit on the review column" |
| "QA was a bottleneck" | "one person holds sign-off for six streams" |

Two rules that hold the frame:

- **Ask what made the action reasonable at the time.** Everyone acted on the information they
  had. If the action looks stupid in hindsight, the information available was wrong or missing,
  and that is the finding.
- **No names in `review.v1` except as action owners.** An owner is an accountability; a name in a
  cause statement is an accusation.

If a manager is in the room and the team has less power than the manager, say so and offer to run
it without them. Psychological safety is not a value statement here, it is a precondition for the
data being real.

## Step 4 — Converge to one action

Cluster, vote, then cut hard. The action must satisfy all four:

1. **Owned by a name**, not by "the team" — collective ownership is the reliable way for nothing
   to happen.
2. **Dated**, and the date is inside the next cycle. An action due "eventually" is a wish.
3. **Within the team's authority.** If it requires a decision the team cannot make, the action is
   not the fix — the action is escalating it, with a named recipient. Record the underlying item
   as `risk.v1` for `foundry-pmo:risk-manager`.
4. **Observable.** Somebody outside the room could tell whether it happened.

Then write it where the work is: a tracked item in the next cycle via
`foundry-pmo:tracker-operator`, not a line in a document nobody reopens. An improvement that is
not on the board competes with the board and loses.

## Step 5 — Emit `review.v1`

Written to `.foundry/blackboard/<wave>/retrospective.json`, containing the evidence gathered, the
themes raised, the previous action's status, and the single committed action with owner and date.
`summary` ≤ 300 tokens.

## Anti-patterns this skill refuses

- **Producing a list of five actions.** Cut to one. Record the rest as observations, unowned and
  explicitly not committed, so nobody believes they were promised.
- **Repeating the same theme cycle after cycle with no action.** After the second repetition, stop
  discussing and escalate it as a `risk.v1`. Continued discussion is how a team performs
  concern instead of resolving it.
- **Using the retrospective for a production incident.** An incident needs a timeline, a
  contributing-factors analysis and its own postmortem; folding it into team process buries it.
  Route it to `foundry-quality:sre-planner`.
- **Turning it into a status meeting.** Status is the Review's job.
- **Skipping it when the cycle went well.** A good cycle is the cheapest opportunity to learn what
  to keep, and the only time the discussion is not defensive.

## Degradation

- **No tracker data.** Run on team recollection, label the evidence section `self-reported`, and
  make "get the board readable" a candidate action.
- **`superpowers` present.** Its blameless-analysis and verification discipline take precedence;
  invoke rather than duplicate.
- **Remote or asynchronous team.** Collect input in writing before the call, anonymously where
  trust is low, and timebox the live portion to convergence only.

## Progressive disclosure

- `references/formats.md` — the four formats step by step, with facilitation scripts.
- `references/blameless.md` — rewriting accusations into system statements, worked examples.
- `references/action-quality.md` — the four tests, and how each one fails in practice.
