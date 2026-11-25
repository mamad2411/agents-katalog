---
name: keychain-secure-storage
description: Project-specific Keychain conventions — the single `KeychainStore` protocol seam, the accessibility policy (`ThisDeviceOnly` by default), biometric gating with `biometryCurrentSet`, access-group sharing, and the in-memory test double. Load whenever adding auth tokens, passcodes, or any on-device secret.
---

# Keychain (project delta)

For Security-framework fundamentals — `SecItemAdd` / `SecItemCopyMatching` / `SecItemUpdate` query dictionaries, `OSStatus` codes, `SecAccessControlCreateWithFlags` — read [Apple's Keychain Services documentation](https://developer.apple.com/documentation/security/keychain_services). This file documents only this project's decisions. The scaffolded `KeychainStoreLive` template lives in `.claude/skills/ios-app-skeleton/references/app-target.md`.

## When this applies

A hand-rolled `KeychainStore` protocol with one concrete implementation. On an existing app:

- **KeychainAccess / Valet / SwiftKeychainWrapper** → keep the library. The accessibility and biometric policy below still applies — check what the library defaults to, because several default to a syncing, non-`ThisDeviceOnly` class.
- **`SecItem*` called directly from several call sites** → the one-seam argument is worth making, but consolidating is its own change.
- **Secrets in `UserDefaults` or a plist** → that's a finding, not a style preference. Report it and offer the migration below.

## One protocol, one implementation

**Never call `SecItemAdd` / `SecItemCopyMatching` outside the store.** One protocol in `AppCore`, one concrete type in `App`:

```swift
public protocol KeychainStore: Sendable {
    func set(_ value: Data, for key: String) throws
    func get(_ key: String) throws -> Data?
    func delete(_ key: String) throws
}
```

The seam is what makes everything above it testable — a view model or repository that touches `SecItem*` directly can only be tested against the real Keychain, which is stateful, entitlement-dependent, and unavailable in `swift test`.

Two implementation details worth pinning down, because both produce silent misbehaviour:

- **`set` must handle the already-exists case.** `SecItemAdd` on an existing item returns `errSecDuplicateItem` and writes nothing. Query first, then `SecItemUpdate` or `SecItemAdd`.
- **`delete` treats `errSecItemNotFound` as success.** Otherwise sign-out throws on an account that never had a token.

## Accessibility policy

**Default to `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`.** Escalate only with a reason:

| Need | Class |
|---|---|
| Normal token, foreground use | `WhenUnlockedThisDeviceOnly` (default) |
| Background fetch reads it before first unlock | `AfterFirstUnlockThisDeviceOnly` |
| Requires user presence at every read | `WhenPasscodeSetThisDeviceOnly` + `SecAccessControl` |

**`ThisDeviceOnly` is not optional.** The non-suffixed classes are included in encrypted backups and can restore onto a different device; `kSecAttrAccessibleAlways` is deprecated outright. The security reviewer treats either as a finding.

## Biometric gating

For actions needing user presence — unlocking a vault, authorising a payment:

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    [.biometryCurrentSet],
    nil
)!
```

**Use `.biometryCurrentSet`, not `.userPresence` or `.biometryAny`, for anything that authorises value.** `biometryCurrentSet` invalidates the item when a new face or fingerprint is enrolled — which is exactly the attack where someone with the device passcode adds their own biometric. `.userPresence` also falls back to the passcode, defeating the point.

Reading such an item presents the system prompt on its own; you don't need `LAContext` unless you want to pre-authenticate before showing UI.

## Sharing across extensions

A widget or share extension reading the same secrets needs a Keychain-sharing entitlement with a group id (`$(AppIdentifierPrefix)com.example.app`) and `kSecAttrAccessGroup` in **every** query — including deletes, or sign-out leaves the extension holding a live token.

## Migrating off UserDefaults

Write to the Keychain, remove the old key, ship one release, then delete both the migration and the fallback read:

```swift
func migrateTokenIfNeeded(store: KeychainStore) throws {
    guard let token = UserDefaults.standard.string(forKey: "auth_token") else { return }
    try store.set(Data(token.utf8), for: "auth_token")
    UserDefaults.standard.removeObject(forKey: "auth_token")
}
```

Leaving the migration in forever means the insecure read path stays in the binary forever.

## Testing

Inject the protocol; use an in-memory double. **Never touch the real Keychain in unit tests** — it needs entitlements, persists across runs, and isn't available under `swift test`. Integration tests on a simulator are fine for the concrete store itself.

## Hard nos

- **No secrets in `UserDefaults`, a plist, or a file** — the whole reason this skill exists.
- **No logging a token value**, including in DEBUG. See the logging rules in `swift-style`.
- **No `kSecAttrAccessibleAlways*`** and no non-`ThisDeviceOnly` class.
- **No hard-coded secrets in the binary.** Client-side secrets always leak; fetch them after auth or proxy through your backend.
- **No Keychain read in `didFinishLaunching`** before first unlock unless the item is `AfterFirstUnlock*` — it fails silently and the app looks logged out.
