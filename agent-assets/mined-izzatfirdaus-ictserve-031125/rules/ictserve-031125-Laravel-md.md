---
applyTo:
  - '**/*.php'
  - 'routes/**'
  - 'database/**'
  - 'config/**'
  - 'bootstrap/**'
  - 'app/**'
description: |
  Laravel 12 development standards for ICTServe project.
  Enforces Artisan workflows, Eloquent patterns, Service Container usage,
  PSR-12 compliance, and Laravel 12 best practices for AI code generation.
tags:
  - laravel
  - php
  - eloquent
  - artisan
  - testing
version: '1.1.0'
lastUpdated: '2025-02-24'
---

# Laravel 12 Development Standards

## Overview

This rule defines Laravel 12 (February 2025) conventions and best practices for the ICTServe project. Follow these standards for all PHP backend development.

| Property | Value |
| :--- | :--- |
| **Framework** | Laravel 12.x |
| **PHP Version** | 8.2 - 8.4 |
| **Applies To** | Application layer, routing, database, configuration, bootstrap |

## Core Principles

1. **Laravel Way First** — Use framework conventions before custom solutions.
2. **Artisan-Driven** — Generate files via `php artisan make:*` commands.
3. **Dependency Injection** — Use constructor injection over facades.
4. **Eloquent ORM** — Prefer relationships over raw SQL.
5. **PSR-12 Compliance** — Follow PHP-FIG standards (Laravel Pint).

## Laravel 12 Key Changes

| Change | Description |
| :--- | :--- |
| No `app/Http/Kernel.php` | Use `bootstrap/app.php`. |
| No `app/Console/Kernel.php` | Commands auto-register from `app/Console/Commands/`. |
| No middleware directory | Define middleware inline in `bootstrap/app.php`. |
| Service providers | Stored in `bootstrap/providers.php` (auto-discovery). |
| Attribute-based observers | Use `#[ObservedBy]` attribute. |
| Attribute-based scopes | Use `#[ScopedBy]` and `#[Scope]` attributes. |
| UUID/ULID support | Via `HasUuids` / `HasUlids` traits. |

## Bootstrap Configuration

Register middleware, exceptions, and routing in `bootstrap/app.php`:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
    )
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->web(append: [
            \App\Http\Middleware\HandleInertiaRequests::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->reportable(function (Throwable $e) {
            // Custom error handling
        });
    })->create();
````

## Artisan Command Patterns

Always use `--no-interaction` for CI/CD automation.

### Common Generation Commands

```bash
# Model with factory, seeder, migration
php artisan make:model Asset --all --no-interaction

# Controller with resource methods
php artisan make:controller AssetController --resource --no-interaction

# Form Request for validation
php artisan make:request StoreAssetRequest --no-interaction

# Policy for authorization
php artisan make:policy AssetPolicy --model=Asset --no-interaction

# Migration with specific table action
php artisan make:migration add_status_to_assets_table --no-interaction

# Job with queue
php artisan make:job ProcessAssetBorrowing --queued --no-interaction

# Observer for model events
php artisan make:observer AssetObserver --model=Asset --no-interaction

# Scope for query constraints
php artisan make:scope AncientScope --no-interaction
```

### Utility Commands

```bash
php artisan list              # All commands
php artisan make:model --help # Specific command options
php artisan model:show Flight # Shows attributes, relationships, observers, scopes
```

## Eloquent Model Standards

### Complete Model Example

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Asset extends Model
{
    use SoftDeletes;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<string>
     */
    protected $fillable = [
        'name',
        'asset_tag',
        'category_id',
        'status',
        'acquired_date',
    ];

    /**
     * The model's default values for attributes.
     *
     * @var array<string, mixed>
     */
    protected $attributes = [
        'status' => 'available',
    ];

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'acquired_date' => 'date',
            'created_at' => 'datetime',
            'updated_at' => 'datetime',
            'deleted_at' => 'datetime',
        ];
    }

    /**
     * Get the category that owns the asset.
     */
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    /**
     * Get the borrowing records for the asset.
     */
    public function borrowings(): HasMany
    {
        return $this->hasMany(Borrowing::class);
    }
}
```

### Model Requirements Checklist

| Requirement | Description |
| :--- | :--- |
| Strict types | `declare(strict_types=1)` at file start |
| Casts method | Use `protected function casts(): array` (NOT property) |
| Return types | Explicit return type hints for relationships |
| PHPDoc blocks | Document array shapes and method descriptions |
| Soft deletes | Use `SoftDeletes` trait for logical deletion |
| Observers | Use `#[ObservedBy]` attribute (not boot method) |
| Global scopes | Use `#[ScopedBy]` attribute (not boot method) |

