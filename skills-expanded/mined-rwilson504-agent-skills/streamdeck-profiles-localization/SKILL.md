---
name: streamdeck-profiles-localization
description: 'Stream Deck profile bundling, localization/i18n, and Stream Deck + touch-strip layouts: shipping .streamDeckProfile files inside a plugin, switching profiles programmatically (streamDeck.profiles.switchToProfile), language files (en/de/fr/ja/ko/es/zh_CN/zh_TW.json), manifest string overrides + Localization dictionary, streamDeck.i18n.translate, custom touch-strip layout JSON (200×100 canvas, bar/gbar/pixmap/text items), built-in layout IDs ($A0/$A1/$B1/$B2/$C1/$X1), per-feedback-item keys. USE FOR: bundling a default profile with your plugin, switching the device to a bundled profile, translating action names/tooltips, custom dial touch-strip designs, custom layout JSON schema, reserved layout keys (title, icon, value, indicator).'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "profiles", "localization", "i18n", "layouts"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — Profiles, Localization, Touch-Strip Layouts

> **Prerequisite:** `streamdeck-manifest` (the manifest fields for
> `Profiles`, `Encoder.layout`, and localized strings live there) and
> `streamdeck-general` (file layout).

## Purpose

Three loosely-coupled concerns, grouped because none of them is big
enough to be its own skill:

1. **Bundled profiles** — ship a curated layout of buttons the user can
   install with one click.
2. **Localization (i18n)** — translate action names, tooltips, and PI
   strings into supported languages.
3. **Touch-strip layouts** — custom JSON designs for the Stream Deck +
   touch strip beyond the six built-in templates.

---

## PART 1 — Bundled Profiles

A profile is a saved arrangement of buttons + actions + plugin
configuration for a particular Stream Deck device. Bundling one with
your plugin lets the user opt in to a curated starting point.

### 1.1 Create the profile asset

In the Stream Deck desktop app:

1. Set up the layout exactly as you want it on a real device.
2. **Stream Deck Preferences → Profiles → Export**.
3. Save as `<my-profile>.streamDeckProfile`.

Copy the resulting file into your plugin folder:

```
<UUID>.sdPlugin/
└── profiles/
    └── default-layout.streamDeckProfile
```

### 1.2 Declare it in the manifest

```jsonc
{
  "Profiles": [
    {
      "Name":                       "profiles/default-layout",   // path, NO .streamDeckProfile extension
      "DeviceType":                 0,                           // 0 = Stream Deck MK.2, see device type table
      "Readonly":                   false,
      "AutoInstall":                true,
      "DontAutoSwitchWhenInstalled":false
    }
  ]
}
```

| Field | Effect |
|---|---|
| `Name` | Path inside `*.sdPlugin/`, **extension omitted**. |
| `DeviceType` | Which hardware this targets (0–13 — full table in `streamdeck-manifest`). One bundled profile per device type. |
| `Readonly` | If `true`, user can't edit (good for tutorial layouts). |
| `AutoInstall` | If `true`, installs silently on plugin install; if `false`, the user is prompted. |
| `DontAutoSwitchWhenInstalled` | If `true`, Stream Deck doesn't switch the active page to this profile after install. |

### 1.3 Switch to a bundled profile from your plugin

```ts
import streamDeck, { action, SingletonAction,
  type KeyDownEvent,
} from "@elgato/streamdeck";

@action({ UUID: "com.yourhandle.streaming.show-overlay" })
export class ShowOverlay extends SingletonAction {
  override async onKeyDown(ev: KeyDownEvent): Promise<void> {
    await streamDeck.profiles.switchToProfile(
      ev.action.device.id,
      "default-layout",                                  // === manifest Name basename
      0,                                                 // optional: page index inside the profile
    );
  }
}
```

### 1.4 Rules and limits

| ✔ | Restriction |
|---|---|
| ✅ | You can switch to **profiles your plugin bundled**. |
| ❌ | You CANNOT enumerate, switch to, or modify **user-defined** profiles. |
| ❌ | No way to query "what's the active profile right now". |
| ✅ | `switchToProfile` is async and idempotent. Calling with the same args is safe. |
| ❌ | `DontAutoSwitchWhenInstalled: true` does NOT prevent your plugin from calling `switchToProfile` later — only suppresses the install-time switch. |

---

## PART 2 — Localization (i18n)

