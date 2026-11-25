---
name: tcx-order-approve
description: "Approve or reject a checked OrderTicket without executing it after risk review, policy review, restricted-list checks, and creator-versus-approver separation."
---

# Approve Order

Use this skill to approve or reject a checked OrderTicket after risk and policy
review.

Required inputs:

- Canonical order ticket id
- Risk review artifact or risk-check output
- Policy review result or `simulate_policy` output
- Universe/instrument support and adapter eligibility from policy review

Approval path:

1. Fetch the ticket with `get_order_ticket`.
2. Run or inspect `run_order_checks` and require no failing checks.
3. Confirm `approved_by` is not the same principal as `created_by`.
4. Confirm restricted list, enabled adapter, instrument support, notional limit, and approval readiness are all acceptable.
5. Create the approval receipt through `request_order_approval` as the configured approval principal.
6. Confirm the receipt binds `order_ticket_id`, broker/account scope, expiry, and the exact order payload hash.

Reject path:

- If validation, risk, or policy fails, write or reference the rejection reason.
- Do not create an approval receipt for a revise/reject decision.

Rules:

- Do not approve a live broker order unless a user-installed adapter and policy explicitly enable it.
- Do not approve unsupported universes or instruments merely because research or screen-grade analysis exists.
