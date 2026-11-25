---
description: Design Filament v5 Schemas — the unified API for forms, infolists, and layout containers (Grid, Section, Tabs, Fieldset, Wizard) plus fields, entries, reactivity, and conditional visibility. Use when designing or modifying a Filament v5 Schema (form fields, infolist entries, or layout components).
---

# Filament v5 Schemas

`Filament\Schemas\Schema` is the **single** container for forms, infolists, and layouts. Field components, entry components, and layout components are all `->components([...])` children.

## Imports cheat sheet

```php
use Filament\Schemas\Schema;
use Filament\Schemas\Components\{Grid, Section, Tabs, Tabs\Tab, Fieldset, Wizard, Wizard\Step, Group};
use Filament\Forms\Components\{TextInput, Textarea, Select, Toggle, DatePicker, FileUpload, Repeater, Builder, Hidden, RichEditor};
use Filament\Infolists\Components\{TextEntry, IconEntry, ImageEntry, RepeatableEntry, ColorEntry, KeyValueEntry};
```

Note: layout components (`Grid`, `Section`, …) live under `Filament\Schemas\Components` in v5 — **not** under `Filament\Forms\Components` or `Filament\Infolists\Components` as in older versions.

## Skeleton

```php
public static function configure(Schema $schema): Schema
{
    return $schema->components([
        Section::make('Profile')
            ->description('Public information shown on the customer card.')
            ->columns(2)
            ->schema([
                TextInput::make('name')->required()->maxLength(120),
                TextInput::make('email')->email()->required(),
                Select::make('status')
                    ->options(['active' => 'Active', 'paused' => 'Paused'])
                    ->default('active')
                    ->live(),
                DatePicker::make('paused_until')
                    ->visible(fn ($get) => $get('status') === 'paused'),
            ]),
        Section::make('Billing')->collapsible()->schema([
            Repeater::make('addresses')
                ->relationship()
                ->schema([
                    TextInput::make('line1')->required(),
                    TextInput::make('city')->required(),
                ])
                ->columns(2)
                ->defaultItems(0),
        ]),
    ]);
}
```

## Layout components

| Component | Use |
| --- | --- |
| `Grid::make(3)` | Force N-column responsive grid. |
| `Section::make('Title')` | Card with title/description, `->collapsible()`, `->aside()`. |
| `Tabs::make('Tabs')->tabs([Tab::make('General')->schema([...])])` | Tabbed groups. |
| `Fieldset::make('Address')->schema([...])` | Native HTML fieldset look. |
| `Wizard::make([Step::make('Account')->schema([...])])` | Multi-step on create pages. |
| `Group::make([...])->columnSpan(2)` | Transparent grouping for layout. |

## Reactivity & conditions

- `->live()` — broadcast state changes immediately. `->live(onBlur: true)` for cheap reactions.
- `->live(debounce: 500)` for text inputs that drive expensive computations.
- `->afterStateUpdated(fn ($state, callable $set) => $set('slug', Str::slug($state)))` — derive from another field.
- `->visible(fn (Get $get) => $get('type') === 'company')`, `->hidden(...)`, `->disabled(...)`, `->required(...)` all accept closures.
- Use `Get`/`Set` helpers (`Filament\Schemas\Components\Utilities\Get|Set`) for type-safe closures.

## Infolist entries (same Schema, different components)

```php
public static function configure(Schema $schema): Schema
{
    return $schema->components([
        Section::make()->columns(3)->schema([
            TextEntry::make('name'),
            TextEntry::make('status')->badge()->color(fn ($state) => $state === 'active' ? 'success' : 'warning'),
            IconEntry::make('is_verified')->boolean(),
            ImageEntry::make('avatar_url')->circular(),
            RepeatableEntry::make('addresses')->schema([
                TextEntry::make('line1'),
                TextEntry::make('city'),
            ])->columns(2),
        ]),
    ]);
}
```

## Repeater & Builder

- `Repeater::make('items')->relationship()->schema([...])` — bind to a `hasMany`.
- `Repeater::make('items')->reorderable()->cloneable()->collapsed()` — common UX flags.
- `Builder::make('content')->blocks([Block::make('hero')->schema([...]), Block::make('cta')->schema([...])])` — CMS-style.

## Validation

Field-level: `->required()`, `->minLength()`, `->unique(table: User::class, ignoreRecord: true)`, `->rules(['regex:/^\d+$/'])`, `->validationMessages([...])`.

## When to extract

If `configure()` exceeds ~80 lines, split into private static methods (`getProfileSection()`, `getBillingSection()`) returning components, or split into separate schema classes (`CustomerProfileForm`, `CustomerBillingForm`) composed by the resource.

See also: filament-resources, filament-tables, filament-actions, filament-testing.
