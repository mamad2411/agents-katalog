---
name: statamic-with-eloquent
description: "Develops with Statamic CMS (statamic/cms) and the Eloquent Driver (statamic/eloquent-driver). Activates when working with Statamic entries, collections, blueprints, fieldsets, globals, navigations, taxonomies, assets, views, templates, View Composers, Bard/Replicator fields, content blocks, or cp utilities; or when the user mentions Statamic, CMS, blueprint, collection, entry, fieldset, global set, content blocks, please commands, or Statamic routing."
license: MIT
compatible_agents:
  - Claude Code
  - Cursor
tags:
  - eloquent
  - database
  - laravel
  - statamic
  - blade
  - cms
  - php
keywords: ['eloquent', 'statamic', 'laravel', 'database', 'blade', 'cms', 'php']
metadata:
  triggers: Statamic, statamic/cms, statamic/eloquent-driver, Blade CMS, blueprint, collection entries, Statamic entries
  author: Dolphiq
---

# Statamic CMS Development

## When to Apply

Activate this skill when:

- Creating or editing Statamic collections, blueprints, fieldsets, or globals
- Working with Statamic entries, taxonomies, or navigations
- Building page templates or content block partials
- Creating or modifying View Composers for Statamic views
- Working with Bard, Replicator, or other Statamic fieldtypes
- Querying content via Statamic facades
- Running `php please` commands

## Documentation

Use `search-docs` with `packages: ["statamic/cms"]` for version-specific Statamic documentation.

## Blade-Only Templating

This project uses **Blade exclusively** — no Antlers. All templates are `.blade.php` files. Statamic variables are accessed as regular PHP variables in Blade.

```blade
{{-- Correct: Blade syntax --}}
<h1>{{ $title }}</h1>

{{-- WRONG: Antlers syntax — never use this --}}
{{ title }}
```

## Eloquent Driver

This project uses the Statamic Eloquent Driver with a **hybrid storage strategy**. Check `config/statamic/eloquent-driver.php` to see which resources use `eloquent` (database) vs `file` (disk).

- **Entries, terms, globals variables, nav trees, revisions** → stored in database
- **Blueprints, fieldsets, collections, forms** → stored as YAML files on disk
- All Eloquent tables use a configurable prefix (see `STATAMIC_ELOQUENT_PREFIX` env var)

**Always query content via Statamic facades** — they abstract the storage driver.

## Querying Content

Use Statamic facades, never raw DB queries:

```php
use Statamic\Facades\Entry;
use Statamic\Facades\GlobalSet;
use Statamic\Facades\Collection;
use Statamic\Facades\Term;

// Query entries from a collection
$entries = Entry::query()
    ->where('collection', 'pages')
    ->where('status', 'published')
    ->get();

// Find a single entry
$entry = Entry::find($id);

// Get a global set's values
$globalData = GlobalSet::findByHandle('footer')?->inCurrentSite()?->values();

// Collection tree (hierarchical content)
$tree = Collection::findByHandle('knowledge_base')?->structure()?->in('default');
$page = $tree->find($entryId);
$parent = $page?->parent();
```

## Field Access in Blade Templates (Critical)

Statamic injects entry fields into Blade templates. This is the **primary way data reaches templates** and how you should access it. There are two patterns:

### 1. Top-Level Variables (Most Common)

Statamic cascades all entry fields as individual Blade variables. Blueprint field handles become variable names directly:

```blade
{{-- Blueprint fields are available as top-level $variables --}}
{{ $title }}
{{ $hero_title ?? '' }}
{{ $hero_subtitle ?? '' }}

{{-- Always null-coalesce optional fields --}}
@if ($hero_intro ?? false)
    {!! $hero_intro !!}
@endif

{{-- Replicator/Bard fields are iterable --}}
@foreach ($page_content as $set)
    @include('partials.sets.' . $set->type, [...$set])
@endforeach

{{-- Pre-unwrapped blocks (from View Composers) --}}
@foreach ($blocks ?? [] as $block)
    @include("partials.sets.{$block['type']}", $block)
@endforeach
```

### 2. Via the `$page` Entry Object

The current entry is also available as `$page`. Use this for accessing the entry directly:

```blade
{{-- Dynamic property access on the entry --}}
<h1>{{ $page->title }}</h1>
<h2>{{ $page->subtitle }}</h2>

{{-- Conditionals on entry fields --}}
@if ($page->hero_title && $page->show_hero)
    @include('partials.hero')
@endif

{{-- URL and metadata --}}
<a href="{{ $page->url() }}">{{ $page->title }}</a>
```

### Which to Use

- **Top-level `$variables`** — Use for fields that may need null-coalescing or when passing to components. This is what Statamic injects by default.
- **`$page->field`** — Use when you need to access the entry object directly, check multiple fields, or when the field name might conflict with a Blade variable.
- **`$entry->get('field')`** — Use in PHP code (View Composers, helpers) to avoid PHPStan ignores.

### Important: Fields Are Value Objects

