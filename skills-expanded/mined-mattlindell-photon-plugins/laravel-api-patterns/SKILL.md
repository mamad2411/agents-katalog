---
name: laravel-api-patterns
description: Laravel API development patterns — API Resources, Sanctum token authentication, rate limiting, route groups, exception handling, webhook receivers, and cursor pagination. Use when building Laravel APIs.
---

# Laravel API Patterns

Patterns for building robust REST APIs in Laravel. Covers API Resources, route organization, Sanctum authentication, rate limiting, exception handling, webhook receivers, and cursor-based pagination.

## When to Use This Skill

- Building Laravel API routes with resources and authentication
- Implementing Sanctum token-based auth
- Adding rate limiting to API endpoints
- Receiving and validating webhooks in Laravel
- Designing consistent error response formats (RFC 7807)
- Implementing cursor-based pagination for large datasets

## Core Concepts

- **API Resources over raw models**: Always use Resources to decouple your API shape from your database schema
- **Authentication != Authorization**: Sanctum confirms identity via tokens; abilities and policies check permissions. Always implement both layers
- **Validate at the boundary**: Use Form Request validation or inline `$request->validate()` before business logic
- **Consistent error formatting**: Use RFC 7807 Problem Details for machine-readable errors across all endpoints
- **Pagination by default**: Never return unbounded collections -- always paginate
- **Rate limit everything**: Public endpoints need aggressive limits; authenticated endpoints need per-user limits

---

## Pattern 1: API Resource with Conditional Attributes

Use `$this->when()` and `$this->whenLoaded()` to include fields only when conditions are met or relationships are loaded.

```php
<?php
declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class EventResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'          => $this->id,
            'title'       => $this->title,
            'slug'        => $this->slug,
            'description' => $this->description,
            'status'      => $this->status,
            'starts_at'   => $this->starts_at->toIso8601String(),
            'ends_at'     => $this->ends_at?->toIso8601String(),

            // Include only when the relationship is eager-loaded
            'organizer'   => new UserResource($this->whenLoaded('organizer')),
            'venue'       => new VenueResource($this->whenLoaded('venue')),
            'tickets'     => TicketResource::collection($this->whenLoaded('tickets')),

            // Conditional: include count only when loaded via withCount
            'tickets_count' => $this->when(
                isset($this->tickets_count),
                $this->tickets_count ?? 0
            ),

            // Conditional: include sensitive data only for admins
            'revenue'     => $this->when(
                $request->user()?->hasRole('admin'),
                fn () => $this->tickets->sum('price')
            ),

            // Merge additional attributes conditionally
            $this->mergeWhen($this->status === 'cancelled', [
                'cancelled_at'        => $this->cancelled_at?->toIso8601String(),
                'cancellation_reason' => $this->cancellation_reason,
            ]),

            'created_at'  => $this->created_at->toIso8601String(),
            'updated_at'  => $this->updated_at->toIso8601String(),
        ];
    }

    public function with(Request $request): array
    {
        return [
            'links' => [
                'self' => route('api.events.show', $this->id),
            ],
        ];
    }
}
```

---

## Pattern 2: Resource Collection with Pagination Metadata

```php
<?php
declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class EventCollection extends ResourceCollection
{
    public $collects = EventResource::class;

    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
        ];
    }

    public function with(Request $request): array
    {
        return [
            'meta' => [
                'total'        => $this->total(),
                'per_page'     => $this->perPage(),
                'current_page' => $this->currentPage(),
                'last_page'    => $this->lastPage(),
                'from'         => $this->firstItem(),
                'to'           => $this->lastItem(),
            ],
            'links' => [
                'first' => $this->url(1),
                'last'  => $this->url($this->lastPage()),
                'prev'  => $this->previousPageUrl(),
                'next'  => $this->nextPageUrl(),
            ],
        ];
    }
}

// Usage in controller:
namespace App\Http\Controllers\Api;

use App\Http\Resources\EventCollection;
use App\Models\Event;
use Illuminate\Http\Request;

class EventController extends Controller
{
    public function index(Request $request): EventCollection
    {
        $events = Event::query()
            ->with(['organizer', 'venue'])
            ->withCount('tickets')
            ->when($request->query('status'), fn ($q, $status) => $q->where('status', $status))
            ->when($request->query('search'), fn ($q, $search) => $q->where('title', 'like', "%{$search}%"))
            ->orderBy($request->query('sort', 'starts_at'), $request->query('direction', 'asc'))
            ->paginate($request->query('per_page', 15))
            ->withQueryString();

        return new EventCollection($events);
    }
}
```

