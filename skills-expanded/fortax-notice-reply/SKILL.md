---
name: fortax-notice-reply
description: Read an Indian tax notice completely and draft a point-wise reply for the CA to file - income tax 143(1) adjustment, 139(9) defective return, 142(1), 143(2), 148/148A, and GST ASMT-10, DRC-01, DRC-01A. Extracts DIN, section, due date and amounts, builds a facts-and-evidence table and the reconciliation (26AS/AIS vs return, GSTR-1 vs 3B, 2B vs 3B), cites only verified law, and lays out the next steps. Typical asks - "notice aaya hai reply draft karo", "ASMT-10 ka jawab", "139(9) defective return", "148A notice ka reply", "DRC-01 me ITC mismatch", "due date nikal gayi ab kya karein".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Notice analysis and reply

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

You draft; the CA reviews, signs and files on the portal. You never submit a reply, pay under protest or send
anything to the department or the client.

## Step 1 — read the notice completely

Extract into a header block:

- issuing authority and its address / jurisdiction;
- DIN or reference number (an income tax communication without a DIN needs flagging to the CA);
- section and form (143(1), 139(9), 142(1), 143(2), 148A(b), 148; GST ASMT-10, DRC-01A, DRC-01, and so on);
- date of issue and date of service;
- **response due date**;
- period covered (AY for income tax, tax period / FY for GST);
- amount demanded, with tax, interest, penalty and fee separately;
- each specific discrepancy alleged, numbered as in the notice;
- mode of reply (portal tab, email, physical) and hearing date if any.

Compute days left to the due date and put it at the top. If the due date has passed, say so and outline the
options — adjournment request, condonation, or responding with a request to take the reply on record —
checking which the section allows. For income tax adjustments from CPC processing (143(1)), the line-by-line
comparison and the rectification route are in the `fortax-itr-rectification-and-refund` skill.

## Step 2 — build the reply

1. **Facts table**: each allegation -> our position -> evidence file in the client folder (invoice, ledger,
   GSTR-2B, challan, bank entry, 26AS/AIS extract, Form 16). Attach only files that exist.
2. **Reconciliation** where the notice is a mismatch (GSTR-1 vs 3B, 2A/2B vs 3B, 26AS or AIS vs return): explain
   the difference line by line in a spreadsheet with live formulas, or with the engine where one exists
   (`python3 scripts/fortax.py gstr2b ...` for a 2B vs books mismatch — see the `fortax-gstr2b-reconciliation`
   skill). The unexplained residue is the real exposure; say so to the CA rather than arguing it away.
3. **Legal grounds**: cite a section, rule or circular only when confirmed with
   `python3 scripts/fortax.py kb "<point>" --topics gst,itr` (quote its source and captured date) or the
   official text; mark anything else `[verify citation]`. Common ground to check: GST section 16(2) and 16(4)
   for ITC, rule 36(4), section 73 vs 74 (whether a fraud or suppression element is alleged), section 75(4)
   (personal hearing where adverse action is contemplated); income tax 139(9) defect list, 143(1)(a)
   adjustments and the prior intimation they require, 148A procedure and timelines.
4. **Draft** in formal letter form: To / Subject (with DIN and reference) / Respected Sir or Madam / Facts /
   Submissions (numbered to match the allegations) / Prayer / Annexures list / Authorised signatory block. Plain
   English, no rhetoric, no admissions beyond what the evidence shows.
5. **Timeline and next steps**: what to upload where; whether to pay, or pay under protest (GST DRC-03) — the
   CA's call, with the consequence of each laid out; whether to seek an adjournment or a personal hearing; the
   evidence still needed from the client (draft that request for the CA to send from their own mail or
   WhatsApp).

## Worked example — the shape, not the law

An illustrative ASMT-10 for a made-up GSTIN, to show what Steps 1 and 2 produce. The figures are invented;
the citations are left marked because they were not checked for this example.

```
Notice: ASMT-10 | Ref ZA0709XXXXXXXXX | issued 02-09-2026, served 04-09-2026
Period: FY 2024-25 | Authority: <Range / Ward as printed on the notice>
Due: 04-10-2026 (13 days left on 21-09-2026)
Alleged: (1) ITC in 3B exceeds 2B by Rs 1,84,600   (2) GSTR-1 turnover below 3B by Rs 2,10,000
Demand stated: none yet (scrutiny) | Reply mode: portal, Form ASMT-11
```

| # | Allegation | Our position | Evidence (in `notices/annexures/`) |
|---|---|---|---|
| 1 | Excess ITC Rs 1,84,600 | Rs 1,52,000 is supplier invoices of March filed late by the supplier, visible in 2B of April; Rs 32,600 unexplained | `2B_vs_books_FY2425.xlsx`, `supplier_invoices_March.pdf` |
| 2 | Turnover gap Rs 2,10,000 | Advance received in 3B of Feb, invoice raised in April and reported in that month's GSTR-1 | `advance_register.xlsx`, `invoice_INV-0412.pdf` |

Submissions then follow the same numbering: point 1 argues the Rs 1,52,000 timing difference
`[verify citation]` and tells the CA plainly that Rs 32,600 is the real exposure (pay with interest via
DRC-03, or ask the client for the missing invoices); point 2 is a timing difference with no tax short paid.
The facts table is what the CA reads first; keep one row per allegation, never merge two.

## Output

In the client folder (suggested `<Client>/<FY>/<GST|ITR>/notices/`), dated: `reply_<notice-ref>.md` (or .docx
if the CA prefers), the reconciliation workbook, and an annexure checklist with each file name. End with:

- **Check before filing**: DIN and reference quoted match the notice; the period matches; every annexure named
  exists; every citation verified or marked; amounts in the reply tie to the reconciliation; due date still open
  or adjournment requested.
- A **Rules used** block for every section, time limit and rate relied on, with source and date checked.

Ask the CA to review before anything is filed.
