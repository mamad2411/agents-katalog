---
name: backend-stack-rails
description: "A Ruby on Rails backend: conventions, strong parameters, ActiveRecord validations, associations and includes against N+1, transactions and locking, safe migrations with strong_migrations, jobs with Solid Queue or Sidekiq, authentication with the Rails 8 generator or Devise, authorisation with Pundit, serialisation, errors with rescue_from, credentials, caching, and tests with Minitest or RSpec. Read when the project uses Rails."
---

# Ruby on Rails

The generated Rails app puts the rules in fat controllers or in callbacks
that fire on every save, permits whatever arrives, checks uniqueness only in
Ruby, loads `order.customer` inside a loop, adds an index that locks a busy
table at deploy, sends email inside the transaction, and answers
`render json: @order` with every column. The backend rules are in the
`backend` skill; these are Rails's own. Keep the project's versions and
gems; the notes assume Rails 7.2 or 8.

## 1. Conventions

- The Ruby and Rails versions pinned (`.ruby-version`, `Gemfile.lock`). A
  new app: current Rails 8 with `--database=postgresql`, and `--api` for an
  API alone.
- Follow the conventions rather than fight them: RESTful controllers,
  Zeitwerk naming (`bin/rails zeitwerk:check`), routes as `resources` inside
  `namespace :api` and `namespace :v1`, with `only:` listing the actions and
  extra actions as member routes (`post :cancel, on: :member`).
- Rules live in models (validations, scopes, small methods) and in plain
  Ruby objects for workflows that span models (`Order::Placement`, or
  `app/services/` if the project has it). Callbacks only for the record's
  own state (normalising a field), never for sending mail, charging cards
  or changing other records.

## 2. Controllers and strong parameters

```ruby
class Api::V1::OrdersController < Api::BaseController
  def show
    render json: OrderResource.new(Current.user.orders.find(params[:id])).serialize
  end

  def create
    order = Order::Placement.new(customer: Current.user, params: order_params).call
    render json: OrderResource.new(order).serialize, status: :created,
           location: api_v1_order_url(order)
  end

  private

  def order_params
    params.expect(order: [:note, lines: [[:product_id, :quantity]]])
  end
end
```

- `params.expect` (Rails 8) returns only the listed keys and answers `400`
  when the shape is wrong; before 8, `params.require(:order).permit(...)`.
  Never `permit!`, never `params` straight into `create`: `role`, `price`
  and `user_id` are set in code.
- Every lookup goes through the caller (`Current.user.orders.find(id)`), so
  another user's id raises `RecordNotFound`, a `404`.
- API controllers inherit from `ActionController::API`; full-stack ones
  keep CSRF protection (on by default in `ActionController::Base`).

## 3. Models: validations and constraints both

- Each validation that protects data has a database constraint behind it:
  `uniqueness` plus a unique index (the validation alone races), `presence`
  plus `null: false`, `inclusion` plus a check constraint, `belongs_to`
  (required by default) plus a foreign key.
- Duplicates caught where they happen: `rescue ActiveRecord::RecordNotUnique`
  becomes a `409` or a field error; `create_or_find_by` relies on the
  unique index.
- `normalizes :email, with: ->(email) { email.strip.downcase }` (7.1+), so
  lookups and the unique index agree.
- Enums with explicit values
  (`enum :status, { pending: 0, paid: 1, cancelled: 2 }, validate: true`),
  or string values with a check constraint so the data reads well in SQL.
- Money as integer cents plus a currency (or the money-rails gem); times
  stored in UTC, `config.time_zone` only for display.

## 4. Associations and N+1

- `preload` (separate queries, the usual choice), `eager_load` (one
  `LEFT JOIN`, when filtering on the association) or `includes` (Rails
  picks); counts with `counter_cache` or one grouped query, never `.count`
  per row.
- N+1 fails in development and tests: `strict_loading` (per relation, per
  model with `self.strict_loading_by_default = true`, or app-wide with
  `config.active_record.strict_loading_by_default`), set to raise, and the
  Bullet gem for what slips past.
- Work over many rows with `find_each` (batches of 1,000) or `in_batches`,
  never `Model.all.each`; `pluck` and `select` for the columns a report
  needs; `exists?` to test for presence.

