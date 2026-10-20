---
name: implement-push-notifications
description: Implements end-to-end mobile push — APNs token-auth and FCM HTTP v1 provider setup, device-token registration and rotation, alert vs silent/data payload schemas, the server send path, foreground/background/killed receipt handling, tap-to-deep-link routing, rich media via service extensions, and permission-prompt UX.
when_to_use: Adding or debugging push on iOS/Android (native or RN/Flutter) — token registration/rotation, payload design, foreground/background/killed delivery, tap deep-linking, silent data pushes, or permission timing. Distinct from message-queue-jobs (server-side fan-out/retry) and build-native-mobile-ui (the deep-link router/navigation it taps into).
---

## When to Use

Reach for this skill when the work is **getting a notification onto a device and reacting to it** — the client↔provider↔server push loop:

- "Register the device for push and store its APNs/FCM token against the user"
- "Token keeps changing / notifications stopped after reinstall — handle refresh"
- "Send a push from the backend and have the tap open a specific screen"
- "Silent/background push to sync data without showing an alert"
- "Notification isn't showing when the app is in foreground / killed"
- "Add an image + action buttons to the notification (rich push)"
- "When and how should we ask for notification permission?"

NOT this skill:
- Server-side queueing, retry, and fan-out of the send jobs to millions of tokens → message-queue-jobs
- Delivery-rate dashboards, open-rate funnels, alerting on send failures → observability-instrument
- Designing the REST/GraphQL endpoint that receives the token from the client → rest-graphql-contract
- Who the user is / signing the request that registers the token → auth-jwt-session
- Throttling how often you send to one user → rate-limiting
- In-app realtime state sync (WebSocket/SSE, not OS push) → manage-client-server-state
- Building the in-app router / navigation stack the tap hands off to → build-native-mobile-ui
- Code signing, push capability provisioning, APNs auth-key upload, TestFlight/Play distribution → ship-mobile-app-store-release

## Steps

1. **Pick the transport per platform — there is exactly one right answer each.** Use **APNs token-based auth (`.p8` key + JWT)** for iOS, never the legacy `.p12` cert (certs expire yearly and are per-app; one `.p8` covers all your bundle IDs). Use **FCM HTTP v1** (`https://fcm.googleapis.com/v1/projects/{id}/messages:send`, OAuth2 bearer) for Android and as a unified façade for both — never the deprecated legacy `key=` server-key API (shut down June 2024). On iOS, register Firebase as the APNs delegate so you get one FCM token covering both stores.

   | Concern | iOS | Android |
   |---|---|---|
   | Provider | APNs (direct) or FCM→APNs | FCM |
   | Server auth | `.p8` key → ES256 JWT (`apns-topic`=bundle id) | OAuth2 SA token → FCM v1 |
   | Token source | `didRegisterForRemoteNotifications` deviceToken, or FCM token | FCM `getToken()` |
   | Capability | Xcode **Push Notifications** + **Background Modes→Remote notifications** | none (FCM in `google-services.json`) |
   | Silent push | `content-available:1`, **no** `alert` | `data`-only message, `priority:"high"` |

2. **Time the permission prompt — never on first launch.** Show a pre-permission *value* screen, then call the OS prompt only on a user action ("Turn on alerts"). iOS: `UNUserNotificationCenter.requestAuthorization([.alert,.sound,.badge])` returns a one-shot grant — if denied you cannot re-prompt, you must deep-link to Settings, so don't waste it. Android 13+ (API 33) requires the runtime `POST_NOTIFICATIONS` permission; target SDK 33+ and request it explicitly or you get silently zero notifications. iOS provisional auth (`.provisional`) delivers quietly to Notification Center with no prompt — good default for low-stakes apps.

3. **Obtain the token, then push it to the backend — and re-push on every refresh.** The token is not stable: it rotates on reinstall, restore-to-new-device, and at the OS's discretion. Treat the refresh callback as the source of truth, not the one-time fetch at startup.

   ```kotlin
   // Android — fires on first token AND every rotation
   override fun onNewToken(token: String) {
     api.registerDevice(token, platform = "android", appVersion = BuildConfig.VERSION_NAME)
   }
   ```
   ```swift
   // iOS via Firebase — delegate fires on rotation too
   func messaging(_ m: Messaging, didReceiveRegistrationToken token: String?) {
     guard let token else { return }
     Api.registerDevice(token, platform: "ios", bundle: Bundle.main.bundleIdentifier!)
   }
   ```
   Send `Authorization` from the logged-in session so the token binds to the user. Re-register on **login** and **app foreground** too — a token issued while logged out must be re-bound after sign-in.

