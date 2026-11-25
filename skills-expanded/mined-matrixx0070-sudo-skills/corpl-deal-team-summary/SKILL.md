---
name: corpl-deal-team-summary
version: 1.0.0
description: Produce a concise deal-team status summary — where the transaction stands, open issues, decisions needed, and next steps — for internal circulation.
author: matrixx0070
tags: [corporate-legal, m&a, status, deal-team, summary, communication]
capabilities: []
---

## When to use

Use this to brief the internal deal team (partners, associates, client contacts) on where a transaction stands: recent progress, open diligence issues, decisions the team must make, and the near-term critical path. It is the recurring pulse that keeps a deal coordinated.

**Not for:** external communication to a counterparty or client without attorney review (this is an internal working summary); the definitive diligence-issue analysis (use corpl-diligence-issue-extraction); the operational closing tracker (use corpl-closing-checklist). This summary distills status — it does not render legal conclusions, which stay with counsel.

## Method

1. **Header the deal state.** Deal name, structure, stage (diligence / negotiation / pre-closing), signing and target-closing dates.
2. **Summarize progress since the last update** in a few lines — what advanced, what closed out.
3. **List open issues by priority.** For each: the issue, its status, the owner, and whether it threatens the timeline. *Decision point:* flag any deal-jeopardizing issue (financing, material consent, regulatory, undisclosed liability) at the top and route it to the deal lead.
4. **State decisions needed** from the team or client, each with a recommended option and a needed-by date — but frame legal calls as "for counsel's decision," not as your conclusion.
5. **Give the critical path** — the 3-5 items that gate closing right now.
6. **Note the next milestones and dates.**
7. **Keep it to one page**; escalate anything material rather than burying it.

## Example

Project Harbor (stock purchase, diligence stage, signing target 6/30). Progress: financial diligence complete; 32 of 41 material contracts reviewed. Open issues: (1) change-of-control consent on top customer contract — at risk, owner: buyer counsel, threatens timeline; (2) pending IP litigation — under review. Decisions needed: escrow amount (for client, needed by 6/20). Critical path: customer consent, IP review, escrow terms. Next: draft SPA circulates 6/22.

## Pitfalls

- **Burying the deal-killer.** The one issue that can sink the deal belongs at the top, not paragraph six.
- **Stating legal conclusions.** "This consent isn't required" is counsel's call — present it as an open item for counsel.
- **Status theater.** "In progress" on everything tells the team nothing; give owners and needed-by dates.
- **Letting it sprawl.** A summary no one finishes reading fails its purpose.

## Output format

```
DEAL SUMMARY — <deal> (<structure>, <stage>) | Signing: <date> | Close: <date>
Progress since last update:
Open issues (priority order):
  | Issue | Status | Owner | Timeline risk |
Decisions needed: <decision> — recommended: <option> — by: <date> — (for counsel? Y/N)
Critical path (now):
Next milestones:
Internal — not for external distribution without attorney review
```

## Reference

An effective deal summary leads with risk, assigns every open item an owner and date, and separates operational status from legal judgment (which stays with counsel). Mark internal summaries "Privileged & Confidential" where they reflect legal analysis, and never forward one externally without attorney review. This summary pulls from the diligence issue list and closing checklist rather than duplicating them.
