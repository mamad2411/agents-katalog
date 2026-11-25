---
name: moonshine-appearance-v4
description: Use when working on MoonShine v4 layouts, custom layouts, menus, color palettes, icons, assets, custom pages, dark mode, branding, or Blade templates.
---

# MoonShine v4 Appearance

Covers layout templates, menu configuration, color palette system, icons, asset management, dark mode, branding, and Blade integration.

## CRITICAL v4 changes from v3

- **CompactLayout removed** -- extend `AppLayout` directly and use `$contentSimpled`, `$contentCentered` properties instead.
- **NEW palette system** -- `PurplePalette` is the default; palette classes replace direct color config. Colors now use OKLCH format.
- **MenuItem parameter swap** -- `$filler` is now the first parameter, `$label` is second and optional (auto-derived from `getLabel()`/`getTitle()`).
- **Profile component** -- `$withBorder` parameter removed.
- **Component control** -- new boolean properties `$sidebar`, `$topBar`, `$bottomBar`, `$mobileMode` on layout.
- **BottomBar** -- new component for bottom navigation, auto-displays top menu.
- **Mobile Mode** -- new `$mobileMode` property for mobile-optimized layouts.

## 1. Layout basics

MoonShine v4 publishes `app/MoonShine/Layouts/AppLayout.php` at install. All custom layouts extend `AppLayout`.

### Hierarchy

```
BaseLayout (abstract)
  -> AppLayout (standard sidebar layout)
  -> BlankLayout (bare bones -- Head + Body only)
  -> LoginLayout (authentication page)
```

### Choosing a layout

```php
// config/moonshine.php
'layout' => \App\MoonShine\Layouts\MoonShineLayout::class,

// Or via MoonShineServiceProvider
$config->layout(\App\MoonShine\Layouts\CustomLayout::class);
```

### Extending AppLayout

```php
namespace App\MoonShine\Layouts;

use MoonShine\Laravel\Layouts\AppLayout;
use MoonShine\UI\Components\Layout\Layout;

final class MoonShineLayout extends AppLayout
{
    protected function getFooterMenu(): array
    {
        return [
            'https://example.com' => 'Custom link',
        ];
    }

    protected function getFooterCopyright(): string
    {
        return 'My Company';
    }

    public function build(): Layout
    {
        return parent::build();
    }
}
```

### Override individual component methods

```php
protected function getHeadComponent(bool $withAssetsFragment = true): Head { /* ... */ }
protected function getLogoComponent(): Logo { /* ... */ }
protected function getSidebarComponent(): Sidebar { /* ... */ }
protected function getHeaderComponent(): Header { /* ... */ }
protected function getTopBarComponent(): Topbar { /* ... */ }
protected function getFooterComponent(): Footer { /* ... */ }
protected function getProfileComponent(): Profile { /* ... */ }
protected function getContentComponents(): array { /* ... */ }
protected function getLogo(bool $small = false): string { /* ... */ }
protected function getHomeUrl(): string { /* ... */ }
```

### Content layout properties

```php
// Remove border and background from content block
protected bool $contentSimpled = true; // default false

// Center content in a fixed-width container
protected bool $contentCentered = true; // default false
```

## 2. Component control (NEW in v4)

Control layout components via boolean properties -- no need to override `build()`.

```php
final class MoonShineLayout extends AppLayout
{
    protected bool $sidebar = true;     // enabled by default
    protected bool $topBar = false;     // disabled by default
    protected bool $bottomBar = false;  // disabled by default
    protected bool $mobileMode = false; // disabled by default
}
```

- **Sidebar** -- set `$sidebar = false` to disable.
- **TopBar** -- set `$topBar = true` to enable. If used with Sidebar, TopBar must come first in `build()`.
- **BottomBar** -- set `$bottomBar = true` to enable. Auto-displays top menu.
- **Mobile Mode** -- set `$mobileMode = true` for compact styles, hidden Burger, auto BottomBar.

### Layout slots

```php
protected function sidebarSlot(): array
{
    return [Search::make()->enabled()];
}

protected function sidebarTopSlot(): array
{
    return [Notifications::make()];
}

protected function topBarSlot(): array
{
    return [/* custom components */];
}
```

See [references/layouts.md](references/layouts.md) for the full layout API.

## 3. Creating custom layouts

```shell
php artisan moonshine:layout MyLayout
```

Creates `app/MoonShine/Layouts/MyLayout.php`.

### Page-specific layouts

```php
class CustomPage extends Page
{
    protected ?string $layout = MyLayout::class;
}

// Or via attribute
use MoonShine\Core\Attributes\Layout;

#[Layout(MyLayout::class)]
class CustomPage extends Page {}
```

## 4. Menu system

The menu is declared in the layout's `menu()` method.

### MenuItem -- NEW parameter order in v4

