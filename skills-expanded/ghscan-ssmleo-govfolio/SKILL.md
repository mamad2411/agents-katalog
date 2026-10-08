# skill: extraction-strategy
Purpose: choose deterministic vs LLM per document class
Load when: SPEC/BUILD parse decisions
Core checklist:
- text layer present? deterministic first -> measure confidence -> LLM constrained to schema as fallback -> record choice + why in SAF
Anti-patterns: LLM-first on parseable docs; unrecorded strategy flips
Learnings (dated):
- 2026-07-04 (us_house PTR): "text layer present?" is not one question — test DATA
  cells and LABELS separately. Generated PDFs can style labels (small caps) with fonts
  whose reduced glyphs have no ToUnicode: labels extract lossy-but-deterministically
  while data survives verbatim. Anchor grammar on data tokens (date pairs, $-bands)
  and surviving label capitals, never on full label text. Verify with TWO independent
  extractors before blaming the crate; check content-stream order vs layout order —
  layout mode can interleave wrapped cells that content order keeps contiguous.
- 2026-07-05 (uk_commons_register): documented-JSON-API sources invert the drift
  problem — deserialize with deny_unknown_fields on the response ENVELOPE so contract
  drift freezes loudly, while data-carrying vocabularies (per-category field names)
  stay open and land verbatim in Silver. Type money by machine markers
  (typeInfo.currencyCode present), never by field name/number-ness alone: the same
  source ships currencyless Decimals (HoursWorked) beside money Decimals.
- 2026-07-05 (canada_ciec): when LIST cards render free-text blobs, inspect the
  DETAILS page before reaching for an LLM — CIEC list cards flatten summaries into
  `<br>`-joined prose, but the details page carries per-item stable GUIDs + section
  labels (`ciec-declaration-disclosureitem`), turning "blob" into deterministic
  per-item rows. Parse the richest rendering of a document, not the first one seen;
  choose the row unit (per-item vs per-document) per grammar FAMILY and record it
  in the SAF.
Write-back: deepen this file when the procedure teaches you something; same PR.
