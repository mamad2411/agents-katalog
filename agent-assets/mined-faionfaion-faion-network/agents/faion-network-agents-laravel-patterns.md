# Laravel Patterns

## Summary

**One-sentence:** Idiomatic Laravel layered architecture: thin controllers, Form Requests for validation, services for business logic, Eloquent models accessed via services, and API Resources for serialization.

**One-paragraph:** Build Laravel 10/11/12 APIs with a clean Controller → FormRequest → Service → Resource stack. Controllers stay HTTP-only, Form Requests own validation + authorization, services own transactions and business logic, Eloquent models are accessed only via services, and API Resources shape responses. The pattern keeps controllers under 50 lines and makes the app's behaviour testable without hitting HTTP.

**Ефективно для:**

- Greenfield Laravel API проєкти, де очікується довге життя і команда >1 розробника.
- Refactor fat-controllers де бізнес-логіка живе у controller methods.
- Стандартизація API-версіонування (Api\V1\) + Sanctum / Passport на boundary.
- Уніфікація валідації через Form Requests з authorize() + rules() + messages().

## Applies If (ALL must hold)

- Laravel 10/11/12 project (Eloquent + standard request lifecycle).
- API serves JSON to clients (not Inertia / Livewire / Filament).
- Team needs reproducible CRUD slice generators (controller + form request + resource + service + policy).
- Transactions span >1 Eloquent call (cross-aggregate writes).

## Skip If (ANY kills it)

- Tiny apps (<10 routes) — service layer is over-engineering.
- Projects standardized on lorisleiva/laravel-actions, Spatie LaravelData, or DDD — check team standard first.
- Inertia / Livewire / Filament — framework idiom is different (controller ↔ component).
- Console-only artisan apps — controller/Form Request/Resource trio doesn't apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain resource | Eloquent model + migration | domain model |
| API contract | OpenAPI / route plan | product |
| Auth scheme | Sanctum / Passport tokens | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[php-laravel]] | Laravel framework basics (routing, providers) assumed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: no-eloquent-in-controller, form-request-for-validation, api-resource-for-response, service-owns-transaction, policy-for-authorization | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-crud-slice` | sonnet | Templated artisan + boilerplate. |
| `design-policy-rules` | opus | Authorization decisions are domain-heavy. |
| `lint-fat-controller` | haiku | Mechanical line-count + grep audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/OrderController.php` | Thin Api/V1 controller delegating to service + returning Resource |
| `templates/OrderService.php` | Service owning DB::transaction + business rules |
| `templates/StoreOrderRequest.php` | Form Request with authorize() + rules() + messages() |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-laravel-patterns.py` | Validate the Laravel slice artefact against the schema | Pre-commit + CI |
| `scripts/laravel-layering-audit.sh` | Lint Eloquent calls in controllers, DB::transaction in controllers, raw model responses | Pre-commit + CI on Laravel projects |

## Related

- [[php-laravel]]
- [[php-laravel-patterns]]
- [[php-laravel-queues]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/OrderController.php`

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreOrderRequest;
use App\Http\Requests\UpdateOrderRequest;
use App\Http\Resources\OrderResource;
use App\Models\Order;
use App\Services\OrderService;

class OrderController extends Controller
{
    public function __construct(private readonly OrderService $service)
    {
        $this->authorizeResource(Order::class, 'order');
    }

    public function store(StoreOrderRequest $request): OrderResource
    {
        return new OrderResource($this->service->create($request->validated()));
    }

    public function update(UpdateOrderRequest $request, Order $order): OrderResource
    {
        return new OrderResource($this->service->update($order, $request->validated()));
    }

    public function show(Order $order): OrderResource
    {
        return new OrderResource($order->loadMissing('items'));
    }
}
```

### `templates/OrderService.php`

```php
<?php

namespace App\Services;

use App\Models\Order;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = Order::create([
                'user_id' => auth()->id(),
                'status' => 'pending',
            ]);
            foreach ($data['items'] as $item) {
                $order->items()->create($item);
            }
            return $order->load('items');
        });
    }

    public function update(Order $order, array $data): Order
    {
        return DB::transaction(function () use ($order, $data) {
            $order->update(array_filter($data, fn($k) => $k !== 'items', ARRAY_FILTER_USE_KEY));
            if (isset($data['items'])) {
                $order->items()->delete();
                foreach ($data['items'] as $item) {
                    $order->items()->create($item);
                }
            }
            return $order->fresh('items');
        });
    }
}
```

### `templates/StoreOrderRequest.php`

```php
<?php

namespace App\Http\Requests;

use App\Models\Order;
use Illuminate\Foundation\Http\FormRequest;

class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'items' => ['required', 'array', 'min:1', 'max:100'],
            'items.*.sku' => ['required', 'string', 'regex:/^[A-Z0-9-]+$/'],
            'items.*.qty' => ['required', 'integer', 'min:1', 'max:999'],
        ];
    }

    public function messages(): array
    {
        return [
            'items.required' => 'order must have at least one line item',
            'items.*.sku.regex' => 'SKU must be uppercase alphanumeric',
        ];
    }
}
```
