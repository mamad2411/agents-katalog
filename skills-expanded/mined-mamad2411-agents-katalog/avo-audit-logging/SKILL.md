---
name: avo-audit-logging
description: Track and visualize who changed, viewed, or acted on records in an Avo admin — an activity timeline, changeset diffs, and revert — powered by the Enterprise `avo-audit_logging` gem on top of `paper_trail` (or `audited`). Use when the user wants an audit trail / activity log for the admin, to see who edited a record and when, show a history or timeline of changes on a record, diff a changeset of an update, revert a record to a previous version, log every admin action for compliance, record who viewed a record, add accountability across the admin, or show all activity by a given user.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo Audit Logging

Audit logging records **who did what** in an Avo admin — every index/show visit, create, update, delete, attach/detach, and custom action — and shows it back as a timeline on the record, a changeset diff, a per-author activity table, and a global activity overview. It's an **Enterprise** add-on gem (`avo-audit_logging`) that sits on top of a versioning backend: [`paper_trail`](https://github.com/paper-trail-gem/paper_trail) (recommended, and what the installer sets up) or [`audited`](https://github.com/collectiveidea/audited). The gem captures activity into its own `avo_audit_logging_activities` table; the backend provides the per-attribute change history that powers the diff and the revert action.

Two things gate whether anything shows up, and they trip people constantly: audit logging is **disabled by default** (`config.enabled`), and even when enabled **nothing is tracked until a resource or action opts in** with `self.audit_logging = { activity: true }`. Both must be true.

## Docs

Authoritative docs — fetch on demand rather than guessing, and verify every option name against the docs or the app's installed gem source (`avo-audit_logging`) before writing it:

- Docs map (start here to discover pages): https://docs.avohq.io/4.0/docs-map.md
- Audit Logging guide: https://docs.avohq.io/4.0/audit-logging.md
- Custom controls (dependency): https://docs.avohq.io/4.0/custom-controls.md
- Authorization (dependency): https://docs.avohq.io/4.0/authorization.md
- Execution context (lambda scope for `activity:`): https://docs.avohq.io/4.0/execution-context.md

## Install

