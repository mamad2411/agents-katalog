---
name: streamdeck-actions
description: 'Stream Deck action implementation: SingletonAction class, @action decorator, registering with streamDeck.actions, key actions (onKeyDown/onKeyUp, setImage, setTitle, setState, showOk/showAlert), dial actions (onDialDown/onDialRotate/onDialUp/onTouchTap, setFeedback, setFeedbackLayout, setTriggerDescription), multi-state toggles, multi-actions (userDesiredState), action lifecycle (willAppear → events → willDisappear), accessing visible actions. USE FOR: writing an action class, key press handlers, dial handlers, toggle action, multi-state action, multi-action behavior, setting key images dynamically, updating dial touch-strip feedback, showOk/showAlert visual feedback, iterating visible actions, sending sendToPropertyInspector.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "actions", "dials", "keypad", "typescript"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — Actions (Keys & Dials)

> **Prerequisite:** Load `streamdeck-general` first for the runtime
> model. This skill assumes you understand the `src/plugin.ts` entry
> point and the `*.sdPlugin/manifest.json` action declarations
> (see `streamdeck-manifest`).

## Purpose

Actions are the units of functionality the user wires onto a Stream Deck
key or dial. This skill covers the **runtime side** — the
`SingletonAction` class, the `@action` decorator, all lifecycle events,
the key-specific and dial-specific commands, and the patterns that show
up over and over (toggles, multi-actions, async refresh).

The manifest side (registering metadata, choosing controllers, declaring
states) is covered in `streamdeck-manifest`.

## Two action types: Key vs Encoder (Dial)

| Type | Hardware | Manifest `Controllers` | Events |
|---|---|---|---|
| Key | Buttons, pedals, G-Keys, Stream Deck Mobile | `["Keypad"]` | `onKeyDown`, `onKeyUp` |
| Encoder (Dial) | Stream Deck + dial **+** the slice of touch-strip it owns | `["Encoder"]` | `onDialDown`, `onDialUp`, `onDialRotate`, `onTouchTap` |
| Both | The user picks at placement time | `["Keypad", "Encoder"]` | All of the above |

A single `SingletonAction` subclass can handle both — implement only the
events the controller supports. Use `ev.action.isKey()` /
`ev.action.isDial()` to branch when needed.

---

## 1. The minimum viable action

`src/actions/greet.ts`:

```ts
import streamDeck, {
  action,
  SingletonAction,
  type KeyDownEvent,
  type WillAppearEvent,
} from "@elgato/streamdeck";

type Settings = {
  greeting?: string;
};

@action({ UUID: "com.yourhandle.hello-world.greet" })
export class Greet extends SingletonAction<Settings> {
  override onWillAppear(ev: WillAppearEvent<Settings>): Promise<void> {
    return ev.action.setTitle(ev.payload.settings.greeting ?? "Hello");
  }

  override async onKeyDown(ev: KeyDownEvent<Settings>): Promise<void> {
    const next = ev.payload.settings.greeting === "Hello" ? "World" : "Hello";
    await ev.action.setSettings({ greeting: next });
    await ev.action.setTitle(next);
  }
}
```

`src/plugin.ts`:

```ts
import streamDeck from "@elgato/streamdeck";
import { Greet } from "./actions/greet";

streamDeck.actions.registerAction(new Greet());
streamDeck.connect();          // ALWAYS LAST
```

### Key rules

1. **`@action({ UUID })`** must match the action UUID in the manifest exactly.
2. **One singleton per action UUID** — the SDK routes all instances of
   the action on every device to this one object.
3. **Register every action BEFORE `streamDeck.connect()`**. Calling
   connect first is the #1 cause of "actions just don't fire".
4. **Return the promise** from event handlers (or `await`) so the SDK
   knows when async work is done — important for `showOk` / `showAlert`
   semantics.

---

## 2. Action lifecycle

