---
name: rutis-remote-plugin
description: Use when a rutis plugin must run on another machine, device or app instead of next to the host — "remote plugin", running a Python/Node/Go/Swift plugin on a GPU box or a Mac, connecting two rutis hosts, exposing a phone app's capabilities to rutis. Walks through choosing a node link vs a remote runtime vs app hosting, writing the plugin in the rutis paradigm, deploying, configuring rutis.json, verifying, and the rules that keep it inside the rutis design. Self-contained; reference material is in references/.
---

# Adding a remote plugin to rutis

rutis (https://github.com/arcships/rutis) is a plugin host with a Rust core that takes plugins in several languages. This skill does not depend on the rutis repository; everything it refers to is in `references/`:

| File | Contents |
| --- | --- |
| `references/plugin-api.md` | The plugin API: declarations, ctx, events, lifecycle, how values cross, sync calls and reentrancy, cancellation, versions |
| `references/nodes.md` | Links, running plugins on another node, remote language runtimes, security |
| `references/rutis-json.md` | `rutis.json`: `runtimes` (`restart`), `listen`, `rows`, the connection rows `rutis-host/dial` / `rutis-host/listen`; exit status, live reload, when a runtime ends, credentials, deployment |

Keep one sentence in mind: **rutis has no such thing as a "remote plugin" — only an ordinary plugin plus a runtime, node or app that runs somewhere else, reached through a connection row.** The plugin code is exactly what it would be locally; what changes is where its runtime runs and how rutis reaches it. Do not write a separate plugin API, protocol or lifecycle for remote use.

## 1. Decide which kind it is

| What the other side is | Use | Row on the rutis side |
| --- | --- | --- |
| A language runtime on another machine; **this rutis** loads, configures, starts and stops its plugins | Remote runtime: a `rutis-host/dial` row (the runtime listens) | `<connection row>:<plugin>` |
| Another full rutis host that manages its own plugins and only shares services and events | Node: a `rutis-host/dial` row on one side, a `rutis-host/listen` row on the other | No new row; its services are seen here by name, and this side's there |
| Another full rutis host on which this side wants to run rows it writes | Node, as above | `<connection row>:<plugin>` |
| A phone or desktop app offering its own capabilities as plugins | App hosting (Swift and Kotlin apps): a `rutis-host/listen` row (the app dials in) or `rutis-host/dial` (the app listens) | None: the app installs its own plugins, which register as `<app id>:<plugin>` |

When unsure, ask one question: **who decides whether the plugin is loaded and with what configuration?** This rutis → remote runtime. The other side → app hosting (the app configures its plugins in `RutisApp`) or node link.

## 2. What works today (2026-10-19; check the repository before relying on it)

| Language | Remote listening `listen:` (rutis dials in) | Dialing out `dial:` (runtime connects to rutis) |
| --- | --- | --- |
| Python | ✅ | ✅ ([#383](https://github.com/arcships/rutis/issues/383)) |
| Node / TypeScript | ✅ | ✅ ([#384](https://github.com/arcships/rutis/issues/384)) |
| Go | ✅ | ✅ ([#384](https://github.com/arcships/rutis/issues/384)) |
| Bun | ✅ (#384) | ✅ (#384) |
| Swift (macOS plugin binaries) | ✅ ([#387](https://github.com/arcships/rutis/issues/387)) | ✅ ([#387](https://github.com/arcships/rutis/issues/387)) |
| Swift apps (plugins hosted in an iOS / iPadOS / macOS app, `RutisApp`) | ✅ ([#389](https://github.com/arcships/rutis/issues/389)) | ✅ ([#389](https://github.com/arcships/rutis/issues/389)) |
| Kotlin apps (plugins hosted in an Android app) | ✅ (jvm target) | ✅ |

One `rutis-host/listen` row takes any number of connections on one port (many devices): each is a session of its own, and what the far end provides registers as `<id>:<plugin>`. rutis 0.19 creates no instance per connection: logic computed once per device lives on the device, or a host plugin tells devices apart itself (step 4c). Rows `<connection row>:<plugin>` run only through `rutis-host/dial`: for a runtime whose plugins this rutis chooses, the runtime listens and rutis dials it.

## 3. Write the plugin: the paradigm, same as local

Details in `references/plugin-api.md`. The essentials:

- Write a leaf plugin with the language's SDK: declare `inject` (service names it uses) and a config schema; in `apply(ctx, config)` use `ctx.use` / `ctx.provide` / `ctx.effect`. What `ctx.provide` provides reaches rutis by itself (its public methods, all `async`); `provides` is optional, to mark methods `sync` and let `rutis-host check` know before running what the plugin provides. The current plugin API version is 3 (rutis 0.13: events with `ctx.on` and the five ways to emit, `emit` / `parallel` / `serial` / `waterfall` / `bail`, plus `filter`).
- A service of the host application's Rust code is used the same way, `ctx.use(name)`, once the host marks its type `#[rutis::service]` and provides it (from rutis 0.15; no binding to write on either side). An unmarked Rust service is not reachable: a row waiting for it is reported with the fix by the host (`Loader::waits`).
- The plugin does **not** decide when it runs, does not reconnect, does not probe whether the other side is up: it is applied when all its services are ready, stops when any is withdrawn, and starts again when it returns. A remote disconnect is, to the plugin, an ordinary stop.
- Values follow the cross-process rules: JSON-compatible data is copied; dates and times, binary data, maps, sets, big integers, decimals and UUIDs are copied and arrive as each language's own types (integers beyond ±(2^53−1) cross as big integers automatically); functions and objects go by reference; nesting at most 64 levels. Never assume the same process.
- Do not hold locks while calling other services: your service may be called again in the middle of your own synchronous call. Prefer `async` methods for calls that cross runtimes and may cross each other.
- Events are **one logical bus** across processes, languages and machines: `ctx.on` registers with the host by itself, and an event reaches every listener in the emitter's scope or above it, wherever that listener runs, with the same result as in one process. Nothing to declare for a remote runtime, an app or a node: a far node's listeners are entries of this bus too. `emit` never waits and a failing listener is only reported; use `parallel` to wait, `serial` / `waterfall` / `bail` for results. When the far end goes away its listeners leave the bus and calls in flight fail once (`BindingError`). Runtimes and nodes older than 0.19 cannot join a current host (refused by protocol version); upgrade every end together.
- Dependency declarations contain only service names, never languages, machines or addresses.

## 4. Deploy a remote runtime (listening, as of today)

On the remote machine:

1. **Install** the plugin there: Python `pip install` into the interpreter the runtime uses; Node `npm install` in the project; Bun `bun add` in the project; Go, build the binary; Swift (macOS), build the binary with `swift build` (its Info.plist linked in when the plugin uses calendars, contacts and the like: macOS asks the user on that machine, for that binary). A remote runtime loads only plugins already deployed there — **there is no code upload**.
2. Prepare TLS: non-loopback addresses must be `wss://`. Point `RUTIS_CERT` / `RUTIS_KEY` at the certificate and key; with a self-signed certificate, give the issuing CA to `RUTIS_CA` on the rutis side.
3. Set the token: `RUTIS_TOKEN` on the remote side, equal to `RUTIS_TOKEN_<ROW ID>` on the rutis side (the id of the `rutis-host/dial` row, uppercase, `-` as `_`).
4. Start it listening. `--id` is the id of the `rutis-host/dial` row on the rutis side, `--peer` is the `id` of the rutis that controls it:

   ```bash
   # Python
   RUTIS_TOKEN=… RUTIS_CERT=server.pem RUTIS_KEY=server.key \
     python -m rutis listen:wss://0.0.0.0:7443/rutis --id gpu --peer main /srv/plugins

   # Node (inside that machine's Node project)
   node node_modules/@arcships/rutis-runtime/src/runner.mjs listen:wss://0.0.0.0:7443/rutis --id gpu --peer main ./package.json

   # Bun (inside that machine's Bun project; rows `<connection row>:<module>`)
   bun --no-install --no-env-file node_modules/@arcships/rutis-bun/src/main.ts listen:wss://0.0.0.0:7443/rutis --id gpu --peer main .
   ```

   A Go or Swift plugin binary accepts `listen:wss://…` as its channel the same way.

   Every remote runtime (Python, Node, Bun, a Go or Swift binary) reports on stderr the address it actually bound: `rutis: listening on <address>`. With port 0 (`listen:ws://127.0.0.1:0/rutis`) the system picks a free port; a script or test reads it from this line instead of picking a port first and passing it on (another process can take that port before the runtime binds it). `rutis-host run` does the same for its listeners: `rutis-host: listening on <name> <address>`.

   The Python runtime also reports on stderr: when a session ends, `rutis: session ended (<reason>); waiting for a controller` (reason such as `heartbeat timeout`, `connection lost`, `closed (1000): …`), or `rutis: session ended (replaced by a new connection)` when a new connection takes over.

## 4b. Or let the runtime connect in (dialing out)

When the remote machines are behind NAT or change address, the runtime connects to rutis instead. In 0.19 a far end that connects in brings only the plugins it installed itself and provides (apps, step 4c); rows `<connection row>:<plugin>` do not run on it, so for a language runtime whose plugins rutis chooses, prefer step 4. On the remote machine, with the plugins installed:

```bash
# Python
RUTIS_TOKEN=… RUTIS_CA=ca.pem \
  python -m rutis dial:wss://main.example.com:7443/rutis --id worker-1 --peer main /srv/plugins

# Node (inside that machine's Node project)
RUTIS_TOKEN=… RUTIS_CA=ca.pem \
  node node_modules/@arcships/rutis-runtime/src/runner.mjs dial:wss://main.example.com:7443/rutis --id worker-1 --peer main ./package.json

# Bun (inside that machine's Bun project)
RUTIS_TOKEN=… RUTIS_CA=ca.pem \
  bun --no-install --no-env-file node_modules/@arcships/rutis-bun/src/main.ts dial:wss://main.example.com:7443/rutis --id worker-1 --peer main .

# Go or Swift: the plugin binary takes the same channel, flags and environment
RUTIS_TOKEN=… RUTIS_CA=ca.pem \
  ./weather dial:wss://main.example.com:7443/rutis --id worker-1 --peer main .
```

- `--id` is the id this connection gives in its handshake (`[a-z0-9-]+`, unique per process: two processes with one id keep replacing each other); what it provides registers as `<id>:<plugin>`; `--peer` is the rutis `id`. `RUTIS_CA` is needed only for a self-signed certificate on the rutis side.
- It reconnects by itself: backoff 0.5 s doubling to 30 s; a refused token (401 / 403, or 4003 from the handshake's check) every 30 s; an incompatible protocol stops it (exit status 1). Each disconnect unloads its rows; each reconnection is a new session. SIGTERM / Ctrl-C stops it for good. It reports on stderr: `rutis: connected to …`, `rutis: connection lost (…); retrying in …`, `rutis: refused: auth-rejected (…)`, `rutis: refused: incompatible (…); stopping`.
- The rutis side: a `listen` entry and one `rutis-host/listen` row naming it. The token is `RUTIS_TOKEN_<ROW ID>` there (`RUTIS_TOKEN_WORKER` below):

  ```json
  {
    "id": "main",
    "listen": [{ "name": "public", "address": "0.0.0.0:7443", "cert": "server.pem", "key": "server.key" }],
    "rows": [{ "id": "worker", "name": "rutis-host/listen", "config": { "listener": "public" } }]
  }
  ```

  Every connection is a session of its own; a newer connection with the same id replaces the older (the older's plugins all unload, then it is closed with 4002, then the newer's plugins register). rutis prints `worker: connected worker-1`, `worker: disconnected worker-1 (connection lost)`, `worker: disconnected worker-1 (replaced by a new connection)`.

## 4c. Or host the plugins in an app (Swift: iOS, iPadOS, macOS)

The plugins are compiled into the app (the Swift package `https://github.com/arcships/rutis`, product `Rutis`; Kotlin: the `rutis` library). **The app installs its own plugins**, with the configurations given in `RutisApp(configs: …)` (a plugin without one gets its schema's defaults), and announces their services once connected; they register on rutis as `<app id>:<plugin>` (`kim-iphone:health`). The rutis side is one `rutis-host/listen` row as in 4b; nothing about the app's plugins is written in rutis.json.

```swift
let rutis = RutisApp(plugins: [health, device], configs: ["device": DeviceConfig(installation: "kim-iphone")],
                     connect: "wss://main.example.com:7443/rutis",
                     id: "kim-iphone", token: token)   // optional: peer:, trust: [SecCertificate], shutdownTimeout:, log:
try await rutis.start()   // returns once dialing started; reconnects by the 4b rules until stop()
await rutis.stop()        // unloads every plugin (latest first), then disconnects; start() may follow
// rutis.state: .stopped(reason:) / .connecting / .connected — Observable, and rutis.states (AsyncStream)
```

- When to start and stop is the app's business (on iOS, typically start in the foreground and stop on entering the background); a suspended app is, to rutis, a lost connection: its remote plugins unload and their users stop.
- A plugin in the app that fails to install (config not matching its schema, `apply` throwing, a service name rutis already has) is written only in the app's log (`log:` / `System.err`) in 0.19; rutis prints nothing: the plugin simply does not appear.
- Two devices providing one service name: the later one is refused (kernel rule). For logic once per device, either put it in the app, or name the device's services `health-<device>` and have a host plugin listen to `rutis/service`: on `available: true` for `health-<device>` it calls the `rutis/loader` service, `loader.create({id: "coach-<device>", name: "py:coach-one", config: {device}, inject: ["health-<device>"]})`, and `loader.remove("coach-<device>")` on `available: false` — in the event handler, not in `apply`.
- Permissions (HealthKit, location, contacts) belong to the app: entitlements and usage descriptions in the app; a denial is an error the plugin throws, which reaches the caller.
- Connecting to a local-network address asks the user for the local network permission (`NSLocalNetworkUsageDescription` in Info.plist); until allowed, the app keeps retrying.
- A device at a fixed address can listen instead: `RutisApp(plugins:, configs:, listen: "wss://0.0.0.0:7443/rutis", id:, token:, certificate: <SecIdentity>)`, dialed from rutis by a `rutis-host/dial` row (step 5); it installs its own plugins the same way.
- Guides: https://github.com/arcships/rutis/blob/main/docs/guide/swift-app.en.md, https://github.com/arcships/rutis/blob/main/docs/guide/kotlin-app.en.md

## 4d. Or bring your own connection

When the far end is reached by a way of connecting rutis does not ship (a relay, Bluetooth), write a connection plugin that hands the connection over as a session: in Rust `ctx.plugin(rutis_bridge::Session::new(channel))` (the host provides `rutis_bridge::LocalId` in the root ctx; rutis-host does), in other languages `ctx.use('rutis/sessions').open({ send, close })` with `inject: ['rutis/sessions']`. Details and a full example: [references/nodes.md](references/nodes.md#your-own-connection). The far end's plugins are then `<far id>:<plugin>` here; rows `<connection row>:<plugin>` run plugins there.

## 5. Configure the rutis side

Details in `references/rutis-json.md` and `references/nodes.md`.

```json
{
  "rows": [
    { "id": "gpu", "name": "rutis-host/dial", "config": { "address": "wss://gpu.example.com:7443/rutis" } },
    { "id": "embedder", "name": "gpu:embedder", "config": { "model": "small" } }
  ]
}
```

- One connection row per far end: `rutis-host/dial` (`address`; rutis dials it, backing off between attempts) or `rutis-host/listen` (`listener`; far ends dial in, step 4b / 4c). The row id names the connection: the runtime's `--id`, the token `RUTIS_TOKEN_<ROW ID>`, the prefix of the output lines. No language is written: plugin names are resolved on the far end. The connection is over WebSocket.
- Rows run on the far end are named `<connection row>:<plugin>`; the plugin is resolved on the remote machine, its config in the row.
- `runtimes.remote` (0.18) is removed in 0.19: it is an unknown field. Local runtimes (`runtimes.node` / `py` / `go` / `swift` / `bun`) are unchanged.
- A connection of your own (another transport, your own authentication): write a connection plugin that hands over a Channel: Rust `ctx.plugin(rutis_bridge::Session::new(channel))`; other languages call `open(far)` of the service `rutis/sessions` (see [Your own connection](references/nodes.md#your-own-connection)).

## 6. Verify

- `rutis-host check`: remote runtimes are not contacted during checking; services that might come from them are reported as such, not as failures.
- `rutis-host run`: expect `gpu: connected` (a listen row: `phone: connected <id>` per connection), then `<row id>: running`. `rutis-host status` lists them under `connections:` (`gpu: connected`; a listen row, the ids connected now: `phone: kim, lee`).
- `gpu: disconnected (auth-rejected: gpu.example.com:7443: upgrade refused with 403 Forbidden); retrying in 30s` means the token or certificate is wrong; `gpu: disconnected (incompatible: …); stopped` means the protocol does not match (the reason says which end to upgrade). On a listen row, a connection refused at the upgrade prints nothing on rutis: look at the dialing side. A row failing with `embedder: unresolved: entry "embedder" rejected: runtime gpu: this connection does not contain plugin embedder` names a plugin the remote side does not have.
- Stop the remote process: those rows stop, and so do the rows using their services; when it comes back rutis reconnects and loads them again.

## 7. What not to do

| Don't | Because |
| --- | --- |
| Implement reconnects, heartbeats or offline caches in the plugin to "keep the remote available" | Connections and lifecycle belong to rutis; a plugin only sees whether services are there |
| Upload code to a remote runtime or load plugins by path | A remote runtime loads only deployed plugins |
| Use `ws://` to a non-loopback address | Non-loopback needs TLS; the rutis dialer refuses it outright |
| Model "devices" or "identities" in the protocol or the plugin | Device information is a service some plugin provides; identity belongs to a future management service |
| Expect rutis to keep one copy of a host plugin per device | rutis creates no instance per connection (0.19): per-device logic lives on the device, or the host plugin tells devices apart by service name (`health-<device>`) |
| Write a separate plugin API for remote use, or make an SDK depend on Rust | The runtime side is implemented entirely in its platform language |
| Handle phone foreground/background or keep-alive in an SDK | That is the app's business logic; the SDK offers only `start` / `stop` |

## Further reading

- Remote plugins design: https://github.com/arcships/rutis/blob/main/docs/design-remote-plugins-2026-10-03.en.md
- Remote runtimes — dialing out and dynamic connections: https://github.com/arcships/rutis/blob/main/docs/design-remote-runtime-dial-2026-10-14.en.md
- App integration: https://github.com/arcships/rutis/blob/main/docs/design-app-integration-2026-10-14.en.md
