---
name: vdr-management
description: >
  Virtual Data Room classification and organization. Scans unstructured file
  uploads, identifies document types (cap tables, IP licenses, vendor contracts,
  tax filings, payroll), applies standardized M&A naming conventions and folder
  hierarchies. Transforms chaotic seller document dumps into diligence-ready
  repositories on day one.
  Use when user asks to "set up a data room", "organize VDR", "data room management", or mentions virtual data room, document indexing, or VDR permissions.
---

# VDR Management

Respect VDR permissions, clean-team rules, privilege, personal data, export restrictions, and retention policy. Do not upload, rename, move, delete, share, OCR through an external service, or change access without explicit authorization.

The genesis of any M&A transaction involves the population of a Virtual Data Room. Sellers or their investment bankers dump thousands of poorly labeled files into a centralized repository — scanned PDFs of decades-old leases, raw Excel trial balances, unformatted payroll ledgers. The administrative burden of organizing these files represents a massive loss of analytical bandwidth.

## The /vdr-classify Protocol

### How It Works

1. **Ingest** each file's text using NLP and OCR
2. **Recognize** the legal or financial taxonomy of each document
3. **Map** to standard M&A index structures:
   - Legal (corporate governance, contracts, IP, litigation)
   - Financial (audited statements, tax returns, trial balances, bank statements)
   - HR (employee census, benefit plans, org charts)
   - Operational (customer lists, vendor agreements, real estate)
   - Regulatory (permits, licenses, compliance records)
4. **Apply** standardized naming conventions
5. **Generate** a complete VDR index with document counts per category

### Standard M&A Folder Hierarchy

```
VDR/
├── 01 - Corporate & Governance
├── 02 - Financial Statements & Tax
├── 03 - Material Contracts
├── 04 - Intellectual Property
├── 05 - Real Estate & Assets
├── 06 - HR & Employee Benefits
├── 07 - Insurance
├── 08 - Regulatory & Compliance
├── 09 - Environmental
├── 10 - Litigation & Claims
├── 11 - Technology & IT
├── 12 - Customers & Revenue
└── 13 - Miscellaneous
```

### Output Format

```
## VDR Classification Report

**Total Files Processed**: [N]
**Auto-Classified**: [N] ([%])
**Requires Manual Review**: [N]

### Classification Summary
| Category | Files | Key Documents Identified |
|----------|-------|-------------------------|
| Corporate & Governance | [N] | Articles of incorporation, bylaws, board minutes... |
| Financial & Tax | [N] | 3-year audited financials, tax returns... |
| Material Contracts | [N] | Customer MSAs, vendor agreements... |
| ... | ... | ... |

### Flagged Items
- [Files that couldn't be classified]
- [Duplicate documents detected]
- [Missing expected documents (e.g., no audited financials found)]
```

## Operating Guidelines

- Prioritize accuracy over speed — misclassified documents create downstream diligence errors
- Flag documents that appear to be duplicates or multiple versions
- Identify missing categories — if no tax returns are found, flag immediately
- Apply consistent date formatting in file names (YYYY-MM-DD)
- Preserve original file names in a mapping table for audit trail
- Never delete or modify original files — classification is additive

## Time Savings

Generate a proposed index, duplicate and missing-item report, and rename or move plan. Do not rename, move, upload, delete, or change VDR permissions without explicit authorization and an auditable rollback plan.
