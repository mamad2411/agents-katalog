# Providers — Agent Instructions

Native providers implement core ports without depending on optional upstream projects. External integrations remain under `adapters/`.

## Rules

- Import provider-neutral contracts; never make core packages import a provider.
- Preserve workspace scope on every read and write.
- Fail closed on malformed input, unavailable dependencies, or unsupported versions.
- Never fall back from local to cloud.
- Declare health, capabilities, limits, and data paths in `provider.json`.
- Add behavioral tests and run the shared conformance helper.
- Provider-specific IDs and payloads must not become canonical public identifiers.
- Context candidate-source providers discover records only; they must preserve
  provenance and leave final eligibility, scoring, budgeting, and assembly to
  the Context Compiler.
- Changes that broaden filesystem, process, network, or secret access require security review.
