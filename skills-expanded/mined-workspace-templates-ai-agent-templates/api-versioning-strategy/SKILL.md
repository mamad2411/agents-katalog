---
name: api-versioning-strategy
description: Plans and introduces a new API version without breaking existing clients, with deprecation headers, usage tracking and a dated sunset schedule.
---

# API versioning strategy

Do not version what you can evolve. Version only what you must break.

## Steps

1. Classify the change. Safe: new optional field, new endpoint, new enum value only if clients are told to tolerate unknown ones. Breaking: removed or renamed field, changed type or meaning, new required input, stricter validation, changed status code.
2. If nothing breaks, ship it without a version and stop.
3. Pick the existing selector and stay with it. If none exists, use a URL prefix (`/v2/`) for public APIs or a date header for APIs with many small breaks.
4. Route by version at the edge of the app. Share the domain logic; put only the request and response mapping in per-version modules, so v1 is a thin adapter and not a copy of the code.
5. On the old version, send `Deprecation: true`, `Sunset: <HTTP date>` and a `Link: <migration guide>; rel="deprecation"` header.
6. Log the version, client id and route on every call so you can list who still uses the old version.
7. Write a migration note with before and after payloads for each break.
8. Propose a sunset date no earlier than the notice period the clients were promised. After the date, return 410 with the guide link.

## Rules

- Never change v1 behavior to suit v2.
- Never remove a version while traffic data shows active callers.
- Keep at most two live versions.

## Report

Breaking changes found, the selector chosen, files changed, the sunset date proposed and the clients still on the old version.
