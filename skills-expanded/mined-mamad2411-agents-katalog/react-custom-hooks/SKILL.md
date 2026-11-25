---
name: react-custom-hooks
description: Use when extracting reusable stateful logic in React — toggle state, async data fetching with refetch, debounced values. Use before writing ad-hoc useState/useEffect combos that will likely be needed in more than one component.
metadata:
  origin: ECC (decomposed from frontend-patterns)
allowed-tools: Read, Edit, Grep, Glob
---

# React custom hooks patterns

## Toggle state

```tsx
export function useToggle(initialValue = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue);
  const toggle = useCallback(() => setValue((v) => !v), []);
  return [value, toggle];
}
```

## Async data fetching with a stable `refetch`

**Trap**: if `refetch` closes over `fetcher`/`options` directly, a caller passing an inline arrow
function makes `refetch` a new reference every render, which re-triggers any `useEffect([...,
refetch])` — an infinite fetch loop. Fix: stash the latest `fetcher`/`options` in refs, keep
`refetch` itself dependency-free.

```tsx
export function useQuery<T>(key: string, fetcher: () => Promise<T>, options?: { onSuccess?: (d: T) => void; onError?: (e: Error) => void; enabled?: boolean }) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const fetcherRef = useRef(fetcher);
  const optionsRef = useRef(options);
  useEffect(() => {
    fetcherRef.current = fetcher;
    optionsRef.current = options;
  });

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetcherRef.current();
      setData(result);
      optionsRef.current?.onSuccess?.(result);
    } catch (err) {
      const e = err as Error;
      setError(e);
      optionsRef.current?.onError?.(e);
    } finally {
      setLoading(false);
    }
  }, []);

  const enabled = options?.enabled !== false;
  useEffect(() => {
    if (enabled) refetch();
  }, [key, enabled, refetch]);

  return { data, error, loading, refetch };
}
```

For real apps prefer SWR or React Query over hand-rolling this — write this pattern only when
those libraries aren't available.

## Debounce

```tsx
export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debounced;
}
```

## Checklist before extracting a hook

- Does the logic show up in 2+ components already, or is it clearly about to? If it's truly
  one-off, leave it inline.
- Any callback the hook returns and that callers put in a dependency array (`refetch`, `toggle`)
  must be reference-stable (`useCallback` with an empty or minimal dep array) — otherwise callers
  get infinite-effect loops for free.
