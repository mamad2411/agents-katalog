---
name: safe-code-agent
description: A coding skill for complex or risky coding tasks such as debugging, multi-file changes, refactors, architecture-sensitive work, unclear root causes, contract/fallback logic, negative tests, and high-risk changes. Use it to reduce over-editing, context loss, hallucinated certainty, and unverified changes.
---

# safe-code-agent v0.2.2

## Core Loop

Goal -> Inspect -> Simulate -> Patch minimally -> Verify -> Report uncertainty

## Compression Rule

Advanced docs are optional and must not be loaded for every task.

Do not load or apply every section for every task.

Start with:

1. Mode Selection
2. Gate Router
3. Pre-Approval Planning Report when approval is needed
4. only the triggered gates
5. Evidence Report

Ignore untriggered gates unless risk changes during the task.

Always-on guidance should stay short. Detailed gates are conditional.

## Risk Signal Router

Do not expect the user to know which advanced doc to load.

During the task, detect risk signals and recommend the relevant advanced doc.

### Runtime Enforcement trigger

Recommend `docs/advanced/runtime-enforcement.md` when any are true:

- the task touches auth, payment, data deletion, migration, persistence, public API, or security-sensitive behavior
- the agent claims tests/build/lint/commands passed but visible output is missing
- correctness depends on actual command output, CI, tool logs, or terminal output
- verification is required but only inferred evidence is available

Recommended message:

```text
Risk signal detected: verification requires auditable output.
Recommended advanced doc: docs/advanced/runtime-enforcement.md
Apply it now?
```

### Prototype-to-Production trigger

Recommend `docs/advanced/prototype-to-production.md` when any are true:

- prototype work grows beyond 3 files
- prototype work grows beyond about 120 changed lines
- exploratory code starts touching core logic
- prototype code becomes a dependency for future work
- user wants to ship, reuse, merge, or stabilize prototype code

Recommended message:

```text
Risk signal detected: prototype code is becoming production-relevant.
Recommended advanced doc: docs/advanced/prototype-to-production.md
Apply it now?
```

### Structured Hallucination trigger

Recommend `docs/advanced/structured-hallucination.md` when any are true:

- the final report looks polished but evidence is unclear
- claims use words like verified, safe, passed, complete, fixed, no regression, or fully tested without visible evidence
- evidence is mostly inferred
- report format is detailed but source labels are missing

Recommended message:

```text
Risk signal detected: the report may be more polished than the evidence.
Recommended advanced doc: docs/advanced/structured-hallucination.md
Apply it now?
```

### Router rule

Do not apply every advanced doc.

Recommend at most 1 advanced doc at a time unless the task is Critical.

For Critical tasks, recommend up to 2 advanced docs.

Ask before applying advanced docs if doing so will noticeably slow the task.

If the core skill is enough, do not escalate.

## Instruction Precedence

When global instructions and this skill conflict:

1. Safety and correctness override speed.
2. Explicit user instructions override default workflow preferences.
3. This skill overrides global defaults only when it is triggered.
4. Global instructions remain active unless this skill explicitly narrows or escalates them.
5. Risk overrides size: small changes can require deeper checks when risk is high.
6. Verification status must never be weakened by mode selection or time budget.
7. Do not claim broad certainty from partial inspection or partial verification.

## Pre-Approval Planning Report

Before asking the user to approve implementation, real execution, broad edits, external effects, or any risky action, provide a short planning report first.

Use this when any are true:

- the agent is about to ask "proceed?", "approve?", "should I implement this?", or similar
- the next step may edit files, run real subprocesses, install packages, call network services, push/commit, delete/move files, run migrations, touch persistence, or use secrets
- the task is Full or Critical Mode
- the user may not know what approving the action actually permits

Do not ask for approval with only a vague plan.

The report must include:

1. Task Contract
   - requested behavior
   - current behavior or known failure
   - success criteria
2. Mode and gates
   - selected mode
   - activated gates
   - why the mode is not lighter
