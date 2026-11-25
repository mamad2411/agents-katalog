---
name: corpl-entity-compliance
version: 1.0.0
description: Track and maintain an entity's corporate housekeeping — good standing, annual reports, registered agent, franchise tax, and minute-book currency.
author: matrixx0070
tags: [corporate-legal, entity, compliance, good-standing, annual-report, records]
capabilities: []
---

## When to use

Use this to keep a legal entity (or a portfolio of entities) in good standing: annual/biennial report filings, franchise tax, registered-agent maintenance, qualification in states where it does business, and an up-to-date minute book. It is the recurring hygiene that keeps an entity clean for financing, M&A, or ordinary operations.

**Not for:** forming a new entity or dissolving one (distinct workflows with their own filings); board action itself (use corpl-board-minutes / corpl-written-consent); resolving a lapsed-status remediation with legal consequences — that goes to counsel. This tracks obligations and status; determinations of legal effect (e.g., of a lapse) belong to counsel.

## Method

1. **Inventory the entity/entities.** Name, type, jurisdiction of formation, and every state where qualified to do business.
2. **Map recurring obligations per jurisdiction.** Annual/biennial report, franchise or privilege tax, registered-agent requirement, business-license renewals — with due dates and filing authority.
3. **Pull current status.** Good standing? Any delinquent filings or taxes? Registered agent current and correct?
4. **Flag gaps and deadlines.** *Decision point:* any not-in-good-standing or delinquent status → escalate to counsel, since lapse can impair the entity's capacity to sue, contract, or close a deal.
5. **Confirm the minute book is current** — charter/bylaw versions, board and stockholder consents, cap-table records, and stock ledger.
6. **Build a compliance calendar** with owners and lead-time reminders for each recurring filing.
7. **Record status and next actions**; re-verify status directly with the filing authority rather than trusting a stale record.

## Example

Portfolio of 3 entities. Parent (DE C-corp): good standing, DE franchise tax due 3/1 — on calendar; qualified in CA and NY. Sub A (DE LLC): DELINQUENT — missed CA annual filing, escalated to counsel. Sub B: good standing, registered agent resigned last quarter — new agent needed within 30 days. Minute book: parent current; Sub A missing last two consents — flagged for reconstruction.

## Pitfalls

- **Tracking formation state only.** Every state where the entity does business has its own qualification and filing duties.
- **Trusting a cached status.** Verify good standing with the actual authority before relying on it.
- **Letting the registered agent lapse.** A resigned agent means missed service of process and eventual administrative dissolution.
- **A stale minute book.** Missing consents surface as diligence defects at the worst moment.

## Output format

```
ENTITY COMPLIANCE — <entity> (<type>, formed <jurisdiction>)
Qualified in: <states>
Recurring obligations:
  | Jurisdiction | Filing/tax | Due date | Authority | Owner | Status |
Current status: good standing | delinquent — <detail>
Registered agent: <name> — current? Y/N
Minute book currency: <gaps>
Compliance calendar (with reminders):
Escalations to counsel:
```

## Reference

Core entity obligations: annual/biennial reports, franchise/privilege tax, registered-agent maintenance, foreign qualification in each state of operation, and business-license renewals — all jurisdiction-specific. Good standing gates the entity's ability to contract, sue, and close transactions. The minute book (charter/bylaws, board and stockholder consents, stock ledger, cap table) is the corporate-records backbone diligence relies on. Status determinations with legal consequence and remediation of lapses are handled by counsel.
