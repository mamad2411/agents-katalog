---
name: avo-notifications
description: Add and send in-app notifications in an Avo admin panel with the avo-notifications add-on — a bell dropdown in the navbar plus a full notifications resource, sent with `Avo::Notifications.send(to:, title:, ...)` from actions, model callbacks, or jobs, with severity levels, type tags, up to 3 action buttons, per-recipient read/saved/done state, and optional real-time delivery over ActionCable. Use when the user wants to notify admins when an order comes in, tell a user their export/report is ready, alert admins about a signup spike, ping a reviewer when something needs approval, add an in-app inbox / notification center / bell badge, let admins mark messages read, push a maintenance message to all users, add Approve/Reject buttons to an alert, or get real-time notifications without a page refresh.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo Notifications

Avo Notifications is a **paid add-on** that gives an Avo admin panel an in-app notification system: a bell icon with an unread badge in the navbar, a dropdown of recent items, and a full Avo resource for browsing/managing them. You create notifications from anywhere in the app with one call — `Avo::Notifications.send(...)` — and each one is delivered to a specific recipient, optionally in real time over ActionCable.

- **Send API:** `Avo::Notifications.send(to:, title:, body:, level:, notification_type:, url:, sender:, buttons:)` (aliased `Avo::Notifications.notify`).
- **Recipient-owned:** there are no shared "global" rows — every recipient gets their own row, so read/saved/done state is always per user.
- **License:** paid add-on ([avohq.io/addons/notifications](https://avohq.io/addons/notifications)). ActionCable is optional and only needed for real-time delivery.

**Docs** — fetch on demand with WebFetch; prefer the raw `.md` (clean, no HTML):

- Guide (tasks + worked examples): https://docs.avohq.io/4.0/notifications.md
- Reference (every config option, `send` parameter, query method + validation rules): https://docs.avohq.io/4.0/notifications-api.md
- Docs map (find any other Avo page): https://docs.avohq.io/4.0/docs-map.md

Read the guide before implementing anything non-trivial, and the reference whenever you need the exact signature, default, or validation of a parameter.

## Install

The add-on ships an installer that generates a migration, an initializer, an Avo resource, and a controller. Do the steps in order:

1. **Add the gem** (private package source):

   ```ruby
   # Gemfile
   gem "avo-notifications", source: "https://packager.dev/avo-hq/"
   ```

   Then `bundle install`.

2. **Run the installer:**

   ```bash
   bin/rails generate avo:notifications install
   ```

   Generates: a migration for the `avo_notifications_notifications` table, `config/initializers/avo_notifications.rb`, `app/avo/resources/avo_notification.rb`, and `app/controllers/avo/avo_notifications_controller.rb`.

3. **Migrate:**

   ```bash
   bin/rails db:migrate
   ```

4. **Include the concern in the recipient model** (usually `User`):

   ```ruby
   # app/models/user.rb
   class User < ApplicationRecord
     include Avo::Notifications::HasNotifications
   end
   ```

   This adds an `avo_notifications` association plus the per-user read-state helpers.

The bell component then mounts itself in the navbar automatically — no view wiring needed.

## When this applies

Reach for this add-on when the request is "**let the admin see / send an in-app message**" — a bell, an inbox, an alert, an approval ping:

| Request | What to build |
| --- | --- |
| "Notify admins when an order comes in", "ping a reviewer when something needs approval" | `send` to a user or a relation, usually from a model callback or an action |
| "Tell the user their export/report is ready" | `send` from the background job, `level: :success`, a `url:` to the result |
| "Alert admins about a signup spike" | `send` to `User.where(admin: true)` |
| "Push a maintenance message to everyone" | `send(to: :all, level: :warning)` |
| "Add Approve/Reject buttons to an alert" | `send` with `buttons:` (up to 3) |
| "Add an in-app inbox / notification center / unread badge" | install the add-on — the bell + resource are automatic |
| "Let admins mark messages read / saved / done" | the bell hover actions + resource bulk actions are built in; drive them in code with the state API |
| "Real-time notifications without a page refresh" | keep `config.realtime = true` and configure ActionCable |

If the notification is sent **from an Avo action** (bulk-approve, then notify the owner), build the action with the **`avo-actions`** skill and call `Avo::Notifications.send` inside its `handle`.

## Workflow

### 1. Send a notification

`to:` and `title:` are the only required arguments. Everything else is optional.

```ruby
Avo::Notifications.send(
  to: user,
  title: "Your export is ready",
  body: "The report finished processing.",
  level: :success,
  url: "/admin/exports/42"
)
```

- `level:` — `:info` (default), `:success`, `:warning`, or `:error`; sets the icon and color.
- `notification_type:` — a freeform tag (`"mention"`, `"system"`, `"billing"`) rendered as a small label on the row.
- `url:` — where clicking the title navigates.
- `sender:` — the record that sent it, for attribution (its name is resolved via `user_display_name_method`).
- `buttons:` — up to 3 action buttons, each `{ label:, url:, method: }` (`method` defaults to `"get"`).

### 2. Choose who receives it

The `to:` argument fans out into one row per recipient, so state is tracked per user:

```ruby
# One user — returns the notification
Avo::Notifications.send(to: @user, title: "Welcome!")

# A relation — one row each, returns an Array
Avo::Notifications.send(to: User.where(admin: true), title: "New signup spike")

# Everyone (every record of `user_class`) — returns an Array
Avo::Notifications.send(to: :all, title: "Maintenance tonight at 10 PM", level: :warning)
```

### 3. Send from where the event happens

From an Avo action's `handle`:

```ruby
# app/avo/actions/approve_project.rb
def handle(query:, current_user:, **args)
  query.each do |project|
    project.approve!
    Avo::Notifications.send(
      to: project.owner,
      title: "Your project was approved",
      body: "#{current_user.name} approved '#{project.name}'.",
      level: :success,
      sender: current_user,
      url: "/admin/projects/#{project.id}"
    )
  end
  succeed "#{query.count} project(s) approved."
end
```

From a model callback:

```ruby
# app/models/order.rb
after_update :notify_status_change

def notify_status_change
  return unless saved_change_to_status?
  Avo::Notifications.send(to: user, title: "Order ##{id} is now #{status}", url: "/admin/orders/#{id}")
end
```

From a background job — send after the work finishes, with a `url:` to the result:

```ruby
Avo::Notifications.send(to: user, title: "Your export is ready", level: :success, url: export.download_url)
```

### 4. Add action buttons (optional)

```ruby
Avo::Notifications.send(
  to: @user,
  title: "Project review pending",
  buttons: [
    { label: "Approve", url: "/projects/#{@project.id}/approve", method: "post" },
    { label: "Reject",  url: "/projects/#{@project.id}/reject",  method: "post" },
    { label: "View",    url: "/projects/#{@project.id}" }
  ]
)
```

### 5. Read state (drive the badge / a custom UI)

```ruby
Avo::Notifications.for_user(user, limit: 10)   # the inbox (not-done, newest first)
Avo::Notifications.unread_count(user)          # drives the bell badge
Avo::Notifications.mark_all_as_read(user)
```

After the `HasNotifications` concern, the model exposes the same directly: `user.unread_avo_notifications_count`, `user.mark_all_avo_notifications_read!`, `user.avo_notification_unread?(notification)`.

### 6. Configure (optional)

Every option in `config/initializers/avo_notifications.rb` has a sensible default; an empty block works out of the box.

```ruby
Avo::Notifications.configure do |config|
  config.ttl = 30.days                    # kept this long before cleanup can delete
  config.realtime = true                  # real-time delivery via ActionCable
  config.dropdown_limit = 10              # rows in the bell dropdown
  config.user_class = "User"             # model used to resolve `to: :all`
  config.user_display_name_method = :name # method for sender attribution
end
```

### 7. Schedule cleanup

Every notification gets an `expires_at` from `ttl`. Delete expired rows with the rake task — schedule it daily:

```bash
bin/rails avo_notifications:cleanup
# 0 2 * * * cd /path/to/app && bin/rails avo_notifications:cleanup
```

## Key API

**Send** — `Avo::Notifications.send(to:, title:, body: nil, level: :info, notification_type: nil, url: nil, sender: nil, buttons: nil)` (alias `notify`). Return value depends on `to:` — a single record returns the notification; an Array or `:all` returns an Array.

**Levels** — `:info` (blue), `:success` (green), `:warning` (amber), `:error` (red).

**Buttons** — Array of up to 3 Hashes, each `{ label:, url:, method: }`; `method` is `get`/`post`/`patch`/`put`/`delete` (case-insensitive), default `"get"`.

**Query & state** (module methods on `Avo::Notifications`):

| Method | Does |
| --- | --- |
| `for_user(user, limit:)` | The inbox — not-done, newest first (a relation). |
| `unread_count(user)` | Unread count in the inbox (done excluded). |
| `mark_all_as_read(user)` | Mark the whole unread inbox read. |
| `mark_as_read` / `mark_as_unread` | Toggle read on one notification (`read_at`). |
| `save_for_later` / `unsave` | Toggle the "saved" bookmark (`saved_at`). |
| `mark_as_done` / `mark_as_undone` | Archive out of / back into the inbox (`marked_as_done_at`). |
| `cleanup_expired!` | Delete rows past `expires_at` (also the `avo_notifications:cleanup` rake task). |

The three states (**read**, **saved**, **done**) are independent and each tracked per recipient row.

**Config options** — `ttl` (`30.days`), `realtime` (`true`), `dropdown_limit` (`10`), `user_class` (`"User"`), `user_display_name_method` (`:name`).

## Gotchas

- **No global notifications.** Every recipient gets a row. `to:` fans out: a relation or `:all` returns an **Array**; a single record returns **one** notification. Don't expect a shared row you can mutate once for everyone.
- **A blank `to:` raises; an empty Array is a no-op.** `to: nil` or `to: ""` raises `Avo::Notifications::Error` — notifications must be addressed. `to: []` deliberately sends nothing and returns `[]`, so `send(to: User.where(...))` on a relation that matches no one is safe.
- **`title` is required and capped at 255 chars.** Blank or over 255 raises. `body` is the place for longer text.
- **`level` must be one of the four.** Any other symbol raises — validate user-supplied levels before passing them.
- **`buttons` validation is strict.** Max 3; each must be a Hash with a non-blank `label` and `url`; `method`, if present, must be a supported verb. Anything else raises.
- **Real-time is best-effort.** With `realtime = true` but no ActionCable configured (or no running server), broadcasting is **silently skipped** — notifications still land and appear on the next page load. Broadcast errors are logged, never raised. Don't rely on real-time as the only delivery path.
- **The generated resource is hidden from the sidebar by design** (`self.visible_on_sidebar = false`) — it's reached through the bell's "View all" link. It's a plain Avo resource: edit `app/avo/resources/avo_notification.rb` to add fields/filters/actions or flip it onto the sidebar.
- **Sending from an action is the `avo-actions` skill's job.** Build the action there; just call `Avo::Notifications.send` inside its `handle`.

## Report

When done, tell the user:

- Whether you **installed** the add-on (gem + generator + migrate + concern) or just added sending code to an existing install.
- **Where** notifications are sent from (which action/model callback/job) and to **whom** (`to:` a record / relation / `:all`).
- The **shape** of each notification: `level`, any `notification_type`, `url`, `sender`, and buttons.
- Any **follow-ups** the user still owns: adding `include Avo::Notifications::HasNotifications` to the recipient model, configuring ActionCable for real time, tuning `config/initializers/avo_notifications.rb`, or scheduling `avo_notifications:cleanup`.
