---
name: ruby-on-rails
description: >
  Ruby on Rails best practices covering ActiveRecord, controllers, service objects,
  background jobs, testing, and API design. Use this skill when building or
  maintaining Rails applications.
license: MIT
metadata:
  author: skillbox
  version: "1.0"
  category: backend
  tags: rails, ruby, activerecord, api, web
---

# Ruby on Rails Best Practices

## Project Structure and Conventions

Follow Rails conventions but add structure for business logic. Do not put all logic in models or controllers.

```
app/
  controllers/
    api/
      v1/
        orders_controller.rb
        users_controller.rb
  models/
    order.rb
    user.rb
  services/            # business logic
    orders/
      create_order.rb
      cancel_order.rb
    payments/
      process_payment.rb
  forms/               # complex validations and multi-model operations
    registration_form.rb
  queries/             # complex database queries
    orders/
      dashboard_query.rb
  serializers/         # API response formatting
    order_serializer.rb
  jobs/                # background jobs
    send_order_confirmation_job.rb
  policies/            # authorization (with Pundit)
    order_policy.rb
config/
  initializers/
db/
  migrate/
spec/
  models/
  requests/
  services/
  factories/
```

## ActiveRecord Patterns

### Scopes

Use scopes for reusable query conditions. Keep them composable.

```ruby
# app/models/order.rb
class Order < ApplicationRecord
  belongs_to :customer, class_name: "User"
  has_many :order_items, dependent: :destroy
  has_many :products, through: :order_items

  enum :status, {
    pending: "pending",
    confirmed: "confirmed",
    shipped: "shipped",
    delivered: "delivered",
    cancelled: "cancelled"
  }

  scope :active, -> { where.not(status: :cancelled) }
  scope :recent, -> { where(created_at: 30.days.ago..) }
  scope :for_customer, ->(customer_id) { where(customer_id: customer_id) }
  scope :expensive, -> { where(total_amount: 100..) }

  validates :total_amount, presence: true, numericality: { greater_than: 0 }
  validates :status, presence: true

  def confirm!
    raise InvalidTransitionError unless pending?
    update!(status: :confirmed, confirmed_at: Time.current)
  end
end

# Usage: composable
Order.active.recent.for_customer(user.id).expensive
```

### Associations

Set `dependent` on every `has_many`. Use `inverse_of` when Rails cannot infer it.

```ruby
class User < ApplicationRecord
  has_many :orders, foreign_key: :customer_id, dependent: :restrict_with_error, inverse_of: :customer
  has_many :addresses, dependent: :destroy
end

class Order < ApplicationRecord
  belongs_to :customer, class_name: "User", counter_cache: true
  has_many :order_items, dependent: :destroy
end
```

Use `counter_cache: true` for counts displayed frequently. It avoids a COUNT query every time.

### Callbacks

Use callbacks only for data integrity within the same model. Do not use them for side effects like sending emails or calling external services.

```ruby
# ACCEPTABLE: maintaining data integrity
class OrderItem < ApplicationRecord
  belongs_to :order
  belongs_to :product

  after_save :recalculate_order_total
  after_destroy :recalculate_order_total

  private

  def recalculate_order_total
    order.update_column(:total_amount, order.order_items.sum("quantity * unit_price"))
  end
end

# BAD: side effect in callback -- use a service object instead
class Order < ApplicationRecord
  after_create :send_confirmation_email  # WRONG: hidden, hard to test, runs in transaction
  after_create :charge_payment           # WRONG: external call inside DB transaction
end
```

## Controllers

Keep controllers thin. They handle HTTP concerns: params, auth, response codes. Business logic belongs in service objects.

```ruby
# app/controllers/api/v1/orders_controller.rb
module Api
  module V1
    class OrdersController < ApplicationController
      before_action :authenticate_user!
      before_action :set_order, only: [:show, :cancel]

      def index
        orders = current_user.orders
          .active
          .includes(order_items: :product)
          .order(created_at: :desc)
          .page(params[:page])
          .per(20)

        render json: OrderSerializer.new(orders).serializable_hash, status: :ok
      end

      def create
        result = Orders::CreateOrder.call(
          customer: current_user,
          items: order_params[:items]
        )

        if result.success?
          render json: OrderSerializer.new(result.order).serializable_hash, status: :created
        else
          render json: { errors: result.errors }, status: :unprocessable_entity
        end
      end

      def cancel
        result = Orders::CancelOrder.call(order: @order)

        if result.success?
          render json: OrderSerializer.new(result.order).serializable_hash, status: :ok
        else
          render json: { errors: result.errors }, status: :unprocessable_entity
        end
      end

      private

      def set_order
        @order = current_user.orders.find(params[:id])
      end

      def order_params
        params.require(:order).permit(items: [:product_id, :quantity])
      end
    end
  end
end
```

## Service Objects

