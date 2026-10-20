---
name: livewire-component-design
description: Design Livewire components with clear boundaries - state ownership, props vs events, performance (network round-trips, lazy, computed), forms, and Alpine handoff. Use when creating or reviewing Livewire components, deciding how to split a page into components, debugging re-render or state-sync issues, or when a Livewire page feels slow.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [livewire, tall, components, alpine, performance]
---

# Livewire Component Design

Every Livewire interaction is a **network round-trip carrying component state**. Good component design minimizes what crosses the wire and who owns what.

## When to use

- Creating or splitting Livewire components ("one big component or three small?")
- State desync, unexpected re-renders, or lost input
- A Livewire page feels sluggish (too many/too heavy requests)
- Deciding Livewire vs Alpine for an interaction

## Principles

- **Components own state; children receive data and emit events.** Two components owning the same state will disagree.
- **Alpine for the browser, Livewire for the server.** Toggles, tabs, dropdowns = Alpine (zero round-trips). Anything touching data/authorization = Livewire.
- **Public properties are the payload — and the attack surface.** Everything public crosses the wire every request and can be tampered with client-side. Keep it minimal, validate/authorize server-side always.
- **A component is a unit of update, not a unit of markup.** Split where update frequency differs, not where the design grid does.

## Process

### 1. Decide what's a component

- Split when a region updates independently (search results vs filters vs cart badge)
- Don't split static markup into components — Blade partials/components are free, Livewire components are not
- Page-level component + small interactive islands beats a deep nesting tree

### 2. Assign state ownership

- The owner mutates; everyone else reads
- Parent → child: pass data as props (child re-renders when parent re-renders)
- Child → parent: dispatch events (`$this->dispatch('order-updated')`), parent listens with `#[On('order-updated')]`
- Cross-component shared state (cart count in navbar): events, or re-fetch in the listener — don't mirror writable copies

### 3. Keep the payload lean

- Public properties: scalars, arrays, IDs. Prefer passing IDs + `#[Computed]` lookups over fat serialized models
- `#[Computed]` for derived data — cached per request, doesn't ride the payload
- `#[Locked]` on IDs and anything the client must not change (`public #[Locked] int $orderId`)
- Never put secrets or other users' data in public properties — view-source shows them

### 4. Control the round-trips

| Pattern | Use |
|---|---|
| `wire:model.live.debounce.300ms` | Search-as-you-type (default `wire:model` is deferred — already cheap) |
| `wire:model.blur` | Validate a field on blur |
| Alpine (`x-show`, `x-data`) | Pure UI state — no server trip at all |
| `#[Lazy]` component | Below-the-fold or expensive components; loads after page paint |
| Polling `wire:poll.10s` | Sparingly; prefer events/broadcasts for real-time |
| `wire:loading` / optimistic UI | Mask unavoidable latency |

### 5. Forms

- Form objects (`UserForm` extends `Form`) once a form exceeds a few fields — validation rules, state, and `save()` live together
- Real-time validation: `wire:model.blur` + `$this->validateOnly($field)`
- Always re-validate and re-authorize in the action method — client state is untrusted input

### 6. Test it

```php
Livewire::test(OrderTable::class)
    ->set('search', 'foo')
    ->assertSee('foo-order')
    ->call('delete', $order->id)
    ->assertForbidden();          // authorization is testable — test it
```

Cover: initial render, each action, validation errors, authorization, emitted events (`assertDispatched`).

## Output format

```markdown
## Livewire design: <page/feature>

### Components
| Component | Owns | Receives | Emits | Lazy? |
|-----------|------|----------|-------|-------|
| …         | …    | …        | …     | …     |

### Wire-vs-Alpine
Alpine handles: … (zero round-trips). Livewire handles: …

### Payload review
Public props: … — locked: …, computed instead of serialized: …

### Round-trip budget
Interaction X: N requests → target M.
```

## Anti-patterns

- ❌ One God-component owning the whole page — every keystroke re-renders everything
- ❌ Two components with writable copies of the same state, synced by hope
- ❌ `wire:model.live` on every input out of habit (request per keystroke)
- ❌ Fat models in public properties when the view needs three fields
- ❌ Trusting a public property because "the UI doesn't let you change it" — `#[Locked]` or re-check
- ❌ Livewire round-trip for a dropdown toggle Alpine does for free
- ❌ Skipping authorization in actions because the button was hidden
