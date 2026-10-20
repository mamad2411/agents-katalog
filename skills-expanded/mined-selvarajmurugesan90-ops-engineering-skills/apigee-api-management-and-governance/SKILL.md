---
name: apigee-api-management-and-governance
description: >
  Governs the full API lifecycle in Google Apigee (or comparable
  enterprise API-management platforms) — API proxy design, policy
  attachment (OAuth2/API key verification, quota, spike arrest,
  transformation), developer portal publishing, product-based
  monetization, and semantic versioning/deprecation of published APIs
  at organizational scale. Use when a user asks to "design an Apigee
  API proxy," "set up an API product for monetization," "version an
  API without breaking existing consumers," "add a spike arrest or
  quota policy in Apigee," "publish an API to a developer portal," or
  "govern API lifecycle across many teams."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Apigee API Management and Governance

## Purpose

Apigee (and enterprise API-management platforms like it) solves a
different problem than a gateway like Kong or Ingress-NGINX: instead of
"route this HTTP request to that upstream with a few plugins," it
governs an API's entire lifecycle across an organization — who's
allowed to design and publish a new proxy, how a backend service is
packaged into a sellable/consumable **API product**, how a breaking
change gets versioned without stranding existing consumers, and how
usage is measured for monetization or internal chargeback. The
operational risk here isn't a misrouted request; it's organizational —
an API published without a deprecation plan, a proxy with no quota that
lets one consumer degrade a shared backend for everyone, or a
versioning scheme that forces every consumer to migrate on the
platform team's schedule instead of their own. This skill covers
designing Apigee API proxies and policies, structuring API products for
governance and monetization, and versioning/deprecating APIs
deliberately — not general gateway routing/plugin mechanics, which are
covered for the open-source case in
[kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md).

## When to use

- Designing a new Apigee API proxy in front of one or more backend
  target services, including which policies (auth, quota, transformation,
  spike arrest) attach at the proxy vs. product level.
- Structuring API products to bundle proxies/operations for a specific
  consumer segment (internal teams, partners, paying external
  customers) with distinct quota/rate-limit tiers.
- Setting up monetization — rate plans, usage-based billing tied to API
  product consumption — for externally-facing APIs.
- Versioning a published API (path-based `/v1`/`/v2`, header-based, or
  proxy-basePath-based) without breaking consumers still on the
  previous version, and planning a deprecation timeline.
- Establishing organization-wide governance: proxy naming/versioning
  conventions, mandatory policies (auth, quota) every proxy must carry,
  and a review/approval process before a proxy reaches production.
- Deciding whether a need calls for full API-management governance
  (Apigee) or is better served by a lighter open-source gateway — see
  [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md)
  for that comparison.

## Prerequisites & environment

- An Apigee organization and environment (`eval`, `test`, `prod`, or
  custom-named environments) provisioned, with environment groups
  configured to route hostnames to the correct environment.
- Apigee roles assigned deliberately per function — API proxy
  developers, API product managers, and organization admins are
  typically distinct roles; avoid a single shared admin credential for
  all proxy publishing.
- The `apigeecli` CLI or Apigee's Maven/Gradle deployment plugins (for
  CI-driven proxy deployment) — or the Apigee UI for interactive
  design, though anything reaching production should go through a
  reviewable, version-controlled deployment path rather than
  UI-only edits.
- A defined backend target (existing service, or a mock target for
  proxies still in design) reachable from the Apigee runtime, with TLS
  configured for the target endpoint if the backend requires it.
- For monetization: Apigee Monetization enabled on the organization,
  and a billing/rating plan defined before any rate plan goes live —
  monetization configuration errors directly affect what customers are
  billed, so treat this configuration with the same review rigor as a
  financial system change, not as ordinary gateway config.
