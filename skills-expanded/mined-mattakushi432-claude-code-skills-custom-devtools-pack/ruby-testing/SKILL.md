---
name: ruby-testing
description: "When to activate: RSpec, describe context it, let and let!, FactoryBot, factories vs fixtures, request specs, shared examples, verified doubles, instance_double, VCR, Ruby testing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Ruby Testing Patterns

## When to Use

Writing unit, request, or integration specs with RSpec, including Rails-flavored request specs and factory-based test data.

## Core Patterns

### describe / context / it Structure

```ruby
RSpec.describe DiscountCalculator do
  describe "#rate_for" do
    context "when total is below the minimum threshold" do
      it "returns zero" do
        expect(described_class.rate_for(500)).to eq(0.0)
      end
    end

    context "when total qualifies for gold tier" do
      it "returns the gold discount rate" do
        expect(described_class.rate_for(10_000)).to eq(0.15)
      end
    end
  end
end
```

Use `describe` for the thing under test, `context` for the scenario/precondition, `it` for the expected behavior — reads like a spec, not a list of method names.

### let vs let!

```ruby
RSpec.describe Order do
  let(:customer) { create(:customer) }               # lazy — only built when referenced
  let!(:existing_order) { create(:order, customer:) } # eager — built before every example

  it "excludes cancelled orders from the pending scope" do
    create(:order, customer:, status: :cancelled)
    expect(Order.pending).to contain_exactly(existing_order)
  end
end
```

Prefer `let` by default; reach for `let!` only when a record must exist before the example runs (e.g. testing a scope that queries existing rows).

### FactoryBot Over Fixtures

```ruby
FactoryBot.define do
  factory :order do
    customer
    status { :pending }
    total_cents { 5000 }

    trait :shipped do
      status { :shipped }
      shipped_at { Time.current }
    end
  end
end

# In a spec
order = create(:order, :shipped, total_cents: 12_000)
```

Factories build exactly the data a test needs, are composable via traits, and avoid the shared-global-state fragility of static YAML fixtures.

### Request Specs Over Controller Specs

```ruby
RSpec.describe "POST /orders", type: :request do
  it "creates an order for an authenticated user" do
    customer = create(:customer)
    product = create(:product, price_cents: 1500)

    post "/orders", params: {
      order: { customer_id: customer.id, items: [{ sku: product.sku, qty: 2 }] }
    }, headers: auth_headers(customer.user)

    expect(response).to have_http_status(:created)
    expect(response.parsed_body["total_cents"]).to eq(3000)
  end
end
```

Request specs exercise the full stack (routing, middleware, params) — controller specs are deprecated in modern RSpec-Rails.

### Verified Doubles Over Loose Doubles

```ruby
# RISKY: a loose double never checks that #charge actually exists on PaymentGateway
gateway = double("gateway", charge: true)

# BETTER: verified against the real class's public interface —
# fails if PaymentGateway#charge is renamed or removed
gateway = instance_double(PaymentGateway, charge: true)

allow(PaymentGateway).to receive(:new).and_return(gateway)
```

### Shared Examples for Repeated Contracts

```ruby
RSpec.shared_examples "an archivable record" do
  it "excludes archived records from the default scope" do
    archived = create(described_class.name.underscore.to_sym, archived_at: Time.current)
    expect(described_class.active).not_to include(archived)
  end
end

RSpec.describe Order do
  it_behaves_like "an archivable record"
end
```

### VCR for External HTTP Calls

```ruby
RSpec.describe PaymentGateway do
  it "captures a payment" do
    VCR.use_cassette("payment_gateway/capture_success") do
      result = PaymentGateway.new.charge(amount: 5000, token: "tok_test")
      expect(result).to be_success
    end
  end
end
```

Records the real HTTP interaction once, replays it on subsequent runs — fast, deterministic, no live third-party dependency in CI.

## Checklist

- [ ] Specs read as behavior descriptions (`context "when ..."`, `it "does ..."`), not method-name echoes
- [ ] FactoryBot used instead of static fixtures for anything beyond trivial seed data
- [ ] Request specs used instead of controller specs
- [ ] Mocks/stubs are verified doubles (`instance_double`, `class_double`), not loose `double()`
- [ ] External HTTP calls go through VCR cassettes or WebMock stubs, never hit the real network in CI
- [ ] `let!` used deliberately, not as a default habit that slows every example down

## Quick Reference

| Need | Tool |
|---|---|
| Test data | FactoryBot |
| Full-stack HTTP test | Request spec |
| Verified test double | `instance_double` / `class_double` |
| Shared behavior contract | `shared_examples` / `it_behaves_like` |
| Record/replay external HTTP | VCR |
| Coverage report | SimpleCov |

## See Also

- `skills/ruby-ecosystem/rails-patterns.md`
- `skills/ruby-ecosystem/ruby-patterns.md`
