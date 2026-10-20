---
applyTo:
  - 'resources/views/livewire/**'
  - 'resources/views/pages/**'
  - 'app/Livewire/**'
description: |
  Livewire Volt single-file component standards for ICTServe project.
  Class-based and functional API patterns, state management, and testing.
tags:
  - volt
  - livewire
  - single-file-components
  - reactive
  - frontend
version: '2.0.0'
lastUpdated: '2025-01-06'
---

# Livewire Volt — ICTServe Single-File Component Standards

## Overview

This rule defines Livewire Volt conventions for ICTServe. Volt is a single-file component API for Livewire that allows PHP logic and Blade templates to coexist in the same file, providing a streamlined development experience similar to Vue.js single-file components.

| Attribute | Value |
| :--- | :--- |
| **Framework** | Livewire 3.x with Volt 1.x |
| **Applies To** | `resources/views/livewire/**`, `resources/views/pages/**` |
| **Traceability** | D13 (UI/UX Frontend Framework), D14 (UI/UX Design Guide) |

## Core Principles

1. **Single-File Components**: PHP logic and Blade templates in one file.
2. **Class-Based API**: Use anonymous classes extending `Livewire\Volt\Component` for complex logic.
3. **Functional API**: Use functional helpers (`state`, `computed`) for simple components.
4. **Server-Side State**: State lives on the server, UI reflects it reactively.
5. **Convention Over Configuration**: Minimal boilerplate, maximum productivity.
6. **Progressive Enhancement**: Works without JavaScript, enhanced with it.

## Feature Matrix

| Feature | Support | Notes |
| :--- | :--- | :--- |
| Single-File Components | ✅ | PHP + Blade in one file |
| Class-Based API | ✅ | Full Livewire features with anonymous classes |
| Functional API | ✅ | Simplified syntax for common patterns |
| State Management | ✅ | Reactive properties with `state()` helper |
| Computed Properties | ✅ | Cached values with `computed()` helper |
| Lifecycle Hooks | ✅ | `mount()`, `updated()`, `boot()`, etc. |
| Alpine.js Integration | ✅ | Seamless interop with `$wire` |
| Testing Support | ✅ | Full Livewire testing capabilities via `Volt::test()` |

---

## Installation and Setup

### Installing Livewire with Volt

```bash
# Volt is included with Livewire 3, but needs installation
composer require livewire/volt

# Install Volt
php artisan volt:install
````

### Creating Components

```bash
# Create Volt component
php artisan make:volt assets/create-asset

# Create Volt component with test
php artisan make:volt assets/edit-asset --test

# Create Functional Volt component
php artisan make:volt counter --functional
```

### Directory Structure

```text
resources/views/
├── livewire/
│   ├── assets/
│   │   ├── create-asset.blade.php    # Volt component
│   │   └── asset-list.blade.php      # Volt component
├── pages/
│   ├── dashboard.blade.php           # Volt page (auto-routing)
│   └── assets/
│       └── [id].blade.php            # Dynamic route page
```

---

## Class-Based API

Use the Class-Based API for components with complex logic, extensive validation, or when migrating from standard Livewire components.

### Basic Component Structure

```php
<?php

use App\Models\Asset;
use App\Models\Category;
use Illuminate\Validation\Rule;
use Livewire\Volt\Component;

new class extends Component
{
    public string $name = '';
    public string $assetTag = '';
    public ?int $categoryId = null;

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'assetTag' => ['required', 'string', 'unique:assets,asset_tag'],
            'categoryId' => ['required', 'exists:categories,id'],
        ];
    }

    public function save(): void
    {
        $validated = $this->validate();
        
        Asset::create([
            'name' => $validated['name'],
            'asset_tag' => $validated['assetTag'],
            'category_id' => $validated['categoryId'],
            'created_by' => auth()->id(),
        ]);
        
        $this->dispatch('asset-created');
        $this->reset();
    }

    public function with(): array
    {
        return [
            'categories' => Category::orderBy('name')->get(),
        ];
    }
}; ?>

<div class="p-6">
    <form wire:submit="save">
        {{-- Asset Name --}}
        <div class="mb-3">
            <label>Nama Aset</label>
            <input type="text" wire:model="name" class="form-control">
            @error('name') <span class="text-danger">{{ $message }}</span> @enderror
        </div>

        {{-- Category --}}
        <div class="mb-3">
            <label>Kategori</label>
            <select wire:model="categoryId" class="form-select">
                <option value="">-- Pilih Kategori --</option>
                @foreach($categories as $category)
                    <option value="{{ $category->id }}">{{ $category->name }}</option>
                @endforeach
            </select>
            @error('categoryId') <span class="text-danger">{{ $message }}</span> @enderror
        </div>

        <button type="submit" class="btn btn-primary">
            <span wire:loading.remove>Simpan</span>
            <span wire:loading>Menyimpan...</span>
        </button>
    </form>
</div>
```

---

## Functional API

Use the Functional API for simpler components, widgets, or small interactive UI elements.

### State Management Basics

```php
<?php

use function Livewire\Volt\{state};

state(['count' => 0]);

$increment = fn() => $this->count++;
$decrement = fn() => $this->count--;

