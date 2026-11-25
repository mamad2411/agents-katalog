---
name: android-auth-security
description: |
  Authentication and app security patterns for Android/KMP - login/logout flows, session ownership, token refresh, secure local storage, guarded navigation, and secret handling. Use this skill whenever adding sign-in, session restore, token refresh, protected APIs, logout, or handling secrets and user credentials. Trigger on phrases like "login", "signup", "token refresh", "session", "logout", "auth guard", "secure storage", "biometric", or "secret management".
---

# Android / KMP Authentication and Security

## Core Principles

- Authentication state is a first-class domain concern.
- Store only the minimum secret data required.
- Treat tokens and credentials differently from general preferences.
- UI decides what to render from a session state model; it does not inspect tokens directly.
- Logging must never expose passwords, tokens, refresh responses, or personally sensitive payloads.

---

## Recommended Module Ownership

```text
:core:domain              -> shared `SessionState`, auth error types if used broadly
:core:data or :core:auth  -> token storage abstraction, session persistence
:feature:auth:domain      -> auth contracts and models
:feature:auth:data        -> API/data source implementations
:feature:auth:presentation-> login screen, registration screen, auth ViewModels
```

Create a dedicated `:core:auth` module when auth grows beyond a few classes.

---

## Session Model

Expose a typed session model instead of raw token checks:

```kotlin
sealed interface SessionState {
    data object Unknown : SessionState
    data object LoggedOut : SessionState
    data class LoggedIn(val userId: String) : SessionState
}
```

The app root observes `SessionState` and decides whether to show the auth flow or the main flow.

---

## Auth Contracts

Keep contracts in domain:

```kotlin
interface AuthRepository {
    fun observeSession(): Flow<SessionState>
    suspend fun login(email: String, password: String): EmptyResult<AuthError>
    suspend fun logout(): EmptyResult<AuthError>
    suspend fun refreshSession(): EmptyResult<AuthError>
}
```

Use typed auth errors for expected failures such as invalid credentials, expired session, or too many attempts.

---

## Login Flow

Recommended sequence:
1. Validate inputs locally.
2. Call auth API.
3. Persist session/token data securely.
4. Emit `SessionState.LoggedIn`.
5. Load user-specific bootstrap data if needed.

The login screen should not navigate by itself based on success booleans. It should react to a session/event change from the `ViewModel`.

---

## Token Refresh

Token refresh belongs in the data/auth layer, not in screens or ViewModels.

- Access token: short-lived
- Refresh token: stored securely and used only for refresh
- Expired session: clear secure storage and emit `LoggedOut`

If the app uses Ktor, centralize refresh behavior in the `Auth` plugin configuration. See the **android-data-layer** skill.

---

## Secure Storage

Use a storage abstraction so the rest of the app does not depend on platform APIs directly:

```kotlin
interface SessionStorage {
    suspend fun read(): StoredSession?
    suspend fun write(session: StoredSession)
    suspend fun clear()
}
```

Guidelines:
- Do not store passwords after login.
- Store refresh/session secrets in secure platform-backed storage when available.
- Use plain DataStore only for non-sensitive preferences.
- Clear all session data on logout.

---

## App Startup / Session Restore

At app start:
1. read persisted session data
2. decide whether the session looks restorable
3. refresh if needed
4. emit final `SessionState`

Keep startup logic in a dedicated bootstrap/auth coordinator, not in the first composable that happens to render.

---

## Protected Navigation

Navigation decisions should be based on `SessionState`, not ad-hoc token checks:

```kotlin
when (sessionState) {
    SessionState.Unknown -> SplashScreen()
    SessionState.LoggedOut -> AuthNavHost()
    is SessionState.LoggedIn -> MainNavHost()
}
```

Feature screens should assume they are already inside the correct graph.

---

## Logout

Logout should:
- revoke session remotely when required
- clear local secure storage
- cancel user-scoped sync/work if applicable
- reset in-memory caches tied to the user
- emit `SessionState.LoggedOut`

Do not leave stale account data cached after logout.

---

## Secret Handling

- Never hardcode API secrets in source.
- Use `local.properties` + generated config for local development.
- Keep production secrets on backend services whenever possible.
- Redact tokens, cookies, authorization headers, and PII from logs.

See the **android-module-structure** skill for shared secret/config guidance.

---

## Biometrics and Device Credentials

Use biometrics only as a local unlock convenience layered on top of an existing session, not as the primary server authentication mechanism.

Good uses:
- unlock cached app session
- confirm sensitive local action
- re-enter secure section

Bad uses:
- replacing backend authorization entirely
- storing raw credentials for silent replay

---

## Checklist: Adding Auth

- [ ] Define `SessionState` and auth contracts in domain
- [ ] Centralize login/logout/refresh in an auth repository
- [ ] Use secure storage abstraction for session secrets
- [ ] Base navigation on `SessionState`
- [ ] Clear all user-scoped state on logout
- [ ] Redact secrets from logs and analytics