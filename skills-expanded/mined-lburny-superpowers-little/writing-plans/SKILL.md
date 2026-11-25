---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans for the current session: which files each task touches, code, testing, how to test. Break into bite-sized tasks. DRY. YAGNI. TDD.

Assume you are a skilled developer, but new to the codebase and problem domain.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** any local path; default `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`. No commit required.

## Scope Check

Multiple independent subsystems should have been split into sub-projects during brainstorming. If not, suggest separate plans — one per subsystem, each producing working, testable software.

## File Structure

Before tasks, map which files will be created or modified and each one's responsibility. Decomposition is locked in here.

- One clear responsibility per file, with well-defined interfaces.
- Prefer small, focused files — you reason and edit more reliably on code that fits in context.
- Files that change together live together. Split by responsibility, not technical layer.
- In existing codebases, follow established patterns. Don't unilaterally restructure large files — but splitting an unwieldy file you're already modifying is reasonable.

Each task should produce self-contained, independently sensible changes.

## Task Right-Sizing

A task is the smallest unit with its own test cycle and review gate. Fold
setup, config, scaffolding, and docs into the task whose deliverable needs
them; split only where a reviewer could reject one task while approving
its neighbor. Each task ends with an independently testable deliverable.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step

## Length Budget

Plans are working documents, not specifications. Long plans cost writing,
reading, and context-window time.

- **Budget: at most ~500 lines.** Beyond that, split into sub-plans (see
  Scope Check) or reduce per-task detail.
- **Scale detail to risk.** Full code blocks for core logic and non-obvious
  implementations. Mechanical steps — config edits, dependencies, wiring
  existing functions, moving files — need only exact path, exact change or
  command, expected result.
- **Don't restate the spec.** Quote exact constraining values (version
  floors, naming rules) verbatim; summarize everything else in one line.
- **Diffs over repetition.** Show only what changes, never repeat blocks.

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Implement this plan in the current session. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[Project-wide requirements — version floors, dependency limits, naming
rules, platform requirements — one line each, exact values verbatim from
the spec. Every task implicitly includes this section.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact names, parameter and return
  types. Implementers see only their own task; this is how they learn
  neighboring tasks' names and types.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS
````

## No Placeholders

Every step must contain what an engineer actually needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" *with nothing else* — referencing an identical earlier task is allowed only if you state exactly what changes (names, values, paths)
- Steps that describe what without showing how (code blocks required for core logic; see Length Budget for mechanical steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code for core-logic steps; path+command+expected-result for mechanical steps
- Exact commands with expected output
- Stay within the Length Budget
- DRY, YAGNI, TDD

## Self-Review

After writing the plan, re-read the requirements and check the plan against them — a self-check, not a subagent dispatch.

**1. Spec coverage:** For each spec requirement, can you point to a task that implements it? List gaps.

**2. Placeholder scan:** Search for the red flags from "No Placeholders" above. Fix them.

**3. Type consistency:** Do names, signatures, and types in later tasks match earlier definitions? `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Length check:** Within budget (~500 lines max)? If not, tighten mechanical steps to one-liners and use diffs — cut repetition, never required content.

Fix issues inline and move on. If a spec requirement has no task, add the task.

## Execution Handoff

After saving the plan, execute it in the current session. Whether to dispatch subagents for individual tasks depends on task complexity — handle simple tasks inline; delegate substantial, independent ones.

Each task follows the RED-GREEN-REFACTOR cycle (write failing test → implement → pass). Use the `test-driven-development` skill as the execution method — it defines the rules for writing the failing tests and minimal implementations that every step above specifies.

When all tasks are done, invoke the verification-before-completion skill before claiming completion.

> "Plan complete. I will now execute the plan step by step."