```
        ┌────────────────────────────────────────────────────┐
        │  action added to canvas / Stream Deck loads        │
        └────────────────────────────────────────────────────┘
                              │
                              ▼
                  onWillAppear  (one per device + slot)
                              │
       ┌──────────────────────┼────────────────────────┐
       │                      │                        │
       ▼                      ▼                        ▼
  user inputs            settings change          PI opens
  ─ onKeyDown            ─ onDidReceiveSettings   ─ onPropertyInspectorDidAppear
  ─ onKeyUp                                       ─ onSendToPlugin
  ─ onDialDown                                    ─ onPropertyInspectorDidDisappear
  ─ onDialUp
  ─ onDialRotate
  ─ onTouchTap
  ─ onTitleParametersDidChange
       │
       ▼
  onWillDisappear   (page changes, action removed, plugin stopping)
```

Every event handler receives `ev` with at least:

- `ev.action` — the typed action instance (`KeyAction` or `DialAction`)
  with commands like `setTitle`, `setSettings`.
- `ev.action.device` — the device this instance is on (`id`, `name`, `type`, `size`).
- `ev.payload.settings` — the current per-action settings (typed via the
  class generic).
- `ev.payload.controller` — `"Keypad"` or `"Encoder"`.
- `ev.payload.coordinates` — `{ column, row }` for keys, dials, etc.

### Events shared by both controllers

| Event | When | Notes |
|---|---|---|
| `onWillAppear` | Action becomes visible (page load, device connect, plugin start) | Initialize visual state here. Fires once per visible instance. |
| `onWillDisappear` | Action becomes hidden | Persist anything you must; this is your cleanup hook. |
| `onDidReceiveSettings` | Settings changed (by PI or by `setSettings`) | Re-render on settings update. |
| `onDidReceiveResources` | Resources blob updated via `setResources` | Companion to `getResources`; large state outside the settings size limit. |
| `onTitleParametersDidChange` | User changed font/size/color in the title editor | Re-render only if the change affects you. |
| `onPropertyInspectorDidAppear` | PI opened | Push initial data: `streamDeck.ui.current?.sendToPropertyInspector(payload)` |
| `onPropertyInspectorDidDisappear` | PI closed | Cancel any pending PI-targeted refreshes. |
| `onSendToPlugin` | PI called `streamDeckClient.send(payload)` | Handle PI → plugin messages. |

### Key-only events

| Event | Payload extras |
|---|---|
| `onKeyDown` | `state`, `userDesiredState`, `isInMultiAction` |
| `onKeyUp` | same as `onKeyDown` |

### Dial / encoder-only events

| Event | Payload extras |
|---|---|
| `onDialDown` | — |
| `onDialUp` | — |
| `onDialRotate` | `ticks` (signed int; negative = CCW), `pressed` (boolean — true if rotated while pushed) |
| `onTouchTap` | `tapPos: [x, y]` (200×100 canvas), `hold` (boolean) |

---

## 3. Key actions — patterns

### Toggle (two states; auto-flip)

In the manifest, declare two states. The SDK auto-flips on each
`onKeyDown` unless `DisableAutomaticStates: true`.

```jsonc
{
  "UUID": "com.yourhandle.hello-world.mute",
  "Name": "Mute",
  "States": [
    { "Image": "imgs/actions/mute/off", "Name": "Unmuted" },
    { "Image": "imgs/actions/mute/on",  "Name": "Muted" }
  ]
}
```

```ts
@action({ UUID: "com.yourhandle.hello-world.mute" })
export class Mute extends SingletonAction {
  override async onKeyDown(ev: KeyDownEvent): Promise<void> {
    // SDK already flipped ev.payload.state to the NEW state
    await myAudioApi.setMuted(ev.payload.state === 1);
  }
}
```

### Manual state control (`DisableAutomaticStates: true`)

Use when the canonical truth comes from outside (a server, an external app).

```ts
@action({ UUID: "com.yourhandle.hello-world.lamp" })
export class Lamp extends SingletonAction<{ on?: boolean }> {
  override async onKeyDown(ev: KeyDownEvent<{ on?: boolean }>): Promise<void> {
    const next = !(ev.payload.settings.on ?? false);
    try {
      await hueApi.setLamp(next);
      await ev.action.setSettings({ on: next });
      await ev.action.setState(next ? 1 : 0);
      await ev.action.showOk();          // green checkmark
    } catch (err) {
      streamDeck.logger.error("Lamp toggle failed", err);
      await ev.action.showAlert();       // amber "!" badge
    }
  }
}
```

