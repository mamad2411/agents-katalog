---
name: openapi-engineering
description: Author and maintain OpenAPI specs. Use when design-first API
  documentation or spec generation.
metadata:
  tags: openapi, engineering
---

# OpenAPI Engineering

## Use this skill when
- Designing APIs with OpenAPI as the contract
- Generating clients/servers from specs
- Keeping the spec in sync with implementation

## Do not use this skill when
- General API design rules (use api-contracts)
- Non-OpenAPI documentation formats

## Instructions
1. Use a consistent spec version and file organization (components).
2. Define schemas precisely with types, examples, and validations.
3. Document every status code and error schema.
4. Add security schemes matching the real auth.
5. Keep spec and code in sync: contract tests, linting, generation.
6. Version the spec with the API.
7. Validate the spec with tools (swagger-cli, spectral).

## Checklist
- Spec validates
- Every endpoint documented
- Security schemes accurate

## Output Format
- Spec layout | schemas | operations | sync mechanism

## Common Mistakes
- Spec drifting from reality
- No error schemas
- Two sources of truth diverging
