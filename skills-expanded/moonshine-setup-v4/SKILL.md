---
name: moonshine-setup-v4
description: Use when working on MoonShine v4 installation, configuration, bootstrapping, routing, middleware, localization, artisan commands, project structure, IDE setup, or v3→v4 migration.
---

# MoonShine v4 Setup

## Requirements

- PHP 8.2+
- Laravel 10.48+
- Composer 2+

## Installation

### Step 1: Install via Composer

```shell
composer require moonshine/moonshine
```

### Step 2: Run the installer

```shell
php artisan moonshine:install
```

The installer will interactively prompt you to configure:

1. **Authentication** -- enable/disable the `middleware` that checks whether the user has access to the panel.
2. **Migrations** -- required for built-in user and role management (`moonshine_users`, `moonshine_user_roles` tables).
3. **Notifications** -- enable/disable the notification system; optionally use the database driver.
4. **Superuser** -- if migrations are enabled, create an initial admin user.

### Quick mode (non-interactive)

```shell
php artisan moonshine:install -Q
```

Accepts all defaults: authentication on, migrations on, notifications on, then prompts only for superuser credentials.

### Installer flags

| Flag | Short | Effect |
|------|-------|--------|
| `--quick-mode` | `-Q` | Accept all defaults, skip confirmations |
| `--without-auth` | `-a` | Disable built-in authentication |
| `--without-migrations` | `-m` | Skip system migrations |
| `--without-notifications` | `-d` | Disable notifications |
| `--without-user` | `-u` | Skip superuser creation |
| `--default-layout` | `-l` | Use default (non-compact) layout |
| `--tests-mode` | `-t` | For automated testing |

### Starter kit (single command)

If you have `laravel/installer` globally:

```shell
laravel new example-app --using=moonshine/app
```

## What the installer creates

| Path | Purpose |
|------|---------|
| `app/Providers/MoonShineServiceProvider.php` | Registers resources, pages, and global settings |
| `app/MoonShine/` | Main directory for resources, pages, and layouts |
| `app/MoonShine/Pages/Dashboard.php` | Default dashboard page |
| `app/MoonShine/Layouts/MoonShineLayout.php` | Default layout template |
| `app/MoonShine/Resources/` | Directory for model resources |
| `config/moonshine.php` | Configuration file |
| `lang/vendor/moonshine/` | Language files |
| `public/vendor/moonshine/` | Published assets |

The provider is automatically added to `bootstrap/providers.php`. A `storage:link` is also executed.

After installation, the admin panel is available at `/admin`.

## Project directory structure

```
app/
  MoonShine/
    Layouts/
      MoonShineLayout.php    # Page template (menu, header, sidebar)
    Pages/
      Dashboard.php          # Default landing page
    Resources/               # ModelResource classes for CRUD
  Providers/
    MoonShineServiceProvider.php
config/
  moonshine.php
lang/
  vendor/
    moonshine/               # Translation files
public/
  vendor/
    moonshine/               # Published frontend assets
```

## Configuration methods

MoonShine can be configured two ways. Provider configuration takes precedence over the config file.

### Via config/moonshine.php

```php
return [
    'title' => env('MOONSHINE_TITLE', 'MoonShine'),
    'logo' => 'vendor/moonshine/logo.svg',
    'logo_small' => 'vendor/moonshine/logo-small.svg',
    'use_migrations' => true,
    'use_notifications' => true,
    'use_database_notifications' => true,
    'use_routes' => true,
    'use_profile' => true,
    'prefix' => 'admin',
    'locale' => 'en',
    'auth' => [
        'enabled' => true,
        'guard' => 'moonshine',
    ],
    'layout' => \MoonShine\Laravel\Layouts\AppLayout::class,
    'palette' => \MoonShine\ColorManager\Palettes\PurplePalette::class,
];
```

You can keep only the keys that differ from defaults. See [references/config-options.md](references/config-options.md) and [references/config-auth-localization.md](references/config-auth-localization.md) for the full option reference.

