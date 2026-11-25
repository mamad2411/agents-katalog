---
name: moonshine-fields-v4
description: Use when working on MoonShine v4 field types, relationship fields, field validation, lifecycle, apply logic, field modes, reactivity, showWhen, or creating custom fields.
---

# MoonShine v4 Fields

## Field Concept

Fields are the core building blocks of the MoonShine admin panel. They are used in:
- `FormBuilder` for building forms
- `TableBuilder` for creating tables
- `ModelResource` for filters
- Custom pages and Blade views

Every field is created via the static `make()` method:

```php
use MoonShine\UI\Fields\Text;

Text::make('Title')                // label only, column auto-detected as "title"
Text::make('Title', 'title')       // explicit label + column
Text::make('Title', 'first_name', fn($item) => $item->first_name . ' ' . $item->last_name)
```

Constructor signature for all fields:
```php
make(Closure|string|null $label = null, ?string $column = null, ?Closure $formatted = null)
```

> Fields in MoonShine are NOT tied to a model (except `Slug` and relationship fields).

## Field Modes

Every field has three visual states:

| Mode | Method | When Used | Description |
|------|--------|-----------|-------------|
| **Default** | `defaultMode()` | Forms | Renders as HTML form element (`<input>`, `<select>`, etc.) |
| **Preview** | `previewMode()` | Tables, detail views | Displays formatted value (thumbnails, formatted dates, etc.) |
| **Raw** | `rawMode()` | Export | Outputs the original unmodified value |

```php
Text::make('Title')->defaultMode()   // always form element
Text::make('Title')->previewMode()   // always preview display
Text::make('Title')->rawMode()       // always raw value
```

## Field Lifecycle

### In FormBuilder (saving)
1. Field declared in resource
2. Field enters FormBuilder
3. FormBuilder fills the field (`fill()`)
4. FormBuilder renders the field
5. On submit: `beforeApply()` -> `apply()` -> model `save()` -> `afterApply()`

### In TableBuilder (display)
1. Field enters TableBuilder in preview mode
2. TableBuilder iterates data, fills each field
3. TableBuilder renders rows with field previews

### In Export
1. Field enters Handler in raw mode
2. Handler iterates data, fills fields, generates table from raw values

## Common Methods Quick Reference

| Method | Description |
|--------|-------------|
| `make($label, $column, $formatted)` | Create field instance |
| `setLabel($label)` | Change label (accepts Closure) |
| `translatable($key)` | Translate label via Laravel localization |
| `hint($text)` | Add hint text below label |
| `link($url, $name, $icon, $blank)` | Add link next to field |
| `badge($color, $icon)` | Show as colored badge in preview (13 colors) |
| `horizontal()` | Label and field side by side |
| `sortable($callback)` | Enable column sorting in tables |
| `required()` | Mark as required |
| `disabled()` | Disable input |
| `readonly()` | Read-only |
| `nullable()` | Allow NULL value |
| `default($value)` | Set default value |
| `customAttributes($attrs)` | Add HTML attributes |
| `customWrapperAttributes($attrs)` | Add wrapper attributes |
| `withoutWrapper()` | Remove wrapper div |
| `canSee(fn)` | Conditional display |
| `when(fn, fn)` | Fluent conditional |
| `showWhen($column, $op, $value)` | Dynamic JS-based show/hide |
| `showWhenDate($column, $op, $value)` | Dynamic show/hide for date fields |
| `showWhenRow($column, $op, $value)` | Show/hide within Json table row |
| `reactive(fn, lazy, debounce, throttle, silent, silentSelf)` | Reactive field changes |
| `updateOnPreview()` | Edit in table cells |
| `withUpdateRow($component)` | Update entire row on change |
| `updateInPopover($component)` | Edit in popover |
| `onApply(fn)` | Override apply logic |
| `onBeforeApply(fn)` | Before apply hook |
| `onAfterApply(fn)` | After apply hook |
| `canApply(fn)` | Skip apply conditionally |
| `fill($value)` | Manually fill value |
| `changeFill(fn)` | Modify fill logic |
| `afterFill(fn)` | Post-fill logic |
| `changePreview(fn)` | Custom preview rendering |
| `changeRender(fn)` | Replace entire render |
| `modifyRawValue(fn)` | Modify raw/export value |
| `fromRaw(fn)` | Convert raw to value (import) |
| `onChangeUrl(fn)` | Action on value change (URL) |
| `onChangeMethod($method)` | Async method call on change |

