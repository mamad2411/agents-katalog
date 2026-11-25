---
name: expense-tracker
description: "Creates an expense tracking and categorization system in Notion with transaction records, category breakdowns, monthly summaries, and tax-deduction flagging for freelancers and small businesses. Use when a user needs to track business expenses, wants to replace spreadsheet-based bookkeeping, or needs to organize receipts and transactions for tax time."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-database mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-fetch
metadata:
  author: Salah-XD
  version: "1.0"
---

# Expense Tracker

## When to Use This Skill

Use this skill when you need to:
- Build a business expense tracking database in Notion from scratch
- Replace a spreadsheet, shoebox of receipts, or mental math system for tracking expenses
- Categorize expenses by IRS Schedule C categories for tax preparation
- Flag tax-deductible purchases so nothing gets missed at year-end
- Import existing transactions from a bank statement export, CSV, or manual list

**DO NOT** use this skill for:
- Personal budgeting or household expense tracking (this is for business expenses)
- Invoicing or accounts receivable (use an invoice-template skill instead)
- Payroll processing or tax filing (requires dedicated software and professionals)
- Full double-entry bookkeeping or chart of accounts (use QuickBooks or Wave)

---

## Quick Reference: Expense Tracker Features

| Feature | Details |
|---------|---------|
| Properties | 12 fields per expense record |
| Expense categories | 15 IRS Schedule C aligned categories |
| Payment methods | 6 options (Cash, Credit Card, Debit, Bank Transfer, PayPal, Other) |
| Tax deduction flags | Full, Partial, None, Verify |
| Database views | 5 pre-built filtered views |
| Seeding | Bulk import from CSV, bank statement, or manual list |

## Quick Reference: Database Schema

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| Expense Name | Title | Short description of the purchase | Required |
| Date | Date | Transaction date | Required |
| Amount | Number (USD) | Total amount spent | Required |
| Category | Select | IRS Schedule C classification | See category table |
| Vendor | Rich text | Business or person paid | Empty |
| Payment Method | Select | How the expense was paid | Credit Card |
| Tax Deductible | Select | Deduction qualification | Verify |
| Receipt | URL | Link to receipt image or file | Empty |
| Notes | Rich text | Context, purpose, or client association | Empty |
| Client/Project | Rich text | Related client or project | Empty |
| Recurring | Checkbox | Monthly recurring expense | false |
| Tags | Multi-select | Labels for filtering | See below |

### Payment Methods

Credit Card, Debit, Cash, Bank Transfer, PayPal, Other

### Default Tags

`monthly`, `quarterly`, `annual`, `client-billable`, `reimbursable`, `pending-receipt`, `large-purchase`, `subscription`, `one-time`

---

## Quick Reference: Expense Categories (IRS Schedule C Aligned)

THESE CATEGORIES ARE FOR TRACKING PURPOSES ONLY. CONSULT A TAX PROFESSIONAL FOR DEDUCTION ELIGIBILITY AND COMPLIANCE.

| Category | Typical Deductibility | Examples |
|----------|----------------------|----------|
| Advertising | Full | Google Ads, Facebook Ads, business cards, sponsored posts |
| Car & Truck | Partial (business % only) | Gas, maintenance, tolls, parking for business trips |
| Contractors | Full (1099 over $600) | Freelance designers, virtual assistants, subcontractors |
| Education | Full | Online courses, certifications, workshops, books |
| Insurance | Full | Liability, E&O, health (self-employed), equipment |
| Legal & Professional | Full | CPA fees, legal consultation, business coaching |
| Meals | Partial (50%) | Client lunches, meals during business travel |
| Office Expenses | Full | Printer ink, paper, cleaning supplies, coffee for office |
| Rent & Lease | Full | Coworking space, office lease, equipment rental |
| Software & Subscriptions | Full | Adobe Creative Cloud, Notion, Slack, Zoom, hosting |
| Supplies | Full | Packaging materials, raw materials, inventory supplies |
| Taxes & Licenses | Full | Business license, state registration, professional dues |
| Travel | Full | Flights, hotels, rental cars, rideshare for business |
| Utilities | Partial (business %) | Internet, phone plan, electricity (home office portion) |
| Other | Varies | Bank fees, postage, miscellaneous business costs |

### Tax Deduction Flags

| Flag | Meaning | Action |
|------|---------|--------|
| Full | 100% deductible | No adjustment needed at tax time |
| Partial | Only a percentage is deductible | Record business-use % in Notes |
| None | Not deductible | Do not include on Schedule C |
| Verify | Uncertain | Flag for review with your accountant |

