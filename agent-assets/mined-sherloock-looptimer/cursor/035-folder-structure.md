---
description: Where to put types, utils, lib, and component-level code. See 037-project-map for full map.
globs: "**/*.ts, **/*.tsx"
alwaysApply: false
---

## Folder roles (types / utils / lib / components)

- **types/** — Domain types, const enums, type guards, `*.d.ts`. No business logic, no React, no Zod.
- **utils/** — Pure, framework-agnostic functions. No React, no imports from `lib/` or `app/`. Use for time formatting, compute-total-time, time-input parsing, etc.
- **lib/** — App and feature infrastructure: constants, navigation, timer-tree, ai, export, sound, workout-processing; UI-coupled helpers (e.g. `cn`, timer toasts).
- **schema/** — Zod schemas for API/form boundaries only.
- **components/** — UI only. No standalone `.ts` files that are pure domain or tree logic; move those to `lib/` or `utils/`. Hooks belong in `hooks/`.

## When adding or moving code

- New pure time/domain helper with no app deps → `utils/`.
- New domain type or type guard → `types/`.
- New constant or app/feature module → `lib/` (constants in `lib/constants/`).
- New React hook → `hooks/` (e.g. `hooks/timers/use-*.ts`).