Encapsulate business operations in service objects. Use a consistent interface.

```ruby
# app/services/orders/create_order.rb
module Orders
  class CreateOrder
    attr_reader :order, :errors

    def self.call(**args)
      new(**args).call
    end

    def initialize(customer:, items:)
      @customer = customer
      @items = items
      @errors = []
    end

    def call
      ActiveRecord::Base.transaction do
        create_order
        create_order_items
        reserve_stock
      end

      SendOrderConfirmationJob.perform_later(@order.id) if success?
      self
    rescue ActiveRecord::RecordInvalid => e
      @errors << e.message
      self
    end

    def success?
      @errors.empty? && @order&.persisted?
    end

    private

    def create_order
      @order = Order.create!(
        customer: @customer,
        status: :pending,
        total_amount: calculate_total
      )
    end

    def create_order_items
      @items.each do |item|
        product = Product.find(item[:product_id])
        @order.order_items.create!(
          product: product,
          quantity: item[:quantity],
          unit_price: product.price
        )
      end
    end

    def reserve_stock
      @items.each do |item|
        product = Product.lock.find(item[:product_id])
        remaining = product.stock - item[:quantity]
        raise ActiveRecord::RecordInvalid, "Insufficient stock for #{product.name}" if remaining < 0
        product.update!(stock: remaining)
      end
    end

    def calculate_total
      @items.sum do |item|
        product = Product.find(item[:product_id])
        product.price * item[:quantity]
      end
    end
  end
end
```

## Form Objects

Use form objects for complex validations that span multiple models or do not map to a single ActiveRecord model.

```ruby
# app/forms/registration_form.rb
class RegistrationForm
  include ActiveModel::Model
  include ActiveModel::Validations

  attr_accessor :email, :password, :password_confirmation, :company_name, :plan

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 12 }
  validates :password_confirmation, presence: true
  validates :company_name, presence: true
  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      user = User.create!(email: email, password: password)
      company = Company.create!(name: company_name, owner: user)
      Subscription.create!(company: company, plan: plan)
    end
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end

  private

  def passwords_match
    errors.add(:password_confirmation, "does not match") unless password == password_confirmation
  end
end
```

## Background Jobs with Sidekiq

Keep jobs small, idempotent, and retriable. Pass IDs, not objects.

```ruby
# app/jobs/send_order_confirmation_job.rb
class SendOrderConfirmationJob < ApplicationJob
  queue_as :default
  retry_on Net::SMTPServerBusy, wait: :polynomially_longer, attempts: 5
  discard_on ActiveRecord::RecordNotFound

  def perform(order_id)
    order = Order.includes(:customer, order_items: :product).find(order_id)
    OrderMailer.confirmation(order).deliver_now
  end
end
```

```ruby
# config/sidekiq.yml
:concurrency: 10
:queues:
  - [critical, 3]
  - [default, 2]
  - [low, 1]
```

Use `retry_on` for transient failures and `discard_on` for permanent failures. Do not let jobs silently fail.

## Testing with RSpec

### Model Specs

```ruby
# spec/models/order_spec.rb
RSpec.describe Order, type: :model do
  describe "validations" do
    it { is_expected.to validate_presence_of(:total_amount) }
    it { is_expected.to validate_numericality_of(:total_amount).is_greater_than(0) }
  end

  describe "scopes" do
    let!(:active_order) { create(:order, status: :confirmed) }
    let!(:cancelled_order) { create(:order, status: :cancelled) }

    it "returns only active orders" do
      expect(Order.active).to include(active_order)
      expect(Order.active).not_to include(cancelled_order)
    end
  end

  describe "#confirm!" do
    let(:order) { create(:order, status: :pending) }

    it "transitions from pending to confirmed" do
      order.confirm!
      expect(order.reload.status).to eq("confirmed")
      expect(order.confirmed_at).to be_present
    end

    it "raises error when not pending" do
      order.update!(status: :shipped)
      expect { order.confirm! }.to raise_error(InvalidTransitionError)
    end
  end
end
```

### Request Specs

Use request specs instead of controller specs. They test the full stack.

```ruby
# spec/requests/api/v1/orders_spec.rb
RSpec.describe "Api::V1::Orders", type: :request do
  let(:user) { create(:user) }
  let(:headers) { auth_headers_for(user) }

  describe "GET /api/v1/orders" do
    let!(:user_order) { create(:order, customer: user) }
    let!(:other_order) { create(:order) }

    it "returns only the user's orders" do
      get "/api/v1/orders", headers: headers

      expect(response).to have_http_status(:ok)
      order_ids = json_response["data"].map { |o| o["id"] }
      expect(order_ids).to include(user_order.id)
      expect(order_ids).not_to include(other_order.id)
    end

    it "returns 401 without auth" do
      get "/api/v1/orders"
      expect(response).to have_http_status(:unauthorized)
    end
  end

  describe "POST /api/v1/orders" do
    let(:product) { create(:product, price: 29.99, stock: 10) }

    it "creates an order" do
      post "/api/v1/orders",
        params: { order: { items: [{ product_id: product.id, quantity: 2 }] } },
        headers: headers

      expect(response).to have_http_status(:created)
      expect(json_response["data"]["attributes"]["total_amount"]).to eq("59.98")
    end
  end
end
```

