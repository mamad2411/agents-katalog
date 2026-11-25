---
name: ansvar-citation-check
description: Check legal references and quotations in supplied text against sources served by Ansvar. Use for citation audits and checking quoted legal text, not general fact-checking or deciding whether a legal conclusion is correct.
license: CC-BY-4.0
---

# Ansvar Citation Check

Read [account and evidence boundaries](references/grounding.md) before tool use.

## Check the supplied text

1. Extract each legal reference and its exact quotation, keeping its location in
   the input. Ask for the instrument or jurisdiction when ambiguous. A paraphrase
   is not a quotation; label it as interpretation.
2. Discover the relevant served source and fetch each named provision through
   its advertised lookup. Copy the returned routed `source_id` and exact
   `canonical_ref`; keep the user's claimed reference and quotation unchanged.
   If no exact source match is available, retain the row as unresolved.
3. Call `verify_citations` with a unique `subject_id` for each item,
   the source-pinned reference, and the original quotation when present.
   For reference-only checks, omit `quotation`; never submit an empty string.
   Ask for a complete clause when a quote is too short. Respect the live
   schema's batch and byte limits; account for every input item across batches.
4. Preserve each returned verdict, reason and quotation warning, including
   omitted-tail or truncation warnings. `quote_checked` checks the
   quotation against the served body; `reference_resolved` checks the reference
   only. Neither establishes legal force, currency, pinpoint accuracy or support
   for the conclusion. `withheld`, `unavailable`, `not_served` and an
   exhausted verification budget remain unresolved, never false or nonexistent.
5. If a quotation differs, display the difference and any fetched candidate
   correction separately. Do not silently replace the quotation and mark the
   original as verified. Preserve the same distinction for a wrong article.
6. Produce a table: input location, claimed reference, quotation supplied,
   tool verdict, source link, and action needed. State the number submitted,
   checked and unresolved from the actual results, including unprocessed items.
   Finish with the scope of the check, not an overall legal-validity badge.

This skill uses read-only discovery, search, exact lookups and verification.
It does not need document registration, workflow creation or audit-package
export. Do not start those operations for a pasted-text citation check.
Request signed evidence only when the user asks and their entitlement permits;
signatures attest integrity and provenance, not legal validity.

Example: Using Ansvar, check the references and quotations in this legal memo
and show which items you could not verify.
