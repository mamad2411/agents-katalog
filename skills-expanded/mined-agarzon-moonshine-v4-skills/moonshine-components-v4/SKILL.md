---
name: moonshine-components-v4
description: Use when working on MoonShine v4 FormBuilder, TableBuilder, ActionButton, layout components, navigation, modals, tabs, cards, metrics, overlays, or display components.
---

# MoonShine v4 Components

## Component Basics

Every UI element in MoonShine extends `MoonShineComponent`, a Blade component with admin-panel helpers.

**Namespace:** `MoonShine\UI\Components\*`

### Key Base Methods (all components)

```php
// Conditional display
Box::make()->canSee(fn(Box $ctx) => $user->isAdmin());

// Fluent conditional
Box::make()->when($condition, fn(Box $ctx) => $ctx->dark());
Box::make()->unless($condition, fn(Box $ctx) => $ctx->dark());

// Custom Blade view
Box::make('Title')->customView('my-view', ['key' => 'val']);

// Before-render hook
Box::make()->onBeforeRender(fn(Box $ctx) => /* ... */);

// Add assets on the fly
Box::make()->addAssets([new Css(Vite::asset('resources/css/block.css'))]);

// HTML attributes
Box::make()->customAttributes(['class' => 'my-class', 'data-id' => 1]);
Box::make()->class('extra-class')->style(['color: red']);

// Alpine.js attributes
Div::make([])->xData(['title' => 'Hello']); // x-data
Text::make('Title')->xModel();               // x-model
Text::make('Title')->xIf('type', 1);         // x-if
Text::make('Title')->xShow('type', '1');      // x-show

// Naming (required for events)
Box::make()->name('my-box');

// Macros
MoonShineComponent::macro('myMethod', fn() => /* ... */);
MoonShineComponent::mixin(new MyNewMethods());
```

### Creating Custom Components

```shell
php artisan moonshine:component MyComponent
```

---

## FormBuilder Quick Start

```php
use MoonShine\UI\Components\FormBuilder;
use MoonShine\Support\Enums\FormMethod;

// Simple form
FormBuilder::make('/crud/update')
    ->fields([
        Text::make('Title'),
        Textarea::make('Description'),
    ])
    ->fill(['title' => 'Hello', 'description' => 'World'])
    ->submit('Save', ['class' => 'btn-primary'])

// Async form that triggers table refresh on success
FormBuilder::make('/crud/update')
    ->name('main-form')
    ->async(events: [
        AlpineJs::event(JsEvent::TABLE_UPDATED, 'crud-table'),
        AlpineJs::event(JsEvent::FORM_RESET, 'main-form'),
    ])
    ->fields([Text::make('Title')])

// Call resource/page method without extra controller
FormBuilder::make()
    ->asyncMethod('updateSomething')
    ->fields([Text::make('Title')])

// Apply (process fields in controller)
$form->apply(fn(Model $item) => $item->save());

// Cast data to model
FormBuilder::make('/crud/update')
    ->fields([Text::make('Text')])
    ->fillCast(User::query()->first(), new ModelCaster(User::class))

// Precognitive validation
FormBuilder::make('/crud/update')->precognitive()

// Dispatch events on submit
FormBuilder::make()
    ->dispatchEvent(AlpineJs::event(JsEvent::OFF_CANVAS_TOGGLED, 'default'))
```

> See `references/form-table-builders.md` for full FormBuilder, TableBuilder, ActionButton, and ActionGroup API.

---

## TableBuilder Quick Start

```php
use MoonShine\UI\Components\Table\TableBuilder;

// Basic table
TableBuilder::make()
    ->fields([
        ID::make()->sortable(),
        Text::make('Title'),
    ])
    ->items([
        ['id' => 1, 'title' => 'First'],
        ['id' => 2, 'title' => 'Second'],
    ])
    ->buttons([
        ActionButton::make('Edit', fn() => route('edit')),
        ActionButton::make('Delete', fn() => route('delete'))->bulk(),
    ])

// Editable table with drag-drop and sticky header
TableBuilder::make()
    ->fields([Text::make('Title'), Text::make('Slug')])
    ->items($collection)
    ->editable()
    ->reorderable(url: '/reorder', key: 'id')
    ->sticky()
    ->creatable(limit: 10, label: 'Add Row')
    ->name('my-table')
    ->async()

// Async with lazy loading from external source
TableBuilder::make()
    ->name('dashboard-table')
    ->fields([ID::make(), Text::make('Title')])
    ->async()
    ->lazy()
    ->whenAsync(fn(TableBuilder $t) => $t->items(Http::get('/api/posts')->json()))

// Vertical display (detail page style)
TableBuilder::make()->fields($fields)->items([$item])->vertical()
```

