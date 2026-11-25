---
name: streamdeck-manifest
description: 'Exhaustive Stream Deck plugin manifest.json reference: every top-level property, Action object, Encoder, State, OS, Nodejs, Profile, ApplicationsToMonitor, Software, TriggerDescriptions, SDKVersion (2 vs 3 / DRM), JSON schema URL, TypeScript declaration, file-path extension rules, version format. USE FOR: writing manifest.json, hand-editing manifest, choosing SDKVersion, choosing MinimumVersion, configuring Nodejs Version + Debug mode, declaring actions, controllers (Keypad/Encoder), states, encoder layouts, profile bundles, application monitoring, OS minimum versions, $schema URL for IntelliSense, fixing validation errors.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "manifest", "json-schema", "configuration"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — Manifest Reference

> **Prerequisite:** Skim `streamdeck-general` for the file layout context
> (the manifest lives at `<UUID>.sdPlugin/manifest.json`). This skill is
> the exhaustive field-by-field reference.

## Purpose

The manifest is the **source of truth** for everything Stream Deck needs
to load, render, and interact with your plugin: actions, icons, OS/Node
versions, profiles, monitored apps. Misconfigure it and the plugin
silently fails to appear, or fails validation with an unhelpful error.

This skill enumerates every property with its type, whether it's
required, and the most common gotchas. Pair it with the JSON schema for
in-editor validation.

## Quick start — minimum viable manifest

```jsonc
{
  "$schema": "https://schemas.elgato.com/streamdeck/plugins/manifest.json",
  "UUID": "com.yourhandle.hello-world",
  "Name": "Hello World",
  "Version": "1.0.0.0",
  "Author": "Rick Wilson",
  "Description": "Demonstrates the Stream Deck SDK.",
  "Icon": "imgs/plugin/marketplace",
  "CodePath": "bin/plugin.js",
  "SDKVersion": 2,
  "Software": { "MinimumVersion": "6.6" },
  "OS": [
    { "Platform": "windows", "MinimumVersion": "10" },
    { "Platform": "mac",     "MinimumVersion": "12" }
  ],
  "Nodejs": { "Version": "20" },
  "Actions": [
    {
      "UUID": "com.yourhandle.hello-world.greet",
      "Name": "Greet",
      "Tooltip": "Say hello.",
      "Icon": "imgs/actions/greet/icon",
      "Controllers": ["Keypad"],
      "States": [{ "Image": "imgs/actions/greet/key" }]
    }
  ]
}
```

**Always include `$schema`.** Without it your editor can't validate the
file and the CLI errors are far less useful.

---

## File-path extension rules — the #1 source of validation errors

Some manifest fields take a path **without** an extension; others
**require** an extension. Get this wrong and `streamdeck validate`
complains.

| Field | Extension? | Example |
|---|---|---|
| `Icon` (plugin) | **No** | `"imgs/plugin/marketplace"` (file on disk is `imgs/plugin/marketplace.png`) |
| `CategoryIcon` | **No** | `"imgs/plugin/category"` |
| `Actions[].Icon` | **No** | `"imgs/actions/greet/icon"` |
| `Actions[].States[].Image` | **No** | `"imgs/actions/greet/key"` |
| `Actions[].States[].MultiActionImage` | **No** | — |
| `Encoder.Icon`, `Encoder.background` | **No** | — |
| `Profiles[].Name` | **No** | `"my-profile"` (file is `my-profile.streamDeckProfile`) |
| `CodePath`, `CodePathMac`, `CodePathWin` | **Required `.js`** | `"bin/plugin.js"` |
| `PropertyInspectorPath` | **Required `.htm` or `.html`** | `"ui/greet.html"` |
| `Encoder.layout` (custom) | **Required `.json`** | `"layouts/my-layout.json"` |

For extension-less fields, Stream Deck auto-picks the best image variant
from disk: prefers `@2x.png` on hi-DPI, falls back to `.png`, `.svg`,
`.jpg`, `.webp` in that order. **GIFs are not supported.**

---

## Top-level Manifest properties

### Required