### Via MoonShineServiceProvider

```php
use Illuminate\Support\ServiceProvider;
use MoonShine\Contracts\Core\DependencyInjection\CoreContract;
use MoonShine\Laravel\DependencyInjection\MoonShine;
use MoonShine\Laravel\DependencyInjection\MoonShineConfigurator;
use MoonShine\Contracts\Core\DependencyInjection\ConfiguratorContract;

class MoonShineServiceProvider extends ServiceProvider
{
    /**
     * @param  MoonShine  $core
     * @param  MoonShineConfigurator  $config
     */
    public function boot(
        CoreContract $core,
        ConfiguratorContract $config,
    ): void
    {
        $config
            ->title('My Application')
            ->logo('/assets/logo.png')
            ->logo('/assets/logo_small.png', true)
            ->useMigrations()
            ->useNotifications()
            ->useDatabaseNotifications()
            ->dir('app/MoonShine', 'App\MoonShine')
            ->locale('ru')
            ->locales(['en', 'ru'])
            ->guard('moonshine')
            ->authPipelines([])
            ->authorizationRules(
                function(ResourceContract $ctx, mixed $user, Ability $ability, mixed $data): bool {
                    return true;
                }
            )
            ->layout(\App\MoonShine\Layouts\CustomLayout::class)
            ->disk('public')
            ->cacheDriver('redis')
            ->homeRoute('moonshine.index')
            ->notFoundException(MoonShineNotFoundException::class);

        $core
            ->resources([...])
            ->pages([...]);
    }
}
```

> **Important**: Route-related configuration (`prefix`, `domain`, `page_prefix`, `resource_prefix`) must be set in `config/moonshine.php` because routes are loaded before the service provider's `boot` method runs.

> **Important**: `use_migrations`, `use_notifications`, and `use_database_notifications` must always be present in either `moonshine.php` or `MoonShineServiceProvider`.

## Key configuration areas

### Routing

```php
// config/moonshine.php
'domain' => env('MOONSHINE_DOMAIN'),          // e.g., 'admin.example.com'
'prefix' => env('MOONSHINE_ROUTE_PREFIX', 'admin'),
'page_prefix' => env('MOONSHINE_PAGE_PREFIX', 'page'),
'resource_prefix' => env('MOONSHINE_RESOURCE_PREFIX', 'resource'),
'home_route' => 'moonshine.index',
```

Resulting URL pattern: `/{prefix}/{resource_prefix}/{resourceUri}/{pageUri}`

### Authentication

```php
// config/moonshine.php
'auth' => [
    'enabled' => true,               // set false to disable built-in auth
    'guard' => 'moonshine',          // Laravel auth guard name
    'model' => MoonshineUser::class, // user model (config file only)
    'middleware' => [
        Authenticate::class,
    ],
    'pipelines' => [],               // e.g., [TwoFactor::class]
],

'user_fields' => [
    'username' => 'email',
    'password' => 'password',
    'name' => 'name',
    'avatar' => 'avatar',
],
```

To use your own User model, set `auth.model` in `config/moonshine.php` and adjust `user_fields` to match your column names.

### Localization

```php
// config/moonshine.php
'locale' => 'en',
'locales' => ['en', 'ru'],
'locale_key' => '_lang',  // query parameter name for locale switching
```

Language files are stored in `lang/vendor/moonshine/`. The `ChangeLocale` middleware handles locale switching automatically.

### Branding

```php
// In MoonShineServiceProvider
$config
    ->logo('/images/logo.png')
    ->logo('/images/logo-mini.png', small: true);

// Colors via palette class (v4 uses palette system)
// config/moonshine.php
'palette' => \MoonShine\ColorManager\Palettes\PurplePalette::class,

// Or custom palette
'palette' => \App\MoonShine\Palettes\CorporatePalette::class,
```

### Favicons

