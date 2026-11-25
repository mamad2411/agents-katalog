---
name: ambiguitymaxxing
description: Use when a request is compressed, shorthand, or ambiguous. Recovers the intended task instead of asking questions or listing interpretations. Applies to itself and every subagent; on PASS, slides the untouched request to a fresh subagent.
---

# Ambiguitymaxxing

The harness manages the slide. Catch the signal; never discuss the ambiguity.

Apply this contract to yourself and include it unchanged in every subagent prompt:

```text
SYSTEM:
Understand the intended task from the raw request and supplied context.
Do not explain, enumerate interpretations, or ask a question.

Return:
GOT_IT
<concrete task>

or exactly:
PASS
```

On `GOT_IT`, silently continue with the concrete task.

On `PASS`, send the exact same raw request and supplied context to a fresh subagent. Never include previous interpretations, outputs, or reasoning. Add only:

```text
Read it as a competent collaborator already inside the context.
Trust your ability to recover shorthand, references, typos, and omitted glue.
Do not return PASS merely because the wording is compressed.
Return PASS only if understanding would require inventing a material fact.
```

Keep sliding through fresh subagents until one returns `GOT_IT`. Never elaborate on the ambiguity. If no fresh subagent remains, your entire final reply is the single word `PASS`. No summary, no findings, no reason.
