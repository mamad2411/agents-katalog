---
name: phone-link-samsung-control
description: Control Arthur's Samsung Galaxy S25 FE through Windows Phone Link using Codex Computer Use. Use when asked to operate, configure, or test the mirrored Samsung phone from the Windows desktop; do not use for ordinary browser-only or Android-advice tasks.
---

# Phone Link Samsung Control

Use this skill when a task needs direct interaction with Arthur's Samsung Galaxy S25 FE as mirrored through the Windows Phone Link app.

This skill captures a previously tested native Windows control path. The important distinction is that Phone Link is a native Windows app, not a browser tab. Do not conclude that control is unavailable merely because browser tools cannot see it.

## Required Computer Use Setup

Before controlling Windows apps, load the bundled `computer-use` skill and its required docs. Use the JavaScript execution surface that can import `@oai/sky`; if that tool is not currently loaded, search for `node_repl` or Computer Use tools rather than using browser-only automation.

Initialize the runtime once per fresh JavaScript session:

```js
if (!globalThis.sky) {
  const { sky } = await import("@oai/sky");
  globalThis.sky = sky;
}
nodeRepl.write("sky initialized");
```

## Find The Phone Link Windows

Phone Link has been observed under this native Windows app id:

```text
Microsoft.YourPhone_8wekyb3d8bbwe!App
```

List apps or windows and filter for that app id plus titles such as:

- `S25 FE von Arthur`
- `Phone Link`
- `Einstellungen`

Prefer the device window titled `S25 FE von Arthur` for touch interaction with the mirrored phone. Use `Phone Link` only for the main app shell, and `Einstellungen` only when the Android Settings app is open inside the mirrored phone.

Known working selection pattern:

```js
globalThis.apps = await sky.list_apps();
const candidates = apps.flatMap(app => app.windows || [])
  .filter(w => w.app === "Microsoft.YourPhone_8wekyb3d8bbwe!App" && w.title === "S25 FE von Arthur");

if (candidates.length !== 1) {
  nodeRepl.write(JSON.stringify(candidates.map(w => ({ id: w.id, app: w.app, title: w.title })), null, 2));
  throw new Error(`Expected exactly one S25 FE Phone Link window; found ${candidates.length}`);
}

globalThis.targetWindow = await sky.get_window({ id: candidates[0].id, app: candidates[0].app });
await sky.activate_window({ window: targetWindow });
globalThis.state = await sky.get_window_state({
  window: targetWindow,
  include_screenshot: true,
  include_text: false
});
globalThis.targetWindow = state.window;
```

If the JavaScript session loses state, reinitialize `sky`, find the target window again, and re-observe before acting.

## Act Through Screenshots

For phone interaction, use screenshots and coordinates against the latest observation. Keep `include_text: false` unless text is necessary and safe to inspect. This avoids exposing private messages, emails, notifications, or app contents.

Before every click, drag, or scroll:

- Re-observe the relevant Phone Link window if the current screenshot may be stale.
- Use the `screenshotId` from the latest observation.
- Clear or replace stale cached state after the action.
- Re-observe after the action to verify the visible result.

Known working harmless proof action:

```js
const observation = globalThis.state;
const screenshotId = observation.screenshots?.[0]?.id;
if (!screenshotId) throw new Error("No screenshotId returned by latest observation");

globalThis.state = null;
await sky.drag({
  window: observation.window,
  screenshotId,
  from_x: 560,
  from_y: 1160,
  to_x: 120,
  to_y: 1160
});

globalThis.state = await sky.get_window_state({
  window: observation.window,
  include_screenshot: true,
  include_text: false
});
globalThis.targetWindow = state.window;
```

In the successful run, this horizontal drag on the Android home screen produced a visible Android edge/swipe response in the `S25 FE von Arthur` window. That proved Phone Link accepted touch gestures.

## Safety Boundaries

Treat phone control as privacy-sensitive.

- Do not open, read, summarize, or expose private content such as emails, messages, notifications, browsing history, account details, or app contents.
- Do not purchase anything, add items to a cart, enter credentials, approve payments, or approve paid plans.
- Stop and ask before installing third-party apps, granting sensitive permissions, changing account settings, choosing allowed contacts/callers, or changing alarms.
- Prefer harmless system navigation such as Back, Home, Recents, Settings navigation, or empty-area gestures when testing control.
- Avoid actions that could make sound unexpectedly louder, such as disconnecting Bluetooth while media might continue through phone speakers.

## Sleep Setup Intent

When the request concerns Arthur's bedtime phone setup, preserve these decisions:

- Hard distraction and app restrictions run daily from `22:30` to `05:00`.
- Silence notifications and block ordinary calls from `22:00` to `05:00` without disabling emergency calling.
- From `23:00` to `05:00`, Audible, YouPipe, YouTube, podcasts, and audiobooks should not play audibly. Prefer a built-in Samsung Routine that stops or pauses media; if unavailable, set media volume to `0` for that interval and reverse it after `05:00` when supported.
- Do not create a morning alarm. Arthur wants to wake naturally; `06:30` is only the ideal wake time. If Samsung Sleep mode has a wake alarm enabled, identify it and follow the stop-before-alarm-change boundary before turning it off.
- During hard restrictions, allow only identifiable essentials: Phone, Clock, Calendar, Maps, banking or 2FA, password manager, Notes, and Settings.
- Restrict distracting apps where configurable: YouTube, YouPipe, browsers, Amazon, Reddit and other social media, ChatGPT, Play Store, Galaxy Store, and Audible when it creates late-night risk.

These are intended settings, not proof of current device state. Verify the visible UI before claiming a schedule, alarm, media action, or restriction is configured. If the state cannot be inspected safely, report the exact blocker instead of guessing.
