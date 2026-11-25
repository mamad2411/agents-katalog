---
name: oauth-mobile
description: OAuth 2.1 + PKCE for native mobile apps. Covers redirect URIs, AppAuth libraries, and the flows that are safe vs deprecated. Use when implementing or reviewing user login.
---

# OAuth 2.1 on Mobile (with PKCE)

## Instructions

Mobile OAuth is a minefield. Use audited libraries, follow RFC 8252 (OAuth 2.0 for Native Apps), and never hand-roll the flow.

### 1. Allowed Flows

- **Authorization Code + PKCE** — the only acceptable interactive flow for native apps (RFC 7636).
- **Device Authorization Grant** — acceptable for input-constrained devices (TVs, some wearables).
- **Client Credentials** — only for server-to-server. Never ship a client secret in a mobile binary.

**Banned on mobile:**
- Implicit flow (returns access tokens in the URL fragment — can leak).
- Resource Owner Password Credentials ("password grant") — the app sees the user's password.
- Any flow that relies on a confidential `client_secret` baked into the app.

### 2. PKCE — What the Client Does

```ts
// code_verifier: 43–128 chars of [A-Z a-z 0-9 -._~]
const verifier = base64url(crypto.getRandomValues(new Uint8Array(32)));
const challenge = base64url(await sha256(verifier));

// 1. Open system browser (NOT WebView) to /authorize with:
//    response_type=code
//    code_challenge=<challenge>
//    code_challenge_method=S256
//    redirect_uri=<registered>
//    state=<CSRF token>

// 2. On redirect back, exchange code at /token with code_verifier=<verifier>.
```

`code_challenge_method=plain` is forbidden. Always `S256`.

### 3. Use AppAuth, Not a WebView

| Platform | Library |
| -------- | ------- |
| Android  | `net.openid:appauth` |
| iOS      | `AppAuth-iOS` (via SPM / CocoaPods) |
| Flutter  | `flutter_appauth` |
| React Native | `react-native-app-auth` |

Why not WebView:
- Shared cookies enable SSO (Chrome Custom Tabs / `ASWebAuthenticationSession`).
- WebViews can be MITMed by a malicious in-app JS bridge.
- Apple and Google reject apps that collect third-party credentials in a WebView.

### 4. Redirect URIs

Three acceptable schemes, in order of preference:

1. **App Links (Android) / Universal Links (iOS)** — claimed HTTPS URLs, verified by the OS. Best.
2. **Loopback redirect** (`http://127.0.0.1:<random>`) — great for desktop-style flows, limited on mobile.
3. **Private-use URI scheme** (`com.example.app:/oauth`) — acceptable if unique and reverse-DNS. Another app can register the same scheme on Android, so this is a last resort.

Never use `http://localhost` on iOS (it conflicts with Universal Links) or a scheme you don't own.

### 5. Android Example (AppAuth)

```kotlin
val serviceConfig = AuthorizationServiceConfiguration(
    Uri.parse("https://id.example.com/authorize"),
    Uri.parse("https://id.example.com/token"),
)

val authRequest = AuthorizationRequest.Builder(
    serviceConfig,
    clientId,
    ResponseTypeValues.CODE,
    Uri.parse("com.example.app:/oauth"),
).setScope("openid profile offline_access")
 .build() // PKCE is generated automatically

val service = AuthorizationService(context)
val intent = service.getAuthorizationRequestIntent(authRequest)
startActivityForResult(intent, RC_AUTH)
```

### 6. iOS Example (AppAuth)

```swift
let config = OIDServiceConfiguration(
    authorizationEndpoint: URL(string: "https://id.example.com/authorize")!,
    tokenEndpoint:         URL(string: "https://id.example.com/token")!
)
let request = OIDAuthorizationRequest(
    configuration: config,
    clientId:      clientId,
    scopes:        ["openid", "profile", "offline_access"],
    redirectURL:   URL(string: "com.example.app:/oauth")!,
    responseType:  OIDResponseTypeCode,
    additionalParameters: nil
)

currentAuthFlow = OIDAuthState.authState(byPresenting: request, presenting: vc) {
    authState, error in /* persist authState */
}
```

### 7. Post-Login Hygiene

- Validate `id_token` signature and `aud`, `iss`, `exp`, `nonce`.
- Persist the **refresh token** in Keystore / Keychain (see [token-storage](../auth/token-storage/SKILL.md)).
- Support `end_session_endpoint` on logout to revoke the server session, not just drop local tokens.

## Checklist

- [ ] Flow is Authorization Code + PKCE with `S256`.
- [ ] No `client_secret` is embedded in the app.
- [ ] Authorization is opened in Chrome Custom Tabs / `ASWebAuthenticationSession`, not a WebView.
- [ ] Redirect URI is an App Link / Universal Link where possible.
- [ ] `state` and `nonce` are validated on return.
- [ ] Refresh tokens are stored in Keystore / Keychain.
- [ ] Logout calls the server's `end_session_endpoint`.
