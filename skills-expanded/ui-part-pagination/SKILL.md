---
name: ui-part-pagination
description: "Pagination and loading more: numbered pages, Previous and Next over cursors, Show more and infinite scroll, paging on the server in a stable order, the range and total, page size, the page in the URL, focus and scroll after a change, phones, and public paged pages. Read before building any list that can grow past one screen."
---

# Pagination and loading more

The generated version: every row fetched and sliced in the browser, ten
page numbers that run off a phone, page 3 that resets to page 1 on back,
an infinite scroll that makes the footer unreachable, and a total that
changes as you page. Pagination is a promise about position: where the
reader is, how much there is, and that going back returns them to the same
place. The principles are in the `ui` skill, the measures in `ui-layout`,
the API side in `backend-api` (section 5).

## 1. Choose by the task

| Pattern | For | Needs |
|---|---|---|
| Numbered pages | lists people navigate and come back to: search results, records, admin tables | a total, the page in the URL |
| Previous and Next | cursor-based APIs; very large or growing lists | the cursor in the URL |
| A "Show more" button | feeds and catalogues read from the top | the depth kept on back |
| Infinite scroll | endless feeds (activity, social) where nothing needs the footer | the position kept on back, a reachable footer |

- Numbered pages when position matters (search results, records); a "Show
  more" button for feeds; infinite scroll only when nothing needs the
  footer, and never without keeping the scroll position on return.
- No controls when everything fits on one page.

## 2. On the server

- On the server, always, once a list can pass a couple of hundred rows:
  the page, the sort and the filters go into the query (`LIMIT` with a
  cursor or an offset, backed by an index), and the response carries the
  rows and either the total or whether there is more.
- Cursor pagination (`?after=<cursor>`) for long or growing lists, where an
  offset gets slow and skips rows as new ones arrive; page numbers with a
  total ("1 to 25 of 1,284") when the reader jumps around.
- The order is stable: the sort column, then the id, so no row repeats or
  goes missing between pages. The cursor is opaque: the last row's sort key
  and id, encoded.
- Ask for one row more than the page to learn whether there is a next page
  without counting.
- A total over a very large table is costly: count once per filter and
  cache it, or say "More than 10,000", rather than a page count that jumps
  as you page.

```sql
-- PostgreSQL keyset page; the cursor carries the last row's created_at and id.
SELECT id, number, total, created_at
FROM invoices
WHERE status = $1
  AND (created_at, id) < ($2, $3)
ORDER BY created_at DESC, id DESC
LIMIT 26; -- 25 to show, one more to know there is a next page
-- Backed by: CREATE INDEX ON invoices (status, created_at DESC, id DESC);
```

## 3. Numbered pages

- `<nav aria-label="Pagination">` around a list: Previous, the numbers,
  Next.
- The first, the last, the current page and one on each side, an ellipsis
  for each gap: Previous 1 … 4 5 6 … 20 Next. Seven numbers at most; fewer
  on phones.
- Every page a real link to its URL (`?page=5`): it works without
  JavaScript, opens in a new tab and can be shared. Page 1 is the plain URL,
  with no `?page=1`.
- The current page carries `aria-current="page"` and is filled or outlined
  and bold, not marked by colour alone.
- The ends: on page 1 there is no Previous link, but a `span` with
  `aria-disabled="true"` keeps its place so nothing shifts; the same for
  Next on the last page.
- Previous and Next are words, with a chevron if you like, never chevrons
  alone; numbers may carry `aria-label="Page 5"`.
- 36 to 40px squares on desktop, 44px on touch, 4px apart, in
  `tabular-nums` so the row does not twitch as the numbers change.
- In a table, the range and total at the start of the footer and the
  controls at its end (`ui-part-tables`): "51 to 100 of 1,240", formatted
  for the locale (`Intl.NumberFormat`).
- A page size of 25 by default, with 50 and 100 to choose from in tables
  ("Rows per page"); changing it returns to page 1.
- The page, the size, the sort and the filters in the URL, so back and
  reload return to the same page; changing a filter goes back to page one.
- A page past the end (`?page=99` of 20): the last page, or a line saying
  there is no page 99 with a link to page 1; never an empty table with no
  explanation.

## 4. Changing page

- While the next page loads, the current one stays on screen, dimmed, and
  the controls show the wait (`ui-part-loading`).
- Then the top of the list is in view (scroll to the list, not to the top of
  the page when the list sits lower), and focus moves to the list's heading
  or its count (`tabindex="-1"`), so the next Tab starts in the new page.
