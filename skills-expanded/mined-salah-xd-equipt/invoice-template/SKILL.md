---
name: invoice-template
description: "Generates professional invoice documents with line items, tax calculations, payment terms, and late payment policies, plus a reusable template for future invoices. Use when a user needs to create an invoice, set up a billing system, or standardize their invoicing process as a freelancer or small business owner."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Invoice Template

## When to Use This Skill

Use this skill when you need to:
- Generate a professional invoice for a completed project, milestone, or retainer period
- Set up a reusable invoice template with your business details baked in
- Calculate line items, taxes, discounts, and totals for a client billing document
- Standardize your invoicing process so every invoice looks consistent
- Create a billing system from scratch as a freelancer, consultant, or small business owner

**DO NOT** use this skill for:
- Accounting or bookkeeping (this generates documents, not payment tracking)
- Recurring subscription billing automation (static documents, not payment processing)
- Expense reports or purchase orders (different document format)
- Tax filing or tax advisory (consult an accountant for tax compliance)

---

## Quick Reference: Invoice Capabilities

| Feature | Details |
|---------|---------|
| Invoice fields | 13 standard fields per invoice |
| Payment terms | 4 presets (Net 15, Net 30, Due on Receipt, 50/50 Split) |
| Tax handling | Percentage-based, multi-rate, or tax-exempt |
| Line item types | Hourly, fixed, quantity-based, and milestone |
| Output format | Markdown document saved as `.md` file |
| Reusable template | Variable-based template with `{{PLACEHOLDER}}` syntax |
| Late fee policies | 3 presets (percentage, flat, tiered) |

## Quick Reference: Invoice Fields

| Field | Required | Example |
|-------|----------|---------|
| Invoice Number | Yes | INV-2025-001 |
| Invoice Date | Yes | January 15, 2025 |
| Due Date | Yes | February 14, 2025 |
| From (Your Business) | Yes | Acme Design LLC, 123 Main St, Chicago IL 60601 |
| Bill To (Client) | Yes | Sarah Chen, Bright Solutions Inc. |
| Line Items | Yes | Web design - Homepage, 1, $2,500.00 |
| Subtotal | Auto | $5,000.00 |
| Discount | No | 10% ($500.00) |
| Tax Rate | No | 8.25% |
| Tax Amount | Auto | $371.25 |
| Total | Auto | $4,871.25 (subtotal - discount + tax) |
| Payment Terms | Yes | Net 30 |
| Late Fee Policy | Yes | 1.5% per month on unpaid balance |
| Payment Methods | Yes | Bank transfer, PayPal, check |
| Notes | No | Thank you for your business! |

## Quick Reference: Payment Terms

| Term | Meaning | Best For |
|------|---------|----------|
| Due on Receipt | Payment due immediately | Small jobs under $500, one-time services |
| Net 15 | Due 15 days from invoice date | Ongoing freelance work, trusted clients |
| Net 30 | Due 30 days from invoice date | Standard B2B, retainers |
| 50/50 Split | 50% upfront, 50% on completion | Large projects over $2,500, new clients |

**DEFAULT: Net 30** -- most common standard for freelancers and small businesses.

## Quick Reference: Tax Rates

| Scenario | Rate | Notes |
|----------|------|-------|
| Tax-exempt | 0% | Below revenue threshold, exempt services, or digital B2B |
| US state sales tax | 4% - 10.25% | Physical goods, some services depending on state |
| US general estimate | 7.5% | Placeholder when user is unsure; advise accountant confirmation |
| Canadian GST | 5% | Goods and services in Canada |
| Canadian HST (Ontario) | 13% | Goods and services in Ontario |
| UK VAT | 20% | Goods and services in the UK |
| EU VAT | 19% - 27% | Goods and services in the EU |
| Australian GST | 10% | Goods and services in Australia |

**TAX RATES ARE FOR REFERENCE ONLY.** Always advise the user to confirm with a qualified accountant.

## Quick Reference: Late Fee Policies

| Policy | Structure | Example Language |
|--------|-----------|-----------------|
| Percentage | Fixed % monthly on unpaid balance | "1.5% per month on any unpaid balance after the due date." |
| Flat fee | Fixed amount after grace period | "$25.00 late fee if not received within 7 days of due date." |
| Tiered | Escalating penalties | "1-15 days late: $25. 16-30 days: $50. Over 30 days: 1.5% monthly." |

