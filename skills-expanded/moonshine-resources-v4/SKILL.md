---
name: moonshine-resources-v4
description: Use when working on MoonShine v4 ModelResource, CrudResource, CRUD operations, pages, tables, forms, filters, search, query tags, pagination, events, buttons, import/export, metrics, or response modifiers.
---

# MoonShine v4 -- ModelResource

## Overview

`ModelResource` is the primary building block for admin panel sections backed by Eloquent models. It extends `CrudResource` and provides full CRUD functionality.

**KEY V4 CHANGE: Page-Centric Architecture.** In v4, many methods that previously lived on the resource class have moved to dedicated page classes (`IndexPage`, `FormPage`, `DetailPage`). Resources declare pages; pages own their fields, filters, buttons, metrics, validation, and component modifiers.

## Creating a Resource

```bash
php artisan moonshine:resource Post
```

This generates a resource class plus three page classes (`PostIndexPage`, `PostFormPage`, `PostDetailPage`).

## Core Properties

```php
namespace App\MoonShine\Resources\Post;

use App\Models\Post;
use MoonShine\Laravel\Resources\ModelResource;

/**
 * @extends ModelResource<Post>
 */
class PostResource extends ModelResource
{
    protected string $model = Post::class;
    protected string $title = 'Posts';
    protected array $with = ['category'];          // eager load
    protected string $column = 'id';               // display column for breadcrumbs/relations
    protected ?string $alias = null;               // custom URL alias
}
```

## Page-Centric Architecture (v4 Key Change)

Resources declare their page classes in `pages()`. Each page owns its fields, filters, metrics, buttons, validation, and component modifiers.

```php
class PostResource extends ModelResource
{
    protected function pages(): array
    {
        return [
            PostIndexPage::class,
            PostFormPage::class,
            PostDetailPage::class,
        ];
    }
}
```

### What Moved from Resource to Pages

| v3 (on Resource)                | v4 (on Page class)                              |
|---------------------------------|-------------------------------------------------|
| `rules()`                       | `rules()` on `FormPage`                         |
| `validationMessages()`          | `validationMessages()` on `FormPage`            |
| `prepareForValidation()`        | `prepareForValidation()` on `FormPage`          |
| `modifyFormComponent()`         | `modifyFormComponent()` on `FormPage`           |
| `filters()`                     | `filters()` on `IndexPage`                      |
| `metrics()`                     | `metrics()` on `IndexPage`                      |
| `queryTags()`                   | `queryTags()` on `IndexPage`                    |
| `modifyListComponent()`         | `modifyListComponent()` on `IndexPage`          |
| `modifyDetailComponent()`       | `modifyDetailComponent()` on `DetailPage`       |
| `topButtons()`                  | `topLeftButtons()` / `topRightButtons()` on `IndexPage` |
| `indexButtons()`                | `buttons()` on `IndexPage`                      |
| `formButtons()`                 | `buttons()` on `FormPage`                       |
| `formBuilderButtons()`          | `formButtons()` on `FormPage`                   |

### Properties Removed from Resource

Use `modifyListComponent()` on `IndexPage` instead of these removed resource properties:

- `$clickAction`, `$stickyTable`, `$stickyButtons`, `$columnSelection`

```php
class PostIndexPage extends IndexPage
{
    protected function modifyListComponent(ComponentContract $component): ComponentContract
    {
        return $component->sticky()->stickyButtons()->columnSelection();
    }
}
```

## Declaring in the System

Resources are auto-registered when using `php artisan moonshine:resource`. Manual registration in `MoonShineServiceProvider`:

```php
public function boot(CoreContract $core, ConfiguratorContract $config): void
{
    $core->resources([PostResource::class])->pages([...$config->getPages()]);
}
```

Autoloading: `$core->autoload();`

## Resource Properties

