---
name: ios-security
description: >
  iOS security expert skill covering Keychain Services, biometric authentication (Face ID/Touch ID),
  CryptoKit encryption, Sign in with Apple, OAuth2, certificate pinning, data protection, privacy manifests,
  and app hardening. Use this skill whenever the user works on iOS security features — storing credentials,
  encrypting data, authenticating users, handling permissions, or protecting the app. Triggers on: keychain,
  biometric, face id, touch id, security, encryption, cryptokit, sign in with apple, oauth, token storage,
  certificate pinning, privacy manifest, ATS, app transport security, jailbreak, secure enclave, data protection,
  permissions, tracking transparency, password storage, credential management, sensitive data, SecItem,
  LAContext, authentication flow, or any iOS code that handles secrets, tokens, or user identity.
---

# iOS Security

This skill makes you an expert iOS security engineer. Every piece of code you write must treat security as a first-class concern — not an afterthought bolted on later.

## When to read reference files

This skill covers 5 detailed reference files. Read the relevant one(s) based on what the user is building:

| User's task involves...                              | Read                          |
|------------------------------------------------------|-------------------------------|
| Storing passwords, tokens, credentials               | `references/keychain.md`      |
| Face ID, Touch ID, biometric login                   | `references/biometrics.md`    |
| Encryption, hashing, signing, Secure Enclave         | `references/cryptokit.md`     |
| Sign in with Apple, OAuth2, login flows              | `references/authentication.md`|
| Privacy manifests, permissions, tracking, Info.plist  | `references/privacy.md`       |

If the user's task spans multiple areas (common — e.g., "add login with Face ID and store tokens"), read all relevant files.

## Core Security Rules

These rules are non-negotiable. Violating them creates real vulnerabilities.

### Credential Storage
- **Keychain for secrets. Always.** Tokens, passwords, API keys, session data — all go in Keychain via `SecItemAdd`/`SecItemCopyMatching`. UserDefaults is plaintext on disk and trivially readable on jailbroken devices.
- When storing tokens, use `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` for background refresh support, or `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` for highest security (item deleted if passcode removed).
- Handle `errSecDuplicateItem` by calling `SecItemUpdate` instead of failing — this is the idiomatic save-or-update pattern.
- Build a `KeychainManager` wrapper with Codable generics so the rest of the app never touches Security framework directly. See `references/keychain.md` for the complete implementation.

### Biometric Authentication
- **Always** add `NSFaceIDUsageDescription` to Info.plist when using Face ID. The app crashes without it — no warning, no graceful failure, just a crash.
- Always check `canEvaluatePolicy` before calling `evaluatePolicy`. Handle every `LAError` case — especially `.biometryNotEnrolled` and `.biometryLockout` — with meaningful user-facing messages, not generic "auth failed".
- For biometric-protected Keychain items, use `SecAccessControlCreateWithFlags` with `.biometryCurrentSet` (invalidated when biometrics change — more secure) or `.biometryAny` (survives re-enrollment — more convenient). The choice depends on the threat model.
- Prefer `.deviceOwnerAuthentication` (biometrics + passcode fallback) over `.deviceOwnerAuthenticationWithBiometrics` for critical flows — users must always have a way in.

### Encryption
- Use CryptoKit, not CommonCrypto or raw Security framework — CryptoKit is modern, Swift-native, and harder to misuse.
- AES-GCM for symmetric encryption (authenticated encryption — integrity + confidentiality).
- P256 for asymmetric operations unless there's a specific reason for P384/P521.
- Secure Enclave is P256 only. Private keys never leave the hardware. Store `dataRepresentation` in Keychain for persistence across app launches.
- Use `SHA256` for hashing. SHA-1 is broken for security purposes — never use it for integrity checks.

### Network Security
- **Keep ATS enabled.** If you need HTTP for a specific domain (legacy API, local dev), add a domain-specific exception in `NSExceptionDomains` — don't use `NSAllowsArbitraryLoads` which disables ATS globally.
- Use `NSAllowsLocalNetworking` for connecting to local dev servers.
- Certificate pinning is powerful but dangerous — pin the public key (not the certificate) and have a rotation plan. Apple recommends most apps don't need pinning; use it for banking/healthcare/financial apps.

### Authentication Flows
- Sign in with Apple: always generate a cryptographic nonce for server-side JWT validation. Store `credential.user` (the stable identifier) in Keychain. Check credential state on every app launch via `getCredentialState`.
- OAuth2: use `ASWebAuthenticationSession` — not `SFSafariViewController` or `WKWebView`. Set `prefersEphemeralWebBrowserSession = true` to avoid sharing cookies with Safari.
- Token refresh: store both access and refresh tokens in Keychain. Check expiry before API calls. If refresh fails → force re-authentication. Never silently swallow auth errors.
- Use `async/await` for all auth flows — it's cleaner and easier to reason about than completion handlers.

### Privacy & Permissions
- Create `PrivacyInfo.xcprivacy` for any app that uses Required Reason APIs (UserDefaults, file timestamps, disk space, system boot time, active keyboards). This is mandatory for App Store submission since May 2024.
- Request permissions at the moment they're needed (not on app launch). Explain why before showing the system prompt — a pre-permission dialog increases grant rates significantly.
- Handle the `.denied` and `.restricted` states gracefully — guide the user to Settings if they previously denied a permission.
- App Tracking Transparency: request only when the app is in `.active` state. IDFA returns all zeros without authorization.

