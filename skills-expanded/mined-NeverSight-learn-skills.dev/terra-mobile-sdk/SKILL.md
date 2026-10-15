---
name: terra-mobile-sdk
description: Integrate the Terra API mobile SDK for on-device health sources that have no web API – Apple Health (HealthKit), Samsung Health, and Health Connect. Use when connecting Apple Health, Samsung Health, or Health Connect from a mobile app; when working with TerraiOS, TerraAndroid, terra-react, or terra_flutter_bridge; when minting a mobile SDK auth token via generateAuthToken; when configuring HealthKit background delivery, initConnection permission popups, getUserId validation, ProGuard rules for Samsung, or Health Connect manifest permissions; or when writing on-device data with postActivity/postBody/postNutrition.
license: MIT
compatibility: Requires network access to docs.tryterra.co for full API schemas
metadata:
  author: terra
  version: "1.0.0"
---

# Terra API Mobile SDK

Guidance for integrating the Terra API mobile SDK on iOS, Android, React Native, and Flutter. The workflow and every cross-platform gotcha live here in SKILL.md; per-platform setup detail (capabilities, manifest entries, install coordinates, code snippets, platform quirks) lives in `references/`.

## When the mobile SDK is the right tool

The mobile SDK exists for one reason: to reach health sources that have **no web API**. Only three integrations require it:

- **Apple Health / HealthKit** (iOS)
- **Samsung Health** (Android)
- **Health Connect** (Android)

