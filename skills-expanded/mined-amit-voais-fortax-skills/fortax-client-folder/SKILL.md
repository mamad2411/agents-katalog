---
name: fortax-client-folder
description: Keep a CA firm's client folders in order - one folder per client, FY and area sub-folders, a one-page CLIENT.md, dated file names - and file loose documents (GSTR PDFs, 26AS, AIS, Form 16, challans, notices, bank statements, invoice registers) from the folder where the CA drops files into the right client, FY and area. Proposes every move and moves only on a yes; never deletes or renames raw files. Typical asks - "ye files sahi folder me daal do", "naye client ka folder bana do", "folder saaf karo", "kaunsa document missing hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Client folder

A suggested layout, not a rule. If the firm already has its own structure, follow it and only apply
the naming, `CLIENT.md` and never-delete rules below.

## Layout

```
<workspace>/
  <Client Name> (<PAN or GSTIN>)/
    CLIENT.md                <- one page about the client (below)
    Permanent/               <- constitution documents, registrations, PAN/GST/TAN certificates,
                                agreements, board resolutions that outlive a year
    FY 2026-27/
      GST/  ITR/  TDS/  ROC/  Bank/  Audit/  Payroll/  Books/  Notices/  Correspondence/
```

- **FY is the Indian financial year, April to March.** A document belongs to the FY of the period it
  covers, not the date it was downloaded. An ITR for AY 2027-28 lives under `FY 2026-27/ITR/`.
- **Outputs sit next to their inputs**, in the same area folder, with a dated name. A GSTR-1 JSON sits
  beside the sales register it was built from; a 2B reconciliation beside the 2B and the purchase
  register. Monthly areas may use a `YYYY-MM/` sub-folder (`GST/2026-08/`).
- **Portal screenshots** go in the area folder under `screens/` with the date in the name.
- **Working files you create never overwrite anything.** If a name is taken, add `_v2`.

## CLIENT.md

One page, facts only:

```markdown
# Sharma Traders (ABCDE1234F)
Entity: Proprietorship          State: Uttar Pradesh
PAN: ABCDE1234F   GSTIN: 09ABCDE1234F1Z5   TAN: —   CIN/LLPIN: —
GST filer type: monthly / QRMP / composition     ITR form last filed: <form, AY>
Books kept in: <software>        Auditor: <name, if any>
Contacts: <name, role, email, phone>            Language for client mail: English
Bank: <bank name and branch only>
Notes: <standing instructions from the CA>
```

**Never in `CLIENT.md` or any file:** bank account numbers, passwords, OTPs, portal user ids with
passwords, Aadhaar numbers, card details. Fill only what the CA or a document gave you; leave `—` for
the rest and do not guess. Validate PAN and GSTIN format before writing them (see
`fortax-evidence-discipline`).

## Onboarding a client

1. Write `CLIENT.md` from what the CA gives you and the documents in hand.
2. Create the FY and area folders. Do not move the CA's existing files.
3. If existing files are scattered, produce `YYYY-MM-DD_file_index.md` in the client folder listing
   each file, its guessed area, period and suggested destination. Move only after the CA says yes.
4. **Inventory**: for each area, list what is present and what is missing for the current period
   (for example, "GST 2026-08: sales register present, purchase register missing, 2B not downloaded").

## Naming

`YYYY-MM-DD_<Doc>_<Period>_<qualifier>.<ext>`, with the GSTIN or PAN where it helps:

- `2026-09-10_GSTR3B_Aug26_working.xlsx`
- `2026-09-10_ASMT10_reply_draft.md`
- `2026-09-12_Form16A_Q1-FY2026-27_ABCDE1234F.pdf`

Engine outputs keep the names the engine gives them (`GSTR1_<GSTIN>_<MMYYYY>.json`,
`GSTR2B_recon_<GSTIN>_<MMYYYY>.xlsx`); do not rename them.

## Filing loose documents

The CA drops files in one place (a downloads or scans folder, a shared "to file" folder). To file
them:

1. **List the folder.** For each file read enough to classify it: the text of a PDF, CSV or XLSX; the
   file name pattern (`GSTR3B_09ABCDE1234F1Z5_082026.pdf`); a GSTIN, PAN, TAN or CIN inside; the
   period; the document type — GSTR-1, GSTR-3B, GSTR-2B, GSTR-9, 26AS, AIS/TIS, Form 16/16A, challan,
   a notice with its DIN, a bank statement, a sales or purchase register, an invoice.
2. **Match the client** using the GSTIN, PAN or CIN against each client's `CLIENT.md`. A GSTIN
   contains the PAN (characters 3 to 12), so match on that too. If nothing matches, propose a new
   client folder — ask first.
3. **Decide the area** — GST / ITR / TDS / ROC / Bank / Audit / Payroll / Books / Notices /
   Correspondence — and the **FY** from the period (April to March).
4. **Present a table** before moving anything:

   | File | Client | FY | Area | New name |
   |---|---|---|---|---|
   | GSTR3B_09ABCDE1234F1Z5_082026.pdf | Sharma Traders | FY 2026-27 | GST/2026-08 | (keep) |
   | scan001.pdf | Sharma Traders | FY 2026-27 | Notices | 2026-09-05_ASMT10_Aug26.pdf |

   Keep the original name. Propose a new one only when the name is meaningless, like `scan001.pdf`,
   as `YYYY-MM-DD_<doc>_<period>.<ext>`.
5. **After the CA says yes**, move each file (your tool may ask for permission per move; that is
   expected). Never delete. Files you could not match stay where they are, listed in
   `YYYY-MM-DD_unfiled.md` in that folder with the reason.

## Never

- Never delete a file, and never overwrite a raw client file.
- Never move or rename anything before the CA's yes, and rename only a meaningless name.
- Never write outside the workspace the CA gave you.
- Never store credentials, OTPs, Aadhaar or bank account numbers in any file.