---

## Pattern 3: Route Group with Prefix, Middleware, and Naming

```php
<?php
declare(strict_types=1);

// routes/api.php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\EventController;
use App\Http\Controllers\Api\TicketController;
use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\WebhookController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Public Routes (no authentication required)
|--------------------------------------------------------------------------
*/
Route::prefix('v1')->as('api.v1.')->group(function () {
    Route::post('/auth/login', [AuthController::class, 'login'])->name('auth.login');
    Route::post('/auth/register', [AuthController::class, 'register'])->name('auth.register');

    // Public read-only resources
    Route::get('/events', [EventController::class, 'index'])->name('events.index');
    Route::get('/events/{event}', [EventController::class, 'show'])->name('events.show');

    // Webhooks (authenticated via signature, not Sanctum)
    Route::post('/webhooks/stripe', [WebhookController::class, 'stripe'])->name('webhooks.stripe');
});

/*
|--------------------------------------------------------------------------
| Authenticated Routes (Sanctum token required)
|--------------------------------------------------------------------------
*/
Route::prefix('v1')
    ->as('api.v1.')
    ->middleware(['auth:sanctum', 'throttle:api'])
    ->group(function () {
        Route::post('/auth/logout', [AuthController::class, 'logout'])->name('auth.logout');
        Route::get('/auth/user', [AuthController::class, 'user'])->name('auth.user');

        // Events CRUD (create, update, delete require auth)
        Route::apiResource('events', EventController::class)->except(['index', 'show']);

        // Nested resource: event tickets
        Route::apiResource('events.tickets', TicketController::class)->shallow();

        // User profile
        Route::get('/user/profile', [UserController::class, 'profile'])->name('user.profile');
        Route::put('/user/profile', [UserController::class, 'updateProfile'])->name('user.profile.update');
    });

/*
|--------------------------------------------------------------------------
| Admin Routes (Sanctum token + admin ability required)
|--------------------------------------------------------------------------
*/
Route::prefix('v1/admin')
    ->as('api.v1.admin.')
    ->middleware(['auth:sanctum', 'ability:admin', 'throttle:admin-api'])
    ->group(function () {
        Route::get('/users', [UserController::class, 'index'])->name('users.index');
        Route::get('/stats', [EventController::class, 'stats'])->name('stats');
    });
```

---

## Pattern 4: Sanctum Token Authentication

Issue tokens with scoped abilities and revoke them.

