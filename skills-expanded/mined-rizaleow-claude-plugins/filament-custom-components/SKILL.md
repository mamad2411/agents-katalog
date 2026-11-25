---
description: Build reusable Filament v5 components — custom fields, columns, infolist entries, and full Filament Plugin classes — with views, view data, Livewire/Alpine interop, and panel registration. Use when authoring a custom Filament component or plugin.
---

# Filament v5 Custom components

Three component families share the same recipe: a PHP class extending the base, plus a Blade view. Plugins bundle several of them behind a `Plugin` contract.

## Preflight

- `mcp__boost__filament_list_custom_components` — see existing custom fields/columns/entries.
- `mcp__boost__filament_scaffold_custom_field --name ColorSwatch` — generate class + view diff.

## Custom field

```php
namespace App\Filament\Forms\Components;

use Filament\Forms\Components\Field;

class ColorSwatch extends Field
{
    protected string $view = 'filament.forms.components.color-swatch';

    protected array $palette = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444'];

    public function palette(array $colors): static
    {
        $this->palette = $colors;
        return $this;
    }

    public function getPalette(): array
    {
        return $this->palette;
    }
}
```

`resources/views/filament/forms/components/color-swatch.blade.php`:

```blade
<x-dynamic-component :component="$getFieldWrapperView()" :field="$field">
    <div
        x-data="{ state: $wire.$entangle('{{ $getStatePath() }}') }"
        class="flex gap-2"
    >
        @foreach ($getPalette() as $color)
            <button
                type="button"
                @click="state = '{{ $color }}'"
                :class="state === '{{ $color }}' ? 'ring-2 ring-offset-2' : ''"
                style="background: {{ $color }}"
                class="h-8 w-8 rounded-full"
            ></button>
        @endforeach
    </div>
</x-dynamic-component>
```

Use in a schema: `ColorSwatch::make('brand_color')->palette(['#fff', '#000'])`.

## Custom column

```php
namespace App\Filament\Tables\Columns;

use Filament\Tables\Columns\Column;

class StatusPill extends Column
{
    protected string $view = 'filament.tables.columns.status-pill';
}
```

Access state in the view as `$getState()`.

## Custom infolist entry

```php
namespace App\Filament\Infolists\Components;

use Filament\Infolists\Components\Entry;

class TimelineEntry extends Entry
{
    protected string $view = 'filament.infolists.components.timeline-entry';
}
```

## Filament Plugin class

Plugins package components + bootstrap + config behind `Filament\Contracts\Plugin`.

```php
namespace Acme\BrandKit;

use Filament\Contracts\Plugin;
use Filament\Panel;

class BrandKitPlugin implements Plugin
{
    public static function make(): static
    {
        return app(static::class);
    }

    public function getId(): string
    {
        return 'acme-brand-kit';
    }

    public function register(Panel $panel): void
    {
        $panel->resources([\Acme\BrandKit\Resources\BrandResource::class])
              ->widgets([\Acme\BrandKit\Widgets\BrandPaletteWidget::class]);
    }

    public function boot(Panel $panel): void
    {
        // runtime wiring; runs once per request after register()
    }
}
```

Register on the panel:

```php
->plugins([
    \Acme\BrandKit\BrandKitPlugin::make(),
])
```

## View data & JS assets

- `getViewData(): array` — extra variables for the view (e.g. computed defaults).
- `extraAttributes()` / `extraAlpineAttributes()` — pass HTML or `x-on:*` attrs.
- For JS/CSS: register via `FilamentAsset::register([Js::make('foo', __DIR__.'/../dist/foo.js')->loadedOnRequest()])` inside the plugin's `boot()`, then `@assets`/`@filamentScripts` pick them up.

## Livewire interop

Custom components inherit the host component's Livewire instance. Use `$wire.$entangle('state.path')` for two-way binding, `$this->dispatch('event-name')` for events, and Alpine via the Blade snippet above.

## Where to put files

| Kind | Path |
| --- | --- |
| Custom field | `app/Filament/Forms/Components/` |
| Custom column | `app/Filament/Tables/Columns/` |
| Custom entry | `app/Filament/Infolists/Components/` |
| Custom page/widget | `app/Filament/{Pages,Widgets}/` |
| Distributable plugin | own composer package, namespaced |

See also: filament-schemas, filament-tables, filament-panels.
