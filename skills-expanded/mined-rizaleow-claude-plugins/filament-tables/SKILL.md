---
description: Build Filament v5 Tables — columns (Text/Icon/Image/Color), filters, search, sorting, grouping, `recordActions()` and `toolbarActions()`, query modifiers, defaults. Use when defining or modifying a Filament v5 table (columns, filters, grouping, row/bulk actions).
---

# Filament v5 Tables

`Filament\Tables\Table` configures the listing surface for a Resource (or a `TableWidget`/`HasTable` page). Actions inside a Table come from `Filament\Actions\*`, **never** `Filament\Tables\Actions\*` (that namespace is v4).

## Imports

```php
use Filament\Tables\Table;
use Filament\Tables\Columns\{TextColumn, IconColumn, ImageColumn, ColorColumn, ToggleColumn, SelectColumn};
use Filament\Tables\Filters\{Filter, SelectFilter, TernaryFilter, QueryBuilder, TrashedFilter};
use Filament\Tables\Grouping\Group;
use Filament\Actions\{Action, EditAction, DeleteAction, ViewAction, BulkActionGroup, DeleteBulkAction};
```

## Skeleton

```php
public static function configure(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('name')->searchable()->sortable(),
            TextColumn::make('email')->searchable()->copyable(),
            TextColumn::make('status')
                ->badge()
                ->color(fn (string $state): string => match ($state) {
                    'active' => 'success',
                    'paused' => 'warning',
                    default  => 'gray',
                }),
            IconColumn::make('is_verified')->boolean(),
            ImageColumn::make('avatar_url')->circular(),
            TextColumn::make('created_at')->dateTime()->since()->sortable(),
        ])
        ->filters([
            SelectFilter::make('status')->options([
                'active' => 'Active',
                'paused' => 'Paused',
            ]),
            TernaryFilter::make('is_verified'),
            TrashedFilter::make(),
        ])
        ->recordActions([
            ViewAction::make(),
            EditAction::make(),
            DeleteAction::make(),
        ])
        ->toolbarActions([
            BulkActionGroup::make([
                DeleteBulkAction::make(),
            ]),
        ])
        ->defaultSort('created_at', 'desc')
        ->striped()
        ->deferLoading();
}
```

## Columns

- `->searchable()` — global search. `->searchable(isIndividual: true)` for per-column input.
- `->sortable()` — DB-side sort. Pass a closure for custom: `->sortable(query: fn (Builder $q, $dir) => $q->orderBy(...))`.
- `->formatStateUsing(fn ($state) => Number::currency($state, 'USD'))`.
- `->badge()`, `->numeric()`, `->money('USD')`, `->dateTime()`, `->date()`, `->since()` — display helpers.
- `->toggleable(isToggledHiddenByDefault: true)` — user-toggle visibility.
- `->wrap()`, `->limit(50)`, `->tooltip(fn ($state) => $state)`.

## Filters

- `Filter::make('verified')->query(fn (Builder $q) => $q->whereNotNull('verified_at'))`.
- `SelectFilter::make('author_id')->relationship('author', 'name')->multiple()->preload()`.
- `QueryBuilder::make()->constraints([...])` — power-user filter UI.
- `->filtersLayout(FiltersLayout::AboveContent)` — render filters above table instead of in a modal.

## Grouping

```php
->groups([
    Group::make('status')->collapsible(),
    Group::make('created_at')->date(),
])
->defaultGroup('status')
```

## Query modifiers

- `->modifyQueryUsing(fn (Builder $q) => $q->with('author'))` — eager loads, soft scope.
- Authorization-scoped data → override `static getEloquentQuery()` on the Resource instead.

## Pagination & defaults

- `->paginated([10, 25, 50, 100])`.
- `->persistFiltersInSession()`, `->persistSearchInSession()`, `->persistSortInSession()`.
- `->poll('10s')` — auto-refresh for live dashboards.

## Reorderable rows

```php
->reorderable('sort_order')
->defaultSort('sort_order')
```

## Tools

- `mcp__boost__filament_inspect_resource` shows the current table columns/filters/actions.
- `mcp__boost__filament_lint` flags v4-style `->actions([...])` / `->bulkActions([...])` usage.

See also: filament-resources, filament-actions, filament-schemas, filament-testing.
