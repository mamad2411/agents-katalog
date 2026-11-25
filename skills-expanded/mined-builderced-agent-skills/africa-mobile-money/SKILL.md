---
name: africa-mobile-money
description: Integrate M-Pesa, Orange Money, Wave, and MTN MoMo payment APIs with proper error handling, reconciliation, and multi-operator patterns.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: africa
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [africa]
priority: medium
dependencies:
  mcp: []
  skills: []
  apis: [mpesa-daraja, orange-money, wave, mtn-momo]
  data: []
update_sources:
  - url: "https://developer.safaricom.co.ke"
    check_frequency: "quarterly"
    last_checked: "2026-04-17"
license: MIT
---

# Africa Mobile Money Integration

> **DISCLAIMER**: This skill provides integration patterns only. It does not constitute financial advice. Payment processing is regulated — verify compliance with local financial authorities in each market.

## When to Use

- Accepting payments from African mobile money users
- Building multi-operator payment flows
- Implementing reconciliation for mobile money transactions
- Designing payment UX for feature phones (USSD) and smartphones

## Supported Operators

| Operator | Markets | API | Auth |
|----------|---------|-----|------|
| M-Pesa (Safaricom) | Kenya, Tanzania, DRC, Mozambique | Daraja 2.0 | OAuth2 |
| Orange Money | Senegal, Mali, Cote d'Ivoire, Cameroon, 10+ | OMAPI | API Key |
| Wave | Senegal, Cote d'Ivoire, Mali, Uganda | REST | API Key |
| MTN MoMo | Ghana, Uganda, Rwanda, Cameroon, 10+ | Open API | OAuth2 + Subscription Key |

## Common Payment Flow

```
1. Customer initiates payment (app, USSD, or web)
2. Your server calls operator API (STK Push / Payment Request)
3. Customer receives prompt on phone → enters PIN
4. Operator processes → sends callback to your server
5. Your server verifies callback signature
6. Update order status + send confirmation
```

## Key Patterns

### Multi-Operator Detection
Detect operator from phone number prefix:
```
Kenya:
  07XX, 01XX → Safaricom (M-Pesa)
  0720-0729  → Safaricom
  0733-0739  → Safaricom

Senegal:
  77X → Orange Money
  78X → Wave
  76X → Free Money
```

### Idempotency
Mobile money callbacks can arrive multiple times. Always:
- Use a unique transaction ID per request
- Check if transaction already processed before updating state
- Store callback raw payload for reconciliation

### Timeout Handling
Mobile money transactions have long confirmation times:
- M-Pesa STK Push: up to 60s for customer PIN entry
- Orange Money: up to 120s
- Design for: pending → success/failed/expired states
- Never assume failure on timeout — always check status API

### Reconciliation
Daily reconciliation is critical:
1. Fetch transaction report from operator API (daily)
2. Compare with your local records
3. Flag mismatches: received but not recorded, recorded but not received
4. Investigate and resolve within 24h

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Insufficient balance | Customer lacks funds | Show clear message, suggest lower amount |
| Wrong PIN | Customer entered wrong PIN | Allow retry (max 3) |
| Timeout | Customer didn't respond | Check status API, don't retry automatically |
| Duplicate | Same transaction sent twice | Return existing result (idempotent) |
| System unavailable | Operator maintenance | Queue and retry with exponential backoff |

## Security

- **Never log full phone numbers** (PII) — mask middle digits
- **Verify callback source** — check IP whitelist or signature
- **Use HTTPS** for all API calls
- **Store API keys** in environment variables, never in code
- **Amount validation** — server-side, never trust client

## What This Skill Does NOT Do

- Does not handle operator onboarding/KYC (business process)
- Does not manage currency conversion (use forex APIs)
- Does not implement USSD menus (see `africa-ussd-development`)
- Does not handle regulatory compliance per country (varies widely)
