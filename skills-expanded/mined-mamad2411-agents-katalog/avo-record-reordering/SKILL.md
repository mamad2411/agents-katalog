---
name: avo-record-reordering
description: Let admins arrange records in a persistent, user-defined order in an Avo resource — via up/down/top/bottom buttons or drag-and-drop on the Index or has_many association view — by configuring the `self.ordering` resource attribute in `app/avo/resources/<name>.rb`. Use when the user wants to reorder records, add up/down (move higher/lower) arrows, make a list sortable by position, drag-and-drop to rearrange rows, order carousel slides / menu items / gallery images / steps, add a position field and let staff arrange the order, or persist a manual sort order for a table. Pairs with acts_as_list.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo Record Reordering

Record reordering lets admins arrange records in a specific, persistent order — reordering `Slide`s in a `Carousel`, `MenuItem`s in a `Menu`, gallery images, or ordered steps — using move buttons (up / down / to-top / to-bottom) or drag-and-drop on the **Index** view or a `has_many` **association** view. It's configured entirely through one class attribute, `self.ordering`, on the resource at `app/avo/resources/<name>.rb` — there is **no generator**; you add the attribute by hand.

**This is a paid add-on.** Record reordering ships in a separate licensed package and only works on installs that have the add-on enabled. Say so up front if the user hasn't already confirmed they have it — the config below is inert without the license.

Avo doesn't move records itself: each control is a plain lambda you write, so the actual position change is delegated to your model — most naturally the [`acts_as_list`](https://github.com/brendon/acts_as_list) gem (which provides `move_higher` / `move_lower` / `move_to_top` / `move_to_bottom` / `insert_at`), or your own positioning logic.

## Docs

Authoritative docs — fetch on demand rather than guessing, and verify every option name against the docs or the app's installed Avo source before writing it:

- Docs map (start here to discover pages): https://docs.avohq.io/4.0/docs-map.md
- Record reordering guide: https://docs.avohq.io/4.0/record-reordering.md
- Record reordering API reference: https://docs.avohq.io/4.0/record-reordering-api.md
- Resources API (for `index_query`): https://docs.avohq.io/4.0/resources-api.md
- Authorization (for the `reorder?` policy): https://docs.avohq.io/4.0/authorization.md

## When this applies

**Explicit (Avo named):** "add record reordering to the `Slide` resource", "configure `self.ordering`", "enable drag-and-drop reordering", "show the move up/down buttons on the association view", "let me reorder from the Index".

**Implicit (product-shaped, no mention of Avo):** "let admins drag to reorder the carousel slides / menu items", "add up/down arrows to sort these records", "make this list sortable by position", "reorder the gallery images by dragging", "add a position field and let staff arrange the order", "I want a manual sort order that sticks", "let editors move a featured post to the top".

If the request is really about *default* sorting (sort by a column, newest first) with no user-driven rearranging, that's `self.default_sort_column` / `self.index_query` on the plain resource — not this add-on.

## Workflow

### 1. Give the model a position and a positioning API

Reordering needs somewhere to store the order and methods that change it. The standard path is `acts_as_list`:

```ruby
# Gemfile
gem "acts_as_list"

# app/models/slide.rb
class Slide < ApplicationRecord
  belongs_to :carousel
  acts_as_list scope: :carousel   # drop the scope for a single global list
end
```

Add an integer `position` column if the model doesn't have one, and **backfill existing rows** — `acts_as_list` misbehaves when some records have a `NULL` position:

```bash
bin/rails g migration AddPositionToSlides position:integer
bin/rails db:migrate
# then, in a console or a one-off task: Slide.order(:created_at).each.with_index(1) { |s, i| s.update_column(:position, i) }
```

`acts_as_list` then gives each record `move_higher`, `move_lower`, `move_to_top`, `move_to_bottom`, and `insert_at(n)`. Not using the gem? Implement equivalent methods (or inline the SQL) — the lambdas in step 2 just have to change the persisted order somehow.

### 2. Add `self.ordering` to the resource

Configure the buttons and wire each control to a model method. `record` inside every lambda is the instantiated model being moved:

```ruby
# app/avo/resources/slide.rb
class Avo::Resources::Slide < Avo::BaseResource
  self.ordering = {
    visible_on: :index,
    actions: {
      higher: -> { record.move_higher },
      lower: -> { record.move_lower },
      to_top: -> { record.move_to_top },
      to_bottom: -> { record.move_to_bottom },
    }
  }

  def fields
    field :id, as: :id
    field :name, as: :text
    field :position, as: :number
  end
end
```

By default the controls sit behind a popover trigger. To keep them visible in every row (good for lists you reorder often), add `display_inline: true`. Each lambda also has access to `resource`, `options` (the whole `ordering` hash), and `params`.

### 3. Choose where the controls appear — `visible_on` is mandatory

`visible_on` has **no implicit default**. Omit it and the buttons render nowhere, even with actions defined. Always set it:

- `:index` — controls on the resource's own Index view.
- `:association` — controls only inside the `has_many` association view (use this when order only makes sense within a parent, e.g. `Slide`s of one `Carousel`, `MenuItem`s of one `Menu`).
- `[:index, :association]` — both.

```ruby
self.ordering = {
  visible_on: [:index, :association],
  actions: { higher: -> { record.move_higher }, lower: -> { record.move_lower } }
}
```

### 4. Sort the Index by position

Defining `ordering` does **not** sort the list — it only adds controls. Without a sort, records won't visibly stay in their new order after a move. Order the Index query by the position column with `self.index_query` (Avo-only; preferred):

