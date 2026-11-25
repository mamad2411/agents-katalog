---
name: ui-part-command-palette
description: "A command palette: when an application needs one, opening it with Cmd or Ctrl+K, searching actions and places together, grouping and recents, the combobox keyboard pattern, shortcut hints, scoped modes, and the libraries that do it. Read before adding a command palette or global quick search."
---

# Command palette

The generated palette is a search box in a modal that lists the sidebar's
pages, opens with a shortcut nobody is told about, lets focus fall to the
page behind it, and ends up as the only way to reach half the actions. This
skill says when an application earns a palette, how it opens, what it
searches and in what order, the keyboard pattern it must follow, and the
libraries that already do it. Site search results are `ui-part-search`, the
dialog rules `ui-part-dialogs`.

## 1. When it earns its place

- In applications with many places and actions, used daily by returning
  people: trackers, editors, admin tools, developer tools, anything with
  many records to jump between.
- Not on marketing sites or small apps with five screens (the navigation is
  enough), and never the only way to do something: every command also
  lives in a visible menu, button or page. The palette is a faster road,
  not the road.
- A documentation site's Cmd+K search is the same pattern over pages
  (`ui-part-search`).

## 2. Opening and closing

- Cmd+K on macOS, Ctrl+K on Windows and Linux; the same keys close it. Call
  `preventDefault()`: browsers use Ctrl+K for their own search bar.
- Leave the keys alone when focus is in a rich text editor that uses Cmd+K
  to insert a link. `/` also opens search on many sites, but only when
  focus is not in a field.
- A visible trigger: a search-shaped button in the top bar or at the top of
  the sidebar ("Search or jump to", with the shortcut at its end) carrying
  `aria-keyshortcuts="Meta+K Control+K"`, so people who do not know the
  keys still find it.
- Open in under 100ms: the command list is already in memory and the
  palette's code loaded while the app is idle; nothing is fetched before it
  paints.
- Escape closes it (or first leaves a nested page). Focus returns to what
  had it before, and the page's own shortcuts work again.

## 3. Anatomy and measures

```
┌──────────────────────────────────────────────────────────────┐
│ ⌕  Search issues, people and actions                    Esc  │ input 48 to 56px
├──────────────────────────────────────────────────────────────┤
│ Recent                                                       │ group label
│▌INV-2041 · Oak Street renovation                   Invoice   │ active row
│ Dina Putri                                          Person   │
│ Actions                                                      │
│ Create invoice                                          C    │
│ Assign to...                                            A    │
│ Go to                                                        │
│ Customers                                           G  C     │
├──────────────────────────────────────────────────────────────┤
│ ↑↓ move · ↵ run · Esc close                                  │ wide screens only
└──────────────────────────────────────────────────────────────┘
```

- A modal 560 to 720px wide, its top 12 to 20vh below the top of the
  window rather than centred, so it does not jump as the list changes; at
  most 60 to 70vh tall, the list scrolling inside.
- The input 48 to 56px high, 16 to 18px text, a search icon, no box of its
  own; the placeholder says what can be found.
- Rows 40 to 44px (48 on touch): a 16 to 20px icon, the name, muted context
  (project, path or kind), a shortcut hint at the right; group labels 12 to
  13px in the muted colour; 6 to 8 rows visible before scrolling.
- The active row has a background of its own from the tokens, distinct
  from hover in both themes (`ui-themes`), and is kept in view with
  `scrollIntoView({ block: "nearest" })`.

## 4. What it searches, and in what order

- One input over places (screens, settings), records (issues, customers,
  files) and actions (create, assign, change theme, sign out), grouped by
  kind.
- Fuzzy matching that forgives typos and matches initials and word starts
  ("crinv" finds "Create invoice"); ranked exact, then prefix, then word
  starts, then fuzzy; lifted by what this person uses often and recently.
- Keywords and synonyms per command ("logout", "log out", "exit" for Sign
  out; "dark" for the theme switch).
- Matched letters emphasised with weight or `mark`, not colour alone.
- Commands filter in the browser as the user types. Records come from the
  server, debounced 150 to 250ms, the stale request cancelled with an
  `AbortController`, and join the list without moving the active row.
- Context first: with an empty query, the last five recent items and the
  actions for the current screen ("Assign INV-2041", "Change status").
- Only what this person may do, and the server checks again when it runs.

## 5. Keyboard and ARIA

