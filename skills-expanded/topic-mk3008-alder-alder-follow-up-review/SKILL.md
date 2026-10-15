---
name: alder-follow-up-review
description: Apply supplied human decisions and maintain Alder Check-to-Test evidence after an implementation review. Use for "Alderレビューのフォローアップをして", "この人間判断をAlderレビューへ反映して", or "Alderのチェックとテストの対応を更新して". Scoped record maintenance, not independent read-only review, new Check drafting, generic implementation, or automatic business approval.
license: MIT
---

# Follow up an Alder review

Read [current traceability guidance](references/check-item-traceability.md) in full and [adoption](references/adoption.md#4-run-a-separate-alder-review-after-implementation) section 4 plus its Check Item section. For optional drift reconciliation, additionally read [the pilot reconfirmation workflow](references/study.md#reconfirmation-workflow-for-an-opt-in-pilot). These pinned bundled authorities supply the workflow; no user-side Alder knowledge checkout is needed.

Locate project instructions and the requested prior review, actual human decisions, Business Design, Check list, documented implementation rationales, tests/assertions and their execution evidence. Use established paths; ask only for ambiguous or missing inputs needed for the requested changes. Record each input revision or exact working-tree scope. Retain the prior review's supplied SR sources, revisions, applicable scope and evidence gaps. Compare them with current inputs before dependent record updates; if SR or another relevant source changed, keep the old result visibly pinned and return the affected scope for review. Continue genuinely unaffected records. Do not convert SR findings into new Check Items or resolve BD/SR conflicts through record maintenance. Do not silently replace a missing independent review with the implementer's self-approval. If it is missing, report that remaining gate and perform only independent record preparation supported by actual evidence.

## Decisions and meaning

Map each supplied decision to its affected finding and responsible person. Keep unresolved or explicitly deferred questions open. Business Design is the SSOT; neither the review's suggestion, a Decision Record, existing behavior nor passing tests can answer an undecided business policy.

For a decision changing meaning, revise Business Design first only if that edit is requested; use `alder-draft-business-design` and its bundled authoring guidance. Preserve the actual decision and its limits. Do not label new wording agreed unless the responsible human's confirmation covers it. Await confirmation of unresolved changed meaning before changing affected downstream expectations. Continue independent confirmed items. For changes beyond the requested records, return a bounded handoff rather than silently editing code or tests.

Record confirmed material assumptions/choices and their reasons in the existing Decision Record format/location when requested. Use the implementer's documented rationale and actual decisions, not invented retrospective reasons. A missing rationale remains a question. Distinguish technical implementation choices from business decisions; routine reversible choices do not require a new approval record.

## Check-to-Test evidence

Compare confirmed expectations and precise conditions against actual representative test assertions and available execution results. A matching name, an existing edge or a pass result alone proves no semantic coverage. Keep design revision, list revision and Check ID connected to the test/assertion. Maintain forward and reverse Business Design ↔ optional Interface ↔ Check ↔ Test navigation; never a permanent Code/file/symbol/SQL/line map.

Update only requested affected mappings and evidence gaps in the same Check detail. Preserve IDs, expectation meaning, human review state and unrelated mappings. Distinguish mapped, partial/missing evidence, ambiguous mapping, conflicting behavior and candidate/unapproved. Static assertion inspection and an observed passing execution are different evidence; identify never-run/failed/stale execution separately. Do not reclassify confirmed meaning as undecided merely because regression evidence is incomplete. Unapproved expectations cannot prove a product defect.

If a Check itself needs correction, use the Check-maintenance workflow and its meaning-preservation audit. If meaning would change, return to Business Design first. Do not weaken Checks to fit current tests. Do not add a general complete-test-evidence requirement to the earlier design handoff.

## Optional pilot pins

Only in an already chosen compatible pilot and when reconciliation updates are explicitly requested, compare each affected source to its Check and its changed Check to actual assertions. Update only edges whose semantic reconciliation is complete; record the evidence/reason using the project's normal review records. Leave unresolved candidates stale. A source reconfirmation with unchanged Check body leaves matching Test pins untouched. Test execution alone does not authorize a Test pin refresh. Never bulk-acknowledge, regenerate a baseline, migrate formats or equate fingerprints with human confirmation. Re-run the existing read-only detector after allowed updates and report remaining candidates; absent/incompatible adapter is a limitation, not permission to invent one.

Return changed records, supported findings, evidence references, remaining gaps and genuine human decisions. Do not mark the implementation accepted or the business agreed. Code/Test fixes and their execution require a separately scoped implementation task when not already requested. Report the installed Alder version from `../../plugin.json`, [authority provenance](references/provenance.json), product revisions and plugin source commit when known.