## Field Types Catalog

### Basic Input Fields
| Field | Namespace | Description |
|-------|-----------|-------------|
| `Text` | `MoonShine\UI\Fields\Text` | Text input with extensions (copy/eye/locked/prefix/suffix) |
| `Textarea` | `MoonShine\UI\Fields\Textarea` | Multi-line text |
| `Number` | `MoonShine\UI\Fields\Number` | Numeric input with min/max/step/buttons/stars |
| `Password` | `MoonShine\UI\Fields\Password` | Password input (auto-hashes on apply) |
| `PasswordRepeat` | `MoonShine\UI\Fields\PasswordRepeat` | Password confirmation (no apply) |
| `Email` | `MoonShine\UI\Fields\Email` | Email input |
| `Phone` | `MoonShine\UI\Fields\Phone` | Phone input with mask support |
| `Url` | `MoonShine\UI\Fields\Url` | URL input with title/blank preview |
| `Color` | `MoonShine\UI\Fields\Color` | Color picker |
| `Date` | `MoonShine\UI\Fields\Date` | Date/datetime input with format/inputFormat |
| `DateRange` | `MoonShine\UI\Fields\DateRange` | Date range (fromTo) |
| `Range` | `MoonShine\UI\Fields\Range` | Numeric range (fromTo) |
| `RangeSlider` | `MoonShine\UI\Fields\RangeSlider` | Range with slider UI |
| `Slug` | `MoonShine\Laravel\Fields\Slug` | Auto-generated slug (model-dependent) |
| `ID` | `MoonShine\UI\Fields\ID` | Primary key (hidden in forms) |
| `Hidden` | `MoonShine\UI\Fields\Hidden` | Hidden input with showValue() |
| `HiddenIds` | `MoonShine\UI\Fields\HiddenIds` | Collects selected IDs for bulk actions |
| `Position` | `MoonShine\UI\Fields\Position` | Row numbering in repeating elements |
| `Preview` | `MoonShine\UI\Fields\Preview` | Read-only display (badge, boolean, link, image) |
| `Template` | `MoonShine\UI\Fields\Template` | Empty field built via fluent interface |

### Selection Fields
| Field | Namespace | Description |
|-------|-----------|-------------|
| `Select` | `MoonShine\UI\Fields\Select` | Dropdown with Tom Select (options, async, searchable, multiple, plugins) |
| `Enum` | `MoonShine\UI\Fields\Enum` | Select from PHP Enum with color/icon support |
| `Checkbox` | `MoonShine\UI\Fields\Checkbox` | Checkbox (on/off values) |
| `Switcher` | `MoonShine\UI\Fields\Switcher` | Toggle switch (extends Checkbox) |

### File and Editor Fields
| Field | Namespace | Description |
|-------|-----------|-------------|
| `File` | `MoonShine\UI\Fields\File` | File upload (disk, dir, extensions, multiple, removable) |
| `Image` | `MoonShine\UI\Fields\Image` | Image upload with preview and extraAttributes |
| `Code` | Package `moonshine/ace` | Code editor (Ace) |
| `Markdown` | Package `moonshine/easymde` | Markdown editor (EasyMDE) |
| `TinyMCE` | Package `moonshine/tinymce` | WYSIWYG editor |

### Structural Fields
| Field | Namespace | Description |
|-------|-----------|-------------|
| `Json` | `MoonShine\UI\Fields\Json` | JSON data (fields, keyValue, onlyValue, object, nested) |
| `Fieldset` | `MoonShine\UI\Fields\Fieldset` | Groups fields visually (replaces StackFields from v3) |

