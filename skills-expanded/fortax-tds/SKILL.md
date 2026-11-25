---
name: fortax-tds
description: Prepare quarterly TDS/TCS returns (24Q, 26Q, 27Q, 27EQ) from the deduction register - PAN checks, section-wise rate and threshold checks, short and late deduction interest, challan mapping, 234E fee - and work TRACES beyond the return - deductor registration, Form 16/16A/27D downloads, conso file, justification report, reading a default, online and offline corrections, and section 197 lower deduction certificates. Stops before FVU upload, OTP, DSC, payment and Submit. Typical asks - "26Q ka working bana do", "TDS return Q3", "TRACES pe default aaya hai", "justification report download karo", "challan mapping galat hai correction karo", "Form 16 download karna hai", "197 certificate verify karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# TDS / TCS returns and TRACES

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

The return working, the TRACES registration screens, every download, reading a default, building the
correction and filling each field are yours. Passwords, OTP, captcha, DSC, the RPU/FVU run and upload, paying a
default, and the final Submit are the CA's. **Refusing a TRACES run because it ends in their authentication is
a failure.** Say where you will stop, then start.

Open TRACES (tdscpc.gov.in) or the e-filing portal in your browser tool (Claude in Chrome, a Playwright/browser
MCP, or the Codex browser) after the CA has logged in; if you have none, give the CA the click path. Never type
or store a password; if an account is locked or a password expired, hand over — never attempt a reset.

**Rates, thresholds and dates.** Every rate, threshold, deposit due date, statement due date, interest rate,
fee and cap comes from `python3 scripts/fortax.py kb "<query>" --topics tds` (quote its source URL and captured
date) or the portal / notification for that FY and quarter. If `kb` returns `weak` or `none`, mark the value
"confirm on the portal / notification" with the section it comes from. **Write none from memory.** From FY
2026-27 the Income-tax Act, 2025 applies, so section and form references may differ from the 1961 Act numbers
used below — confirm which Act governs the period.

Client folder (suggested): `<Client>/<FY 2026-27>/TDS/`, outputs next to inputs, file names with TAN, form
and quarter, e.g. `TDS_26Q_Q3_ABCD12345E_working.xlsx`.

## Step 0 — fix the identifiers first

TRACES is organised by TAN, quarter and form, not by client name. Get all four right before opening a screen:

- **TAN** (format AAAA99999A). A deductor with several TANs has several TRACES accounts.
- **Deductor PAN**, which must match the TAN record.
- **FY and quarter** — Q1 Apr–Jun, Q2 Jul–Sep, Q3 Oct–Dec, Q4 Jan–Mar — always named with its FY.
- **Form** — 24Q salary, 26Q resident non-salary, 27Q non-resident, 27EQ TCS.

Note the login too: deductor, taxpayer and PAO logins are separate, and the deductor login does correction work.

## Part A — preparing the quarterly return

### Inputs

- Deduction register: deductee name, PAN, section, payment/credit date, amount, TDS deducted, deposit date.
- Challan details (from the bank counterfoil or OLTAS / 26AS view): BSR code, challan serial, date, amount,
  minor head (200 deductor-paid, 400 on demand).
- For 24Q: the salary register with Chapter VI-A declarations, the regime each employee chose, Form 12BB.
- The previous quarter's justification report if defaults exist.

### A1. Quarter and due dates

Look up every deposit and statement due date for that year, including the different deposit date for March and
for tax deducted by government offices. Record each in **Rules used**.

### A2. PAN hygiene

- Format AAAAA9999A; the 4th character is the holder type — P individual, C company, H HUF, F firm/LLP, A AOP,
  T trust, B BOI, L local authority, J artificial juridical person, G government.
- Missing or invalid PAN -> the higher rate under section 206AA (206CC for TCS) — look the rate up.
- PAN valid but inoperative (not linked with Aadhaar) -> also the higher rate; flag it as a check item.
- Never guess a PAN. A blank stays blank with a flag.

### A3. Section-wise rate check

Build a table: section, nature of payment, threshold, rate applied, rate expected, difference. Common sections:
192 (salary, at slab under the regime chosen), 194A (interest), 194C (contracts — separate rates for
individual/HUF and others), 194H (commission), 194I (rent — separate rates for plant/machinery and for land or
building), 194J (separate rates for technical services and professional fees), 194Q (purchase of goods), 195
(non-residents — per the Act and the DTAA with a valid TRC and Form 10F), 206C(1H) and other TCS items. **Every
rate and threshold comes from `kb` for that year**, including the higher rate for non-filers where it still
applies.

### A4. Short and late deduction

For each row: expected TDS minus actual. Where deduction or deposit was late, compute interest at the rate
prescribed for each (they differ — late deduction and late payment), from the relevant date, with a part of a
month counted as a full month. Look both rates up before computing, and use a spreadsheet with live formulas.

### A5. Challan mapping

Map deductions to challans by month and section. List unconsumed challan balances and unmapped deductions
separately. BSR code, serial, date and amount must match OLTAS exactly. Never guess a challan serial.

### A6. Late filing fee and penalty

Fee u/s 234E per day of delay, capped at the TDS amount (₹200 per day in recent years — confirm), and the
section 271H penalty exposure where the statement is more than a year late. Mention only if the due date has
passed.

### A7. Output

`TDS_<form>_<quarter>_<TAN>_working.xlsx` (or .csv set) with sheets: deductee-wise detail, section summary,
challan map, defaults (short/late deduction, late payment, PAN issues) with interest, and "Check before
filing". FVU generation in RPU and upload are the CA's. Record the token number only when the CA gives the
acknowledgement.

