---
name: debug-fix
description: Find the cause of an error or wrong behavior in this app before changing code. Use when something throws, fails to build, or does not do what the user expected.
---

# Debugging

The failure mode to avoid is guessing: changing a line that looks related, seeing a
different error, and changing another. On a small context window that loop will fill
the window before it finds anything. Read first.

## Order of Work

1. **Read the actual error.** The stack frame naming a file in `src/` is the one that
   matters, not the framework frames above it.
2. **Read that file** before forming a theory. Not the file you assume is at fault.
3. **State the cause in one sentence** before you edit anything. If you cannot, you do
   not have it yet — keep reading.
4. **Make one change.**
5. **Verify it**, with the command below.
6. If the error changed but did not go away, go back to step 1 with the new one.

## Verifying

Read `package.json` for the app's real scripts — they differ by template — and run the
build or typecheck through `bash`. A type error is the cheapest bug to find; find them
all before running anything.

The dev server's output is in the Terminal panel, which the user can see and you
cannot. If the answer is likely in there, ask them what it says rather than guessing.

## Common Causes

- **The import path is wrong**, not the code. Check the file actually exists with `ls`.
- **The package is not installed.** Read `package.json`. If it is missing, add it and
  run `install_deps` — not `bash bun install`.
- **The API changed.** If you are calling a library and the error says a function is
  not a function, look it up with `web_fetch` before assuming your call is right.
- **The state is stale**, not wrong. A value read once at startup will not reflect a
  later change.

## When a Fix Makes It Worse

Stop editing. `get_history`, find the commit before you started, and `rollback`. Then
say what you learned. Two failed fixes on top of each other are much harder to unpick
than one clean revert.
