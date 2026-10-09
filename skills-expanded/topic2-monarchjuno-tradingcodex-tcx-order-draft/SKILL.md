---
name: tcx-order-draft
description: "Create a canonical draft OrderTicket after research, valuation, portfolio, and risk context exist."
---

# Create Order Ticket

Use this skill only after research, valuation, portfolio, and risk artifacts exist.

Primary output is a canonical `OrderTicket` created through the TradingCodex
service layer, normally via the workspace MCP tool `create_order_ticket`.

Universe and adapter gate:

- Confirm the universe and instrument are supported by the current order ticket schema, policy, broker/adapter path, and user request.
- Built-in paper support does not imply live broker, options, futures, crypto account, margin, short borrow, FX, commodity, or credit-instrument execution support.
- If the requested instrument cannot be represented by the installed order ticket schema and adapter, write a revise/block reason instead of drafting.
- `screen-grade` and `not-decision-ready` work cannot become draft orders.

Required fields:

- `ticket_id`
- `symbol`
- `side`
- `quantity`
- `limit_price`
- `currency`
- `broker_id`
- `created_by`

Rules:

- `created_by` must match the configured drafting principal.
- Default broker is `paper-trading`.
- Live broker adapters are not installed by default.
- Do not fabricate missing prerequisite analysis, prices, quantities, costs, portfolio state, approval state, or user constraints.
- Do not fabricate instrument support, adapter support, borrow/locate, option terms, margin terms, funding rates, or account eligibility.
- In narrative notes, distinguish sourced facts, analysis, and assumptions in natural prose; keep non-schema labels out of the order ticket payload.
- Run the `run_order_checks` MCP tool after creating the ticket.
- Include the ticket id, current state, check results, and unresolved gaps in the output.
- Include a note that approval and execution are separate downstream gates.
- If prerequisites are missing, write a revise/block reason instead of drafting.
