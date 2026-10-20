# frontend/src/components/sidebar

UI pieces composed by [Sidebar.tsx](../Sidebar.tsx), which wires these
components to `useTerminals()` and the [local hooks](hooks/CLAUDE.md).

## UI map

- `NewTerminalDropdown.tsx` — plus/chevron chooser for plain shells, Claude/dangerous Claude, Pi, Codex, and curated Pi models; `useNewTerminal` owns launching.
- `constants.ts` — `createTerminalSpec` commands/labels and `HEADER_ICON_SIZE`; Pi uses `--approve` with validated per-spawn models, and `codexYolo` controls Codex's default `--yolo`.
- `SidebarHeaderActions.tsx` — Startup restart-all button (`restartPending` disables it), or Terminals restore/new buttons.
- `RestoreNotice.tsx` — registry restore prompt and result strip; `describeRestoreSummary` formats the last pass's outcome.
- `SidebarPanelTabs.tsx` — Terminals switcher plus non-empty Merging/Startup panels; Merging has a count badge.
- `SidebarSearchBox.tsx` — inline search/clear controls, shown by Sidebar when the viewed panel has tabs.
- `SidebarTabsBar.tsx` — scroll arrows, drag/reorder and rename state, and `serverId` membership in the busy set; reorders the full context list by id despite panel/search filtering.
- `SidebarTab.tsx` — memoized tab row with kind/spinner, label, status/restore indicators, activation, close, rename and context-menu gestures; exited/dead tabs suppress the spinner, unopened tabs remain eligible.
- `RenameInput.tsx` — local rename draft; `doneRef` makes Enter/blur commit once and Escape cancel.
- `TabContextMenu.tsx` — positioned close-left/right/others popover; hook-owned targets and confirmations.
- `SidebarPanes.tsx` — retains every `projectTerminals` pane wrapper across panel switches; an empty viewed panel shows `SidebarEmptyState` as a sibling so mounted panes stay attached.
- `SidebarEmptyState.tsx` — per-panel empty messaging.

## Owning guides

- [Sidebar hooks](hooks/CLAUDE.md) — launch flow, startup admission, scoping, panel/search state, mounting, bulk close and activity invariants.
- [Terminal state](../../terminal/CLAUDE.md) — `TerminalsContext`, project comparisons, registry reconciliation and backend side effects.
- [Terminal view/connection](../terminal/CLAUDE.md) — xterm lifetime, attach/reconnect and active WebGL handling.
- [Backend terminal](../../../../backend/src/terminal/CLAUDE.md) — PTY lifecycle and harness launch defaults; [registry](../../../../backend/src/terminalRegistry/CLAUDE.md) owns durable tabs, session identity and restore policy.
