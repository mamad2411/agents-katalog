---
name: streamdeck-system-devices
description: 'Stream Deck system + devices namespaces: streamDeck.system.openUrl, system wake (onSystemDidWakeUp), deep linking (streamdeck://plugins/message/<UUID> active vs passive), onDidReceiveDeepLink, application monitoring (onApplicationDidLaunch/onApplicationDidTerminate + manifest.ApplicationsToMonitor), device events (onDeviceDidConnect/Change/Disconnect), device type enum (0–13), per-device action access. USE FOR: opening a URL in the user browser, restoring connections after sleep, receiving streamdeck:// deep-link messages, IPC between local apps via deep link, monitoring app launch/terminate (OBS, Spotify, Wave Link), enumerating connected Stream Decks, reacting to a device being unplugged.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "devices", "deep-linking", "system-events"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — System & Devices

> **Prerequisite:** `streamdeck-general` (runtime architecture and the
> `src/plugin.ts` entry point). Most handlers here register at the
> plugin scope, not inside an action class.

## Purpose

The `streamDeck.system` and `streamDeck.devices` namespaces are the
plugin's window into the host OS and connected hardware. This skill
covers every event and command they expose:

- `streamDeck.system.openUrl(url)` — open in user's default browser
- `streamDeck.system.onSystemDidWakeUp(...)` — restore connections after sleep
- `streamDeck.system.onDidReceiveDeepLink(...)` — receive `streamdeck://` messages
- `streamDeck.system.onApplicationDidLaunch/Terminate(...)` — react to monitored apps
- `streamDeck.devices.onDeviceDidConnect/Change/Disconnect(...)` — device lifecycle

For OAuth — which composes `openUrl` + `onDidReceiveDeepLink` + global
settings into a sign-in flow — load `streamdeck-oauth` instead, which
goes end-to-end.

---

## 1. `streamDeck.system.openUrl`

Opens a URL in the user's default browser.

```ts
import streamDeck from "@elgato/streamdeck";

await streamDeck.system.openUrl("https://elgato.com");
```

| Rule | Notes |
|---|---|
| `https://` and `http://` only | Custom schemes (e.g. `my-app://`) are NOT supported through this API. To deep-link into another app, the OS handles it — just don't expect `openUrl("my-app://...")` to work everywhere. |
| Opens in the **default** browser | Not configurable. |
| Async, fire-and-forget | The promise resolves when Stream Deck dispatched the open, not when the browser finished loading. |

Common uses:

- Send the user to your support page (`SupportURL` already does this on
  the actions list, but you may want a runtime "Help" button).
- Launch an OAuth authorize URL — see `streamdeck-oauth`.
- Open the user's settings page on a SaaS dashboard.

---

## 2. `streamDeck.system.onSystemDidWakeUp`

Fires once when the host machine resumes from sleep/hibernate. Also,
`onWillAppear` fires for every visible action shortly after. Use
`onSystemDidWakeUp` for **plugin-global** restoration (re-open
WebSockets, re-acquire OAuth tokens) and `onWillAppear` for per-action
re-rendering.

```ts
streamDeck.system.onSystemDidWakeUp(() => {
  streamDeck.logger.info("System woke up — reconnecting upstream");
  reconnectWebSocket();
  refreshAllVisible();
});
```

> ⚠️ This event fires **only in the plugin runtime**, not in the
> property inspector. Don't try to listen from a PI script.

---

## 3. Deep linking — `streamdeck://plugins/message/<UUID>`

Stream Deck registers a `streamdeck://` URL scheme with the OS. Anyone
on the user's machine (browser, OS shortcut, another app) can fire a URL
of this shape and your plugin will receive it:

```
streamdeck://plugins/message/<PLUGIN_UUID>[/path][?query][#fragment]
```

### Receiving

```ts
streamDeck.system.onDidReceiveDeepLink((ev) => {
  const { path, fragment, searchParams } = ev.url;   // URL instance
  streamDeck.logger.info("deep-link", { path, fragment, search: ev.url.search });
});
```

The hostname/prefix (`streamdeck://plugins/message/<UUID>`) is stripped.
You see only the path/query/fragment.

