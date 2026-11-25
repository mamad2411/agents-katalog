---
name: specmgr
description: >
  Spec-driven development workflow manager. Use when: (1) creating a DRAFT spec
  from input files or raw ideas, (2) creating a chunk plan
  from a DRAFT spec, (3) implementing a DRAFT spec (DRAFT to IMPLEMENTED transition),
  or (4) managing spec state transitions. Triggers on "create spec", "draft spec",
  "implement spec", "chunk plan", "spec workflow", or references to *-spec.md files.
metadata:
  tags: spec, specification, workflow, implementation, planning, chunking
  platforms: Claude, ChatGPT, Gemini
---

# Spec-Driven Development Workflow Manager

Individual `*-spec.md` files are treated as the specification for each feature—they define what the feature is and what it must do. These specification files are the authoritative ("canonical") source of requirements for their parts of the application.

- All spec files that are created from other raw report documents should reference those documents in the title header of the spec
- When writing a new spec, review the existing specs in the specs/ directory and identify any that are clearly superseded by your new specification. List only the directly superseded (first-level) specs.

---

## Workflow 1: Create DRAFT Spec

**Triggers:** "create a DRAFT spec from...", "write a spec for...", "draft spec..."

### Before writing the spec

1. Read all input/reference files first
2. Read all files matching `*-spec.md` in the project's `specs/` directory; newer specs take priority over older ones
3. Check `specs/README.md` for the existing spec index

### STOP: Ask clarifying questions

**Do NOT proceed to writing the spec until this step is complete.**

Present your questions to the user about:
- Anything that needs clarification in the input
- Any incompatibilities found with existing specs
- Recommendations or design choices you see

Wait for the user's answers before writing the spec document.

### Naming convention

- Filename format: `specs/<name>-spec.md`
- The `<name>` portion is derived from the input file or feature name (e.g., `featurereport74.md` → `specs/featurereport74-spec.md`)

### Spec template

Include the following fields at the top of every DRAFT spec:

```
## Title

- **Date:** `<ISO 8601 format with seconds, America/Denver timezone>`
- **References:** list of `<other-raw-report-path.md>` or `<none>`
- **Supersedes:** list of `<other-spec-file.md>`
- **Chunkplan:** `<path-to-chunkplan.md>` or `none`
- **Chunked:** `true` or `false`
- **State:** one of these valid values: `DRAFT`, `IMPLEMENTED`, `VALIDATED`
```

### Setting the `Chunked:` field

- Set to `true` if the spec should be broken into a chunk plan before implementation. Set to `false` if it can be implemented in a single pass.
- Consider `true` when: the spec touches many files across different subsystems, requires multiple independent features or phases, has complex test strategy spanning several areas, or would exceed what an agent can reliably implement and test in one session.
- Consider `false` when: the changes are mechanical/uniform (e.g., same pattern applied across many call sites), the scope is limited to one subsystem, or the spec is a straightforward bug fix.
- This is a recommendation for the human reviewer — the chunk plan is not created until after review.

### Root cause analysis

If the raw issue is a bug or something broken, perform a root cause analysis and include that in the spec.

### Companion agent test plan

Always create a companion agent test plan file alongside the spec: `<spec-basename>-agent-test-plan.md` (e.g., `condense-build-header-spec.md` → `condense-build-header-agent-test-plan.md`). The agent test plan must contain concrete CLI commands that an agent can execute to verify the implementation works end-to-end against the real tool and environment. Link the agent test plan from a `## Agent Test Plan` section at the end of the spec (before the `## SPEC workflow` section).

### Agent test plan guidelines
The point of an agent test plan is to validate that once a spec is implemented, that all the components exist together as part of a coheseive whole.  e.g.

- website (if any) can start up without errors
- expected website content is visible
- cli tool (if any) can run with options modified under spec
- execute basic functionality against known external data according to the spec

A test plan is not:
- a substitute for a unit test
- a substitute for an end to end test
- a substitute for an integration test
- a substitute for passing all CI/CD tests
- a comprehensive test of everything changed in the spec

### SPEC workflow section

Include the following verbatim at the end of every DRAFT spec:

