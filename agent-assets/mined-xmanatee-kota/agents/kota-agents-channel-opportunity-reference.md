# Channel Opportunity Reference Module

This module is a reference composition for high-volume community-channel
opportunity matching. It proves that inbound signal routing, workflow batching,
calendar availability, owner decisions, and confirmed provider actions can work
together without adding sports-specific logic to core.

- Keep this module provider-neutral. Telegram sports communities are the main
  fixture, not the domain boundary.
- Provider-specific details belong in the routed inbound signal payload and in
  the module-owned provider-action input.
- The cheap classifier should reject noisy batches before any owner prompt.
- The stronger screening boundary is where a real deployment can swap in a
  capable model or parser; the committed reference fixture stays deterministic.
- Provider actions are dry-run fake adapters in tests. Do not send real channel
  replies, reactions, bookings, or website mutations here.
- Slack, Gmail, Discord, or other community sources follow the same route:
  normalize to `inbound.signal.received`, route by source, batch by channel or
  source, screen the batch, check availability, ask the owner, then dispatch a
  module-owned confirmed action adapter.
