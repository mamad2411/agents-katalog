---
name: moonshine-advanced-v4
description: Use when working on MoonShine v4 custom controllers, handlers, routes, type casts, notifications, toasts, testing, package development, CrudResource, JsonResponse, AsyncMethod, or recipe patterns.
---

# MoonShine v4 Advanced Topics

## Custom Controllers

MoonShine provides a base `MoonShineController` with helper methods for views, toasts, notifications, and JSON responses. Inheriting from it is optional but convenient.

### Generate a Controller

```shell
php artisan moonshine:controller CustomController
```

Creates a controller in `app/MoonShine/Controllers/`.

### Show a Blade View Inside MoonShine Layout

```php
use MoonShine\Contracts\Core\PageContract;
use MoonShine\Laravel\Http\Controllers\MoonShineController;

final class CustomViewController extends MoonShineController
{
    public function __invoke(): PageContract
    {
        return $this->view('path_to_blade', ['param' => 'value']);
    }
}
```

### Return a MoonShine Page Directly

```php
use App\MoonShine\Pages\MyPage;
use MoonShine\Laravel\Http\Controllers\MoonShineController;

final class CustomViewController extends MoonShineController
{
    public function __invoke(MyPage $page): MyPage
    {
        return $page;
    }
}
```

### Toast, Notification, and JSON Helpers

```php
// Toast notification (v4 uses toast() helper)
$this->toast('Hello world', ToastType::SUCCESS);
return back();

// Send persistent notification to notification center
$this->notification('Message');
return back();

// JSON response with message + optional redirect
return $this->json(message: 'Saved', data: [], redirect: '/url');
```

### Access Page or Resource from Request

```php
use MoonShine\Contracts\Core\DependencyInjection\CrudRequestContract;

public function __invoke(CrudRequestContract $request)
{
    $page = $request->getPage();
    $resource = $request->getResource();
}
```

> See `references/controllers-routes.md` for full controller and route examples.

---

## Handlers (Handler)

Handlers are reusable action classes that automatically generate UI buttons on resource index pages. They do not require separate controllers.

**V4 CHANGE**: The base class is now `MoonShine\Crud\Handlers\Handler` (imported from Crud package). The toast helper is `toast()` instead of `MoonShineUI::toast()`.

### Generate a Handler

```shell
php artisan moonshine:handler MyCustomHandler
```

### Handler Structure

```php
use MoonShine\Contracts\UI\ActionButtonContract;
use MoonShine\Crud\Handlers\Handler;
use MoonShine\UI\Components\ActionButton;
use MoonShine\UI\Exceptions\ActionButtonException;
use Symfony\Component\HttpFoundation\Response;

class MyCustomHandler extends Handler
{
    public function handle(): Response
    {
        if (! $this->hasResource()) {
            throw new ActionButtonException('Resource is required for action');
        }

        if ($this->isQueue()) {
            toast(__('moonshine::ui.resource.queued'));
            return back();
        }

        self::process();
        return back();
    }

    public static function process()
    {
        // Your logic here
    }

    public function getButton(): ActionButtonContract
    {
        return ActionButton::make($this->getLabel(), $this->getUrl());
    }
}
```

### Register in IndexPage

```php
use MoonShine\Support\ListOf;
use MoonShine\Laravel\Pages\Crud\IndexPage;

class PostIndexPage extends IndexPage
{
    protected function handlers(): ListOf
    {
        return parent::handlers()->add(new MyCustomHandler());
    }
}
```

Handler capabilities: access resource via `$this->getResource()`, queue support via `isQueue()`, notification recipients via `notifyUsers()`, button customization via `modifyButton()`.

> See `references/handlers.md` for import/export handler examples.

---

## Custom Routes

MoonShine uses standard Laravel routing. The `Route::moonshine()` directive simplifies route registration with proper middleware and parameter prefixes.

```php
// In routes/moonshine.php
Route::moonshine(static function (Router $router) {
    $router->post('permissions/{resourceItem}', PermissionController::class)
        ->name('permissions');
}, withResource: true, withPage: true, withAuthenticate: true);
```

Result: `POST /admin/resource/{resourceUri}/{pageUri}/permissions/{resourceItem}` with `moonshine` + `Authenticate` middleware.

Get route from resource context:

```php
$this->getRoute('permissions')
```

Get route outside resource:

```php
route('moonshine.permissions', ['resourceUri' => 'user-resource', 'pageUri' => 'custom-page'])
```

> WARNING: Do not use `web` and `moonshine` middleware groups simultaneously -- they start sessions at the same time.

> See `references/controllers-routes.md` for full route definitions and middleware options.

---

