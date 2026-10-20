# frontend/src/components

The UI. **To find which component (or stylesheet) owns X, read `MAP.md`** (this
folder). A subfolder with its own `CLAUDE.md` owns its detail — read it before
changing that subfolder.

## Rules for all components

- **Launcher shims stay shims:** top-level `TaskBoard.tsx`, `Workflows.tsx`,
  `ForceGraphView.tsx` are one-line re-exports; code goes in `taskboard/`,
  `workflows/`, `forceGraph/`.
- **Reuse the shared chrome:** confirmations through `shared/ConfirmDialog.tsx`
  `useConfirm()`; errors through `shared/ErrorToast.tsx`; backdrop overlays
  through `Modal.tsx`; movable panels through `FloatingPanel.tsx` (geometry
  persists under `lattice.<thing>.window`). Settings is a `FloatingPanel`, not a
  `Modal` — the app behind it stays interactive; keep its ref handles thin save
  adapters and per-tab draft state in `use*Draft` hooks (`settings/CLAUDE.md`).
- **Pure logic** (copy, derivation, geometry) lives in plain `.ts` modules with
  node:test units under `src/__tests__/` (e.g. `terminalServerChipDerive.ts`,
  `gitSetup/gitSetupDerive.ts`); components stay rendering + wiring.
- **WebGL contexts are scarce** (Chrome caps ~16 per page): a terminal pane
  holds its WebglAddon only while active and disposes it on deactivate
  (`terminal/CLAUDE.md`).
- **Git Setup** (`gitSetup/CLAUDE.md`): entry points `await ensureGitRepo(path)`;
  **`nested` is never offered init** (a repo inside a repo is the worst
  outcome the feature can produce).
- **Start actions own their retry policy:** the backend-reconnecting pill is
  informational only; a Resume / Run retries only a definitely-unaccepted
  transient failure and never replays an unkeyed POST
  (`taskboard/hooks/CLAUDE.md`, `workflows/hooks/CLAUDE.md`).

## Styles

Every rule lives in a feature stylesheet under `frontend/src/styles/`; the file
→ class-name table is `MAP.md` → "Styles" (navigation and aggregation order:
`styles/CLAUDE.md`). Cascade-sensitive rules when editing:

- `.icon-btn`, `.btn-primary`, `.btn-ghost`, `.text-input`, `.error-msg`,
  `.spinner`, `.popover` live in `controls.css`, which imports before every
  feature file. A feature rule that needs to beat a control goes in the feature
  file (which imports later) — don't edit `controls.css` for it.
- `@keyframes spin` is defined in `controls.css` and reused by
  `.wf-run-chip-spinner` (`appbar.css`), `.merge-run-strip-spinner`
  (`merge-run.css`) and `.sidebar-tab-spinner` (`sidebar.css`);
  `@keyframes modal-fade` is defined in `modal.css` and reused by
  `.taskboard-overlay`. Keep the defining file imported before any file that
  references the animation.
- `timeline.css` adds a second `:root { --timeline-h: 64px }` block — the
  variable is timeline-local, so it stays with the timeline rules rather than
  moving to `tokens.css`.
- Aggregators (`settings.css`, `graph.css`, `taskboard.css`, `workflows.css`)
  `@import` their partials in cascade order — files are not auto-globbed; add a
  partial's `@import` where its cascade needs it.

## Commands

From `frontend/`: `npm run build` (build), `npm test` (tests), `npx tsc -b`
(type-check). See [test conventions](../__tests__/CLAUDE.md).