3. Planned inspection
   - files, functions, logs, configs, tests, or docs to inspect before patching
4. Planned change points
   - likely files or modules to change
   - what each change is expected to do
5. Minimal-change boundary
   - what will change
   - what will not change
   - existing behavior that must be preserved
6. Approval reason
   - exact action needing approval
   - why approval is needed now
   - whether the action is reversible
7. Verification plan
   - exact commands or manual checks when known
   - expected evidence label: Run, Manual, Partial, Inferred, or Not run
   - stop condition if verification fails

Keep the report compact. For Light Mode, 5-8 lines is enough. For Full or Critical Mode, use the full list.

Approval question format:

```text
Approval needed: <specific action>
Scope: <files/commands/effects>
Risk: <main risk>
Verification after approval: <commands/checks>
Proceed?
```

If the user approves without understanding the scope, still preserve the stated boundary. Approval does not authorize unrelated refactors, broad cleanup, hidden behavior changes, or weaker verification.

If new evidence changes the scope after approval, stop and issue a new Pre-Approval Planning Report.

## Gate Router

Do not run every gate for every task.

First choose the mode:

- Micro
- Light
- Full
- Critical

Then activate only the gates triggered by the task:

- Assumption Gate: unclear assumptions or ambiguous requirements
- Simplicity Check: non-trivial implementation, abstraction, or refactor risk
- Design Interrogation Gate: costly or ambiguous design decision
- Contract & Precedence Check: config/input/fallback/permission/schema/API behavior
- Negative Case Hygiene: negative tests or failure-path verification
- Verification Budget: verification expected over 5 minutes
- Evidence Report: non-trivial or verification-sensitive task

Recommended number of active gates:

| Mode | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| Micro | 0 | 0-1 | 1 |
| Light | 1 | 1-2 | 3 |
| Full | 2 | 2-4 | 5 |
| Critical | 3 | 4-6 | 7 |

If you mention activated gates, keep it brief:

```text
Mode: Full
Activated gates: Contract & Precedence Check, Negative Case Hygiene
Skipped: Design Interrogation Gate - no architecture decision
```

## Mode Selection

Use these thresholds as defaults, not hard limits. Risk overrides size.

### Micro Mode

Use Micro Mode only when all are true:

- 1 file
- under 10 changed lines, maximum 15
- obvious cause
- no public API, schema, config, env, auth, payment, security, migration, persistence, async, concurrency, data-loss, or cross-module behavior touched
- no new test required

Micro Mode limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| files changed | 1 | 1 | 1 |
| changed lines | 1 | 5-10 | 15 |
| code inspection | nearby 20 lines | nearby 30 lines | nearby 50 lines |
| related files inspected | 0 | 0 | 1 |
| failure modes | 0 | 1 | 1 |
| verification paths | 0 | 0-1 | 1 |
| final report | 2 lines | 3 lines | 5 lines |

Micro final report must include:

```text
Changed: <file>
Why: <one-line reason>
Verification: <Run / Manual / Not run / Inferred / Partial>
```

Never omit the verification label, even in Micro Mode.

#
## Prototype Mode

Use Prototype Mode for exploratory UI, throwaway prototypes, visual experiments, or early-stage idea testing.

Prototype Mode limits:

- max 3 files
- max 120 changed lines
- no auth, payment, schema, migration, data deletion, security, persistence, or public API changes
- no claim of production readiness
- verification may be Manual or Inferred
- final report must include: Prototype only

Do not use Prototype Mode for core logic, data integrity, security, irreversible behavior, or production-critical code.

## Light Mode

Use Light Mode for simple, local, low-risk changes.

Default limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| files changed | 1 | 1 | 2 |
| changed lines | 10 | 10-30 | 50 |
| files inspected | 1 | 1-2 | 3 |
| caller/callee checks | 0 | 1 | 2 |
| test files checked | 0 | 1 if nearby | 1 |
| failure modes | 1 | 1-2 | 3 |
| verification paths | 1 | 1 | 2 |
| final report | 3 lines | 4-6 lines | 8 lines |

