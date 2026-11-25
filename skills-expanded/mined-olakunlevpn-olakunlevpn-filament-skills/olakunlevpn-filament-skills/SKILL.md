---
name: olakunlevpn-filament-skills
description: Use when writing, reviewing, or refactoring Filament PHP v5 code -- resources, forms, tables, infolists, actions, widgets, panels, relation managers, multi-tenancy, testing, or plugin development. Always apply these standards to all Filament work.
---

# Filament PHP v5 Coding Standards

Comprehensive standards for building production-grade Filament v5 admin panels. Filament v5 requires PHP 8.3+, Laravel 13+, Livewire 4+, Tailwind CSS 4.1+. Follow these rules exactly. For detailed code examples, see REFERENCE.md.

## When to Apply

Apply to ALL Filament work: resources, forms, tables, infolists, actions, widgets, dashboards, panels, relation managers, imports/exports, custom pages, multi-tenancy, testing, and deployment.

---

## 1. Project Structure

### Directory Layout
- Domain-grouped, plural-named: `Resources/Shop/`, `Resources/Blog/`, `Resources/HR/`
- Resources in plural directories: `Resources/Shop/Products/ProductResource.php`
- Schemas extracted: `Resources/Shop/Products/Schemas/ProductSchema.php`
- Tables extracted: `Resources/Shop/Products/Tables/ProductsTable.php`
- Multiple panels: `Providers/Filament/AdminPanelProvider.php`, `AppPanelProvider.php`

### Resource Complexity Tiers
- **Simple** (ManageRecords) -- modal CRUD, single page, no relation managers
- **Standard** (List+Create+Edit) -- separate pages, basic CRUD
- **Full** (List+Create+Edit+View) -- sub-navigation, relation managers, widgets

### Naming Rules
- Plural resource directories: `Products/`, not `Product/`
- File names match class names: `ProductResource.php`
- Slugs kebab-case: `order-items`
- Namespace matches directory path exactly

---

## 2. Resource Architecture

### Delegation Pattern
Resources delegate to dedicated Schema and Table classes. Keep resource classes slim.

```php
class ProductResource extends Resource
{
    protected static ?string $model = Product::class;
    protected static ?string $slug = 'products';
    protected static ?string $recordTitleAttribute = 'name';
    protected static string|BackedEnum|null $navigationIcon = Heroicon::OutlinedShoppingBag;
    protected static ?string $navigationGroup = 'Shop';
    protected static ?int $navigationSort = 1;

    public static function form(Schema $schema): Schema
    {
        return ProductSchema::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return ProductsTable::configure($table);
    }
}
```

### Key Rules
- Always set `$recordTitleAttribute` for global search
- Navigation icons: always `Heroicon::Outlined*` (not Solid for nav)
- Use `Heroicon` enum, never string icon names
- All actions import from `Filament\Actions\*` namespace only
- Table methods: `recordActions()` not `actions()`, `groupedBulkActions()` not `bulkActions()`

---

## 3. Form Design

- Top-level: `$schema->components([...])` with `Section` wrapping
- Section from `Filament\Schemas\Components\Section`
- Layout components (Section, Grid, Tabs, Flex) from `Filament\Schemas\Components\*`
- Slug fields: `->live(onBlur: true)`, create-only via `Operation::Create`, `->disabled()->dehydrated()`
- Selects with relationships: always `->searchable()` and `->preload()`
- File uploads: set `->disk()`, `->directory()`, `->visibility()`
- Use `Operation` enum for conditional logic: `Operation::Create`, `Operation::Edit`
- Repeaters for line items with calculated fields
- Tabs for complex multi-section forms
- All text labels via language files, never hardcoded

---

## 4. Table Design

- Columns: TextColumn, IconColumn (booleans), BadgeColumn (enums), ImageColumn
- Toggleable columns: `->toggleable(isToggledHiddenByDefault: true)` for less important columns
- Filters: SelectFilter, TernaryFilter (boolean), date range via custom filter
- Actions wrapped in `ActionGroup`: View, Edit, Delete grouped
- Bulk actions via `groupedBulkActions()`: delete, export, status change
- Toolbar actions via `toolbarActions()`: create, import, export
- Default sort: `->defaultSort('created_at', 'desc')`
- Searchable columns: `->searchable()` on key text columns
- Money: `->money('USD')` or `->formatStateUsing()` for custom formatting

