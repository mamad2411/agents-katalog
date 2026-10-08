---
name: pest-feature-test
description: PulseDesk's Pest feature-test pattern — auth setup, happy path, role denial, and the mandatory cross-tenant 404. Every endpoint PR includes these.
---

# Pest Feature Test (pattern)

## Setup
- `RefreshDatabase`. Build orgs/users via factories. Authenticate with Sanctum: `actingAs($user)`.

## Always cover
1. **Happy path** — authorized user gets the expected 2xx + payload shape.
2. **Auth** — unauthenticated → 401.
3. **Role** — wrong role → 403.
4. **Cross-tenant 404** — user in Org B hits Org A's resource → 404. (the security gate)

## Style
- One behavior per test; assert status AND body where it matters (`assertJsonPath`).
- Name tests by behavior: `it('returns 404 when ticket belongs to another org')`.

## Run `php artisan test` (or `vendor/bin/pest`) green BEFORE opening the PR.
