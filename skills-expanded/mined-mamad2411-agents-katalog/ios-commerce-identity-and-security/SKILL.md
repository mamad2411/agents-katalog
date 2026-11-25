---
name: ios-commerce-identity-and-security
description: Route, implement, or review iOS commerce, identity, secrets, local authentication, cryptography, app-integrity, and secure-network features. Use when a feature sells digital goods, accepts Apple Pay, adds Wallet passes, signs users in, protects credentials, gates a local action, or needs server-verified integrity.
allowed-tools: Read, Grep, Glob
---

# iOS Commerce, Identity, and Security

## Overview

Use this skill to keep purchase, payment, identity, secrets, device-user authentication, app-instance signals, transport security, server authorization, and product entitlement as separate trust boundaries.

`user intent -> system authorization/input -> local or server verification -> policy decision -> bounded side effect -> durable entitlement/audit state`

## Read before acting

- Inspect the actual Xcode targets, deployment target, product type, capabilities, entitlements, App Store Connect/merchant/service configuration, server contract, Keychain access groups, URL/transport layer, privacy copy, and existing entitlement/authentication adapters.
- Read the [commerce/identity/security route](../ios-knowledge-base/references/40-framework-routes/05-commerce-identity-and-security.md), [StoreKit and entitlements deep dive](../ios-knowledge-base/references/41-framework-deep-dives/02-storekit-and-entitlements.md), [networking/security/identity deep dive](../ios-knowledge-base/references/42-framework-deep-dives/03-networking-security-and-identity.md), and [commerce/identity/security recipes](../ios-knowledge-base/references/70-code-recipes/17-commerce-identity-and-security-recipes.md).
- Read the [data/device-services package](../ios-data-and-device-services/SKILL.md) when local persistence, CloudKit, account state, or protected personal data is involved. Refresh the exact official Apple pages in the Sources section before relying on an API, entitlement, region/device rule, or server-validation requirement.

## Route workflow

1. Classify the user outcome: digital content/subscription, physical goods/services payment, Wallet pass, Apple Account sign-in, secret/token storage, local device-user gate, app-instance abuse signal, or authenticated network request.
2. Choose the narrowest route. Use StoreKit for digital goods distributed through the App Store; PassKit/Apple Pay for supported physical payment; Wallet for signed passes; AuthenticationServices for Sign in with Apple; Security/Keychain for secrets; LocalAuthentication for a device-user policy; CryptoKit for an established protocol; DeviceCheck/App Attest as server inputs; URLSession/Network for transport.
3. Record the trust matrix before implementation: target, capability/entitlement, merchant/product/service IDs, server role, nonce/challenge, account state, Keychain accessibility/access control, data retention/deletion, supported device/region, and offline/manual fallback. Mark unknown setup as `to-verify`.
4. Model separate state machines. For StoreKit, separate product loading, purchase, pending, verified/unverified, entitlement, expiry, refund/revocation, restore, and transaction finishing. For identity, separate request, user cancellation, credential receipt, account linking, server verification, credential revocation, sign-out, and deletion. For secrets/auth, separate item availability, policy evaluation, lockout, fallback, migration, and deletion.
5. Draw the proof boundary: `system result -> local validation -> server verification when required -> product policy -> user-facing effect`. A framework callback, product ID, token, credential, biometric result, pass, or device signal is not automatically the policy decision.
6. Keep free/local functionality useful when a paid, account, server, biometric, or integrity service is unavailable unless the user outcome inherently requires that service. Never unlock premium/security-sensitive effects from a local flag that stronger verification did not establish.
7. Minimize sensitive data. Keep tokens/private keys out of source, logs, analytics, URLs, screenshots, UserDefaults, ordinary model fields, and error messages. Use Keychain configuration appropriate to the threat model and define deletion, migration, reinstall, backup, restore, and access-group behavior.
8. Verify with deterministic fixtures first, then signed sandbox/TestFlight/physical-device and server evidence. Record environment, Apple Account/merchant/product configuration, device, OS, transaction/credential state, server response, and remaining release gaps; do not generalize local StoreKit or simulator results to production.

## Fast path

Start with a trust-and-authority ledger: actor, credential, system/server authority, replay boundary, user confirmation, and final commit. Prove one happy path plus denial, replay, cancellation, and offline recovery before adding optional providers or polishing secondary screens.

## Non-negotiable safety and evidence rules

- Never treat an unverified transaction, local “premium” flag, product ID, payment sheet/token, Wallet pass, Apple credential, biometric callback, Keychain item, DeviceCheck/App Attest signal, client-side certificate check, or successful HTTP response as sufficient entitlement, payment capture, identity, authorization, or absolute security proof.
- Keep local verification, server verification, and product policy visibly separate. State exactly which proof unlocks which effect and what happens when a service is unavailable or returns an ambiguous result.
- Do not store credentials, access tokens, private keys, payment data, health/personal data, or attestation material in logs, screenshots, analytics, source control, URLs, UserDefaults, or ordinary SwiftData fields.
- Do not add an account, payment route, backend, biometric prompt, tracking signal, or integrity telemetry beyond the stated user-facing need. Preserve supplied privacy scope and provide deletion/sign-out/account unlink behavior.
- Never claim production payment, entitlement, credential, app-integrity, hardware-security, or App Store readiness from previews, simulators, local fixtures, a successful compile, or a single sandbox run.

## Deliverable

Produce a compact route note or implementation change containing:

- selected framework and rejected alternatives;
- target, product/merchant/service IDs, capabilities, entitlements, account/server, Keychain, privacy, retention, region/device, and fallback matrix;
- purchase/credential/secret/integrity/network state machines with cancellation, retry, revocation, expiry, deletion, and stale-state behavior;
- exact local, server, signed sandbox/TestFlight, physical-device, App Store, privacy, signing, and release evidence plan;
- remaining `to-verify` gaps and claims deliberately not made.

For implementation, change only the requested target and directly related adapters/configuration. Do not add a server, account flow, payment capability, entitlement, secret, biometric prompt, integrity signal, analytics, or telemetry without a stated product need and authorization.

Further sections — read when the above is not enough: `references/details.md`.