Audit logging is an **Avo Enterprise** feature — confirm the app has an Enterprise license before setting it up (otherwise the gem won't be available). It also relies on **custom controls** and **authorization**, which Avo Enterprise ships.

1. Add the gem, pointed at the private registry:

   ```ruby
   # Gemfile
   gem "avo-audit_logging", source: "https://packager.dev/avo-hq/"
   ```

   ```bash
   bundle install
   ```

2. Run the installer. This generates the activities migration, the activity resources/controllers, and appends an `Avo::AuditLogging.configure` block to `config/initializers/avo.rb`. It also runs `bundle add paper_trail` + `rails generate paper_trail:install --with-changes` **if paper_trail isn't already present**. `avo-diff_field` (which renders the changeset diff) is a hard dependency of the gem, so it comes in automatically.

   ```bash
   bin/rails generate avo:audit_logging install
   ```

3. Migrate — the feature's `enabled?` check literally verifies the `avo_audit_logging_activities` table exists, so this step is mandatory:

   ```bash
   bin/rails db:migrate
   ```

## When this applies

**Explicit (Avo / audit named):** "install/configure Avo audit logging", "enable the activity timeline", "add the `Avo::ResourceTools::Timeline` to this resource", "opt this resource into `self.audit_logging`", "add the revert/undo action", "show `avo_activities` / `avo_authored` on a resource", "add the global activity overview to the menu".

**Implicit (no mention of Avo audit logging):** "track who changed what in the admin", "I need an audit trail / activity log for the admin", "who edited this record and when", "show a history/timeline of changes on a record", "let admins revert a record to a previous version", "show the changeset diff of an update", "log every admin action for compliance", "record who *viewed* a record", "add accountability across the admin", "show all activity by a given user / everything user X did".

## Workflow

Install first (above), then work through these in order — display only works once tracking is enabled, and tracking only works once a resource opts in.

### 1. Enable it globally

The installer leaves it off. Turn it on in the initializer. `config.enabled = false` is a hard master switch that overrides every per-resource setting.

```ruby
# config/initializers/avo.rb
Avo::AuditLogging.configure do |config|
  config.enabled = true
end
```

### 2. Declare the author model(s)

Avo needs to know which models can be *authors* of activity so it can wire up the `avo_authored` association. The default is `["User"]` — if `User` is your only author model, **skip this step**. Otherwise:

```ruby
Avo::AuditLogging.configure do |config|
  config.enabled = true

  config.author_model = "Account"                 # a single author model
  # config.author_models = ["User", "Account"]    # …or several
end
```

`author_model=` is an alias for `author_models=`; both take model-name strings. If your author isn't `User` and you skip this, the per-author table (step 5) won't have an association to render.

### 3. Opt resources and actions into tracking

Nothing is recorded until you set `self.audit_logging` on a resource or action. `activity: true` turns on tracking for that resource/action:

```ruby
# app/avo/resources/product.rb
class Avo::Resources::Product < Avo::BaseResource
  self.audit_logging = {
    activity: true
  }

  def fields
    field :id, as: :id, link_to_record: true
    field :name, as: :text, link_to_record: true
    field :price, as: :number, step: 1
  end

  def actions
    action Avo::Actions::ChangePrice
  end
end
```

```ruby
# app/avo/actions/change_price.rb
class Avo::Actions::ChangePrice < Avo::BaseAction
  self.name = "Change Price"

  self.audit_logging = {
    activity: true
  }

  def fields
    field :price, as: :number
  end

  def handle(query:, fields:, **)
    query.each { |record| record.update!(price: fields[:price]) }
  end
end
```

`activity:` also accepts a **lambda** for conditional logging — e.g. log only for certain users. Inside it you get all [`Avo::ExecutionContext`](https://docs.avohq.io/4.0/execution-context.md) attributes plus `payload`, `action`, `records`, and `activity_class`:

```ruby
self.audit_logging = {
  activity: -> { current_user.audit_avo_activity? }
}
```

### 4. Show activity on a record

Two complementary displays:

- **Sidebar timeline** — a compact, streamlined feed via the gem's `Avo::ResourceTools::Timeline`, placed inside a `sidebar` block.
- **Full `has_many` table** — `field :avo_activities, as: :has_many` lists activities as a normal association table.

```ruby
# app/avo/resources/product.rb
class Avo::Resources::Product < Avo::BaseResource
  self.audit_logging = { activity: true }

  def fields
    panel do
      card do
        field :id, as: :id, link_to_record: true
        field :name, as: :text, link_to_record: true
        field :price, as: :number, step: 1
      end

      sidebar do
        tool Avo::ResourceTools::Timeline
      end
    end

    field :avo_activities, as: :has_many
  end
end
```

Timeline entries show a compact relative time (hover for the full timestamp); clicking one opens the activity's detail page with the full payload.

### 5. Enable the changeset diff and revert

Update activities show **no change log and no revert** until PaperTrail is tracking the *model itself*. Add `has_paper_trail` to the model to unlock the per-attribute diff and the built-in **Undo change** action (`Avo::Actions::Undo`, which reifies and saves the prior version):

```ruby
# app/models/product.rb
class Product < ApplicationRecord
  has_paper_trail
end
```

The changeset diff and the revert action are **`paper_trail`-only** — with the `audited` backend, activities are still tracked, but this step doesn't apply.

### 6. Show all activity by an author

Drop the reverse association onto the author resource to see everything a given user did:

```ruby
# app/avo/resources/user.rb
class Avo::Resources::User < Avo::BaseResource
  def fields
    field :id, as: :id, link_to_record: true
    field :email, as: :text, link_to_record: true
    field :avo_authored, as: :has_many, name: "Activity"
  end
end
```

If the author model isn't `User`, make sure step 2 is done first.

### 7. Add a global activity overview

For an admin-wide feed of every activity, add the generated `avo_activity` resource to the menu:

```ruby
# config/initializers/avo.rb
Avo.configure do |config|
  config.main_menu = -> {
    section "Audit Logging", icon: "presentation-chart-bar" do
      resource :avo_activity
    end
  }
end
```

### 8. Trim which controller actions get logged

Once a resource is opted in, **all** controller actions are logged (visits included). Silence specific ones under the `actions:` key:

```ruby
self.audit_logging = {
  activity: true,
  actions: {
    edit: false,
    show: false
  }
}
```

The full set of keys, all defaulting to `true`: `index`, `new`, `create`, `edit`, `update`, `show`, `destroy`, `attach`, `detach`, `handle`. (Logging `index`/`show` is how "who *viewed* a record" works — leave them on if that's the goal.)

## Gotchas

- **Enterprise-only.** Audit logging requires an Avo Enterprise license, plus the custom-controls and authorization features it builds on. See **avo-authorization** and **avo-custom-controls**.
- **Exactly one backend — this is the #1 failure.** You need `paper_trail` **or** `audited`, never both and never neither. With both installed (or neither), the pivot callbacks bail out early, the activity associations never register, and **nothing is tracked** — silently. The installer sets up paper_trail; if the app already has `audited`, don't also add paper_trail.
- **Diff + revert are `paper_trail`-only.** The changeset diff and the `Avo::Actions::Undo` revert require `paper_trail` (and `has_paper_trail` on the model, step 5). On `audited`, activity is tracked but there's no diff/revert.
- **Two switches, both required.** `config.enabled = true` **and** a per-resource/action `self.audit_logging = { activity: true }`. Miss either and you get nothing. `config.enabled = false` overrides everything.
- **You must migrate.** `enabled?` checks that the `avo_audit_logging_activities` table exists, so an un-migrated install behaves as disabled.
- **`enabled = false` doesn't hide *past* activity.** Disabling stops new recording but already-recorded activity still renders. To also hide the display, wrap the fields/tools in a condition, e.g. `if Avo::AuditLogging.configuration.enabled?` around `field :avo_authored, …`.
- **`changeset` always `nil`?** Rails is refusing to deserialize the YAML. Add the permitted classes in `config/application.rb`:

  ```ruby
  config.active_record.yaml_column_permitted_classes = [Symbol, Date, Time, ActiveSupport::TimeWithZone, ActiveSupport::TimeZone]
  ```

- **Non-`User` author.** If activity should be attributed to something other than `User`, set `config.author_model`/`author_models` (step 2) *before* relying on `avo_authored`, or the association won't exist on that model.
- **Verify before writing.** Option and association names (`config.enabled`, `author_model(s)`, `self.audit_logging`, `avo_activities`, `avo_authored`, `Avo::ResourceTools::Timeline`) can drift between versions — check the docs URL above or the installed gem source rather than trusting memory.

## Report

When done, tell the user:

- Whether the gem is installed and the generator/migration were run (or that those steps are still pending), and that it's an Enterprise feature.
- Which versioning backend is in play (`paper_trail` vs `audited`) and confirmation that **exactly one** is present.
- That `config.enabled` was set, the author model(s) configured, and **which resources/actions you opted in** with `self.audit_logging` — nothing tracks until they do.
- Which displays you wired up: sidebar `Timeline` tool, `avo_activities` table, `avo_authored` per-author table, and/or the `avo_activity` menu overview.
- Whether the changeset diff + revert are available (i.e. `has_paper_trail` added to the relevant models), or that they're unavailable because the app uses `audited`.
- Any follow-ups: run `db:migrate`, add the `yaml_column_permitted_classes` config if `changeset` comes back `nil`, or wrap displays in `enabled?` if they plan to toggle the feature off later.
