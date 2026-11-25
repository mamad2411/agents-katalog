---
name: canon-search
description: Use when designing, auditing, or refactoring search input fields, search bars, search results pages, autocomplete, typeahead, or command palette UI. Covers input styling, placeholder rules, debouncing, result presentation, keyboard navigation of results, empty states, and the combobox ARIA pattern for search-with-suggestions. Trigger when the user mentions search, search bar, autocomplete, typeahead, command palette, or find.
---

# CANON · Search

Search is where users land when the nav fails them. Make it fast, forgiving, and keyboard-first.

## The search input itself

```html
<form role="search">
  <label for="q" class="sr-only">Search</label>
  <svg aria-hidden="true" class="search-icon">...</svg>
  <input
    id="q"
    type="search"
    name="q"
    placeholder="Search projects, files, people…"
    autocomplete="off"
    spellcheck="false"
    autocapitalize="off"
    autocorrect="off"
  />
  <button type="button" aria-label="Clear search" class="clear-btn" hidden>✕</button>
</form>
```

- `<form role="search">` wraps the input — gives screen reader context.
- `<label>` is always present (can be visually hidden).
- `type="search"` — mobile keyboard shows a "search" button, browsers add a clear-X.
- Turn off `autocomplete`, `spellcheck`, `autocapitalize`, `autocorrect` for identifier-like searches; leave on for natural-language search.
- Custom clear button for consistent look (native X is inconsistent across browsers).

## Input visual spec

| Property | Value |
|---|---|
| Height | 36–48px (40px default) |
| Horizontal padding | 36–40px left (room for icon), 32–40px right (room for clear) |
| Font size | 14–16px (**16px on mobile** — iOS zooms inputs < 16px) |
| Icon size | 16–18px, `currentColor`, muted |
| Border radius | 6–8px for fields, fully rounded (999px) for pill style |
| Focus ring | 2–3px offset 2px, 3:1 contrast minimum |

## Placeholder — show examples, not instructions

| Bad | Good |
|---|---|
| Search | Search projects, files, people |
| Enter keywords | Try "Q4 roadmap" |
| Type to search | Find teammates, tickets, docs |

Placeholder is a preview of what you can do. It disappears on focus, so it can't be the label.

## Debouncing

| Action | Delay |
|---|---|
| Keystroke → fetch suggestions | **150–250ms debounce** |
| Keystroke → render suggestions (client-side) | 0ms |
| Keystroke → run full search (submit) | Only on Enter or search button |

150–250ms is the sweet spot: fast enough to feel responsive, slow enough to avoid firing a request per keypress.

## Autocomplete suggestions — use the combobox pattern

When the input expands into a list of suggestions, it becomes a **combobox** per WAI-ARIA.

```html
<div role="combobox" aria-expanded="false" aria-haspopup="listbox" aria-controls="results">
  <input
    type="text"
    aria-autocomplete="list"
    aria-activedescendant=""
    aria-controls="results"
  />
</div>
<ul role="listbox" id="results">
  <li role="option" id="r1">Result 1</li>
  <li role="option" id="r2" aria-selected="true">Result 2</li>
</ul>
```

### Keyboard

| Key | Behavior |
|---|---|
| ArrowDown | Focus next suggestion (or first, if none focused) |
| ArrowUp | Focus previous |
| Enter | Activate focused suggestion, or submit raw query |
| Escape | First press: clear suggestions. Second press: clear input. |
| Home / End | Usually used for cursor-within-text, not list nav |
| Typing | Updates query, fetches new suggestions |

Focus stays in the input. Selected option is indicated via `aria-activedescendant` pointing to the highlighted `<li>`.

## Suggestion list design

```
┌──────────────────────────────────────┐
│ Recent                               │
├──────────────────────────────────────┤
│ 🕓  Q4 roadmap                       │
│ 🕓  sprint planning notes            │
├──────────────────────────────────────┤
│ Results                              │
├──────────────────────────────────────┤
│ 📄  Q4 Roadmap 2026.pdf              │
│     in /Projects/Planning            │
│                                      │
│ 👤  Quinn Barrett                    │
│     Product Manager                  │
└──────────────────────────────────────┘
```

- Section headers (small, uppercase, muted) separate categories: Recent, People, Files, etc.
- Each result: primary text (title) + optional secondary (path, role, metadata).
- Highlight matching query substring with `<mark>` or CSS bold.
- Icon or avatar per result type for visual categorization.
- First suggestion highlighted by default so Enter works without ArrowDown.

## Result limits

