---
name: fortax-mca-annual-filing
description: MCA / ROC annual compliance for a company or LLP — AOC-4 (CFS, XBRL), MGT-7 / MGT-7A, ADT-1, DIR-3 KYC, DPT-3, MSME-1, LLP Form 11 and Form 8 — as a filing matrix with due dates, late fees, prerequisites, draft board resolutions and an attachment checklist, stopping before upload and payment. Typical asks: "ROC filing kab tak hai", "AOC-4 MGT-7 bharna hai", "annual filing pending hai kya", "late fee kitni lagegi".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# MCA / ROC annual filings

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## First

Get the entity type, CIN/LLPIN, FY end and AGM date from the client's own records — the previous
year's filings, the certificate of incorporation, the minutes — and from MCA master data. Company vs
LLP vs OPC vs small company changes the form and the fee. For an LLP, the full treatment of Form 11
and Form 8 is in `fortax-llp-filings`.

**Dates and fees are looked up before quoting.** Run
`python3 scripts/fortax.py kb "AOC-4 due date after AGM" --topics mca` and quote its source and
captured date. Where the reply is `weak` or `none`, read the Companies Act, 2013 / LLP Act, 2008 and
the MCA portal and mark the figure "confirm on the portal". Put each in a **Rules used** block.

## Annual cycle (company)

- Board meeting approving accounts → notice of AGM → AGM (section 96). The notice period and the
  outer date for the AGM are statutory and an OPC is treated differently: look both up for this
  company before you put a date on anything.
- **AOC-4 / AOC-4 CFS / AOC-4 XBRL** (section 137), due a set number of days after the AGM.
  Attachments: signed financials, board report, auditor report, CSR annexure if applicable.
- **MGT-7 (MGT-7A for OPC / small company)** (section 92), due a set number of days after the AGM.
  Attachments: list of shareholders, MGT-8 if applicable.
- **ADT-1** (section 139), due within the prescribed days of the AGM where an auditor was appointed.
- **DIR-3 KYC / KYC-WEB**: every DIN holder, by the annual cut-off (see `fortax-mca-director-changes`
  for which form).
- **DPT-3**: return of deposits and exempted amounts, by its annual cut-off.
- **MSME-1**: half-yearly, where dues to an MSME are outstanding beyond the prescribed period.

## Annual cycle (LLP)

- **Form 11** (annual return): commonly due 30 May. **Form 8** (statement of account and solvency):
  commonly due 30 October. Both run from the FY end, not from any meeting — confirm both dates for
  the FY on the MCA portal (LLP Rules, 2009).

## Steps

1. Build a filing matrix for the client as a spreadsheet: form, trigger, due date, status, days left
   (a formula, not typed), additional fee if late. The additional fee for AOC-4 and MGT-7 has been
   ₹100 per day with no cap; other forms are slab-based — verify the current fee rules for the FY
   before quoting either, and compute any late fee with a formula.
2. Verify prerequisites: DSC validity of signatories, DIN status (not deactivated), master data on
   MCA matches the folder (registered office, directors, capital). Open MCA master data in your
   browser tool (Claude in Chrome, a Playwright or browser MCP, or the Codex browser); if you have
   none, give the CA the click path.
3. Draft the board resolution / notice / director's report skeleton where asked, in standard
   Companies Act 2013 language, with blanks marked `[[ ]]` for facts you do not have. Meeting records
   must exist before a form reports them — see `fortax-mca-charges-and-resolutions`.
4. Assemble an attachment checklist with the file names found in the client's ROC folder and mark
   the missing ones.
5. Write `<date>_ROC_<FY>_filing_matrix.xlsx` (or `.md` for a quick view) in the client's ROC folder,
   for example `<Client>/<FY 2026-27>/ROC/`.

## Never

- Never quote an SRN, challan or approval status you did not see in a downloaded document.
- On the MCA portal: browse, download, pre-fill. The CA signs in, affixes the DSC, uploads and pays.
