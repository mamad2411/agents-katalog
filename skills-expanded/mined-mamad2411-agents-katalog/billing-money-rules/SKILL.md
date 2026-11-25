---
name: billing-money-rules
description: >-
  Use when creating or editing code under services/billing. Enforces Helpline's
  money-handling rules — integer cents only, seat limits, and BillingError for
  every violation.
paths: services/billing/**
---

# Billing money rules

This skill activates when work is happening in `services/billing`. It exists so
money bugs never ship.

## The rules (load these every time)

1. **Money is integer cents.** Never a float, never dollars. Variables and
   fields end in `_cents`.
2. **Plan economics live in one place** — `_SEAT_LIMITS` and
   `_PRICE_PER_SEAT_CENTS` in `subscriptions.py`. Never hard-code a price or a
   limit anywhere else.
3. **Every money/plan violation raises `BillingError`** (HTTP 402). Never
   silently clamp seats, skip a charge, or return a partial result.
4. **Inactive subscriptions cannot be invoiced.**

## When you need the detail

For the full rationale, edge cases, and worked examples, read
[references/money-conventions.md](references/money-conventions.md). Only load it
when a change is non-trivial — the four rules above cover most edits.
