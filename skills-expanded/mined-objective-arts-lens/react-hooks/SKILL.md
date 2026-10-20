---
name: react-hooks
description: "React hooks mastery"
---

# React Hooks — Beyond the Basics

Applying the React team's hooks API correctly when building components that need DOM access, layout measurement, accessible IDs, concurrent rendering, imperative child APIs, or custom hook composition. Auto-triggers on .jsx/.tsx files using useRef, useLayoutEffect, useId, useTransition, useDeferredValue, useImperativeHandle, or forwardRef. Not for basic useState/useEffect (see react-state), not for state management architecture, not for styling.

---

## 1. useRef — The Escape Hatch

Refs hold mutable values that persist across renders without triggering re-renders. Two use cases: DOM node access and mutable instance storage.

```tsx
// DOM ref — focus on mount
function AutoFocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => { inputRef.current?.focus(); }, []);
  return <input ref={inputRef} />;
}
```

`ref.current` survives re-renders like state, but changing it does not re-render.

```tsx
// Not this — state for non-rendered values causes wasted re-renders
function Stopwatch() {
  const [intervalId, setIntervalId] = useState<number | null>(null);
  // Every setIntervalId call re-renders. The interval ID is never displayed.
}

// This — ref for values that don't affect rendering
function Stopwatch() {
  const intervalRef = useRef<number | null>(null);
  const [elapsed, setElapsed] = useState(0);

  function start() {
    intervalRef.current = window.setInterval(() => setElapsed(e => e + 1), 1000);
  }
  function stop() { window.clearInterval(intervalRef.current!); }
  return <span>{elapsed}s</span>;
}
```

Previous value pattern -- a ref updated in useEffect lags one render behind:

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => { ref.current = value; });
  return ref.current;
}
```

**Rule:** Displayed in JSX? Use state. Only read by handlers or effects? Use a ref.

---

## 2. useLayoutEffect vs useEffect

Both run after render. `useEffect` runs asynchronously *after* paint. `useLayoutEffect` runs synchronously *before* paint, blocking the browser.

```tsx
// Not this — useEffect causes visible flicker (tooltip at 0,0 then jumps)
function Tooltip({ anchorRef, children }: TooltipProps) {
  const [pos, setPos] = useState({ top: 0, left: 0 });
  useEffect(() => {
    const rect = anchorRef.current!.getBoundingClientRect();
    setPos({ top: rect.bottom + 8, left: rect.left });
  }, [anchorRef]);
  return <div style={pos}>{children}</div>;
}

// This — useLayoutEffect measures before user sees anything
function Tooltip({ anchorRef, children }: TooltipProps) {
  const [pos, setPos] = useState({ top: 0, left: 0 });
  useLayoutEffect(() => {
    const rect = anchorRef.current!.getBoundingClientRect();
    setPos({ top: rect.bottom + 8, left: rect.left });
  }, [anchorRef]);
  return <div style={pos}>{children}</div>;
}
```

Scroll restoration is another classic case:

```tsx
function ChatMessages({ messages }: { messages: Message[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    ref.current!.scrollTop = ref.current!.scrollHeight;
  }, [messages.length]);
  return (
    <div ref={ref} style={{ overflow: 'auto', maxHeight: 400 }}>
      {messages.map(m => <MessageRow key={m.id} message={m} />)}
    </div>
  );
}
```

**Rule:** Default to useEffect. Switch to useLayoutEffect only when DOM measurement or mutation would cause visible flicker.

---

## 3. useId — SSR-Safe Unique IDs

`useId` generates stable IDs that match between server and client. Hand-rolled counters break hydration.

```tsx
// Not this — IDs mismatch between server and client
let nextId = 0;
function FormField({ label }: { label: string }) {
  const id = `field-${nextId++}`;
  return <><label htmlFor={id}>{label}</label><input id={id} /></>;
}

// This — stable across server and client
function FormField({ label }: { label: string }) {
  const id = useId();
  return <><label htmlFor={id}>{label}</label><input id={id} /></>;
}
```

Derive multiple related IDs from one call:

```tsx
function PasswordField() {
  const id = useId();
  return (
    <div>
      <label htmlFor={`${id}-input`}>Password</label>
      <input id={`${id}-input`} type="password" aria-describedby={`${id}-error ${id}-help`} />
      <p id={`${id}-help`}>Must be 8+ characters</p>
      <p id={`${id}-error`} role="alert">Password too short</p>
    </div>
  );
}
```

**Rule:** Use `useId` for all `htmlFor`, `aria-describedby`, `aria-labelledby`. Never counters or `Math.random()`.

---

## 4. useTransition — Non-Blocking State Updates

Marks a state update as low-priority. React keeps the UI responsive while computing the next render in the background.

```tsx
// Not this — expensive filter blocks the input on every keystroke
function UserSearch({ users }: { users: User[] }) {
  const [query, setQuery] = useState('');
  const filtered = users.filter(u => u.name.toLowerCase().includes(query.toLowerCase()));
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <UserList users={filtered} />
    </>
  );
}

