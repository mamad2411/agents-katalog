# Laravel Layered Patterns (Controller → Service → Resource)

## Summary

**One-sentence:** Layered Laravel architecture: thin HTTP controllers, services owning business logic + transactions, Eloquent via services, Form Requests for validation, API Resources for responses, Policies for authorization.

**One-paragraph:** Strict layering: controllers stay HTTP-only (parse + delegate + serialize via Resource), Form Requests own validation + authorize(), services own multi-step business logic + DB::transaction, Eloquent is accessed only via services, API Resources shape responses, Policies centralize permission checks. The methodology overlaps with laravel-patterns but is the per-project layering manifest, not just CRUD scaffolding.

**Ефективно для:**

- Команди >2 розробники, що хочуть стандартизувати Laravel layout.
- Refactor legacy fat-controllers (>100 LoC) у layered structure.
- Migration від facades-everywhere до DI-everywhere + Policies + Resources.
- Code review checklist: layering як binary gate в PR.

## Applies If (ALL must hold)

- Laravel 10/11/12 project with >5 controllers.
- Team agreed layering convention (controller → service → eloquent).
- API + JSON responses are dominant (not Inertia / Blade).
- Code review enforces architectural rules (PRs blocked on violations).

## Skip If (ANY kills it)

- Tiny app — layering overhead > benefit.
- Project uses Spatie LaravelData / Actions instead of services.
- Inertia.js / Livewire — different component model.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Code style guide | CONTRIBUTING.md | team lead |
| Existing controllers | app/Http/Controllers/ | repo |
| Domain models | Eloquent classes | domain |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[laravel-patterns]] | Per-slice CRUD scaffolding pattern. |
| [[php-laravel]] | Framework basics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: controller-thin, form-request-required, resource-required, service-owns-tx, policy-required | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-layering` | haiku | Mechanical script run. |
| `extract-service` | sonnet | Templated move of methods. |
| `design-policy-rules` | opus | Authorization decisions are domain-heavy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller.php` | Thin layered controller skeleton |
| `templates/service.php` | Service with DB::transaction + business rules |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel-patterns.py` | Validate the layering audit artefact against the schema | Pre-commit + CI |
| `scripts/laravel-anti-pattern-lint.sh` | Lint fat controllers / inline validation / raw responses / tx in controller | Pre-commit + CI |

## Related

- [[laravel-patterns]]
- [[php-laravel]]
- [[php-eloquent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/controller.php`

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreOrderRequest;
use App\Http\Requests\UpdateOrderRequest;
use App\Http\Resources\OrderResource;
use App\Models\Order;
use App\Services\OrderService;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class OrderController extends Controller
{
    public function __construct(private readonly OrderService $service)
    {
        $this->authorizeResource(Order::class, 'order');
    }

    public function index(): AnonymousResourceCollection
    {
        return OrderResource::collection($this->service->listForCurrentUser());
    }

    public function store(StoreOrderRequest $request): OrderResource
    {
        return new OrderResource($this->service->create($request->validated()));
    }

    public function update(UpdateOrderRequest $request, Order $order): OrderResource
    {
        return new OrderResource($this->service->update($order, $request->validated()));
    }

    public function destroy(Order $order): void
    {
        $this->service->cancel($order);
    }
}
```

### `templates/service.php`

```php
<?php

namespace App\Services;

use App\Models\Order;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function listForCurrentUser(): Collection
    {
        return Order::where('user_id', auth()->id())->with('items')->latest()->get();
    }

    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = Order::create(['user_id' => auth()->id(), 'status' => 'pending']);
            foreach ($data['items'] as $item) {
                $order->items()->create($item);
            }
            return $order->load('items');
        });
    }

    public function cancel(Order $order): void
    {
        DB::transaction(function () use ($order) {
            $order->update(['status' => 'cancelled', 'cancelled_at' => now()]);
            event(new OrderCancelled($order));
        });
    }
}
```
