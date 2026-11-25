---
name: shopify-hydrogen-analyze-oxygen
description: Analyze Hydrogen deployment to Shopify Oxygen including environments, bindings, runtime constraints, deployment behavior, logs, domains, and edge execution. Use for Shopify Hydrogen headless commerce architecture, implementation review, production diagnosis, or modernization.
---

# Analyze Oxygen

1. Read the Hydrogen repository, `.digital-platform-ai/` metadata, environment configuration, dependencies, and relevant service instructions.
2. Identify the Hydrogen package/API versions and use the repository's actual React Router/Shopify conventions rather than assuming an older Remix-era implementation.
3. Inspect the exact route, loader/action, GraphQL operation, component, session, API client, or server context involved before making code-level claims.
4. Gather runtime evidence from Oxygen or the deployed host, Shopify API errors, application logs/traces, browser/network evidence, and enterprise middleware when diagnostic.
5. Separate storefront rendering, Shopify API behavior, customer/session state, edge/runtime behavior, and downstream enterprise-system behavior.
6. Optimize independent data fetches in parallel and defer non-critical data when appropriate; avoid serial request waterfalls without evidence they are required.
7. Never cache Customer Account API data or other personalized/PII-bearing responses. Verify caching scope before applying public cache strategies.
8. Verify current Shopify API versions, Hydrogen APIs, deprecations, and product lifecycle before recommending framework-specific components or utilities.
9. Route Admin API, generic Shopify backend, Datadog, AKS, Spring Boot, Redis, or database-specific investigation to the owning technology skills when those layers are material.
10. Do not mutate production storefronts, Shopify configuration, customer data, carts, orders, or external systems unless explicitly authorized. Never expose access tokens, session secrets, customer PII, or private API credentials.

## Output
- Storefront Context
- Code/API Findings
- Runtime Evidence
- Commerce Impact
- Root Cause or Architecture Assessment
- Recommended Action
- Remaining Unknowns
