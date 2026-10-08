---
name: keyboard-shortcuts
description: >
  Reference for keyboard shortcut implementation, keybinding registration,
  shortcut parity with vim and other TUI tools, and the complete shortcut
  assignment table across all sidecar plugins. Use when adding or modifying
  keyboard shortcuts, checking shortcut assignments, resolving key conflicts,
  or assessing alignment with vim conventions.
---

# Keyboard Shortcuts

Complete shortcut listings and context reference for all sidecar plugins. For implementation patterns, see `docs/guides/deprecated/ui-feature-guide.md`. For a detailed assessment of inconsistencies, vim alignment, mnemonic quality, and improvement proposals, see `references/assessment.md` in this skill directory.

## Architecture

- **Centralized binding registry**: `internal/keymap/bindings.go` is the single source of truth for key bindings.
- **Context-based dispatch**: Each plugin defines contexts; bindings are scoped to contexts.
- **Command palette** (`?`): Auto-discovers bindings for discoverability.
- **User overrides**: Supported via `~/.config/sidecar/config.json`.
- **Key sequences**: Compound commands like `g g` are supported with 500ms timeout.

### Adding a New Shortcut

1. Add the binding in `internal/keymap/bindings.go` under the appropriate context.
2. Add command handling in the plugin's `Update()` method (usually in a `handlers.go` file).
3. Add the command to the plugin's `Commands()` method for footer hint and command palette.
4. Keep command names short (1 word preferred) to prevent footer wrapping.

### TD Monitor Shortcuts

TD shortcuts are dynamically exported from TD itself via `ExportBindings()` and `ExportCommands()` in `pkg/monitor/keymap/`. TD is the single source of truth. To add TD shortcuts:

1. Add binding to TD's `pkg/monitor/keymap/bindings.go`
2. Add command constant to TD's `pkg/monitor/keymap/registry.go`
3. Add metadata to TD's `pkg/monitor/keymap/export.go`
4. Handle in TD's `pkg/monitor/model.go`

## Global Shortcuts

