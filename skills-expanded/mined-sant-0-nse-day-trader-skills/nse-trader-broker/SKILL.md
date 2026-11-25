---
name: nse-trader-broker
description: Broker-neutral Manual NSE Order Ticket. Accepts only an order that passed nse-trader-risk, writes portable JSON and Markdown for the entry plus protective exits, logs exact approval and optional observed fills, and never contacts a broker. Use when the user says "show my order ticket", "place it manually", "approve this trade", names any Indian broker app, or after nse-trader-risk passes.
---

# nse-trader-broker

The final handoff to **manual broker entry**. It refuses tickets without a
matching `PASS` in `risk_state.json`, then creates a broker-neutral `ticket.json`
and human `ticket.md`. It can label any broker, log approval and record a fill
you observed. It never imports a broker SDK, reads credentials or sends an order.

## Show the ticket

```bash
python scripts/ticket.py --order nse-trader/orders.json --broker generic
```

Status is `AWAITING_APPROVAL`. After reviewing every field:

```bash
python scripts/ticket.py --order nse-trader/orders.json \
  --approval "I approve RELIANCE 8 shares with this stop and target"
```

Record a fill that you manually saw in your broker:

```bash
python scripts/ticket.py --order nse-trader/orders.json \
  --approval "approved" --fill --price 1452.40 --qty 8
```

Approval is only a local audit record. It does not grant this skill broker
access.

## Manual broker sequence

1. Verify the exact NSE instrument. For F&O, verify expiry, strike, option type
   and current NSE lot size.
2. Enter the BUY limit order in your selected broker.
3. Wait for a **full fill**.
4. Prefer the broker's OCO/bracket protection: SELL target LIMIT + stop `SL-M`.
   If OCO is unavailable, manage exits manually and never leave separate
   exits capable of both executing.
5. Cancel remaining orders and flatten MIS by 15:15 IST.

The default profile is generic and contains no app-specific code. Passing
`--broker groww` adds an optional, not-executed Groww SDK illustration. The
installed script itself still has no broker execution path.

### Broker/product caveats

- OCO/bracket support, product labels and square-off policy differ by broker.
- This toolkit sizes long options only; it does not create naked/short-option tickets.
- For the optional Groww example, re-check the current Smart Orders docs before use.

## Gate and files

| File | What |
|---|---|
| `nse-trader/orders.json` | sized order from `nse-trader-budget` |
| `nse-trader/risk_state.json` | must contain matching PASS |
| `nse-trader/ticket.json` | portable broker-neutral order contract |
| `nse-trader/ticket.md` | human ticket; optional profile-specific appendix |
| `nse-trader/approvals.jsonl` | exact local approval phrases |
| `nse-trader/fills.jsonl` | user-observed fills only |

No PASS, no ticket. No explicit `--approval`, no approval record. Nothing here
is a guarantee of execution, fill price, margin or broker acceptance.
The JSON contract is documented in `references/ticket-schema.md`.

Educational tooling only, not financial advice.