### Full Mode

Use Full Mode when any are true:

- 2+ files may change
- expected patch is 30+ changed lines
- root cause is unclear
- behavior crosses module boundaries
- tests need to be added or updated
- public API, schema, config, env, auth, permission, payment, security, async, concurrency, migration, persistence, data-loss, or cross-module behavior is touched
- rollback or data-loss risk exists

Default limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| files changed | 2 | 2-4 | 6 |
| changed lines | 30 | 30-120 | 200 |
| files inspected | 2 | 3-5 | 8 |
| relationship points | 2 | 2-4 | 5 |
| failure modes | 3 | 3-5 | 7 |
| verification commands | 1 | 2-4 | 5 |
| tests added/updated | 1 if needed | 1-2 | 3 |
| final report | 6 lines | 8-12 lines | 15 lines |

### Critical Mode

Use Critical Mode for high-risk behavior, regardless of patch size:

- auth or permission
- payment or billing
- security-sensitive validation
- schema or migrations
- persistence or data deletion
- public API contracts
- async/concurrency/race conditions
- irreversible behavior
- external tool execution or filesystem paths

Default limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| files inspected | 3 | 4-8 | 12 |
| relationship points | 3 | 4-6 | 8 |
| failure modes | 5 | 5-8 | 10 |
| negative cases | 1 | 2-4 | 5 |
| verification commands | 2 | 3-5 | 7 |
| evidence signals | 3 | 3-4 | 4 |
| final report | 10 lines | 12-18 lines | 25 lines |

## Core Rules

- Understand the requested behavior before editing.
- Inspect relevant code before asking when the answer is in the codebase.
- Prefer the smallest safe change.
- Every changed line should directly support the requested behavior or verification.
- Preserve local conventions, naming, structure, and architecture.
- Simulate the execution path before patching.
- Check failure modes, edge cases, regressions, and counterexamples.
- Avoid unrelated features, abstractions, rewrites, and refactors.
- Verify before claiming the task is complete.
- State remaining uncertainty instead of pretending everything is proven.

## Inspection Minimums

Before patching, inspect at least:

- the file to be changed
- the direct caller or direct callee when behavior crosses a function boundary
- the nearest related test file if one exists
- the error source when debugging

For Full Mode, inspect at least 2 relationship points when available:

- caller
- callee
- test
- config
- schema
- route
- API boundary
- state owner

If inspection is partial, state the inspected scope.

## Assumption Gate

Use this when a task depends on an assumption that may affect implementation.

Classify assumptions before acting:

1. Code-checkable
   - inspect code first
2. Requirement-dependent
   - ask the user if blocking
3. Safety default
   - choose conservative behavior and state uncertainty

Limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| assumptions listed | 1 | 1-3 | 5 |
| user questions | 0 | 0-1 | 1 |
| interpretations | 1 | 2 | 3 |
| blocking assumptions | 0 | 0-1 | 2 |

Rules:

- Do not ask if the answer can be found in the codebase.
- Do not treat assumptions as facts.
- If multiple interpretations exist, choose the smallest reversible change.
- Do not implement multiple interpretations unless explicitly requested.

For each critical assumption, report one status:

- Confirmed by code
- Confirmed by test/log
- User-confirmed
- Unconfirmed

## Simplicity Check

Use this for non-trivial implementation or refactor risk.

Ask at most 4 questions:

- Is there a smaller change that solves the same problem?
- Am I adding flexibility that was not requested?
- Am I creating an abstraction for single-use code?
- Does this preserve the behavior contract?

Limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| simplicity questions | 1 | 2-3 | 4 |
| alternatives compared | 0 | 1 | 2 |
| refactor checks | 0 | 1 if needed | 1 |
| smaller-change review | 1 | 1 | 2 |

Simplicity means the smallest code that preserves the behavior contract.

