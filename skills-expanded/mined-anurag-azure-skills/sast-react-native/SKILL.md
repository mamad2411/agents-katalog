---
name: "sast-react-native"
description: "Static application security testing guidance for React Native / TypeScript apps: secure token storage, transport security, input validation, dependency and secret hygiene. Use when reviewing RN security."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# SAST — React Native / TypeScript

## Checks
- **Secrets:** no API keys/tokens in source, `.env` committed, or bundle. Secrets via secure config; tokens in Keychain/Keystore (expo-secure-store), never AsyncStorage.
- **Transport:** HTTPS only; certificate pinning where required; no `NSAllowsArbitraryLoads`/cleartext.
- **Input validation:** validate all user input (e.g. msisdn pattern from `entities`); escape before rendering in WebView; avoid `dangerouslySetInnerHTML`/`eval`.
- **Deep links:** validate/authorize deep-link params; no privileged action from unauthenticated link.
- **Dependencies:** `npm audit` clean of high/critical; pin versions; no abandoned native modules.
- **Logging:** no PII/token logging; strip console logs in release.
- **Auth:** token refresh + logout clears secure storage; biometric where the design specifies.
