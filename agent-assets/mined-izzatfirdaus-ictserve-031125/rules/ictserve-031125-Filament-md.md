---
applyTo:
  - 'app/Filament/**'
  - 'app/Providers/Filament/**'
description: |
  Filament 4 admin panel standards for ICTServe project.
  Enforces Resources, Actions, Forms, Tables, SDUI patterns, and authorization.
tags:
  - filament
  - admin
  - sdui
  - resources
  - forms
version: '1.2.0'
lastUpdated: '2025-11-30'
---

# Filament 4 — ICTServe Admin Panel Standards

## Overview

This rule defines Filament 4 conventions for the ICTServe admin panel. It covers Resources (CRUD), Actions, Forms, Tables, Widgets, Pages, SDUI (Server-Driven UI) patterns, and authorization integration.

| Attribute | Value |
| :--- | :--- |
| **Framework** | Filament 4.1+ (Latest Stable) |
| **Applies To** | Admin panel components (`app/Filament/**`) |
| **Traceability** | D13 (UI/UX Frontend Framework), D14 (UI/UX Design Guide) |
| **Laravel Version** | Laravel 12.x |

## Core Principles

1. **Server-Driven UI (SDUI)**: Define UI in PHP, rendered by Filament.
2. **Artisan-First**: Use `php artisan make:filament-*` commands.
3. **Resource Pattern**: One Resource per Eloquent Model for CRUD.
4. **Policy Integration**: Use Laravel Policies for authorization.
5. **Discovery-Based**: Files in `app/Filament/` auto-discovered.

## Filament 4 Key Changes

**From Filament 3**:

* ✅ **File visibility** is `private` by default.
* ✅ **Deferred filters** are default (users must click "Apply" button).
* ✅ **Grid/Section/Fieldset** no longer span all columns by default.
* ✅ **No `all` pagination** option by default.
* ✅ **All actions** extend `Filament\Actions\Action` (Unified Actions).
* ✅ **Layout components** moved to `Filament\Schemas\Components` (Unified Schemas).
* ✅ **New Repeater component** for Forms and Tables.
* ✅ **Icons** use `Filament\Support\Icons\Heroicon` Enum.
* ✅ **Native Nested Resources** supported via `--nested` flag.

---

## Installation and Setup

```bash
# Install Filament
composer require filament/filament

# Publish configuration
php artisan filament:install --panels

# Create admin panel provider
php artisan make:filament-panel admin
````

**Configure Panel** (`app/Providers/Filament/AdminPanelProvider.php`):

```php
use Filament\Panel;

public function panel(Panel $panel): Panel
{
    return $panel
        ->default()
        ->id('admin')
        ->path('admin')
        ->login()
        ->colors([
            'primary' => 'amber', // MOTAC branding
        ])
        ->discoverResources(in: app_path('Filament/Resources'), for: 'App\\Filament\\Resources')
        ->discoverPages(in: app_path('Filament/Pages'), for: 'App\\Filament\\Pages')
        ->discoverWidgets(in: app_path('Filament/Widgets'), for: 'App\\Filament\\Widgets')
        ->middleware([
            'auth',
            'verified',
        ])
        ->authMiddleware([
            'auth',
        ]);
}
```

## Resource Structure

### Creating Resources

```bash
# Basic Resource
php artisan make:filament-resource Asset --no-interaction

# Resource with soft deletes
php artisan make:filament-resource Asset --soft-deletes --no-interaction

# Resource with view page
php artisan make:filament-resource Asset --view --no-interaction

# Simple resource (single page)
php artisan make:filament-resource Asset --simple --no-interaction

# Nested resource (Filament 4+)
php artisan make:filament-resource Asset --nested --parent=Category
```

### Basic Resource Example

```php
namespace App\Filament\Resources;

use App\Filament\Resources\AssetResource\Pages;
use App\Models\Asset;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Schemas\Components\Section;

