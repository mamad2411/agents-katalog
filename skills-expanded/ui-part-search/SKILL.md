---
name: ui-part-search
description: "Search: which kind to build, the labelled field and its shortcut, submitted or instant results with debouncing and cancelling, suggestions with the combobox pattern, the results page and its URL, filters with counts, the no-results state, engines for static sites and servers, and search on phones. Read before adding a search field, suggestions or a results page."
---

# Search

The generated version: a rounded field with a magnifier and "Search..." in
grey, no label, a ⌘K badge that opens nothing, results fired on every
keystroke that arrive out of order, and "No results" alone on a blank
page. Search is a short conversation: the field says what can be found,
the results say how many were found for what, and a failed search says
what to try next. The principles are in the `ui` skill, the measures in
`ui-layout`; an app's jump-to-anything is `ui-part-command-palette`.

## 1. Which search

- **Site search** (docs, a shop, a blog): a field or a named button in the
  header, and a results page with the query in its URL.
- **Filtering a list in place**: the field first in the list's toolbar, 240
  to 400px wide, results instant (`ui-layout`, section 4).
- **Suggestions while typing**: a combobox under the field (section 4).
- **An application's places and actions**: a command palette
  (`ui-part-command-palette`), not a site search in disguise.
- A search box that searches nothing yet is left out, and so is a shortcut
  hint for a search that does not exist.

## 2. The field

- A labelled input with a button or Enter to search: `<search>` (or a `form`
  with `role="search"`), `<input type="search" name="q">` with a `<label>`
  (visible, or visually hidden when the icon and the button make it
  plain), and a submit button named "Search".
