---
name: payment-migrator
description: Plans and executes a migration from one payment provider to another without downtime. Establishes what cannot move (stored card tokens usually cannot), maps the two providers' event vocabularies, flags architectural differences such as a change of notification model or a move to a merchant of record, and sequences a coexistence period rather than an atomic switch. Powers /pagokit:migrate.
when_to_use: |
  - The user invokes /pagokit:migrate, or asks how to move from one provider to another
  - A provider is being wound down, or its fees or coverage no longer fit
allowed-tools: Read, Glob, Grep
---

# payment-migrator

There is no moment at which flipping every payment from one provider to another is safe. A
migration is a period during which both run, and the job is to make that period short,
observable and reversible.

## Step 1 — Inventory what exists

Read `PAGOKIT_INTEGRATION.md`, then verify it against the code; it goes stale. You need:

- Routed events and what each one does.
- Customers with a stored payment method, and how many.
- Active subscriptions and their next billing dates.
- Every place a provider id or provider-shaped identifier is persisted.

## Step 2 — Establish what cannot move

Say this before planning anything, because it determines whether the migration is a technical
task or a customer-facing event.

**Stored card tokens usually cannot migrate.** They belong to the provider that vaulted them.
Some providers support a PCI-scoped token export or a network-token migration on request;
most do not, and the ones that do require a written agreement between both parties. Until
that is confirmed in writing, plan for existing subscribers to re-enter a card — which is a
churn event, not a detail.

## Step 3 — Diff the two providers

Read both catalog entries and name every difference that changes the architecture:

| Compare | If it differs |
|---|---|
| `notification_model` | Moving to `return_url_commit` or `ping_then_poll` is a different architecture, not a swapped SDK |
| `webhook.required_events_minimum` | Map them explicitly. Flag every event with no equivalent |
| `mor.is_mor` | A merchant of record becomes the seller. Invoices, tax handling and the statement descriptor all change |
| `methods` and their `reversibility` | New irreversible rails mean the refund path changes shape |
| `settlement.payout_delay_days` | Cash flow changes, and someone in finance needs to know |
| `recurring.rails` | Card-to-mandate is a different lifecycle entirely |
| `pci.scope` | Moving to a direct-API integration can push the merchant from SAQ A to SAQ D |

## Step 4 — Sequence the coexistence

1. Add the new provider alongside the old one. Both webhook routes live; they are namespaced
   already.
2. Route **new** payments to the new provider. Leave everything existing where it is.
3. Migrate subscriptions at their natural renewal, not in a batch. A batch migration turns one
   bad assumption into every customer's problem simultaneously.
4. Keep the old handler alive for as long as the old provider can still send disputes and
   refunds — months, not days.
5. Keep the `provider` column on every payment row permanently. Reconciliation needs it long
   after the old provider is gone.

## Step 5 — Write it down

`PAGOKIT_MIGRATION.md`: what moves when, what cannot move, what the customer sees, how to
tell whether it is working, and the rollback. A migration without a written rollback is a bet.

## Instrument it

Before the first payment routes to the new provider, make these observable: success rate by
provider, decline reasons by provider, webhook delivery failures, and time from checkout to
confirmed payment. A migration that quietly halves your approval rate looks exactly like a
successful one until the end of the month.

## Anti-patterns

- Do not switch atomically.
- Do not migrate and refactor in the same change. When it breaks you will not know which did it.
- Do not delete the old webhook handler when the last payment is created — disputes arrive weeks later.
- Do not promise that stored cards will migrate before both providers have confirmed it in writing.
- Do not migrate a subscription mid-cycle without deciding what happens to the unused portion.