class AssetResource extends Resource
{
    protected static ?string $model = Asset::class;
    protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Section::make('Maklumat Aset')
                    ->schema([
                        Forms\Components\TextInput::make('name')
                            ->label('Nama Aset')
                            ->required()
                            ->maxLength(255),

                        Forms\Components\TextInput::make('asset_tag')
                            ->label('Kod Aset')
                            ->required()
                            ->unique(ignoreRecord: true)
                            ->maxLength(100),

                        Forms\Components\Select::make('category_id')
                            ->label('Kategori')
                            ->relationship('category', 'name')
                            ->required()
                            ->searchable()
                            ->preload(),

                        Forms\Components\Select::make('status')
                            ->label('Status')
                            ->options([
                                'available' => 'Tersedia',
                                'borrowed' => 'Dipinjam',
                                'maintenance' => 'Penyelenggaraan',
                                'retired' => 'Dilupuskan',
                            ])
                            ->required()
                            ->default('available'),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('asset_tag')
                    ->label('Kod Aset')
                    ->searchable()
                    ->sortable(),

                Tables\Columns\TextColumn::make('name')
                    ->label('Nama')
                    ->searchable()
                    ->sortable(),

                Tables\Columns\TextColumn::make('category.name')
                    ->label('Kategori')
                    ->sortable(),

                Tables\Columns\BadgeColumn::make('status')
                    ->label('Status')
                    ->colors([
                        'success' => 'available',
                        'warning' => 'borrowed',
                        'info' => 'maintenance',
                        'danger' => 'retired',
                    ]),
            ])
            ->filters([
                Tables\Filters\SelectFilter::make('status')
                    ->label('Status')
                    ->options([
                        'available' => 'Tersedia',
                        'borrowed' => 'Dipinjam',
                        'maintenance' => 'Penyelenggaraan',
                        'retired' => 'Dilupuskan',
                    ]),

                Tables\Filters\TrashedFilter::make(),
            ])
            ->deferFilters() // Filament 4 default
            ->actions([
                Tables\Actions\ViewAction::make(),
                Tables\Actions\EditAction::make(),
                Tables\Actions\DeleteAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                    Tables\Actions\RestoreBulkAction::make(),
                    Tables\Actions\ForceDeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListAssets::route('/'),
            'create' => Pages\CreateAsset::route('/create'),
            'edit' => Pages\EditAsset::route('/{record}/edit'),
        ];
    }
}
```

## Form Components

### Text Inputs

```php
Forms\Components\TextInput::make('name')
    ->label('Nama Aset')
    ->required()
    ->maxLength(255)
    ->placeholder('Masukkan nama aset')
    ->helperText('Nama penuh aset')
    ->autofocus()
    ->columnSpan(2);
```

### Select and Relationship

```php
// Relationship Select (Recommended)
Forms\Components\Select::make('category_id')
    ->label('Kategori')
    ->relationship('category', 'name')
    ->required()
    ->searchable()
    ->preload()
    ->createOptionForm([
        Forms\Components\TextInput::make('name')
            ->required()
            ->maxLength(255),
    ]);
```

### Date and Time Pickers

```php
Forms\Components\DatePicker::make('acquired_date')
    ->label('Tarikh Pemerolehan')
    ->required()
    ->maxDate(now())
    ->displayFormat('d/m/Y')
    ->format('Y-m-d');

Forms\Components\DateTimePicker::make('borrowed_at')
    ->label('Tarikh Dipinjam')
    ->seconds(false)
    ->displayFormat('d/m/Y H:i');
```

### File Upload

```php
Forms\Components\FileUpload::make('image')
    ->label('Gambar Aset')
    ->image()
    ->imageEditor()
    ->maxSize(2048) // 2MB
    ->directory('assets/images')
    ->visibility('private') // Filament 4 default
    ->downloadable()
    ->previewable();
```

### Repeater (New in Filament 4)

```php
Forms\Components\Repeater::make('specifications')
    ->label('Spesifikasi')
    ->schema([
        Forms\Components\TextInput::make('key')
            ->label('Nama')
            ->required(),
        Forms\Components\TextInput::make('value')
            ->label('Nilai')
            ->required(),
    ])
    ->columns(2)
    ->addActionLabel('Tambah Spesifikasi')
    ->collapsible()
    ->itemLabel(fn (array $state): ?string => $state['key'] ?? null);
```

## Layout Components

In Filament 4, layout components are now standardized under `Filament\Schemas\Components`.

```php
use Filament\Schemas\Components\Section;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Tabs;

