---
name: front-counter-service
description: Handles governed in-person service-counter intake, queue triage, order or service lookup, payment handoff, document exchange, complaint escalation, and transaction closure. Use for front-counter, service-desk, clerk, or walk-in customer workflows.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source: Original LeeWay work-domain skill requested during D/E capability reconciliation
---

# Front Counter Service

Use an approved greeting and identify the requested service. Verify identity only to the level required by policy. Confirm item, order, appointment, price, eligibility, documents, and next step from authorized systems; never infer them from appearance or memory.

Keep payments, refunds, signatures, regulated disclosures, access changes, and exceptions behind their specialist workflows and approval controls. Read back critical details and provide a receipt or reference only after the system confirms the transaction.

Record queue time, request class, actions, handoffs, exceptions, and final state while minimizing personal data. Use `INQUIRY`, `WAITING`, `IN_SERVICE`, `PENDING_APPROVAL`, `COMPLETED_VERIFIED`, or `ESCALATED`.
