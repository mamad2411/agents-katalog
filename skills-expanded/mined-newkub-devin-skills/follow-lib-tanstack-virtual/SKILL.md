---
name: follow-lib-tanstack-virtual
description: Use TanStack Virtual end to end — lists, window scroll, grids, dynamic sizes, infinite scroll, table rows
argument-hint: "[framework] [mode]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Virtual (v3) fully — virtualize element lists: scroll container, window virtualizer, grids, dynamic measurement, infinite scroll, table row virtualization

## Scope

Use when rendering many items (100+) — lists, table rows, grids, chat feeds; short lists don't need it (overhead > benefit)

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the virtual package

```bash
bun add @tanstack/react-virtual   # solid/vue/svelte variants available
```

### 2. List Virtualizer

> Goal: virtualize a list with correct scroll behavior

```tsx
const parentRef = useRef<HTMLDivElement>(null)
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 40,    // approximate px
  overscan: 5,               // render extra beyond the viewport
})

return (
  <div ref={parentRef} style={{ height: 400, overflow: 'auto' }}>
    <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
      {virtualizer.getVirtualItems().map((v) => (
        <div key={v.key} data-index={v.index} ref={virtualizer.measureElement}
          style={{ position: 'absolute', top: 0, transform: `translateY(${v.start}px)` }}>
          {items[v.index]}
        </div>
      ))}
    </div>
  </div>
)
```

### 3. Modes

> Goal: pick the virtualizer matching the layout

1. **Fixed container** — `useVirtualizer` + a scroll element (above)
2. **Window scroll** — `useWindowVirtualizer` when scrolling on the window/document
3. **2D grid** — pair a row + column virtualizer (or `lanes` for masonry)
4. **Dynamic heights** — `measureElement` ref + `data-index` (above) — good for chat feeds/cards
5. **Sticky headers** — check the `vItem.lane`/sticky patterns in the docs

### 4. Patterns

> Goal: composition with other libs

1. **Infinite scroll**: tail virtual item + `useInfiniteQuery` (`follow-query`) — call `fetchNextPage` when the index nears the end:

   ```ts
   const lastItem = virtualItems[virtualItems.length - 1]
   useEffect(() => {
     if (lastItem?.index >= items.length - 1 && hasNextPage) fetchNextPage()
   }, [lastItem?.index])
   ```

2. **Table rows**: virtualize the tbody of `follow-table` — spacer rows + `translateY`
3. **Keyboard nav**: `virtualizer.scrollToIndex(i)` for active-item scroll-into-view
4. **Padding/gap**: `paddingStart`/`gap` options — don't put margin on the items

### 5. Verify

> Goal: prove windowing handles dynamic sizes correctly before finishing

1. `/run-typecheck` + `/run-test`
2. DevTools: DOM nodes equal viewport+overscan, scroll recycling is correct
3. 10k+ items stay smooth, dynamic heights don't jump
4. If it fails → `/resolve-errors` max 3 rounds

## Rules

- The scroll container must have a fixed height + `overflow: auto`
- `estimateSize` close to reality — a big error makes the scrollbar jump during measurement
- Use `vItem.key` as the React key — never `vItem.index` when items reorder
- Items must not have margin — use the `gap` option or internal padding
- `measureElement` must be paired with `data-index`

## Expected Outcome

- Large lists render fast with a bounded DOM
- Window/grid/dynamic/infinite modes used in the right places
- Integration with Query/Table works