### Multi-Actions — respect `userDesiredState`

When the user drops an action inside a Multi-Action (a sequence of
actions on one key), they pick which state the action should go to.
That choice arrives in `ev.payload.userDesiredState`:

```ts
override async onKeyDown(ev: KeyDownEvent<MyType>): Promise<void> {
  const wantOn =
    ev.payload.isInMultiAction
      ? ev.payload.userDesiredState === 1      // user picked "Turn ON"
      : !(ev.payload.settings.on ?? false);    // normal toggle

  await myApi.setLamp(wantOn);
  await ev.action.setState(wantOn ? 1 : 0);
}
```

Forgetting this is the most common Multi-Action bug.

### Dynamic key images

Three ways, in increasing order of weight:

```ts
// 1. From file (cheapest — relative to *.sdPlugin/)
await ev.action.setImage("imgs/actions/lamp/on.png");

// 2. From data URL (good for runtime-generated PNGs)
await ev.action.setImage(`data:image/png;base64,${pngBytes.toString("base64")}`);

// 3. From dynamic SVG (best for templated text/badges)
const svg = `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72">
    <rect width="72" height="72" fill="#1e1e1e"/>
    <text x="50%" y="55%" text-anchor="middle" fill="#fff"
          font-family="sans-serif" font-size="32">${count}</text>
  </svg>`;
await ev.action.setImage(`data:image/svg+xml,${encodeURIComponent(svg)}`);
```

Options:

```ts
await ev.action.setImage(svgUrl, {
  state: 0,                              // which state to update (toggle actions)
  target: Target.HardwareAndSoftware,    // Hardware | Software | HardwareAndSoftware (default)
});
```

> ❌ **No animated formats.** GIF/APNG won't render. If you want
> animation, push a series of images on a `setInterval` from the plugin
> (and call `clearInterval` in `onWillDisappear`).

### Display precedence

When multiple sources try to set the same visual:

1. User-set value (from the Stream Deck UI) wins.
2. Runtime value (your `setImage`/`setTitle`) is next.
3. Manifest default (`States[].Image`, `States[].Title`) is fallback.

To let the user override your runtime value, leave the corresponding
manifest field present and respect `UserTitleEnabled` semantics.

### Feedback — `showOk` / `showAlert`

```ts
await ev.action.showOk();       // green checkmark overlay, ~1s
await ev.action.showAlert();    // amber "!" overlay, ~1s
```

Use these instead of "flashing the icon" loops. They're the SDK's
official success/failure language.

---

## 4. Dial actions — patterns

A dial action owns:

- The dial (rotate, push, long-push).
- 1/4 of the touch strip (200×100 px touch-strip canvas, divided across
  up to 4 dial actions on Stream Deck +).

### Setting touch-strip feedback

```ts
override async onDialRotate(ev: DialRotateEvent<{ volume: number }>): Promise<void> {
  const current = ev.payload.settings.volume ?? 0;
  const next    = Math.max(0, Math.min(100, current + ev.payload.ticks));
  await ev.action.setSettings({ volume: next });

  // Update touch-strip layout items by key
  await ev.action.setFeedback({
    title:     "Volume",
    value:     `${next}%`,
    indicator: { value: next },          // 0–100 progress
  });
}
```

### Selecting a layout

In the manifest (set once):

```jsonc
"Encoder": { "layout": "$B1" }            // built-in
```

Or programmatically (e.g. swap layout based on settings):

```ts
await ev.action.setFeedbackLayout("$B1");                  // built-in
await ev.action.setFeedbackLayout("layouts/custom.json");  // custom layout JSON
```

Built-in layouts:

| Key | Purpose |
|---|---|
| `$X1` | Icon + title (minimal) |
| `$A0` | Single value, no indicator |
| `$A1` | Single value with indicator |
| `$B1` | Two values |
| `$B2` | Two values with indicator |
| `$C1` | Three-cell layout |

For custom layouts (item types: `bar`, `gbar`, `pixmap`, `text`) see
`streamdeck-profiles-localization`.

### Trigger descriptions

The text users see in Stream Deck's onboarding overlay for each
interaction:

```ts
await ev.action.setTriggerDescription({
  push:      "Mute",
  rotate:    "Adjust volume",
  touch:     "Mute",
  longTouch: "Reset to 50%",
});
```

