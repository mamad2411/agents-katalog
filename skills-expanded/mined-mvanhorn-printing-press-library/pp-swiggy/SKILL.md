---
name: pp-swiggy
description: "Every Swiggy Builders Club tool, one persistent OAuth session, and a local order history no Swiggy surface shows you. Trigger phrases: `order food on Swiggy`, `search Swiggy restaurants`, `order groceries on Instamart`, `book a table on Dineout`, `track my Swiggy order`, `use swiggy`, `run swiggy`."
author: "Som Samantray"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - swiggy-pp-cli
    install:
      - kind: go
        bins: [swiggy-pp-cli]
        module: github.com/mvanhorn/printing-press-library/library/food-and-dining/swiggy/cmd/swiggy-pp-cli
---

# Swiggy — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `swiggy-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install swiggy --cli-only
   ```
2. Verify: `swiggy-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails (no Node, offline, etc.), fall back to a direct Go install (requires Go 1.26.6 or newer). This installs into `$GOPATH/bin` (default `$HOME/go/bin`), so add that directory to `$PATH` instead:

```bash
go install github.com/mvanhorn/printing-press-library/library/food-and-dining/swiggy/cmd/swiggy-pp-cli@latest
```

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

Wraps all 51 official Swiggy MCP tools across Food, Instamart, and Dineout into one CLI that respects Swiggy's own session-reuse rules instead of tripping rate limits. Adds cross-domain spend history, a safe-retry guard for non-idempotent order placement, and a UPI payment-wait command on top.

## When to Use This CLI

Use this CLI for scripted or agent-driven Swiggy commerce flows: searching restaurants/products, managing carts, placing orders, booking tables, and tracking deliveries/bookings across Food, Instamart, and Dineout. Good for building or debugging an agent on top of Swiggy Builders Club before wiring a full agent framework, or for personal automation of routine orders.

## Anti-triggers

Do not use this CLI for:
- Do not use this CLI for Swiggy's consumer web/app features outside the Builders Club MCP surface (e.g. loyalty program management, customer support chat).
- Do not use this CLI for production-scale/multi-tenant traffic without applying for production access at mcp.swiggy.com/builders/access — this CLI targets a single authenticated user's own account.
- Do not use this CLI to exceed the ₹1000 Food cart cap or bypass Swiggy's documented rate limits.

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Local state that compounds
- **`history`** — See spend and order counts across Food and Instamart in one view, even though Swiggy keeps them completely separate. Instamart totals are a sample of at most 20 orders (`get_orders` has no pagination) and are labeled `partial` when that cap is hit. `--since` is reserved and unused. Dineout has no orders-list tool and is not included.

  _Reach for this when the user asks about overall Swiggy spend or activity rather than a single domain's orders._

  ```bash
  swiggy-pp-cli history --address-id addr_01HXYZ --agent
  ```

### Agent-native plumbing
- **`pay wait`** — Block until a UPI payment resolves instead of hand-rolling a polling loop yourself. Not for COD orders — check payment status once and proceed instead.

  _Use this immediately after any UPI place-order/checkout/book-table call; do not poll check-payment-status manually._

  ```bash
  swiggy-pp-cli pay wait --paas-id paas_123 --order-id ord_01HXYZ --domain food --max-wait 5s
  ```
- **`status`** — Check local credential presence and stored token expiry. A token with no stored expiry (typical for `SWIGGY_ACCESS_TOKEN`) is reported as unknown, not fully authenticated, and re-auth is recommended. This is not a live Swiggy validation.

  _Check this before starting a multi-step order flow; treat unknown expiry or a later 401 as a signal to re-run auth login._

  ```bash
  swiggy-pp-cli status
  ```

### Reachability mitigation
- **`order verify-before-retry`** — Check whether a food or grocery order actually went through before retrying a failed placement. Matches amount/restaurant only inside `--within` (default 30m). Orders without timestamps fail closed instead of being treated as already placed or safe to retry.

  _Use this before ever re-issuing place-food-order or checkout after a 5xx or timeout._

  ```bash
  swiggy-pp-cli order verify-before-retry --domain food --address-id addr_01HXYZ --amount 450 --within 30m
  ```

## Command Reference

**dineout** — Swiggy Dineout MCP tools

