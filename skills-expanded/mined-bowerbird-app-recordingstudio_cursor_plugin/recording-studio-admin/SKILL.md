---
name: recording-studio-admin
description: Set up Recording Studio Admin via an admin root and Accessible grants (not nominated admin users). Use when installing admin, mounting screens, defining sections or widgets, or deciding what belongs on an admin page. Prefer a few high-signal widgets over filling the section.
---

# Recording Studio admin

**Recording Studio Admin** is staff operations UI. Access is **Accessible** (`recording-studio-access`) — do not copy that skill’s install here. Page shape: `recording-studio-ui`. Words: `recording-studio-text`.

Install Accessible first, then this gem. Admin is one **mount point**. Other gems often ship a user slice *and* a separate admin slice.

## Admin root, not nominated admins

Do not set `user.admin = true`.

1. Create an **admin root** (a normal root — for example `AdminRoot`).
2. Mount admin **under that root**.
3. Grant Accessible access to that root (`grant_access`). Whoever can access it can use the admin UI, subject to roles.

Host app authenticates. Admin authorizes against a mandatory **access recording** (usually the admin root) with `RecordingStudioAccessible.authorized?`. If Accessible cannot express the policy, **stop and ask**.

Keep three concerns separate:

1. **Access recording** — which recording gates this mount
2. **Enabled sections** — which registered sections appear for the current recordable type
3. **Section recordable** — optional object created after a section opens

## Install Admin

```bash
bin/rails generate recording_studio_admin:install
bin/rails generate recording_studio_admin:admin_root   # optional host scaffolding
```

```ruby
gem "recording_studio_admin"

mount RecordingStudioAccessible::Engine, at: "/admin/access"
recording_studio_admin_for :admin, at: "/admin", root_section: :root

RecordingStudioAdmin.configure do |config|
  config.default_mount_path = "/admin"
  config.authentication_method = :authenticate_user!
  # Host auth identifies the actor. This gem’s hook is current_actor_method
  # (often :current_user). Some hosts set Current.actor instead.
  config.current_actor_method = :current_user
  config.access_recording_resolver = ->(context) {
    context.controller.current_admin_root_recording
  }
end
```

Fail closed: missing auth → `401`; missing access recording or Accessible denial → `403`. Default gate is Accessible `:view` before sections, widgets, or screen queries.

Enable sections on the admin root recordable:

```ruby
class AdminRoot < ApplicationRecord
  include RecordingStudio::Recordable
  include RecordingStudioAdmin::AllowsAdminSections

  recording_studio_recordable label: "Admin", root: true
  RecordingStudio.enable_capability(:accessible, on: self)

  recording_studio_admin_sections do
    section :root
    section :webhooks
  end
end
```

Access is Accessible: `grant_access` / `authorized?` (`recording-studio-access`). Do not add `AllowsAccessibleChildren` or homemade `admin?`.

## Screens and widgets

Keep definitions in `app/admin` and load them from `to_prepare`.

```text
app/admin/
  manifest.rb
  webhooks/
    manifest.rb
    section.rb                 # hub + maybe “failed last 24h”
    failed_deliveries/
      screen.rb
      table.rb
```

| Kind | Job |
|---|---|
| **Section** | Hub: links + a few signals |
| **Screen** | One operational job: filter, table, maybe a chart |
| **Widget** | Card that changes what someone does next (`number`, `list`, `chart`, `progress`). Extra-info when the title is not obvious (`recording-studio-text`) |
| **Resource** | Table actions; host owns the mutation controller |

```ruby
context.admin_screen_path("failed_deliveries")
context.admin_section_path("webhooks")
```

## Useful widgets, not filler

Empty space is fine. Do not add a widget per model or a screen per table.

Ask: what does staff **notice, decide, or fix**? If removing the widget would not change an action, delete it.

| Worth a widget | Rarely |
|---|---|
| Failed deliveries in 24 hours | Total webhooks ever |
| Invites waiting | Total users |
| Jobs stuck | A second chart of the same count |
| Usage vs plan | “Activity” with no decision |

**List** of work beats a vanity number. Do not repeat the same fact as number + chart + list.

A **section** is two to four signals plus links. A **screen** is one job (failed deliveries). A gem’s admin slice answers **that gem’s** operational questions — not a tour of the database.

Newcomer check: can they tell what needs them? Cryptic number → extra-info, not three more widgets.

## Wiring checklist

1. Actor can authenticate (`authentication_method`).
2. Current actor resolves (`current_actor_method` / `Current.actor` — host choice).
3. `access_recording_resolver` returns a real recording.
4. That recordable enables the needed sections.
5. Actor has Accessible access on that recording (usually `:view`).
6. Site-wide blast-radius screens: `site_admin_recording_resolver`.

## Guardrails

- Use Admin’s Flatpack rendering. Queries in definitions or services, not ERB.
- Exhaust belongs in **logs** (`recording-studio-data-shape`).
- Mutations: `RecordingStudioAdmin.authorize_resource!` and `perform_recording_studio_admin_action!`.
- Grant on the **admin root**, not a broad workspace grant to unlock one page.

Canonical: Admin README, `docs/gem_template/ADMIN_SCREENS.md`, dummy `test/dummy/app/admin`.