```php
// config/moonshine.php
'favicons' => [
    'apple-touch' => '/vendor/moonshine/apple-touch-icon.png',
    '32' => '/vendor/moonshine/favicon-32x32.png',
    '16' => '/vendor/moonshine/favicon-16x16.png',
    'safari-pinned-tab' => '/vendor/moonshine/safari-pinned-tab.svg',
],
```

## Artisan commands quick reference

| Command | Purpose |
|---------|---------|
| `php artisan moonshine:install` | Install MoonShine (run once) |
| `php artisan moonshine:install -Q` | Quick install with defaults |
| `php artisan moonshine:user` | Create an admin user |
| `php artisan moonshine:resource {Name}` | Generate a model resource with CRUD pages |
| `php artisan moonshine:page {Name}` | Generate a custom page |
| `php artisan moonshine:layout {Name}` | Generate a layout template |
| `php artisan moonshine:component {Name}` | Generate a custom component |
| `php artisan moonshine:field {Name}` | Generate a custom field |
| `php artisan moonshine:controller {Name}` | Generate a controller |
| `php artisan moonshine:handler {Name}` | Generate a handler class |
| `php artisan moonshine:policy` | Generate a policy for admin panel user |
| `php artisan moonshine:type-cast {Name}` | Generate a TypeCast class |
| `php artisan moonshine:apply {Name}` | Generate an apply class |
| `php artisan moonshine:publish` | Publish assets, templates, resources, forms, or pages |
| `php artisan moonshine:resources` | List all registered resources |
| `php artisan moonshine:pages` | List all registered standalone pages |

### Creating your first resource

```shell
php artisan moonshine:resource User
```

This generates a `UserResource` in `app/MoonShine/Resources/` with CRUD pages (`UserIndexPage`, `UserFormPage`, `UserDetailPage`) and automatically registers it. The resource is then accessible at:

```
http://127.0.0.1:8000/admin/resource/user-resource/user-index-page
```

## Replacing default pages and forms

```php
// config/moonshine.php
'pages' => [
    'dashboard' => \App\MoonShine\Pages\DashboardPage::class,
    'profile' => ProfilePage::class,
    'login' => LoginPage::class,
    'error' => ErrorPage::class,
],

'forms' => [
    'login' => LoginForm::class,
    'filters' => FiltersForm::class,
],
```

Retrieve pages and forms programmatically:

```php
$dashboard = moonshineConfig()->getPage('dashboard');
$loginForm = moonshineConfig()->getForm('login');
```

Or via dependency injection:

```php
use MoonShine\Contracts\Core\DependencyInjection\ConfiguratorContract;
use MoonShine\Laravel\DependencyInjection\MoonShineConfigurator;

/**
 * @param  MoonShineConfigurator  $config
 */
public function index(ConfiguratorContract $config)
{
    $page = $config->getPage('dashboard');
    $form = $config->getForm('login');
}
```

## IDE support

