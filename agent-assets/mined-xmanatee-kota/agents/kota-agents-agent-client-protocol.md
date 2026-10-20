# Agent Client Protocol

This module owns KOTA's Agent Client Protocol adapter.

- Keep ACP JSON-RPC, stdio framing, and ACP capability decisions inside this
  module. Do not add ACP-specific routing to core.
- Stdout is protocol-only: every byte written there must be a valid ACP
  JSON-RPC message followed by a newline. Diagnostics go to stderr.
- Treat every ACP frame as external input. Decode it at this boundary into
  typed values before calling daemon/session primitives.
- Route live session work through the daemon control session API. Do not read
  `.kota/` session state directly and do not add a parallel session store.
- Advertise only implemented ACP capabilities. Reject unsupported methods and
  non-empty optional features with typed JSON-RPC errors and no side effects.