**DEFAULT: Set Tax Deductible to "Verify" when deductibility is not obvious.** Let the user's accountant make the final call.

---

## Core Workflow

EVERY EXPENSE TRACKER STARTS BY GATHERING BUSINESS DETAILS AND CREATING THE DATABASE WITH THE FULL SCHEMA BEFORE ADDING ANY TRANSACTIONS -- NEVER ADD PAGES TO A DATABASE THAT IS MISSING PROPERTIES.

### Step 1: Gather Requirements

1. **Business type** -- sole proprietorship, LLC, S-corp, partnership
2. **Notion parent page** -- where should the expense database live
3. **Fiscal year** -- calendar year (Jan-Dec) or custom fiscal year
4. **Currency** -- USD default; confirm or change
5. **Custom categories** -- any additions to the 15 defaults
6. **Existing expenses** -- transactions to import (CSV, list, or dictated)
7. **Tax situation** -- any known deduction rules or accountant preferences

If the user provides only items 1 and 2, proceed with all defaults.

**Brief template for vague requests:**

```
I'll build your expense tracker in Notion. Quick answers needed:

1. What type of business entity? (sole prop, LLC, S-corp)
2. Which Notion page should I create the tracker under?
3. Fiscal year? (default: January - December)
4. Currency? (default: USD)
5. Any expense categories beyond the 15 defaults?
6. Do you have existing expenses to import?
```

### Step 2: Locate the Parent Page in Notion

1. Call `notion-search` with the page name or keywords the user provided
2. Confirm the page ID with the user if multiple matches exist

**IF THE PAGE IS NOT FOUND:** Ask for exact title or URL, retry with shorter keyword. **After 3 failed searches, stop:** "I cannot find that page. Check Settings > Connections in Notion and verify the integration has access."

### Step 3: Create the Database in Notion

1. Call `notion-create-database` with the parent page ID and full schema:

**Database title:** `Business Expenses`

**Properties to create:**

```
Expense Name       -> title
Date               -> date
Amount             -> number (format: dollar)
Category           -> select
  options: Advertising (blue), Car & Truck (brown), Contractors (purple),
           Education (pink), Insurance (orange), Legal & Professional (yellow),
           Meals (red), Office Expenses (gray), Rent & Lease (green),
           Software & Subscriptions (blue), Supplies (orange),
           Taxes & Licenses (yellow), Travel (pink), Utilities (gray),
           Other (default)
Vendor             -> rich_text
Payment Method     -> select
  options: Credit Card (blue), Debit (green), Cash (yellow),
           Bank Transfer (purple), PayPal (orange), Other (gray)
Tax Deductible     -> select
  options: Full (green), Partial (yellow), None (red), Verify (gray)
Receipt            -> url
Notes              -> rich_text
Client/Project     -> rich_text
Recurring          -> checkbox
Tags               -> multi_select
  options: monthly (blue), quarterly (purple), annual (orange),
           client-billable (green), reimbursable (pink),
           pending-receipt (red), large-purchase (yellow),
           subscription (brown), one-time (gray)
```

2. Verify with `notion-fetch` on the returned database ID
3. Confirm creation with a summary of all configured properties

**IF DATABASE CREATION FAILS:** Verify parent page ID with `notion-fetch`, retry once. **If it fails again:** "Please go to the parent page > three-dot menu > Connections and ensure the integration has 'Can edit' access."

### Step 4: Seed with Existing Expenses

**SKIP THIS STEP if the user has no existing expenses to import.**

1. Parse the user's expense data (CSV, bank statement, bullet list, or natural language)
2. Map each expense to the schema:
   - **Expense Name** -- short, descriptive (e.g., "Adobe Creative Cloud - January")
   - **Date** -- transaction date from the data
   - **Amount** -- dollar amount; **NEVER guess amounts**
   - **Category** -- match to the closest IRS category
   - **Vendor** -- extract business name
   - **Payment Method** -- infer from context, default to "Credit Card"
   - **Tax Deductible** -- set from category rules; default "Verify" when uncertain
   - **Recurring** -- check true for subscriptions and monthly services
   - **Tags** -- infer from context (e.g., subscription = `monthly` + `subscription`)

3. Call `notion-create-pages` to add expenses in batches
4. Report seeding results with category breakdown and totals

**IF EXPENSE DATA IS AMBIGUOUS:** Present interpretation before creating pages. **IF BATCH CREATION PARTIALLY FAILS:** Report successes/failures, retry individually, provide manual entry details if retries fail.