### Active vs passive

| Trait | Active (default) | Passive |
|---|---|---|
| URL form | `streamdeck://plugins/message/<UUID>/anything` | `…?streamdeck=hidden` |
| Brings Stream Deck window to front | ✓ | ✗ |
| Stream Deck app version required | 6.5+ | 7.0+ |
| Recommended for | OAuth callbacks; any flow where the user needs to see Stream Deck next | Silent setup messages from a companion app (e.g. "here is the port my IPC server is listening on") |

```
streamdeck://plugins/message/com.x.y/oauth/callback?code=...           ← active
streamdeck://plugins/message/com.x.y/ipc?port=1234&streamdeck=hidden    ← passive
```

### Limits and warnings

| Limit | Value |
|---|---|
| Max URL length | ~2,000 characters total. For larger payloads use a local WebSocket between the companion app and the plugin. |
| Remote access | Local-only. You can't deep-link a plugin from a remote machine. |
| Provider compatibility | Many OAuth providers (Google, Microsoft, Spotify) reject custom URI schemes as callback URLs — for those, route through the Elgato proxy. See `streamdeck-oauth`. |

> ⚠️ **Treat deep-link input as untrusted.** Any process on the machine
> can fire URLs at your plugin. Validate `path`, validate any tokens
> (e.g. CSRF `state`), and never blindly execute commands from a
> deep-link payload.

### Testing deep links

```pwsh
# Windows: Win+R, paste, Enter
streamdeck://plugins/message/com.yourhandle.hello-world/test?x=1

# Or, on any OS: paste into a browser address bar
```

---

## 4. Application monitoring

Tells your plugin when a specific app launches or quits — useful to
toggle action icons or auto-connect when, say, OBS opens.

### Manifest (declare what to watch)

```jsonc
"ApplicationsToMonitor": {
  "mac":     ["com.obsproject.obs-studio", "com.spotify.client"],
  "windows": ["obs64.exe",                  "Spotify.exe"]
}
```

How to find the identifier:

| OS | Identifier | How to find |
|---|---|---|
| Windows | exe name | Task Manager → Details tab → "Name" column |
| macOS | bundle id | `mdls -name kMDItemCFBundleIdentifier /Applications/<App>.app` |

### Plugin handlers

```ts
streamDeck.system.onApplicationDidLaunch((ev) => {
  streamDeck.logger.info("launched", ev.application);
  if (ev.application === "Spotify.exe" || ev.application === "com.spotify.client") {
    void streamDeck.actions.forEach((a) => void a.setTitle("Spotify ✓"));
  }
});

streamDeck.system.onApplicationDidTerminate((ev) => {
  streamDeck.logger.info("terminated", ev.application);
});
```

Only apps you've declared in `ApplicationsToMonitor` are reported. The
event fires **once per launch / quit**, not for already-running
processes when Stream Deck starts.

---

## 5. Devices

A "device" is one piece of Stream Deck hardware (or Mobile, or Virtual).
A single user can have several connected at once; your plugin sees all
of them.

### Events

```ts
streamDeck.devices.onDeviceDidConnect((ev) => {
  const { id, isConnected, name, size, type } = ev.device;
  streamDeck.logger.info("connect", { id, name, type, size });
});

streamDeck.devices.onDeviceDidChange((ev) => {       // Stream Deck app 7.0+
  // E.g. user renamed the device, or the size changed (Mobile)
});

streamDeck.devices.onDeviceDidDisconnect((ev) => {
  streamDeck.logger.info("disconnect", ev.device.id);
});
```

> ⚠️ A disconnected device's actions are still **registered** with
> Stream Deck (they re-appear when the user plugs it back in). Don't
> tear down per-action state on `disconnect` — wait for `onWillDisappear`
> on the individual actions if you need per-instance cleanup.

### `ev.device.type` integer table

| Value | Device |
|---|---|
| 0 | Stream Deck (original / MK.2) |
| 1 | Stream Deck Mini |
| 2 | Stream Deck XL |
| 3 | Stream Deck Mobile |
| 4 | Corsair GKeys |
| 5 | Stream Deck Pedal |
| 6 | Voyager |
| 7 | Stream Deck + |
| 8 | SCUF Stream Deck |
| 9 | Stream Deck Neo |
| 10 | Stream Deck Studio |
| 11 | Virtual Stream Deck |
| 12 | Galleon |
| 13 | Stream Deck Plus XL |

