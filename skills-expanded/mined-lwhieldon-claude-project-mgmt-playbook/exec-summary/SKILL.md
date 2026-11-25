---
name: exec-summary
description: Compress a long document (SOW, report, assessment, change request) into a one-page executive summary for a C-suite or board audience. Use when a decision-maker will not read the full document. Usage - /exec-summary path/to/document.md -- audience notes
---

# Executive Summary

Compress a long document into a tight one-page executive summary. Written for a C-suite or board
audience who will not read the full document.

## Input

`$ARGUMENTS` is the path to the document, optionally followed by audience context after `--`:

```
/exec-summary sample-projects/globex-erp-migration/sow.md -- audience is the CFO, focus on cost and timeline
```

Read the whole document before summarizing. If no path was given, ask for one.

## Output

**Executive Summary: [Document Title]**
*Prepared for: [Audience if specified | Senior Leadership]*
*Date: [Today's date]*

---

**Situation** (2 to 3 sentences):
What is this document about? What decision or context does it address?

**Key Findings / What's in This Document:**
- 3 to 5 bullets covering the most important points
- Lead with the "so what": not just what it says, but why it matters

**Risks or Open Issues:**
- Top 2 to 3 risks, gaps, or items requiring attention or decision

**Recommendations / Proposed Next Steps:**
| Recommendation | Owner | Target Date |
|---|---|---|

**Bottom Line:**
One sentence. If the reader remembers one thing from this document, it should be this.

*Drafted with Claude Code on YYYY-MM-DD; reviewed by [NAME]*

---

Use concise, executive-level prose. No jargon without explanation. Bullets 12 words or fewer. The
total summary should fit on one printed page (roughly 350 to 450 words). Every figure in the
summary must appear in the source document; do not round, extrapolate, or combine numbers.

## Example Output

**Executive Summary: Acme Corp Data Warehouse SOW**
*Prepared for: CFO and Project Sponsor*
*Date: May 8, 2025*

**Situation:**
This Statement of Work defines the scope, timeline, and pricing for a 6-month data warehouse modernization project. It replaces Acme's on-premise SQL Server environment with a cloud-based Snowflake platform to support faster reporting and analytics.

**Key Findings:**
- Total contract value: $485,000 fixed-price
- Go-live target: December 12, 2025 (assumes client data access by June 1)
- Three workstreams: data migration, reporting layer, and user training

**Risks or Open Issues:**
- Acceptance criteria are not defined; "fully functional" language creates ambiguity
- Change control process is absent; any scope additions will require a CR process to be established

**Bottom Line:**
The SOW is directionally sound but needs two additions before signing: defined acceptance criteria and a change control clause.
