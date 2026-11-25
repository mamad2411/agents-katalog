---
name: martix-power-platform
description: "Definition-first guidance for Microsoft Power Platform, Power Automate cloud flows, environments, solutions, Dataverse ALM, and especially custom connectors. Use this skill whenever a request mentions custom connectors, OpenAPI or Swagger imports, x-ms extensions, paconn, Power Automate flow design, connector authentication, OAuth or Microsoft Entra ID, polling or webhook triggers, connector policies, custom C# code, connection references, environment variables, connector testing, quotas, sharing, or certification. Do not use it for generic REST API implementation, general Azure API Management, desktop UI automation, Power BI modeling, or generic Copilot Studio design."
license: Complete terms in LICENSE.txt
---

# MartiX Power Platform router

Use this skill as an environment-aware decision guide, not as a generic REST
snippet library. Start by identifying the product surface, target environment,
API security model, licensing boundary, and ALM state. Then open only the
smallest relevant rule or reference file.

## In scope

- Power Platform environments, Dataverse, solutions, connection references, DLP,
  gateways, VNet boundaries, and deployment decisions.
- Power Automate cloud-flow type selection, trigger/action graph design,
  run-history troubleshooting, limits, retries, pagination, and idempotency.
- Custom connector authoring from the blank designer, OpenAPI/Swagger 2.0,
  Postman (after checking the current supported format), or `paconn`.
- Connection parameters and authentication: anonymous, Basic, API key, OAuth 2.0,
  Microsoft Entra ID, managed identity, redirect URIs, and multi-auth.
- Connector schemas and `x-ms-*` extensions, dynamic values/schema, test
  connection, polling/webhook triggers, policy templates, and custom C# code.
- Connector validation, sharing, versioning, certification, and preview-to-GA
  readiness.

## Route by problem

| Problem | Start with | Add when |
| --- | --- | --- |
| Product, flow type, environment, or permissions | [Foundation and flow rules](./rules/foundation-flow-environments.md) | [Testing and limits](./rules/testing-troubleshooting-limits.md) for capacity or run behavior |
| Create or import a connector | [Connector authoring](./rules/connector-authoring.md) | [OpenAPI extensions](./rules/openapi-extensions.md) for schemas and design-time UX |
| API key, OAuth, Entra, managed identity, or connection failure | [Authentication and connections](./rules/authentication-connections.md) | [Environment and ALM](./rules/solutions-alm-versioning.md) for solution rebinding |
| Polling or webhook event behavior | [Triggers and runtime](./rules/triggers-runtime.md) | [Testing and troubleshooting](./rules/testing-troubleshooting-limits.md) for duplicates, throttling, or orphaned subscriptions |
| Routing, conversion, headers, or response shaping | [Policies and custom code](./rules/policies-custom-code.md) | [Connector authoring](./rules/connector-authoring.md) if the contract itself is wrong |
| A connector or flow fails, throttles, or produces the wrong shape | [Testing and troubleshooting](./rules/testing-troubleshooting-limits.md) | [Volatile values](./references/volatile-values.md) when docs disagree |
| Move, share, deprecate, certify, or publish | [Solutions, ALM, and versioning](./rules/solutions-alm-versioning.md) | [Certification and boundaries](./rules/sharing-certification.md) for public distribution |

## Working rules

1. Distinguish a connector definition, a credential-bearing connection, a
   solution connection reference, and a flow. A valid definition does not prove
   that a target environment can authenticate, reach the API, or run the flow.
2. Prefer an explicit OpenAPI 2.0 contract and stable schemas. Add an
   `x-ms-*` extension only when it changes maker-facing behavior; use a policy
   for a narrow runtime adaptation and custom code only when the contract and
   policies cannot express the behavior.
3. Keep secrets out of source control, solutions, logs, and ordinary environment
   variables. Rebind connections and values in the target environment.
4. Test in a nonproduction environment, validate the connector definition,
   inspect raw operation outputs, and test representative failures before
   deploying or sharing.
5. Treat licensing, quotas, preview features, portal labels, Postman versions,
   OAuth redirect examples, custom-code timeout, and certification timelines as
   volatile. Load [the volatile-values reference](./references/volatile-values.md)
   and recheck the current Microsoft Learn page before making a concrete claim.

## Boundaries and handoffs

- Hand off generic REST or OpenAPI design without a Power Platform target to the
  owning API or language skill.
- Hand off general Azure API Management, Functions, networking, or identity
  provisioning to the relevant Azure skill; return here for connector metadata,
  flow wiring, or solution ALM.
- Hand off desktop-flow UI automation, Power BI modeling, and Copilot Studio
  agent design unless the task specifically concerns their connector boundary.

## Package references

- [Companion and maintainer guide](./AGENTS.md)
- [Decision map](./references/decision-map.md)
- [Source index](./references/doc-source-index.md)
- [Volatile values and conflicts](./references/volatile-values.md)
- [Connector plan template](./templates/connector-plan.template.md)