| Context | Max suggestions |
|---|---|
| Inline autocomplete | 5–8 |
| Command palette | 8–12 visible, scroll for more |
| Full search results page | Paginate, 20–50 per page |

Truncate with a "Show all 47 results" action rather than infinite inline.

## Empty states

| State | Message |
|---|---|
| Initial (no query) | Show recent searches, suggested actions, or navigate shortcuts |
| No results | "No results for 'xyz'. Try broader terms." + optional suggestions |
| Error | "Couldn't reach search. [Retry]" |
| Loading | Skeleton rows or spinner (≥ 200ms loads) |

"No results" should help the user recover: remove a filter, try different terms, link to browse.

## Command palette (⌘K)

Command palettes are search + actions combined. Common shortcut: ⌘K (Mac) / Ctrl+K (Win/Linux).

Rules:
- Modal overlay with backdrop.
- Focus trapped inside.
- Escape closes.
- Shortcut hints visible (⌘K, ↵, Esc).
- Shows recent/default actions when empty.
- Filters actions + content + navigation in a unified list.
- Works entirely keyboard-first.

## Search results page

Beyond the inline autocomplete:

- Echo the query prominently at the top.
- Show total result count.
- Breakdown by category (files, people, projects) with counts.
- Filters (date, type, owner) as sidebar or chip row.
- Each result: title + context + metadata + path.
- Pagination or virtualization for large result sets.
- Sort options: Relevance (default), Date, Name.

## Recent searches

- Store client-side (localStorage or cookie).
- Show on empty input focus.
- 5–8 most recent, reverse chronological.
- Clear button per item + "Clear all".
- Surface in the same list format as suggestions.

## Fuzzy matching

- Forgive typos: "feb" matches "February".
- Handle diacritics: "rene" matches "René".
- Handle partial words: "dash" matches "dashboard".
- But don't overreach — "x" matching every word with an x is worthless.

Libraries like Fuse.js, MiniSearch, FlexSearch handle this client-side.

## Mobile

- 16px minimum input font size (iOS zoom).
- Full-width input, taking the top bar.
- On focus, dedicate screen to search: hide page chrome, show cancel button, show recent/suggestions below.
- Back button exits search.
- Tap-to-clear, not hover.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Placeholder as the only label | Disappears on focus; WCAG 3.3.2 |
| No clear button | Users can't quickly reset |
| Firing a fetch on every keypress | Rate-limits hit, janky UX |
| Search input smaller than 16px on mobile | iOS zoom-on-focus, annoying |
| No keyboard support for suggestion list | Accessibility fail |
| Suggestions appear/disappear before users can click | Race condition |
| No "no results" state | Users think search is broken |
| Results page without query echo | Users forget what they searched |
| No recent searches | Users retype the same thing |
| Search icon inside input but not clickable to submit | Confusing affordance |
| Case-sensitive search | Users don't think in case |

## Decision tree

```
Is the search query expected to be identifier-like (SKU, ticket ID, slug)?
  ├─ Yes → autocomplete="off", spellcheck="off", case-insensitive exact match
  └─ No → Natural-language friendly, fuzzy matching, spellcheck on

Should suggestions appear as you type?
  ├─ Yes → Combobox pattern with aria-autocomplete="list"
  └─ No → Simple form submit on Enter

Is search tied to commands (actions + navigation)?
  └─ Yes → Command palette with ⌘K shortcut

Results > 5?
  └─ Paginate or virtualize
```

## Audit checklist

- [ ] `<form role="search">` wrapper
- [ ] Label present (visually hidden OK)
- [ ] `type="search"`
- [ ] 16px minimum font size on mobile
- [ ] Clear button appears when input has value
- [ ] Debounce 150–250ms on autocomplete fetches
- [ ] Combobox ARIA pattern used for suggestions
- [ ] ArrowUp/Down navigate suggestions
- [ ] Enter submits or activates highlighted suggestion
- [ ] Escape has two-stage clear (suggestions, then input)
- [ ] Empty state has a recovery path
- [ ] Recent searches surfaced on focus
- [ ] Results page echoes query + count
- [ ] Result snippets show match highlight
- [ ] Case-insensitive matching
- [ ] Mobile keyboard shows "search" button

## Sources

- WAI-ARIA Authoring Practices · Combobox, Listbox
- WCAG 2.2 · 2.1.1 Keyboard, 3.3.2 Labels or Instructions, 1.4.13 Content on Hover or Focus
- Nielsen Norman · "Search Is Not Enough" (faceted search + navigation)
- Material Design 3 · Search bar
- Apple HIG · Search Fields
