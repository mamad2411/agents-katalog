---
name: a11y-media-motion
description: Use when adding CSS/JS animations or transitions in a React app — respecting prefers-reduced-motion via a hook. Pair with react-animation for the Framer Motion side of the same component.
metadata:
  origin: community (decomposed from frontend-a11y)
allowed-tools: Read, Edit, Grep, Glob
---

# Respecting reduced motion

Some users set "reduce motion" at the OS level (vestibular disorders, motion sickness, or just
preference) — animations that ignore this setting are an accessibility failure, not just a UX
nitpick.

```tsx
export function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  return prefersReduced;
}

export function AnimatedCard({ children }: { children: React.ReactNode }) {
  const reduceMotion = useReducedMotion();
  return <div style={{ transition: reduceMotion ? 'none' : 'transform 300ms ease' }}>{children}</div>;
}
```

## Rules

- Read the media query on mount (don't assume `false`) — a user who already has the OS setting on
  should never see the first animation either.
- Subscribe to `change` — the setting can flip while the app is open (OS settings panel).
- "Respect" doesn't have to mean zero animation: shrinking to opacity-only fades, or cutting
  duration drastically, is often enough — full removal is only required for large
  transform/parallax/autoplay motion.
- Framer Motion has its own `useReducedMotion` (from the `framer-motion` package) that does the
  same thing — prefer that one over hand-rolling this hook in a Framer Motion codebase, to avoid
  two separate media-query listeners.

## Related

- `react-animation` — the Framer Motion transitions this hook should gate.