## Type Casts

Fields work with primitive types by default. TypeCasts bridge typed data (models, DTOs) to MoonShine components.

Implement `DataCasterContract` and `DataWrapperContract`:

```php
interface DataCasterContract
{
    public function cast(mixed $data): DataWrapperContract;
    public function paginatorCast(mixed $data): ?PaginatorContract;
}

interface DataWrapperContract
{
    public function getOriginal(): mixed;
    public function getKey(): int|string|null;
    public function toArray(): array;
}
```

Usage with FormBuilder/TableBuilder:

```php
TableBuilder::make(items: User::paginate())
    ->fields([Text::make('Email')])
    ->cast(new ModelCaster(User::class));

FormBuilder::make()
    ->fields([Text::make('Email')])
    ->fillCast(User::query()->first(), new ModelCaster(User::class));
```

Generate a custom TypeCast:

```shell
php artisan moonshine:type-cast MyCustomCaster
```

> See `references/typecasts-packages.md` for full implementation examples.

---

## CrudResource (Non-Eloquent Data)

`CrudResource` lets you work with any data source -- APIs, files, custom databases -- without Eloquent. Located at `MoonShine\Crud\Resources\CrudResource`.

### Abstract Methods to Implement

```php
use MoonShine\Contracts\Core\DependencyInjection\FieldsContract;
use MoonShine\Contracts\Core\TypeCasts\DataWrapperContract;
use MoonShine\Crud\Resources\CrudResource;

final class RestCrudResource extends CrudResource
{
    public function findItem(bool $orFail = false): ?DataWrapperContract { /* ... */ }
    public function getItems(): iterable { /* ... */ }
    public function massDelete(array $ids): void { /* ... */ }
    public function delete(DataWrapperContract $item, ?FieldsContract $fields = null): bool { /* ... */ }
    public function save(DataWrapperContract $item, ?FieldsContract $fields = null): DataWrapperContract { /* ... */ }
}
```

Key differences from v3: methods now accept/return `DataWrapperContract` instead of `mixed`. Use `$this->getCaster()->cast($data)` to wrap raw data.

For maximum flexibility, implement `CrudResourceContract` directly.

> See `references/typecasts-packages.md` for full REST API resource example.

---

## JsonResponse

**V4 CHANGE**: `MoonShineJsonResponse` renamed to `JsonResponse` at `MoonShine\Crud\JsonResponse`.

```php
use MoonShine\Crud\JsonResponse;
use MoonShine\Support\Enums\ToastType;

// Toast
JsonResponse::make()->toast('Message', ToastType::SUCCESS, duration: 3000);

// Redirect
JsonResponse::make()->redirect('/dashboard');

// Trigger JS events
JsonResponse::make()->events([AlpineJs::event(JsEvent::TABLE_UPDATED, 'index')]);

// Insert HTML into a selector
JsonResponse::make()->html('Content');

// Multiple selectors
JsonResponse::make()
    ->htmlData((string) Text::make('One'), '#selector1')
    ->htmlData((string) Text::make('Two'), '#selector2', HtmlMode::BEFORE_END);

// Set field values by CSS selector
JsonResponse::make()->fieldsValues([
    '.field-title-1' => 'some value 1',
    '.field-title-2' => 'some value 2',
]);

// Merge additional data (useful for async Select options)
JsonResponse::make()->merge(['options' => $options]);
```

> See `references/typecasts-packages.md` for detailed method reference.

---

## Notifications

**V4 CHANGE**: `NotificationButton` moved to `MoonShine\Crud\Notifications\NotificationButton`.

```php
use MoonShine\Laravel\Notifications\MoonShineNotification;
use MoonShine\Crud\Notifications\NotificationButton;
use MoonShine\Support\Enums\Color;

MoonShineNotification::send(
    message: 'Notification text',
    button: new NotificationButton('Click me', 'https://example.com', attributes: ['target' => '_blank']),
    ids: [1, 2, 3],       // admin user IDs (null = all)
    color: Color::GREEN,
    icon: 'information-circle'
);
```

Or via DI:

```php
use MoonShine\Crud\Contracts\Notifications\MoonShineNotificationContract;

public function di(MoonShineNotificationContract $notification)
{
    $notification->notify('Hello');
}
```

Configuration in `config/moonshine.php`:

```php
'use_notifications' => true,
'use_database_notifications' => true,
```

---

## Toasts

**V4 CHANGE**: `MoonShineUI::toast()` replaced by the global `toast()` helper function.

