---
name: ios-data-and-device-services
description: Route, implement, or review iOS persistence, CloudKit sync, HealthKit, Contacts, EventKit, WeatherKit, HomeKit, Core Bluetooth, Nearby Interaction, and local-network features. Use when an app stores personal data, syncs across devices, reads protected records, discovers accessories, measures proximity, or connects to a local service.
allowed-tools: Read, Grep, Glob
---

# iOS Data and Device Services

## Overview

Use this skill to keep app-owned data, Apple-managed records, external service state, device discovery, protocol trust, permissions, sync, and physical-world side effects distinct.

`user intent -> authorization/capability -> typed local state -> external/service operation -> stale/error/conflict handling -> reviewable result -> retention/deletion`

## Read before acting

- Inspect the actual Xcode targets, deployment target, platforms, model containers, schema/migrations, iCloud containers, capabilities, entitlements, usage descriptions, background modes, network/accessory protocols, and persistence/privacy adapters.
- Read the [data/persistence/sync route](../ios-knowledge-base/references/40-framework-routes/01-data-persistence-and-sync.md), [location/maps/weather route](../ios-knowledge-base/references/40-framework-routes/03-location-maps-and-places.md), [SwiftData/CloudKit deep dives](../ios-knowledge-base/references/41-framework-deep-dives/00-swiftdata-and-local-persistence.md), [HealthKit deep dive](../ios-knowledge-base/references/42-framework-deep-dives/01-healthkit-and-sensitive-data.md), [HomeKit/Bluetooth/Nearby deep dive](../ios-knowledge-base/references/42-framework-deep-dives/02-homekit-bluetooth-and-nearby.md), and [contacts/calendar/network deep dives](../ios-knowledge-base/references/43-system-framework-deep-dives/01-contacts-calendar-and-notifications.md).
- Refresh the exact official pages in the Sources section before relying on an authorization status, capability, entitlement, iCloud/account behavior, protected-data rule, radio state, local-network prompt, weather freshness, or background-delivery claim.

## Route workflow

1. State the user-owned outcome and data class: private local record, synced record, selected HealthKit/Contacts/EventKit data, weather observation, HomeKit physical state, Bluetooth protocol, Nearby distance/direction, or local-network service.
2. Choose the smallest storage/service route. Use SwiftData for structured local records, files for large user-owned data, Keychain for secrets, CloudKit only when cross-device/shared replication is needed, and the narrow system framework for protected data or device access. Do not add a backend or account to solve a local-first problem.
3. Record the target matrix before implementation: platform/device family, permission and usage description, capability/entitlement, account/service state, model/schema version, data retention/deletion, supported accessory/protocol, network topology, and offline/manual fallback. Mark unknown availability as `to-verify`.
4. Separate state layers. Keep local persistence, migration, sync/account, authorization, discovery, trust/protocol, operation, freshness, conflict, and user review as separate states; never collapse them into `isConnected`, `isAuthorized`, `isSynced`, or `hasData`.
5. Draw the operation boundary: `intent -> check current state -> validate target/schema -> perform bounded operation -> reconcile callback/change -> persist projection -> show stale/error/retry/manual route`. Make writes idempotent where a duplicate can cause harm.
6. Define privacy and retention before querying or logging. Ask for the minimum type/field/date range, keep raw health/contact/location/home/radio data out of logs, minimize synced projections, explain what leaves the device, and provide app-side deletion/export/revocation behavior.
7. Bound asynchronous work. Cancel queries, observations, sync batches, discovery scans, connections, ranging sessions, and retries when the feature no longer owns them. Finish observer/background callbacks, release radio sessions, and ignore stale callbacks after cancellation.
8. Verify with fixtures first, then signed physical devices and real services/accessories. Record OS, device, account, authorization state, dataset, schema/environment, accessory firmware, network topology, timestamp, and observed latency/freshness; do not generalize one successful run.

## Fast path

Write a truth-ownership table first: local, Apple system, remote, or derived. Implement one create/read/update/delete or observation slice with migration, conflict, and offline behavior, and add CloudKit, HealthKit, Contacts, or an accessory only when the table shows that service owns a required boundary.

## Persistence and sync boundaries

- Keep a domain model independent of SwiftData/Core Data/CloudKit. Use SwiftData `ModelContainer`/`ModelContext` and explicit schema/migration policy for local records; use `ModelActor` or an intentional isolation boundary for background persistence.
- Store large media/files outside record rows with stable references and coordinated deletion. Keep secrets in Keychain, not UserDefaults, logs, analytics, URLs, or ordinary model fields.
- CloudKit is replication with account, container, environment, network, quota, conflict, deletion, and schema state. It is not automatically the app’s only source of truth. Model iCloud unavailable, account changes, remote deletion, duplicate edits, server-record conflicts, schema migration, and partial/offline state.
- Treat a local write, successful save, change token, sync event, or last-known projection as evidence about one boundary only. Do not label it “synced,” “current,” “backed up,” or “shared” without the corresponding account/environment and reconciliation evidence.
- For reviewable AI-derived or external records, persist source identifiers, timestamps, model/algorithm version, provenance, review/edit state, and deletion relationship. Do not silently promote generated data into domain truth.

## Protected personal data

- HealthKit authorization is fine-grained and privacy-preserving. A processed authorization request does not mean every type was granted; an empty read does not prove denial or absence of data. Query only needed types/ranges and preserve source/date/unit metadata.
- HealthKit observer updates indicate that matching data changed; follow with a bounded query, call the background completion handler, and handle limited history, deletions, account/device changes, and unavailable data. Never turn a missing sample or derived trend into a diagnosis, treatment, medical necessity, or guaranteed wellness claim.
- Contacts and EventKit are external user-owned stores. Choose picker/store authorization deliberately, request the minimum access, handle revoked/limited access, stale identifiers, user edits/deletions, duplicate events, time zones, and write confirmation. An imported contact or event is not permission to message, modify, or expose it elsewhere.
- WeatherKit results have service/entitlement, location, attribution, network, timestamp, forecast/historical scope, and cache/freshness state. Label location and observation time; do not present a forecast as a guarantee or a cached value as current.

Further sections — read when the above is not enough: `references/details.md`.
