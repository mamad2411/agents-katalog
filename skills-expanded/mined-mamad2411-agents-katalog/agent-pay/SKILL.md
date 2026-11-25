---
name: agent-pay
description: Auto-provision a virtual Visa card to complete an online purchase. Use when user asks to buy something and needs payment, or explicitly mentions cypher-pay/agent-pay. Handles onboarding (email OTP + KYC — once ever), token generation (once per device), funding, card creation, 3DS, and card lifecycle.
---

# Cypher Pay — Virtual Cards for AI Agents

Cypher Pay gives AI agents programmable virtual Visa cards. Create cards on demand, set spend limits, handle 3DS, and manage card lifecycle (single-use or reusable). All operations available via the `agent-pay` CLI — every command outputs JSON to stdout.

## When to invoke

Trigger when end-user needs to buy something online and lacks a payment method, OR explicitly asks for "cypher pay" / "agent card" / "virtual card for this purchase".

This is a CONSUMER automation flow. Do NOT:
- ask which directory to create a project in
- ask about frameworks, TypeScript vs JavaScript, or build tools
- show code to the user or ask permission to run code
- ask to set up a `package.json` or install dependencies into user projects

You run CLI commands yourself. The user sees only: onboarding prompts (email, OTP, personal details), funding links, and purchase confirmations. All agent-pay commands output JSON — parse it silently, surface only what matters to the user.

## Prerequisites

Ensure the CLI is available. Install globally once (silent, no user prompt needed):
```bash
npm install -g @cypherhq/agent-pay
```
Or use `npx @cypherhq/agent-pay <command>` if you prefer not to install globally.

## Session detection (run FIRST, every invocation)

Start here. Every time. No exceptions.

**Step 1 — Check for existing token:**
The CLI auto-reads tokens from `AGENT_PAY_TOKEN` env var or `~/.config/cypher-pay/token`. Just verify:
1. Run `agent-pay agent`. If exit code 0 → token valid, skip to purchase flow.
2. If exit code 2 or no token → ask user for their email, then run:
   ```bash
   agent-pay auth-status <email>
   ```
   This returns `{ "enrolled": bool, "kycComplete": bool }`. No OTP sent, no auth required. Branch:

   | enrolled | kycComplete | Action |
   |----------|-------------|--------|
   | true     | true        | User has account — just needs token. Run **Returning user flow** below. |
   | true     | false       | Account exists, KYC incomplete. Get token first (Returning user flow), then resume KYC. |
   | false    | false       | Brand new user. Present **Onboarding paths** and let them pick. |

**Step 2 — Handle stale token:**
If `agent-pay agent` returns exit code 2 (auth error), delete the stored token and restart from Step 1:
```bash
rm -f ~/.config/cypher-pay/token
```

### Returning user flow

User is enrolled but has no local token. Get one via OTP:
```bash
agent-pay request-token <email>
```
Tell user: "Check your email for a verification code."
```bash
agent-pay verify-otp <email> <otp>
```
Token is stored automatically by the CLI. No manual persistence needed.
If `kycComplete` was false, continue to KYC steps in Path B below.

## Onboarding paths

First-run only (enrolled=false). Present BOTH options — do not pick for the user:

> First-time setup — pick one:
> **A) Web signup** — sign up at https://agentpay.cypherhq.io in your browser. Easiest option.
> **B) Right here** — I'll walk you through it step by step. You'll only need your browser once for identity verification.

### Path A — Webapp onboarding

1. Tell user: "Open **https://agentpay.cypherhq.io** and complete signup + identity verification."
2. Once done, user returns and the agent runs the **Returning user flow** (request-token → verify-otp) to authenticate locally.
3. Verify with `agent-pay agent`.

### Path B — Native (CLI) onboarding

All commands run by you. User provides info conversationally — never show them raw commands or JSON.

**B1. Send OTP:**
```bash
agent-pay request-token <email>
```
Tell user: "I've sent a verification code to your email."

**B2. Verify OTP:**
Ask user for the code they received.
```bash
agent-pay verify-otp <email> <code>
```
Token is stored automatically by the CLI.

**B3. Submit KYC application:**
Collect from user conversationally: first name, last name, phone, date of birth, address (line1, city, state, country, postal code). Then:
```bash
agent-pay submit-application \
  --firstName "Alice" --lastName "Smith" \
  --email "alice@example.com" --phone "+14155551234" \
  --dob "1990-01-15" \
  --line1 "123 Main St" --city "San Francisco" \
  --state "CA" --country "US" --postalCode "94105"
```
If response contains `kycUrl` → tell user: "Open this link to complete identity verification: <kycUrl>"
If `kycAlreadyComplete` is true → skip to B4.

