---
name: spar-retain
description: >-
  Use after implementation when the user approves closeout. Reconcile the active
  spec and plan with what shipped, propose broader documentation updates for
  approval, then move the whole change folder from specs/active to
  specs/completed.
---

# Retain

Turn completed implementation into durable project knowledge.

Retain is closeout, not a retrospective by default. Make the active spec and
plan accurate, preserve useful context, update broader docs only with approval,
then archive the whole change folder.

## Inputs

- `specs/active/<change-name>/<change-name>_spec.md`
- `specs/active/<change-name>/plan.md`
- Completed implementation in the repository
- Optional notes or artifacts in the same change folder
- Relevant repo documentation, such as README, setup, architecture, or product docs

If implementation appears incomplete, stop and ask whether to return to
`spar-act`.

## Retention Context

Before editing, review the spec, plan, implementation changes, validation
results, and optional notes. Preserve optional artifacts unless the user asked to
remove them or they are clearly obsolete.

The retained folder should explain what shipped and why it matters without
becoming a noisy build log.

## Reconcile the Spec

Update `<change-name>_spec.md` so it describes final behavior and durable intent.

- Keep `Summary`, `Problem`, `Scope`, and `Out of Scope` accurate.
- Update `Constraints` if implementation revealed durable requirements.
- Update `Success Criteria` so they reflect the outcomes that shipped and were
  validated.
- Update `Decisions` with important product or technical choices discovered
  during implementation.
- Resolve or remove stale `Open Questions`; keep only questions that materially
  affect future implementation or validation.

Do not add step-by-step implementation narrative to the spec.

## Reconcile the Plan

Update `plan.md` so it remains a useful execution record.

- Ensure `Tasks` are checked or explicitly explained.
- Ensure `Validation Strategy` reflects what actually ran or what could not be
  validated.
- Ensure `Risks / Follow-ups` captures unresolved risks, deferred work, or
  follow-up decisions.
- Ensure `Approach` and `Execution Constraints` do not contradict what shipped.
- Remove only scratch notes or duplicate lines that would confuse future readers.

## Documentation Updates

Identify broader documentation impact from the final spec, plan, implementation
changes, and repo docs.

If broader docs should change, propose concrete edits and ask for approval before
applying them. Do not silently edit repo-wide documentation.

If no broader documentation updates are warranted, say so briefly in the final
summary so the user knows it was considered.

## Archive the Change

Move the entire folder:

`specs/active/<change-name>/` -> `specs/completed/<change-name>/`

Create `specs/completed/` and `specs/completed/<change-name>/` if needed. Do
not leave a copy under `specs/active/`. If a destination file already exists,
stop and ask how to resolve it; do not overwrite or merge file contents silently.

## Stop Conditions

Stop and ask if:

- Implementation appears incomplete.
- Validation is missing and cannot be explained honestly.
- Final behavior contradicts the spec in a way the user has not approved.
- Broader documentation changes are needed but not yet approved.
- A destination file already exists in `specs/completed/<change-name>/`.

## Completion

Retention is complete when:

- The spec matches the implementation.
- The plan reflects completed or explained work.
- Approved documentation updates are applied, or none were needed.
- The change folder exists only under `specs/completed/<change-name>/`.

Then summarize concisely with genuine enthusiasm for the completed change: final
archived path, spec and plan reconciliation, documentation updates made or
skipped, and any retained follow-ups. Emphasize that the completed folder is the
durable source of truth for what shipped.

## Artifact Recap

| Artifact | In this phase |
| --- | --- |
| `<change-name>_spec.md` | Final behavior, durable intent, constraints, success criteria, decisions, and material open questions |
| `plan.md` | Final task state, validation record, risks, and follow-ups |
| `specs/completed/<change-name>/` | Archived source of truth for the shipped change |
