---
description: Build and refactor Filament v5 Resource classes — `static form(Schema $schema)`, `static table(Table $table)`, page list, extracted `Schemas/` and `Tables/` subfolders, model binding, navigation, policies. Use when creating, modifying, or refactoring a Filament v5 Resource class.
---

# Filament v5 Resources

A Resource is a CRUD surface bound to an Eloquent model. In v5 the resource file should stay thin — schemas and tables get extracted into sibling classes.

## Preflight

- `mcp__boost__filament_list_resources` — see what already exists, avoid duplicates.
- `mcp__boost__filament_inspect_resource --resource App\\Filament\\Resources\\Customers\\CustomerResource` — read current shape before editing.
- For new resources, prefer `mcp__boost__filament_scaffold_resource --model App\\Models\\Customer` (returns a diff, you apply with Edit/Write).

## Directory layout

```
app/Filament/Resources/Customers/
├── CustomerResource.php
├── Pages/
│   ├── ListCustomers.php
│   ├── CreateCustomer.php
│   └── EditCustomer.php
├── Schemas/
│   ├── CustomerForm.php
│   └── CustomerInfolist.php
└── Tables/
    └── CustomersTable.php
```

Pluralised model folder, singular class names. Pages are full-page Livewire components.

## Canonical resource file

```php
namespace App\Filament\Resources\Customers;

use App\Filament\Resources\Customers\Pages;
use App\Filament\Resources\Customers\Schemas\CustomerForm;
use App\Filament\Resources\Customers\Schemas\CustomerInfolist;
use App\Filament\Resources\Customers\Tables\CustomersTable;
use App\Models\Customer;
use BackedEnum;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;
use Filament\Tables\Table;

class CustomerResource extends Resource
{
    protected static ?string $model = Customer::class;

    protected static string | BackedEnum | null $navigationIcon = Heroicon::OutlinedUserGroup;

    protected static ?string $recordTitleAttribute = 'name';

    public static function form(Schema $schema): Schema
    {
        return CustomerForm::configure($schema);
    }

    public static function infolist(Schema $schema): Schema
    {
        return CustomerInfolist::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return CustomersTable::configure($table);
    }

    public static function getPages(): array
    {
        return [
            'index'  => Pages\ListCustomers::route('/'),
            'create' => Pages\CreateCustomer::route('/create'),
            'edit'   => Pages\EditCustomer::route('/{record}/edit'),
        ];
    }
}
```

## Extracted schema class

```php
namespace App\Filament\Resources\Customers\Schemas;

use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

class CustomerForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema->components([
            Section::make('Identity')->schema([
                TextInput::make('name')->required(),
                TextInput::make('email')->email()->unique(ignoreRecord: true),
            ])->columns(2),
        ]);
    }
}
```

## Rules

- Resource file holds **only** wiring: `$model`, navigation, `form/table/infolist/getPages`. Move everything else out.
- Eloquent query mods → `static getEloquentQuery(): Builder` on the resource.
- Authorization → bind a `Policy` to the model; Filament respects it automatically. Override `static canViewAny()` only for non-policy cases.
- Global search → `static getGloballySearchableAttributes(): array` + `static getGlobalSearchResultDetails($record): array`.
- Tenant scoping → return `parent::getEloquentQuery()` (the parent already applies tenant constraints when the panel uses `->tenant()`).

## When to split further

| Sign | Action |
| --- | --- |
| `form()` body > 30 lines | Extract `Schemas/<Model>Form.php`. |
| Same fields used in a modal action | Extract reusable static methods. |
| Table columns/filters > 20 lines | Extract `Tables/<Models>Table.php`. |
| Custom create/edit logic | Override `mutateFormDataBeforeCreate` on the Page, not the Resource. |

See also: filament-schemas, filament-tables, filament-actions, filament-testing.
