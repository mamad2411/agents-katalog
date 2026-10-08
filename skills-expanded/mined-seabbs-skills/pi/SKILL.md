---
name: pi
description: Delegate a self-contained task to pi (cheap local AI coding agent) and report back.
argument-hint: [task-description]
disable-model-invocation: true
---

Delegate the task to pi:

```bash
pi -p "$ARGUMENTS" --print --no-session 2>&1
```

Pi runs from cold context in the current directory. Its stdout is captured in
the bash result — read it, verify it, and report back to the user.

For code tasks, pi can write files directly. Check the files it created or
modified rather than trusting inline snippets.

If the command fails (non-zero exit, timeout, empty output), show stderr and
offer to retry with a more specific prompt. If it keeps failing, do the task in
Claude instead.