```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    /**
     * Issue a new Sanctum token.
     */
    public function login(Request $request): JsonResponse
    {
        $request->validate([
            'email'       => ['required', 'email'],
            'password'    => ['required', 'string'],
            'device_name' => ['required', 'string', 'max:255'],
        ]);

        $user = User::where('email', $request->email)->first();

        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }

        // Define abilities based on user role
        $abilities = match (true) {
            $user->hasRole('admin')     => ['*'],
            $user->hasRole('organizer') => [
                'events:read', 'events:create', 'events:update', 'events:delete',
                'tickets:read', 'tickets:manage',
                'profile:read', 'profile:update',
            ],
            default => [
                'events:read', 'events:create',
                'tickets:read', 'tickets:purchase',
                'profile:read', 'profile:update',
            ],
        };

        $token = $user->createToken(
            name: $request->device_name,
            abilities: $abilities,
            expiresAt: now()->addDays(30),
        );

        return response()->json([
            'token'      => $token->plainTextToken,
            'token_type' => 'Bearer',
            'expires_at' => $token->accessToken->expires_at?->toIso8601String(),
            'abilities'  => $abilities,
            'user'       => $user->only(['id', 'name', 'email']),
        ], 201);
    }

    /**
     * Revoke the current token.
     */
    public function logout(Request $request): JsonResponse
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json(['message' => 'Token revoked.'], 200);
    }

    /**
     * Get the authenticated user and token info.
     */
    public function user(Request $request): JsonResponse
    {
        $user  = $request->user();
        $token = $user->currentAccessToken();

        return response()->json([
            'user'  => $user->only(['id', 'name', 'email', 'created_at']),
            'token' => [
                'name'       => $token->name,
                'abilities'  => $token->abilities,
                'expires_at' => $token->expires_at?->toIso8601String(),
                'last_used'  => $token->last_used_at?->toIso8601String(),
            ],
        ]);
    }
}

// -- Checking abilities in controllers: -----------------------------------

class EventController extends Controller
{
    public function update(Request $request, Event $event): JsonResponse
    {
        // Check that the token has the required ability
        if (! $request->user()->tokenCan('events:update')) {
            abort(403, 'Token does not have the events:update ability.');
        }

        // Also check ownership
        if ($event->organizer_id !== $request->user()->id && ! $request->user()->tokenCan('*')) {
            abort(403, 'You can only update your own events.');
        }

        // ... perform update
    }
}

// -- Custom middleware for ability checking: -------------------------------

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class CheckTokenAbility
{
    public function handle(Request $request, Closure $next, string ...$abilities): Response
    {
        foreach ($abilities as $ability) {
            if (! $request->user()?->tokenCan($ability)) {
                abort(403, "Token missing required ability: {$ability}");
            }
        }

        return $next($request);
    }
}

// Register in bootstrap/app.php:
// ->withMiddleware(function (Middleware $middleware) {
//     $middleware->alias([
//         'ability' => \App\Http\Middleware\CheckTokenAbility::class,
//     ]);
// })
```

---

## Pattern 5: Rate Limiting

Define custom rate limiters and apply them to routes.

```php
<?php
declare(strict_types=1);

// App\Providers\AppServiceProvider (or bootstrap/app.php for Laravel 11+)

use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        $this->configureRateLimiting();
    }

    private function configureRateLimiting(): void
    {
        // Default API limiter: 60 requests per minute per user/IP
        RateLimiter::for('api', function (Request $request) {
            return Limit::perMinute(60)
                ->by($request->user()?->id ?: $request->ip())
                ->response(function (Request $request, array $headers) {
                    return response()->json([
                        'type'   => 'https://httpproblems.com/http-status/429',
                        'title'  => 'Too Many Requests',
                        'status' => 429,
                        'detail' => 'Rate limit exceeded. Try again in ' . $headers['Retry-After'] . ' seconds.',
                    ], 429, $headers);
                });
        });

        // Stricter limiter for authentication endpoints
        RateLimiter::for('auth', function (Request $request) {
            return [
                Limit::perMinute(5)->by('auth:' . $request->ip()),
                Limit::perHour(30)->by('auth-hourly:' . $request->ip()),
            ];
        });

        // Dynamic limiter based on subscription tier
        RateLimiter::for('tiered', function (Request $request) {
            $user = $request->user();

            if (! $user) {
                return Limit::perMinute(10)->by($request->ip());
            }

            return match ($user->subscription_tier) {
                'enterprise' => Limit::none(),
                'pro'        => Limit::perMinute(300)->by($user->id),
                'basic'      => Limit::perMinute(60)->by($user->id),
                default      => Limit::perMinute(30)->by($user->id),
            };
        });
    }
}

// Apply rate limiters to routes (routes/api.php):

Route::middleware('throttle:auth')->group(function () {
    Route::post('/auth/login', [AuthController::class, 'login']);
    Route::post('/auth/register', [AuthController::class, 'register']);
});

Route::middleware(['auth:sanctum', 'throttle:tiered'])->group(function () {
    Route::apiResource('events', EventController::class);
});
```

---

## Pattern 6: Exception Handling for API Responses

Customize how exceptions are rendered for API consumers using RFC 7807 Problem Details.

