---
name: owasp-api-security
description: >-
  OWASP API Security Top 10 2023: review HTTP, GraphQL and RPC APIs against API1:2023 to API10:2023, with
  upgrades from the legacy 2019 edition (no preview). Walks each risk's vulnerability checks, attack
  scenarios and prevention: broken object level authorization (BOLA, IDOR), broken authentication, broken
  object property level authorization (excessive data exposure, mass assignment), unrestricted resource
  consumption (rate limiting, GraphQL batching, spending limits), broken function level authorization
  (BFLA), unrestricted access to sensitive business flows (bots, scalping), server side request forgery
  (SSRF, webhooks), security misconfiguration (CORS, TLS, verbose errors), improper inventory management
  (shadow and deprecated APIs) and unsafe consumption of third-party APIs. Use when designing, threat
  modelling, code reviewing or pentest-scoping an API, triaging an API finding, or mapping 2019 IDs to 2023.
  Triggers: owasp api top 10, API1:2023, BOLA, BFLA, BOPLA, API security review.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OWASP API Security Top 10

The OWASP API Security Top 10 is the OWASP API Security Project's awareness list of the ten most critical API security risks. The 2023 edition, its second, names API1:2023 to API10:2023 and gives each a risk rating, threat agents and attack vectors, the security weakness, impacts, an "Is the API Vulnerable?" test, example attack scenarios and "How To Prevent". With this skill the agent reviews an HTTP, GraphQL or RPC API entry by entry and reports findings with the matching prevention steps.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Citations name the entry and section, with the bullet or paragraph number counted from the top: (API1:2023 Prevent 2) is the second "How To Prevent" bullet, (API2:2023 Vulnerable 7) the seventh "Is the API Vulnerable?" bullet. When a rule and the pinned source disagree, the source wins.

## Inputs (fill in, or ask before starting)

- Scope: which APIs, hosts, versions and environments are in the review, and their style (REST-style HTTP, GraphQL, RPC).
- Mode: design review, code review, threat model, or test plan.
- Roles and objects: the user roles and groups, and the object types each role may read or change.
- Integrations: third-party APIs the API consumes, and URLs it fetches on a client's behalf.
- Target version: OWASP API Security Top 10 2023 (default). OWASP API Security Top 10 2019 is legacy: read 2019 findings and map them, never report new findings under 2019 IDs. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned edition pages in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the project page and the `editions/` folder of the repository for a newer edition or release candidate, and update the pins.

## Invariants

1. **Object-level authorization in every function that takes a client-supplied ID** (API1:2023 Vulnerable 2; Prevent 2). Matching the session user ID to the ID parameter is not enough (API1:2023 Vulnerable 4), and unpredictable IDs are only defence in depth (API1:2023 Prevent 3).
2. **Property-level authorization on reads and writes.** Return only properties the caller may see, chosen explicitly, never through a generic serialiser; accept only properties the caller may change, never auto-bound (API3:2023 Prevent 1 to 4).
3. **Function-level authorization denies by default** through one consistent module, whatever the path looks like (API5:2023 Prevent 1; Vulnerable, closing paragraphs).
4. **Authentication uses standards and protects every flow.** Recovery is treated as login, sensitive changes need re-authentication, tokens are validated for signature and expiry, and API keys never authenticate users (API2:2023 Prevent 3, 4, 5, 10; Vulnerable 6 to 8).
5. **Every resource has a limit:** timeouts, memory, payload and page sizes, operations per request, rate, and third-party spend (API4:2023 Vulnerable 1 to 8).
6. **Sensitive business flows are identified and protected against automation** according to the business harm (API6:2023 Prevent).
7. **Outbound requests are constrained.** Client-supplied URLs are fetched from an isolated network with allow lists and no redirects (API7:2023 Prevent 1 to 3); third-party responses are validated like user input, over TLS, with timeouts and an allow list for redirects (API10:2023 Prevent 2 to 4).
8. **TLS everywhere, internal hops included,** with error schemas that never leak stack traces (API8:2023 Prevent 4, 9).
9. **Every host, version and sensitive data flow is inventoried,** and older or non-production versions get production protections (API9:2023 Prevent 1, 2, 6, 7).

## Workflow

1. **Pick the version.** Review against 2023 and record it. If the input cites 2019 IDs, map them first.
   -> [`references/versions.md`](references/versions.md)
   ✓ The report names the edition, and every ID carries its year (`API3:2023`, never `API3`).
