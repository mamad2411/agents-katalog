---
name: reflect
version: 1.1.1
description: "Clarify a rough request with ReFLECT: Role, Format, Language, Example, Context, Task. Use for prompt engineering, an explicit ReFLECT request, or an ambiguous task the user wants clarified before execution. Ask only for material gaps, confirm the prompt, then do the work. Skip complete requests and factual questions."
---

# ReFLECT

ReFLECT is Gartner's prompt framework. It uses six prompt parts: Role, Format, Language, Example, Context, and Task. Task is required. Context and Example often decide whether the answer is grounded or generic. Role, Format, and Language tune the result when they matter.

This skill reads the user's request, maps it to those six parts, asks only for important missing pieces, and then completes the work. Do not turn prompt cleanup into paperwork. The point is to prevent the expensive mistake: a polished answer to the wrong task.

---

## The framework

| Element | Description | Priority |
| ------- | ----------- | -------- |
| Role | The persona of the AI, or the audience it writes for. | Nice to have |
| Format | Desired response structure (list, table, doc, JSON, code). | Nice to have |
| Language | Voice, tone, reading level, writing style. | Nice to have |
| Example | A short sample of the desired output shape. | Important |
| Context | The project, task background, and any private/proprietary facts the model can't know. | Important |
| Task | The specific action expected. | Must have |

Three pillars sit underneath every element: Clarity, Context, and Constraints. The prompt should stay close to the objective, include what the model needs to interpret the request, and name any hard limits.

---

## When not to run it

- The request is already complete and unambiguous. Do the work; do not interrogate.
- The user wants a quick factual answer. Answer it.
- You are mid-task and the user gives a small correction. Apply it directly.

Don't turn a 10-second ask into a questionnaire. ReFLECT is for requests substantial enough that a wrong interpretation wastes real effort.

---

## Phase 1: parse the six elements

Read the user's request and silently map what is present onto Role, Format, Language, Example, Context, and Task. Mark each part as present, inferable, or missing.

Infer before asking. Check the conversation, attached files, the repo, and relevant project instructions or saved project memory exposed by the user's workspace. Project instructions and memory are optional external context, not bundled skill dependencies; do not assume they exist or search unrelated projects. If the format is obvious from the request, such as "write a function" meaning code, do not ask. Spend about 30 seconds. A part you can reasonably infer is not missing.

---

## Phase 2: ask about real gaps

Ask only for important parts that are missing and not inferable, in this order:

1. Task. If you cannot state the expected action in one sentence, ask. Everything else is secondary.
2. Context. If the request depends on a project, dataset, audience, or private facts you do not have, ask. Name the missing context instead of guessing.
3. Example. If the output shape is not obvious, or the user seems to have a specific format in mind, ask for a short sample.

Use the `AskUserQuestion` tool when there are discrete choices to offer (e.g. format options, tone, depth), so the user can pick rather than type. Use plain prose for a single open-ended gap like a missing Task. Offer your best-guess default as a selectable option so the user can move fast.

Do not ask about Role, Format, or Language unless they affect the result. They are refinements. Too many questions make prompt cleanup feel like a chore. Ask the minimum set, then stop once the Task is clear and the important gaps are closed.

---

## Phase 3: assemble the prompt

Once the user has answered or chosen, compose the completed prompt from the filled elements. Apply the technique that fits the task:

- Zero-shot: direct instruction, no example. Use this for clear tasks.
- Few-shot: include the user's examples to lock the output pattern.
- Chain of thought: request explicit reasoning when the task needs multi-step logic.
- Prompt chaining: split stable workflows into ordered steps.
- Prompt orchestration: use multiple chains with branching logic for variable workflows or external interactions.

Echo the assembled prompt back to the user in a short block covering the six resolved parts, so they can confirm or correct it before it runs. Keep it tight. This is a confirmation, not a report.

---

## Phase 4: execute

Run the completed prompt and produce the deliverable. Do not stop after writing the prompt. Carry it through to the result the user wanted.

---

## Phase 5: evaluate when stakes justify it

For high-stakes or repeated output, score the draft before delivering it. Judge it against the resolved Task, Context, and Constraints, not against your own taste.

Score each metric from 1 to 5:

| Metric | 1 (fail) | 3 (borderline) | 5 (pass) |
| ------ | -------- | -------------- | -------- |
| Relevance | Misses the query | Partly on target, some drift | Directly answers the Task |
| Accuracy / faithfulness | Contains hallucination or unsupported claims | Mostly supported, one weak claim | Every claim traces to a source |
| Completeness | Misses major parts of the Task | Covers the core, misses an edge | Covers the whole Task |
| Groundedness | Fabricates beyond provided Context | Mixes grounded and invented detail | Uses only provided Context |
| Instruction following | Ignores Format, Language, or Constraints | Follows most, breaks one | Follows every constraint |
| Safety | Harmful or offensive content | Borderline or needs a caveat | Clean |
| Verbosity | Padded or truncated | Slightly long or terse | Concise and complete |

Pass only when Accuracy/Faithfulness is at least 4, Safety is 5, and no metric is below 3. Anything else fails.

Map the scorecard to a decision:

- Accept: threshold met.
- Regenerate: Relevance, Completeness, Instruction following, or Verbosity is below 3. Tighten the ReFLECT parts and rerun.
- Retrieve more context: Groundedness or Accuracy is below 4 because the model lacked information.
- Escalate to the user: scores conflict, the Task is ambiguous, or judgment is subjective.
- Block: Safety is below 5.

Calibrate the scoring. These anchors only help if the scores match a human review. When the skill is used repeatedly for the same kind of output, compare a few results against the user's rating and adjust. For everyday one-off tasks, a light pass is enough. Save the full scorecard for work that ships, repeats at scale, or carries real consequences.

---

## Operating notes

- Task is non-negotiable. Never proceed past Phase 2 without a one-sentence Task you could repeat back.
- Infer aggressively, ask sparingly. The skill's value is catching the *real* gap, not generating a form.
- Name what the model can't know. Knowledge recency and private data are common blind spots. Surface them as Context requests.
- Echo before you execute. A 5-line confirmation of the resolved elements costs little and prevents building on a misread.
- Carry through to the deliverable. The prompt is the means; the answer is the end.

---

*Source: ReFLECT is Gartner's framework. The element priority, prompt-management guidance, modular prompting practices, and evaluation model follow Gartner's prompt-engineering guidance.*
