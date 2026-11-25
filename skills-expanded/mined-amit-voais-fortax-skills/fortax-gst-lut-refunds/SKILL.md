---
name: fortax-gst-lut-refunds
description: File the export LUT in RFD-11 and build a GST refund claim in RFD-01 - pick the ground and statement (export under LUT, inverted duty, SEZ, wrong head, excess payment, excess cash ledger), invoice-level working paper with Net ITC and adjusted total turnover, portal filing up to the signature, the RFD-03 deficiency reply, RFD-08/09 and tracking RFD-02 to RFD-06. Typical asks - "LUT file karo", "export refund claim", "inverted duty refund", "RFD-01 bana do", "deficiency memo aaya hai", "refund kab tak aayega".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GST LUT and refunds (RFD-11, RFD-01)

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

An LUT and a refund both end in a DSC or an EVC. Everything before it — the eligibility check, the statement,
the invoice-level working paper, the undertakings, the portal navigation — is yours. **Refusing a refund because
the CA must sign it is a failure.** Say where you stop, then start.

Portal work: the CA logs in (password, captcha, OTP are theirs). Then use your browser tool (Claude in Chrome, a
Playwright/browser MCP, or the Codex browser), reading the page before every click; if you have none, give the
CA the click path with the value for every field.

## Part 1 — the LUT (RFD-11)

An exporter (or SEZ supplier) shipping without paying IGST furnishes a Letter of Undertaking in RFD-11, for a
financial year. Fix the FY first and check whether one is on record for it: on the portal, Services -> User
Services -> Furnish Letter of Undertaking (LUT), and read the list already furnished. Before filing, confirm and
record three things: that the client is eligible to give an LUT rather than a bond, whether a bond with security
applies instead, and the two witnesses the form asks for — name, address, occupation. Where a bond applies, the
amount and the form of security are monetary limits: look them up with
`python3 scripts/fortax.py kb "LUT eligibility bond RFD-11" --topics gst` or on the portal, never from memory.
Fill the form, attach the previous year's LUT where the portal asks, stop at the signature, then download the
acknowledgement into the client folder and record the ARN and FY. Tell the CA what the LUT commits the client to
— export within the prescribed period and realise the proceeds, or pay the tax with interest. Do not state that
period or rate without a source.

## Part 2 — refunds (RFD-01)

### Step 1 — fix the ground, because the ground decides everything

| Ground | Statement | Built from |
|---|---|---|
| Export of goods or services without payment of tax (under LUT) | Statement 3 / 3A | Zero-rated turnover, Net ITC, adjusted total turnover |
| Export of services with payment of tax | Statement 2 | Invoices, FIRC or BRC |
| Supplies to SEZ without payment of tax | Statement 5 / 5A | Endorsed invoices, LUT |
| Supplies to SEZ with payment of tax | Statement 4 | Endorsed invoices |
| Inverted duty structure | Statement 1 / 1A | Rate-wise inward and outward turnover, Net ITC |
| Tax paid on the wrong head, intra treated as inter or the reverse | Statement 6 | The two returns and the challan |
| Excess payment of tax | Statement 7 | Return and challan |
| Excess balance in the electronic cash ledger | none | Cash ledger balance |

Export of goods **with** payment of IGST usually needs no RFD-01: the shipping bill is treated as the application
and the refund flows from customs. There the job is reconciliation, not filing — GSTR-1 export table against the
shipping bill and against tax paid in GSTR-3B, plus the EGM. Where nothing has come, read the status on ICEGATE in
a separate browser tab (the CA logs in) and report the error code.

### Step 2 — the working paper is the claim

Write `<Client>/<FY>/GST/Refunds/<date>_RFD01_<ground>_<period>_working.xlsx`, with live formulas, before
touching the portal. It holds:

- The period claimed as a clean range, the FY, and the invoice-level export or inverted-rate register with a
  source column per invoice. Net ITC for the period, tied to GSTR-3B Table 4 and to GSTR-2B (the 2B figures from
  `fortax-gstr2b-reconciliation`), with ineligible or reversed credit removed and shown separately. Adjusted total
  turnover from rows.
- The refund formula for that ground **as Rule 89 reads for that period** — broadly, turnover of the zero-rated
  or inverted-rated supply times Net ITC over adjusted total turnover, less (for inverted duty) the tax payable on
  the inverted-rated supply. Amended more than once: read the current text and cite it.
- The refund claimed, the ledger balance it must not exceed, and a tie-out sheet against GSTR-1 and 3B.

Gather from the folder: export invoices, shipping bills or bills of export, FIRC or BRC for services, SEZ
endorsed invoices, the LUT acknowledgement, the portal's declarations, and the CA certificate where the claim
crosses the limit requiring one — a monetary threshold, so look it up.

### Step 3 — file up to the signature

Select the refund type, period and ground, upload the statement in the portal's own template, let it validate.
Check the bank account selected is validated and is the one the client wants the money in, and that the
credit-ledger debit proposed matches the working paper. Then stop; the CA signs. Record the ARN and date and
download the RFD-02 acknowledgement.

### Step 4 — deficiency memo (RFD-03) and the reply

A deficiency memo is not a rejection. It sends the claim back and, as the rule generally works, the credit is
restored and a **fresh** application is filed after curing the defect. That matters because the two-year filing
time limit (section 54) is counted on the fresh application — check how the period is counted for that FY before
telling the CA the claim is safe. Work the memo point by point in
`<Client>/<FY>/GST/Refunds/<date>_RFD03_reply_<ARN>.md`: the deficiency as worded, what it actually asks for,
what the folder has, what is missing, the fix. Then rebuild the statement and working paper and refile up to the
signature.

### Step 5 — the sanction chain

| Form | What it is |
|---|---|
| RFD-02 | Acknowledgement of the application |
| RFD-03 | Deficiency memo |
| RFD-04 | Provisional sanction, typically on zero-rated claims |
| RFD-05 | Payment order to the bank |
| RFD-06 | Final sanction, or rejection, order |
| RFD-07 | Adjustment against dues, or withholding of the refund |
| RFD-08 | Notice proposing rejection, answered in RFD-09 |

Track the ARN through this chain and record each stage with its date. An RFD-08 gets the same treatment as any
notice: read the ground, answer it point by point in RFD-09 with annexures, stop at the signature. Interest on a
delayed refund exists (section 56) — its rate and start date are numbers, so look them up.

## Rules used

Every time limit, threshold, bond amount, formula version and interest rate goes in a **Rules used** block: the
rule, the section / rule / notification and period it is for, and the `kb` source URL with captured date or
"confirm on the portal / notification". A `kb` match of `weak` or `none` is not a source.

## What the CA gets

Dated files in the client's GST folder: the LUT acknowledgement note, the refund working paper with its tie-out
sheet, the statement in the portal's template, the annexure index, and a status note carrying every ARN and form
in the chain. Raw client files are never renamed or deleted. End with **Rules used** and:

**Check before filing**
- Ground and statement match; the period claimed does not overlap an earlier claim.
- Net ITC and adjusted total turnover computed by formula from the rows and tied to GSTR-1, 3B and 2B, and the
  claim not exceeding the balance in the electronic credit or cash ledger.
- LUT valid for the FY of every invoice in an export-without-payment claim; FIRC or BRC on record for export of
  services; SEZ endorsements for SEZ supplies; bank account validated and correct.
- Whether a CA certificate is required, and the time limit for filing, both confirmed from source.