2. **Map the API surface.** List hosts and versions, operations, object types and their ID fields, roles and groups, authentication flows, sensitive business flows, URL-fetching features and consumed third-party APIs. Translate GraphQL fields and RPC procedures into the Top 10's "endpoint", "object ID" and "property" terms.
   -> [`references/review-checklist.md`](references/review-checklist.md#mapping-api-styles-to-the-top-10s-terms)
   ✓ Every operation has an owner role, the objects it touches and the properties it reads and writes.
3. **Walk the ten risks.** For each entry, apply its "Is the API Vulnerable?" test to the surface, using the attack scenarios as test ideas.
   -> [`references/risks-api1-api5.md`](references/risks-api1-api5.md), [`references/risks-api6-api10.md`](references/risks-api6-api10.md)
   ✓ Each entry has a verdict: not applicable (with reason), mitigated (with evidence), or finding.
4. **Run the checklist.** Check authorization, authentication, resource limits, business flows, outbound requests, configuration and inventory item by item.
   -> [`references/review-checklist.md`](references/review-checklist.md)
   ✓ Every unchecked item is a finding or an accepted risk with an owner.
5. **Classify findings.** Pick the entry by root cause. Wrong object through an allowed operation is API1; an operation the role may not call is API5 (API1:2023 Vulnerable 5). A sensitive property read or written is API3. Volume that exhausts resources or money is API4; automation that harms the business through a legitimate flow is API6. A client-supplied URL is API7; data or redirects from an integrated API is API10. Generic injection or vulnerable components go to the general OWASP Top 10 (Methodology and Data).
   ✓ Each finding names one 2023 entry.
6. **Report.** For each finding, give the scenario, the affected operations, the default rating from the entry with your own business impact, and the prevention bullets that fix it.
   ✓ Every recommendation traces to a cited "How To Prevent" bullet.
7. **Upgrade** (only when asked). Move a 2019-based review, policy or scanner mapping to 2023.
   -> [`references/versions.md`](references/versions.md#2019-to-2023)
   ✓ Every 2019 finding has a 2023 home or an explicit place outside the list, and no verdict changed through relabelling alone.

## Verify before done

- [ ] All ten 2023 entries have a verdict, and every ID carries its year.
- [ ] Every operation that takes an object ID has an object-level check tied to the current user and action, with tests.
- [ ] No response is built by a generic serialiser, and no request body is auto-bound to a model.
- [ ] Admin and write operations deny by default; they were tested as a regular user and with changed methods or operation types.
- [ ] Login and recovery limits count operations, not HTTP requests, so GraphQL batching cannot bypass them.
- [ ] Page sizes, payload sizes, operations per request and third-party spending all have enforced maxima.
- [ ] URL-fetching features cannot reach internal addresses or cloud metadata, and do not follow redirects.
- [ ] Third-party responses are validated before storage or queries.
- [ ] Old, beta and non-production hosts are in the inventory and protected like production.

## Reference index

- **`references/versions.md`**: the 2023 and 2019 lines, what changed, the full 2019 to 2023 mapping, the upgrade steps, and why no preview is listed. Load for steps 1 and 7.
- **`references/risks-api1-api5.md`**: API1:2023 to API5:2023 with ratings, vulnerability tests, scenarios and prevention. Load for step 3.
- **`references/risks-api6-api10.md`**: API6:2023 to API10:2023 in the same form, and what the list leaves out. Load for step 3.
- **`references/review-checklist.md`**: the mapping of HTTP, GraphQL and RPC onto the Top 10's terms, and the checklist grouped by concern. Load for steps 2 and 4.

## Related skills

- `owasp-top-10` for the generic web risks this list leaves out, such as injection and vulnerable components: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-top-10`.
- `owasp-asvs` for verifiable security requirements, which the 2023 edition recommends for defining them: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-asvs`.
- `oauth` for token issuance, validation and scopes behind API2 and API5: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.
- `http-semantics` for methods, redirects and caching behind API5, API7 and API8: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `openapi` for the open-standard documentation and response schemas API3, API8 and API9 call for: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read. The `owasp.org/API-Security/` pages redirect to `api-security.owasp.org`; the text is the same as the repository's `master` branch.

- [OWASP API Security Top 10 2023 (cover)](https://owasp.org/API-Security/editions/2023/en/0x00-header/): stable release, 2023 edition (5 June 2023), checked 2026-10-05.
- [OWASP Top 10 API Security Risks – 2023 (list)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/): stable release, 2023 edition, checked 2026-10-05.
- [2023 Release Notes](https://owasp.org/API-Security/editions/2023/en/0x04-release-notes/): stable release, 2023 edition, checked 2026-10-05.
- [2023 API Security Risks (risk rating)](https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/): stable release, 2023 edition, checked 2026-10-05.
- [2023 Methodology and Data](https://owasp.org/API-Security/editions/2023/en/0xd0-about-data/): stable release, 2023 edition, checked 2026-10-05.
- [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/): stable release, 2023 edition, checked 2026-10-05.
- [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/): stable release, 2023 edition, checked 2026-10-05.
- [API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/): stable release, 2023 edition, checked 2026-10-05.
- [API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/): stable release, 2023 edition, checked 2026-10-05.
- [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/): stable release, 2023 edition, checked 2026-10-05.
- [API6:2023 Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/): stable release, 2023 edition, checked 2026-10-05.
- [API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/): stable release, 2023 edition, checked 2026-10-05.
- [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/): stable release, 2023 edition, checked 2026-10-05.
- [API9:2023 Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/): stable release, 2023 edition, checked 2026-10-05.
- [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/): stable release, 2023 edition, checked 2026-10-05.
- [OWASP API Security Top 10 2019 (cover)](https://owasp.org/API-Security/editions/2019/en/0x00-header/): stable release, superseded by 2023, 2019 edition (26 December 2019), checked 2026-10-05.
- [OWASP Top 10 API Security Risks – 2019 (list)](https://owasp.org/API-Security/editions/2019/en/0x11-t10/): stable release, superseded by 2023, 2019 edition, checked 2026-10-05.
- [OWASP/www-project-api-security (project page source, news and roadmap)](https://github.com/OWASP/www-project-api-security): latest commit 10 December 2025, checked 2026-10-05.
- [OWASP/API-Security (repository)](https://github.com/OWASP/API-Security): `master` at 33cea37 (21 September 2026), VERSION 2.7.0; `develop` carries unreleased 2023 clarifications, checked 2026-10-05.