- **PhpStorm**: Install the [MoonShine plugin](https://plugins.jetbrains.com/plugin/28640-moonshine) for autocompletion and navigation.
- **PhpStorm alternative**: Install the [MetaStorm plugin](https://plugins.jetbrains.com/plugin/26121-metastorm/) for improved MoonShine autocompletion.

## MoonShine AI

For productive work with AI assistants, use the [FortyFive](https://github.com/moonshine-software/forty-five) package which provides additional context and tooling.

## v3 to v4 migration summary

### Auto upgrade tool

Use the [warete/moonshine-upgrade](https://github.com/warete/moonshine-upgrade) package to automatically apply most migration changes.

### Namespace changes

```php
// Old (v3)                                              // New (v4)
use MoonShine\Laravel\Forms\FiltersForm;              // use MoonShine\Crud\Forms\FiltersForm;
use MoonShine\Laravel\Forms\LoginForm;                // use MoonShine\Crud\Forms\LoginForm;
use MoonShine\Laravel\Http\Responses\MoonShineJsonResponse; // use MoonShine\Crud\JsonResponse;
use MoonShine\Laravel\MoonShineRequest;               // use MoonShine\Contracts\Core\DependencyInjection\CrudRequestContract;
use MoonShine\Laravel\Enums\Action;                   // use MoonShine\Support\Enums\Action;
use MoonShine\Laravel\Enums\Ability;                  // use MoonShine\Support\Enums\Ability;
use MoonShine\Laravel\Traits\WithComponentsPusher;    // use MoonShine\Crud\Traits\WithComponentsPusher;
```

### Resource restructuring (methods moved to pages)

Many resource methods moved to their corresponding CRUD pages in v4:

- `rules()`, `modifyFormComponent()` -- moved to form page class
- `metrics()`, `queryTags()`, `filters()`, `modifyListComponent()` -- moved to index page class
- `modifyDetailComponent()` -- moved to detail page class
- `indexButtons()` -- replaced by `buttons()` in index page class
- `topButtons()` -- replaced by `topLeftButtons()` and `topRightButtons()` in index page class
- `formButtons()` -- replaced by `buttons()` in form page class
- `formBuilderButtons()` -- replaced by `formButtons()` in form page class
- Properties `$clickAction`, `$stickyTable`, `$stickyButtons`, `$columnSelection` -- override `modifyListComponent()` in index page instead

### Field changes

`StackFields` removed. Use `Fieldset` instead:

```php
// v3
StackFields::make('Title', [Text::make('Field 1'), Text::make('Field 2')])

// v4
Fieldset::make('Title', [Text::make('Field 1'), Text::make('Field 2')])
```

### Layout changes

- `CompactLayout` removed -- extend `AppLayout` instead.
- New palette system: `PurplePalette` is the default.

### MenuItem parameter swap

`MenuItem::make()` now takes `$filler` first, then `$label` (optional, defaults to `getLabel()`):

```php
// v3
MenuItem::make('Settings', SettingResource::class)

// v4
MenuItem::make(SettingResource::class)
```

### Async methods require attribute

All async methods must have the `#[AsyncMethod]` attribute and now support DI:

```php
use MoonShine\Crud\JsonResponse;
use MoonShine\Support\Attributes\AsyncMethod;

class MyPage extends Page
{
    #[AsyncMethod]
    public function someAsyncMethod(JsonResponse $response): JsonResponse
    {
        return $response->toast('Loaded successfully');
    }
}
```

### Deprecated classes (removed in 5.0)

| Old class | New replacement |
|-----------|---------------|
| `MoonShine\Laravel\Notifications\NotificationButton` | `MoonShine\Crud\Notifications\NotificationButton` |
| `MoonShine\Laravel\MoonShineUI` | Use `toast()` helper instead of `MoonShineUI::toast()` |
| `MoonShine\Laravel\Handlers\Handlers` | `MoonShine\Crud\Handlers\Handlers` |
| `MoonShine\Laravel\Handlers\Handler` | `MoonShine\Crud\Handlers\Handler` |

## Cross-references

- **moonshine-resources-v4** -- Creating and configuring ModelResource classes, CRUD operations, pages, filters, and actions.
- **moonshine-fields-v4** -- Field types, validation, and field configuration.
- **moonshine-components-v4** -- UI components (Grid, Column, Box, LineBreak, FormBuilder, TableBuilder, etc.).
- **moonshine-appearance-v4** -- Layouts, menu configuration, color palettes, icons, and dark mode.
- **moonshine-frontend-v4** -- API mode, SDUI, Alpine.js events, and async UI updates.
- **moonshine-security-v4** -- Authentication, authorization, guards, pipelines, and user management.
- **moonshine-advanced-v4** -- Controllers, handlers, testing, package development, and recipe patterns.
- [references/config-options.md](references/config-options.md) -- Full configuration option reference with both config file and ServiceProvider examples.
- [references/config-auth-localization.md](references/config-auth-localization.md) -- Artisan command signatures, localization details, and troubleshooting.