---

## 5. Infolist (View) Patterns

- Entry types: TextEntry, IconEntry (boolean), ImageEntry, BadgeEntry (enum)
- Inline labels for compact display: `->inlineLabel()`
- Rich content: `->prose()->markdown()` for formatted text
- Tabs for complex view pages
- Contextual actions on view pages with visibility conditions
- Key-value entries for metadata

---

## 6. Enum Design System

Every status/type/category uses a PHP 8.1 backed string enum implementing Filament contracts:
- `HasLabel` -- display name
- `HasColor` -- semantic color
- `HasIcon` -- Heroicon

**Semantic colors:** success (positive), danger (negative), warning (caution), info (new), primary (special), gray (neutral)

**Naming:** PascalCase case names, snake_case backed values. Cast in model: `'status' => OrderStatus::class`

---

## 7. Actions & Notifications

- All actions: `Filament\Actions\Action`, `Filament\Actions\CreateAction`, etc.
- Never import from `Filament\Tables\Actions\*` (removed in v5)
- Action modals use `->schema()` not `->form()`
- ActionGroup ordering: View, Edit, Delete (most common first)
- Notifications: `Notification::make()->title()->success()->send()`
- Refresh after action: `$this->dispatch('$refresh')` or return redirect
- Bulk actions: `->authorizeIndividualRecords()` for policy-gated bulk operations

---

## 8. Relation Managers

- Standard: extend `RelationManager`, define `form()` and `table()`
- Alternative: `ManageRelatedRecords` page for complex relations
- Action placement: `headerActions` (create), `recordActions` (per row), `groupedBulkActions` (selected)
- Reuse across resources when the same relation appears in multiple places
- Default sort on related records

---

## 9. Widgets & Dashboards

- **StatsOverview**: multiple stat cards, optional inline charts, descriptions, icons
- **Chart widgets**: line, bar, doughnut, pie -- extend `ChartWidget`
- **Lazy loading**: on by default (`$isLazy = true`)
- **Polling**: default 5s, customize via `$pollingInterval` or `null` to disable
- **Dashboard filters**: implement `HasFiltersForm` for filterable dashboards
- **Resource page widgets**: use `ExposesTableToWidgets` trait
- Widget sort order via `$sort` property

---

## 10. Multi-Tenancy

- Panel: `->tenant(Team::class)` in PanelProvider
- User model: implement `HasTenants` with `getTenants()` and `canAccessTenant()`
- Automatic query scoping on all resources (opt-out with `$isScopedToTenant = false`)
- **CRITICAL**: Form selects are NOT auto-scoped -- add `modifyQueryUsing` with `Filament::getTenant()`
- Validation: use `->scopedUnique()` and `->scopedExists()` for tenant-aware rules
- Domain-based: `->tenantDomain('{tenant:slug}.example.com')`
- Path-based with slug: `->tenant(Team::class, slugAttribute: 'slug')`
- Registration page: extend `RegisterTenant`
- Profile page: extend `EditTenantProfile`

---

## 11. Multi-Panel Architecture

- Separate PanelProvider per panel (admin, app, vendor)
- Each panel: own auth, resources, pages, widgets, middleware, theme
- `FilamentUser::canAccessPanel()` controls per-panel access
- Shared config via Plugin class or static helper
- `Filament::setCurrentPanel('app')` for testing non-default panels

---

## 12. Custom Pages & Clusters

- Custom pages: `php artisan make:filament-page Settings`
- Access control: `canAccess()` method
- Header actions, header/footer widgets, widget data passing
- Clusters: group related pages under sub-navigation
- `SubNavigationPosition::Top` for horizontal tabs
- Resource sub-navigation: `getRecordSubNavigation()` for View/Edit/Related pages

---

## 13. Testing (Pest + Livewire)

