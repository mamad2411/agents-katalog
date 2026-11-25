---
name: recording-studio-big-picture
description: Explain Recording Studio philosophy: roots as buckets, actors not only users, recordings vs events vs logs, and reusable gems. Use when designing the data model or deciding where behaviour belongs. For whether something is a Recording at all, use recording-studio-data-shape. For setup order use recording-studio-getting-started.
---

# Recording Studio big picture

Most of an app should be **reusable gems** on **Recording Studio core**, assembled by a thin host. Setup order and addons: `recording-studio-getting-started`.

## Recordings, recordables, events, logs

Core is a Basecamp-style `delegated_type` model:

| Layer | Role |
|---|---|
| **Recording** | Stable identity and mixin surface |
| **Recordable** | Immutable snapshot of state |
| **Event** | Append-only history of that recording |
| **Log** | Caused-but-unowned exhaust that must not clog the tree |

Prefer public helpers on `RecordingStudio` and `RecordingStudio::Recording`. Writes: `recording-studio-saving`. Whether something is a Recording at all — vs Event, Log, hierarchy vs foreign key — is `recording-studio-data-shape`.

**Roots** are recordings declared as the top-level **bucket**. Content, settings, and **billing** live on the root — not on the user. People and systems get **access** to the bucket (`recording-studio-access`). Hierarchy is natural: nested recordings inherit the bucket.

## Actors, not only users

A user is one actor. API clients, AI agents, and later types are actors too. Same Accessible path for all of them. Do not hard-code “only Devise users own everything.”

## Reusable gems

Assume **most of the product is reusable**. Extract a `recording-studio-*` addon instead of one-app code (`recording-studio-new-gem`). Prefer approved ecosystem gems over third-party substitutes (`recording-studio-gems`). Mixins are opt-in per type (`recording-studio-capabilities`).

If the gem has UI or API, they share **one domain action** (`recording-studio-ui`, `recording-studio-api`). Do not invent a second action for JSON.

Standard stack — do not replace these:

- Access: Accessible (ask if it cannot cover the case)
- Staff UI: Admin
- JSON: API
- Components: Flatpack

## Related

`recording-studio-getting-started`, `recording-studio-gems`, `recording-studio-data-shape`, `recording-studio-access`, `recording-studio-new-gem`.
