# Design system (designer crash course)

- Always use `gap-4` for grid spacing between major layout blocks and card grids.
- Never use raw hex colors in components; use Tailwind tokens tied to CSS variables (e.g. `bg-primary`, `text-muted-foreground`, `border-border`).
- All buttons must include the `transition-all` class (shadcn `Button` already ships with it—preserve it when adding `className` overrides).

When adding new UI, prefer existing shadcn/ui primitives under `src/components/ui` and match patterns in `src/app/page.tsx` and `src/app/dashboard/page.tsx`.