(Same table as `streamdeck-manifest` → `Profile.DeviceType` — the
manifest profile field uses the same integers.)

### Inspecting all known devices

```ts
for (const device of streamDeck.devices) {
  streamDeck.logger.debug(device.name, device.type, device.size);
}
```

### Inside an action — access the owning device

```ts
override onKeyDown(ev: KeyDownEvent) {
  const device = ev.action.device;
  streamDeck.logger.info(`pressed on ${device.name} (type=${device.type})`);
}
```

---

## 6. Restoring after sleep / device unplug — the resilience pattern

A robust plugin survives the user closing the lid, switching docks, and
hot-plugging hardware. Wire it like this:

```ts
import streamDeck from "@elgato/streamdeck";

let upstreamSocket: WebSocket | null = null;

function connectUpstream() {
  upstreamSocket?.close();
  upstreamSocket = new WebSocket("ws://localhost:8080");
  upstreamSocket.addEventListener("open",  () => refreshAllVisible());
  upstreamSocket.addEventListener("close", () => setTimeout(connectUpstream, 1000));
}

streamDeck.system.onSystemDidWakeUp(() => connectUpstream());
streamDeck.devices.onDeviceDidConnect(() => refreshAllVisible());

function refreshAllVisible() {
  streamDeck.actions.forEach((a) => void a.setTitle("ok"));
}

connectUpstream();
streamDeck.connect();
```

Rules:

- Reconnect from `onSystemDidWakeUp` (sleep) AND on socket `close`
  (transient drops).
- Re-render on `onDeviceDidConnect` (the device's `onWillAppear` will
  also fire, but a plugin-wide refresh is cheap insurance).
- Don't tear down per-action state on disconnect — the device may come
  back.

---

## 7. Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `openUrl("my-app://...")` does nothing | Custom schemes not supported by `openUrl` | Use OS-specific APIs or `child_process.exec(...)`; or trigger the other app via OAuth-style flow |
| Deep-link fires Stream Deck but plugin handler doesn't run | Handler not registered before `streamDeck.connect()`, or wrong UUID in URL | Register at plugin scope before connect; verify the `<UUID>` in the URL matches `manifest.UUID` |
| `state mismatch` in OAuth on plugin restart | `pending` map cleared at restart; user finished sign-in in the browser after | Expected — re-prompt sign in (or persist `pending` in global settings) |
| `onApplicationDidLaunch` never fires | App's bundle id / exe name typoed in manifest | macOS: `mdls -name kMDItemCFBundleIdentifier`. Windows: Task Manager → Details → "Name" |
| `onDeviceDidChange` doesn't fire | User has Stream Deck app < 7.0 | Bump `manifest.Software.MinimumVersion >= "7.0"` if you rely on it |
| Plugin loses connection after sleep | Not handling `onSystemDidWakeUp` | Reconnect in the handler |
| Deep-link payload corrupts when it contains special characters | Not URL-encoded by the sender | `encodeURIComponent` everything; decode via `URL` API on receipt (already done by `ev.url`) |
| `streamDeck.system.onDidReceiveDeepLink` is `undefined` | Older SDK (`@elgato/streamdeck` v1) — deep-link API was added in v2 | Upgrade the npm package |

---

## See Also

- System guide: <https://docs.elgato.com/streamdeck/sdk/guides/system>
- Deep-Linking guide (incl. URL Builder): <https://docs.elgato.com/streamdeck/sdk/guides/deep-linking>
- App Monitoring guide: <https://docs.elgato.com/streamdeck/sdk/guides/app-monitoring>
- Devices guide: <https://docs.elgato.com/streamdeck/sdk/guides/devices>
- Sibling skills: `streamdeck-oauth` (composes openUrl + deep link),
  `streamdeck-actions` (per-action lifecycle on connect/disconnect),
  `streamdeck-manifest` (declaring `ApplicationsToMonitor`)
