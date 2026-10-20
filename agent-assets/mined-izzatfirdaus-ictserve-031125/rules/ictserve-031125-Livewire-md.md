---
applyTo:
  - 'app/Livewire/**'
  - 'resources/views/livewire/**'
  - '**/*.blade.php'
description: |
  Livewire 3 reactive components, lifecycle hooks, validation, testing patterns,
  and Volt single-file conventions for ICTServe project.
tags:
  - livewire
  - volt
  - reactive
  - frontend
  - blade
version: '2.0.0'
lastUpdated: '2025-01-06'
---

# Livewire 3 — ICTServe Interactive Component Standards

## Overview

This rule defines Livewire 3 and Volt single-file component conventions for ICTServe. It covers reactive properties, wire directives, lifecycle hooks, form validation, real-time updates, and testing patterns.

| Attribute | Value |
| :--- | :--- |
| **Framework** | Livewire 3.6+ |
| **Applies To** | `app/Livewire/**`, `resources/views/livewire/**` |
| **Traceability** | D13 (UI/UX Frontend Framework), D14 (UI/UX Design Guide) |

## Core Principles

1. **Server-Side State**: State lives on the server, UI reflects it reactively.
2. **Single Root Element**: Components must have exactly one root element.
3. **wire:key in Loops**: Always use `wire:key` for list items.
4. **Lifecycle Hooks**: Use `mount()`, `updated*()` for initialization and reactions.
5. **Validation on Server**: All form validation happens server-side.
6. **Progressive Enhancement**: Works without JavaScript when possible.

## Livewire 3 Key Changes from V2

### Breaking Changes

| Livewire 2 | Livewire 3 |
| :--- | :--- |
| `wire:model` (live by default) | `wire:model` (deferred by default) |
| `App\Http\Livewire` namespace | `App\Livewire` namespace |
| `$this->emit()` | `$this->dispatch()` |
| `$this->emitTo()` | `$this->dispatch()->to()` |
| `$this->dispatchBrowserEvent()` | `$this->dispatch()` |
| `layouts.app` | `components.layouts.app` |
| `@livewireStyles` / `@livewireScripts` | Auto-injected |

### New Directives in Livewire 3

| Directive | Purpose |
| :--- | :--- |
| `wire:show` | Toggle visibility with transitions |
| `wire:transition` | Smooth CSS transitions |
| `wire:cloak` | Hide element until Livewire loads |
| `wire:offline` | Show content when offline |
| `wire:target` | Specify loading state targets |
| `wire:confirm` | Native confirmation dialog |
| `wire:navigate` | SPA-like navigation |

## Installation and Configuration

### Installation

```bash
# Install Livewire 3
composer require livewire/livewire

# Publish configuration (optional)
php artisan livewire:publish --config

# Publish assets (if not auto-injecting)
php artisan livewire:publish --assets
````

### Configuration

```php
// config/livewire.php
return [
    'class_namespace' => 'App\Livewire',
    'view_path' => resource_path('views/livewire'),
    'layout' => 'components.layouts.app',
    'lazy_placeholder' => null,
    'temporary_file_upload' => [
        'disk' => null,
        'rules' => ['required', 'file', 'max:12288'],
        'directory' => 'livewire-tmp',
        'middleware' => 'throttle:60,1',
        'preview_mimes' => ['png', 'gif', 'bmp', 'svg', 'wav', 'mp4', 'mov', 'avi', 'wmv', 'mp3', 'jpg', 'jpeg', 'webp'],
        'max_upload_time' => 5,
        'cleanup' => true,
    ],
    'render_on_redirect' => false,
    'legacy_model_binding' => false,
    'inject_assets' => true,
    'navigate' => [
        'show_progress_bar' => true,
        'progress_bar_color' => '#2299dd',
    ],
    'pagination_theme' => 'tailwind',
];
```

## Component Structure

### Creating Components

```bash
# Create class-based component
php artisan make:livewire Assets/AssetList

# Create component with inline view
php artisan make:livewire Assets/Counter --inline

# Create component with test
php artisan make:livewire Assets/CreateAsset --test

# Create Volt component
php artisan make:volt assets/asset-form
```

### Standard Class-Based Component

```php
<?php

declare(strict_types=1);

namespace App\Livewire\Assets;

use App\Models\Asset;
use App\Models\Category;
use Illuminate\Contracts\View\View;
use Illuminate\Support\Collection;
use Livewire\Attributes\Computed;
use Livewire\Component;
use Livewire\WithPagination;

class AssetList extends Component
{
    use WithPagination;

    public string $search = '';
    public string $status = '';
    public ?int $categoryId = null;
    public string $sortBy = 'created_at';
    public string $sortDirection = 'desc';

    protected $queryString = [
        'search' => ['except' => ''],
        'status' => ['except' => ''],
        'categoryId' => ['except' => null],
    ];

    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    #[Computed]
    public function categories(): Collection
    {
        return Category::orderBy('name')->get();
    }

