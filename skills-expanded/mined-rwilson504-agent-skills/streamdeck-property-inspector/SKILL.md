---
name: streamdeck-property-inspector
description: 'Stream Deck property inspector (PI) UI: HTML in *.sdPlugin/ui/, sdpi-components web components (sdpi-item / textfield / select / checkbox / range / file / password / color / button etc.), streamDeckClient (setSettings, getSettings, send, onDidReceiveSettings, onSendToPlugin), action vs global settings, sending sendToPropertyInspector from plugin, debugging at localhost:23654, security (never store secrets in action settings — use global). USE FOR: building an action configuration UI, sdpi-components, web components for PI, settings persistence patterns, plugin↔PI messaging, secure token storage, PI ↔ plugin handshake on open, dropdowns populated from plugin (e.g. fetched device list), zod validation of settings.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "property-inspector", "sdpi-components", "ui", "settings"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — Property Inspector (UI) + Settings

> **Prerequisite:** Load `streamdeck-general` first to understand the
> two-runtime model. The property inspector is the **Chromium** half of
> a plugin — separate from the Node.js plugin code. This skill covers
> the PI HTML, the `sdpi-components` library, the messaging contract
> between PI and plugin, and the settings APIs on both sides.

## Purpose

When a user selects an action in the Stream Deck app, the right pane
shows the action's *property inspector* — an HTML view where they
configure the action. This skill is how to build that view:

- File layout, manifest wiring, opening it for debug
- `sdpi-components` (Elgato's web-component library) — every component,
  with snippets
- The `streamDeckClient` API the PI calls from inside the WebView
- The `onSendToPlugin` / `sendToPropertyInspector` handshake
- Action settings vs. global settings — and why **secrets always go in
  global settings**
- Runtime-safe settings types with Zod

The runtime side (action classes, lifecycle events) lives in
`streamdeck-actions`.

---

## 1. File layout & wiring

```
<UUID>.sdPlugin/
├── manifest.json
└── ui/
    ├── sdpi-components.js          ← vendored UI library (recommended)
    └── <action-slug>.html          ← one HTML file per action's PI
```

Manifest wires the PI to its action:

```jsonc
{
  "Actions": [
    {
      "UUID": "com.yourhandle.hello-world.greet",
      "Name": "Greet",
      "PropertyInspectorPath": "ui/greet.html",
      "States": [{ "Image": "imgs/actions/greet/key" }]
    }
  ]
}
```

Or define a **plugin-level** PI used by any action without its own:

```jsonc
{
  "PropertyInspectorPath": "ui/default.html",
  "Actions": [
    { "UUID": "com.x.y.action-a", "Name": "A", "Icon": "...", "States": [...] }
    // ↑ uses ui/default.html unless it sets PropertyInspectorPath
  ]
}
```

---

## 2. The `sdpi-components` library

Don't roll your own. The Elgato-provided `sdpi-components` library is
the same one Elgato's own plugins use; it handles styling, the
plugin↔PI handshake, and settings persistence with zero ceremony.

### Installing (local — recommended)

Download <https://sdpi-components.dev/releases/v4/sdpi-components.js>
into your `ui/` folder. Vendoring it locally means the PI works without
internet access and the user can't be MITM'd by a CDN compromise.

Reference it:

```html
<script src="sdpi-components.js"></script>
```

### Installing (remote)

```html
<script src="https://sdpi-components.dev/releases/v4/sdpi-components.js"></script>
```

Faster to set up; depends on network access.

---

## 3. Minimum viable property inspector

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="sdpi-components.js"></script>
  </head>
  <body>
    <sdpi-item label="Greeting">
      <sdpi-textfield setting="greeting" placeholder="Hello"></sdpi-textfield>
    </sdpi-item>
  </body>
</html>
```

That's it. `setting="greeting"`:

- Reads the current value from the action's settings on PI open.
- Writes back to action settings on every change (debounced).
- Triggers `onDidReceiveSettings` in your action class.

### `sdpi-item` is the layout primitive

Every form row is wrapped in `<sdpi-item label="…">`. This gives you
the consistent two-column layout (label on the left, control on the
right) that Stream Deck users expect.

---

## 4. Component catalog

Every component supports `setting="…"` for automatic action-settings
binding (or `global-setting="…"` for global settings). Pass `disabled`,
`required`, `placeholder` where they make sense.

| Component | Tag | When to use |
|---|---|---|
| Button | `<sdpi-button>` | Trigger actions like "Refresh devices" or "Sign in". Hook `click` with JS. |
| Calendar | `<sdpi-calendar type="date">` | Pick a date. `type="datetime-local" \| "month" \| "time" \| "week"`. |
| Checkbox | `<sdpi-checkbox>` | Single boolean. |
| Checkbox list | `<sdpi-checkbox-list>` | Multiple booleans. Items via `<sdpi-option>`. |
| Color | `<sdpi-color>` | Color picker, stored as `#rrggbb`. |
| Delegate | `<sdpi-delegate>` | Generic — wrap a custom control and bind it to a setting. |
| File | `<sdpi-file>` | Pick a local file path. |
| Password | `<sdpi-password>` | Masked input. **Visual only — see warning below.** |
| Radio | `<sdpi-radio>` | One-of-many. Items via `<sdpi-option>`. |
| Range | `<sdpi-range>` | Slider with min/max/step. |
| Select | `<sdpi-select>` | Dropdown. Items via `<sdpi-option>` or dynamic data. |
| Textarea | `<sdpi-textarea>` | Multi-line text. |
| Textfield | `<sdpi-textfield>` | Single-line text. Supports `type="number"`. |

### Examples

```html
<sdpi-item label="Volume">
  <sdpi-range setting="volume" min="0" max="100" step="1" showLabels></sdpi-range>
</sdpi-item>

<sdpi-item label="Mode">
  <sdpi-select setting="mode">
    <sdpi-option value="off">Off</sdpi-option>
    <sdpi-option value="on">On</sdpi-option>
    <sdpi-option value="auto">Auto</sdpi-option>
  </sdpi-select>
</sdpi-item>

<sdpi-item label="Polling">
  <sdpi-checkbox setting="poll" label="Poll device every 5s"></sdpi-checkbox>
</sdpi-item>

<sdpi-item label="Color">
  <sdpi-color setting="color"></sdpi-color>
</sdpi-item>

<sdpi-item label="Log file">
  <sdpi-file setting="logPath"></sdpi-file>
</sdpi-item>
```

> ⚠️ **`<sdpi-password>` masks the input visually only.** It still
> persists to action settings (or global settings) as plain text. For
> *user-provided* API tokens, use `<sdpi-password global-setting="token">`
> — store in global settings, not action settings. For OAuth tokens,
> never use a textfield — use the OAuth flow (see `streamdeck-oauth`).

---

## 5. The `streamDeckClient` — for everything sdpi-components can't do

Inside the PI HTML you can drop down to imperative JS:

```html
<script src="sdpi-components.js"></script>
<script>
  const { streamDeckClient } = SDPIComponents;

  // Wait until the PI is connected to Stream Deck
  streamDeckClient.onConnected(async () => {
    // Read settings
    const { settings } = await streamDeckClient.getSettings();
    console.log("current settings:", settings);

    // Write settings (also triggers onDidReceiveSettings in the plugin)
    await streamDeckClient.setSettings({ greeting: "Hello" });

    // Listen for settings changes pushed from elsewhere
    streamDeckClient.onDidReceiveSettings((ev) => {
      console.log("settings now:", ev.settings);
    });

    // Send a message to the plugin (handled by plugin's onSendToPlugin)
    await streamDeckClient.send({ event: "getDevices" });

    // Receive messages from the plugin (sent via sendToPropertyInspector)
    streamDeckClient.onSendToPropertyInspector((ev) => {
      console.log("from plugin:", ev.payload);
    });
  });
</script>
```

### Global settings (for shared/secure values)

```js
const { settings } = await streamDeckClient.getGlobalSettings();
await streamDeckClient.setGlobalSettings({ apiKey: "abc" });
streamDeckClient.onDidReceiveGlobalSettings((ev) => { /* ... */ });
```

---

## 6. PI → plugin handshake — populating dynamic dropdowns

Pattern: you have a list of devices/playlists/channels that the *plugin*
knows about (via an API), and you want the PI to show them in a dropdown.

### Plugin side

```ts
import streamDeck, { action, SingletonAction,
  type PropertyInspectorDidAppearEvent,
  type SendToPluginEvent,
} from "@elgato/streamdeck";

type Payload = { event: "getDevices" };

@action({ UUID: "com.yourhandle.x.pick-device" })
export class PickDevice extends SingletonAction {
  override async onPropertyInspectorDidAppear(
    ev: PropertyInspectorDidAppearEvent,
  ): Promise<void> {
    const devices = await myApi.listDevices();
    await ev.action.sendToPropertyInspector({ event: "devices", devices });
  }

  override async onSendToPlugin(
    ev: SendToPluginEvent<Payload, unknown>,
  ): Promise<void> {
    if (ev.payload.event === "getDevices") {
      const devices = await myApi.listDevices();
      await ev.action.sendToPropertyInspector({ event: "devices", devices });
    }
  }
}
```

### PI side

```html
<sdpi-item label="Device">
  <sdpi-select id="device-picker" setting="deviceId"></sdpi-select>
</sdpi-item>

<script>
  const { streamDeckClient } = SDPIComponents;
  const picker = document.getElementById("device-picker");

  function fillPicker(devices) {
    picker.innerHTML = "";
    for (const d of devices) {
      const opt = document.createElement("sdpi-option");
      opt.setAttribute("value", d.id);
      opt.textContent = d.name;
      picker.appendChild(opt);
    }
  }

  streamDeckClient.onConnected(async () => {
    // Plugin pushes on PI open; also ask explicitly in case we missed it
    streamDeckClient.onSendToPropertyInspector((ev) => {
      if (ev.payload.event === "devices") fillPicker(ev.payload.devices);
    });
    await streamDeckClient.send({ event: "getDevices" });
  });
</script>
```

Idempotence matters: the user may close and re-open the PI several
times. Push on `onPropertyInspectorDidAppear` AND respond to the PI's
explicit request — covers both startup ordering races.

---

## 7. Action settings vs. global settings — the security divide

### Action settings (per-action instance)

```ts
type Settings = { greeting: string };

await ev.action.setSettings({ greeting: "Hi" });
const cur = await ev.action.getSettings<Settings>();
```

| ✔ Use for | ✘ Never use for |
|---|---|
| The user's display preference | API keys, OAuth tokens, passwords |
| Which device/channel/playlist this key targets | Anything the user wouldn't want in a backup |
| Cached values that can be re-fetched | PII / secrets |

**Why never secrets:** action settings travel with the action. When the
user exports a profile (e.g. to share with a friend), action settings go
with it. A leaked profile would leak every embedded secret.

### Global settings (plugin-wide)

```ts
type Global = { apiKey?: string; oauthToken?: string };

await streamDeck.settings.setGlobalSettings<Global>({ apiKey: "abc" });
const cur = await streamDeck.settings.getGlobalSettings<Global>();
```

| ✔ Use for | ✘ Don't use for |
|---|---|
| API keys (user-supplied) | Per-action preferences (use action settings) |
| OAuth access / refresh tokens | Anything the user picks per-button |
| Stream Deck-wide preferences for this plugin | Frequently-changing values (writes are not free) |

Stored locally on the user's machine in the Stream Deck app's settings
store. Not synced to any cloud service.

### Listening on either side

```ts
override onDidReceiveSettings(ev: DidReceiveSettingsEvent<Settings>): void {
  /* re-render using ev.payload.settings */
}
```

```ts
streamDeck.settings.onDidReceiveGlobalSettings<Global>((ev) => {
  /* react to global-settings change (e.g. user signed in) */
});
```

---

## 8. Runtime-safe settings with Zod (highly recommended)

Settings come back as `unknown`-shaped JSON. The TypeScript type is a
*claim*, not a guarantee. Wrap parsing in Zod to fail loudly when an
old version's settings shape doesn't match the new code:

```ts
import { z } from "zod";

const ActionSettings = z.object({
  greeting: z.string().default("Hello"),
  volume:   z.number().int().min(0).max(100).default(50),
});
type ActionSettings = z.infer<typeof ActionSettings>;

@action({ UUID: "com.x.y.greet" })
export class Greet extends SingletonAction<ActionSettings> {
  override async onWillAppear(ev: WillAppearEvent<ActionSettings>) {
    const settings = ActionSettings.parse(ev.payload.settings ?? {});
    await ev.action.setTitle(settings.greeting);
  }
}
```

When you migrate settings between versions, do the migration inside the
`.parse` call (or use a Zod `.transform`). The user's existing buttons
keep working.

---

## 9. Debugging the PI

1. Make sure `streamdeck dev` is enabled (default after `create`).
2. Open Stream Deck and select your action so its PI renders.
3. Visit <http://localhost:23654/> in a Chromium-based browser.
4. Find your PI in the list, click → DevTools opens with full Chrome
   tooling (Elements, Console, Sources, Network, debugger).

Tips:

- Wrap the PI body in `<script>console.log("PI opened")</script>` so
  you can confirm load order.
- Use `streamDeckClient.onDidReceiveSettings` console-logs to watch
  the round-trip on every keystroke.
- On the plugin side, log into the PI:

  ```ts
  streamDeck.ui.current?.sendToPropertyInspector({ debug: "ping" });
  ```

---

## 10. Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| PI doesn't appear in debug page list | Not visible in Stream Deck | Open the action in the app first |
| `setting="x"` doesn't persist | Typo or referencing a value that's not a string/number/bool | Settings are JSON-serialized; complex objects need explicit `streamDeckClient.setSettings` |
| Plugin doesn't receive PI messages | `streamDeck.connect()` never called, or handler not declared on the right action class | Connect at startup; messages route by UUID |
| Dropdown is empty on PI open | Plugin pushed devices before PI was connected | Push from `onPropertyInspectorDidAppear` AND respond to explicit `send` |
| Settings shape mismatch crashes the action | New version expects new fields | Zod-parse on read; migrate inside `.parse` |
| Password field "doesn't hide my secret" | Action settings are not encrypted | Use global settings; for OAuth, use `streamdeck-oauth` flow |
| `getSettings()` returns `{}` on first open | New action, no settings yet | Always default-coalesce: `ev.payload.settings.x ?? "default"` |

---

## See Also

- Official property inspector guide: <https://docs.elgato.com/streamdeck/sdk/guides/ui>
- Settings guide: <https://docs.elgato.com/streamdeck/sdk/guides/settings>
- sdpi-components: <https://sdpi-components.dev/>
- Stream Deck Client docs: <https://sdpi-components.dev/docs/helpers/stream-deck-client>
- Sibling skills: `streamdeck-actions` (the plugin-side counterpart),
  `streamdeck-oauth` (secure auth flow that USES global settings),
  `streamdeck-general` (runtime architecture)
