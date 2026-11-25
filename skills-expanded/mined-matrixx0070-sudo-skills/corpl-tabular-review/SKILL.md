---
name: corpl-tabular-review
version: 1.0.0
description: Review a set of similar documents in a consistent tabular format — one row per document, one column per attribute — for fast, comparable diligence.
author: matrixx0070
tags: [corporate-legal, diligence, review, tabular, contracts, comparison]
capabilities: []
---

## When to use

Use this when you must review many documents of the same type — a stack of contracts, leases, employment agreements, or corporate resolutions — and need them comparable side by side. A consistent table turns a document pile into a scannable matrix where outliers and gaps jump out.

**Not for:** deep single-document analysis of a bespoke agreement; open-ended issue-spotting (use corpl-diligence-issue-extraction on the outputs); building the disclosure schedule (use corpl-material-contract-schedule). Tabular review structures and compares facts; the legal significance of what the table surfaces is assessed by counsel.

## Method

1. **Define the document set and the columns.** Choose the attributes that matter for this review type (parties, term, key clauses, dollar values, flags) before reading — a stable schema is what makes rows comparable.
2. **Read each document into a row**, filling every column. *Decision point:* if an attribute is absent or ambiguous, record "not present" or "unclear" — never leave a cell blank or guess, since blanks and guesses both hide risk.
3. **Cite the source location** (section/page) for load-bearing cells so any value can be traced.
4. **Normalize values** so columns are truly comparable (consistent date format, currency, yes/no for clause presence).
5. **Add a flags column** for anything off-market, missing, or notable, so the table doubles as a triage layer.
6. **Scan for outliers and gaps** across rows — the whole point is that inconsistency becomes visible.
7. **Hand the completed table to the relevant workflow** (issue extraction, schedule) and to counsel for significance calls.

## Example

Review of 25 customer contracts. Columns: counterparty, effective date, term, auto-renew, value/yr, assignment clause, change-of-control, termination-for-convenience, governing law, flags. Filled 25 rows with §-level citations; normalized all values to a common format. Scan surfaced 4 contracts missing any assignment clause and 2 with unusually long 5-year auto-renew terms — flagged. Table routed to issue extraction.

## Pitfalls

- **Unstable columns.** Changing the schema mid-review makes rows non-comparable; lock it first.
- **Blank cells.** A blank is ambiguous — is it absent, or unreviewed? Use explicit "not present"/"unclear."
- **Uncited load-bearing values.** A key value with no source location can't be verified later.
- **Reading significance into the table.** The table shows what is; whether a missing clause is a legal problem is counsel's call.

## Output format

```
TABULAR REVIEW — <document type> | Set: <n documents>
Column schema (locked): <attr1 | attr2 | ... | flags>
  | # | Doc | <attr1> | <attr2> | ... | Source (§/pg) | Flags |
Outliers & gaps: <observation>
Coverage: <reviewed / total>
Fact matrix — significance to be assessed by counsel
```

## Reference

Tabular review is the workhorse of high-volume diligence: one row per document, one column per attribute, a locked schema, explicit "not present"/"unclear" values, and source citations on load-bearing cells. Normalization makes columns comparable so outliers surface on a scan. The table is a fact matrix feeding corpl-diligence-issue-extraction and corpl-material-contract-schedule; legal significance and materiality determinations are made by counsel.