```php
MenuItem::make(
    Closure|MenuFillerContract|string $filler,  // FIRST: resource, page, URL, or closure
    Closure|string $label = null,               // SECOND: optional, auto-derived from getTitle()
    string $icon = null,
    Closure|bool $blank = false
)
```

### Quick example

```php
use MoonShine\MenuManager\MenuItem;
use MoonShine\MenuManager\MenuGroup;
use MoonShine\MenuManager\MenuDivider;

protected function menu(): array
{
    return [
        MenuGroup::make('Content', [
            MenuItem::make(ArticleResource::class),
            MenuItem::make(CategoryResource::class, icon: 'tag'),
        ])->icon('newspaper'),

        MenuDivider::make(),

        MenuItem::make(DashboardPage::class, 'Dashboard', 'home'),
        MenuItem::make('https://example.com', 'External', blank: true),
    ];
}
```

### Key menu features

- **MenuItem** -- links to Resource, Page, URL, or Closure. Label auto-derived from filler.
- **MenuGroup** -- groups items with optional icon.
- **MenuDivider** -- visual separator with optional label.
- **badge()** -- show counts: `->badge(fn() => Comment::count())`
- **canSee()** -- conditional display: `->canSee(fn() => auth()->user()->isAdmin())`
- **translatable()** -- i18n: `->translatable('menu')`
- **whenActive()** -- custom active state logic.
- **icon()** -- Heroicons or custom SVGs.
- **onlyIcon()** -- display icon without text label, shows tooltip on hover.
- **changeButton()** -- modify the underlying ActionButton.

### Autoloaded menu

```php
protected function menu(): array
{
    return $this->autoloadMenu();
    // or with icon-only mode:
    // return $this->autoloadMenu(onlyIcons: true);
}
```

Attributes for autoload: `#[SkipMenu]`, `#[Group('name', 'icon')]`, `#[Order(1)]`, `#[CanSee(method: 'methodName')]`, `#[Badge('new')]`.

See [references/menu-system.md](references/menu-system.md) for the full menu API.

## 5. Color palette system (NEW in v4)

MoonShine v4 uses palette classes instead of direct color arrays. The default is `PurplePalette`.

### Setting a palette

```php
// In layout
final class MoonShineLayout extends AppLayout
{
    protected ?string $palette = CorporatePalette::class;
}

// In config/moonshine.php
'palette' => \MoonShine\ColorManager\Palettes\PurplePalette::class,

// Programmatically in ServiceProvider
$colors->palette(new CorporatePalette());
```

### Available built-in palettes

`PurplePalette` (default), `CyanPalette`, `GrayPalette`, `GreenPalette`, `HalloweenPalette`, `LimePalette`, `NeutralPalette`, `OrangePalette`, `PinkPalette`, `RetroPalette`, `RosePalette`, `SkyPalette`, `SpringPalette`, `TealPalette`, `ValentinePalette`, `WinterPalette`, `YellowPalette`.

### Creating a custom palette

```php
namespace App\MoonShine\Palettes;

use MoonShine\Contracts\ColorManager\PaletteContract;

final class CorporatePalette implements PaletteContract
{
    public function getColors(): array
    {
        return [
            'primary' => 'oklch(65% 0.18 264)',
            'base' => [
                'default' => '0 0 0',
                50 => 'oklch(98% 0.02 250)',
            ],
        ];
    }

    public function getDarkColors(): array
    {
        return [
            'primary' => 'oklch(60% 0.17 264)',
            'base' => [
                'default' => '0.24 0 0',
                50 => 'oklch(98% 0.02 250)',
            ],
        ];
    }
}
```

### ColorManager override in layout

```php
protected function colors(ColorManagerContract $colorManager): void
{
    $colorManager
        ->primary('oklch(65% 0.18 264)')
        ->secondary('oklch(70% 0.14 230)')
        ->successBg('oklch(63.9% 0.218 142.495)')
        ->errorBg('oklch(58.9% 0.214 26.855)');

    // Dark theme
    $colorManager
        ->set('body', '0.2 0.0168 274.32', dark: true);
}
```

See [references/colors.md](references/colors.md) for the full color API.

## 6. Icons

MoonShine v4 uses **Heroicons** with four sets: Outline (default), Solid (`s.`), Mini (`m.`), Compact (`c.`).

```php
->icon('cog')           // Outline (default)
->icon('s.cog')         // Solid
->icon('m.cog')         // Mini
->icon('c.cog')         // Compact
```

Custom icon sets via `$path` parameter or `$custom` mode with raw HTML/SVG.

See [references/icons.md](references/icons.md) for icon details.

## 7. Assets

Add CSS/JS to a layout via the `assets()` method:

```php
use MoonShine\AssetManager\Css;
use MoonShine\AssetManager\Js;
use MoonShine\AssetManager\InlineCss;

protected function assets(): array
{
    return [
        ...parent::assets(),
        Css::make('/css/custom.css'),
        Js::make('/js/custom.js')->defer(),
        InlineCss::make(':root { --spacing: 0.15rem; }'),
    ];
}
```

### Vite integration

```php
use Illuminate\Support\Facades\Vite;

protected function assets(): array
{
    return [
        $this->getMainThemeJs(),
        Css::make(Vite::asset('resources/css/app.css')),
        Js::make(Vite::asset('resources/js/app.js')),
    ];
}
```

Asset types: `Js`, `Css`, `InlineCss`, `InlineJs`, `Raw`.

See [references/assets-branding.md](references/assets-branding.md) for the full asset and branding API.

## 8. Dark mode

### Always-dark theme

```php
protected function isAlwaysDark(): bool
{
    return true;
}
```

### Disable theme switcher (light only)

```php
protected function hasThemes(): bool
{
    return false;
}
```

The `ThemeSwitcher` component is included by default in Sidebar and TopBar.

### Force dark mode on custom components

Sidebar, TopBar, and MobileBar are styled dark by default. Force dark on custom additions:

```php
$this->getSidebarComponent()->class('dark'),
$this->getTopBarComponent()->class('dark'),
```

## 9. Branding

### Logo

```php
protected function getLogo(bool $small = false): string
{
    return $small ? '/images/logo-small.png' : '/images/logo.png';
}
```

Or via config:

```php
// config/moonshine.php
'logo' => '/images/logo.png',
'logo_small' => '/images/logo-small.png',
```

### Favicon

```php
protected function getFaviconComponent(): Favicon
{
    return parent::getFaviconComponent()->customAssets([
        'apple-touch' => '/favicon/apple-touch-icon.png',
        '32' => '/favicon/favicon-32x32.png',
        '16' => '/favicon/favicon-16x16.png',
        'safari-pinned-tab' => '/favicon/safari-pinned-tab.svg',
    ]);
}
```

### Footer

```php
protected function getFooterMenu(): array
{
    return ['https://docs.example.com' => 'Docs'];
}

protected function getFooterCopyright(): string
{
    return sprintf('&copy; %d My Company', now()->year);
}
```

## 10. Blade templates

MoonShine v4 supports pure Blade layouts using `<x-moonshine::layout.*>` components.

```blade
<x-moonshine::layout>
    <x-moonshine::layout.html :with-alpine-js="true" :with-themes="true">
        <x-moonshine::layout.head>
            <x-moonshine::layout.meta name="csrf-token" :content="csrf_token()"/>
            <x-moonshine::layout.favicon />
            <x-moonshine::layout.assets>
                @vite(['resources/css/main.css', 'resources/js/app.js'], 'vendor/moonshine')
            </x-moonshine::layout.assets>
        </x-moonshine::layout.head>
        <x-moonshine::layout.body>
            <x-moonshine::layout.wrapper>
                <x-moonshine::layout.sidebar :collapsed="true">
                    <!-- sidebar content -->
                </x-moonshine::layout.sidebar>
                <x-moonshine::layout.div class="layout-page">
                    <x-moonshine::layout.header>
                        <x-moonshine::layout.burger/>
                    </x-moonshine::layout.header>
                    <x-moonshine::layout.content>
                        Your content
                    </x-moonshine::layout.content>
                </x-moonshine::layout.div>
            </x-moonshine::layout.wrapper>
        </x-moonshine::layout.body>
    </x-moonshine::layout.html>
</x-moonshine::layout>
```

### Fragments

Layout parts live inside `Fragment` components for AJAX updates:

- `sidebar-top` -- logo and theme switch
- `sidebar-content` -- side menu content
- `topbar-logo` -- logo in top menu
- `topbar-menu` -- top menu items
- `topbar-actions` -- action block in top menu
- `assets` -- styles and scripts

```php
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;

return JsonResponse::make()->events([
    AlpineJs::event(JsEvent::FRAGMENT_UPDATED, 'sidebar-content'),
    AlpineJs::event(JsEvent::FRAGMENT_UPDATED, 'topbar-menu'),
]);
```

## 11. Cross-references

- [references/layouts.md](references/layouts.md) -- full layout API, component control, slots, build method
- [references/menu-system.md](references/menu-system.md) -- full menu API, autoload, attributes
- [references/colors.md](references/colors.md) -- palette system, ColorManager methods, color tokens
- [references/icons.md](references/icons.md) -- Heroicons sets, custom icons, icon component
- [references/assets-branding.md](references/assets-branding.md) -- AssetManager, Vite, branding, custom build
- **moonshine-setup-v4** -- Installation, configuration, routing
- **moonshine-components-v4** -- UI components used inside layouts
- **moonshine-resources-v4** -- ModelResource classes for menu items
- **moonshine-fields-v4** -- Field types used within page components