```php
<?php
declare(strict_types=1);

// bootstrap/app.php (Laravel 11+)

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Auth\AuthenticationException;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpKernel\Exception\HttpException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\HttpKernel\Exception\TooManyRequestsHttpException;

return Application::configure(basePath: dirname(__DIR__))
    ->withExceptions(function (Exceptions $exceptions) {

        // Render all API exceptions as RFC 7807 Problem Details
        $exceptions->render(function (Throwable $e, Request $request) {
            if (! $request->is('api/*') && ! $request->expectsJson()) {
                return null; // Let Laravel handle non-API exceptions normally
            }

            return match (true) {
                $e instanceof ValidationException => response()->json([
                    'type'   => 'https://httpproblems.com/http-status/422',
                    'title'  => 'Validation Failed',
                    'status' => 422,
                    'detail' => 'The request data did not pass validation.',
                    'errors' => $e->errors(),
                ], 422),

                $e instanceof ModelNotFoundException,
                $e instanceof NotFoundHttpException => response()->json([
                    'type'   => 'https://httpproblems.com/http-status/404',
                    'title'  => 'Resource Not Found',
                    'status' => 404,
                    'detail' => 'The requested resource could not be found.',
                ], 404),

                $e instanceof AuthenticationException => response()->json([
                    'type'   => 'https://httpproblems.com/http-status/401',
                    'title'  => 'Unauthenticated',
                    'status' => 401,
                    'detail' => 'A valid authentication token is required.',
                ], 401),

                $e instanceof TooManyRequestsHttpException => response()->json([
                    'type'        => 'https://httpproblems.com/http-status/429',
                    'title'       => 'Too Many Requests',
                    'status'      => 429,
                    'detail'      => 'Rate limit exceeded.',
                    'retry_after' => $e->getHeaders()['Retry-After'] ?? null,
                ], 429, $e->getHeaders()),

                $e instanceof HttpException => response()->json([
                    'type'   => 'https://httpproblems.com/http-status/' . $e->getStatusCode(),
                    'title'  => \Symfony\Component\HttpFoundation\Response::$statusTexts[$e->getStatusCode()] ?? 'Error',
                    'status' => $e->getStatusCode(),
                    'detail' => $e->getMessage() ?: 'An error occurred.',
                ], $e->getStatusCode()),

                // Catch-all for unexpected errors
                default => response()->json([
                    'type'   => 'https://httpproblems.com/http-status/500',
                    'title'  => 'Internal Server Error',
                    'status' => 500,
                    'detail' => app()->hasDebugModeEnabled()
                        ? $e->getMessage()
                        : 'An unexpected error occurred.',
                ], 500),
            };
        });
    })
    ->create();
```

---

## Pattern 7: Webhook Receiver with Signature Validation and Idempotency

Securely receive webhooks with HMAC signature verification, idempotency checks, and async processing via queued jobs.

