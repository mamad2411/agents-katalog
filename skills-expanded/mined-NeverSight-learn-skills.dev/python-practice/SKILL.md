---
name: python-practice
description: >
  Generate adaptive Python coding exercises for broad practical Python fluency:
  fundamentals, OOP, standard library, testing, CLIs, automation, backend services,
  FastAPI, Flask, AWS automation, data handling, and production scripting. Use whenever
  the user wants to practice Python, learn Python concepts, review Python code, debug
  Python programs, build backend APIs, automate AWS with Python, or mentions Python
  exercises, challenges, pytest, FastAPI, Flask, boto3, scripts, CLIs, or automation.
  Exercises must be created inside dated folders in /home/laborant/repos/python-practice.
  The skill tracks recurring mistakes and clarifying questions in the root learning-log.md;
  no progress tracker script or dynamic progress database is used.
---

# Python Practice — Practical Fluency

Generate Python exercises that build practical language fluency first, then apply
it to backends, CLIs, automation, AWS workflows, testing, and production-style
projects.

The center of gravity is **becoming fluent enough to build useful things in
Python**. FastAPI, Flask, and AWS automation are preferred application tracks,
not the whole curriculum.

Each normal practice request produces **3 exercises** as separate `.py` files or
small Python packages, depending on topic. Use the root learning log to choose
useful practice, but do not run a progress tracker or maintain a hidden progress
database.

All user exercise work lives in this fixed repo:

```text
/home/laborant/repos/python-practice
```

Do not create Python practice exercises elsewhere unless the user explicitly
gives a different path.

## When To Use

- User wants Python practice, exercises, challenges, code review, or debugging.
- User asks about functions, classes, typing, pytest, files, JSON, HTTP, CLIs,
  APIs, FastAPI, Flask, boto3, AWS automation, backend work, or scripts.
- User asks for backend Python learning, automation skill, AWS scripting, or
  open-source Python contribution prep.
- User says "I'm stuck", "review my solution", "make it harder/easier", or asks
  clarifying questions while solving Python exercises.

## Workflow

### Step 1: Ask For Topic If Missing

If the user did not specify a topic, offer this menu:

```text
Which Python area do you want to practice?

1. Foundations       — syntax, functions, data structures, files, exceptions
2. OOP + Design      — classes, dataclasses, protocols, composition, package boundaries
3. Standard Library  — pathlib, json, csv, datetime, collections, itertools, logging, argparse
4. Testing + Quality — pytest, fixtures, mocks, typing, lint-friendly design
5. Backend Python    — HTTP, FastAPI, Flask, validation, middleware, service boundaries
6. Automation + AWS  — boto3-shaped clients, retries, pagination, IAM-safe scripts, CLIs
7. Data + Utilities  — pandas-style data handling, CSV/JSON transforms, reporting scripts

Pick one, or name a specific thing like "FastAPI dependencies" or "boto3 pagination".
```

Skip this step when the user names a topic directly.

### Step 2: Choose Learning Mode

If the user does not specify a mode, use `batch`.

Modes:
- `batch`: 3 exercises. Default for steady practice.
- `drill`: 1 small focused task for one concept or repeated mistake.
- `debug`: broken production-ish code plus tests.
- `applied`: realistic backend, CLI, AWS, or automation task.
- `pr-simulation`: read a small existing package, patch a bug, explain tradeoffs.
- `design-review`: choose package boundaries, types, dependencies, and error
  behavior before coding.
- `capstone`: multi-step project from the capstone ladder.

Use the mode to control scope. Do not force 3 exercises when the user asks for a
small drill, review, or project-style task.

### Step 3: Prepare Practice Workspace

Use `/home/laborant/repos/python-practice` as the exercise repo.

If it does not exist, create it as a git repo with:
- `README.md`
- `learning-log.md`
- `.gitignore`

When creating exercises, put them in a date folder under that repo. Folder names
use this format:

```text
D-mmm-YY
```

Examples:
- `3-may-26`
- `30-apr-26`
- `12-jun-26`

Use lowercase English month abbreviations: `jan`, `feb`, `mar`, `apr`, `may`,
`jun`, `jul`, `aug`, `sep`, `oct`, `nov`, `dec`.

