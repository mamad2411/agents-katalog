---
name: frontend-radix-ui
description: Use when building accessible UI with Radix UI primitives — unstyled components you style with Tailwind/CSS, asChild composition, vs shadcn/ui.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [frontend-shadcn-ui, frontend-tailwind, ux-wcag-a11y]
---

# Frontend Radix UI

**Iron Law: Radix gives you behavior + accessibility. You bring the styles. NEVER re-implement a primitive — you will get the ARIA wrong. Compose via `asChild`, don't wrap-and-forward props.**

## Why Radix (vs other component models)

| Approach                               | Verdict                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Radix Primitives**                   | unstyled, headless, WAI-ARIA correct, keyboard nav done — **base layer** for design systems |
| **shadcn/ui**                          | Radix + Tailwind recipes you copy into your repo (you own the code); ideal for app teams    |
| **Headless UI** (Tailwind Labs)        | similar idea, smaller surface; fine if you're already in Tailwind ecosystem                 |
| **MUI / Mantine / Chakra**             | opinionated styles bundled; battle with theme tokens; pick when you don't want to design    |
| **Ariakit**                            | similar to Radix, broader scope, less idiomatic React                                       |
| **Roll your own modal/popover/select** | DON'T. You'll ship inaccessible UI with focus traps that leak.                              |

## Install per primitive

```bash
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tooltip
```

Each primitive is a separate package — only what you use ships. There is no "Radix" monolith.

## Primitive categories

| Category       | Examples                                                                              |
| -------------- | ------------------------------------------------------------------------------------- |
| **Overlays**   | `Dialog`, `AlertDialog`, `Popover`, `Tooltip`, `HoverCard`, `Toast`                   |
| **Menus**      | `DropdownMenu`, `ContextMenu`, `Menubar`, `NavigationMenu`                            |
| **Forms**      | `Checkbox`, `RadioGroup`, `Switch`, `Slider`, `Select`, `Form`                        |
| **Layout**     | `Tabs`, `Accordion`, `Collapsible`, `ScrollArea`, `Separator`                         |
| **Disclosure** | `Toggle`, `ToggleGroup`                                                               |
| **Utilities**  | `Portal`, `Slot` (the engine behind `asChild`), `VisuallyHidden`, `DirectionProvider` |

If a primitive doesn't exist (`DataTable`, `Calendar`, `Combobox` pre-1.0), reach for **shadcn/ui** (Radix + community recipes) or **Headless UI**.

## Composition with `asChild`

```tsx
import * as Dialog from "@radix-ui/react-dialog";

<Dialog.Root>
  <Dialog.Trigger asChild>
    <button className="btn-primary">Open</button> {/* your button, your styles */}
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/60" />
    <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded">
      <Dialog.Title>Confirm</Dialog.Title>
      <Dialog.Description>This cannot be undone.</Dialog.Description>
      <Dialog.Close asChild>
        <button>Close</button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>;
```

`asChild` (via `Slot`) merges Radix's props (refs, ARIA, handlers) onto your single child. **The child must accept and forward `ref`** — use `forwardRef` for custom components.

```tsx
const MyButton = React.forwardRef<HTMLButtonElement, ButtonProps>((props, ref) => <button ref={ref} {...props} />);
```

Without `forwardRef`, focus management breaks.

## Styling approaches

| Approach                                   | Notes                                                                                            |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Tailwind**                               | most common; `data-[state=open]:bg-slate-100`, `data-[side=top]:...` attribute selectors are key |
| **CSS Modules**                            | scoped, fine; lose some Tailwind speed                                                           |
| **Vanilla CSS**                            | works; target `[data-state="open"]` and `[data-side]` attributes Radix exposes                   |
| **CSS-in-JS** (styled-components, Emotion) | works, watch SSR + RSC compatibility                                                             |
| **shadcn/ui**                              | gives you Tailwind recipes pre-baked — `pnpm dlx shadcn@latest add dialog` and edit              |

**Radix exposes state via data attributes** — that's how you style hover/open/closed/checked. Inspect element to see them.

## Accessibility — what Radix gives you

- Focus trap inside Dialog/Popover; restores focus on close
- `aria-*` attributes wired (`aria-expanded`, `aria-controls`, `aria-labelledby`)
- Keyboard nav (arrow keys in Menu, Esc to close, Tab order)
- Screen reader announcements (`aria-live` on Toast)
- RTL support via `DirectionProvider`

**What it does NOT give you**: color contrast (your styles), motion-reduce preferences (set `data-motion-safe` yourself), error message wiring on forms (use `<Form.Message>` from `@radix-ui/react-form`).

## Anti-patterns

- Re-implementing `Dialog` because "it's just a div with display:none" — focus trap, scroll lock, ARIA, ESC handling: 50+ edge cases you'll miss
- Wrapping with `<div onClick>` instead of `asChild` — Radix's handlers don't bind, keyboard breaks
- Forgetting `forwardRef` on custom triggers — focus management silently fails
- Mixing Radix + manual ARIA (`aria-expanded` on Trigger) — duplicate or conflicting state
- `<Dialog.Content>` without `<Dialog.Title>` and `<Dialog.Description>` (or `VisuallyHidden`) — screen readers warn loudly
- Styling state via JS (`isOpen ? "..." : ""`) instead of `data-state` selectors — re-render churn, less idiomatic
- Wrapping every primitive in a custom component that loses `asChild` — defeats composition
- Using shadcn/ui AND vanilla Radix in the same project for the same primitive — pick a lane

## Red flags

| Thought                                | Reality                                                             |
| -------------------------------------- | ------------------------------------------------------------------- |
| "I'll just make a custom dropdown"     | You'll ship it inaccessible; Radix handles 47 keyboard edge cases   |
| "Why isn't the click registering?"     | Missing `forwardRef` on the `asChild` child                         |
| "Styles don't apply on open"           | Use `data-[state=open]:` Tailwind variants, not React state         |
| "The modal scrolls the page behind it" | Radix locks scroll on `Dialog.Content` — make sure `Portal` is used |

## Hand-off

For the Tailwind-flavored copy-paste version of these primitives: `Skill(frontend-shadcn-ui)`. For Tailwind itself: `Skill(frontend-tailwind)`. For WCAG audit basics: `Skill(ux-wcag-a11y)`.