```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessWebhookEvent;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class WebhookController extends Controller
{
    public function stripe(Request $request): JsonResponse
    {
        // 1. Validate signature
        $payload   = $request->getContent();
        $signature = $request->header('Stripe-Signature', '');
        $secret    = config('services.stripe.webhook_secret');

        if (! $this->verifyStripeSignature($payload, $signature, $secret)) {
            Log::warning('Webhook signature verification failed.', [
                'ip' => $request->ip(),
            ]);

            return response()->json(['error' => 'Invalid signature.'], 401);
        }

        $event = json_decode($payload, true);

        // 2. Idempotency check
        $eventId  = $event['id'] ?? null;
        $cacheKey = 'webhook:stripe:' . md5($eventId);

        if (Cache::has($cacheKey)) {
            return response()->json(['status' => 'already_processed'], 200);
        }

        // 3. Dispatch to queue for async processing
        ProcessWebhookEvent::dispatch(
            provider: 'stripe',
            eventType: $event['type'],
            eventData: $event['data'],
            eventId: $eventId,
        );

        // 4. Mark as processed (48-hour TTL)
        Cache::put($cacheKey, true, now()->addHours(48));

        return response()->json(['status' => 'accepted'], 200);
    }

    private function verifyStripeSignature(
        string $payload,
        string $signatureHeader,
        string $secret,
        int $tolerance = 300,
    ): bool {
        $parts = collect(explode(',', $signatureHeader))
            ->mapWithKeys(function (string $pair) {
                [$key, $value] = explode('=', $pair, 2);

                return [trim($key) => trim($value)];
            });

        $timestamp = $parts->get('t', '');
        $expected  = $parts->get('v1', '');

        if (! $timestamp || ! $expected) {
            return false;
        }

        if (abs(time() - (int) $timestamp) > $tolerance) {
            return false;
        }

        $computed = hash_hmac('sha256', $timestamp . '.' . $payload, $secret);

        return hash_equals($expected, $computed);
    }
}

// The background job:
namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class ProcessWebhookEvent implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public array $backoff = [30, 120, 600];

    public function __construct(
        public readonly string $provider,
        public readonly string $eventType,
        public readonly array $eventData,
        public readonly string $eventId,
    ) {}

    public function handle(): void
    {
        Log::info("Processing {$this->provider} webhook: {$this->eventType}", [
            'event_id' => $this->eventId,
        ]);

        match ($this->eventType) {
            'payment_intent.succeeded'          => $this->handlePaymentSucceeded(),
            'customer.subscription.deleted'     => $this->handleSubscriptionCancelled(),
            'invoice.payment_failed'            => $this->handlePaymentFailed(),
            default => Log::info("Unhandled webhook type: {$this->eventType}"),
        };
    }

    private function handlePaymentSucceeded(): void
    {
        // Business logic for successful payment...
    }

    private function handleSubscriptionCancelled(): void
    {
        // Business logic for subscription cancellation...
    }

    private function handlePaymentFailed(): void
    {
        // Business logic for failed payment...
    }
}
```

---

## Pattern 8: Error Response Format -- RFC 7807 Problem Details

A reusable Problem Details builder class. Use this alongside Pattern 6 (exception handling) for consistent error responses.

```php
<?php
declare(strict_types=1);

class ProblemDetails implements JsonSerializable
{
    public function __construct(
        private readonly string $type,
        private readonly string $title,
        private readonly int $status,
        private readonly ?string $detail = null,
        private readonly ?string $instance = null,
        private readonly array $extensions = [],
    ) {}

    public function jsonSerialize(): array
    {
        $data = [
            'type'   => $this->type,
            'title'  => $this->title,
            'status' => $this->status,
        ];

        if ($this->detail !== null) {
            $data['detail'] = $this->detail;
        }

        if ($this->instance !== null) {
            $data['instance'] = $this->instance;
        }

        return array_merge($data, $this->extensions);
    }

    public function getStatus(): int
    {
        return $this->status;
    }

    // -- Factory methods for common error types --

    public static function notFound(string $detail = 'The requested resource was not found.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/404',
            title: 'Not Found',
            status: 404,
            detail: $detail,
        );
    }

    public static function validationFailed(array $errors, string $detail = 'Validation failed.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/422',
            title: 'Unprocessable Entity',
            status: 422,
            detail: $detail,
            extensions: ['errors' => $errors],
        );
    }

    public static function unauthorized(string $detail = 'Authentication is required.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/401',
            title: 'Unauthorized',
            status: 401,
            detail: $detail,
        );
    }

    public static function forbidden(string $detail = 'You do not have permission.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/403',
            title: 'Forbidden',
            status: 403,
            detail: $detail,
        );
    }

    public static function tooManyRequests(int $retryAfter, string $detail = 'Rate limit exceeded.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/429',
            title: 'Too Many Requests',
            status: 429,
            detail: $detail,
            extensions: ['retry_after' => $retryAfter],
        );
    }

    public static function internal(string $detail = 'An unexpected error occurred.'): self
    {
        return new self(
            type: 'https://httpproblems.com/http-status/500',
            title: 'Internal Server Error',
            status: 500,
            detail: $detail,
        );
    }
}

// -- Laravel usage in a controller: ----------------------------------------
public function show(string $id): JsonResponse
{
    $event = Event::find($id);

    if (! $event) {
        $problem = ProblemDetails::notFound("Event #{$id} does not exist.");

        return response()->json($problem, $problem->getStatus())
            ->header('Content-Type', 'application/problem+json');
    }

    return new EventResource($event);
}
```

---

## Pattern 9: Cursor-Based Pagination

