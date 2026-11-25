---
name: go-practice
description: >
  Generate adaptive Go coding exercises for developers who want broad practical Go
  fluency: writing correct programs, building backends, creating CLIs/tools, working
  with concurrency, and eventually building Kubernetes/CNCF ecosystem tooling. Use
  whenever the user wants to practice Go, learn Go concepts, review Go code, debug Go
  programs, build backend Go skills, prepare for Kubernetes ecosystem work, or mentions
  Go exercises, goroutines, channels, context, HTTP services, CLI tools, controllers,
  operators, cloud tooling, distributed systems, or CNCF projects. The skill tracks
  recurring mistakes and clarifying questions in /home/laborant/repos/go-practice/
  learning-log.md so future exercise batches adapt to the user's actual learning
  pattern. Exercises must be created inside dated folders in the go-practice repo.
---

# Go Practice — Adaptive Cloud-Native Learning

Generate Go exercises that build practical language fluency first, then apply it
to backends, CLIs, cloud tooling, CI/CD systems, Kubernetes/CNCF projects, and
distributed-system work.

The center of gravity is **becoming fluent enough to build anything in Go**.
Kubernetes/CNCF work is a preferred specialization track, not the only path.

Each normal practice request produces **3 exercises** as separate `.go` files or
small Go modules, depending on the topic. Mix code completion, debugging, and
design tasks based on the user's learning log.

All user exercise work lives in this fixed repo:

```text
/home/laborant/repos/go-practice
```

Do not create Go practice exercises elsewhere unless the user explicitly gives a
different path.

Use Go by Example and official Go documentation as the source baseline:
- Go by Example for concise runnable examples across syntax, concurrency,
  testing, CLI, HTTP, files, context, and process handling.
- A Tour of Go for language foundations, methods/interfaces, generics, and
  concurrency foundations.
- Effective Go for idioms: `gofmt`, short names, package naming, small
  interfaces, explicit error handling, and simple control flow.

## When To Use

- User wants Go practice, Go exercises, Go challenges, or Go code review.
- User asks about goroutines, channels, context, interfaces, errors, modules,
  testing, HTTP servers, CLIs, Kubernetes controllers, operators, CI/CD tools,
  cloud APIs, or distributed systems in Go.
- User asks for backend Go learning, practical Go fluency, CNCF project readiness,
  or open-source Go contribution prep.
- User says "I'm stuck", "review my solution", "make it harder/easier", or
  asks clarifying questions while solving Go exercises.

## Workflow

### Step 1: Ask For Topic If Missing

If the user did not specify a topic, offer this menu:

```text
Which Go area do you want to practice?

1. Foundations       — syntax, slices, maps, structs, methods, interfaces, errors
2. Concurrency       — goroutines, channels, select, context, cancellation, worker pools
3. Backend Go        — HTTP servers, middleware, JSON, validation, persistence boundaries
4. Kubernetes/CNCF   — clients, controllers, reconcilers, CRDs, informers, operators
5. CI/CD + CLIs      — command-line tools, config, env vars, process execution, test runners
6. Distributed Go    — retries, idempotency, rate limits, queues, leases, observability

Pick one, or name a specific thing like "context cancellation" or "Kubernetes reconciler".
```

Skip this step when the user names a topic directly.

### Step 2: Choose Learning Mode

If the user does not specify a mode, use `batch`.

Modes:
- `batch`: 3 exercises. Default for steady practice.
- `drill`: 1 small focused task for one concept or repeated mistake.
- `debug`: broken production-ish code plus tests.
- `applied`: realistic backend, CLI, cloud, or CNCF task.
- `pr-simulation`: read a small existing package, patch a bug, explain tradeoffs.
- `design-review`: choose package boundaries, interfaces, and failure behavior
  before coding.
- `capstone`: multi-step project from the capstone ladder.

Use the mode to control scope. Do not force 3 exercises when the user asks for a
small drill, review, or project-style task.

### Step 3: Prepare Practice Workspace

Use `/home/laborant/repos/go-practice` as the exercise repo.

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
- Keep the root `learning-log.md` as the durable memory across days.
- Read earlier date folders when useful, especially when the log references them.
- Commit exercise additions in the `go-practice` repo unless the user asks not to.