- `swiggy-pp-cli dineout book-table` — Swiggy Dineout (Reservations): Book a table at a restaurant for a specific time slot
- `swiggy-pp-cli dineout cancel-booking` — Swiggy Dineout (Reservations): Cancel an existing table reservation by orderId
- `swiggy-pp-cli dineout check-payment-status` — Check one payment-status iteration for an in-flight UPI payment
- `swiggy-pp-cli dineout confirm-order` — Complete an order after payment succeeds
- `swiggy-pp-cli dineout create-cart` — Swiggy Dineout (Reservations): Create a booking cart
- `swiggy-pp-cli dineout get-available-slots` — Swiggy Dineout (Reservations): Check available time slots for TABLE BOOKING at a restaurant
- `swiggy-pp-cli dineout get-booking-status` — Swiggy Dineout (Reservations): Get booking status and details for a dineout reservation
- `swiggy-pp-cli dineout get-payment-options` — Fetch the live payment methods currently available for the cart
- `swiggy-pp-cli dineout get-restaurant-details` — Swiggy Dineout (Reservations): Get details about a specific restaurant for TABLE BOOKING
- `swiggy-pp-cli dineout get-saved-locations` — Swiggy Dineout (Reservations): Get user's saved addresses for restaurant search
- `swiggy-pp-cli dineout report-error` — Generate an error report to share with the Swiggy MCP team
- `swiggy-pp-cli dineout search-restaurants-dineout` — Swiggy Dineout (Reservations): find restaurants to BOOK A TABLE at

**food** — Swiggy Food MCP tools

- `swiggy-pp-cli food apply-food-coupon` — Apply coupon code or discount to food delivery order
- `swiggy-pp-cli food check-payment-status` — Check one payment-status iteration for an in-flight UPI payment
- `swiggy-pp-cli food confirm-order` — Complete an order after payment succeeds
- `swiggy-pp-cli food create-address` — Swiggy (Instamart/Food): Create a new delivery address for the authenticated user.
- `swiggy-pp-cli food delete-address` — Swiggy (Instamart/Food): Delete a saved delivery address for the authenticated user.
- `swiggy-pp-cli food fetch-food-coupons` — Get available coupons and offers for food delivery order
- `swiggy-pp-cli food flush-food-cart` — Clear or empty the food delivery cart
- `swiggy-pp-cli food get-addresses` — Swiggy (Instamart/Food): Get saved delivery addresses for the authenticated Swiggy user
- `swiggy-pp-cli food get-food-cart` — Get current food delivery cart with all items
- `swiggy-pp-cli food get-food-delivery-status` — Get the latest delivery ETA and terminal delivery state for a Food order
- `swiggy-pp-cli food get-food-order-details` — Get detailed information about a specific food delivery order
- `swiggy-pp-cli food get-food-orders` — Swiggy Food order history - Use this to fetch ORDER HISTORY, past orders, or active orders
- `swiggy-pp-cli food get-payment-options` — Fetch the live payment methods currently available for the cart
- `swiggy-pp-cli food get-restaurant-menu` — Browse a restaurant's complete menu as a flat, deduplicated list of dishes
- `swiggy-pp-cli food place-food-order` — Place food delivery order and confirm order placement
- `swiggy-pp-cli food report-error` — Generate an error report to share with the Swiggy MCP team
- `swiggy-pp-cli food search-menu` — Search for dishes and menu items to order for food delivery
- `swiggy-pp-cli food search-restaurants` — Search and order food from restaurants for delivery
- `swiggy-pp-cli food track-food-order` — Track food delivery order status and delivery progress
- `swiggy-pp-cli food update-food-cart` — Add items to food delivery cart or update cart contents

**instamart** — Swiggy Instamart MCP tools

- `swiggy-pp-cli instamart apply-coupon` — Swiggy Instamart (Grocery): Apply a coupon code to the current Instamart cart
- `swiggy-pp-cli instamart check-payment-status` — Check one payment-status iteration for an in-flight UPI payment
- `swiggy-pp-cli instamart checkout` — Swiggy Instamart (Grocery): Place and confirm Swiggy Instamart grocery order
- `swiggy-pp-cli instamart clear-cart` — Clear (remove all items from) the Instamart cart
- `swiggy-pp-cli instamart confirm-order` — Complete an order after payment succeeds
- `swiggy-pp-cli instamart create-address` — Swiggy (Instamart/Food): Create a new delivery address for the authenticated user.
- `swiggy-pp-cli instamart delete-address` — Swiggy (Instamart/Food): Delete a saved delivery address for the authenticated user.
- `swiggy-pp-cli instamart get-addresses` — Swiggy (Instamart/Food): Get saved delivery addresses for the authenticated Swiggy user
- `swiggy-pp-cli instamart get-cart` — Swiggy Instamart (Grocery): Get current Swiggy Instamart grocery cart with all items and bill breakdown
- `swiggy-pp-cli instamart get-delivery-status` — Usage notes - Use for structured delivery ETA refreshes after an Instamart order is placed.
- `swiggy-pp-cli instamart get-order-details` — Get detailed information for a specific Swiggy Instamart order by order ID
- `swiggy-pp-cli instamart get-orders` — Swiggy Instamart order history - Use this to fetch ORDER HISTORY, past orders, or order preferences
- `swiggy-pp-cli instamart get-payment-options` — Fetch the live payment methods currently available for the cart
- `swiggy-pp-cli instamart list-coupons` — Swiggy Instamart (Grocery): List available coupons for the current cart
- `swiggy-pp-cli instamart report-error` — Generate an error report to share with the Swiggy MCP team
- `swiggy-pp-cli instamart search-products` — Search for products available at the selected address
- `swiggy-pp-cli instamart track-order` — Track Swiggy Instamart order status in real-time
- `swiggy-pp-cli instamart update-cart` — Swiggy Instamart (Grocery): Update Swiggy Instamart grocery cart with items
- `swiggy-pp-cli instamart your-go-to-items` — Fetch the user's Your Go To Items (frequently or recently ordered items) for the selected delivery address


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
swiggy-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query. `--json` (and other machine formats) keep that exit-2 contract and write `{"matches":[]}` on stdout so agents can inspect the envelope without treating a miss as success.

