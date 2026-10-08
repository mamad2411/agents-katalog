---
name: netchain
description: Drive the NetChain corporate netting ledger (record obligations, run netting cycles, settle) through the netchain MCP server. Use when asked to record an invoice/obligation, check balances or net positions, run or settle a netting cycle, or verify NetChain's per-party settlement caps or contract privacy.
---

# NetChain agent workflow

NetChain nets obligations between companies and settles them in cycles, gated by each
party's on-ledger `TreasuryPolicy` cap. Use the `netchain` MCP server's tools for all of
this, do not guess at ledger state, always read it first.

## Recommended order of operations

1. **Look before acting.** Call `list_obligations`, `get_balances`, and/or
   `get_net_positions` for the relevant party before creating or settling anything.
2. **Record obligations** with `create_obligation` as invoices/payables arise. Each one
   starts PENDING (bilateral consent) and does not net until the obligee accepts it.
3. **Confirm as the obligee** with `accept_obligation` (using the obligation's `contractId`
   from `list_obligations`, where a pending one reads `accepted: false`). Only accepted
   obligations enter a netting cycle, this is the fake-invoice safeguard: a debt settles
   only after both the obligor (who created it) and the obligee (who accepts it) agree.
4. **Before proposing a settlement**, check the relevant party's cap with `get_policy`
   and, if you have a specific amount in mind, dry-run it with `check_policy`. This tells
   you whether a settlement will be accepted, without changing ledger state.
5. **Run the cycle** with `run_netting_cycle`, then inspect the result with
   `get_net_positions` before settling.
6. **Settle** with `settle`. Remember: this call is capped on-ledger by every involved
   party's `TreasuryPolicy.maxSettlementPerCycle`. If the netted amount for any party
   exceeds its cap, the ledger itself rejects the whole settlement, do not try to
   retry, split the request, or otherwise work around this from the agent side. If
   `settle` fails this way, the correct response is to reduce the obligations that make up
   the cycle (or wait for a human to raise the party's policy cap), not to keep retrying
   the same call.
7. **Audit with `get_activity`** to confirm what actually happened, and use
   `query_contract` if you need to demonstrate or verify that a party genuinely cannot see
   a contract it isn't a stakeholder on (a 404 there is expected privacy behavior, not a
   bug). Use `verify_transaction` if you need to prove a `settle`/transaction `updateId` is
   real, it re-fetches it from the live Canton validator without exposing its private
   content.

Obligations you create are stamped `source: "agent"` on-ledger by default, pass
`source: "manual"` to `create_obligation` if you are recording something on a human's
behalf instead of acting autonomously.

## Bounded authority

This is the one thing to internalize: you (the agent) can *propose* any obligation, cycle,
or settlement. You cannot make the ledger accept a settlement that breaks a party's
`TreasuryPolicy` cap. That enforcement lives in the Daml contract, not in this server or in
your own judgment, treat a policy rejection as final, not as an error to engineer around.
