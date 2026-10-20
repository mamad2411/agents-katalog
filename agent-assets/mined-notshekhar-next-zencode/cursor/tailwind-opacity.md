---
description: Never use Tailwind color/alpha modifier syntax (color/number). Use opacity-XX or theme colors instead.
globs: "**/*.tsx"
alwaysApply: false
---

# No Color Alpha Modifier (`/number`)

Never use Tailwind's color-alpha modifier syntax like `bg-red-500/10`, `text-muted-foreground/60`, `border-primary/40`, etc. The `/number` syntax propagates opacity to child components.

## Instead use:

1. **`opacity-XX` utility** for overall element transparency:

```tsx
// BAD
<div className="bg-muted/30">

// GOOD
<div className="bg-muted opacity-30">
```

2. **Theme colors** for subtle tinted backgrounds (badges, pills, cards):

```tsx
// BAD
<span className="bg-destructive/10 text-destructive">Error</span>

// GOOD
<span className="bg-muted text-destructive">Error</span>
// or
<span className="bg-accent text-destructive">Error</span>
```

3. **`opacity-XX` on text elements** for dimmed text:

```tsx
// BAD
<code className="text-muted-foreground/60">path</code>

// GOOD
<code className="text-muted-foreground opacity-60">path</code>
```

## Theme colors to use for subtle backgrounds:

- `bg-muted` — neutral subtle background
- `bg-accent` — slightly highlighted background
- `bg-secondary` — secondary surface color
