---
name: fortax-advance-tax-and-interest
description: Estimate current-year income, build the advance tax instalment schedule, compute interest u/s 234A, 234B and 234C with a script, tie every challan to 26AS, and prepare the e-Pay Tax challan (advance tax 100, self-assessment 300, regular assessment 400) for the CA to pay. Covers the 44AD/44ADA single instalment, resident senior citizens, and 234C relief for capital gains arising later in the year. Typical asks - "advance tax kitna bharna hai", "15 December ki installment", "234B 234C interest nikalo", "self assessment tax challan bana do", "challan 26AS me nahi dikh raha".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "scripts/compute_interest_234.py from https://github.com/Loki200399/india-itr-copilot (MIT, Copyright (c) 2026 Lokendar Ram P S)"
---

# Advance tax and interest under 234A, 234B and 234C

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).
`scripts/compute_interest_234.py` runs locally (MIT, see `LICENSE-THIRD-PARTY-india-itr-copilot.txt`).

## Do the work, then stop at the payment

The estimate, the instalment working, the interest computation, the challan tie-out and the filled e-Pay Tax
screen are yours. **You never pay.** The CA presses Pay and completes the bank authentication. Refusing the
working because the payment is theirs is a failure. Say where you will stop, then start.

## Step 0 — fix the year, and say which one you are in

FY is April to March; AY = FY + 1. Advance tax is paid **during** the FY on that FY's income; self-assessment
tax after it ends. Both carry the same AY on the challan and are told apart only by the minor head — get that
wrong and the credit lands in the wrong bucket. State at the top of every working: the FY, the AY, the date you
are computing as at, and whether the figures are estimated or actual.

## Step 1 — estimate the current-year income

A forecast, and it must say so on its face. Build it from evidence, not from last year scaled up.

| Head | Evidence | Trap |
|---|---|---|
| Salary | Payslips to date projected for the balance, the employer's TDS projection | Bonus, arrears, ESOP perquisite, mid-year job change |
| House property | Rent agreement, interest certificate | Vacancy; a let-out treated as self-occupied |
| Business or profession | Books to date, prior-year pattern, GST turnover as a cross-check | Year-end provisions, depreciation not yet booked |
| Capital gains | Broker statements to date | A gain arising **after** an instalment date changes 234C — record each date |
| Other sources | Interest accrued, dividend credited, AIS to date | Interest accrued but not yet credited |

