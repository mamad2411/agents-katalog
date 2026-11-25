---
name: graphql-federation-offering
description: "Design how a platform lets outside partners and third-party apps contribute fields or data to its own public GraphQL graph - the extension ladder from app-owned custom fields and platform-run connectors up to partner-hosted subgraphs, what partner SDL may claim (@override, @requires), what the router forwards to a partner, blast radius, and offboarding. Use whenever the user mentions partner subgraphs, letting partner apps add fields to their schema, a partner-extensible supergraph, or stitching partner APIs into the graph they publish - even without saying federation. Not for consuming third-party APIs in your own client, or building an app on another platform. Do NOT use for a single-owner schema or internal federation - use samber/developer-platform-skills@public-graphql-api-design instead."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# GraphQL Federation Offering

You are a platform architect deciding how outside parties extend a public GraphQL graph. Federation tooling assumes every subgraph author is a trusted team of one organization; the moment a partner contributes, composition still validates the schema but no longer protects the platform.

No major public API platform verifiably composes raw partner-owned subgraphs into its production public graph. The ones that let partners extend the graph keep schema ownership: app-owned namespaced data, connectors the platform runs, operator-added remote schemas. Start from that fact, and treat "partners ship subgraphs into our supergraph" as the rung a team must earn, not the default.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. The file is an advisory reference, not a mandatory requirement. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.

## Interview

Ask before designing. Each answer deletes or re-ranks rungs in step 2.

1. What do partners need, in their words? Attach stored data to platform objects, show live data computed on their side, react to platform events, or add whole capabilities of their own.
2. How many partners, and how bound? A few under contract, or self-serve apps from anyone.
3. Who sees partner fields: every tenant, or only tenants that installed the partner and consented?
4. Which platform data would a partner need to compute its fields? Name the fields; flag personal or regulated data.
5. Current graph stack: single schema or federated, which router and registry, under which license?
6. Client latency SLA on the queries partner fields would join.
7. Date the first partner must go live, one-off integration or compounding program, and the effort ceiling: review staff, platform engineering weeks, appetite for running partner traffic.

If your harness has persistent memory, store the decisions so later runs (a new partner, a review, an offboarding) start from them:

- Chosen rung per partner need.
- Extendable-entity allowlist and data-clearance list per entity.
- Credential model toward partners.
- Per-partner timeout and circuit-breaker values.
- Visibility rule (all tenants or installing tenants).
- Offboarding notice period.

## Workflow

1. Classify the partner need.
2. Pick the rung on the extension ladder.
3. Write the partner contract: extendable entities, namespace, SDL policy.
4. Bound the data and credentials that reach the partner.
5. Bound the blast radius.
6. Decide who sees partner fields.
7. Run the lifecycle: publish, change, offboard.

Steps 3-7 apply in full to rungs 4-5. Rungs 0-2 keep partner code out of the request path. Rung 3 puts the partner's endpoint in it while the platform writes the schema: apply steps 4-7 and only the namespace rule of step 3.

When the request is a review of an existing or already-approved design (a config, an SDL, a launch checklist):

- Skip interview questions the artifacts already answer; state the assumptions you make for the rest.
- Open with the blockers, ordered by severity, each naming the step and failure mode it violates.
- Emit the step 2 ranking only for rungs step 1 left standing.
- Report an approved rung the ladder would not pick as a finding with its promotion condition, not as a blocker. Refuse only partner subgraphs in the first-party production supergraph.

## 1. Classify the partner need

Map interview answer 1 to one shape before looking at mechanisms. The shape deletes rungs; it never ranks them.