Rules:
- On a new day, create that day's folder.
- If the user asks for more exercises on the same day, add more exercises to the
  same folder.
- Number new exercises after existing ones in that folder.
- Keep the root `learning-log.md` as durable memory across days.
- Read earlier date folders when useful, especially when the log references them.
- Commit exercise additions in the `python-practice` repo unless the user asks not to.

### Step 4: Read Learning Context

Open `/home/laborant/repos/python-practice/learning-log.md` if it exists;
otherwise copy the starter shape from `references/learning-log.md`.

Scan:
- Recurring mistakes
- Clarifying questions the user keeps asking
- Concepts already comfortable
- Domain goals and current focus
- Last exercise batch
- Prior dated exercise folders

Do not use `scripts/progress_tracker.py`, `progress.json`, or any hidden scoring
system. Update the learning log directly after reviews and after important
clarifying questions.

### Step 5: Choose Difficulty And Domain

Use `references/topic-catalog.md`.
Use `references/practice-tracks.md` when the user wants backend, FastAPI, Flask,
AWS automation, CLI/tooling, data utility, or capstone direction.

Default progression:
- Difficulty 1/5: core language and small single-file tasks
- Difficulty 2/5: functions, modules, tests, exceptions, typing, and standard library
- Difficulty 3/5: realistic scripts, CLIs, backend handlers, AWS automation boundaries
- Difficulty 4/5: project-style tasks using FastAPI, Flask, AWS automation, or packages
- Difficulty 5/5: capstone-style package or service work with phased tests

Adjust from the learning log:
- Repeated syntax/type confusion -> lower difficulty, isolate concept.
- Repeated "why this abstraction?" questions -> include design-review or package-boundary task.
- Repeated testing confusion -> include pytest fixture/mock drill.
- Strong fundamentals -> shift toward backend, automation, AWS, and project-style exercises.
- User asks for challenge -> use Difficulty 3/5 or 4/5 with tests and realistic constraints.

### Step 6: Generate Exercises

Read `references/exercise-templates.md` before creating files.

Default batch:
- 1 completion exercise
- 1 debugging exercise
- 1 applied backend/automation/framework exercise with tests

Adapt batch mix:
- If user struggles with bugs -> 2 debugging exercises.
- If user asks many clarifying questions -> 1 concept drill, 1 guided completion, 1 applied task.
- If user is advanced -> 3 applied tasks across backend, AWS automation, testing, and utilities.

Mode-specific output:
- `drill`: 1 file plus test.
- `debug`: 1 broken file plus test, or 3 bugs in one focused package.
- `applied`: 1 small module/package with README and tests.
- `pr-simulation`: 1 small existing-style package with failing test and review prompt.
- `design-review`: markdown prompt plus skeleton package only if useful.
- `capstone`: module with README, phased tests, and learning-log checkpoint.

File naming:

```text
NN_<topic>_<subtopic>_<type>.py
NN_<topic>_<subtopic>_<type>_test.py
```

Start `NN` from `01` in each date folder. If the date folder already has
exercises, continue from the highest existing number.

For package-level exercises, create:

```text
<date-folder>/NN_<topic>_<subtopic>/
  README.md
  pyproject.toml
  src/<package_name>/...
  tests/...
```

Every exercise should include:
- Short header comment/docstring with topic, difficulty, domain, and source inspiration.
- Clear goal.
- `TODO` markers for completion tasks or intentionally broken code for debug tasks.
- Tests that initially fail.
- Realistic backend/AWS/framework framing when useful.
- No hidden answer in comments.
- No full solution unless the user explicitly asks for one.

Prefer standard library first. Use FastAPI, Flask, boto3, pandas, or other
libraries only when the exercise specifically needs them; otherwise simulate
boundaries with small functions or protocols to keep setup light.

### Step 7: Verify Exercises Fail Correctly

Run from the date folder or specific package folder:

```bash
python -m pytest
```

For single-file exercises with inline tests, run:

```bash
python <exercise_file.py>
```

Expected: generated exercises should fail because the user has work to do. If
any exercise passes before the user edits it, make the missing work explicit and
re-run.

