---
name: filament-plugin-development
description: Build and publish custom Filament plugins (Filament is the Laravel admin-panel framework). Use when creating a Filament plugin/package, implementing the Plugin contract, scaffolding from the plugin skeleton, registering assets/resources/pages/render-hooks, making a configurable plugin, testing it, or publishing to Packagist and the filamentphp.com/plugins directory. Targets Filament v4 (v5 shares the same plugin API). For USING Filament (resources/forms/tables), use the laravel-filament skill instead.
---

# Building & publishing Filament plugins (v4 / v5)

A Filament "plugin" is just a **Composer package** that extends a Filament app. Verified against `filamentphp.com/docs/4.x`. v5 shares the same plugin API.

## Two tiers - pick the smaller one

**A. Plain package (components only).** Ships resources/pages/widgets/fields/actions and does **not** implement any contract. The installing app wires them in manually (`->resources([...])`, `->widgets([...])`). **If your package is one widget or one field, do this - you do not need the `Plugin` contract.**

**B. Panel Plugin.** A class implementing `Filament\Contracts\Plugin`, registered with `->plugin(YourPlugin::make())`. Reach for this only when you bundle **multiple** things behind one registration, need **per-panel configuration**, or need boot-time logic. Rule of thumb: more than one moving part, or configurable -> Plugin contract; otherwise ship it plain.

## The `Plugin` contract

Three methods:

| Method | Runs | Purpose |
|---|---|---|
| `getId(): string` | - | Globally-unique, stable singleton key (e.g. `'blog'` - not `'settings'`, which clashes) |
| `register(Panel $panel): void` | while the panel is **configured** | register resources/pages/widgets/render hooks/assets on the panel |
| `boot(Panel $panel): void` | only for the **active** panel (via middleware) | runtime side effects |

```php
namespace Vendor\FilamentBlog;

use Filament\Contracts\Plugin;
use Filament\Panel;

class BlogPlugin implements Plugin
{
    public function getId(): string { return 'blog'; }

    public function register(Panel $panel): void
    {
        $panel->resources([PostResource::class])
              ->pages([Settings::class])
              ->widgets([BlogOverviewWidget::class]);
    }

    public function boot(Panel $panel): void { /* runtime side effects here */ }

    public static function make(): static { return app(static::class); }         // install-side: ->plugin(BlogPlugin::make())
    public static function get(): static { return filament(app(static::class)->getId()); } // read configured instance anywhere
}
```

Register in the app's `PanelProvider`: `->plugin(BlogPlugin::make())`.

> **#1 v3 -> v4 migration break:** boot-time side effects must be in `boot(Panel $panel)`, NOT the constructor - in v4 the constructor no longer fires them and they silently stop working.

## Configurable plugins

Fluent setter returns `static`; getter reads it; `register()`/`boot()` branch on it. Config is **per-panel** (each `->plugin(Make()->...)` call gets its own container-bound instance):

```php
protected bool $hasAuthorResource = false;

public function authorResource(bool $condition = true): static { $this->hasAuthorResource = $condition; return $this; }
public function hasAuthorResource(): bool { return $this->hasAuthorResource; }

public function register(Panel $panel): void
{
    if ($this->hasAuthorResource()) { $panel->resources([AuthorResource::class]); }
}
```
Install-side: `->plugin(BlogPlugin::make()->authorResource(true))`. Read anywhere: `filament('blog')->hasAuthorResource()`.