// Section
Section::make('Maklumat Asas')
    ->description('Maklumat utama aset')
    ->schema([
        // Form fields
    ])
    ->columns(2)
    ->collapsible();

// Grid
Grid::make(3)
    ->schema([
        Forms\Components\TextInput::make('name'),
        Forms\Components\TextInput::make('code'),
        Forms\Components\Select::make('status'),
    ]);

// Tabs
Tabs::make('Tabs')
    ->tabs([
        Tabs\Tab::make('Maklumat Asas')
            ->schema([/* Fields */]),
        Tabs\Tab::make('Spesifikasi')
            ->schema([/* Fields */]),
    ]);
```

## Table Columns

### Text Column

```php
Tables\Columns\TextColumn::make('name')
    ->label('Nama')
    ->searchable()
    ->sortable()
    ->toggleable()
    ->copyable()
    ->wrap();

Tables\Columns\TextColumn::make('created_at')
    ->label('Dicipta')
    ->dateTime('d/m/Y H:i')
    ->sortable()
    ->toggleable(isToggledHiddenByDefault: true);
```

### Badge Column

```php
Tables\Columns\BadgeColumn::make('status')
    ->label('Status')
    ->colors([
        'success' => 'available',
        'warning' => 'borrowed',
        'danger' => 'retired',
    ])
    ->icons([
        'heroicon-o-check-circle' => 'available',
        'heroicon-o-clock' => 'borrowed',
        'heroicon-o-x-circle' => 'retired',
    ]);
```

### Image Column

```php
Tables\Columns\ImageColumn::make('image')
    ->label('Gambar')
    ->circular()
    ->size(40);
```

## Table Filters

### Select Filter

```php
Tables\Filters\SelectFilter::make('status')
    ->label('Status')
    ->options([
        'available' => 'Tersedia',
        'borrowed' => 'Dipinjam',
    ])
    ->multiple();

Tables\Filters\SelectFilter::make('category')
    ->label('Kategori')
    ->relationship('category', 'name');
```

### Date Filter

```php
Tables\Filters\Filter::make('acquired_date')
    ->form([
        Forms\Components\DatePicker::make('acquired_from')
            ->label('Dari'),
        Forms\Components\DatePicker::make('acquired_until')
            ->label('Hingga'),
    ])
    ->query(function (Builder $query, array $data): Builder {
        return $query
            ->when(
                $data['acquired_from'],
                fn (Builder $query, $date): Builder => $query->whereDate('acquired_date', '>=', $date),
            )
            ->when(
                $data['acquired_until'],
                fn (Builder $query, $date): Builder => $query->whereDate('acquired_date', '<=', $date),
            );
    });
```

## Actions

### Table Actions

```php
Tables\Actions\ViewAction::make(),
Tables\Actions\EditAction::make(),
Tables\Actions\DeleteAction::make()
    ->requiresConfirmation()
    ->modalHeading('Padam Aset')
    ->modalDescription('Adakah anda pasti mahu memadam aset ini?')
    ->modalSubmitActionLabel('Ya, Padam');
```

### Custom Action

```php
Tables\Actions\Action::make('borrow')
    ->label('Pinjam')
    ->icon('heroicon-o-arrow-right-circle')
    ->color('success')
    ->requiresConfirmation()
    ->form([
        Forms\Components\DatePicker::make('return_by')
            ->label('Tarikh Pulangan')
            ->required()
            ->minDate(now()->addDay()),
    ])
    ->action(function (Asset $record, array $data): void {
        Borrowing::create([
            'asset_id' => $record->id,
            'user_id' => auth()->id(),
            'return_by' => $data['return_by'],
        ]);

        $record->update(['status' => 'borrowed']);

        Notification::make()
            ->title('Aset berjaya dipinjam')
            ->success()
            ->send();
    })
    ->visible(fn (Asset $record): bool => $record->status === 'available');
```

### Bulk Actions

```php
Tables\Actions\BulkActionGroup::make([
    Tables\Actions\DeleteBulkAction::make(),

    Tables\Actions\BulkAction::make('updateStatus')
        ->label('Kemaskini Status')
        ->icon('heroicon-o-pencil')
        ->form([
            Forms\Components\Select::make('status')
                ->label('Status Baru')
                ->options([
                    'available' => 'Tersedia',
                    'maintenance' => 'Penyelenggaraan',
                ])
                ->required(),
        ])
        ->action(function (Collection $records, array $data): void {
            $records->each->update(['status' => $data['status']]);

            Notification::make()
                ->title('Status dikemaskini')
                ->success()
                ->send();
        }),
]);
```

## Authorization (Policies)

Resource Authorization (`app/Policies/AssetPolicy.php`):

```php
public function viewAny(User $user): bool
{
    return $user->can('view_asset');
}