## 5. Transactions and locking

```ruby
Order.transaction do
  order = Order.create!(customer: user, status: :pending)
  lines.each do |line|
    reserved = Product.where(id: line[:product_id])
                      .where("stock >= ?", line[:quantity])
                      .update_all(["stock = stock - ?", line[:quantity]])
    raise OutOfStock, line[:product_id] if reserved.zero?
    order.items.create!(product_id: line[:product_id], quantity: line[:quantity])
  end
  order
end
```

- Bang methods inside transactions (`create!`, `update!`, `save!`): a plain
  `save` that returns `false` lets the rest commit.
- Counters and stock with conditional `update_all` or `update_counters`;
  `with_lock` (a transaction and `SELECT ... FOR UPDATE`) when you must read
  then decide; optimistic locking with a `lock_version` column
  (`ActiveRecord::StaleObjectError` answers `409`).
- Side effects after commit: `after_commit`, or enqueue after the
  `transaction` block. Rails 7.2 added `enqueue_after_transaction_commit`
  and its default has shifted since: check the project's setting instead of
  assuming. No HTTP calls or mail inside a transaction.

## 6. Migrations with strong_migrations

The strong_migrations gem stops unsafe migrations in development and prints
the safe recipe. On Postgres:

| Change | Safe way |
|---|---|
| Add an index | `algorithm: :concurrently` with `disable_ddl_transaction!` |
| Add a foreign key | `validate: false`, then `validate_foreign_key` in a second migration |
| `NOT NULL` on a filled column | a check constraint with `validate: false`, validate it, `change_column_null`, drop the check |
| Remove a column | `self.ignored_columns += ["name"]` deployed first, then the migration |
| Rename a column or table | a new one, write both, backfill, switch reads, drop the old |
| Change a column's type | a new column and a backfill (most type changes rewrite the table) |
| Backfill data | a job or a separate migration in batches, not inside the schema change |

- `StrongMigrations.lock_timeout` (a few seconds) and `statement_timeout`
  set, so a migration waiting on a lock fails fast instead of queueing every
  request behind it. Adding a column with a constant default is instant on
  Postgres 11+.
- `db/schema.rb` (or `structure.sql` when the database has views, triggers
  or functions) committed with the migration; a migration that ran is never
  edited.

## 7. Jobs

- Active Job on Solid Queue (Rails 8's default, backed by the database:
  `bin/jobs` runs the workers, `config/queue.yml` sets queues and threads,
  `config/recurring.yml` holds scheduled work), or Sidekiq with Redis where
  the project has it or volume demands it.
- Jobs take records or ids (GlobalID passes records as ids and loads them
  when the job runs) and are idempotent (`backend-jobs`). `retry_on` what
  can succeed later (`wait: :polynomially_longer, attempts: 10`),
  `discard_on` what never will (`ActiveJob::DeserializationError` when the
  record is gone).
- Solid Queue's `limits_concurrency` for jobs that must not run twice at
  once for the same record; Mission Control Jobs to see and retry failures.
- Mail with `deliver_later`, never `deliver_now` in a request.

## 8. Authentication and authorisation

- Rails 8's `bin/rails generate authentication`: database sessions,
  `has_secure_password` (bcrypt), password reset, and a rate limit on
  sign-in; sign-up is yours to add. Devise where the project has it or needs
  confirmation, locking and OAuth together. API tokens are random, shown
  once and stored as a digest; `has_secure_token` keeps them in plain text,
  so not for credentials (`backend-auth`).
- `rate_limit to: 10, within: 3.minutes, only: :create` (7.2+) on sign-in,
  sign-up, reset and anything that sends mail. It counts in the cache
  store, which must be shared across instances.
- Pundit (or Action Policy): a policy per model, `authorize @order` in each
  action, `policy_scope(Order)` for lists, and
  `after_action :verify_authorized` (plus `verify_policy_scoped` on `index`)
  so a forgotten check fails in tests.

## 9. JSON and errors

- Serializers decide the fields: Alba (fast, explicit) or Jbuilder views
  where the project uses them. Never `render json: @record` or `to_json` of
  a model: every column goes out, future ones included.
- Lists paginated in the query (pagy, or keyset on `(created_at, id)`) with
  the associations the serializer shows preloaded.

