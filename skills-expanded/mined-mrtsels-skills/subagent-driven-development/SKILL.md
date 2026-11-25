---
name: subagent-driven-development
description: "Dispatch coding tasks via Hermes delegate_task subagents. Two modes: Direct Execution (one subagent = one PR) and 2-Stage Review (spec + quality audit)."
version: 1.2.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks
- **You need to dispatch bounded, self-contained coding work to a Hermes subagent** (Direct Execution mode) for verification + commit + PR in one shot

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early (Mode B)
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

**Which mode to choose:**
- **Direct Execution (Mode A):** Task is bounded, has clear success metrics, subagent can self-verify via existing tests. Use by default for most coding tasks — one subagent = one PR.
- **2-Stage Review (Mode B):** Task is complex, correctness-critical, or could easily miss the spec. Use for architectural changes, data-migration logic, security-sensitive features, or when the team needs an independent audit trail.

## The Process

This skill supports two modes. **Use Direct Execution for self-contained tasks with clear verification** (one subagent = one branch = one PR). Use 2-Stage Review for complex, multi-file, correctness-critical work.

#### Variant: Parallel Independent Tasks (no branches)

See `references/parallel-independent-tasks.md` for dispatching multiple
subagents on disjoint code paths without branches or worktrees.

**User preference:** Some users prefer full autonomy — given a plan
and a list of tasks, dispatch everything and deliver the final result
without intermediate check-ins. The signal is: _"按你计划的顺序把这些都做了，
然后集中交付。中间不需要和我汇报。"_ When this is stated, execute
the entire batch and summarize at the end only.

**Safety check for trust-driven dispatch:** Before dispatching parallel
subagents, verify file overlap with `git diff --stat <branch>` or
`find ... -newer`. If any file appears in both task descriptions, fall
back to sequential or worktree-based dispatch to avoid conflicts.

## Mode C: Parallel Multi-Branch (Multiple subagents, same repo)

**When to use:** You need many independent changes to the same repository simultaneously — different files, different sections of the same file, or frontend + backend changes that don't overlap. Each subagent works in its own branch + worktree.

Rules:
- **Each subagent = one branch = one worktree.** Never share a worktree across subagents.
- **Changes must NOT touch the same code paths** (same function, same handler, same database migration). If two subagents modify the same function, you WILL get merge conflicts. Use `git merge --squash` to merge sequentially; conflicts indicate work was not independent enough.
- **After all subagents complete → merge branches sequentially → verify** with `node --check` (for JS) or `pytest` (for Python) on the accumulated result.
- **Track progress visibly.** Use the `todo` tool as a kanban substitute: create one item per subagent, mark in_progress when dispatched, completed when merged.
- **Push all branches upfront** to avoid merge base issues.

#### Batch Setup Pattern

```python
from hermes_tools import terminal

# 1. Create all branches + worktrees upfront
branches = ['feat/change-a', 'feat/change-b', 'feat/change-c']
for br in branches:
    terminal(f"git push origin main:refs/heads/{br}")
    terminal(f"git worktree add /tmp/wt-{br} {br}")

# 2. Dispatch subagents in parallel (use delegate_task tasks=[])
delegate_task(
    tasks=[
        dict(goal="Change A description", context="worktree=/tmp/wt-change-a ...", toolsets=["terminal", "file"]),
        dict(goal="Change B description", context="worktree=/tmp/wt-change-b ...", toolsets=["terminal", "file"]),
        dict(goal="Change C description", context="worktree=/tmp/wt-change-c ...", toolsets=["terminal", "file"]),
    ]
)

# 3. After all complete, squash merge into main sequentially
for br in branches:
    terminal(f"cd /repo && git merge --squash {br} && git commit -m 'feat: squash {br}'")

# 4. Verify merged result
terminal("cd /repo && node --check index.html")
terminal("cd /repo && git push origin main")

# 5. Clean up
for br in branches:
    terminal(f"cd /repo && git branch -D {br} && git push origin --delete {br}")
    terminal(f"git worktree remove --force /tmp/wt-{br}")
terminal("git worktree prune")
```

#### Safety Checks

- **Always verify the MERGED result** (not just individual branches). Parallel changes can interact in unexpected ways that pass individual checks but fail as a whole.
- **Run `node --check`** on HTML files by extracting script blocks to .js files:
  ```python
  import re, subprocess
  with open('index.html') as f:
      c = f.read()
  scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
  for i, s in enumerate(scripts):
      with open(f'/tmp/check_{i}.js', 'w') as f2: f2.write(s)
      r = subprocess.run(['node', '--check', f'/tmp/check_{i}.js'])
      assert r.returncode == 0, f'Script {i} failed'
  ```