```php
// Sorting
protected string $sortColumn = 'created_at';
protected string $sortDirection = 'DESC';

// Pagination
protected int $itemsPerPage = 25;
protected bool $simplePaginate = false;
protected bool $cursorPaginate = false;

// Async mode (enabled by default, disable on resource or page)
protected bool $isAsync = false;

// Lazy loading (on IndexPage)
protected bool $isLazy = true;
```

### Modal Windows

```php
protected bool $createInModal = true;
protected bool $editInModal = true;
protected bool $detailInModal = true;
```

Modal modifiers: `modifyCreateModal()`, `modifyEditModal()`, `modifyDetailModal()`, `modifyDeleteModal()`, `modifyMassDeleteModal()`, `modifyFiltersOffCanvas()`.

### Redirects

```php
use MoonShine\Support\Enums\PageType;

protected ?PageType $redirectAfterSave = PageType::FORM;

public function getRedirectAfterSave(): string { return '/'; }
public function getRedirectAfterDelete(): string { return $this->getIndexPageUrl(); }
```

### Active Actions

```php
use MoonShine\Support\Enums\Action;
use MoonShine\Support\ListOf;

protected function activeActions(): ListOf
{
    return parent::activeActions()->except(Action::VIEW, Action::MASS_DELETE);
}
```

Available: `Action::CREATE`, `Action::VIEW`, `Action::UPDATE`, `Action::DELETE`, `Action::MASS_DELETE`.

## Fields in Resources

In v4, fields are declared on the page classes, not on the resource.

```php
class PostIndexPage extends IndexPage
{
    protected function fields(): iterable
    {
        return [ID::make()->sortable(), Text::make('Title')];
    }
}

class PostFormPage extends FormPage
{
    protected function fields(): iterable
    {
        return [Box::make([ID::make(), Text::make('Title')->required()])];
    }
}
```

## Query Modification

Stays on the resource:

```php
protected function modifyQueryBuilder(Builder $builder): Builder
{
    return $builder->where('active', true);
}

protected function modifyItemQueryBuilder(Builder $builder): Builder
{
    return $builder->withTrashed();
}
```

## Query Tags (New in v4)

Defined on `IndexPage`. Quick-filter buttons displayed above the table.

```php
class PostIndexPage extends IndexPage
{
    protected function queryTags(): array
    {
        return [
            QueryTag::make('With author', fn(Builder $query) => $query->whereNotNull('author_id'))
                ->icon('users')->default(),
            QueryTag::make('Archived', fn(Builder $query) => $query->where('is_archived', true))
                ->alias('archive'),
        ];
    }
}
```

See `references/filters-search-querytags.md` for full details.

## Filters & Search

Filters are now on `IndexPage`:

```php
class PostIndexPage extends IndexPage
{
    protected function filters(): iterable
    {
        return [Text::make('Title', 'title')];
    }
}
```

Search stays on the resource:

```php
protected function search(): array { return ['id', 'title', 'text']; }
```

Cache filter state: `protected bool $saveQueryState = true;`

See `references/filters-search-querytags.md` for full-text, JSON, relation search, and global search.

## Metrics

Defined on `IndexPage`:

```php
class PostIndexPage extends IndexPage
{
    protected function metrics(): array
    {
        return [
            ValueMetric::make('Articles')->value(fn() => Post::count())->columnSpan(6),
        ];
    }
}
```

## Buttons

In v4, buttons are defined on page classes.

```php
// IndexPage: topLeftButtons/topRightButtons for above-table, buttons() for per-row
class PostIndexPage extends IndexPage
{
    protected function topLeftButtons(): ListOf
    {
        return parent::topLeftButtons()->add(
            ActionButton::make('Refresh', '#')
                ->dispatchEvent(AlpineJs::event(JsEvent::TABLE_UPDATED, $this->getListComponentName()))
        );
    }

    protected function buttons(): ListOf
    {
        return parent::buttons()->prepend(
            ActionButton::make('Link', fn(Model $item) => '/endpoint?id=' . $item->getKey())
        );
    }
}

// FormPage: buttons() for page-level, formButtons() for inside-form
class PostFormPage extends FormPage
{
    protected function formButtons(): ListOf
    {
        return parent::formButtons()->add(
            ActionButton::make('Back', fn() => $this->getIndexPageUrl())->class('btn-lg')
        );
    }
}
```