### Step 5: Set Up Views and Deliver

**Notion MCP does not support creating views programmatically.** Provide exact instructions:

```
RECOMMENDED VIEWS (create these in Notion):

1. ALL EXPENSES (Table) — Sort: Date descending. No filter.
2. THIS MONTH (Table) — Filter: Date is "This month". Group by: Category.
3. BY CATEGORY (Table) — Group by: Category. Sort: Amount descending.
4. TAX DEDUCTIONS (Table) — Filter: Tax Deductible is "Full" OR "Partial".
   Group by: Category. Sort: Date ascending.
5. NEEDS ATTENTION (Table) — Filter: Tax Deductible is "Verify" OR Tags
   contains "pending-receipt". Sort: Date ascending.
```

**USAGE GUIDE (deliver to every user):**

```
ADDING AN EXPENSE (same day as purchase):
1. Click "+ New" in "All Expenses"
2. Enter Expense Name, Amount, Date, Category, Vendor, Payment Method
3. Set Tax Deductible: Full (clearly business), Partial (mixed use),
   None (personal), Verify (unsure — flag for accountant)
4. Paste receipt link if available; check "Recurring" for subscriptions

MONTHLY REVIEW (30 min, end of month):
1. Open "This Month" — check totals by category
2. Open "Needs Attention" — resolve "Verify" items, upload missing receipts

TAX TIME PREP (annually):
1. Open "Tax Deductions" — filter by tax year
2. Group by Category to match Schedule C line items
3. Resolve remaining "Verify" items
4. Share database with your accountant via Notion sharing

PARTIAL DEDUCTIONS: Set to "Partial", record business-use % in Notes
(e.g., "Home internet — 40% business use")
```

**IMPORTANT DISCLAIMER (include in every delivery):**

```
DISCLAIMER: This expense tracker is for record-keeping and organization
purposes only. It does not constitute tax advice. Consult a qualified
tax professional for deduction eligibility, compliance, and filing.
```

---

## Example 1: Freelance Web Developer

**User request:** "I'm a freelance web developer, sole prop. Track my expenses in Notion under 'Freelance Finances'. I have some recent expenses to add."

**Execution:**

1. **Requirements:** Sole prop, parent "Freelance Finances", calendar year, USD, 8 expenses
2. **Search:** `notion-search` for "Freelance Finances" -> `pg_fin456`. Confirmed.
3. **Create:** `notion-create-database` with full schema -> `db_exp789`
4. **Seed 8 expenses:**

```
Expenses imported: 8 of 8 successful

  SOFTWARE & SUBSCRIPTIONS:
    Adobe Creative Cloud - January      $54.99   Credit Card   Full
    GitHub Pro - January                $4.00    Credit Card   Full
    Notion Team Plan - January          $10.00   Credit Card   Full
    AWS Hosting - January               $127.43  Credit Card   Full

  CONTRACTORS:
    Logo redesign - Sarah Kim Design    $750.00  PayPal        Full
    Copywriting - Jake Torres           $400.00  Bank Transfer Full

  OFFICE EXPENSES:
    Standing desk riser                 $189.99  Debit         Full
    USB-C hub and cables                $67.50   Credit Card   Full

Total: $1,603.91 | Recurring: $196.42/mo (4 subscriptions) | All fully deductible
```

5. **Delivered:** Views + usage guide + disclaimer. Next steps: create views, add February subscriptions, log expenses same-day, schedule monthly review.

---

## Example 2: E-Commerce Store Owner

**User request:** "I run a small e-commerce shop selling handmade candles. LLC. My Notion page is 'Candle Biz Operations'. I have about 10 recent expenses."

**Execution:**

1. **Requirements:** LLC, parent "Candle Biz Operations", calendar year, USD, 10 expenses
2. **Search:** `notion-search` for "Candle Biz Operations" -> `pg_candle321`. Confirmed.
3. **Create:** `notion-create-database` with full schema -> `db_candle654`
4. **Seed 10 expenses:**

