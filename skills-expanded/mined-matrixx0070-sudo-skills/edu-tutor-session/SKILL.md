---
name: edu-tutor-session
version: 1.0.0
description: Run a Socratic tutoring session that diagnoses gaps and adapts questioning to the learner in real time.
author: matrixx0070
tags: [education, tutoring, socratic, adaptive, questioning]
capabilities: []
---

## When to use

Use this to guide a learner to an answer through questions rather than telling them — a live, adaptive dialogue that surfaces their thinking, targets the actual gap, and adjusts difficulty as they respond. Best for building reasoning and durable understanding.

**Not for:** a one-shot explanation (use edu-explainer), a static lesson plan (use edu-lesson-plan), or when the learner explicitly just needs a fast factual answer.

## Method

1. Diagnose first. Ask what they're trying to do and where they're stuck; have them show their current thinking before you steer. Decision point: if the gap is a missing fact they can't derive, teach it directly, then return to questioning.
2. Set the target. Pick one specific sub-goal for this exchange, not the whole topic.
3. Ask, don't tell. Pose one question that moves them one step forward. Prefer questions that expose reasoning ("why did you pick that?") over yes/no.
4. Adapt to the response. Correct → raise difficulty or extend. Partial → probe the shaky part. Wrong → don't correct outright; ask a question that reveals the contradiction. Decision point: after ~2 failed hints on the same step, give a worked micro-example, then resume.
5. Make them articulate. Have the learner restate the idea in their own words before moving on.
6. Close the loop. End with a recap in their words plus one transfer question applying it to a new case.

## Example

Learner: "Why is my loop infinite?" You: "Walk me through what changes each time it runs." Learner: "Nothing — oh, i never increases." Rather than confirming, you ask: "What has to be true for a while-loop to stop?" Learner: "The condition becomes false." You: "So what would make i < 10 become false?" Learner adds i++. You raise difficulty: "What if the step were i += 3 — would it still terminate?" Recap in their words + transfer to a countdown loop.

## Pitfalls

- Giving the answer at the first sign of struggle, so the learner never builds reasoning.
- Asking vague "does that make sense?" checks instead of questions that reveal thinking.
- Stacking multiple questions at once, overwhelming instead of guiding one step.
- Never escalating out of Socratic mode even after repeated failure — hint fatigue; drop to a worked example.

## Output format

```
Session goal: <what the learner wants> | Level: <...>

Turn-by-turn:
- Diagnose: <opening question + learner's shown thinking>
- Q1 → (learner response) → adapt: <correct/partial/wrong branch>
- Q2 → ...
- [Fallback used?]: worked micro-example when stuck

Learner's own-words recap: <...>
Transfer question (new case): <...>
Next step / what to practice: <...>
```
