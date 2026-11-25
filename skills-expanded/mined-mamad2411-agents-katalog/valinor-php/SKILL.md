---
name: valinor-php
description: Write and fix PHP code using `cuyz/valinor`. Use this skill whenever the user mentions Valinor, `MapperBuilder`, `NormalizerBuilder`, `MappingError`, mapping arrays, JSON, YAML, or HTTP requests into typed PHP objects, normalizing objects back to arrays or JSON, custom converters, constructors, transformers, or advanced PHPStan or Psalm type signatures with Valinor.
version: 1.0.0
source: https://valinor.cuyz.io/latest/
license: MIT
---

# Valinor PHP

Use this skill to write production-quality code against Valinor's public API.
Favor the smallest correct Valinor configuration and keep the code on the public
surface.

## Core stance

1. Default to strict mapping. Relax rules only when the input contract actually
   requires it.
2. Prefer precise PHP and PHPDoc types over `mixed` or `object`.
3. Prefer public entrypoints such as `MapperBuilder`, `NormalizerBuilder`,
   `Mapper\Source\Source`, `Normalizer\Format`, `HttpRequest`,
   `AsConverter`, `AsTransformer`, and `Object\Constructor`.
4. Treat builders as immutable configuration objects. Chain or reassign them;
   do not assume in-place mutation.
5. Prefer reusable configurators for shared application policy.
6. Avoid internal classes under areas like `Library`, `Compiler`, `Definition`,
   or concrete mapper internals.

## Read only what you need

| Task | Read |
|---|---|
| General mapping, builder setup, cache, public API | `references/api-surface.md` |
| Choosing exact types and signatures | `references/type-signatures.md` |
| JSON/YAML/file sources, path mapping, and custom iterable sources | `references/source-shaping.md` |
| Converters, key remapping, constructors, interface inference, custom errors | `references/customization.md` |
| HTTP request mapping, PSR-7 integration, source-binding attributes | `references/http-request-mapping.md` |
| Array or JSON normalization and transformers | `references/normalization.md` |
| Formatting, translating, and remapping validation messages | `references/error-messages-formatting.md` |
| Static-analysis plugins, purity, framework integration, and upgrade notes | `references/static-analysis-and-integration.md` |
| Picking an implementation pattern from a user request | `references/common-use-cases.md` |
| Debugging mapping failures or weird behavior | `references/troubleshooting-workarounds.md` |
| Fast starter snippets | `examples/happy-path.md` |
| HTTP-specific starter snippets | `examples/http-requests.md` |
| Message-formatting snippets | `examples/error-formatting.md` |
| Production-safe baseline | `examples/production-safe.md` |
| Smells and corrected versions | `examples/anti-patterns.md` |

## Workflow

1. Identify the boundary: object mapping, callable arguments, HTTP request
   mapping, normalization, or customization.
2. Load the one or two reference files that match the task.
3. Use the narrowest correct target type.
4. Start with strict defaults; only add toggles like
   `allowScalarValueCasting()` or `allowSuperfluousKeys()` when justified by the
   input contract.
5. Catch `CuyZ\Valinor\Mapper\MappingError` at the application boundary when
   invalid external input is expected.
6. If the same Valinor policy will be reused, extract it into a builder
   configurator instead of repeating chained calls.
7. If code is production-facing, add cache usage when appropriate.

## Preferred defaults

- For JSON, YAML, and files, prefer `Mapper\Source\Source::json()`,
  `Source::yaml()`, and `Source::file()`.
- For new code, prefer provided key-case configurators over deprecated source
  modifiers like `Source::camelCaseKeys()`.
- `Source::map()` path mapping is still valid when reshaping inbound payloads;
  only the deprecated key-case source modifier should be avoided in new code.
- Use direct type signatures like `'list<Foo>'` or
  `'array{status: non-empty-string, page?: positive-int}'` when a dedicated DTO
  would be unnecessary.
- Use DTOs or value objects when the structure is reused, domain-bearing, or
  deserves constructor validation.
- Use `infer()` for interface or abstract-class polymorphism when the concrete
  implementation depends on input data.
- Use `registerConstructor()` or `#[Object\Constructor]` when object creation is
  not a plain constructor mapping problem.
- Use `registerConverter()` for input value transformation and
  `registerTransformer()` for output normalization.
- For HTTP request mapping, remember route and query parameters already support
  scalar casting without enabling global `allowScalarValueCasting()`.

## Hard rules

- Do not recommend internal Valinor classes for application code.
- Do not silently widen types just to make mapping pass.
- Do not enable permissive behavior globally without an explicit reason.
- Do not forget that custom constructors, converters, transformers, and infer
  callbacks must stay pure and deterministic.

## Delivery checklist

Before finishing, make sure the code:

1. Uses public Valinor APIs only.
2. Uses the exact type signature the boundary needs.
3. Explains any non-default flexibility setting by the input contract.
4. Handles `MappingError` where invalid external input can occur.
5. Avoids deprecated patterns unless maintaining existing code.

This skill is self-contained and should be sufficient at runtime.
