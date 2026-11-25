---
name: canon-pagination
description: Use when designing, auditing, or refactoring pagination, page numbers, prev/next controls, infinite scroll, load-more buttons, or any pattern for traversing long lists. Covers pagination vs infinite scroll vs virtualization, when each wins, page-number layout, URL behavior, keyboard navigation, and the "where was I" problem. Trigger when the user mentions pagination, paginate, page number, prev/next, infinite scroll, load more, or virtualized list.
---

# CANON · Pagination

Long lists need traversal. Pick the pattern to match the task, not the fashion.

## The three patterns

| Pattern | Use when |
|---|---|
| **Pagination** (numbered pages) | Users compare, revisit, bookmark, or share specific positions |
| **Infinite scroll** | Feed-style discovery where "what's next" is primary (social, news) |
| **Load more** (button) | Discovery with control — user decides when to fetch more |
| **Virtualized list** | 10,000+ items where semantics matter (tables, ordered lists) |

Default: **pagination** for task-oriented UIs (search results, tables, admin lists). Infinite scroll is a feed pattern, not a universal answer.

## Why pagination beats infinite scroll for most apps

- **Position is addressable** — users can bookmark page 5, share a URL, return to where they were.
- **The footer is reachable** — infinite scroll eats footers.
- **Users know when they're done** — "Page 12 of 47" gives a clear scale.
- **Browser back button works** — infinite scroll loses scroll position on navigation.
- **Screen readers** — paginated pages announce completion.

Infinite scroll wins for: Twitter-style feeds, image galleries, TikTok-style single-item-at-a-time.

## Pagination layout

Two patterns, both valid:

### Numbered pages

```
←  1  2  3  …  47  48  49  →
```

- Show: first page, last page, current page, two neighbors on each side.
- Ellipsis between gaps.
- Prev/Next arrows bracket the numbers.
- Current page visually distinct (filled, disabled, not a link).

### Simple prev/next with position

```
Showing 21–40 of 934        ←  Previous  |  Next  →
```

- Position text is always visible.
- Prev disabled on page 1. Next disabled on last page.
- Works when page count is unknown (live data).

Use numbered pagination when the total is known; use simple prev/next when it isn't.

## Sizing

| Element | Value |
|---|---|
| Button height | 36–40px |
| Button min-width | 36–40px (square for numbers) |
| Gap between buttons | 2–4px |
| Horizontal padding | 8–12px |

Mobile floor: 44×44px tap target.

## Total count — always show it

```
Showing 1–20 of 487 projects
```

Users need scale. "Showing 20 projects" without total leaves them blind to how much more exists.

## Per-page selector (optional)

When users work with lots of data, let them set the page size:

```
Per page: [20 ▾]  [50]  [100]
```

Default: 20–25 for tables, 10–15 for cards, 50 for dense lists.

Persist the choice (localStorage) so it carries across sessions.

## URL sync — required for pagination

```
/projects?page=3
/projects?page=3&per_page=50&sort=name
```

- Pagination state lives in the URL.
- Back button works.
- Links can be shared.
- Refresh doesn't reset position.

Without URL sync, pagination is half-broken.

## Keyboard

| Key | Behavior |
|---|---|
| Tab | Through pagination buttons |
| Enter / Space | Activate page link or button |
| Arrow keys (optional) | Prev/next page — nice power-user feature |
| Home / End (optional) | First / last page |

Don't trap arrow keys in the pagination when they have other meaning on the page.

## Load more button

```
[Results 1–20 of 487]
[Show 20 more ↓]
```

Hybrid between pagination and infinite scroll:
- Loaded items stay on screen.
- User controls when to load.
- Scroll position preserved.
- No URL position (or use hash fragments).

Good for: gallery views, discovery feeds where users sometimes want more context, mobile.

## Infinite scroll — if you must

Rules that make it less bad:

- **Load more 400–600px before the bottom.** Feels seamless.
- **Show a spinner during fetch.** User knows more is coming.
- **Sticky footer access.** Add a "Jump to footer" link or make the footer reachable via keyboard command.
- **Track scroll position on navigation away.** Restore on return via `history.scrollRestoration = 'manual'`.
- **Show item number or timestamp** so users know where they are.
- **Stop eventually.** Show "You've reached the end" when no more data.

