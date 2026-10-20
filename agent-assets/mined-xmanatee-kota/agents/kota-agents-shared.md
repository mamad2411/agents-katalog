# Shared TypeScript Client Contracts

This directory contains framework-free TypeScript contracts shared by the web
and React Native clients.

- Keep React, React Native, transport, storage, and routing dependencies in the
  platform client that owns them.
- Share state machines and other product-neutral types only when both clients
  consume the same semantics.
- Prefer discriminated variants over related optional flags so invalid client
  states are unrepresentable.
- Search state owns query and typed-refinement matching together so filter-only
  results cannot bypass the shared empty transition.
