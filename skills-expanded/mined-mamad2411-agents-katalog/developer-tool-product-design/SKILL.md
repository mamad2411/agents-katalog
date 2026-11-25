---
name: developer-tool-product-design
description: Design and audit developer tools, APIs, SDKs, CLIs, libraries, platforms, dashboards, docs, examples, onboarding, quickstarts, pricing, usage limits, telemetry, changelogs, support, and community growth. Use when building developer-facing products, improving developer experience, launching APIs/SDKs, or reviewing docs-to-activation funnels.
---

# Developer Tool Product Design

Use this skill to make developer products easy to understand, fast to try, safe to adopt, and credible in production.

## Workflow

1. Identify developer persona, job-to-be-done, integration surface, adoption path, and production risk.
2. Read `references/developer-tool-product-systems.md`.
3. Map the path from discovery to first successful call/run, production integration, debugging, billing, and support.
4. Audit docs, examples, SDK/API shape, error messages, limits, telemetry, changelog, and trust signals.
5. Produce an activation plan with product changes, docs changes, instrumentation, and support readiness.

## Guardrails

- Do not optimize only for signups; optimize for first success and safe production adoption.
- Do not hide limits, pricing, auth requirements, data handling, or breaking-change policy.
- Treat error messages, logs, examples, and support traces as product UX.

## Output format

```text
Developer persona/job:
Integration surface:

Activation path:
- <step> -> success evidence, failure mode, fix

DX findings:
- P0 <issue> -> product/docs/API change

Operational trust:
- limits, pricing, changelog, status, support, migration policy

Metrics:
- discovery, first success, production adoption, retention, support load
```