**B4. Wait for KYC approval:**
```bash
agent-pay kyc-status
```
Poll this every 15–30 seconds. When status indicates approval, confirm to user: "You're all set."

**B5. Verify:**
```bash
agent-pay agent
```

Both paths produce same result. Subsequent invocations skip onboarding entirely (Step 1 finds stored token).

## Card mode selection

After onboarding completes (first run only), ask the user which card mode they prefer:

> How would you like cards handled for purchases?
> **A) Single-use cards** (recommended) — a new card is created for each purchase and destroyed afterward. More secure: each purchase is isolated, card details can't be reused.
> **B) Reusable card** — one card is created and reused across purchases. Frozen between uses, unfrozen when needed. Simpler to manage if you make frequent purchases.

Persist the choice to `~/.config/cypher-pay/card-mode` (value: `single-use` or `reusable`). Default to `single-use` if user doesn't pick. On subsequent runs, read from file — don't re-ask.

## Purchase flow

This is the core loop. User wants to buy something → you handle payment.

**1. Check balance:**
```bash
agent-pay balance
```
Returns `$X.XX` (e.g. `$12.50`). If balance < purchase amount:
```bash
agent-pay fund <amountUsd>
```
Returns `{ "redirectUrl": "...", ... }`. Tell user: "Open this link to add funds: <redirectUrl>". Poll `agent-pay balance` until funds arrive.

### Mode A — Single-use cards

**2. Create card sized to purchase:**
```bash
agent-pay create-card --tag "purchase-$(date +%s)" --purpose "Buy headphones" --limit 50
```
- `--tag` must be unique per agent. Use timestamp or order ID.
- `--limit` = max per-transaction in USD. Set to expected charge amount.

Output shows tag, masked card number, and expiry.

**3. Get card details for checkout:**
```bash
agent-pay get-card --tag "purchase-$(date +%s)" --reveal
```
Returns full PAN/CVV/expiry. Use to fill checkout form silently.

To display the card to the user:
```bash
agent-pay get-card --tag "purchase-tag" --pretty
```
Shows an ASCII art card with masked PAN (last 4 only) and expiry. Show this to the user after card creation.

If user explicitly asks for full PAN or CVV:
```bash
agent-pay get-card --tag "purchase-tag" --reveal --pretty
```
Shows full PAN and CVV in the ASCII art card. Warn once: "Card details will be visible in your conversation history."

**SECURITY: Default output is masked — last 4 + expiry only. Full PAN/CVV only with `--reveal` when user explicitly asks. Use `--reveal` without `--pretty` to fill checkout forms, then discard.**

**4. Handle 3DS if triggered:**
```bash
agent-pay 3ds-poll <cardId> --timeout 30000
```
Two possible outcomes:
- `{ "approved": true, "requestId": "..." }` — 3DS auto-approved. No user action needed.
- `{ "approved": false, "requiresUserOtp": true, "message": "..." }` — 3DS OTP was sent to the user's email by the card provider. Tell the user: "A verification code was sent to your email for this purchase. Please enter it on the merchant's checkout page." The agent cannot approve this automatically — the user must complete it themselves in the browser.

**5. Wait for charge to land:**
```bash
agent-pay wait-for-txn <cardId> --timeout 30000
```
Polls until a transaction appears on the card. Do NOT cancel before this confirms — cancelling during an in-flight auth will decline the charge.

**6. Cancel card:**
```bash
agent-pay cancel-card <cardId>
```
Destroys the card. Frees the slot (max 5 active cards). If `wait-for-txn` times out with `settled: false`, freeze instead of cancel and tell user the charge may still be processing.

### Mode B — Reusable card

**2. Get or create the reusable card:**
Check for an existing reusable card first:
```bash
agent-pay list-cards
```
Look for a card with tag `reusable-default` (or whatever tag was used). If found and status is frozen/inactive → unfreeze it:
```bash
agent-pay get-card --tag "reusable-default"
# If status is inactive:
agent-pay unfreeze --tag "reusable-default"
```

If no reusable card exists, create one:
```bash
agent-pay create-card --tag "reusable-default" --purpose "Reusable purchase card" --limit 500
```

**3–4. Get card and 3DS:** Same as Mode A steps 3–4 (use `--tag "reusable-default"`).