```php
use MoonShine\Support\Enums\ToastType;

// Basic toast
toast(message: 'Hello');

// With type and duration
toast(message: 'Success', type: ToastType::SUCCESS, duration: 3000);

// Sticky toast (stays until clicked)
toast(message: 'Sticky toast', duration: false);
```

Types: `ToastType::DEFAULT`, `ToastType::SUCCESS`, `ToastType::INFO`, `ToastType::WARNING`, `ToastType::ERROR`.

Via JsonResponse:

```php
JsonResponse::make()->toast('Test', type: ToastType::SUCCESS, duration: 1000);
```

Via JS event:

```php
ActionButton::make('Toast')->dispatchEvent(
    AlpineJs::event(JsEvent::TOAST, params: ToastEventParams::make(ToastType::SUCCESS, 'Hello', duration: 2000))
);
```

Global JS override: `MoonShine.config().setToastDuration(5000);`

---

## Testing

### Generate Tests with Resources

```shell
php artisan moonshine:resource PostResource --test   # PHPUnit
php artisan moonshine:resource PostResource --pest   # Pest
```

### Test Setup

```php
protected function setUp(): void
{
    parent::setUp();
    $user = MoonshineUser::factory()->create();
    $this->be($user, 'moonshine');
}

public function test_index_page_successful(): void
{
    $response = $this->get(
        $this->getResource()->getIndexPageUrl()
    )->assertSuccessful();
}
```

> See `references/testing.md` for complete test examples and assertions.

---

## Package Development

Through your package's `ServiceProvider`, you can add resources, pages, create menus, and authorization rules.

```php
use Illuminate\Support\ServiceProvider;
use MoonShine\Contracts\Core\DependencyInjection\CoreContract;
use MoonShine\Laravel\DependencyInjection\MoonShine;

class MyPackageServiceProvider extends ServiceProvider
{
    /** @param MoonShine $core */
    public function boot(CoreContract $core): void
    {
        $core
            ->resources([MyPackageResource::class])
            ->pages([MyPackagePage::class]);
    }
}
```

Key capabilities: MenuManager interaction, AssetManager for CSS/JS, ColorManager for theming, authorizationRules for access control, pushComponent for page injection.

> See `references/typecasts-packages.md` for full package development guide.

---

## AsyncMethod (NEW in v4)

The `#[AsyncMethod]` attribute allows defining async endpoints directly on resources or pages without creating separate controllers. Supports dependency injection.

```php
use MoonShine\Support\Attributes\AsyncMethod;
use MoonShine\Contracts\Core\DependencyInjection\CrudRequestContract;
use MoonShine\Crud\JsonResponse;

#[AsyncMethod]
public function myAction(CrudRequestContract $request): JsonResponse
{
    // Process async request with full DI support
    return JsonResponse::make()->toast('Done', ToastType::SUCCESS);
}
```

Usage: `FormBuilder::make()->asyncMethod('myAction', events: [...])` or `ActionButton::make('Run')->method('myAction')`.

Get URL: `$this->getAsyncMethodUrl('myAction')` or `$this->getResource()->getAsyncMethodUrl('myAction')`.

---

## Localization

After installing MoonShine, translations appear in `lang/vendor/moonshine`. Default language is English.

### Configuration

```php
// config/moonshine.php
'locale' => 'en',
'locales' => ['en', 'ru'],

// Or in MoonShineServiceProvider
$config->locale('en');
$config->locales(['en', 'ru']);
```

Language switching is handled by `MoonShine\Laravel\Http\Middleware\ChangeLocale`. Selection saved in session takes precedence over config.

Third-party localization package: `laravel-lang/moonshine`.

---

## Recipes Overview

Practical patterns for common MoonShine tasks. Full code in reference files:

- **recipes-dashboard.md** — Async metrics, dashboard settings, custom profile, menu authorization, breadcrumbs
- **recipes-resources.md** — Soft deletes, reorderable rows, HasMany parent ID, updateOnPreview pivot
- **recipes-forms-tables.md** — Form events, field logic, fields group, mass edit, config saving, select patterns
- **recipes-ui-other.md** — Index cards, Template field, tabs, paginator, fragments, async remove

---

## Cross-References

- **references/controllers-routes.md** — Controllers, routes, middleware, JSON responses
- **references/handlers.md** — Handler creation, import/export, IndexPage registration
- **references/typecasts-packages.md** — TypeCast, CrudResource, JsonResponse, packages, notifications, toasts
- **references/testing.md** — Test setup, resource/page testing, assertions
- **moonshine-resources-v4** — ModelResource, query scopes, filters, actions
- **moonshine-setup-v4** — Artisan commands reference
- **moonshine-components-v4** — FormBuilder, TableBuilder, CardsBuilder, Fragment, ActionButton
