---
name: corpl-diligence-issue-extraction
version: 1.0.0
description: Read diligence documents and extract material issues — risks, liabilities, and red flags — into a prioritized, sourced issues list for counsel.
author: matrixx0070
tags: [corporate-legal, m&a, diligence, issues, risk, red-flags]
capabilities: []
---

## When to use

Use this during M&A or investment diligence to convert a pile of data-room documents into a structured issues list: what was found, why it matters, how severe it is, and where it lives. It turns raw document review into the risk picture the deal team and counsel act on.

**Not for:** organizing the review itself (use corpl-tabular-review); building the disclosure/contract schedule (use corpl-material-contract-schedule); rendering the final legal risk opinion — severity flags are triage, and the legal conclusion belongs to counsel. Every extracted issue is a flag for attorney assessment, not a determination.

## Method

1. **Scope the review.** Which documents, which diligence categories (corporate, contracts, IP, litigation, employment, tax, regulatory, financial), against what materiality threshold.
2. **Read for issue types**, not just contents: missing consents, change-of-control triggers, undisclosed liabilities, unusual or off-market terms, expired or auto-renewing agreements, encumbrances, litigation, compliance gaps.
3. **Capture each issue with its source.** Document name, section/page, and a one-line description of the fact.
4. **Assess severity** — high / medium / low — based on likelihood and magnitude of impact on the deal. *Decision point:* any high-severity or deal-jeopardizing finding (material undisclosed liability, missing key consent, regulatory violation) is flagged for immediate counsel review, not batched.
5. **Note the implication and a proposed action** (needs consent, price adjustment, rep/warranty, escrow, walk-away) — framed as options for counsel.
6. **Cross-reference related issues** so the same root problem is not double-counted.
7. **Route the list to counsel** before it informs any negotiating position.

## Example

IP diligence, 12 documents, threshold "any exclusive license or IP assignment gap." Issues: (1) HIGH — key patent assigned by a former contractor with no IP-assignment agreement on file (source: employment folder 3.1); implication: ownership defect, propose R&W + escrow. (2) MEDIUM — software license auto-renews with 90-day notice, missed window approaching (source: contracts 5.4). (3) LOW — trademark registration lapsed in one minor jurisdiction. High item escalated same day.

## Pitfalls

- **Extracting without sources.** An issue counsel can't trace to a document is unusable.
- **Uniform severity.** If everything is "high," nothing is; calibrate to deal impact.
- **Stating legal conclusions.** "This breaches the license" is counsel's call — record the fact and flag it.
- **Batching a deal-killer.** High-severity findings escalate immediately, not at the end of the review.

## Output format

```
DILIGENCE ISSUES — <deal> | Scope: <categories> | Threshold: <...>
  | # | Issue | Category | Source (doc/§) | Severity | Implication | Proposed action |
High-severity — escalated to counsel:
Related/duplicate issues (grouped):
Coverage: <docs reviewed / total>
For attorney assessment — severity flags are triage, not legal conclusions
```

## Reference

Standard diligence categories: corporate/organizational, material contracts, intellectual property, litigation, employment/benefits, tax, regulatory/compliance, real property, environmental, and financial. Common red flags: missing consents, change-of-control triggers, undisclosed or contingent liabilities, off-market terms, encumbrances, and compliance gaps. Severity is triage for prioritization; the legal risk assessment and its deal consequences are determined by counsel. Feed high-severity items to the deal summary and the schedule workflows.
