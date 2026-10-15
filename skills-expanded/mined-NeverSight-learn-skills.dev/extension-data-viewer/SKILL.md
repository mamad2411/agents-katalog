---
name: extension-data-viewer
description: Admin-only paginated viewer for stable canister state. Use whenever the user asks for a viewer, dashboard, debug panel, or admin browse over backend data — users, items, orders, logs, or any stable Map/Set/Array/VarArray/List/Stack/Queue. Pre-installed in every Caffeine app via the `caffeineai-data-viewer` mops package; this skill explains what it does and how to keep using it correctly.
version: 0.1.0
compatibility:
  mops:
    caffeineai-data-viewer: "~0.1.0"
caffeineai-subscription: [none]
---

# Data Viewer

Admin-only data inspection extension for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral).

## Overview

Every Caffeine app ships with the `caffeineai-data-viewer` mops package and the moc `--generate-view-queries` flag enabled. Together with `include MixinViews()` in the actor, the compiler **auto-exposes a controller-only `__<var>` query** for every stable variable of a supported type:

- `Map.Map<K, V>` — `(?K, ?Nat) -> [(K, V)]`
- `Set.Set<K>` — `(?K, ?Nat) -> [K]`
- `[V]`, `[var V]`, `List.List<V>`, `Stack.Stack<V>`, `Queue.Queue<V>` — `(?Nat, ?Nat) -> [V]`

A `null` cursor starts at the beginning; a `null` count returns everything from the cursor. Each generated query traps on any non-controller caller — they exist for admin dashboards and debug viewers, not user-facing endpoints.

# Backend

The package and `include` are already wired into the template. You don't need to add or edit anything for the viewer to work — declare a stable variable of a supported type and the `__<var>` query appears automatically.

```motoko filepath=src/backend/main.mo
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import MixinViews "mo:caffeineai-data-viewer/MixinViews";

actor {
  include MixinViews();

  let users = Map.empty<Principal, Text>();

  // Generated automatically: __users : (ko : ?Principal, count : ?Nat) -> [(Principal, Text)] query
};
```

Lintoko rule `include-mixin-views` (shipped with the package) errors if the actor body is missing `include MixinViews();`. Keep the include — removing it disables every auto-generated viewer.

## Rules

- NEVER use the generated `__<var>` queries as a substitute for user-facing endpoints — they trap for any non-controller caller. Public list/feed/search methods still need to be written normally with `public query func listX(...)`.
- NEVER declare an actor member whose name starts with `__` — it either collides with an auto-generated query or hits a reserved prefix.
- Pure (immutable) collections (`pure/Map`, `pure/Set`, `pure/List`, `pure/Queue`) are **not** supported. The viewer is mutable-only by design; pure collection field access is a deprecated pattern in Caffeine projects anyway.
