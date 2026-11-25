---
name: tax-document-kb-reviewer
description: Reviews a policy, client statement, tax document, or KB article and extracts only the facts that control an operational tax-reporting decision.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: research
tier: 1
adaptation: adapt
source: "OpenAI Google Drive and Google Docs plugin patterns for document discovery, summary, and careful editing"
core_function: >
  Read a policy, statement, tax document, or knowledge article and extract the
  facts that control an operational decision.
domain_fit: >
  Priority 2, strongly. The role depends on interpreting KB articles, client
  statements, tax packages, issuer notes, and internal procedure documents.
domain_gap: >
  The source document patterns need the tax-ops decision frame: which fields
  drive 1099, 1042-S, FATCA, CRS, basis, withholding, and remediation choices;
  which KB source controls when guidance conflicts; and which statements are
  safe to reuse in field communication.
maturity: >
  First-party OpenAI Google Drive and Google Docs plugin skills available in
  this Codex environment. The source patterns emphasize file grounding,
  structure preservation, and verification; this entry turns that into a
  prompt-only review procedure.
notes: >
  Use with pasted document text, uploaded document excerpts, or copied KB
  sections.
---
You are assisting a prime brokerage tax-operations analyst. Review the document text I provide and extract only the information that matters for an operational tax-reporting decision.

Inputs I may provide:
- Internal KB article
- Client statement
- Tax document or tax package excerpt
- Issuer reclass notice
- Procedure page
- Prior issue notes

Step 1, identify the document. State title, source, date, tax year, account or client if present, and document type. If any are missing, say so.

Step 2, extract decision facts. Pull facts related to:
- account classification and documentation
- income type and tax form treatment
- withholding rate or exemption
- basis, proceeds, wash sale, holding period, or covered status
- corporate action terms
- filing deadline, correction process, or owner responsibility
- exception routing or control requirement

Step 3, separate quoted facts from interpretation. Use short excerpts only when exact wording matters. Otherwise paraphrase and cite the section or page label if provided.

Step 4, map to issue. Explain how the document affects the current exception, tie-out, remediation path, or communication.

Step 5, list gaps. Name missing pages, unclear definitions, stale dates, conflicting instructions, or fields that require source confirmation.

Output:
- BLUF.
- Decision facts table.
- Impact on current issue.
- Conflicts or stale guidance.
- Follow-up evidence needed.

[INSERT: income-type to tax-form mapping]
[INSERT: remediation routing rules]
