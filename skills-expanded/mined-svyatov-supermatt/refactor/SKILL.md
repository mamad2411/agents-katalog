---
name: refactor
description: "Refactor code at method, file, or project scope. Assesses first and stops when the code is already clean, routes architecture problems elsewhere, and gates edits on test coverage. Language-agnostic."
argument-hint: "[method, file, path, or 'the changes on this branch since <ref>']"
disable-model-invocation: true
metadata:
  credits-skill: refactor, refactor-plan, refactor-method-complexity-reduce, reducing-entropy
  credits-author: GitHub; Leonardo Flores
  credits-url: "https://github.com/github/awesome-copilot/tree/main/skills/refactor"
license: MIT
---

# Refactor

Improve code structure without changing behavior. Works at three scopes: **project**, **file**, or **method**. Starts by assessing whether refactoring is even warranted: if the code is already clean, say so and stop.

**Refactoring vs architecture:** this skill handles code-level improvements: complexity, duplication, naming, dead code, method extraction. If the assessment shows that the real problem is module boundaries, coupling between packages, or shallow modules that need deepening, say so. That is an architecture problem this skill won't fix: tell the user to run `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP.

## Philosophy

These principles calibrate what "good enough" means and guide every step below:

- **Measure the end state, not the effort.** Writing 50 lines that delete 200 is a win.
- **Simple over easy.** Simple means one concept, not intertwined. Easy means familiar. Choose simple.
- **Separate, don't combine.** Good design is taking things apart: removing dependencies, not adding abstractions.
- **Data over abstractions.** 100 functions on one data structure beat 10 functions on 10 custom types.
- **Less total code.** If "better organized" means more lines, it's more entropy, not less.
- **When in doubt, leave it alone.** The default verdict is Clean. Don't invent work.

Read a reference only when the assessment actually turns on it:

- `SIMPLICITY-VS-EASY.md`: when the choice is between a familiar approach and a simpler one
- `DATA-OVER-ABSTRACTIONS.md`: when custom types could be plain data structures
- `DESIGN-IS-TAKING-APART.md`: when a coupled system needs decomposing
- `EXPENSIVE-TO-ADD-LATER.md`: when deciding whether something missing is worth adding now

## Step 1: Determine scope

Infer from the user's request:

| Trigger | Scope |
|---------|-------|
| "refactor this method/function" or a specific symbol name | **method** |
| "refactor this file" or a file path | **file** |
| "refactor this project/codebase" or no specific target | **project** |

"The changes on this branch since `<ref>`" is file scope over each file in `git diff --name-only <ref>...HEAD`, judged on the changed code. If the scope is still ambiguous, ask the user, with the three scopes as the options.

## Step 2: Assess whether refactoring is warranted

**This step is mandatory.** Read the target code and evaluate it against the criteria below. The default verdict is **Clean**: only escalate when there's clear evidence.

### Method scope

- Cognitive complexity: nesting depth >3, boolean expressions with >2 operators, or branch count that makes the flow hard to follow. Investigate, but a long method that reads linearly is not automatically a smell.
- Length: functions over ~50 lines warrant a look, but length alone isn't a verdict. A 70-line function with clear flow is better than 5 tiny functions that scatter the logic.
- Parameter count: >4 parameters on a public API boundary suggests grouping. Internal helpers can have more.
- Single responsibility: does it do one thing?
- Naming clarity: do names describe intent or mechanics?

### File scope

All method-level checks, plus:
- Dead code (unused functions, imports, variables)
- Duplicated logic across functions in the same file
- God class or kitchen-sink module: too many unrelated responsibilities
- Cohesion: do all parts belong together?

### Project scope

All file-level checks, plus:
- Circular dependencies between modules
- Duplicated logic across files/modules
- Overly deep module nesting or excessive file count for what the code does
- Total codebase size: could fewer files/functions achieve the same result?

A whole codebase always offers more findings than are worth acting on. Read `HOTSPOTS.md` and rank by change frequency crossed with complexity before listing anything. It decides what to look at first, not what is wrong.

Read the ranked candidates through subagents, one per area, each returning findings rather than file contents. A project-scope assessment reads far more code than it reports on, and most of it comes back Clean. Step 4 reads what it actually edits. A project under about 1,000 source lines is the exception: read it directly, a few files per call, so each output stays under the 30,000-character limit that moves a result to a file.

