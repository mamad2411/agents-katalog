# Ruby on Rails Service Objects

## Summary

**One-sentence:** Extract multi-step business workflows from fat controllers and models into service-object classes (app/services/BoundedContext/ActionService) with a single #call method returning a ServiceResult (success/failure).

**One-paragraph:** Service objects encapsulate one business action (PlaceOrder, CancelOrder, RefundOrder). One class per action; one public #call method; explicit return type (ServiceResult.success(data:) / ServiceResult.failure(error:)). Services own the transaction boundary, validation, and orchestration; controllers stay thin; models stay focused on persistence + invariants. The pattern compresses sprawling logic into named, testable units.

**Ефективно для:**

- Rails apps з fat controllers (>80 LoC per action) або fat models (>500 LoC).
- Multi-step business flows (place_order, refund, cancel) з ≥3 кроками.
- Onboarding нових devs — services є named entry points для бізнес-логіки.
- Refactor god-objects (Order model з 30+ methods) у service-based decomposition.

## Applies If (ALL must hold)

- Rails app with multi-step business workflows.
- Models or controllers exceed maintainability thresholds (>500 / >80 LoC).
- Team commits to a per-action service pattern (not Interactor / Trailblazer / dry-monads).
- Tests can isolate service logic from HTTP + DB.

## Skip If (ANY kills it)

- Trivial CRUD app (model.update is enough).
- Team already on Trailblazer Operations / Interactor — different abstraction.
- Workflows are simple enough that the model's public method works fine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Business action | named operation (verb + object) | product |
| Current fat code | controller method or model method | repo |
| ServiceResult class | Ruby class with .success / .failure factories | repo / app/services |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ruby-rails]] | Rails conventions are the substrate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one-action-per-service, service-result-explicit, service-owns-tx, no-callbacks-call-services, service-tested-in-isolation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `name-and-scope-service` | opus | Naming + context decision is high-judgment. |
| `implement-call` | sonnet | Move logic + add ServiceResult. |
| `lint-callback-calls-service` | haiku | Mechanical grep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/place_order_service.rb` | Service object skeleton with #call + ServiceResult + transaction |
| `templates/service_result.rb` | ServiceResult value object with .success / .failure factories + predicates |
| `templates/spec-skeleton.rb` | RSpec skeleton for service isolation test (no rails_helper) |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails-patterns.py` | Validate the service-object artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails]]
- [[ruby-activerecord]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/place_order_service.rb`

```ruby
module Orders
  class PlaceOrderService
    def initialize(user, gateway: PaymentGateway.instance, inventory: InventoryService.new, mailer: OrderMailer)
      @user = user
      @gateway = gateway
      @inventory = inventory
      @mailer = mailer
    end

    def call(params)
      ActiveRecord::Base.transaction do
        order = build_order(params)
        return ServiceResult.failure(error: :invalid_params, details: order.errors) unless order.save

        stock = @inventory.reserve(order.items)
        return ServiceResult.failure(error: :insufficient_stock) unless stock.success?

        charge = @gateway.charge(amount: order.total_cents, customer: @user)
        return ServiceResult.failure(error: :payment_declined) unless charge.success?

        order.update!(charge_id: charge.id, status: :paid)
        @mailer.confirmation(order).deliver_later

        ServiceResult.success(data: order)
      end
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(error: :validation_error, details: e.record.errors.full_messages)
    end

    private

    def build_order(params)
      @user.orders.build(params).tap do |order|
        order.status = :pending
        order.placed_at = Time.current
      end
    end
  end
end
```

### `templates/service_result.rb`

```ruby
class ServiceResult
  attr_reader :data, :error, :details

  def self.success(data: nil)
    new(success: true, data: data)
  end

  def self.failure(error:, details: nil)
    new(success: false, error: error, details: details)
  end

  def initialize(success:, data: nil, error: nil, details: nil)
    @success = success
    @data = data
    @error = error
    @details = details
  end

  def success?
    @success
  end

  def failure?
    !@success
  end
end
```

### `templates/spec-skeleton.rb`

```ruby
# frozen_string_literal: true

require "spec_helper"
require_relative "../../app/services/orders/place_order_service"
require_relative "../../app/services/service_result"

RSpec.describe Orders::PlaceOrderService do
  let(:user) { instance_double("User", id: 1, orders: orders_relation) }
  let(:orders_relation) { instance_double("Orders") }
  let(:gateway) { instance_double("PaymentGateway") }
  let(:inventory) { instance_double("InventoryService") }
  let(:mailer) { class_double("OrderMailer") }

  subject(:service) { described_class.new(user, gateway: gateway, inventory: inventory, mailer: mailer) }

  it "returns success when all steps succeed" do
    # Arrange
    order = build_stubbed_order
    allow(orders_relation).to receive(:build).and_return(order)
    allow(order).to receive(:save).and_return(true)
    allow(inventory).to receive(:reserve).and_return(double(success?: true))
    allow(gateway).to receive(:charge).and_return(double(success?: true, id: "ch_1"))
    allow(order).to receive(:update!)
    allow(mailer).to receive_message_chain(:confirmation, :deliver_later)

    # Act
    result = service.call(items: [{ sku: "X", qty: 1 }])

    # Assert
    expect(result.success?).to be true
    expect(result.data).to eq(order)
  end

  it "returns failure when inventory insufficient" do
    order = build_stubbed_order
    allow(orders_relation).to receive(:build).and_return(order)
    allow(order).to receive(:save).and_return(true)
    allow(inventory).to receive(:reserve).and_return(double(success?: false))

    result = service.call(items: [])
    expect(result.failure?).to be true
    expect(result.error).to eq(:insufficient_stock)
  end

  def build_stubbed_order
    instance_double("Order", id: 1, items: [], total_cents: 1000)
  end
end
```