- A dialog (`role="dialog"`, `aria-modal="true"`, labelled "Command
  palette") around the combobox pattern. The input is `role="combobox"`
  with `aria-expanded="true"`, `aria-controls` naming the list,
  `aria-autocomplete="list"`, and `aria-activedescendant` set to the active
  row's id. The list is `role="listbox"`, each group `role="group"`
  labelled by its heading, each row `role="option"`, with
  `aria-selected="true"` on the active one.
- Focus stays in the input throughout. Up and Down move the active row
  (wrapping at the ends), Enter runs it, Escape closes, Backspace in an
  empty input leaves a nested page, and Tab never strands focus in the
  list.
- Hover moves the active row; a click runs it.
- The result count is announced politely once typing settles ("8 results",
  "No results").
- The page behind does not scroll, and focus cannot leave the dialog.

## 6. Running a command

- A place: close and go. Cmd or Ctrl+Enter opens it in a new tab where that
  makes sense.
- An action: run, close, and show the result where it happened, with Undo
  when it can be undone ("Moved to Done · Undo", `ui-part-notifications`).
- An action that needs an argument opens a nested page inside the palette
  ("Assign to" lists people, a chip in the input shows the parent), never a
  second dialog.
- Destructive actions sit last and confirm inside the palette ("Delete
  INV-2041? Enter to delete, Esc to cancel") or in a dialog.
- A failure is said on the row or at the top of the list, and the palette
  stays open.

## 7. Scopes and shortcut hints

- Prefixes for people who learn them: `>` for commands only, `@` for
  people, `#` for tags or channels, listed in the empty state and never
  required. A typed prefix becomes a chip in the input; Backspace removes
  it.
- Opened inside a project, that project's results come first, with "Search
  everywhere" as the last row.
- Shortcuts right-aligned in `kbd` elements, in the platform's symbols (⌘ ⌥
  ⇧ on macOS; Ctrl, Alt, Shift elsewhere), sequences in order ("G then C"),
  and only for shortcuts that really work: the palette is where people
  learn them. Hidden on phones.

## 8. States

- Empty query: recent items, suggested actions, one line of prefix hints.
- Loading records: the local results stay, a small spinner at the end of
  the input, a "Searching..." row below them.
- No results: "No results for 'invoce'", with what still helps ("Search all
  documents for 'invoce'", or "Create 'invoce'" where creating makes sense).
- Error: "People could not be loaded. Retry" as a row, local results kept.

## 9. Libraries

- React: cmdk (shadcn/ui's `Command` and `CommandDialog` are built on it),
  or kbar. Vue: Nuxt UI's `CommandPalette`, or shadcn-vue's `Command`.
  Svelte: Bits UI's `Command` (shadcn-svelte's).
- Anything else: a headless dialog and combobox (React Aria, Ark UI,
  Headless UI), never a bare `div` with key handlers.

```tsx
import { useEffect } from "react";
import { Command } from "cmdk";

export function Palette({ open, setOpen }: { open: boolean; setOpen: (o: boolean) => void }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen(!open);
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, setOpen]);

  return (
    <Command.Dialog open={open} onOpenChange={setOpen} label="Command palette">
      <Command.Input placeholder="Search issues, people and actions" />
      <Command.List>
        <Command.Empty>No results.</Command.Empty>
        <Command.Group heading="Actions">
          <Command.Item value="Create invoice" keywords={["new", "add"]} onSelect={createInvoice}>
            Create invoice <kbd>C</kbd>
          </Command.Item>
        </Command.Group>
        <Command.Group heading="Go to">
          <Command.Item onSelect={() => go("/customers")}>Customers</Command.Item>
        </Command.Group>
      </Command.List>
    </Command.Dialog>
  );
}
```

cmdk filters and sorts on its own; when results come from the server, set
`shouldFilter={false}` and filter there.

## 10. On a phone, themes, motion

- The trigger is an icon button named "Search" in the top bar.
- The palette fills the screen: the input at the top with a Cancel button,
  rows 48px, no shortcut hints or key footer, the list above the keyboard.
- It opens with a fade and a scale from 0.98 over 150 to 200ms and closes in
  about 120ms; the active row moves without animation (`motion-interface`,
  section 2). Colours from tokens in both themes.

## Check it

- Cmd+K, Ctrl+K and the visible trigger: type, arrows, Enter, Escape; focus
  returns where it was.
- A screen reader reads the active row as the arrows move, and the count.
- Every command is also reachable somewhere else in the interface.
- Throttled network: local results appear at once, server results join
  without the active row jumping.
- Cmd+K inside the editor still does the editor's own thing.
- `preview` at 360px (full screen, 48px rows) and at 1440px (the box in the
  upper part of the window, not centred).

## Avoid

A palette on a marketing site; the palette as the only way to an action; a
shortcut with no visible trigger; focus leaving the input so typing stops
working; results that jump as the server answers; commands the user cannot
run; a dialog opened from the palette; Ctrl+K left to the browser; hints for
shortcuts that do not exist; a box centred vertically that jumps as the list
grows.
