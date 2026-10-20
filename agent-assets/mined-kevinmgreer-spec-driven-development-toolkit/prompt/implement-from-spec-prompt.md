---
description: "Implement production code to make failing acceptance tests pass. Works scenario by scenario in priority order. Only adds code that tests require. Never modifies test files."
agent: agent
tools: [read, edit, search, execute]
argument-hint: "Feature name or path to .feature file (e.g. specs/changes/add-user-login/delta.feature)"
---

Implement the production code needed to make the failing acceptance tests pass for:

${input}

## Steps

1. Read the `.feature` file and `specs/changes/<name>/delta-rules.md`.

2. **Read `docs/project-profile.md` — mandatory.** Pay particular attention to:
   - `Conventions` — architecture, error handling, validation, naming, etc.
   - `Reference Files` — the existing files the agent should mirror, one per layer
   - `Anti-patterns to avoid in this repo`

   If `docs/project-profile.md` does not exist, **stop** and run `/analyze-project` first.

3. **Open at least one reference file from the same layer you are about to write** (controller,
   service, repository, etc.). For multi-layer features, open one reference per layer.

4. **State explicitly which conventions you will follow** before writing any code, e.g.:
   > Following profile: layered architecture, constructor DI, custom `AppError` for business
   > failures, zod validation at controller boundary, JSDoc on public exports, kebab-case files.
   > Mirroring `src/features/orders/orders.service.ts`.

   This statement is required output — do not skip it.

5. **Check whether acceptance tests exist** — search for a test file that references the feature
   (look for the header comment `// Spec: specs/capabilities/<domain>/behavior.feature` or equivalent).

   **If no test file exists** — stop and run `/write-acceptance-tests` first:
   - Invoke `/write-acceptance-tests ${input}` to generate, run, and confirm red stubs
   - Do not proceed with implementation until every stub fails for the right reason
   - Return here once stubs are confirmed red

   **If test file(s) exist** — read them in full before writing any code:
   - Open every file that references the feature spec
   - Understand the assertion structure, helpers, and setup — implementation must satisfy the
     assertions as written, not just pass runner output

6. Run the current tests to see which are failing and why.

7. Implement in priority order: `@smoke` → `@happy-path` → `@edge-case` → `@error`.

8. For each scenario:
   a. Read the scenario carefully — understand the expected behavior
   b. Write the **minimum** code that makes this scenario's test pass
   c. **Mirror** the patterns from the project profile and reference files — do not introduce
      a new architecture, error style, validation library, or naming scheme. If the failing test
      seems to require a new pattern, stop and ask.
   d. Run the test — if green, move to the next scenario
   e. If a test fails unexpectedly, diagnose and fix before moving on

9. **Rules** (enforced strictly):
   - Do NOT write code not required by a failing test
   - Do NOT modify test files — fix the implementation
   - Do NOT implement `@wip`-tagged scenarios
   - Do NOT add error handling for cases not covered by an `@error` scenario
   - Do NOT introduce a new convention without first updating `docs/project-profile.md` and
     telling the user

10. When all non-`@wip` scenarios are green, report:
    - The conventions statement from step 4
    - Which files were created and modified
    - How many scenarios went from red to green
    - Any `@wip` scenarios skipped (and their descriptions)
    - Whether you introduced any new convention or dependency that needs to be added to
      `docs/project-profile.md` (Phase 6 will sync these)
