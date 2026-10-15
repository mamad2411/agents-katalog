---
name: bounded-backend
description: >-
  Author a Bounded backend: policy.json rules and invariants
  (rollingSum/conserve/tenantTag/bound), functions (ctx.user/ctx.bounded/ctx.ai/
  ctx.services/ctx.secrets), the actor and identity model (@user, runAs/actAs,
  @origin, service keys, reserved identity sets), data and queries, realtime/live
  rooms, and the proof loop (bounded verify, counterexamples, proof coverage). Use
  when writing or changing server-side Bounded logic, policies, or the rules that
  govern who can do what. Part of the Bounded skill family; see the bounded skill
  to route across frontend, deploy, onchain, teams, and observe.
---

# Bounded backend

The server side of a Bounded app: the policy that governs every write, the
invariants that are proven at deploy and enforced at runtime, the functions that
run trusted code, and the actor model that decides who is acting. The proof loop
is `bounded verify`; `bounded deploy` compiles and pushes; runtime rule and
invariant checks fail closed. For CLI/deploy see the **bounded-deploy** skill; for
the client SDK and auth UI see **bounded-frontend**; to route across the family,
see the root **bounded** skill.

Write the actor model in mind from the start: know who `@user` is, which principal
a function acts as (`runAs`/`actAs`), and where authorization comes from
(`@origin`) before you write a rule.

## Task Router

