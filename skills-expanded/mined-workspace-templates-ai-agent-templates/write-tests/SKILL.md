---
name: write-tests
description: Writes tests for a named file or function in your existing test style, runs them and reports what they cover and what they miss.
disable-model-invocation: true
---

Write tests for: $ARGUMENTS

1. Read the target and what it depends on. Then find the closest existing test file and copy its runner, imports, naming, fixtures and mocking style. Find the test command in package.json, pyproject.toml, Makefile or the CI file.
2. List the behaviors first: the normal path, boundaries (empty, zero, one, maximum), invalid input, error paths, and any ordering or time dependence.
3. Write one test per behavior with a name that states the expectation. Assert on outputs and visible effects, not on internals. Mock only I/O boundaries such as network, clock and filesystem.
4. Run only the new tests. If one fails, decide whether the test or the code is wrong. Never weaken an assertion to get green.
5. Put the file next to the others, following project layout.

Report: the tests added, the command to run them, behaviors deliberately left out, and any real bug found. Ask before changing source code.
