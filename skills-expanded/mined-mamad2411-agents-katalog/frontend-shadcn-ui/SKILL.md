---
name: frontend-shadcn-ui
description: Use when adopting shadcn/ui — copy-paste model, CLI install, Radix primitives, Tailwind theming, when shadcn fits vs DaisyUI.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [frontend-tailwind, frontend-daisyui, frontend-design-essentials, react]
---

# shadcn/ui

**Iron Law: shadcn is copy-paste, NOT a dependency. You own the components after install. Use it when you need rich customization with Radix primitives.**

A CLI that copies component source into your repo. You own the code, edit it, version it. Underneath, components wrap **Radix UI** primitives styled with **Tailwind**. If you don't want to own component source, use a real library — not shadcn.

## When it fits

| Fits                                             | Doesn't                                       |
| ------------------------------------------------ | --------------------------------------------- |
| React (Next.js, Vite, Remix, Astro+React)        | Non-React stacks — vue/svelte ports lag       |
| Brand-customised UI, full markup control         | "Drop-in and ship" — use DaisyUI              |
| Need accessible behaviour out of the box (Radix) | Throwaway prototype — Daisy has less ceremony |
| Willing to maintain components as your own code  | Won't touch the copy — you don't need shadcn  |

## Decision tree: shadcn vs DaisyUI vs Radix-bare

| Need                                | Pick            | Why                                             |
| ----------------------------------- | --------------- | ----------------------------------------------- |
| Full brand control + a11y + React   | **shadcn**      | Radix behaviour, your styling, your code        |
| Speed > brand, generic look ok      | **DaisyUI**     | Semantic classes, theme swap, zero owned source |
| Bespoke styling, no CVA conventions | **Radix bare**  | `@radix-ui/react-*` directly; style anything    |
| Non-React or on Mantine/Chakra      | **stay there**  | Mixing component libs is pain                   |
| Kitchen-sink forms                  | **shadcn Form** | react-hook-form + zod wired up                  |

## Install

```bash
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button dialog dropdown-menu
```

`init` creates: `components/ui/` (where components land), `lib/utils.ts` (`cn()` = `clsx` + `tailwind-merge`), `components.json` (registry config), Tailwind CSS-variable theme + `tailwindcss-animate`.

Source files land in `components/ui/`. **They are now your code.**

## Architecture

```
components/ui/
├── button.tsx        ← shadcn copy
├── dialog.tsx        ← shadcn copy (wraps @radix-ui/react-dialog)
└── dropdown-menu.tsx ← shadcn copy (wraps @radix-ui/react-dropdown-menu)
```

Each component: imports Radix primitive (the real dep) → composes with Tailwind via CVA → re-exports stylable typed API.

## Theming with CSS variables

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --radius: 0.5rem;
}
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
}
```

Tailwind config maps to utilities: `bg-background`, `text-foreground`, `bg-primary`. Toggle `.dark` on `<html>`.

**Swap HSL → OKLCH (recommended for brand-quality work)**: this is NOT a one-value-form change — shadcn's Tailwind config wraps values in `hsl(var(--background))`. To switch, (1) replace each variable's value with `oklch(...)`, (2) change every `hsl()` wrapper in `tailwind.config.ts` to `oklch()`, (3) confirm the `.dark` block uses the same form. See `Skill(devkit:frontend-design-essentials)` for the OKLCH palette workflow.

2025 CLI also imports from custom registries + theming via `tweakcn`-style generators.

## Composition (Radix pattern)

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm</DialogTitle>
      <DialogDescription>Are you sure?</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button onClick={confirm}>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

`asChild` (Radix `Slot`) merges the child with the wrapper's behaviour. No nested `<button><button>` when your Button is the trigger.

## Variants — your file, your rules

```ts
const buttonVariants = cva("inline-flex items-center rounded-md ...", {
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      brand: "bg-action text-on-action hover:bg-action-hover", // your addition
    },
    size: { sm: "h-9 px-3", md: "h-10 px-4", lg: "h-11 px-8" },
  },
  defaultVariants: { variant: "default", size: "md" },
});
```

No upstream contract to break.

## Updating

No `shadcn upgrade`. Pull newer source via `add <component>` and diff. Git preserves your customisations. Cost of ownership: explicit, manual integration.

## RSC / Next.js

shadcn detects RSC via `components.json` and emits `"use client"` where Radix needs it. Pure presentational (e.g. `Card`) stays server-rendered. See `Skill(react)`.

## Forms

```tsx
<Form {...form}>
  <FormField
    control={form.control}
    name="email"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input {...field} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>
```

Built on react-hook-form + zod. Bigger learning curve; pay it once.

## Anti-patterns

- **Treating shadcn as a versioned dep.** There is no `@shadcn/ui` package.
- **Treating `components/ui/` as untouchable.** Defeats the model.
- **Fighting Radix's API** — using `asChild` wrong, hand-rolling focus management. Read Radix docs once.
- **Wrapping every shadcn component** "to keep our API stable" — you already own the API.
- **Mixing shadcn + Daisy** — overlapping styling vocabularies.
- **Ignoring `asChild`** → nested interactive elements.
- **Hardcoding hex in components** instead of using CSS variables.

## Red flags

| Thought                                              | Reality                                                                |
| ---------------------------------------------------- | ---------------------------------------------------------------------- |
| "I'll wrap shadcn's `Button` in `AppButton`"         | Rebuilding the abstraction shadcn already gave you. Edit `button.tsx`. |
| "I'll pin the shadcn version"                        | There is no package. Pin nothing. Git tracks copies.                   |
| "Radix's `asChild` is confusing, I'll use a `<div>`" | And lose keyboard + ARIA. Read the Slot docs.                          |

## Hand-off

Tailwind underpinnings: `Skill(frontend-tailwind)`. Faster alternative: `Skill(frontend-daisyui)`. Tokens, colour, type, variant patterns (CVA), design-system layering: `Skill(frontend-design-essentials)`. React hooks + state: `Skill(react)`. Server/client split: `Skill(react)`.