Every other provider (Garmin, Fitbit, Oura, Whoop, Strava, Dexcom, and 500+ more) connects through the [Health & Fitness API](https://docs.tryterra.co/health-and-fitness-api), not the SDK. Google Fit can be read through the SDK via Health Connect, but the web API is the preferred, more reliable route for it. If a provider you need has a web API, use the web API.

Data captured by the SDK flows to the same Data Destination (webhook) as web API data, and connections are managed with the same auth model. If you are building the receiving webhook or storing the health data, that is the `terra-api` skill's territory; this skill covers the on-device connection.

## The six-step workflow

The shape is identical on every platform. Platform differences are in the `references/` files.

1. **Install the SDK and grant native capabilities.** Add the package, declare HealthKit/background capabilities (iOS) or manifest permissions and minSDK 28 (Android). See the per-platform reference.
2. **Initialize the SDK on every app start and every foreground.** Create the `TerraManager` (iOS/Android) or call `initTerra` (RN/Flutter). This call is **asynchronous** and must complete before any other SDK call. Initializing is a prerequisite for everything else, so do it every time the app opens, not just once per install.
3. **Mint a single-use auth token from YOUR BACKEND.** `POST https://api.tryterra.co/v2/auth/generateAuthToken` with your `dev-id` and `x-api-key` in the headers. The token is single-use **and expires in 3 minutes** (the response includes `expires_in`), so mint it just-in-time when the user initiates the connection, not at app start. It exists so the connection endpoint cannot be abused. In production, **never** ship the API key in the client; call this from your server and hand the token to the client through your own channel. During development only, a client-side call (exposing the key) is tolerable.
4. **Open the connection with `initConnection`.** Pass the connection type, the token, and your permission set. This triggers the OS permission popup. See "Permission popup behavior" below – it is the highest-friction part of the integration.
5. **Validate with `getUserId` on every re-initialization.** `getUserId` is synchronous and returns the `user_id` if the connection is live or `nil`/`null` if not. Call it right after every init; on `nil`, call `initConnection` again to reconnect. Re-connecting an already-connected user triggers no popup and does not interrupt the user.
6. **iOS only: enable background delivery.** Call `Terra.setUpBackgroundDelivery()` in your `AppDelegate`'s `didFinishLaunchingWithOptions`. Without it, Apple Health data is not pushed automatically.

**Deauthenticating** a user uses the same endpoint as web integrations: `DELETE /auth/deauthenticateUser`, called from your backend. See [the web API auth reference](https://docs.tryterra.co/health-and-fitness-api).

## Permission popup behavior (read before shipping)

- **The popup fires once.** On both Apple Health and Health Connect, the OS shows the permission screen only the first time. Calling `initConnection` again is a no-op for the popup. It re-triggers **only** if: (a) you call `initConnection` with an **expanded** set of `customPermissions`, (b) the app is deleted and reinstalled, or (c) – Health Connect only – you request a permission that Google has not approved for your app on release.
- **The HealthKit popup is a WebView.** If your app is itself WebView-based, you must interrupt your WebView, call `initConnection`, and reopen your WebView on completion. Otherwise the popup cannot render.
- **`getUserId` returning `nil` means reconnect, not re-popup.** Reconnecting a still-authorized user is silent.

## Background delivery (iOS)

`Terra.setUpBackgroundDelivery()` enables automatic Apple Health pushes, but the delivery is constrained:

- Fires at a **much lower frequency** when the app is killed.
- Fires **only when the phone is unlocked**.
- Fires **only with a network connection**.
- Delivers **only data types enabled on [the Terra Dashboard](https://dashboard.tryterra.co)**.
- If you use `customPermissions`, background delivery needs specific per-category permissions enabled: **Daily** needs `STEPS`; **Sleep** needs `SLEEP_ANALYSIS`; **Body** needs `BMI` and `HEART_RATE`; **Activity** needs `WORKOUT_TYPE`; **Nutrition** needs `NUTRITION_CALORIES`.

`schedulerOn` has **no effect on iOS** – background delivery is controlled entirely by `setUpBackgroundDelivery()`. On Android, `schedulerOn = true` enables Terra API to make scheduled requests while the app is in the foreground.

## Cross-platform gotchas

- **Samsung Health needs an approved partnership.** Terra API has a privileged Samsung partnership that bypasses Health Connect, but you must [apply for access](https://developer.samsung.com/SHealth/business-partner/m48wvqi1mt9w2w4c). While waiting, develop against Health Connect; switching to Samsung direct later is a **version bump with no code changes**. Release builds need the ProGuard rule `-keep class com.samsung.android.** { *; }` (R8 strips the Samsung classes without it and crashes at runtime), and test devices need **Developer Mode** enabled in Samsung Health.
- **Health Connect needs manifest work and Google approval.** Your manifest needs a privacy-policy `<activity>` with the `ACTION_SHOW_PERMISSIONS_RATIONALE` and `VIEW_PERMISSION_USAGE` intent-filters. Before going live you must apply to Google for Health Connect data-type access and add `tools:node="remove"` `<uses-permission>` lines for every permission you do not use. See `references/android.md`.
- **`setIgnoredSources` is iOS-only and not persisted.** It filters out data from specific source apps in HealthKit (useful when a user has both a cloud Terra API connection and that provider's companion app syncing into Apple Health, which produces duplicates). It resets on every app restart, so call it after every init. On Android it is a no-op.
- **A new device or reinstall replaces the connection – handle `user_reauth`.** When an SDK auth arrives with the same `(dev-id, reference_id, provider)` as an existing connection but a new device identifier (second device, or a reinstall that reset the vendor ID), Terra API issues a **new** `user_id`, **deletes every previous connection** for that tuple, and sends a `user_reauth` webhook carrying `old_user` and `new_user`. Handle that event by migrating your stored `old_user.user_id` to `new_user.user_id`; there is only ever one active connection per `(dev-id, reference_id, provider)`. This replacement only fires when a `reference_id` is supplied – with an empty `reference_id` stale connections accumulate instead, one more reason to always set `reference_id`.
- **`postActivity` requires `device_data` and iOS 14+.** Writing a completed activity fails without `device_data` in the payload.

## Decisions left to you

These are your calls; the docs do not prescribe them. Make them deliberately:

- **Which data types / permissions to request.** Empty `customPermissions` defaults to all available; narrowing reduces the permission surface but you must keep background-delivery categories (above) enabled.
- **Immediate vs deferred HealthKit prompting.** `requestPermissions: false` on `Terra.instance` recognizes returning users silently and lets you gate the popup on an explicit user action. See `references/ios.md`.
- **Device-switch handling.** A second device or reinstall replaces the existing connection and fires `user_reauth` (see above), so decide whether to let any device connect (and migrate `user_id`s on `user_reauth`) or gate `initConnection` to a single primary device.
- **Samsung direct vs Health Connect** as your Android route (and whether to start on Health Connect while the Samsung partnership is pending).
- **Backfill approach.** The `getDaily`/`getSleep`/etc. getters accept `toWebhook: true` (push to your destination) or `toWebhook: false` (return the payload to the client callback).
- **How your backend hands the auth token to the client**, and your **`reference_id` scheme** (this is the join key in every webhook).

## Platform references

Read the file for the platform you are building on:

- **`references/ios.md`** – read when integrating **TerraiOS** natively (Swift): capabilities, info.plist keys, `Terra.instance`, deferred prompting, `setUpBackgroundDelivery`, `setIgnoredSources`, writing data, planned-workout WorkoutKit sync.
- **`references/android.md`** – read when integrating **TerraAndroid** natively (Kotlin): `build.gradle` coordinates, minSDK 28, Samsung vs Health Connect setup, ProGuard, manifest intent-filters, `startIntent` (deprecated, always null).
- **`references/react-native.md`** – read when integrating **terra-react**: install, iOS + Android native setup, `initTerra`/`initConnection`, the AppDelegate background-delivery edit, `postActivity` (Apple Health only).
- **`references/flutter.md`** – read when integrating **terra_flutter_bridge**: `flutter pub`, native setup, `TerraFlutter` API, AppDelegate background delivery, getters.

Full docs: [docs.tryterra.co](https://docs.tryterra.co) (append `.md` to any docs URL for a markdown version). Where a signature or enum is not shown here, see the SDK reference linked from [docs.tryterra.co](https://docs.tryterra.co/health-and-fitness-api/mobile-only-sources). If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch the docs instead.
