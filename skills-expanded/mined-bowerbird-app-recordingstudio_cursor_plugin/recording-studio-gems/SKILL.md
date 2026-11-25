---
name: recording-studio-gems
description: Choose an approved Recording Studio gem instead of a third-party library. Use when adding webhooks, billing, auth, access, admin, API, notifications, navigation, mixins, or any Gemfile dependency for a Recording Studio app. Use when tempted to add Pundit, a generic webhook engine, or another substitute.
---

# Recording Studio gems

Build with **these** gems. Do not add a third-party library that does the same job.

If the need is not on this list, **stop and ask**. Do not invent a substitute.

This skill is the kit. Each gem’s **README** is the API. Mixins: how to enable them is `recording-studio-capabilities`. Setup order: `recording-studio-getting-started`.

Repos live under [bowerbird-app](https://github.com/bowerbird-app). Ruby names are `recording_studio_*` unless noted.

## Platform

| Need | Gem | Follow |
|---|---|---|
| Recordings, recordables, events, logs | [`recording_studio`](https://github.com/bowerbird-app/RecordingStudio) | `recording-studio-saving`, `recording-studio-data-shape` |
| Access grants to any actor | [`recording_studio_accessible`](https://github.com/bowerbird-app/RecordingStudio_accessible) | `recording-studio-access` |
| Staff operations UI | [`recording_studio_admin`](https://github.com/bowerbird-app/RecordingStudio_admin) | `recording-studio-admin` |
| JSON / AI HTTP API | [`recording_studio_api`](https://github.com/bowerbird-app/RecordingStudio_api) | Wrapper with Accessible. Stores MCP widget ids (`ui:`); does not serve `ui://` (`recording-studio-api`) |
| App / API payload cache and rate limits | [`recording_studio_cache`](https://github.com/bowerbird-app/RecordingStudio_cache) | `RecordingStudioCache::RateLimiter` (and `fetch` / tree invalidation). Do not invent a limiter |
| Shared metrics | [`recording_studio_metrics`](https://github.com/bowerbird-app/RecordingStudio_metrics) | `RecordingStudioMetrics.register` / `execute`. API gate is that gem’s `api_authorize`. Do not teach Metrics Accessible or Admin auth |
| High-volume exhaust tables | [`recording_studio_logs`](https://github.com/bowerbird-app/RecordingStudio_logs) | `RecordingStudioLogs.register` / `aggregate`. Not recordings; not `log_event!` (`recording-studio-data-shape`) |
| OAuth authorization server (Connect, third-party apps) | [`recording_studio_oauth`](https://github.com/bowerbird-app/RecordingStudio_Oauth) | Resource server stays API. Accessible still authorizes |
| Remote MCP HTTP adapter | [`recording_studio_mcp`](https://github.com/bowerbird-app/RecordingStudio_MCP) | Protocol adapter over API + Accessible. Serves `ui://` when MCP UI is loaded. Not a second API |
| MCP Apps widgets | [`recording_studio_mcp_ui`](https://github.com/bowerbird-app/RecordingStudio_MCP_UI) | Register widgets; package HTML (FlatPack CSS/components). API stores the widget id; MCP serves `ui://` |
| Sign-in, invitations, people as actors | [`recording_studio_users`](https://github.com/bowerbird-app/RecordingStudio_users) | Auth identifies; Accessible still authorizes |
| Plans and usage on the **root** | [`recording_studio_billing`](https://github.com/bowerbird-app/RecordingStudio_billing) | Never `plan_id` on User |
| Switch workspace / site | [`recording_studio_root_switchable`](https://github.com/bowerbird-app/RecordingStudio_root_switchable) | Switcher is a helper/component (`recording-studio-ui`) |
| Menus and quick links | [`recording_studio_navigation`](https://github.com/bowerbird-app/RecordingStudio_navigation) | Gems register items; one host menu |
| Type icons | [`recording_studio_icons`](https://github.com/bowerbird-app/RecordingStudio_icons) | Reuse shared icons |
| Inbound provider webhooks | [`recording_studio_webhooks`](https://github.com/bowerbird-app/RecordingStudio_webhooks) | Endpoints are recordings; exhaust is logs (`recording-studio-data-shape`) |
| Notices | [`recording_studio_notifications`](https://github.com/bowerbird-app/RecordingStudio_notifications) | This gem’s tables, not a new recordable |
| Email as a notice channel | [`recording_studio_notifications_email`](https://github.com/bowerbird-app/RecordingStudio_notifications_email) | Pair with Notifications |
| Threads / chat | [`recording_studio_messages`](https://github.com/bowerbird-app/RecordingStudio_messages) | README |
| In-app AI on a root | [`recording_studio_ai`](https://github.com/bowerbird-app/RecordingStudio_AI) | Actors go through Accessible + API |
| Site-level category groups | [`recording_studio_site_categories`](https://github.com/bowerbird-app/RecordingStudio_site_categories) | Registry other gems register into |
| Screens, buttons, forms | [`flat_pack`](https://github.com/bowerbird-app/flatpack) | `recording-studio-flatpack`, `recording-studio-ui` |

Add a gem for a **need**, not because it exists. If it has UI or API, expose the **same domain action**.

MCP Apps split (do not collapse these into the API gem):

1. **API** stores widget ids (`ui:` on registrations).
2. **MCP** serves `ui://` resources when MCP UI is loaded.
3. **MCP UI** registers widgets and packages FlatPack HTML.

## Mixins

Opt-in **per recordable type**. Installing the gem does not enable it everywhere. How: `recording-studio-capabilities`.

| Need | Gem |
|---|---|
| Move in the tree | [`recording_studio_moveable`](https://github.com/bowerbird-app/RecordingStudio_moveable) |
| Duplicate | [`recording_studio_duplicatable`](https://github.com/bowerbird-app/RecordingStudio_duplicatable) |
| Attach files | [`recording_studio_attachable`](https://github.com/bowerbird-app/RecordingStudio_attachable) — provider controllers call `authorize_provider_upload!` |
| Comments | [`recording_studio_commentable`](https://github.com/bowerbird-app/RecordingStudio_commentable) |
| Trash / restore | [`recording_studio_trashable`](https://github.com/bowerbird-app/RecordingStudio_trashable) |
| Publish | [`recording_studio_publishable`](https://github.com/bowerbird-app/RecordingStudio_publishable) |
| Order / sort | [`recording_studio_orderable`](https://github.com/bowerbird-app/RecordingStudio_orderable) |
| Categories on a type | [`recording_studio_categorisable`](https://github.com/bowerbird-app/RecordingStudio_categorisable) |
| Export | [`recording_studio_exportable`](https://github.com/bowerbird-app/RecordingStudio_exportable) |
| Embed | [`recording_studio_embeddable`](https://github.com/bowerbird-app/RecordingStudio_Embeddable) |

Do not hand-roll move, trash, comments, attachments, or the rest when a mixin exists.

## New addon

Do not `rails plugin new`. Copy **[RecordingStudio_gem_template](https://github.com/bowerbird-app/RecordingStudio_gem_template)** and rename it (`recording-studio-new-gem`). Then add that gem to this list.

## Do not

- Pundit, CanCan, or `user.admin?` — use Accessible (and Admin as an **admin root**).
- A generic webhook engine (including `captain_hook`) — use `recording_studio_webhooks`.
- A user-centric billing gem or `plan_id` on User — use Billing on the root.
- One-off `app/controllers/api` that skips capability actions — use API.
- Homemade rate limiters or counters — use Cache `RateLimiter` and Metrics `register`.
- A second MCP server, raw `ui://` handler, or widget HTML outside MCP UI.
- Direct ActiveStorage upload routes that skip Attachable’s own direct-upload route and its checks.
- A second admin gem or `RecordingStudio_admin_depreciated`.
- `RecordingStudio_users_broken`.
- Devise-only ownership of the tree — Users identifies the actor; Accessible authorizes.
- This Cursor plugin as a Rails dependency — it is not a gem.

If a listed repo README still looks like the template, it is still the approved gem. Read that repo; do not replace it with a third-party.

## Related

`recording-studio-getting-started`, `recording-studio-capabilities`, `recording-studio-new-gem`.
