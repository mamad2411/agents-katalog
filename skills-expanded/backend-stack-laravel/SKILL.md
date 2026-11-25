---
name: backend-stack-laravel
description: "A Laravel backend (11 to 13): API routes and resource controllers, Form Requests, mass assignment, API Resources, Eloquent without N+1, chunking, transactions and race-free updates, policies and gates, Sanctum, exception rendering to consistent JSON, queues with Horizon, the scheduler, events and listeners, caching, config caching and Octane in production, tests with Pest or PHPUnit, Larastan and Pint. Read when building or changing a Laravel app."
---

# Laravel

The generated Laravel app: `$request->all()` into `Order::create()`,
`$guarded = []`, a model returned as JSON with hidden columns and a lazy load
per row, authorisation only in the Vue page, `env()` called in a controller
(it returns `null` once config is cached), a job dispatched inside a
transaction that runs before the commit, and a scheduled command running on
every server. The backend rules are in the `backend` skill; these are
Laravel's own. Keep the project's version, structure and packages; the notes
below assume Laravel 11 or later (`bootstrap/app.php` for middleware and
exceptions). Laravel 13 (current, PHP 8.3+) adds PHP attributes for much of
the configuration; use them when the project does.

## 1. Routes and controllers

- API routes in `routes/api.php` (`php artisan install:api` adds it), grouped
  with a prefix and middleware (`auth:sanctum`); resource controllers
  (`Route::apiResource('orders', OrderController::class)`) and route model
  binding.
- Thin controllers: a Form Request in, one call to an action or service
  class (`app/Actions/PayOrder.php`) that holds the rules, an API Resource
  out.
- Nested resources with `->scoped()`, so `/orders/1/items/5` is a `404` when
  item 5 is not order 1's.
- The base controller has no traits since Laravel 11: `$this->authorize()`
  needs `AuthorizesRequests` added; `Gate::authorize('refund', $order)` works
  anywhere (Laravel 13 also has the `#[Authorize]` controller attribute).
- Rate limits defined in `AppServiceProvider::boot()`, applied as
  `throttle:api`:
  `RateLimiter::for('api', fn (Request $r) => Limit::perMinute(60)->by($r->user()?->id ?: $r->ip()))`;
  tighter ones (`Limit::perMinute(5)`) on sign-in and anything that mails.

## 2. Input

- A Form Request per write (`StoreOrderRequest`) with `rules()` and
  `authorize()`; the controller uses `$request->validated()`, never
  `$request->all()`.
- Models list `$fillable` explicitly; never `$guarded = []`. Fields a user
  must not set (`role`, `price`, `user_id`) are assigned in code. Laravel 13
  writes the list as `#[Fillable([...])]` on the class.
- Unknown fields refused (`backend-api`): Laravel 13 has
  `#[FailOnUnknownFields]` per request, or `FormRequest::failOnUnknownFields()`
  once in a service provider.

```php
public function rules(): array
{
    return [
        'lines' => ['required', 'array', 'min:1', 'max:50'],
        'lines.*.product_id' => ['required', 'uuid', Rule::exists('products', 'id')],
        'lines.*.quantity' => ['required', 'integer', 'between:1,100'],
        'note' => ['nullable', 'string', 'max:500'],
    ];
}
```

## 3. Output

- API Resources (`OrderResource`, `OrderResource::collection`) decide the
  fields; never return a model or `->toArray()` directly (hidden columns and
  future ones leak).
- Lists with `->paginate(25)` or `->cursorPaginate(25)` in the query,
  `with()` for the relations the resource shows.
- Relations in a resource through `$this->whenLoaded('items')` and counts
  through `whenCounted`, so a resource never triggers a query of its own.
  `JsonResource::withoutWrapping()` in `AppServiceProvider` returns a record
  as itself rather than inside `data`.