// This — transition keeps input responsive
function UserSearch({ users }: { users: User[] }) {
  const [query, setQuery] = useState('');
  const [filterQuery, setFilterQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const filtered = users.filter(u => u.name.toLowerCase().includes(filterQuery.toLowerCase()));

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setQuery(e.target.value);           // Urgent: update input immediately
    startTransition(() => {
      setFilterQuery(e.target.value);   // Deferred: filter can wait
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <UserList users={filtered} />
    </>
  );
}
```

Works for tab switching too -- wrap `setTab` in `startTransition` so heavy tab content renders without blocking other clicks.

**Rule:** Wrap `setState` in `startTransition` when the resulting render is expensive and the user should not be blocked.

---

## 5. useDeferredValue — Deferred Rendering

Returns a "stale" copy of a value that lags behind during urgent updates. Defers the *consumer*, whereas `useTransition` defers the *producer*.

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  return (
    <div style={{ opacity: isStale ? 0.6 : 1 }}>
      <ExpensiveList query={deferredQuery} />
    </div>
  );
}
```

Use `useDeferredValue` when you do not control the state update -- the value arrives as a prop. Use `useTransition` when you own the `setState` call.

```tsx
function Parent() {
  const [text, setText] = useState('');
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <SlowChild text={text} />
    </>
  );
}

// Child defers the prop it receives
function SlowChild({ text }: { text: string }) {
  const deferred = useDeferredValue(text);
  return <ExpensiveTree text={deferred} />;
}
```

---

## 6. useImperativeHandle + forwardRef

`forwardRef` passes a ref through a component. `useImperativeHandle` restricts what that ref exposes.

```tsx
// Not this — parent gets the full DOM node
const FancyInput = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />;
});

// This — expose only intended operations
interface FancyInputHandle {
  focus: () => void;
  scrollIntoView: () => void;
}

const FancyInput = forwardRef<FancyInputHandle, InputProps>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null);
  useImperativeHandle(ref, () => ({
    focus()          { inputRef.current?.focus(); },
    scrollIntoView() { inputRef.current?.scrollIntoView({ behavior: 'smooth' }); },
  }));
  return <input ref={inputRef} {...props} />;
});

// Parent
function Form() {
  const inputRef = useRef<FancyInputHandle>(null);
  return (
    <>
      <FancyInput ref={inputRef} />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
    </>
  );
}
```

**Rule:** Prefer declarative props. Use `useImperativeHandle` only for focus, scroll, play, measure -- actions that cannot be props.

---

## 7. Hook Composition — Custom Hooks from Primitives

Custom hooks compose built-in hooks to extract reusable stateful logic.

```tsx
// useState + useEffect + useRef composed into a declarative interval
function useInterval(callback: () => void, delay: number | null) {
  const saved = useRef(callback);
  useEffect(() => { saved.current = callback; }, [callback]);
  useEffect(() => {
    if (delay === null) return;
    const id = setInterval(() => saved.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}
```

Custom hooks compose with each other:

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

function useSearchResults(query: string) {
  const debouncedQuery = useDebounce(query, 300);
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!debouncedQuery) { setResults([]); return; }
    let cancelled = false;
    setLoading(true);
    fetchResults(debouncedQuery).then(data => {
      if (!cancelled) { setResults(data); setLoading(false); }
    });
    return () => { cancelled = true; };
  }, [debouncedQuery]);
  return { results, loading };
}
```

Hooks can return refs alongside state for DOM-binding patterns:

```tsx
function useHover<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  const [hovering, setHovering] = useState(false);
  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const enter = () => setHovering(true);
    const leave = () => setHovering(false);
    node.addEventListener('mouseenter', enter);
    node.addEventListener('mouseleave', leave);
    return () => { node.removeEventListener('mouseenter', enter); node.removeEventListener('mouseleave', leave); };
  }, []);
  return [ref, hovering] as const;
}
```

**Rule:** One hook, one job. If it needs a name like `useFormValidationAndSubmissionAndAnalytics`, split it.

---

## 8. Rules of Hooks — Why They Exist

React tracks hooks by **call order** in a linked list on the fiber node. Slot 0 is the first `useState`, slot 1 the second. Conditional calls corrupt this mapping.

```tsx
// Not this — early return before hooks changes call order between renders
function Profile({ userId }: { userId: string | null }) {
  if (!userId) return <p>Select a user</p>;
  const [user, setUser] = useState(null);     // Slot 0... sometimes
  useEffect(() => { fetchUser(userId).then(setUser); }, [userId]);
  return <UserCard user={user} />;
}

