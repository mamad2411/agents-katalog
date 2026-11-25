---
name: fortax-itr-portal-operations
description: Work the income tax e-filing portal (incometax.gov.in) end to end for a client - new taxpayer registration, representative assessee requests, bank account validation and refund nomination, Aadhaar-PAN and contact checks, downloading 26AS, AIS, TIS, pre-filled JSON and filed returns, uploading the ITR and comparing the preview - then stop at the CA's e-verification. Typical asks - "portal pe register karo", "26AS aur AIS download karo", "bank account validate nahi ho raha", "pre-filled JSON nikal do", "ITR upload karke preview check karo", "legal heir registration".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Income tax portal operations (incometax.gov.in)

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

Everything before Submit and e-Verify is yours: registration screens, profile repairs, downloads, the
pre-filled JSON, every field on the upload screen. Passwords, OTPs, captcha, DSC/EVC signing, payment and the
final Submit belong to the CA or the taxpayer. **Refusing a portal run because it ends in an OTP is a
failure.** Say what you will do and where you will stop, then start.

Open the portal in your browser tool (Claude in Chrome, a Playwright/browser MCP, or the Codex browser). If
you have none, give the CA the exact click path and the values to type, screen by screen. The CA logs in;
never type or store a password.

## Step 0 — fix the year and the person

FY is April to March; AY = FY + 1. Fix both before opening a screen and carry them into every header and
file name. Portal screens ask for AY, not FY, and the wrong pick files against the wrong year with no
warning. Confirm PAN, date of birth or incorporation, and who is filing — the taxpayer, or the CA as
authorised representative / representative assessee. That decides which login is used.

## Step 1 — registering a new taxpayer

Take the Register path on the e-filing site and fill from the documents in the client folder.

| Screen | Needs | From |
|---|---|---|
| Basic details | PAN, name, DOB/DOI, residential status | PAN card, incorporation certificate |
| Category | Individual, HUF, firm, company, trust | Constitution proof, the CA's client details |
| Contact | Primary mobile and email, and whose they are | The CA states this; never assume |
| Address | As per PAN records | PAN card or Aadhaar; a mismatch here delays the OTP letter |

Name and DOB must match the PAN database character for character. That mismatch is the commonest
registration failure — check it against the PAN card before typing, and flag it rather than "correct" it.
Then stop: **the two OTPs and the password are the CA's.** Say which OTPs are coming and to where.

## Step 2 — representative assessee

For a taxpayer who cannot act — deceased, minor, of unsound mind, outside India. The representative raises
the request under their own login, naming the taxpayer, with the legal heir or equivalent certificate, the
death certificate where relevant, and both PANs. Prepare it, upload the annexures, stop at submission.
Approval is the department's and takes time — look the turnaround up, never promise one, and raise the
request first, because nothing can be filed for that taxpayer until it is approved.

## Step 3 — profile items that block a filing (do these before any return work)

- **Bank account validation.** At least one validated account. Validation fails on a name, PAN or IFSC
  mismatch with the bank's record. Read the status column and report exactly what it says — Validated, in
  progress, or Failed with its reason.
- **Refund nomination.** A validated account is not automatically the refund account; confirm the
  nomination is on for the one the CA intends.
- **Contact validation.** Mobile and email verified in My Profile — an unverified contact breaks Aadhaar OTP.
- **Aadhaar–PAN linkage** affects the return, the refund and TDS credit. Look the fee and consequence up
  (`python3 scripts/fortax.py kb "PAN Aadhaar link fee inoperative PAN" --topics itr`); never state them
  from memory.
- **DSC and principal contact / key person** registration for a company, firm or LLP.

Write findings to `ITR_portal_readiness_<PAN>_AY<year>.md` in `<Client>/<FY>/ITR/`, one row per item with
status and a fix owner.

## Step 4 — the downloads

| Document | Where | Note |
|---|---|---|
| Form 26AS | e-File -> Income Tax Returns -> View Form 26AS (redirects to TRACES) | Accept the redirect; the list is AY-wise |
| AIS and TIS | AIS menu, per FY | Take both; TIS is derived, AIS is the source. JSON is easier to parse than PDF |
| Pre-filled JSON | e-File -> File Income Tax Return, or Download Pre-filled Data | Per AY and per form |
| Filed returns, ITR-V, intimations | e-File -> Income Tax Returns -> View Filed Returns | Prior-year carry-forward, comparison |

Work one tab per client per portal, and re-read the page before every click, because element references
change. Files are password protected in the format the portal states (commonly PAN in lower case plus
DOB) — note the format, never a password value. Save into `<Client>/<FY>/ITR/` unrenamed and announce every
path. A pre-filled figure is not a sourced one; it reconciles against the documents like anything else
(the `fortax-itr` skill, Step 2).

## Step 5 — uploading the return

1. Confirm the return data — built with the `fortax-itr` skill, not here — is for the same AY and the same
   form as the computation.
2. e-File -> Income Tax Returns -> File Income Tax Return -> AY -> Online, or offline JSON upload.
3. Upload and let the portal validate. Fix nothing on the portal ad hoc: each validation defect goes back to
   the computation, is corrected there, and the JSON is regenerated. (Known portal quirks and the
   validation-defect catalogue: `fortax-itr` `references/portal-workflow.md`.)
4. Read the preview and compare it against the working paper line by line. Report any difference; never
   adjust the portal to match the paper, or the paper to match the portal.
5. Save a screenshot or PDF of the preview as evidence, then stop at Proceed to Verification.

## Step 6 — the e-verification routes

| Route | Prerequisite | You do | They do |
|---|---|---|---|
| Aadhaar OTP | Aadhaar linked to PAN, mobile registered with UIDAI | Select it, reach the OTP box | Enter the OTP |
| Net banking | Bank on the portal's list, linked to PAN | Select the bank, reach the redirect | Sign in, confirm |
| Bank EVC | A validated, EVC-enabled account | Select it, reach Generate EVC | Generate and enter it |
| DSC | Registered current DSC, signer utility running | Select DSC, reach the token prompt | Token, PIN, sign |

All four end in an act that is not yours; say which applies and what will appear on screen. DSC is mandatory
rather than optional for some categories (for example companies and tax-audit cases) — verify which for this
assessee and AY. A return not verified within the window is treated as never filed. **Never state that
window from memory**; read it off the confirmation screen or `python3 scripts/fortax.py kb "e-verification
time limit ITR" --topics itr`.

## Output and handover

In `<Client>/<FY>/ITR/`, dated: the readiness note, a download manifest (each path and date), the
preview-versus-working-paper comparison, and the acknowledgement number once it exists — never a submitted
return. Hand over with the exact next click, the verification route that applies, and:

- **Check before filing**: AY on screen matches the computation; the form matches; preview totals match the
  working paper; amount payable reads zero with the self-assessment challan reflected; the refund account is
  validated and nominated; every AIS entry is in the return or explained.
- A **Rules used** block for every date, window, fee or limit relied on, with source URL and date checked
  (from `kb` or the portal), or marked "confirm on the portal".