public function create(User $user): bool
{
    return $user->can('create_asset');
}

public function update(User $user, Asset $asset): bool
{
    return $user->can('update_asset');
}

public function delete(User $user, Asset $asset): bool
{
    return $user->can('delete_asset');
}
```

## Pages

### Create Page with Mutation

```php
namespace App\Filament\Resources\AssetResource\Pages;

use App\Filament\Resources\AssetResource;
use Filament\Resources\Pages\CreateRecord;

class CreateAsset extends CreateRecord
{
    protected static string $resource = AssetResource::class;

    protected function getRedirectUrl(): string
    {
        return $this->getResource()::getUrl('index');
    }

    protected function mutateFormDataBeforeCreate(array $data): array
    {
        $data['created_by'] = auth()->id();
        return $data;
    }
}
```

## Widgets

### Stats Widget

```bash
php artisan make:filament-widget AssetStatsOverview --stats --no-interaction
```

```php
namespace App\Filament\Widgets;

use App\Models\Asset;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class AssetStatsOverview extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Jumlah Aset', Asset::count())
                ->description('Semua aset dalam sistem')
                ->descriptionIcon('heroicon-o-rectangle-stack')
                ->color('success'),

            Stat::make('Aset Tersedia', Asset::where('status', 'available')->count())
                ->description('Boleh dipinjam')
                ->descriptionIcon('heroicon-o-check-circle')
                ->color('success'),

            Stat::make('Aset Dipinjam', Asset::where('status', 'borrowed')->count())
                ->description('Sedang dipinjam')
                ->descriptionIcon('heroicon-o-clock')
                ->color('warning'),
        ];
    }
}
```

## Testing Filament

### Resource Test

```php
use App\Filament\Resources\AssetResource\Pages\CreateAsset;
use App\Filament\Resources\AssetResource\Pages\ListAssets;
use App\Models\Asset;
use App\Models\User;
use Livewire\Livewire;

class AssetResourceTest extends TestCase
{
    public function test_can_list_assets(): void
    {
        $user = User::factory()->create();
        $assets = Asset::factory()->count(10)->create();

        Livewire::test(ListAssets::class)
            ->actingAs($user)
            ->assertCanSeeTableRecords($assets);
    }

    public function test_can_create_asset(): void
    {
        $user = User::factory()->create();

        Livewire::test(CreateAsset::class)
            ->actingAs($user)
            ->fillForm([
                'name' => 'Laptop HP',
                'asset_tag' => 'LT-001',
                'status' => 'available',
            ])
            ->call('create')
            ->assertHasNoErrors();

        $this->assertDatabaseHas('assets', [
            'name' => 'Laptop HP',
            'asset_tag' => 'LT-001',
        ]);
    }
}
```

## References and Resources

* **Filament 4 Documentation**: [https://filamentphp.com/docs/4.x](https://filamentphp.com/docs/4.x)
* **Filament Examples**: [https://demo.filamentphp.com](https://demo.filamentphp.com)
* **ICTServe Traceability**: D13 (UI/UX Framework), D14 (UI/UX Design)

## Compliance Checklist

When generating Filament code, ensure:

* [ ] Use `php artisan make:filament-*` commands.
* [ ] Configure panel in `AdminPanelProvider.php`.
* [ ] Use `relationship()` for select fields.
* [ ] Apply authorization via Policies.
* [ ] Use `Section` for form grouping (via `Filament\Schemas\Components`).
* [ ] Add `wire:key` in custom Blade views.
* [ ] Test with `Livewire::test()`.
* [ ] Use `deferFilters()` for table filters.
* [ ] Set file visibility to `private` (default).
* [ ] Follow WCAG 2.2 AA accessibility standards.

Status: ✅ Active for ICTServe Filament 4 development Version: 1.0.0 Last Updated: 2025-01-06
