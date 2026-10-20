# AI Rules for Horse Racing Simulator

Interactive horse racing simulation in Vue.js: generate horses, 6-round schedule, sequential races with animation and results.

**Stack:** Vue.js, Vuex Store, component-based architecture.

**Main features:**

- **Generate:** creates a list of 1–20 horses (unique color, condition 1–100) and a 6-round schedule; each round – 10 random horses from a pool of 20 (no duplicates). Distances: 1200, 1400, 1600, 1800, 2000, 2200 m.
- **Start:** runs races; one round at a time, next starts automatically after the previous finishes; after each round – results (ranking/positions).
- **UI:** horse list panel, race track with animated horse movement (reset between rounds), program/schedule panel, results panel. Start disabled until Generate has been used.
- **Vuex:** state – horses, round schedule, results; actions – generate, start round, save results; components read state and dispatch actions.

**Bonus:** unit tests (Vitest), E2E (Playwright).

**Conventions:**

- Keep shared types in `src/types` (e.g. `src/types/data-table.ts`), not in component folders
- Do not use barrel files (index.ts) for exports; import directly from the target file (e.g. `@/components/base/data-table/BaseDataTable.vue`, `@/types/data-table`)