?>

<div class="text-center">
    <h1>{{ $count }}</h1>
    <button wire:click="decrement">-</button>
    <button wire:click="increment">+</button>
</div>
```

### Computed Properties

```php
<?php

use App\Models\Asset;
use function Livewire\Volt\{state, computed};

state(['categoryId' => null]);

// Computed: Cached until dependencies change
$assets = computed(function () {
    return Asset::query()
        ->when($this->categoryId, fn($q) => $q->where('category_id', $this->categoryId))
        ->get();
});

$totalAssets = computed(fn() => $this->assets->count());

?>

<div>
    <h3>Total: {{ $this->totalAssets }}</h3>
    
    @foreach($this->assets as $asset)
        <div>{{ $asset->name }}</div>
    @endforeach
</div>
```

### Rules and Validation (Functional)

```php
<?php

use App\Models\Asset;
use function Livewire\Volt\{state, rules};

state([
    'name' => '',
    'assetTag' => '',
]);

rules([
    'name' => ['required', 'string', 'max:255'],
    'assetTag' => ['required', 'unique:assets,asset_tag'],
]);

$save = function () {
    $this->validate();

    Asset::create([
        'name' => $this->name,
        'asset_tag' => $this->assetTag,
    ]);
    
    $this->reset();
    $this->dispatch('asset-created');
};

?>

<form wire:submit="save">
    <input type="text" wire:model="name">
    <button type="submit">Save</button>
</form>
```

---

## Lifecycle Hooks

### Functional API Hooks

```php
<?php

use function Livewire\Volt\{mount, boot, updated, on};

// Mount: Runs once when component initializes
mount(function () {
    $this->name = auth()->user()->name ?? '';
});

// Boot: Runs on every request
boot(function () {
    // Permission checks
});

// Updated: Runs when specific properties update
updated([
    'name' => function ($value) {
        $this->validateOnly('name');
    }
]);

// On: Listen to events
on(['user-updated' => function () {
    $this->refreshUserData();
}]);

?>
```

### Class-Based Lifecycle

```php
public function mount(): void
{
    // Initialize
}

public function updatedName($value): void
{
    // Specific property update
}

public function rendering(): void
{
    // Before view render
}
```

---

## Event Handling

### Dispatching Events

```php
// Functional
$save = function () {
    // ... logic
    $this->dispatch('asset-created', assetId: $id);
    $this->dispatch('refresh')->to('asset-list');
};

// Class-Based
public function save(): void
{
    // ... logic
    $this->dispatch('asset-created');
}
```

### Listening to Events

```php
// Functional
use function Livewire\Volt\{on};

on(['asset-created' => function () {
    $this->loadAssets();
}]);

// Class-Based
use Livewire\Attributes\On;

#[On('asset-created')]
public function refresh(): void
{
    $this->loadAssets();
}
```

---

## Testing Volt Components

Use `Volt::test()` instead of `Livewire::test()`.

### Basic Component Test

```php
use Livewire\Volt\Volt;

#[Test]
public function can_create_asset(): void
{
    $user = User::factory()->create();

    Volt::test('assets.create-asset')
        ->actingAs($user)
        ->set('name', 'Laptop Dell')
        ->set('assetTag', 'LT-001')
        ->set('categoryId', 1)
        ->call('save')
        ->assertHasNoErrors()
        ->assertDispatched('asset-created');

    $this->assertDatabaseHas('assets', [
        'name' => 'Laptop Dell',
    ]);
}
```

### Testing Validation

```php
#[Test]
public function validates_required_fields(): void
{
    Volt::test('assets.create-asset')
        ->call('save')
        ->assertHasErrors(['name', 'assetTag']);
}
```

---

## Best Practices Summary

### Do's

* [ ] Use `wire:key` in all loops for proper DOM diffing.
* [ ] Debounce user input (`.debounce.300ms`) to reduce server requests.
* [ ] Use **Computed Properties** for expensive queries or derived data.
* [ ] Authorize actions inside the component methods (using `$this->authorize`).
* [ ] Use **Class-Based** API for forms and complex logic (\>50 lines).
* [ ] Use **Functional** API for simple widgets and display components.
* [ ] Write comprehensive tests using `Volt::test()`.

### Don'ts

* [ ] Don't skip `wire:key` in loops.
* [ ] Don't put sensitive logic in the Blade template; keep it in the PHP block.
* [ ] Don't use `public` properties for sensitive data (it is exposed to the frontend).
* [ ] Don't mix Class-based and Functional syntax in the same file.

## Compliance Checklist

When developing Volt components, ensure:

* [ ] Component created via `php artisan make:volt`.
* [ ] `state()` used for all reactive properties (Functional).
* [ ] `computed()` used for cached derived values.
* [ ] `wire:key` present on all loop items.
* [ ] Loading states included with `wire:loading`.
* [ ] Validation rules defined and tested.
* [ ] Accessibility guidelines (WCAG 2.1 AA) followed.

| Field | Value |
| :--- | :--- |
| **Status** | Active for ICTServe Livewire Volt development |
| **Version** | 2.0.0 |
| **Last Updated** | 2025-01-06 |