    public function render(): View
    {
        return view('livewire.assets.asset-list', [
            'assets' => Asset::query()
                ->when($this->search, fn ($q) => $q->where('name', 'like', "%{$this->search}%"))
                ->when($this->status, fn ($q) => $q->where('status', $this->status))
                ->orderBy($this->sortBy, $this->sortDirection)
                ->paginate(15),
        ]);
    }
}
```

## Wire Directives Reference

### wire:model (Data Binding)

```blade
{{-- Deferred (Default in Livewire 3) --}}
<input type="text" wire:model="name">

{{-- Live (Real-Time) --}}
<input type="text" wire:model.live="search">

{{-- Live with Debounce --}}
<input type="text" wire:model.live.debounce.300ms="search">

{{-- Live with Throttle --}}
<input type="text" wire:model.live.throttle.500ms="search">

{{-- Blur --}}
<input type="text" wire:model.blur="email">

{{-- Change --}}
<select wire:model.change="status">
    <option>Pilih...</option>
</select>
```

### wire:click (Actions)

```blade
{{-- Basic action --}}
<button wire:click="save">Simpan</button>

{{-- With parameters --}}
<button wire:click="delete({{ $id }})">Padam</button>

{{-- Prevent default --}}
<a href="#" wire:click.prevent="loadMore">Muat Lagi</a>

{{-- With confirmation --}}
<button wire:click="delete" wire:confirm="Adakah anda pasti?">
    Padam
</button>

{{-- Magic actions --}}
<button wire:click="$refresh">Refresh</button>
<button wire:click="$set('status', 'active')">Aktifkan</button>
```

### wire:loading (Loading States)

```blade
{{-- Show while loading --}}
<div wire:loading>Memuatkan...</div>

{{-- Target specific action --}}
<div wire:loading wire:target="save">Menyimpan...</div>

{{-- Add class --}}
<div wire:loading.class="opacity-50">Content</div>

{{-- Add attribute --}}
<button wire:loading.attr="disabled">Simpan</button>
```

### wire:key (Loop Identification)

```blade
@foreach($assets as $asset)
    <div wire:key="asset-{{ $asset->id }}">
        {{ $asset->name }}
    </div>
@endforeach
```

### wire:poll (Polling)

```blade
{{-- Poll every 2 seconds --}}
<div wire:poll.2s>
    {{ now() }}
</div>

{{-- Poll specific method --}}
<div wire:poll="refreshData">
    {{ $data }}
</div>

{{-- Poll only when visible --}}
<div wire:poll.visible>
    Status: {{ $status }}
</div>
```

### wire:offline (Offline Detection)

```blade
<div wire:offline>
    <div class="alert alert-warning">
        <i class="bi bi-wifi-off me-2"></i>
        Tiada sambungan internet
    </div>
</div>

<button wire:offline.attr="disabled">
    Requires connection
</button>
```

### wire:dirty (Unsaved Changes)

```blade
{{-- Show when form has unsaved changes --}}
<span wire:dirty>* Perubahan belum disimpan</span>

{{-- Target specific field --}}
<span wire:dirty wire:target="name">Nama berubah</span>

{{-- Add class when dirty --}}
<input type="text" wire:dirty.class="border-yellow-500">
```

### wire:transition (Smooth Transitions)

```blade
<div wire:transition>
    Content with smooth transition
</div>

<div wire:transition.fade>Fade transition</div>
<div wire:transition.slide>Slide transition</div>
```

### wire:navigate (SPA Navigation)

```blade
{{-- SPA-like navigation --}}
<a href="/assets" wire:navigate>Senarai Aset</a>

{{-- Prefetch on hover --}}
<a href="/assets/1" wire:navigate.hover>Lihat Aset</a>
```

## Lifecycle Hooks

### Mount (Initialization)

```php
public function mount(Asset $asset): void
{
    $this->authorize('update', $asset);
    $this->asset = $asset;
    $this->name = $asset->name;
}
```

### Updated Hooks

```php
public function updatedSearch(): void
{
    $this->resetPage();
}

public function updatedStatus(): void
{
    $this->resetPage();
    $this->validateOnly('status');
}

// For nested property $form['name']
public function updatedFormName(string $value): void
{
    $this->validateOnly('form.name');
}
```

### Hydration Hooks

```php
public function hydrate(): void
{
    // Called when component is hydrated
}

public function dehydrate(): void
{
    // Called before component is dehydrated
}
```

## Form Validation

### Defining Rules

```php
use Illuminate\Validation\Rule;

protected function rules(): array
{
    return [
        'name' => ['required', 'string', 'max:255'],
        'assetTag' => [
            'required', 
            'string', 
            Rule::unique('assets', 'asset_tag')->ignore($this->assetId)
        ],
        'categoryId' => ['required', 'exists:categories,id'],
    ];
}

