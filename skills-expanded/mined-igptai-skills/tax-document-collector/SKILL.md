---
name: tax-document-collector
description: Finds all tax-related documents referenced or attached in email — including VAT invoices, tax receipts, 1099s, and official tax correspondence. Use when a user is preparing for tax filing and needs to collect supporting documents from email. Triggers on "tax documents", "find my tax receipts", "VAT invoices", "1099s from email", "tax filing documents", "collect documents for taxes".
metadata:
  version: 1.0.0
---

# Tax Document Collector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email history for tax-related documents — VAT invoices, official receipts,
1099 or equivalent forms, tax authority correspondence, and any document
explicitly marked as needed for tax purposes — and returns a structured list
the user can use as a tax document checklist.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give. Both are required.

   - [tax_year] — the tax year or period to cover (e.g. "2024",
     "fiscal year 2024-2025", "the 2023 tax year"). No default — must
     come from the user. Keep the user's natural phrasing for use in
     the ask input; convert to ISO start and end dates for the search
     call.
   - [tax_jurisdiction] — the user's country or tax jurisdiction (e.g.
     "United States", "Israel", "United Kingdom") — used to know which
     document types are relevant. No default — must come from the user.

2. Call search with:
   - query: tax VAT invoice receipt 1099 tax return deductible official
   - date_from: ISO start date of [tax_year]
   - date_to: ISO end date of [tax_year]

3. Call ask with:
   - input: Find all tax-related documents in email for [tax_year] relevant to [tax_jurisdiction]. This includes VAT invoices, official receipts, 1099 or equivalent tax forms, tax authority correspondence, and any document marked as a tax receipt or needed for tax filing. For each document record the sender, document type, date, amount if present, and whether an attachment was mentioned.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Tax document collection report for a specific tax year or period",
       "additionalProperties": false,
       "properties": {
         "tax_period_from": {
           "type": "string",
           "description": "ISO8601 start date of the tax period"
         },
         "tax_period_to": {
           "type": "string",
           "description": "ISO8601 end date of the tax period"
         },
         "jurisdiction": {
           "type": "string",
           "description": "Tax jurisdiction or country this collection covers"
         },
         "documents": {
           "type": "array",
           "description": "List of every tax-relevant document found in email",
           "items": {
             "type": "object",
             "description": "A single tax document found in email",
             "additionalProperties": false,
             "properties": {
               "sender": {
                 "type": "string",
                 "description": "Company or authority that sent this document"
               },
               "document_type": {
                 "type": "string",
                 "description": "Type of tax document",
                 "enum": [
                   "vat_invoice", "official_receipt", "1099_equivalent",
                   "tax_authority_correspondence", "deductible_expense_receipt",
                   "bank_statement", "payroll_document", "other"
                 ]
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date of the document"
               },
               "amount": {
                 "type": "number",
                 "description": "Amount on the document if present, 0 if not applicable"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the amount, empty string if not applicable"
               },
               "has_attachment": {
                 "type": "boolean",
                 "description": "Whether the email mentioned or included an attachment for this document"
               },
               "notes": {
                 "type": "string",
                 "description": "Any additional context about this document relevant to tax filing"
               }
             },
             "required": [
               "sender", "document_type", "date", "amount",
               "currency", "has_attachment", "notes"
             ]
           }
         },
         "total_deductible_amount": {
           "type": "number",
           "description": "Sum of amounts on documents that appear to be deductible expenses"
         },
         "missing_document_flags": {
           "type": "array",
           "description": "List of document types that are typically required but were not found",
           "items": {
             "type": "string",
             "description": "A missing document type or category the user should locate"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of documents found, total deductible amount, and any gaps"
         }
       },
       "required": [
         "tax_period_from", "tax_period_to", "jurisdiction", "documents",
         "total_deductible_amount", "missing_document_flags", "summary"
       ]
     }
   }

4. Present with summary first, then documents grouped by type. Highlight
   missing document flags prominently so the user knows what to look for.

5. Ask: "Would you like me to organize these into a checklist you can share
   with your accountant?"
