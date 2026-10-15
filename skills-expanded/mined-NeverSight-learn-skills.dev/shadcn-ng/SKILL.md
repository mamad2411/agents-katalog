---
name: shadcn-ng
description: "ALWAYS use when writing code importing shadcn-ng (shadcn/angular). Consult for debugging, best practices, or modifying Angular shadcn components."
metadata:
  version: 2.4.3
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# unovue/shadcn-ng `shadcn-ng`

**Version:** Latest (2025)
**Tags:** Angular, Tailwind CSS, Radix Primitives

**References:** [Docs](./references/docs/_INDEX.md) — installation, components, theming • [GitHub Issues](./references/issues/_INDEX.md) — bugs, workarounds • [GitHub Discussions](./references/discussions/_INDEX.md) — Q&A, patterns

## API Changes

This section documents version-specific API changes.

- NEW: Angular support — shadcn-ng is the Angular port of shadcn/ui, providing copy-paste components styled with Tailwind CSS

- NEW: CLI commands — Use `npx shadcn-ng@latest init` for initialization and `npx shadcn-ng@latest add <component>` for adding components

- NEW: Standalone components — All components are Angular standalone components with proper imports

- NEW: `cn` utility — Use the `cn()` helper from `lib/utils.ts` to merge Tailwind CSS classes

- NEW: CSS variables theming — Configure colors via CSS variables in `globals.css`

## Best Practices

- Use standalone components — All shadcn-ng components are standalone, import them directly in `imports` array

```ts
import { Component } from "@angular/core";
import { UbButtonDirective } from "~/components/ui/button";

@Component({
  standalone: true,
  imports: [UbButtonDirective],
  // ...
})
export class ExampleComponent {}
```

- Configure Tailwind CSS — Follow the official installation guide to set up tailwindcss-animate, class-variance-authority, clsx, and tailwind-merge

- Use CSS variables for theming — Define colors in `:root` in your globals.css for dynamic theming

- Treat components as your own code — Copy components into your project and customize as needed

- Use registry for custom components — Create your own registry.json to share and reuse custom components across projects
