---
description: Scaffold a new controlled-GenUI (L3) component following the flight-card / pie-chart pattern
argument-hint: <component-name> <what the agent should render with it>
allowed-tools: Read, Edit, Write, Bash
---
Arguments: `$ARGUMENTS`
Treat the **first token** as the component name and **the rest** as a description
of what the agent should render with it. If no arguments were given, ask me for them.

Scaffold a new controlled Generative-UI component for L3, following the existing
pattern exactly.

Steps:
1. Read `src/components/flight-card.tsx`, `src/components/pie-chart.tsx`, and
   `src/lessons/L3Components.tsx` to match the established pattern (naming, props,
   how components are registered).
2. Create `src/components/<name>.tsx`:
   - A typed React component.
   - **Every array/object prop MUST have a default** (e.g. `items = []`) —
     streaming delivers partial props and an undefined `.map` white-screens the page.
3. Create a colocated `src/components/<name>.test.tsx` (vitest +
   @testing-library) covering: (a) renders with no / partial props without
   crashing, (b) renders representative data correctly.
4. Register it in `src/lessons/L3Components.tsx` via
   `useComponent({ name, description, parameters: <zod schema>, render })`,
   mirroring the existing registrations.
5. Run `npm run typecheck` and `npx vitest run`; fix anything red.
6. Summarize what you added and suggest a chat prompt I can use to trigger it.

Follow the existing code style. Do not add new dependencies without asking.
