---
name: avo-filters
description: Add and configure filtering on an Avo resource's Index view — basic filters (developer-written Ruby filter classes), dynamic filters (user-built ad-hoc filtering via `filterable` fields and `dynamic_filter`), and scopes (one-click segment tabs and default views). Use when the user wants to filter, segment, or set a default view for the records on a resource index — e.g. "filter projects by status", "filter users by role", "filter by a date range", "let users build their own ad-hoc filters", "filter by an association", "only show active records by default", "hide soft-deleted by default", "add a tab for admin/active users", "segment orders into paid/unpaid tabs", "show a count next to each tab", or "hide the All tab". Covers the avo:filter and avo:scope generators, def filters and def scopes, ransackable_attributes, and default scopes.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Filter and segment an Avo resource index

Avo has three separate systems for narrowing down the records on a resource's `Index` view. This skill's leading job is **routing** to the right one, then implementing it with the correct generator and DSL. Getting the routing wrong means writing the wrong kind of code, so start with the routing table below every time.

**Docs** (fetch on demand with WebFetch — the `.md` variants are agent-friendly):

- Overview / decision: https://docs.avohq.io/4.0/filters.md
- Basic filters: https://docs.avohq.io/4.0/basic-filters.md · API: https://docs.avohq.io/4.0/basic-filters-api.md
- Dynamic filters: https://docs.avohq.io/4.0/dynamic-filters.md · API: https://docs.avohq.io/4.0/dynamic-filters-api.md
- Scopes: https://docs.avohq.io/4.0/scopes.md · API: https://docs.avohq.io/4.0/scopes-api.md
- Full docs map: https://docs.avohq.io/4.0/docs-map.md

Fetch the relevant page when you need an option you don't see here (custom conditions, `fetch_values_from`, `picker_options`, per-scope `fields`, humanized pills, …). This file covers the common cases end to end.

## When this applies

The user wants to change **which records appear** on a resource's index (or an association's `has_many` listing) — filter them, let end users filter them, segment them into tabs, or pick a default view. All three systems apply to the `Index` view only and encode their state in the URL, so a filtered/segmented view can be bookmarked and shared.

Avo files live under `app/avo/`. Before editing, locate the resource (`app/avo/resources/<name>.rb`) and its model (`app/models/<name>.rb`). Use Glob (`app/avo/resources/**/*.rb`) if you're unsure of the exact path.

## Choose the right tool

Read the request against this table **first**. The three systems are independent — a resource can use any combination — but each request usually maps to exactly one.

| What the user is asking for | Use | License |
| --- | --- | --- |
| A specific, developer-defined filter with exact query logic the developer controls — "filter by status", "published/unpublished", "featured only", "by author", "by a date range". One filter = one value or checkbox set. | **Basic filter** | Community |
| End users composing their **own** filters across many attributes — pick an attribute, a condition (`Contains`, `Is`, `>=`, `Is null`), and a value, stacking several at once. "let users filter however they want", "ad-hoc filtering", "filter by an association". | **Dynamic filters** | Paid add-on |
| One-click **segment tabs** above the table — "add a tab for admins", "segment orders into paid/unpaid tabs", "Active / Archived tabs", "show a count next to each tab". | **Scopes** | Paid add-on |
| A **default view** — "only show active records by default", "hide soft-deleted by default", "default to my team's records". | **Scope** marked `default: true` (optionally with `remove_scope_all`) | Paid add-on |

Quick disambiguation:

- **"Filter" is ambiguous.** If the developer decides the exact query and offers a fixed set of choices → basic filter. If the *end user* builds the query from a palette of attributes/conditions → dynamic filters.
- **Tabs vs. filters.** A tab bar the user clicks between (mutually-exclusive segments, one active at a time) → scopes. A panel where the user sets values and applies → basic or dynamic filters.
- **"By default" / "only show X" is almost always a default scope**, not a filter — filters start empty; scopes can be pre-applied.

If the user's own words don't settle it, ask one clarifying question rather than guessing (e.g. "Do you want a fixed 'Status' filter you control, or should users build their own filters?").

**License gate:** basic filters ship in Avo's **Community** edition. **Dynamic filters and scopes are paid add-ons.** If the routing lands on dynamic filters or scopes, mention the add-on requirement in your report so the user isn't surprised when the DSL is present but nothing renders on an unlicensed install.