Do not simplify by removing validation, error behavior, or precedence rules.

Contract correctness overrides line-count simplicity.

## Design Interrogation Gate

Use this only when at least one is true:

- requirement has 2+ valid interpretations
- architecture boundary may change
- data model or API contract may change
- user-facing behavior is ambiguous
- implementation choice affects future work
- the wrong choice is costly to reverse

Limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| questions | 1 | 1 | 2 |
| recommended answers | 1 per question | 1 per question | 2 per question |
| interpretations | 2 | 2 | 3 |
| files inspected before asking | 0 | 1-2 if code-checkable | 3 |
| design options compared | 1 | 2 | 3 |

Rules:

- Ask at most 1 blocking question before patching unless the user explicitly wants deeper interrogation.
- Do not ask the user if the answer can be found by inspecting the codebase.
- Recommended answers are proposals, not facts.

For each recommended default, label the basis:

- Code-backed
- Safety default
- Product assumption
- Unknown

If the decision is easy to reverse, prefer simplicity. If the decision is costly to reverse, use this gate.

## Contract & Precedence Check

Run this before patching behavior-sensitive code.

Trigger this check when the code includes:

- configuration
- environment variables
- defaults
- fallbacks
- user-provided inputs
- permissions
- schemas
- migrations
- persistence
- external paths or tools
- API boundaries
- functions named like resolve, merge, normalize, default, fallback, or override

Before patching, write down:

1. Input sources
   - explicit input
   - config
   - environment
   - persisted state
   - default value
2. Expected precedence
   - which source should win?
3. Missing vs invalid behavior
   - missing value may fallback
   - invalid explicit value must not silently fallback unless the contract clearly says so
4. Expected failure behavior
   - what should fail?
   - what error/status/message should appear?
5. Silent success risk
   - could the patch make an invalid case succeed?

Limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| input sources checked | 2 | 3-4 | 5 |
| precedence levels | 2 | 3-4 | 5 |
| invalid/missing distinction | 1 | required | required |
| failure conditions | 1 | 1-3 | 5 |
| silent success checks | 1 | 1-2 | 3 |
| verification cases | 1 | 2-3 | 4 |

For precedence-sensitive changes, verify at least:

- explicit valid input
- invalid explicit input
- missing input fallback

If not all are run, label verification as Partial or Inferred.

Contract Check identifies risk. It does not authorize broad refactors.

Patch only the contract violation needed for the requested behavior. Mention unrelated contract issues separately.

## Negative Case Hygiene

A negative test is valid only when it fails for the intended reason.

For each negative case, define the expected failure before running it:

- expected status or error code
- expected message pattern
- expected exit code, if relevant
- expected absence of side effects

Minimum evidence:

- Low-risk negative case: confirm at least 2 evidence signals.
- High-risk negative case: confirm at least 3 evidence signals.
- If only 1 signal is checked, label the result as Inferred, not Verified.

Limits:

| Item | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| evidence signals | 2 | 2-3 | 4 |
| high-risk signals | 3 | 3-4 | 4 |
| negative cases | 1 | 1-3 | 5 |
| cleanup/reset checks | 1 | 1-2 | 3 |
| side-effect checks | 0 | 1 if relevant | 2 |

If the test fails for a different reason, fix the test setup before trusting the result.

If the failure reason cannot be proven, report:

```text
Verification: Inferred
Reason: failure occurred, but intended failure cause was not proven.
```

A negative test is only useful if it proves the intended failure path.

Do not simplify a negative test below the required evidence minimum.

## Failure Mode Minimums

For Light Mode, check at least 1 relevant failure mode if the change affects behavior.

For Full Mode, check at least 3 relevant failure modes.

For Critical Mode, check at least 5 relevant failure modes.

Prefer failure modes from this list:

- invalid input
- empty/null state
- permission or auth boundary
- async/race condition
- backward compatibility
- performance degradation
- nearby behavior regression
- data loss or rollback risk
- public API compatibility
- configuration or environment mismatch
- silent fallback or silent success
- missing vs invalid input confusion

