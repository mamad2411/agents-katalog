---
name: interview-elicitation
description: Requirements elicitation framework for the Interview phase — six question domains, verifiable acceptance criteria, and the stop condition for when requirements are complete.
---

# Requirements Elicitation

**Helpers**: required — requirements-coverage.mjs, flow-state.mjs (helper rule: missing → STOP and tell the user to reinstall the codex-flow plugin; non-zero exit → surface the error and STOP).

Goal: leave the interview with requirements so unambiguous that a different engineer could implement them without asking anything.

## Six domains to cover (minimum one confirmed answer each)

1. **Goal & success criteria** — What does "done" look like? What user-visible behavior changes? How will we measure success?
2. **Scope boundaries** — What is explicitly IN? What is explicitly OUT? What must not change?
3. **Technical constraints** — Required stack/libraries, patterns to follow, files/areas not to touch, compatibility targets (OS, browsers, versions).
4. **Edge cases & failure behavior** — What happens on invalid input, empty state, concurrency, timeouts, partial failure? What should the user see when things go wrong?
5. **Non-functional requirements** — Performance targets, security/privacy expectations, i18n, accessibility, observability.
6. **Testing expectations** — What proof is required: unit/integration/E2E, coverage bar, manual verification steps.

## Rules

- Ask with AskUserQuestion; batch related questions (max 4 per round) instead of one long interrogation.
- Offer concrete options with a recommended default — users answer choices faster than open questions.
- Convert every vague answer into a verifiable statement and read it back ("So: uploads over 10 MB are rejected with a visible error — correct?").
- Write each acceptance criterion **atomic and independently testable** — one behavior per criterion. These become the per-task `Acceptance` lines in the backlog, so a criterion that bundles three behaviors forces an oversized, hard-to-review task later.
- Record assumptions you had to make as explicit "Assumed:" lines the user can veto.

## Stop condition

Stop interviewing when every acceptance criterion is **verifiable** (testable pass/fail) and the user has confirmed a written summary:

```markdown
## Requirements Summary
- Goal: …
- In scope: … / Out of scope: …
- Constraints: …
- Edge cases: …
- Non-functional: …
- Acceptance criteria: 1. … 2. … (each testable)
- Assumed: …
```

Before requesting confirmation, format each requirement and its acceptance criteria as:

```markdown
## R<n>: <title>
- R<n>.<m>: <clause>
```

Write one atomic, verifiable acceptance criterion per `R<n>.<m>` bullet. Express one testable
WHEN/THEN-style behavior per ID, and split compound clauses into separate IDs.

The moment the user confirms the Requirements Summary, write it VERBATIM to
`.codex-flow/REQUIREMENTS.md`. Do not start planning until the write completes.

## Changing requirements mid-run

Never edit the original requirement sections in place. For a legitimate change, get user
confirmation and append a timestamped delta under `## Deltas` using this format:

```markdown
### <ISO date> <ADDED|MODIFIED|REMOVED> R<n>[.<m>]
<new or changed clause text>
```

Treat the original requirement sections plus all deltas as the effective requirement set in every
downstream phase. The user's delta confirmation refreshes `requirementsApproved` in
`.codex-flow/STATE.md` to `yes (delta <ISO date>)`. Record the delta by running
`node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" requirement-delta`, which sets
`requirementsApproved` to `yes (delta <date>)`, resets `planApproved` and `backlogApproved` to
`no (delta <date>)`, and returns `phase` to `plan`; no earlier plan or backlog approval survives a
requirement change.

Before execution resumes, re-run Phase 2 impact analysis against the effective set and obtain plan
approval, rebuild the affected tasks, run
`node "${CLAUDE_PLUGIN_ROOT}/scripts/requirements-coverage.mjs" --requirements .codex-flow/REQUIREMENTS.md --tasks .codex-flow/TASKS.md --plan .codex-flow/PLAN.md`,
and obtain backlog re-approval. Stop on any coverage violation.
