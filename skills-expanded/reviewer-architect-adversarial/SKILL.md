---
name: reviewer-architect-adversarial
description: Adversarial plan review — structural validation and assumption attack on grill artifacts before implementation begins.
usedBy: [reviewer]
version: 0.7.0
lastUpdated: 2026-09-12
---

## Purpose

A plan that survives adversarial scrutiny saves hours of rework. Code review catches bugs in what was built. This skill catches flaws in what will be built. It validates structural soundness of the grill artifacts (do referenced files and APIs exist? do the epics cover all acceptance criteria? are the epics coherent?) and attacks assumptions (where will this break? what does the plan take for granted?). Surface problems now, when the fix costs a plan revision, not a code rewrite.

## Procedure

1. **Read the artifacts end-to-end.** Read `tree.md`, `plan.md`, `arch.md`, and `impl.md` in `.memory/plan/<feature-slug>/`. Understand the design tree, acceptance criteria, directory structure, epics, information flows, methods, and tests.

2. **Initialize the progress file.** Create `.memory/reviews/review-architecture-<timestamp>.md` and save it before proceeding:

   ```markdown
   # Architecture Review Progress

   ## Status
   - Last updated: <timestamp>
   - Overall: In Progress

   ## Phases
   - [ ] 1. Completeness
   - [ ] 2. Structural validation
   - [ ] 3. Coverage
   - [ ] 4. Assumptions
   - [ ] 5. Standards
   - [ ] 6. Scope

   ## Findings
   ```

   Do not proceed until the file exists on disk.

3. **Completeness.** Answer each question with yes or no. A "no" is a Blocker. Write findings to the progress file under `## Findings` with heading `### Completeness`. Mark phase 1 as `[x]`. Save the file before proceeding.

   **tree.md:**
   - Does `tree.md` exist with a `Path:` line naming the selected path?
   - Is every node in `tree.md` marked `[settled]`? Any `[open]` node is a Blocker — the grill terminated early.
   - Does every fact in `## Facts` carry a found answer? An open fact with no node depending on it is a Warning.

   **plan.md:**
   - Does `plan.md` contain a context section (2-3 sentences)?
   - Does `plan.md` contain an acceptance criteria section with at least one numbered criterion?
   - Is `plan.md` free of implementation mechanism (no file paths, function names, class names)? Technical terms that describe the product's domain are product language, not mechanism. Flag only terms that prescribe how to build, not terms that describe what the product is.
   - **Clean rewrite check.** Does `plan.md` contain zero strikethrough markup, "Revised:" annotations, "no longer" phrasing, or diff-style markers? If any are present: Blocker.

   **arch.md:**
   - Does `arch.md` contain a directory structure section?
   - Does `arch.md` describe layer separation?
   - Does `arch.md` list reference projects when applicable?

   **impl.md:**
   - Does `impl.md` contain at least one epic with a name and description?
   - Does each epic identify which acceptance criteria it delivers?
   - Does each epic list file paths to create or modify?
   - Does each epic contain method signatures for the methods it introduces?
   - Does each epic contain test specifications (Good, Bad, Ugly) for each method?
   - Does each epic contain an information flow section tracing the request path?
   - Does each epic contain an estimated LOC?
   - Does `impl.md` note parallelizable groups?

