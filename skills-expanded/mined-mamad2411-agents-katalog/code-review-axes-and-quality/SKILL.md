---
name: code-review-axes-and-quality
description: Use when a change needs a complete, actionable, and resumable ten-axis review before merge
---

# Code Review Axes and Quality

Use this skill for a structured review of a commit range, feature, module, or
working tree. It uses delegation mode as the execution layer and produces
durable plans instead of a chat-only opinion.

## Relevant companion skill

Use `delegation-mode` as the execution layer for this skill. Before creating
or running a review plan, read:

```text
../delegation-mode/SKILL.md
```

Follow its worker contract, stable task IDs, `.agents/plans/` output convention,
sequential/parallel selection rules, validated result-file marker, and
cross-session `DONE_IDS` resume procedure. This skill defines review quality;
`delegation-mode` defines how the review is dispatched and resumed. The
executable review template also validates every axis artifact and rejects a
final approval that ignores unresolved CRITICAL or HIGH findings.

The review template uses the shared `delegation-mode` validation core for plan
identity, safe paths, `DONE_IDS`, frontmatter, completion markers, and durable
file checks. Review-specific axis requirements and verdict/blocker checks remain
local to this template.

## Review standard

Review every change before it is merged, but keep the approval bar
proportional: approve a change when it improves overall code health and has no
unresolved blocking issue. Do not block on personal style preferences or
perfect-code expectations. Do not rubber-stamp because tests pass or because
the author is confident.

Every finding must be evidence-based, actionable, and ordered by leverage:
correctness and security first, then structural regressions and missed
simplifications, then lower-impact concerns. If a structural problem is
reported, propose the move that fixes it rather than only describing that the
code is complex.

## Fixed review axes

Run all ten axes, including axes with no findings:

| # | Axis | Focus |
| --- | --- | --- |
| 1 | Correctness | Bugs, edge cases, incorrect assumptions, regressions |
| 2 | Performance | Bottlenecks, unnecessary work, latency, memory, hot paths |
| 3 | Scalability | Failure or degradation under growth, concurrency, larger inputs |
| 4 | Infrastructure | Existing project wiring, boundaries, operations |
| 5 | Library hygiene | Dependencies, supported APIs, versions, usage |
| 6 | Security | Input handling, auth, secrets, injection, SSRF, XSS, abuse |
| 7 | Data integrity and concurrency | Atomicity, idempotency, races, ordering, retries |
| 8 | Observability | Logs, metrics, traces, alerts, diagnostics, failure visibility |
| 9 | Maintainability | Coupling, cohesion, change risk, duplication, architecture |
| 10 | Readability | Naming, control flow, local comprehension, cognitive load |

Maintainability and readability are separate: maintainability evaluates whether
future changes are safe and localized; readability evaluates whether current
behavior is understandable without reconstructing hidden intent.

Every finding includes:

- what is wrong;
- file and line or symbol;
- why it matters;
- recommended fix;
- severity: `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.

Every axis result also includes the exact scope, assigned axis, and actual
verification evidence. An empty axis explicitly states that no findings were
found. A marker-only file is not a completed review result.

An empty axis is complete only when it states that the reviewed scope had no
findings.

### Axis guidance

Use the following lenses while staying within each assigned axis:

- **Correctness:** Compare behavior with the specification and tests. Check
  null, empty, boundary, retry, timeout, and error paths, not only the happy
  path. Look for state inconsistencies, off-by-one errors, and regressions.
- **Performance:** Check N+1 queries, unbounded work or fetching, avoidable
  synchronous operations, hot-path allocations, and UI re-render costs.
- **Scalability:** Check behavior as data, traffic, tenants, concurrency, and
  payload size grow. Look for resource limits, queue/backpressure behavior,
  contention, and fan-out.
- **Infrastructure:** Check project wiring, deployment/runtime assumptions,
  configuration, migrations, operational boundaries, rollback behavior, and
  failure recovery.
- **Library hygiene:** Prefer the existing stack and standard library. Review
  new dependencies for maintenance, license, vulnerability, bundle/runtime
  impact, supported APIs, changelog/migration notes, and lockfile changes.
- **Security:** Treat user input, external data, logs, and configuration as
  untrusted at boundaries. Check validation, authorization, secrets, injection,
  XSS, SSRF, abuse controls, and dependency supply-chain risk.
- **Data integrity and concurrency:** Check atomicity, idempotency, ordering,
  retries, races, transaction boundaries, duplicate work, and partial failure.
- **Observability:** Check useful structured logs, metrics, traces, alerts,
  diagnostics, and error visibility for important success and failure paths.
- **Maintainability:** Look for coupling, duplication, feature logic in shared
  modules, circular dependencies, and abstractions that relocate rather than
  reduce complexity. Question unclear type boundaries and silent fallbacks.
- **Readability:** Check names, control flow, local comprehension, dead code,
  comments, file size, and conditional branches bolted onto unrelated flows.

## Review protocol

Use this order for every review:

1. **Understand intent.** Read the task/spec, relevant plans, current checkout,
   and recent commits. State the expected behavior change and exact scope.
2. **Read tests first.** Identify tests for the change, check that they test
   behavior rather than implementation details, and note missing regression or
   edge-case coverage.
3. **Read complete implementation context.** Do not review only diff hunks.
   Trace callers, canonical helpers, type boundaries, configuration, and
   dependencies needed to understand the behavior.
4. **Run all ten axes.** Keep axes separate, including axes with no findings.
   Do not repeat the same finding across axes unless the impact is genuinely
   different; the final report will deduplicate overlaps.
5. **Verify the verification story.** Record tests, lint, type checks, builds,
   manual checks, screenshots for UI changes, benchmarks, and dependency
   checks that were actually run. Do not claim a check that was not run.
6. **Give a verdict.** Approve only when no unresolved `CRITICAL` or `HIGH`
   finding remains. If lower-severity work is deferred, record the rationale,
   owner/next action when known, and residual risk.

## Finding severity and status

Use these severity meanings consistently:

| Severity | Meaning | Default decision |
| --- | --- | --- |
| `CRITICAL` | Exploitable security issue, data loss, broken core behavior, or an immediate production blocker | Blocks approval |
| `HIGH` | Likely bug, serious security/contract issue, or structural regression with material impact | Normally blocks approval |
| `MEDIUM` | Material maintainability, performance, scalability, observability, or correctness gap with bounded impact | Fix before merge when in scope, otherwise document deferral |
| `LOW` | Limited-impact improvement, polish, or localized cleanup | Optional unless project rules say otherwise |

Use the existing `Status` column for the action state:
`required`, `recommended`, `optional`, `accepted-risk`, or `resolved`. A
finding must not be labeled `resolved` unless the reviewed scope contains
evidence that it was fixed and verified.

## Structural remedies

When the issue is structural, name a concrete remedy. Prefer the option that
removes moving pieces:

- replace a conditional chain with a typed model or explicit dispatcher;
- collapse duplicate branches into one clear flow;
- separate orchestration from business logic;
- move feature-specific logic into the package that owns it;
- reuse the canonical helper instead of adding a near-duplicate;
- make a type boundary explicit so downstream branching disappears;
- delete a pass-through wrapper that adds indirection without clarifying an API;
- extract a helper or split a large file into focused modules.

Do not recommend a broad abstraction simply because code is repeated once.
Generalize when a real shared invariant or third use case justifies it.

## Change sizing and decomposition

Review the resulting file size and change size, not only whether the diff
passes tests:

```text
~100 changed lines   → easy to review
~300 changed lines   → acceptable for one logical change
~1000 changed lines  → split the change
~1000 total lines in one file → inspection signal; consider decomposition
```

These are inspection signals, not automatic rejection rules. Recommend stack,
by-file-group, horizontal, or vertical decomposition when a change is too
large. Separate refactoring from new behavior unless a small cleanup is
necessary to make the feature safe.

## Dead code and dependency hygiene

After refactors, identify unreachable or unused code explicitly. Axis workers
must not silently delete uncertain code; list the symbol and why it appears
unused, then recommend a separate removal or a verified cleanup decision.

For dependency changes, check whether the existing stack already solves the
problem, package maintenance and license, known vulnerabilities, bundle or
runtime impact, supported APIs, changelog/migration notes, and the lockfile
diff. Prefer one dependency upgrade per logical change and never hand-edit a
lockfile.

## Establish scope before dispatch

Before creating the plan:

1. Read `.agents/chats/current.md`, when present.
2. Read relevant active or reference plans.
3. Inspect the current checkout and recent commits.
4. Determine the exact review range or working-tree scope.
5. Read project rules and relevant memory topics.

Verify saved handoffs against the current checkout. Never trust a stale branch,
file, commit, or validation claim.

## Run the reusable plan

Copy `scripts/review-plan.template.js` to:

```text
.agents/plans/YYYY-MM-DD-<slug>.js
```

Fill in `DATE`, `SLUG`, `PROJECT_CONTEXT`, and the review scope. Choose:

```js
const MODE = "sequential"; // or "parallel"
```

Each axis writes one flat plan file:

```text
YYYY-MM-DD-<slug>-01-correctness.md
...
YYYY-MM-DD-<slug>-10-readability.md
YYYY-MM-DD-<slug>-FINAL.md
```

Axis workers must be `config: { $kind: "general" }` because they write files.
They must read complete relevant files, avoid modifying application source, and
include the exact marker in the file and end only after writing their exact
file:

```text
FILE_WRITTEN: <exact-path>
```

The runner treats a missing marker as unresolved and does not aggregate until
all ten axes confirm.

Each axis result must include:

- exact reviewed scope and relevant evidence;
- the assigned axis and explicit no-findings statement when empty;
- findings with severity, location, impact, recommended fix, and status;
- verification performed or unavailable;
- structural remedy, dead-code note, or dependency note when relevant;
  - `FILE_WRITTEN: <exact-path>` as the final non-empty line in the file and
    response. The dispatcher confirms the file itself, not the response alone.

## Resume across sessions

After an interrupted run:

```bash
ls .agents/plans/YYYY-MM-DD-<slug>-*.md 2>/dev/null
```

Inspect the output files and update `DONE_IDS` with only confirmed axis IDs:

```js
const DONE_IDS = [
  "01-correctness",
  "02-performance",
];
```

Rerun the complete plan. It skips those IDs and dispatches only missing axes.
Set `FINAL_DONE = true` only after verifying the final report exists and is
complete. Do not infer completion from chat silence or a partial file.

## Final report

The final plan deduplicates findings, sorts the master table by severity,
groups concrete priority work items, and gives the next agent enough context
to act. It must also include:

- a concise context and intent summary;
- a verdict: `APPROVE`, `APPROVE_WITH_FOLLOW_UP`, or `REQUEST_CHANGES`;
- unresolved blockers and deferred lower-severity risks;
- verification evidence and explicit gaps;
- change-size/decomposition, dependency, and dead-code conclusions when
  applicable.

It does not change application code.

After the review:

1. Verify all ten axis files and the final report exist.
2. Check frontmatter and relative links.
3. Run applicable tests, lint, type checks, compilation, and build.
4. Run `git diff --check`.
5. Record verification and unresolved risks in the final plan.
6. Confirm no `CRITICAL` or `HIGH` finding is marked `resolved` without
   evidence.
7. Do not claim approval while unresolved `CRITICAL` or `HIGH` findings remain.
   The template enforces this postcondition; the final report must contain a
   machine-readable `**Verdict:**` line.