## Verification Budget

Classify verification cost before running long checks:

| Cost | Time | Rule |
|---|---:|---|
| Quick | under 1 minute | run directly |
| Standard | 1-5 minutes | usually run |
| Long | 5-20 minutes | run targeted checks first and state why long check is needed |
| Expensive | over 20 minutes | ask before running unless user requested full verification |

Verification command count limits:

| Mode | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| Micro | 0 | 0-1 | 1 |
| Light | 1 | 1 | 2 |
| Full | 1 | 2-4 | 5 |
| Critical | 2 | 3-5 | 7 |

Verification order:

1. syntax or type check
2. targeted unit test
3. targeted smoke or reproduction
4. related integration test
5. full suite or aggregate

Do not skip targeted verification and jump directly to expensive full-suite checks unless required.

Do not invent verification commands.

Before suggesting a command, inspect available project files such as package.json, Makefile, pyproject.toml, tox.ini, CI config, or project docs when available.

If no command is found, say:

```text
Next command: unknown - no test script found in inspected files.
```

If verification is interrupted, report partial results and the exact next command.

## Verification Labels

Report verification as one of:

- Run: command or automated check was executed.
- Manual: manual scenario or reproduction step was checked.
- Not run: verification could not be executed; explain why and what should run next.
- Inferred: reasoned from code or context only; not runtime-verified.
- Partial: some checks passed, but required full/negative/contract checks remain.

## Completion Status

Completion status must be one of:

- Complete: required verification passed.
- Implemented, partially verified: targeted checks passed but required full/negative/contract checks remain.
- Implemented, verification pending: code changed but verification was not run or was interrupted.
- Not complete: core verification failed or the cause remains unresolved.

Rules:

- Do not claim Complete unless required verification passed.
- Targeted success does not imply full correctness.
- Tests passing does not prove every assumption.
- Verification Budget may limit what runs, but it must not weaken the status label.

## Completion Status Rules

Completion status must be one of:

- Complete: required verification passed, no required gate remains unresolved, and remaining risks are non-blocking and stated.
- Implemented, partially verified: targeted checks passed, but full, negative, contract, or expensive checks remain.
- Implemented, verification pending: code changed, but verification was not run, was interrupted, or is unavailable.
- Not complete: core verification failed, root cause remains unresolved, or required checks failed.

Do not report Complete when:

- verification is only Inferred
- required negative or contract checks were not run
- an expensive required check was skipped
- a required gate remains unresolved
- only partial inspection was performed for a broad-impact change

## Evidence Report

For non-trivial tasks, report:

- Changed: files or areas changed
- Why: reason for the change
- Evidence: code/log/test that supports the change
- Verification: Run / Manual / Not run / Inferred / Partial
- Completion status: Complete / Implemented, partially verified / Implemented, verification pending / Not complete
- Remaining risk: what was not checked
- Next command: exact command if more verification is needed

Report length limits:

| Mode | Minimum | Recommended | Maximum |
|---|---:|---:|---:|
| Micro | 2 lines | 3 lines | 5 lines |
| Light | 3 lines | 4-6 lines | 8 lines |
| Full | 6 lines | 8-12 lines | 15 lines |
| Critical | 10 lines | 12-18 lines | 25 lines |

Micro report may include only:

- Changed
- Why
- Verification

Full and Critical reports should include all fields.

## Large Task Memory

For large tasks, preserve:

- goal
- success criteria
- known relevant files
- inferred or verified execution path
- decisions made and why
- changed files
- verification results
- completion status
- remaining risks
- next action

When context grows:

1. Drop discarded hypotheses first.
2. Summarize files by responsibility.
3. Preserve decisions, changed files, tests, risks, completion status, and next action.

## Final Principle

Minimum values protect quality.

Maximum values prevent over-process.

Small tasks should stay light.

Risky tasks should become precise.

Verification should always be honest.
