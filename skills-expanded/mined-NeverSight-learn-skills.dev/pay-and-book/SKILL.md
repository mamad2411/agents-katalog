---
name: pay-and-book
description: >
  End-to-end hotel booking with USDC wallet payment. Use when the user wants
  the agent to search, book, and pay for a hotel in one autonomous flow —
  phrases like "book me a hotel in Tokyo and pay with USDC", "find a place in
  Paris and pay from my wallet", "handle the whole booking for next week".
  Orchestrates: search → select → authenticate wallet → fund if needed → pay
  via x402 → confirm. Do NOT use for search-only, payment-only, or non-hotel
  bookings.
license: MIT
---

# pay-and-book

End-to-end orchestration skill that combines hotel search and on-chain payment into a single flow. This is a **meta-skill** — it doesn't run any commands itself but coordinates the other skills in the right order.

## When to use

Use this skill when the user wants the entire booking handled in one shot:

- "Book me a hotel in Tokyo for next weekend, pay with USDC"
- "Find a 4-star place in Paris May 1–5 and book it from my wallet"
- "I need a hotel near Shibuya for 3 nights, handle the whole thing"

Use the **individual** skills (`search-hotel`, `book-hotel`, etc.) when the user clearly wants step-by-step control.

## The full flow

Execute these steps in order. Skip a step only if its precondition is already met.

### Step 1: Search hotels

Use the `search-hotel` skill. Present the top results to the user and ask which one they want. **Do not pick for them.**

### Step 2: (Optional) Show room options

If the user wants to see different rate plans for one specific hotel, use the `search-room` skill. Otherwise the default `packageId` from search-hotel is fine.

### Step 3: Confirm wallet is ready

Before authentication, check current state:

```bash
npx awal@latest balance
```

Three cases:

- **No auth** → Run `authenticate-wallet` skill (from `coinbase/agentic-wallet-skills`). Ask the user for their email; awal sends an OTP.
- **Authenticated but USDC < booking total** → Run `fund` skill. Calculate the shortfall (`booking_total - current_balance + small buffer`) and tell the user how much to fund.
- **Authenticated with sufficient USDC** → Skip to Step 4.

### Step 4: Final confirmation + book

Use the `book-hotel` skill. It handles the x402 payment and confirmation.

### Step 5: Summarize

Give the user a clean recap with booking ID, total paid (USDC), tx hash, and cancellation deadline.

## Decision tree

```
User asks to book a hotel autonomously
  │
  ├─ Has destination + dates?
  │    No → ask once, gather both
  │    Yes ↓
  │
  ├─ search-hotel skill → present results
  │
  ├─ User picked a hotel?
  │    No → wait for choice
  │    Yes ↓
  │
  ├─ User wants to see other rate plans?
  │    Yes → search-room skill
  │    No ↓ (use default packageId)
  │
  ├─ Wallet authenticated?
  │    No → authenticate-wallet skill
  │    Yes ↓
  │
  ├─ USDC balance >= total + 5%?
  │    No → fund skill
  │    Yes ↓
  │
  ├─ User confirmed total + guest details?
  │    No → ask for guest details, summarize, confirm
  │    Yes ↓
  │
  └─ book-hotel skill (x402 pay) → confirm + recap
```

## Example session

```
User: Find me a hotel in Tokyo May 1-5 and book it with USDC

Agent: [search-hotel skill]
  → Presents 5 hotels

User: Book the Park Hyatt

Agent: [check wallet] → not authenticated
  → "Need to log in first. What email?"

User: me@example.com

Agent: [authenticate-wallet skill] → email OTP
User: OTP code is 123456
Agent: [authenticate-wallet completes]
  → "Logged in. Wallet balance: 0 USDC."
  → "You'll need 1,800 USDC for this booking. Want to fund the wallet?"

User: Yes, fund 2000

Agent: [fund skill] → onramp link
  → User completes onramp
  → "Wallet now has 2000 USDC."
  → "Ready to book Park Hyatt Tokyo, May 1-5, 1,800 USDC.
     What name/email for the guest?"

User: Nguyen Van A, guest@example.com

Agent: → "Booking summary: ... Confirm? (yes/no)"
User: yes
Agent: [book-hotel skill — awal x402 pay]
  → "✅ Booked! BK_2026_05_001, paid 1,800 USDC, tx 0xabc..."
```

## Critical rules

- **Never skip the user choice steps.** Even if the search returns one obvious result, show it to the user and wait for confirmation.
- **Never auto-fund.** Always ask before triggering the `fund` skill — funding involves an external payment from the user.
- **Never auto-pay.** The final `book-hotel` step always shows a summary and waits for explicit yes.
- **Stop and ask** if anything is unclear: dates, occupancy, hotel choice, guest details, fund amount.
- The user can interrupt at any step ("actually, show me different dates"). Restart the relevant earlier step.

## Skills referenced (must be installed)

| Skill | Source | Purpose |
| --- | --- | --- |
| `search-hotel` | this package | Find hotels |
| `search-room` | this package | (optional) See rate plans |
| `book-hotel` | this package | x402 payment + booking |
| `authenticate-wallet` | `coinbase/agentic-wallet-skills` | Email OTP login |
| `fund` | `coinbase/agentic-wallet-skills` | Top up USDC via Coinbase Onramp |

If any of the Coinbase skills aren't installed, tell the user:

> This flow needs Coinbase wallet skills too. Install them with:
> ```
> npx skills add coinbase/agentic-wallet-skills
> ```
