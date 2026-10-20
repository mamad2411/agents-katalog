# taskboard

Components behind the Tasks button. `TaskBoard.tsx` (parent dir) is a re-export
shim. This file covers the files DIRECTLY here; the taskboard's hooks live in
`hooks/` (its own `hooks/CLAUDE.md`).

## Shell / layout

- `TaskBoardLauncher.tsx` — top-level component: owns the FAB (with active-count
  badge) + FloatingPanel chrome. Calls `useTaskBoardController` and hands the
  result to `TaskBoardPanelBody`.
- `TaskBoardPanelBody.tsx` — fans the controller's public surface into filters,
  lanes / search-empty, post-merge row, new-task/detail overlays, error toast,
  and footer so the launcher stays chrome-only.
- `TaskBoardTitle.tsx` — FloatingPanel titlebar: title label + case-insensitive
  search box (`fp-no-drag` so it works inside the draggable titlebar; Escape / ✕
  clear).
- `TaskBoardFilters.tsx` — lane-visibility chips (each with a count) plus the task
  harness/Pi-model `<select>` (rendered only when >1 option).
- `TaskBoardFooter.tsx` — footer summary line: total/matching count, a
  running-vs-queued spawn-queue indicator, and static interaction hints.
- `TaskBoardLaneGrid.tsx` — maps the visible lanes to `<Lane>` and owns every
  per-lane action decision (run-all gating under search, the QA-only Push /
  Playwright e2e buttons, per-lane sort wiring, merge-vs-bulk strip precedence via
  `mergeRunStripFor(...) ?? bulkRunStripFor(...)`). The panel body passes resolved
  hook outputs; all the `lane.id === 'qa'` / `searchActive` branching lives here.
- `TaskBoardSearchEmpty.tsx` — the "no tasks match your search" empty state (with
  a Clear-search button), shown only for the active-search-zero-results case.

## Lanes / cards

- `Lane.tsx` — one kanban column. Drop slots between cards for explicit
  positioning; lane-background drop = status-only move. Hosts the local `DropSlot`
  helper; drag/drop mechanics come from `hooks/useLaneDropTargets`.
- `LaneHeader.tsx` — dot/title/count, lane-level run-all action, per-lane sort
  clock/caret, the QA Playwright cluster (enable / headed-eye / run-all), push,
  add. Layout only; the run-all copy/icon/disabled rules live in
  `laneRunAllConfig.ts`.
- `laneRunAllConfig.ts` — pure `laneRunAllConfig(id, tasks)` returning the
  per-lane bulk-action presentation (class/icon/disabled/title/aria/disabledReason)
  or `null` for lanes without one.
- `TaskCard.tsx` — one memoized row. Plain click opens the detail overlay;
  ctrl/⌘+click toggles and shift+click range-selects. Accent-colored (via
  `taskColors.ts` `taskColor`) in the `in_progress`/`ready_to_merge` lanes
  (`ACCENT_STATUSES`). Composes body + action row from `TaskCardSubcomponents.tsx`
  and re-exports the `TaskCardSelection` helpers so existing importers stay stable.
- `TaskCardSubcomponents.tsx` — the memoized presentational pieces: `TaskCardBody`
  (title/desc/summary + queued/conflict pills), `TaskReviewBadge` (Reviewing,
  Doubtful/reason, Re-running; accepted/error hidden), `TaskCardConflictBadges`, and
  `TaskCardActions` (renders the icon-button row).
- `TaskCardActions.ts` — declarative action specs + `buildTaskCardActions`: the
  ordered icon-button set (terminal, run, cancel-queued, resume, merge, qa,
  always-present delete), each gated on whether its handler was supplied.
- `TaskCardSelection.ts` — pure card helpers: `ACCENT_STATUSES`,
  `getTaskDragPayloadIds`, `getSelectionClickIntent`.
