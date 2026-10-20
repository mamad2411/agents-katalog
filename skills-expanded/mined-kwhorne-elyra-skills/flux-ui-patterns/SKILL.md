---
name: flux-ui-patterns
description: Build TALL stack UIs with Flux UI the intended way - pick the right component, compose forms and tables, theme with CSS variables, and avoid fighting the library with custom CSS. Use when building or reviewing Blade views in a project using Flux, converting custom Tailwind markup to Flux components, or deciding between Flux and hand-rolled UI.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [flux, tall, livewire, blade, ui]
---

# Flux UI Patterns

Flux earns its keep when you **use components as designed** — accessibility, dark mode, and keyboard handling come free. Fight it with overrides and you inherit all that work back.

## When to use

- Building Blade/Livewire views in a project that uses Flux UI
- Reviewing UI code for consistency ("half Flux, half hand-rolled divs")
- Converting custom Tailwind markup to Flux components
- "Does Flux have something for this, or do we build it?"

## Principles

- **Check Flux first, build second.** Before hand-rolling any control, check whether a Flux component (or composition of two) covers it. Hand-rolled means hand-rolled a11y, dark mode, and focus management.
- **Props before classes.** Use `variant`, `size`, `icon` props for supported variations. Utility classes on Flux components are for *layout* (margin, width, grid placement) — not for restyling internals.
- **The accessibility is in the composition.** `flux:field` + `flux:label` + `flux:error` wire up `for`/`aria` automatically. Skip the wrapper and you silently lose it.
- **Consistency beats preference.** One project, one way to render a form row, a table, an action button.

## Process

### 1. Map the design to components

- Inventory what the page needs: forms, tables, modals, dropdowns, toasts, badges
- For each, find the Flux equivalent; in elyra, verify against the live index with `flux_component_index` rather than memory — APIs move
- No match? Compose primitives (`flux:dropdown` + `flux:navlist`, `flux:modal` + form) before writing custom markup

### 2. Forms — the standard recipe

```blade
<flux:field>
    <flux:label>Email</flux:label>
    <flux:input wire:model.blur="form.email" type="email" />
    <flux:error name="form.email" />
</flux:field>
```

- Every input gets the field/label/error wrapper — that's where the a11y wiring lives
- `wire:model` granularity per `livewire-component-design` (deferred by default, `.blur` for validate-on-blur)
- Shorthand props (e.g. `label="Email"` directly on input) are fine — pick one style per project and stick to it

### 3. Actions and feedback

- Buttons: `variant` prop (`primary`, `danger`, `ghost`, …) — one primary action per view region
- Destructive flows: `flux:modal` confirmation, danger variant on the confirming button
- After Livewire actions: toast via Flux's toast component, triggered from the component — not inline status divs

### 4. Tables and lists

- Use Flux's table for sortable/paginated data wired to Livewire; keep row actions in a trailing dropdown
- Empty states: design them explicitly — a bare "No results." row is a design hole

### 5. Theming — variables, not overrides

- Customize via the documented CSS variables / Tailwind config (accent color, radius) so **all** components shift together
- Dark mode: Flux handles it per component — your job is to not break it with hard-coded `bg-white`/`text-black` in surrounding layout
- If a component must look genuinely different from what props allow, that's a *design-system decision*: wrap it in your own Blade component once (`<x-app.stat-card>`), don't sprinkle the same six utilities across twelve views

### 6. Review pass

```bash
# Smell: raw form controls in a Flux project
grep -rn "<input\|<select\|<button" resources/views --include="*.blade.php" | grep -v "flux:"
```

- Mixed Flux/hand-rolled controls in the same view → converge
- Repeated identical class-soup on Flux components → extract a wrapper component
- In elyra: `blade_to_flux` suggests conversions; `design_system_check` catches consistency drift

## Output format

```markdown
## Flux review: <view/feature>

### Component mapping
| UI need | Used | Should be |
|---------|------|-----------|
| date input | raw `<input type="date">` | `flux:input type="date"` |

### Consistency findings
1. <view:line> — <issue> → <fix>

### Extracted wrappers
- `<x-app.…>` for <repeated pattern> (used N places)

### Theming
Variables touched: … | hard-coded colors found: …
```

## Anti-patterns

- ❌ Hand-rolling a dropdown/modal/toast that Flux ships — and losing keyboard + a11y behavior
- ❌ Restyling component internals with utility classes instead of variants/props/variables
- ❌ Inputs without the `field`/`label`/`error` composition — looks fine, fails screen readers
- ❌ `bg-white dark:bg-zinc-900` hand-managed on every container while Flux handles its own — drift guaranteed
- ❌ Three different button styles for the same action across views
- ❌ Writing Flux component code from memory instead of checking the current component API
- ❌ One-off wrapper divs with the same 8 classes pasted in 12 views — extract the Blade component
