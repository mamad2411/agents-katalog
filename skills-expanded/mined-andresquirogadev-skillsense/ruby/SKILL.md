# Ruby

Expert Ruby development with modern idioms, performance patterns, and testing best practices.

## Language & Style

- Use `frozen_string_literal: true` at the top of every file to reduce object allocations
- Prefer `symbol.to_proc` for simple enumerables: `users.map(&:name)` over `users.map { |u| u.name }`
- Use keyword arguments for methods with 2+ optional params; avoids positional confusion
- Avoid `rescue Exception` — rescue `StandardError` or specific subclasses only
- Use `Struct.new(:a, :b, keyword_init: true)` for lightweight value objects
- Prefer `then` / `yield_self` for pipeline-style transformations over deep nesting

## Memory & Performance

- Use `lazy` enumerators for large collections: `(1..Float::INFINITY).lazy.select { ... }.first(10)`
- Avoid creating unnecessary strings in loops; use symbols where semantics allow
- Use `frozen_string_literal` and `String#dup` only when mutation is needed
- Profile with `ruby-prof` or `stackprof` before optimizing; don't guess

## Testing with RSpec

```ruby
# Describe behavior, not implementation
RSpec.describe Order do
  describe '#total' do
    subject(:order) { described_class.new(items: [item]) }
    let(:item) { build(:item, price: 9.99) }

    it 'sums item prices' do
      expect(order.total).to eq(9.99)
    end
  end
end
```

- Use `let` for lazy setup, `let!` only when the side effect is required before the example
- Prefer `described_class` over hardcoding the class name
- Use FactoryBot factories for complex models; avoid fixtures
- Use `aggregate_failures` to report all failures in one example rather than stopping at first

## Sidekiq (Background Jobs)

```ruby
class EmailWorker
  include Sidekiq::Job
  sidekiq_options retry: 3, queue: :mailers

  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end

# Enqueue
EmailWorker.perform_async(user.id)
EmailWorker.perform_in(5.minutes, user.id)
```

- Always pass serializable primitives (IDs, strings) — never pass ActiveRecord objects
- Set explicit retry counts per job; rely on exponential backoff for transient failures
- Use `Sidekiq::Testing.fake!` in tests; assertions via `EmailWorker.jobs.size`

## Devise Authentication

- Generate with `rails generate devise:install` then `rails generate devise User`
- Override only what you need; avoid monkey-patching Devise internals
- Use `authenticate_user!` as a before action; scope queries with `current_user`

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!

  def create
    @post = current_user.posts.build(post_params)
    @post.save ? redirect_to(@post) : render(:new, status: :unprocessable_entity)
  end
end
```

- Use `devise_for :users, controllers: { sessions: 'users/sessions' }` to customize controllers

## Error Handling

- Raise specific errors that inherit from `StandardError`; include a descriptive message
- Use `rescue` at the boundary (controller, job), not deep in domain logic
- Log errors with context: `Rails.logger.error { "Payment failed: #{e.message}" }` (block form is lazy)

## Common Patterns

```ruby
# Safe navigation operator — avoids NoMethodError on nil
user&.profile&.avatar_url

# Pattern matching (Ruby 3.x)
case response
in { status: 200, body: String => body }
  process(body)
in { status: 422, errors: [*, String => first, *] }
  handle_error(first)
end

# Pop idiom for consuming a value
token = params.delete(:token)
```
