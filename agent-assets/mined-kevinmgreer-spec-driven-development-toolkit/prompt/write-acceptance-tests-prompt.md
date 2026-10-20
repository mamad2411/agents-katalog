---
description: "Generate acceptance test stubs from a Gherkin feature file. Creates step definitions for every scenario that fail with 'not implemented' — ready for the green phase. Output will be red (failing tests)."
agent: agent
tools: [read, edit, search, execute]
argument-hint: "Path to .feature file (e.g. specs/changes/add-user-login/delta.feature) or feature name"
---

Generate acceptance test stubs for:

${input:specs/changes/}

## Steps

1. Read the specified `delta.feature` (or the most recently modified `specs/changes/*/delta.feature`).
   Also read the capability it targets — `specs/capabilities/<domain>/behavior.feature` — so
   `@modified:` scenarios are tested in full, not just the steps the delta restates

2. **Read `docs/project-profile.md` — mandatory.** Use the test framework, test command, test
   directory, and test file pattern from the `Tooling` section, and the test-related entries in
   the `Conventions` and `Reference Files` sections.

   **If `docs/project-profile.md` does not exist, stop.** Do not detect on the fly — silent
   fallback is what causes the profile to never get written. Run `/analyze-project` first, then
   return here. Tell the user: _"No project profile found — running /analyze-project first so
   the test stubs match this codebase's conventions."_

3. Generate a test file with:
   - **Header comment**: `// Spec: specs/capabilities/<domain>/behavior.feature` (or language equivalent)
   - Step definitions for **every** Given/When/Then step in the feature file
   - Each stub must **fail** with a clear "not implemented" error — not be empty or skipped
   - Import and setup boilerplate matching project conventions

4. Place the test file in the correct location following project conventions

5. Run the tests and confirm they are **red** (failing for the right reason — not import/syntax
   errors)

6. Report: "X step definitions created, all failing ✓"

The stubs must fail because the implementation doesn't exist yet — not because of setup errors.
If there are setup errors, fix them before reporting.
