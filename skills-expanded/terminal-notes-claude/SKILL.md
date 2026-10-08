# Claude Development Notes

This document contains Claude-specific context about the terminal-notes codebase, development decisions, and architectural patterns.

## Project Overview

A vim-style terminal note-taking application built with React and Ink. The app uses a TUI (Terminal User Interface) for managing notes with vim keybindings and a priority system.

## Architecture

### Component Structure

The application follows a simple React component architecture with three main views:

- **NoteListView** - Main list view showing all notes with navigation and sorting
- **NoteEditor** - Dual-mode component (view/edit) for displaying and editing notes
- **DeleteConfirmation** - Confirmation dialog for note deletion

### State Management

All state is managed in `app.js` using React hooks:
- `view` - Current view state ('list', 'edit', 'delete')
- `notes` - Array of all notes loaded from storage
- `selectedNoteId` - Currently selected note ID
- `editorMode` - Whether NoteEditor opens in 'view' or 'edit' mode
- `sortMode` - Current sort configuration ('priority-asc', 'priority-desc', 'date-asc', 'date-desc')

### Data Storage

Notes are persisted to `~/.terminal_notes.json` as a JSON array. Each note contains:

```javascript
{
  id: "timestamp-string",
  title: "Note title",
  content: "Note content",
  priority: "high" | "medium" | "low" | "none",
  createdAt: "ISO-8601-timestamp",
  updatedAt: "ISO-8601-timestamp"
}
```

## Key Features & Implementation Details

### Priority System

Implemented with 4 levels: high, medium, low, none

**List View Quick Priority:**
- Keys 1/2/3/4 set priority instantly without entering edit mode
- Calls `handleChangePriority` which updates storage and refreshes

**Edit Mode Priority:**
- Tab key cycles through priorities in order: high → medium → low → none → high
- Priority always displays on the right side of the header (using `justifyContent="space-between"`)

**Priority Colors:**
Defined in `source/utils/colors.js`:
- high: red/bright color
- medium: yellow/warning color
- low: blue/info color
- none: dim/gray color

### Sorting System

4 sort modes accessible via 's' key in list view:
- priority-asc: High priority first
- priority-desc: None priority first
- date-asc: Oldest first
- date-desc: Newest first

Sort state cycles through modes and resets selection to top (index 0).

### View vs Edit Mode

**View Mode (Read-Only):**
- Triggered by pressing Enter on a note in list view
- Shows note content as plain text
- Press Enter to switch to edit mode
- Press ESC to return to list

**Edit Mode:**
- Triggered by pressing 'e' on a note in list view, or Enter while in view mode
- Allows editing title and content with TextInput components
- Up/Down arrows switch between title and content fields ONLY (not priority)
- Tab cycles priority
- Enter moves from title → content, or saves from content
- Ctrl+S saves from any field
- ESC cancels and returns to list

**Key Implementation Detail:**
The `NoteEditor` component uses a single prop `mode` to determine initial state, then manages `isViewMode` state internally. This allows switching from view → edit without remounting the component.

### Navigation & Vim Keybindings

**List View:**
- j/k or ↓/↑: Move selection
- g: Jump to top (first note)
- G: Jump to bottom (last note)
- dd: Quick delete (vim-style double-tap)
- Enter: View note
- e: Edit note
- i/a: Add new note
- s: Toggle sort mode
- 1/2/3/4: Set priority
- q/ESC: Quit

**Edit Mode:**
- ↑/↓: Switch title/content (NOT priority)
- Tab: Cycle priority
- Enter: Next field or save
- Ctrl+S: Save
- ESC: Cancel

### Scrolling & Viewport

The NoteListView implements centered scrolling:
- Calculates `maxVisibleNotes` based on terminal height
- Uses `scrollOffset` to keep selected note centered in viewport
- Selection stays in middle of screen when possible
- Shows current position indicator when list is longer than viewport

## Development Decisions

### Why Separate View/Edit Modes?

