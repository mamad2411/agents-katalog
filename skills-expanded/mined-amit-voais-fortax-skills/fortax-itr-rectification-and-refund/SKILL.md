---
name: fortax-itr-rectification-and-refund
description: After an income tax return is filed - read the 143(1) intimation against the computation line by line, choose between rectification u/s 154, revised return u/s 139(5), a 139(9) defect response or appeal, prepare the rectification or the response to outstanding demand, and chase a failed or adjusted refund (refund reissue, section 245). Typical asks - "143(1) intimation aaya hai demand dikha raha", "TDS credit nahi mila", "rectification file karni hai", "refund fail ho gaya reissue karo", "245 adjustment ka reply", "demand galat hai disagree karna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Rectification, demands and refunds

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Reading the intimation, finding the difference, choosing the route, drafting the response and filling every
field is yours. Login, OTP, Submit and e-verification are the CA's. **Refusing the whole job because it ends
in their click is a failure.** Fix FY and AY first (AY = FY + 1); an intimation is always for an AY, and a
rectification filed against the wrong one is a wasted month.

Use your browser tool (Claude in Chrome, a Playwright/browser MCP, or the Codex browser) on
incometax.gov.in after the CA has logged in; if you have none, give the CA the click path. Work in
`<Client>/<FY>/ITR/`.

## Step 1 — read the intimation first

A 143(1) intimation arrives by email and sits under e-File -> Income Tax Returns -> View Filed Returns and
under Pending Actions. It is password protected in the format the portal states; note the format only.
Extract into `143(1)_analysis_<PAN>_AY<year>.md`:

- the DIN and date of the order;
- the AY and which return it processed (original, revised, belated);
- the response due date shown on the order, with days left at the top;
- the net amount payable or refund determined;
- the interest and fee lines separately, because that is where most differences sit.

If it shows a demand, also open Pending Actions -> Response to Outstanding Demand — the same demand sits there
with its own window.

## Step 2 — compare it line by line

Never argue with an intimation before finding where it diverges. One table, in Part B-TTI order, your figure
beside theirs: gross total income, Chapter VI-A deductions, total income, tax on total income, rebate,
surcharge and cess, relief, interest under 234A/234B/234C, late filing fee, TDS and TCS credit, advance and
self-assessment tax, net payable or refundable. Add Difference and Cause columns. Only the difference lines
matter after that; an unexplained residue is the real exposure and a question for the CA, not something to
argue away.

Recurring causes, in checking order:

- **TDS credit not allowed** — the deductor has not filed, filed against the wrong PAN, or the entry sits in a
  different AY in 26AS. Check 26AS for that AY before blaming CPC. (The deductor-side fix is a TDS correction —
  the `fortax-tds` skill.)
- **Challan not matched** — BSR code, serial, date or amount typed differently in the return than in 26AS.
  Compare all four.
- **Deduction disallowed** — usually a supporting schedule left blank, or a 10E / 10-IEA / Form 67
  prerequisite not filed.
- **Income added from AIS or 26AS** that the return did not report.
- **Interest recomputed** on a different payment date or instalment position — recompute it yourself with the
  `fortax-advance-tax-and-interest` skill before disputing it.

## Step 3 — choose the route (the wrong one is rejected unread)

| Situation | Route |
|---|---|
| Return was right; CPC made an arithmetic, credit or challan-matching error | Rectification u/s 154 |
| The return itself was wrong — income missed, deduction not claimed, wrong figure | Revised return u/s 139(5) |
| The department has called the return defective | Response u/s 139(9), not 154 |
| A dispute on a position of law, not a mistake apparent from the record | Appeal — escalate to the CA |
| Revised window closed and more income must be offered | Updated return u/s 139(8A) — CA decision |

Two limits decide whether a route is open: the time limit for a revised return and the time limit for a
rectification. **Do not state either from memory.** Look both up for that AY
(`python3 scripts/fortax.py kb "revised return time limit 139(5)" --topics itr`, and the same for section 154)
and put them in **Rules used**; where a window has closed, say so before proposing the route. A rectification
corrects only a mistake apparent from the record — a change of claim is not that. If the CA wants a new claim
after the revised window has shut, say so plainly rather than filing a 154 that will be rejected.

## Step 4 — filing the rectification

Services -> Rectification, for the AY, against the latest processed order. The request type decides everything:

- **Reprocess the return** — nothing to change; CPC re-runs it. For a credit that has since appeared in 26AS,
  or a challan since matched.
- **Tax credit mismatch correction** — corrected TDS, TCS and challan rows only; every row must already exist
  in 26AS for that AY or it fails again.
- **Return data correction** — a corrected JSON regenerated from the corrected computation (the `fortax-itr`
  skill), never by hand-editing the earlier file.

Then read the summary screen, compare it against the analysis note, save a screenshot, and stop at Submit.

## Step 5 — responding to an outstanding demand

Pending Actions -> Response to Outstanding Demand. Each demand takes exactly one position.

| Response | When | What goes with it |
|---|---|---|
| Demand is correct | The comparison confirms it | Nothing; the CA then pays (minor head 400) |
| Disagree, fully or partly | The comparison shows the cause | Reason category, amount disagreed, evidence |
| Already paid | A challan exists | BSR code, serial, date, amount — from 26AS, never from a screenshot |

Pick the reason category that matches the actual cause, not the nearest-sounding one. Write the free text in
the voice of the `fortax-notice-reply` skill: facts, position, evidence file. Attach only files that exist in
the folder. Say plainly what an unpaid demand can do — recovery, adjustment against a later refund, running
interest — without stating the rate or period from memory.

## Step 6 — refund failure, reissue and adjustment

**Failure.** Services -> Refund Reissue names the reason: account closed, name mismatch, IFSC changed after a
bank merger, account not pre-validated, PAN not linked. Fix the cause first — a reissue to the same broken
account fails identically. Validate the account and confirm the refund nomination (the
`fortax-itr-portal-operations` skill, Step 3), raise the reissue, and stop at the CA's Aadhaar OTP, EVC or DSC.

**Status.** Refund status shows on the portal under the filed return and with the refund banker; read what it
says and report it verbatim with the date.

**Adjustment.** Where a refund for one year is proposed to be set off against a demand of another, an
intimation u/s 245 issues with a window to respond. Compare the demand it names against your own analysis for
that year first: agreeing settles the demand; disagreeing keeps it alive and needs reasons on record. Look the
response window up; never assume it.

**Refund interest.** Interest u/s 244A received with a refund is taxable in the year received — note it for
next year's return.

## Output and handover

In `<Client>/<FY>/ITR/`, dated: the line-by-line analysis, the route decision with its reason, the drafted
rectification or demand response, and a refund status note with the bank position — never a submitted
request. Hand over with the route chosen, why it beats the others, and the next click, plus:

- **Check before filing**: the AY on screen matches the order; the DIN quoted matches the order; every TDS and
  challan row cited appears in 26AS for that AY; the bank account is validated and nominated; the response
  window is still open; the recomputed interest was checked, not accepted.
- A **Rules used** block for every window, limit, fee and rate relied on, with source URL and date checked, or
  marked "confirm on the portal / notification".
