---
name: ui-part-loading
description: "Loading and progress: what to show for each length of wait, loading per block rather than per page, skeletons shaped like the content, keeping old data during a refresh, busy buttons, optimistic updates, spinners and progress bars, streaming, screen reader announcements, and no layout shift. Read before building any state where the interface waits for data or work."
---

# Progress and loading

The generated version: a full-page spinner for every request, grey bars in
a layout the data never fills, content that jumps when it lands, a
progress bar that eases to 90% and waits, and a Save button that can be
pressed five times while it saves. A loading state answers three
questions: is something happening, what, and for how long. The principles
are in the `ui` skill, the measures in `ui-layout`, the motion in
`motion-interface` (section 11).

## 1. Choose by the wait

| The wait | Show |
|---|---|
| Under about 200 to 300ms | nothing: a spinner that flashes is worse than none |
| The first load of a region of content | a skeleton shaped like the content, appearing after about 200ms |
| 300ms to 2 or 3s, for an action or a small widget | the control's own busy state, or an inline spinner with text |
| Past about 3s | progress with a label saying what is happening; a bar with numbers when progress is known |
| Past about 10s | say it is still working, and offer to carry on while it runs in the background and notify when done (`backend-jobs`) |

- About 0.1s feels instant, 1s keeps the train of thought, 10s is as long
  as attention holds (Nielsen's limits). Aim for most actions under 1s.
- Once an indicator shows, keep it at least about 400ms so it does not
  flicker (the `spin-delay` hook does the delay and the minimum).

## 2. Per block, not per page

- Each part of a screen loads its own data and shows its own skeleton, so
  the fast parts appear first and one slow query blanks nothing else. The
  frame (navigation, headers, the page title and its actions) renders at
  once.
- Never a full-page spinner or overlay for a small update, and never a
  blank page with a centred logo while an app boots: render the frame on
  the server, or put the shell's HTML in `index.html`.
- Stream what is ready: a `<Suspense>` boundary with a skeleton around each
  slow block in React (`loading.tsx` for a route in Next.js), promises
  streamed from a SvelteKit `load` and shown with `{#await}`, `server:defer`
  islands with a fallback in Astro.

## 3. Skeletons

- A skeleton only where it matches the layout that will load: the same
  blocks at the same sizes. Text lines at the text's line height, the last
  one shorter; images at their aspect ratio; avatars as circles; table rows
  at the row height. The content then takes its place without a jump.
- For regions of content on their first load: a list, a card grid, a detail
  panel, a chart's frame. Not for a button, a count, a single number or a
  select: those show an inline spinner or keep their old value.
- As many as usually arrive: a page of rows, or three when the list usually
  holds three.
- `--surface-2` on `--surface`, low contrast, the content's radius; static,
  or a slow shimmer (1.5 to 2s a sweep) that stops under reduced motion.
- A skeleton appears only after about 200ms, so fast loads do not flash.
- `aria-hidden="true"` on the skeleton; the region carries
  `aria-busy="true"` and a visually hidden status ("Loading invoices").

## 4. Refreshing, filtering and saving

- Refreshing data stays on screen while the new copy loads (stale while
  revalidate); a small spinner in the block's header says it is updating.
  A new filter or page dims the old rows slightly and keeps them until the
  new ones replace them (`ui-part-pagination`).
  - TanStack Query: `placeholderData: keepPreviousData`; `isPending` means
    nothing yet (the skeleton), `isFetching` means refreshing (the small
    spinner). SWR: `keepPreviousData: true`. React's `useTransition` keeps
    the current screen while the next one renders.
- Buttons show their own loading state: a 16px spinner and the verb in
  progress ("Saving…"), the width kept (a `min-width`, or the spinner laid
  over the label), `aria-disabled="true"` so a second press does nothing
  while focus stays on the button (setting `disabled` on a focused button
  drops its focus in some browsers). Then the result ("Saved") or the error
  beside it.
- Optimistic updates for quick actions that almost always succeed (star,
  mark as read, reorder, rename, add a comment): the change shows at once,
  the request runs behind it, and a failure puts it back and says so with a
  retry. React 19's `useOptimistic`, TanStack Query's `onMutate` with a
  rollback in `onError`, SWR's `optimisticData`. Not for payments, sending,
  or deleting what cannot be restored.
- Long work the user started (an export, an import) becomes a status they
  can leave: a row with its progress, and a notification when it is done
  (`ui-part-notifications`).

## 5. Spinners and progress bars

- A spinner with text saying what is loading: one small arc turning (0.8
  to 1s a turn, linear), 16px in a control, 20 to 24px in a region. Not
  bouncing dots, not the logo spinning.
- A progress bar with numbers for long tasks: "312 of 1,240 rows", "45%",
  and time left only when it can be estimated honestly. `<progress
  value="312" max="1240">` with a visible label, or `role="progressbar"`
  with `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-valuetext`
  and a name. 4 to 8px tall, the numbers in text beside it.
- Unknown length: an indeterminate bar or a spinner, with the current step
  in words ("Matching payments, step 2 of 3").
- No fake progress: a bar that eases to 90% and waits is a lie; an
  indeterminate bar is honest.
- A Cancel button on anything long the user started.

## 6. Screen readers and layout

- `aria-busy="true"` on the region while it loads, removed when it is done.
- A polite status (`role="status"`, in the page before its text changes)
  says it started when the wait is long enough to notice, and says the
  outcome once ("24 invoices loaded", or the error). Milestones at most
  (every 25%), never every percent.
- Focus stays where it was; arriving content never takes it.
- No layout shift when content arrives: the skeleton or a `min-height`
  holds the space, images have their dimensions (`ui-part-images`). CLS
  stays under 0.1 (`frontend-performance`).

## 7. Phones, themes and motion

- On a phone the same per-block loading; a sticky action button shows its
  busy state in place.
- Themes: skeleton, shimmer and progress track from tokens in both themes;
  on dark the shimmer is a slightly lighter step, not a white sweep
  (`ui-themes`).
- Motion: spinners and shimmers are the only loops, and they end when the
  loading does; under reduced motion the shimmer is static
  (`motion-interface`, section 11; `motion-comfort`).

## 8. A sketch

```css
/* Hidden for the first 200ms, so a fast load never flashes. */
.skeleton { animation: wait-then-show 0s 200ms backwards; }
@keyframes wait-then-show { from { visibility: hidden; } }

.bone {
  position: relative;
  overflow: hidden;
  background: var(--surface-2);
  border-radius: var(--radius-sm);
}
@media (prefers-reduced-motion: no-preference) {
  .bone::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, var(--shine), transparent);
    transform: translateX(-100%);
    animation: shimmer 1.8s linear infinite;
  }
}
@keyframes shimmer { to { transform: translateX(100%); } }
```

```tsx
const { data, isPending, isFetching, isError, refetch } = useQuery({
  queryKey: ["invoices", filters],
  queryFn: () => fetchInvoices(filters),
  placeholderData: keepPreviousData,
});

return (
  <section aria-labelledby="invoices-title" aria-busy={isFetching}>
    <header className="block-head">
      <h2 id="invoices-title">Invoices</h2>
      {isFetching && !isPending && <Spinner label="Updating invoices" />}
    </header>
    {isPending ? (
      <InvoiceRowsSkeleton rows={25} />
    ) : isError ? (
      <BlockError message="The invoices did not load." onRetry={refetch} />
    ) : (
      <InvoiceTable rows={data.items} dimmed={isFetching} />
    )}
  </section>
);
```

## Check it

- DevTools, network throttled to Slow 4G: each block shows its own
  skeleton, the frame is there at once, nothing jumps when content lands.
  Unthrottled: nothing flashes.
- `preview` with `motion: true`: layout shift while loading over 0.05 is
  reported with the elements that moved; anything repeating forever is
  listed (a spinner left turning after the data arrived).
- Press a saving button twice quickly: one request. Tab to it while it
  saves: focus stays.
- A screen reader hears that loading started and how it ended, once each.
- Go offline in DevTools: the failed block shows its error and a retry;
  the rest of the screen still works.

## Avoid

A full-page spinner for a small update; skeletons shaped like a layout the
data never fills; content that jumps when it arrives; spinners that flash
for 100ms; a spinner with no words; a progress bar that eases to 90% and
waits; a bright, fast shimmer; blanking the old data on every refetch; a
button that can be pressed again while it saves; the logo spinning on a
boot screen; a loading state that never ends when the request fails.