```ruby
class Avo::Resources::Slide < Avo::BaseResource
  self.index_query = -> { query.order(position: :asc) }

  self.ordering = {
    display_inline: true,
    visible_on: :index,
    actions: {
      higher: -> { record.move_higher },
      lower: -> { record.move_lower },
      to_top: -> { record.move_to_top },
      to_bottom: -> { record.move_to_bottom },
    }
  }
end
```

Alternatively add a `default_scope { order(:position) }` on the model — but that applies to *every* query app-wide, so only reach for it when you want that globally. Prefer `index_query`.

### 5. (Optional) Enable drag-and-drop

Drag handles need **both** `drag_and_drop: true` **and** an `insert_at` action — with either missing, handles don't render. Inside `insert_at`, the `position` local is the target position (an `Integer`) Avo computes from where the row was dropped:

```ruby
self.ordering = {
  drag_and_drop: true,
  display_inline: true,
  visible_on: [:index, :association],
  actions: {
    higher: -> { record.move_higher },
    lower: -> { record.move_lower },
    to_top: -> { record.move_to_top },
    to_bottom: -> { record.move_to_bottom },
    insert_at: -> { record.insert_at position },
  }
}
```

To compute the drop target, Avo reads the position of the first record in the list — by default `record.position` (what `acts_as_list` exposes). If your column/getter is named differently, point `position:` at it:

```ruby
self.ordering = {
  position: -> { record.position_in_list },
  drag_and_drop: true,
  visible_on: :index,
  actions: { insert_at: -> { record.insert_at position }, higher: -> { record.move_higher }, lower: -> { record.move_lower } }
}
```

### 6. Authorize reordering

If the app uses [authorization](https://docs.avohq.io/4.0/authorization.md) (see the **avo-authorization** skill), the controls are gated by the `reorder?` policy method — Avo silently hides them when it returns false. Add it to the record's policy:

```ruby
# app/policies/slide_policy.rb
class SlidePolicy < ApplicationPolicy
  def reorder? = edit?          # or a custom rule, e.g. user.can_reorder_items?
end
```

## Key options

All keys live inside the `self.ordering` Hash on the resource.

| Key | Does | Tiny example |
| --- | --- | --- |
| `visible_on` | **Required.** Which views show controls; no default → omit and nothing renders | `visible_on: :index` (`:association` / `[:index, :association]`) |
| `actions` | Hash of lambdas that change position; controls render only if ≥1 is defined | `actions: { higher: -> { record.move_higher } }` |
| `actions[:higher]` / `[:lower]` | Move one position up / down | `-> { record.move_lower }` |
| `actions[:to_top]` / `[:to_bottom]` | Move to first / last position | `-> { record.move_to_top }` |
| `actions[:insert_at]` | Move to a dropped `position` (required for drag-and-drop) | `-> { record.insert_at position }` |
| `display_inline` | Buttons in the row vs. behind a popover (default `false`) | `display_inline: true` |
| `drag_and_drop` | Enable drag handles; needs `insert_at` too (default `false`) | `drag_and_drop: true` |
| `position` | Lambda returning a record's current position; used to compute drop target | `position: -> { record.position_in_list }` |
| `self.index_query` | (Resource attr, not in the hash) sort the Index by position | `self.index_query = -> { query.order(position: :asc) }` |

Inside every action lambda you can use: `record` (the model being moved), `resource`, `options` (the full `ordering` hash), `params`, plus `direction` (a String, directional actions) or `position` (an Integer, `insert_at` only).

## Gotchas

- **Paid add-on.** None of this works without the record-reordering add-on licensed and installed — flag it before writing config.
- **`visible_on` has no implicit default.** Omitting it hides the controls *everywhere*; it does not fall back to `:index`. Always set `:index`, `:association`, or `[:index, :association]` explicitly.
- **No controls without actions.** The reordering UI only renders when the `actions` hash defines at least one lambda.
- **Drag-and-drop needs two things.** Both `drag_and_drop: true` **and** `actions[:insert_at]` must be present — with either missing, drag handles never appear.
- **Ordering doesn't sort the Index.** Defining `ordering` only adds controls. Add `self.index_query = -> { query.order(position: :asc) }` (or a model `default_scope`) or the list won't reflect the saved order.
- **Custom position attribute → set `position:`.** Drag-and-drop reads `record.position` by default (the `acts_as_list` column). If yours is named otherwise, supply a `position:` lambda or drops land in the wrong spot.
- **`acts_as_list` needs every row to have a position.** Backfill existing records after adding the column, or moves behave unpredictably. Set `acts_as_list scope:` when the list is per-parent (e.g. slides within one carousel).
- **Association-scoped ordering → `visible_on: :association`.** When order only means something inside a parent record, show controls there, not on the global Index.
- **Authorization gates it silently.** With the authorization feature on, a `reorder?` policy returning false hides the controls with no error. Add `reorder?` to the policy (cross-link the **avo-authorization** skill).
- **No generator.** `self.ordering` is a hand-written resource attribute — there's no `bin/rails g` command for it.
- **Verify before writing.** Option names drift between versions — check the docs URLs above or the app's installed Avo source rather than trusting memory.

## Report

When done, tell the user:

- Which resource file you edited (full path) and the `self.ordering` config you added — `visible_on`, which actions, and whether drag-and-drop is on.
- What the model needs: `acts_as_list` (or equivalent) providing `move_higher` / `move_lower` / `move_to_top` / `move_to_bottom` / `insert_at`, a `position` column, and any pending migration or backfill of existing rows.
- Whether you added `self.index_query` to sort the Index by position (and why it's needed for the order to be visible).
- If drag-and-drop is enabled, confirm both `drag_and_drop: true` and `insert_at` are present, and note any custom `position:` lambda.
- Remind them it's a **paid add-on**, and if authorization is enabled, that a `reorder?` policy method is required for the controls to show.
