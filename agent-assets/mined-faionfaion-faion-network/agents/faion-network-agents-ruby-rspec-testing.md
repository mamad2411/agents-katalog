# RSpec Testing Patterns

## Summary

**One-sentence:** Structure RSpec specs with describe/context/it BDD style, factory_bot for fixtures, request specs for HTTP, isolated unit specs for services, and shared_examples for cross-class invariants.

**One-paragraph:** RSpec is the Ruby BDD testing framework. Effective use: describe the SUT, context for variant conditions, it for behavior; factory_bot.build_stubbed for unit specs (no DB), factory_bot.create for integration; request specs for HTTP behavior; isolated unit specs (without rails_helper) for services; shared_examples for cross-class invariants. Avoid letting tests grow database-coupled; prefer in-memory builds where possible.

**Ефективно для:**

- Rails 7/8 проєкти з RSpec як test framework.
- Сервіси, що мають ізольовані unit specs (без Rails boot).
- Інтеграційні request specs для HTTP behavior.
- Refactor old TestUnit-style або minitest проєктів у RSpec idiom.

## Applies If (ALL must hold)

- Rails 7+ project with rspec-rails + factory_bot installed.
- Tests run in CI on every push.
- Suite size justifies investment in shared_examples + custom matchers.
- Team writes specs in TDD/BDD style (not after-the-fact).

## Skip If (ANY kills it)

- Project uses minitest exclusively — different idiom.
- Suite under 50 specs — overhead > benefit.
- Throwaway scripts.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subject under test | Ruby class | developer |
| Factories | spec/factories/*.rb | fixtures |
| spec_helper + rails_helper | config files | repo |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: describe-context-it, factory-bot-build-stubbed-default, isolated-service-specs, shared-examples-for-invariants, no-let-bang-when-not-needed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | sonnet | Templated describe/context/it. |
| `design-cases` | opus | Identifying meaningful variants is judgment. |
| `lint-create-overuse` | haiku | Mechanical grep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/place_order_service_spec.rb` | Isolated RSpec service spec (spec_helper only) |
| `templates/shared_examples_auditable.rb` | Shared examples for the 'auditable' invariant across models |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rspec-testing.py` | Validate the spec artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[php-phpunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/place_order_service_spec.rb`

```ruby
# frozen_string_literal: true

require "spec_helper"
require_relative "../../../app/services/orders/place_order_service"
require_relative "../../../app/services/service_result"

RSpec.describe Orders::PlaceOrderService do
  let(:user) { instance_double("User", id: 1) }
  let(:orders_relation) { instance_double("Orders") }
  let(:order) { instance_double("Order", id: 7, items: [], total_cents: 1000) }
  let(:gateway) { instance_double("PaymentGateway") }
  let(:inventory) { instance_double("InventoryService") }
  let(:mailer) { class_double("OrderMailer") }

  subject(:service) { described_class.new(user, gateway: gateway, inventory: inventory, mailer: mailer) }

  before do
    allow(user).to receive(:orders).and_return(orders_relation)
    allow(orders_relation).to receive(:build).and_return(order)
  end

  context "when inventory sufficient and payment succeeds" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(order).to receive(:update!)
      allow(inventory).to receive(:reserve).and_return(double(success?: true))
      allow(gateway).to receive(:charge).and_return(double(success?: true, id: "ch_1"))
      allow(mailer).to receive_message_chain(:confirmation, :deliver_later)
    end

    it "returns success with the order" do
      result = service.call(items: [{ sku: "X", qty: 1 }])
      expect(result.success?).to be true
      expect(result.data).to eq(order)
    end
  end

  context "when inventory is insufficient" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(inventory).to receive(:reserve).and_return(double(success?: false))
    end

    it "returns failure with :insufficient_stock" do
      result = service.call(items: [])
      expect(result.failure?).to be true
      expect(result.error).to eq(:insufficient_stock)
    end
  end

  context "when payment is declined" do
    before do
      allow(order).to receive(:save).and_return(true)
      allow(inventory).to receive(:reserve).and_return(double(success?: true))
      allow(gateway).to receive(:charge).and_return(double(success?: false))
    end

    it "returns failure with :payment_declined" do
      result = service.call(items: [{ sku: "X", qty: 1 }])
      expect(result.failure?).to be true
      expect(result.error).to eq(:payment_declined)
    end
  end
end
```

### `templates/shared_examples_auditable.rb`

```ruby
# frozen_string_literal: true

RSpec.shared_examples_for "auditable" do
  it "tracks created_by" do
    expect(subject).to respond_to(:created_by_id)
  end

  it "tracks updated_by" do
    expect(subject).to respond_to(:updated_by_id)
  end

  it "exposes audit_log association" do
    expect(subject.class.reflect_on_association(:audit_log)).not_to be_nil
  end
end
```