| Key | Command | Description |
|-----|---------|-------------|
| `j` / `down` | cursor-down | Move cursor down |
| `k` / `up` | cursor-up | Move cursor up |
| `G` | cursor-bottom | Jump to bottom |
| `g g` | cursor-top | Jump to top |
| `ctrl+d` | page-down | Page down |
| `ctrl+u` | page-up | Page up |
| `enter` | select | Select item |
| `esc` | back | Go back / close |
| `` ` `` | next-plugin | Next header entry |
| `~` | prev-plugin | Previous header entry |
| `]` | next-plugin | Next header entry |
| `[` | prev-plugin | Previous header entry |
| `1`-`7` | focus-plugin-N | Focus the Nth project tab (positional; stops at 7) |
| `8` | focus-sessions | Sessions (global) |
| `9` | focus-activity | Activity (global) |
| `0` | focus-tasks | Tasks (global; no-op when the Tasks host is disabled) |
| `?` | toggle-palette | Command palette |
| `!` | toggle-diagnostics | Diagnostics overlay |
| `@` | switch-project | Project switcher |
| `W` | switch-worktree | Worktree switcher |
| `#` | switch-theme | Theme switcher |
| `,` | open-configuration | Open Configuration (contexts that bind `,` win) |
| `i` | open-issue | Open issue |
| `r` | refresh | Refresh |
| `q` | quit | Quit (root contexts only) |
| `ctrl+c` | quit | Force quit |

### The header row is one ring

Sidecar's header is a single row of entries: the global ones in the left cluster
(Sessions, Activity, and Tasks when its feature is on) followed by the project's
plugin tabs on the right.

`[` / `]` (and their `~` / `` ` `` aliases) wrap through **all** of it, in that
order, and the ring is identical from either scope — the project tabs are
painted only in project scope, but they stay in the ring from the global space
so the cycle is never a trap and `]` then `[` is always the identity. Tasks is
absent from the ring whenever its feature is off.

The number row addresses the same row, but by two different rules:

- `1`-`7` are **positional** project tabs. They stop at 7. An eighth plugin tab
  is reached with `[` / `]` or from the command palette.
- `8` / `9` / `0` are **named** global entries — Sessions, Activity, Tasks — and
  mean the same thing in every scope. A key whose entry is disabled (`0` with
  the Tasks host off) does nothing at all, silently; it never falls through to a
  plugin tab.

All ten digits and the four cycling keys are in `keymap.GlobalKeys`, so no
plugin may claim them, and all of them yield to a focused text input.

## Configuration (`config` / `config-edit` / `config-confirm` contexts)

Opened with `,` or by clicking the header gear, always on Sidecar Setup. Like the Overview,
Configuration covers the plugin pane and owns keyboard focus: unhandled keys are swallowed
rather than leaking to the hidden plugin. `?` still opens the command palette.

| Key | Command | Context | Action |
|-----|---------|---------|--------|
| `j` / `k` / `up` / `down` | cursor-down / cursor-up | config | Move through sidebar destinations |
| `enter` | select | config | Open the selected destination |
| `/` | search | config | Focus Search (enters `config-edit`) |
| `tab` | focus-search | config | Move focus between sidebar and Search |
| `esc` | close-configuration | config | Return from a child route, else close and restore the prior surface |
| `down` | first-result | config-edit | Move from Search to the first visible result |
| `up` | focus-search | config-edit | Return to Search from the first result |
| `esc` | clear-search | config-edit | Clear the query and restore the full sidebar |
| `enter` / `y` | confirm | config-confirm | Confirm a consequential change |
| `esc` / `n` | cancel | config-confirm | Cancel it |

## Agent Overview (`overview` context)

Opened with `K` or by clicking the Sidecar logo. The Overview covers the plugin pane and
owns keyboard focus: a plugin left in interactive/text-input mode underneath it (embedded
shell, inline editor) does not receive keys while it is open, and unhandled keys are
swallowed rather than leaking to the hidden plugin.

| Key | Action |
|-----|--------|
| `h` / `l` / `left` / `right` | Move between lanes |
| `j` / `k` / `up` / `down` | Move within a lane |
| `enter` | Open the selected workspace (switches project) |
| `r` | Refresh the board |
| `esc` / `K` | Close the Overview |
| `q` | Quit Sidecar (confirmation modal) |

Global shortcuts stay live while it is open: `` ` ``/`~`, `[`/`]`, `1-9`, `@`, `#`, `W`, `?`, `!`,
`^`, `i`, `ctrl+c`, `q`. Plugin-switching keys (`` ` ``, `~`, `1-9`) close the Overview first.
`esc` on the Agents board or Workspaces list leaves the global space. `q` opens Sidecar's quit modal.

## Global Workspaces

Contexts: `global-workspaces` (list, root), `global-workspaces-filter`, `global-workspaces-rename`, `global-workspaces-create`, `global-workspaces-delete`, `global-workspaces-terminal` (typing), `global-workspaces-doc`, `global-workspaces-doc-search`, `global-workspaces-doc-find`, `global-workspaces-issue`, `global-workspaces-diff`.

There is no watched-preview focus: hiding the sidebar is layout only. `l` / `→` do not move focus to the preview. Clicking a file or td id focuses a content leaf with its own context; footer, help, and the palette follow `WorkspaceFocusContext()`.

| Key | Action |
|-----|--------|
| `j` / `k` / arrows / `g` / `G` | Move selection; preview follows; not typing |
| `enter` / `E` | Start typing in the selected live pane. A dead row stays put |
| click in pane | Start typing. Clicking Diff/Task action chips opens a leaf and does not type |
| click a file tab | Select that file in the document preview. `{` / `}` also cycle when the document is focused |
| click an issue tab | Select that issue in the issue preview. `{` / `}` also cycle when the issue is focused |
| click a list row | Select it; preview follows; not typing |
| click another row while typing | Switch session and stay typing |
| double-click a row | Open that identity in its owning project |
| wheel on terminal | Scroll only; do not activate |
| `ctrl+\` / `esc esc` | Stop typing and land on the list |
| `ctrl+shift+f` while typing | Search the complete terminal history |
| `i` | Find TD task (`open-issue`). Not interactive |
| `n` | Open Create Workspace (Worktree) |
| `ctrl+n` | Open Create Workspace with Shell selected (modal) |
| `D` | Delete the selected shell (shown only for shell rows) |
| `m` | Open the owning project's established merge strategy workflow for a safe worktree |
| `/` | Filter |
| `v` / `s` | Open View: sort the list. `v` matches the project sidebar; `s` is the original alias |
| `\` | Toggle sidebar |
| `esc` | Leave the global space (or clear the filter first) |
| `q` | Quit Sidecar (confirmation modal) |
| `K` | Toggle the global space |
| `M` | Open the reposition modal on the focused pane, or on the selected row's Primary terminal from the list (`pane_move`) |
| `B` | Open Broadcast to agents (`broadcast-agents`, `agent_control`) |

`ctrl+]` attach stays project-only and is off unless `tmux_full_attach` is enabled. While typing, `i` and `q` go to the pane.

### Focused document (`global-workspaces-doc`)

Same keys as the project document pane: `q`/`esc` close, `x` close tab,
`{`/`}` cycle tabs, `m` toggle render, `Y` yank path — and the same three
searches, all rooted at the pane's own directory: `/` in-file search,
`ctrl+p` file finder, `f` project search. The finder and project search are
`internal/panesearch`; the in-file bar is `internal/docview`. Contexts while
one is up: `global-workspaces-doc-search` and `global-workspaces-doc-find`.

### Focused issue (`global-workspaces-issue`)

An unmodified click on a `td-…` link opens it beside the terminal. A
second click appends a tab; an already-open ID is focused. Click a
drawn tab to select it. The header is only the tab strip: ID plus
headline, truncated at the end so the ID stays visible. Footer hints
are Tab× Tab← Tab→. There is no close chip.

`enter` on a parent or subtask uses the same open-or-focus path (no
duplicate, no silent replace). Tabs stay in memory for the selected
row and are not written to disk.

| Key | Command | Description |
|-----|---------|-------------|
| `enter` | open-item | Open or focus the selected parent or subtask as a tab |
| `O` | open-in-td | Open the selected issue in td (same jump as the preview modal's `o`) |
| `x` | close-tab | Close the active tab. Last tab closes the pane and forgets the set |
| `{` / `}` | prev-tab / next-tab | Previous / next issue tab |
| `y` | yank-issue | Copy issue as markdown |
| `Y` | yank-issue-key | Copy issue ID |
| `q` / `esc` | close | Close the pane and forget this row's in-memory tabs |

### Project issue pane (`workspace-issue`)

Same open/append/click/cycle/close journey and the same `{` / `}` / `x`
/ yank / enter keys. `tab` / `shift+tab` cycle panes; `\` toggles the
sidebar. `q` / `esc` hide the pane and retain tabs for that surface;
last `x` forgets. Switching shells or relaunching restores tabs, the
active tab, and each tab's scroll.

| Key | Command | Description |
|-----|---------|-------------|
| `enter` | open-item | Open or focus the selected parent or subtask as a tab |
| `O` | open-in-td | Open the selected issue in td (same jump as the preview modal's `o`) |
| `x` | close-tab | Close the active tab. Last tab forgets the pane |
| `{` / `}` | prev-tab / next-tab | Previous / next issue tab |
| `y` | yank-issue | Copy issue as markdown |
| `Y` | yank-issue-key | Copy issue ID |
| `tab` / `shift+tab` | next-pane / prev-pane | Move focus between sidebar, terminal, document, and issue |
| `\` | toggle-sidebar | Toggle sidebar visibility |
| `q` / `esc` | close | Hide the pane. Tabs stay remembered for this surface |

## Sidebar Controls (All Two-Pane Plugins)

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Switch focus between panes |
| `\` | Toggle sidebar visibility |
| `h` / `left` | Focus left pane |
| `l` / `right` | Focus right pane |
| `+` | Grow sidebar width |
| `-` | Shrink sidebar width |

## Git Status Plugin

### Contexts

| Context | View |
|---------|------|
| `git-status` | File list (root) |
| `git-status-commits` | Recent commits sidebar (root) |
| `git-status-diff` | Inline diff pane (root) |
| `git-commit-preview` | Commit detail in right pane |
| `git-diff` | Full-screen diff |
| `git-commit` | Commit editor |
| `git-push-menu` | Push strategy selection |
| `git-pull-menu` | Pull strategy selection |
| `git-pull-conflict` | Conflict resolution |
| `git-history` | Commit history |
| `git-commit-detail` | Single commit view |

### File List Shortcuts

| Key | Command | Description |
|-----|---------|-------------|
| `s` | stage-file | Stage selected file |
| `u` | unstage-file | Unstage selected file |
| `S` | stage-all | Stage all modified |
| `U` | unstage-all | Unstage all |
| `c` | commit | Open commit editor |
| `A` | amend | Amend last commit |
| `d` / `enter` | show-diff | View file changes |
| `D` | discard-changes | Discard unstaged changes |
| `h` | show-history | Open commit history |
| `P` | push | Open push menu |
| `L` | pull | Open pull menu |
| `f` | fetch | Fetch from remote |
| `b` | branch | Branch operations |
| `z` | stash | Stash changes |
| `Z` | stash-pop | Pop stash |
| `ctrl+z` | stash-apply | Stash apply |
| `o` | open-in-github | Open in GitHub |
| `O` | open-in-file-browser | Open in file browser |
| `y` | yank-file | Copy file info |
| `Y` | yank-path | Copy file path |

### Inline Diff Pane (`git-status-diff`)

The right-hand pane of the Git tab, focused with `enter` / `l` from the file
list.

| Key | Command | Description |
|-----|---------|-------------|
| `j` / `k` | scroll-down / scroll-up | Scroll the diff |
| `ctrl+d` / `ctrl+u` | page-down / page-up | Scroll half a page |
| `g` / `G` | — | Jump to start (also resets the horizontal axis) / end |
| `h` / `l` | — | Scroll horizontally; `h` at column 0 returns to the sidebar |
| `\|` | reset-hscroll | Snap the horizontal scroll back to column 0 |
| `enter` | full-diff | Open the full-screen diff |
| `s` / `u` | stage-file / unstage-file | Stage / unstage the file |
| `v` | toggle-diff-view | Cycle unified → split → full-file |
| `w` | toggle-wrap | Toggle line wrap |
| `\` | toggle-sidebar | Toggle the sidebar |
| `+` / `-` | resize-pane-grow / resize-pane-shrink | Resize the split |

`|` is vim's goto-column key. It reads as the odd choice next to vim's `0`, and
`0` is what this pane used to bind — but the whole number row belongs to the
header (see "The header row is one ring"), so `0` never reaches the plugin. It
was a live handler that had quietly stopped being reachable; `|` is the
replacement, and unlike `0` it is registered, so it appears in the footer and
in `?`.

### Full-Screen Diff (`git-diff`)

| Key | Command | Description |
|-----|---------|-------------|
| `,` / `.` | prev-file / next-file | Previous / next changed file |
| `s` / `u` | stage-file / unstage-file | Stage / unstage the file on screen |
| `v` | toggle-diff-view | Cycle the diff view mode |
| `w` | toggle-wrap | Toggle line wrap |
| `y` | yank-diff | Copy the diff |
| `c` | commit | Open the commit editor |
| `q` / `esc` | close-diff | Leave the diff |

This view has no tabs, so `{` / `}` are deliberately unbound here rather than
made to mean "next file" — that would be the one place in Sidecar where a brace
did something other than cycle tabs, and a silent wrong action is worse than a
no-op. File stepping is `,` / `.`, the same as in the Workspaces Diff pane.

### Commit List Shortcuts

| Key | Command | Description |
|-----|---------|-------------|
| `enter` / `d` | view-commit | Open commit details |
| `h` | show-history | Open history view |
| `y` | yank-commit | Copy commit as markdown |
| `Y` | yank-id | Copy commit hash |
| `/` | search-history | Search commit messages |
| `f` | filter-author | Filter by author |
| `p` | filter-path | Filter by path |
| `F` | clear-filter | Clear filters |
| `n` | next-match | Next search match |
| `N` | prev-match | Previous match |
| `o` | open-in-github | Open commit in GitHub |
| `v` | toggle-graph | Toggle commit graph |

### Pull Menu

| Key | Command |
|-----|---------|
| `p` | pull-merge |
| `r` | pull-rebase |
| `f` | pull-ff-only |
| `a` | pull-autostash |

## File Browser Plugin

### Contexts

| Context | View |
|---------|------|
| `file-browser-tree` | Tree view (root) |
| `file-browser-preview` | Preview pane |
| `file-browser-search` | Filename search |
| `file-browser-content-search` | Content search |
| `file-browser-quick-open` | Fuzzy file finder |
| `file-browser-project-search` | Ripgrep search modal |
| `file-browser-file-op` | File operation input |
| `file-browser-inline-edit` | Inline vim editor (all keys forwarded, global shortcuts bypassed) |

### Tree Shortcuts

| Key | Command | Description |
|-----|---------|-------------|
| `/` | search | Filter files by name |
| `ctrl+p` | quick-open | Find — a file by name (same key, same name as a workspace file pane) |
| `f` | project-search | Search — the project's contents (ripgrep) |
| `/` (preview) | search-content | InFile — this file's contents |
| `a` | create-file | Create new file |
| `A` | create-dir | Create new directory |
| `d` | delete | Delete (with confirmation) |
| `t` | new-tab | Open in new tab |
| `{` | prev-tab | Previous tab |
| `}` | next-tab | Next tab |
| `x` | close-tab | Close active tab |
| `y` | yank | Copy to clipboard |
| `p` | paste | Paste from clipboard |
| `s` | sort | Cycle sort mode |
| `m` | move | Move file/directory |
| `R` | rename | Rename |
| `ctrl+r` | reveal | Reveal in file manager |

A file opened in an app content pane beside Files uses the shared `workspace-doc` document context. It keeps the same file-facing shortcuts as the primary Files preview wherever the shared viewer owns the capability: `/` InFile, `ctrl+p` Find, `f` Search, `e` inline Edit, `E` external Editor, `r` Reload, `m` Render, `w` Wrap, `I` Info, `ctrl+r` Reveal, `y` Contents, `Y` Path, configured selection copy/select-all, `{` / `}` tabs, and `+` / `-` resize. Its finder and project search are the same `internal/panesearch` surfaces used by project and global Workspace document panes, rooted at that content deck's project and loading results back into the focused pane. Files-only tree operations such as rename and its full-screen blame mode remain owned by the primary Files surface; they are not document-viewer shortcuts and are not forwarded to a potentially different file behind the focused pane.

## Conversations Plugin

### Contexts

| Context | View |
|---------|------|
| `conversations` | Session list single-pane (root) |
| `conversations-sidebar` | Session list two-pane (root) |
| `conversations-main` | Messages pane |
| `conversations-search` | Search mode |
| `conversations-filter` | Adapter filter |
| `conversation-detail` | Turn list |
| `message-detail` | Single turn content |
| `analytics` | Usage stats |

## Workspaces Plugin

### Contexts

| Context | View |
|---------|------|
| `workspace-list` | Workspace list (root) |
| `workspace-preview` | Preview pane |
| `workspace-doc` | File tabs beside the terminal (hide with `q`) |
| `workspace-doc-search` | A pane's file finder / project search (owns the keyboard) |
| `workspace-doc-find` | A pane's in-file search bar (owns the keyboard) |
| `workspace-doc-edit` | A pane's inline editor (owns every key, ctrl+c included) |
| `workspace-issue` | Issue tabs beside the terminal (hide with `q`; last `x` forgets) |
| `workspace-diff` | Diff tabs beside the terminal (hide with `q`; last `x` forgets) |
| `workspace-create` | Create Workspace form |
| `workspace-task-link` | Task selection modal |
| `workspace-merge` | Merge workflow modal |
| `workspace-interactive` | Embedded terminal |

### List Shortcuts

| Key | Command | Description |
|-----|---------|-------------|
| `n` | new-workspace | Open Create Workspace (Worktree) |
| `ctrl+n` | new-shell | Create a new shell immediately (shadows the global `ctrl+n` cursor-down in this context) |
| `v` | open-view | Open View: sort the list (Manual, Activity, Recent, Name) |
| `V` | toggle-view | Toggle list/kanban |
| `D` | delete-workspace | Delete workspace / delete shell (confirm) |
| `d` | show-diff | Open working-tree Diff leaf |
| `p` | push | Push branch |
| `m` | merge-workflow | Start merge workflow |
| `T` | link-task | Link/unlink task |
| `s` | start-agent | Start agent |
| `enter` / `E` | interactive | Enter interactive mode |
| `i` | open-issue | Find TD task (global; not interactive) |
| `t` | attach | Full tmux attach (`tmux_full_attach`, default off) |
| `S` | stop-agent | Stop agent |
| `F` | find-file | Open a file pane on the fuzzy file finder |
| `P` | fetch-pr | Fetch a remote PR as a workspace |
| `M` | move-pane | Open the reposition modal on the selected row's Primary terminal (`pane_move`) |
| `B` | broadcast-agents | Open Broadcast to agents (`agent_control`) |


### Preview Shortcuts

| Key | Command | Action |
|-----|---------|--------|
| `o` | open-pane | Open the pane switcher (kind list focused) without leaving the preview |
| `d` | show-diff | Open working-tree Diff leaf |
| `ctrl+t` | toggle-terminal | Toggle a terminal split beside the preview |
| `M` | move-pane | Open the reposition modal on the focused pane (`pane_move`) |

### The Pane Switcher Is Reachable From Every Pane

`n` opens the pane switcher whenever a **content pane** has focus — Document,
Issue, Note, Diff or Resource — on both the project workspace
(`workspace-doc|issue|note|diff|resource`) and the global Workspaces browser
(`global-workspaces-doc|issue|note|diff|resource`). Every content pane absorbs
the keys it does not own, so without this the switcher was reachable only from
the sidebar or the terminal: putting a second pane beside the one you were
reading meant leaving it first.

`n` is the same key the sidebar and the terminal preview already answer with
"make me a new thing", so the answer does not change with focus. Two
consequences follow, and both are deliberate:

- The **Diff pane's** `n` / `N` next-change pair moved to `>` / `<` — the
  shifted forms of its `,` / `.` file steps, so the pair reads as one
  hierarchy: step a file, shift to step a change inside it. One key means one
  thing in every pane; a key that meant next-change here and "new pane"
  everywhere else is exactly the drift this codebase refuses.
- A **live input surface inside a pane still wins**. A committed in-file
  search owns `n` for its next-match while it is up, as does the doc editor
  and the finder overlay; the switcher is asked only after they decline.

The terminal preview keeps `o` rather than `n`, because `n` there belongs to
the list's create. `internal/keymap`'s parity tests hold both surfaces to the
same key in the same contexts.

#### The plugin half: `ctrl+n`

The same entry exists in the ordinary plugins, under `ctrl+n` rather than `n`.
Every plugin that has a create already spends `n` on it — `new-note`,
`next-match` — so displacing those would be the drift the Workspaces half
deliberately avoided.

It is bound in **one place** for all five plugins: `internal/app/pane_switcher.go`,
not once per plugin. The deck the switcher opens into is the app's
(`internal/app/content_deck.go`) and so is the key routing, so a plugin opts in
simply by being deck-eligible — implementing `plugin.ContentLinkProvider` and
`plugin.PaneFocusProvider`, with `features.PluginContentPanes` on. Today that is
`file-browser`, `git-status`, `notes`, `tasks` and `td-monitor`; `workspace` is
excluded because it owns its own pane tree.

Three rules decide where the key appears, and none of them is a per-plugin list:

- **The keymap is the whole opt-in.** The host reads the entry key out of the
  keymap for whatever context is active (`paneSwitcherKeyFor`) rather than
  comparing against a constant. A context that never names `open-pane` never
  reaches the switcher, and a user who rebinds `open-pane` moves the key *and*
  its footer hint together.
- **Browse and preview contexts only.** `ctrl+n` is `cursor-down` in the global
  context and in every filter, finder, search and editor context. Claiming it
  where it already walks a list would take the cursor out from under someone who
  is typing, so those contexts keep it. See the assignment table below.
- **A focused passive leaf answers `n`, not `ctrl+n`.** A leaf inside a plugin's
  deck reports the same `workspace-doc|issue|note|diff|resource` context the two
  Workspaces surfaces report for the same pane, so it answers the same key
  there. One model, three projections, one key each.

The switcher offers **pane kinds only** outside Workspaces — File, Git diff,
td issue, Note, one row per configured resource provider — and is titled
"Open Pane" rather than "Create Workspace". Shell and Worktree create workspace
rows, which a Notes plugin has nowhere to put; Terminal split is absent because
a plugin deck is a passive `contentpanes` deck with no live-leaf host. That is
`workspacecreate.OpenOpts.PaneKindsOnly` plus `AllowTerminalSplit: false` — the
same data-driven catalog, one more flag, no second modal.

See `docs/plans/active/pane-switcher-everywhere.md`.

#### Where `ctrl+n` goes, in full

Every context that binds `ctrl+n` in `keymap.DefaultBindings()`, and to what.
`internal/keymap/pane_switcher_parity_test.go` holds this table to the tree.

| Context | Command | Why |
|---------|---------|-----|
| `global` | `cursor-down` | The emacs/readline default. Everything below either shadows it or inherits it. |
| `notes-list` | `open-pane` | Notes' browse context. |
| `file-browser-tree`, `file-browser-preview` | `open-pane` | The File Browser's two browse contexts. |
| `git-status`, `git-status-commits`, `git-status-diff`, `git-diff`, `git-commit-preview` | `open-pane` | Git names both the focused pane and the cursor's row in its context, so reading a file row, reading a commit and reading a diff are three contexts. |
| `tasks-list`, `tasks-detail`, `tasks-response`, `tasks-response-detail` | `open-pane` | Exactly Tasks' four root contexts; everything else Tasks reports is an overlay it owns the keyboard in. |
| `td-monitor`, `td-board`, `td-kanban` | `open-pane` | td's three browse views: the main list, board mode, the kanban view. |
| `global-workspaces`, `workspace-list` | `new-shell` | The Workspaces lists' second create. This is the precedent `ctrl+n` follows here — one modifier out from `n`, same intent. |
| `global-workspaces-filter`, `project-switcher` | `cursor-down` | Filters. The key walks the list while you type. |
| `file-browser-quick-open`, `file-browser-project-search` | `cursor-down` | Finders. |
| `notes-search`, `notes-editor` | `cursor-down` | Search and the built-in editor. |

Contexts deliberately **without** a row, and the reason each is different:

- `notes-preview` — the note preview answers `ctrl+n`/`ctrl+p` as its own cursor
  motion in plugin code (`notes.handleEditorPreviewKey`), with nothing in
  `bindings.go` to show for it. The rule stands aside; Notes stays reachable
  from `notes-list`.
- `td-modal` and its sub-focus states (`td-epic-tasks`, `td-parent-epic`,
  `td-blocked-by-focused`, `td-blocks-focused`) — `tdmonitor.BlocksGlobalKeys`
  hands every key in that context to the embedded td model at precedence level
  2, two rungs above the switcher's, so a binding there would never fire. This
  is the one genuinely wanted pane the entry does not reach.
- `td-search`, `td-form`, `td-board-editor`, `td-confirm`, `td-close-confirm`,
  and every non-root `tasks-*` context — text input or an overlay the plugin
  forwards wholesale.
- `git-history` — has bindings in `bindings.go` but `gitstatus.FocusContext()`
  never reports it. A binding on a context nobody stands in is a key that does
  nothing.
- Anything reaching a **live PTY**. `ctrl+n` is a real control character:
  `tty.MapKeyToTmux` encodes it as `C-n` and sends it to the pane. The tty
  layer's own chords are `ctrl+\` (exit), `ctrl+]` (attach), `alt+c` (copy),
  `alt+v` (paste), `ctrl+a` (select all) and the platform copy chord; its
  scrollback set is the arrows plus the `j/k/g/G/ctrl+d/ctrl+u` pager aliases.
  The two host `OnKey` hooks claim only terminal search and `ctrl+t`. Above all
  of that, `workspace-interactive`, `file-browser-inline-edit`,
  `notes-inline-edit` and `workspace-doc-edit` forward every key two rungs
  before the switcher's is reached.

`g` / `G` jump to the top / bottom of the preview's scrollback. `0` is
deliberately **not** bound here: it is the header's global Tasks shortcut, and a
context-local binding would make the same key mean two different things one tab
apart. (It previously carried a `reset-scroll` command that had no handler
anywhere in the tree.)

### `M` Opens the Reposition Modal From Every Pane

`M` (`move-pane`, feature `pane_move`, default on) opens the shared pane reposition modal — the same modal the pane header's `⊞` button opens, and the same one for all three pane hosts. It is an entry point, not a second interaction: `M` never mutates the live tree by itself. Inside the modal, `h/j/k/l` and the arrows edit a draft, `z` toggles zoom, `enter` commits the whole sequence atomically, and `esc` discards it.

**Which pane it targets** depends on which window owns the keyboard:

- **From a focused pane** — a preview, a document, an issue, a note, a diff, a resource — `M` targets that leaf.
- **From either Workspaces list** (`workspace-list`, and `global-workspaces`, which the Sessions surface also reports for a focused Primary terminal) `M` targets the selected row's Primary terminal. Host focus decides which of the two the shared `global-workspaces` context means.
- **From a plugin content deck** the key is answered on the app's own structural rung, so it targets the focused passive leaf and never the primary plugin leaf underneath.

**Bound contexts** (all feature-gated on `pane_move`): `workspace-list`, `workspace-preview`, `workspace-doc`, `workspace-issue`, `workspace-note`, `workspace-diff`, `workspace-resource`, `global-workspaces`, `global-workspaces-doc`, `global-workspaces-issue`, `global-workspaces-note`, `global-workspaces-diff`, `global-workspaces-resource`. The app content decks report the same `workspace-*` context names for their own leaves and inherit these bindings.

**Not bound** in text-input, interactive-terminal, modal, or unrelated plugin browse contexts — `workspace-filter`, `workspace-interactive`, `workspace-doc-edit|search|find`, `global-workspaces-filter`, `global-workspaces-terminal`, `file-browser-tree`, `git-status`, `notes-list`, and the rest. Those contexts keep every printable key for themselves, and `internal/keymap/pane_move_parity_test.go` holds them to it.

**Why `M` and not `m`.** `m` is free in ten of the twelve pane contexts, and taken in exactly the two that would break parity: `global-workspaces-doc` spends it on `render`, and `global-workspaces` (what a focused Primary terminal reports on the Sessions surface) spends it on `merge-workflow`. One key must mean one thing in every pane, so a key that works in ten and not the other two is not a candidate. `M` is bound nowhere else except `git-status` (`stash-pop`), a plugin browse context that is never a pane leaf.

**A pane with nowhere to go has no entry.** A tree with a single leaf offers neither the key's modal nor the header's `⊞`: `PlanMove` refuses every destination on it, so both would open onto a layout that cannot change. The button appears when a second pane does.

**The agent's half of the same capability is `sidecar layout move`** over the same planner, with `--to left|right|up|down` compiling through the identical direction rule. See `.claude/skills/ui-features/SKILL.md` and `docs/reference/cli.md`.

### Interactive Mode

| Key | Command |
|-----|---------|
| `ctrl+\` | exit |
| `ctrl+]` | attach (`tmux_full_attach`, default off) |
| `ctrl+t` | toggle a terminal split beside the preview (`workspace_terminal_panel`, default on) |
| `ctrl+shift+f` | search complete terminal history |
| `alt+c` | copy |
| `super+c` | copy (Cmd+C, when the emulator passes it through) |
| `alt+v` | paste |

### Document Pane

An unmodified click on a resolvable file path in workspace or shell terminal
output opens it beside that terminal. A second click appends a tab; a path
that is already open is focused (and `path:line` jumps). Click a drawn tab
to select it. The header is only the tab strip: each label is the relative
path, left-truncated so the filename end always wins. Document panes are
enabled by default; `--disable-feature=workspace_doc_panes` opts out for a
launch and also disables Diff (no pane tree). `shift`-drag and `alt`-drag remain terminal selection gestures.

The global Workspaces view uses the same tab strip and the same click / `{`
/ `}` / `x` keys. Those tabs stay in memory for the selected row.

`q` / `esc` hide the pane and remember the tab set for this shell or
workspace. `x` on the last tab forgets the set. Switching surfaces or
relaunching onto the same surface restores open files, the active tab,
render mode, wrap, scroll, and split ratio. `,` / `.` cycle Diff target
tabs only while a Diff leaf is focused; they do not cycle document tabs.

| Key | Command | Description |
|-----|---------|-------------|
| `j` / `down` | scroll-down | Scroll down |
| `k` / `up` | scroll-up | Scroll up |
| `ctrl+d` / `ctrl+u` | page-down / page-up | Scroll half a page |
| `g` / `G` | cursor-top / cursor-bottom | Jump to start / end |
| `/` | search-content | Search within this file (in-pane bar; same feature as the Files plugin's `/`) |
| `e` | edit | Edit this file inline (tmux PTY editor in the pane body; `features.tmux_inline_edit`) |
| `ctrl+p` | find-file | Find a file by name in this pane (modal scoped to the pane) |
| `f` | search-project | Search the project in this pane (modal scoped to the pane) |
| `x` | close-tab | Close the active tab. Last tab closes the pane and forgets the set |
| `{` / `}` | prev-tab / next-tab | Previous / next file tab |
| `m` | render | Toggle rendered/raw markdown (markdown only; no-op otherwise) |
| `w` | toggle-wrap | Toggle line wrap |
| `I` | info | File info modal |
| `ctrl+r` | reveal | Reveal in the OS file manager |
| `Y` | yank-path | Copy the relative path |
| `+` / `-` | resize-pane-grow / resize-pane-shrink | Resize the workspace split |
| `tab` / `shift+tab` | next-pane / prev-pane | Move focus between sidebar, terminal, and document |
| `q` / `esc` | close | Hide the pane. Tabs stay remembered for this surface |

While a pane search is open (`workspace-doc-search`) it owns every key in
the pane: `esc` closes it, `enter` loads the hit in the active tab, and
`shift+enter` opens it in a new tab.

Inline edit (`e`) opens the same tmux-PTY editor the Files plugin uses, sized
to the pane body, on both pane surfaces (`workspace-doc-edit` and the global
browser's document pane). While a session is live every key is the editor's —
`ctrl+\` or `esc esc` exit it — and clicking outside the pane raises the
save / discard / cancel confirmation instead of leaving the buffer behind.

In-file search (`/`) is a third surface, drawn by `internal/docview` as one
row inside the pane, and it owns every key while it is up
(`workspace-doc-find`, `global-workspaces-doc-find`): `enter` commits,
`n` / `N` step matches, `esc` closes. It dismisses when the pane loses focus.
While it is up it also keeps `n` away from the pane switcher, which is asked
only after the pane's own input surfaces decline.

### Diff Pane

`d` / `show-diff` on the Workspaces list or preview opens a working-tree Diff
leaf beside the terminal. The leaf is not a root context: `q` / `esc` hide it.
`{` / `}` cycle Diff target tabs while the leaf is focused; `,` / `.` step
next/prev file inside the view, and `>` / `<` step next/prev change inside a
file (this pair was `n` / `N` until the pane switcher took `n` in every content
pane).

**One rule everywhere: `{` / `}` is always "cycle the tabs of the thing I am
looking at."** Document, issue, File Browser and Diff leaves all obey it. The
Diff pane is the only surface with a second navigation axis — the files inside
the active target — and that axis gets its own pair, `,` / `.`.

The earlier arrangement was the reverse (`{` / `}` = file, `,` / `.` = tab), on
the reasoning that in-view file jumping is the more frequent act in a diff and
so deserved the better-known keys. That reasoning was sound in isolation and
wrong in aggregate: it made the diff the one place in Sidecar where `}` did not
mean "next tab", so the cost was paid on every context switch into and out of
the diff, by everyone, forever — while the benefit accrued only inside the diff.
Consistency of a key's *meaning* across surfaces beats optimality of its
*assignment* on one surface. If you are tempted to re-optimise a key for a
single pane again, that is the trade to weigh.

| Key | Command | Description |
|-----|---------|-------------|
| `d` | show-diff | Open working-tree Diff leaf (list and preview) |
| `q` / `esc` | close | Hide the pane. Tabs stay remembered for this surface |
| `x` | close-tab | Close the active tab. Last tab forgets the pane |
| `{` / `}` | prev-tab / next-tab | Previous / next Diff target tab |
| `,` / `.` | prev-file / next-file | Previous / next file in this target |
| `Y` | yank-id | Copy the target identity (`wt` / `c:…` / `r:…`) |
| `tab` / `shift+tab` | next-pane / prev-pane | Move focus between sidebar, terminal, and content |
| `\` | toggle-sidebar | Toggle sidebar visibility |

Moving around inside the viewer. These are the shared viewer's own keys
(`internal/workspacediff/keys.go`); they are registered in `bindings.go` for both
`workspace-diff` and `global-workspaces-diff` so the footer, help and palette show
them, and the viewer answers them before keymap dispatch.

| Key | Command | Description |
|-----|---------|-------------|
| `l` / `right` / `enter` | diff-open | Open the selected file's diff, or a commit's file list |
| `j` / `down` | diff-down / diff-scroll-down | Next item in the list; scroll the diff body |
| `k` / `up` | diff-up / diff-scroll-up | Previous item; scroll the diff body up |
| `h` / `left` | diff-back | Back to the file list (scrolls sideways first when panned) |
| `g` / `G` | diff-top / diff-bottom | Jump to the top / bottom |
| `ctrl+d` / `pgdown` | diff-page-down | Page down |
| `ctrl+u` / `pgup` | diff-page-up | Page up |
| `v` | toggle-diff-view | Cycle unified → side-by-side → full-file |
| `z` | toggle-diff-scope | Cycle working tree → commits → aggregate |
| `>` / `<` | diff-next-change | Next / previous change (full-file mode) |
| `f` | file-picker | Open the file picker (project pane only) |

### Issue Pane

An unmodified click on a `td-…` link in workspace or shell terminal
output opens it beside that terminal. A second click appends a tab; an
ID that is already open is focused. Click a drawn tab to select it.
The header is only the tab strip: each label is the issue ID plus
headline, truncated at the end so the ID stays visible. There is no
close chip. Footer hints are Tab× Tab← Tab→.

The global Workspaces view uses the same tab strip and the same click /
`{` / `}` / `x` keys. Those tabs stay in memory for the selected row
and are not written to disk. `q` / `esc` and last-`x` forget that row's
set.

In project Workspaces, `q` / `esc` hide the pane and remember the tab
set for this shell or workspace. `x` on the last tab forgets the set.
Switching surfaces or relaunching onto the same surface restores open
issues, the active tab, and each tab's scroll. Parent and subtask
`enter` uses the same open-or-focus path.

File tabs keep left-truncated paths so the filename survives. Issue
tabs keep the ID visible and truncate the headline.

| Key | Command | Description |
|-----|---------|-------------|
| `j` / `k` | scroll-down / scroll-up | Scroll down / up |
| `down` / `up` | | Walk parent, siblings, and subtasks |
| `ctrl+d` / `ctrl+u` | page-down / page-up | Scroll half a page |
| `g` / `G` | cursor-top / cursor-bottom | Jump to start / end |
| `x` | close-tab | Close the active tab. Last tab closes the pane and forgets the set |
| `{` / `}` | prev-tab / next-tab | Previous / next issue tab |
| `enter` | open-item | Open or focus the selected parent or subtask as a tab |
| `y` | yank-issue | Copy the issue as markdown |
| `Y` | yank-issue-key | Copy the issue ID |
| `tab` / `shift+tab` | next-pane / prev-pane | Move focus between sidebar, terminal, document, and issue |
| `q` / `esc` | close | Hide the pane. Tabs stay remembered for this surface |

## Notes Plugin

Contexts: `notes-list` (root), `notes-preview`, `notes-editor`, `notes-search`, `notes-info`, `notes-task-modal`, `notes-delete-modal`, `notes-inline-edit`.

The built-in editor is modeless: printable keys type. Selection and undo use modifier chords so `v`, `u`, `y`, `d`, `x`, and `p` stay letters.

### Built-in editor (`notes-editor`)

| Key | Command | Description |
|-----|---------|-------------|
| `shift+arrows` / `shift+home` / `shift+end` | select-* | Extend a source-coordinate selection |
| `alt+s` | select-toggle | Set or clear the selection anchor; ordinary movement then extends |
| `alt+a` | select-all | Select the whole note |
| `super+a` | select-all | Select the whole note when the terminal delivers Cmd; `alt+a` is the portable advertised fallback |
| `super+up` / `super+down` | note-start / note-end | Move to the start / end of the note when delivered |
| `shift+super+up` / `shift+super+down` | select-note-start / select-note-end | Extend selection to the start / end of the note when delivered |
| `alt+c` | copy-note | Copy the selection, or the whole note if none |
| `alt+x` | cut | Cut the selection |
| backspace / delete / type / paste | — | Replace the selection (one undo unit) |
| `ctrl+z` | undo-edit | Undo the last edit unit |
| `ctrl+y` / `ctrl+shift+z` | redo-edit | Redo |
| `ctrl+s` | save | Save now; after leaving edit, retry a failed save from list, preview, or search |
| `esc` / `tab` | back / switch-pane | Leave edit and persist |

The tmux/`$EDITOR` pane (`e`) keeps vim's own undo and selection.

In the list and read-only preview, `ctrl+y` copies the selected note ID. In the
built-in editor it remains redo, and in the tmux/`$EDITOR` pane it is forwarded
unchanged. Enter and note-body clicks follow `plugins.notes.defaultEditor`;
`i`, `e`, and `E` remain explicit built-in, in-pane, and external editor paths.

## TD Monitor Plugin

Contexts: `td-monitor` (root), `td-board`, `td-kanban`, `td-modal`, `td-stats`, `td-search`, `td-confirm`, `td-epic-tasks`, `td-parent-epic`, `td-handoffs`.

Shortcuts are defined in TD's `pkg/monitor/keymap/` and auto-exported. The
context *names* come from there too — td names its own context and
`monitor/keymap.ContextToSidecar` spells it for sidecar — so any sidecar-side
binding on a `td-*` context is a copy of someone else's constant.
`tdmonitor.TestBrowseContextsCarryThePaneSwitcherEntry` derives them from the
upstream constants so a rename in td fails a test here rather than silently
unbinding a key.

`ctrl+n` opens the pane switcher in `td-monitor`, `td-board` and `td-kanban`.
See "The Pane Switcher Is Reachable From Every Pane" for why `td-modal` is not
among them.

## Tasks Plugin

Contexts: `tasks-list`, `tasks-detail`, `tasks-response`, `tasks-response-detail`
(the four **root** contexts), plus every overlay Tasks reports —
`tasks-filter`, `tasks-form`, `tasks-modal`, `tasks-picker`, `tasks-prompt`,
`tasks-task-edit`, `tasks-agent-activity` and the rest.

Shortcuts are defined in Tasks' `pkg/tui` and auto-exported, and the context
names come from there verbatim (`tasksui.FocusContext`). Root-ness is sidecar's
own judgement (`internal/plugins/tasks/routing.go`) and it fails conservative:
anything unknown is treated as an overlay, so sidecar's global keys do not fire
underneath one.

`ctrl+n` opens the pane switcher in the four root contexts and nowhere else —
in an overlay, `BlocksGlobalKeys` has already handed the key to the tab.

## Project Switcher

| Key | Command |
|-----|---------|
| `@` | toggle |
| `down` / `ctrl+n` | cursor-down |
| `up` / `ctrl+p` | cursor-up |
| `Enter` | select |
| `Esc` | close |

## Command Palette

Press `?` to open. Press `tab` to toggle between current-context and all-contexts view.

| Key | Action |
|-----|--------|
| `j` / `k` / `up` / `down` | Navigate |
| `ctrl+d` / `ctrl+u` | Page down/up |
| `enter` | Execute |
| `esc` | Close |
| `tab` | Toggle context filter |

## Known Conflicts and Design Decisions

Key conflicts exist across plugins (e.g., `d` = delete in file-browser, diff in git, delete-session in conversations). See `references/assessment.md` for the full inconsistency analysis, vim alignment audit, mnemonic analysis, and proposed improvement plan.

### Shift Modifier Convention (Current)

- `s`/`S`: stage / stage-all (git)
- `u`/`U`: unstage / unstage-all (git)
- `d`/`D`: diff / discard (git), delete/- (file-browser)
- `y`/`Y`: yank item / yank path
- `n`/`N`: next-match / prev-match (search contexts)
