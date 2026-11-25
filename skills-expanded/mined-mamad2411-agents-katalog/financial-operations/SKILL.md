---
name: financial-operations
description: Playbook for executing financial operations, banking, payments, corporate cards, and fraud verification.
---

# Financial Operations

This skill defines the workflow for managing Cooper's financial operations, including bank triage, fraud alerts, Zelle transfers, and corporate API interactions (Brex, Stripe, Gusto).

## Security & Approval Boundaries
- **Read-Only by Default:** You may investigate, read balances, and scrape alerts autonomously.
- **GATED ACTIONS (Require Explicit Confirmation):** Sending money (Zelle, Wires), disputing fraud, clicking "Yes/No" on fraud alerts, rotating API keys, updating KYC details.
- **Observable Evidence:** Never mark a financial task "Done" without verifiable evidence (a receipt, a success JSON response, or explicitly handing off to Cooper).

## 1. Browser Access for Legacy Banks (BoA, Amex, Capital One)
Use the Live Chrome CDP workflow, NOT Camofox remote sessions, because these sites rely on device trust and passkeys.
- **Full reference:** `references/live-chrome-cdp.md` — setup, security rules, OAuth flows, DOM interaction patterns, **and AppleScript fallback when CDP port 9222 is down** (including the multi-instance Chrome targeting fix).
- **Endpoint:** `127.0.0.1:9222`
- **Helper Script:** `~/.hermes/scripts/live-chrome-cdp.js`
- **Workflow:** Navigate to a new tab, use DOM inspection to read alerts. Stop if "Remember this device" or "Fraud Yes/No" decisions are prompted, unless guided by the user.
- **CDP Down?** Fall back to AppleScript (`osascript`) + `computer_use`. See the "Fallback: AppleScript When CDP Is Down" section in `references/live-chrome-cdp.md` — covers the multi-instance Chrome problem (kill Playwright/Puppeteer Chrome processes so AppleScript targets Cooper's real Chrome) and enabling "Allow JavaScript from Apple Events".

## 1b. Zelle Transfers via AppleScript (CDP Down Fallback)

When CDP is unavailable and you've fallen back to AppleScript JS execution,
the complete BofA Zelle transfer flow (login → select recipient → enter
amount → set date → review → confirm) is documented in
`references/bofa-zelle-applescript.md` — includes all field selectors, the
multi-tab targeting pattern, and the Python subprocess technique for reliable
JS escaping in `osascript`.

**Key pitfalls:**
- BofA's `fsdgoto()` SPA navigation function is not accessible from
  AppleScript `execute javascript` context. Must find and click link elements
  directly, or check for an already-open Zelle tab.
- The **Pay button** (`#Pay-review-btn`) is a SPA button with no parent
  `<form>`. JS `.click()` via `execute javascript` silently fails and may
  cause a partial-submission error. Must use AppleScript AX
  `perform action "AXPress"` via `entire contents of w` to press it
  natively. See Step 7 in the reference for the full pattern.

## 2. 1Password Service Account Injection
**Never bare `op`** (biometric / human pop-up). Always himitsu service account:
- **Token:** `op-service-account/token` via `himitsu` (`TOKEN` env inside `himitsu exec`).
- **Usage:**
  ```bash
  himitsu exec op-service-account/token -- bash -lc \
    'OP_SERVICE_ACCOUNT_TOKEN=$TOKEN op item get <id> --vault <vault> --format json'
  ```
- **REQUIRED:** `--vault` on every SA call (`cm` | `cooper` | `dev`). List also needs vault when scoped.
- **Standing cards:** default pay **Amex Platinum** vault `cm` id `nj33napkeiybo5o4fezookdb4i` (Koutarou Maruyama, ZIP 90015). Coinbase One is `p2yhadwwld4fpxilkw6w4hhvwa` only if user picks it.
- Deep call flow: skill **`vapi-call-ops`** (prefer over thinner `vapi-phone*` stubs). KB/Vapi Files may hold addresses/emails/cards; still gate spend; never invent PAN.
- **Pitfall:** Never print passwords/PANs to stdout or shell arrays. Scrub temp files. Pass secrets only into the process that needs them.

## 3. Retrieving 2FA / OTP
If SMS 2FA is sent, extract it securely from the local macOS Messages database using SQLite:
```python
import sqlite3
# Example query logic for ~/Library/Messages/chat.db looking at recent rows where is_from_me=0
```

## 4. Brex API
Brex provides a developer API which is vastly preferred over UI automation.
- **Credential:** Stored in himitsu as `brex-api-token`.
- **Usage:** `himitsu exec brex-api-token -- bash -c 'curl -s -X GET https://platform.brexapis.com/v2/users/me -H "Authorization: Bearer <REDACTED>"'`
- **Pitfall:** Ensure you map API version requirements appropriately (e.g., `v2` for Users).

## 5. Stripe & Gusto Handling
- **Stripe:** Platform dictates strong KYC (address reviews, beneficial owner checks). Provide the direct `connect.stripe.com/express/...` link to Cooper as a HANDOFF task.
- **Gusto:** Used for domestic and international contractor payouts. Verify transaction completion statuses by querying Gmail for automated debit confirmations rather than interacting with the UI.