### Step 4: Read Learning Context

Open `/home/laborant/repos/go-practice/learning-log.md` if it exists; otherwise
copy the starter shape from `references/learning-log.md`.

Scan:
- Recurring mistakes
- Clarifying questions the user keeps asking
- Concepts already comfortable
- Domain goals and current focus
- Last exercise batch
- Prior dated exercise folders

If the user is working in a specific exercise directory, prefer that directory's
local notes for that exercise, but still update the root `learning-log.md`.

Do not use a progress tracker script. Update the learning log directly after
reviews and after important clarifying questions.

### Step 5: Choose Difficulty And Domain

Use `references/topic-catalog.md`.
Use `references/practice-tracks.md` when the user wants a backend, CLI/tooling,
cloud, distributed-system, Kubernetes, CNCF, or capstone direction.

Default progression:
- Difficulty 1/5: core language and small single-file tasks
- Difficulty 2/5: package boundaries, tests, errors, context, interfaces, and small CLIs/services
- Difficulty 3/5: realistic backend/CNCF tasks with concurrency, API boundaries, and failure modes
- Difficulty 4/5: project-style tasks modeled after Kubernetes/CNCF patterns
- Difficulty 5/5: capstone-style modules with phased tests and production constraints

Adjust from the learning log:
- Repeated syntax or type confusion -> lower difficulty, isolate the concept.
- Repeated "why this interface?" questions -> include design explanation and interface-focused task.
- Repeated concurrency confusion -> include timeline comments, cancellation paths, and race checks.
- Strong fundamentals -> shift toward backend, CNCF, and distributed-system exercises.
- User asks for challenge -> use Difficulty 3/5 or 4/5 with tests and realistic constraints.

### Step 6: Generate Exercises

Read `references/exercise-templates.md` before creating files.

Default batch:
- 1 completion exercise
- 1 debugging exercise
- 1 cloud-native/backend design exercise with tests

Adapt batch mix:
- If user struggles with bugs -> 2 debugging exercises.
- If user asks many clarifying questions -> 1 concept drill, 1 guided completion, 1 applied task.
- If user is advanced -> 3 applied tasks across backend/CNCF/distributed systems.

Mode-specific output:
- `drill`: 1 file plus test.
- `debug`: 1 broken file plus test, or 3 bugs in one focused package.
- `applied`: 1 small module with README and tests.
- `pr-simulation`: 1 small existing-style package with failing test and review prompt.
- `design-review`: markdown prompt plus skeleton package only if useful.
- `capstone`: module with README, phased tests, and learning-log checkpoint.

File naming:

```text
NN_<topic>_<subtopic>_<type>.go
NN_<topic>_<subtopic>_<type>_test.go
```

Start `NN` from `01` in each date folder. If the date folder already has
exercises, continue from the highest existing number.

For module-level exercises, create:

```text
<date-folder>/NN_<topic>_<subtopic>/
  go.mod
  README.md
  <package>.go
  <package>_test.go
```

Every exercise should include:
- Short header comment with topic, difficulty, domain, and source inspiration.
- Clear goal.
- `TODO` markers for completion tasks or `BUG` markers for debugging tasks.
- Tests that initially fail.
- Realistic backend/CNCF framing when useful.
- No hidden answer in comments.
- No full solution unless the user explicitly asks for one.

Prefer standard library first. Use Kubernetes or CNCF libraries only when the
exercise specifically needs them; otherwise simulate boundaries with small
interfaces to keep setup light.

### Step 7: Verify Exercises Fail Correctly

Run:

```bash
gofmt -w .
go test ./...
```

Expected: generated exercises should fail because the user has work to do.
If any exercise passes before the user edits it, make the missing work explicit
and re-run.

For single-file `package main` exercises without tests, run:

```bash
go run <file>.go
```

Run commands from the date folder or from the specific module folder, depending
on exercise layout. Prefer `go test` when possible because backend/CNCF work
benefits from fast, repeatable tests.

### Step 8: Deliver To User

Use this structure:

