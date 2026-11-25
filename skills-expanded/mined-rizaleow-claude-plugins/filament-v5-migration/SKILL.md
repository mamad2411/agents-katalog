---
description: Migrate Filament v3/v4 code to v5 — Schemas API consolidation, `Filament\Actions` namespace move, resource signature change, `recordActions/toolbarActions` rename, extracted Schema classes. Use when upgrading to Filament v5 or when v3/v4 idioms appear in code being edited.
---

# Filament v4 → v5 migration

Filament v5 is a coordinated API shift: forms+infolists+layouts unify under `Filament\Schemas`, actions consolidate under `Filament\Actions`, and resource methods change signatures. The lint+upgrade tools below detect and rewrite the high-confidence cases.

## Preflight

1. `composer show filament/filament` — confirm `^5.0`.
2. `mcp__boost__filament_lint --path app/Filament` — list every v3/v4 holdover.
3. `mcp__boost__filament_upgrade_suggest --path app/Filament` — diff of safe AST rewrites; apply with user approval.

Always commit before applying suggestions.

## Top 8 migration patterns

| # | v3 / v4 | v5 |
| --- | --- | --- |
| 1 | `use Filament\Forms\Form;` `public static function form(Form $form): Form` | `use Filament\Schemas\Schema;` `public static function form(Schema $schema): Schema` |
| 2 | `$form->schema([...])` inside resource | extract: `return CustomerForm::configure($schema);` |
| 3 | `use Filament\Tables\Actions\EditAction;` | `use Filament\Actions\EditAction;` |
| 4 | `$table->actions([EditAction::make()])` | `$table->recordActions([EditAction::make()])` |
| 5 | `$table->bulkActions([DeleteBulkAction::make()])` | `$table->toolbarActions([BulkActionGroup::make([DeleteBulkAction::make()])])` |
| 6 | `use Filament\Infolists\Infolist;` `public static function infolist(Infolist $infolist)` | `use Filament\Schemas\Schema;` `public static function infolist(Schema $schema): Schema` |
| 7 | `use Filament\Forms\Components\Section;` (layout) | `use Filament\Schemas\Components\Section;` |
| 8 | `Action::make('x')->form([TextInput::make('y')])` | `Action::make('x')->schema(fn (Schema $s) => $s->components([TextInput::make('y')]))` |

## Detection cues (instant red flags)

When reading code, treat these as v4 leftovers and migrate:

- Any import from `Filament\Tables\Actions\*` or `Filament\Pages\Actions\*`.
- `Form $form` or `Infolist $infolist` typehints on Resource methods.
- `->actions([` or `->bulkActions([` chained on a `Table`.
- `getFormSchema()` method on a Resource (deprecated).
- `Filament\Forms\Components\{Grid,Section,Tabs,Fieldset,Wizard}` imports — these moved to `Filament\Schemas\Components\*`.
- Layout components called via static `Section::make()->schema()` inside a `->form([])` array literal in the resource itself (extract to a Schema class).

## Before / after — resource

Before (v4):

```php
use Filament\Forms\Form;
use Filament\Tables\Actions\{EditAction, DeleteBulkAction};

public static function form(Form $form): Form
{
    return $form->schema([
        TextInput::make('name')->required(),
    ]);
}

public static function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->actions([EditAction::make()])
        ->bulkActions([DeleteBulkAction::make()]);
}
```

After (v5):

```php
use App\Filament\Resources\Customers\Schemas\CustomerForm;
use App\Filament\Resources\Customers\Tables\CustomersTable;
use Filament\Schemas\Schema;

public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}

public static function table(Table $table): Table
{
    return CustomersTable::configure($table);
}
```

```php
// Tables/CustomersTable.php
use Filament\Actions\{EditAction, BulkActionGroup, DeleteBulkAction};

class CustomersTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([...])
            ->recordActions([EditAction::make()])
            ->toolbarActions([
                BulkActionGroup::make([DeleteBulkAction::make()]),
            ]);
    }
}
```

## Migration workflow

1. Branch: `git checkout -b filament-v5`.
2. Bump composer: `composer require filament/filament:^5.0 -W` and resolve peers.
3. `mcp__boost__filament_lint` — capture baseline.
4. `mcp__boost__filament_upgrade_suggest` — apply rewrites file-by-file with `git add -p`.
5. Per resource: extract `Schemas/<Model>Form.php` and `Tables/<Models>Table.php` even if v4 inlined them — keeps future churn down.
6. Run Pest. Most assertion helpers (`fillForm`, `callTableAction`, `assertSchemaStateSet`) are v5-stable; failing tests usually point at namespace imports in your own code.
7. Re-run lint until clean.

## Out of scope for the tool

- Custom Blade views that referenced the old `$component` API in form fields — needs manual review.
- Heavily customized panel themes — re-publish the v5 theme stub via `php artisan filament:install --panels`.
- Third-party plugins — check each plugin's release notes; v4 plugins rarely run on v5 unchanged.

See also: filament-resources, filament-schemas, filament-tables, filament-actions.
