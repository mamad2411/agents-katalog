---
name: livewire
description: Version-aware best practices for Laravel Livewire (Caleb Porzio's full-stack framework), covering v1 through v4. Use whenever building, reviewing, or upgrading Livewire components, wire:model bindings, actions, events, validation, lifecycle hooks, or single-file/island components. ALWAYS detects the installed Livewire major version first, because behavior flips significantly between majors (wire:model default changed in v3; component model + wire:model bubbling changed in v4). Covers every upgrade path (v1->v2, v2->v3, v3->v4).
---

# Laravel Livewire (v1 - v4)

Livewire builds reactive UIs with a PHP class + Blade view and no dedicated JS. Its behavior has **flipped in important ways between majors** - the same `wire:model` is real-time on v1/v2, deferred on v3, and non-bubbling on v4. So: **detect the version, then apply that version's rules.**

## Step 1 - Detect the installed version FIRST

```bash
composer show livewire/livewire | grep -i '^versions'   # resolved version
grep '"livewire/livewire"' composer.json                # the constraint (^1/^2/^3/^4)
php artisan about | grep -i livewire                    # if available
```
Map to major `1.x` / `2.x` / `3.x` / `4.x`. Fresh install -> default to latest stable and confirm. Can't tell -> ask, don't guess.

## Step 2 - Load the matching reference

| Version | Era (one-liner) | Reference |
|---|---|---|
| **v1** (Feb 2020) | First stable; Alpine separate; `wire:model` live by default | `references/livewire-v1.md` |
| **v2** (Sep 2020) | `$wire` + `@entangle`, `wire:model.defer`, `$rules`, scoped events | `references/livewire-v2.md` |
| **v3** (Aug 2023) | `App\Livewire`, Alpine bundled, **`wire:model` deferred by default**, `dispatch()`, PHP attributes, `wire:navigate` | `references/livewire-v3.md` |
| **v4** (Jan 2026) | Single-file & island components, parallel updates, `.async`, `wire:sort/intersect/ref`, `Route::livewire()` | `references/livewire-v4.md` |

## Step 3 - For upgrades, load the matching guide

| Path | Guide | The headline break |
|---|---|---|
| v1 -> v2 | `references/upgrades/v1-to-v2.md` | `$updatesQueryString`->`$queryString`, routing, `{{ $slot }}` |
| v2 -> v3 | `references/upgrades/v2-to-v3.md` | **`wire:model` now deferred** (add `.live`); `emit`->`dispatch`; namespace move; Alpine bundled |
| v3 -> v4 | `references/upgrades/v3-to-v4.md` | **`wire:model` stops bubbling** (add `.deep`); `.blur/.change` no longer request (add `.live`); self-closing tags; `Route::livewire()` |

## The two behavior flips to burn into memory

1. **v2 -> v3: `wire:model` went from live to DEFERRED.** On v3+, an input doesn't update the server as you type - add `.live` where you need real-time (search, live validation). This is the #1 v3 surprise.
2. **v3 -> v4: `wire:model` stops listening to bubbled child events, and `.blur`/`.change` become client-only sync (no request).** Custom-input wrappers break silently - add `.deep`; add `.live` to `.blur`/`.change` to keep hitting the server.

## Version-independent best practices

- **Single root element** per component - true on every version.
- **Public properties are exposed to the browser** and client-writable. Never put secrets in them; lock IDs/prices (`#[Locked]` on v3+).
- **`wire:key` on every item in a loop** so DOM diffing tracks rows correctly (v4 defaults smart keys on, but be explicit).
- **Prefer computed properties** for derived/expensive data over recomputing in `render()`.
- **Validate on the server** - client state is never trustworthy; `wire:model` values are user-controlled.
- **`mount()` runs once; `boot()` runs every request** (v2+). Put per-request re-resolution in `boot()`/computed, not `mount()`.
- **Don't hardcode volatile API from memory** - verify signatures for the detected version against `https://livewire.laravel.com/docs/<major>.x` (older v1/v2 pages live on the legacy `laravel-livewire.com` docs).

## Output expectations

State the detected version ("Detected Livewire v3"), give code in that version's exact syntax labeled with the version, and on upgrades produce the ordered steps from the relevant guide (automated `livewire:upgrade` where it exists, then the manual breaking changes).
