---
name: thin-client-headless-server-split
description: Let the same Electron desktop app run EITHER as an all-in-one (local server embedded in main process) OR as a thin client against a remote headless server, by routing every RPC through a WsRpcClient that can point locally or remotely.
category: architecture
version: 1.0.0
version_origin: extracted
tags: [electron, architecture, headless-server, thin-client, websocket]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/server-core/src
imported_at: 2026-04-18T00:00:00Z
---

# Thin-client + headless-server split with one codebase

## When to use
- Desktop app where some users want "it just works locally" and others want "let me run the heavy stuff on a VPS and only render the UI on my laptop".
- Long-running agent sessions that should survive laptop sleep/restart by living on a server.
- You'd like to ALSO expose the same RPC layer as a web UI.

## How it works
1. Extract all session + agent logic into a `server-core` package: bootstrap, transport, RPC handlers, session manager, platform-services interface.
2. In the Electron main process, `bootstrapServer({ host: '127.0.0.1', port: 0, ... })` starts an in-process `WsRpcServer` on a random loopback port.
3. Renderer connects via `WsRpcClient` - to a URL that is EITHER the locally-started server OR a remote `wss://` URL passed in `CRAFT_SERVER_URL` env.
4. **Thin-client detection**: if `CRAFT_SERVER_URL` is set, skip the embedded server startup; otherwise run local.
5. Extra piece: a `@craft-agent/server` package exposes the same `bootstrapServer` as a standalone `bun run` entry point — that's the headless server users SSH into.
6. Optional Web UI: `server-core/webui` serves static Vite assets + a `/api/auth` login (JWT cookie signed with the server token). Same WsRpcServer accepts both native-app WebSocket handshakes AND cookie-authenticated browser WebSocket upgrades.
7. A `PlatformServices` interface is the ONLY thing that differs between Electron and headless — image processing, OS keychain, shell integration. Inject via `applyPlatformToSubsystems(platform)` at bootstrap.

## Example
```ts
// Electron main
const instance = await bootstrapServer({
  bundledAssetsRoot, serverVersion, tls: undefined,
  createSessionManager: () => new SessionManager(),
  applyPlatformToSubsystems: (p) => { setSearchPlatform(p); setImageProcessor(p.imageProcessor); },
  registerAllRpcHandlers: registerCoreRpcHandlers,
});
connectRenderer(instance.url, instance.token);
```

```ts
// Headless entrypoint (packages/server/src/index.ts)
await bootstrapServer({ /* same args */, tls, httpHandler: webuiHandler });
console.log(`CRAFT_SERVER_URL=${url}`);
console.log(`CRAFT_SERVER_TOKEN=${token}`);
```

## Gotchas
- Keep RPC contracts typed in a shared `@craft-agent/shared/protocol` package so client + server can't drift.
- Platform differences must be behind an interface - no `if (isElectron)` in `server-core` or you've broken the abstraction.
- For local mode you still want TOKEN auth on the loopback socket so other local processes can't hijack sessions.
- Use a random loopback port in local mode (`CRAFT_RPC_PORT=0`) and emit the URL line - the renderer reads it the same way a CLI does.
- Feature parity tests (headless vs Electron) should run against the SAME RPC handlers, with a mock `PlatformServices`.