- For the same file, prefer `patch` tool over Python string manipulation. `patch` has fuzzy matching. If you must use Python (e.g. when patch's old_string matching fails due to escaped quotes), write a dedicated `.py` file and run it via `terminal()` — never inline complex replacements in a `-c` string.

#### Pitfalls

- **`patch` can insert literal `\\n`** when the replacement text contains backslash-n sequences. If a `patch` diff shows `\\n` (literal backslash + n) instead of actual newlines, use `execute_code()` with `.replace(b'\\\\n', b'\\n')` on the bytes, or use `sed` in terminal to fix.
- **Don't use regex to remove functions** from large JS files. The regex `r'async function name\(\)\{[^}]*\}'` will match greedily across braces and destroy surrounding code. Instead, find the exact function by its unique content markers (`file.find('function marker')`) and slice it out.
- **Reset from git** when patch chains get too tangled. If you've made 5+ patches to the same file and they're producing cascading errors, `git checkout -- index.html` back to clean and redo with fewer, more precise operations.

### Mode A: Direct Execution (Recommended for most tasks)

**When to use:** The task is a bounded piece of work with clear success criteria, the subagent can verify its own output, and you trust it to produce a reasonable result without an independent reviewer.

Rules:
- **One subagent = one branch = one PR.** Never have one subagent touch multiple branches.
- **The subagent must verify its own work** — run tests and prove they pass before finishing.
- **Include git + verification commands in the prompt.** The subagent has no access to the parent conversation.
- **Handle git proxy.** If `$http_proxy` is set (e.g. Shadowrocket at 127.0.0.1:1082) and returns 503 for GitHub, set `git config --global http.proxy ""` (empty string, NOT `--unset`) to bypass. `--unset` causes git to fall back to the env var.
- **Git commit at every step.** Every subagent must commit its work before finishing. Commits are atomic — one change = one commit. Push immediately after each commit.
- **Model selection:** Match model to task complexity. Pro for architectural decisions, mathematical correctness, constraint-aware logic, multi-file orchestration. Flash for mechanical boilerplate, matplotlib plots, simple heuristics, pattern-following. Litmus test: if a competent junior could do it right with clear specs, use flash.

#### Setup Pattern

```python
# 1. Create branch and push
terminal(command="cd /repo && git checkout -b feat/my-task origin/main && git push origin feat/my-task")
# 2. Create worktree
terminal(command="cd /repo && git worktree add /tmp/work/feat/my-task feat/my-task")
# 3. Switch main back (worktree takes the branch)
terminal(command="cd /repo && git checkout main")
# 4. Dispatch subagent (blocking)
delegate_task(
    goal="Implement feature X",
    context="""FULL context including:
    - Worktree path: /tmp/work/feat/my-task/
    - .venv path: /repo/.venv/
    - Files to read, files to create, files to modify
    - Verification commands with expected outcomes
    - Git commands: commit, push, PR creation
    """,
    toolsets=["terminal", "file"],
)
# 5. After completion: create + merge PR
terminal(command="cd /tmp/work/feat/my-task && git push origin HEAD && gh pr create --fill")
terminal(command="cd /repo && gh pr merge <N> --squash --delete-branch")
# 6. Clean up worktree
terminal(command="cd /repo && git worktree remove /tmp/work/feat/my-task")
```

#### Cost Tracking

Every delegate_task returns `total_cost_usd`. Track it:
```python
import json
from pathlib import Path
cost_file = Path(".hermes/cost-tracking.json")
tracking = json.loads(cost_file.read_text()) if cost_file.exists() else []
tracking.append({"task": "feat/my-task", "cost": result.total_cost_usd, "date": "..."})
cost_file.write_text(json.dumps(tracking, indent=2))
```

### Mode B: 2-Stage Review (Complex Tasks)

Use this when correctness is critical, tasks are complex, or the implementation could easily miss the spec.

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality) when using Mode B
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues
- **Use `git config --global --unset http.proxy`** to fix proxy issues — this makes git fall back to `$http_proxy` env var (still broken). Use `git config --global http.proxy ""` (empty string) instead, which overrides the env var deterministically.

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

### Worktree + DelegateTask Integration

**Key pitfall:** When you create a worktree for a subagent and dispatch via `delegate_task`, the subagent runs in its own isolated terminal session. Its working directory is the project root (main checkout), NOT the worktree. Files written by the subagent end up in the main checkout.

**Resolution — Strategy A (stash-pop, recommended):**
```python
# After subagent completes:
terminal("cd /repo && git stash")              # stash files from main
terminal("cd /tmp/work/feat/my-task && git stash pop")  # apply in worktree
terminal("cd /tmp/work/feat/my-task && git add . && git commit -m ...")
terminal("cd /tmp/work/feat/my-task && git push origin feat/my-task")
```

**Strategy B — Explicit worktree path in prompt:**
Include the worktree path in the subagent's context so it writes there directly:
```
ALL file writes must go under /tmp/bgg-worktree/feat/my-task/
e.g. write_file(path="/tmp/bgg-worktree/feat/my-task/src/module.py", ...)
```

**Gating check after subagent completion:**
```python
# Verify files exist in worktree before merging
assert os.path.exists(f"{worktree}/src/module.py"), "File missing!"
```

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/policy-data-import.md`** — Data import from research documents (.md files) into production database. Covers API discovery, field mapping, relevance tagging, and pitfalls. Load when a subagent's task involves moving research output into a running system.
- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.
- **`references/parallel-independent-tasks.md`** — Pattern for dispatching multiple subagents on disjoint code paths in a single checkout, with conflict-resolution steps for post-batch test failures.

References adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
