# GitHub Issue Refinement

## Purpose
Turn rough issues into execution-ready specifications: verifiable acceptance criteria, mapped technical dependencies, correct labels/milestone, and explicit out-of-scope boundaries — without changing the reporter's original intent.

## Use when
- An issue is vague, missing repro steps, or has untestable acceptance criteria ("works correctly", "fast").
- A milestone needs backlog grooming: sizing, dependency ordering, duplicate merging.
- A discussion or support thread should convert into actionable engineering tasks.
- Operating in mode(s): `implementation`, `review`.

## Do not use when
- Authoring a brand-new issue from scratch (use `github-issue-create`).
- Triaging inbound volume for routing and priority (use `github-issue-triage`).
- Debating product direction (escalate to product owner; refinement implements decisions, not makes them).

## Required context
- Issue URL, current title/body, labels, milestone, and linked issues or PRs.
- Repository context (area labels, CODEOWNERS, active roadmap Goals).
- Reporter intent: the problem statement that must survive refinement unchanged.

## Procedure
1. **Preserve intent, then sharpen**: restate the reporter's problem in one sentence and confirm it matches before rewriting anything else.
2. **Make acceptance criteria testable**: convert adjectives into measurements ("loads in < 200 ms p95 on staging", "rejects empty titles with error E-102"); each criterion gets a checkbox and an observable verification method.
3. **Map dependencies explicitly**: link blocking/blocked-by issues, required ADRs, and affected components (`area/backend`); split the issue if it hides two independent deliverables.
4. **Right-size and label**: assign type (`bug`/`enhancement`/`task`), severity (P0–P3), area labels, and the milestone matching current capacity; remove stale or contradictory labels.
5. **Declare non-goals**: add an explicit out-of-scope line so implementers know where to stop.
6. **Verify the edit**: re-read the refined issue top to bottom; confirm every checkbox is independently verifiable and no new scope was smuggled in.

## Decision rules
- **Intent is immutable**: refinement clarifies; it never reinterprets the reporter's problem into a different feature.
- **Every checkbox observable**: criteria without a stated verification method are rejected.
- **One deliverable per issue**: hidden second tasks split out and cross-linked.
- **No silent scope growth**: added scope requires reporter or owner acknowledgment in a comment.

## Evidence required
- Before/after diff summary of the refinement with intent-preservation note.
- Dependency map (links) and milestone/label rationale.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Structured GitHub artifact (refined issue body with testable criteria, dependencies, milestone).
- Validation confirmation (self-check that all criteria are observable).

## Stop conditions
- Issue has testable acceptance criteria, mapped dependencies, correct labels/milestone, and stated non-goals.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to product owner when refinement reveals conflicting requirements or missing product decisions.
- Escalate to reporter when intent is ambiguous and guessing would risk wrong scope.