- **Stored data on platform objects** (a loyalty tier on a customer, a shipment ID on an order): rungs 1 and 2 cover it. Delete rungs 3-5.
- **Events** (partner reacts when an order ships): rung 0. Delete every graph rung.
- **Live data computed by the partner** (a real-time quote, a risk score from the partner's model): rungs 3-5.
- **New capabilities of the partner's own**, unrelated to platform objects: the partner runs its own API. The platform graph gains nothing by hosting it; stop and say so.

A request that mixes shapes splits into one design per shape. "Partners want to extend our graph" almost always turns out to be stored data plus events, which never needs a partner resolver.

## 2. The extension ladder

Six rungs. Each one higher puts more partner code, data flow and failure into the platform's request path.

| # | Rung | What the partner provides | Platform effort | Live partner data in one query | Security and compliance exposure | Durability |
| - | --- | --- | --- | --- | --- | --- |
| 0 | Webhooks plus API callback | Its own endpoint and API calls | `+++` near-zero beyond the webhook platform | `---` none | `+++` platform sends only event payloads | `+++` |
| 1 | App-owned extension data: namespaced custom fields and objects the platform stores | Definitions and values via API | `++` a storage and definitions API, once | `-` stored, not live | `++` data stays in platform storage under platform schema | `+++` |
| 2 | Platform-ingested connector into canonical types | A sync into platform object types | `+` per canonical type | `-` synced, not live | `++` same as rung 1 | `++` |
| 3 | Platform-operated connector or remote schema: the platform maps the partner's REST or GraphQL API under a partner namespace | An HTTP endpoint | `-` mapping work per partner | `+` live, platform-shaped | `-` platform calls out, controls headers and timeouts | `++` |
| 4 | Mediated extension field: one platform-owned field (`Order.extension(app: ID!)`) resolved through a platform proxy | A resolver endpoint behind a published contract | `--` proxy, contract, per-partner limits | `++` live, partner-shaped | `--` partner code in the request path | `+` |
| 5 | Partner subgraph in an isolated partner variant or router | A subgraph | `---` review staff, policy CI, separate router, isolation | `++` live, partner-shaped | `---` composition plus request path | `-` tied to the router's federation dialect |

Composing partner subgraphs into the first-party production supergraph is not a rung. Every partner failure, hijack and composition break would land on first-party traffic; rung 5 gives the same partner capability behind a boundary. Refuse it by name when asked.

Rung 4 has a hosted variant: the partner's function runs in a platform sandbox instead of on the partner's endpoint. It removes partner egress only when the sandbox has no outbound network; otherwise keep the data-clearance list, an egress allowlist approved per tenant, and the SSRF rules of step 5. Either way, cap CPU, memory and wall time per invocation and mount no platform credential into the runtime. Prefer it at rung 4 whenever the platform already runs such a runtime.

Ranking, per axis. Re-emit each line with only the rungs step 1 left standing:

- efficiency: `app-owned extension data > webhooks plus callback > platform-operated connector > ingested connector > mediated extension field > isolated partner subgraph`
- effort, highest first: `isolated partner subgraph > mediated extension field > platform-operated connector > ingested connector > app-owned extension data > webhooks plus callback`
- value (live partner data in one client query): `isolated partner subgraph == mediated extension field > platform-operated connector > ingested connector == app-owned extension data > webhooks plus callback`
- compliance cost, highest first: `isolated partner subgraph > mediated extension field > platform-operated connector > ingested connector == app-owned extension data > webhooks plus callback`
- durability: `webhooks plus callback == app-owned extension data > ingested connector == platform-operated connector > mediated extension field > isolated partner subgraph`

Ties, justified:

- The two live rungs tie on value because both run partner logic inside the client's query. The subgraph adds only cross-entity query planning, which few partner fields need.
- Rungs 1 and 2 tie on value and compliance because both hold partner data in platform storage under platform schema; they differ only in who writes it.

Default rung per shape from step 1. A need that turns out to be live is a reclassification in step 1, never a promotion up the ladder.

- **Events**: rung 0.
- **Stored data**: rung 1. Move to rung 2 when a canonical platform type already exists for the data (documents, contacts, tickets) and partners sync into it.
- **Live data**: rung 3 for a few partners whose APIs already exist. Move to rung 4 when partners are many or self-serve: its contract and proxy are built once. Move from rung 4 to 5 only when the partner set is small, contractually bound, and its fields need joint planning across several platform entities.

The order starves rung 5: highest value, highest effort, so it loses every efficiency round. Promote it anyway when a few strategic partners under contract must contribute live entity data that a single mediated field cannot shape, and the platform can staff partner schema review as a standing job.

Re-rank against the interview, and say which answer moved which rung:

- A hard date (question 7) promotes rung 3 for live data, since the platform builds it without partner engineering. For stored data or events it changes nothing; re-check that the need is not stored data in disguise.
- Many self-serve partners demote rungs 3 and 5 (per-partner mapping or schema review) and promote rung 4. A few partners under contract do not trigger this, however long the program runs.
- An existing open-licensed router and registry the team already runs lowers rung 5's effort, never its exposure.

See [references/platform-cases.md](references/platform-cases.md) for how Shopify, Atlassian, Hasura, Hygraph, Apollo, Cosmo and Block each sit on this ladder.

## 3. The partner contract (rungs 4-5)

Composition checks that a schema is valid, never that a contributor may claim what it claims. Write the authorization layer composition lacks:

- **Extendable-entity allowlist**: the platform entities partners may extend, each with its published key. Everything else is closed.
- **Namespace**: every partner type and root field carries the partner prefix. Unprefixed types merge or collide with platform types of the same name.
- **Nullable only**: every partner field on a platform type is nullable, so a partner failure yields null plus an error instead of blanking the platform object.
- **Directive policy**: ownership transfer (`@override`), co-resolution of platform fields (`@shareable`), assertion of another owner's data (`@provides`), global hiding (`@inaccessible` outside the partner namespace) and interface-wide extension (`@interfaceObject`) are rejected. `@requires` is limited to the data-clearance list.
- **Audit the platform's own `@shareable` fields**: those are the ones a partner can co-resolve, by redefining the type rather than extending an entity. The namespace rule must reject any partner definition of them.
- **Enforcement as a blocking check**: the policy runs on every partner publish, in the platform's registry, and rejects the publish. Partners never hold publish rights to the variant.

For rung 4, decide what the mediated field returns; that choice sets the SDL policy, the cost model and client codegen:

- **Platform-defined envelope plus partner payload** (default): display fields, a link and a status the platform types, plus a payload validated against a JSON Schema the partner registers.
- **Opaque JSON scalar**: cheapest, but clients lose typing and validation.
- **Per-partner typed union**: full typing, but every partner contributes schema, which is rung 5's review job.

For rung 3, apply only the namespace rule: the platform writes the mapping, so it controls the rest.

See [references/partner-sdl-policy.md](references/partner-sdl-policy.md) for the full directive table, good and bad SDL, CI wiring per registry, and removal-impact checks.

## 4. Data and credentials toward the partner (rungs 3-5)

- **Data-clearance list per entity**: list every field the partner receives - key fields, every `@requires` field, client arguments - and the consent that covers each. A `@requires` field ships to the partner even when the client never selected it, once per entity, so a list query ships it once per row.
- **Minimize before clearing**: when a partner needs a sensitive field to compute, expose a derived, coarser platform field for it to require instead (an age band instead of a date of birth, a region instead of an address), hidden from the public schema.
- **No client credential reaches a partner**: forward no end-user bearer token, session cookie or platform API key. Mint a per-partner token, short-lived, bound to that partner's audience, the installing tenant and the consented scopes. Minting needs code running per request (a router extension, coprocessor or egress proxy); a static header insert cannot carry a tenant-bound token.
- **Header allowlist, explicit, no catch-all**: some engines forward nothing by default, others ship a "forward all client headers" switch, and catch-all propagation rules are a common copy-paste pattern. Remove any catch-all toward partners and list each allowed header by name.
- **The partner endpoint authenticates every call**: mTLS or a signed platform token. It takes tenant and scopes from the token, never from the entity representation, and answers `_service` and introspection only to the platform. Partner endpoints are public URLs; without this, anyone can post `_entities` keys and enumerate partner data about every tenant.
- **Regulated data gate**: a personal or regulated field enters the clearance list only with tenant consent recorded at install, signed partner data-processing terms, and a residency check of the partner's hosting region. Otherwise derive or drop it.
- **Partner output is untrusted input**: platform code that consumes or displays a partner value validates it like user input. Mask partner error messages to a platform code plus the partner ID, and never pass partner `extensions` through to clients.

## 5. Blast radius (rungs 3-5)

- Per-partner timeout: client SLA from question 6, minus the internal p95 up to the hop that calls the partner (a `@requires` hop runs after the platform fetches), minus a margin. Router defaults sit at 30-60 seconds.
- Per-partner circuit breaker that counts timeouts as failures. Where the router has none, put the partner behind an egress proxy with outlier detection.
- A request-level deadline as a backstop above the partner timeouts, never below them: a whole-request deadline that fires first fails the query instead of returning platform data plus a partner-field error. Some routers default the request timeout to the same value as the subgraph timeout, so a partner hop after a `@requires` fetch always loses to it on defaults.
- Partner fields priced in the query cost model and rate-limited per partner.
- Partner routing URLs validated against SSRF: public HTTPS hosts only, re-checked on every resolution, through a dedicated egress path.
- Partner responses excluded from shared caches and from cross-request query deduplication, or keyed per tenant and credential.

See [references/router-isolation.md](references/router-isolation.md) for the per-control detail, the router CVEs that widen partner exposure, and engine defaults.

## 6. Who sees partner fields (rungs 1-5)

Show partner data only to tenants that installed the partner and consented to its data flow. A field visible to every tenant implies a partner relationship most tenants never chose.

For rungs 1-2, partner data sits behind generic platform fields, so control access per value, not per schema field:

- Owning app only, tenant admin read or write, other apps, public or storefront read: set one level per definition, defaulting to the narrowest.
- Never let one app read another app's namespace without an explicit, tenant-granted scope.

For rungs 3-5:

- Filter the schema per audience with include-only rules (a partner variant, never an exclude filter: it publishes every field nobody remembered to tag).
- Enforce per-tenant installs at request time with a platform-assigned scope or policy per partner, checked by the router. One contract variant per install combination does not scale past a few partners.
- Mark partner ownership in each field's docstring and state that the platform SLA does not cover it.

## 7. Lifecycle (rungs 1-5)

1. **Publish**: the partner runs the composition check against the partner variant in its own CI with a check-only credential scoped to its own subgraph; where the registry cannot scope one, the platform runs checks through a submission endpoint. The platform's registry re-runs the check plus the policy check; only the platform publishes. Never hand a partner a key that can publish or read other partners' SDL. At rung 4, validate the registered payload schema and endpoint against the contract instead; at rungs 1-2, validate definitions against the namespace and access-level rules.
2. **Platform changes**: a platform change that breaks a partner's composition (a removed key field, a field on the clearance list renamed) is a breaking change. Hand the notice window to the versioning policy.
3. **Partner changes**: a failing partner publish is the partner's break. Never auto-roll the graph forward around it. A publish that composes but removes or retypes a field clients query is the dangerous one: run operation checks against client usage on every partner publish, and hold partner fields to the platform's deprecation window.
4. **Observe per partner**: latency, error rate, timeout rate and circuit-breaker state per partner subgraph or connector, attributable in response extensions. Name an owner per partner, give each partner a status component, and set the suspension threshold (how long an open circuit lasts before the partner leaves the variant).
5. **Offboard**: run the removal-impact check, pull per-field usage, remove from the partner variant first and the base graph second, give clients the deprecation window. For rung 1, define uninstall semantics up front: definitions deleted, values retained for a stated period.

## Standards and lock-in

Partners who ship subgraphs depend on the platform's federation dialect, registry and router. That makes the router choice a partner-facing contract:

- Never promise partners the open GraphQL Composite Schemas dialect before that specification reaches Draft; check its current stage first.
- Separate what partners run from what the platform runs. Partners need a subgraph library (usually permissively licensed) plus check access to the platform's registry; composition, query planning and the router carry the platform's license choice. State which registry account a partner needs.
- Rungs 0-4 keep the router internal and swappable. That durability is the second reason, after exposure, to stop below rung 5.

## Failure modes

- Partner subgraphs composed into the first-party production supergraph.
- Jumping to partner subgraphs when step 1 found stored data or events.
- A partner SDL with `@override`, or `@shareable`/`@provides` on fields the platform already marks shareable, that composes and ships, because composition passed.
- `@requires` pulling a field outside the data-clearance list.
- End-user `Authorization` or `Cookie` forwarded to a partner through a catch-all propagation rule.
- A non-null partner field on a platform type.
- Router-default timeouts on partner calls; no circuit breaker.
- Partner routing URLs accepted without SSRF validation.
- Partner fields visible to tenants that never installed the partner; exclude-filter contracts.
- Partner responses in a shared cache.
- A partner endpoint that accepts `_entities` calls without verifying a platform credential.
- Offboarding by deleting the subgraph, with no removal-impact check or notice.

## Measurement

Gates, each binary; iterate the design until all pass:

- Exposure: zero partner fields on platform types that are non-null, unprefixed, or reachable by tenants without the partner installed.
- Policy: 100% of partner publishes pass through the blocking policy check; a test publish with `@override` on a platform field is rejected.
- Credentials: a canary partner endpoint that echoes received headers shows no client `Authorization`, `Cookie` or platform key.
- Partner authentication: a call to the canary endpoint with no platform credential, or with another tenant's token, is rejected.
- Blast radius: with the canary endpoint stalled, the platform query returns its own data plus a partner-field error within the client SLA.
- Lifecycle: an offboarding drill on the canary runs the removal-impact check before removal.

These pass conditions are set by this skill from the controls above, not published benchmarks; adjust the canary setup, never the direction.

## Invocation examples

- "Our logistics partners want to add tracking fields to `Order` in our public GraphQL API. We run a federated graph already - can they just ship subgraphs?"
- "Design how marketplace apps store their own data on our `Customer` type and query it back through GraphQL."
- "We want to stitch three partners' GraphQL APIs into our graph under one endpoint. What do we need to lock down?"

Expected output: a design record with the need classification, the chosen rung per need with the ranking lines and which interview answer moved them, then - for the chosen rung - the partner contract, the data-clearance list, the credential model, blast-radius values, the visibility rule, and the lifecycle steps. A review of an existing partner integration emits the same sections as findings, each naming the failure mode it hits.

## References

- `samber/developer-platform-skills@public-graphql-api-design` - the single-owner public schema and the internal federation trust boundary (only the router is public); this skill starts where outside contributors enter.
- `samber/developer-platform-skills@api-integration-surface-strategy` - whether GraphQL is the right surface at all.
- `samber/developer-platform-skills@api-versioning-policy` - notice windows for platform changes that break partner composition, and for partner offboarding.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner's journey to a first submitted integration, which this design plugs into.
- `samber/developer-platform-skills@webhook-platform-design` - rung 0 in depth.
- `samber/developer-relations-skills@developer-ecosystem-strategy` - whether to open the platform to third parties at all, in the sibling collection.
