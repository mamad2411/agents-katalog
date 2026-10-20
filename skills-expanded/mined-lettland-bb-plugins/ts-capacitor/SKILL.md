---
name: ts-capacitor
description: Use when wrapping a web app for mobile with Capacitor — native bridge, core plugins, Android build, when Capacitor vs PWA.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: language
  languages: [typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [ts-electron, react, frontend-pwa-workbox]
---

# TS Capacitor 8

**Iron Law: one web build runs inside a native WebView — the JS thread is the UI thread. Don't block it, don't assume web APIs map to native, don't put secrets in the bundle, and run `npx cap sync` after every plugin change or the native project never sees it.**

## Model — your web app, wrapped

Capacitor takes a static web build (`dist/`) and embeds it in a native shell (`WKWebView` on iOS, Android System WebView). One codebase ships to web, iOS, and Android. A bridge marshals JS ↔ native via plugins; everything else is the same HTML/CSS/JS you already run in a browser.

```
myapp/
├── dist/                 # your built web app (Vite/etc) → the WebView loads this
├── capacitor.config.ts
├── android/              # generated native project — committed, edited in Android Studio
├── ios/                  # generated native project (macOS only)
└── package.json
```

## `capacitor.config.ts`

```ts
import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.example.app", // reverse-DNS, must match store listing
  appName: "MyApp",
  webDir: "dist", // where `cap copy` reads the web build from
  android: { allowMixedContent: false }, // HTTPS only — no mixed content
  // server.url ONLY for live-reload dev; never ship a remote URL — it's a webview to anywhere.
};
export default config;
```

## Core plugins — usage patterns

Each plugin is an npm package + native code synced into the platform project. Install, then `npx cap sync`.

```ts
import { Filesystem, Directory, Encoding } from "@capacitor/filesystem";
import { Preferences } from "@capacitor/preferences";
import { LocalNotifications } from "@capacitor/local-notifications";

// Filesystem — real device storage. Pick the Directory deliberately (Data is private, sandboxed).
await Filesystem.writeFile({ path: "notes/1.txt", data: body, directory: Directory.Data, encoding: Encoding.UTF8 });

// Preferences — small key/value (NOT localStorage; the WebView may clear that). NOT for secrets.
await Preferences.set({ key: "lastSync", value: String(Date.now()) });
const { value } = await Preferences.get({ key: "lastSync" });

// Local notifications — request permission first, then schedule.
const perm = await LocalNotifications.requestPermissions();
if (perm.display === "granted") {
  // No `schedule` field ⇒ fires immediately (right for "sync complete"); add `schedule: { at: new Date(...) }` to defer.
  await LocalNotifications.schedule({ notifications: [{ id: 1, title: "Done", body: "Sync complete" }] });
}
```

`Preferences` is unencrypted platform storage — fine for flags and timestamps, wrong for tokens. Use the OS keystore/secure-storage plugins for credentials.

## Background work — foreground service (Android)

A WebView is suspended when the app backgrounds; `setInterval`/timers freeze. For work that must keep running (polling, sync), use an Android **foreground service** with a persistent notification — the only sanctioned way to run while backgrounded.

```ts
import { ForegroundService } from "@capawesome-team/capacitor-android-foreground-service";

await ForegroundService.startForegroundService({
  id: 1,
  title: "Syncing",
  body: "Running in background",
  smallIcon: "ic_stat",
});
// ... do the work ...
await ForegroundService.stopForegroundService();
```

Needs `FOREGROUND_SERVICE` (and on Android 14+ a typed `FOREGROUND_SERVICE_*`) permission in the manifest. iOS has no equivalent — background execution there is tightly limited; design for it.

## Android build flow

```bash
npm run build          # produce dist/ first — Capacitor never builds your web app
npx cap copy android   # copy dist/ into the native project (fast, web-only changes)
npx cap sync android   # copy + install/update native plugin code (after add/remove plugin)
npx cap open android   # open Android Studio to build/run/sign
# release APK/AAB via Gradle:
#   cd android && ./gradlew assembleRelease   (or bundleRelease for Play Store .aab)
```

`copy` = web changes only. `sync` = web changes **plus** native plugin wiring — run it whenever the plugin set changes. Signing/keystore is configured in Android Studio or `android/app/build.gradle`.

## Permissions — AndroidManifest

Native permissions live in `android/app/src/main/AndroidManifest.xml`, not your JS. A plugin's docs list what it needs; you add the `<uses-permission>` and, for runtime-dangerous ones (notifications on 13+, location, camera), request at runtime via the plugin's `requestPermissions()`.

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
```

## Platform detection

```ts
import { Capacitor } from "@capacitor/core";

if (Capacitor.isNativePlatform()) {
  // iOS/Android only — safe to call native plugins
} else {
  // running in a plain browser (web target) — guard plugin calls or use a web fallback
}
const platform = Capacitor.getPlatform(); // "ios" | "android" | "web"
```

Branch on this before any native-only call — the same bundle runs on the web target where the plugin may be a no-op or throw.

## Capacitor vs PWA — decision

| Use…          | When                                                                                                                 |
| ------------- | -------------------------------------------------------------------------------------------------------------------- |
| **PWA**       | Install via browser, offline caching, push, no app-store gate. Reach is the goal; no deep native APIs.               |
| **Capacitor** | Need app-store presence, native APIs (filesystem, foreground service, biometrics, BLE), or store-required packaging. |

They're not exclusive — a Capacitor app is still a web app and benefits from PWA-grade offline/caching. For service worker, manifest, install-prompt, and caching strategy, see `Skill(devkit:frontend-pwa-workbox)`.

## Anti-patterns

- Assuming a web API exists natively — `navigator.geolocation`, Web Bluetooth, etc. behave differently or not at all in a WebView; use the matching plugin.
- Blocking the JS thread (sync crypto, huge JSON parse, tight loops) — the WebView IS the UI; it freezes. Offload or chunk.
- Secrets/API keys in the JS bundle — the bundle ships inside the APK and is trivially extractable. Keep them server-side.
- Forgetting `npx cap sync` after `npm install <plugin>` — the native project never registers the plugin; calls fail at runtime.
- Shipping `server.url` pointing at a remote site — turns the app into an open WebView; lose offline + invite content injection.
- Using `localStorage` for anything that must persist — the WebView can evict it; use `Preferences`/`Filesystem`.
- Expecting `setInterval` to survive backgrounding — it's suspended; use a foreground service.
- Editing generated native files and then re-running `sync` without committing — changes get overwritten silently.

## Red flags

| Thought                                         | Reality                                                        |
| ----------------------------------------------- | -------------------------------------------------------------- |
| "It works in the browser, so it'll work native" | The WebView lacks/changes APIs; test on a real device early    |
| "I'll just hide the key in the JS"              | The APK is a zip — `unzip` and read it; the key is public      |
| "A background `setInterval` keeps it running"   | Backgrounded WebViews suspend; you need a foreground service   |
| "I added the plugin, why does it crash?"        | You skipped `cap sync`; the native side doesn't know it exists |
| "Capacitor or PWA — must pick one"              | A Capacitor app is a PWA inside a shell; you can have both     |

## Hand-off

For the desktop equivalent (same web app, native shell, IPC security): `Skill(devkit:ts-electron)`. For the React app you're wrapping (hooks, composition, performance): `Skill(devkit:react)`. For the offline/caching/install layer that complements or replaces the native shell: `Skill(devkit:frontend-pwa-workbox)`.
