---
name: bounded
description: >-
  Build and use Bounded (bounded.sh), a provable realtime backend for apps. Start
  here for any Bounded task: this skill routes you to the right member of the
  Bounded skill family (backend/policy, frontend, deploy, onchain, teams, observe)
  and covers setup, billing, buckets, usage limits, and project config such as
  bounded.json and account profiles. Use whenever working with the Bounded CLI,
  policy.json, verify/deploy, functions, auth, realtime, payments, or invariants.
---

# Bounded

Bounded is a provable realtime backend for apps. The public workflow is:

```text
describe app -> generate policy.json -> bounded verify -> fix/accept proof results -> bounded deploy -> use via SDK/CLI
```

`bounded verify` is the proof loop. `bounded deploy` validates, compiles, and
pushes the policy. Runtime rule and invariant checks fail closed.

This is the **root** of the Bounded skill family. It routes to the focused
sibling skills below and covers the cross-cutting basics (setup, billing). Each
sibling carries its own task and term routers over its docs.

## Who you are

You are a coding agent (Claude Code, Codex, or similar) operating Bounded **on the
user's behalf**: you author `policy.json`, run `bounded verify`/`deploy`, write
functions and frontends, and call the SDK/CLI for them. Default to *doing* the work
end-to-end, not just explaining it. The user may be non-technical; keep their app
working and the defaults safe without making them think about ids, keys, or proofs
unless they ask.

## Which skill

Pick the sibling skill for the task; load one, do the work, avoid unrelated context.

| The task is about | Skill |
|---|---|
| Policy rules, invariants (rollingSum/conserve/tenantTag/bound), functions, data/queries, realtime/live, the actor & identity model (`@user`, runAs/actAs, `@origin`, roles, service keys), proofs & counterexamples | **bounded-backend** |
| The client: `@bounded-sh/client` SDK, hosted frontend, end-user auth UI (email OTP, OAuth, guest) | **bounded-frontend** |
| Shipping & config: the CLI, environments, live-edit, domains/slugs, `bounded.json`, accounts, sharing access | **bounded-deploy** |
| Wallets, tokens, on-chain transactions, crypto & card payments (Bounded Pay) | **bounded-onchain** |
| Org/team governance: org-wide observe, enforcement, custody, and invariants shown on a shared team view | **bounded-teams** |
| Turning observe on for one app; watching its actions, decisions, and action boundaries | **bounded-observe** |

Install the whole family with `npx skills add bounded-sh/skill --all`.

## Public Boundary

This skill is for Bounded users and app builders. Keep guidance user-facing:

- Explain product behavior, public CLI/SDK commands, public pricing, usage limits,
  app design patterns, and compliance responsibilities. Stay within the public
  product surface; do not invent non-public details or unpublished pricing.
- For Bounded-managed third-party service proxies, state the public rule: provider
  cost plus 5%, itemized. Users can opt out by integrating a provider directly with
  their own API keys.
- For Bounded Pay, the 1% platform fee is in addition to Stripe's own processing fees.
- For SMS, WhatsApp, and email, Bounded Auth authenticates the user; it is not
  recipient consent. Use real provider integrations and comply with the channel's rules.

## Cross-cutting docs

| Topic | Read |
|---|---|
| Billing, buckets, plan limits, top-ups, upgrade | [docs/billing.md](docs/billing.md) |
| Per-app product analytics (traffic, web vitals, errors) | [docs/analytics.md](docs/analytics.md) |
| Observe/limit an agent's external actions (Action Boundaries) — pointer | [docs/observe.md](docs/observe.md) |
| Capability boundaries | [guides/capabilities-and-limits.md](guides/capabilities-and-limits.md) |

## Error Router

| Error/status | Meaning |
|---|---|
| `403` | A write or function invoke failed a rule (bounded-backend). Denied reads are hidden as `200` with empty data, not `403`. |
| `409` + invariant name | The transaction would violate an invariant (bounded-backend). |
| `declined` + boundary name | An escorted external action would cross an Enforced boundary, checked before the call fires (bounded-observe / bounded-teams). Read the named boundary; do not retry harder. |
| `429` + `dimension`/`projectedUsage` | A plan limit or spend cap would be exceeded. Explain the axis; suggest upgrade, top-up, cap change, or less volume ([docs/billing.md](docs/billing.md)). |
| `DISPROVED` + counterexample | The proof found a breaking assignment (bounded-backend). Strengthen the policy and verify again. |

## Billing Basics

Two user-visible buckets:

- **AI/external-services bucket**: AI (`ctx.ai`) and managed third-party service proxies (`ctx.services`).
- **Bounded infra bucket**: metered Bounded platform usage at public rates.

Free accounts include 3 AI builds per rolling day (fast model) plus a small
AI/external-services trial allowance for runtime services, but cannot top up
buckets. Pro-or-better accounts can top up eligible buckets. Both the relevant
bucket and any app-level cap must have room before cost-bearing work runs.

## Setup

```bash
curl -fsSL https://get.bounded.sh/install.sh | sh
bounded init
bounded deploy --create --name my-app
bounded verify
bounded dashboard
```

Wallet/keypair mode (`global`, `project`, `profile`, `env`) or web-account mode
(`bounded account use --web` then `bounded login`). Do not commit private keys or
secrets. Details in the **bounded-deploy** skill.

## Rules Of Thumb

- Read project config first when entering an existing app; it selects the app/environment/account source.
- Use `@user.id` for ownership and membership; `@user.address` only for wallet/onchain (bounded-onchain).
- Denied reads return empty `200` responses; test read denial with a different permitted identity.
- To give a person or agent access to an app, reach for `bounded share ... --role ...`; never search app code for an allowlist (bounded-deploy).
- Give users the clearest public command or URL; do not route them to non-public Bounded service surfaces.
