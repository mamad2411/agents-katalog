---
name: en-16931
description: >-
  EN 16931: the semantic data model of the core elements of an electronic invoice. Covers EN 16931-1:2017+A1:2019. Use when mapping a core invoice. Triggers: EN 16931, e-invoicing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# EN 16931

EN 16931-1:2017+A1:2019, Electronic invoicing - Part 1: Semantic data model of the core elements of an electronic invoice. The fetched text is the English version included in STN EN 16931-1+A1, announced May 2020, which identifies the European text approved in 2017 with Amendment 1 approved in September 2019 and dated November 2019.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when mapping a core electronic invoice.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a sender or a receiver of a core invoice.
- Target version: EN 16931-1:2017+A1:2019 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "Senders and receivers of e-invoices shall ensure the authenticity and integrity of the invoice according to relevant regulations."
2. **text.** "R32 Identifier 0..1 Scheme identifier The identification scheme identifier of the Deliver to location identifier.If used, the identification scheme shall be chosen from the entries of the list published by the ISO/IEC 6523 maintenance agency."
3. **6.4.1.** "Invoice BG-25BR-17 The Payee name (BT-59) shall be provided in the Invoice, if the Payee (BG-10) is different from the Seller (BG-4)."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

- `peppol-bis`, when the invoice is also a Peppol BIS billing document: `npx skills add ScaleDockHQ/scaledock-skills --skill peppol-bis`
- `ubl`, when the invoice is expressed as UBL: `npx skills add ScaleDockHQ/scaledock-skills --skill ubl`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [EN 16931-1:2017+A1:2019](https://www.normoff.gov.sk/files/docs/e-fakturacia-stn-en-16931-1-a1-614d692fbcaa2.pdf): European Standard, EN 16931-1:2017+A1:2019, November 2019, checked 2026-10-06.