Stream Deck ships with localized versions in:

| Code | Language |
|---|---|
| `en` | English (default — falls back here) |
| `de` | German |
| `es` | Spanish |
| `fr` | French |
| `ja` | Japanese |
| `ko` | Korean |
| `zh_CN` | Chinese (Simplified) — Stream Deck app 6.8+ |
| `zh_TW` | Chinese (Traditional) — Stream Deck app 6.8+ |

If the user has Stream Deck set to one of those languages, your plugin
can serve translated strings.

### 2.1 Manifest string overrides (the easy stuff)

Ship language files next to the manifest:

```
<UUID>.sdPlugin/
├── manifest.json
├── en.json
├── de.json
└── ja.json
```

Each language file mirrors the manifest fields you want translated,
keyed by the action UUID for action strings:

```jsonc
// de.json
{
  "Name":        "Hallo Welt",
  "Description": "Demonstriert das SDK.",
  "com.yourhandle.hello-world.greet": {
    "Name":    "Grüßen",
    "Tooltip": "Sagt Hallo.",
    "States": [
      { "Name": "Aus" },
      { "Name": "An"  }
    ]
  },
  "Localization": {
    "Save":  "Speichern",
    "Reset": "Zurücksetzen"
  }
}
```

| Field | Translates… |
|---|---|
| Top-level `Name` | Plugin name |
| Top-level `Description` | Plugin description |
| `<action-UUID>.Name` | Action name in the actions list |
| `<action-UUID>.Tooltip` | Action tooltip |
| `<action-UUID>.States[i].Name` | State name (toggle picker) |
| `<action-UUID>.Encoder.TriggerDescription.{Push,Rotate,Touch,LongTouch}` | Trigger hint strings |
| `Localization.<key>` | Free-form lookup table for `streamDeck.i18n.translate("<key>")` |

If a language file is missing OR a key is missing inside it, Stream Deck
falls back to the value in `manifest.json`.

### 2.2 Translating dynamic strings — `streamDeck.i18n`

```ts
import streamDeck from "@elgato/streamdeck";

const label = streamDeck.i18n.translate("Save");
// Returns "Speichern" if user is on German, "Save" otherwise.

// With explicit language override (rarely needed)
const labelDe = streamDeck.i18n.translate("Save", "de");
```

Lookup chain: `<active-language>.json` → `en.json` → the key itself.

> sdpi-components have their own localization mechanism (the
> `data-localize` attribute and a translations file referenced in the
> HTML). Consult the sdpi-components docs if you go deep on PI i18n;
> for most plugins the auto-translated manifest fields are enough.

### 2.3 What to translate vs. what to leave

| Translate | Leave as-is |
|---|---|
| `Name`, `Description`, `Tooltip`, `States[].Name` | `UUID` (never), `CodePath`, `Icon`, `Version` |
| User-facing button captions in the PI | Settings keys, log messages |
| Trigger descriptions for dials | Internal IDs, protocol strings |

---

## PART 3 — Touch-Strip Layouts (Stream Deck +)

The touch strip on Stream Deck + is divided into **four 200×100 px
canvases**, one per dial action. The SDK gives you six built-in
templates and a JSON schema for custom layouts.

### 3.1 Built-in layouts — pick one in the manifest

```jsonc
"Encoder": { "layout": "$B1" }
```

| ID | Visual | When to use |
|---|---|---|
| `$X1` | icon + title | Minimal label-only |
| `$A0` | one big value, no indicator | Big number readout (timer, temperature) |
| `$A1` | one value + horizontal indicator | Single dial control (volume) |
| `$B1` | two values stacked | Two related readouts (mic vs system volume) |
| `$B2` | two values + indicator | Two values, one progress bar |
| `$C1` | three values across | Three columns (mic, system, alert) |

Update from your action with `setFeedback`:

```ts
await ev.action.setFeedback({
  title:     "Volume",
  value:     "75%",
  indicator: { value: 75 },
});
```

Built-in keys: `title`, `value`, `value2`, `value3`, `indicator`, `icon`.
The exact set depends on the chosen layout.

### 3.2 Custom layouts

When the built-ins don't cut it, author a JSON layout file alongside the
manifest:

```
<UUID>.sdPlugin/
└── layouts/
    └── eq-meter.json
```

Set it as either the default in the manifest:

