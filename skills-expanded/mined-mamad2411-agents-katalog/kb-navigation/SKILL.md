---
name: kb-navigation
description: Portable navigation patterns for Next.js App Router apps — config-driven nav items as SSOT, RBAC filtering at the config layer, badge count hook pattern, mobile bottom-nav + desktop sidebar composition with overflow sheet, collapsible groups, feature-flag gating at config level. Invoke when modeling navigation in a new app or feature. For kit-shipped components → `sk-navigation`.
last-verified: 2026-04-23
---

# kb-navigation — Portable Navigation Patterns

> Pair: [`sk-navigation`](../sk-navigation/SKILL.md)

Stack-anchored to Next.js App Router. Agnostic to any specific kit's component names or barrels. Use this skill to reason about how navigation _should_ be modeled in a new app or feature; use `sk-navigation` when integrating with the kit's shipped primitives.

---

## 1. Config-driven navigation (SSOT)

Every nav item lives in a single typed config array — not hardcoded inside the sidebar or tab bar. The rule: **changing navigation = editing one file**, never `.tsx` components.

- One config module exports the array. Components consume derived views of it (desktop sidebar, mobile tab bar, overflow sheet, breadcrumbs).
- Each item is a plain object with stable fields (label, route, icon ref, optional roles, optional children, optional feature flag). Icons imported by reference, not hardcoded strings.
- Derived helpers (pure functions) produce the filtered lists each surface needs. Components receive already-filtered data; they don't re-filter themselves.

**Why:** adding a route becomes one edit instead of N; RBAC and feature-flag gating stay centralized; a11y labels and analytics hooks have one canonical source.

---

## 2. RBAC filtering at the config layer

Each item may declare the roles allowed to see it. Filtering happens **before rendering**, ideally server-side when the session is already available.

- `roles` field is a string array of role names (or an empty/omitted field meaning "visible to any authenticated user").
- A pure helper `filterByRole(items, userRole)` walks the tree, drops items the user can't see, and recursively filters children. Collapsible parents with zero surviving children are auto-removed.
- Do the filter once, high in the tree (layout or shell), not inside each item component — that avoids layout shift and prevents leaking hidden routes into the DOM.

**Trust boundary:** config-level filtering is UX, not security. The route itself must still enforce authorization server-side (redirect / 403). Hiding an item from the nav is not access control.

---

## 3. Badge counts — hook-driven per item

Counts (unread notifications, pending approvals, inbox, etc.) attach to items without coupling the config to data fetching.

- Item declares an opaque `badge` key (e.g. `'notifications'`, `'pendingApprovals'`). The key identifies _which_ count, not _how_ to fetch it.
- A small registry maps keys to hooks: `{ notifications: useUnreadCount, pendingApprovals: usePendingCount }`. Each hook owns its own data source (SSE, polling with debounce, server action, cache subscription).
- Component renders the badge only when the hook returns `count > 0`. Zero renders nothing (no empty pill).
- Keep counts client-side and subscribed — not re-fetched on every render.

**Why:** config stays declarative; data-fetching strategy can evolve per badge without touching the nav components.

---

## 4. Mobile + desktop composition

Two surfaces, one config. Pick a single breakpoint and commit to it across the shell.

| Surface               | Breakpoint           | Content                                                                    |
| --------------------- | -------------------- | -------------------------------------------------------------------------- |
| Sidebar               | desktop (e.g. `≥lg`) | Full nav tree, collapsible groups, every visible item                      |
| Bottom tab bar        | mobile (e.g. `<lg`)  | Capped N primary tabs (4 is the iOS/Android norm) sorted by explicit order |
| Overflow "more" sheet | mobile (`<lg`)       | Every other visible item, grouped as in the sidebar                        |

**Rules of thumb:**

- Hard cap the bottom tab bar (4 primary + "More" = 5 slots). Extra primary tabs degrade thumb reachability.
- Primary tabs need a short label (≈ 10 chars). If the sidebar label is longer, support a `shortLabel` override rather than truncating at render time.
- Some items (e.g. a profile entry already reachable from a desktop avatar menu) should appear _only_ on mobile. Support a `mobileOnly` (or inverse `desktopOnly`) flag at the config level.
- Collapsible parents often have no real landing page (`/settings`). Let such items declare an alternative mobile href (e.g. "go to first child") so the tap on mobile lands on a real page.
- Respect `env(safe-area-inset-bottom)` on the bottom bar so the home indicator doesn't cover tappable targets.

---

## 5. Collapsible groups

Sidebar groups with children.

- Parent declares `collapsible: true` + `children: NavItem[]`. Children inherit role filtering recursively.
- Expand/collapse state is local UI state (component state, not URL). Persisting the open group across navigations is optional and belongs in `localStorage`, not in the route.
- Active-state resolution: a child active → parent is active _and_ expanded on mount.
- In the mobile "more" sheet, render groups as `section header + children grid` rather than a collapsible; mobile users expect all options visible at once.

---

## 6. Feature-flag gating

Items may be gated behind a feature flag at the config level.

- Item declares `featureFlag: 'flagKey'`. A helper resolves the flag against env / context / remote config and drops the item if disabled.
- Resolution happens in the same pass as RBAC — one traversal, one filtered tree.
- Do _not_ conditionally add items to the array at import time based on `process.env` — that hides the item from type-aware tooling and makes the config harder to read. Keep every item declared; let the filter resolve visibility.

---

## 7. Anti-patterns

- **Hardcoding items inside `Sidebar.tsx` / `BottomNav.tsx`.** Breaks the SSOT; every new route becomes a multi-file change and RBAC drifts per surface.
- **Running the RBAC check inside the item component.** Every hidden item still renders (and hydrates) before deciding to return `null`. Filter once, high up.
- **Reading roles from the client store to hide nav items.** If the client is the gate, hiding is race-prone and leaks into the DOM. Resolve on the server where possible.
- **Polling badge counts on every render.** Use a subscription (SSE / websocket) or a debounced interval, and cache at the hook level. Bare `useEffect` + `setInterval(fetch, 1000)` melts the server.
- **Truncating long labels at render time with CSS.** Declare `shortLabel` in the config so the author decides the abbreviation, not the viewport.
- **Using `href` as an identity key.** Item identity is separate from route (same route may appear in sidebar + more sheet with different labels). Give each item a stable `id` for keys and analytics.
- **Treating "hidden from nav" as "access denied".** It isn't. Always enforce authorization at the route/handler.

---

Cross-reference: [`sk-navigation`](../sk-navigation/SKILL.md) — kit-shipped. [`kb-security`](../kb-security/SKILL.md) — RBAC modeling. [`sk-features-index`](../sk-features-index/SKILL.md) — feature catalog.
