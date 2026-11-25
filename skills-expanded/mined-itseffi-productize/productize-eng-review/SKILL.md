---
name: productize-eng-review
description: >-
  Engineering gate for architecture, data flow, system boundaries, implementation risk, test
  strategy, performance, security, observability, and build readiness. Use before or after
  implementation when technical execution can block shipping.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Eng Review

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `eng-review`
- **Lifecycle**: Build With AI
- **Category**: AI Execution
- **Primary artifact**: Engineering review with architecture readout, execution risks, test strategy, decision, and handoff

Use this gate to decide whether the technical plan or implementation is coherent,
testable, maintainable, and safe enough for the next playbook move.

Eng Review is the execution gate. It should read like a strong engineering manager
reviewing whether a plan can actually ship, be tested, be operated, and be changed
later without surprising the team.

## Artifact Format

Use Markdown for concise technical findings. Use self-contained HTML when the
review needs architecture diagrams, data-flow maps, risk heatmaps, annotated code
snippets, sequence diagrams, or a shareable PR/implementation explainer. If
implementation ambiguities must be preserved while coding, call
`$implementation-notes` and keep the requested notes file current.

## Pre-Review Audit

Before reviewing:

1. Read the product plan, relevant code, architecture docs, tests, TODOs, and
   prior gate outputs.
2. Detect the platform, runtime, data stores, external services, test framework,
   and deployment path when a repo exists.
3. Mark stale diagrams, stale plans, stale tests, or review outputs that predate
   the current code or product scope.
4. Identify whether the review is plan-mode, diff-mode, post-fix, or release-gate
   support.
5. If the plan touches 8+ files or creates 2+ new classes/services/modules, run a
   scope-reduction challenge before deep review.

## Scope Challenge

Ask:

- What is the smallest implementation that proves the product outcome?
- What existing code, component, data model, or service can be reused?
- What can be a follow-up PR or later loop?
- What architecture decision becomes expensive to reverse?
- What would make a competent engineer unable to ship a useful slice in two weeks?

## Review Passes

### 1. Architecture And Data Flow

Trace the actual path through the system:

- entry point
- authentication/authorization
- input validation
- state changes
- persistence
- async/background work
- external calls
- output/rendering
- error handling
- observability

Include an ASCII diagram for non-trivial flows:

```text
User/Input -> Boundary -> Service/Model -> Data Store -> Output
                 |             |
              errors       logs/metrics
```

Flag hidden coupling, cyclic dependencies, unclear ownership, migration risk, and
state transitions that are not explicit.

### 2. Code Quality And Maintainability

- Is the abstraction necessary or premature?
- Are names, boundaries, and contracts guessable?
- Does the plan follow existing repo patterns?
- Are edge cases handled where they occur, not patched downstream?
- Is there any metadata churn or unrelated refactor risk?

### 3. Test Strategy

Detect existing test infrastructure first. Then require:

- unit tests for pure logic and edge conditions
- integration tests for contracts/data flow
- regression tests for changed behavior that could break existing users
- eval tests for AI/prompt/model behavior
- e2e tests only for critical paths or high-risk flows

If the review identifies a regression, add a regression test requirement. Do not
treat regression coverage as optional.

### 4. Failure Modes And Rescue Paths

List realistic production failures:

| Flow | Failure mode | User impact | Detection | Recovery |
|---|---|---|---|---|

Cover timeouts, nil/empty values, permissions, stale state, duplicate submission,
partial writes, race conditions, retries, idempotency, and rollback.

### 5. Security, Privacy, And Data Integrity

- Does the change expose sensitive data?
- Are permissions checked at the right boundary?
- Are inputs trusted too early?
- Are audit logs or consent requirements needed?
- Does rollback leave data in a coherent state?

### 6. Performance And Operability

- What is the expected load or data size?
- What query, render, or model-call path could get slow?
- What metric, trace, log, or alert would reveal trouble?
- Can support/debugging reconstruct what happened three weeks later?

### 7. Parallelization And Sequencing

When implementation is non-trivial, propose slices with disjoint write scopes and
dependencies. Do not parallelize work that shares fragile files or unresolved
interfaces.

## Decision Protocol

For each engineering issue:

- State the risk and evidence.
- Recommend revise, split, spike, test, instrument, or block.
- If a decision affects architecture, scope, or test burden, handle it separately.
- If the fix is obvious and local, state the fix and continue.
- Never approve with hidden unresolved engineering decisions.

## Route Internally

- `$technical-architecture-brief-from-product-requirements-doc`
- `$backend-design`
- `$spec-writing`
- `$engineering-problem-solving-and-solution-structuring`
- `$tdd`
- `$systematic-debugging`
- `$verification`
- `$implementation-notes`

## Required Output

Return:

1. **Architecture Readout**: boundaries, data flow, dependencies, state, and failure modes.
2. **Execution Risks**: complexity, coupling, migration risk, security, performance, and observability gaps.
3. **Diagrams**: architecture/data-flow/state diagrams when the flow is non-trivial.
4. **Test Strategy**: unit, integration, regression, e2e, eval, and verification coverage needed.
5. **Failure Mode Register**: failure, impact, detection, and recovery.
6. **Decision**: approve, revise, split, spike, or block.
7. **Handoff**: QA, release, docs, DX, or product gate needs.
8. **Completion Summary**: status, confidence, stale artifacts, unresolved decisions, and accepted technical risks.