// This — hooks first, early return after
function Profile({ userId }: { userId: string | null }) {
  const [user, setUser] = useState(null);
  useEffect(() => { if (!userId) return; fetchUser(userId).then(setUser); }, [userId]);
  if (!userId) return <p>Select a user</p>;
  return <UserCard user={user} />;
}
```

No hooks in loops -- use a ref Map instead of calling `useRef` per item:

```tsx
// Not this
const refs = tags.map(() => useRef<HTMLInputElement>(null)); // Hook count varies

// This
const refsMap = useRef<Map<string, HTMLInputElement>>(new Map());
// Use callback refs: ref={node => { if (node) refsMap.current.set(tag, node); }}
```

No hooks in nested functions or event handlers. Always call at the component's top level.

**The invariant:** Every render must call the exact same hooks in the exact same order.

---

## Anti-Patterns

**Ref mirroring state** -- `countRef.current = count` after every render is pointless duplication. Ref is for non-rendered values only.

**useLayoutEffect for data fetching** -- Blocks paint for a network request. Always use useEffect for async work.

**Overusing useImperativeHandle** -- Exposing `focus`, `blur`, `getValue`, `setValue`, `validate`, `reset` reinvents an uncontrolled component. Use controlled props.

**Wrapping every setState in startTransition** -- Not every update is expensive. Transitions add scheduling overhead. Measure first.

**Custom hook returning 6+ values** -- The hook does too much. Split `useFetcher` into `useFetch` + `useFetchControl`.

---

## Decision Framework

| Situation | Hook |
|-----------|------|
| Value not displayed in JSX | `useRef` |
| Access a DOM node | `useRef` + `ref` prop |
| DOM measurement/mutation before paint | `useLayoutEffect` |
| Sync with external system after paint | `useEffect` |
| Accessible IDs in SSR apps | `useId` |
| Keep UI responsive during expensive setState | `useTransition` |
| Defer rendering of a received prop | `useDeferredValue` |
| Expose imperative child API | `useImperativeHandle` + `forwardRef` |
| Reuse stateful logic | Custom hook |

| useEffect vs useLayoutEffect | useEffect | useLayoutEffect |
|-------------------------------|-----------|-----------------|
| Flicker without it? | No | Yes |
| Reads DOM measurements? | No | Yes |
| Involves network/timers? | Yes | No |

| useTransition vs useDeferredValue | useTransition | useDeferredValue |
|-----------------------------------|---------------|-----------------|
| You own the setState? | Yes | No |
| Value arrives as prop? | No | Yes |
| Need isPending? | Yes | No (compare values) |

---

## Code Review Checklist

- [ ] `useRef` for non-rendered values, `useState` for rendered values
- [ ] `useLayoutEffect` justified by DOM measurement or flicker prevention
- [ ] `useId` used for all `htmlFor`, `aria-describedby`, `aria-labelledby`
- [ ] `startTransition` wraps only genuinely expensive updates
- [ ] `useDeferredValue` used when state update is in an ancestor
- [ ] `useImperativeHandle` exposes minimal API, not the full DOM node
- [ ] Custom hooks do one thing and compose primitives cleanly
- [ ] All hooks called at top level -- no conditionals, loops, or nested functions
- [ ] Cleanup functions for all subscriptions, listeners, and intervals
- [ ] No `useLayoutEffect` for data fetching or async work

---

## Resources

- [React docs: Referencing Values with Refs](https://react.dev/learn/referencing-values-with-refs)
- [React docs: useLayoutEffect](https://react.dev/reference/react/useLayoutEffect)
- [React docs: useId](https://react.dev/reference/react/useId)
- [React docs: useTransition](https://react.dev/reference/react/useTransition)
- [React docs: useDeferredValue](https://react.dev/reference/react/useDeferredValue)
- [Dan Abramov: Making setInterval Declarative with React Hooks](https://overreacted.io/making-setinterval-declarative-with-react-hooks/)
- [React docs: Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)
