---
name: debug-error
description: Finds the root cause of an error message or stack trace in your code, shows the evidence and proposes a minimal fix.
disable-model-invocation: true
---

Debug this error: $ARGUMENTS

1. Read the message and trace. Ignore framework and library frames; find the first frame inside this repository and open that file around the line.
2. Search the repo for the exact message text to see where it is raised, and check recent changes to those files with `git log -n 5 --oneline -- <file>`.
3. Write down two or three hypotheses ranked by likelihood. For each, name a quick check: print a value, read a config, run a failing test, query a log.
4. Run the cheapest checks. Do not change code to test a theory unless you can revert it at once.
5. Identify the root cause. Distinguish the line that crashed from the line that put bad data in place.
6. Propose the smallest fix and a test that would have caught it.

Report: **Cause** (one sentence), **Evidence** (file:line and what you saw), **Fix** (diff), **Test**. If you cannot reproduce or confirm the cause, say which information is missing instead of guessing. Ask "Apply this fix?" before editing.
