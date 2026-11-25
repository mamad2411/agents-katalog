---
name: rizumu
description: Rizumu's rules for writing clear code comments in AI-assisted coding. Use when writing or reviewing code comments.
metadata:
  author: Rizumu
  version: "2026.06.17"
  source: Based on Rizumu's blog post on code comments for AI-assisted coding
---

# Code Comments

**Comments belong outside the function, describing what callers can't see from the signature — not inside, restating what the code does.**

## Rules

- Use `/** ... */` on the function signature to document non-obvious behavior: error conditions, side effects, cleanup requirements (e.g., "returns an unsubscribe function that must be called").
- Don't comment inside the function body unless the logic is genuinely complex. If you need to, first try to rewrite the code more clearly.
- For Vue's `computed` / `watch` / `watchEffect`, add a comment only when the name doesn't convey the purpose.
- Write comments in English.

## Example

✅ Good — tells the caller something they can't infer from types:

```ts
/**
 * Registers a scroll listener. Returns an unsubscribe function —
 * call it on unmount to avoid memory leaks.
 */
function onScroll(el: HTMLElement, handler: () => void): () => void
```

❌ Bad — restates the code:

```ts
let total = 0 // Initialize total
for (const item of items) { // Loop through items
  total += item.price // Add price
}
```
