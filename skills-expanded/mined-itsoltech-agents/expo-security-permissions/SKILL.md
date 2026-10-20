---
name: expo-security-permissions
description: "Secure Expo permissions, auth, SecureStore, privacy, deep links, WebViews, and OTA."
---

# Expo Security Permissions

Harden Expo and React Native apps across mobile trust boundaries: device permissions, local storage, app config, auth/session, deep links, WebView, networking, dependencies, and OTA update integrity.

## Process

1. Map the trust model: JavaScript bundle, app config, native binary, local storage, SecureStore, backend APIs, auth/session, permissions, deep links, notification payloads, WebView, network, analytics SDKs, EAS credentials, and OTA updates.
2. For an existing repo, detect pinned Expo SDK, React Native, Expo Router, EAS CLI, `expo-updates`, `expo-secure-store`, native dependencies, and platform targets before relying on defaults. For new apps, use latest stable. For security-sensitive Expo/RN/EAS behavior, check current official docs through `itsol-current-tech-context`.
3. Implement controls at the trusted boundary: backend authorization, native permission declarations, app config, secure storage adapters, route/link validation, WebView isolation, network policy, update signing, CI gates, and store privacy declarations.
4. Add negative tests or QA evidence for denied permissions, malformed links, unsafe redirects, token refresh races, logout cleanup, tampered or wrong-channel updates, dependency-added permissions, and leaked secrets.
5. Do not rely on bundled secrecy, frontend-only checks, hidden screens, `EXPO_PUBLIC_*`, EAS build secrets after embedding, or OTA to change native permissions.

## Baseline

Production Expo apps should use development/preview builds for real permission testing, minimal native permissions, clear privacy declarations, PKCE for mobile OAuth, SecureStore or equivalent for refresh tokens, validated deep links, restricted WebViews, HTTPS with deliberate network policy, signed or controlled updates for high-risk apps, pinned dependencies, and release-gated credentials.

## Focused References

- [01-threat-model-secrets-auth.md](./references/01-threat-model-secrets-auth.md) - mobile threat model, bundled data, secrets, OAuth/PKCE, token storage, session cleanup, and backend authorization.
- [02-permissions-privacy-storage.md](./references/02-permissions-privacy-storage.md) - permission prompts, Info.plist/AndroidManifest, blocked permissions, privacy declarations, SecureStore, SQLite, files, and cleanup.
- [03-deep-links-webview-network.md](./references/03-deep-links-webview-network.md) - deep links, universal/app links, notification payloads, WebView, browser/OAuth flows, and network security.
- [04-update-integrity-supply-chain.md](./references/04-update-integrity-supply-chain.md) - EAS Update integrity, code signing, credentials, dependency permissions, native packages, CI gates, and supply-chain review.