See `references/events-buttons.md` for full button reference.

## Import/Export

Requires `moonshine/import-export` package:

```php
use MoonShine\ImportExport\Contracts\HasImportExportContract;
use MoonShine\ImportExport\Traits\ImportExportConcern;

class PostResource extends ModelResource implements HasImportExportContract
{
    use ImportExportConcern;
    protected function importFields(): iterable { return [ID::make(), Text::make('Title')]; }
    protected function exportFields(): iterable { return [ID::make(), Text::make('Title')]; }
}
```

See `references/events-buttons.md` for handler configuration.

## Events & Lifecycle

Resource CRUD events (stays on the resource, v4 uses `DataWrapperContract`):

```php
use MoonShine\Contracts\Core\TypeCasts\DataWrapperContract;

protected function beforeCreating(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function afterCreated(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function beforeUpdating(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function afterUpdated(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function beforeDeleting(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function afterDeleted(DataWrapperContract $item): DataWrapperContract { return $item; }
protected function beforeMassDeleting(array $ids): void {}
protected function afterMassDeleted(array $ids): void {}
```

Resource lifecycle: `onLoad()` (resource active), `onBoot()` (instance created).
Page lifecycle: `onLoad()`, `booted()`.

## Response Modifiers

```php
use MoonShine\Crud\JsonResponse;

public function modifySaveResponse(JsonResponse $response): JsonResponse { return $response; }
public function modifyDestroyResponse(JsonResponse $response): JsonResponse { return $response; }
public function modifyMassDeleteResponse(JsonResponse $response): JsonResponse { return $response; }
public function modifyErrorResponse(Response $response, Throwable $exception): Response { return $response; }
```

## CRUD Operation Handlers (New in v4)

Override save/delete/mass-delete logic using attributes:

```php
use MoonShine\Crud\Attributes\SaveHandler;
use MoonShine\Crud\Attributes\DestroyHandler;
use MoonShine\Crud\Attributes\MassDestroyHandler;

#[SaveHandler(PostHandlers::class, 'save')]
#[DestroyHandler(PostHandlers::class, 'destroy')]
#[MassDestroyHandler(PostHandlers::class, 'massDestroy')]
class PostResource extends ModelResource { }
```

```php
final readonly class PostHandlers
{
    public function save(Post $model, array $data): Post
    {
        $model->fill($data);
        $model->save();
        return $model;
    }
    public function destroy(Post $model): bool { return $model->delete(); }
    public function massDestroy(array $ids): void
    {
        Post::query()->whereKey($ids)->each->delete();
    }
}
```

## Authorization

```php
protected bool $withPolicy = true;
```

Policy methods: `viewAny`, `view`, `create`, `update`, `delete`, `massDelete`, `restore`, `forceDelete`. Generate: `php artisan moonshine:policy PostPolicy`.

## Routes Helper

```php
$resource->getUrl();                        // first page
$resource->getIndexPageUrl();               // index page
$resource->getFormPageUrl();                // create page
$resource->getFormPageUrl(1);               // edit page by ID
$resource->getDetailPageUrl(1);             // detail page by ID
$resource->getAsyncMethodUrl('method');     // async method URL
$resource->getRoute('crud.update', $id);    // CRUD routes
$resource->getActivePage();                 // current active page or null
```

## Cross-References

- For field types and relationship fields, see the `moonshine-fields-v4` skill.
- For ActionButton advanced usage, see the `moonshine-components-v4` skill.
- For Layout and menu configuration, see the `moonshine-appearance-v4` skill.
- For TableBuilder and FormBuilder components, see the `moonshine-components-v4` skill.
- Detailed CRUD page customization: `references/crud-pages.md`
- Filters, search, query tags: `references/filters-search-querytags.md`
- Events, buttons, import/export, metrics: `references/events-buttons.md`
