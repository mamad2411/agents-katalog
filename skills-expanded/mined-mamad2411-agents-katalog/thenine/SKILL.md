# [APPNAME] Cursor Rules

You are working on [APPNAME], a group-only dating app. Follow the architecture in `11-technical-architecture` and the product requirements in `00-strategy` through `10-appendices`.

## Do

1. Do use TypeScript for application code, shared contracts, scripts, and tests.
2. Do model Group as the unit of matching distribution.
3. Do require complete verified Groups before introductions.
4. Do route all dating inventory through Introduction objects.
5. Do make conversations group-owned.
6. Do create breakout conversations only after explicit mutual consent.
7. Do keep post-meetup interest private until mutual.
8. Do include safety actions in active group, chat, plan, and debrief flows.
9. Do derive push notifications from persisted domain events.
10. Do preserve the free distribution baseline when adding paid features.
11. Do keep payment entitlements additive and explicit.
12. Do store raw government ID and liveness artifacts only with the verification provider.
13. Do validate provider webhook signatures and idempotency.
14. Do persist state before publishing realtime events.
15. Do use domain event outbox for realtime, push, analytics, and worker side effects.
16. Do use group-scoped authorization guards for group resources.
17. Do add tests for group eligibility, debrief privacy, safety access, and paid matching guardrails.
18. Do update architecture docs when schema, API, event, provider, infra, or security behavior changes.
19. Do use privacy-safe notification copy by default.
20. Do write clear error codes matching `11-technical-architecture/03-api-spec.md`.
21. Do keep safety reports and evidence access restricted and audited.
22. Do design thin-city matching states honestly with no filler inventory.
23. Do keep raw matching scores internal and explain only allowed reason categories.
24. Do use expand-migrate-contract for production database changes.

## Don't

1. Don't create solo swipe, solo feed, or member discovery APIs.
2. Don't let a Member receive introductions outside a complete verified Group.
3. Don't make paid state a ranking feature.
4. Don't suppress free group distribution to sell upgrades.
5. Don't expose one-sided crush, friend, or both signals.
6. Don't publish incomplete or unverified Groups.
7. Don't store broad contact books or expose social graph relationships without explicit consent.
8. Don't broadcast held or rejected moderation content to recipients.
9. Don't create generic "come back" push notifications.
10. Don't put safety actions behind premium, delayed flows, or hidden screens.
11. Don't let realtime clients write durable chat or plan state directly.
12. Don't use provider SDK state as the only source of truth; mirror state through audited domain transitions.
13. Don't return report details that identify the reporter unless policy explicitly allows it.
14. Don't use exact member location for matching unless a documented consent and retention rule exists.
15. Don't add unfinished endpoints or fake provider integrations in production paths.
16. Don't change product terminology from Group, Introduction, Plan, Debrief, Breakout, or Vouch without updating docs.
17. Don't add non-TypeScript code to the application stack.
18. Don't make destructive migrations without an expand-migrate-contract plan.
19. Don't skip doc-version footers in documentation files.
20. Don't assume an API change is safe without updating OpenAPI narrative and tests.

## Architecture Patterns

- Controllers validate transport shape and delegate to domain services.
- Domain services enforce invariants and write transactional state.
- Repositories own database access and typed queries.
- Provider adapters translate third-party payloads into internal commands.
- Workers consume queues idempotently and write domain events for user-visible changes.
- Realtime uses Ably as transport only; PostgreSQL remains source of truth.
- Notification Service creates intents only from `domain_event_outbox` rows.
- Entitlement Service computes capabilities; matching receives only additive stack size metadata.
- Safety Service can pause group eligibility, disable chat, reconfirm plans, and hide reporters.

## File Structure

- Put mobile screens and components in `apps/mobile`.
- Put API modules in `apps/api/src/modules`.
- Put worker consumers in `apps/workers/src`.
- Put shared domain types in `packages/domain`.
- Put API contracts in `packages/api-contracts`.
- Put database schema and migrations in `packages/db`.
- Put infrastructure in `infra`.
- Keep architecture docs in `11-technical-architecture`.

## Doc-Update Triggers

Update architecture docs in the same change when modifying:

- Stack/provider decisions.
- Database schema, index, enum, or relationship.
- API path, auth, request, response, or error code.
- Realtime event, channel, payload, or guarantee.
- Matching eligibility, scoring, allocation, or cold-start behavior.
- Media, verification, moderation, push, payment, or entitlement integration.
- Security model or staff access.
- Infrastructure, queues, environments, or CI/CD.

---
<!-- doc-version: 1.0 -->