### Planned and settled work

Before you list any finding, read each issue the target's commits reference, with its comments, through the **Read an issue** operation in `docs/agents/issue-tracker.md`. Drop a finding that a comment already settled, such as a user's answer to the same question during `implement`, and name that comment in the verdict.

A finding that removes an indirection (a function where a value would do, a parameter, a hook, a seam) can take out what the next planned change needs. Before you list one, also read the open children of those issues' parent issue. Drop a finding that a planned issue needs, and name that issue in the verdict.

### The verdict

| Rating | Meaning | Action |
|--------|---------|--------|
| **Clean** | No meaningful improvements available | Tell the user the code looks good and end the run there. **Stop here** unless they provide a specific reason to continue. An item worth offering the user makes the verdict Minor. |
| **Minor** | Small improvements possible (naming, minor duplication) | List findings. Recommend applying them or leaving the code as is, give the deciding reason, then ask. These are optional. |
| **Significant** | Clear code smells or structural issues | List findings with priorities. Proceed to Step 3. |
| **Critical** | Major structural problems blocking maintainability | List findings urgently. Proceed to Step 3. |

**Idempotency rule:** if you run this skill on the same code twice and it's already been refactored, the verdict must be **Clean**.

**User override:** if the user provides a specific reason to refactor code rated Clean (e.g., "I know it looks fine but I want to extract this into smaller functions"), proceed with their request, but scope the changes strictly to what they asked for. Don't expand into a broader refactoring.

**Architecture signal:** if the assessment shows problems that are really about module boundaries (tightly coupled packages, shallow modules, missing abstractions at the architectural level), say so: refactoring code inside a badly-bounded module won't fix the real problem. Tell the user to run `/improve-architecture` in Claude linked installs or Cursor, `/supermatt:improve-architecture` from the Claude plugin, `$improve-architecture` in Codex, or `/skill:improve-architecture` in OMP.

## Step 3: Plan

For **method** scope, skip to Step 3.5. Planning is unnecessary for single-symbol changes, but the test gate still applies.

Enter plan mode, where the host has one, before planning, so no file changes while the plan is drafted. If the request is too ambiguous to plan safely, ask rather than start.

For **file** scope with 1-3 changes, a bullet list is sufficient:
```
Changes:
- Extract X into helper function
- Remove unused imports
- Rename Y to describe intent
```

For **file** scope with 4+ changes or **project** scope, produce a structured plan:

```
## Refactor Plan: [title]

### Current State
[What's wrong and why it matters]

### Target State
[What the code looks like after: fewer lines, fewer concepts, clearer boundaries]

### Changes
| File | Action | Why | Blocked by |
|------|--------|-----|------------|
| path | modify/create/delete | reason | dependencies |

### Sequence
Phase 1: [contracts/types/interfaces if applicable]
Phase 2: [implementation changes]
Phase 3: [callers]
Phase 4: [test updates, mechanical renames and moves only]
Phase 5: [cleanup, delete dead code]

Verify after each phase: [command]
Final validation: [command that must pass before this is done]

### Rollback
For the riskiest phase: [how to undo it]

### Risks
- [What could go wrong and how to mitigate]
```

**Key principle:** the target state should have **less or equal** total code. If your plan adds net lines without removing complexity, reconsider. "Better organized but more code" is not a win: it's more entropy.

Present the plan through the host's native approval mechanism when exposed, otherwise in chat. Proceed only after explicit approval.

## Step 3.5: Verify test coverage

**Before changing any code**, check that tests exist for the target:

1. Search for test files covering the target code (look for test files matching the module/class name, grep for the function name in test directories).
2. If tests exist, note which behaviors they cover and run the affected tests against the unchanged code. Record the command and result as the baseline. If it fails or flakes, stop and report the failure; resolve it or agree its handling with the user before editing. Do not attribute an existing failure to a refactor or use it as regression evidence. Proceed to Step 4 only with a usable baseline.
3. If tests are missing or sparse, **stop and tell the user.** Refactoring without tests risks silently changing business logic. Ask whether to write characterization tests first or proceed without them. To write them, load and follow the `tdd` skill through the host's skill mechanism and use its characterization tests in their own `test:` commit.