### Factories with FactoryBot

```ruby
# spec/factories/orders.rb
FactoryBot.define do
  factory :order do
    association :customer, factory: :user
    status { :pending }
    total_amount { 99.99 }

    trait :confirmed do
      status { :confirmed }
      confirmed_at { Time.current }
    end

    trait :with_items do
      transient do
        items_count { 3 }
      end

      after(:create) do |order, evaluator|
        create_list(:order_item, evaluator.items_count, order: order)
        order.reload
      end
    end
  end
end

# Usage
create(:order, :confirmed, :with_items, items_count: 5)
```

## Database: Migrations, Indexing, N+1 Prevention

### Migrations

Always add indexes for foreign keys and columns used in WHERE clauses:

```ruby
class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders do |t|
      t.references :customer, null: false, foreign_key: { to_table: :users }
      t.string :status, null: false, default: "pending"
      t.decimal :total_amount, precision: 10, scale: 2, null: false
      t.timestamps
    end

    add_index :orders, :status
    add_index :orders, [:customer_id, :status]
    add_index :orders, :created_at
  end
end
```

### N+1 Prevention

Use the `bullet` gem to detect N+1 queries in development:

```ruby
# Gemfile
gem "bullet", group: :development

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.rails_logger = true
end
```

Use `includes` for preloading. Use `preload` when you need separate queries. Use `eager_load` when you need to filter on the association.

```ruby
# includes: Rails chooses preload or eager_load
Order.includes(:order_items).where(status: :pending)

# preload: always separate queries (use when you don't filter on the association)
Order.preload(order_items: :product).all

# eager_load: always LEFT JOIN (use when filtering on association columns)
Order.eager_load(:order_items).where(order_items: { quantity: 5.. })
```

## API Mode with Serializers

Use `jsonapi-serializer` (or `blueprinter`) for consistent API responses.

```ruby
# app/serializers/order_serializer.rb
class OrderSerializer
  include JSONAPI::Serializer

  attributes :status, :total_amount, :created_at

  attribute :customer_name do |order|
    order.customer.full_name
  end

  has_many :order_items, serializer: OrderItemSerializer
end
```

```ruby
# For simpler APIs, use blueprinter
class OrderBlueprint < Blueprinter::Base
  identifier :id

  fields :status, :total_amount, :created_at

  association :order_items, blueprint: OrderItemBlueprint

  view :extended do
    association :customer, blueprint: UserBlueprint
  end
end

# Usage
OrderBlueprint.render(order, view: :extended)
```

## Security

### Authentication with Devise

```ruby
# Gemfile
gem "devise"
gem "devise-jwt"  # for API token auth

# app/models/user.rb
class User < ApplicationRecord
  devise :database_authenticatable, :registerable,
         :recoverable, :validatable,
         :jwt_authenticatable, jwt_revocation_strategy: JwtDenylist
end
```

### Parameter Sanitization

Always use strong parameters. Never use `params.permit!`.

```ruby
# GOOD
def order_params
  params.require(:order).permit(items: [:product_id, :quantity])
end

# BAD: allows mass assignment of any attribute
def order_params
  params.require(:order).permit!
end
```

### Authorization with Pundit

```ruby
# app/policies/order_policy.rb
class OrderPolicy < ApplicationPolicy
  def show?
    record.customer == user
  end

  def cancel?
    record.customer == user && record.pending?
  end

  class Scope < Scope
    def resolve
      scope.where(customer: user)
    end
  end
end

# In controller
def show
  @order = Order.find(params[:id])
  authorize @order
  render json: OrderSerializer.new(@order).serializable_hash
end
```

## Common Pitfalls

1. **Fat models and fat controllers.** Extract business logic to service objects. Models handle persistence and associations. Controllers handle HTTP.
2. **Callbacks for side effects.** Callbacks that send emails, make API calls, or enqueue jobs create hidden coupling and break transactions. Use service objects.
3. **Not using `includes`/`preload`.** Every collection that accesses associations must preload them. Install `bullet` to catch N+1 queries.
4. **Missing database indexes.** Add indexes for every foreign key, every column in WHERE clauses, and every column in ORDER BY clauses.
5. **Using `dependent: :destroy` on large associations.** For large collections, use `dependent: :delete_all` or handle cleanup in a background job to avoid timeout.
6. **Not using database constraints.** Add `null: false`, `unique: true`, and foreign key constraints at the database level. Do not rely only on ActiveRecord validations.