```jsonc
"Encoder": { "layout": "layouts/eq-meter.json" }
```

Or programmatically at runtime:

```ts
await ev.action.setFeedbackLayout("layouts/eq-meter.json");
```

### 3.3 Custom layout JSON shape

```jsonc
{
  "$schema": "https://schemas.elgato.com/streamdeck/plugins/layout.json",
  "id":      "eq-meter",
  "items": [
    {
      "key":     "title",
      "type":    "text",
      "rect":    [0, 0, 200, 16],
      "alignment":  "center",
      "color":      "#ffffff",
      "font":       { "size": 12, "weight": 600 }
    },
    {
      "key":     "bass",
      "type":    "bar",
      "rect":    [0, 24, 200, 16],
      "subtype": 1,
      "value":   0,
      "range":   { "min": 0, "max": 100 },
      "bar_fill_c":   "#26d07c",
      "bar_border_c": "#202020",
      "border_w":     1
    },
    {
      "key":     "treble",
      "type":    "bar",
      "rect":    [0, 48, 200, 16],
      "subtype": 1,
      "value":   0,
      "range":   { "min": 0, "max": 100 },
      "bar_fill_c":   "#3aa0ff"
    },
    {
      "key":     "vu",
      "type":    "gbar",
      "rect":    [0, 72, 200, 28],
      "subtype": 2,
      "value":   0,
      "range":   { "min": 0, "max": 100 },
      "bar_fill_c": "#ffcc00"
    }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique within your plugin. |
| `items[]` | array | Each item has a `key` (referenced from `setFeedback`), `type`, `rect`. |
| `items[].type` | `text` / `bar` / `gbar` / `pixmap` | See below. |
| `items[].rect` | `[x, y, width, height]` | Pixels on the 200×100 canvas. |
| `items[].key` | string | Reserved keys: `title`, `icon` — these mirror user-customizable parts. Pick anything else for custom items. |
| `items[].zOrder` | number | Higher = front. |
| `items[].opacity` | 0, 0.1, 0.2, … 1 | |
| `items[].enabled` | boolean | Hide an item dynamically (set `enabled` via `setFeedback`). |

### 3.4 Item type reference

| `type` | Purpose | Item-specific keys |
|---|---|---|
| `text` | Text label | `value` (the displayed text), `alignment` (left/center/right), `color`, `font: { size, weight }`, `text-overflow: clip|ellipsis|fade` |
| `bar` | Solid progress bar | `value`, `range: { min, max }`, `bar_fill_c`, `bar_bg_c`, `bar_border_c`, `border_w`, `subtype` (0–4 visual variants) |
| `gbar` | Bar + triangle indicator | Same as `bar`, with the indicator triangle rendered at `value`. |
| `pixmap` | Image | `value` (path or data: URL), `background` |

### 3.5 Updating from your action

```ts
await ev.action.setFeedback({
  title:  "EQ",
  bass:   { value: 65 },
  treble: { value: 40 },
  vu:     { value: 85, bar_fill_c: "#ff0000" },          // mutate any item key
});
```

Pass the value directly when you only need to change the value, or pass
an object to update multiple item fields.

### 3.6 Touch-strip layout rules

| ✔ / ✘ | Rule |
|---|---|
| ✅ | Canvas is 200×100 px. Items outside fail silently. |
| ✅ | The four dial actions share one 800×100 strip; each owns 1/4. |
| ✅ | The `title` and `icon` reserved keys are user-customizable — your `setFeedback({title: "Volume"})` is a **default** that user-set values override. |
| ✘ | Animated images (GIF/APNG) are not supported. |
| ✘ | Custom fonts beyond what Stream Deck ships are not supported. |
| ✅ | Use the JSON schema (`$schema`) for IntelliSense in VS Code. |

---

## See Also

- Profiles guide: <https://docs.elgato.com/streamdeck/sdk/guides/profiles>
- Localization (i18n) guide: <https://docs.elgato.com/streamdeck/sdk/guides/i18n>
- Touch Strip Layout reference: <https://docs.elgato.com/streamdeck/sdk/references/touch-strip-layout>
- Layout JSON schema: <https://schemas.elgato.com/streamdeck/plugins/layout.json>
- Sibling skills: `streamdeck-manifest` (Profiles/Encoder fields),
  `streamdeck-actions` (`setFeedback`, `setFeedbackLayout`)