- Back keeps the scroll position: the browser does it for full page loads;
  a single-page app keeps the pages in its query cache so the list renders
  at once, then restores the scroll.

## 5. Show more and infinite scroll

- "Show more" at the end of the list says what it does ("Show 24 more")
  beside the count so far ("Showing 48 of 312"). On a press the next page
  is appended, focus moves to the first new item (its link, or a heading
  with `tabindex="-1"`), and a `role="status"` line says "24 more products
  loaded".
- The depth goes in the URL (`?page=3`, with `history.replaceState`), and
  back renders pages 1 to 3 and restores the scroll.
- Infinite scroll: an IntersectionObserver on a sentinel 600 to 1000px
  before the end loads the next page; after two or three automatic loads a
  "Show more" button takes over, so the footer can be reached. Or the screen
  has no footer at all.
- A screen that is only an endless feed can follow the APG feed pattern:
  `role="feed"`, `article`s with `aria-setsize` and `aria-posinset`,
  `aria-busy` while more load.
- Very long results are virtualised (`ui-part-lists`, section 5).

## 6. Phones

- Fewer numbers: "Previous · Page 5 of 20 · Next" with 44px targets, or the
  label with a select to jump.
- A table's footer stacks: the count above, the controls below at full
  width.
- For catalogues on a phone "Show more" is often better: one large target
  at the end of the list.

## 7. Themes, motion, search engines

- The current page's fill and border from tokens, 3:1 in both themes
  (`ui-themes`).
- No animation beyond the dimming; new items arrive without a stagger;
  scrolling is instant under reduced motion (`motion-interface`).
- Public paged lists (a blog, a catalogue): each page has its own canonical
  URL (not canonical to page 1), crawlable `<a href>` links and a distinct
  title ("Articles, page 2"). `rel="next"` and `rel="prev"` do no harm but
  Google no longer reads them (`frontend-seo`).

## 8. A sketch

```ts
/** The page numbers to show: the first, the last, the current one and its
 * neighbours, with "…" for each gap. pageItems(5, 20) gives
 * [1, "…", 4, 5, 6, "…", 20]. */
export function pageItems(current: number, total: number, siblings = 1): (number | "…")[] {
  if (total <= 1) return [];
  const pages = new Set([1, total]);
  for (let p = current - siblings; p <= current + siblings; p++) {
    if (p > 1 && p < total) pages.add(p);
  }
  const sorted = [...pages].sort((a, b) => a - b);
  const items: (number | "…")[] = [];
  sorted.forEach((page, i) => {
    const gap = i > 0 ? page - sorted[i - 1] : 1;
    if (gap === 2) items.push(page - 1); // a gap of one page shows that page
    else if (gap > 2) items.push("…");
    items.push(page);
  });
  return items;
}
```

```html
<nav aria-label="Pagination">
  <ul class="pages" role="list">
    <li><a href="/articles?page=4" rel="prev">Previous</a></li>
    <li><a href="/articles" aria-label="Page 1">1</a></li>
    <li><span aria-hidden="true">…</span></li>
    <li><a href="/articles?page=4" aria-label="Page 4">4</a></li>
    <li><a href="/articles?page=5" aria-current="page" aria-label="Page 5">5</a></li>
    <li><a href="/articles?page=6" aria-label="Page 6">6</a></li>
    <li><span aria-hidden="true">…</span></li>
    <li><a href="/articles?page=20" aria-label="Page 20">20</a></li>
    <li><a href="/articles?page=6" rel="next">Next</a></li>
  </ul>
</nav>
```

## Check it

- Go to page 3, open a row, press back: page 3 at the same scroll. Reload:
  page 3. Change a filter: page 1.
- `preview` at 360px: the control fits without overflow, targets reach 44px,
  and no link goes nowhere.
- Keyboard: Previous, the numbers and Next in order, the current page
  announced; after "Show more", focus is on the first new item and the
  count is announced.
- `EXPLAIN` the list's query: the index serves the filter and the sort; no
  request fetches every row.

## Avoid

Fetching every row to paginate in the browser; a page count that jumps as
you page; pages that lose the filters; ten numbers on a phone; chevrons
without words; the current page marked by colour alone; infinite scroll in
front of a footer; a "Show more" that forgets its depth on back; offset
paging on a feed that grows while people read it; a page change that
leaves focus at the bottom of the old page.