```
## SPEC workflow

1. read `specs/CLAUDE.md` and follow all rules there to implement this DRAFT spec (DRAFT->IMPLEMENTED)
```

### Superseded specs

When creating a new spec, identify any existing specs that are directly superseded by the new specification. List them in the `Supersedes:` field.

---

## Workflow 2: Create Chunk Plan

**Triggers:** "create a plan from spec...", "chunk this spec...", "break down spec...", "create a chunk plan..."

### Instructions

1. Load the `references/taskcreator.md` file from this skill for the full decomposition methodology.
2. Load the `references/chunk-template.md` file from this skill for the chunk format template.
3. Follow all rules in `references/taskcreator.md` to decompose the spec.

### Plan file naming

- Plan files are named: `specs/<spec-basename>-chunkplan.md` (e.g., `majorfeature47-spec.md` → `specs/majorfeature47-chunkplan.md`)
- Plan files are created in the `specs/` directory (not `specs/todo/`), regardless of where the source spec file is located. Plans are ready-to-implement artifacts.
- After the chunk plan file is written, update the parent spec's `Chunkplan:` field to reference the chunk plan file.

### SPEC Workflow in plans

The SPEC Workflow block embedded in plans must use generic language:
- "Run all unit tests" (do not hardcode a test runner command — the project's `CLAUDE.md` or `specs/CLAUDE.md` specifies the test runner)
- "Commit and push" (do not hardcode a push command — the project's conventions apply)
- "Update project documentation as specified in the project's CLAUDE.md or specs/CLAUDE.md"

---

## Workflow 3: Implement DRAFT Spec (DRAFT → IMPLEMENTED)

**Triggers:** "implement DRAFT spec...", "implement spec..."

When implementing a DRAFT spec or bug fix, follow these steps in order.

### 3a Before writing code

- [ ] **Check for chunk plan** if there is a chunk plan use Workflow 4 instead of this one
- [ ] **Check build status** and confirm the last build is successful. Do not proceed if the build is setup but broken.  It is ok if there is no build setup for this project yet.
- [ ] **Run all unit tests** and confirm they pass. Do not proceed if there are existing tests but they are failing.

### 3b Implement the feature or fix

- [ ] **Write the code** as described in the spec's Specification section.
- [ ] **Write or update unit tests** as described in the spec's Test Strategy section.
- [ ] **Run all unit tests** and confirm they pass (both new and existing).

#### Existing test modification policy

When your implementation causes a pre-existing test to fail, you may fix it and continue — do not stop to ask. However:

1. **Determine spec backing first.** Before changing an existing test, identify which section of the spec requires the behavioral change that invalidates the old test.
2. **If the spec backs the change:** fix the test and log the change in the implementation review log (see Implementation Review Report section).
3. **If no spec section backs the change:** you still may fix it and continue, but you MUST log it with `Spec Backing: None` in the review log. These entries will be flagged for reviewer attention.
4. **What counts as modifying an existing test:** changing assertions, expected values, fixture data, test domain names, or any other change whose purpose is to make a previously-passing test continue to pass under new behavior. Adding new test cases is not a modification.
5. **Never weaken a test to avoid a failure.** Changing fixture data to sidestep new validation (e.g. removing a `.com` suffix so domain validation is never triggered) is weakening, not fixing. If the test was exercising a code path that your implementation changed, the test should still exercise that code path — with correct updated expectations.

### 3c Run agent test plan (if present)

- [ ] **Check if the spec references an agent test plan** (look for a `## Agent Test Plan` section or a companion `*-agent-test-plan.md` file). If one exists, execute the test plan and verify it is successful.

### 3d Verify CI/CD build is green

- [ ] **CI/CD gate — MANDATORY before marking IMPLEMENTED.** The spec CANNOT be marked IMPLEMENTED unless the CI/CD build is confirmed GREEN (no failures). Follow this procedure:
  1. Check if the project has a `buildgit` skill installed (look for a `SKILL.md` in a `skill/buildgit/` directory) and a configured build job (e.g. `JENKINS_URL` is set, or a Jenkinsfile exists).
  2. **If buildgit is available and a build job is configured:** Run `buildgit status` (or equivalent) and verify the latest build result is SUCCESS with no test failures. If the build is failing, fix the issues and push again. Repeat until the build is GREEN. Do NOT proceed to mark the spec IMPLEMENTED while the build is broken.
  3. **If buildgit is NOT installed or no build job is configured:** This is acceptable — note it in the implementation review report under the `## CI/CD Verification` section (see Implementation Review Report template). Proceed to the next step.

### 3e Update documentation and metadata

- [ ] **Update the spec file:** Change its `State:` field to `IMPLEMENTED` and add it to the spec index in `specs/README.md`.
- [ ] **Handle referenced files:** If the spec lists files in its `References:` header, move those files to `specs/done-reports/` and update the reference paths in the spec accordingly.
- [ ] **Run any additional project-specific finalize steps** as specified in the project's `CLAUDE.md` or `specs/CLAUDE.md`. This is the extension point where project-specific documentation updates, skill file updates, and custom push/CI commands are executed.

## Workflow 4: Implement DRAFT Spec using chunk plan (DRAFT → IMPLEMENTED)

**Triggers:** "implement DRAFT spec with chunk plan ...", "implement chunk X from chunk plan..."

### 4a Before writing code
- [ ] **Check for chunk plan** if there is no chunk plan, use Workflow 3 instead of this one
- [ ] **Run all unit tests** and confirm they pass. Do not proceed if tests are failing. If the test commands themselves are broken (e.g. missing tools, build infrastructure failures, repository configuration errors), do NOT skip tests and continue — this is a blocking failure. Output `RALPH_BLOCKED=<reason>` as the final line and stop.

### 4b Per-Chunk Workflow (every chunk must follow these steps)

- [ ]  **Implement the chunk** as described in its Implementation Details section.
- [ ]  **Write or update unit tests** as described in the chunk's Test Plan section.
- [ ]  **Run all unit tests** and confirm they pass (both new and existing). The **Existing test modification policy** from Workflow 3b applies here as well.
- [ ]  **Mark chunk complete** Mark ONLY the one chunk you implemented as completed in chunkplan (change '- [ ]' to '- [x]').
- [ ]  **Fill in the `#### Implementation Log`** for the chunk you implemented — summarize files changed, key decisions, and anything notable.
- [ ]  **Commit and push** per the project conventions. Use a commit message starting with `chunk N/T:` followed by a brief description.
- [ ]  **Fix build errors** Wait for the build to complete. Fix any errors shown.  Repeat this step as necessary.

**Blocking failure rule:** If at any point during the per-chunk workflow you encounter a failure that you cannot fix (broken build infrastructure, missing tools, repository configuration errors, or test failures unrelated to your chunk's changes), do NOT output `REMAINING_CHUNKS=n`. Instead, output `RALPH_BLOCKED=<brief reason>` as the final line and stop immediately. Do not attempt the next chunk.

### 4c Run agent test plan (if present)

- [ ] **Check if the spec references an agent test plan** (look for a `## Agent Test Plan` section or a companion `*-agent-test-plan.md` file). If one exists, execute the test plan and verify it is successful.

### 4d Verify CI/CD build is green

- [ ] **CI/CD gate — MANDATORY before marking IMPLEMENTED.** The spec CANNOT be marked IMPLEMENTED unless the CI/CD build is confirmed GREEN (no failures). Follow this procedure:
  1. Check if the project has a `buildgit` skill installed (look for a `SKILL.md` in a `skill/buildgit/` directory) and a configured build job (e.g. `JENKINS_URL` is set, or a Jenkinsfile exists).
  2. **If buildgit is available and a build job is configured:** Run `buildgit status` (or equivalent) and verify the latest build result is SUCCESS with no test failures. If the build is failing, fix the issues and push again. Repeat until the build is GREEN. Do NOT proceed to mark the spec IMPLEMENTED while the build is broken.
  3. **If buildgit is NOT installed or no build job is configured:** This is acceptable — note it in the implementation review report under the `## CI/CD Verification` section (see Implementation Review Report template). Proceed to the next step.

### 4e Update documentation and metadata

- [ ] **Update the spec file:** Change its `State:` field to `IMPLEMENTED` and add it to the spec index in `specs/README.md`.
- [ ] **Handle referenced files:** If the spec lists files in its `References:` header, move those files to `specs/done-reports/` and update the reference paths in the spec accordingly.
- [ ] **Run any additional project-specific finalize steps** as specified in the project's `CLAUDE.md` or `specs/CLAUDE.md`. This is the extension point where project-specific documentation updates, skill file updates, and custom push/CI commands are executed.

---

## Spec State Machine

- **DRAFT**: Spec written, not yet implemented.
- **IMPLEMENTED**: Code written, tests passing, docs updated. This is the normal post-implementation resting state and it is acceptable for a spec or its chunks to remain here indefinitely until a human validation pass happens.
- **VALIDATED**: Human has manually verified the implementation. Validation is a separate later step from implementation.

### IMPLEMENTED → VALIDATED

- Perform all manual testing to make sure the change does what it claims (human does this)
- Mark the `State:` of the spec to `VALIDATED`
- For chunked work, it is valid to move every completed chunk from `IMPLEMENTED` to `VALIDATED` in one later pass after the human verifies the integrated feature end-to-end. Do not require each chunk to be validated immediately after its implementation.

---

## Multi-chunk plan workflow tiers

When implementing a spec via a chunk plan, the workflow is split into tiers as documented in `references/taskcreator.md`

**Initialize workflow** (runs before any chunks are implemented)
- Run all unit tests before starting

**Per-chunk workflow** (each chunk does these):

**Finalize workflow** (runs once after all chunks complete):
- Update CHANGELOG.md, README.md, and any other project documentation
- **Generate the implementation review report** (see below)
- Run any additional project-specific finalize steps (per project's CLAUDE.md)
- Push and verify CI
- **CI/CD gate: confirm the build is GREEN before marking the spec IMPLEMENTED** (see Workflow 4d)
- Human validation may later move the completed chunks and/or parent spec from `IMPLEMENTED` to `VALIDATED` in a single follow-up pass

Single-spec implementation (without a plan) continues to do everything in one pass as described above.

---

## Implementation Review Report

Every spec implementation — whether via chunk plan, single-pass, or follow-up bug fix — MUST produce a review report at finalize time.

### File location and naming

`specs/done-reports/{spec-basename}-review.md`

Example: `specs/claim-domain-spec.md` → `specs/done-reports/claim-domain-spec-review.md`

### Report template

```markdown
# Implementation Review: {spec title}

**Spec:** `specs/{spec-file}.md`
**Implemented:** {date}
**Implementer:** {agent or human}

## Existing Test Modifications

| Test File | Change | Spec Backing | Rationale |
|-----------|--------|--------------|-----------|

If no existing tests were modified, write: "No existing tests were modified."

## CI/CD Verification

Record the CI/CD build status at finalize time. One of:
- **Build GREEN:** `<build tool> status` confirmed SUCCESS (build #N, date)
- **No CI/CD configured:** project does not have a buildgit skill installed or no build job is configured. Spec marked IMPLEMENTED without CI/CD verification.

## Flagged Decisions

Any entry above with Spec Backing = "None" must be repeated here with additional context about why the agent proceeded without spec backing. These are the items that most need reviewer attention.

## Files Changed (alphabetical)

- `path/to/modified-file.ext`

List only project files that were modified (not created) by this implementation. Exclude temporary files, build artifacts, and generated output.

## Files Created (alphabetical)

- `path/to/new-file.ext`

List only new project files added by this implementation. Exclude temporary files, build artifacts, and generated output.

## Key Implementation Decisions

- {notable design decisions, trade-offs, or deviations from the spec, one per bullet}

## Consolidation

If a chunk plan was used, summarize each chunk's Implementation Log entry here (one bullet per chunk). This provides a single-file view of the entire implementation.
```

### How the report is built

- **During implementation:** Each time you modify an existing test, immediately append a row to a scratch log (the chunk's `#### Implementation Log` if using a chunk plan, or a temporary `## Implementation Review Notes` section at the bottom of the spec file if not). Do not defer this — log it when you make the change.
- **At finalize time:** Consolidate all logged entries into the review report file. Remove any temporary scratch sections from the spec file.