4. **Store tokens keyed by (user, device) with an upsert — dedupe and invalidate.** A user has many devices; a device's token changes. Key the row on a stable `device_id` (vendor id / install id), not the token, and **upsert** so rotation updates in place instead of accumulating dead rows.

   ```sql
   CREATE TABLE device_tokens (
     user_id    uuid    NOT NULL,
     device_id  text    NOT NULL,          -- stable per install
     token      text    NOT NULL,
     platform   text    NOT NULL,          -- 'ios' | 'android'
     updated_at timestamptz NOT NULL DEFAULT now(),
     PRIMARY KEY (user_id, device_id)
   );
   CREATE UNIQUE INDEX ON device_tokens(token);   -- a token belongs to one user
   ```
   On send failure, the provider tells you a token is dead (see step 8) — **delete it then**, not on a guessed schedule. On logout, delete that device's row so a reassigned phone doesn't get the previous user's pushes.

5. **Design the payload: alert vs data vs silent — keep them distinct.** Put display fields in the platform alert block; put routing/business fields in a **custom data** block your code reads on tap. A FCM v1 unified body:

   ```json
   {"message": {
     "token": "<device-token>",
     "notification": {"title": "New reply", "body": "Pim replied to your post"},
     "data": {"deeplink": "app://thread/8412", "type": "reply"},
     "android": {"priority": "high", "notification": {"channel_id": "social", "image": "https://…/t.jpg"}},
     "apns": {
       "headers": {"apns-priority": "10", "apns-push-type": "alert", "apns-collapse-id": "thread-8412"},
       "payload": {"aps": {"alert": {"title":"New reply","body":"Pim replied"},
                           "sound":"default","badge":3,"mutable-content":1,"category":"REPLY"}}}
   }}
   ```
   Rules: **`data` values must be strings** in FCM. **Silent push** = `content-available:1` / data-only, `apns-push-type:"background"`, `apns-priority:"5"`, **omit `alert`/`sound`/`badge`** entirely — any alert field makes it a visible push. Use **`apns-collapse-id` / FCM `collapse_key`** so a newer update replaces a stale one instead of stacking. Set `mutable-content:1` (iOS) / include `image` (Android) only when a service extension / Notifee will render rich content.

6. **Handle receipt in all three app states — they are different code paths.** Foreground delivery does **not** show a banner unless you opt in. Cold-start-from-tap gives you the payload via a *different* entry point than a tap while running. Wire every one:

   | State | iOS handler | Android handler |
   |---|---|---|
   | Foreground arrives | `userNotificationCenter(_:willPresent:)` → return `[.banner,.sound]` to show | `onMessageReceived` (data msgs) → build local notification |
   | Background/locked tap | `didReceive response` | launcher Activity `intent.extras` |
   | Killed → tap launches | `didFinishLaunching` `launchOptions[.remoteNotification]` | `getInitialNotification()` / launch `Intent` |
   | Silent/background data | `didReceiveRemoteNotification` (call completion handler!) | `onMessageReceived` (no notification block) |

   On tap, read `data.deeplink` and resolve it through the app's **central router** (the same one handling universal links — owned by build-native-mobile-ui; this skill only hands the URL to it). Never inline screen logic in the notification handler — funnel to one `route(url)` so cold-start and warm-tap reach the identical destination.

7. **Rich push needs platform-native rendering, not just an `image` URL.** iOS: add a **Notification Service Extension**; on receipt download the media in `didReceive(_:withContentHandler:)`, attach via `UNNotificationAttachment`, and call the handler within ~30s or the OS drops the attachment. Buttons: register a `UNNotificationCategory` whose `identifier` matches the payload `category`, with `UNNotificationAction`s. Android: pass `image` for a `BigPictureStyle`; add buttons with `addAction(PendingIntent)`. RN/Flutter: use **Notifee** (`@notifee/react-native` / `notifee` Flutter) — it does the channels, big-picture, actions, and full-screen intents both native SDKs require, and it's the only sane cross-platform path for actionable/rich notifications.