- A placeholder that is a real example query from the content ("Try:
  rotate an API key"), never the only label.
- `enterkeyhint="search"` so a phone's keyboard shows Search; 16px text on
  phones so iOS does not zoom; `autocomplete="off"` when your own
  suggestions replace the browser's.
- 40px tall on desktop, 44px on touch; a clear button named "Clear search"
  once there is text; Escape clears.
- A keyboard shortcut shown in the field as a `<kbd>` hint: `/` for a
  site's search, Cmd or Ctrl+K for a command palette. Hidden on touch
  devices, and ignored while the user types in another field.

## 3. Submitted or instant

- **Submitted** (Enter or the button) when the results are a page of their
  own, or each search costs a request to a large index.
- **Instant** when the data is local or cheap: debounce 150 to 300ms, start
  at 2 characters, cancel the stale request (`AbortController`) and ignore
  any answer to an old query, keep the previous results on screen while
  the new ones load, and show a small spinner in the field after 300ms.
- Either way the query is kept in the URL (`?q=`), so back, reload and a
  shared link return the same results.

## 4. Suggestions: the combobox pattern

- The input has `role="combobox"`, `aria-expanded`, `aria-controls` naming a
  `role="listbox"`, and `aria-autocomplete="list"`. Focus stays in the
  input; `aria-activedescendant` names the highlighted option.
- Down Arrow opens the list and moves, Up moves back, Enter takes the
  highlighted option (or searches the typed text when none is highlighted),
  Escape closes the list and a second Escape clears, Tab leaves.
- 8 to 10 suggestions at most, the matching part in `<mark>`, grouped when
  it helps (Recent, Pages, Products) under group labels; the count
  announced politely ("6 suggestions").
- Recent searches when the empty field gets focus: the last five, kept on
  the device, each removable, and "Clear recent searches".
- Use a library: React Aria `ComboBox`, Downshift's `useCombobox`, Headless
  UI or Ariakit `Combobox`, Ark UI or Bits UI in other stacks.

## 5. The results page

- The query stays in the field, and the results say how many were found
  for what, above the list: `24 results for “invoice template”`. The count
  is real; an engine's estimate says "About 1,200".
- The page's `<title>` holds the query ("invoice template: 24 results"), so
  history and screen readers say where the user is.
- Each result: the title as the link, where it lives ("Guides › Billing"),
  a snippet with the matched words in `<mark>`, a date when recency
  matters.
- Filters and facets with counts ("PDF (12)"): beside the results on wide
  screens; on phones in a sheet behind a "Filters" button that shows how
  many are on. Sorting (Relevance, Newest). Pagination
  (`ui-part-pagination`).
- New results announce their count politely; focus stays in the field for
  instant search and moves to the results heading after a submitted one.
- Results pages carry `noindex` (`frontend-seo`).

## 6. No results

- A no-results state that suggests what to try: it says so with the query
  (`No results for “invioce”`), offers the spelling the engine suggests
  ("Did you mean invoice?"), lists the filters that are on with a way to
  clear them, and offers other ways in: categories, the most visited
  pages, a contact route (`ui-part-empty-states`). Never a blank region.
- Log the queries that found nothing, without personal data: they show
  which pages or synonyms are missing.

## 7. Engines

- **A static site**: Pagefind (indexes the built site, searches in the
  browser, ships a UI), or Algolia DocSearch for documentation.
- **A small list in the browser** (up to a few thousand items): MiniSearch
  or FlexSearch, Fuse.js for fuzzy matching.
- **On the server**: PostgreSQL full-text search (`tsvector` with
  `websearch_to_tsquery`) and `pg_trgm` for typos; Meilisearch or Typesense
  when relevance, typo tolerance and facets matter; Elasticsearch or
  OpenSearch at a large scale.
- Search checks access like any other read: a result never shows what the
  user may not open.

## 8. Phones, themes and motion

- On phones a named search button in the header opens a full-screen
  search: the field focused at once (call `focus()` inside the tap's
  handler, or iOS will not raise the keyboard), a Cancel button, recent
  searches, the results in the same view; Back closes it.
- Themes: the `<mark>` colour is a token per theme with its text at 4.5:1;
  the browser's default yellow glares on dark (`ui-themes`).
- Motion: suggestions appear without sliding and the highlight moves
  instantly; the full-screen view fades or slides in over 200ms, not at all
  under reduced motion (`motion-interface`, section 2).

## 9. A sketch

```html
<search>
  <form action="/search" method="get">
    <label for="q" class="visually-hidden">Search the documentation</label>
    <input id="q" name="q" type="search" placeholder="Try: rotate an API key"
           enterkeyhint="search" autocomplete="off">
    <button type="submit">Search</button>
  </form>
</search>
```

```ts
// Instant results: debounced, stale requests cancelled, the query in the URL.
let controller: AbortController | undefined;
let timer: number | undefined;

input.addEventListener("input", () => {
  window.clearTimeout(timer);
  timer = window.setTimeout(async () => {
    const q = input.value.trim();
    controller?.abort();
    history.replaceState(null, "", q ? `?q=${encodeURIComponent(q)}` : location.pathname);
    if (q.length < 2) return showRecent();
    controller = new AbortController();
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`, {
        signal: controller.signal,
      });
      if (!res.ok) throw new Error(`search failed: ${res.status}`);
      showResults(q, await res.json());
    } catch (error) {
      if ((error as Error).name !== "AbortError") showError(q);
    }
  }, 200);
});
```

## Check it

- Keyboard: `/` (or Cmd+K) focuses the field, but not while typing
  elsewhere; the arrows move through suggestions, Enter takes one, Escape
  closes and then clears. A screen reader hears the field's name, the
  number of suggestions and the number of results.
- Type fast, then slowly: one request per pause, and no old results
  replacing new ones.
- Reload a results URL: the same query, filters and page. Search for
  nonsense and for a misspelling: the no-results state helps.
- `preview` at 360px: the field and its button fit, an icon-only button
  shows up in "controls without a name", targets reach 44px.

## Avoid

A search box that searches nothing yet; a ⌘K hint with nothing behind it;
a placeholder as the only label; a request on every keystroke with nothing
cancelled; results that lose the query on reload; "No results" and
nothing else; counts that are guesses; suggestions the keyboard cannot
reach; a highlight colour that fails contrast on dark; results the user
has no right to see.