**DEFAULT: 1.5% per month** -- professional, enforceable, industry standard.

---

## Core Workflow

EVERY INVOICE STARTS BY GATHERING THE USER'S BUSINESS DETAILS BEFORE ANY LINE ITEMS -- NEVER GENERATE AN INVOICE WITHOUT KNOWING WHO IT IS FROM.

### Step 1: Gather Business Details

Collect once -- the reusable template stores these for future invoices.

1. **Business name** -- legal name or DBA
2. **Business address** -- street, city, state/province, postal code, country
3. **Contact email** -- for invoice correspondence
4. **Contact phone** -- optional
5. **Payment methods** -- bank transfer, PayPal, Venmo, Stripe, check, Zelle
6. **Payment details** -- bank name and last 4 digits, PayPal email, Venmo handle
7. **Default payment terms** -- default: Net 30
8. **Default late fee policy** -- default: 1.5% per month
9. **Invoice numbering format** -- default: INV-YYYY-NNN
10. **Tax status** -- rate or exempt; default: tax-exempt unless specified

If the user provides items 1-2 and 5-6, proceed with defaults for the rest.

**Brief template for vague requests:**

```
I'll create your invoice. Quick details needed:

1. Your business name?
2. Your business address?
3. Contact email for the invoice?
4. How can clients pay you? (bank transfer, PayPal, Venmo, check, etc.)
5. Account details for payment (PayPal email, bank name, Venmo handle)?
6. Preferred payment terms? (default: Net 30)
7. Do you charge tax? If so, what rate?
```

**IF THE USER HAS AN EXISTING TEMPLATE:** Read it with `Read`, extract business details, confirm they are current.

### Step 2: Gather Invoice Details

1. **Client name** -- person or company being billed
2. **Client company** -- if different from contact name
3. **Client address** -- mailing address
4. **Client email** -- where to send the invoice
5. **Line items** -- description, quantity/hours, unit rate for each
6. **Discount** -- percentage or flat amount; default: none
7. **Tax rate** -- business default or override
8. **Payment terms** -- business default or override
9. **Invoice number** -- next in sequence or user-specified
10. **Notes** -- project reference, thank-you, scope notes

If the user provides items 1 and 5, proceed with defaults for the rest.

### Step 3: Generate the Invoice

1. **Calculate all amounts:**
   - Line item total = quantity x rate
   - Subtotal = sum of all line item totals
   - Discount = percentage or flat amount off subtotal
   - Taxable amount = subtotal - discount
   - Tax = taxable amount x tax rate
   - Total = taxable amount + tax

2. **VERIFY MATH BEFORE WRITING THE FILE:**
   - Recalculate each value independently
   - **ALL AMOUNTS MUST MATCH TO THE CENT -- FIX ANY DISCREPANCY BEFORE PROCEEDING**

