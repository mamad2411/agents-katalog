# Rails

Expert Ruby on Rails development with Rails 7/8 conventions, security hardening, and performance patterns.

## Rails Version Awareness

These instructions target Rails 7+ / Rails 8. Key modern defaults:
- Propshaft (Rails 8) or Sprockets (7) for assets
- `bin/importmap` for JS by default — avoid Webpacker
- Solid Queue replaces Sidekiq in default Rails 8 stack
- `authenticate` DSL built into Rails 8 (no Devise needed for simple cases)
- SQLite in production is now a first-class option with Litestream

## Models

```ruby
class User < ApplicationRecord
  has_many :posts, dependent: :destroy
  has_secure_password  # BCrypt hashing; adds authenticate()

  validates :email, presence: true,
                    uniqueness: { case_sensitive: false },
                    format: { with: URI::MailTo::EMAIL_REGEXP }
  normalizes :email, with: ->(e) { e.strip.downcase }
end
```

- Use `normalizes` (Rails 7.1+) instead of `before_validation` for simple transformations
- Avoid fat callbacks — use service objects or form objects for complex workflows
- Scope query logic to the model: `scope :published, -> { where(published: true) }`
- Use `includes` to prevent N+1: `Post.includes(:author).limit(20)`

## Controllers

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: %i[show edit update destroy]

  def create
    @post = current_user.posts.build(post_params)
    if @post.save
      redirect_to @post, notice: t('.created')
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_post
    @post = current_user.posts.find(params[:id])
  end

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

- Always scope finds through the current user's association — never `Post.find(params[:id])` bare
- Return `status: :unprocessable_entity` on failed `render` so Turbo handles it correctly
- Use `respond_to` blocks only when you need both HTML and JSON; otherwise keep it simple

## Security Defaults

Rails provides many protections by default — don't accidentally disable them:

```ruby
# config/application.rb — verify these are enabled
config.force_ssl = true  # production only, set in config/environments/production.rb
config.action_dispatch.default_headers = {
  'X-Frame-Options'         => 'SAMEORIGIN',
  'X-Content-Type-Options'  => 'nosniff',
  'X-XSS-Protection'        => '1; mode=block'
}
```

- Always use `params.require(...).permit(...)` — never `params[:post]` directly
- CSRF protection is on by default; don't use `protect_from_forgery with: :null_session` in HTML controllers
- Use encrypted credentials (`bin/rails credentials:edit`) — never hardcode secrets

## Queries & Performance

```ruby
# Avoid N+1 — eager load associations
Post.includes(:author, :tags).where(published: true).order(created_at: :desc)

# Use select to load only needed columns
User.select(:id, :email, :name).where(active: true)

# Counter cache for association counts
belongs_to :category, counter_cache: true
# Add migration: add_column :categories, :posts_count, :integer, default: 0
```

- Add a database index for every foreign key and every column used in `where` / `order`
- Use `explain` in the Rails console to verify query plans: `User.where(email: 'x').explain`
- Cache expensive queries with `Rails.cache.fetch("key", expires_in: 1.hour) { ... }`
- Use `turbo_frame_tag` for incremental page updates rather than full-page reload

## Background Jobs

**Rails 8 (Solid Queue, default):**
```ruby
class WelcomeEmailJob < ApplicationJob
  queue_as :mailers
  retry_on Net::TimeoutError, wait: 5.seconds, attempts: 3

  def perform(user_id)
    UserMailer.welcome(User.find(user_id)).deliver_now
  end
end

WelcomeEmailJob.perform_later(user.id)
```

**Rails 7 with Sidekiq:**
```ruby
# Gemfile: gem 'sidekiq'
# config/application.rb: config.active_job.queue_adapter = :sidekiq
```

- Always pass IDs, not AR objects — jobs must serialize/deserialize safely
- Set `retry_on` for transient errors; use `discard_on` for permanent failures (e.g. `ActiveRecord::RecordNotFound`)

## Migrations

```ruby
class AddIndexToUsersEmail < ActiveRecord::Migration[8.0]
  def change
    add_index :users, :email, unique: true
    add_column :posts, :slug, :string, null: false, default: ''
  end
end
```

- Never use `up`/`down` when `change` with reversible operations is sufficient
- Always set `null: false` and `default:` for non-nullable columns
- Use `add_foreign_key` to enforce referential integrity at the DB level
- Never modify existing migrations — create a new one

## Testing with RSpec + FactoryBot

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    password { 'password123' }
  end
end

# spec/models/post_spec.rb
RSpec.describe Post, type: :model do
  it 'is invalid without a title' do
    expect(Post.new(title: nil)).not_to be_valid
  end
end

# spec/requests/posts_spec.rb
RSpec.describe 'Posts', type: :request do
  let(:user) { create(:user) }

  before { sign_in user }

  it 'creates a post' do
    post posts_path, params: { post: { title: 'Hello', body: 'World' } }
    expect(response).to redirect_to(Post.last)
  end
end
```

- Use request specs for integration; avoid controller specs (deprecated pattern)
- Use `vcr` or `webmock` to stub HTTP calls in tests
