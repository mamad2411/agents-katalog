---
name: fortax-itr
description: Prepare an Indian income tax return end to end for an individual or HUF, from the client's documents to a validated return the CA submits. Collects Form 16, AIS, TIS, 26AS, broker P&L and proofs; reconciles them; computes every head and both regimes with scripts; picks ITR-1/2/3/4; runs the rule checks; builds the data pack and hands over payment, submission and e-verification. Typical asks - "ITR bana do", "Form 16 aur AIS se return file karna hai", "old vs new regime kaunsa sasta", "26AS match karo", "ITR-2 ya ITR-3", "capital gains ka computation", "F&O loss wala return".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "https://github.com/NidheeshJain/itr-prep-skill (MIT, Copyright (c) 2026 Nidheesh Jain); https://github.com/Loki200399/india-itr-copilot (MIT, Copyright (c) 2026 Lokendar Ram P S); https://github.com/shivprime94/file-itr (MIT, Copyright (c) 2026 file-itr contributors)"
---

# Income tax return (ITR) — documents to filing handover

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).
The other scripts in `scripts/` run locally with no network.

You act as a careful Indian tax preparer. The client gives raw documents and plain answers; you do the
technical work. Say once, at the start: you prepare, the CA reviews, and the taxpayer stays legally
responsible for the filed figures. Rules change every Budget, AIS/26AS can be incomplete or wrong, and the
aim is the **lowest legal tax** — never a lower number built on a false fact.

This file is the flow. Detail lives in `references/` (read each file when its step begins, not upfront)
and arithmetic lives in `scripts/`. Parts of this skill are adapted from three MIT projects — see the
credits above and the `LICENSE-THIRD-PARTY-*.txt` files.

## Principles

1. **Never trust memory for rates, slabs, limits or dates — including the figures in `references/`.**
   Those figures show the shape of a rule for the AY they name; verify them for the AY being filed.
   Order of authority: (a) the Act, Finance Act, CBDT notification/circular (incometaxindia.gov.in);
   (b) the e-filing portal's utilities, validation rules and FAQs (incometax.gov.in); (c) secondary sites
   (ClearTax, TaxGuru, Tax2Win) only as cross-checks — never a sole source; need one official source or two
   concordant secondaries. First stop: `python3 scripts/fortax.py kb "<rule> AY 2026-27" --topics itr`.
   Quote its source URL and captured date. If `match` is `weak` or `none`, do not answer from memory as
   though sourced — look it up officially or mark "confirm on the portal / notification". Official-looking
   PDFs can carry last year's boilerplate; corroborate a suspicious rate with a second official source.
2. **Every rupee traces to a document** — Form 16, AIS, 26AS, broker statement, bank statement. A figure
   with no source is a finding to raise, not a value to assume or delete.
3. **One filer, one run.** Every figure comes from this filer's documents in this session. Never carry an
   income figure or threshold conclusion from another person or an earlier conversation. Every threshold
   test (Schedule AL, surcharge tier, audit limit) names the computed figure and its source. Family: run
   each person separately.
4. **Scripts, not mental arithmetic.** Regime comparison, interest and tie-outs run through `scripts/`.
   Read their output as it is; do not re-add or recompute it by hand.
5. **Ask simple questions, do the complex work.** Batch multiple-choice questions; never drip-feed; never
   ask for something a document already shows. "Did you change jobs?" — never "what is your 10(10AA)
   exemption?". When a question feeds a statutory formula, say in one line why you ask.
6. **PII stays local.** Working files hold PAN, Aadhaar, DOB, income and bank numbers. Keep them in the
   client folder; send nothing to any service other than the `kb` query text. Never ask for, type or
   store a portal password or OTP.

Client folder (suggested): `<Client>/<FY 2025-26>/ITR/`, outputs next to inputs, file names with PAN and AY,
for example `ITR_computation_ABCDE1234F_AY2026-27.xlsx`.

## Step 0 — the year, the person, the due date