Prefer pytest for backend, AWS automation, and framework work because production
Python benefits from repeatable tests.

### Step 8: Deliver To User

Use this structure:

```text
Created <count> Python exercise(s) on <topic> at Difficulty <N>/5.

Focus:
- <why these exercises were selected from learning-log.md>

Files:
- <path> — <one-line task>
- <path> — <one-line task>
- <path> — <one-line task>

Run: cd /home/laborant/repos/python-practice/<date-folder> && python -m pytest
Send me your solution when ready.
```

### Step 9: Review User Solutions

When user asks for review:
- Run formatting/linting only if configured in the exercise. Do not invent a new toolchain.
- Run `python -m pytest`.
- For single-file exercises, run `python <exercise_file.py>` if that is the exercise contract.
- Read `references/review-guide.md`.
- Review correctness first, then idiomatic Python, then backend/AWS/framework production concerns.

Review should call out:
- Passing/failing tests
- Bugs or edge cases
- Idiomatic Python improvements
- Type hints and API boundaries
- Error handling
- Test quality
- Backend/framework/AWS production relevance when applicable

### Step 10: Update Learning Log

After each review, update `/home/laborant/repos/python-practice/learning-log.md`
manually.

Record:
- Date folder
- Exercises completed
- Mistakes observed
- Clarifying questions asked
- Concepts now stronger
- Concepts still weak
- Suggested next batch

Mistake examples:
- `mutable-default-arg`
- `missing-return`
- `type-confusion`
- `exception-swallowed`
- `path-string-not-pathlib`
- `mock-too-broad`
- `fixture-scope-confusion`
- `fastapi-dependency-confusion`
- `flask-global-state`
- `boto3-pagination-missing`
- `aws-retry-missing`
- `iam-action-too-broad`
- `not-pythonic-loop`

Clarifying question examples:
- "When should I use a dataclass?"
- "When do I mock versus use a fake?"
- "Why use pathlib here?"
- "Where should validation live in FastAPI?"
- "When should I use Flask blueprints?"
- "How do I handle boto3 pagination?"
- "What makes this script safe to rerun?"

If the same clarifying question category appears twice, the next batch must
include a contrast exercise that forces the distinction.

### Step 11: Interactive Help

- "I'm stuck" -> Give a hint, not the solution. Tie hint to prior mistakes.
- "Show me the solution" or equivalent explicit request -> provide the smallest complete solution and explain the key idea.
- "Explain this concept" -> Explain with a small Python example and one practical use case.
- "Why this exercise?" -> Point to learning-log patterns and target domain.
- "Make it harder" -> Add tests for edge cases, failure paths, validation, idempotency, or mocks.
- "Make it easier" -> Reduce to one concept and remove external dependencies.
- "Review this like backend Python" -> Emphasize boundaries, validation, error handling, tests, and API shape.
- "Prepare me for AWS automation" -> Use boto3-shaped clients, pagination, retries, idempotency, and dry-run patterns.
- "Help me build anything in Python" -> Rotate through foundations, packages, tests, CLIs, backend, automation, and applied projects.

## Capstone Ladder

Offer capstones when the user wants project-style practice or has completed
several batches successfully.

1. `python-toolbox`: file, JSON, CSV, pathlib, argparse, logging, and tests.
2. `automation-runner`: idempotent scripts, dry-run behavior, retries, and reports.
3. `flask-service`: small Flask API with blueprints, validation, tests, and app factory.
4. `fastapi-service`: FastAPI app with dependencies, Pydantic models, routers, and tests.
5. `aws-inventory-tool`: boto3-shaped collectors with pagination, retries, filtering, and dry-run planning.
6. `backend-worker`: queue-shaped worker with retries, structured errors, and persistence boundary.

Keep capstones small enough to finish incrementally. Each phase should have tests
and a learning-log checkpoint.

## Open Source Readiness

When the learning log shows repeated success with:
- Functions, data structures, and exceptions
- OOP and package boundaries
- Type hints and protocols
- pytest fixtures and mocks
- Backend validation and error handling
- AWS automation safety patterns
- Idiomatic Python style

Suggest reading and modifying small issues in Python open-source repositories.
Start with docs/tests/internal utilities before touching core runtime paths.
