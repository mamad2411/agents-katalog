---
name: easypaydirect
description: Answer payment questions from an Easy Pay Direct (EPD) or other NMI-family gateway using the read-only easypaydirect MCP tools — did a customer pay, why a charge failed, what a subscription or plan looks like, what's stored in the Customer Vault. Use whenever the user asks about transactions, declines, refunds, ACH/e-check payments, recurring subscriptions, billing plans, or vault records on EPD / NMI.
---

# Easy Pay Direct / NMI gateway

The `easypaydirect` MCP server gives you **seven read-only tools** over the gateway's
Query API. Nothing here can charge, refund, void, or change a subscription — if the
user asks for that, say it has to be done in the gateway portal, and never imply you did it.

| Tool | Use it for |
|---|---|
| `search_transactions` | "Did X pay?", declines, refunds, anything by email / order id / date / status |
| `get_transaction` | Full detail of one transaction id (every action on it) |
| `get_subscription` | One recurring subscription by id |
| `list_subscriptions` | Subscriptions created/updated in a date range |
| `list_recurring_plans` | Plan templates (name, amount, frequency) — call with no args to find a plan by name |
| `get_customer_vault_record` | One stored customer profile by vault id |
| `list_customer_vault` | Vault records created/updated in a date range |

## Picking the right call

- **"Did this customer pay?" / "why did their card fail?"** → `search_transactions` with
  `email` (add `start_date`/`end_date` to narrow). Then `get_transaction` on the ids that
  matter to see every action.
- **"What is this customer's billing set-up?"** → find their transactions by email, read the
  `customer_vault_id` / subscription ids from them, then `get_customer_vault_record` and
  `get_subscription`.
- **"Which plan is 'Monthly Pro'?"** → `list_recurring_plans` with no arguments, match on
  `plan_name`, then use its `plan_id`.
- **Failures only** → `condition: "failed"`; **refunds** → `action_type: "refund"`;
  **ACH only** → `transaction_type: "ck"`.

## Reading results

Responses are the gateway's XML turned into JSON, so they are nested:

- The root is `nm_response`. Records sit under `nm_response.transaction`,
  `nm_response.subscription`, `nm_response.plan`, or `nm_response.customer_vault.customer`.
- **One match is an object; several matches are an array.** Handle both. An empty
  `nm_response` means no records matched — say so plainly.
- A transaction's `action` is its history (sale, settle, refund, return, …), again an
  object for one entry or an array for several. The **latest action** tells you where
  the money actually is; the top-level `condition` summarises it.
- Every value is a **string**, including amounts. Don't do float maths on them carelessly;
  keep two decimals.

## Traps — check these before you answer

1. **ACH "success" is not "paid".** For `transaction_type` `ck`, a successful sale only means
   the debit was *submitted*: `condition` stays `pendingsettlement` for several business days.
   It is paid when a settle action appears; it bounced if a return (`check_return` /
   `check_late_return`) appears. Never report an ACH payment as collected from the sale alone.
   A subscription can look perfectly healthy (active, no failed count, rising completed
   payments) while every ACH debit is being returned — check the transactions.
2. **Dates.** Inputs and outputs use `YYYYMMDDhhmmss`. Easy Pay Direct returns these in **UTC**;
   convert to the user's timezone before stating a date or "yesterday". If you're on a
   different NMI white-label and unsure of its timezone, say which timezone you assumed.
3. **Big date ranges can time out.** For more than a few weeks of busy history, split the
   range into smaller windows (e.g. a week at a time) and combine the results.
4. **Deleted subscriptions disappear.** A subscription that was deleted is no longer returned
   by the recurring report, so "not found" does **not** prove it never existed. Its charges
   are still visible through `search_transactions`.
5. **One customer, several vault records.** The same email can have more than one
   `customer_vault_id` (a new card or a new set-up often creates a new record). Don't assume
   the first one is the only one.
6. **Who did it?** A transaction's `source` separates scheduled billing (`recurring`),
   integrations (`api`), and a person keying it in (`virtual_terminal`, with a `username`).
   Use it for "was this automatic or manual?".
7. **Manual collections don't move subscription counters.** If someone collects a missed
   instalment by hand in the virtual terminal, the subscription's completed/remaining counts
   don't change, so the recurring engine may try that same instalment again later. A decline
   that follows a manual payment of the same amount may be for money already collected.

## Privacy

Results can contain names, emails, addresses, and masked card details. Only repeat what the
user needs for their question, don't paste whole records unprompted, and never ask for or
echo the gateway security key.

## When a tool returns an error

- `Unexpected non-XML response (check NMI_SECURITY_KEY and NMI_API_URL)` — the key is wrong
  or lacks Query API permission, or `NMI_API_URL` points at the wrong gateway host. The user
  must fix their MCP configuration; retrying won't help.
- `Network error` or an HTTP 5xx — the gateway is unreachable; try once more, then report it.