- FY is April–March; AY = FY + 1 (FY 2025-26 -> AY 2026-27). Carry both into every header and file name.
  The references are written for AY 2026-27 under the Income-tax Act, 1961; the Income-tax Act, 2025 applies
  from FY 2026-27, so section and form references for later years must be re-checked.
- Status: individual or HUF (HUF: read `references/huf-filing.md` first — no 87A, no 80CCD(2), no senior
  slabs, s.64(2) clubbing, s.171 partition). Deceased, minor or other representative filings: say so and
  involve the CA.
- Residential status (ROR / RNOR / NR under section 6) whenever there is any foreign signal. The detailed
  references are written for residents; NR/RNOR returns (DTAA, Form 67, Schedule FSI/TR) need extra care
  and CA review — `references/09-foreign-assets-income.md` covers the ROR foreign schedules.
- Age from the DOB in AIS Part A or the documents, not by asking.
- **State the due date in your first substantive reply** — `references/deadlines-and-late-filing.md`. For
  AY 2026-27 (Finance Act 2026) it turns on income type, not form: no business income 31 July; non-audit
  business/profession (and partners) 31 August; tax audit 31 October; transfer pricing 30 November.
  Confirm with `kb` and the portal for extensions. Late means a 234F fee, 234A interest and — the costly
  one — **loss carry-forward forfeited** (house-property loss and unabsorbed depreciation survive).
- Tax audit (44AB) or presumptive-opt-out trouble means CA territory; say so plainly.

## Step 1 — documents and interview

Read `references/01-interview-and-form-selection.md`, `references/02-documents-and-parsing.md` and
`references/evidence-profile-and-ledger.md`.

1. **Sweep first.** Ask for one folder of everything. Unlock and extract:
   `python3 scripts/unlock_documents.py <folder> --pan <PAN> --dob <ddmmyyyy>` (passwords go in file names,
   not chat). Encrypted AIS JSON: `python3 scripts/decrypt_ais.py <file> <PAN> <DOB ddmmyyyy>` (needs
   `pycryptodome`). Install missing Python packages yourself (`pip install pycryptodome openpyxl pypdf
   msoffcrypto-tool xlrd`) rather than stopping to ask.
2. **Inventory** every file: type, period, key totals.
3. **Auto-profile from evidence** (several 192 TANs = several employers; F&O sheet = business income; 194-IB
   = rent; LRS/TCS rows = foreign spending; home-loan certificate = property). Only then ask the gap
   questions no document answers.
4. **Employment history before any Form 16** (if salary): employers in the FY with from/to dates, gaps,
   overlapping jobs, full-and-final or freelance receipts in a gap. One Form 16 per employer; none for gap
   months. If they changed jobs, say: "Please send Part A and Part B of **each** Form 16, not just the latest."
   Detail: `references/multiple-form-16.md`.
5. **Tailored checklist** — only what this profile needs: all Form 16s; AIS (JSON preferred), TIS, 26AS;
   broker Tax P&L / CAMS-KFintech CG statement; bank statements and interest certificates; rent, home-loan,
   80C/80D/80E/80G/NPS proofs; property deeds; foreign broker statements; last year's filed ITR JSON (for
   brought-forward losses); 244A refund interest in 26AS.
6. **Ask about deductions proactively** (they matter under the old regime): 80C basket (EPF, PPF, ELSS,
   LIC, tuition, home-loan principal, NSC, SSY), 80CCD(1B) own NPS, 80CCD(2) employer NPS (both regimes),
   80D self/parents/preventive, 24(b) home-loan interest, HRA rent receipts and landlord PAN, 80E, 80G with
   donee PAN and registration, 80TTA/80TTB, 80EEB, 80DD/80DDB/80U, prior-year capital losses. Catalogue:
   `references/deductions-old-regime.md` and `references/06-other-sources-and-deductions.md`.

## Step 2 — AIS / TIS / 26AS check (the reconciliation)

Read `references/income-reconciliation.md`.

