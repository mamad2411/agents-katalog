---
name: peppol-bis
description: >-
  Peppol BIS Billing 3.0: send and validate Peppol invoices and credit notes based on EN 16931. Covers Peppol BIS Billing 3.0. Use when sending a Peppol invoice. Triggers: Peppol BIS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Peppol BIS Billing

Peppol BIS Billing 3.0 from OpenPeppol: the Core Invoice Usage Specification of EN 16931 that Peppol uses for invoices and credit notes in UBL, with its semantic data types, VAT and rounding rules and the PEPPOL-EN16931 transaction business rules, read from the published BIS document on docs.peppol.eu.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Invoice sender (seller or service provider), invoice receiver, Peppol Access Point or validator.
- Target version: Peppol BIS Billing 3.0 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 7.2 Semantic data types.** "Whenever a business term is used this term shall always have content and therefore the content is always mandatory."
2. **§ 7.2.7 Date.** "Dates shall not include timezone information."
3. **§ 8.3 VAT Breakdown.** "One VAT Breakdown shall be provided for each distinct combination of VAT category code and VAT rate found in either the line VAT information or the Document level allowance or charges."
4. **§ 9 Rounding.** "All document level amounts shall be rounded to two decimals for accounting"
5. **PEPPOL-EN16931-R001.** "Business process MUST be provided."
6. **PEPPOL-EN16931-R003.** "A buyer reference or purchase order reference MUST be provided."
7. **PEPPOL-EN16931-R004.** "Specification identifier MUST begin with the value 'urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0' and follow the format rules for the identifier."
8. **PEPPOL-EN16931-R008.** "Document MUST not contain empty elements."
9. **PEPPOL-EN16931-R010.** "Buyer electronic address MUST be provided"
10. **PEPPOL-EN16931-R020.** "Seller electronic address MUST be provided"
11. **PEPPOL-EN16931-R051.** "All currencyID attributes must have the same value as the invoice currency code (BT-5), except for the invoice total VAT amount in accounting currency (BT-111)."
12. **PEPPOL-EN16931-F001.** "A date MUST be formatted YYYY-MM-DD."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `en-16931`, `ubl`, `xml-schema`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Peppol BIS Billing 3.0](https://docs.peppol.eu/poacc/billing/3.0/bis/): Specification, Peppol BIS Billing 3.0, May 2026 release, checked 2026-10-06.
