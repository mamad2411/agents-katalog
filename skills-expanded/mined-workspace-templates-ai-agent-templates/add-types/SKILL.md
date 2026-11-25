---
name: add-types
description: Adds precise type annotations to one file and fixes the checker errors that show up, without leaning on any or ignores.
disable-model-invocation: true
---

Add precise types to: $ARGUMENTS

1. Identify the language and the checker already configured (tsconfig.json, mypy.ini, pyproject.toml, pyright). Run it once and record the starting error count. Do not change checker settings.
2. Read the file and its callers and tests to learn the real shapes of parameters, return values and data structures. Check library types in node_modules or site-packages rather than guessing.
3. Annotate bottom-up: data shapes first (interfaces, TypedDict, dataclasses, enums, union literals), then function signatures, then variables the checker cannot infer.
4. Avoid `any`, `object`, `Any`, `as unknown as`, `# type: ignore` and `@ts-ignore`. If a value really is unknown, use `unknown` and narrow it.
5. Run the checker again and fix each error at its cause. If an error exposes a genuine bug, stop and describe it instead of silencing it.
6. Run the tests to make sure runtime behavior is unchanged.

Report starting versus ending error counts, the new types you defined, and any real bugs found. Do not edit other files without asking.