Originally had a single NoteDetailView component for viewing. This was consolidated into NoteEditor to reduce duplication, but view mode was kept to:
1. Prevent accidental edits when just reviewing notes
2. Provide clear separation between reading and editing workflows
3. Match vim philosophy (normal mode vs insert mode)

### Why Tab for Priority Instead of Priority Mode?

Initially, Tab entered a "priority editing mode" where left/right arrows changed values. This was simplified to:
- Tab directly cycles priority (more intuitive)
- Removed priority from `editingField` state
- No need to "enter" and "exit" priority mode
- Faster workflow, fewer keystrokes

### Why Up/Down Don't Touch Priority in Edit Mode?

Up/Down only switch between title and content fields because:
- Priority is set via Tab (separate interaction)
- Keeps vertical navigation simple and predictable
- Priority is displayed but not part of vertical field navigation
- Matches the mental model: title and content are "stacked", priority is "off to the side"

### Why Remove NoteDetailView?

The NoteDetailView and NoteEditor had significant overlap. Consolidating into a single component with dual modes:
- Reduced code duplication
- Simplified state management in app.js
- Allowed smooth transition from view → edit without remounting
- NoteEditor now handles both use cases cleanly

## File Organization

```
source/
├── app.js                      # Main app logic, state management, view routing
├── cli.js                      # CLI entry point, launches app
├── storage.js                  # File I/O, CRUD operations for notes
├── components/
│   ├── NoteListView.js        # List view with vim navigation
│   ├── NoteEditor.js          # Dual view/edit mode component
│   └── DeleteConfirmation.js  # Delete confirmation dialog
├── hooks/
│   └── useScreenSize.js       # Terminal dimensions hook
└── utils/
    └── colors.js              # Color definitions for priorities and UI
```

## Common Patterns

### Input Handling

All components use Ink's `useInput` hook with early returns:

```javascript
useInput((input, key) => {
  if (key.escape) {
    onCancel();
    return;
  }

  if (key.tab) {
    // handle tab
    return;
  }

  // ... more handlers
});
```

### Conditional Rendering

Components use guard clauses for special states:

```javascript
if (notes.length === 0) {
  return <EmptyState />;
}

// Main render
return <NormalView />;
```

### Layout with Flexbox

Ink uses Yoga (flexbox) for layout:
- `flexDirection="column"` for vertical stacking
- `flexGrow={1}` for expanding sections
- `justifyContent="space-between"` for spreading items
- Priority section uses `justifyContent="space-between"` to pin to right

## Known Limitations

1. **Single-line inputs only** - TextInput from ink-text-input doesn't support multiline editing
2. **No search/filter** - Would be useful for large note collections
3. **No tags/categories** - Only priority for organization
4. **No note archiving** - Notes can only be deleted, not archived
5. **No undo/redo** - Changes are immediate and persistent

## Future Enhancements

Potential improvements for consideration:

- Add search/filter functionality
- Implement tags or categories
- Add note archiving (soft delete)
- Multi-line content editing with proper text editor
- Export notes to markdown files
- Import from markdown/text files
- Customizable keybindings via config
- Theme/color customization
- Note linking/references
- Encrypted storage option

## Testing Notes

- Manual testing recommended for TUI components (automated testing of Ink components is challenging)
- Test terminal resizing behavior
- Verify scrolling works with different terminal heights
- Test with varying note counts (0, 1, many)
- Verify all keyboard shortcuts work as documented

## Dependencies

Key dependencies and their purposes:

- **React 19** - UI component framework
- **Ink 6** - React renderer for CLI apps
- **ink-text-input** - Text input component for forms
- **Babel** - JSX transpilation for build process
- **xo** - Linting and code style

## Build Process

1. JSX source in `source/` directory
2. Babel transpiles to CommonJS in `dist/` directory
3. CLI entry point uses hashbang and chmod +x for direct execution
4. npm link creates global `terminal-notes` command

## Performance Considerations

- Notes are loaded once on app start
- Re-read from disk after each modification (simple but effective)
- Sorting happens on every render (acceptable for reasonable note counts)
- No virtual scrolling (terminal height limits visible items naturally)
