---
name: design-every-state
description: Design and build every screen state — empty, loading, error, success — with real content, never just the default with lorem ipsum.
---

# Design every state

The default state is the easy one. The interesting states are the empty screen a brand-new user sees with nothing loaded, the call that fails, the request still in flight. Skipping them is the most common way a built UI feels unfinished. Lorem ipsum hides this — if you can't write the real empty-state copy, the screen isn't fully thought through.

## Patterns

- For every screen, enumerate its states: default, loading, empty, error, success, and any partial states specific to it.
- Build at minimum the empty, loading, and error states — not just the happy path.
- Write real content for every state, including the empty and error states. No placeholder text, no lorem ipsum.
- Failure UI is real UI: say what failed and what the user can do, in the project's voice. Not "Error 500", not an apology.

## Examples

```tsx
// BAD — only the happy path is built; other states are ignored
export function OrderList({ orders }: { orders: Order[] }) {
  return <ul>{orders.map(o => <OrderItem key={o.id} order={o} />)}</ul>
}

// GOOD — all states accounted for with real copy
export function OrderList({ orders, isLoading, error }: Props) {
  if (isLoading) return <Spinner label="Loading your orders…" />
  if (error) return <ErrorState message="We couldn't load your orders. Try refreshing." />
  if (orders.length === 0) return (
    <EmptyState
      heading="No orders yet"
      body="Once you place an order it will appear here."
      action={<Button href="/shop">Browse products</Button>}
    />
  )
  return <ul>{orders.map(o => <OrderItem key={o.id} order={o} />)}</ul>
}
```

## Why it matters

States that get skipped are the ones users hit first and remember worst. Real content forces the design to be honest about what each state actually says.