8. **Verify delivery and reap dead tokens from the provider's response — don't guess.** A 200 from APNs/FCM means *accepted*, not *delivered*; you only learn a token is dead from a specific error. Delete on these, retry/backoff on those:

   | Signal | Meaning | Action |
   |---|---|---|
   | APNs `410` / reason `Unregistered` | token dead (uninstall) | **delete token** |
   | APNs `400 BadDeviceToken` / `DeviceTokenNotForTopic` | wrong env or topic | fix env (sandbox vs prod) / `apns-topic`; delete if truly invalid |
   | FCM `UNREGISTERED` / `INVALID_ARGUMENT`(token) | dead / malformed token | **delete token** |
   | APNs `429 TooManyRequests` / FCM `QUOTA_EXCEEDED`(429) | throttled | exponential backoff + retry |
   | FCM `UNAVAILABLE`(503) / APNs `503` | transient | retry with `Retry-After` |

   Match the APNs **environment** to the build: dev/TestFlight tokens are APNs *sandbox*; App Store builds are *production* — sending a sandbox token to the prod gateway returns `BadDeviceToken`, the #1 "works on my phone, dead in prod" bug. (The build channel and signing that decide that env are owned by ship-mobile-app-store-release; here you only route the token to the matching gateway.)

## Common Errors

- **Legacy FCM `key=AAAA…` server key.** Removed June 2024 — returns 404. Use HTTP v1 with an OAuth2 bearer from a service account.
- **APNs sandbox vs production mismatch.** TestFlight = sandbox, App Store = production; crossing them yields `BadDeviceToken`. Pick the gateway from the build channel, not a global flag.
- **Storing only one token per user.** Overwrites the user's other devices; only the last-registered phone gets pushes. Key on `(user, device_id)`.
- **Keying the row on the token.** Token rotates → orphan rows pile up and you spray dead tokens. Key on stable `device_id`, upsert the token.
- **Silent push with an `alert`/`sound`/`badge` field.** It becomes a *visible* push and the OS may also throttle your background budget. Background pushes carry `content-available:1` and nothing displayable.
- **Expecting a foreground banner for free.** iOS suppresses it unless `willPresent` returns presentation options; Android `notification`-type messages are dropped in foreground — handle as `data` and post a local notification.
- **Android 13+ with no `POST_NOTIFICATIONS` request.** Silent zero delivery, no error. Target SDK 33+ and request the runtime permission.
- **Missing Android notification channel.** On API 26+ a notification with no created channel never shows. Create channels at startup; set `channel_id` in the payload.
- **Not calling the silent-push completion handler.** iOS `didReceiveRemoteNotification` must call `completionHandler(.newData)` fast, or iOS throttles future background pushes for the app.
- **`data` values as numbers/objects in FCM.** v1 requires all `data` values be strings; non-strings 400 the request. Stringify, parse on the client.
- **Deleting dead tokens on a timer.** You evict live tokens and keep dead ones. Delete only on `Unregistered`/`UNREGISTERED` from the actual send response.
- **Re-prompting after iOS denial.** The grant is one-shot; a second `requestAuthorization` no-ops. Detect denied and deep-link to system Settings instead.

## Verify

1. **Round-trip per state:** with a real token, send and confirm a banner appears in **foreground, background, and killed**. Tapping each opens the screen named by `data.deeplink` — cold-start tap and warm tap land on the *same* screen.
2. **Token rotation:** reinstall the app → `onNewToken`/refresh fires → backend row is **updated in place** (no second row), and a push to the new token arrives while the old one returns `Unregistered`.
3. **Silent push:** send `content-available:1` / data-only → app wakes and runs the handler with **no visible banner**; iOS completion handler is called.
4. **Dead-token reap:** uninstall, then send → provider returns `410 Unregistered` / FCM `UNREGISTERED` and the backend **deletes** that row. A subsequent send skips it.
5. **Env correctness:** an App Store / production build's token accepted by the **production** APNs gateway (no `BadDeviceToken`); a dev build by sandbox.
6. **Permission UX:** fresh install shows the OS prompt only after the in-app value screen / user action; on Android 13+ the `POST_NOTIFICATIONS` dialog appears; denying then re-trying routes to Settings rather than silently failing.
7. **Rich push:** a payload with an image + actions renders the picture and buttons; each button fires its intended action/deeplink.
8. **Collapse:** two updates with the same `apns-collapse-id`/`collapse_key` show as **one** replaced notification, not two stacked.

Done = a real device receives and correctly deep-links a push in all three app states, tokens upsert-and-rotate without duplicate or stale rows, dead tokens are deleted on the provider's `Unregistered`/`UNREGISTERED` signal, silent pushes wake the app without a banner, and the prod build hits the prod APNs gateway with zero `BadDeviceToken`.
