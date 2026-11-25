---
name: remove-console-logs
description: Finds and removes leftover debug logging and prints while keeping the intentional logger calls and CLI output.
disable-model-invocation: true
---

Remove leftover debug output in: $ARGUMENTS (whole project if empty).

1. Search for debug output by language: console.log, console.debug, debugger, print(, pprint, var_dump, dd(, puts, fmt.Println, System.out.println, println!, dbg!, and commented-out copies. Skip node_modules, vendor and build folders.
2. Classify each hit. **Remove:** bare prints of variables, "here" or "test" markers, dumps of objects, commented-out logging. **Keep:** calls to the project's logger, output in files whose purpose is to print (CLI scripts, build tools), deliberate console.error in a catch, and test helpers.
3. Flag any hit that logs a token, password, email or full request body as a leak, even if you keep it.
4. Do not delete a line that has side effects inside the call, such as `console.log(i++)`; mention it instead.
5. Remove the confirmed ones, tidy now-unused imports and variables, then run the linter and tests.

First show a table of hits with file, line, the decision and the reason. Apply only after I say go. Finish with counts removed, kept and flagged.
