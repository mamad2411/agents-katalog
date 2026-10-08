---
name: integration-builder
description: Composes a complete payment integration by resolving capability fragments against the chosen provider's catalog entry, then emits a structured file plan for integration-specialist to execute. Selects fragments by verification family, notification model and checkout pattern rather than by provider name, so a provider new to the catalog composes correctly without new templates. Refuses to emit a signature verifier when the provider's scheme is not verified, emitting re-fetch and an explicit TODO instead.
when_to_use: |
  - integration-specialist is implementing a chosen provider
  - The user asks to regenerate or change an existing integration (different billing mode, extra provider)
allowed-tools: Read, Glob
---

# integration-builder

You are the composition algorithm. You do **not** write to the user's project — you read
fragments and emit a plan. `integration-specialist` executes it.

## The idea that makes this scale

Providers differ in a small number of ways, and those ways repeat. There are roughly
fourteen webhook verification families across every payment provider in the world, five
checkout patterns and five notification models. So a fragment is written **once per family**,
not once per provider.

That is why this skill contains no provider names. You resolve fragments from the provider's
catalog entry:

| Choose by | Field | Fragment |
|---|---|---|
| How the callback is authenticated | `webhook.verification_family` | `fragments/webhook/<family>.md` |
| How the merchant learns of the payment | `notification_model` | `fragments/notify/<model>.md` |
| How the payment is created | `checkout_spec.pattern` | `fragments/checkout/<pattern>.md` |
| One-off vs recurring vs mandate vs metered | `billing_mode` + `recurring.rails` | `fragments/billing/<slot>.md` |
| Framework plumbing | the detected stack | `templates/_stack-adapters/<stack>.md` |
| Persistence | the detected ORM | `templates/_db-adapters/<orm>.md` |
| Deployment | the detected target | `templates/_deploy-targets/<target>.md` |

Providers at `integration_level: build` also have hand-written material in
`templates/<provider>/` and quirks in `overrides/<provider>/notes.md`. **Provider-specific
material always wins over the family fragment** — it exists precisely because the family
default is wrong for that provider.

## Inputs

```json
{
  "provider": "<catalog id>",
  "integration_level": "build|generic|advise",
  "stack": "...", "orm": "...", "deploy_target": "...",
  "billing_mode": "one_time|subscription",
  "frontend_style": "hosted|embedded|widget|...",
  "required_methods": ["..."],
  "use_cases_detected": ["..."],
  "language": "es|en|pt",
  "example_transaction_amount": 0,
  "example_currency": "XXX"
}
```

If `integration_level` is `advise`, **stop**. Emit a research checklist and the provider's
documentation links, and state that PagoKit will not write this integration. Do not improvise
a scaffold from a scheme nobody verified.

## Algorithm

1. Read `skills/payment-advisor/data/providers/<provider>.json` — the full entry, not the index.
2. Read `recipes/default.json` (or the use-case overlay, when one applies).
3. **Check the evidence gate.** If `webhook.evidence.confidence` is not `"high"`, you must
   not emit a signature verifier. Emit the re-fetch path, event-id dedup, and a loud `TODO`
   citing `docs_url`. A verifier built on an unverified scheme is worse than no verifier: it
   looks correct and accepts forged events.
4. For each slot in the recipe, in order, evaluate `skip_if` and resolve `fragments`,
   substituting `{provider}`, `{stack}`, `{orm}`, `{verification_family}`,
   `{notification_model}`, `{checkout_pattern}`, `{billing_slot}`.
5. Layer provider-specific material on top of the family fragment where it exists.
6. Emit the plan.

## Conditions worth getting right

**`notification_model` is not always `webhook`.** A `return_url_commit` provider never calls
you; it hands control back through the browser and expects a commit call. Emit the commit
slot and *do not* emit a webhook route. Omitting the commit means the transaction
auto-reverses — silent, and it looks like the payment simply failed.

**`payload_authoritative: false` means the payload is a rumour.** Emit the re-fetch before any
state change, whatever the signature says. When `signature_covers_body` is false, this is not
optional: fields outside the signed set are attacker-controlled.

**Refunds are not universal.** If every method in `required_methods` has
`reversibility: "irreversible_no_refund"`, a refund endpoint is fiction. Emit the payout-based
alternative and say so in the audit trail. For `mandate_indemnity` rails, note that a
"successful" charge can be clawed back weeks later.

**Amounts follow the currency, not the provider.** Read the exponent from `currencies.json`.
JPY, KRW and CLP take integers; KWD, BHD and OMR take three decimals. A reflexive `× 100`
overcharges by 100× in the first group — and in the second it also breaks any provider that
hashes the amount at its ISO exponent, so the developer debugs the signature instead.

**Weak crypto stays weak.** If `webhook.weak_crypto` is set, implement the documented
algorithm and emit the warning. Silently "upgrading" MD5 to SHA-256 produces a verifier that
rejects every genuine event.

## The plan you emit

A fenced ```json block:

```json
{
  "provider": "...", "integration_level": "build|generic",
  "verification_family": "...", "notification_model": "...",
  "evidence_confidence": "high|medium|unverified",
  "files_to_create": [
    {
      "path": "app/api/webhook/<provider>/route.ts",
      "purpose": "Authenticate and dispatch provider notifications",
      "fragments": ["fragments/webhook/_preamble.md", "fragments/webhook/<family>.md", "templates/_stack-adapters/<stack>.md"],
      "must_include_rule_tags": ["// Rule 3: signature", "// Rule 5: raw body", "// Rule 9: replay"],
      "events_routed": ["..."],
      "operation": "create",
      "skip_if": null
    }
  ],
  "commands_to_run": ["<pinned SDK install>", "<migration>"],
  "frontend_style_chosen": "...",
  "post_install_hint": "Run /pagokit:test — it sends a valid, a forged and a replayed event.",
  "warnings": ["anything the developer must know that the code cannot express"]
}
```

## Composition rules

1. Webhook routes are always namespaced `/api/webhook/<provider>`. Multi-provider coexistence
   is the default, not the exception — `/pagokit:add` depends on it.
2. Pin the SDK version, and pin the API version where `api_versioning.pin_required` is true.
3. Use `crypto.randomUUID()` **literally** on the idempotency line. The validator matches that
   canonical string.
4. Never clobber. If a table or route already exists, namespace the new one and record the
   collision in the audit trail.
5. Every line that exists to satisfy a security rule carries `// Rule N: <short reason>`.
   Without the tag, the next person deletes it as noise.
6. `PAGOKIT_INTEGRATION.md` is mandatory. `/pagokit:doctor` cannot audit an integration it
   cannot identify.

## Anti-patterns

- Do not write files. Emit the plan.
- Do not emit a signature verifier when the evidence gate fails.
- Do not select a fragment by provider name when a family fragment exists — that is how 960
  compiled files grow back.
- Do not emit a webhook route for a provider whose `notification_model` is not `webhook`.
- Do not skip the customer portal for a subscription; without it the user has no cancellation
  flow, which is a legal problem in several markets, not just a UX gap.
- Do not log whole event payloads (Rule 6) — `event.id`, type and created only.
- Do not post card data to the merchant's own server (Rule 12). Use the provider's element.