- Errors in the format of `backend-errors`, rendered in `bootstrap/app.php`
  with `->withExceptions(...)` for requests that expect JSON; `abort(404)` and
  domain exceptions with a `render` method rather than hand-built responses.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(fn (Request $r) => $r->is('api/*') || $r->expectsJson());
    $exceptions->render(function (ValidationException $e, Request $request) {
        if (! $request->is('api/*')) {
            return null; // web forms keep the redirect back with errors
        }
        $errors = [];
        foreach ($e->validator->failed() as $field => $rules) { // ['lines.0.quantity' => ['Between' => [...]]]
            foreach (array_keys($rules) as $rule) {
                $errors[] = ['field' => preg_replace('/\.(\d+)/', '[$1]', $field), 'code' => Str::snake($rule)];
            }
        }
        return response()->json(['type' => 'https://example.com/errors/validation-failed', 'status' => 422,
            'code' => 'validation_failed', 'errors' => $errors], 422, ['Content-Type' => 'application/problem+json']);
    });
})
```

- Laravel answers validation with `422`; keep it when clients rely on it
  (`backend-api` allows either).

## 4. Who may do what

- Policies per model (`OrderPolicy`) and `$this->authorize('refund',
  $order)` or `Gate`, on every action; queries scoped to the user or tenant
  (a global scope, or `$user->orders()`), so another id in the URL gives
  `404`.
- A policy can answer `Response::denyAsNotFound()` where even a `403` would
  reveal that the record exists; `before()` for the admin shortcut.

```php
class OrderPolicy
{
    public function refund(User $user, Order $order): Response
    {
        return $order->user_id === $user->id ? Response::allow() : Response::denyAsNotFound();
    }
}

// The controller: a Form Request in, the check, one action, a resource out.
public function refund(RefundOrderRequest $request, Order $order, RefundOrder $refund): OrderResource
{
    Gate::authorize('refund', $order);
    return new OrderResource($refund($order, $request->validated('reason')));
}
```

- Sanctum: cookie sessions for the app's own frontend (with `statefulApi()`
  and CSRF), personal access tokens with abilities for mobile and other
  clients. Starter kits (Breeze, or the React, Vue and Livewire kits) and
  Fortify for sign-in, reset and verification rather than writing them.
- Sanctum tokens never expire by default (`expiration` is `null` in
  `config/sanctum.php`): set it, and schedule `sanctum:prune-expired
  --hours=24`. Abilities are checked with `$request->user()->tokenCan(...)`
  or the `abilities` and `ability` middleware, whose aliases are registered
  in `bootstrap/app.php`.

## 5. Eloquent and data

- `Model::preventLazyLoading(! app()->isProduction())` in
  `AppServiceProvider`, so N+1 fails in development; `with()`,
  `withCount()`, `load()` to load relations. `Model::shouldBeStrict()` also
  makes a silently discarded or a missing attribute throw.
- `DB::transaction(fn () => ...)` around writes that belong together.
  Race-free stock with a conditional update that reports rows changed:
  `Product::whereKey($id)->where('stock', '>=', $qty)->decrement('stock',
  $qty)` returns 0 when there is not enough; `lockForUpdate()` inside the
  transaction when you must read then write.
- `DB::transaction($callback, 3)` retries a deadlocked transaction up to three
  times; `createOrFirst()` leans on a unique index where `firstOrCreate()`
  races; `upsert()` for bulk writes.
- Casts for types (`'total' => 'integer'`, enums, `'immutable_datetime'`) in
  the `casts()` method, money as integers, timestamps in UTC (`'timezone' =>
  'UTC'` in `config/app.php`; `APP_TIMEZONE=UTC` in Laravel 11), converted
  for display.
- Large sets in pieces: `chunkById(500, ...)` (plain `chunk()` skips rows
  when the callback changes the filtered column), `lazyById()` to stream,
  never `->get()` on a whole table.
- Public ids with `HasUuids` (UUIDv7 since Laravel 12, so inserts stay in
  index order) or `HasUlids`; `php artisan model:show Order` lists a model's
  casts, relations and columns.
- Migrations from `php artisan make:migration`, with foreign keys
  (`foreignId('order_id')->constrained()->restrictOnDelete()`) and unique
  indexes; factories and seeders for sample data.

## 6. Queues and the scheduler

- Jobs implementing `ShouldQueue` with `$tries`, `backoff()`, `ShouldBeUnique`
  where a duplicate would harm, and `afterCommit` so they never run before
  the transaction; the database driver to start, Redis with Horizon later.
- Laravel 13 declares these with attributes (`#[Tries(5)]`,
  `#[Backoff(10, 60, 300)]`, `#[Timeout(120)]`); `ShouldQueueAfterCommit`
  makes every dispatch wait for the commit.

```php
#[Tries(5), Backoff(10, 60, 300), Timeout(60)]
class SendReceipt implements ShouldQueueAfterCommit
{
    use Queueable;

    public function __construct(public int $orderId) {} // an id, fetched again in handle()

    public function middleware(): array
    {
        return [new WithoutOverlapping($this->orderId)];
    }

    public function handle(ReceiptMailer $mailer): void
    {
        $mailer->sendOnce(Order::findOrFail($this->orderId)); // safe to run twice
    }
}
```

