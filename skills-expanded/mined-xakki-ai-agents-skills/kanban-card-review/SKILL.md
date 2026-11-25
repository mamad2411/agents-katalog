---
name: kanban-card-review
description: 'Read-only review of a card lifecycle or a proposed promotion against history, dependencies and evidence, returning APPROVE or REQUEST CHANGES. Use for independent review of card stage changes. RU: ревью карточки, проверка перехода.'
---

# Kanban card review

Read-only review of a card lifecycle, status document or proposed promotion. Do not edit, commit or publish during the review.

## Lifecycle review

Use for read-only review of a card's lifecycle or a status document that cites it. Capture the current source, branch, base, HEAD, affected paths, and repository status when applicable. Inspect the complete baseline-to-HEAD change, not only the last repair.

- Verify one canonical card and ID, its actual stage, any maintained status field, dependencies, acceptance criteria, and referenced cards. Do not infer completion from a directory name alone.
- Read the complete current card and its decisions and execution log. Identify active wording that contradicts later decisions, such as an unresolved promotion question or an obsolete instruction to remain in an earlier stage. Recommend marking superseded statements as historical with the resolving evidence, or removing redundant wording when authorized; retain unresolved future gates.
- Keep `ready` or a pilot handoff distinct from `done`, production rollout, rollback, and any other acceptance gates. Check that roadmap and status claims describe the actual verified endpoint rather than elevating it.
- Run the available read-only board and diff checks; distinguish current results from historical claims and report unavailable checks. A clean linter alone does not prove lifecycle consistency.
- Repeat the relevant final snapshot before the verdict. Classify findings by impact: a false completion or dependency claim that could bypass a security or production gate is high; conflicting path, status, or card text that can misdirect work is medium; stale wording with no active scheduling effect is low. Report each finding with its exact source, contradictory claim, current evidence, impact, and minimum correction. Do not edit, commit, or publish during a read-only review.

See [historical lifecycle wording](references/historical-lifecycle-wording.md) for the targeted review and evidence checklist.

## Promotion review

Use for a read-only verdict on an already proposed or performed lifecycle promotion.

Freeze branch, HEAD, review baseline, untracked files, changed-file summary and diff check; review the complete current card and its change rather than only a later correction. Check the actual stage and any maintained status field, uniqueness, approved scope and exclusions, dependencies, safety boundaries, and required verification claims. Compare current facts to the authoritative sources and related cards; recompute applicable catalog rows, targets and special variants instead of relying on examples, and keep explicitly deferred work separate. Verify any relevant execution identity, resource isolation and security prerequisites remain distinct from output classification.

Inspect the entire card for unresolved questions, unqualified stale decisions, and contradictions. Re-run safe authorized targeted and whole-board lint, diff and relevant static parsing; distinguish current from carried results, and report unavailable checks. A clean linter alone is not proof that scope or acceptance is correct. Repeat the status snapshot before the verdict.

Return evidence-backed `APPROVE` or `REQUEST CHANGES`, with the exact location, contradictory claim, source evidence, impact, and smallest correction for each finding. A confirmed blocking contradiction prevents approval. Do not edit, commit, or publish during this review.

See the [promotion checklist](references/promotion-review-checklist.md) for review evidence and safety boundaries.
