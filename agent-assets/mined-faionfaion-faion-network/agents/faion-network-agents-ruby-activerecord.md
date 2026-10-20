# Ruby ActiveRecord Patterns

## Summary

**One-sentence:** Use ActiveRecord idiomatically: scopes for reusable queries, includes/preload/eager_load for N+1 elimination, strong attributes (counter_cache, enum, monetize), explicit transactions, and validation in models.

**One-paragraph:** ActiveRecord is Rails' ORM — productive but easy to misuse. The discipline: scopes for reusable WHERE clauses, includes/preload/eager_load for N+1 elimination (preload uses 2 queries, eager_load uses LEFT JOIN), enum for status columns, validates_* for invariants, transaction blocks for multi-write atomicity, and counter_cache for cheap counts. Avoid update_all / delete_all in business logic (bypasses callbacks); avoid Time.now (use Time.current for app timezone).

**Ефективно для:**

- Rails 7/8 проєкти з реляційною БД (PostgreSQL/MySQL).
- Refactor N+1 queries (визначено через bullet gem).
- Greenfield models — встановити scope/enum/callbacks одразу.
- Migration від raw SQL обходів до AR idiom (зокрема, where + scope).

## Applies If (ALL must hold)

- Rails 7+ project with ActiveRecord (not Sequel / ROM).
- Models have associations + validations.
- Performance matters (organic traffic / paid features).
- Database is PostgreSQL or MySQL.

## Skip If (ANY kills it)

- Read-only data warehouse — use raw SQL or dbt.
- Project standardizes on Sequel or ROM — different ORM, different rules.
- Sub-table-count: <3 tables in entire app.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Model + migration | Ruby class + db/migrate | domain |
| bullet gem output | N+1 detection log | dev |
| DB schema | db/schema.rb | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Rails framework basics assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: scopes-for-reused-where, includes-no-n-plus-one, transaction-block-multi-write, enum-for-status, no-time-now | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-scopes` | sonnet | Templated migration. |
| `design-enum-values` | opus | Domain decision on status values. |
| `lint-time-now` | haiku | Mechanical grep + rubocop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/order.rb` | ActiveRecord model with enum, scopes, includes-friendly associations |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-activerecord.py` | Validate the AR model artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/order.rb`

```ruby
class Order < ApplicationRecord
  belongs_to :customer
  has_many :items, class_name: "OrderItem", dependent: :destroy

  enum status: { pending: 0, paid: 1, shipped: 2, cancelled: 3 }, _prefix: true

  validates :status, presence: true
  validates :total_cents, numericality: { greater_than_or_equal_to: 0 }

  scope :recent, -> { where("created_at >= ?", 30.days.ago) }
  scope :for_user, ->(user) { where(customer_id: user.customer_id) }
  scope :priced, -> { where("total_cents > 0") }

  def total
    Money.new(total_cents, currency)
  end

  def cancel!
    transaction do
      update!(status: :cancelled, cancelled_at: Time.current)
      items.each(&:release_inventory!)
    end
  end
end
```
