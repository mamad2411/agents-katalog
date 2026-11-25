---
name: recording-studio-getting-started
description: Map a new Recording Studio app from first decisions through core setup, Accessible, and which addons to include. Use when starting a product, adding Recording Studio to a Rails app, or choosing setup order. Prefer this skill over jumping into a single addon. For which gem to add, use recording-studio-gems. For a new addon gem, use recording-studio-new-gem.
---

# Getting started with Recording Studio

Treat a product as **gems around a thin host**, not a custom monolith. Philosophy: `recording-studio-big-picture`.

Order: **shape → core → Accessible → only the addons you need**. Do not invent access control, admin users, or one-off JSON endpoints.

## 1. Decide the shape

Answer these before generating models. Why: `recording-studio-big-picture`.

- **Root** — the bucket for content, settings, and **billing**. Not the signed-in user. Team workspace, site, or organisation. Confirm with the team before two types both sit at the top (**shared roots**).
- **Actors** — people, API clients, AI agents. Not “users only.”
- **Recordables** — types of tree content (`recording-studio-new-recordable`). Decide object vs fact, and hierarchy vs foreign key, before generating models (`recording-studio-data-shape`). Exhaust (deliveries, traces) is a **log**, not a child recording.

## 2. Install core

1. Add `recording_studio`, install migrations, `db:migrate`.
2. Generate the root recordable (for example `Workspace`) with `RecordingStudio::RootRecording`.
3. Set `RecordingStudio.configuration.root_recording_type`.
4. Implement `root_recording_for`.
5. Wire the current **actor**. Core’s hook is `RecordingStudio.configuration.current_user` — pass the actor (person or machine), not a Devise-only assumption. Other gems use their own keys (`Current.actor`, `current_actor_method`).

Core is recordings, recordables, events, logs, and the write path. It is **not** access control.

New addon gem: `recording-studio-new-gem`.

## 3. Add Accessible

Add it as soon as more than one actor can see a root. Grants, actors, and “stop and ask”: `recording-studio-access`. Admin as an admin root, not `user.admin?`: `recording-studio-admin`.

## 4. Choose addons

Pick from the approved kit (`recording-studio-gems`). Do not reach for a third-party gem that does the same job. Add a gem for a **need**, not because it exists. If that need has UI or API, expose the **same domain action**.

Typical first slice: **core → Accessible → auth → tree UI → API if agents → Admin if staff → Billing when you charge the root.**

Screens: `recording-studio-ui`. Components: `recording-studio-flatpack`. Words: `recording-studio-text`. Writes: `recording-studio-saving`. Tests: `recording-studio-tests`.

## Sequence

1. Name the root, actors, and first types.
2. Install core; wire `root_recording_for` and the current actor.
3. Add Accessible; grant access to the root.
4. Add auth. Still no custom ACL.
5. Tree UI + saving.
6. Root switchable if people have more than one root.
7. API when integrations or agents need the same actions.
8. Admin only for operations — admin root, few widgets.
9. Billing on the root.
10. Mixins as the tree needs them.
11. Domain logic in gems; host stays thin.
