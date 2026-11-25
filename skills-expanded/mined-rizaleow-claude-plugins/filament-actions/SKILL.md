---
description: Author Filament v5 Actions — row, bulk, header, and page actions from the unified `Filament\Actions` namespace, with modal schemas, confirmations, authorization, and extracted action classes. Use when creating, modifying, or refactoring Filament v5 actions (record, header, toolbar, bulk, or modal).
---

# Filament v5 Actions

All actions in v5 live under `Filament\Actions\*`. The legacy `Filament\Tables\Actions\*` and `Filament\Pages\Actions\*` namespaces are **gone** — using them is a v4 bug.

## Imports

```php
use Filament\Actions\{Action, EditAction, ViewAction, DeleteAction, CreateAction, ReplicateAction, RestoreAction, ForceDeleteAction};
use Filament\Actions\{BulkActionGroup, BulkAction, DeleteBulkAction, RestoreBulkAction, ForceDeleteBulkAction};
use Filament\Actions\ActionGroup;
```

## Where they go

| Surface | Method |
| --- | --- |
| Table row | `->recordActions([...])` on `Table` |
| Table footer (bulk) | `->toolbarActions([BulkActionGroup::make([...])])` |
| Resource page header | `protected function getHeaderActions(): array` on the Page |
| Schema components (e.g. Repeater item button) | `->extraItemActions([Action::make(...)])` |
| Modal nested | `->extraModalFooterActions([Action::make(...)])` |

## Built-in actions

```php
EditAction::make();          // opens the resource form in a modal on the index page
ViewAction::make()->infolist(fn (Schema $schema) => CustomerInfolist::configure($schema));
DeleteAction::make()->requiresConfirmation();
ReplicateAction::make()->excludeAttributes(['email']);
```

## Custom action with modal schema

```php
use Filament\Actions\Action;
use Filament\Forms\Components\{Select, Textarea};
use Filament\Schemas\Schema;
use Filament\Support\Icons\Heroicon;

Action::make('send_invoice')
    ->icon(Heroicon::OutlinedPaperAirplane)
    ->color('primary')
    ->requiresConfirmation()
    ->schema(fn (Schema $schema): Schema => $schema->components([
        Select::make('template')->options(['standard' => 'Standard', 'late' => 'Late notice'])->required(),
        Textarea::make('note')->rows(4),
    ]))
    ->action(function (array $data, Customer $record): void {
        $record->sendInvoice($data['template'], $data['note'] ?? null);
    })
    ->successNotificationTitle('Invoice sent');
```

Use `->fillForm(fn (Customer $record) => ['email' => $record->primary_email])` to prefill the modal.

## Bulk actions

```php
->toolbarActions([
    BulkActionGroup::make([
        DeleteBulkAction::make(),
        BulkAction::make('export')
            ->icon(Heroicon::OutlinedArrowDownTray)
            ->action(fn (Collection $records) => CustomerExport::dispatch($records->pluck('id'))),
    ]),
])
```

`BulkActionGroup` collapses children into a dropdown; place plain actions outside it to keep them as standalone buttons.

## Page header actions

```php
namespace App\Filament\Resources\Customers\Pages;

use App\Filament\Resources\Customers\CustomerResource;
use Filament\Actions\CreateAction;
use Filament\Resources\Pages\ListRecords;

class ListCustomers extends ListRecords
{
    protected static string $resource = CustomerResource::class;

    protected function getHeaderActions(): array
    {
        return [CreateAction::make()];
    }
}
```

## Authorization

- `->visible(fn (?Customer $record) => auth()->user()->can('update', $record))` — fast path.
- `->authorize('update')` — uses the bound model's policy.

## Extracted action classes

```php
namespace App\Filament\Actions;

use Filament\Actions\Action;

class SendInvoiceAction
{
    public static function make(): Action
    {
        return Action::make('send_invoice')
            ->requiresConfirmation()
            ->action(fn ($record) => $record->sendInvoice());
    }
}
```

Use `mcp__boost__filament_scaffold_action --name SendInvoice` to generate the boilerplate.

## Common mistakes (v4 → v5)

- `use Filament\Tables\Actions\EditAction;` ← wrong. Use `Filament\Actions\EditAction`.
- `->actions([...])` on a table ← wrong. Use `->recordActions([...])`.
- `->bulkActions([...])` ← wrong. Use `->toolbarActions([BulkActionGroup::make([...])])`.
- `->form([...])` on an action ← wrong. Use `->schema(fn (Schema $schema) => $schema->components([...]))`.

Run `mcp__boost__filament_lint` to surface these automatically.

See also: filament-tables, filament-schemas, filament-v5-migration.
