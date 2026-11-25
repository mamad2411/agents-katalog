---
name: ui-part-empty-states
description: "Empty states that help: first use, no results, cleared, filtered to nothing, no permission and failed to load, each saying why it is empty and offering the one action that fills it. Read before building any view that can be empty."
---

# Empty states

The generated empty state is a grey box icon over "No data", the same for
every reason, or a full-page illustration with a joke and nothing to click.
Worse, it flashes up while the data is still loading, or stands in for a
request that failed, telling people they have nothing when the server never
answered. This skill tells the kinds apart, gives each its words and its one
action, and puts it in the region it replaces. Principles are in `ui`,
measures in `ui-layout`, words in `writing`.

## 1. Tell the kinds apart

| Kind | When | It says | The action |
|---|---|---|---|
| First use | The collection has never had a record | What will appear here, and why it helps | Create the first one; import as a link |
| No results | A search or filter the user set matched nothing | The query and the filters that are on | Clear filters; a spelling suggestion if the engine has one |
| Filtered to nothing | A built-in view is empty (Overdue, Assigned to me) | That this is good or neutral news | Usually none; a link to the full list |
| Cleared | The user finished the work (inbox zero) | Done, and what happens next | None needed |
| Not yet | The data comes from outside (first event, first sale) | What it is waiting for | The setup step: a snippet, a connection |
| No permission | Records exist that this user cannot see | Who can grant access | Request access, when it is wired |
| Failed to load | The request failed | Not an empty state: an error (`frontend-errors`) | Retry |
| Loading | No answer yet | Nothing: a skeleton (`ui-part-loading`) | None |

## 2. Decide from the data, not from an empty array

An empty array can mean any row of that table. Decide in one function that
every list shares, so they all agree:

```ts
type EmptyKind = "loading" | "error" | "no-access" | "no-results" | "cleared" | "first-use";

export function emptyKind(q: {
  isPending: boolean; isError: boolean; status?: number;
  count: number; hasAny: boolean; userFiltered: boolean;
}): EmptyKind | null {
  if (q.isPending) return "loading";
  if (q.isError) return q.status === 403 ? "no-access" : "error";
  if (q.count > 0) return null;
  if (q.userFiltered) return "no-results";
  return q.hasAny ? "cleared" : "first-use";
}
```

- The API says whether the unfiltered collection has any record (`hasAny`,
  or the unfiltered total beside the page). Without it, first use and
  cleared look the same.
- `userFiltered` is true when the search or any filter differs from the
  view's default. An empty built-in view ("Overdue") is not a failed
  search: it takes the cleared wording with the view's name.
- "Not yet" is first use for data that arrives from outside: the same slot,
  its own words.
- With TanStack Query, `isPending` means no data yet: a skeleton, never
  "No results".

## 3. The words for each kind

Plain and specific, in the product's own nouns (`writing`); plurals and the
quoted query through `i18n`, the query escaped because it is user input.

- **First use**: what appears here and why, then the step. "Invoices you
  send appear here. Create one, or import them from a spreadsheet."
  [Create invoice] · Import CSV
- **No results**: echo the query and name the filters that are on. "No
  books match 'tolkein'. Did you mean Tolkien?" (the suggestion only when
  the search engine returns one). "Two filters are on: Branch Kemang,
  Available now." [Clear filters]
- **Filtered to nothing**: the good news is the message. "Nothing is
  overdue."
- **Cleared**: "All caught up. New requests will appear here."
- **Not yet**: "No events yet. Send the first one with the snippet below;
  this page updates when it arrives." Claim it is listening only when the
  page really polls or subscribes.
- **No permission**: "You don't have access to Payroll. Ask a workspace
  owner to add you." Name the owners when the user may know them; show
  [Request access] only when the request reaches someone.

A heading of two to six words, a body of one or two sentences, the action a
verb and an object. No "Oops", "No data", "Nothing to see here",
exclamation marks, or jokes on errors and permission screens.

## 4. Where it sits, and how big

- In the region it replaces: the table body, the list, the panel, the
  chart's plot area, the dashboard block. The page header, the toolbar,
  the search and the filters stay, so people can change what emptied it.
- Centred in that region as one short block, the text at most 40 to 48ch,
  48 to 96px of space above and below in a large region.
- Type: the heading one step above body (16 to 20px, semibold), the body
  14 to 16px in the muted colour at 4.5:1, 8px between them, 16 to 24px
  above the action.