```ruby
class Api::BaseController < ActionController::API
  rescue_from ActiveRecord::RecordNotFound do
    render_problem 404, "not_found"
  end

  rescue_from ActiveRecord::RecordInvalid do |e|
    render_problem 422, "invalid",
                   errors: e.record.errors.map { |err| { field: err.attribute, code: err.type } }
  end

  private

  def render_problem(status, code, **extra)
    render json: { status: status, code: code, **extra }, status: status,
           content_type: "application/problem+json"
  end
end
```

- `StaleObjectError` and domain errors (`OutOfStock`) get their own
  `rescue_from` with `409` and a code; anything else reaches Rails's handler,
  a bare `500` in production. Status `422` is `:unprocessable_content` in
  Rack 3.1+ (`:unprocessable_entity` before).
- Messages users read come from I18n (`errors.add(:quantity, :too_many)`
  with keys in `config/locales`, the `i18n` skill).

## 10. Configuration and logs

- Secrets in encrypted credentials, edited with
  `bin/rails credentials:edit --environment production` and read with
  `Rails.application.credentials.dig(:stripe, :secret_key)`, the key in
  `RAILS_MASTER_KEY` on the server; or in `ENV` where the platform provides
  them. `config/master.key` and `config/credentials/*.key` never committed.
- Required values read so a missing one fails at boot:
  `ENV.fetch("STRIPE_SECRET_KEY")` in an initializer, not `ENV["..."]` deep
  in a request.
- `config.filter_parameters` covers passwords, tokens, keys and card
  numbers (the generated list plus yours); `config.log_tags = [:request_id]`;
  JSON logs through lograge or the project's logger.

## 11. Caching, real-time and files

- `Rails.cache.fetch(key, expires_in: 10.minutes, race_condition_ttl: 10.seconds)`
  on Solid Cache (Rails 8's default) or Redis; keys from
  `cache_key_with_version`, fragment caching with `cache @product`, and
  Russian-doll nesting with `touch: true` on `belongs_to` (`backend-caching`).
- Turbo Streams broadcasts (`broadcasts_refreshes`) or Action Cable channels
  on Solid Cable or Redis, authorised in the channel's `subscribed`
  (`backend-realtime`).
- Active Storage with direct uploads to S3 or R2 and variants through
  libvips (`backend-files`).

## 12. Tests

```ruby
class OrdersApiTest < ActionDispatch::IntegrationTest
  test "refuses an order for more than the stock" do
    product = products(:kopi) # a fixture with stock: 5
    post api_v1_orders_url, as: :json, headers: auth_headers(users(:ana)),
         params: { order: { lines: [{ product_id: product.id, quantity: 999 }] } }
    assert_response :conflict
    assert_equal "out_of_stock", response.parsed_body["code"]
    assert_equal 5, product.reload.stock
  end
end
```

- Minitest (the default) or RSpec, as the project has; fixtures or
  factory_bot; request tests through the whole stack against Postgres, as
  in production (`bin/rails db:test:prepare` in CI).
- `ActiveJob::TestHelper` (`assert_enqueued_with`, `perform_enqueued_jobs`),
  `travel_to` for time, WebMock so no test reaches a real service,
  `parallelize(workers: :number_of_processors)`.
- System tests (Capybara) only for the few flows that need a browser.

## Check it

`bin/rails test` (or `bundle exec rspec`), `bin/rubocop`
(rubocop-rails-omakase), `bin/brakeman`; `bin/rails db:migrate` then
`bin/rails db:rollback` on a copy for reversible migrations;
`bin/rails routes -g orders` for the routes. Then `bin/rails server` and
`curl` the endpoints: an invalid body gives every field with its code,
another user's id a `404`. The log of a list request shows one query per
association, not one per row, and the tests raise no strict loading error.

## Avoid

`permit!` or raw `params` into `create`; uniqueness checked only in Ruby;
callbacks that send mail, charge or call APIs; `deliver_now` in a request;
`render json: @record`; `Model.all.each`; N+1 hidden by a small development
database; plain `save` inside a transaction; migrations that lock big tables
(plain indexes, validated foreign keys, type changes); editing a migration
that ran; the master key committed; `has_secure_token` values used as API
keys; no `verify_authorized`; tests that call real services.