Judge coverage over the code you are about to change, not over the repository. A repo at 85% overall tells you nothing if the target sits in the untested 15%.

This gate is especially important for code with business logic (calculations, validation rules, state transitions, money). Structural code (routing, configuration, glue) is lower-risk without tests, but still worth flagging.

Do not skip this step. Refactoring means "change structure, preserve behavior", and you can only guarantee "preserve behavior" if there are tests to prove it.

## Step 4: Refactor

### Ground rules

1. **Behavior is preserved**: refactoring changes structure, not behavior.
2. **Small steps**: one change at a time, verify after each.
3. **One concern at a time**: don't mix refactoring with feature work.
4. **Bias toward deletion**: every refactoring is a chance to remove code. Ask: what does this make obsolete?
5. **Tests are frozen**: do not edit test files to make them pass. A test that has to change is telling you the behavior changed, which means this is no longer a refactor. Mechanical renames and file moves are the only exception.
6. **Start from a clean, committed baseline**: commit or stash unrelated work first, then record the current commit as `<baseline>`. Any characterization tests from Step 3.5 must already be committed.
7. **Commit each step separately, as `refactor:`, and never mix structural and behavioral change in one commit**: a move and an optimization are two commits even though both are structural.
8. **Revert, don't debug forward**: when a step goes red, undo it and take a smaller one. The revert is free; the debugging session is not.

### Common refactoring moves

Apply whichever are relevant. Do not apply moves that don't improve the specific code.

When one move repeats across more than a handful of sites, read `MECHANICAL-SWEEPS.md` before editing by hand.

**Reduce complexity:**
- Replace nested conditionals with guard clauses or early returns
- Extract focused helper functions from long methods
- Replace complex boolean expressions with named predicates
- Break god classes into cohesive modules

**Eliminate duplication:**
- Extract shared logic into a single function
- Replace copy-pasted code with parameterized functions
- Consolidate duplicate type definitions

**Improve clarity:**
- Rename variables/functions to describe intent, not mechanics
- Replace magic numbers/strings with named constants
- Group related parameters into objects/records
- Move logic to the object that owns the data (fix feature envy)

**Reduce entropy:**
- Delete dead code: unused functions, imports, variables, commented-out blocks
- Inline single-use abstractions (unnecessary wrappers, thin delegators)
- Prefer data structures over custom types when custom behavior isn't needed
- Ask: could this be fewer functions? Fewer files? Fewer concepts?

### Where deletion goes wrong

"Less code" is the measure, not the goal. Reject a transformation that wins on line count and loses on reading:

- Nested ternaries and dense one-liners are fewer lines and harder to read. Choose clarity over brevity.
- An abstraction that organizes the code is not the same as an unnecessary wrapper. Inline the thin delegator, keep the one that names a concept.
- If the metric improved but the code reads worse, the transformation failed. Readability is the criterion; line count is a proxy.

### Method complexity reduction

When refactoring a specific method for complexity:

1. Identify complexity sources: nesting, long if/else chains, repeated blocks, complex booleans.
2. Extract focused helpers, each with a single clear responsibility.
3. Use guard clauses to reduce nesting depth.
4. The main method should read as a high-level flow.
5. Preserve all input/output behavior, error handling, and edge cases.

## Step 5: Verify

After refactoring:

1. **Check that no test changed.** Compare the baseline commit from ground rule 6 with the current tracked working-tree state: `git diff --name-only <baseline>` includes committed, staged, and unstaged changes. Characterization tests committed in Step 3.5 are already in the baseline; subsequent changes to them belong in that list and follow the same frozen-test rule. If an existing test file was modified beyond a rename or a move, stop and say so: the behavioral contract was rewritten to match the new code, which hides exactly the failure this step exists to catch.
2. **Run all tests** that cover the refactored code. Read the actual output; a command that exited is not a suite that passed. If any fail, fix your refactoring, not the tests.
3. **Confirm behavior is unchanged**: same inputs produce same outputs. If tests were written in Step 3.5, they serve as the proof.
4. **Check the result**: re-evaluate the code against Step 2 criteria. The verdict should be **Clean** or **Minor**. If only Minor issues remain, note them but do not re-enter the refactoring loop.
