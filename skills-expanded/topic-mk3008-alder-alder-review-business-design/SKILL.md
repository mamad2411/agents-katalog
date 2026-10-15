---
name: alder-review-business-design
description: Review an Alder Business Design itself for description quality, connections between business activities, and material omissions. Use for requests such as "業務設計書をAlderでレビューして", "この業務設計書をレビューして", or "Alderで業務設計書をレビューして". This is a read-only Business Design review, not implementation review, authoring, optimization, or follow-up.
license: MIT
---

# Alder Business Design review

Use this installed plugin's bundled Business Design guidance as the authority. Read [document structure](references/business-design-structure.ja.md), [description quality](references/business-design-quality-check.ja.md), [business correlation](references/business-design-correlation-check.ja.md), and [omission review](references/business-design-omission-check.ja.md) before reviewing. These are byte-identical copies from one pinned Alder revision recorded in [provenance.json](references/provenance.json). Do not ask the project to copy Alder review documents or substitute implementation behavior for unresolved business meaning.

1. Locate the product repository and its `AGENTS.md`; follow project instructions. Resolve the Business Design from the requested file, a declared project path, or the conventional `docs/business-design/`. If several designs are plausible and the request does not identify one, ask only for the target needed to continue.
2. Read the Business Design as a whole, including connected Activities and Objects. Apply the bundled document structure's “原要求の保持と欄への割当” check to the document-level Scope and every Activity name; factual coherence and complete information do not establish correct field allocation. Review whether the text follows each field's role and whether Input → Procedure → Output, Result → later When, and relevant Exception → receiving Exception When are understandable and internally consistent.
3. Review connections between business activities using the bundled correlation guidance. Check actual handoffs, state/starting conditions, responsibility, constraints, interruption/restart, and completion. Do not treat document order as execution order or invent missing external operations.
4. Check material omissions only where they can change whether the described work succeeds. Use the omission guidance to surface concrete missing conditions or questions, not speculative edge cases or an exhaustive feature checklist.
5. Report the smallest useful set of findings. For each material issue, identify the location, evidence, why it matters to the work, and a correction or question. Separate wording/structure fixes from matters requiring requester/designer business judgment. If the evidence is sufficient, say so rather than manufacturing a finding.
6. Keep the review read-only. Do not edit the Business Design, approve business meaning, decide unresolved business rules, generate Check Items, review code/DDL/tests, or implement the product. Include the installed Alder version from `../../plugin.json` and the pinned Business Design review source revision from provenance in the result.

This skill reviews Business Design itself. Requests whose object is code, implementation, DDL, or tests belong to the separate `alder-review-implementation` skill. Requests to create or revise Business Design belong to `alder-draft-business-design`.
