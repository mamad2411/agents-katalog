---
name: avo-kanban
description: Install and configure Avo Kanban — database-backed, multi-resource drag-and-drop boards in the Avo admin where moving a card between columns writes a value onto a property of the underlying record. Use when the user wants a Trello / GitHub-Projects-style board, to organize records into columns by status or stage, a pipeline or workflow board (backlog → in progress → done), a sales pipeline / stage board, to drag records between stages, or to track tickets / tasks / issues on a board — and when they want to add boards, columns, or items; make a resource addable to a board; tailor the board picker search; add virtual status properties; customize the kanban card; or set up kanban authorization. Paid add-on, Beta.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo Kanban Boards

Avo Kanban adds **database-backed, multi-resource kanban boards** to an Avo admin. A `Board` `has_many` `Column`s, and each `Column` `has_many` `Item`s; an `Item` is a polymorphic pointer to any record in the app (an `Issue`, `Project`, `Task`, `User`, …), so one board can mix several resources — think GitHub Projects. Boards, columns, and items are all real rows you create in-app on the fly, not code.

The core mechanic: **a board owns one `property`, each column owns one `value`, and dropping a card into a column writes that column's `value` onto the record's `property` and saves the record.** A board with columns `No status` (value `""`), `Backlog` (`backlog`), `In progress` (`in_progress`), `Done` (`done`) and `property = status` becomes a status pipeline — move a card to *In progress* and the record's `status` becomes `in_progress`.

This is a **paid add-on** and currently **Beta / work-in-progress** — behavior and APIs can shift. Verify option names against the docs or the installed gem source before writing them.

## Docs

Fetch on demand rather than guessing; the `.md` suffix returns raw markdown:

- Docs map (discover pages): https://docs.avohq.io/4.0/docs-map.md
- Kanban boards guide: https://docs.avohq.io/4.0/kanban-boards.md
- `board` menu item (add a board to the sidebar): https://docs.avohq.io/4.0/menu-editor-api.md
- Authorization (Pundit setup this builds on): https://docs.avohq.io/4.0/authorization.md

Related skills: **avo-navigation-search** (the `board` menu item and menu editor), **avo-authorization** (Pundit policies), **avo-custom-ui** (ejecting/overriding the card component).

## Install

1. Add the gem (it's served from Avo's private package registry, not RubyGems):

   ```ruby
   # Gemfile
   gem "avo-kanban", source: "https://packager.dev/avo-hq/"
   ```