**5. Wait for charge to land:**
```bash
agent-pay wait-for-txn <cardId> --timeout 30000
```

**6. Freeze card (do NOT cancel):**
```bash
agent-pay freeze <cardId>
```
Card stays in your active slots but is blocked from new charges until next purchase.

### Both modes — Report to user

Confirm purchase succeeded. Show last-4 digits of card if useful (from `get-card`). Never reveal PAN/CVV/expiry/token.

## Operations reference

All commands require `AGENT_PAY_TOKEN` in env unless noted. Output is human-readable by default; add `--json` to any command for machine-parseable JSON.

### Auth (no token required)
```bash
agent-pay auth-status <email>          # Check enrollment + KYC status
agent-pay request-token <email>        # Send OTP to email
agent-pay verify-otp <email> <otp>     # Verify OTP → get bot token
```

### Account
```bash
agent-pay agent                        # Get agent account info
agent-pay kyc-status                   # Check KYC status
agent-pay balance                      # Balance in USD cents
agent-pay fund <amountUsd>             # Get funding redirect URL
```

### Cards
```bash
agent-pay create-card --tag "x" [--purpose "..."] [--limit N] [--daily-limit N] [--monthly-limit N] [--reveal] [--pretty]
agent-pay get-card --tag "x"           # Card info (masked)
agent-pay get-card --tag "x" --reveal  # Full PAN/CVV/expiry — SENSITIVE
agent-pay get-card --tag "x" --pretty  # ASCII art card (masked)
agent-pay get-card --tag "x" --reveal --pretty  # ASCII art card (full PAN+CVV)
agent-pay freeze --tag "x"             # Deactivate card
agent-pay unfreeze --tag "x"           # Reactivate frozen card
agent-pay cancel-card --tag "x" [--reason "..."]  # Permanent, irreversible
agent-pay list-cards                   # Active cards (--all includes cancelled)
```

### Transactions & analytics
```bash
agent-pay wait-for-txn <cardId> [--timeout 30000] [--interval 3000]  # Poll until charge lands
agent-pay transactions                 # Cross-card transaction history
agent-pay spend-stats [--start "2025-01-01"] [--end "2025-01-31"]
```

### 3DS
```bash
agent-pay 3ds-poll <cardId> [--timeout 60000] [--interval 2000]
```

### Machine-readable schema
```bash
agent-pay --schema                     # Full JSON schema of all commands, flags, and outputs
```

## Default limits

- $500/transaction, $500/day, $5,000/month, max 5 cards per agent.
- Per-card limits set at creation (capped by agent-level rules).

## Error handling

| Exit code | Meaning |
|-----------|---------|
| 0         | Success — JSON on stdout |
| 1         | Usage error (bad command, missing flag) — message on stderr |
| 2         | API error (auth failure, server error) — message on stderr |

On exit code 2 with auth message → token may be stale. Delete `~/.config/cypher-pay/token` and re-auth.

## Security rules

1. **Card details display**: Show last 4 of PAN and expiry by default. Expiry is low-risk — show freely. If user explicitly asks for full PAN or CVV, display them but warn once: "Heads up — card details will be visible in your conversation history." Never display full PAN or CVV unprompted — they are used silently for checkout.
2. **Always dispose of cards after use** — single-use mode: wait for charge, then cancel. Reusable mode: freeze. Either way, never leave a card active and idle.
3. **Token prefix**: must start with `agt_`
4. **Token storage**: handled automatically by CLI. Never echo token values in conversation — the agent should not read, display, or manipulate token strings.
5. **Rotate tokens** before 90-day expiry via [agentpay.cypherhq.io](https://agentpay.cypherhq.io)

## SDK Reference (for programmatic consumers)

The CLI wraps the `@cypherhq/agent-pay` TypeScript SDK. Developers building custom integrations can use the SDK directly:

```bash
npm install @cypherhq/agent-pay
```

```typescript
import { createClient } from '@cypherhq/agent-pay';
const ap = createClient(); // reads AGENT_PAY_TOKEN from env
```

Key exports: `createClient`, `parseExpiry`, `AgentPayAuthError`, `AgentPayApiError`.
Full SDK documentation: see the package README or `agent-pay --schema` for the complete API surface.

Environment variables:
- `AGENT_PAY_TOKEN` — bot token (required, must start with `agt_`)
- `AGENT_PAY_BASE_URL` — API base URL (optional, defaults to production)
