---
name: fortax-bank-statement-to-books
description: Book a client's bank statement and reconcile it to the books. Proves the statement (running balance ties), puts every entry on a ledger, gives a Tally import file, then prepares the BRS with timing items, unrecorded bank entries, proposed journal entries and 40A(3)/269ST/director-transfer flags. For clients who hand over a bank statement instead of books, and for month-end or year-end BRS. Typical asks - "iska bank statement book kar do", "HDFC ka Aug statement Tally me daalna hai", "statement se entries bana do", "BRS bana do", "bank aur books match nahi ho rahe".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Bank formats and narration patterns used by the engine adapted from Hisaabo, https://github.com/hisaabo/hisaabo (O'Saasy License)"
---

# Bank statement to books, and bank reconciliation

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Two jobs on the same statement. **Part A** books a statement for a client who has no books (the engine
reads, proves and ledgers it). **Part B** reconciles a statement to books that already exist and gives
the BRS. The engine does the reading and adding; you judge only which ledger a counterparty belongs to.
The CA imports into Tally, passes the journal entries and signs off.

## Inputs

- The statement for one account and one period: the net-banking **CSV, Excel (.xlsx) or the bank's
  net-banking .xls download**. Look in `<Client>/<FY>/Bank/` or the folder where the CA drops files;
  move it into `<Client>/<FY>/Bank/` first.
- Not accepted: a PDF, a screenshot, a photograph, or an old binary .xls saved by hand. Ask the CA once
  for the net-banking CSV/Excel download for that account and period; say where to click if you know the
  bank (usually Accounts -> Account Statement -> choose period -> Download as Excel/CSV).
- Company name as it is in Tally, and the bank's ledger name in Tally, when the folder or the CA has them.
- For Part B: the bank ledger from the books for the same period (Tally/Busy/Zoho export, .xlsx/.csv),
  and last period's BRS if one exists (its open items carry forward).
- The client's ledger list, trial balance or an earlier Tally export, if any: use its ledger names.

## Part A — book the statement

### Step 1 — run the engine

```bash
python3 scripts/fortax.py bank --statement "<Client>/<FY>/Bank/HDFC_1234_2026-08.csv" \
  --company "Sharma Traders Pvt Ltd" --bank-ledger "HDFC Bank A/c 1234"
```

It writes `<stem>_books.xlsx`, `<stem>_summary.txt` and, only when the running balance ties,
`<stem>_tally.xml`, next to the statement (or in `--out DIR`).

### Step 2 — read the summary out as it is

Bank and account, period, total withdrawals and deposits, opening and closing balance, whether the
running balance ties, what was booked by rule, by judgement, and what is in Suspense.
**Never recompute, re-add or re-list anything in it.**

### Step 3 — counterparties in Suspense

When the reply ends with a `NEXT STEP` line, that step is yours, not the CA's. Give each Suspense
counterparty a ledger from its name, the sample narration, and whether money went out or came in:

- a customer paying in -> their party ledger (e.g. `ABC Enterprises Pvt Ltd`, under Sundry Debtors);
- a payment out -> **its expense head by default**, because a bank statement has no bills behind it:
  a stationer -> `Printing & Stationery`, a travel agent -> `Travelling Expenses`, a CA or advocate firm ->
  `Professional Fees`, a landlord -> `Rent`, a repair shop -> `Repairs & Maintenance`;
- a supplier's own party ledger (Sundry Creditors) only when the folder shows the client books that
  supplier's bills in Tally (its name in a purchase register, ledger list or earlier Tally export);
- a director or partner -> their capital / current / loan account;
- an own-account transfer -> the other bank's ledger;
- a statutory payment -> the liability it settles (narration patterns like `GST` / `GSTN` / `CPIN` for the
  electronic cash ledger, `CBDT` / `ITNS` / `TIN` for TDS and income tax, `EPFO` for PF, `ESIC` for ESI);