```text
Created <count> Go exercise(s) on <topic> at Difficulty <N>/5.

Focus:
- <why these exercises were selected from learning-log.md>

Files:
- <path> — <one-line task>
- <path> — <one-line task>
- <path> — <one-line task>

Run: cd /home/laborant/repos/go-practice/<date-folder> && go test ./...
Send me your solution when ready.
```

### Step 9: Review User Solutions

When user asks for review:
- Run `gofmt -w .`.
- Run `go test ./...`.
- Run `go test -race ./...` for concurrency exercises.
- Read `references/review-guide.md`.
- Review correctness first, then idiomatic Go, then backend/CNCF production concerns.

Review should call out:
- Passing/failing tests
- Bugs or edge cases
- Idiomatic Go improvements
- Error handling and context behavior
- API boundaries and interface size
- Concurrency safety
- Production relevance for backend/CNCF work

### Step 10: Update Learning Log

After each review, update `/home/laborant/repos/go-practice/learning-log.md`
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
- `nil-map-write`
- `slice-aliasing`
- `loop-variable-capture`
- `pointer-vs-value-receiver`
- `interface-too-large`
- `ignored-error`
- `context-not-propagated`
- `goroutine-leak`
- `channel-close-owned-by-receiver`
- `data-race`
- `test-flakiness`
- `kubernetes-reconcile-not-idempotent`
- `retry-without-backoff`
- `missing-timeout`

Clarifying question examples:
- "When should I use pointer receivers?"
- "Why pass context first?"
- "Who closes this channel?"
- "Why define an interface in the consumer package?"
- "What makes a reconciler idempotent?"
- "When should I mock Kubernetes client behavior?"

Use these entries to adapt future batches.

If the same clarifying question category appears twice, the next batch must
include a contrast exercise that forces the distinction. Examples:
- Repeated receiver-choice questions -> compare pointer and value receiver tasks.
- Repeated context questions -> include cancellation and timeout behavior.
- Repeated channel ownership questions -> include producer/consumer close rules.
- Repeated interface-placement questions -> include consumer-owned interface design.
- Repeated reconciler questions -> include desired vs observed state and idempotency.

### Step 11: Interactive Help

- "I'm stuck" -> Give a hint, not the solution. Tie hint to prior mistakes.
- "Show me the solution" or equivalent explicit request -> provide the smallest complete solution and explain the key idea.
- "Explain this concept" -> Explain with a small Go example and one cloud-native use case.
- "Why this exercise?" -> Point to learning-log patterns and target domain.
- "Make it harder" -> Add tests for cancellation, race safety, idempotency, or edge cases.
- "Make it easier" -> Reduce to single concept and remove external dependencies.
- "Review this like CNCF code" -> Emphasize API boundaries, context, logs, tests, and failure modes.
- "Prepare me for Kubernetes projects" -> Use reconciler, client, cache, informer, and CRD-shaped exercises.
- "Help me build anything in Go" -> Rotate through foundations, packages, tests,
  backend, CLI/tooling, concurrency, and applied projects.

## Capstone Ladder

Offer capstones when the user wants project-style practice or has completed
several batches successfully.

1. `go-toolbox`: small CLI utilities for parsing flags, env, JSON, YAML-like
   structs, files, and exit codes.
2. `backend-health-api`: HTTP service with handlers, validation, timeouts,
   graceful shutdown, and table-driven tests.
3. `ci-job-runner`: concurrent job runner with context cancellation, logs,
   artifacts, retries, and deterministic tests.
4. `cloud-resource-sync`: desired/observed-state sync loop with idempotency,
   patch planning, and retry/backoff.
5. `mini-controller`: Kubernetes-shaped reconciler with queue, status
   conditions, finalizer-like cleanup, and race-safe workers.

Keep capstones small enough to finish incrementally. Each phase should have
tests and a learning-log checkpoint.

## Open Source Readiness

When the learning log shows repeated success with:
- Interfaces and package boundaries
- Context cancellation and timeouts
- Error wrapping and observability
- Table-driven tests
- Race-free concurrency
- Idempotent reconcile loops
- CLI/backend ergonomics

Suggest reading and modifying small issues in CNCF Go repositories. Start with
docs/tests/internal packages before touching controller or distributed paths.