4. **Structural validation.** Build lists from the plan, then verify each item. Write findings to the progress file under `### Structural validation`. Mark phase 2 as `[x]`. Save the file before proceeding.
   - **Information flow.** Does each epic's information flow trace a complete path from user entry point through each layer to infrastructure and back? Missing layers or handoffs: Warning. Completely absent or incoherent: Blocker.
   - **Method signatures.** List every method signature across all epics. For each, verify the name follows the project's naming rules (responsibility-first, no tool names in signatures, compound names). Names that violate rules: Warning.
   - **Reference files.** Does each epic list at least one reference file? Missing: Warning.
   - **Files to modify.** List every existing file path the plan says to change. For each, run: `test -f "path/to/file" && echo "EXISTS" || echo "MISSING"`. A "MISSING" is a Blocker.
   - **Files to create.** List every new file path the plan says to add. For each, run: `test -d "$(dirname "path/to/file")" && echo "EXISTS" || echo "MISSING"`. A "MISSING" parent directory is a Blocker.
   - **Named entities.** List every function name, type name, endpoint path, or interface name the plan mentions. For each, search the codebase: `grep -r "entity_name" -l` (adapt file extensions to the project's languages). Zero results for an entity claimed as existing is a Blocker. Entities marked "to create" are expected to be new. Skip those.
   - **Layer boundaries.** If the project documents its architecture (in `.context.md` files, an architecture skill, or a dedicated architecture file), read it. For each file the plan touches, write which layer it belongs to. For each pair of files in different layers, write the dependency direction. If any dependency points from an inner layer to an outer layer, that is a Blocker.
   - **Epic sizing.** Verify each epic's estimated LOC is at or below 600 (soft cap). If it exceeds 600 but not 900: Warning. If it exceeds 900: Blocker. An epic over the cap may need splitting.

5. **Coverage.** Build columns and cross-reference. Write findings to the progress file under `### Coverage`. Mark phase 3 as `[x]`. Save the file before proceeding.
   - **Column A:** List each acceptance criterion from `plan.md` (numbered, with name).
   - **Column B:** List each epic in `impl.md`.
   - **Column C:** List the epic assignments (which acceptance criteria belong to which epic).
   - For each acceptance criterion in Column A, write which epic in Column B delivers it. If a criterion has no matching epic, that is a Warning (not yet delivered — expected if the feature is in progress). If a criterion is marked ✓ or ~, confirm the corresponding epic has been implemented.
   - For each epic in Column B, write which acceptance criterion it delivers. If an epic delivers no acceptance criterion, that is a Blocker (orphan work).
   - **Epic assignment consistency.** Cross-reference Column C against Columns A and B. Every acceptance criterion must be assigned to exactly one epic and delivered by exactly one epic. A criterion assigned to multiple epics, or assigned to an epic but delivered by a different epic, is a Warning.
   - **Test cap check.** For each method, count the test specs per lens (Good, Bad, Ugly). If any method has more than 1 test per lens, that is a Warning.
   - For each test specification, write which acceptance criterion it verifies. If a test verifies no criterion, that is a Warning (wasted test).

6. **Assumptions.** Scan the plan for each pattern below. For each match, verify or flag. Write findings to the progress file under `### Assumptions`. Mark phase 4 as `[x]`. Save the file before proceeding.
   - **Library capability.** Does the plan say a library or framework can do something? Confirm by checking the library's README, its official documentation, then its source code. Stop at the first source that answers the question. Unverified: Warning.
   - **Schema existence.** Does the plan reference a database table, column, index, or migration by name? Search migration files or schema definitions to confirm it exists. Zero results: Warning.
   - **API contract.** Does the plan reference a response field, status code, or endpoint behavior from an external or internal API? Read the handler or client code to confirm the contract matches. Unverified: Warning.
   - **Environment.** Does the plan reference an environment variable, config key, or infrastructure resource by name? Search config files and deployment manifests to confirm. Unverified: Warning.

7. **Standards.** Read every rule loaded in the `<rules>` block. For each plan section that specifies an implementation approach (library choice, pattern, query style, error handling strategy, naming convention), verify the approach does not contradict any loaded rule. A contradiction is a Blocker. Write findings to the progress file under `### Standards`. Mark phase 5 as `[x]`. Save the file before proceeding.

8. **Scope.** Compare the original request against the plan, line by line. Write findings to the progress file under `### Scope`. Mark phase 6 as `[x]`. Save the file before proceeding.
   - List each distinct thing the original request asks for. For each, find the acceptance criterion or epic that satisfies it. If no matching section exists, that is a Blocker (under-delivery).
   - List each file or abstraction the plan creates. For each, find the request sentence that motivated it. If no matching sentence exists and the plan does not explain why it is necessary, that is a Warning (scope creep).
   - **Epic shippability check.** Does each epic deliver user-visible value or a verifiable contract? An epic that requires a future epic to be functional at all is a Warning.

9. **Assemble findings.** Read the progress file. For each finding, verify the severity:
   - **Blocker** — logic incoherence, missing required section, file/entity not found, architectural violation, unmet acceptance criterion. Must be fixed.
   - **Warning** — minor structural concern, edge case, over-specification, orphan work, epic sizing issue. Should be addressed.
   - **Note** — observation or question. No action required.

   Format each finding as:

   ```
   - [<section>: <check name>] Expected: <what the plan claims or requires>. Found: <what verification revealed>. Fix: <concrete action for the Architect>.
   ```

   Group findings under `### Blockers`, `### Warnings`, and `### Notes` headings. Set Overall status to `Complete`. Deliver using the handoff format (follows: `skills/reviewer-handoff/SKILL.md`).

## Guardrails

- Never approve a plan you have not verified against the codebase. Reading the plan is not enough. Check that what it references exists on disk.
- Never flag simplicity concerns as Blockers. A plan that over-engineers is suboptimal, not broken. Simplicity issues are Warnings.
- Never critique the plan's writing style, formatting, or structure. Only its substance. If the plan is clear enough to implement, its prose is fine.
