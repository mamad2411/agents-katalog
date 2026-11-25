---
name: corpl-integration-management
version: 1.0.0
description: Organize post-closing legal integration — entity consolidation, contract assignment, governance alignment, and the covenants that survive the deal.
author: matrixx0070
tags: [corporate-legal, m&a, integration, post-closing, entity, governance]
capabilities: []
---

## When to use

Use this after a transaction closes to drive the legal side of integration: consolidating or restructuring entities, assigning or novating contracts, aligning governance and policies, satisfying post-closing covenants, and completing the filings the deal left open. It converts a closed deal into a properly integrated legal structure.

**Not for:** pre-closing execution (use corpl-closing-checklist); business/operational integration (out of scope — this is the legal workstream); interpreting whether a survival obligation has been met — that legal determination is counsel's. This organizes and tracks the legal integration plan; it does not waive covenants or opine on compliance.

## Method

1. **Extract surviving obligations from the agreement.** Post-closing covenants, earn-outs, indemnity/escrow terms, non-competes, transition-services commitments, and their deadlines.
2. **Map the target entity structure** and the desired end state — which entities merge, dissolve, or continue, and the resulting org chart.
3. **Inventory contracts to assign, novate, or terminate**, noting which required (or still require) counterparty consent.
4. **Plan governance alignment.** New board/officer appointments, adopted bylaws/policies, bank-signatory changes, and authorization consents needed.
5. **List required filings.** Entity amendments, mergers, name changes, and qualifications in new states. *Decision point:* any integration step with regulatory or third-party-consent dependency is confirmed with counsel before execution.
6. **Assign owners, dependencies, and dates** across the workstreams; integration steps often have ordering constraints.
7. **Track covenant satisfaction and escrow/earn-out milestones** to closure, escalating disputes to counsel.

## Example

Post-close of an asset acquisition. Surviving obligations: 18-month non-compete, TSA for 6 months, $2M indemnity escrow releasing at 12 months. Entity plan: acquired assets moved into a new subsidiary, target LLC to be dissolved after wind-down. Contracts: 22 assigned (14 needed consent — 12 obtained, 2 pending, escalated). Governance: new officers appointed by written consent, bank signatories updated. Filings: subsidiary formation done, foreign qualification in 2 states pending.

## Pitfalls

- **Losing the surviving covenants.** Non-competes and earn-outs bind after closing and need active tracking.
- **Assigning contracts without consent.** An assignment that required consent and got none can be a breach.
- **Skipping governance updates.** Stale signatories and unappointed officers create authority gaps.
- **No ordering.** Dissolving an entity before its contracts are novated strands obligations.

## Output format

```
INTEGRATION PLAN — <deal> (post-closing)
Surviving obligations:
  | Obligation | Deadline | Owner | Status |
Entity restructuring: current → end state:
Contract assignment/novation:
  | Contract | Action | Consent needed? | Status |
Governance alignment: appointments / policies / signatories:
Required filings:
Escrow / earn-out milestones:
Escalations to counsel:
```

## Reference

Legal integration workstreams: surviving covenants (non-compete, indemnity/escrow, earn-out, TSA), entity consolidation, contract assignment/novation with consent tracking, governance alignment (officer/director appointments, policies, bank signatories), and post-closing filings (amendments, mergers, qualifications). Steps carry ordering and consent dependencies. Covenant-satisfaction determinations and dispute handling are counsel's; this workstream organizes and tracks them.
