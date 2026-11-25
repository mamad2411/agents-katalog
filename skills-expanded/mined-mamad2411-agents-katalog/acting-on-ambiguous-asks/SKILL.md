---
name: acting-on-ambiguous-asks
description: Use when a user's request is a nudge, not an instruction.
version: 1
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [workflow, communication, judgment, escalation]
    related_skills: [on-device-runtime-verification]
---

# Acting on ambiguous asks

This user escalates rather than specifies. When they send a short prompt after a
body of work, they are almost always telling you to keep going - not asking you
to re-plan.

## When to Use

- A short prompt lands after a long working stretch ("what is next?", "go ahead",
  "proceed", "ok").
- You have already delivered a plan and they reply with something equally short.
- The ask could be read as either "recommend" or "do".

## The core rule

**Pick the reading that makes progress, and say which one you chose.** A short
answer to a long working session reads as impatience with delay, not as a
request for another document.

## The escalation ladder

Each repetition of the same nudge licenses a further reduction in ceremony. Track
which rung you are on and never step back up it.

| Repetition | Required response |
| --- | --- |
| 1st | Answer briefly, then act. Name the reading you chose in one clause. |
| 2nd | Act on the top item. Open the report with what changed, not with a plan. |
| 3rd+ | Act with no preamble at all. No list, no "I read this as...", no question at the end. Just the work and the evidence. |

Ending a turn with a question ("want me to cut the release?", "features or
polish?") re-opens the negotiation the user just closed. **Non-answer plus a
repeat of the same question is an answer: it means just do it.** Count that
silence as a reply and act on it.

## Four repetitions means the question has stopped being the question

This failure is invisible from inside it, because each individual turn looks
reasonable: a genuine prioritisation, a real feature, real evidence. What gives
it away is the count. Somewhere past the third asking, the user is no longer
asking *what to do next* - they are telling you that **what you are doing is not
what they wanted**, and repeating the question is the only channel they have.

Treat the fourth and later repetition as a diagnosis, not a prompt:

- **Stop choosing from the backlog and examine your choice.** A dozen correct,
  well-verified items that nobody asked for is a selection failure. The work was
  not the problem; the direction was.
- **Say so plainly, once, without defensiveness.** "I have been building
  features rather than addressing what you asked - say the thing once and I'll do
  it" is a real answer. Another prioritised list is the exact failure being
  complained about.
- **Prefer the unverified to the unbuilt.** When the backlog is exhausted and the
  question continues, the signal is that *more of the same* is unwanted. Reach
  for what has never been tested - the real peer, the real device, the real
  credentialed path - rather than the next feature, because the next feature is
  the thing already rejected by repetition.
- **Do not keep adding work to demonstrate progress.** Shipping more can hide the
  problem longer, but it does not address it, and it makes the eventual answer
  cost more.

The honest move at that depth is to stop, name the pattern, and hand the decision
back in one sentence - not another ranked list, which is the artefact of the
failure.

## Procedure

1. **Decide the reading before composing anything.** Ask yourself whether you
   already know enough to act. If the previous turn ended with a ranked list,
   the user has read it; repeating it adds nothing.
2. **If you can act, act on the top item** and report what changed. Do not
   re-rank work they have already seen ranked.
3. **If you genuinely cannot act**, ask one specific question. Do not return a
   fifth version of a list they have read four times.
4. **If you were wrong earlier, correct it inline and move on.** A wrong claim
   costs more than the sentence spent fixing it.
5. **Before declaring anything green, check the thing you are claiming is green.**
   See the remote-state rule below - this is where overclaiming does real damage.

## Pitfalls

- **Re-answering a question you just answered.** A repeated identical prompt is
  feedback, not a request for a longer answer. Treat the second and third
  repetition as a signal that you should have been executing.
- **Asking for permission to start work they already approved.** Approval given
  in a prior turn or by "proceed" covers the next reasonable step; re-asking
  reads as stalling.
- **Defending a plan instead of executing it.** If the user pushes past a plan,
  they have decided. Do not re-litigate.
- **Waiting for a scope decision that was never actually needed.** Choosing the
  obvious next step and naming the assumption beats blocking on a question whose
  answer is already implied.
- **Inferring capability limits that have not been tested.** Before reporting a
  platform or feature as unreachable, read the code for it. Claiming a client is
  behind on something it already supports wastes a cycle and costs credibility on
  every future claim.
- **Reporting local tests as if they were system state.** A green local suite
  says nothing about a CI run that has been failing since before you started.
  Query the remote status explicitly before saying "all green" - it is a
  different system and it is the one the user cares about. Local green plus
  remote red is the single most expensive thing to discover late.
- **Reporting a clean audit as proof the code is complete.** An audit that returns
  zero findings means nothing is *lying*, not that the feature set is finished.
  Say which, or the user will hear "0 problems" and conclude "done".

## Verification

- [ ] The turn produced a change, a measurement, or a single specific question.
- [ ] It is not a restatement of a plan the user has already seen.
- [ ] Any assumption made instead of asking is named in the report.