---

## ActionButton Patterns

```php
use MoonShine\UI\Components\ActionButton;

// Basic
ActionButton::make('Click Me', '/url')->primary()->icon('pencil')

// Open modal
ActionButton::make('Open')
    ->inModal(title: 'Edit', content: 'Content', name: 'edit-modal')

// Async with events
ActionButton::make('Refresh', '/endpoint')
    ->async(events: [AlpineJs::event(JsEvent::TABLE_UPDATED, 'my-table')])

// Confirmation dialog
ActionButton::make('Delete', '/delete')
    ->withConfirm(title: 'Sure?', content: 'This is irreversible')

// Call resource method
ActionButton::make('Export')
    ->method('exportData', params: fn($item) => ['resourceItem' => $item->getKey()])

// Grouping with visibility
ActionGroup::make([
    ActionButton::make('Inline', '/')->showInLine(),
    ActionButton::make('Dropdown', '/')->showInDropdown(),
    ActionButton::make('Hidden', '/')->canSee(fn() => false),
])

// Bulk action (in table)
ActionButton::make('Mass Delete', route('mass.delete'))->bulk()

// Colors: primary(), secondary(), success(), warning(), error(), info()
// Badge: ->badge(fn() => Comment::count())
// Hotkeys: ->hotKeys(['shift', '2'])
```

---

## Layout Components Catalog

| Component | Namespace | Key Methods |
|---|---|---|
| Grid | `Layout\Grid` | `make($components, $gap = 6)` |
| Column | `Layout\Column` | `make($components, colSpan: 6, adaptiveColSpan: 12)` |
| Box | `Layout\Box` | `make($label, $components)`, `dark()`, `icon()` |
| Div | `Layout\Div` | `make($components)` |
| Flex | `Layout\Flex` | `make($components)`, `justifyAlign()`, `itemsAlign()`, `withoutSpace()`, `wrap()`, `unwrap()` |
| Wrapper | `Layout\Wrapper` | `make($components)` |
| Fragment | `Crud\Components\Fragment` | `make($components)`, `name()`, `updateWith()`, `autoUpdate($ms)`, `withSelectorsParams()` |
| Tabs | `Tabs` | `make([Tab::make()])`, `vertical()` |
| Tab | `Tabs\Tab` | `make($label, $components)`, `active()`, `name()`, `icon()`, `labelAttributes()` |
| Collapse | `Collapse` | `make($label, $components, $open, $persist)`, `icon()` |
| Card | `Card` | `make($title, $thumb, $url, $values, $subtitle, $overlay)`, `header()`, `actions()` |
| CardsBuilder | `CardsBuilder` | `make($items, $fields)`, `title()`, `subtitle()`, `thumbnail()`, `overlay()`, `columnSpan()`, `async()`, `paginator()` |

> See `references/layout-components.md` for full API with examples.

---

## Navigation Components

```php
use MoonShine\UI\Components\Layout\{TopBar, Sidebar, BottomBar, MobileBar, Menu};
use MoonShine\UI\Components\Breadcrumbs;

// TopBar with horizontal menu
TopBar::make([
    Fragment::make([Menu::make()->top()])->class('menu menu--horizontal'),
    Fragment::make([Profile::make(), ThemeSwitcher::make()])->class('menu-actions'),
])

// Sidebar with collapsible option
Sidebar::make([
    Fragment::make([Menu::make()])->class('menu menu--vertical'),
])->collapsed()

// BottomBar
BottomBar::make([Menu::make([MenuItem::make('/', 'Home')])])

// MobileBar (place above Sidebar/TopBar)
MobileBar::make([Menu::make()->top()])

// Menu (horizontal or vertical)
Menu::make([MenuItem::make('/', 'Dashboard')])->top()
Menu::make()->withoutScrollTo()

// Breadcrumbs
Breadcrumbs::make(['/' => 'Home', '/articles' => 'Articles'])
```

---

## Common Component Combinations

### Form inside Modal

```php
Modal::make(
    'Create User',
    static fn() => FormBuilder::make(route('users.store'))
        ->async()
        ->fields([Text::make('Name'), Email::make('Email')])
        ->submit('Create'),
)->name('create-modal'),

ActionButton::make('New User')->toggleModal('create-modal')
```

### Tabs with Tables and Forms