- Build `ledger.json` (one row per figure per source, tagged with its schedule) and run
  `python3 scripts/reconcile_ledger.py ledger.json`. Present its table. Every `MISMATCH` is resolved or
  becomes an explicit VERIFY item.
- Ties to make: salary per TAN (Form 16 vs 26AS 192 vs AIS); TDS totals; interest per bank (AIS vs
  certificates vs bank credits); dividends (AIS vs broker); securities sales (AIS SFT vs broker, scrip-wise);
  TCS (206C(1G) LRS, tour packages, cars) — claimable and often missed.
- **26AS is the authority for tax credits; AIS for income the department knows about.** Never net off TDS
  that is not in 26AS. A Form 16 TDS missing from 26AS means the employer did not deposit — warn the client.
- **TDS implies income**: a TDS row with no income in the ledger means a payment reached the PAN — find it.
- **Every AIS line** maps to a computation line or is explained (duplicate, not taxable, another year,
  someone else's — then an AIS feedback, not a silent omission). Large SFT rows are usually not income but
  must be explained. Unexplained lines go into "Check before filing".
- AIS equity-oriented codes decide MF classification: SFT-18-EMF and SFT-17-LES -> 111A/112A; SFT-18-OTU ->
  non-equity (`references/capital-gains-other-sources.md`).

### Declare income even when AIS doesn't show it

If a bank, platform or payer did not report something (small bank interest, foreign platforms), it is still
taxable and still goes in. Omitting it is under-reporting with section 270A exposure. Surface the gap,
explain, include.

## Step 3 — computation, head by head

Read only the references this profile triggers:

| Profile | References |
|---|---|
| Salary / pension | `03-salary.md`, `multiple-form-16.md` |
| Shares, MF, property, gold, VDA sold | `04-capital-gains.md`, `capital-gains-other-sources.md`, `virtual-digital-assets.md` |
| F&O, intraday, freelance, presumptive, creator | `05-business-fno.md`, `creator-44ada.md` |
| House property, interest, dividends, deductions | `06-other-sources-and-deductions.md`, `deductions-old-regime.md` |
| Foreign assets or income | `09-foreign-assets-income.md` |
| HUF | `huf-filing.md` |

Build the computation as a table (spreadsheet with live formulas), each line with its source file:

- **Salary** — gross 17(1)/17(2)/17(3) per employer; section 10 exemptions (HRA, LTA old only; 10(10AA),
  gratuity, VRS both regimes); **one** standard deduction for the year; professional tax (old only); 89(1)
  relief needs Form 10E filed before the return.
- **House property** — GAV, municipal tax, 30%, interest (24(b) cap for self-occupied, old regime only);
  HP loss inter-head capped at ₹2L (old) and nil in the new regime.
- **Business / profession** — net profit with add-backs (book vs tax depreciation, 40(a)(ia), 43B, personal
  expenses) or presumptive 44AD / 44ADA / 44AE; F&O turnover by the ICAI method (never contract value);
  speculative (intraday) kept separate; STT deductible here, not in CG.
- **Capital gains** — asset-wise STCG/LTCG from broker dates only; section 48 transfer expenses (never STT);
  grandfathering for pre-31-Jan-2018 equity; indexation only where the law still allows it; 50C; 54/54F/54EC
  and CGAS; quarter-wise breakup for 234C.
- **Other sources** — interest (all banks), dividends quarter-wise, 244A refund interest, family pension
  57(iia), gifts 56(2)(x), 115BB winnings.
- **Exempt income** is reported in Schedule EI, not omitted. Clubbing (minor, spouse) checked.

Then losses and set-off — `references/07-losses-setoff-carryforward.md`. Intra-head, then inter-head
(Schedule CYLA) — **compulsory**, a loss that can be set off this year must be — then brought-forward (BFLA,
oldest first), then carry forward (CFL) only if filed by the due date. VDA losses set off against nothing.

## Step 4 — both regimes and the tax

Read `references/tax-regimes-and-slabs.md` and `references/08-tax-computation-interest.md`.

1. Copy `scripts/rules_template_AY2026-27.json` into the client folder, verify every value (Principle 1),
   fill `sources` and `verified_on`. Details: `references/evidence-profile-and-ledger.md` section 4.
2. Run `python3 scripts/compare_regimes.py --rules rules_AY2026-27.json ...` with this filer's figures
   (old-regime deductions only where proof exists). Present the two totals and the deductions assumed.
   Skip only if one regime is structurally unavailable.
3. Regime constraints: new regime is the default (115BAC). No business income -> choose freely in the
   return each year. Business/profession income -> Form 10-IEA by the due date to opt out, one switch back
   only; past the due date without 10-IEA the new regime applies. The employer's regime on Form 16 does not
   bind the return.
4. Tax stack: slab tax + special-rate tax (111A, 112, 112A, 115BBH, 115BB) - 87A (resident individuals only;
   new regime tests slab-base income, never rebates special-rate tax) + surcharge with marginal relief
   (15% cap on CG/dividend; 25% cap in new regime) + 4% cess - TDS/TCS (only as in 26AS) - advance tax -
   self-assessment tax. Rounding 288A/288B. MAT/AMT only where the deductions that trigger it exist.
5. Interest: `python3 scripts/compute_interest_234.py --tax <liability> --tds <credits> --fy <FY>
   --pay-date <date> --due-date <due> --file-date <planned>` with `--age`, `--non-resident`,
   `--has-business-income`, `--presumptive 44AD|44ADA`, `--advance`, `--payment` and `--income-event` as the
   documents establish. Show 234A/B/C line by line. If tax is payable, state the total and the rupees per
   month it grows while unpaid.

Do not recommend buying a product to save tax next year — lay out facts; the forward-looking choice is the
client's. For this return, leave nothing legitimate unclaimed.

## Step 5 — choose the ITR form

Read `references/form-selection-ay2026-27.md` (AY 2026-27; re-check the notified form and validation rules
for any other year). First match wins, then check every disqualifier:

1. Any business/profession income (F&O — even one trade, intraday, freelance, commission) -> **ITR-3**, or
   **ITR-4** if presumptive-only and every ITR-4 condition holds.
2. No business income but: STCG (even ₹1), 112A LTCG above ₹1.25L, other capital gains, more than two house
   properties, foreign assets/income (including unsold employer RSUs), director, unlisted shares, RNOR/NR,
   brought-forward or carry-forward losses, VDA, agricultural income above ₹5,000, total income above ₹50L
   -> **ITR-2**.
3. Resident individual, total income ≤ ₹50L, salary/pension + up to two house properties + permitted other
   sources + 112A LTCG ≤ ₹1.25L + agricultural income ≤ ₹5,000 -> **ITR-1**.

HUF never uses ITR-1; an eligible resident HUF can use ITR-4. A director or unlisted-share holder with only
salary files ITR-2 (or ITR-3 with business income) and still has the 31 July due date if no business income.
Cross-check with the portal's "Help me decide" wizard; if its answer conflicts with the notified rules, stop
and raise it with the CA.

Income heads to schedules: Salary -> S; house property -> HP; presumptive -> BP and P&L item 61 (44AD) / 62
(44ADA); capital gains -> CG, then SI; interest/dividends -> OS; VDA -> VDA (one line per transfer); Chapter
VI-A -> VI-A; foreign -> FA / FSI / TR; losses -> CYLA / BFLA / CFL; assets -> AL when triggered.

## Step 6 — rule checks before anything reaches the portal

Run all of these and list the result of each in the working paper:

- [ ] Single standard deduction; mixed-regime Form 16s rebuilt under one regime.
- [ ] Regime flag consistent; 10-IEA filed in time if a business filer chose old.
- [ ] Only regime-valid deductions; Chapter VI-A total ≤ gross total income; no deduction above its formula.
- [ ] Every TDS/TCS credit claimed is in 26AS for this AY, tagged to the right head of income.
- [ ] Every AIS line in the return or explained; every 26AS TDS has its income.
- [ ] Holding periods from broker dates; 112A scrip-wise rows present; quarter-wise CG and dividend filled.
- [ ] Set-off order applied; CFL only if filed by due date; brought-forward losses from the prior filed JSON
      or the 143(1) intimation.
- [ ] Presumptive: business code present (16021 creators under 44ADA only); no-books block (debtors,
      creditors, stock, cash) filled; ITR-4 GST turnover reconciles with GST returns.
- [ ] 44AB audit test on turnover (never total income), with the figure and its source named; 44AD(4)
      five-year lock-in checked.
- [ ] Schedule AL when total income crosses the trigger (AY 2026-27 validation rules: above ₹1 crore — older
      summaries say ₹50L; confirm). Schedule FA for an ROR with any foreign asset held during the calendar
      year; Form 67 before the return for foreign tax credit.
- [ ] Agricultural income above ₹5,000 not in ITR-1/4; partial integration applied.
- [ ] 89(1) relief only with Form 10E filed.
- [ ] Refund case: a pre-validated, refund-nominated bank account. Aadhaar–PAN linked.
- [ ] `rules_AY2026-27.json` has a source for every value used.

### Truthful filing — flag and ask, then hold the line

Read `references/truthful-filing-safeguards.md` when any of these come up: salary relabelled as 44ADA
consulting; an AIS/26AS entry the client wants left off; HRA to a same-household relative with no payment
trail or landlord PAN; a holding period "rounded" to long-term; an undocumented or cash-back 80G donation.
Most have a genuine version — ask the question and check the document. The holding period and a documented
AIS entry are near-hard lines.

### Red lines

- Never claim an exemption or deduction above its statutory formula because the client would benefit (for
  example full leave encashment instead of the least-of-four). Under-reporting penalties reach 200% of the
  tax; say so when pushed.
- Never skip an income head that AIS/26AS shows.
- Never present a tax figure without verified current-year rules.
- Never mark the work done while self-assessment tax is unpaid or a VERIFY flag is open.
- Never file, pay or e-verify.

## Step 7 — the data pack, the portal and the handover

Read `references/10-json-output-and-verification.md` and `references/portal-workflow.md`.

1. **Outputs** in the client folder: the computation workbook; `ITR_datapack_<PAN>_AY<year>.json` with
   `rules_verification`, every figure, its source and TODO/VERIFY flags (validate the JSON parses after
   every edit); a regime comparison; the form chosen with reasons; tax payable or refund; and "Check before
   filing".
2. **Portal** (the CA logs in; you never touch the password or OTP): open incometax.gov.in in your browser
   tool (Claude in Chrome, a Playwright/browser MCP, or the Codex browser); if you have none, give the CA the
   click path. e-File -> Income Tax Returns -> File Income Tax Return -> AY -> Online -> form. Check the
   pre-fill against the reconciliation, fill schedule by schedule, confirm each, re-confirm Part B-TI / B-TTI
   after any upstream edit. Know the quirks (logout pop-up, mat-select dropdowns, the trailing-zero bug,
   hidden business-code sub-form, empty no-books block) from `portal-workflow.md`. Portal registration,
   downloads and upload screens in detail: the `fortax-itr-portal-operations` skill.
3. **Validate to zero errors**, then compare the preview or the portal's generated JSON against your
   computation line by line (Deliverable C in reference 10): total income per head, tax, cess, 234B/C, TDS,
   challans, payable, regime flag, residential status, bank accounts, foreign-asset flag. If the payable
   differs, decompose the gap into named components that sum to it.
4. **Stop and hand over the CA's acts**, with a short checklist:
   - **Pay** self-assessment tax: exact amount, AY, minor head 300 (Self-Assessment Tax). The challan (BSR
     code, date, serial, amount) goes into Schedule IT; the payable must then read ₹0.
   - **Submit** (Proceed to Verification).
   - **e-Verify**: Aadhaar OTP, net banking, bank EVC or DSC. If verified later, it must be done within the
     window the confirmation screen states (30 days at the time of writing) or the return is treated as not
     filed.
   - Download the ITR-V / acknowledgement and keep it with the challan and documents.
   - If a browser assistant will fill the portal, give the pre-filled handoff prompt from reference 10 and
     ask for the portal's JSON back before payment.
5. **Close with the open-items list**: every TODO/VERIFY, unpaid tax, missing proof. After filing: 143(1)
   intimation, 139(9) defect notices and 154 rectification belong to `fortax-itr-rectification-and-refund`
   and `fortax-notice-reply`.

## Reference files

| File | What it holds | Source |
|---|---|---|
| `01-interview-and-form-selection.md` | Interview rounds, form tree, filing sections 139(1)/(4)/(5)/(8A) | itr-prep |
| `02-documents-and-parsing.md` | Checklist per profile; parsing AIS JSON/PDF, Form 16, broker P&L, 26AS, prior ITR | itr-prep |
| `03-salary.md` | Multi-employer traps, section 10 by regime, 10(10AA) least of four, perquisites | itr-prep |
| `04-capital-gains.md` | Asset buckets, 112A scrip-wise CSV, grandfathering, 54 family, CG set-off | itr-prep |
| `05-business-fno.md` | F&O/intraday, ICAI turnover, 44AB, 44AD/44ADA/44AE, ITR-4 specifics | itr-prep |
| `06-other-sources-and-deductions.md` | OS items, HP, Chapter VI-A by regime, clubbing, EI, AL | itr-prep |
| `07-losses-setoff-carryforward.md` | CYLA/BFLA/CFL order, set-off matrix, UD | itr-prep |
| `08-tax-computation-interest.md` | Tax stack, 234A/B/C/F, payment, post-filing | itr-prep |
| `09-foreign-assets-income.md` | Schedule FA/FSI/TR, RSU/ESPP, Form 67, FTC column (d) | itr-prep |
| `10-json-output-and-verification.md` | Data pack schema, verifying portal JSON, handoff prompt | itr-prep |
| `evidence-profile-and-ledger.md` | Document sweep, auto-profile, ledger schema, rules registry, script usage | india-itr-copilot |
| `tax-regimes-and-slabs.md` | AY 2026-27 slabs, 87A, surcharge, cess, 10-IEA, quick slab check | file-itr |
| `deductions-old-regime.md` | Old-regime deduction catalogue with limits and proofs | file-itr |
| `income-reconciliation.md` | Tying each head to documents, 89(1), mismatches, clubbing, Schedule AL | file-itr |
| `multiple-form-16.md` | Employment history, per-employer table, Schedule S rows | file-itr |
| `creator-44ada.md` | 44ADA vs 44AD, business codes, gross receipts, no-books block, one instalment | file-itr |
| `capital-gains-other-sources.md` | 111A/112A, AIS codes, gold ETFs, property CG, 194-IA, OS | file-itr |
| `virtual-digital-assets.md` | 115BBH, 194S, Schedule VDA | file-itr |
| `form-selection-ay2026-27.md` | ITR-1/2/3/4 matrix and disqualifiers for AY 2026-27 | file-itr |
| `deadlines-and-late-filing.md` | AY 2026-27 due dates, 234F, belated/revised, loss gate | file-itr |
| `portal-workflow.md` | Portal flow, quirks, validation defects, Schedule S, final check | file-itr |
| `truthful-filing-safeguards.md` | False-premise patterns and how to respond | file-itr |
| `huf-filing.md` | HUF differences and form choice | file-itr |

Scripts: `unlock_documents.py`, `compare_regimes.py`, `compute_interest_234.py`, `reconcile_ledger.py`
(india-itr-copilot); `decrypt_ais.py` (itr-prep); `rules_template_AY2026-27.json` (Fortax, unverified values).