All field variables in templates are `Statamic\Fields\Value` objects, not raw PHP values. Blade's `{{ }}` syntax calls `__toString()` automatically for simple fields, but for complex fields (arrays, relationships) you must handle them explicitly:

```blade
{{-- Simple fields: Value auto-casts to string in {{ }} --}}
{{ $title }}

{{-- Complex fields: use unwrap() or check type --}}
@php $items = unwrap($usps ?? []) @endphp
@foreach ($items as $item)
    <li>{{ $item['text'] }}</li>
@endforeach
```

## Value Object Handling in PHP

In PHP code (View Composers, helpers), Statamic wraps field data in `Statamic\Fields\Value` and `Statamic\Fields\Values` objects. These must be unwrapped explicitly.

### Checking and Unwrapping Values

```php
use Statamic\Fields\Value;

// Check if a field is a Value with actual content
if ($field instanceof Value && $field->value()) {
    $raw = $field->value();  // Get the underlying data
}

// For relationship fields (entries fieldtype)
if ($entries instanceof Value && $entries->value()) {
    foreach ($entries as $entry) {
        // Each $entry is a Statamic Entry object
    }
}
```

### Field Access in PHP Code

```php
// Preferred in PHP — no PHPStan ignores needed
$value = $entry->get('field_name');

// Dynamic property access — works but needs @phpstan-ignore
$title = $entry->title;  // @phpstan-ignore property.notFound
```

## Blueprints

Blueprints are YAML files in `resources/blueprints/`. They define the field structure for collections, globals, navigations, and asset containers.

### Common Fieldtypes

| Fieldtype | Description |
|-----------|-------------|
| `text` | Single-line text |
| `textarea` | Multi-line text |
| `bard` | Rich text editor with sets |
| `replicator` | Repeatable content blocks |
| `entries` | Relationship to other entries |
| `assets` | File/image upload |
| `toggle` | Boolean |
| `select` | Dropdown |
| `color` | Color picker |
| `link` | URL or entry reference |
| `icon` | Icon picker |
| `taxonomy` | Taxonomy term relationship |
| `grid` | Table-like repeating rows |

### Blueprint Conventions

- Use `import` for shared fieldsets (e.g., `hero`, `seo`)
- Group fields into tabs: `main`, `seo`, `sidebar`
- Use `required: true` on essential fields
- Handles use `snake_case`

```yaml
tabs:
  main:
    sections:
      - fields:
          - handle: title
            field:
              type: text
              required: true
          - import: page_blocks
  seo:
    sections:
      - import: seo
```

## Content Blocks (Replicator Pattern)

Content blocks are Replicator sets rendered as Blade partials. Each block type has a corresponding partial:

```blade
@foreach ($page_content as $set)
    @include('partials.sets.' . $set->type, [...$set])
@endforeach
```

When creating a new block:
1. Add the set definition to the Replicator field in the blueprint
2. Create the Blade partial (e.g., `block_<name>.blade.php`)

## View Composers

Use View Composers to enrich Statamic template data with additional queries or transformations:

```php
use Illuminate\Contracts\View\View;
use Illuminate\View\Composer as ViewComposer;

class PageComposer implements ViewComposer
{
    public function compose(View $view): void
    {
        $data = $view->getData();

        // Transform or add data
        $view->with('extraData', $this->fetchRelated($data));
    }
}
```

Register in a ServiceProvider:

```php
View::composer('pages.show', PageComposer::class);
```

## Asset Handling

Statamic asset fields can return different types. Always handle defensively:

```php
// Asset field might be a Value, an Asset object, an array, or a string path
$asset = $entry->get('logo');

// Safe resolution patterns:
if ($asset instanceof Value) {
    $asset = $asset->value();
}

// If it's an array of assets, take the first
if (is_array($asset) && isset($asset[0])) {
    $asset = $asset[0];
}

// Get the URL
$url = $asset?->url();
```

## Navigation

Navigations are hierarchical structures for building site menus. They support entry references, hardcoded URLs, and text-only nodes — all managed via drag-and-drop in the CP.

### Storage

- **Nav definitions** → `content/navigation/<handle>.yaml` (file driver)
- **Tree data** → stored via Eloquent (`navigation_trees` driver)
- **Blueprints** → `resources/blueprints/navigation/<handle>.yaml` (file driver)

### Rendering Navs in Blade (Preferred)

**Always prefer the `<statamic:nav:handle>` Blade tag.** It handles entry resolution, URL generation, and variable scoping automatically — no manual `Nav::find()` or `resolveNavEntry()` needed for standard menus.

```blade
<ul>
    <statamic:nav:footer_main>
        <li>
            <a href="{{ $url }}" @if ($is_current || $is_parent) class="active" @endif>
                {{ $title }}
            </a>
        </li>
    </statamic:nav:footer_main>
</ul>
```

#### Available Variables Inside the Tag

| Variable | Type | Description |
|----------|------|-------------|
| `$url` | string | Resolved URL (entry URL or hardcoded) |
| `$title` | string | Item title (nav override or entry title) |
| `$is_current` | bool | Whether this is the exact current page |
| `$is_parent` | bool | Whether this is a parent of the current page |
| `$is_entry` | bool | Whether the item references an entry |
| `$is_external` | bool | Whether the URL is external |
| `$children` | array | Child nav items |
| `$depth` | int | Current nesting level |
| Custom fields | mixed | Any fields from the nav blueprint |