### UUID and ULID Primary Keys

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;

class Article extends Model
{
    use HasUuids;

    /**
     * Get the columns that should receive a unique identifier.
     *
     * @return array<int, string>
     */
    public function uniqueIds(): array
    {
        return ['id', 'discount_code'];
    }
}
```

For ULIDs (26 character, lexicographically sortable):

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;

class Article extends Model
{
    use HasUlids;
}
```

### Model Configuration

```php
use Illuminate\Database\Eloquent\Model;

public function boot(): void
{
    parent::boot();

    // Prevent lazy loading in development
    Model::preventLazyLoading(!$this->app->isProduction());

    // Throw exception when filling unfillable attributes
    Model::preventSilentlyDiscardingAttributes(!$this->app->isProduction());
}
```

### Model Pruning

```php
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->subMonth());
    }

    /**
     * Prepare the model for pruning.
     */
    protected function pruning(): void
    {
        // Delete associated files before pruning
    }
}
```

Schedule pruning in `routes/console.php`:

```php
Schedule::command('model:prune')->daily();
```

## Query Scopes

### Global Scopes with Attributes

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy(AncientScope::class)]
class User extends Model
{
    //
}

class AncientScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

### Local Scopes with Attributes

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Attributes\Scope;

class User extends Model
{
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }

    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

Usage:

```php
$users = User::popular()->active()->get();
$users = User::ofType('admin')->get();
```

### Pending Attributes

Scopes with default values:

```php
#[Scope]
public function draft(Builder $query): PendingAttributes
{
    return $query->where('status', 'draft')
        ->withAttributes([
            'hidden' => true,
        ]);
}

// Usage
$draft = Post::draft()->create(['title' => 'In Progress']);
// $draft->hidden will be true
```

## Database Migrations

### Migration Rules

* Always include rollback logic in `down()` method.
* When modifying columns, include ALL previous attributes (or they are lost).
* Use Laravel's column modifiers (nullable, default, index, unique).
* Never use raw SQL unless absolutely necessary.

### Creating Tables

```php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('assets', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('asset_tag')->unique();
            $table->foreignId('category_id')->constrained()->cascadeOnDelete();
            $table->enum('status', ['available', 'borrowed', 'maintenance', 'retired'])
                ->default('available');
            $table->date('acquired_date');
            $table->timestamps();
            $table->softDeletes();

            $table->index(['status', 'category_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('assets');
    }
};
```

### Modifying Columns

```php
public function up(): void
{
    Schema::table('assets', function (Blueprint $table) {
        $table->string('asset_tag', 100)->unique()->nullable(false)->change();
    });
}
```

## Routing Conventions

### Web Routes

```php
use App\Http\Controllers\AssetController;
use Illuminate\Support\Facades\Route;

Route::middleware(['auth'])->group(function () {
    Route::resource('assets', AssetController::class)->names('assets');

    Route::post('assets/{asset}/borrow', [AssetController::class, 'borrow'])
        ->name('assets.borrow');
});
```

### API Routes

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('assets', AssetController::class);
});
```

### Route Model Binding

Routes automatically resolve model parameters:

```php
public function borrow(Asset $asset, User $user): Borrowing
{
    $borrowing = $this->assetRepository->createBorrowing($asset, $user);
    $this->auditLogger->log('asset.borrowed', $borrowing);

    return $borrowing;
}
```

## Service Provider Bindings

In `app/Providers/AppServiceProvider.php`:

```php
public function register(): void
{
    $this->app->singleton(AssetBorrowingService::class);
    $this->app->bind(AssetRepositoryInterface::class, EloquentAssetRepository::class);
}
```

## Form Request Validation

### Form Request Class

```php
namespace App\Http\Requests;

use App\Models\Asset;
use Illuminate\Foundation\Http\FormRequest;

class StoreAssetRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Asset::class);
    }

    /**
     * @return array<string, array<int, string>>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'asset_tag' => ['required', 'string', 'unique:assets,asset_tag'],
            'category_id' => ['required', 'exists:categories,id'],
            'status' => ['required', 'in:available,borrowed,maintenance,retired'],
            'acquired_date' => ['required', 'date', 'before_or_equal:today'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'asset_tag.unique' => 'This asset code already exists in the system.',
            'acquired_date.before_or_equal' => 'Acquisition date cannot be in the future.',
        ];
    }
}
```

### Controller Usage

```php
public function store(StoreAssetRequest $request): RedirectResponse
{
    $asset = Asset::create($request->validated());

    return redirect()->route('assets.show', $asset)
        ->with('success', 'Asset successfully added.');
}
```

## Query Optimization

### Preventing N+1 Queries

```php
// BAD: N+1 query problem
$assets = Asset::all();
foreach ($assets as $asset) {
    echo $asset->category->name; // Fires 1 query per asset
}

// GOOD: Eager loading
$assets = Asset::with('category')->get();
foreach ($assets as $asset) {
    echo $asset->category->name; // Only 2 queries total
}

// BETTER: Constrained eager loading
$assets = Asset::with([
    'borrowings' => fn($query) => $query->latest()->limit(5)
])->get();
```

### Using Query Scopes

```php
#[Scope]
protected function available(Builder $query): void
{
    $query->where('status', 'available');
}

#[Scope]
protected function byCategory(Builder $query, int $categoryId): void
{
    $query->where('category_id', $categoryId);
}

// Usage
$assets = Asset::available()->byCategory(3)->get();
```

## Configuration Best Practices

Never use `env()` outside `config/` files:

```php
// config/external-api.php
return [
    'api' => [
        'key' => env('EXTERNAL_API_KEY'),
        'url' => env('EXTERNAL_API_URL', '[https://api.example.com](https://api.example.com)'),
        'timeout' => env('EXTERNAL_API_TIMEOUT', 30),
    ],
];
```

## Queue and Job Patterns

### Creating a Queued Job

```php
namespace App\Jobs;

use App\Models\Asset;
use App\Models\User;
use App\Notifications\AssetBorrowedNotification;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class SendAssetBorrowedNotification implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        private Asset $asset,
        private User $borrower
    ) {}

    public function handle(): void
    {
        $this->borrower->notify(new AssetBorrowedNotification($this->asset));
    }

    public function failed(\Throwable $exception): void
    {
        Log::error('Failed to send asset borrowed notification', [
            'asset_id' => $this->asset->id,
            'borrower_id' => $this->borrower->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

### Dispatching Jobs

```php
// Dispatch immediately
SendAssetBorrowedNotification::dispatch($asset, $user);

// Dispatch with delay
SendAssetBorrowedNotification::dispatch($asset, $user)
    ->delay(now()->addMinutes(5));

// On specific queue
SendAssetBorrowedNotification::dispatch($asset, $user)
    ->onQueue('notifications');
```

## Testing Standards

### Feature Test Example

```php
namespace Tests\Feature;

use App\Models\Asset;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AssetBorrowingTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_borrow_available_asset(): void
    {
        $user = User::factory()->create();
        $asset = Asset::factory()->create(['status' => 'available']);

        $response = $this->actingAs($user)
            ->post(route('assets.borrow', $asset));

        $response->assertRedirect();
        $this->assertDatabaseHas('borrowings', [
            'asset_id' => $asset->id,
            'user_id' => $user->id,
        ]);
    }

    public function test_user_cannot_borrow_unavailable_asset(): void
    {
        $user = User::factory()->create();
        $asset = Asset::factory()->create(['status' => 'borrowed']);

        $response = $this->actingAs($user)
            ->post(route('assets.borrow', $asset));

        $response->assertForbidden();
    }
}
```

### Running Tests

```bash
php artisan test                                       # All tests
php artisan test --filter=AssetBorrowingTest          # Specific class
php artisan test tests/Feature/AssetBorrowingTest.php # Specific file
php artisan test --parallel                            # Parallel execution
```

## URL Generation

Always use named routes:

```blade
{{-- BAD: Hard-coded URLs --}}
<a href="/assets/{{ $asset->id }}">View Asset</a>

{{-- GOOD: Named route helper --}}
<a href="{{ route('assets.show', $asset) }}">View Asset</a>

{{-- GOOD: In controllers --}}
return redirect()->route('assets.index');
```

## Authentication and Authorization

### Gates

For simple authorization checks:

```php
Gate::define('view-admin-panel', function (User $user) {
    return $user->hasRole('admin');
});

// Usage
if (Gate::allows('view-admin-panel')) {
    // User has access
}
```

### Policies

For model-specific authorization:

```php
public function update(User $user, Asset $asset): bool
{
    return $user->id === $asset->created_by || $user->hasRole('admin');
}

// Usage in controller
$this->authorize('update', $asset);
```

## Error Handling

Configure custom exception handling in `bootstrap/app.php`:

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->reportable(function (AssetNotFoundException $e) {
        Log::warning('Asset not found', ['asset_id' => $e->assetId]);
    });

    $exceptions->renderable(function (AssetNotFoundException $e, Request $request) {
        if ($request->expectsJson()) {
            return response()->json(['error' => 'Asset not found'], 404);
        }
        return response()->view('errors.asset-not-found', [], 404);
    });
})
```

## Laravel 12 Starter Kits

### Available Options

| Kit | Stack |
| :--- | :--- |
| React | Inertia 2, TypeScript, shadcn/ui |
| Vue | Inertia 2, TypeScript, shadcn/ui |
| Livewire | Flux UI, Volt |
| WorkOS AuthKit | Variant |

All starter kits support WorkOS AuthKit with:

* Social authentication.
* Passkeys support.
* SSO (Single Sign-On).
* Free up to 1 million monthly active users.

### Installation

```bash
laravel new my-app
# Choose starter kit during installation
```

> **Note**: Laravel Breeze and Jetstream will no longer receive additional updates. Use the new starter kits instead.

## Laravel Boost and AI Integration

Laravel Boost bridges AI coding agents and Laravel applications.

### Features

* 15+ specialized tools (database queries, Tinker, documentation search).
* 17,000+ vectorized Laravel ecosystem documentation pieces (version-specific).
* Laravel-maintained AI guidelines.
* Automatic package version detection.

### Installation

```bash
composer require laravel/boost --dev
php artisan boost:install
```

### IDE Support

| IDE | Extension |
| :--- | :--- |
| **VS Code / Cursor** | Laravel VS Code Extension |
| **PhpStorm** | Laravel Idea plugin |
| **Cloud IDE** | Firebase Studio |

## Common Anti-Patterns

### Using DB Facade Instead of Eloquent

```php
// BAD
$assets = DB::table('assets')->where('status', 'available')->get();

// GOOD
$assets = Asset::where('status', 'available')->get();
```

### N+1 Query Problems

```php
// BAD
foreach ($assets as $asset) {
    echo $asset->category->name; // N+1
}

// GOOD
$assets = Asset::with('category')->get();
```

### Missing Authorization Checks

```php
// BAD
public function update(Request $request, Asset $asset)
{
    $asset->update($request->all());
}

// GOOD
public function update(UpdateAssetRequest $request, Asset $asset)
{
    $this->authorize('update', $asset);
    $asset->update($request->validated());
}
```

### Using env() Outside Config Files

```php
// BAD
$apiKey = env('API_KEY');

// GOOD
$apiKey = config('services.api.key');
```

### Hard-Coded URLs

```php
// BAD
return redirect('/assets/' . $asset->id);

// GOOD
return redirect()->route('assets.show', $asset);
```

## References and Resources

| Resource | URL |
| :--- | :--- |
| Official Laravel 12 Docs | [https://laravel.com/docs/12.x](https://laravel.com/docs/12.x) |
| Release Notes | [https://laravel.com/docs/12.x/releases](https://laravel.com/docs/12.x/releases) |
| Starter Kits | [https://laravel.com/docs/12.x/starter-kits](https://laravel.com/docs/12.x/starter-kits) |
| Laravel News | [https://laravel-news.com](https://laravel-news.com) |
| Laracasts | [https://laracasts.com](https://laracasts.com) |
| Laravel Boost | [https://laravel.com/docs/12.x/boost](https://laravel.com/docs/12.x/boost) |
| Standards | PSR-12 (Code Style), Semantic Versioning |

## Compliance Checklist

When generating Laravel code, ensure:

* [ ] `declare(strict_types=1);` at file start.
* [ ] Type hints on all parameters and return types.
* [ ] PHPDoc blocks for arrays and complex types.
* [ ] Use `protected function casts(): array` (not `$casts` property).
* [ ] Named routes for all URL generation.
* [ ] Form Request classes for validation.
* [ ] Eager loading to prevent N+1 queries.
* [ ] Authorization checks via policies.
* [ ] Queue jobs for async operations.
* [ ] Comprehensive tests with RefreshDatabase.

| Property | Value |
| :--- | :--- |
| **Status** | Active for ICTServe Laravel 12 development |
| **Version** | 1.1.0 |
| **Last Updated** | 2025-02-24 |
