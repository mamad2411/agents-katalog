---
name: react-animation
description: Use when animating list enter/exit or modal transitions in React with Framer Motion — AnimatePresence for mount/unmount animations. Pair with a11y-media-motion to respect prefers-reduced-motion.
metadata:
  origin: ECC (decomposed from frontend-patterns)
allowed-tools: Read, Edit, Grep, Glob
---

# Framer Motion animation patterns

## List enter/exit

```tsx
import { motion, AnimatePresence } from 'framer-motion';

export function AnimatedMarketList({ markets }: { markets: Market[] }) {
  return (
    <AnimatePresence>
      {markets.map((market) => (
        <motion.div key={market.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.3 }}>
          <MarketCard market={market} />
        </motion.div>
      ))}
    </AnimatePresence>
  );
}
```

`key` must be the stable item id, not the array index — index keys break exit animations when
items reorder or get removed from the middle of the list.

## Modal open/close

```tsx
export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div className="modal-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} />
          <motion.div className="modal-content" initial={{ opacity: 0, scale: 0.9, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9, y: 20 }}>
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

## Respect reduced motion

Don't ship these transitions unconditionally — gate duration/transform amplitude behind
`prefers-reduced-motion` (see `a11y-media-motion`'s `useReducedMotion` hook), or use Framer
Motion's own `useReducedMotion` from `framer-motion` and shrink transitions to opacity-only when
it's true.

## Modal accessibility

Animating a modal's mount/unmount is separate from making it accessible — it still needs
`role="dialog"`, `aria-modal`, focus move-in/restore-out, and Escape-to-close. See
`a11y-focus-management` for that; this skill only covers the motion.