#### Nested Children with `@recursive_children`

For multi-level navs, use `@recursive_children` to repeat the tag contents for child items:

```blade
<ul>
    <statamic:nav:main_navigation>
        <li>
            <a href="{{ $url }}">{{ $title }}</a>
            @if (count($children))
                <ul>
                    @recursive_children
                </ul>
            @endif
        </li>
    </statamic:nav:main_navigation>
</ul>
```

#### Tag Parameters

Control output with parameters on the tag:

```blade
<statamic:nav:main_navigation
    max_depth="2"
    include_home="true"
    select="title|url"
>
    ...
</statamic:nav:main_navigation>
```

- `max_depth` — Limit nesting depth (performance optimization)
- `include_home` — Include the home page in the tree
- `show_unpublished` — Include unpublished entries
- `select` — Limit fields retrieved (pipe-separated, improves performance)

### When to Use `Nav::find()` Instead

The `<statamic:nav>` tag covers most cases. Only fall back to the PHP facade when you need to **pre-process nav data before rendering** — e.g., serializing to JSON for Alpine.js, pre-rendering icons server-side, or building complex dropdown structures:

```php
use Statamic\Facades\Nav;

$tree = Nav::find('main_navigation')?->in('default')?->tree() ?? [];
```

Each item in the tree is an array with keys: `title`, `url`, `entry` (UUID if linked), `children`, plus any custom blueprint fields. When using this approach, resolve items with the project's `resolveNavEntry()` helper:

```php
$resolved = resolveNavEntry($item);
// Returns: ['url' => '/some-page', 'title' => 'Page Title']
```

The helper checks `entry`, `reference`, `data.reference`, and `data.entry` for an entry UUID, resolves it via `Entry::find()`, and falls back to the item's `url` field.

**Note:** Custom blueprint fields may appear at the top level or under `data.*`. Defensively check both:

```php
$icon = $item['icon'] ?? ($item['data']['icon'] ?? null);
```

### Nav Config Options

In the nav definition YAML (`content/navigation/<handle>.yaml`):

```yaml
title: 'Main Navigation'
collections:          # Which collections appear in the CP entry selector
  - pages
  - integrations
max_depth: 2          # Maximum nesting depth
```

### Best Practices

- **Use `<statamic:nav>` by default** — It resolves entries, builds URLs, and provides `$is_current`/`$is_parent` automatically. Only use `Nav::find()` when you need PHP pre-processing.
- **Restrict collections** — Configure `collections` in the nav YAML to limit which entries editors can link to.
- **Set `max_depth`** — Match the frontend's rendering capability (e.g., `2` for a mega nav with one level of children).
- **Filter empty items** — After manual resolution, filter out items where title is empty (entry may have been deleted).
- **Pre-process for Alpine/JS** — When passing nav data to JavaScript, resolve entries and render server-side components (like icons) in PHP before encoding to JSON.

## Routing

Statamic handles routing via collection URLs defined in each collection's YAML config. Custom middleware can control which requests Statamic handles.

Key config: `config/statamic/routes.php`

## Artisan / Please Commands

Use `php please` for Statamic-specific operations:

```bash
php please make:collection      # Create a new collection
php please make:fieldset        # Create a reusable fieldset
php please make:nav             # Create a navigation
php please make:widget          # Create a CP dashboard widget
php please stache:refresh       # Rebuild the content cache
php please static:clear         # Clear static cache
php please support:details      # Debug Statamic setup info
```

## PHPStan Considerations

Statamic's dynamic properties trigger PHPStan errors. Common patterns:

```php
$entry->title           // @phpstan-ignore property.notFound
$entry->url()           // @phpstan-ignore method.notFound
```

Prefer `$entry->get('field_name')` in PHP code to avoid ignores. Dynamic property access is fine in Blade templates where PHPStan doesn't analyze.

## Common Pitfalls

1. **Forgetting to unwrap Values** — Statamic field data is wrapped in Value objects. Always unwrap before using in conditions or passing to components.
2. **Asset fields returning arrays** — An `assets` field may return an array even for `max_files: 1`. Handle both single and array returns.
3. **Link fields with `entry::` prefix** — Link fieldtype stores entry references as `entry::<uuid>`. Resolve via `Entry::find()`.
4. **Global sets need site context** — Always chain `->inCurrentSite()` when reading global set values for multi-site support.
5. **Tree/structure queries** — Use `Collection::findByHandle()->structure()->in('default')` for hierarchical collections, not flat `Entry::query()`.
6. **Bard content is augmented** — Bard fields return augmented HTML when accessed as Values. Use `->value()` for raw ProseMirror JSON.
7. **Component name conflicts** — When using Flux UI alongside Statamic Blade components, watch for name collisions (e.g., `header`, `footer`). Register explicit Blade aliases if needed.
