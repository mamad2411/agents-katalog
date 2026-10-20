# A2A Channel

This module owns KOTA's Agent2Agent HTTP surface.

- Keep A2A Agent Card shape, JSON-RPC method decoding, SSE framing, and
  capability decisions inside this module.
- Treat every A2A HTTP body, header-derived value, task id, message part, and
  context id as external input. Decode it once at the boundary before calling
  daemon/session primitives. Routing selectors share the protocol-owned decoder;
  message and push configuration callers select their own envelopes.
- Route live work through the daemon `/sessions` control API. Do not read raw
  `.kota/` session files and do not add a parallel task queue, workflow
  engine, session store, agent registry, or MCP mirror.
- A2A task ids are KOTA daemon session ids. Any adapter memory must be
  transient request state only; durable task/session truth stays in the daemon.
- The public Agent Card must advertise only stable, non-sensitive capability
  metadata. Put token-bearing or deployment-sensitive details only behind
  bearer-protected `/api/a2a/*` routes.
- Advertise only implemented capabilities. Push callback authentication,
  persistence and unsubscribe behavior belong to this adapter.
- Never expose internal reasoning traces, raw tool state, system prompts,
  workflow run internals, memory internals, or raw `.kota/` files through A2A.

Protocol fixtures replace the daemon backend and outbound callback ports. HTTP
scenarios use in-memory Node HTTP requests and the production server request
handler for routing and authorization;
never recreate the host's bearer-token gate in a channel fixture. A2A task frames
are projections of daemon sessions, not a second task lifecycle.
