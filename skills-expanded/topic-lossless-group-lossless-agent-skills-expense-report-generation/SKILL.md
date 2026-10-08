---
name: expense-report-generation
description: How to turn raw card and bank statement downloads into a defensible, client-ready expense report. Use whenever the user asks to build an expense report, reconcile AmEx or bank statements, work out "what is this charge for", aggregate reimbursables for a client or trip, split a claim by month, or render an expense PDF; whenever a folder of statement CSVs/PDFs needs to become a submittable document; or whenever the user says "expense report", "reimbursement", "what am I paying for", "which card was that on", "make this a PDF". Encodes the parent-company descriptor trap (Loom bills as ATLASSIAN, Trae as BYTEDANCE), the never-invent-a-product-name rule, the statement-close gap that silently truncates trips, cheap PDF text extraction, and the two-section BASE/EXTENDED structure.
---

# Expense Report Generation

Statement data is not an expense report. The gap between them is identification,
categorisation, and disclosure — and every one of those is where a claim gets
rejected. This skill is the path across.

The deliverable is a document a client's finance team can approve without asking
a single question. Every line names what it bought. Nothing is silently dropped.
Nothing is silently included.

---

## 1. Where the data lives

Statements are financial records. They go in a **gitignored** directory — never in
tracked source. The working layout:

```
private-data/lossless/reimbursable-expenses/
├── amex-business/              statement CSVs + PDFs
├── bank-<institution>-<year>/  bank statement PDFs + .txt extractions
├── receipts/                   per-charge receipts (PDF/email exports)
├── reports/                    generated CSVs, HTML, PDF
├── _all-amex-<year>.csv        merged transactions, with a Statement column
├── _<bank>-debits.csv          parsed bank debits
└── build_*.py                  the generators
```

**Generate, never hand-edit.** Every report is built by a script from the merged
data. A hand-edited CSV cannot be rebuilt when a line changes, and the figures
drift from the source. Categorisation rules live in the script so a rebuild is
deterministic.

Account-to-card mappings, confirmed-personal vendors, and letterhead contact
details are **instance facts** — they belong in the private folder and in agent
memory, not in this committed skill.

---

## 2. Merge before you analyse

Statement CSVs are per-billing-period. Merge them into one file with a `Statement`
column before doing anything else, or you will reason about a partial window.

Two traps in the merge:

- **Dates sort wrong as strings.** `MM/DD/YYYY` string-sorted puts 01/01/2026
  before 12/31/2025. Parse to real dates before sorting or taking a range.
- **Credits are not expenses.** Payments (`MOBILE PAYMENT - THANK YOU`), refunds,
  and statement credits net against charges and will silently deflate a total.
  Filter to `amount > 0` and report the two figures separately.

---

## 3. Bank PDFs: extract text, do not read images

`pdftotext -layout` is available on macOS via Homebrew poppler and is **far**
cheaper than reading statement PDFs as images. A six-statement set extracts in
one command.

```bash
for f in *.PDF; do pdftotext -layout "$f" "${f%.PDF}.txt"; done
```

The parsing shape that matters: bank statements put the **transaction type and
amounts on the dated line, and the merchant name on the continuation line(s)
below it**. Naive line-by-line parsing yields 500 rows of "Electronic Withdrawal"
with no merchant. Gather continuation lines until the next dated line.

Filter to debit types (`Electronic Withdrawal`, `Visa Debit Card Point of Sale
Purchase`, `ATM Withdrawal`, `P2P Zelle Debit`) — transfers and overdraft pulls
are internal movement, not spend.

---

## 4. Identify every vendor — and never invent one

A report whose line items are raw statement descriptors reads as padding. The
report's first content column is **Product / Purpose**; the raw descriptor sits
beside it so a reviewer can verify against the statement.

### The parent-company descriptor trap

The single highest-value pattern in this work. Products routinely bill under the
name of the company that owns them, so a legitimate tool looks like an
unidentifiable charge from a vendor with no footprint in the codebase.

Confirmed instances:

| Descriptor | Actual product |
|---|---|
| `ATLASSIAN` | Loom (Atlassian acquired Loom) |
| `BYTEDANCE` | Trae (ByteDance's AI coding IDE) |
| `AGENT 37` | Hermes agent hosting |
| `POLAR* OPENPANEL` | OpenPanel (billed via Polar) |
| `PADDLE.NET* <name>` | `<name>`, billed via Paddle |
| `GETTIN* <name>` | `<name>`, billed via a reseller |

**How to prove it — timeline continuity.** Pull every charge for both descriptors
in date order. If descriptor A stops the exact period descriptor B starts, on the
same billing day, with no overlap and no gap, it is one subscription that changed
descriptors. Worked example:

```
LOOM   01/11  $48.00     LOOM   04/11  $48.00
LOOM   02/11  $48.00     ATLAS  05/11  $96.00   <- descriptor changes
LOOM   03/11  $48.00     ATLAS  06/11  $96.00
```

Same day of month, no gap, no overlap. That is Loom. Note the rate change at
migration and flag it — a doubling is worth the user knowing about.

A weaker but still usable variant: descriptors that **alternate** month to month
(`BYTEDANCE`, `BYTEDANCE`, `TRAE`, `BYTEDANCE`, `TRAE`) at an identical amount and
billing window. One subscription, inconsistent descriptor.

### Where else to look

1. **The codebase.** `grep` the monorepo for the vendor, its API env vars, its
   config, its workspace URL. Beware false positives: vendored study repos carry
   other companies' placeholder configs (`example.atlassian.net`), and a
   knowledge-base article *about* a product is not evidence of *using* it.
2. **The user's own notes.** A `content/` article dated the same day as the charge
   is strong substantiation — it names the product, the price, and the licence type.
3. **The Chroma corpus** (`search-lossless-corpus`) for prior decisions.
4. **Web search** for the vendor name plus the charge amount.
5. **Ask.** The user knows what they bought. Cheaper than three tool calls.

### Never invent a product name

If it cannot be determined, mark it:

```
** UNKNOWN - identify before submitting **
```

and print a total of the unidentified rows at build time. An invented product name
is materially worse than an admitted blank: the blank prompts one question, the
wrong name destroys the credibility of every other line. Drive the unidentified
total to zero before the report ships; if a vendor resists identification and the
amount is trivial, dropping the line costs less than defending it.

---

## 5. Classification rules

**Confirmed-personal runs first.** Maintain a `PERSONAL` matcher checked *before*
any business categoriser, so a personal vendor can never be matched into a
business category by a later rule. Once the user confirms a vendor is personal,
encode it — do not re-surface it every session.

**Never silently drop.** Every transaction in the window lands in either the
report or a sibling `--excluded.csv` **with a reason**. This is what makes the
work auditable and lets the user reverse a call.

**Never mislabel to make a category tidy.** If the user says "call that group
Audible", the Audible charges become Audible — the Prime Video charge in the same
group does not. Move it to excluded and say so. The raw descriptor is one column
away; a reviewer will see it.

**Categorisation gotchas seen in the wild:**

- **Uber Eats is Meals, not Ground transport.** A rule keyed on `UBER` swallows it.
- **Uber and Uber Eats descriptors carry Uber's HQ address**, not the ride or
  delivery location. `UBER EATS SAN FRANCISCO CA` on a DC trip is not evidence of
  a charge in California. Do not flag it as one.
- **Electronics purchases get their own `Equipment` line.** A $264 Apple Store
  charge filed under "Incidentals" reads as concealment.
- **Domain registration is not hosting.** Split `VERCEL DOMAINS` from `VERCEL INC`.

---

## 6. Two-section structure: BASE and EXTENDED

Where a working agreement lets the user expense things beyond directly-billable
work, split the claim:

- **BASE** — tooling obviously tied to current engaged work.
- **EXTENDED** — logical business expenses not attributable to a live project
  (domain portfolio, research media, business services).

Each section carries its own subtotal; the total sits below both. The reader can
approve, question, or decline a section without unpicking the other.

**Keep the rationale out of the document.** The reason an arrangement exists —
compensation structure, tax characterisation — is context between the user and the
client, not content for a submitted report. The CSV shows categories and amounts.
If the user raises tax treatment, note once that it is worth confirming with their
accountant and move on; do not advise on it, and do not put it in the file.

---

## 7. The statement-close gap

**Statement CSVs end at the billing close date, which lags the present by up to a
month.** A trip that runs past the close date is silently truncated, and the
report implies the trip ended when the data did.

Always compare the claim window against the last transaction date. When the window
extends past it:

1. Surface it as an explicit row in the working CSV — never let it pass silently.
2. Tell the user what is missing and how to close it.
3. **Drop the marker row before rendering the client-facing document.** It is a
   working note, not something the client should read.

Receipts and the *other* card frequently close the gap. A trip's return flight
missing from the AmEx is usually on the personal card — check before concluding
the download is incomplete.

---

## 8. Cross-card reconciliation

Real trips span cards. A receipt naming a card whose last-4 does not match the
business card means the charge is on another account entirely — find it rather
than treating it as missing data.

When a report draws on two cards:

- Carry a **Card** column so every line is traceable.
- Add a footer note explaining why two cards appear. Unexplained, it invites a
  question about whether the claim is doubled.
- **Check for duplicates across sources.** A vendor billing both cards can be
  double-counted by a naive merge. Print the matching rows and verify distinct
  dates and amounts before totalling.

---

## 9. Rendering: HTML → WeasyPrint → PDF

Build HTML, convert with WeasyPrint. It renders the CSS properly, unlike
`cupsfilter`.

```bash
weasyprint report.html report.pdf
```

**Always include `<meta charset="utf-8">` and write the file with explicit UTF-8
encoding.** Without it WeasyPrint reads UTF-8 as Latin-1 and every em-dash renders
as `â€"` across the document.

The report reads from the finalised CSV so printed figures cannot drift from the
reconciled data.

Document anatomy:

- Letterhead: submitting entity, service line, address, phone; "Submitted to
  \<client\>" opposite.
- Meta block: purpose, period, submitted by, line-item count.
- Category summary table.
- Itemised detail, grouped by section → category, with subtotals.
- Total, payment-method note, signature and date lines.

**Clean the payee names for print.** `TST* BARCOCINA 00044BALTIMORE MD` becomes
"Barcocina — Baltimore MD". Truncated descriptors look careless on a submitted
document. Keep the raw descriptor in the CSV.

Verify the PDF by reading page 1 before delivering. Encoding and layout faults are
obvious on sight and invisible in the build log.

---

## 10. Split large claims by month

A multi-month claim submitted as one large figure invites a renegotiation of the
whole thing. Rendered as one report per month plus a summary sheet, the client can
approve, defer, or decline each month independently.

This also **isolates outlier months**. An annual renewal buried in a five-month
total makes the whole claim look like a steady burn rate it is not; broken out, the
anomaly is one line item to explain.

Each monthly report is self-contained — own sections, own subtotals, own signature
line, a footer noting it covers one month and may be approved independently. No
cross-references between months.

Lead with the summary sheet, then the individual reports.

---

## 11. Working posture

The user is a sophisticated operator managing several client relationships. He will
make the judgment calls about what to claim; the job is to make each call
**visible and informed**, not to make it for him.

- Surface the numbers and the risk on a line, then let him decide.
- When he confirms a call, encode it and stop re-raising it.
- When he asks for a target figure that the fixed costs cannot accommodate, say so
  plainly with the arithmetic — do not quietly cut legitimate lines to hit a number.
- Flag the single most audit-prone line in any claim. Usually it is a large
  undocumented meal, a round-number cash withdrawal, or an equipment purchase.
- Cash withdrawals need itemised substantiation. Flag them; never assume.

---

## See also

- `context-v/skills/search-lossless-corpus/SKILL.md` — querying prior decisions
- `context-v/skills/pseudomonorepos/SKILL.md` — where private-data sits in the tree
