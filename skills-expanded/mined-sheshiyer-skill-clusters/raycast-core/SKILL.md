---
name: raycast-core
description: "Shared reference for the Raycast cluster: command types (view / no-view / menu-bar), the @raycast/api component & navigation model, the package.json manifest, preferences, data/storage hooks, and the build/develop/publish flow. USE WHEN building a Raycast extension and you need the cross-cutting model the spokes share. Exact API signatures: defer to developers.raycast.com."
cluster: raycast
version: 1.0.0
---

# Raycast Core

Shared model for the `raycast` cluster. Extensions are React + TypeScript apps rendered inside
Raycast. Keep these concepts consistent across spokes. For exact, current API signatures, defer
to the official docs (developers.raycast.com) — this is the mental model, not an API dump.

## 1. Command types (declared in the manifest)

- **view** — renders a React UI (`List`, `Grid`, `Detail`, `Form`).
- **no-view** — runs logic and returns (background/script-like; show feedback via `showHUD`/`showToast`).
- **menu-bar** — a menu-bar extra (`MenuBarExtra`) that can refresh on an interval.

Each command is an entry in the manifest with its own `mode` and default export.

## 2. The manifest (`package.json`)

Raycast extensions are configured in `package.json`, not code: extension `name`/`title`/`description`/`icon`, the **`commands[]`** array (each with `name`, `title`, `mode`), **`preferences[]`**, **`tools[]`** (for AI extensions → `raycast-ai-extensions`), and `categories`. The file is the source of truth for what Raycast shows and runs.

## 3. UI & navigation (`@raycast/api`)

- Containers: `List` (searchable rows + `List.Item`), `Grid`, `Detail` (markdown), `Form` (inputs).
- Every item exposes an **`ActionPanel`** of **`Action`**s (the ⌘K actions) — this is how users act on results.
- Navigation: `useNavigation().push()/pop()` to move between views; Raycast manages the stack.

## 4. Preferences & environment

- Declare preferences in the manifest; read with `getPreferenceValues<T>()`. Per-command or extension-wide; types include password (secret) fields.
- `environment` exposes runtime info; `LaunchProps` carries arguments/launch context.

## 5. Data, async & storage

- Data hooks (from `@raycast/utils`): `useFetch`, `useCachedPromise`, `useExec`, `usePromise` — they handle loading/error/revalidation and pair with `List`'s `isLoading`.
- Persistence: `LocalStorage` (key/value) and `Cache` for cross-launch state.
- Feedback: `showToast` (Success/Failure/Animated), `showHUD`, `confirmAlert` for destructive actions.

## 6. Build / develop / publish

- `ray develop` (or `npm run dev`) — live-reload into Raycast while building.
- `ray build` — typecheck + bundle.
- **Publish** = submit to the Raycast Store via PR to `raycastapp/extensions` → `raycast-store-publishing`.

## 7. Two different "Raycast" jobs (don't conflate)

- **Building an extension** that runs *inside* Raycast → `raycast-extension` (+ this core).
- **Designing your own app** to *look like* Raycast (light mode, Inter, 4px grid) → `raycast-ui-skills`. This is an aesthetic, not the extension API.

## 8. Shared guardrails

- Manifest is the source of truth — keep `commands[]`/`preferences[]`/`tools[]` in sync with code.
- Use the `@raycast/utils` data hooks for `isLoading`/error/revalidation instead of hand-rolled state.
- Confirm destructive actions (`confirmAlert`); never print secrets read from preferences.
- Defer exact/changing API signatures to developers.raycast.com rather than guessing.