```
Expenses imported: 10 of 10 successful

  SUPPLIES:
    Soy wax bulk order (50 lbs)         $189.00  Credit Card   Full
    Fragrance oils assortment (12 pk)   $84.50   Credit Card   Full
    Wicks and labels bundle             $42.00   Debit         Full
    Glass jars (case of 48)             $156.00  Credit Card   Full

  ADVERTISING:
    Instagram Ads - January             $250.00  Credit Card   Full
    Etsy Promoted Listings - January    $87.30   Debit         Full
    Facebook Ads - January              $150.00  Credit Card   Full

  TRAVEL:
    Craft fair booth rental - Portland  $175.00  Cash          Full
  CAR & TRUCK:
    Gas and tolls for Portland trip     $63.20   Cash          Partial

  SOFTWARE & SUBSCRIPTIONS:
    Shopify Basic Plan - January        $39.00   Credit Card   Full

Total: $1,236.00 | Recurring: $526.30/mo | Full (9), Partial (1)
Tip: Tag inventory with "one-time" and ad spend with "monthly" to separate
cost of goods from operating expenses at tax time.
```

5. **Delivered:** Views + usage guide + disclaimer. Next steps: create views, upload 2 cash receipts, record business-use % for Car & Truck, log expenses same-day.

---

## Pre-Delivery Checklist

Run this before delivering. **DO NOT SKIP ANY ITEM.**

| Check | What to Verify |
|-------|----------------|
| Database exists | `notion-fetch` with database ID succeeds |
| All 12 properties | Every schema property configured |
| Category options | All 15 categories exist as select options |
| Payment methods | All 6 methods exist as select options |
| Tax Deductible options | Full, Partial, None, Verify all present |
| Amount format | Number formatted as dollar |
| Date + Recurring | Date is date type, Recurring is checkbox |
| Tags configured | All 9 default tags exist as multi-select options |
| Expenses seeded | All provided expenses created, no duplicates |
| Amounts accurate | Dollar amounts match user data exactly |
| Disclaimer delivered | Tax disclaimer included in delivery |
| Views + usage guide | All 5 views and operations guide delivered |
| Parent page correct | Database under requested page |

```
Pre-Delivery Checklist:
  [x] Database created and accessible
  [x] All 12 properties configured
  [x] Category options correct (15 IRS-aligned)
  [x] Payment methods present (6)
  [x] Tax Deductible options correct (4)
  [x] Amount formatted as dollar
  [x] Date and Recurring properties configured
  [x] Tags configured (9 defaults or custom)
  [x] All expenses seeded, no duplicates, amounts verified
  [x] Tax disclaimer delivered
  [x] View instructions and usage guide delivered
  [x] Database under correct parent page
```

---

## Recovery and Troubleshooting

### Notion Search Returns No Results

1. Ask for exact page title (case-sensitive)
2. Try shorter keyword (e.g., "Finance" instead of "Business Finance Dashboard")
3. Confirm the page is shared with the Notion integration
4. **After 3 failures:** "Check Settings > Connections in Notion and verify integration access."

### Database Creation Fails

1. Verify parent page ID with `notion-fetch`
2. Check for permission errors
3. Retry once
4. **If still fails:** "Go to parent page > three-dot menu > Connections > ensure 'Can edit' access."

### Expense Seeding Partially Fails

1. Report which expenses succeeded and which failed
2. Retry failed expenses individually
3. If retries fail, provide details for manual entry

### Notion API Rate Limits

1. Pause 10 seconds between batches, reduce to 5 per call
2. **DO NOT skip expenses due to rate limits** -- slow down and retry

### User Is Unsure About Categories

1. Present the category table
2. Map to most likely category
3. If ambiguous, default to "Other" with Tax Deductible = "Verify"
4. Add Note: "Category uncertain -- review with accountant"

### User Wants to Modify Schema Later

**Notion MCP does not support modifying schemas.** Instruct the user: click "+" to add property, click column header > "Edit property" to modify, or add new category options via "Edit property" on the Category column.

### Large CSV Import

1. Parse headers and present mapping for confirmation
2. Process in batches of 10-15 per `notion-create-pages` call
3. Report progress after each batch
4. **50+ rows:** Warn that import takes several minutes due to API limits

---

## Anti-Patterns

- **DO NOT** provide specific tax advice -- this is a tracking system, not a tax advisory service
- **DO NOT** assume deductibility without flagging -- when in doubt, set to "Verify"
- **DO NOT** mix personal and business expenses -- advise separate tracking
- **DO NOT** guess or fabricate dollar amounts -- only record what the user provides
- **DO NOT** create the database without the full property schema
- **DO NOT** skip the tax disclaimer -- every delivery must include it
- **DO NOT** categorize car expenses as 100% deductible -- almost always partial
- **DO NOT** promise IRS compliance -- this organizes records, not guarantees audits
- **DO NOT** create views programmatically -- provide manual instructions
- **DO NOT** deliver without the usage guide -- the tracker requires daily operation knowledge