## Part B — TRACES operations

### B1. Registration and login

Deductor registration needs a statement already accepted for that TAN, its token number (provisional receipt
number), one challan's details, and the deductee PAN–amount combinations the screen asks for. Take all of it
from the filed return in the folder, never from recollection — a wrong combination locks the attempt. Fill the
registration page from the folder and stop at the activation link and code, which go to the CA's email and
mobile; say which two are coming and where. For an existing account the CA signs in (credentials and captcha
are theirs).

### B2. The downloads (queued: request everything first, collect together)

| Item | Menu | For |
|---|---|---|
| Form 16 (Part A and B) | Downloads -> Form 16 | Salary certificate, 24Q, annual; Part B may need the annexure |
| Form 16A, Form 27D | Downloads -> Form 16A / Form 27D | TDS and TCS certificates, quarterly, per deductee |
| Conso file | Statements/Payments -> Request for Conso File | Input for any offline correction |
| Justification report | Defaults -> Request for Justification Report | The reason behind every default, line by line |
| Challan status | Statements/Payments -> Challan Status | Whether a challan is claimed, unclaimed, overbooked |

Conso files and justification reports arrive as password-protected zips needing the TRACES utility. State the
password format the portal shows; never put a password in chat or a file. Save each into `<Client>/<FY>/TDS/`
unrenamed and announce every path. Certificates carry a number and a generation date — record both, since a
reissue supersedes the earlier one and the deductee holds whichever was sent.

### B3. Reading a default notice — split it by type; the total tells you nothing

| Default | Usual cause | Fixed by |
|---|---|---|
| Short deduction | Wrong section, wrong rate, threshold misjudged, invalid/inoperative PAN forcing the higher rate | Correction, plus paying the difference |
| Short payment | Challan unmatched, claimed against the wrong challan, or overbooked | Usually a challan correction, not a payment |
| Late deduction / late payment | Deducted after the liability arose, or deposited after the due date | Interest, then correction |
| Late filing fee u/s 234E | Statement filed after the due date | Paid under the fee head, then reported |
| PAN error | Invalid, or valid but not the deductee's | PAN correction |

Look up each rate, threshold, due date, fee per day and cap for that FY and quarter and record them in **Rules
used**. Then **recompute each default from the deduction register before accepting it**: a short payment
raised only because a challan is unclaimed is no shortfall at all, and paying it twice is a real loss.

### B4. Correcting a return — two routes; choose by what is wrong and say why

- **Online correction** (Defaults -> Request for Correction): challan and PAN corrections, adding a challan,
  paying an interest or fee demand against the statement. Some actions need a DSC registered on the account —
  check that first.
- **Offline correction**: conso file -> RPU -> FVU -> filing. The route for adding deductees and changing
  amounts, sections or annexures. You prepare the data; the RPU run and upload are the CA's.

Correction types:

- **Challan correction.** Move a deduction from an unclaimed or wrongly claimed challan to the right one, or
  split one challan across deductions. BSR code, serial, date and amount must match OLTAS exactly, and a
  challan absorbs deductions only up to its unconsumed balance — show that balance before and after.
- **PAN correction.** There are limits on how many times an entry may be changed and how far the corrected PAN
  may differ from the original — verify both for that year before promising it will go through. A valid but
  inoperative PAN is a different problem: it drives the higher rate, and correcting the statement won't fix it.
- **Adding deductees.** Each new row needs deduction date, payment amount, section and TDS, mapped to a challan
  with balance. New rows almost always create a late deduction or late payment charge — compute it in the same
  working.

Build `TDS_<form>_<quarter>_<TAN>_correction.xlsx` with before, after and reason columns per changed row.

### B5. Lower deduction certificates u/s 197

A deductee applies in Form 13 under their own login for a named deductor, section, period and amount; the
certificate carries a number, a rate, an amount and a validity period.

- **Client is the deductor**: verify the certificate on TRACES before applying it — it names this TAN and this
  section, its period covers the payment date, and the amount already covered is not exhausted. Quote the
  certificate number in the statement against every deduction relying on it; a certificate applied but not
  quoted produces a short deduction default even though the deduction was right. Never treat the rate as
  anything but what the certificate says, and never assume it covers a section it does not name.
- **Client is the deductee**: prepare the Form 13 application — estimated income, existing and estimated
  liability, prior returns and assessment particulars, deductor-wise projected receipts — then stop at the DSC
  or EVC.

## Output and handover

In `<Client>/<FY>/TDS/`, dated: the return working (Part A), a download manifest with each path and date, the
default analysis split by type with your recomputation beside the department's figure, the correction working
with before / after / reason, and the certificate register where 197 applies — never a filed return or
correction, never a payment. Hand over which defaults are genuine, which are mapping, the money between those
readings, and the route chosen and why.

- **Check before filing**: TAN, form and quarter on screen match the working; every challan cited matches OLTAS
  on all four fields; challan balances are sufficient after the changes; every PAN added is validated and
  operative; every 197 certificate verified against this TAN, section and period; interest and fee here match
  what is paid; blanks left blank are flagged, never guessed.
- A **Rules used** block for every rate, threshold, due date, fee and limit, with source URL and date checked,
  or marked "confirm on the portal / notification".
- Do not mark the return as filed anywhere until the CA confirms and gives the token / acknowledgement number.
