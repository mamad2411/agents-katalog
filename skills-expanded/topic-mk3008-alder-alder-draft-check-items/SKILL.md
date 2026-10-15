---
name: alder-draft-check-items
description: Draft, review for consistency, or update Alder Check Items from agreed Business Design and human feedback. Use for "Alderでチェック項目を作って", "Alderの検査項目を更新して", or an explicit request to organize Functional Interfaces. Preserve human review states and existing IDs. Not an implementation review, Test-evidence follow-up, or business approval.
license: MIT
---

# Draft and maintain Alder Check Items

Read the bundled [current Check Item guidance](references/check-item-traceability.md) in full and [adoption](references/adoption.md#draft-and-review-check-items-required) through the optional Functional Interface section. For initial derivation, read [c3](references/candidate-c3.md). Current adoption and traceability take precedence over historical c3/f1 passages: permanent mappings stop at Test/assertion, never Code, file, SQL entry point or line. Do not fetch newer authority or ask the requester to supply Alder's internal documents.

## Locate the work and choose the requested operation

Read project instructions, then locate the requested Business Design, current Check list and feedback from the request or established project paths. Use `docs/business-design/` only if no project location is declared. Ask only for unreadable or genuinely ambiguous product inputs. Record design/list revisions or precise working-tree scope.

- Initial draft: read the whole applicable completed, business-correlation-reviewed Business Design. Do not read implementation, tests, prior reviews or another derivation to invent its expected results. If the input is explicitly unfinished, offer only a clearly labeled unresolved-input reference draft; never describe it as ready for handoff. If agreement is unknown, ask whether this is the agreed design before representing it as such; independent draft work may proceed as unconfirmed.
- Update: read the existing list, same-ID detail and actual feedback. Preserve stable IDs, human review states and existing Business Design/Test mappings unless an evidenced change requires repair. Existing tests or mappings do not authorize business meaning. Compare before/after guarantees when splitting, regrouping, renaming or regenerating; record intentional removals and their basis. Do not silently discard supporting detail or unrelated Checks.
- Consistency review only: report evidence, missing derivation or feedback conflicts without editing files or changing review states. This is not human confirmation.

Derive one independently reviewable observable expectation per Check using whole-design conditions, connections, roles, data meaning and relevant representative cases. Keep inseparable condition/result pairs together; do not force one Check per assertion or enumerate every combination. Follow c3's two-layer view: short ID/title/expected result/review state for people; same-ID conditions, source evidence, derivation class, confidence and connections for maintenance. Separate explicit, strong derivation and unapproved consideration candidates. Show priority questions in the response as well as the artifact.

New AI drafts start 未レビュー; an unresolved meaning is 要確認. Apply 確認済み only to the exact title, condition and expectation actually confirmed by a responsible human. High confidence, a passing test, a prior confirmed version, or a generic approval of the drafting task is not confirmation of changed meaning. A materially changed expectation requires renewed human review. Keep human feedback requesting correction as 要修正 until the correction is made; correction alone does not assert renewed confirmation. Do not downgrade unchanged human-confirmed meaning merely because Test evidence is missing.

If feedback changes business meaning, conditions or guarantees, or exposes a genuinely undecided outcome, mark the affected item 要確認 and return a focused Business Design question with alternatives and effects. Do not settle it inside Checks. Business Design must be revised and human-confirmed first; only then re-derive affected Checks. Continue independent items. Do not repeatedly solicit explicitly deferred decisions.

## Optional Functional Interface index

Use this mode only when requested or when the requester has chosen it to improve navigation. Read [f1](references/prompt.md) sections 1–2 and 4, subject to the current Test-only boundary above. A small Interface describes observable responsibility, actor, input/precondition, result, preserved facts, source and related Check IDs; it is not a required API, function or file. Preserve existing reviewed interfaces and IDs. Do not generate Checks as a side effect of an interface-only request, and do not turn a draft interface into approved meaning. Direct Business Design → Check → Test needs no extra index where already clear.

Write only the requested Check/Interface artifact(s), using the established format and location. Report changed IDs, retained guarantees, review questions and unresolved items. The design handoff comprises agreed Business Design and human-reviewed Checks with revisions/IDs; it does not require evidence from newly created Tests. When preparing that handoff, apply [security requirement intake](references/adoption.md#carry-security-requirements-into-implementation): carry provided sources, scoped non-applicability and unresolved security inputs separately. Do not convert unknown technical policy into business Checks or claim security readiness. A Check-only draft can continue without a complete SR and does not authorize writing or approving SR. Missing Test evidence is separate from business uncertainty. After implementation, the separate follow-up maintains assertions/evidence; this skill does not implement code or tests or accept an implementation.

Record the installed Alder version from `../../plugin.json`, authority revision/digests from [provenance](references/provenance.json), product inputs and plugin commit when known. Stop with a reviewable draft or requested update, never an AI declaration of human agreement.
