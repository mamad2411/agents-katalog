---
name: user-story-acceptance-manifest
description: 'Create, validate, reuse, or replace a frozen codebase-aware Acceptance Manifest for one GitHub story. Supports new delivery and resumed existing PRs by checking design revision, issue contract, relevant base assumptions, stable criteria, invariants, tests, exclusions, and blocker boundaries without implementing code or expanding scope.'
metadata:
  author: eho
  version: '1.3.0'
---

# User Story Acceptance Manifest

Create the implementation and review contract for exactly one story. The manifest translates an already-approved design and GitHub Issue into auditable rows; it does not redesign the feature.

## Inputs

Require:

- Design document path and `Revised` status.
- Story ID and GitHub Issue number or URL.
- Current default-branch commit SHA.
- Completed dependency stories, if any.
- Existing PR and head SHA, if discovered, as inspection context only.
- Existing marked Acceptance Manifest versions, if any.

If the design, issue, or story identity is ambiguous, stop and report the missing source instead of guessing.

## Workflow

1. Read the complete story in the revised design and the synchronized GitHub Issue.
2. Verify that the issue still matches the design. Report material drift as a blocker; do not silently choose one source.
3. Inspect only the repository areas needed to validate referenced paths, existing contracts, tests, commands, and supported workflows.
4. Preserve existing acceptance-criterion IDs. If a legacy story has no IDs, assign deterministic IDs in story order: `<STORY-ID>-AC01`, `<STORY-ID>-AC02`, and so on.
5. Add invariant rows only when they are required for an explicit criterion or for the criterion to be safe and correct. Examples include authorization boundaries for protected data, idempotency for an explicitly retryable write, or cleanup for an explicitly durable lifecycle.
6. Do not add speculative hardening, optional polish, future architecture, or unsupported edge cases to the required manifest. Record useful non-required ideas under `Follow-up candidates`.
7. Identify the strongest relevant verification already supported by the repository. Separate required verification from optional additional confidence.
8. Record failures that already exist at the base SHA so later workers do not misattribute them to the story.
9. Compare any existing manifest with the current normalized story/issue contract, relevant design sections, supported workflows, and referenced code contracts.
10. Choose:
    - `REUSE`: the latest manifest remains valid.
    - `CREATE`: no manifest exists.
    - `REPLACE`: requirements or relevant assumptions materially changed; increment the version.
    - `BLOCKED`: the difference requires product/architecture reconciliation.
11. A newer default-branch SHA alone does not invalidate a manifest. Replace it only when the changed base alters a referenced contract, dependency assumption, implementation location, supported workflow, or required verification.
12. Return the exact manifest schema below. Do not edit code, create branches, or create a PR.

Return the chosen action separately from the immutable manifest:

```markdown
## Manifest Resolution Handoff v1
- Story ID:
- Worker context/ref:
- Manifest action: REUSE | CREATE | REPLACE | BLOCKED
- Active manifest version:
- Active source fingerprint:
- Reused prior version:
- Replacement reason:
- Blocked:
- Blocker:
```

## Scope Rules

A required row must trace to at least one of:

- An explicit acceptance criterion.
- A design contract or invariant directly referenced by the story.
- Security, authorization, privacy, data-safety, lifecycle, or compatibility behavior necessary to make an explicit story outcome correct.

When an invariant requires a product or architecture decision not settled by the sources, set `Blocked: yes` and name the decision. The manifest cannot settle new product scope.

## Acceptance Manifest v1

```markdown
## Acceptance Manifest v1
- Story ID:
- Issue:
- Design doc:
- Design revision:
- Base SHA:
- Source fingerprint:
- Manifest version:
- Manifest status: Ready | Blocked

| ID | Requirement or invariant | Type | Source | Implementation location | Required evidence | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <STORY>-AC01 | ... | Acceptance | Issue criterion 1 | `path` | focused test / browser evidence / code inspection | `command` | Not started |
| <STORY>-INV01 | ... | Security / Data safety / Lifecycle / Contract | Design section or AC ID | `path` | ... | `command` | Not started |

## Preconditions
- Supported platforms and workflows:
- Completed dependencies:
- Required credentials or services:

## Existing failures
- Command:
- Failure:
- Evidence at base SHA:

## Out of scope
- ...

## Follow-up candidates
- ...

## Merge-blocker boundary
This story is blocked only by an unmet required manifest row, a P0/P1 defect,
a failing required gate, a supported-workflow regression, or a required contract break.
P2/P3 hardening and polish are follow-up work.

## Manifest handoff
- Required rows:
- Reused prior version:
- Replacement reason:
- Pre-existing failures recorded: yes/no
- Ambiguities:
- Blocked: yes/no
- Blocker:
```

Use `None` rather than omitting empty sections. Every required row must have a source and a verification method.

## Operating Rules

- Keep the manifest compact enough to pass in full to implementers and reviewers.
- Treat each manifest version as immutable after implementation begins. Product-approved scope changes or material source changes require a new version and restart INITIAL review.
- PR number, PR head SHA, implementation status, and review status are mutable delivery state. Keep them in the Story Resume Checkpoint and SHA-specific handoffs, never in the immutable manifest or its source fingerprint.
- On `REUSE`, return the existing manifest byte-for-byte. The coordinator may repair duplicate marker comments, but must not rewrite that version with updated delivery state.
- Do not delete or rewrite previous versions; resume logic needs their historical source and review relationship.
- When called by `user-story-delivery`, the manifest and resolution handoff are worker-to-coordinator artifacts. Return control to that coordinator; they are not a user-facing completion point for the story or feature.
- Do not implement story code or review a PR from this worker context. Its independence keeps the acceptance boundary fixed before implementation.
- Model selection is outside this skill. Use the model configured by the caller or runtime.