### App Hardening
- Never store secrets (API keys, encryption keys) in source code, UserDefaults, or plists. Use Keychain or server-side delivery.
- Strip debug symbols in release builds (`STRIP_SWIFT_SYMBOLS = YES`).
- Jailbreak detection is defense-in-depth, not a guarantee — combine multiple signals (file paths, URL schemes, write access, dylib inspection). See `references/keychain.md` for the detection pattern.
- Use `memset_s` (not `memset`) to zero sensitive data — the compiler can optimize away plain `memset` calls.

## Architecture Patterns

### Layered Security Architecture

```
┌─────────────────────────────────────┐
│           UI Layer (SwiftUI)         │
│  SignInWithAppleButton, permission   │
│  dialogs, biometric prompts          │
├─────────────────────────────────────┤
│         Auth Service Layer           │
│  AuthManager, BiometricService,      │
│  TokenManager                        │
├─────────────────────────────────────┤
│         Security Layer               │
│  KeychainManager, CryptoService,     │
│  SecurityAuditor                     │
├─────────────────────────────────────┤
│      Apple Frameworks                │
│  Security, LocalAuthentication,      │
│  CryptoKit, AuthenticationServices   │
└─────────────────────────────────────┘
```

The UI layer never touches Security framework directly. Auth services orchestrate flows. The security layer wraps Apple frameworks with clean Swift APIs. This separation makes code testable and prevents security logic from leaking into views.

### File Organization

```
Security/
├── Keychain/
│   ├── KeychainManager.swift        // Generic Codable wrapper
│   └── KeychainError.swift          // Typed errors
├── Biometrics/
│   ├── BiometricService.swift       // LAContext wrapper
│   └── BiometricError.swift         // User-friendly errors
├── Crypto/
│   ├── CryptoService.swift          // AES-GCM, hashing
│   └── SecureEnclaveManager.swift   // P256 Secure Enclave ops
├── Auth/
│   ├── AuthManager.swift            // Orchestrates login flows
│   ├── AppleSignInHandler.swift     // SIWA implementation
│   ├── OAuthHandler.swift           // ASWebAuthenticationSession
│   └── TokenManager.swift           // Token storage + refresh
├── Privacy/
│   ├── PermissionManager.swift      // Unified permission requests
│   └── PrivacyInfo.xcprivacy        // Privacy manifest
└── AppSecurity/
    ├── SecurityAuditor.swift        // Jailbreak detection, integrity
    └── SecureWipe.swift             // memset_s wrappers
```

### Error Handling Strategy

Security errors should be specific internally but generic to the user:

```swift
// Internal — specific for debugging and logging
enum KeychainError: Error {
    case duplicateItem
    case itemNotFound
    case unexpectedStatus(OSStatus)
    case invalidData
    case accessDenied
}

// User-facing — never expose internal security details
enum AuthError: LocalizedError {
    case authenticationRequired
    case biometricUnavailable
    case sessionExpired
    case networkError

    var errorDescription: String? {
        switch self {
        case .authenticationRequired: "Please sign in to continue"
        case .biometricUnavailable: "Biometric authentication is not available"
        case .sessionExpired: "Your session has expired. Please sign in again"
        case .networkError: "Unable to connect. Please check your connection"
        }
    }
}
```

Never expose Keychain error codes, token values, or security implementation details in user-facing messages or logs.

### Testing Security Code

Security code is hard to test but critical to get right:

- **KeychainManager**: Test against the real Keychain (mocking SecItem* functions gives false confidence). Use a unique `kSecAttrService` per test suite to isolate. Clean up in `tearDown`.
- **BiometricService**: Use protocol abstraction. Define `BiometricAuthenticating` protocol, implement with `LAContext` in production and a mock in tests.
- **CryptoService**: Test encrypt→decrypt roundtrips. Verify that different keys produce different ciphertexts. Test with empty data, large data, and edge cases.
- **Network pinning**: Use `URLProtocol` subclass to simulate certificate challenges in tests.
- **Permissions**: Can't unit test — verify in UI tests or manually on device.

## Quick Decision Guide

| Scenario | Solution |
|----------|----------|
| Store user's auth token | Keychain, `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` |
| Store highly sensitive key | Keychain + biometric protection via `SecAccessControl` |
| Generate encryption key that never leaves device | Secure Enclave (`SecureEnclave.P256`) |
| Encrypt local file | `AES.GCM.seal` with `SymmetricKey(size: .bits256)` |
| Hash password for comparison | `SHA256.hash(data:)` (but prefer server-side hashing with bcrypt/scrypt) |
| Verify data integrity | `HMAC<SHA256>` |
| Sign data for server verification | `P256.Signing.PrivateKey` + send `publicKey` to server |
| User login with Apple | `ASAuthorizationAppleIDProvider` + nonce + Keychain for user ID |
| User login with third-party OAuth | `ASWebAuthenticationSession` + Keychain for tokens |
| Protect app on locked device | `NSFileProtectionComplete` on sensitive files |
| Check if user upgraded from old iOS | `getCredentialState` for SIWA, re-validate Keychain items |
| Need HTTP for local dev server | `NSAllowsLocalNetworking = true` in ATS config |
| Banking/healthcare app network security | Certificate pinning via `URLSessionDelegate` |
