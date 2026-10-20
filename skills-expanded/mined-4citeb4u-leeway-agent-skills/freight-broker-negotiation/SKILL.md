---
name: freight-broker-negotiation
description: Prepares and governs freight-broker load qualification and rate negotiation for carriers and dispatchers. Use for broker calls, rate strategy, load questions, carrier fit, written confirmation, or documenting a negotiated offer.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source: LeeWay DISPATCH_LOGISTICS_PACK.md normalized from E-drive capability inventory
  source-skill: logistics.broker.negotiate_load
---

# Freight Broker Negotiation

## Boundary

Do not place calls, represent a carrier, accept a rate, sign a rate confirmation, or disclose credentials without explicit authorization and a live approved telephony/email adapter. A generated script is not a negotiation, and a spoken offer is not a booked load.

## Workflow

1. Verify carrier identity, authority, insurance, equipment, driver availability, and permitted negotiation range.
2. Qualify the load: commodity, weight, dimensions, stops, times, detention, layover, TONU, lumper, tracking, special handling, and payment terms.
3. Establish a sourced lane benchmark and calculate the carrier's floor from total miles, time, risk, and operating cost.
4. Prepare an opening request, objective justification, walk-away point, and approved concessions.
5. During an authorized interaction, record offers accurately; never invent broker statements or commitments.
6. Require written rate confirmation and compare every term with the negotiated record before human acceptance.

## Receipt

Bind broker/load identity, source, time, participants, offers, final written terms, discrepancies, approvals, and execution state. Use `PREPARED`, `CONTACTED`, `OFFERED`, `WRITTEN_CONFIRMATION_RECEIVED`, or `BOOKED_VERIFIED` precisely.
