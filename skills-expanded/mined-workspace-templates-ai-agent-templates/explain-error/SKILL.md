---
name: explain-error
description: Explains an error message or stack trace in plain words, points to the line most likely at fault and suggests what to check first.
disable-model-invocation: true
---

Explain this error: $ARGUMENTS (paste the message or stack trace; if empty, ask for it).

1. Identify the language, runtime and tool from the trace format. Quote the exact error message and its type once.
2. Say in two plain sentences what the error means, without jargon. Explain any technical term you must keep.
3. Walk the stack from the bottom of your own code. Skip frames from libraries and the framework unless the fault is inside them. Open the files and lines from the trace in this repository and read the code around each one.
4. Name the most likely cause and a second one, and say how sure you are for each. State which variable, value or call looks wrong and why.
5. Give a short sequence of checks the user can run to confirm: a log line to add, a command to run, a value to print. Prefer checks that take under a minute.
6. If the error comes from the environment (missing package, wrong version, permissions), say so and give the exact command that checks it.

Do not edit any files. End by asking whether to apply the most likely fix, and show it as a diff first.
