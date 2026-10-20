---
name: device-revocation-reset-flow
description: Implement a graceful credentials-invalid reset for PowerSync-style apps so account-deleted (410) or device-revoked (403) clients drop their local DB, clear localStorage, and restart signed-out without crashes.
category: auth
confidence: high
version: 1.0.0
version_origin: extracted
source_type: extracted-from-git
source_url: https://github.com/thunderbird/thunderbolt.git
source_ref: main
source_commit: 9d9c18ba511decfd3b45fc0f72c265d83355fe95
source_project: thunderbolt
imported_at: 2026-04-18T00:00:00Z
tags: [auth, powersync, devices, session, reset]
linked_knowledge: [device-revocation-status-codes-contract]
---

## When to use

A user deletes their account, or revokes a device from elsewhere. The revoked device is still running; you need it to cleanly reset without crashing when PowerSync sync wipes its local data.

## Steps

1. **Track device identity**: on first launch, mint a `deviceId` (uuidv7) and store it in `localStorage`. Send it as `X-Device-ID` on every PowerSync token request and `X-Device-Name` when you want to label it in the devices list.
2. **Backend device gate**: the `GET /powersync/token` handler, when given `X-Device-ID`, looks up the row in `devices`. If `status === 'REVOKED'` or `revoked_at IS NOT NULL`, return **403** with `{ code: 'DEVICE_DISCONNECTED' }` and no token. If the user no longer exists, return **410 Gone** with `{ code: 'ACCOUNT_DELETED' }`. If an existing `deviceId` is claimed by another user, return **409** with `{ code: 'DEVICE_ID_TAKEN' }`.
3. **Client connector**: when the token response is 410 or 403+DEVICE_DISCONNECTED or 409+DEVICE_ID_TAKEN, dispatch a `window.dispatchEvent(new CustomEvent('powersyncCredentialsInvalid', { detail: { reason } }))` event. Do **not** reset inside the connector — keep the reset in a React listener so it runs even if AuthProvider has already unmounted.
4. **Sync-row listener**: watch the current device's row via React Query with `getDevice(db, deviceId)` and key `['devices', deviceId]`. When the synced row has `revoked_at` or `status === 'REVOKED'`, trigger the reset.
5. **Reset handler**: `setSyncEnabled(false)` → `localStorage.clear()` → `resetAppDir()` (delete the SQLite file and app dir) → `window.location.replace('/')` (or `/account-deleted` for the 410 path).
6. **Sequence guard**: use refs (`hasTriggeredResetRef`, `hadDeviceOnceRef`) so you don't fire reset twice. For "device row missing", only trigger reset if you previously *had* the row — otherwise the first load before sync finishes would look indistinguishable from a delete.

## Counter / Caveats

- Mount the listener hook inside `AuthProvider` *before* its early return. Once the backend deletes the user, PowerSync sync wipes settings, `cloudUrl` disappears, and `AuthProvider` returns `null`. If the listener lived under those children, it never fires and the app wedges.
- Do not use 401 as a reset trigger. 401 is generic auth failure (stale token, clock skew) — treat it as a refresh hint, not a destructive signal.
- Revoke is idempotent: returning 204 on an already-revoked device keeps retry loops from hammering the DB.

## Evidence

- `src/hooks/use-powersync-credentials-invalid-listener.ts:1-113`
- `docs/powersync-account-devices.md:98-205`
- `docs/delete-account-and-revoke-device.md`