| Field | Type | Notes |
|---|---|---|
| `UUID` | string | Reverse-DNS, lowercase `a-z 0-9 . -`. **Permanent.** Matches `<UUID>.sdPlugin/` folder name. |
| `Name` | string | Display name in the Stream Deck app. |
| `Version` | string | `"MAJOR.MINOR.PATCH.BUILD"` — four-component, all integers. `"1.0.0.0"`, not `"1.0.0"`. |
| `Author` | string | Display author. |
| `Description` | string | Short description shown in the actions list. |
| `Icon` | string (no ext) | Plugin marketplace icon. |
| `CodePath` | string (`.js`) | Entry script. Almost always `"bin/plugin.js"`. |
| `SDKVersion` | `2` or `3` | `3` enables DRM; requires `Software.MinimumVersion >= "6.9"` and `@elgato/streamdeck@^2`. |
| `Software` | object | See `Software` below. |
| `OS` | array of OS | At least one entry. See `OS` below. |
| `Actions` | array of Action | At least one (unless plugin is profile-only — rare). |

### Optional

| Field | Type | Notes |
|---|---|---|
| `CodePathMac` | string (`.js`) | macOS-specific entry, overrides `CodePath`. |
| `CodePathWin` | string (`.js`) | Windows-specific entry, overrides `CodePath`. |
| `Nodejs` | object | Node runtime config. See `Nodejs` below. |
| `Category` | string | Group actions under a heading in the actions list. |
| `CategoryIcon` | string (no ext) | Icon for the category. |
| `URL` | string | Website link shown in plugin info. |
| `SupportURL` | string | Support/help link. |
| `PropertyInspectorPath` | string (`.htm`/`.html`) | Default PI for actions that don't declare their own. |
| `DefaultWindowSize` | `[width, height]` | PI window size in px. |
| `ApplicationsToMonitor` | object | See `ApplicationMonitoring` below. |
| `Profiles` | array of Profile | Bundled profiles. See `Profile` below. |

---

## `Software`

```jsonc
"Software": { "MinimumVersion": "7.0" }
```

| Field | Type | Notes |
|---|---|---|
| `MinimumVersion` | enum string | One of `"6.4"`–`"7.4"`. |

Rule of thumb:

| If you use… | Minimum |
|---|---|
| Baseline v2 SDK | `"6.5"` |
| Active deep-links | `"6.5"` |
| Dial actions (Stream Deck +) | `"6.5"` |
| Passive deep-links (`?streamdeck=hidden`) | `"7.0"` |
| Device-change events | `"7.0"` |
| DRM (`SDKVersion: 3`) | `"6.9"` |
| Localization Chinese variants | `"6.8"` |

---

## `OS`

Array, at most two entries (one per platform).

```jsonc
"OS": [
  { "Platform": "windows", "MinimumVersion": "10" },
  { "Platform": "mac",     "MinimumVersion": "12" }
]
```

| Field | Type | Notes |
|---|---|---|
| `Platform` | `"windows"` / `"mac"` | Required. |
| `MinimumVersion` | string | OS version. `"10"` for Windows 10, `"12"` (macOS Monterey) is a safe macOS baseline. |

If you support both, list both. Omit a platform to make the plugin
unavailable there.

---

## `Nodejs`

