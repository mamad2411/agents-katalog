---
name: knowledge-save
description: Capture reusable knowledge from a completed workflow — problem, signals, resolution, guardrails, and applicability — and write it to a durable, repository-appropriate sink.
---

> References to plugin documentation files (e.g. `docs/workflow-artifact-templates.md`) refer to the plugin-level `docs/` directory (`../../docs/` relative to this file). Other `docs/` paths (such as artifact output destinations) refer to the target project.

## Purpose

Use this skill when a completed workflow has produced a reusable lesson — a debugging insight, a non-ADR implementation decision, a non-obvious configuration fix, or any resolution that future contributors or agents would benefit from knowing. The skill extracts the lesson into a structured knowledge artifact and writes it to a durable sink so it survives the current session.

This skill is a **capture** workflow: it turns an already-resolved problem into a reusable artifact. It does not perform the original investigation, debugging, or implementation — those belong to the originating workflow (e.g., `debug`, `incident-rca`, `parallel-impl`).

Persistent team, squad, or fleet-style long-lived orchestration is out of scope for this skill. Use a separate orchestration layer if persistent coordination is needed.

**Capture vs. refresh boundary**: this skill owns the initial capture of a
reusable lesson into a durable artifact. It does not evaluate, deduplicate,
retire, or refresh previously captured knowledge — those maintenance concerns
belong to `/flow:knowledge-refresh`. When capture discovers
that a substantially similar artifact already exists in the knowledge sink, it
should note the overlap and recommend a refresh pass rather than silently
creating a duplicate.

**Out of scope**: automatic refresh of previously captured knowledge, mining of past sessions for latent lessons, and enforcement of a mandatory global directory taxonomy for knowledge artifacts. Those concerns belong to `/flow:knowledge-refresh` or project-level conventions.

## When to Use It

Activate when the developer asks for things like:

- "capture what we learned from that debugging session"
- "write up the lesson from that incident"
- "save this resolution so we don't repeat it"
- "turn that fix into a knowledge artifact"
- "document what we discovered for future reference"

Also activate when:

- a workflow has completed and the resolution contains a non-obvious insight worth preserving;
- the developer flags a resolved problem as likely to recur;
- a post-incident or post-debugging review identifies a reusable pattern;
- the originating workflow's durable artifact (RCA summary, track report, etc.) contains a lesson that should be extracted into a standalone knowledge artifact.

Do **not** activate for:

- capturing knowledge from a workflow that is still in progress (wait until it completes);
- general documentation or README updates (use normal editing);
- architecture decision records (use `arch-review`);
- codebase orientation (use `map-codebase`).

## Project-Specific Inputs

Before you start, identify:

- **source type** — the kind of workflow that produced the knowledge (e.g., `debug`, `incident-rca`, `parallel-impl`, or a manual investigation);
- **source references** — links or paths to the originating session, PR, issue, RCA, commit, or other evidence;
- **summary** — a short description of what was learned, provided by the developer or extracted from the source;
- **sink** — where the durable knowledge artifact should be written (e.g., a file path, issue, wiki page). When the repository declares shared workflow defaults (see `docs/workflow-defaults-contract.md`) with a knowledge-capture sink preference, use that configured path as the default destination. When the developer provides an explicit sink, the developer's choice overrides any configured default. When neither an explicit choice nor a configured default is available, ask before proceeding. Do not assume a default directory — sink location is a project-level decision, and the defaults contract does not impose a mandatory taxonomy.

## Workflow

### Phase 1 — Gather context

Collect the factual context brief from the originating workflow:

- the problem that was solved (symptom, root cause);
- the signals that indicated the problem (error messages, metric anomalies, behavioral clues);
- the resolution that was applied (approach, code changes, configuration);
- any guardrails or edge cases discovered during resolution;
- the source references (session artifacts, PRs, commits, issues).

If the originating workflow produced a durable artifact (e.g., an RCA summary, a track report), use it as the primary source. Supplement with session context if the artifact is incomplete.

If the factual context is insufficient to form a complete knowledge artifact — the problem is unclear, the resolution is ambiguous, or the source references are missing — ask the developer to fill the gaps before proceeding.

**Gate: Context sufficient**

- PASS — enough information to populate all required fields in the knowledge artifact template.
- FAIL — critical fields cannot be populated. Ask the developer for the missing information.

### Phase 2 — Draft the artifact

Using the knowledge artifact template from `docs/workflow-artifact-templates.md`, draft the artifact with all required fields:

- **Problem**: concise description of the problem that was solved.
- **Signals**: observable symptoms that indicated the problem.
- **Resolution**: what was done to resolve the problem.
- **Guardrails**: conditions under which the resolution is safe to apply, and known risks.
- **Applicability**: when this knowledge applies — technology, context, failure shape.
- **Source references**: links to the originating evidence.
- **Sink reference**: where the artifact will be durably stored.

Present the draft to the developer for review. Allow edits before writing.

**Gate: Draft approved**

- PASS — developer approves the draft (explicitly or by not objecting).
- FAIL — developer requests changes. Revise and re-present.

### Phase 3 — Write to sink

Write the approved artifact to the confirmed sink location. Resolve the sink using the following precedence: (1) the developer's explicit choice, (2) the knowledge-capture sink from shared workflow defaults, (3) ask the developer. This precedence preserves the no-mandatory-taxonomy rule — the defaults contract provides a configurable preference, not a required directory layout.

