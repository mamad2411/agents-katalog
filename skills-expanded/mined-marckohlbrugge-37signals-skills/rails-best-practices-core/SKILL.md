---
name: rails-best-practices-core
description: Apply core Ruby on Rails best practices for architecture, naming, safety, and maintainability. Use for most Rails coding, refactoring, and code review tasks so baseline standards stay consistent.
---

# Rails Best Practices Core

Use this as the default baseline for Rails work. Distilled from 37signals codebases (Campfire, Fizzy) and DHH's review patterns.

## Core Defaults

- Prefer clear, explicit code over clever abstractions. Abstractions must earn their keep; if you can't point to 3+ variations that need it, inline it.
- Keep controllers thin and put domain behavior in models.
- Prefer Rails conventions and built-ins before adding gems.
- Model state and behavior with domain concepts, not ad-hoc flags.
- Scope tenant/user data through ownership boundaries.
- Favor database constraints for hard invariants; only validate in AR when you need user-facing error messages.
- Keep interfaces small; don't add public methods that aren't used anywhere.
- Prefer write-time computation over expensive read-time composition (counter caches, delegated types, precomputed roll-ups, `dependent: :delete_all` when no callbacks needed).
- Use `params.expect(...)` for strong params in modern Rails.
- Let it crash: bang methods (`create!`), handle exceptions at boundaries. Only use `!` when a non-bang counterpart exists.
- Fix root causes, not symptoms (e.g. `enqueue_after_transaction_commit` over retry logic for races).
- Ship tests in the same PR as behavior changes.

## Modeling Patterns

- **State as records, not booleans.** Instead of `closed: boolean`, create a `Closure` record with `creator` and timestamps. You get who/when for free, and scoping is trivial:

```ruby
has_one :closure, dependent: :destroy
scope :closed, -> { joins(:closure) }
scope :open, -> { where.missing(:closure) }
```

- **Slice large models into concerns** named for capability (`Closeable`, `Watchable`, `Assignable`), each self-contained (associations + scopes + methods), ~50-150 lines, cohesive. Prefer nested modules under the model's namespace (`Card::Closeable` in `app/models/card/closeable.rb`) for domain slices; reserve `app/models/concerns/` for genuinely cross-model behavior. Never extract concerns containing only private methods.
- **POROs live in `app/models/`**, not `app/services/`: presentation objects (`Event::Description`), complex operations (`SystemCommenter`), view-context bundles (`User::Filtering`). They're model-adjacent, not controller-adjacent.
- **Default values via lambdas:** `belongs_to :creator, class_name: "User", default: -> { Current.user }`; `belongs_to :account, default: -> { board.account }`.
- **Current attributes for request context** (`Current.user`, `Current.account`), with cascading setters (assigning `session` resolves `identity`, which resolves `user` for the account).
- **Callbacks for setup/cleanup, not business logic.** Keep callback counts low.
- **Rails shortcuts to reach for:** `normalizes` (data cleanup before validation), `store_accessor` (JSON columns), `delegated_type` (heterogeneous collections), `generates_token_for` (expiring signed tokens), string enums via `enum :status, %w[drafted published].index_by(&:itself)`, `after_save_commit`, `touch: true` chains for cache invalidation, `delegate`.
- **Association extensions for bulk domain operations:** define `grant_to`/`revise` on the `has_many` proxy; use `insert_all` for bulk creates and `dependent: :delete_all` on join tables with no callbacks.
- **Human-friendly URLs:** override `to_param` with a per-tenant `number` rather than exposing raw IDs/UUIDs.

## Naming

- Spend time on names — naming is design. `Closure` beats `CardClose`; `Mention` beats `UserReference`.
- Positive names: `active` not `not_deleted`, `visible` not `not_hidden`.
- Semantic associations named for role: `belongs_to :creator, class_name: "User"` not `belongs_to :user`.
- Domain-driven over technical: `quota.depleted?` not `quota.over_limit?`.
- Business-focused scopes: `:active`, `:unassigned`, `:golden` — not SQL-ish `:without_pop`.
- Consistent domain language: don't mix `source`/`resource`/`container` for one concept.

## REST & Routing

- Everything is CRUD: turn verbs into nouns. Close → `resource :closure` (POST closes, DELETE reopens); publish → `resource :publication`. No custom member actions.
- Singular `resource` for one-per-parent state; `scope module:` to group nested controllers (`Cards::ClosuresController`); shallow nesting for deep hierarchies.
- Resource-scoping controller concerns (`CardScoped` sets `@card` via `Current.user.accessible_cards.find_by!(...)`) shared across nested controllers, including shared Turbo render helpers.
- `resolve "Comment"` for polymorphic URL generation to the parent with an anchor.
- Same controllers serve HTML/Turbo/JSON via `respond_to` — no separate API namespace.

## Authorization

- No Pundit/CanCanCan: simple predicate methods on models (`card.editable_by?(user)`, `user.can_administer_board?(board)`).
- Controllers check (`head :forbidden unless ...`), models define what the permission means.
- Declarative controller macros for auth posture: `allow_unauthenticated_access`, `ensure_can_administer`.

## Dependencies

Before adding a gem ask: can vanilla Rails do this? Is 50-150 lines in-repo simpler than a dependency? Commonly skipped: Devise, Pundit, ViewComponent, RSpec, FactoryBot, Redis (Solid Queue/Cache/Cable use the DB), service objects, form objects, decorators, GraphQL, SPA frameworks, Tailwind.

## Review Priorities

1. Correctness and data safety.
2. Multi-tenant/security boundaries.
3. Maintainability and readability.
4. Performance hot spots.
5. Style and polish.

## Always Flag

- Unscoped record lookups in tenant-aware flows (`Comment.find(params[:id])`).
- New dependencies without strong justification.
- In-memory filtering/sorting that belongs in SQL (and `.map(&:name)` where `.pluck(:name)` works).
- Service objects replacing straightforward model methods.
- Non-RESTful custom actions when resource modeling is clearer.
- Boolean state columns where a record would capture who/when.
- Pages with forms using HTTP caching (`fresh_when`/etag) — stale CSRF tokens cause 422s.
- String status checks (`status == "x"`) when predicate-style APIs are available (StringInquirer / string enums).
- `validates :x, uniqueness: true` without a backing unique index.
- Helpers depending on implicit instance variables instead of explicit arguments.
- Unescaped interpolation into `html_safe` strings — escape first: `"<b>#{h(input)}</b>".html_safe`.
- Metaprogramming for 2-3 cases — just write the methods.
- Private-only concerns — inline them.

## Review Output

- Start with highest-severity findings.
- For each finding: issue, impact, concrete fix with file:line references.
- Be direct and practical; "This is over-engineered" is a complete sentence.
- End with either `Ship it` or a short prioritized fix list.
