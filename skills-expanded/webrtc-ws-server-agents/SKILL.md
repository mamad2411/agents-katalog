# AGENTS.md

AI agent context file for the `webrtc-ws-server` project.

## Project Summary

A WebSocket-based WebRTC signaling server built with Node.js and TypeScript. It relays SDP offers/answers and ICE candidates between peers organized into rooms. All state is in-memory — no database or persistent storage.

## Tech Stack

- **Runtime:** Node.js 22 LTS+
- **Language:** TypeScript 5.7+ (ES2022 target, NodeNext modules, ESM)
- **Runtime dependency:** `ws` (WebSocket server)
- **Test framework:** Vitest
- **Linting:** ESLint 9 (flat config) + Prettier
- **Package manager:** npm

## Directory Structure

```
src/
  main.ts                 # Entrypoint: loads config, starts server, signal handlers
  config.ts               # Env var parsing → ServerConfig object
  types.ts                # All interfaces/types (messages, config, WebRTC stubs, errors)
  room-manager.ts         # RoomManager class: room state, join/leave, TTL sweep
  connection-handler.ts   # Message parsing, validation, dispatch, relay logic
  server.ts               # createServer() factory, heartbeat, graceful shutdown

tests/
  config.test.ts               # Unit: config defaults, env var parsing, edge cases
  room-manager.test.ts         # Unit: join, leave, removeAll, capacity, TTL, clear
  connection-handler.test.ts   # Unit: parseMessage, sendMessage, sendError, handleMessage, handleDisconnect
  server.test.ts               # Integration: full signaling flows over real WebSocket connections

eslint.config.js          # ESLint 9 flat config
vitest.config.ts          # Vitest configuration
tsconfig.json             # TypeScript config (ES2022, NodeNext, strict)
tsconfig.release.json     # Release build config (no sourcemaps, no comments)
```

## Commands

| Command | Purpose |
|---|---|
| `npm run build` | Compile TypeScript to `build/` |
| `npm run build:watch` | Compile in watch mode |
| `npm run build:release` | Clean build without sourcemaps/comments |
| `npm start` | Run the compiled server (`build/src/main.js`) |
| `npm test` | Run all tests once |
| `npm run test:watch` | Run tests in watch mode |
| `npm run lint` | Lint all files |
| `npm run lint:fix` | Auto-fix lint issues |
| `npm run clean` | Remove `build/` directory |

## Key Patterns & Conventions

- **ESM throughout** — `"type": "module"` in package.json; all imports use `.js` extensions
- **Factory pattern** — `createServer(config)` returns a `SignalServer` handle with `wss`, `rooms`, and `close()` for testability
- **Discriminated unions** — message types use `type` field as discriminant (`ClientMessage`, `ServerMessage`)
- **Immutable config** — `ServerConfig` is loaded once from env vars at startup
- **No global mutable state** — all state lives in `RoomManager` instances, making tests isolated
- **Error responses** — validation errors return `{ type: 'error', code, message }` to clients instead of dropping messages
- **JSDoc on all exports** — every exported function, class, interface, and type has JSDoc documentation

## Common Modification Points

- **Add a new message type:** Update `types.ts` (add interface + extend `ClientMessage` union + update `VALID_MESSAGE_TYPES`), then add a case in `connection-handler.ts` `handleMessage()` switch
- **Change default config:** Edit `DEFAULTS` in `config.ts`
- **Add a new env var:** Add to `DEFAULTS` and `loadConfig()` in `config.ts`, update `ServerConfig` in `types.ts`, update test configs
- **Adjust security limits:** Change defaults in `config.ts` or override via env vars (`MAX_ROOMS`, `MAX_ROOMS_PER_PEER`, `MAX_CONNECTIONS_PER_IP`, `MAX_KEY_LENGTH`)
- **Change room behavior:** Modify `RoomManager` in `room-manager.ts`
- **Change server lifecycle:** Modify `createServer()` in `server.ts`

## Testing Expectations

- All tests should pass with `npm test`
- Unit tests use mock `PeerSocket` objects (vi.fn() stubs for send/ping/close/terminate)
- Integration tests (`server.test.ts`) spin up real WebSocket servers on port 0 (random) and connect real clients
- Tests are isolated — each `describe` block creates/tears down its own `RoomManager` or `SignalServer`
- TTL sweep tests use `vi.useFakeTimers()` for deterministic timing

## WebSocket Protocol

See [README.md](README.md#websocket-protocol) for the full protocol reference including message formats, error codes, and a sequence diagram.