1. Write the artifact to the sink.
2. Confirm the write succeeded (file exists, issue was created, etc.).
3. If the write fails, report the failure and ask the developer for an alternative sink.

**Gate: Artifact persisted**

- PASS — artifact written to the durable sink and confirmed.
- FAIL — write failed and no alternative sink was provided. Stop with a warning.

### Produce the durable knowledge artifact

At the end of every invocation — whether the workflow completes fully or stops early — ensure the knowledge artifact has been written to the confirmed sink. If the workflow stops before Phase 3, present the draft to the developer and offer to write it to an alternative location.

"Durable" means written to a repository-appropriate sink — a committed file, an issue, a wiki page, or another persistent location — not only to chat. Chat-only output does not satisfy this requirement.

### Update SESSION.md

Write `.agent/SESSION.md` using the full schema defined in `docs/session-md-schema.md`. All five YAML frontmatter fields are required on every write:

- `current-task`: the knowledge capture description
- `current-phase`: the current phase name
- `next-action`: what happens next
- `workspace`: the active branch or repository reference
- `last-updated`: current ISO-8601 timestamp

Required sections: `## Decisions`, `## Files Touched`, `## Open Questions`, `## Blockers`, `## Failed Hypotheses`.

Write SESSION.md after each phase gate. If the write fails, log a warning and continue.

## Required Gates

### Phase gates

Each phase must satisfy its specific gate condition (see workflow above) before advancing to the next phase. A failed gate halts forward progress; the skill must either ask the developer for the missing input or stop.

### Artifact persistence gate

The durable knowledge artifact must be written to the confirmed sink at the end of every invocation. If the primary sink fails, offer an alternative. If no sink is available, the gate fails.

### Verification checklist — knowledge captured

Before declaring the knowledge capture complete, confirm ALL of the following. Any failing item blocks the "capture complete" declaration.

- [ ] Problem, signals, and resolution are clearly stated — PASS / FAIL
- [ ] Guardrails and applicability are documented — PASS / FAIL
- [ ] Source references point to real, accessible evidence — PASS / FAIL
- [ ] Artifact written to durable sink — PASS / FAIL
- [ ] Sink reference recorded in the artifact — PASS / FAIL
- [ ] SESSION.md written with correct phase — PASS / FAIL

If any item is FAIL: report the failing item(s) by name, state what must be done to resolve each, and do not advance past the gate.

## Stop Conditions

- The developer does not provide a sink and declines to choose one — stop with the draft presented in chat.
- The source material is too incomplete to form a meaningful knowledge artifact after asking the developer for clarification — stop and explain what is missing.
- The developer asks to stop.
- The write to the sink fails and no alternative is available — stop with the draft presented in chat and a warning that the artifact is not yet durable.

Before stopping, ensure any partial draft is presented to the developer so the work is not lost. A rescue attempt consists of offering an alternative sink or asking the developer to provide the missing information.

## Example

### Invocation

```text
Developer: Capture the lesson from our debugging session — the CI auth failure was caused by
async seed ordering in the test setup.
Source: docs/debug-session-2025-01-15.md, PR #289
Sink: docs/knowledge/ci-auth-seed-ordering.md
```

### Walkthrough

**Phase 1 — Gather context**

Read the source artifact (`docs/debug-session-2025-01-15.md`) and PR #289 to extract:
- Problem: CI auth test fails intermittently due to async seed ordering.
- Signals: `UserService.authenticate` returns null in CI but not locally; non-deterministic failure.
- Resolution: await seed completion before authenticate call in CI setup hook.
- Guardrails: only applies to test setups using async seed scripts; production code unaffected.
- Applicability: any Node.js test suite using async database seeding with order-dependent fixtures.

Context is sufficient — all fields can be populated.

**Phase 2 — Draft the artifact**

```text
Problem: CI authentication tests fail intermittently because the async database seed script
has not completed when the auth fixture is queried.
Signals: UserService.authenticate returns null for valid credentials in CI but passes locally;
failure is non-deterministic and correlates with CI parallelism settings.
Resolution: Await seed completion in the CI test setup hook before executing auth-dependent tests.
Guardrails: Only applies to test setups using async seed scripts. Production auth code is
unaffected. If the seed script is refactored to synchronous, this guardrail no longer applies.
Applicability: Node.js test suites using async database seeding with order-dependent fixtures,
especially in parallel CI environments.
Source references: docs/debug-session-2025-01-15.md, PR #289
Sink reference: docs/knowledge/ci-auth-seed-ordering.md
```

Developer approves the draft.

**Phase 3 — Write to sink**

Write the artifact to `docs/knowledge/ci-auth-seed-ordering.md`. File created and confirmed on disk.

### Durable knowledge artifact (abbreviated)

```markdown
# Knowledge — CI auth seed ordering

Problem: CI authentication tests fail intermittently due to async seed ordering.
Signals: UserService.authenticate returns null in CI; non-deterministic.
Resolution: Await seed completion in CI setup hook.
Guardrails: Test-setup only; production unaffected.
Applicability: Async database seeding with order-dependent fixtures in parallel CI.
Source references: docs/debug-session-2025-01-15.md, PR #289
Sink reference: docs/knowledge/ci-auth-seed-ordering.md
```