| User task | Read |
|---|---|
| Generate or repair a policy from an app description | [docs/policy-generation-guide.md](docs/policy-generation-guide.md) |
| See complete policy examples | [docs/policy-examples.md](docs/policy-examples.md) |
| Rules, field types, expressions, `get()`, `getAfter()` | [docs/policy-reference.md](docs/policy-reference.md) |
| Add spending/rate caps | [docs/invariants.md](docs/invariants.md#rollingsum--caps-over-time-windows) |
| Model balances, points, P&L, or supply | [docs/invariants.md](docs/invariants.md#conserve--sums-dont-change) |
| Tenant isolation | [docs/invariants.md](docs/invariants.md#tenanttag--documents-carry-their-tenant) |
| Hard field ceilings/floors, anti-cheat bounds | [docs/invariants.md](docs/invariants.md#bound--hard-ceilings--floors-on-a-field-anti-cheat) |
| Conditional ownership or holder transfer | [docs/policy-reference.md](docs/policy-reference.md#conditional-transfer-authority) |
| Constants, reusable rule fragments, `@const`, `@def` | [docs/constants-and-defs.md](docs/constants-and-defs.md) |
| Decide rule vs invariant vs hook vs function | [docs/functions-when-to-use.md](docs/functions-when-to-use.md) |
| Functions and external API calls | [docs/functions.md](docs/functions.md) |
| Start simple, graduate to functions | [docs/functions-graduation.md](docs/functions-graduation.md) |
| Give backend code user-owned API keys | [docs/secrets.md](docs/secrets.md) |
| Scheduled functions or in-boundary scheduled hooks | [docs/hooks-scheduled-webhooks.md](docs/hooks-scheduled-webhooks.md) |
| What anti-cheat can and cannot prove | [docs/hooks-and-anti-cheat.md](docs/hooks-and-anti-cheat.md) |
| Data-plane read/write semantics and atomic batches | [docs/data-plane.md](docs/data-plane.md) |
| Queries, pagination, aggregates | [docs/queries.md](docs/queries.md) |
| Files and search | [docs/files-and-search.md](docs/files-and-search.md) |
| Realtime rooms and games | [docs/realtime-and-games.md](docs/realtime-and-games.md) |
| Native live modules and live status | [docs/live-runtime.md](docs/live-runtime.md) |
| Realtime game feel: input cadence, interpolation, prediction | [docs/realtime-netcode.md](docs/realtime-netcode.md) |
| AI NPCs / AI players | [docs/ai-npcs.md](docs/ai-npcs.md) |
| Long-running backend runtime | [docs/backend-runtime.md](docs/backend-runtime.md) |
| Multi-step Flue agents | [docs/agents-flue.md](docs/agents-flue.md) |
| Roles, owners, collaborators, scoped admins | [docs/admin-and-ownership.md](docs/admin-and-ownership.md) |
| Top-level roles and read/write scopes | [docs/roles.md](docs/roles.md) |
| `access` block, custom roles, external access, platform super-admins | [docs/access-control.md](docs/access-control.md) |
| Manager/owner/collaborator identity sets or function log access | [docs/identity-and-logs.md](docs/identity-and-logs.md) |
| Service keys / backend identities, payout bots | [docs/service-keys.md](docs/service-keys.md) |
| Who the actor is on a live call: `runAs`, `actAs`, `@origin` | [docs/principals-and-origins.md](docs/principals-and-origins.md) |
| Proof coverage and counterexamples | [docs/proof-coverage.md](docs/proof-coverage.md) · [docs/verify-and-counterexamples.md](docs/verify-and-counterexamples.md) |
| End-to-end tests for authed apps | [docs/testing-authed-apps.md](docs/testing-authed-apps.md) |
| Quality checklist before calling the app done | [docs/quality-checklist.md](docs/quality-checklist.md) |
| Build for agents or a backend-only app | [docs/building-for-agents.md](docs/building-for-agents.md) · [docs/building-a-backend.md](docs/building-a-backend.md) |

## Term Router

| If you see | Read |
|---|---|
| `rollingSum`, `windowSeconds`, `scopeVariable`, `conserve`, `bound`, `tenantTag`, `tenantEdge` | [docs/invariants.md](docs/invariants.md) |
| `@user`, `@data`, `@newData`, `@time`, `get()`, `getAfter()` | [docs/policy-reference.md](docs/policy-reference.md) |
| `transferAuthority`, one-click market trade, holder transfer | [docs/policy-reference.md](docs/policy-reference.md#conditional-transfer-authority) |
| `@const`, `@def`, deploy constants | [docs/constants-and-defs.md](docs/constants-and-defs.md) |
| `functions`, `ctx.user`, `ctx.bounded`, `ctx.env`, `ctx.secrets` | [docs/functions.md](docs/functions.md) |
| `ctx.ai.run`, AI NPC | [docs/functions.md](docs/functions.md#ctxai--real-ai-no-api-keys) · [docs/ai-npcs.md](docs/ai-npcs.md) |
| `ctx.services`, managed services, third-party API proxy | [docs/functions.md](docs/functions.md#ctxservices--managed-api-discovery-and-invoke) · [docs/backend-runtime.md](docs/backend-runtime.md) |
| `actAs`, `runAs`, service key, payout bot, backend identity | [docs/service-keys.md](docs/service-keys.md) · [docs/principals-and-origins.md](docs/principals-and-origins.md) |
| `@origin`, `ctx.origin`, live call provenance | [docs/principals-and-origins.md](docs/principals-and-origins.md) |
| `roles`, `members`, `read:"*"`, scoped admin | [docs/roles.md](docs/roles.md) |
| `__owners__`, `__admins__`, `__developers__`, `__viewers__` role sets in policy | [docs/access-control.md](docs/access-control.md) · [docs/identity-and-logs.md](docs/identity-and-logs.md) |
| `session.live`, `init`, `tick`, `views`, `@effect`, `live.intent` | [docs/live-runtime.md](docs/live-runtime.md) |
| `session.tick`, `settleTo`, `settleFrom`, fog-of-war views | [docs/realtime-and-games.md](docs/realtime-and-games.md) |
| `schedule`, `dueRows`, `hooks.scheduled`, `webhooks`, `verifyWebhook` | [docs/hooks-scheduled-webhooks.md](docs/hooks-scheduled-webhooks.md) |
| `getPage`, `queryAggregate`, `count`, filters, sort, cursor | [docs/queries.md](docs/queries.md) |
| `setFile`, storage collection, full-text search | [docs/files-and-search.md](docs/files-and-search.md) |

## Error Router

| Error/status | Meaning |
|---|---|
| `403` | A write or function invoke failed a rule. Check auth, ownership, roles, or function `auth`. Denied reads are hidden as `200` with empty data, not `403`. |
| `409` + invariant name | The transaction would violate an invariant. Fix state or policy. |
| `DISPROVED` + counterexample | The proof found a breaking assignment. Read it, strengthen the policy, and verify again unless the user explicitly accepts the risk. |
| Static validation error | Fix policy syntax, field types, tier/invariant pairing, constants, or expression use. |

## Rules Of Thumb

- Use `@user.id` for normal ownership and membership checks; `@user.address` only for wallet/onchain semantics.
- Denied reads return empty `200` responses. Test read denial with a different permitted identity, not by waiting for a read `403`.
- Use `conserve` for money-like values; `rollingSum` for caps over time; one atomic `set-many` when correctness spans multiple writes.
- Put provider API keys in Bounded secrets, not frontend code.
- Know the acting principal before writing a rule: a function's `runAs`/`actAs` and `@origin` decide who `@user` is and whether the call is authorized.
