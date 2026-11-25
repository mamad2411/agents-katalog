---
name: token-storage
description: Handling access and refresh tokens on mobile — storage, rotation, revocation, and expiration. Use when wiring up the authenticated HTTP layer.
---

# Token Storage, Rotation, and Revocation

## Instructions

Treat tokens as short-lived credentials with a clear lifecycle. Storage alone is not enough — rotation and revocation matter just as much.

### 1. Split Access and Refresh Tokens

| Token | Lifetime | Where it lives |
| ----- | -------- | -------------- |
| Access token (JWT or opaque) | 5–60 min | In-memory, optionally in Keychain for cold-start resume. |
| Refresh token | Hours → days (with rotation) | Keystore / Keychain **only**. |
| `id_token` (OIDC) | Same as access | In memory; used for claims only, not for auth headers. |

Access tokens in memory survive backgrounding but are lost on process death — that is acceptable if refresh is cheap.

### 2. Refresh Token Rotation

Rotation is mandatory for public clients (RFC 6749bis / OAuth 2.1):

1. On each refresh, the server issues a **new** refresh token and invalidates the old one.
2. If the client sends an already-used refresh token, the server revokes the entire token family (refresh reuse detection).
3. The client must always persist the latest refresh token atomically before issuing the next request.

```kotlin
suspend fun refresh(): TokenPair {
    val current = secureStore.read("refresh") ?: throw NotAuthenticated
    val next = api.refresh(current) // may throw 400 invalid_grant -> reuse detected
    secureStore.write("refresh", next.refreshToken) // persist BEFORE using access token
    return next
}
```

### 3. Concurrency: One Refresh at a Time

Multiple parallel 401s must trigger a **single** refresh, not N. Use a mutex:

```kotlin
private val refreshMutex = Mutex()

suspend fun authenticatedCall(block: suspend (String) -> Response): Response {
    var token = memoryStore.access ?: refreshMutex.withLock { refreshIfNeeded() }
    val resp = block(token)
    if (resp.code == 401) {
        token = refreshMutex.withLock { refreshIfNeeded(force = true) }
        return block(token)
    }
    return resp
}
```

Same pattern works in Swift with an `actor`, in Dart with a `Completer`, and in JS with a shared `Promise`.

### 4. Revocation

On logout:

1. Call the server's **revocation endpoint** (RFC 7009) with the refresh token.
2. Delete every token from secure storage.
3. Wipe memory copies.
4. Clear cached HTTP responses that may embed user data.

On "logout everywhere" (user intent or suspected compromise) call the `revoke_all_sessions` endpoint or equivalent.

### 5. 401 vs 403

- **401** → try refresh once, then re-auth.
- **403** → the user is authenticated but not authorized for that resource. Never refresh on 403; it will loop.

### 6. Token Leakage Surfaces

Audit all of these:

- URL query params (never put tokens in the query string).
- HTTP logs / cURL dumps in debug builds.
- Crash reports (strip `Authorization` headers — most SDKs have a filter hook).
- Analytics / observability pipelines (same).
- WebView / deep link parameters on redirect.

### 7. Flutter / Dio Example

```dart
final interceptor = QueuedInterceptorsWrapper(
  onRequest: (req, h) async {
    req.headers['Authorization'] = 'Bearer ${await tokenStore.accessToken()}';
    h.next(req);
  },
  onError: (e, h) async {
    if (e.response?.statusCode == 401) {
      final newToken = await tokenStore.refresh();
      final retried = await dio.fetch(e.requestOptions
        ..headers['Authorization'] = 'Bearer $newToken');
      return h.resolve(retried);
    }
    h.next(e);
  },
);
```

`QueuedInterceptorsWrapper` (not `InterceptorsWrapper`) serializes concurrent refresh attempts.

## Checklist

- [ ] Refresh tokens live **only** in Keystore / Keychain.
- [ ] Access tokens live in memory (or short-lived secure cache), not plaintext disk.
- [ ] Refresh rotation is enforced server-side and reuse is detected.
- [ ] Concurrent 401s trigger exactly one refresh (mutex / actor / queued interceptor).
- [ ] 403 does not trigger refresh loops.
- [ ] Logout hits the revocation endpoint and wipes local state.
- [ ] No token appears in URL, logs, crash reports, or analytics.
