---
name: add-provider
description: Step-by-step recipe for adding or modifying an OpenSDR provider client (src/providers/*.ts) behind the capability interfaces, including registry wiring, error mapping, cost estimates, demo fixtures and contract tests. Use when implementing Apollo/Hunter/Exa/Tavily/Instantly/HubSpot or any new data source, sequencer, or CRM.
---

# Add a provider

## 0. Prerequisite
Run the `verify-provider-api` skill first. `docs/providers/<name>.md` must exist and be current.

## 1. Pick capabilities
Implement only the interfaces from `src/providers/types.ts` (plan §9.1) that the provider truly supports: `PeopleSearchProvider`, `CompanySearchProvider`, `PersonEnrichProvider`, `CompanyEnrichProvider`, `EmailFinderProvider`, `EmailVerifierProvider`, `WebSignalsProvider`, `CampaignSender`, `CrmProvider`.

If you need a capability that doesn't exist, **stop**. Adding an interface changes plan §9.1 and needs the user's agreement.

## 2. Implement `src/providers/<name>.ts`
```ts
export function create<Name>Provider(deps: { http: HttpClient; apiKey: string; logger: Logger }): <Interfaces> { ... }
```
- All HTTP goes through `deps.http.request({ provider: "<name>", ... })`. Never call `fetch` directly.
- Set `idempotent: false` on any request that creates resources (plan §9.2).
- Map the response → domain models from `src/types.ts`. Normalize domains (lowercase, no scheme, no `www.`) and emails (lowercase, trimmed). Set `sources: ["<name>"]`.
- Map provider-specific error bodies to `OpenSdrError` codes (plan §4.4). For example, a body saying "insufficient credits" → `QUOTA_EXCEEDED` even when the HTTP status is 200 or 422.
- Export a cost estimate per method (`COSTS = { matchPerson: 1, ... }`), with the source of the number noted in `docs/providers/<name>.md`.
- No store access and no MCP imports in provider files.

## 3. Wire the registry
- Add the env var to the config schema (`src/config.ts`) and to `.env.example`, `README.md` (configuration table) and plan §4.2.
- Register the provider in `src/providers/registry.ts` for its capabilities. If two providers share a capability, add a selection env var (like `OPENSDR_SIGNALS_PROVIDER`) and document its default.

## 4. Demo provider
Extend `src/providers/demo/` so the same capability returns deterministic, realistic fixture data using `.example` domains only.

## 5. Tests (`test/providers/<name>.test.ts`)
Minimum:
- Request shape: method, URL, auth header present, params mapped (assert on the intercepted request).
- Response mapping from a scrubbed fixture → expected domain object.
- Error mapping: 401, 403, 429 (with `Retry-After`), 5xx, and the provider-specific quota body.
- No retry on non-idempotent create calls.
- The secret never appears in a thrown error message.

## 6. Done checklist
- [ ] `docs/providers/<name>.md` is current
- [ ] Config, `.env.example`, README and plan §4.2 updated
- [ ] Registry wired, plus `sdr_provider_status` shows the provider and its capabilities
- [ ] Demo fixtures added
- [ ] Contract tests pass, and `npm run lint && npm run typecheck && npm test && npm run build` is green