- Test via `livewire(PageClass::class)` -- pages are Livewire components
- Auth: `actingAs(User::factory()->create())` in `beforeEach`
- Multi-tenant: `Filament::setTenant($team)` + `Filament::bootCurrentPanel()`
- Multi-panel: `Filament::setCurrentPanel('admin')`

**Key test patterns:**
- List: `->assertCanSeeTableRecords()`, `->searchTable()`, `->sortTable()`, `->filterTable()`
- Create: `->fillForm([...])->call('create')->assertHasNoFormErrors()->assertNotified()`
- Edit: `->assertSchemaStateSet([...])->fillForm([...])->call('save')`
- Actions: `->callAction(TestAction::make('send')->table($record))`
- Bulk: `->selectTableRecords($ids)->callAction(TestAction::make('delete')->table()->bulk())`
- Relations: `livewire(RelationManager::class, ['ownerRecord' => $record, 'pageClass' => EditPage::class])`

---

## 14. Import & Export

- Exporter: `ExportColumn` definitions, placed in `app/Filament/Exports/`
- Importer: `ImportColumn` with rules, examples, casting, relationship resolution
- Actions: `ExportAction::make()`, `ImportAction::make()` in toolbar
- Record resolution: `firstOrNew`, `new Model`, or `null` to skip

---

## 15. Authorization

- `FilamentUser` interface required in production (APP_ENV != local)
- Model policies auto-discovered: `viewAny`, `create`, `update`, `delete`, `restore`, `forceDelete`, `reorder`
- Skip authorization: `$shouldSkipAuthorization = true`
- Bulk action authorization: `->authorizeIndividualRecords()`
- Per-panel access: `canAccessPanel(Panel $panel)` with panel ID check

---

## 16. Performance & Deployment

**Production:**
```
php artisan optimize
php artisan filament:optimize
```

**Panel config:**
- `->spa()` for SPA mode
- `->unsavedChangesAlerts()` for data protection
- `->databaseTransactions()` for action safety

**Widgets:** Lazy by default. Set polling interval or `null` to disable. Use `wire:init` for deferred API loads.

**Never run `filament:optimize` in local dev** -- new components won't be discovered.

**Tailwind v4:** CSS-based config via Vite plugin. No `tailwind.config.js`. Use `@source` directives.

---

## 17. Livewire 4 Features (via Filament v5)

- **Islands**: isolated re-render regions with `@island` directive
- **Async actions**: `#[Async]` attribute for fire-and-forget (analytics, logging)
- **wire:model.deep**: required when relying on child element event bubbling
- **wire:sort**: built-in drag-and-drop without external packages
- **Parallel requests**: `wire:model.live` no longer blocks
- **Self-closing tags required**: `<livewire:component />`

---

## 18. Strict Rules

- Never publish Blade views. Use CSS hooks with `fi-` prefix.
- Never hardcode brand names, logos, currency. Use dynamic settings.
- All user-facing text through language files and translation keys.
- `$recordTitleAttribute` set on every resource.
- Action modals: `->schema()` not `->form()`
- Table: `recordActions()` not `actions()`, `groupedBulkActions()` not `bulkActions()`
- Schema: `$schema->components([...])` at top level
- Icons: `Heroicon::` enum only, never string names
- Operation: `Operation::Create`, `Operation::Edit`, never string comparisons

## Summary Checklist

- [ ] Resource delegates to Schema and Table classes
- [ ] `$recordTitleAttribute` set on every resource
- [ ] `Heroicon::` enum for all icons, `Outlined` for navigation
- [ ] All actions from `Filament\Actions\*` namespace
- [ ] Table uses `recordActions()`, `groupedBulkActions()`, `toolbarActions()`
- [ ] Enums implement HasLabel, HasColor, HasIcon with semantic colors
- [ ] Form selects are searchable and preloaded
- [ ] Multi-tenant form selects manually scoped to tenant
- [ ] `FilamentUser` interface implemented with `canAccessPanel()`
- [ ] Model policies for authorization on every resource
- [ ] `filament:optimize` in production deploy script
- [ ] Tests use `livewire()` with `Filament::setTenant()` for multi-tenant
- [ ] No hardcoded text -- all through language files
- [ ] No published Blade views -- CSS hooks only
