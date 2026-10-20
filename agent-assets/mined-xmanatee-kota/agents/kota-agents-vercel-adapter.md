# Vercel Adapter Module

This directory owns the `vercel-adapter` repo module — Vercel AI SDK Data Stream Protocol integration.

- Contributes a chat route for Vercel `useChat` clients.
- Each request creates an `AgentSession` bound to the client-supplied conversation
  `id`; replacement recovers that conversation through core continuity. Requests
  without an id create independently preserved work. A new id starts new work.
- `data-stream.ts` owns the Data Stream Protocol v1 transport and wire format helpers.
- Request sessions use configured autonomy explicitly. Missing session-autonomy
  config is a request-boundary error, not a hidden fallback.
