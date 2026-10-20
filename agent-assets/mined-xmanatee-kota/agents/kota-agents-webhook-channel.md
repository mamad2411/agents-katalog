# Webhook Channel Module

This module provides a generic inbound HTTP webhook channel. External services
POST a JSON payload to create or resume agent sessions.

- Implements the `ChannelDef` protocol from `src/core/channels/channel.ts`.
- Registers its HTTP route via module route contribution.
- Supports optional HMAC-SHA256 signature verification.
- Supports source-based routing to different agents with durable source/agent
  continuity through module-created sessions. Direct requests recover their own
  persisted owner after cache replacement; unknown ids remain not found.
- Reports live webhook session ids to daemon scope-drain inspection and clears
  them when the daemon default scope changes.
- Separate from the outbound `webhook` notification module.
- Inbound sessions use configured autonomy explicitly. Missing
  session-autonomy config is a route-boundary error, not a hidden fallback.
- `handler.ts` owns types, helpers, source resolution, and request handling.
- `index.ts` owns the module definition and route registration.

Handler tests supply only configuration, event/log and agent-session ports.
Share the request/response boundary fixture across parsing and source-routing
scenarios; module contribution checks use the production loader. Keep source
continuity here, while workflow and domain lifecycle decisions stay downstream.
