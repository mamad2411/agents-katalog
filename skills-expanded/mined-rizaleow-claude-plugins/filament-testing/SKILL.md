---
description: Test Filament v5 surfaces with Pest + Livewire — assert schema state, fill forms, call actions, assert table columns/records/actions, mount modal actions. Use when writing or fixing tests for Filament v5 resources, pages, actions, or widgets.
---

# Filament v5 Testing

Filament tests are Livewire component tests. Use Pest's `function Pest\Livewire\livewire` helper to mount a Page (List/Create/Edit/View) or a Widget.

## Setup

```php
// tests/Pest.php
uses(\Tests\TestCase::class, \Illuminate\Foundation\Testing\RefreshDatabase::class)->in('Feature');
```

Authenticate as a user that passes `canAccessPanel()` in every test:

```php
beforeEach(fn () => $this->actingAs(User::factory()->admin()->create()));
```

## Forms / Schemas

```php
use App\Filament\Resources\Customers\Pages\CreateCustomer;
use function Pest\Livewire\livewire;

it('creates a customer', function () {
    livewire(CreateCustomer::class)
        ->fillForm([
            'name'  => 'Ada Lovelace',
            'email' => 'ada@example.com',
        ])
        ->call('create')
        ->assertHasNoFormErrors();

    expect(Customer::where('email', 'ada@example.com'))->toBeTruthy();
});
```

Reactive derivations — assert downstream state with `assertSchemaStateSet`:

```php
livewire(CreatePost::class)
    ->fillForm(['title' => 'My title'])
    ->assertSchemaStateSet(['slug' => 'my-title']);
```

Validation:

```php
livewire(CreateCustomer::class)
    ->fillForm(['email' => 'not-an-email'])
    ->call('create')
    ->assertHasFormErrors(['email' => 'email']);
```

## Tables

```php
use App\Filament\Resources\Customers\Pages\ListCustomers;

it('lists customers', function () {
    $customers = Customer::factory()->count(3)->create();

    livewire(ListCustomers::class)
        ->assertCanSeeTableRecords($customers)
        ->assertTableColumnExists('email')
        ->assertCanRenderTableColumn('name');
});

it('searches by name', function () {
    $matching = Customer::factory()->create(['name' => 'Ada Lovelace']);
    $other    = Customer::factory()->create(['name' => 'Linus Torvalds']);

    livewire(ListCustomers::class)
        ->searchTable('Ada')
        ->assertCanSeeTableRecords([$matching])
        ->assertCanNotSeeTableRecords([$other]);
});

it('filters by status', function () {
    livewire(ListCustomers::class)
        ->filterTable('status', 'active')
        ->assertCanSeeTableRecords(Customer::where('status', 'active')->get());
});
```

## Actions

Row action:

```php
it('deletes a customer', function () {
    $customer = Customer::factory()->create();

    livewire(ListCustomers::class)
        ->callTableAction('delete', $customer)
        ->assertHasNoTableActionErrors();

    expect(Customer::find($customer->id))->toBeNull();
});
```

Modal action with schema:

```php
it('sends invoice with custom note', function () {
    $invoice = Invoice::factory()->create();

    livewire(EditInvoice::class, ['record' => $invoice->getRouteKey()])
        ->mountAction('send_invoice')
        ->assertSchemaStateSet(['template' => 'standard'])
        ->setActionData(['template' => 'late', 'note' => 'Pls pay'])
        ->callMountedAction()
        ->assertHasNoActionErrors();

    expect($invoice->refresh()->isSent())->toBeTrue();
});
```

Visibility / authorization:

```php
->assertTableActionVisible('edit', $record)
->assertTableActionHidden('delete', $record)
->assertActionExists('send_invoice')
->assertActionEnabled('send_invoice');
```

## Bulk actions

```php
livewire(ListCustomers::class)
    ->callTableBulkAction('delete', Customer::all())
    ->assertHasNoTableBulkActionErrors();
```

## Widgets

```php
use App\Filament\Widgets\RevenueOverview;

it('shows revenue stats', function () {
    Order::factory()->paid()->count(3)->create(['total' => 100]);

    livewire(RevenueOverview::class)
        ->assertSee('$300');
});
```

## Common pitfalls

- Always pass the **record key** (`$invoice->getRouteKey()`) to `EditX`/`ViewX`, not the model instance.
- `fillForm` keys must match the field `make('key')` name; nested via dot notation (`'address.city'`).
- For Repeater inputs, fill with arrays of UUID-keyed rows or call `addRepeaterItem(...)` first.
- Tests rely on policy gates — register a policy or override `canAccessPanel()` in your test user factory.

See also: filament-resources, filament-tables, filament-actions, filament-schemas.
