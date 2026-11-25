---
name: explain-code
description: "Explains a file or function to a newcomer: purpose, a step-by-step walk-through with a worked example, and the gotchas."
disable-model-invocation: true
---

Explain this code to a developer who is new to the project: $ARGUMENTS

1. Locate the target. For a function name, search for its definition. Read the whole function, then its callers and the types it uses. If the name matches several places, list them and ask which one.
2. Start with one sentence: what problem this code solves and who calls it.
3. Walk through it in execution order. Pick a small concrete input and show how values change at each step, quoting the lines with `file:line`.
4. Call out the non-obvious: hidden state, side effects, error paths, performance cost, and assumptions the callers must keep.
5. Finish with "Where to look next": two or three related files or functions.

Rules: explain what the code does, not what you wish it did. Mark guesses with "I infer". Do not edit anything and do not suggest refactors unless asked. Keep it under 400 words.
