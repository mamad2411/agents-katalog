---
name: payment-link
description: Use when the user wants to create a payment link, set up Stripe billing for a SaaS or product, run a sandbox checkout without Stripe Elements, diagnose the `payment-link` CLI, or mentions `payment-link` / `loopix` / Merchant of Record billing. Covers the full zero-signup flow from product creation to a shareable checkout URL, including sandbox testing and structured error handling for agents.
allowed-tools: Bash, Read, Grep
---

# payment-link — agent skill

`payment-link` is a zero-signup CLI that creates real Stripe-backed payment
links in one command. It was built agent-first: every command supports
`--json`, emits structured `{code, exitCode}` errors, and has a runtime
`schema` command so an agent can discover the full surface without reading
documentation.

## When to use this skill

Activate this skill when the user says any of:

- "create a payment link / checkout / Stripe product for X"
- "set up billing for my SaaS / course / template / toolkit"
- "collect $N/month for X" or "sell X for $N one-time"
- "test a paid flow without a real card"
- "diagnose / debug payment-link"
- "why is my sandbox checkout not working"
- anything that mentions `payment-link`, `npx payment-link`, `loopix`,
  Merchant of Record (MoR) billing, or the `checkout.new` domain

## Core workflow — fastest path

Always start with `schema` and `doctor`. Both are read-only, cheap, and
give you the full agent contract (exit codes, error codes, env vars,
rate limits, idempotency, command inventory) in one call.

```sh
# 1. Discover capabilities
npx payment-link schema --json
#    → .data.commands, .data.exitCodes, .data.errorCodes, .data.workflows

# 2. Verify runtime + reachability (read-only, no account changes)
npx payment-link doctor --json
#    → .data.ok is true iff no check failed

# 3. Preview before creating (validates everything, no side effects)
npx payment-link create "My SaaS" --price 29 --monthly --sandbox --dry-run --json

# 4. Execute — sandbox mode needs no signup
npx payment-link create "My SaaS" --price 29 --monthly --sandbox --json
#    → .data.url is the real checkout URL
#    → .data.checkoutId is the session id (used for simulate)

# 5. Simulate a customer paying, without Stripe Elements / a real card
npx payment-link simulate checkout <checkoutId> --email alice@test.dev --json
#    → .data.orderId / .data.subscriptionId / .data.benefitGrantIds
```

Everything past step 4 is sandbox-only. To go live the user must connect
Stripe (`payment-link connect-stripe`) and drop `--sandbox`.

## Contract agents can rely on

1. **Every command supports `--json`** and auto-enables it when stdout is
   not a TTY. Parse `.data` for success, `.code` + `.exitCode` on failure.
2. **Exit codes are stable:** `0` ok, `1` generic, `2` usage, `3` auth,
   `4` not found, `5` rate limit, `6` network, `7` conflict. Always
   branch on exit code, not stderr text.
3. **Error codes are machine-readable:** `auth_required`, `auth_failed`,
   `missing_argument`, `invalid_input`, `unknown_command`, `duplicate_slug`,
   `not_sandbox`, `not_found`, `rate_limited`, `network_error`,
   `idempotency_mismatch`, etc. Full list at
   `npx payment-link schema --json | jq .data.errorCodes`.
4. **`--dry-run`** on `create` validates and previews without side effects.
5. **`--idempotency-key`** on mutation commands makes retries safe.
6. **Prices are dollars by default.** Pass `--cents` to use integer cents.
7. **`--sandbox`** gives the user a zero-signup anonymous org that
   persists 30 days. Rate limited to 5 sessions/IP/day.

## MCP server (for Claude Desktop / Cursor / any MCP client)

`payment-link` ships with a built-in stdio MCP server. Register it in
the MCP client's config:

```json
{
  "mcpServers": {
    "payment-link": {
      "command": "npx",
      "args": ["-y", "payment-link", "mcp"],
      "env": {
        "LOOPIX_API_KEY": "sk_test_..."
      }
    }
  }
}
```

The MCP server exposes 5 focused tools: `create_payment_link`,
`list_products`, `simulate_checkout`, `doctor`, `get_schema`. Use this
when the user is setting up Claude Desktop / Cursor to create payment
links interactively.

For anything beyond the hero flow (customers, subscriptions, refunds,
webhooks, analytics, benefits, coupons, API keys, licenses), suggest
`npx loopix` and its own MCP server at `@loopix/mcp`.

## Reference files

Load these on demand when the user asks for details:

- **[reference.md](./reference.md)** — complete command-by-command surface
  (every flag, every exit code, every error code). Read this when the
  user asks about a specific command or wants to build a more complex
  workflow.
- **[examples.md](./examples.md)** — common patterns: idempotent retries,
  recovering from a failed checkout, chaining create → simulate → verify,
  wiring up webhooks, moving from sandbox to live.

## Common agent mistakes to avoid

- **Do not parse stderr text** — branch on `.code` / `.exitCode`. The
  text may be localized or reworded.
- **Do not construct checkout URLs manually.** The only source of truth
  is `.data.url` from `create` or `/v1/checkouts`. Pre-0.0.5 versions
  of the CLI used to hand out `pay.loopix.com` URLs that never worked.
- **Do not forget `--email`** on `simulate checkout` if the original
  checkout was created without one — without a customer attached, the
  webhook handler silently skips subscription and benefit granting.
- **Do not call `simulate` with a live key.** It will return
  `code: "not_sandbox"` with exit 3. Simulation is sk_test_* only.
- **Do not skip `doctor`** when debugging. It is read-only and tells
  you whether the API is reachable and the key is accepted in one call.
- **Do not hit the live Stripe account** from a sandbox test. Use
  `--sandbox` for all throwaway flows; sandbox sessions are isolated
  and self-expire in 30 days.

## Quick recipes

### "I want $29/month for my SaaS"

```sh
npx payment-link create "My SaaS" --price 29 --monthly --sandbox --json
# copy .data.url to share, or run `simulate checkout` to test the full
# paid flow end-to-end
```

### "Sell a $49 one-time toolkit"

```sh
npx payment-link create "Toolkit" --price 49 --sandbox --json
```

### "14-day free trial on an annual plan"

```sh
npx payment-link create "Pro" --price 299 --yearly --trial 14 --sandbox --json
```

### "Test the full paid flow end to end"

```sh
# Create
CHECKOUT=$(npx payment-link create "Test" --price 10 --monthly --sandbox --json | jq -r .data.checkoutId)
# Pay as a customer (sandbox only — no real money moves)
npx payment-link simulate checkout "$CHECKOUT" --email buyer@test.dev --json
# Inspect the resolved order / subscription / benefit grants
```

### "I want to diagnose a broken key"

```sh
npx payment-link doctor --json
# Look at .data.checks[] — each has status: pass/warn/fail/skip and a hint.
```
