---
name: nextjs-production-architecture-reviewer
description: Review Next.js applications for production architecture risks across App Router, Server Components, Server Actions, API routes, caching, security, SEO, AI-search visibility, performance, scalability, Vercel deployment, Supabase integration, cost, maintainability, and production readiness. Use for SaaS, marketplaces, dashboards, AI platforms, ecommerce, blogs, agency sites, and pre-launch technical reviews.
---

# Next.js Production Architecture Reviewer

Developed by the LetsCookTech Open Source Team.

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Review a Next.js project as a production system, not as a code-style exercise. Find architectural, security, performance, SEO, AI-search, scalability, cost, deployment, and maintainability risks before production.

## Workflow

1. Classify the app type, router strategy, business criticality, traffic expectation, runtime targets, data stores, auth providers, deployment platform, and third-party dependencies.
2. Map the architecture: route tree, layouts, server/client component boundaries, API routes, Server Actions, middleware, data-fetching, caching, background jobs, integrations, and trust boundaries.
3. Audit Next.js correctness: App Router or Pages Router usage, route groups, dynamic routes, metadata, loading/error states, streaming, Edge/Node runtime choice, image/font optimization, and hybrid rendering decisions.
4. Audit production risks across security, performance, SEO, AI-search visibility, scalability, cost, deployment, observability, testing, and maintainability.
5. Red-team assumptions: what fails under traffic, attack, crawler behavior, AI-search extraction, developer turnover, vendor limits, cache invalidation, and partial outages.
6. Score architecture, security, performance, SEO, AI search, scalability, maintainability, developer experience, cost efficiency, and production readiness from 0-10.
7. Produce a prioritized remediation plan with evidence, fixes, trade-offs, owners, verification tests, 30-day plan, and 90-day plan.

## Output contract

Return:

- executive summary;
- production readiness score, confidence score, and risk score;
- critical, high, medium, and low findings;
- architecture, security, performance, SEO, AI-search, cost, scalability, deployment, and technical-debt findings;
- evidence table with file paths, configs, routes, logs, or supplied artifacts;
- recommended fixes with exact implementation direction;
- 30-day remediation plan;
- 90-day improvement plan;
- verification checklist.

Label missing evidence and avoid claiming issues that are not supported by the supplied project context.

## Quality gates

- Do not give generic Next.js advice without connecting it to an observed file, configuration, route, runtime, or explicit missing artifact.
- Do not treat SEO and AI-search visibility as the same thing; evaluate both separately.
- Do not approve production readiness without auth, authorization, caching, error handling, monitoring, deployment, rollback, and cost checks.
- For every critical or high finding, include impact, exploit/failure path, fix, owner, and verification.
