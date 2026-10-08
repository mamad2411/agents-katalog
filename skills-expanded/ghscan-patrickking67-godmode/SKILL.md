---
name: prophecy
description: "Get step-by-step guidance for accomplishing a task in this repo."
---

Produce a concrete, repo-grounded how-to for the task in `$ARGUMENTS`: the exact files,
conventions, and commands someone needs to do it here, not generic advice.

Unlike `/genesis`, this command explains how the task would be done; it does not make
the changes itself.

## 1. Orient

Inspect the repo before writing a word. Learn its actual structure and conventions, then
find the closest thing that already exists and treat it as the template:

- **Locate a precedent**: if `$ARGUMENTS` is "add an API route", find an existing route;
  if it's "wire up a test", find a passing test of the same kind. Read it in full.
- **Extract the pattern**: naming, file placement, registration/wiring, error handling,
  and how the example is tested.
- **Find the commands**: the real build, test, lint, and run scripts from the package
  manifest, Makefile, or task config.

For a repo of any size, dispatch the `Explore` agent to find the precedent and conventions
rather than reading from the root yourself.

## 2. Check current docs for library specifics

If the task touches a library, framework, or tool, do not rely on memory (APIs drift). The
bundled **Context7** MCP serves current docs for most libraries; the **Microsoft Learn**
MCP covers Azure and Microsoft tooling. Consult them for exact syntax, config, and version
details, and ground the steps in what they return.

## 3. Write the how-to

Produce an ordered, numbered procedure specific to THIS codebase. Each step must be
actionable here:

- The real file to copy or modify, as a clickable `path:line` reference.
- The concrete change to make, following the convention from the precedent in step 1.
- Any wiring the example revealed: registration, exports, config entries, fixtures.

No filler steps and no boilerplate that would apply to any repo. If a step only matters
in some cases, say when.

## 4. Commands and verification

End with the exact commands to run, copy-paste ready and in order (generate, build, test,
lint, run), using the project's real scripts from step 1. State how to confirm success:
which test should pass, what output to expect, what the result should look like.

Hand back the guide. Do not edit files or run the build; `/genesis` does that.
