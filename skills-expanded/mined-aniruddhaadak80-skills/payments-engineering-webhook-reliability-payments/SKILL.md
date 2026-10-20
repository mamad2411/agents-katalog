---
name: payments-engineering-webhook-reliability-payments
description: "Idempotent handlers, signature checks, and replay safety for provider callbacks."
---
# Process payment webhooks reliably

> Idempotent handlers, signature checks, and replay safety for provider callbacks.

**Track:** 💰 Finance & Fintech · **Domain:** Payments Engineering · **Level:** intermediate · **~35 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Idempotent handlers, signature checks, and replay safety for provider callbacks.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Verify signatures first; reject before any parsing side effects
2. Persist raw event immediately, acknowledge fast, process async
3. Deduplicate on event ID; assume providers retry aggressively
4. Handle out-of-order events via state machine per payment object
5. Backfill job reconciles missed webhooks against provider API hourly
6. Alert on processing lag and dead-letter depth, not just failures

## Common Pitfalls

- Business logic inside webhook handler timing out mid-write
- Trusting event arrival order for status transitions

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-webhook-reliability-payments
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-webhook-reliability-payments -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills