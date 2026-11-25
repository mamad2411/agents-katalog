---
name: push-notifications
description: FCM push notifications — setup, token registration, permission flow, daily reminders, and MCP tooling. Use when adding push notifications, wiring token storage, implementing reminders, or debugging delivery.
---

Apply the following push notification standards to all code in this project.

## Stack

- `@react-native-firebase/messaging` — FCM token retrieval + foreground/background message handling
- `expo-notifications` — local notification scheduling, permissions API, notification handler
- `device_tokens` Supabase table — stores FCM tokens per user

## Setup checklist

- `yarn expo install expo-notifications expo-device @react-native-firebase/messaging`
- Add `expo-notifications` to the plugins array in `app.config.ts` with icon + color:

  ```ts
  ["expo-notifications", {
    icon: "./assets/images/notification-icon.png",
    enableBackgroundRemoteNotifications: true,
  }]
  ```

  Do not set `color` — `react-native-firebase_messaging` already injects `default_notification_color` into the Android manifest, and adding `color` here causes a manifest merger conflict.
  Create `assets/images/notification-icon.png` — white/transparent PNG (Android renders notification icons using alpha channel only; color is ignored). Keeping it separate from `adaptive-icon.png` lets you update it independently.
- Add `"@firebase-messaging": ["src/services/firebase-messaging/index.ts"]` to `tsconfig.json` paths
- Firebase project must have FCM enabled (Cloud Messaging tab in Firebase console)
- Run `inspect_push_tokens` MCP tool to check if `device_tokens` table exists — apply the generated migration if not

## Canonical service (`src/services/firebase-messaging/index.ts`)

```ts
import { getMessaging, getToken, onMessage } from '@react-native-firebase/messaging'
import { getApp } from '@react-native-firebase/app'
import AsyncStorage from '@react-native-async-storage/async-storage'
import * as Device from 'expo-device'
import * as ExpoNotifications from 'expo-notifications'

if (Platform.OS === 'android') {
  ExpoNotifications.setNotificationChannelAsync('default', {
    name: 'Default',
    importance: ExpoNotifications.AndroidImportance.MAX,
    vibrationPattern: [0, 250, 250, 250],
    // Do NOT pass sound: 'default' — expo-notifications treats it as a custom file lookup
    // and logs a warning. Omitting it uses the system default sound.
  })
}

ExpoNotifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldPlaySound: true,
    shouldSetBadge: false,
    shouldShowBanner: true,
    shouldShowList: true,
  }),
})

const messaging = getMessaging(getApp())

export type NotificationPermissionStatus = 'undetermined' | 'granted' | 'denied'

export async function getNotificationPermissionStatus(): Promise<NotificationPermissionStatus> {
  if (!Device.isDevice) return 'denied'
  const { status } = await ExpoNotifications.getPermissionsAsync()
  if (status === 'granted') return 'granted'
  if (status === 'undetermined') return 'undetermined'
  return 'denied'
}

export async function requestNotificationPermission(): Promise<boolean> {
  if (!Device.isDevice) return false
  const { status } = await ExpoNotifications.requestPermissionsAsync()
  return status === 'granted'
}

export async function getFCMToken(): Promise<string | null> {
  if (!Device.isDevice) return null
  try {
    return await getToken(messaging)
  } catch (e) {
    console.warn('[FCM token] Failed to get token:', e)
    return null
  }
}

export function subscribeToForegroundMessages(
  onMessageCallback: (title: string, body: string) => void,
): () => void {
  return onMessage(messaging, async remoteMessage => {
    onMessageCallback(
      remoteMessage.notification?.title ?? 'App',
      remoteMessage.notification?.body ?? '',
    )
  })
}

const REMINDER_NOTIF_ID_KEY = '@app/reminder_notif_id'

export async function scheduleLocalNotification(title: string, body: string, delaySeconds = 3) {
  await ExpoNotifications.scheduleNotificationAsync({
    content: { title, body },
    trigger: { type: ExpoNotifications.SchedulableTriggerInputTypes.TIME_INTERVAL, seconds: delaySeconds },
  })
}

export async function scheduleDailyReminder(hour: number, minute: number): Promise<void> {
  const existingId = await AsyncStorage.getItem(REMINDER_NOTIF_ID_KEY)
  if (existingId) {
    await ExpoNotifications.cancelScheduledNotificationAsync(existingId)
  }
  const id = await ExpoNotifications.scheduleNotificationAsync({
    content: { title: 'App', body: "Time to check in." },
    trigger: {
      type: ExpoNotifications.SchedulableTriggerInputTypes.CALENDAR,
      hour,
      minute,
      repeats: true,
    },
  })
  await AsyncStorage.setItem(REMINDER_NOTIF_ID_KEY, id)
}

export async function cancelDailyReminder(): Promise<void> {
  const id = await AsyncStorage.getItem(REMINDER_NOTIF_ID_KEY)
  if (id) {
    await ExpoNotifications.cancelScheduledNotificationAsync(id)
    await AsyncStorage.removeItem(REMINDER_NOTIF_ID_KEY)
  }
}
```

## Background handler (`index.js`)

Register the FCM background handler at the module level in `index.js`, before `expo-router/entry`:

```js
import messaging from '@react-native-firebase/messaging'
import * as ExpoNotifications from 'expo-notifications'
import { Platform } from 'react-native'

// FCM automatically displays notification-payload messages — only handle data-only messages here.
messaging().setBackgroundMessageHandler(async remoteMessage => {
  if (remoteMessage.notification) return

  const title = remoteMessage.data?.title
  const body = remoteMessage.data?.body
  if (!title && !body) return

  if (Platform.OS === 'android') {
    await ExpoNotifications.scheduleNotificationAsync({
      content: { title: title ?? 'App', body: body ?? '' },
      trigger: null,
    })
  }
})

import 'expo-router/entry'
```

**Critical:** if the FCM payload contains a `notification` key, Android FCM displays the notification automatically. Scheduling a local notification in the handler too causes a duplicate. Return early when `remoteMessage.notification` is present — only schedule for data-only messages.

## iOS foreground banners: the `firebase.json` gotcha (React Native Firebase)

When `@react-native-firebase/messaging` is installed, **it — not expo-notifications — owns the iOS `UNUserNotificationCenter` delegate** (via method swizzling). So on iOS, `setNotificationHandler`'s `shouldShowBanner`/`shouldShowList` are **ignored for foreground presentation**: RNFirebase's delegate decides, and its default foreground options are empty → **no banner, sound, or badge shows while the app is in the foreground**. Taps and background/lock-screen delivery still work, which makes this very easy to misdiagnose as a permissions or scheduling bug. It affects **all** foreground notifications, local ones included, because they all flow through that one delegate.

Fix — tell RNFirebase to present in the foreground, in `firebase.json` at the repo root:

```json
{
  "react-native": {
    "messaging_ios_foreground_presentation_options": ["badge", "sound", "list", "banner"]
  }
}
```

- Valid options: `badge`, `sound`, `list`, `banner` (maps to Apple's `UNNotificationPresentationOptions`).
- This does **not** disable the Firebase app-delegate proxy, so **FCM push keeps working**. Do *not* reach for the old `FirebaseAppDelegateProxyEnabled=false` workaround — it can break APNs/token registration.
- It is a **native config change**: it only takes effect in a new build, and it shifts the runtime-version fingerprint on **both** platforms (see the `ota` skill), so it **cannot** be delivered via OTA. `firebase.json` is also in neither the OTA nor the auto-build CI path filter, so trigger the store build manually.
- Keep `setNotificationHandler` with `shouldShowBanner`/`shouldShowList` regardless — it's what Android uses and what iOS would use if RNFirebase were removed.
- **Symptom signature** of this specific bug: `getAllScheduledNotificationsAsync()` shows the notification scheduled, permission is `granted` (iOS `getPermissionsAsync().ios.status === 2` = authorized), Android shows it fine, but iOS shows nothing in the foreground. That exact combination points here, not at permissions.

## Local-notification deep-linking (tap → open the right screen)

For scheduled notifications that should open a specific screen/entity on tap, attach a typed payload and handle **all three launch states** (foreground, background-in-memory, cold-start-from-killed):

```ts
// schedule with a discriminated payload
content: { title, body, data: { type: 'memory', entryId: entry.id } }
```

```ts
// in a root-level hook (mounted for the whole app lifecycle)
const handled = useRef<Set<string>>(new Set())
const handleResponse = (r: Notifications.NotificationResponse | null) => {
  if (!r) return
  const { identifier } = r.notification.request
  if (handled.current.has(identifier)) return            // dedupe cold-start + listener
  const data = r.notification.request.content.data
  if (data?.type === 'memory' && typeof data?.entryId === 'string') {
    handled.current.add(identifier)
    setPendingEntryId(data.entryId)                       // RECORD only — do NOT navigate here
  }
}
// cold start (tap launched a killed app): the listener never fires for this — recover it
Notifications.getLastNotificationResponseAsync().then(handleResponse)
// foreground + background-in-memory taps
const sub = Notifications.addNotificationResponseReceivedListener(handleResponse)
return () => sub.remove()
```

Hard-won rules for the tap→navigate flow:

- **Cold start needs `getLastNotificationResponseAsync()`.** `addNotificationResponseReceivedListener` does **not** fire when the tap cold-launched a killed app. Run both and dedupe by `request.identifier`, or the response gets lost and the app just opens to its default screen.
- **Decouple recording from navigating.** Stash the target id in a store; navigate from a *separate* effect that only runs once the user is authenticated **and** the target data has loaded. The tap can arrive while signed out, so you must **replay it after login**, not drop it.
- **Clear the data query cache on sign-out.** If the entity list is a React Query cache keyed *without* the user id, sign-out leaves it stale, so after login the nav effect's deps never change → the replay never fires (you end up on the wrong screen, with the target screen silently mounted/opened in the background). `queryClient.removeQueries({ queryKey: [...] })` in the `SIGNED_OUT` handler forces the post-login refetch that re-fires the nav effect *after* the auth transition settles.
- **Keep the navigation synchronous.** If the target screen consumes-and-clears the pending id the moment it opens (common when it's always mounted), deferring the navigation (`InteractionManager.runAfterInteractions`, `setTimeout`) lets the clear re-run the effect and cancel the deferred navigate before it fires → the tab/route switch never lands. Call `router.push(...)` directly in the effect body.
- With `expo-router` Material Top Tabs + `lazy: false`, the target tab's screen is mounted even when unfocused — it can open its modal in the background, so the *only* missing piece is the tab switch. Don't rely on the unfocused screen's side effect to also switch tabs.

## Server-push (FCM) tap deep-linking — a *separate* channel

Everything above handles **local** notifications (expo-notifications' response listener). **Server pushes (FCM) arrive on a different channel** and are easy to miss: on a remote FCM tap, `expo-notifications`' `addNotificationResponseReceivedListener` does **not** reliably surface the data payload. Use `@react-native-firebase/messaging`:

```ts
import { getMessaging, onNotificationOpenedApp, getInitialNotification } from '@react-native-firebase/messaging'
import { getApp } from '@react-native-firebase/app'

const messaging = getMessaging(getApp())
const onFcmTap = (msg: { data?: { [k: string]: string | object } } | null) => {
  if (msg?.data?.type === 'daily-reminder') setPendingCompose(true)   // RECORD only — navigate from an effect
}
const unsub = onNotificationOpenedApp(messaging, onFcmTap)   // warm (background → foreground)
getInitialNotification(messaging).then(onFcmTap)             // cold (tap launched a killed app)
return () => unsub()
```

Wire this **alongside** the expo local-notification listener whenever the *same* action can be triggered by both a local notification (e.g. guests' on-device reminder) and a server push (signed-in users' FCM reminder). Key both on the same `data.type` and funnel into the same "record → navigate from an effect" store flag.

Hard-won rules:

- **The SENDER must attach `data`, or the tap does nothing — silently.** This is the #1 landmine and cost a full debugging session. A message with only `notification: { title, body }` and **no** `data` arrives on tap as `data = {}`, so `data?.type` is `undefined` and the handler no-ops: the app opens but never navigates. **Every** "go here" push must include the payload — the cron/edge function (FCM v1 `message.data`) **and** any admin/manual console send. Audit the *server* side, not just the client handler.
- **FCM `data` values must be strings.** `{ type: 'daily-reminder' }` is fine; numbers/nested objects get dropped or coerced.
- **On iOS, one FCM tap fires BOTH channels.** The expo response listener fires with `data = null` (it doesn't surface the FCM payload) *and* RNFirebase's handler fires with the real `data`. So on iOS you **cannot** read the FCM payload from the expo channel — rely on the RNFirebase handler for server pushes. The overlap is harmless when both just set the same idempotent flag.
- **Diagnose handler-vs-payload with an on-device alert.** When a tap "does nothing," you can't tell whether the handler didn't fire or the data was empty. Temporarily `Alert.alert('tap', JSON.stringify(msg?.data ?? null))` at the top of each handler (expo + FCM). One tap tells you everything: no alert → handler not firing; `{}`/`null` → the *sender* isn't attaching `data`; correct `type` but no nav → it's the navigation target/timing (see the synchronous-navigate rule above). Strip the alerts once located.

## Scheduling batches without duplicates

For data-driven scheduled notifications (e.g. N days of "memories" derived from a list), the scheduling effect re-runs on every data refetch (new array reference), so a naive "already scheduled today" guard performs a read-modify-write across many `await`s and **races → double-schedules**. Make the scheduler concurrency-safe:

```ts
let inFlight: Promise<void> | null = null
export function scheduleMemories(entries, title, hour = 9, minute = 0): Promise<void> {
  if (inFlight) return inFlight                                   // 1. single-flight lock
  inFlight = (async () => {
    try {
      const today = new Date().toDateString()
      if ((await AsyncStorage.getItem(LAST_KEY)) === today) return // 2. guard BEFORE cancelling
      // ...cancel previously-scheduled ids (tracked in AsyncStorage)...
      await AsyncStorage.setItem(LAST_KEY, today)                 // 3. mark before the await-heavy loop
      // ...schedule loop, collect ids, persist the id list...
    } finally {
      inFlight = null
    }
  })()
  return inFlight
}
```

- **Single-flight lock** — concurrent effect runs return the same promise instead of both scheduling a full batch (you'd otherwise get 2× notifications at the same time, and the second id-list write orphans the first batch so it can never be cancelled).
- **Check the daily guard BEFORE cancelling** — otherwise a same-day re-run cancels the already-scheduled batch and then bails, leaving nothing scheduled.
- **Write the guard before the await-heavy loop** to close the read-modify-write window for anything that slips past the lock.
- A **stg-only test trigger** gated on `process.env.EXPO_PUBLIC_ENV === 'stg'` that fires one notification ~15s after app open is invaluable for exercising the tap/deep-link/foreground paths without waiting for the real daily trigger. Have it cancel its own previous pending notification (track the id) so relaunching can't stack copies, and strip it (or keep it strictly env-gated) before release.

## Token registration (`src/services/user-devices/index.ts`)

Save the FCM token to `device_tokens` after permission is granted and on every sign-in. Populate
the engagement columns on the same write — `userId` is optional so guests are tracked too, and
`last_active_at` is stamped every call so a plain app-open keeps the row fresh:

```ts
import { supabase } from '@services/supabase'
import { getFCMToken } from '@firebase-messaging'
import { getLocales, getCalendars } from 'expo-localization'

// userId omitted → a guest row (user_id NULL); sign-in later claims it.
export async function upsertDeviceToken(userId?: string): Promise<void> {
  const fcmToken = await getFCMToken()
  if (!fcmToken) return
  const now = new Date().toISOString()
  await supabase.from('device_tokens').upsert(
    {
      ...(userId ? { user_id: userId } : {}),
      fcm_token: fcmToken,
      locale: getLocales()[0]?.languageTag ?? null,          // e.g. "es-AR"
      timezone: getCalendars()[0]?.timeZone ?? null,         // IANA, e.g. "America/Argentina/Buenos_Aires"
      last_active_at: now,                                   // engagement signal — stamp every open
      updated_at: now,
    },
    { onConflict: 'fcm_token' },
  )
}

// Cheap "touch" for app-foreground when the token hasn't changed — keeps last_active_at live
// so retention/winback queries stay accurate even between sign-ins.
export async function touchDeviceActivity(): Promise<void> {
  const fcmToken = await getFCMToken()
  if (!fcmToken) return
  await supabase.from('device_tokens')
    .update({ last_active_at: new Date().toISOString() })
    .eq('fcm_token', fcmToken)
}
```

Call `touchDeviceActivity()` from an `AppState` `active` listener so activity is recorded on every
foreground, not only when the token or sign-in state changes.

**Conflict target = `fcm_token`, not `user_id`** (the table needs a UNIQUE constraint on `fcm_token`). One user legitimately has multiple devices — `onConflict: 'user_id'` would collapse them to a single row, so the user'd only get push on their most-recently-signed-in device. Keying on `fcm_token` keeps one row per device and refreshes the row when the same device re-signs-in. Tradeoff: stale tokens from old devices accumulate (clean them up when FCM reports them unregistered, or on a TTL).

Call `upsertDeviceToken(user.id)` in two places:

1. `useAuthSession` — on `SIGNED_IN` auth state event
2. Settings screen — immediately after the user grants permission

## Permission flow (Settings screen pattern)

```ts
async function refreshPermissionStatus() {
  if (!Device.isDevice) return
  const status = await getNotificationPermissionStatus()
  setNotifPermission(status)
  if (status === 'granted') {
    const { data: { user } } = await supabase.auth.getUser()
    if (user) upsertDeviceToken(user.id)
  }
}

useEffect(() => {
  refreshPermissionStatus()
  // Re-check when user returns from the iOS Settings app
  const sub = AppState.addEventListener('change', state => {
    if (state === 'active' && openedSettings.current) {
      openedSettings.current = false
      refreshPermissionStatus()
    }
  })
  return () => sub.remove()
}, [])

async function handlePermissionPress() {
  if (!Device.isDevice) return
  if (notifPermission === 'undetermined') {
    const granted = await requestNotificationPermission()
    setNotifPermission(granted ? 'granted' : 'denied')
    if (granted) {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) upsertDeviceToken(user.id)
    }
    return
  }
  // Already denied — deep-link to OS settings
  openedSettings.current = true
  await Linking.openSettings()
}
```

## `device_tokens` table schema

Run `inspect_push_tokens` — if the table is missing it will emit a ready-to-run migration. The expected shape:

| column | type | notes |
| --- | --- | --- |
| `id` | uuid PK | `gen_random_uuid()` |
| `user_id` | uuid FK → `auth.users` | **nullable** — see *guest tracking* below; ON DELETE CASCADE |
| `fcm_token` | text | NOT NULL, UNIQUE (upsert conflict target) |
| `platform` | text | `ios` / `android` / `web` |
| `firebase_project_id` | text | NOT NULL default — supports multiple Firebase projects (which project minted the token; the sender picks creds by it) |
| `reminder_enabled` | boolean | NOT NULL default `false` — explicit toggle, so "no reminder set" ≠ "reminder off" |
| `reminder_hour` | int | nullable — set when reminder enabled |
| `reminder_minute` | int | nullable |
| `timezone` | text | nullable — IANA string; needed to fire reminders/winbacks in the device's local time |
| `locale` | text | nullable — device locale, so server pushes are localized (fallback English) |
| `last_active_at` | timestamptz | nullable — last app-open; the core engagement signal (retention, winback eligibility, ad-cohort activity) |
| `created_at` | timestamptz | `now()` |
| `updated_at` | timestamptz | `now()`, kept current by moddatetime trigger |

RLS: owner policy on `user_id = auth.uid()`. With nullable `user_id`, also allow a guest row
(`user_id IS NULL`) to be read/claimed and let sign-in **claim** it (update `user_id` from NULL →
`auth.uid()`) — split the blanket owner policy into per-command policies so the claim UPDATE passes.

### Capture the engagement columns from day one (you can't backfill history)

Add `last_active_at`, `locale`, `timezone`, and nullable `user_id` **in the first migration**, even
before you build reminders or winback. The reason is asymmetric: a column you add later starts
accumulating data only from that day — every user who was active before is invisibly lost. By the
time you want to answer "which ad cohort is still active after 14 days?" or "who lapsed and should
get a winback?", the months of history you needed were never written. These columns are cheap to
carry and impossible to reconstruct, so default them into the schema:

- **`last_active_at`** — touch it on every app foreground (a lightweight upsert, not just on token
  change). It powers retention curves, winback targeting (`last_active_at < now() - 14d`), and
  measuring whether paid-install cohorts actually stick — the numbers that tell you if ads work.
- **`user_id` nullable (guest tracking)** — register a token even when signed out, so guests are
  reachable by push/reminders and counted in activity. Claim the row to the user on sign-in.
- **`locale` / `timezone`** — captured once, they let every future server push be localized and
  time-correct without a schema change or a reach-back migration.

## Admin push test page

`https://reflects.sytes.net/admin/push.html` — served via GitHub Pages from `docs/admin/push.html` on the `main` branch (`/docs` source folder).

If it returns 404, GitHub Pages has been disabled on the repo. Re-enable with:

```bash
gh api repos/anicca-labs/reflect/pages \
  --method POST \
  --field "source[branch]=main" \
  --field "source[path]=/docs"
```

The HTTPS cert survives disablement, so it comes back immediately after re-enabling.

## Editor setup for the Edge Functions

The FCM-sending functions are Deno code. If VSCode flags the `Deno` global or remote imports
as errors in `supabase/functions/`, set up the Deno LSP scoped to that folder — see the
**VSCode / Deno editor setup** section in the `ota` skill. It's a one-time per-repo config
that covers all Edge Functions.

## Edge Function secrets live in Supabase, not Doppler

The FCM-sending Edge Functions (`send-reminders`, `send-test-push`, `admin-push`) read their creds at runtime via `Deno.env.get(...)` — from **Supabase's own function-secret store**, NOT from Doppler. `doppler run --config <env> -- supabase functions deploy` uses Doppler only to authenticate the deploy; it does **not** upload function secrets. So Doppler and the live Supabase secrets can silently drift (e.g. stg has `FIREBASE_CLIENT_EMAIL`/`FIREBASE_PRIVATE_KEY`, prd is missing them, yet prod push still works because the secrets were set directly on the Supabase project).

If you want Doppler to be the source of truth, add an explicit sync step — a standalone `functions:push-secrets:<env>` script, kept **out of the deploy chain** unless validated (a bad push silently overwrites a working key):

```bash
# scripts/push-function-secrets.sh <project-ref>  — run via `doppler run --config <env> -- ...`
# Pushes an allowlist (ADMIN_PUSH_SECRET, FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL,
# FIREBASE_PRIVATE_KEY, and *_STG variants) via `supabase secrets set --env-file`.
```

Hard-won rules:

- **Never push `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY`** — Supabase auto-injects these into every function and `supabase secrets set` rejects the `SUPABASE_` prefix.
- **`FIREBASE_PRIVATE_KEY` is multiline.** Encode it single-line with literal `\n` for env-file safety; the function decodes with `.replace(/\\n/g, '\n')`, so real-newline or `\n`-escaped both work.
- **Verify safely before/after a push:** `supabase secrets list`'s `DIGEST` is plain `sha256(value)` — compare it to `sha256` of the Doppler value to detect whether a push would actually change anything (no values exposed). Before re-keying a live env, confirm the key still works by minting a Google token (JWT-bearer flow, `firebase.messaging` scope) — a service account can hold several valid keys, so a "different" key may still be valid.

## MCP tools

- `inspect_push_tokens` — shows total token count by platform + recent tokens; emits migration if table missing
- `send_test_push` — fires a real FCM message to a token using the Firebase service account (requires `firebase.serviceAccountPath` in `mcp.config.json`)

## Rules

- Always guard with `Device.isDevice` — FCM and permission APIs crash or silently fail on simulators
- Never use `shouldShowAlert` in `setNotificationHandler` — it is deprecated; use `shouldShowBanner` + `shouldShowList`
- **iOS foreground banners need `messaging_ios_foreground_presentation_options` in `firebase.json`** when `@react-native-firebase/messaging` is installed — `shouldShowBanner` alone is ignored because RNFirebase owns the iOS notification delegate. Native change → new build, not OTA.
- **Cold-start taps need `getLastNotificationResponseAsync()`** on mount — `addNotificationResponseReceivedListener` does not fire when the tap launched a killed app. Dedupe the two by `request.identifier`.
- **Deep-link taps: record the target, navigate separately** — replay after login (not drop), navigate synchronously (deferral gets cancelled), and clear the data query cache on `SIGNED_OUT` so the post-login refetch re-fires the nav effect.
- **Data-driven batch schedulers need a single-flight lock** + check the daily guard *before* cancelling — the scheduling effect re-runs on every refetch and otherwise double-schedules (or wipes the batch).
- Upsert with `onConflict: 'fcm_token'` (table needs a UNIQUE constraint on it) — one row per device so a user with multiple devices gets push on all of them; `onConflict: 'user_id'` would collapse them to one device
- `scheduleDailyReminder` must cancel the previous notification ID before scheduling a new one — otherwise duplicate reminders accumulate
- In `setBackgroundMessageHandler`, return early when `remoteMessage.notification` is present — FCM already displays it; scheduling a local notification too causes duplicates
- Never pass `sound: 'default'` to `setNotificationChannelAsync` — expo-notifications treats it as a custom file lookup and logs a warning; omit it to use the system default
- Token column in DB is `fcm_token`, not `token` — `inspect_push_tokens` handles both via introspection, but migrations should use `fcm_token` for clarity
