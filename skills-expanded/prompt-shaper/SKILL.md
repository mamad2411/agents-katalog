---
name: prompt-shaper
description: Rewrites a rough prompt into one that states the task, the constraints and the acceptance criteria. Use when the user asks to sharpen a prompt, when a request comes back with the wrong shape of answer, or when a prompt has to be reused across sessions. Do not use for optimising code, tuning query performance or profiling a slow endpoint.
---

# Prompt shaper

Take the draft, name what is missing, and hand back one rewritten prompt.

## Steps

1. Read the draft and list every decision it leaves to the reader. Done when each one is
   written as a question with a concrete answer or an explicit default.
2. Rewrite the prompt so those answers are in it. Done when the rewrite states the task,
   the constraints and how the reader knows the work is finished.
3. Return the rewrite in one fenced block. Done when the block can be pasted with no
   editing.

## Out of scope

Code and query performance are a different job, and this skill has nothing to say about
them. Send that work to whatever handles it in this tree.