### Relationship Fields
| Field | Namespace | Laravel Relation |
|-------|-----------|-----------------|
| `BelongsTo` | `MoonShine\Laravel\Fields\Relationships\BelongsTo` | `BelongsTo` |
| `BelongsToMany` | `MoonShine\Laravel\Fields\Relationships\BelongsToMany` | `BelongsToMany` |
| `HasOne` | `MoonShine\Laravel\Fields\Relationships\HasOne` | `HasOne` |
| `HasMany` | `MoonShine\Laravel\Fields\Relationships\HasMany` | `HasMany` |
| `HasOneThrough` | `MoonShine\Laravel\Fields\Relationships\HasOneThrough` | `HasOneThrough` |
| `HasManyThrough` | `MoonShine\Laravel\Fields\Relationships\HasManyThrough` | `HasManyThrough` |
| `MorphOne` | `MoonShine\Laravel\Fields\Relationships\MorphOne` | `MorphOne` |
| `MorphMany` | `MoonShine\Laravel\Fields\Relationships\MorphMany` | `MorphMany` |
| `MorphTo` | `MoonShine\Laravel\Fields\Relationships\MorphTo` | `MorphTo` |
| `MorphToMany` | `MoonShine\Laravel\Fields\Relationships\MorphToMany` | `MorphToMany` |
| `RelationRepeater` | `MoonShine\Laravel\Fields\Relationships\RelationRepeater` | `HasMany`/`HasOne` inline |

## Relationship Fields Overview

All relationship fields require a registered `ModelResource`. Constructor:

```php
BelongsTo::make(
    Closure|string $label,
    ?string $relationName = null,
    Closure|string|null $formatted = null,
    ModelResource|string|null $resource = null,
)
```

**Key patterns across relationship fields:**
- `asyncSearch()` - async search with custom query, formatted output, limit
- `creatable()` - create related object via modal
- `valuesQuery()` - modify the query that fetches dropdown values
- `withImage()` - add images to dropdown items
- `searchable()` - enable search in dropdown
- `selectMode()` - display BelongsToMany as dropdown instead of checkboxes
- `relatedLink()` - show as a link with count instead of full list
- `tabMode()` / `modalMode()` - display HasOne/HasMany in tabs or modals
- `disableOutside()` - render inside the main form instead of separately
- `associatedWith()` - link field values to another field with asyncOnInit support

## v4 Changes from v3

| Change | Details |
|--------|---------|
| **StackFields removed** | Use `Fieldset` instead for grouping fields |
| **Fieldset field** | New field for grouping with HTML `<fieldset>` tag, supports conditional display |
| **RelationRepeater** | New field for HasMany/HasOne inline editing inside main form |
| **Template field** | New empty field built via fluent interface (setLabel/fields) |
| **HiddenIds field** | New field for collecting primary keys in bulk actions |
| **Select enhancements** | `Options`/`Option`/`OptionGroup` DTOs, `OptionProperty`/`OptionImage`, Tom Select plugins/settings/fieldsNames/asyncSettings, `selectCreatable()`, `selectMaxItems()` |
| **Reactivity params** | New: `lazy`, `silent`, `silentSelf` parameters with Closure support |
| **showWhen variants** | New: `showWhenDate()` for date fields, `showWhenRow()` for Json table rows |
| **AsyncMethod attribute** | Use `#[AsyncMethod]` attribute for async method declarations |
| **BelongsToMany enhancements** | `pivotModalMode()`, `pivotCardsMode()`, `deduplication()`, `horizontalMode()` |

## Creating a Custom Field

```shell
php artisan moonshine:field
```

This generates a field class with its own Blade view. Override `resolvePreview()`, `resolveOnApply()`, and the view to customize behavior.

## Reference Files

- `references/basic-fields.md` - Text, Number, Date, Slug, ID, Hidden, and other basic input fields
- `references/selection-fields.md` - Select (with Tom Select plugins, Options DTOs), Enum, Checkbox, Switcher, Preview
- `references/file-fields.md` - File, Image, Code, Markdown, TinyMCE editors
- `references/relationship-fields.md` - All relationship field types with full method reference
- `references/field-display-attributes.md` - Display methods, view modes, attributes, wrapper, sorting
- `references/field-values-lifecycle.md` - Value methods, fill logic, apply lifecycle, onChange, render
- `references/field-interactive.md` - Reactivity, showWhen, Json, Fieldset, Template, HiddenIds, inline editing, assets