- bank charges and GST on charges -> `Bank Charges` (and input GST where the bank's invoice supports it);
  interest credited -> `Interest Received`; EMI / insurance auto-debits -> the loan or the expense.

Use the client's own ledger names when a ledger list is in the folder. **Leave out any you cannot tell
from the evidence — Suspense is the honest answer.** Write the map to a JSON file:

```json
{"NEFT-ABC ENTERPRISES": "ABC Enterprises Pvt Ltd", "UPI-SWIGGY": "Staff Welfare"}
```

keys exactly as the summary lists the counterparty, and rerun with `--ledger-map map.json`. Then tell
the CA which counterparties you mapped (and to which ledger, so they can confirm) and what stays in Suspense.

### Step 4 — hand over

The workbook and the Tally file sit next to the statement. Tell the CA to check the ledger names match
the company in Tally (a missing ledger fails the import), then Gateway of Tally -> Import -> Vouchers.
GST on purchases, TDS on payments and bill-wise details are not in a bank statement — say so when the
payments are to suppliers or professionals.

### When the running balance does not tie

The reply says at which rows. Rows are missing or mis-read — usually a statement downloaded in pages, a
filter on the download, or a hand-edited file. **No Tally file is made** (and an older one next to the
statement is removed). Ask the CA for the complete statement for the period; do not book around the gap.

## Part B — bank reconciliation (books already exist)

Where the client already keeps books, reconcile rather than rebook. Run Part A's engine on the statement
first: it normalises the bank side and proves the statement ties. Then bring the books' bank ledger to
the same shape. Do the matching in a short script or a workbook with formulas, never by eye.

1. **Normalise both sides** into `date, narration, debit, credit, balance, ref`. Indian formats:
   dd/mm/yyyy, `1,23,456.78`, Dr/Cr suffixes, UPI/NEFT/IMPS/RTGS reference codes, cheque numbers.
   Remember the sides flip: a bank-statement credit is a debit in the books' bank ledger.
2. **Match in this order**, recording the rule used on every pair:
   1. exact amount + date within 3 days + reference (UTR / cheque no);
   2. exact amount within the same month;
   3. split / aggregate — one bank entry against several ledger entries that sum to it (or the reverse).
   A pair matched on amount alone where several candidates exist is a judgement: list it for the CA.
3. **Classify unmatched bank entries**: bank charges / GST on charges, interest credited, auto-debits
   (EMI, insurance), statutory payments (GST cash ledger, TDS challan, PF/ESI — by narration pattern),
   customer receipts not in books, payments not in books, bounced cheques and return charges.
4. **Classify unmatched ledger entries**: cheques issued not presented, deposits in transit, wrong-date
   postings, duplicate entries. Items carried from last period's BRS that still have not cleared get
   their age in days.
5. **BRS** from balance per bank to balance per books, each adjustment listed:

   ```
   Balance as per bank statement on 31-08-2026          X
   Add: Cheques deposited, not yet credited             X
   Less: Cheques issued, not yet presented             (X)
   Add/Less: Bank errors                                X
   Adjusted bank balance                                X

   Balance as per books (bank ledger) on 31-08-2026     X
   Add: Interest / receipts credited by bank, not in books      X
   Less: Bank charges / auto-debits, not in books              (X)
   Add/Less: Errors in books                            X
   Adjusted book balance                                X

   Difference                                           0.00
   ```

   Build it with formulas that pull from the matched sheet, so the difference is computed, not typed.
   Any non-zero difference: follow `fortax-reconciliation` (find the cause; no plug).
6. **Flags for the CA** (rules are for the Income-tax Act, 1961; from tax year 2026-27 the Income-tax
   Act, 2025 applies with new section numbers — check with
   `python3 scripts/fortax.py kb "cash payment disallowance limit" --topics itr` and quote the source):
   - cash withdrawals and cash payments above the s.40A(3) limit (Rs 10,000 per person per day;
     Rs 35,000 for payments to transporters) — round-sum withdrawals especially;
   - payments to the same party split just under a threshold (40A(3), TDS thresholds);
   - cash receipts of Rs 2 lakh or more (s.269ST) and cash loans/deposits of Rs 20,000 or more
     (ss.269SS / 269T);
   - transfers to directors, partners or their relatives (loan to director s.185 Companies Act, deemed
     dividend s.2(22)(e), related-party disclosure);
   - days on which the cash book would go negative.
7. **Outputs** into `<Client>/<FY>/Bank/`, with account and period in the name:
   `BRS_<bank>_<last4>_<YYYY-MM>.xlsx` (matched, unmatched each way, the BRS, a `Source` column on every
   row) and a short `BRS_<bank>_<last4>_<YYYY-MM>_entries.md` with the proposed journal entries for
   unrecorded bank items (format in `fortax-journal-entry`).

Do not post anything to the accounting software yourself; give the entries for the accountant to pass.

## Never

- Book from a PDF, a screenshot, or a statement that does not tie.
- Add up the statement, or type entries yourself — the engine and the formulas do the figures.
- Put a counterparty on a ledger by guess.
- Plug a BRS difference to zero.
- Import into Tally or post entries yourself; the CA imports and posts.

## Credit

The engine's bank formats and narration patterns are adapted from Hisaabo
(https://github.com/hisaabo/hisaabo, O'Saasy License).