- A developer portal (Apigee's integrated portal or a separate one)
  if external partners/customers need self-service API discovery,
  registration, and API-key provisioning.

## Step-by-step guidance

1. **Design the API proxy as a facade, not a passthrough** — separate
   the proxy's public-facing contract (`ProxyEndpoint`) from the
   backend's actual implementation (`TargetEndpoint`), so the backend
   can change without breaking the published contract:
   ```xml
   <ProxyEndpoint name="default">
     <HTTPProxyConnection>
       <BasePath>/v1/payments</BasePath>
     </HTTPProxyConnection>
     <RouteRule name="default">
       <TargetEndpoint>payments-backend</TargetEndpoint>
     </RouteRule>
   </ProxyEndpoint>
   ```

2. **Attach verification and quota policies at the proxy's request
   flow**, ordered so authentication happens before quota is checked
   (an unauthenticated request shouldn't consume a legitimate
   consumer's quota):
   ```xml
   <PreFlow name="PreFlow">
     <Request>
       <Step><Name>Verify-API-Key</Name></Step>
       <Step><Name>Verify-Quota</Name></Step>
       <Step><Name>Spike-Arrest</Name></Step>
     </Request>
   </PreFlow>
   ```
   ```xml
   <VerifyAPIKey name="Verify-API-Key">
     <APIKey ref="request.queryparam.apikey"/>
   </VerifyAPIKey>
   <Quota name="Verify-Quota">
     <Interval>1</Interval>
     <TimeUnit>month</TimeUnit>
     <Allow countRef="verifyapikey.Verify-API-Key.apiproduct.developer.quota.limit"/>
     <Identifier ref="request.queryparam.apikey"/>
   </Quota>
   <SpikeArrest name="Spike-Arrest">
     <Rate>100ps</Rate>
   </SpikeArrest>
   ```
   `SpikeArrest` protects the backend from short traffic bursts even
   within an allowed monthly quota — the two policies solve different
   problems (burst smoothing vs. total allowance) and are not
   substitutes for each other. See
   [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md)
   for the deeper strategy distinguishing rate-limiting from quota
   management.

3. **Bundle proxy operations into API products, not raw proxies**, so
   governance (which consumer segment gets which quota/scope) is
   expressed at the product level rather than duplicated per proxy:
   ```yaml
   # apiproduct definition (conceptual; actual config is via Apigee UI/API)
   name: payments-api-partner-tier
   proxies: [payments-api-v1]
   operationGroup:
     operationConfigs:
       - apiSource: payments-api-v1
         operations:
           - resource: /charges
             methods: [GET, POST]
   quota: 10000
   quotaInterval: 1
   quotaTimeUnit: month
   ```
   A partner-tier product and an internal-tier product can wrap the
   *same* underlying proxy with different quotas/scopes, rather than
   maintaining separate proxy deployments per consumer segment.

4. **Version by contract, not by convenience** — a breaking change (a
   removed field, an incompatible response shape) requires a new major
   version (`/v2`) deployed alongside the still-supported `/v1`; a
   backward-compatible addition (a new optional field) does not:
   ```
   payments-api-v1  →  BasePath: /v1/payments   (existing consumers, supported)
   payments-api-v2  →  BasePath: /v2/payments   (new contract, new consumers)
   ```
   Never rewrite `/v1`'s existing behavior in place for a breaking
   change — that silently breaks every consumer still pointed at `/v1`
   with no opportunity to migrate on their own schedule.

5. **Publish a deprecation timeline before removing an old version**,
   not just a announcement after the fact:
   - Mark the old version deprecated in the developer portal and in
     response headers (`Sunset: Sat, 31 Oct 2026 00:00:00 GMT`, per RFC
     8594) as soon as the replacement is available.
   - Track actual consumer traffic on the deprecated version (Apigee
     Analytics) and reach out to consumers still calling it before the
     sunset date, rather than assuming the announcement alone reached
     them.
   - Only disable/remove the old version's proxy deployment after
     traffic on it has genuinely dropped to zero (or an explicitly
     accepted cutover date has passed), not on a fixed calendar date
     regardless of actual usage.

6. **Set up monetization deliberately, treating rate-plan changes like
   a financial-system change**, not an ordinary config edit:
   - Define a rate plan against a specific API product (not directly
     against a proxy), so pricing changes don't require touching proxy
     logic.
   - Test a new or changed rate plan against a non-production
     organization/environment first, confirming the computed charges
     for a known set of test transactions match expectations before it
     goes live for real customers.
   - Require a second reviewer on any monetization rate-plan change —
     an error here directly misbills customers, unlike a routing bug
     that merely breaks functionality.

7. **Establish and enforce organization-wide governance conventions**
   before proxy sprawl makes retrofitting them painful:
   - A required policy set every proxy must carry (e.g. `Verify-API-Key`
     or OAuth2 verification, `Spike-Arrest`, structured error handling)
     enforced via a proxy template or a CI lint step, not left to each
     team's discretion.
   - A consistent versioning/naming convention
     (`<api-name>-v<major>`) across all proxies, so a consumer or
     platform team can infer a proxy's version from its name alone.
   - A review/approval gate before a new proxy or API product reaches
     the production environment, distinct from and in addition to the
     deployment pipeline's own checks.

8. **Publish to a developer portal for external/partner consumers**,
   giving self-service discovery, API-key registration, and
   documentation rather than manual key provisioning over email/ticket:
   - Auto-generate reference docs from the proxy's OpenAPI spec so
     documentation doesn't drift from the actual deployed contract.
   - Gate registration for higher-tier products (partner, paid) behind
     an approval step; leave low-risk internal/free-tier products
     self-service.

## Best practices

- Treat the API proxy's public contract (`ProxyEndpoint`/`BasePath`)
  and the backend implementation (`TargetEndpoint`) as independently
  changeable — the whole point of a facade is that the backend can be
  replaced, re-platformed, or scaled without a consumer-visible change,
  as long as the contract doesn't change.
- Order policies so authentication precedes quota/rate checks —
  charging quota against an unauthenticated or invalid request wastes a
  legitimate consumer's allowance on nothing.
- Express consumer-segment differences (quota, scope, pricing) at the
  API product level, not by duplicating proxies per segment — a
  proxy-per-tier approach multiplies the surface area that needs to
  stay in sync on every backend change.
- Never modify a published version's contract in place for a breaking
  change — always ship a new major version alongside the old one, with
  an explicit, tracked deprecation timeline for the old one.
- Treat monetization rate-plan changes with the review rigor of a
  billing-system change (test-transaction validation, second reviewer)
  — an error here has direct financial consequences, unlike most
  gateway misconfigurations.
- Enforce mandatory policies (auth, spike arrest) and naming/versioning
  conventions via a shared proxy template or CI lint, not tribal
  knowledge — as the number of proxies and teams publishing them grows,
  unenforced conventions decay.
- Track actual consumer traffic on a deprecated API version via
  analytics before removing it — an announcement alone doesn't confirm
  every consumer has actually migrated.

## Common pitfalls

- **Symptom:** A backend service is re-platformed (new host, changed
  internal response format) and every consumer of the published API
  breaks simultaneously.
  **Fix:** The proxy was treated as a passthrough rather than a facade —
  the `TargetEndpoint` change should have been absorbable without
  touching the `ProxyEndpoint` contract. Add a transformation policy at
  the proxy layer to keep the public contract stable across the backend
  change, and going forward, always design the proxy so the backend can
  change independently of the published response shape.

- **Symptom:** A quota policy is in place per API product, but a single
  misbehaving consumer still manages to degrade the shared backend
  during a traffic spike well within their monthly quota allowance.
  **Fix:** Quota alone limits total volume over a long window (e.g.
  10,000/month); it does nothing to prevent a short, sharp burst.
  Add a `SpikeArrest` policy sized to the backend's real per-second
  capacity, independent of the quota policy — they protect against
  different failure modes and are both needed.

- **Symptom:** A breaking change is deployed as an in-place update to
  the existing `/v1` proxy "since most consumers wanted the new
  behavior anyway," and a subset of consumers start failing
  immediately with no warning.
  **Fix:** This is exactly the scenario versioning exists to prevent.
  Roll back the in-place change, deploy the new behavior as `/v2`
  instead, and give existing `/v1` consumers an explicit, published
  deprecation timeline to migrate on their own schedule rather than
  being broken without notice.

- **Symptom:** A monetization rate-plan change goes live and a batch of
  customers are billed incorrectly for a full cycle before anyone
  notices.
  **Fix:** The change skipped test-transaction validation and
  second-reviewer sign-off before going live. Treat any future rate-plan
  change as requiring the same pre-production validation as the initial
  worked example below, and build an automated reconciliation check
  comparing expected vs. actual billed amounts for a sample of
  transactions immediately after any rate-plan change ships.

- **Symptom:** During an incident, someone disables the `Verify-API-Key`
  or quota policy on a production proxy "to rule out auth/quota as the
  cause of an error spike," confirms traffic flows, and it's still
  disabled days later.
  **Fix:** This removes both access control and abuse protection for
  every consumer of that proxy, not just the one being debugged — and
  for a monetized product, it also means usage stops being metered for
  billing purposes during that window. Treat disabling either policy as
  a strictly time-boxed diagnostic step on a non-production
  environment/revision where possible, and restore it (with a tracked
  follow-up if the real cause was something else entirely) before
  closing the incident.

## Worked example

**Scenario:** Publish `payments-api` as a governed, monetized product:
a `/v1` proxy in front of the existing backend, bundled into two API
products (`internal-tier`, unlimited quota, no billing; `partner-tier`,
10,000 requests/month, billed per 1,000 requests over a base
allowance), with spike-arrest protection and a planned `/v2` migration
path already scoped for a future breaking change.

```xml
<!-- ProxyEndpoint (default.xml) -->
<ProxyEndpoint name="default">
  <HTTPProxyConnection>
    <BasePath>/v1/payments</BasePath>
  </HTTPProxyConnection>
  <PreFlow name="PreFlow">
    <Request>
      <Step><Name>Verify-API-Key</Name></Step>
      <Step><Name>Verify-Quota</Name></Step>
      <Step><Name>Spike-Arrest</Name></Step>
    </Request>
  </PreFlow>
  <RouteRule name="default">
    <TargetEndpoint>payments-backend</TargetEndpoint>
  </RouteRule>
</ProxyEndpoint>
```

```xml
<SpikeArrest name="Spike-Arrest">
  <Rate>50ps</Rate>
</SpikeArrest>
```

API products (conceptual definitions, created via the Apigee UI/
management API):
```yaml
- name: payments-api-internal-tier
  proxies: [payments-api-v1]
  quota: null            # unlimited for internal consumers
  monetized: false

- name: payments-api-partner-tier
  proxies: [payments-api-v1]
  quota: 10000
  quotaInterval: 1
  quotaTimeUnit: month
  monetized: true
  ratePlan:
    ratePlanName: partner-standard-2026
    baseAllowance: 5000       # included free
    rateAboveAllowance: "$0.01 per request"
```

Rollout sequence:
1. Deploy `payments-api-v1` to a non-production environment; run a
   fixed set of test transactions against the `partner-tier` product
   and confirm the computed charge for a known request count matches
   `baseAllowance` + `rateAboveAllowance` math exactly before enabling
   the rate plan in production.
2. Confirm `Spike-Arrest` at `50ps` doesn't reject legitimate expected
   peak load (load-test against staging) before promoting.
3. Deploy to production, publish both products to the developer
   portal, and register the first partner developer's API key against
   `payments-api-partner-tier`.
4. When a breaking change is eventually needed, deploy it as
   `payments-api-v2` alongside the still-running `v1`, publish a
   `Sunset` header and portal deprecation notice for `v1`, and track
   `v1` traffic in Apigee Analytics until it reaches zero before
   undeploying it.

## Cross-references

- [kong-api-gateway-configuration](../kong-api-gateway-configuration/SKILL.md) — the open-source gateway alternative for teams that need routing/plugins but not full lifecycle governance, monetization, or a developer portal.
- [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md) — the cross-tool strategy behind the `Quota`/`SpikeArrest` policy distinction used here.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — the service-mesh comparison point for east-west, service-to-service traffic management, distinct from Apigee's north-south, externally-published API governance role.
