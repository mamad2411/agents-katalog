---
name: receiving-review
description: "Call when review findings arrive — from code-reviewer, DeepSeek, CI or the owner. Trigger words (RU+EN): замечания, находки, ревьюер пишет, посмотри что нашли, поправь по ревью, вот отчёт ревью / remarks, findings, the reviewer says, look at what was found, fix per review, here is the review report. A technical check of each item, not a show of agreement: verify before adopting, ask before assuming, one item at a time. Boundary: code-reviewer finds the findings; this skill receives them."
---

# Receiving a code review

A review calls for a technical judgment, not an emotional reaction.

**Core: verify before adopting. Ask before assuming. Technical correctness over social comfort.**

## Response pattern

```
On receiving a review finding:
1. READ — in full, without reacting
2. UNDERSTAND — restate the requirement in your own words (or ask)
3. VERIFY — check against the reality of the code/DB, not against memory
4. JUDGE — technically correct FOR THIS project?
5. ANSWER — a technical confirmation OR a reasoned pushback
6. ADOPT — one item at a time, each verified
```

## Forbidden responses

**NEVER:**
- "You're absolutely right!" / "Great catch!" / "Well spotted!" — performative agreement.
- "Adopting now" — before verifying.

**INSTEAD:**
- restate the technical requirement in your own words;
- ask a clarifying question;
- push back with a technical rationale, if the finding is wrong — on a dangerous topic, with
  evidence (below);
- simply start working (actions over words).

This rests on a rule we already hold: **re-verify someone else's findings by running, do not take
them on faith.** A reviewer's finding is a hypothesis until confirmed by the code/DB. A reviewer can
be wrong too.

## An unclear finding → STOP

```
If even one item is unclear:
  STOP — adopt NOTHING yet
  ask for clarification on the unclear items
```

Reason: the items may be linked. Partial understanding = a wrong implementation.

```
Reviewer: "fix 1–6". Clear 1,2,3,6. Unclear 4,5.
❌ adopt 1,2,3,6 now, ask about 4,5 later
✅ "Understood 1,2,3,6. On 4 and 5 I need clarification before continuing."
```

## The finding's source

- **From the owner** — trusted; adopt after understanding; still ask if the scope is unclear; no
  performative agreement; straight to work.
- **From an external reviewer (DeepSeek etc.)** — verify first: technically correct FOR THIS
  project? Documentation may have rotted, the reviewer may not have known the context. Confirm by
  the code, then adopt.

## Severity levels

Critical → fix immediately. Important → before continuing. Minor → note for later. Disagree →
push back with a rationale, not silent ignoring or silent submission.

## A finding on a dangerous topic is rejected only with evidence

Eight topics where a finding waved away costs the most: data loss, access and permissions,
secrets, injection, a public contract (an API, a file format or a command that other code relies
on), concurrency, memory, cryptography.

On these topics a rationale is not enough. The finding is rejected only with one of:
- a `file:line` that shows the case is handled;
- the documentation of the exact version in use;
- the short hash of a commit that already closes it;
- a test that runs exactly the finding's scenario and passes.

No such evidence — the finding is **unresolved**, not rejected: it stays open in the reply and in
the task, where the merge gate sees it. "This cannot happen" is not evidence.

## A finding about a criterion is not removed by editing the criterion

A separate case that looks like compliance rather than pushback: the reviewer says "this criterion
cannot be checked", and the criterion is rewritten so the remark no longer applies to it. The
finding is removed, the cause remains, and the work it questioned reaches the merge intact.

The discriminator is one question: **what changed in the CODE after the criterion was edited?**
Nothing changed — the remark is not removed but hidden.

There are two legitimate exits:

1. the criterion becomes checkable: a failing test is written against it, and then the rewording is
   genuine;
2. the fork goes to the owner together with its cost in the code — "the criterion requires what the
   mockup does not have: drop the block or keep it and complete the statement". This is the very
   "not for product decisions" case from the boundaries below; rewording a criterion is NOT a fork,
   because it asks nothing.

A fork leaves a trace in the marker form from [[task-cycle]] — `[CLARIFY: …; default: …]` — in the
task body. Without it, the second exit is indistinguishable from the first after the fact.

**The trace is mandatory, and it is in a comment.** The previous wording of the criterion does not
vanish from the tracker: the body's version history lives in its web handle and returns a diff, even
though there is no event for a body edit in the task's event list — so the edit is invisible in the
feed yet recoverable via the handle. Relying on the handle alone is still not safe: not every tool
reads it and not every tracker has it. So the finding and the response to it live in a comment, and
the criterion edit names in it what changed in the code; the merge gate at such a finding also looks
at the body diff.

Machine-visible are "the criterion was edited after a finding" and "what exactly changed in it" —
that is the same diff. Machine-INVISIBLE is the only thing that decides here: whether this is an
honest clarification of the statement or a removal of the remark. So there is no gate step for the
rule: it cannot tell an honest edit from a sham one, and reddening on every criterion edit means
reddening on normal work. The rule is held by the review, the merge gate and the trace in the
comment.

## When NOT to apply

- **Not for findings you invented yourself.** This is the technique of RECEIVING someone else's
  finding. Your own hypothesis is verified by the [[diagnosing]] loop, not analyzed by this pattern.
- **Not for product decisions.** A review judges technical correctness; "whether to do this at all"
  is a question for the owner, and severity levels do not settle it.
- **Not where the finding is already confirmed by a red run.** Verifying the proven is stalling:
  fix it.
- **Not as a way to deflect.** Pushback with a rationale is part of the technique; pushback without
  one is exactly what it is written against.

Related: [[task-cycle]] (review is a cycle step; the fork-marker form is there too), [[diagnosing]]
(verifying a finding through the loop).
