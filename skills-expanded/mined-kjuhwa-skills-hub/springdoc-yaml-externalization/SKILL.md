---
name: springdoc-yaml-externalization
description: Move long `@Operation description` and `@RequestBody examples` text out of Spring controllers into per-controller YAML files under `resources/api-docs/`, injected at runtime via a single `OperationCustomizer` bean. Swagger UI output unchanged.
category: backend
tags: [spring-boot, springdoc, openapi, swagger, yaml, refactor]
triggers:
  - "swagger externalize annotations"
  - "move swagger description to yaml"
  - "OperationCustomizer"
scope: user
version: 1.0.0
---

# springdoc OpenAPI YAML Externalization

Move long Swagger annotation text (description, request body examples, parameter docs) out of controllers into per-controller YAML under `resources/api-docs/`, injected at runtime via a single `OperationCustomizer` bean.

## When to use
- springdoc-openapi project where controllers are hard to read due to multi-line doc strings.
- Want non-devs (TW / PO) to edit docs without touching Java.
- No API surface change — only doc source relocated.

## Steps
1. Add one `SwaggerDocsConfig` `@Configuration` exposing `OperationCustomizer` bean.
2. On startup, scan `classpath:api-docs/*.yml` and cache `{controllerSimpleName → {methodName → docs}}`.
3. In the customizer: look up by `handlerMethod.getBeanType().getSimpleName()` + `handlerMethod.getMethod().getName()` and inject `description`, `requestBody.description`, `requestBody.examples`, and `parameters.<name>.description`.
4. Create `resources/api-docs/<ControllerName>.yml`. Top-level keys are Java method names.
5. Strip `description = """..."""` and `@io.swagger.v3.oas.annotations.parameters.RequestBody(...)` from controllers. Keep `summary` inline for IDE help.
6. Parse example `value:` as JSON via Jackson; fall back to raw string on parse failure.

## Gotchas
- Spring's `@RequestBody` stays; only Swagger's `@io.swagger.v3.oas.annotations.parameters.RequestBody` goes.
- Filename must exactly match controller `SimpleName`.
- Load `docsCache` once at bean init — customizer runs per operation.

## Related
- Complementary to `swagger-ai-optimization` (content quality for AI agents) — this one addresses *source location* of doc text, orthogonal concern.