```jsonc
"Nodejs": { "Version": "20", "Debug": "enabled" }
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `Version` | `"20"` / `"24"` | ✓ | Pin one. `"20"` for stability, `"24"` for newer language features / `fetch` improvements. |
| `Debug` | string | — | `"enabled"` (auto-port `--inspect`), `"break"` (`--inspect-brk`), or omit for auto-pick. |
| `GenerateProfilerOutput` | boolean | — | Writes a `.cpuprofile` next to logs. Enable only when diagnosing perf. |

---

## `Actions` — the meat

Each entry describes one action exposed to the user. See `streamdeck-actions`
for runtime semantics; here we cover only the manifest shape.

```jsonc
{
  "UUID":                 "com.yourhandle.hello-world.greet",     // reverse-DNS, prefixed by plugin UUID
  "Name":                 "Greet",
  "Tooltip":              "Say hello when pressed.",
  "Icon":                 "imgs/actions/greet/icon",              // no extension
  "Controllers":          ["Keypad"],                             // or ["Encoder"] or ["Keypad", "Encoder"]
  "States":               [{ "Image": "imgs/actions/greet/key" }],
  "PropertyInspectorPath":"ui/greet.html",
  "SupportedInMultiActions": true,
  "VisibleInActionsList":   true,
  "DisableAutomaticStates": false,
  "DisableCaching":         false,
  "UserTitleEnabled":       true
}
```

### Action fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `UUID` | string | ✓ | Must be prefixed by plugin UUID (e.g. `com.x.y.<action-slug>`). **Permanent.** |
| `Name` | string | ✓ | Shown in the actions list. |
| `Icon` | string (no ext) | ✓ | Icon in the actions list. |
| `States` | array of State | ✓ | At least one. Two = toggle (auto-flips unless `DisableAutomaticStates`). |
| `Controllers` | `["Keypad"]` / `["Encoder"]` / both | — | Default `["Keypad"]`. |
| `OS` | array of `"mac"`/`"windows"` | — | Restrict the action to certain platforms. Defaults to all the plugin supports. |
| `Tooltip` | string | — | Hover text in the actions list. |
| `PropertyInspectorPath` | string (`.htm`/`.html`) | — | Per-action PI; overrides the plugin-level one. |
| `SupportedInMultiActions` | boolean | — | Default `true`. Set `false` to forbid use inside Multi-Actions. |
| `SupportedInKeyLogicActions` | boolean | — | Whether this action can be used inside Key Logic compound actions. |
| `VisibleInActionsList` | boolean | — | Default `true`. Set `false` to keep the action functional but hidden (handy for profile-only actions or deprecation). |
| `DisableAutomaticStates` | boolean | — | If `true` and two states are declared, the SDK won't auto-toggle on press — you must call `setState` yourself. |
| `DisableCaching` | boolean | — | Disable image caching for this action. Use only if dynamic icons aren't refreshing as expected (rare). |
| `UserTitleEnabled` | boolean | — | If `false`, user can't override the title in the action editor. |
| `SupportURL` | string | — | Per-action help link. |
| `Encoder` | Encoder object | required if `Controllers` includes `"Encoder"` | See `Encoder` below. |

### `State`

```jsonc
{
  "Image":            "imgs/actions/greet/key",       // no extension; required
  "MultiActionImage": "imgs/actions/greet/key-multi", // optional; shown in Multi-Action picker
  "Name":             "On",                           // optional; shown to user in state picker
  "Title":            "",                             // default title text
  "TitleAlignment":   "middle",                       // "top" | "middle" | "bottom"
  "TitleColor":       "#ffffff",
  "FontFamily":       "Arial",
  "FontSize":         12,
  "FontStyle":        "Bold",                         // "Regular" | "Bold" | "Italic" | "Bold Italic" | ""
  "FontUnderline":    false,
  "ShowTitle":        true
}
```

Only `Image` is required. Two states = toggle action (e.g. mute/unmute);
the SDK alternates between them on each press unless `DisableAutomaticStates`.

### `Encoder` (dial actions only)

Required when `Controllers` includes `"Encoder"`. Configures the touch-strip
panel for the dial.

```jsonc
"Encoder": {
  "Icon":       "imgs/actions/volume/encoder-icon",   // no extension
  "background": "imgs/actions/volume/encoder-bg",     // touch-strip background
  "StackColor": "#444444",
  "layout":     "$B1",                                // built-in OR "layouts/custom.json"
  "TriggerDescription": {
    "Push":      "Mute",
    "Rotate":    "Adjust volume",
    "Touch":     "Mute",
    "LongTouch": "Reset"
  }
}
```

Built-in layouts: `$A0`, `$A1`, `$B1`, `$B2`, `$C1`, `$X1`. Custom JSON
layouts live at any path with `.json` — see `streamdeck-profiles-localization`
for the touch-strip layout schema.

---

## `Profiles` (optional, bundled profiles)

```jsonc
"Profiles": [
  {
    "Name":                       "default-layout",   // no extension; file is default-layout.streamDeckProfile
    "DeviceType":                 7,                  // Stream Deck + — see device type table
    "Readonly":                   false,
    "DontAutoSwitchWhenInstalled":false,
    "AutoInstall":                true
  }
]
```

| Field | Type | Notes |
|---|---|---|
| `Name` | string (no ext) | Filename of the profile asset shipped in `<UUID>.sdPlugin/<Name>.streamDeckProfile`. |
| `DeviceType` | integer 0–13 | Which hardware this profile targets. |
| `Readonly` | boolean | If true, user can't edit. |
| `DontAutoSwitchWhenInstalled` | boolean | If true, Stream Deck doesn't switch to this profile on install. |
| `AutoInstall` | boolean | If true, profile installs silently; otherwise the user is prompted. |

### Device type integer table

| `DeviceType` | Hardware |
|---|---|
| 0 | Stream Deck (original/MK.2) |
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

---

## `ApplicationsToMonitor`

Tells Stream Deck to notify your plugin when listed apps launch/quit.
See `streamdeck-system-devices` for the event-handler side.

```jsonc
"ApplicationsToMonitor": {
  "mac":     ["com.spotify.client"],
  "windows": ["Spotify.exe"]
}
```

- macOS: bundle identifiers (find via `mdls -name kMDItemCFBundleIdentifier /Applications/Foo.app`)
- Windows: executable names (find via Task Manager → Details column)

---

## `SDKVersion` — `2` vs `3` (DRM)

| Field | `SDKVersion: 2` | `SDKVersion: 3` |
|---|---|---|
| Required SDK version | `@elgato/streamdeck` v1 or v2 | `@elgato/streamdeck@^2` |
| Required Stream Deck app | per `Software.MinimumVersion` | **`>= "6.9"`** |
| File encryption (DRM) | none | enabled after Maker Console upload |
| Integrity checking | none | enabled |
| New SDK-exclusive features | — | enabled |
| Local dev | unaffected | unaffected (DRM applied only on Maker upload) |

If you intend to publish on the Marketplace and want piracy protection,
go `SDKVersion: 3`. Otherwise `2` is fine.

---

## TypeScript declaration (abbreviated)

```ts
type Manifest = {
  $schema?: "https://schemas.elgato.com/streamdeck/plugins/manifest.json";
  UUID: string;
  Name: string;
  Version: string;                       // "MAJOR.MINOR.PATCH.BUILD"
  Author: string;
  Description: string;
  Icon: string;
  CodePath: string;                      // ends in .js
  CodePathMac?: string;
  CodePathWin?: string;
  SDKVersion: 2 | 3;
  Software: { MinimumVersion: "6.4" | "6.5" | "6.6" | "6.7" | "6.8" | "6.9" | "7.0" | "7.1" | "7.2" | "7.3" | "7.4" };
  OS: [
    { Platform: "mac" | "windows"; MinimumVersion: string },
    { Platform: "mac" | "windows"; MinimumVersion: string }?
  ];
  Nodejs?: { Version: "20" | "24"; Debug?: string; GenerateProfilerOutput?: boolean };
  Category?: string;
  CategoryIcon?: string;
  PropertyInspectorPath?: `${string}.htm` | `${string}.html`;
  DefaultWindowSize?: [number, number];
  URL?: string;
  SupportURL?: string;
  ApplicationsToMonitor?: { mac?: string[]; windows?: string[] };
  Profiles?: Array<{
    Name: string;
    DeviceType: 0|1|2|3|4|5|6|7|8|9|10|11|12|13;
    Readonly?: boolean;
    DontAutoSwitchWhenInstalled?: boolean;
    AutoInstall?: boolean;
  }>;
  Actions: Array<Action>;
};
```

Full schema (with all enums):
<https://schemas.elgato.com/streamdeck/plugins/manifest.json>

---

## Common validation errors and fixes

| Error from `streamdeck validate` | Cause | Fix |
|---|---|---|
| `must NOT have additional properties` | Typo in a field name; manifest is strict | Compare against `$schema` autocomplete |
| `Icon must NOT match pattern "\.(png\|svg\|jpg\|jpeg\|webp)$"` | Extension included in `Icon` field | Remove `.png`/etc; only the file on disk has it |
| `CodePath must match pattern ".+\.js"` | Missing `.js` on entry path | Use `"bin/plugin.js"` |
| `Version must match pattern "^\d+\.\d+\.\d+\.\d+$"` | Three-component semver | Use four: `"1.0.0.0"` |
| `Actions[i].UUID must start with <PluginUUID>` | Action UUID isn't nested | Prefix with plugin UUID: `com.x.y.<slug>` |
| `Software.MinimumVersion must be >= "6.9"` (when `SDKVersion: 3`) | DRM minimum | Bump `Software.MinimumVersion` to `"6.9"` or drop to `SDKVersion: 2` |
| `DefaultWindowSize must NOT be larger than 500×650` | PI window cap | Reduce to `[500, 650]` or smaller |
| `Profiles[i].Name must NOT match pattern "\.streamDeckProfile$"` | Extension included | Remove `.streamDeckProfile` |

---

## See Also

- Official manifest reference: <https://docs.elgato.com/streamdeck/sdk/references/manifest>
- JSON schema: <https://schemas.elgato.com/streamdeck/plugins/manifest.json>
- Touch-strip layout schema: <https://schemas.elgato.com/streamdeck/plugins/layout.json>
- Sibling skills: `streamdeck-general`, `streamdeck-actions`,
  `streamdeck-profiles-localization`, `streamdeck-publishing`
