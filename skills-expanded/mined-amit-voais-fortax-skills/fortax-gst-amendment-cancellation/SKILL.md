---
name: fortax-gst-amendment-cancellation
description: Change or end a GST registration - REG-14 core and non-core amendment, REG-16 cancellation by the taxpayer with stock and ITC reversal working, REG-17 show cause and REG-18 reply, REG-21 revocation, and the GSTR-10 final return. Prepares every field, working and draft reply, stops at EVC/DSC. Typical asks - "GST me address change karna hai", "partner add karo", "GST number cancel karwana hai", "cancellation notice aaya hai", "revocation file karo", "GSTR-10 bharna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GST amendment, cancellation and revocation

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Each of these ends in an EVC, a DSC or an Aadhaar authentication — the last step, not the whole job.
**Refusing the job because its final click is the CA's is a failure.** The fields, the stock working, the
annexures, the portal navigation and the draft reply are yours. Say where you stop, then start.

Portal work: the CA logs in (password, captcha, OTP are theirs). Then drive the page with your browser tool
(Claude in Chrome, a Playwright/browser MCP, or the Codex browser), reading the page before every click; if
you have none, give the CA the click path with the value for every field.

## Step 1 — decide which job this actually is

| What the CA says | What it is | Form |
|---|---|---|
| Address changed, partner added, trade or legal name changed | Amendment | REG-14 |
| Business closed, transfer, merger, constitution changed with new PAN | Cancellation by the taxpayer | REG-16 |
| Notice received proposing cancellation | Officer-initiated cancellation | REG-17, reply in REG-18 |
| Already cancelled by the officer, client wants it back | Revocation | REG-21 |
| Cancellation effective, nothing filed since | Final return | GSTR-10 |

A change needing a new PAN — proprietorship to partnership or company, or a shift to another state — is a
fresh registration (`fortax-gst-registration`) plus a cancellation, never an amendment. Say this before any
form is opened.

## Step 2 — amendment (REG-14)

Core fields go to the officer for approval; non-core fields are approved on the portal without one. The split
decides how long the client waits and whether an ARN needs tracking. Typically core: legal name of the
business, principal place of business, any additional place, and addition, deletion or retirement of
promoters, partners, karta, directors or trustees. Typically non-core: bank account, goods and services,
state specific information, most other details. **Do not rely on this list.** The portal's amendment tabs
mark which fields are core: read them, confirm before touching a field, and record what you found in
**Rules used**. The authorised signatory's contact details follow their own OTP route.

Prepare `<Client>/GST/Registration/<date>_GST_amendment_<GSTIN>.md`: field changed, old value, new value,
date of change, reason, and the document that proves it. Then open the amendment application and fill each
changed field, attaching only files already in the client folder.

Stop at Verification. For a core amendment, tell the CA an ARN follows, that the officer may raise a query in
REG-03 answered in REG-04, and that approval comes as an order in REG-15. The window for filing after the
change, and the window to reply to REG-03, are time limits — look them up with
`python3 scripts/fortax.py kb "REG-14 amendment time limit" --topics gst` or on the portal, never from memory.

## Step 3 — cancellation by the taxpayer (REG-16)

Clear the ground first. All returns due up to the intended date of cancellation must be filed and dues
cleared, or the portal blocks the application. List what is pending before drafting. Then build:

- Reason: discontinuance, transfer or amalgamation, change in constitution needing a new PAN, no longer
  liable, or death of the proprietor. And the date sought, with why that date.
- Stock held on the day immediately before it: inputs as such, inputs in semi-finished and finished goods,
  and capital goods, valued from the stock register and purchase invoices with a source column.
- Tax payable on that stock, as the rule prescribes for the period (section 29(5) and Rule 44) — broadly the
  higher of the ITC involved or the output tax on it, capital goods worked on the prescribed remaining useful
  life. Confirm the current text; state neither the useful life nor any rate from memory.
- Particulars of the last return filed, with ARN and period. For a transfer, the transferee's GSTIN.

Write `<Client>/GST/Registration/<date>_REG16_stock_and_liability_<GSTIN>.xlsx` with live formulas, fill the
portal form from it, stop at the verification step.

## Step 4 — cancellation by the officer (REG-17 and REG-18)

The notice is REG-17. Pull three things off it: the exact ground alleged, the periods covered, and the date
the reply is due. Do not assume the reply window; read it off the notice. Then cure, do not merely draft:
the missing returns get filed and what is admitted gets paid (the CA files and pays), and you collect the
ARNs and challans. A reply saying the defect is cured, with ARNs listed, beats argument. Draft REG-18 as an
annexure-backed letter: ground, facts, what has been done, evidence list, prayer. Satisfied, the officer
drops proceedings in REG-20; otherwise cancellation is ordered in REG-19. Attach the reply and annexures on
the portal and stop at the signature.

## Step 5 — revocation (REG-21)

Revocation applies only where the officer cancelled the registration; a taxpayer who applied for their own
cancellation cannot revoke it. Check the order before promising anything. Before REG-21 can succeed, every
return up to the effective date must be filed and the tax, interest and late fee paid. Build that list from
the portal's return dashboard, get the returns filed, then draft the application stating the ground on which
cancellation was ordered and how it has since been cured. The officer may propose rejection by notice in
REG-23, answered in REG-24; revocation is ordered in REG-22. The window to apply, and any extension of it,
are time limits — look them up and cite them.

## Step 6 — GSTR-10, the final return

GSTR-10 is filed once, after cancellation, separately from the periodic returns. It reports the stock held on
the day immediately preceding the effective date of cancellation, the tax payable on it, and the ARN of the
cancellation order. Reuse the REG-16 stock working rather than rebuilding it, and reconcile the two: if the
effective date in the order differs from the date applied for, the stock date moves and the figures change.
Where the rule requires the stock statement to be certified by a practising CA or CMA, say so and name what
the certificate must cover. The due date and the late fee for GSTR-10 are looked up, never recalled.

## Rules used

Every time limit, threshold, rate, useful life or fee goes in a **Rules used** block at the end: the rule, the
section / rule / notification, and the `kb` source URL with captured date, or "confirm on the portal /
notification". A `kb` match of `weak` or `none` is not a source.

## What the CA gets

Dated files in the client's GST folder: the amendment note or the stock and liability working, the draft
reply with its annexure index, and a one-page status note carrying every ARN and date. Raw client files are
never renamed or deleted. Always end with **Rules used**, and:

**Check before filing**
- GSTIN, legal name and effective date on the form against the order or the proving document.
- Whether the amended field is core or non-core, as the portal marks it, and the approval route.
- Every pending return filed and every due paid, with ARNs and challans listed.
- Stock date matched to the effective date of cancellation, totals computed by formula from the rows.
- Which authentication applies — EVC or DSC — and that the CA presses it.
