---
name: use-koruma
description: >
  Apply koruma and koruma-collection in application Rust code. Use when adding or revising
  #[validator] validators, #[koruma(...)] field rules, optional or each(...) targets, typed
  validation errors, Display or es-fluent rendering, nested validation, validated newtypes,
  checked constructors, validator metadata, or built-in validator selection. Do not trigger for
  generic Rust build/test work or repository maintenance that does not change validation usage.
---

# Use Koruma

## Follow the application workflow

1. Inspect the application's `Cargo.toml`, validated types, error consumers, and existing Koruma
   patterns. Preserve compatible dependency versions and feature choices.
2. Depend on `koruma` as the facade. Add `koruma-collection` when a built-in rule matches the
   requirement.
3. Define a custom `#[validator]` only for domain-specific behavior, custom error data, or custom
   rendering.
4. Put every validator and modifier for a field in one `#[koruma(...)]` attribute. Configure
   validators with dot-chain setters and derive `Koruma` on the containing type.
5. Inspect failures through generated field and validator accessors. Add `KorumaAllDisplay` for
   displayable borrowed error variants or `KorumaAllFluent` for es-fluent rendering.
6. Use `nested` for a validated child object and `newtype` for transparent validation through an
   exactly-one-field wrapper. Select `try_new`, `try_from`, or `try_from_inner` according to
   the caller-facing construction API.
7. Update dependency features, imports, validation attributes, and error handling together.

## Load details only when needed

- Read [the public feature map](references/koruma-feature-map.md) for macros, target selection,
  generated errors, rendering, metadata, nested validation, and newtypes.
- Read [the validator catalog](references/validator-catalog.md) only when choosing or configuring a
  `koruma-collection` validator.

## Apply the non-obvious rules

- Optional fields and optional elements unwrap by default. Use an explicit `Option<_>` validator
  type or `full(...)` only when the rule must inspect the whole option.
- Put generic arguments on the validator path, as in
  `RangeValidation::<_>.min(0).max(10)`; each setter takes one expression.
- Label repeated validator types with lower-snake names to avoid generated accessor collisions.
- `each(...)` recognizes `Vec<T>`, slices, arrays, and their optional forms syntactically. Do not
  assume aliases or custom collections are expanded.
- Regular nested accessors return `Option<&Error>` and are `Some` only when the child fails.
  Newtype field access is transparent when no direct field validators are added.
- Aggregate Fluent rendering omits `each(...)` failures. Enumerate element errors so messages keep
  their indices.
- Normalize external input before validation. Use `CanonicalFormValidation` to reject a stored
  value that is not already canonical, not to transform it.
- Prefer typed failed-validator accessors when tooling needs runtime
  `ValidatorMetadata::validator_params()`; structured issues are the generic reporting view.

Use current public APIs, examples, and manifests as evidence when repository code is available.
Keep application guidance focused on observable behavior rather than generated implementation
details.
