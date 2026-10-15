---
name: alder-explore-functional-conditions
description: Explore undecided functional conditions with Alder after Business Design and correlation review. Use for "Alderで未記載の機能条件を探して" or "この業務設計の機能上の考慮漏れをAlderで確認して". Return read-only, unapproved questions, not Check Item drafting, design-quality review, optimization or implementation review.
license: MIT
---

# Explore functional conditions

Read the bundled [functional consideration discovery](references/functional-considerations.md) in full and the current [traceability authority](references/check-item-traceability.md). Do not ask the requester to select or copy internal Alder documents. This adopted optional inquiry is not a required gate or exhaustive checklist.

Locate the product's instructions, whole applicable Business Design, Scope, existing confirmed Decisions and shared contracts. Record their versions. Confirm the design/correlation-review basis; if it is incomplete, identify the needed design confirmation instead of presenting structural defects as missing functional policies. Ask only for material missing product inputs.

Use concrete situations where multiple observable outcomes could satisfy the existing rules. Distinguish document-derived expectations from questions prompted by external knowledge. Close questions answered by the whole design, confirmed decisions, explicit exclusions or shared contracts before asking the requester. Cite primary sources if external facts are needed, separating those facts from their inferred applicability here. Do not use existing code or another product's features as approval of this product's requirements.

Return only a small useful set, including zero. Each unapproved candidate includes an ID, its affected capability, concrete situation/result difference, design evidence establishing relevance, unresolved choice, knowledge/inference, assumptions, smallest alternatives and implications. Mark 候補・未承認 / 要確認. Do not relabel relevance evidence as evidence for a proposed answer. Routine reversible technical choices need no business question. State briefly why settled or remote questions were closed; claim neither completeness nor improved defect-detection rate.

Keep the work read-only: no Business Design, Check, Test, code or decision-record edits. If people decide a business meaning or guarantee, return it to Business Design revision and confirmation first; only the confirmed version supports downstream Checks. Unapproved inquiry candidates are never pass/fail assertions. Record the installed Alder version from `../../plugin.json`, the [authority provenance](references/provenance.json), input versions and plugin commit when known.
