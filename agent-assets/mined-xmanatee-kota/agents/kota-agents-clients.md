# Clients

This directory contains thin operator clients for the KOTA daemon.

- Clients read live state and perform operations through the daemon's typed
  control API and event stream. They do not parse `.kota/`, start a runtime, or
  recreate daemon decisions locally.
- Each platform has one client wrapper that owns discovery, authentication,
  transport, decoding, error normalization, and event-stream lifecycle. Views
  depend on domain operations and view state, not route strings.
- Native shells own platform presentation and affordances. Shared product
  behavior belongs in the daemon contract, not in copied screen logic.
- A missing product capability is resolved by changing the owning daemon
  contract and affected clients as one coherent slice; directory boundaries do
  not force separate task or migration surfaces.

## Thin-client contract

The daemon owns one versioned machine-readable contract for structural wire
shapes. Generate language bindings from that source. Do not hand-copy route
catalogs, discriminated unions, or canonical payload trees between clients.

Authored conformance examples cover semantics that a schema cannot express:
cross-field invariants, version negotiation, capability readiness, error
meaning, security-sensitive redaction, and event ordering. An implementation
runs only the suites for contracts or capabilities it declares. Adding a
surface does not automatically require positive, negative, restart, source-
absence, and copy-identity tests.

Clients must:

- render the daemon-provided identity and canonical scope model without
  deriving either from local files;
- discover capability readiness and make unavailable actions understandable;
- derive daemon URLs and workflow choices from daemon responses rather than
  hardcoded deployment assumptions;
- normalize typed errors consistently without exposing credentials; and
- own one reconnecting event transport per connection rather than per screen.

Clients consume only the current canonical scope and capability model. Replace
obsolete public wire shapes at the daemon boundary instead of preserving
client-side compatibility paths.

## Platform ownership

- `web/` owns the browser dashboard.
- `apple/` owns native macOS and iOS shells and their shared Swift code.
- `mobile/` owns shared React Native behavior and Android parity. It does not
  create a second independent iOS product contract.
- `conformance/` owns authored cross-language semantic vectors and generation
  entrypoints, not copied production decoders or an exhaustive product fixture.
