---
name: fortax-gst-registration
description: New GST registration (REG-01) end to end - intake sheet from the PAN, Aadhaar, rent agreement and bills the CA gives, a document checklist by constitution, Part A up to the TRN, every tab of Part B with uploads, stopping only for captcha, OTP and the Aadhaar/EVC/DSC verification; then REG-03 query, REG-04 reply and REG-06 certificate tracking. Typical asks - "naya GST number lena hai", "GST registration kar do", "Part B bhar do", "TRN aa gaya aage karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GST registration (REG-01)

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the whole registration. Ask for two things only.

When the CA hands you the details and the documents, you register — not "prepare for". Read the documents,
fill Part A, take the TRN, fill every tab of Part B, upload every file, and run the application up to the
authentication screen. Use your browser tool (Claude in Chrome, a Playwright/browser MCP, or the Codex
browser); if you have none, produce the filled intake sheet and a tab-by-tab click path with the exact value
for every field.

**You ask the CA for exactly two things, and only when the portal asks:**

1. A captcha, whenever one appears (the CA solves it on their screen).
2. The final authentication: the Part A OTPs, and the Aadhaar OTP, EVC or DSC at Verification — and the
   final Submit.

Everything else is yours. Do not ask the CA to type a field you can type, upload a file you can upload, or
confirm a value that is in the documents in front of you. Ask only for what is genuinely missing, and ask
for all of it at once, not one item at a time.

Open with one line: what you are about to do and the two points where you will need them. Then start.

## Reading what the CA gave you

Photographs and scans are readable — a PAN card, an Aadhaar, a rent agreement, an electricity bill, a
cancelled cheque. Read each file and take the fields from it rather than asking.

Check what you read against what the CA typed. Where the document and the message disagree — a name spelt
differently, a PAN that does not match — say which two sources disagree and which you used. Never silently
pick one.

## Step 1 — the intake sheet

Write `<Client>/GST/Registration/<date>_GST_registration_intake.md` and fill what you were given. Ask only
for what is missing, and only what the CA alone knows.

| Field | Needed for |
|---|---|
| Legal name, exactly as on PAN | Part A, and it must match or Part A fails |
| PAN | Part A |
| Constitution (proprietor, partnership, LLP, company, HUF, trust) | Part B, and it decides the documents |
| Mobile and email of the primary authorised signatory | Part A OTP |
| State and district | Part A |
| Principal place of business, with pincode | Part B |
| Nature of possession of premises (own, rented, leased, consent) | Part B, decides the address proof |
| Bank account (optional at registration, required later) | Part B |
| Goods and services actually dealt in | Part B, HSN/SAC |
| Date of commencement, and date liability arose | Part B |

Validate the PAN format (5 letters, 4 digits, 1 letter) and check the 4th character against the stated
constitution: P individual/proprietor, F firm or LLP, C company, H HUF, T trust, A AOP, B BOI, L local
authority, J artificial juridical person, G government. A mismatch is a flag, not something to correct
silently.

## Step 2 — the document checklist

Build the list from the constitution, not from a generic list. For each document say whose it is, what form
it must be in, and whether it is already in the client folder.

Typical shape, to be confirmed for the constitution and the state:

- Identity: PAN and Aadhaar of the proprietor, each partner, or each director.
- Photograph of the promoter and the authorised signatory.
- Proof of principal place of business, matched to the nature of possession: ownership document, or
  rent/lease deed, or a consent letter with the owner's ownership proof, plus a recent utility bill.
  **A rented premises without the agreement stops the filing** — flag it now, not at Part B.
- Constitution proof: partnership deed, certificate of incorporation, trust deed.
- Authorisation: letter of authorisation, or a board resolution for a company or LLP.
- Bank proof: cancelled cheque, or the first page of a passbook, or a statement.

Anything you cannot see in the folder goes in a short "please send" list at the top.

## Step 3 — Part A

Open the new registration page on the GST portal (services.gst.gov.in -> Services -> Registration -> New
Registration). Fill legal name, PAN, state, district, mobile and email exactly as in the intake sheet.

Then stop. **The mobile and email OTPs are the CA's.** Tell them precisely which two OTPs are coming, to
which number and which address, and that you continue the moment they are entered. Wait. Do not guess, do
not resend, do not ask for the OTP to be typed to you.

When the TRN appears, record it in the intake sheet with the date. The TRN has a limited life (the portal
and the TRN mail state the expiry — commonly 15 days; confirm on screen), so say when it expires and keep
the rest of the work inside it.

## Step 4 — Part B, tab by tab

Work the tabs in the portal's own order and record what you filled in each: Business Details, Promoter and
Partners, Authorised Signatory, Authorised Representative, Principal Place of Business, Additional Places,
Goods and Services, State Specific Information, Aadhaar Authentication, and Verification.

- Fill from the intake sheet and the documents in the folder. Never invent a date, an HSN, a turnover
  figure or an address line.
- Upload with your browser tool's file-upload action, using files inside the client folder only. After each
  upload, read the page back and confirm the portal shows the file before moving on.
- Check each file against the portal's stated format and size limit first. Where a document is missing,
  keep going with the rest and list what is left at the end.
- HSN and SAC codes come from what the business actually sells. Where the CA has not said, list your
  reading and ask them to confirm before you enter it.
- Some fields are state specific — professional tax, shops and establishment, excise. Look them up for that
  state rather than assuming.
- Save at each tab. A registration lost to a session timeout is an hour of the CA's day.

## Step 5 — stop at Verification

Fill the verification tab's name and place. Then stop.

Aadhaar authentication, EVC and DSC are the CA's or the taxpayer's, always. Hand over with:

- What is filled, tab by tab, and what is still blank and why.
- Which authentication route applies for this constitution (DSC is mandatory for companies and LLPs).
- The exact next click, and that the ARN appears after it.
- **Check before submitting**: legal name against PAN, address against the proof uploaded, the signatory's
  details, and the HSN list.

## Step 6 — after the ARN

Record the ARN and the date in the intake sheet. Tell the CA that a query in REG-03 may follow, that it is
answered in REG-04 within the stated window, and that the certificate arrives as REG-06. Do not state the
window, the physical verification rule or any fee from memory: look each up with
`python3 scripts/fortax.py kb "GST registration REG-03 reply time limit" --topics gst` or on the portal, and
cite it in the **Rules used** block.

## Rules used

End every reply that relies on a time limit, threshold or fee with a **Rules used** block: the rule, the law
or notification it comes from, and either the `kb` source URL with captured date or "confirm on the portal".
A `kb` match of `weak` or `none` is not a source.

## Output

In the client's GST folder, dated: the intake sheet with the TRN and ARN, the document checklist with what is
still missing, and a short note of what was filled where. Never a submitted application.
