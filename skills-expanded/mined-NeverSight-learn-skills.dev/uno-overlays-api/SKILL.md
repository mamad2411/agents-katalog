---
name: uno-overlays-api
description: 'Work with overlays.uno overlay graphics via the UNO app APIs. Use when: controlling overlay graphics, sending API commands to uno apps, building scripts or web apps for uno overlays, integrating uno soccer, badminton, tennis, handball, hockey, countdown, ticker, flipper, playlist, lucky draw, media looper, or essentials apps, sending HTTP PUT requests to overlays.uno, updating scoreboard, match time, team names, overlay visibility, customization fields.'
argument-hint: 'Describe what you want to do with the overlay (e.g. "show soccer scoreboard", "build a control panel for countdown app")'
---

# UNO Overlay API Skill

Work with [overlays.uno](https://overlays.uno/home) overlay graphics powered by Singular.live. This skill covers all UNO apps, their API commands, and how to build integrations ranging from single HTTP calls to full control web apps.

## When to Use
- Send commands directly to a UNO overlay (show/hide, set scores, update text, etc.)
- Build a Node.js, Python, or browser script to control overlays programmatically
- Create a web-based control panel for a UNO app
- Automate overlay updates from an external data source

## How the API Works

### Step 1 — Resolve the Token to an App

Before sending commands you need to know which UNO app the token belongs to. Fetch the app metadata:

```
GET https://app.overlays.uno/apiv2/controlapps/{{token}}
```

**Example response shape:**
```json
{
  "id": ...,
  "name": "Tennis Scorebug | Champion",
  "appTemplateId": ...,
  "appTemplateVersion": ...,
  "type": "controlapp",
  "outputUrl": "https://app.overlays.uno/output/.../Output?aspect=16:9",
  "broadcastOutputUrl": "https://app.overlays.uno/output/.../Broadcast?aspect=16:9",
  "publicControlUrl": "https://app.overlays.uno/control/{{token}}",
  "publicControlApiUrl": "https://app.overlays.uno/apiv2/controlapps/{{token}}/control",
  "publicCommandApiUrl": "https://app.overlays.uno/apiv2/controlapps/{{token}}/command",
  "publicModelApiUrl": "https://app.overlays.uno/apiv2/controlapps/{{token}}/model",
  "compositionId": ...,
  "datastoreId": "app_..."
}
```

> **Note:** Use `outputUrl` for embedding or previewing the graphics. Ignore `broadcastOutputUrl` — it is not intended for regular use and may not work reliably.

Use `appTemplateId` to identify which UNO app this token controls:

| `appTemplateId` | App |
|----------------|-----|
| 473 | UNO Soccer |
| 495 | UNO Countdown |
| 498 | UNO Flipper |
| 503 | UNO Playlist |
| 518 | UNO Essentials |
| 533 | UNO Tennis |
| 586 | UNO Badminton |
| 608 | UNO Ticker |
| 877 | UNO Media Looper |
| 890 | UNO Hockey |
| 893 | UNO Handball |
| 999 | UNO Lucky Draw |

Once you know the app, load its reference file from `./references/` for the full command table.

If you cannot determine the app from `appTemplateId`, or the reference file isn't available in `./references/`, you can fetch the API documentation directly from the running app:

- `GET https://app.overlays.uno/apiv2/controlapps/{{token}}/api/info` — returns the full API documentation as Markdown (primary reference)
- `GET https://app.overlays.uno/apiv2/controlapps/{{token}}/api/json` — returns available commands as JSON (primarily used by the Steam Deck plugin, but may be useful for structured parsing)

### Step 2 — Send Commands

All UNO apps share the same command endpoint. Send HTTP PUT to the `/api` path:

```
HTTP PUT https://app.overlays.uno/apiv2/controlapps/{{token}}/api
Content-Type: application/json
```

The body is always a JSON object with a `command` field and an optional `value` field:

```json
{
  "command": "CommandName",
  "value": "optionalValue"
}
```

- `{{token}}` — the app token found in the app's URL or settings in overlays.uno
- All commands are case-sensitive strings
- The response body for the `/api` endpoint is always wrapped:

  ```json
  {"status": 200, "result": "ok", "payload": <data>}
  ```

  Where `<data>` is the return value (object, array, or string). Status codes other than 200 indicate an error.
- Boolean values: `"true"`, `"1"`, `"on"`, `"yes"` are all interpreted as `true`
- Color values follow HTML color format (e.g. `#ff0000`, `red`)
- Max string length: 64 KB

## Rate Limits

> **Always communicate rate limits to the user when building any integration, script, or control panel.** The API enforces hard limits — hitting them will cause requests to silently fail with HTTP 429, which can break live broadcast overlays at the worst possible moment.

Every UNO API endpoint is rate-limited. Limits depend on the user's subscription:

| Subscription | Daily API calls | Daily data | Burst (per minute) | Burst data (per minute) |
|---|---|---|---|---|
| **Free** | 10,000 | 25 MB | 50 calls | 200 KB |
| **Uno Plus** | 20,000 | 50 MB | 200 calls | 500 KB |

**Free plan users hit 50 calls/minute easily** — a polling loop running every second will exhaust the burst limit in under a minute.

### Response headers to monitor

Every rate-limited response includes these headers so you can track remaining quota:

```
X-Singular-Ratelimit-Burst-Calls:  {"limit":50,"remaining":49,"reset":1614430792}
X-Singular-Ratelimit-Daily-Calls:  {"limit":10000,"remaining":9999,"reset":1614430792}
X-Singular-Ratelimit-Burst-Data:   {"limit":200000,"remaining":199854,"reset":1614470401}
X-Singular-Ratelimit-Daily-Data:   {"limit":25000000,"remaining":24995200,"reset":1614470401}
```

The `reset` value is a Unix timestamp indicating when the limit window resets.

### Best practices — always apply these

1. **Send only on change.** Never poll and blindly re-send the same data. Only call the API when a value actually changes.
2. **Throttle loops.** If driving the overlay from a live data source, add a minimum interval between sends (≥ 2 seconds is a safe default for Free tier; ≥ 300 ms for Uno Plus).
3. **Watch the headers.** In any script or app, read the `X-Singular-Ratelimit-Burst-Calls` header and back off when `remaining` is low (e.g., < 5).
4. **Handle 429 gracefully.** On a 429 response, pause sending and retry after the `reset` timestamp. Do not hammer the endpoint with retries.
5. **Keep payloads small.** Only include fields that changed — don't send the entire state object on every update. This helps stay within data limits.

### Common traps to warn users about

- **Testing/development loops** — rapid test runs can exhaust the burst limit before going live. Slow them down.
- **Growing data payloads** — apps like Flipper, Playlist, and Media Looper send JSON arrays. If the array grows over time, data limits can be hit. Send only the current slice of data needed.
- **Multiple tabs/instances** — if the user has multiple scripts or browser tabs all calling the same token simultaneously, their limits are shared.

## Apps Overview

The `_info.md` file is the API documentation for each app. The `_json.json` file lists available commands in a structured format — primarily used by the Steam Deck plugin, but may be useful for structured parsing.

| App | Purpose | API docs | Commands JSON |
|-----|---------|----------|---------------|
| **Essentials** | Custom graphics with user-defined overlays and fields | [info](./references/uno-essentials-api_info.md) | [json](./references/uno-essentials-api_json.json) |
| **Soccer** | Soccer scoreboard — goals, match time, periods, teams, dropdown events | [info](./references/uno-soccer-api_info.md) | [json](./references/uno-soccer-api_json.json) |
| **Badminton** | Badminton scoreboard — games, points per game, serve, match time | [info](./references/uno-badminton-api_info.md) | [json](./references/uno-badminton-api_json.json) |
| **Tennis** | Tennis scoreboard — points, sets, tie break, serve | [info](./references/uno-tennis-api_info.md) | [json](./references/uno-tennis-api_json.json) |
| **Handball** | Handball scoreboard — goals, match time, periods, penalties | [info](./references/uno-handball-api_info.md) | [json](./references/uno-handball-api_json.json) |
| **Hockey** | Ice hockey scoreboard — goals, match time, periods, shots, penalties | [info](./references/uno-hockey-api_info.md) | [json](./references/uno-hockey-api_json.json) |
| **Countdown** | Countdown timer with optional message when reaching zero | [info](./references/uno-countdown-api_info.md) | [json](./references/uno-countdown-api_json.json) |
| **Ticker** | Scrolling text ticker — set messages separated by newlines | [info](./references/uno-ticker-api_info.md) | [json](./references/uno-ticker-api_json.json) |
| **Flipper** | Auto-rotating content cards driven by JSON data | [info](./references/uno-flipper-api_info.md) | [json](./references/uno-flipper-api_json.json) |
| **Playlist** | Manually stepped content cards driven by JSON data | [info](./references/uno-playlist-api_info.md) | [json](./references/uno-playlist-api_json.json) |
| **Lucky Draw** | Spin-wheel random winner picker with names list | [info](./references/uno-lucky-draw-api_info.md) | [json](./references/uno-lucky-draw-api_json.json) |
| **Media Looper** | Looping media messages driven by JSON data | [info](./references/uno-media-looper-api_info.md) | [json](./references/uno-media-looper-api_json.json) |

## Common Commands (All Apps)

Every app supports these overlay visibility commands:

| Command | Value | Description |
|---------|-------|-------------|
| `ShowOverlay` | — | Show the overlay |
| `HideOverlay` | — | Hide the overlay |
| `ToggleOverlay` | — | Toggle overlay visibility |
| `GetOverlayVisibility` | — | Returns current visibility |
| `GetCustomizationModel` | — | Returns schema of customization fields |
| `GetCustomization` | — | Returns current customization values |
| `SetCustomization` | JSON | Set multiple customization fields at once |
| `SetCustomizationField` | `fieldId/value` | Set a single customization field |
| `IncrementCustomizationField` | `fieldId/value` | Increment a numeric customization field |
| `DecrementCustomizationField` | `fieldId/value` | Decrement a numeric customization field |
| `ToggleCustomizationField` | `fieldId` | Toggle a boolean customization field |
| `ExecuteCustomizationField` | `fieldId/value` | Execute a function on a customization field |

See [Essentials App — Special Notes](./references/essentials-app-special-notes.md) for Essentials-specific commands and details.

## Building a Control Panel

- Use the `GetCustomizationModel` / `GetOverlayModel` commands first to discover available fields
- Render controls dynamically based on field types: `text`, `number`, `color`, `boolean`
- For sport apps, group controls by category: Visibility / Scores / Match Time / Teams / Events
- For Essentials, group by overlay name
- **Last resort — REST model endpoint:** If the API commands above are unavailable or insufficient, you can fetch the full composition tree (overlay structure + all field schemas) via a GET request:

  ```
  GET https://app.overlays.uno/apiv2/controlapps/{{token}}/model
  ```

  This returns the entire overlay hierarchy including subcompositions, field types, default values, min/max/step ranges, and selection options in a single response. Use this only when the normal API commands cannot provide what you need.

## JSON Format Reference

**SetCustomization:**
```json
{
  "command": "SetCustomization",
  "content": { "PrimaryColor": "#ffffff", "SecondaryColor": "#ff0000" }
}
```

**SetCustomizationField:**
```json
{ "command": "SetCustomizationField", "fieldId": "myField", "value": "some text" }
```

**SetOverlayContent (Essentials only):**
```json
{
  "command": "SetOverlayContent",
  "id": "45eac98d-cc99-4a8a-b430-872391c30aca",
  "content": { "text": "Hello World", "socialMediaLogo": "https://..." }
}
```

**SetData (Flipper / Playlist / Media Looper):**
```json
{
  "command": "SetData",
  "value": "[{\"Name\":\"Alice\",\"Title\":\"CEO\"},{\"Name\":\"Bob\",\"Title\":\"CTO\"}]"
}
```