---

## Basic filters

One Ruby class per filter under `app/avo/filters/`. You choose the input type, define its `options`, and write the exact Active Record query in `apply`. Then register it on each resource that should show it.

### Generate

```bash
bin/rails generate avo:filter published --type select
```

`--type` accepts `boolean` (default), `select`, `multiple_select`, `text`, and `date_time`. Each maps to a base class and a value shape in `apply`:

| Type | Base class | `apply` receives |
| --- | --- | --- |
| `boolean` | `Avo::Filters::BooleanFilter` | `Hash` of `"option_id" => true/false` |
| `select` | `Avo::Filters::SelectFilter` | `String` (selected option id) |
| `multiple_select` | `Avo::Filters::MultipleSelectFilter` | `Array` of `String`s |
| `text` | `Avo::Filters::TextFilter` | `String` |
| `date_time` | `Avo::Filters::DateTimeFilter` | `String` (or `"<start> to <end>"` in range mode) |

### Write the filter

A select filter — the everyday "filter by status" case:

```ruby
# app/avo/filters/published.rb
class Avo::Filters::Published < Avo::Filters::SelectFilter
  self.name = "Published status"

  # value is a String, e.g. "published"
  def apply(request, query, value)
    case value
    when "published" then query.where.not(published_at: nil)
    when "unpublished" then query.where(published_at: nil)
    else query
    end
  end

  def options
    {published: "Published", unpublished: "Unpublished"}
  end
end
```

A boolean filter receives a hash keyed by option id — **read the keys as strings** (see Gotchas):

```ruby
# app/avo/filters/featured.rb
class Avo::Filters::Featured < Avo::Filters::BooleanFilter
  self.name = "Featured"

  # values = { "is_featured" => true, "is_unfeatured" => false }
  def apply(request, query, values)
    return query if values["is_featured"] && values["is_unfeatured"]

    if values["is_featured"]
      query.where(featured: true)
    elsif values["is_unfeatured"]
      query.where(featured: false)
    else
      query
    end
  end

  def options
    {is_featured: "Featured", is_unfeatured: "Unfeatured"}
  end
end
```

A date-time filter — for "filter by a date range". Default `self.mode` is `:range`:

```ruby
# app/avo/filters/created_at.rb
class Avo::Filters::CreatedAt < Avo::Filters::DateTimeFilter
  self.name = "Created at"
  self.type = :date    # :date_time (default), :date, or :time
  self.mode = :range   # :range (default) or :single

  def apply(request, query, value)
    from, to = value.split(" to ")           # range arrives as "2024-08-13 to 2024-08-16"
    query.where(created_at: Date.parse(from)..Date.parse(to))
  end
end
```

Text filters need no `options` (`value` is the raw string). Multiple-select filters get an `Array` of strings and `options` like select.

### Register on the resource

Filters only render once registered inside the resource's `filters` method:

```ruby
# app/avo/resources/post.rb
class Avo::Resources::Post < Avo::BaseResource
  def filters
    filter Avo::Filters::Published
    filter Avo::Filters::Featured
  end
end
```

The same filter class can be registered on many resources. To vary behavior per resource, pass `arguments: {...}` — available in `apply`, `options`, and the `self.name`/`self.visible` blocks.

### Common extras (in the guide)

- **Default state:** define `default` returning the same shape `apply` expects (`:published`, `{is_featured: true}`, `["a", "b"]`).
- **Dynamic options:** `options` is plain Ruby — query the DB or an API.
- **Conditional visibility:** `self.visible = -> { current_user.admin? }`.
- **Filters that depend on each other:** read `applied_filters` in `options`, or override `react` to change a filter's own value when another changes.
- **Link to a pre-filtered view:** `Avo::Filters::BaseFilter.encode_filters({"Avo::Filters::Name" => "Apple"})` → pass as `encoded_filters:`.

---

## Dynamic filters