protected function messages(): array
{
    return [
        'name.required' => 'Nama aset adalah wajib.',
        'assetTag.unique' => 'Kod aset ini telah wujud.',
    ];
}
```

### Real-Time Validation

```php
public function updatedName(): void
{
    $this->validateOnly('name');
}
```

### Validation in Blade

```blade
<div class="mb-3">
    <label>Nama Aset</label>
    <input type="text" wire:model.blur="name" class="form-control @error('name') is-invalid @enderror">
    @error('name')
        <div class="invalid-feedback">{{ $message }}</div>
    @enderror
</div>
```

## Form Objects (Livewire 3)

Extract form logic into dedicated classes.

```php
namespace App\Livewire\Forms;

use Livewire\Form;
use Livewire\Attributes\Validate;

class AssetForm extends Form
{
    #[Validate('required|min:5')]
    public string $name = '';

    #[Validate('required|email')]
    public string $email = '';

    public function save(): void
    {
        $this->validate();
        // Save logic...
    }
}
```

Usage in Component:

```php
use App\Livewire\Forms\AssetForm;

class CreateAsset extends Component
{
    public AssetForm $form;

    public function save(): void
    {
        $this->form->save();
        $this->redirect('/assets');
    }
}
```

## Events and Communication

### Dispatching Events

```php
// Dispatch to browser
$this->dispatch('asset-created');

// With data
$this->dispatch('asset-created', assetId: 1);

// To specific component
$this->dispatch('refresh')->to('asset-list');

// To self
$this->dispatch('reload')->self();
```

### Listening to Events

```php
use Livewire\Attributes\On;

#[On('asset-created')]
public function refreshList(): void
{
    // Refresh logic
}
```

## JavaScript Integration

```javascript
document.addEventListener('livewire:initialized', () => {
    Livewire.on('asset-created', (data) => {
        alert('Asset created: ' + data.assetId);
    });
});
```

## Pagination

```php
use Livewire\WithPagination;

class AssetList extends Component
{
    use WithPagination;

    public function render()
    {
        return view('livewire.asset-list', [
            'assets' => Asset::paginate(10)
        ]);
    }
}
```

**Blade:**

```blade
{{ $assets->links() }}
```

## File Uploads

```php
use Livewire\WithFileUploads;

class UploadPhoto extends Component
{
    use WithFileUploads;

    #[Validate('image|max:1024')]
    public $photo;

    public function save(): void
    {
        $this->photo->store('photos');
    }
}
```

```blade
<input type="file" wire:model="photo">
@error('photo') <span class="error">{{ $message }}</span> @enderror
```

## Computed Properties

Use `#[Computed]` attribute for efficient data access.

```php
use Livewire\Attributes\Computed;

#[Computed]
public function totalAssets(): int
{
    return Asset::count();
}

// Caching
#[Computed(persist: true, seconds: 60)]
public function stats(): array
{
    return [/* expensive query */];
}
```

## Alpine.js Integration

### Entangle

Sync Livewire and Alpine state.

```blade
<div x-data="{ open: @entangle('showModal') }">
    <div x-show="open">Modal Content</div>
</div>
```

### Wire Magic

Access Livewire from Alpine.

```blade
<button @click="$wire.save()">Save via Alpine</button>
<button @click="$wire.set('name', 'New Name')">Set Name</button>
```

## Testing Livewire Components

```php
use App\Livewire\CreateAsset;
use Livewire\Livewire;
use App\Models\User;

#[Test]
public function can_create_asset(): void
{
    $user = User::factory()->create();

    Livewire::actingAs($user)
        ->test(CreateAsset::class)
        ->set('name', 'MacBook Pro')
        ->set('assetTag', 'MBP-001')
        ->call('save')
        ->assertHasNoErrors()
        ->assertRedirect('/assets');
    
    $this->assertDatabaseHas('assets', ['name' => 'MacBook Pro']);
}

#[Test]
public function validation_works(): void
{
    Livewire::test(CreateAsset::class)
        ->set('name', '')
        ->call('save')
        ->assertHasErrors(['name' => 'required']);
}
```

## Compliance Checklist

When developing Livewire components, ensure:

* [ ] `declare(strict_types=1);` in all class-based components.
* [ ] Single root element in all Blade templates.
* [ ] `wire:key` on all loop items.
* [ ] Server-side validation with `rules()` or Form Objects.
* [ ] Proper lifecycle hooks (`mount()`, `updated*()`).
* [ ] Event dispatching with `$this->dispatch()`.
* [ ] Debounced inputs for search/filter (`debounce.300ms`).
* [ ] Loading states with `wire:loading`.
* [ ] Authorization checks in component methods (`$this->authorize`).
* [ ] Locked properties for sensitive data (`#[Locked]`).
* [ ] Comprehensive tests with `Livewire::test()`.
* [ ] Alpine.js integration where appropriate.

Status: ✅ Active for ICTServe Livewire 3 development Version: 2.0.0 Last Updated: 2025-01-06
