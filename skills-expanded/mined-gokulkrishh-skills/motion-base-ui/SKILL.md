---
name: motion-base-ui
description: "Animating Base UI components with Motion for React. Use this skill when implementing animations on Base UI components (Menu, Dialog, Popover, Tooltip, Switch, etc.) with the Motion library. Triggers on: motion animation, base-ui animate, animate dropdown, animate dialog, animate popover, exit animation, spring animation, render prop animation, AnimatePresence base-ui."
metadata:
  short-description: Animate Base UI components with Motion for React
  user-invocable: true
---

# Animating Base UI with Motion for React

## Instructions

When animating Base UI components with Motion, follow these rules strictly.

### Importing

- Always import from `motion/react`, never from `framer-motion`

```tsx
import { motion, AnimatePresence } from "motion/react";
```

### Base UI + Motion Integration

Pass a `motion` component via the Base UI `render` prop. Never use the function/spread props approach as this causes type errors.

```tsx
<Menu.Popup
  render={<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} />}
>
  {/* Children */}
</Menu.Popup>
```

### Exit Animations

Some Base UI components (ContextMenu, Popover, Dialog) control their own conditional rendering. To add exit animations:

1. Hoist the `open` state with `useState`
2. Add `keepMounted` to the `Portal` component
3. Wrap the `Portal` in `AnimatePresence`

```tsx
function App() {
  const [open, setOpen] = useState(false);
  return (
    <Dialog.Root open={open} onOpenChange={setOpen}>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <AnimatePresence>
        {open && (
          <Dialog.Portal keepMounted>
            <Dialog.Backdrop
              render={
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                />
              }
            />
            <Dialog.Popup
              render={
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                />
              }
            >
              {/* Content */}
            </Dialog.Popup>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}
```

**Note:** `Portal` keeps the tree mounted as long as Base UI detects animations via `element.getAnimations()`. Motion runs `opacity`, `transform`, `filter`, and `clipPath` via hardware acceleration, so ensure at least one of these is used for exit animations.

### Performance

- Add `willChange: "transform"` when animating `transform`, `x`, `y`, `scale`, etc.
- Also add `opacity`, `clipPath`, or `filter` to `willChange` if animating those
- **Only** these values are valid for `willChange`: `transform`, `opacity`, `clipPath`, `filter`
- Prefer animating `transform` over independent transforms (`x`, `y`, `scaleX`) for hardware acceleration
- Use independent transforms when composing multiple competing transforms:

```tsx
animate(element, { x: 100 });
hover(() => {
  animate(element, { scale: 1.2 });
  return () => animate(element, { scale: 1 });
});
```

- Always use independent transforms when defining any transform via `style`:

```tsx
<motion.div animate={{ x: 100 }} style={{ scale: 2 }} />
```

### Motion Values

- Use `value.on("change", update)`, never `value.onChange(update)`
- Use `value.stop()` to end current animation — don't track animation in a variable
- Starting a new animation on a value automatically stops the current one

### `animate` Function

Three valid syntaxes:

```tsx
// Motion value
animate(motionValue, targetValue, options);

// Origin to target (add onUpdate to options)
animate(originValue, targetValue, { onUpdate: (v) => {} });

// Element or object
animate(element, { opacity: 1 }, options);
```

### Variant Propagation

Use `initial`/`whileHover`/`whileTap` on parent `motion.*` elements. Children with matching `variants` keys inherit the active variant automatically — no `animate` prop needed:

```tsx
<motion.li initial="idle" whileHover="hover">
  <motion.span
    variants={{
      idle: { scale: 1 },
      hover: { scale: 1.2 },
    }}
  />
</motion.li>
```

### Easing

- Easing is defined via the `ease` option in camelCase: `easeOut`, `easeInOut`
- Spring config via `lib/springs.ts`:

```tsx
import { springs } from "@/lib/springs";

animate(motionX, targetX, springs.moderate);

// or
<motion.div transition={springs.moderate} />;
```

## Rules

- Never import from `framer-motion`
- Always use `render` prop for Base UI + Motion, never function/spread
- Use `AnimatePresence` + `keepMounted` for exit animations on portalled components
- Prefer `willChange` over `transform: translateZ(0)`
- Use camelCase for easing: `easeOut` not `ease-out`

---