Set in manifest as defaults; override at runtime if your action is
mode-switching.

---

## 5. Accessing visible actions outside events

For background work — e.g. a websocket pushed an update and you need to
refresh every visible instance of your "Now Playing" action:

```ts
import streamDeck from "@elgato/streamdeck";

// Every visible action across all your plugin's UUIDs
streamDeck.actions.forEach((action) => {
  void action.setTitle("Refreshed");
});
```

From inside one action class, `this.actions` is auto-scoped to that
class's UUID:

```ts
@action({ UUID: "com.yourhandle.hello-world.counter" })
export class Counter extends SingletonAction {
  refreshAll() {
    this.actions.forEach((a) => void a.setTitle("Hello"));
  }
}
```

You can iterate by type too:

```ts
import { isKeyAction, isDialAction } from "@elgato/streamdeck";

for (const action of streamDeck.actions) {
  if (isKeyAction(action))  await action.setTitle("hi");
  if (isDialAction(action)) await action.setFeedback({ value: "hi" });
}
```

> ❗ You can only access actions **owned by your plugin**. Other plugins'
> actions are invisible.

---

## 6. Commands available on every action

| Command | Notes |
|---|---|
| `setTitle(text, opts?)` | Set displayed title. `opts.state`, `opts.target`. |
| `setSettings(json)` | Persist per-action settings. Triggers `onDidReceiveSettings`. |
| `getSettings()` | Fetch current settings (returns Promise). |
| `setResources(json)` | Larger blob outside settings size limit. |
| `getResources()` | Fetch the resources blob. |
| `showOk()` | Green checkmark, ~1s. |
| `showAlert()` | Amber `!`, ~1s. |
| `sendToPropertyInspector(payload)` | Push data to the open PI. |
| `isKey()` / `isDial()` | Type guards. |

Key-only:

| Command | Notes |
|---|---|
| `setImage(urlOrPath, opts?)` | See "Dynamic key images" above. |
| `setState(0|1)` | Force state on multi-state actions. |

Dial-only:

| Command | Notes |
|---|---|
| `setFeedback({ key: value, … })` | Update layout-item values (e.g. `title`, `value`, `indicator`). |
| `setFeedbackLayout(idOrPath)` | Switch the active layout. |
| `setTriggerDescription({ push, rotate, touch, longTouch })` | Update interaction hints. |
| `setImage(urlOrPath)` | Override the encoder icon. |

---

## 7. Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Action never fires | Registered after `connect()` | Register first, connect last |
| `onKeyDown` doesn't fire on Stream Deck + dial | Action's `Controllers` excludes `"Keypad"` | Add `"Keypad"`, or implement `onDialDown` instead |
| Multi-Action ignores the user's "Turn ON" choice | Not checking `userDesiredState` | Branch on `isInMultiAction` + `userDesiredState` |
| Image flickers/stutters | New image computed in every event without throttling | Cache + throttle; or pre-bake images at start |
| Title doesn't update | User has set a custom title; SDK respects user override | Set `UserTitleEnabled: false` in manifest, or don't set a title |
| `setState` does nothing | Only one state declared in manifest | Add a second state (or use dynamic `setImage`) |
| Dial feedback ignored | Layout item `key` doesn't match a key in the active layout | Verify against the layout JSON (`title`, `value`, `indicator` are the most common reserved keys) |
| `showOk()` fires before async work succeeded | Not awaiting the API call | `await` the API, then `showOk()` only on success |
| State persists incorrectly across plugin restarts | Used local variables instead of `setSettings` | Persist via `setSettings` (per-action) or `setGlobalSettings` (plugin-wide) |

---

## See Also

- Official actions guide: <https://docs.elgato.com/streamdeck/sdk/guides/actions>
- Keys guide: <https://docs.elgato.com/streamdeck/sdk/guides/keys>
- Dials guide: <https://docs.elgato.com/streamdeck/sdk/guides/dials>
- Sibling skills: `streamdeck-manifest` (action declaration),
  `streamdeck-property-inspector` (PI ↔ plugin messaging),
  `streamdeck-profiles-localization` (touch-strip layout JSON)
