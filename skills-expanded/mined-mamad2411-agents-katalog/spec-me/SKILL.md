---
name: spec-me
description: Turn a user request into Product Spec and Architecture Spec, then recommend to-ticket without jumping to implementation.
---

# spec-me

## What it does

`spec-me` is the public entrypoint for turning a user request into Product Spec and Architecture Spec. It does not jump straight to implementation. It first asks for product understanding, then for architecture shape, and only then recommends `to-ticket`.

If the request is about broken behavior, flaky regression, or performance regression, `spec-me` is not the right on-ramp; use `diagnosing-bugs` instead.

## Flow

1. Run `product-spec`, which uses `grill-with-docs`.
2. Run `architecture-spec`, which uses `grill-with-docs`.
3. Use `event-storming`, `ddd-design`, and `codebase-design` as needed inside the architecture step.
4. Stop after Product Spec and Architecture Spec are complete.
5. Recommend `to-ticket`, but do not call it automatically.

## Documents

- Write the completed Product Spec to `docs/specs/product-spec.md` using the `product-spec` template.
- Write the completed Architecture Spec to `docs/specs/architecture-spec.md` using the `architecture-spec` template.
- Create `docs/specs/` when missing.
- Do not overwrite an existing spec without explicit user approval.
- Do not claim either stage is complete until its document exists.

## Rules

- Product Spec does not inspect source or test code.
- Architecture Spec does inspect current code and test structure.
- `CONTEXT.md` is glossary only.
- ADR 작성 여부는 모델이 결정한다. 결정이 오래 남을 가치가 있으면 ADR을 쓰고, 아니면 안 쓴다.

## Pulled out on purpose

`spec-me` is the user-facing wrapper for the design flow. It keeps the public surface small while delegating the actual design work to the internal skills.
