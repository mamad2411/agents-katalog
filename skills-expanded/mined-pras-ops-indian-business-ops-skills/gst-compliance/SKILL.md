---
name: gst-compliance
description: >-
  India GST operations: GST returns (GSTR-1, GSTR-3B, GSTR-9, CMP-08), the QRMP scheme and
  IFF, HSN/SAC classification and slab rates, the CGST/SGST/IGST split, reverse charge, and
  input tax credit (ITC) eligibility and GSTR-2B reconciliation; bundles a GSTIN validator and
  a tax-split helper. Use when the task is a GST return, a GST rate or ITC question,
  validating a GSTIN, or how much GST applies. NOT for the invoice document itself (mandatory
  fields, e-invoice IRN/QR, e-way bill) — that is invoicing-einvoice-eway; NOT for moving data
  in/out of Tally — that is tally-operations.
---

# GST compliance (India)

Goods and Services Tax is India's destination-based indirect tax. This skill helps a business
**prepare, understand and reconcile** GST work. It does not file on the user's behalf and does not
state anyone's final liability as advice — it gets the structure right and routes every live
number to the official portal.

> [!IMPORTANT]
> Rates, slabs, thresholds and due dates change (GST was overhauled on 22 September 2025). Never
> assert a current rate or date from memory. Confirm it on the GST portal (https://www.gst.gov.in)
> or CBIC (https://www.cbic-gst.gov.in). The reference files here are dated snapshots for
> orientation only.

## First, establish the context

Before answering anything specific, pin down the facts that change the answer. Ask only for what's
missing:

- **Registration type** — regular, Composition scheme, or Input Service Distributor? Composition
  dealers file differently (CMP-08 + GSTR-4), can't collect tax the normal way, and can't claim ITC.
- **Aggregate annual turnover** — this decides monthly vs quarterly (QRMP), e-invoice applicability,
  and HSN-digit requirements. Get the figure; don't assume.
- **State(s) of registration** — GST is state-wise; a business with branches in multiple states has
  a GSTIN and a return set per state.
- **The period** in question, and whether this is a normal filing, a correction, or a notice.

## The return cycle

Most of GST operations is a monthly or quarterly rhythm. The shape:

1. **Outward supplies → GSTR-1** (or IFF under QRMP): every sales invoice, credit/debit note, export
   and advance, with the correct place of supply and tax split.
2. **Summary + payment → GSTR-3B**: a summary of outward tax, ITC claimed, and net cash paid.
3. **ITC check → GSTR-2B**: the auto-drafted statement of credit available from suppliers. ITC is
   claimed in 3B but must be reconciled against 2B.
4. **Annual → GSTR-9 / 9C**: a yearly consolidation (and reconciliation statement) above a turnover
   threshold.

Read [`references/returns-calendar.md`](references/returns-calendar.md) for the form-by-form map,
who files which, and where to confirm the current due dates. It is the file to open for any "which
return / when / monthly or quarterly" question.

## The CGST / SGST / IGST split

Getting the tax *type* right matters as much as the rate:

- **Intra-state** supply (supplier and place of supply in the same state) → **CGST + SGST**, split
  equally.
- **Inter-state** supply, imports, and exports → **IGST**.
- The deciding factor is **place of supply**, which has its own rules (especially for services) —
  not simply where the customer is billed.

If a user has charged the wrong type (e.g. IGST on an intra-state sale), that's a correction to walk
through, not a rate question.

## Rates and classification

Every supply needs an **HSN code** (goods) or **SAC code** (services) and the rate that attaches to
it. The number of HSN digits a business must show depends on its turnover.

Read [`references/rates-and-classification.md`](references/rates-and-classification.md) for the
current slab structure (post-September-2025), how to find the rate for a specific item, reverse
charge (RCM), and the HSN-digit requirement. Do not guess an item's rate — classification disputes
are common; confirm against the portal's rate finder and, when unsure, say so and recommend a CA.

## Input Tax Credit (ITC)

ITC is where most real questions arise ("why can't I claim this?"). Credit is only available when a
set of conditions are *all* met, and several categories are **blocked** regardless. Read
[`references/itc-rules.md`](references/itc-rules.md) before answering any credit-eligibility or
2B-reconciliation question.

## Deterministic helpers — use the script, don't compute by hand

This skill bundles [`scripts/gst_calc.py`](scripts/gst_calc.py) for the parts that must be exact.
Call it rather than working the arithmetic or a checksum out yourself — a validator and a
calculator don't make the mistakes a model making them in prose will, and the whole pack's design
rule is that **code decides the numbers**.

```bash
python scripts/gst_calc.py validate 27AAPFU0939F1ZV   # GSTIN structure + check digit + state
python scripts/gst_calc.py parse    27AAPFU0939F1ZV   # → state, embedded PAN, entity type
python scripts/gst_calc.py split --taxable 1000 --rate 18 --intra   # CGST+SGST (intra-state)
python scripts/gst_calc.py split --taxable 1000 --rate 18           # IGST (inter-state)
```

- **Validate every GSTIN** a user gives you before trusting it — the check digit catches the single-
  character typos that silently block a buyer's input tax credit.
- The `--rate` is **supplied by you from the portal rate finder**, never assumed by the script; this
  is deterministic arithmetic on a rate you've confirmed, not a guess at the slab.
- `split` keeps `cgst + sgst == total_tax` to the paisa, so invoice totals reconcile.

## How to help, concretely

- **Preparing a return:** help assemble and sanity-check the data (totals tie out, tax type correct,
  place of supply sensible, RCM entries present, credit/debit notes included). Produce a clean
  working sheet; the user files on the portal.
- **A reconciliation:** compare the user's purchase register to GSTR-2B and list mismatches
  (missing in 2B, rate differences, GSTIN typos) with the likely cause for each.
- **An error or notice:** identify what rule is in play, explain the options (amendment in a later
  GSTR-1, DRC-03 payment, reply to notice), and point to the official procedure — then recommend a
  professional for anything contentious.
- **A "what rate / which form" question:** confirm the live value on the portal rather than
  answering from memory, and show the user where you got it.

## Privacy

GSTINs embed a PAN, and GST work often involves other identifiers. Before a user pastes invoices
or registers, remind them to share only what's needed and to mask identifiers they don't — a wrong
or over-shared PAN/Aadhaar is both a compliance and a privacy risk. On-device redaction tooling
(e.g. RedactKit) can strip these before text leaves the machine.

## Guardrails

- State the structure confidently; mark any specific number as "verify on the portal" unless the
  user has just given it to you.
- Never present a liability figure as advice. Compute *illustrations* the user can check, and say
  so.
- For penalties, late fees and interest, give the mechanism and point to the portal's calculator;
  the exact figure depends on dates and is best confirmed there.