2. `bundle install`. This auto-pulls two runtime dependencies: [`acts_as_list`](https://github.com/brendon/acts_as_list) (column/item ordering) and [`hotwire_combobox`](https://github.com/josefarias/hotwire_combobox) (the card picker).

3. Generate the resources, controllers, card partial, and migration:

   ```bash
   bin/rails generate avo:kanban install
   ```

   This writes `Avo::Resources::Board` / `Column` / `Item` (in `app/avo/resources/`), their controllers (in `app/controllers/avo/`), the item partial `app/views/avo/kanban/items/_item.html.erb`, and a `create_avo_kanban` migration (tables `avo_kanban_boards`, `avo_kanban_columns`, `avo_kanban_items`). The `install` argument is required — `bin/rails generate avo:kanban` with no argument does nothing.

4. `bin/rails db:migrate`.

Only `Board` shows in the sidebar after install; `Column` and `Item` are generated with `self.visible_on_sidebar = false` and are managed through the board.

## When this applies

**Explicit (Avo/kanban named):** "install avo-kanban", "add a kanban board", "configure the Board resource", "let issues be added to a board", "customize the kanban card", "set up kanban authorization", "extend the kanban models".

**Implicit (product-shaped, Avo not mentioned):** "I want a drag-and-drop board for tasks / issues", "organize records into columns by status", "a Trello-style / GitHub-Projects-style board in the admin", "move a card to change its status", "a pipeline board — backlog → in progress → done", "a sales pipeline / stage board", "drag records between stages", "track tickets on a board".

## Workflow

### 1. Create a board and put it in the menu

Boards are created **in-app**, not in code: open the **Boards** resource and click **Create board**. The board's `settings` (a JSON column) hold everything below and are edited on the board's own form.

Once saved, surface it in the sidebar with a `board` menu item (see avo-navigation-search):

```ruby
# config/initializers/avo.rb  (inside config.main_menu)
board :board_slug_or_id
```

### 2. Configure the board (its settings form)

The generated `Avo::Resources::Board` exposes these, all stored in `settings`:

- **`property`** — the record attribute each drop writes to. **Required**; the `Avo::Kanban::Board` model has `validates_presence_of :property`, so a board **cannot be saved without it**.
- **`allowed_resources`** — which resources' records may be added to this board (a tags field; blank and duplicate entries are stripped on save).
- **`full_width_container`** — render full-width vs. the standard large container. Default `true`.
- **`exclude_duplicates`** — hide records already on the board from the picker so the same record can't be pinned twice. Default `true`.
- **`name`** / **`description`** — label and free text.

### 3. Create columns

Columns are created from the board / the Column association view. Each column has a **`name`**, a **`value`**, and a **`position`** (drag to reorder — `acts_as_list`). If you leave `value` blank on create it defaults to `name.parameterize` with dashes turned into underscores (e.g. *In progress* → `in_progress`). Give the "unstatused" column an **empty-string value** so a card dropped there clears the property. The `value` is exactly what gets written to the record's `property` on every drop.

### 4. Make a resource addable to the board

A resource can be pinned to a board **only if it has BOTH**:

- **`self.search[:query]`** — the picker searches each allowed resource through this block. A resource without a `search` block is silently skipped by the picker (the controller bails on a blank search query).
- **`self.title`** — used as the card label and as the label in the picker results.

```ruby
# app/avo/resources/issue.rb
class Avo::Resources::Issue < Avo::BaseResource
  self.title = :title

  self.search = {
    query: -> {
      query.ransack(number_eq: params[:q], title_cont: params[:q], m: "or").result(distinct: false)
    }
  }
end
```

### 5. Tailor the board picker search (important gotcha)

The board's picker is **special**: unlike the index, global, and association search surfaces, it does **not** inject a `search_type` or a `q` local into your `query:` block. Read the user's term from **`params[:q]`**, and detect that the call came from a board with **`params[:for_kanban_board]`** (the picker sets it):

```ruby
class Avo::Resources::Project < Avo::BaseResource
  self.title = :name

  self.search = {
    query: -> {
      if params[:for_kanban_board]
        query.where(active: true).ransack(name_cont: params[:q]).result
      else
        query.ransack(name_cont: params[:q]).result
      end
    }
  }
end
```

### 6. Understand the drop → save flow

Adding a card creates an `Avo::Kanban::Item` (tracking board, column, position, and the polymorphic `record`) and immediately writes the target column's `value` onto the record's `property`, then saves the record. Moving a card between columns rewrites the property to the new column's `value`. Dropping into the empty-string column sets the property to `""`.

**Two-way sync (verified in the gem, not yet in the guide):** if the record's model declares the inverse association and an after-update hook, changing the property *elsewhere* (a normal edit, a background job) moves the card to the matching column automatically:

```ruby
class Issue < ApplicationRecord
  has_many :kanban_items, class_name: "Avo::Kanban::Item", as: :record
  after_update { Avo::Kanban::Item.trigger_after_update(self) }
end
```

### 7. Records whose model lacks the column (virtual property)

Different models can share a board even if they store "status" differently. When a model has no real column for the board's `property`, define a **virtual getter + setter**. The getter derives the status from real columns; the setter maps a column `value` back onto them. **The setter must only assign attributes — do NOT call `save!`; Avo assigns the property and then saves the record.**

```ruby
class Post < ApplicationRecord
  def status
    published_at.present? ? "published" : (published_status == "draft" ? "draft" : "private")
  end

  def status=(value)
    case value
    when "published" then self.published_at = Time.current; self.published_status = "published"
    when "draft"     then self.published_at = nil;          self.published_status = "draft"
    else                  self.published_at = nil;          self.published_status = nil
    end
  end
end
```

### 8. Customize the card

The documented route is to **eject** the card component and edit the ERB:

```bash
bin/rails generate avo:eject --component Avo::Kanban::Items::ItemComponent
```

```erb
<%# app/components/avo/kanban/items/item_component.html.erb %>
<%= item.record.name %>
```

`item` is the `Avo::Kanban::Item`; `item.record` is the underlying record. To restyle **only one resource's cards** instead of all of them, the gem also supports a per-resource override via `self.components` on that resource (source-verified; point `"Avo::Kanban::Items::ItemComponent"` at your own component). See avo-custom-ui.

### 9. Authorization (Pundit)

Assumes Pundit authorization is already set up (avo-authorization). The board is backed by `Avo::Kanban::Board`, so its policy is **namespaced to match**: `Avo::Kanban::BoardPolicy` at `app/policies/avo/kanban/board_policy.rb`. Each method maps to an `authorize_action(:action)` call in the board's controllers/components; methods you don't define fall back to `ApplicationPolicy`.

```ruby
# app/policies/avo/kanban/board_policy.rb
class Avo::Kanban::BoardPolicy < ApplicationPolicy
  def show? = true           # can the board page be visited at all
  def edit? = true           # "Edit board" button — also governs editing the board in the resource view
  def add_column? = true     # "Add column" button + the add_column action
  def add_item? = true       # every "Add a card" button (board header, column header, column footer)
  def manage_column? = true  # the column three-dot menu (remove column, clear items, settings)

  class Scope < ApplicationPolicy::Scope
    def resolve = scope.all
  end
end
```

### 10. Extend the kanban models for business logic

Add associations, validations, or callbacks to the gem's models by reopening them inside `Rails.configuration.to_prepare` (so it survives dev reloads) with `class_eval`:

```ruby
# config/initializers/avo.rb
Rails.configuration.to_prepare do
  Avo::Kanban::Board.class_eval do
    belongs_to :team, optional: true
    validates :name, presence: true, uniqueness: { scope: :team_id }
  end

  Avo::Kanban::Item.class_eval do
    belongs_to :assignee, class_name: "User", optional: true
    # ...callbacks, tracking, etc.
  end
end
```

## Gotchas

- **Beta / WIP.** The feature and its docs are work-in-progress; expect changes. Verify option names against the installed gem before writing them.
- **`property` is required.** No `property` → the board fails validation and can't be saved. It's the single attribute every column writes to.
- **A resource needs BOTH `self.search[:query]` AND `self.title` to be addable.** Missing `search` → the resource is skipped by the picker (no error, it just never appears). Missing `title` → no usable card / picker label.
- **The board picker search is not the index search.** No `search_type` and no `q` local are injected into the block. Read `params[:q]`; branch on `params[:for_kanban_board]`. Reusing an index-search block that references a `q` local will break here.
- **A column `value` overwrites the record `property` on every drop** — including an empty string for a "No status" column. Column values default to `name.parameterize` (dashes → underscores) if left blank.
- **Virtual-property setters set attributes only — never `save!`.** Avo assigns the property and saves the record; calling `save!` in the setter double-saves.
- **The board policy is namespaced.** It's `Avo::Kanban::BoardPolicy` in `app/policies/avo/kanban/board_policy.rb`, not `BoardPolicy`. Getting the namespace wrong means your methods are never called.
- **Extend models via `Rails.configuration.to_prepare` + `class_eval`**, not a bare reopen in the initializer, or your changes get dropped on reload.
- **Only `Board` is in the sidebar.** `Column` and `Item` are generated hidden; a board reaches the menu through a `board` menu item, not the auto-generated resource list.

## Report

When done, tell the user:

- Which files the generator created/edited (full paths) and the commands run (`bundle install`, `bin/rails generate avo:kanban install`, `bin/rails db:migrate`).
- That it's a paid, Beta add-on pulling `acts_as_list` + `hotwire_combobox`.
- The board's `property` and each column's `name`/`value`, and which resources you made addable (and that each got `self.search[:query]` + `self.title`).
- Any board-picker search tailoring (`params[:for_kanban_board]`) or virtual properties you added, and for which models.
- Whether you set up the `Avo::Kanban::BoardPolicy`, ejected/overrode the card component, or extended the kanban models — and any remaining manual step (create the board in-app, add columns, add the `board` menu item, run pending migrations).