Cursor-based pagination avoids the performance problems of `OFFSET` on large datasets and provides stable page boundaries when records are inserted or deleted between requests.

```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\EventResource;
use App\Models\Event;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class EventController extends Controller
{
    public function feed(Request $request): JsonResponse
    {
        $request->validate([
            'limit'     => ['integer', 'min:1', 'max:100'],
            'cursor'    => ['nullable', 'string'],
            'direction' => ['in:next,prev'],
        ]);

        $limit     = (int) $request->query('limit', '20');
        $cursor    = $request->query('cursor');
        $direction = $request->query('direction', 'next');

        $query = Event::query()
            ->where('status', 'published')
            ->with('organizer');

        // Apply cursor filter
        if ($cursor) {
            $decoded = json_decode(base64_decode($cursor, true), true);

            if (is_array($decoded) && isset($decoded['id'], $decoded['starts_at'])) {
                $op = $direction === 'next' ? '<' : '>';

                $query->where(function ($q) use ($decoded, $op) {
                    $q->where('starts_at', $op, $decoded['starts_at'])
                      ->orWhere(function ($q2) use ($decoded, $op) {
                          $q2->where('starts_at', '=', $decoded['starts_at'])
                             ->where('id', $op, $decoded['id']);
                      });
                });
            }
        }

        $order = $direction === 'next' ? 'desc' : 'asc';
        $events = $query
            ->orderBy('starts_at', $order)
            ->orderBy('id', $order)
            ->limit($limit + 1)
            ->get();

        $hasMore = $events->count() > $limit;
        if ($hasMore) {
            $events->pop();
        }

        if ($direction === 'prev') {
            $events = $events->reverse()->values();
        }

        // Build cursors
        $nextCursor = null;
        $prevCursor = null;

        if ($hasMore && $events->isNotEmpty()) {
            $last = $events->last();
            $nextCursor = base64_encode(json_encode([
                'id'        => $last->id,
                'starts_at' => $last->starts_at->toIso8601String(),
            ]));
        }

        if ($events->isNotEmpty() && $cursor) {
            $first = $events->first();
            $prevCursor = base64_encode(json_encode([
                'id'        => $first->id,
                'starts_at' => $first->starts_at->toIso8601String(),
            ]));
        }

        return response()->json([
            'data'    => EventResource::collection($events),
            'cursors' => [
                'next' => $nextCursor,
                'prev' => $prevCursor,
            ],
            'meta' => [
                'has_more' => $hasMore,
                'count'    => $events->count(),
            ],
        ]);
    }
}

// Route registration:
Route::get('/v1/feed', [EventController::class, 'feed'])->name('api.v1.feed');
```

---

## Best Practices Summary

1. **Use API Resources** instead of returning models directly. Resources decouple your API shape from your database schema and give you conditional attributes via `when()` and `whenLoaded()`.
2. **Scope Sanctum tokens with abilities.** Never issue tokens with full access when specific abilities suffice. Check abilities with `tokenCan()` in controllers.
3. **Rate limit every endpoint.** Public endpoints need aggressive limits; authenticated endpoints need per-user limits. Use tiered limits for different subscription plans.
4. **Format errors consistently** using RFC 7807 Problem Details. Consumers should be able to parse every error response with the same code.
5. **Make webhook receivers fast and idempotent.** Validate the signature, check idempotency, dispatch to a queue, and return 200 immediately. Never do heavy processing synchronously.
6. **Use cursor-based pagination for feeds and large datasets.** Offset-based pagination degrades as page numbers increase and produces inconsistent results when records change between requests.
7. **Version your API namespace** (e.g., `/api/v1/`). When breaking changes are needed, introduce `v2` and run both versions until consumers migrate.
8. **Return proper HTTP status codes.** 200 for success, 201 for creation (with `Location` header), 204 for no-content, 4xx for client errors, 5xx for server errors.
9. **Set cache headers** on read endpoints. Use `Cache-Control`, `ETag`, or `Last-Modified` to reduce unnecessary traffic.
10. **Validate at the boundary.** Use Form Request validation or `$request->validate()` before business logic runs. Never trust input that reaches your service layer.
