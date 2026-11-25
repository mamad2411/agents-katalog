---
name: imlazy-planning
description: Create and execute implementation plans. Two modes — light (5-bullet inline plan) for Standard tier; full (plan doc + subagent-dispatched execution + per-task review) for Heavy tier
---

# imlazy-planning

## Mode selection

**Light mode** — used when the router classified Standard tier. Output: 3-7 bullet inline plan in the chat. No plan doc saved. Execute inline in the same session.

**Full mode** — used when the router classified Heavy tier and brainstorming has already produced a spec doc. Output: a saved plan doc at `docs/imlazy/plans/YYYY-MM-DD-<feature>.md`. Execution dispatches a fresh subagent per task with two-stage review (spec-compliance then code-quality).

The router-selected mode is fixed for this task — do not switch modes mid-execution.

---

## Light mode: plan structure (Standard tier)

Write a 3-7 bullet plan inline:

```
Plan (light mode):
1. <one-sentence action — file — expected change>
2. Write failing test for <behavior>
3. Implement <function> in <file> to pass the test
4. Verify: run <test command>, confirm pass
5. Commit: git commit -m "feat: <description>"
```

Rules: each bullet names a file and what changes. TDD bullets are always inline (test → implement → verify). No TBD placeholders.

---

## Full mode: plan document (Heavy tier)

### File structure first

Before defining tasks, map which files are created or modified and what each one is responsible for. Each file has one clear responsibility. Files that change together live together. Split by responsibility, not by technical layer.

### Bite-sized task granularity

Each step is one action (2-5 minutes):
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make it pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

### Plan document header

Every plan doc must start with:

```markdown
# [Feature Name] Implementation Plan

> For agentic workers: use `Skill(imlazy-planning)` in full mode to execute this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]

---
```

### Task structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/test.py`

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

- [ ] **Step 5: Commit**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

### No placeholders

These are plan failures — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "handle edge cases" (without specific code)
- "Write tests for the above" (without actual test code)
- "Similar to Task N" — repeat the code; readers may read tasks out of order
- Steps that describe what to do without showing how

### Plan self-review (before saving)

1. Spec coverage: can you point to a task for each spec requirement? Add missing tasks.
2. Placeholder scan: search for the patterns listed above. Fix them.
3. Type consistency: do method names, types, and paths used in later tasks match what's defined in earlier tasks?

---

## Full mode: execution (subagent-dispatched)

**Why subagents:** fresh context per task — no context pollution between tasks, no confusion about which step you're on. This also preserves the controller's context for coordination work.

**Continuous execution:** do not pause between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete.

**Subagent references:**
- `agents/imlazy-planner.txt` — for creating plans
- `agents/imlazy-architect.txt` — for architecture review
- `agents/imlazy-code-reviewer.txt` — for spec compliance review
- `agents/imlazy-debugger.txt` — for debugging tasks

**Per task:**
1. Dispatch implementer subagent with full task text + context (see `prompts/implementer-prompt.md`)
2. Wait for status: DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
3. If DONE: dispatch spec-compliance reviewer (see `prompts/spec-reviewer-prompt.md`)
4. On spec approval: dispatch code-quality reviewer (see `prompts/code-quality-reviewer-prompt.md`)
5. On quality approval: mark task complete, move to next task
6. Fix any issues, re-review until clean

**Dispatch pattern for imlazy-* subagents:**
When dispatching a subagent using an imlazy-* agent file, load the agent file and prepend it to the system prompt. The agent file provides the role's persona, constraints, and output format. Append the task-specific instructions and context in the user message.

**Handling implementer status:**
- **DONE:** proceed to spec review
- **DONE_WITH_CONCERNS:** read concerns; if correctness/scope issue, address before review; if observation (e.g., "this file is getting large"), note and proceed
- **NEEDS_CONTEXT:** provide the missing info, re-dispatch
- **BLOCKED:** (1) add context and re-dispatch; (2) try a more capable model; (3) break task smaller; (4) if plan is wrong, escalate to the user

**Model selection:**
- 1-2 file isolated tasks with complete spec → cheap/fast model
- Multi-file integration tasks → standard model
- Architecture, design, or review tasks → most capable model

---

## Inline execution fallback (when subagents unavailable)

1. Read plan, review critically — raise any concerns before starting.
2. For each task: follow steps exactly, run verifications as specified, mark complete.
3. Stop and ask when: hit a blocker, plan has a critical gap, instruction is unclear, verification fails repeatedly.
4. On completion: run the completion gate from `Skill(imlazy-tdd)`.

Never start implementation on main/master without explicit user consent.

---

## Cache-friendly dispatch

When dispatching N parallel subagents, construct N requests with **identical** system prompts. The Anthropic prompt cache TTL is ~5 minutes — dispatches within the same batch will hit the cache, making dispatches 2 through N roughly 10× cheaper on input tokens.

What varies per dispatch: the user message (task-specific content).
What stays identical: the system prompt (role, constraints, output format).

Never reuse a subagent across tasks. Fresh context per task; cache hits make this cheap.
