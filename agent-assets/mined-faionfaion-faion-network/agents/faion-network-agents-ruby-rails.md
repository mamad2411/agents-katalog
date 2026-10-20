# Ruby on Rails Framework Fundamentals

## Summary

**One-sentence:** Use Rails 7/8 idioms: convention over configuration, RESTful routing, Strong Parameters, callbacks, concerns for shared logic, and config-environment isolation.

**One-paragraph:** Rails is opinionated; fighting conventions costs months. Adopt the patterns: RESTful resourceful routing (resources :orders), Strong Parameters for mass-assign safety, model callbacks only for invariants (not external side effects), concerns for ≥2-model shared logic, generators for scaffolding, credentials.yml for secrets, and environment-isolated config. Mixing Sinatra-style ad-hoc routes or skipping Strong Parameters defeats Rails' security posture.

**Ефективно для:**

- Greenfield Rails 7/8 проєкти — задати ідіоматичну structure.
- Refactor non-RESTful routes у resources + member/collection convention.
- Migration від config-soup до credentials.yml + environment-specific config.
- Onboarding нових Ruby-devs — methodology як reading list + conventions.

## Applies If (ALL must hold)

- Rails 7+ project (Hotwire-aware).
- Application serves HTML and/or JSON.
- Team commits to Rails conventions (vs Sinatra ad-hoc style).
- Strong Parameters enabled (Rails default).

## Skip If (ANY kills it)

- Rails API-only mode with separate FE — no Hotwire/Turbo; methodology applies but skip view-layer rules.
- Project standardized on Hanami/Roda instead of Rails — different framework.
- Trivial app — convention overhead > benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource definition | Ruby class + table | domain |
| Routes file | config/routes.rb | repo |
| Credentials | config/credentials.yml.enc + master key | ops |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: restful-resources, strong-parameters, credentials-not-env, concern-for-shared-multi-model, callback-only-for-invariants | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `refactor-routes` | sonnet | Mechanical grouping by resource. |
| `decide-callback-vs-service` | opus | Distinguishing invariant vs side effect is judgment. |
| `lint-strong-params` | haiku | Mechanical regex. |

## Templates

| File | Purpose |
|------|---------|
| `templates/routes.rb` | RESTful routes with member/collection convention |
| `templates/orders_controller.rb` | RESTful controller with Strong Parameters + Pundit authorization |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails.py` | Validate the Rails module artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails-patterns]]
- [[ruby-activerecord]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/routes.rb`

```ruby
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :orders, only: %i[index show create update destroy] do
        member do
          patch :cancel
          post :refund
        end

        collection do
          get :recent
        end

        resources :items, only: %i[index show create destroy], shallow: true
      end

      resource :session, only: %i[create destroy]
      resources :users, only: %i[show update]
    end
  end

  get "/health", to: "health#show"
  root "home#index"
end
```

### `templates/orders_controller.rb`

```ruby
class Api::V1::OrdersController < Api::V1::BaseController
  before_action :set_order, only: %i[show update destroy cancel refund]

  def index
    @orders = policy_scope(Order).includes(:items).recent
    render json: OrderResource.from_collection(@orders)
  end

  def show
    authorize @order
    render json: OrderResource.from(@order)
  end

  def create
    @order = OrderService.new(current_user).create(order_params)
    render json: OrderResource.from(@order), status: :created
  end

  def update
    authorize @order
    OrderService.new(current_user).update(@order, order_params)
    render json: OrderResource.from(@order)
  end

  def cancel
    authorize @order, :cancel?
    OrderService.new(current_user).cancel(@order)
    head :no_content
  end

  private

  def set_order
    @order = Order.find(params[:id])
  end

  def order_params
    params.require(:order).permit(:note, items_attributes: %i[sku qty])
  end
end
```
