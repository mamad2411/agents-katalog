---
name: ansvar-privacy-review
description: Review a supplied data processing agreement for GDPR issues with paragraph-level document evidence and fetched legal sources. Use for controller-processor DPA reviews; route a requested processing-risk assessment to an eligible Ansvar DPIA workflow.
license: CC-BY-4.0
---

# Ansvar Privacy Review

Read [account and evidence boundaries](references/grounding.md) first.
The first release reviews controller-processor DPAs. If the user supplies a
privacy notice, joint-controller agreement or another document type, explain
the scope and clarify the requested work before creating a DPA review.

## Prepare the review

Identify the parties' roles, relevant countries, processing activity and whether
the supplied text includes its schedules. Use a document id already authorized
for this review when available. Do not enumerate unrelated library documents.

Check the account's document and workflow access before requesting an upload.
Explain that registering a new DPA stores its text in the organization's Ansvar
library. Honor existing authorization or ask before registration when the user
has only authorized reading an attachment in chat. If upload is unavailable,
explain the boundary; do not silently substitute an unregistered assessment and
claim paragraph verification.

For supplied text or a file whose text the client exposes, use
`register_document_text` after authorization. Retain the filename and use
`text/plain` for extracted PDF/DOCX text. Do not claim the original binary
was uploaded. If the client cannot expose the text, ask for readable or redacted
text; do not invent access or use a presigned upload without HTTP capability.
Wait for `ready`; failed or incomplete registration cannot support a review.
Stop if extraction omits required pages or schedules and clarify the scope.

Read [workflow execution](references/workflow-loop.md) and
[report delivery](references/delivery-rules.md). Discover the live registry and
select an accessible document-review workflow. State its review objective as a
DPA review against fetched GDPR requirements and relevant national or sector
rules, not a blanket declaration of compliance.

## Ground the findings

Use `get_document_segments` and `resolve_document_segment` to read the
paragraphs supporting each finding. Copy returned segment URIs; never construct
one from an assumed paragraph number. Document citations and statutory citations
are different evidence types; `verify_citations` does not verify `doc://` URIs.

Use the [DPA review dimensions](references/dpa-review.md) to organize the work.
Fetch the controlling provisions and exceptions before stating an obligation.
Distinguish absent wording in the supplied material from proven absence in the
entire contract. Identify unread schedules, external policies and incorporation
by reference as scope limits.

For citation-producing steps, record primary-regime, horizontal-regime,
sector-regulator, case-law and authority-guidance passes. Evaluate GDPR, NIS2,
the AI Act, EN 301 549, CSRD and sectoral cyber rules for relevance, without
declaring them all applicable. Resolve source ids; record gated or empty passes
as gaps and inapplicable passes with reasons.

Each finding needs: resolved document paragraph, fetched legal basis, the issue,
practical consequence, proposed amendment for human review, and missing facts.
Label amendments as proposals. Do not mark the agreement approved, contact the
supplier, sign, file, or alter the original contract.

If the user asks for a DPIA instead, scope one processing activity, discover an
eligible DPIA variant and follow its screening and human gates. A DPA review is
not a DPIA, and a DPIA does not establish that a supplier contract is adequate.

Example: Using Ansvar, review this redacted supplier DPA and its schedules,
identify missing safeguards, and propose amendments with paragraph references.
