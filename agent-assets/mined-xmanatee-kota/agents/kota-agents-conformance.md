# Thin-Client Contract Conformance

This directory owns cross-language semantic conformance examples and binding
generation entrypoints.

- Structural wire contracts have one daemon-owned machine-readable source.
  Generated bindings are build products; clients do not maintain handwritten or
  byte-identical mirrors of the same structure.
- Authored vectors exist only for behavior the structural contract cannot
  express, such as cross-field rules, version handling, ordering, redaction,
  and shared operator meaning.
- Each vector names the contract or capability it exercises. A client runs the
  vectors for the capabilities it declares, not a universal fixture corpus.
- A malformed example is added only when it protects a meaningful boundary
  decision. Unknown-field policy belongs in the versioned decoder contract,
  not in a mandatory negative arm for every enum.
- Render examples test stable product meaning. They do not freeze incidental
  wording, score formatting, private view layout, or copied files across every
  platform.

When a contract changes, update its canonical schema, regenerate bindings, add
or revise only the affected semantic vectors, and verify the declaring clients.
Freshness checks compare generated output with its source; runtime suites do not
need separate source-absence or copy-identity tests.