Only reach for closure config (`bool|Closure` + the `EvaluatesClosures` trait's `evaluate()`) when you actually need closures - don't wrap a plain bool in closure machinery.

## Scaffolding: the official skeleton

There is **no** `make:filament-plugin` command. Start from [`filamentphp/plugin-skeleton`](https://github.com/filamentphp/plugin-skeleton):
1. "Use this template" -> your repo, clone it.
2. `php ./configure.php` - interactive; rewrites stubs (vendor/namespace/author) and deletes itself.
3. **Delete unused boilerplate** (`config/`, `database/`, `src/Commands/`, `stubs/`) - lazy wins.

### Service provider - Spatie Package Tools (v4)
Extend `Spatie\LaravelPackageTools\PackageServiceProvider` (the v3 `PluginServiceProvider` is removed; a missing static `$name` throws):
```php
use Spatie\LaravelPackageTools\{Package, PackageServiceProvider};
use Filament\Support\Facades\FilamentAsset;
use Filament\Support\Assets\AlpineComponent;
use Livewire\Livewire;

class ClockWidgetServiceProvider extends PackageServiceProvider
{
    public static string $name = 'clock-widget';

    public function configurePackage(Package $package): void
    {
        $package->name(static::$name)->hasViews()->hasTranslations();
        // ->hasMigrations([...]), ->hasConfigFile(), ->hasCommands([...]) as needed
    }

    public function packageBooted(): void
    {
        Livewire::component('clock-widget', ClockWidget::class);
        FilamentAsset::register(
            [ AlpineComponent::make('clock-widget', __DIR__ . '/../resources/dist/clock-widget.js') ],
            package: 'vendor/clock-widget',
        );
    }
}
```
Auto-discovery via `composer.json` `extra.laravel.providers` (the skeleton sets this).

## Assets

Register in the provider's `packageBooted()`. **Always pass `package:`** to namespace assets into their own `/public` subdir (prevents filename collisions):
```php
use Filament\Support\Assets\{Css, Js, AlpineComponent};

FilamentAsset::register([
    Css::make('my-styles', __DIR__.'/../resources/dist/plugin.css'),
    Js::make('my-scripts', __DIR__.'/../resources/dist/plugin.js')->loadedOnRequest(),
    AlpineComponent::make('my-widget', __DIR__.'/../resources/dist/my-widget.js'),
], package: 'vendor/package');
```
- `->loadedOnRequest()` / async Alpine components = loaded only when referenced. **Prefer this**; don't ship a global CSS/JS that loads on every page for a one-page feature.
- Truly-global assets: register on the panel via `$panel->assets([...])` in `register()`.
- Retrieve: `FilamentAsset::getStyleHref('id', package: 'vendor/pkg')`, `getScriptSrc(...)`, `getAlpineComponentSrc('id','vendor/pkg')` (with `x-load`/`x-load-src` in Blade).
- **Commit built assets** (`resources/dist`) so consumers don't need your Node toolchain.

## Render hooks
Inject Blade at fixed UI points:
```php
use Filament\View\PanelsRenderHook;
// per-panel, in register():
$panel->renderHook(PanelsRenderHook::BODY_START, fn () => view('blog::banner')->render());
// or globally, in the provider (with optional scopes):
\Filament\Support\Facades\FilamentView::registerRenderHook(
    PanelsRenderHook::USER_MENU_BEFORE, fn () => view('blog::menu-extra')->render(),
    scopes: \App\Filament\Pages\Dashboard::class,
);
```
`PanelsRenderHook` has constants for `BODY_*`, `TOPBAR_*`, `SIDEBAR_*`, `PAGE_*`, `USER_MENU_*`, etc.

## Views, translations, testing
- `->hasViews()` namespaces `resources/views/x.blade.php` as `clock-widget::x` (`protected static string $view = 'clock-widget::widget';`). `->hasTranslations()` -> `__('clock-widget::file.key')`. Consumers publish overrides with `--tag=clock-widget-views` (`-translations`, `-config`, `-migrations`).
- **Test with Pest + Orchestra Testbench** (skeleton ships it). Boot a minimal panel with the plugin registered, then Filament's Livewire helpers:
```php
use function Pest\Livewire\livewire;
livewire(ListPosts::class)->assertOk()->assertCanSeeTableRecords(Post::factory()->count(3)->create());
```

## Publishing
1. **Packagist:** valid `composer.json` (`vendor/plugin`, PSR-4, `extra.laravel.providers`, a real `"filament/filament": "^4.0"` constraint - don't float `dev-main`); tag SemVer (`git tag v1.0.0 && git push --tags`); submit to [Packagist](https://packagist.org) + enable the GitHub webhook. Consumers `composer require vendor/plugin`.
2. **Official directory:** request author access at [filamentphp.com/author](https://filamentphp.com/author) (the old GitHub-PR flow is retired - it's the author dashboard now), then submit name/description/docs/repo/categories + support flags (dark mode, i18n, Filament versions). Free or paid listings supported.

## Gotchas recap
- Boot-time side effects -> `boot()`, not the constructor (v4 break).
- `getId()` unique + stable (it's the singleton key).
- Namespace assets with `package:`; prefer on-request/async loading.
- Never hardcode panel assumptions (id `admin`, a path, single-panel) - read the passed `Panel`.
- Extend `PackageServiceProvider` with a static `$name`.
- Keep it plain when one component is all you ship.

## Sources
[Panel plugins](https://filamentphp.com/docs/4.x/plugins/panel-plugins) · [Building a panel plugin](https://filamentphp.com/docs/4.x/plugins/building-a-panel-plugin) · [Assets](https://filamentphp.com/docs/4.x/advanced/assets) · [plugin-skeleton](https://github.com/filamentphp/plugin-skeleton) · [Author dashboard](https://filamentphp.com/author)