Take only deductions the assessee can substantiate today, not what they intend to invest by March;
intentions go in the assumptions block, never into a figure. Compute under the regime that will actually apply
and say which. Slabs, rebate, surcharge and cess come from a verified rules file for that year (the
`fortax-itr` skill's `rules_AY<year>.json`, or `python3 scripts/fortax.py kb "income tax slabs AY <year>"
--topics itr` with its source) — **never from memory and never from last year's working paper.** Use a
spreadsheet with live formulas for the estimate.

## Step 2 — the instalment schedule

The schedule is a sequence of cut-off dates in the FY, each with a cumulative percentage of the year's
estimated liability. The structure is stable; **the dates and percentages are not yours to state from
memory.** Look them up for that FY (`python3 scripts/fortax.py kb "advance tax due dates instalments"
--topics itr`, or the portal) and record each in **Rules used** before computing. Under section 211 as it
stood for recent years they were 15 June / 15 September / 15 December / 15 March at 15% / 45% / 75% / 100% —
confirm for the year.

Two variations rewrite the whole schedule and must be verified rather than assumed:

- Assessees declaring presumptive income under 44AD(1) or 44ADA(1) pay the whole advance tax by 15 March in
  one instalment. This does not extend to 44AE.
- A resident individual aged 60 or more with no business or profession income is outside advance tax (section
  207(2)).

Both are eligibility conditions — confirm each for that year and cite it.

Build one row per instalment: cut-off date, cumulative percentage, cumulative tax required, paid to date,
shortfall. The percentages apply to tax on estimated total income less the TDS and TCS genuinely expected —
take that from 26AS plus what is realistic; an optimistic TDS assumption creates 234B.

## Step 3 — check what has been paid, against 26AS, not against the client

Never compute a shortfall against what the client says they paid. Download 26AS for the AY (the
`fortax-itr-portal-operations` skill, Step 4) and read the advance tax and self-assessment tax part. Record
BSR code, challan serial, date of deposit, amount, minor head and AY for each, tie each to an instalment by
its deposit date, then flag:

- A challan in the folder but not in 26AS — not yet reported, or carrying the wrong PAN or AY. It is not paid
  until it appears. A challan in 26AS under the wrong AY or minor head needs a challan correction, not a second
  payment. Look up the current correction route and its time limit for that challan (portal service,
  bank or assessing officer) before advising.
- A payment made after a cut-off — it counts from its actual date, not the date intended.

## Step 4 — the interest computations

Compute each separately and show the workings. All three are simple interest on a base, for months, at a rate
the Act fixes. **The rate, the rounding and the part-month convention are rules, not memory** — look each up
and record it before multiplying.

| Section | Charged for | Base | Period runs |
|---|---|---|---|
| 234A | Filing after the due date | Tax on total income less TDS/TCS, advance tax and reliefs (tax paid by the due date reduces it) | Day after the due date to the date of filing |
| 234B | Advance tax paid is less than the required share of assessed tax (90% in recent years) | Assessed tax less advance tax paid | First day of the AY to assessment or payment, on the reducing balance |
| 234C | Missing an instalment even where the year total is met | The shortfall at each cut-off | A fixed number of months per instalment |

Verify per year: the threshold below which advance tax is not required at all (₹10,000 in recent years), the
tolerances that excuse a 234C charge on the first two instalments (12% and 36% in recent years), and the relief
where the shortfall comes from income that could not have been estimated at the earlier cut-off — capital
gains, dividends, lottery, a first year of business — which applies only if the tax on it is paid in the
remaining instalments or by 31 March. That is why Step 1 asked for the date of each gain.

Run the script rather than multiplying by hand (individual assessees; for others use a spreadsheet with the
same logic):

```bash
python3 scripts/compute_interest_234.py --tax 150000 --tds 120000 --fy 2025-26 \
  --pay-date 2026-07-30 --due-date 2026-07-31 --file-date 2026-07-30 \
  --age 45 [--non-resident] [--has-business-income] [--presumptive 44AD|44ADA] \
  --advance 2025-09-10:5000 2025-12-12:4000 \
  --payment 2026-05-02:20000 \
  --income-event 2025-11-20:30000 \
  --total-income 1450000 --rate 0.01 --threshold 10000
```

- `--tax` total liability including surcharge and cess; `--tds` TDS + TCS as in 26AS.
- `--advance DATE:AMT` advance-tax challans up to 31 March; `--payment DATE:AMT` self-assessment payments after
  31 March (234B runs on the reducing balance).
- `--income-event DATE:TAX` tax on income that arose on that date (the 234C proviso relief; the script prints a
  VERIFY line reminding you of its condition).
- `--rate` and `--threshold` are defaults — pass the verified values.

The script rounds the base down to the nearest ₹100 and counts a part month as a full month; confirm both
conventions for the year. Read its output as it is. Show 234C instalment by instalment, never as one figure — a
single number cannot be checked by the CA. If tax is still unpaid, state the rupees per month it grows.

## Step 5 — prepare the challan for the CA to pay

The CA logs in to incometax.gov.in -> e-File -> e-Pay Tax -> New Payment. Fill with your browser tool (Claude in
Chrome, a Playwright/browser MCP, or the Codex browser), or give the CA these values:

| Field | Value |
|---|---|
| PAN and name | From the PAN card; check how it renders on the confirm screen |
| Assessment Year | The AY, not the FY |
| Type of payment (minor head) | Advance Tax (100) during the year, Self-Assessment Tax (300) after it, Tax on Regular Assessment (400) against a demand — confirm the label on screen before selecting |
| Tax, then surcharge, cess, interest, penalty, fee | Each in its own box, split exactly as in the working |

Never lump interest into the tax box; a challan split wrongly reconciles badly for years. Then stop at the
gateway — bank sign-in, OTP and the Pay click are the CA's. State the exact total, the minor head and the AY,
and ask for the challan details (BSR code, challan serial / CIN, date) back for the working and the return
(Schedule IT).

## Output and handover

In `<Client>/<FY>/ITR/`, dated, with PAN and AY in the name: the estimate with its assumptions block, the
instalment table, the 26AS challan tie-out, the interest workings section by section (script output attached),
and a one-page payment instruction with the exact amount and heads — never a payment. Hand over the amount, the
minor head, the AY, the date by which paying stops further interest, and what is estimated versus actual, said
plainly.

- **Check before paying**: the AY on the challan is the AY of the working; the minor head matches the purpose;
  the tax / interest split matches the working; the TDS assumed is what 26AS supports; every gain date used for
  234C relief comes from a broker statement in the folder.
- A **Rules used** block for every date, percentage, rate, threshold and tolerance, with source URL and date
  checked, or marked "confirm on the portal / notification" with the section it comes from.
