---
name: layout-stable-hover-via-inset-shadow
description: Replace transform-based hover effects (translate, scale) with inset box-shadow to avoid layout shifts and horizontal-scrollbar flicker
category: design
triggers:
  - hover causes scrollbar
  - hover layout shift
  - translate hover flicker
  - scrollbar flashes on hover
tags:
  - css
  - hover
  - scrollbar
  - layout
version: 1.0.0
---

# Layout-Stable Hover via Inset Shadow

Transform-based hover effects like `transform: translateX(2px)` look tasteful on a single button but break lists inside scrollable containers. Each item's hover overflows its parent horizontally, the browser flashes a horizontal scrollbar, which shifts the vertical scrollbar, which moves the hovered item out from under the cursor — flicker loop.

## The anti-pattern

```css
.list-item {
  transition: all .2s;
}
.list-item:hover {
  transform: translateX(2px);   /* ← overflows parent */
  box-shadow: 0 0 0 1px var(--accent);
}
```

Inside a container with bounded width, every hover triggers:
1. Item moves 2px right
2. Right edge overflows parent
3. Browser adds horizontal scrollbar
4. Vertical scrollbar narrows/moves
5. Item under cursor is no longer hovered
6. Scrollbar disappears
7. Repeat — visible flicker

## The fix

Use an effect that **doesn't change layout**:

```css
.list-item {
  min-width: 0;            /* allow text ellipsis */
  transition: background .2s, box-shadow .2s;   /* explicit, not 'all' */
}
.list-item:hover {
  background: var(--hover-bg);
  box-shadow: inset 2px 0 0 var(--accent);   /* painted inside, no overflow */
}
.list-item-name {
  min-width: 0;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.list-container {
  overflow-x: hidden;      /* defense in depth */
}
```

Key changes:

- **`box-shadow: inset`** paints *inside* the element's box, so it doesn't add to scroll width.
- **Explicit transition properties** (`background, box-shadow`) instead of `all` — prevents re-triggering on any unrelated property.
- **`overflow-x: hidden` on container** — defense in depth against future hover changes that forget this rule.
- **`min-width: 0` on flex children** — required to let `text-overflow: ellipsis` actually truncate inside a flex layout.

## When transforms are still fine

Transform-based hovers are fine when:
- The item has room to grow (e.g. padding or margin buffers on all sides ≥ transform distance)
- The container has `overflow: visible` and doesn't scroll
- The transform is a `scale()` at origin center (no edge overflow)

They're only bad inside tight scrollable containers.

## Related pitfalls

- `transition: all` re-fires on any computed property change — scope transitions explicitly.
- `:active` using `transform: scale(.98)` is usually fine because it's brief and mouse is already held.
- Animated `margin-left/right` also causes reflow; stick to inset shadows or absolutely-positioned overlays for decoration.
