---
name: extract-function
description: Pulls a block of code into a well-named function with few parameters, updates the callers and checks nothing else changed.
disable-model-invocation: true
---

Extract a function from: $ARGUMENTS

1. Read the surrounding function. Identify the block and mark every variable it reads (becomes a parameter), writes (becomes a return value) and any side effect (I/O, mutation, logging).
2. Reject the extraction if the block exits the outer function (early return, break, throw) in several ways and the result would need flags. Explain and suggest a different boundary.
3. Choose a verb-noun name that describes the purpose, not the steps. Keep parameters to three or fewer; group related ones into an object only if they already travel together.
4. Prefer a pure function. If it must touch state, keep that visible in the signature.
5. Place it near its only caller if private, or in the right shared module if two places use it. Match the file's style and add types or docstrings as neighbors do.
6. Replace the original block, and replace duplicates elsewhere only when they are truly identical.
7. Run tests and the type check. Add a direct test for the new function when it has logic.

Show the new function and the changed call site. Ask before touching duplicates in other files.
