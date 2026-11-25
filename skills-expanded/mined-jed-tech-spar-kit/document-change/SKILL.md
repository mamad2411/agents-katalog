---
name: document-change
description: >-
  Finalizes documentation for a completed change under Docs/<scope>/Specs/<change-name>/.
  Aligns <change-name>_spec.md with final behavior, proposes broader doc updates for approval, and moves
  the change folder to Archive. Use after implement-change when implementation is done and
  the user wants cleanup and durable docs.
---

# Document change

Turn completed implementation into clean, accurate, durable knowledge: honest `<change-name>_spec.md`, captured decisions, broader doc updates only with approval, then archive the change folder.

## Inputs

- `Docs/<scope>/Specs/<change-name>/<change-name>_spec.md`
- `Docs/<scope>/Specs/<change-name>/plan.md`
- Completed code changes
- Repository documentation (e.g. `README`, `Docs/technicalBrief.md`, setup or usage docs)

## Outputs

- Finalized `<change-name>_spec.md` (matches actual behavior)
- Optional updates to broader docs (**after approval**)
- Archived folder: `Docs/<scope>/Archive/<change-name>/` (contents moved from `Specs/`)

## Workflow

### 1. Review implementation vs spec

- Compare implemented behavior with `<change-name>_spec.md`
- Note mismatches, missing decisions, outdated assumptions

### 2. Update `<change-name>_spec.md`

- Reflect final behavior (spec must match reality, not original guesses)
- Update **Decisions**, **Constraints**, **Success Criteria** as needed
- Resolve or remove stale **Open Questions**
- Keep intent-focused; no step-by-step implementation in the spec

### 3. Identify broader documentation impact

- Use **Documentation Impact** in `<change-name>_spec.md` and the change itself
- Consider: `Docs/technicalBrief.md`, README, setup/usage, developer notes

### 4. Propose broader documentation updates

- List suggested edits clearly. Be concise.
- **Do not apply** until the user approves

### 5. Apply approved updates

- Update only what was approved; keep changes minimal and accurate

### 6. Final cleanup

- `<change-name>_spec.md`: clear and complete
- `plan.md`: final state (all done or explained); trim noise and temporary notes

### 7. Archive change

Move the entire folder:

`Docs/<scope>/Specs/<change-name>/` → `Docs/<scope>/Archive/<change-name>/`

(Create `Archive` if missing.)

## Rules

- Spec describes final behavior; not a build log
- No silent edits to README, technical brief, or other repo docs—approval first
- Stay concise

## Completion

Done when:

- `<change-name>_spec.md` matches the implementation
- Approved documentation updates are applied (or none were needed)
- Change folder is under `Archive/`

Then:

1. Summarize: key outcomes, doc updates made, archive path
2. Confirm to user that implementation and documentation is complete.