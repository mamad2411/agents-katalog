---
description: "Spring Boot WebSocket/STOMP contract for endpoints, destinations, CORS origins, session tracking, and socket controllers."
globs: "**/pom.xml,**/src/main/resources/application*.yml,**/src/main/resources/application*.yaml,**/*Socket*.java,**/*WebSocket*.java,**/websocket/**/*.java"
alwaysApply: false
---

# Spring Boot WebSocket Contract

These rules apply when an application uses WebSocket/STOMP messaging.
Architecture owns `<Feature>SocketController` naming. REST JSON APIs stay in the
controller contract. Thymeleaf owns browser page UI. HTTP Security stays in the
Security contract; do not invent a partial STOMP-auth story here unless the
product explicitly requires it.

Applications that expose WebSocket/STOMP must meet this contract.

## Dependency and protocol

- Add `spring-boot-starter-websocket` when the application needs real-time
  bidirectional messaging.
- Prefer **STOMP over WebSocket** for application messaging (chat, live updates,
  push notifications).
- Do not introduce raw JSR-356 `@ServerEndpoint` handlers unless the product
  explicitly requires them.
- Keep a one-line purpose comment above the dependency (pom contract).

## Endpoint and destinations

- Register a STOMP endpoint (commonly `/ws`).
- Enable SockJS on that endpoint when browser clients need transport fallback
  (`withSockJS()`).
- Use `/app` as the application destination prefix for client → server sends.
- Use a simple broker with `/topic` for broadcasts (and `/queue` when
  point-to-point destinations are required).
- Prefer the simple in-memory broker for single-instance apps. Do not add an
  external STOMP broker unless the product needs multi-instance fan-out.

## Controllers and flow

- Name STOMP message handlers `<Feature>SocketController` and annotate them with
  `@Controller` (architecture contract).
- Keep socket controllers thin: accept the payload, call a service interface,
  return or route the result. Do not put business rules in the socket
  controller.
- Use `@MessageMapping` for inbound application destinations and `@SendTo` (or
  messaging templates) for broadcasts.
- Optional HTTP status endpoints related to the same feature use normal REST
  naming (`<Feature>RestController`), not `*SocketController`.

## Allowed origins (CORS)

- Bind allowed origins through validated `@ConfigurationProperties` (for example
  `app.websocket.allowed-origins`).
- Never commit `*` as an allowed origin in shared/base or production
  configuration.
- In `application-development.yml`, list explicit local origins (scheme, host,
  and port), such as the browser client origin.
- In `application-production.yml`, load concrete origins from environment
  variables or an external secret/config source (configuration contract).
- If the resolved origin list is empty, fail closed: do not fall back to `*`.
  Refuse to start or refuse to register the STOMP endpoint until origins are
  configured.
- Prefer `setAllowedOriginPatterns` with the configured list over deprecated
  APIs when configuring the endpoint.

## Session lifecycle

- When the product needs connection counts, presence, or cleanup, listen for
  `SessionConnectEvent` / `SessionConnectedEvent` and `SessionDisconnectEvent`
  and track session IDs in a dedicated component.
- To force-disconnect a client, keep the raw `WebSocketSession` (for example via
  a transport decorator) and close it with an explicit `CloseStatus`.
- Prefer STOMP heartbeats on the simple broker when idle/dead clients must be
  detected without waiting for TCP timeout.
- Do not invent vanity session metrics beyond what the product uses.

## Client applications

- Keep the browser client’s server WebSocket URL in `@ConfigurationProperties`.
- Keep user-visible client UI text in i18n bundles (i18n / Thymeleaf contracts).
- Document connect → subscribe → send → receive → disconnect as the expected
  client lifecycle.

## Forbidden

- Never use raw `@ServerEndpoint` by default when STOMP fits the product.
- Never leave production WebSocket origins as `*`.
- Never fall back to `*` when the configured origin list is empty.
- Never put business logic in a `*SocketController`.
- Never name a REST status endpoint `*SocketController`.
- Never hardcode remote WebSocket URLs in Java or JavaScript when they belong in
  configuration properties.
