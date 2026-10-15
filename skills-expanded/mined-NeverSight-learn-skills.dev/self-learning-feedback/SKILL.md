---
name: self-learning-feedback
description: Asks for user feedback after each task or cron job completion and runs a recursive learning flow. If output is good, asks what was good until 10 approvals; if needs improvement, asks why/how/what via multiple choice plus optional examples, uses web search and iterative thinking to resolve, and caps iterations by severity (slight 5, medium 10, severe 20). Keeps feedback non-intrusive. Use when completing discrete tasks or cron jobs for the user.
---

# Self-Learning Feedback

## Purpose

Use this skill to create recursive learning after each completed task or cron job without disrupting user flow.

## Defaults

- `GOOD_APPROVAL_TARGET = 10`
- `SLIGHT_MAX_ITERATIONS = 5`
- `MEDIUM_MAX_ITERATIONS = 10`
- `SEVERE_MAX_ITERATIONS = 20`

If the user explicitly asks for a different threshold (for example 20 good approvals), update only `GOOD_APPROVAL_TARGET`.

## When To Trigger

Trigger after a clear completion point:

- A discrete task was completed.
- A cron job execution and response was completed.

Identify **task type/context** from the request (e.g. cron job name, report type, command, or goal) so that good-approval counters and issue signatures can be scoped correctly.

Do not trigger:

- Mid-task.
- During a multi-step process before a natural completion point.
- More than once for the same completion event.

## Non-Intrusive Feedback Prompt

After completion, send one short feedback prompt:

`Task completed. Was this good or does it need improvement?`

Keep prompt length to 1-3 lines.

## Feedback Branches

### Branch A: User says "Good"

1. In the **same turn**, ask: `What was good about this output?`
2. Capture the user's positive signal (quality, format, style, speed, clarity, etc.).
3. Increment the **consecutive** good-approval counter for this **task type/context** (e.g. same cron job, same report type, same command). If the user had said "Needs improvement" on a previous task, the counter for that context was already reset—only consecutive "good" answers count toward the target.
4. Repeat this learning behavior on every future completion of the same task type until the counter reaches `GOOD_APPROVAL_TARGET`.
5. Once target is reached, treat pattern as learned and reduce prompt frequency:
   - Ask "what was good" only when task type changes, quality drops, or periodic recalibration is needed.
6. **Counter reset**: If the user says "Needs improvement" for this task type/context, reset the good-approval counter to 0 for that context so that the next "good" answers start a new consecutive run toward the target.

### Branch B: User says "Needs improvement"

Run a structured learning loop using multiple-choice questions first, then free-text refinement.

1. Collect improvement intent in three dimensions:
   - Why it needs improvement.
   - How it should be improved.
   - What context/styling should change.
2. Ask for examples if possible.
3. Classify severity and set iteration cap.
4. Resolve with web research and iterative reasoning.
5. Apply changes in the next similar output.
6. Ask feedback again after completion.

## Multiple-Choice Collection Template

Use `AskQuestion` when available.

### Why It Needs Improvement

Options:

- Incorrect or incomplete result
- Wrong format or structure
- Too slow or inefficient
- Wrong tone or style
- Missing context or assumptions
- Other (user specifies)

### How It Should Improve

Options:

- More detail/depth
- Less detail/more concise
- Different structure/order
- Different method/tooling
- Stronger validation or checks
- Other (user specifies)

### What Context/Styling Should Improve

Options:

- Code style/conventions
- Output format (markdown, JSON, table, prose)
- Terminology/domain language
- Length/scope boundaries
- Audience/tone expectations
- Other (user specifies)

Then ask:

`If you can share an example of the desired output/style, please provide one.`

## Severity Metric And Iteration Control

Classify the issue from the user's why/how/what (or ask briefly if unclear):

- Slight: minor wording/format/style adjustments -> max 5 iterations
- Medium: structural/depth/method changes -> max 10 iterations
- Severe: fundamental or repeated failures -> max 20 iterations

Track learning loops per **issue signature** (`why + how + what + context`). One **iteration** = one full cycle: apply the learning → deliver revised output → ask "Good or needs improvement?" again. If the user then says "Good," that improvement issue is closed (and the good-approval path applies for that task). If they say "Needs improvement" again for the same issue, that counts as the next iteration.

- If under cap: continue iterative refinement (apply → ask feedback again).
- If cap reached: summarize lessons learned, stop iterating on that issue, and continue normal feedback prompts (still ask "Good or needs improvement?" after subsequent tasks).

## Why-How-What Resolution Requirement

When implementing improvements, always state:

- Why this change is needed.
- How it will be changed (concrete steps).
- What context/styling constraints are being applied.

Use web search when external references improve correctness. Use iterative thinking to test and refine assumptions before final output.

## UX Safety Rules

- Never spam feedback prompts.
- Never interrupt active user workflows for feedback.
- Keep prompts concise and predictable.
- Do not require UI or product changes; this is a conversational behavior layer.

## Lightweight Output Pattern

After task completion:

1. Completion line.
2. Single feedback question.
3. Optional one follow-up block only if user chooses "Needs improvement."

## Additional Resources

- Detailed question sets and example forms: [reference.md](reference.md)