3. **Generate the markdown invoice** with this structure: header (invoice #, dates), From section (business details), Bill To section (client details), Services table (line items with #, description, qty, rate, amount), Summary table (subtotal, discount, tax, total), Payment Terms (due date, late fee policy), Payment Methods (each method with details), Notes

4. **Save as `{invoice-number}.md`** in the user's working directory or specified location

5. **Present to the user** for review before finalizing

### Step 4: Create the Reusable Template

After the first invoice, create a template with `{{PLACEHOLDER}}` variables for invoice-specific values while keeping business details hardcoded.

**Template variables:**
`{{INVOICE_NUMBER}}`, `{{INVOICE_DATE}}`, `{{DUE_DATE}}`, `{{CLIENT_NAME}}`, `{{CLIENT_COMPANY}}`, `{{CLIENT_ADDRESS}}`, `{{CLIENT_EMAIL}}`, `{{LINE_ITEMS}}`, `{{SUBTOTAL}}`, `{{DISCOUNT_PERCENT}}`, `{{DISCOUNT_AMOUNT}}`, `{{TAXABLE_AMOUNT}}`, `{{TAX_RATE}}`, `{{TAX_AMOUNT}}`, `{{TOTAL_DUE}}`, `{{NOTES}}`

Save as `invoice-template.md` in the same directory. Present usage instructions to the user.

---

## Example 1: Freelance Web Design Invoice ($5,000 project, 3 line items)

**User request:** "Invoice for a web design project. Business: Pixel Forge Studio, 890 Elm Street, Austin TX 78701, billing@pixelforge.io. Client: Marcus Rivera, Rivera Consulting, 220 Pine Road, Denver CO 80202. Three items: homepage redesign $2,500, blog template $1,500, SEO audit $1,000. 8.25% tax. PayPal (billing@pixelforge.io) and bank transfer (Chase, ending 7832). Net 30. Invoice INV-2025-001."

**Math verification:**
- Line 1: 1 x $2,500.00 = $2,500.00
- Line 2: 1 x $1,500.00 = $1,500.00
- Line 3: 1 x $1,000.00 = $1,000.00
- Subtotal: $5,000.00
- Tax: $5,000.00 x 0.0825 = $412.50
- Total: $5,412.50

**Generated invoice (`INV-2025-001.md`):**

```markdown
# INVOICE

---

**Invoice Number:** INV-2025-001
**Invoice Date:** January 20, 2025
**Due Date:** February 19, 2025

---

## From

**Pixel Forge Studio**
890 Elm Street
Austin, TX 78701
billing@pixelforge.io

## Bill To

**Marcus Rivera**
Rivera Consulting
220 Pine Road
Denver, CO 80202
marcus@riveraconsulting.com

---

## Services

| # | Description | Qty | Rate | Amount |
|---|-------------|-----|------|--------|
| 1 | Homepage redesign | 1 | $2,500.00 | $2,500.00 |
| 2 | Blog template design and development | 1 | $1,500.00 | $1,500.00 |
| 3 | SEO audit and recommendations report | 1 | $1,000.00 | $1,000.00 |

---

## Summary

| | |
|---|---|
| **Subtotal** | $5,000.00 |
| **Tax (8.25%)** | $412.50 |
| **Total Due** | **$5,412.50** |

---

## Payment Terms

**Due Date:** February 19, 2025 (Net 30)

**Late Fee Policy:** A late fee of 1.5% per month will be applied to any unpaid balance after the due date.

## Payment Methods

- **Bank Transfer:** Chase Bank, Account ending in 7832
- **PayPal:** billing@pixelforge.io

---

## Notes

Thank you for choosing Pixel Forge Studio! This invoice covers the complete website redesign project.

---

*Generated by Pixel Forge Studio*
```

**Delivered:** Invoice saved, template created with Pixel Forge details embedded, next invoice number INV-2025-002.

---

## Example 2: Monthly Retainer Invoice ($2,500/month consulting)

**User request:** "Retainer invoice. Business: JP Consulting (Jade Park), 1400 Market St Suite 200, Philadelphia PA 19103, jade@jpconsulting.co. Client: Tanya Okafor, Okafor & Partners, 88 Broad St, New York NY 10004. Monthly retainer $2,500 for strategic consulting, January. No tax (under threshold). Zelle (jade@jpconsulting.co) and check. Net 15. Invoice RET-2025-01."

**Math verification:**
- Line 1: 1 month x $2,500.00 = $2,500.00
- Subtotal: $2,500.00
- Tax: Exempt
- Total: $2,500.00

**Generated invoice (`RET-2025-01.md`):**

```markdown
# INVOICE

---

**Invoice Number:** RET-2025-01
**Invoice Date:** February 1, 2025
**Due Date:** February 16, 2025

---

## From

**JP Consulting**
Jade Park
1400 Market Street, Suite 200
Philadelphia, PA 19103
jade@jpconsulting.co

## Bill To

**Tanya Okafor**
Okafor & Partners
88 Broad Street
New York, NY 10004
tanya@okaforpartners.com

---

## Services

| # | Description | Qty | Rate | Amount |
|---|-------------|-----|------|--------|
| 1 | Strategic consulting retainer -- January 2025 | 1 month | $2,500.00 | $2,500.00 |

---

## Summary

| | |
|---|---|
| **Subtotal** | $2,500.00 |
| **Tax** | Exempt |
| **Total Due** | **$2,500.00** |

---

## Payment Terms

**Due Date:** February 16, 2025 (Net 15)

**Late Fee Policy:** A late fee of 1.5% per month will be applied to any unpaid balance after the due date.

## Payment Methods

- **Zelle:** jade@jpconsulting.co
- **Check:** Make payable to "JP Consulting" and mail to the address above

---

## Notes

Monthly retainer invoice for January 2025 strategic consulting services. Thank you for the continued partnership, Tanya!

---

*Generated by JP Consulting*
```

**Delivered:** Invoice saved, template created with JP Consulting details embedded. For next month: "invoice Tanya for February" generates RET-2025-02 automatically.

---

## Pre-Delivery Checklist

Run this before delivering any invoice. **DO NOT SKIP ANY ITEM.**

| Check | What to Verify |
|-------|----------------|
| Math correct | Every line item = qty x rate; subtotal = sum of lines; tax on post-discount amount; total = subtotal - discount + tax |
| All required fields filled | Invoice #, dates, from, bill to, line items, subtotal, total, terms, late fee, payment methods |
| Invoice number unique | No duplicate in the directory (check with `Glob`) |
| Due date matches terms | Net 15 = +15 days, Net 30 = +30 days from invoice date |
| Payment instructions clear | Client knows exactly how to pay with account details |
| Late fee policy stated | Explicit percentage/amount and when it applies |
| Business details accurate | Name, address, email match user input |
| Client details accurate | Name, company, address, email match user input |
| Line items descriptive | Each item clearly describes the work being billed |
| Currency consistent | All amounts use same format ($X,XXX.XX) |
| File saved | Write tool confirmed successful |
| Template created | Reusable template saved with variables |

```
Pre-Delivery Checklist:
  [x] Math verified -- all calculations correct to the cent
  [x] All required fields filled
  [x] Invoice number unique
  [x] Due date matches payment terms
  [x] Payment instructions clear and complete
  [x] Late fee policy stated
  [x] Business and client details accurate
  [x] Line item descriptions clear
  [x] Currency formatting consistent
  [x] File saved successfully
  [x] Reusable template created
```

---

## Recovery and Troubleshooting

### User Does Not Know Their Tax Rate

1. Ask what state/province/country and whether they sell services or goods
2. Provide the reference range from the tax table as guidance
3. **Default to 0% and add a note:** "Tax not included. Consult your accountant for applicable tax obligations."
4. Offer to update and recalculate once they confirm the rate

### Math Does Not Balance

1. Identify the incorrect calculation
2. Recalculate from raw inputs (qty x rate for each line)
3. Rebuild the summary with corrected values
4. Re-verify before saving
5. **NEVER deliver an invoice with incorrect math**

### User Wants to Modify an Existing Invoice

1. Read the existing file with `Read`
2. Make changes and recalculate all affected amounts
3. Save (overwrite or new version)
4. Run the full pre-delivery checklist
5. **If the invoice number changes, save as a new file -- never reuse an old number**

### Existing Template Found

1. Read the existing `invoice-template.md` with `Read`
2. Extract business details
3. Confirm with the user: "I found your template with [Business Name]. Use these details, or have they changed?"
4. Skip Step 1 if confirmed

### User Provides Incomplete Line Items

1. List what is missing per item:
   ```
   "Website redesign" -- need quantity and rate
   "Logo design, $500" -- flat fee for 1 unit?
   "Consulting, 10 hours" -- need hourly rate
   ```
2. Ask the user to fill gaps before generating
3. **NEVER assume a rate or quantity**
4. **If 3 clarification rounds fail, generate with known items and flag incomplete ones**

### User Wants a Different Format

1. Generate the markdown version first (canonical output)
2. Inform: "To convert to PDF, use a markdown-to-PDF tool or paste into a document editor."
3. Reformat to CSV or plain text if requested
4. **Markdown is always the primary output**

---

## Anti-Patterns

- **DO NOT** generate an invoice without verifying math -- every amount must be independently confirmed
- **DO NOT** assume tax rates -- ask or default to 0% with a disclaimer
- **DO NOT** fabricate payment account details -- only include what the user provides
- **DO NOT** reuse invoice numbers -- every invoice needs a unique identifier
- **DO NOT** skip the late fee policy -- every invoice needs consequences for late payment
- **DO NOT** deliver without presenting the invoice to the user for review first
- **DO NOT** provide tax or legal advice -- this generates documents, not professional counsel
- **DO NOT** include full account numbers -- use last 4 digits for bank accounts