- A table keeps its header row and gets one row spanning every column, 48
  to 96px tall, so the columns still say what the table holds
  (`ui-part-tables`).
- A small block (a dashboard card, a side list): one muted line and a
  link, "Nothing due this week · See all tasks", in the block's own padding.

```html
<tbody>
  <tr>
    <td colspan="6">
      <div class="empty">
        <h3>No books match 'tolkein'</h3>
        <p>Two filters are on: Branch Kemang, Available now.</p>
        <button type="button">Clear filters</button>
      </div>
    </td>
  </tr>
</tbody>
```

```css
.empty {
  display: grid; justify-items: center; gap: var(--s-2);
  max-width: 44ch; margin-inline: auto; padding-block: var(--s-8);
  text-align: center;
}
.empty p { color: var(--text-muted); }
.empty button { margin-top: var(--s-3); }
```

## 5. The action

- One primary action, the one that fills the view, and at most one
  secondary link (import, a template, the page that explains the feature).
- A real `button`, or a link when it goes to a create page, and it works: a
  button that does nothing is worse than none (`ui`, section 8).
- The page header keeps its own create button; the empty state repeats the
  same action with the same words, so nothing moves when the first record
  arrives.
- No action the user cannot take: without permission to create, say who
  can ("Only admins add members") rather than showing a disabled button.
- When the action succeeds, the new record replaces the empty state in
  place, and focus goes to it or to the list's heading.

## 6. Illustration and sample data

- An illustration is optional. When used: small (64 to 120px), from the
  product's own world in its icon style, or a faded preview of what a
  filled row will look like, which teaches the layout. Never blobs, people
  at laptops, 3D shapes, a sad face, or one picture on every empty state.
- It is decoration: `alt=""` or `aria-hidden="true"`, coloured from the
  tokens so it holds in the dark theme (`ui-themes`).
- None in tables, small blocks or search results: the words do it.
- Sample data only on request ("Explore with sample data"), labelled on
  every record and in a banner above the list, removable in one action, and
  kept out of counts, reports, exports, billing and anything sent to real
  people. A template is often the better second action.

## 7. Never empty when it is not

- Loading: a skeleton after about 200ms (`ui-part-loading`), never "No
  results" while the first request is in flight.
- Refetching after a filter change: keep the previous rows, dimmed, until
  the new answer arrives (`placeholderData: keepPreviousData` in TanStack
  Query), so a quick filter does not flash an empty state.
- Typing a search: judge the settled query (debounced 200 to 300ms), not
  each keystroke.
- Failed: an error in the same region with what failed and Retry, keeping
  the last good data when there is some (`frontend-errors`).
- The last record deleted: the view becomes cleared or first use, with the
  undo toast still on screen (`ui-part-notifications`).
- On a dashboard, only the block that is empty says so; the others carry
  on.

## 8. Accessibility, phone, themes, motion

- A heading at the level the region's outline needs, the body in a `p`,
  the action a real control with its words.
- For a search, the polite status region that says "24 results" says "No
  results for tolkein" once the query settles (`role="status"`, in the page
  before its text changes). A first-use state is not announced: it is
  content.
- After Clear filters, focus goes to the search field or the results
  heading, not to the top of the page.
- On a phone: the same block with 32 to 48px of padding, under the search
  bar, the action at least 44px tall.
- Muted text, illustration and action from tokens in both themes
  (`ui-themes`); the swap between empty and filled is a fade of 150 to
  200ms or nothing (`motion-interface`, section 9).

## Check it

- Force every state on every list and block: a fresh account, a search
  that matches nothing, filters that empty the list, an empty built-in
  view, a user without access, the endpoint failing (block the request in
  DevTools, or an MSW handler returning 500), and a throttled network.
  Each shows its own words; none says "No results" before data arrives.
- Delete the last record, then undo.
- `preview` at 360, 768 and 1440px, with `login` for screens behind
  sign-in: the block sits in its region, the toolbar stays, the action is
  44px on a phone.
- `ui_check` for generic copy and stock illustrations.
- A screen reader hears the no-results message once, not per keystroke.

## Avoid

"No data" for every kind; an empty state while loading or after a failed
request; the whole page replaced, with the filters that caused it hidden; a
large generic illustration pushing the action out of view; jokes on errors
or permission screens; a disabled button with no reason; two or three equal
buttons; sample data that looks real, cannot be removed or leaks into
reports; first-use wording on a list that is merely filtered.
