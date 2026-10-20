---
name: flutter-session
description: Flutter session and auth standards — the three-state sealed SessionState, secure token storage, single-flight 401 refresh with replay-once, user-scoped provider disposal, complete sign-out teardown, resume revalidation after a background gap, biometric unlock gating a stored secret, and store-compliant in-app purchases with server-side receipt validation. Load when writing or reviewing auth features, the auth interceptor, app lifecycle observers, biometric lock, or purchase flows.
user-invocable: false
stack: auth/flutter-session
paths:
  - "**/features/auth/**/*.dart"
  - "**/core/network/auth_interceptor.dart"
  - "**/core/lifecycle/*.dart"
---

Full standards in [flutter-session.md](flutter-session.md). Always-on summary:

**Scope:** who the user is, and how that fact is stored, refreshed, revalidated and destroyed. Route guarding is `frontend/go-router`; secure-storage mechanics are `storage/flutter-local`; transport plumbing is `api-style/dio`.

**Session state — three states, never two:**
- `sealed class SessionState` with exactly three subclasses: `SessionUnknown` (secure storage not yet read — the cold-start default), `SessionActive` (carries the user and the access-token expiry), `SessionNone` (carries a `SignedOutReason`). Model it as a two-state flag and the router guard flashes sign-in at signed-in users on every cold start, because the Keychain read has not finished yet.
- One notifier writes `SessionState`; everything else reads it. No screen assigns it.
- Tokens live in platform secure storage (Keychain / Android Keystore) behind a `TokenStore` contract — never in shared preferences, never in a database row.
- The `Authorization` header is read from the store inside `onRequest`, per request. Never cached in a field or written once onto `dio.options`.

**Refresh — single-flight, replay exactly once:**
- `AuthInterceptor extends QueuedInterceptor`, so N concurrent 401s await one refresh instead of firing N and getting the token family revoked. A non-queued interceptor causes that stampede.
- In `onError`: bail unless the status is 401; bail if `options.extra['auth_retried']` is already set; refresh through a bare `refreshDio` that has no interceptors; then set the flag and re-send the original request through that **same `refreshDio`**, and `handler.resolve(...)` the response. Both the refresh and the replay must avoid the main Dio — either one re-enters the queue that is still blocked on this refresh, and deadlocks.
- A failed refresh signs the user out with `SignedOutReason.refreshRejected`. Never a retry loop.

**Sign-out clears everything user-scoped, then sets state last:** `tokenStore.clear()` → `biometricSecretStore.clear()` → `database.clearUserScoped()` → `responseCache.clear()` → `PaintingBinding.instance.imageCache.clear()` plus `.clearLiveImages()` → `analytics.reset()` → and only then `state = SessionNone(...)`. Provider teardown is automatic because every user-scoped provider does `ref.watch(sessionProvider)`; do not hand-maintain a list of providers to reset, because the one you forget leaks the previous user's data into the next session.

**Resume revalidation:** a `WidgetsBindingObserver` in `core/lifecycle/` stores the timestamp on `AppLifecycleState.paused` and, on `AppLifecycleState.resumed`, revalidates only when the gap exceeded a threshold such as `Duration(minutes: 5)` — tokens can be revoked while the app is backgrounded, and revalidating on every resume spins on every app switch. Never poll on a repeating timer. The observer changes session state and nothing else; it never navigates.

**Expiry mid-task re-authenticates in place.** The lock is an `Overlay` entry above the current route (`rootOverlay: true`, `PopScope(canPop: false)`), so the half-filled form is still there afterwards. Never push a sign-in route over unsaved work.

**Biometrics gate a stored secret; they are not the credential.** A `true` returned by the plugin is a bool from your own process — a patched binary returns it too. It must unwrap a real credential.
- Declare all three before the first `authenticate()` call: `NSFaceIDUsageDescription` in `Info.plist` (its absence is a hard crash the first time Face ID is requested), `USE_BIOMETRIC` in `AndroidManifest.xml`, and `MainActivity` extending `FlutterFragmentActivity` (`BiometricPrompt` needs a `FragmentActivity`).
- Three-way availability check: `isDeviceSupported()`, then `canCheckBiometrics`, then `getAvailableBiometrics()` non-empty. They answer different questions and each has its own UI response.
- `authenticate(localizedReason: ..., options: AuthenticationOptions(biometricOnly: false, stickyAuth: true, useErrorDialogs: true))` — keep the device-credential fallback, or a wet finger or a temporary lockout strands the user.
- The prompt unwraps a **refresh token** stored under an access-control policy bound to the current enrolment: `biometryCurrentSet` on iOS, `setInvalidatedByBiometricEnrollment(true)` on Android — so adding a fingerprint invalidates the secret. Handle invalidation by clearing the secret and falling back to full sign-in.

**Payments:** store policy picks the rail — IAP for digital goods, card/PSP for physical goods and real-world services. The client never decides a purchase succeeded: listen to `purchaseStream`, POST `purchase.verificationData.serverVerificationData` to your backend, and only after the server grants entitlement call `completePurchase(purchase)` — completing early loses a rejected purchase, never completing auto-refunds it on Play after three days. Entitlement is server state re-read on launch, never a locally persisted flag. `restorePurchases()` sits behind a visible, working button and goes through the same server verification.

**Related:** `frontend/go-router`, `storage/flutter-local`, `api-style/dio`, `state/riverpod`, `logging/flutter-observability`.