```php
Tabs::make([
    Tab::make('List', [
        TableBuilder::make()
            ->fields([ID::make(), Text::make('Title')])
            ->items($articles)
            ->name('articles-table')
            ->async()
    ]),
    Tab::make('Create', [
        FormBuilder::make(route('articles.store'))
            ->fields([Text::make('Title'), Textarea::make('Body')])
            ->async(events: [AlpineJs::event(JsEvent::TABLE_UPDATED, 'articles-table')])
    ]),
])
```

### Dashboard with Metrics

```php
use MoonShine\UI\Components\Metrics\Wrapped\ValueMetric;

Grid::make([
    Column::make([
        ValueMetric::make('Total Orders')
            ->value(fn() => Order::count())
            ->icon('shopping-bag')
    ], colSpan: 4),

    Column::make([
        ValueMetric::make('Revenue')
            ->value(fn() => Order::sum('total'))
            ->valueFormat(fn($v) => '$' . number_format($v))
    ], colSpan: 4),

    Column::make([
        ValueMetric::make('Completion')
            ->value(fn() => Order::completed()->count())
            ->progress(fn() => Order::count())
    ], colSpan: 4),
])
```

### Fragment for Partial Updates

```php
use MoonShine\Crud\Components\Fragment;

Fragment::make([
    TableBuilder::make()->fields($fields)->items($items)->name('data-table')
])->name('data-fragment'),

ActionButton::make('Reload')
    ->dispatchEvent(AlpineJs::event(JsEvent::FRAGMENT_UPDATED, 'data-fragment'))

// Auto-update every 5 seconds
Fragment::make([ValueMetric::make('Live')->value(fn() => rand(1, 100))])
    ->name('live-metric')
    ->autoUpdate(5000)
```

### OffCanvas Side Panel

```php
OffCanvas::make(
    'Filters',
    static fn() => FormBuilder::make()
        ->fields([Select::make('Status')->options($statuses)])
        ->submit('Apply'),
    'Show Filters'
)->left()->name('filter-panel'),
```

---

## JS Events Reference

| Event | Constant | Use |
|---|---|---|
| Form submit | `JsEvent::FORM_SUBMIT` | Trigger form submission |
| Form reset | `JsEvent::FORM_RESET` | Reset form fields |
| Table update | `JsEvent::TABLE_UPDATED` | Refresh async table |
| Table row update | `JsEvent::TABLE_ROW_UPDATED` | Refresh single row |
| Table reindex | `JsEvent::TABLE_REINDEX` | Reindex table fields |
| Table row added | `JsEvent::TABLE_ROW_ADDED` | Append cloned row |
| Modal toggle | `JsEvent::MODAL_TOGGLED` | Open/close modal |
| OffCanvas toggle | `JsEvent::OFF_CANVAS_TOGGLED` | Open/close side panel |
| Fragment update | `JsEvent::FRAGMENT_UPDATED` | Refresh fragment area |
| Tab active | `JsEvent::TAB_ACTIVE` | Activate tab by name |
| Cards updated | `JsEvent::CARDS_UPDATED` | Refresh async cards |
| Toast | `JsEvent::TOAST` | Show notification |

```php
use MoonShine\Support\AlpineJs;
use MoonShine\Support\Enums\JsEvent;

// Dispatching events
AlpineJs::event(JsEvent::TABLE_UPDATED, 'component-name')

// With params
AlpineJs::event(JsEvent::TOAST, params: ToastEventParams::make(ToastType::SUCCESS, 'Done'))
```

---

## Cross-references

- **moonshine-resources-v4**: Components are used extensively in resource pages (index, form, detail). FormBuilder and TableBuilder are the foundation of CRUD pages.
- **moonshine-fields-v4**: Fields are the building blocks placed inside FormBuilder, TableBuilder, and CardsBuilder. Field types, validation, and relationships are covered there.
- **moonshine-appearance-v4**: Layout components (Sidebar, Header, Footer, TopBar) and theming/styling details for the admin panel shell.

## Reference Files

- `references/form-table-builders.md` -- Full API for FormBuilder, TableBuilder, ActionButton, ActionGroup, FieldsGroup
- `references/layout-components.md` -- Grid, Column, Box, Flex, Tabs, Collapse, Card, CardsBuilder, Heading, Link, Button, etc.
- `references/overlay-components.md` -- Modal, OffCanvas, Dropdown, Popover, Alert, Flash, Spinner, Loader, When
- `references/display-components.md` -- Badge, Boolean, Color, Rating, ProgressBar, Thumbnails, Carousel, Icon, Metrics, Profile, etc.
