---
name: trade-it-react
description: Implement Trade It partner integrations using either embedded React connect/trade modals or direct backend trading API calls. Use when asked to integrate @trade-it/react, request Trade It session URLs, connect brokerages such as Charles Schwab, read accounts or holdings, or create, execute, cancel, and monitor trades from a partner server without a Trade It modal.
---

# Trade It Partner Integration

## Overview

Use this skill to add Trade It to a partner application through either an embedded Trade It experience or the direct backend trading API.

Assume the user is (or is becoming) a Trade It partner and stores per-user Trade It access and refresh tokens server-side. If OAuth is not implemented, use Trade It's published authorization-server metadata and scaffold the callback, exchange, refresh, and storage boundaries without inventing credentials.

## Workflow

1. Select the integration path.
- Use the **backend-direct path** when the partner wants its own order UI and wants its server to create, execute, cancel, or monitor trades without opening a Trade It modal.
- Use the **embedded path** when the partner wants Trade It to render connect or trade UI with `@trade-it/react`.
- These paths can be combined: for example, use a hosted connect flow for brokerage linking and backend-direct calls for trading.
- Do not recommend `@trade-it/core` for backend trading. It contains framework-independent embedded URL, configuration, and event primitives; it is not an authenticated API client.

2. Establish server-side OAuth.
- Find the server-side boundary where the current user's stored Trade It access and refresh tokens can be accessed.
- Use Trade It's OAuth authorization-code flow with PKCE and a confidential partner client.
- Keep `client_secret`, access tokens, and refresh tokens on the server.
- Request only the scopes the integration needs. Backend trading commonly needs `brokerage:read`, `trade:read`, `trade:write`, and `tool:execute`.

3. Implement the selected path.

### Backend-direct path

- Read the [Trade It API overview](https://docs.tradeit.app/api) and every operation page needed for the implementation before writing the client.
- Use the [Trade It Postman collection](https://www.postman.com/trade-it/workspace/trade-it-apis/collection/5398302-70e1f409-c978-4701-a2fa-6f58b8b11932?action=share&source=copy-link&creator=5398302) as a runnable companion to the first-party documentation.
- Implement the exact published endpoint, request body, response, authentication, scopes, and safety behavior. Do not infer fields from the MCP transport or invent a separate API contract.
- Treat `create_trade` and `create_options_trade` as separate operations and follow their respective documentation pages.
- Keep all API calls and user tokens on the partner server.
- Present the normalized trade returned by a create operation in the partner's review UI. Execute only after the user approves that exact order, and cancel only after the user requests cancellation.
- Use the documented account, holdings, and trade-list operations for account selection and current state.
- After completing this path, skip the embedded-only steps 4–6 and validate the backend-direct result in step 7.

### Embedded path

- Confirm the app has a React frontend or a place where React can render the Trade It modal.
- Find the server-side boundary where the current user's stored Trade It token can be accessed.

4. Add a partner server route for session URLs.
- Create a server-side route in the partner app that accepts a local request for `connect` or `trade`.
- Read the current user's stored Trade It access token server-side.
- Call Trade It `POST <TRADE_IT_API_URL>/api/session/url` with `Authorization: Bearer <user trade it access token>`.
- Use request bodies:
  - `{ "target": "connect" }`
  - `{ "target": "connect", "brokerageId": <number> }`
  - `{ "target": "trade" }`
- Return the Trade It JSON response unchanged when possible.
- Add a `TRADE_IT_API_URL` env var if the app does not already have one. Default to `https://api.tradeit.app` if unavailable.
- Request a new session URL immediately before opening a modal. Do not cache or reuse it after its 30-minute expiry.

5. Add the client-side SDK integration.
- Install `@trade-it/react`.
- Render one shared `TradeItModal`.
- For connect flows:
  - fetch a connect URL from the partner server
  - call `tradeIt.openConnect({ launch: { mode: 'connect', url } })`
- For trade flows:
  - fetch a trade URL template from the partner server
  - call `tradeIt.openTrade({ launch: { mode: 'trade', url, config } })`

6. Map trade configuration correctly.
- Use SDK enums instead of hard-coded strings.
- Use full config property names (`tradeType`, `orderType`, `timeInForce`, `positionEffect`, etc.).
- Include `direction` for priced multi-leg orders. Use `OrderDirection.Even` only with a zero-price limit order.
- Use `takeProfit` and `stopLoss` only for simple Buy entries and represent their units with `TriggerUnit`.
- For options or multi-leg trades, use `tradeType: TradeType.MultiLeg` and provide `legs`.

7. Validate the finished integration.
- For backend-direct integrations: create returns a draft; execute uses that draft ID; cancel returns the latest trade state; tokens never reach browser code.
- For embedded integrations: the connect/trade modal opens in the requested mode, and missing or expired sessions recover by requesting a fresh session URL.

## Implementation Rules

- Never call Trade It session URL endpoints directly from browser code.
- Never call the backend tool-execution endpoint directly from browser code.
- Never expose `client_secret` in client-side code.
- Prefer returning the full `url` from the partner server rather than rebuilding URLs client-side.
- Keep route names and patterns idiomatic to the partner's stack.
- Reuse the partner's existing modal/state/fetch patterns where possible.
- If there is no trusted server-side source for the current user's Trade It token, stop and document that as the blocker.
- For a direct brokerage connection (e.g.Charles Schwab), use `brokerageId: 7`; omit `brokerageId` when the brokerage picker is preferred.

## Required Deliverables

When using this skill, produce:

- the server-side OAuth/token boundary
- for backend-direct integrations, typed server helpers for tool execution and the requested create/execute/cancel/status operations
- for embedded integrations, the server route that proxies session URL requests and client-side modal wiring
- any required env var additions
- a short note showing where the user's Trade It token must come from
- OAuth callback/token-storage scaffolding when the partner app does not already have it

## References

- Read `references/api-contract.md` for request/response shapes, session URL flows, and SDK launch patterns.
- For backend-direct integrations, use the first-party [Trade It API reference](https://docs.tradeit.app/api) as the source of truth and the [Postman collection](https://www.postman.com/trade-it/workspace/trade-it-apis/collection/5398302-70e1f409-c978-4701-a2fa-6f58b8b11932?action=share&source=copy-link&creator=5398302) for runnable examples.
- Read `references/trade-config.md` for `launch.config` fields, enums, and trade examples.
