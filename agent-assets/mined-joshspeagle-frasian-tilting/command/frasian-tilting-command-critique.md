---
description: Run the skeptic subagent on a method file or brief.
---

Run the `skeptic` subagent on `$ARGUMENTS`.

Pass the path verbatim. The skeptic will:

1. Read the method file or brief at the given path.
2. Read its companion brief / source / property test file.
3. Produce a numbered list of attack vectors with file:line refs.
4. End with `Overall: <block | accept-with-caveats | accept>`.

Do not summarise the skeptic's output — relay it. The user wants to
see every concern.

If `$ARGUMENTS` is empty, ask which file to critique (preferably a
path under `src/frasian/` or `docs/methods/`).
