---
name: rfc2119
description: Enforce correct usage of RFC 2119 requirement level keywords (MUST, SHOULD, MAY, etc.) in documentation and specifications. You MUST load this skill when writing or reviewing standards, specifications, or when applying RFC 2119 terminology.
license: MIT
---

# Skill: rfc2119

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Enforce the standardized meaning of requirement level keywords as defined in BCP 14 (RFC 2119).

## Core Principles

- **Absolute Requirements**: Use `MUST`, `REQUIRED`, or `SHALL` only for absolute requirements of the specification.
- **Absolute Prohibitions**: Use `MUST NOT` or `SHALL NOT` only for absolute prohibitions.
- **Strong Recommendations**: Use `SHOULD` or `RECOMMENDED` when valid reasons exist to ignore an item, but the full implications must be understood and weighed.
- **Weak Prohibitions**: Use `SHOULD NOT` or `NOT RECOMMENDED` when a behavior is acceptable or useful in specific circumstances, but implications must be weighed before implementation.
- **Optional Features**: Use `MAY` or `OPTIONAL` for truly optional items. Implementations must interoperate regardless of feature presence.
- **Capitalization**: ALWAYS capitalize these keywords when used in their RFC 2119 context.
- **Sparseness**: Use imperatives sparingly. Limit usage to requirements necessary for interoperation or to prevent harm.

## Core Process

1. **Identify Imperatives**: Scan the text for requirement-level intent.
2. **Select Keyword**: Map the intent to the exact RFC 2119 keyword.
3. **Capitalize**: Ensure the chosen keyword is fully capitalized.
4. **Verify Necessity**: Confirm the requirement is essential for interoperability or safety; if not, rephrase without RFC 2119 keywords.
5. **Security Context**: Elaborate on the security implications of ignoring `MUST`, `MUST NOT`, `SHOULD`, or `SHOULD NOT` directives.

## Limitations

- These keywords apply strictly to technical specifications and standards; do not use them for general narrative or conversational text where their formal weight is unnecessary.

## References

- [Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119)

## Related Skills

- **docs-writer**:
  You MUST load this skill when generating new documentation that incorporates these specifications.