Paid add-on. You declare which fields are `filterable`; Avo renders a filters bar where **the user** picks an attribute, a condition, and a value, stacking as many as they want. Queries run through [Ransack](https://github.com/activerecord-hackery/ransack).

### Mark fields filterable

```ruby
# app/avo/resources/project.rb
class Avo::Resources::Project < Avo::BaseResource
  def fields
    field :name, as: :text, filterable: true
    field :status, as: :select, filterable: true
    field :country, as: :country, filterable: true
  end
end
```

Each filterable field infers a filter type from its field type (boolean→boolean, badge/select/country/status→select, date→date, number/id→number, tags→tags, everything else→text). Override with `type:`.

### Authorize the attributes for Ransack — do not skip this

Every filterable attribute **must** appear in the model's `ransackable_attributes`, as **strings**:

```ruby
# app/models/project.rb
class Project < ApplicationRecord
  def self.ransackable_attributes(auth_object = nil)
    ["name", "status", "country"]   # strings, NOT symbols
  end
end
```

Whenever you add a `filterable` field or a `dynamic_filter`, update this list (or return `authorizable_ransackable_attributes` to allow all). Missing/symbol entries = the filter silently does nothing. This is the #1 dynamic-filters footgun.

### Customize a filter

Turn `filterable: true` into a hash, or declare a standalone `dynamic_filter` in `def filters` (no field required). The two are equivalent — every option works in both:

```ruby
# Field option
field :first_name, as: :text, filterable: {label: "Name", icon: "avo/font"}

# Standalone, inside def filters
def filters
  dynamic_filter :first_name, label: "Name", icon: "avo/font"
end
```

**Filter by an association** — prefix the attribute(s) with the association name (a Ransack feature; the association must be ransackable), and set `query_attributes:`:

```ruby
field :user, as: :belongs_to, filterable: {
  label: "User (email & first name)",
  icon: "heroicons/solid/users",
  query_attributes: [:user_email, :user_first_name]
}
```

**Filter across multiple columns** (matches any of them, `OR`):

```ruby
dynamic_filter :name, type: :text, query_attributes: [:first_name, :last_name]
```

**Custom id that isn't a real column** — must set both `type:` and `query_attributes:` (or a `query:`), or Avo raises asking for a type:

```ruby
dynamic_filter :custom_population, type: :number, query_attributes: :population
```

Other options (see the API doc): `conditions:` (restrict/rename; `{}` hides the dropdown and uses the first default condition), `query:` (take over the SQL via a proc with `query`/`filter_param`), `options:` (select choices), `suggestions:` / `fetch_values_from:` (typeahead), `apply_on_select:` + `render_apply_button: false` (instant apply), `humanized_value:` / `humanized_condition:` (nicer pills).

### Configure the bar globally (optional)

```ruby
# config/initializers/avo.rb — after Avo.configure
if defined?(Avo::DynamicFilters)
  Avo::DynamicFilters.configure do |config|
    config.always_expanded = false      # collapse behind a toggle button
    config.button_label = "Advanced filters"
  end
end
```

---

## Scopes

Paid add-on. A scope is a one-click **segment tab** rendered in a bar above the records — "Active", "Admins", "Archived". Use scopes for mutually-exclusive segments and for default views.

### Generate

```bash
bin/rails generate avo:scope admins
```

Creates a class in `app/avo/scopes/` inheriting `Avo::Scopes::BaseScope`.

### Write the scope

`self.scope` accepts a Symbol (names a scope on the model) or a Proc that receives `query`:

```ruby
# app/avo/scopes/admins.rb
class Avo::Scopes::Admins < Avo::Scopes::BaseScope
  self.name = "Admins"                       # tab label
  self.description = "Admins only"            # tooltip
  self.scope = :admins                        # a model scope…
  self.visible = -> { current_user.admin? }   # show/hide/authorize the tab
end

# app/models/user.rb
class User < ApplicationRecord
  scope :admins, -> { where(role: :admin) }
end
```

```ruby
# …or a proc, no model scope needed
class Avo::Scopes::Active < Avo::Scopes::BaseScope
  self.name = "Active"
  self.scope = -> { query.where(archived_at: nil) }
end
```

### Register on the resource

Scopes are opt-in per resource, inside `def scopes`:

```ruby
# app/avo/resources/user.rb
class Avo::Resources::User < Avo::BaseResource
  def scopes
    scope Avo::Scopes::Active
    scope Avo::Scopes::Admins
  end
end
```

### Default view — "only show active by default"

Avo injects an **`All`** tab and makes it the default. To ship a different default:

```ruby
def scopes
  scope Avo::Scopes::Active, default: true   # applied on page load
  scope Avo::Scopes::Admins
end
```

`default:` also takes a proc for a per-user default: `default: -> { current_user.admin? }`.

To **replace** the All tab entirely (e.g. never show an unscoped list, or hide soft-deleted by default), call `remove_scope_all` and mark another scope `default: true`:

```ruby
def scopes
  remove_scope_all
  scope Avo::Scopes::Active, default: true    # this becomes the "everything you're allowed to see" tab
  scope Avo::Scopes::Archived
end
```

### Show a count next to each tab

Use the `counter` option — **not** `name`:

```ruby
# app/avo/scopes/active.rb
class Avo::Scopes::Active < Avo::Scopes::BaseScope
  self.scope = -> { query.where(archived_at: nil) }
  self.counter = :lazy   # :lazy (load after paint), :hover (on hover), true/:eager (inline)
end
```

Prefer `:lazy` or `:hover` on large tables so counting doesn't slow the page. For a custom/formatted badge, pass a Hash with `loading:`, `count:`, `visible:`, `format:` keys (see the API doc). The count ignores active search/filters — it always reflects the whole scope.

### Per-scope columns (optional)

A scope can change which **columns** show on the index while active: define a `fields` method (full DSL), or set `field_whitelist` / `field_blacklist`. **These are display-only, not authorization** — see Gotchas.

---

## Gotchas

- **Dynamic filters — ransackable strings.** Every `filterable` attribute and every `dynamic_filter` `query_attributes` entry must be in the model's `ransackable_attributes` **as strings, not symbols**, or filtering silently does nothing. The single most common failure. Update the list whenever you add a filterable field. Association filtering also needs the association in `ransackable_associations`.
- **Basic filter values are always strings.** State is serialized through the URL, so `apply` receives strings and hashes with **stringified keys**. Read `values["is_featured"]`, never `values[:is_featured]`, even if you declared `options` with symbols.
- **`dynamic_filter` with a non-column id must declare its type.** An id that doesn't match a field/column can't infer a type and raises — set `type:` and point at real columns with `query_attributes:` (or provide a `query:`).
- **Two "Filters" buttons.** If a resource has *both* basic and dynamic filters and you set dynamic filters' `always_expanded = false`, two `Filters` buttons appear on the index. The default (`always_expanded = true`) renders the dynamic bar inline and avoids the duplicate.
- **Scope `field_whitelist` / `field_blacklist` are display-only.** They change which columns render on the index; the hidden fields' data is still loaded and stays visible on show/edit and through the API. For real access control use a [policy](https://docs.avohq.io/4.0/authorization.md) or a field's `visible` option.
- **The injected `All` scope.** Avo always adds an `All` tab and defaults to it. To change the default, mark another scope `default: true`; to remove All entirely, call `remove_scope_all` **and** mark a replacement `default: true` (otherwise the page loads with no scope applied).
- **Scope counts belong in `counter`, not `name`.** Computing counts inside `name` (via `scoped_query`) runs the scope on every page load. Use the `counter` option with `:lazy`/`:hover`.
- **Date-time basic filter range format.** In the default `:range` mode the value arrives as the single string `"2024-08-13 to 2024-08-16"` — split it with `value.split(" to ")`. Set `self.mode = :single` for one value.
- **License.** Dynamic filters and scopes are paid add-ons; basic filters are Community. The DSL will be accepted but nothing renders on an unlicensed install — surface this in your report.

## Report

When done, tell the user:

- **Which system** you used and **why** it fit the request (one line of routing rationale).
- **Files created/edited** with absolute paths — the filter/scope class(es), the resource (`def filters` / `def scopes`), and the model (`ransackable_attributes` and any model scope).
- **License note** if you used dynamic filters or scopes (paid add-on), so an unlicensed install's "nothing renders" is expected, not a bug.
- **Follow-ups the user must do themselves:** run the generator if you only wrote the class, add attributes to `ransackable_attributes`, define referenced model scopes, or restart the server to pick up new files.
