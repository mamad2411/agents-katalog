---
name: data-validation-pydantic
description: Validates API payloads, files and config in Python with Pydantic v2 models, strict types and error reports a user can understand.
---

# Data validation with Pydantic

Validate once at the edge, then pass typed models inward.

## Steps

1. Find boundaries: request bodies, queue messages, files, environment variables, third-party API responses. List what each should contain.
2. Write one `BaseModel` per shape. Use precise types (`EmailStr`, `HttpUrl`, `conint(ge=0)`, `Literal[...]`, `datetime`) instead of bare `str` and `int`.
3. Decide strictness per model. Use `model_config = ConfigDict(strict=True, extra="forbid")` for internal contracts so typos fail loudly. Keep coercion only where the source is text, such as CSV.
4. Express rules that span fields with `@model_validator(mode="after")` and single-field rules with `@field_validator`. Raise `ValueError` with a human message.
5. Parse with `Model.model_validate(data)` or `model_validate_json`. Never catch a bare exception; catch `ValidationError`.
6. Convert errors: loop over `e.errors()` and build `{"field": ".".join(map(str, err["loc"])), "problem": err["msg"]}`. Return all errors at once, not the first.
7. Use `SecretStr` for tokens and exclude them from output with `model_dump(exclude=...)`.
8. For settings, use `pydantic-settings` so missing variables fail at startup.

## Rules

- No `dict[str, Any]` crossing a function boundary when a model fits.
- Do not use v1 names (`parse_obj`, `validator`, `Config`).
- Add a test with one valid and three invalid payloads per model.

## Report

List models added, fields tightened, and any input that used to pass and now fails.
