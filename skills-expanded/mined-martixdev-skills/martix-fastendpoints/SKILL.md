---
name: martix-fastendpoints
description: Standalone-first FastEndpoints guidance for `Endpoint<TRequest,TResponse>` design, `Configure()` routing and metadata, DTO binding, validators, processors, OpenAPI, file and streaming flows, SSE, RPC, security, testing, versioning, and Native AOT. Use when requests mention FastEndpoints primitives such as `AddFastEndpoints`, `UseFastEndpoints`, `Configure`, endpoint verbs/routes, `Summary`, processors, send helpers, `FastEndpoints.Swagger`, NSwag, `AllowAnonymous()`, release groups, or FastEndpoints command and event patterns.
license: Complete terms in LICENSE.txt
---

# MartiX FastEndpoints router

- Standalone-first skill package focused on FastEndpoints-specific decisions for
  .NET 10+, C# 14+, and ASP.NET Core services.
- Keep decisions grounded in the bundled rule files and FastEndpoints reference
  maps.
- Use [AGENTS.md](./AGENTS.md) when work crosses multiple streams or needs the
  long-form review routes.

## When to use this skill

- Review or scaffold FastEndpoints feature slices and endpoint classes.
- Route `Configure()` + verb/route + summary/metadata decisions.
- Shape DTO binding, validation, endpoint helpers, and processor flow.
- Decide among HTTP, files, streaming, SSE, and RPC transport patterns.
- Review FastEndpoints security/runtime behavior, testing, and versioning.

## Quick-start routes

Use the closest row first, then add workstream rules only when needed.

| Task | Start with | Add when |
| --- | --- | --- |
| New endpoint slice (`Endpoint<TReq,TRes>`, `Configure`, `Get/Post`, `Routes`) | [FastEndpoints startup and registration](./rules/foundation-startup-registration.md) + [FastEndpoints request DTOs and binding](./rules/contracts-request-dtos-binding.md) | [FastEndpoints validation and error contracts](./rules/contracts-validation-errors.md) and [FastEndpoints endpoint conveniences and hooks](./rules/pipeline-endpoint-conveniences.md) for validator and send-helper behavior. |
| Endpoint metadata and API docs (`Summary`, tags, `Description`, Swagger/NSwag) | [Swagger and OpenAPI with FastEndpoints](./rules/docs-swagger-openapi.md) | [FastEndpoints transport and docs map](./references/transport-docs-map.md) when transport choice also changes API shape. |
| File uploads/downloads, streaming, SSE, or RPC endpoint shape | [File handling, streaming, and server-sent events](./rules/transport-files-streaming-sse.md) + [RPC and HTTP transport patterns](./rules/transport-rpc-http-patterns.md) | [FastEndpoints authentication, authorization, and secure defaults](./rules/security-authn-authz.md) when transport changes security requirements. |
| Cross-cutting endpoint behavior (pre/post processors, hooks, command/event flows) | [FastEndpoints pre and post processors](./rules/pipeline-pre-post-processors.md) + [FastEndpoints commands, events, and bus composition](./rules/architecture-command-event-bus.md) | [FastEndpoints dependency injection and service resolution](./rules/architecture-di-service-resolution.md) for lifetime or scope concerns. |
| Delivery hardening (AOT, auth, throttling, idempotency, tests, versioning) | [FastEndpoints source generation and Native AOT](./rules/foundation-source-generation-aot.md) + [FastEndpoints authentication, authorization, and secure defaults](./rules/security-authn-authz.md) | [FastEndpoints response caching and rate limiting](./rules/runtime-caching-rate-limits.md), [FastEndpoints idempotency and exception handling](./rules/runtime-idempotency-exceptions.md), [FastEndpoints testing](./rules/testing-fastendpoints.md), and [FastEndpoints versioning and release groups](./rules/versioning-release-groups.md). |

## Quick defaults

- **Endpoint shape:** Prefer `Endpoint<TReq,TRes>` with `Configure()`.
  Escalate to attributes only for a small documented case.
- **Auth posture:** Prefer explicit auth/authz.
  Escalate only when public access truly needs `AllowAnonymous()`.
- **Versioning:** Prefer built-in route versioning plus release groups.
  Escalate to `Asp.Versioning.Http` only for a real platform requirement.
- **Docs:** Prefer FE Swagger and keep `UseSwaggerGen()` after
  `UseFastEndpoints()`. Escalate when NSwag export or doc shaping needs more
  control.
- **Tests:** Prefer integration tests first.
  Escalate to handler-only focus when the pipeline is irrelevant.

For mistake-first review, start with the
[FastEndpoints anti-patterns quick reference](./references/anti-patterns-quick-reference.md)
before opening deeper rules.

## Boundaries and handoffs

- Stay in `martix-fastendpoints` for endpoint contracts, `Configure()` behavior,
  DTO binding, processors, transport decisions, endpoint-level
  security/runtime policy, and FastEndpoints testing/versioning.
- Hand off to `martix-dotnet-csharp` for broad ASP.NET Core host architecture,
  resilience, diagnostics, logging, or non-FastEndpoints framework setup.
- Hand off to `martix-fluentvalidation` for deep validator authoring patterns,
  RuleSets, error metadata strategy, localization, or validator test helper
  usage.

## Rule library by workstream

- **Foundation and hosting**: [foundation map](./references/foundation-map.md)
- **Architecture and messaging**:
  [architecture map](./references/architecture-map.md)
- **Request pipeline**:
  [request pipeline map](./references/request-pipeline-map.md)
- **Transport and documentation**:
  [transport and docs map](./references/transport-docs-map.md)
- **Runtime and security**:
  [security and runtime map](./references/security-runtime-map.md)
- **Testing and versioning**:
  [testing and versioning map](./references/testing-versioning-map.md) and
  [cookbook index](./references/cookbook-index.md)

## Package conventions

- Every rule follows the shared section contract in
  [rules/_sections.md](./rules/_sections.md): `Purpose`, `Default guidance`,
  `Avoid`, `Review checklist`, `Related files`, and `Source anchors`.
- Use [the rule template](./templates/rule-template.md) for new rules,
  [the research pack template](./templates/research-pack-template.md) for
  scoped source inventories, and
  [the comparison matrix template](./templates/comparison-matrix-template.md)
  for external comparisons.
- Keep package routing data aligned in [metadata.json](./metadata.json),
  [assets/taxonomy.json](./assets/taxonomy.json), and
  [assets/section-order.json](./assets/section-order.json).

## Standalone-first note

- This skill is authored as a standalone package under `skills`.
- If you document or install the package directly, use
  `npx skills add <source>` rather than `npx skill add`.
- Keep FastEndpoints-specific guidance here. Pull broader ASP.NET Core or
  general .NET guidance only when the task clearly widens beyond this package.