- A job's timeout stays below the connection's `retry_after` (90 seconds in
  `config/queue.php`), or a slow job is handed to a second worker while the
  first still runs. Job middleware for the rest: `WithoutOverlapping`,
  `RateLimited`, `ThrottlesExceptions`; a `failed()` method for the last
  failure (`backend-jobs`).
- Horizon supervises Redis workers from `config/horizon.php`; each deploy
  runs `php artisan horizon:terminate` (plain workers: `queue:restart`, and
  `queue:work --max-time=3600`), since long-lived workers keep the old code.
- Scheduled work in `routes/console.php` with `->onOneServer()` and
  `->withoutOverlapping()`; one `schedule:run` cron or `schedule:work`.
  `onOneServer` needs a shared cache store with locks (Redis, database,
  Memcached, DynamoDB).
- Mail and notifications queued (`ShouldQueue`), with texts through the lang
  files (the `i18n` skill).

## 7. Events and caching

- Events for side effects other parts react to; listeners in
  `app/Listeners` are discovered by their type-hint, queued with
  `ShouldQueue`, and wait for the commit with
  `ShouldHandleEventsAfterCommit`.
- `Cache::remember("product:{$id}", now()->addMinutes(10), fn () => ...)`;
  `Cache::flexible('stats', [300, 600], fn () => ...)` serves stale while it
  refreshes; `Cache::lock("order:{$id}", 10)->block(5, fn () => ...)` for one
  writer at a time; tags only on Redis and Memcached. More in
  `backend-caching`.

## 8. Config, logs and production

- `env()` only inside `config/*.php`; code reads `config('services.x.key')`,
  and production runs `php artisan config:cache`.
- `Log::withContext(['request_id' => ...])` in a middleware; no request
  bodies with passwords or tokens in the log. `Context::add('request_id',
  $id)` (Laravel 11+) does more: it lands on every log record and travels
  into queued jobs.
- Deploys run `php artisan optimize` (config, events, routes and views
  cached), migrations as their own step, and the worker restart above.
  `APP_DEBUG=false`; JSON logs to stderr in containers (`LOG_CHANNEL=stderr`,
  `LOG_STDERR_FORMATTER=Monolog\Formatter\JsonFormatter`); the `/up` route
  for health checks (`backend-observability`).
- Octane (FrankenPHP, Swoole or RoadRunner) boots the app once for many
  requests: no request or user state in singletons or static properties
  (resolve the request where it is used), `octane:reload` on deploy, and
  `--max-requests` (500 by default) recycles workers that leak.

## 9. Tests

Pest or PHPUnit feature tests with `RefreshDatabase`, factories and
`actingAs($user)`; `postJson()` with `assertStatus`, `assertJsonPath` and
`assertJsonValidationErrors`; `Http::fake()`, `Queue::fake()`, `Mail::fake()`
and `$this->travelTo(...)`; the test database of the same kind as
production (`backend-testing`).

```php
it("does not reveal another user's order", function () {
    $order = Order::factory()->create(); // belongs to someone else
    $this->actingAs(User::factory()->create())
        ->postJson("/api/orders/{$order->id}/pay")
        ->assertNotFound();
    expect($order->fresh()->status)->toBe('open');
});
```

- `Http::preventStrayRequests()` fails any outbound call without a fake;
  `Sanctum::actingAs($user, ['orders:write'])` for token abilities;
  `Exceptions::fake()` to assert what was reported; `$this->freezeTime()`;
  `php artisan test --parallel` gives each process its own database.
- `assertJsonValidationErrors` reads Laravel's default `errors` object: once
  validation renders as problem details, assert with `assertJsonPath` on the
  `errors` list instead.
- Pest 5 needs PHP 8.4; Pest 4 runs on PHP 8.3.

## 10. Check

`php artisan test`, `./vendor/bin/pint --test`, Larastan or PHPStan when the
project has it (`vendor/bin/phpstan analyse`, with Larastan's
`extension.neon` included and the level raised over time), `php artisan
route:list` for the routes, `composer audit`, then call them with `curl`.

## Avoid

`$request->all()` into `create()`; `$guarded = []`; models returned as JSON;
authorisation only in the frontend; lazy loading in a loop; `env()` outside
config; a job that runs before its transaction commits; scheduled commands
that run on every server; rules written in controllers; a job timeout above
`retry_after`; workers left on old code after a deploy; Sanctum tokens that
never expire; `chunk()` over rows the callback updates; request state in a
singleton under Octane.
