---
name: invoice-receipt-processor
description: Extract structured data from invoices and receipts (vendor, amount, date, category, line items), flag policy violations, and produce submission-ready expense reports. Use when the user has a batch of receipts or invoices to process, wants to automate expense reporting, or needs to extract clean data from unstructured financial documents. Covers both single-document extraction (#12) and smart expense report building (#18) from the @ai_slacker automation series. Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today."
---

# Invoice & Receipt Processor

Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today" (Intermediate #12 + Advanced #18).

> Extracts vendor, amount, and date from receipts into structured data, then flags policy violations and produces a submission-ready expense report.

## Two modes

### Mode 1 — Single document extraction

```
Extract the following structured data from this invoice/receipt:

[PASTE INVOICE TEXT OR DESCRIBE IMAGE CONTENTS]

Extract:
- Vendor name
- Invoice/receipt date
- Total amount (currency)
- Line items (description | quantity | unit price | total)
- Tax amount (if shown)
- Payment method (if shown)
- Invoice/receipt number (if shown)
- Billing address (if shown)

Output as a clean JSON object. If any field is missing from the document, set it to null — do not infer or guess.
```

---

### Mode 2 — Smart expense report with policy check

```
You are an expense report processor. Process the following receipts and produce a submission-ready expense report.

EXPENSE POLICY:
[PASTE YOUR COMPANY EXPENSE POLICY HERE — or use the defaults below]

Default policy if none provided:
- Meals: max $75/person, alcohol not reimbursable
- Travel: economy class only, hotel max $250/night
- Software/tools: must have prior approval over $100
- Entertainment: requires business purpose and attendee names
- All receipts over $25 require itemized receipt (not just credit card slip)

RECEIPTS TO PROCESS:
[PASTE RECEIPT DATA OR DESCRIPTIONS HERE — one per block]

For each receipt:
1. Extract: vendor, date, amount, category, business purpose (if stated)
2. Check against policy — flag any violation with the specific rule broken
3. Mark status: APPROVED / FLAGGED / MISSING INFO

Final output:
- Summary table: date | vendor | category | amount | status
- Total reimbursable amount
- Total flagged amount
- List of missing information needed before submission
- One-paragraph narrative for the submission covering the business purpose
```

---

## Automation pipeline (n8n)

Full automated flow using `n8n-agent-builder`:
1. **Trigger**: email with receipt attachments, or Google Drive folder watch
2. **Step 1**: extract text from image/PDF (OCR node or Claude vision)
3. **Step 2**: Claude processes with Mode 2 prompt above
4. **Step 3**: push structured data to Airtable/Google Sheets
5. **Step 4**: email flagged items to submitter for correction
6. **Step 5**: auto-submit approved items to accounting system

## Related skills

- **personal-finance-analyzer**: For personal (not business) expense tracking
- **n8n-agent-builder**: Automate the receipt → report pipeline
- **pdf**: Extract text from PDF invoices before processing
