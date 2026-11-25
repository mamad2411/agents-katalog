---
name: generate-a-profit-and-loss-report
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Generate a profit and loss report for a defined period so revenue, expenses, and net income can be reviewed.

## Preconditions

- You can access reporting in the accounting system.
- The report period and accounting basis are known.
- Recent bank feeds, invoices, bills, payroll, and adjustments are entered as far as practical.

## Steps

1. **Open reports.** Go to reports and choose Profit and Loss, Income Statement, or Statement of Activity. → *Expect:* a report setup screen or default P&L appears.
2. **Set the date range.** Choose the month, quarter, year, or custom period being reviewed. → *Expect:* the report header shows the intended period.
3. **Choose accounting basis.** [BRANCH: cash | accrual] select cash basis for paid transactions or accrual basis for earned and incurred activity. → *Expect:* the report basis is visible in settings or header.
4. **Apply filters.** Add class, location, project, department, customer, or comparison columns if needed. → *Expect:* the report scope matches the review purpose.
5. **Run the report.** Refresh or generate the report. → *Expect:* revenue, cost of goods, expenses, and net income display for the period.
6. **Scan for obvious errors.** Look for uncategorized transactions, negative income, unusual balances, or missing payroll and tax entries. → *Expect:* issues are either corrected or noted.
7. **Export or save the report.** Save as PDF, spreadsheet, or system report snapshot for sharing. → *Expect:* the report file or saved view is available.

## Decision points

- Report is for taxes or lending → ask your accountant which basis and adjustments are required.
- Numbers look wrong → review transaction detail before sharing externally.
- Multiple locations or projects exist → run both consolidated and filtered views.
- Inventory or payroll is incomplete → label the report draft until those entries are posted.

## Failure modes & recovery

- **F1 Wrong date range:** detect by report header not matching the requested period → recover by resetting dates and rerunning.
- **F2 Wrong basis:** detect by cash or accrual label not matching the request → recover by changing basis and regenerating.
- **F3 Uncategorized transactions:** detect by Uncategorized, Suspense, or Ask My Accountant lines → recover by categorizing transactions before final export.
- **F4 Missing activity:** detect by known invoices, bills, or payroll absent from detail → recover by entering or syncing missing records.

## Verification

The saved P&L report shows the intended date range, accounting basis, filters, revenue, expenses, and net income, with obvious uncategorized or missing items resolved or documented.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks uses Profit and Loss; Xero uses Profit and Loss under Accounting reports; generic tools may call it Income Statement.
- `us`: tax preparers may request accrual or cash basis depending on filing method and entity type.

## Safety & privacy

Medium risk because the report exposes business performance and can affect tax, lending, or investor decisions. Share exports only with authorized recipients.
