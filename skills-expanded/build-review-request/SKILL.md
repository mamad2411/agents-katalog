---
name: build-review-request
description: Writes an Engineering Review Request with the one question you need an engineer to answer, a plain list of what you are not asking, a thirty-minute walk-through plan, the three places you most suspect a problem and what you will do with each answer. Use for "run build-review-request", "ask an engineer to look at my prototype", "my prototype is stuck in review", "write a review request", "how do I get engineering feedback on a prototype", "plan a walk-through with an engineer", "what should I ask engineering", "nobody has reviewed my prototype", part of the Claude for Product Builders Pack by 90n.
---

# Engineering Review Request

## When To Use
Your prototype has sat in someone's review queue for two weeks and you never said what you wanted from them. "Have a look when you can" is not a request. This skill answers: what one thing do you need an engineer to judge, and how do you make it a half hour instead of an open-ended favour?

## When Not To Use
If engineers do not yet have a note that says what exists and how to open it, run Engineering Handover Note first: this request points at it. If you are stuck on one error while building, run Error Fix Log. If the question is for leaders, not engineers, run Prototype Demo Script.

## Inputs
- The handover note and the prototype vs production note, or what you have of them.
- What you want to know, in your own words, however vague.
- The parts of the prototype you trust least.
If you have none of this, I start from a one-line description of the prototype and mark the output as a first draft.

## Approach
Google's Engineering Practices (https://google.github.io/eng-practices/review/developer/small-cls.html) explain why small, well-described review requests work: they are reviewed faster and more thoroughly, and a reviewer often lacks the author's context. A prototype is one big change by nature, so asking for a code review of all of it asks for the thing that practice warns against. This skill turns the request into one question and a walk-through. The failure it prevents: a link, no question, and silence that you read as a verdict.

## Workflow
1. Ask at most three questions: what do you need to know before the next decision; which engineering role can answer it; what are you afraid they will find?
2. Write one question that can be answered in the session, such as "could this flow be built on what we have" or "is anything here unsafe to show testers". If it holds two questions, keep the one the next decision depends on.
3. Write the not-asking list in plain words: not a merge, not a rewrite, not an estimate, not a date. It is what lets a busy engineer say yes.
4. Attach what the reviewer needs, so nothing has to be hunted for: the handover note and the gap note, with the two pages to read first named.
5. Name the three places you most suspect a problem and why. Three, not ten. Your suspicion is context the reviewer does not have.
6. Plan the thirty minutes in timed parts: the question, the flow on screen, the three suspect places, the engineer's answer. You set the split. Keep the last part for them.
7. Write what you will do with each possible answer before the session, so a "no" changes your plan instead of starting an argument. Then draft the short message that carries all of it.

## Output Format
```markdown
# Engineering Review Request
**Prototype:** [name] | **To:** [engineering role] | **Time asked:** thirty minutes, at a time you choose
**The one question:** [one question, answerable in the session]
**What I am not asking:** a merge, a rewrite, an estimate, a date.
**Attached:** the handover note and the gap note. **Read first:** [page or section] and [page or section].
## Where I suspect a problem
| Place | What I suspect | Why |
|---|---|---|
| [screen or part] | [suspicion] | [what I saw] |
## Walk-through plan
| Part | Minutes | Who leads |
|---|---|---|
| The question | [min] | Builder |
| The flow on screen | [min] | Builder |
| The three suspect places | [min] | Builder, then engineer |
| The engineer's answer | [min] | Engineer |
## What I will do with the answer
- If yes: [action]. If no: [action]. If it depends on [x]: [action].
## Message to send
[Three or four sentences: the question, the time asked, what is attached, what is not being asked]
## Decision
[Engineer, by role] gives a judgement on the one question in the session. [Builder, by role] acts on it as written above by [date the builder sets for their own action].
```

## Done When
- There is one question and it can be answered in a half hour.
- The not-asking list names a merge, a rewrite, an estimate and a date.
- Three suspect places are named, each with a reason, and every possible answer has an action written before the session.

## Quality Bar
- The request is about the prototype. It makes no comment on anyone's queue, workload or speed of reply.
- The message fits on one screen, with the notes attached, not pasted in. A safety question ends with: check with your engineering or security lead.
- The only date in the request is for the builder's own next action.
- The request asks for a judgement, never for a merge or a date; engineers own what ships.

## Next
Run build-learning-card (Prototype Learning Card) to set what you learned, including the engineer's answer, against the pass line.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