## Recipes

### Order food end-to-end

```bash
swiggy-pp-cli food search-restaurants --address-id addr_01HXYZ --query biryani && swiggy-pp-cli food get-restaurant-menu --address-id addr_01HXYZ --restaurant-id r_123 --select restaurantId,items.id,items.name,items.price
```

Search then narrow a large menu payload down to just the fields needed to build a cart.

### Book a table

```bash
swiggy-pp-cli dineout get-available-slots --restaurant-id r_456 --date 2026-09-20 --latitude 28.4595 --longitude 77.0266
```

Check slot availability before booking.

### Safe retry after a failed order

```bash
swiggy-pp-cli order verify-before-retry --domain food --address-id addr_01HXYZ --restaurant-id r_123 --amount 450
```

Confirms whether a non-idempotent place-food-order call actually succeeded before retrying.

### Check spend across Food and Instamart

```bash
swiggy-pp-cli history --address-id addr_01HXYZ --agent --select total_spend,order_count,by_domain
```

Cross-domain aggregation (Food + Instamart; Dineout has no orders-list tool) with a narrowed agent-friendly field selection. --address-id is required to include Food.

## Auth Setup

Swiggy Builders Club uses OAuth 2.1 with PKCE and Dynamic Client Registration — no API key. Run `swiggy-pp-cli auth login` to open a browser, log in with your phone number and OTP on Swiggy's own consent screen, and the CLI stores the resulting 5-day access token. There is no refresh token in v1.0; re-run `auth login` when it expires.

Run `swiggy-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color`.

Global format flags share one contract on promoted, novel, sync, and `--deliver` paths:

- `--json` — one JSON document on stdout (sync progress events go to stderr)
- `--compact` — keep identity/status/timestamp fields; does not change the document vs stream shape
- `--csv` / `--plain` — tabular rows (collection envelopes unwrap to the row array)
- `--quiet` — one identity value per row, no envelope

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  swiggy-pp-cli dineout get-available-slots --restaurant-id 550e8400-e29b-41d4-a716-446655440000 --agent
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Non-interactive** — never prompts, every input is a flag
- **Explicit confirmation** — `--agent` does not imply `--yes`; pass `--yes` separately only after the target, arguments, and side effects are clear
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success

## Paths and state

Agents should treat the CLI's path resolver as part of the runtime contract:

- Use `--home <dir>` for one invocation, or set `SWIGGY_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `SWIGGY_CONFIG_DIR`, `SWIGGY_DATA_DIR`, `SWIGGY_STATE_DIR`, `SWIGGY_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `SWIGGY_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `swiggy-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "swiggy": {
        "command": "swiggy-pp-mcp",
        "env": {
          "SWIGGY_HOME": "/srv/swiggy"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `SWIGGY_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `SWIGGY_HOME`, or `doctor` will not find credentials left under the former root.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
swiggy-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
swiggy-pp-cli feedback --stdin < notes.txt
swiggy-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `SWIGGY_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `SWIGGY_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename). Binary-response commands write decoded payload bytes (not the base64 JSON envelope) and print a small JSON receipt on stdout; `--json`/`--csv` do not refuse when this sink is set. |
| `webhook:<url>` | POST the output body to the URL (`application/json`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled or recurring agent reuses the same saved flags while providing different input each run.

```
swiggy-pp-cli profile save briefing --json
swiggy-pp-cli --profile briefing dineout get-available-slots --restaurant-id 550e8400-e29b-41d4-a716-446655440000
swiggy-pp-cli profile list --json
swiggy-pp-cli profile show briefing
swiggy-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 6 | Partial failure |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `swiggy-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

1. Install the MCP server:
   ```bash
   go install github.com/mvanhorn/printing-press-library/library/food-and-dining/swiggy/cmd/swiggy-pp-mcp@latest
   ```
2. Register with Claude Code:
   ```bash
   claude mcp add swiggy-pp-mcp -- swiggy-pp-mcp
   ```
3. Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which swiggy-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   swiggy-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `swiggy-pp-cli <command> --help`.