## Virtualization

For tables or lists with 1,000+ items where you want pagination-like UX with scroll-like feel:

- Render only visible items (+ buffer above and below).
- Use known row height for predictable scrollbar.
- Maintain semantic structure (table rows, list items).
- Libraries: react-virtuoso, TanStack Virtual, @tanstack/virtual-core.

For dynamic row heights, more care is needed; plan for it.

## Semantic markup

```html
<nav aria-label="Pagination">
  <ul class="pagination">
    <li>
      <a href="?page=2" aria-label="Previous page" rel="prev">← Previous</a>
    </li>
    <li>
      <a href="?page=1">1</a>
    </li>
    <li>
      <a href="?page=2">2</a>
    </li>
    <li>
      <a href="?page=3" aria-current="page">3</a>
    </li>
    <li>
      <a href="?page=4">4</a>
    </li>
    <li>
      <a href="?page=4" aria-label="Next page" rel="next">Next →</a>
    </li>
  </ul>
</nav>
```

- `<nav aria-label="Pagination">` — screen readers announce the landmark.
- Use `<a>` with real URLs (not JS-only buttons) — right-click, middle-click, open-in-tab all work.
- `aria-current="page"` on the active page.
- `rel="prev"` and `rel="next"` for browser hints.

## Loading state during page change

- First load: skeleton for page content.
- Between-page loads: overlay with 60% opacity + spinner on the list area. Pagination controls stay enabled after load.
- Don't reset scroll position to top on page change for paginated lists (unless the user expects it — search results page typically does).

## Empty pagination

- No items total → empty state, no pagination.
- Items fit on one page → no pagination controls at all (don't show "Page 1 of 1").
- Accidentally navigating to page beyond last → redirect to last valid page with a message.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Infinite scroll on a task-oriented list (admin table) | Users can't bookmark, share, or revisit positions |
| No total count | Users can't judge scale |
| No URL sync | Refresh loses position |
| Using buttons with JS handlers instead of `<a>` links | Middle-click, right-click broken |
| Current page styled identical to other pages | Can't tell where you are |
| Pagination controls at top of page only | Users scroll to bottom to see more, then have to scroll back up to paginate |
| "Next" button disabled without explanation | Users don't know they're on the last page |
| Showing all 47 page numbers | Cluttered and useless |
| Page size changes scroll to a random spot | Disorienting |
| Load-more that removes old results | Users lose reference context |
| Infinite scroll with no "end" indicator | Users scroll forever wondering |

## Decision tree

```
Are users task-oriented (searching, filtering, comparing)?
  ├─ Yes → Pagination
  └─ No → Continue

Is it a feed (discovery, what's new)?
  ├─ Yes → Infinite scroll or load-more
  └─ No → Continue

Are there 10,000+ items?
  ├─ Yes → Virtualize
  └─ No → Pagination still works

Unknown total?
  └─ Simple prev/next with "Showing X–Y"
```

## Audit checklist

- [ ] Total count always shown
- [ ] URL syncs to page number
- [ ] Pagination uses `<nav aria-label>`
- [ ] Active page has `aria-current="page"`
- [ ] Prev/Next use real `<a>` elements when possible
- [ ] Current page visually distinct
- [ ] Prev disabled (or hidden) on first page
- [ ] Next disabled (or hidden) on last page
- [ ] Pagination duplicated at top AND bottom of long lists
- [ ] Mobile tap targets ≥ 44px
- [ ] Page-size selector persists across sessions
- [ ] Browser back button returns to previous page position
- [ ] Empty state shown when no items, no pagination displayed
- [ ] Single-page result hides pagination

## Sources

- WCAG 2.2 · 2.4.1 Bypass Blocks, 2.4.5 Multiple Ways, 4.1.2 Name, Role, Value
- Nielsen Norman · "Infinite Scrolling is not for Every Website"
- Smashing Magazine · pagination research
- Material Design 3 · Pagination
- Apple HIG · List views, pagination patterns
