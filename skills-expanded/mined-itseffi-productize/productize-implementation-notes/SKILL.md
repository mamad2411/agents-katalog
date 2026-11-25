---
name: productize-implementation-notes
description: >-
  Running implementation-notes protocol for spec-driven builds. Use when the user asks the
  agent to maintain implementation-notes.md or implementation-notes.html with decisions,
  deviations, tradeoffs, open questions, and verification while implementing a feature, fix,
  or product slice.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Implementation Notes

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

- **Skill**: `implementation-notes`
- **Lifecycle**: Build With AI
- **Category**: AI Execution
- **Primary artifact**: Implementation-notes decision log with spec interpretations, deviations, tradeoffs, open questions, and verification evidence

Use this skill when implementation work needs a durable notes artifact that keeps
the user in the loop without stopping progress for every ambiguity.

This is not a verbose work log. It records the meaningful places where the spec
was interpreted, narrowed, changed, or found incomplete.

## Activation

Activate alongside `$tdd`, `$eng-review`, `$qa`, or `$verification` when the user
asks for any of:

- `implementation-notes.md`
- `implementation-notes.html`
- running implementation notes
- decisions the spec did not cover
- deviations from the spec
- tradeoffs made during implementation
- open questions to confirm after implementation

Do not ask whether to create the file if the user already requested it. Create or
update the requested file and keep working.

## File Selection

- Use the exact path and format the user requested.
- If the user asks for notes but does not name a file, use `implementation-notes.md`.
- If the user asks for HTML, use `implementation-notes.html`.
- If an implementation-notes file already exists for the current task, update it
  instead of overwriting useful existing context.

## Update Cadence

1. Create the notes file before or during the first implementation decision.
2. Update it when the implementation makes a non-obvious choice, interprets an
   ambiguous spec line, departs from the spec, accepts a tradeoff, discovers an
   open question, or changes verification scope.
3. Batch small related choices into one entry instead of writing noisy micro-logs.
4. Before claiming completion, do a final pass that aligns notes with the actual
   diff, verification evidence, and unresolved questions.

## What To Capture

### Design Decisions

Choices made where the spec was ambiguous or silent.

Each entry should include:

- decision
- reason
- spec basis, or `unspecified`
- impact

### Deviations

Intentional departures from the spec.

Each entry should include:

- requested behavior
- implemented behavior
- reason
- impact
- whether user confirmation is needed

### Tradeoffs

Alternatives considered and why the chosen path is better for this slice.

Each entry should include:

- chosen option
- alternatives considered
- why chosen
- cost or downside accepted

### Open Questions

Questions the user may want to confirm or revise.

Each entry should include:

- question
- why it matters
- current default assumption
- status: `needs-review`, `accepted-risk`, `resolved`, or `deferred`

### Verification

Evidence that proves the implementation and the notes are current.

Include:

- commands or checks run
- result
- coverage gaps
- behavior not tested

## What Not To Capture

- Every file edit.
- Internal reasoning or chain-of-thought.
- Obvious implementation details already specified.
- Secrets, credentials, private customer data, or raw logs with sensitive content.
- Generic progress narration that does not help the user review decisions.

## Markdown Template

Use this structure for Markdown notes:

```markdown
# Implementation Notes

## Spec Reference
[Feature, ticket, prompt, or artifact being implemented.]

## Summary
[One paragraph describing how the implementation interprets the spec.]

## Design Decisions
| Decision | Reason | Spec basis | Impact |
|---|---|---|---|

## Deviations
| Requested | Implemented | Why | Impact | Confirmation |
|---|---|---|---|---|

## Tradeoffs
| Choice | Alternatives | Why this path | Downside |
|---|---|---|---|

## Open Questions
| Question | Why it matters | Current assumption | Status |
|---|---|---|---|

## Verification
| Check | Result | Notes |
|---|---|---|
```

## HTML Template Rules

For `implementation-notes.html`, produce a single self-contained HTML file:

- embedded CSS and JavaScript only
- no external assets or remote dependencies unless explicitly requested
- semantic headings and landmarks
- responsive layout
- decision cards or tables for scanability
- status chips for `needs-review`, `accepted-risk`, `resolved`, and `deferred`
- a clear verification section near the bottom
- optional filters, collapsible detail, or copy buttons only when they help review

Recommended HTML sections:

1. **Header**: spec reference, implementation status, last updated, owner if known.
2. **Decision Dashboard**: counts for decisions, deviations, tradeoffs, open questions.
3. **Design Decisions**: cards or table with reason, spec basis, and impact.
4. **Deviations**: requested vs implemented, why, impact, confirmation status.
5. **Tradeoffs**: comparison table with accepted downside.
6. **Open Questions**: status and current default assumption.
7. **Verification**: commands/checks, results, and gaps.

## Route Internally

- `$tdd`
- `$eng-review`
- `$qa`
- `$verification`
- `$docs`
- `$release`

## Required Output

Return:

1. **Notes File**: path, format, and whether it was created or updated.
2. **Captured Decisions**: decisions, deviations, tradeoffs, and open questions added.
3. **Spec Impact**: what downstream product, design, eng, QA, release, docs, or DX work may change.
4. **Verification Linkage**: checks run, gaps, and whether the notes match the final implementation.
5. **Next Review**: user confirmations or gate follow-ups needed.
