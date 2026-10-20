---
name: zod-engineering
description: Select, add, migrate, review, test, or optimize Zod schemas; parse unknown JSON, form, query, environment, event, or tool data; map Zod errors; or use Zod-to-JSON-Schema and backend interoperability. Do not use for static TypeScript-only work, backend-native validation, public API design, authorization, sanitization, or domain-invariant ownership.
---

# Zod Engineering

Use Zod as a runtime boundary adapter, not as a replacement for public-contract,
security, backend, or domain ownership.

## Use When

- A JavaScript or TypeScript boundary needs runtime parsing, normalization, or
  typed output.
- A repository selects or migrates Zod, including Zod 3-to-4 compatibility.
- A Zod schema, mapped validation error, generated JSON Schema, or performance
  claim needs review or tests.

## Boundaries

Parse `unknown` once at ingress; use parsed output afterwards; map it to plain
application or domain types. Independently validate outbound data that crosses
an untrusted or compatibility-sensitive boundary. Zod parsing is neither
authorization nor sanitization and does not own domain invariants.

For a cross-language wire boundary use:

`unknown JSON/IPC → Zod boundary schema → plain wire DTO → backend-native deserializer/validator → backend domain type`

and reverse it through a stable serialized envelope before a UI/application
parse. See the [patterns and examples](references/patterns-and-examples.md#cross-language-interop).

## Workflow

1. Inspect `package.json`, the selected lockfile/package manager/runtime,
   TypeScript version, existing validator and import style, framework adapter,
   trust boundary, and installed Zod version.
2. Preserve a suitable established validator or Standard Schema adapter unless a
   migration is explicitly requested. Decide whether a public artifact, backend
   contract, or boundary schema owns the contract before writing a schema.
3. Decide missing versus `null`, unknown keys, coercion, defaults,
   transforms/codecs, numeric/date/byte representation, size/depth/cardinality
   limits, and error exposure explicitly.
4. Parse at the adapter, map inward, normalize errors at the adapter/render
   layer, and test the observable boundary.

## Core Rules

- Prefer schema-first contracts with `z.infer`, `z.input`, and `z.output`; use
  `z.toZod<T>()` only for type-first compatibility. Never maintain duplicate
  interfaces and schemas that can drift.
- Compose object shapes or use `.safeExtend()` rather than long `.extend()`
  chains. Use strict discriminated branches for overlapping event or intent
  unions.
- Use object getters for recursive objects; use `z.lazy()` when deferred
  non-object or mutually recursive shapes are clearer.
- Read [patterns and examples](references/patterns-and-examples.md) before
  selecting parse APIs, composition, error mapping, JSON Schema, or interop.

## Errors And Security

Map structured issue codes and bounded paths to a stable application/API error
envelope. Do not expose `ZodError`, default library wording, raw input,
transformed values, full issues, or `reportInput` without an explicit sanitized
policy. `z.treeifyError()` and `z.flattenError()` belong only in a presentation
adapter.

Load [`security-review`](../security-review/SKILL.md) and
[`security-review-evidence`](../security-review-evidence/SKILL.md) for trust
boundaries; they own authorization, sanitization, resource limits, and safe
security evidence. Load [`internationalization-localization`](../internationalization-localization/SKILL.md)
for translated user messages.

## Testing

Test accepted and rejected boundaries; optional/null/unknown-key policy;
transforms and input/output divergence; sync and async parsing; mapped error
stability; and generated-contract parity. Add bounded property tests only when
the repository already uses a suitable generator. The runnable oracle is
[common patterns](examples/common-patterns.ts).

Load [`test-driven-development`](../test-driven-development/SKILL.md) for an
implementation loop and [`testing-strategy`](../testing-strategy/SKILL.md) for
coverage review.

## Performance And Migration

Measure representative valid, invalid-with-diagnostics, boolean-validation,
schema construction/reuse, transform, depth, and async workloads before using
`z.compile()` or `z.validate()`. Upstream benchmarks are not local evidence.
Read the dated [Zod 4.5 baseline](references/zod-4.5-baseline.md) before a
version-sensitive change or migration.

## Routing

- [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md)
  owns package/runtime/tooling mechanics.
- [`api-design`](../api-design/SKILL.md) owns public schemas, compatibility,
  versioning, and stable error envelopes.
- [`typescript-javascript-design-patterns`](../typescript-javascript-design-patterns/SKILL.md)
  owns adapter/core placement.
- [`performance-review`](../performance-review/SKILL.md) owns workload evidence.
- [`php-engineering`](../php-engineering/SKILL.md),
  [`python-engineering`](../python-engineering/SKILL.md),
  [`rust-engineering`](../rust-engineering/SKILL.md), and
  [`csharp-dotnet-engineering`](../csharp-dotnet-engineering/SKILL.md) own
  backend-native DTO validation, mapping, serialization, and errors.

## References

- [Patterns and examples](references/patterns-and-examples.md)
- [Zod 4.5 baseline](references/zod-4.5-baseline.md)
- [Runnable common patterns](examples/common-patterns.ts)