- `StuckPill.tsx` — "stuck Nm/Nh" on a conflict card once its resolver has run
  > 3 min. A single shared 30s ticker (paused while the tab is hidden) drives
  every pill rather than one interval per card.
- `NewTaskOverlay.tsx` — modal for creating a task in a specific lane (async
  submit with an in-flight double-submit guard).
- `TaskDetailOverlay.tsx` — view/edit overlay; title/description always editable
  plus lane-appropriate Move/Run buttons. Stays open (edits intact) if a save
  fails. Editing state lives in `hooks/useTaskDetailEdit`.
- `TaskDetailMeta.tsx` — read-only status/timestamps/branch/worktree block shown
  inside the detail overlay, plus latest review verdict/probability/reviewer/reason.
- `moveTargets.ts` — pure `getApplicableMoveTargets(status)` → the "Move to …"
  buttons for the detail overlay.

## Strips (merge run / bulk / post-merge)

- `MergeRunStrip.tsx` — `mergeRunStripFor(...)` gate + the dispatcher that picks
  active / resolving-conflicts / summary. Rendered above Ready-to-Merge.
- `MergeRunStripStates.tsx` — the three presentational states (`ActiveStrip`,
  `ResolvingStrip`, `SummaryStrip`).
- `mergeRunStatFormatting.ts` — centralized count/pluralization for the stat chips
  (merged / conflict / error) + the per-task error tooltip, so all three states
  word stats identically.
- `BulkRunStrip.tsx` — `bulkRunStripFor(...)` + the strip for the Open / In
  Progress / QA lane bulk actions (`Run all` / `Resume all` / `Mark all done`):
  live "(X spawned, Y queued)" counts, auto-dismissing to a summary. Reuses the
  merge-run strip CSS. State lives in `hooks/useBulkRunStrips`.
- `bulkStripProgress.ts` — pure bulk-strip types + `deriveCounts` (classifies each
  targeted task spawned/queued/pending from the live task list; resume rides
  `spawnedIds`).
- `PostMergeHookRow.tsx` — collapsible post-merge-hook config row (prompt textarea
  + harness/Pi-model select) and the live active/recent-run banner (open-terminal
  / abort). Unsaved prompt draft/debounce lives in `hooks/usePostMergePromptDraft`;
  persisted settings stay in `hooks/usePostMergeHookForm`.
- `postMergeHookStatus.ts` — pure `isPostMergeHookConfigured` + the collapsed-strip
  status-chip derivation for that row.

## Pure helpers

- `lanes.ts` — `LANES` array, `LANE_BY_ID` map, `DRAG_MIME` constant,
  `shortLabel()`, `parseDragPayload()`.
- `laneSort.ts` — per-lane arrival-date sort: `LaneSortMode`
  (`recent`/`oldest`/`manual`, default `recent`), `arrivalTime(task, status)` (the
  lane-specific arrival stamp — startedAt/completedAt/mergedAt/doneAt, else
  createdAt), and `sortTasksForLane()`. Drives the lane header's clock + caret.
- `reorderMath.ts` — pure drag/drop reorder math against a lane's *visible* order:
  `selectedTasksInVisibleOrder`, `singleDropOrder`, `multiDropOrder`,
  `appendOrder`, and `fullLaneDropIndex` (maps a search-filtered slot index onto
  the full lane: lands above the next visible non-moving card, else after the
  last visible one). Wired to the API by `hooks/useTaskReorderActions`; unit-tested.

## Styles

Taskboard CSS is split under `frontend/src/styles/taskboard/`; `styles/taskboard.css`
is the ordered aggregator with comments for `shell`, `lanes`, `cards`, `filters`,
`lane-actions`, `detail`, `toast`, `forms`, and `post-merge-hook` (`.post-merge-hook-*`
— the collapsible post-merge hook config strip below the lanes).

## Drag MIME

Cards use `application/x-lattice-task` (defined in `lanes.ts`). Setting both that
and `text/plain` keeps the drag readable for non-task drop targets.
