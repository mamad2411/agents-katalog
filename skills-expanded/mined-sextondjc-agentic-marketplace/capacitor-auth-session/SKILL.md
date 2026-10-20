---
name: capacitor-auth-session
description: Use when implementing or hardening authentication and session management in CapacitorJS apps including OAuth/PKCE flows, deep-link callbacks, token lifecycle, secure refresh, and logout hygiene.
---

# Capacitor Auth Session

## Specialization

Implement and harden authentication/session flows in CapacitorJS hybrid apps with safe OAuth/PKCE, validated callback handling, secure token lifecycle, and deterministic session recovery.

## Trigger Conditions

- A Capacitor app is adding login, refresh, or logout flows.
- Auth behavior differs across web, iOS, and Android contexts.
- Tokens are mishandled in storage, logs, or deep-link callbacks.
- Session expiry or refresh failures degrade user experience.

## Inputs

- Identity provider and protocol (OAuth2/OIDC).
- Redirect URI and deep-link scheme configuration.
- Token TTL and refresh strategy requirements.
- Secure storage approach and risk level.

## Required Outputs

- Auth flow contract: login, callback, refresh, logout, and recovery.
- PKCE and state/nonce validation requirements.
- Secure token storage and rotation policy.
- Session failure handling and re-authentication UX rules.

## Deterministic Workflow

1. Define platform-specific redirect URI and callback constraints.
2. Enforce OAuth PKCE with state and nonce verification.
3. Store tokens using secure platform-backed storage only.
4. Implement proactive refresh before expiry with single-flight guard.
5. Handle refresh failure with deterministic re-auth flow.
6. Implement full logout: token revoke, storage purge, listener cleanup.
7. Validate deep-link callback host/path allowlist and replay protection.

## Session Safety Rules

- Never store access or refresh tokens in plain localStorage.
- Never trust callback parameters without state/nonce validation.
- Prevent parallel refresh storms using request coalescing.
- Rotate refresh tokens when provider supports rotation.
- Redact token-like strings from logs and telemetry.

## Quality Gates

- Login and callback pass PKCE and anti-replay checks.
- Refresh strategy prevents token-expiry race conditions.
- Logout fully invalidates local and remote session state.
- All auth errors map to user-safe actionable states.

## Done Criteria

- Auth/session contract is implemented and validated on target platforms.
- Token lifecycle and storage pass security checks.
- Session failure recovery paths are tested and documented.
