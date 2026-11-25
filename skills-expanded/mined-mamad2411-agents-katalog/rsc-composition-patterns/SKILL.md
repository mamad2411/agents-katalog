---
name: rsc-composition-patterns
version: "1.0"
description: >
  React Server Components architecture patterns for Next.js 14+ with server-first development.
  PROACTIVELY activate for: (1) deciding Server vs Client Component boundaries, (2) composing components with 'use client', (3) managing interactivity patterns.
  Triggers: "server component", "client component", "'use client'"
group: foundation
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# React Server Components Composition Patterns

## Core Principle: Server-First

**DEFAULT**: All components are Server Components unless they need:
- State (`useState`, `useReducer`)
- Effects (`useEffect`, `useLayoutEffect`)
- Event handlers (`onClick`, `onChange`)
- Browser APIs (`window`, `localStorage`)
- React hooks (custom hooks that use the above)

## The 'use client' Boundary Rule

```tsx
// BAD: 'use client' at top level (forces entire tree to be client-rendered)
// app/dashboard/page.tsx
'use client'
export default function Dashboard() {
  const [count, setCount] = useState(0);
  return <div>{/* entire page is now client-rendered */}</div>;
}

// GOOD: Server Component at top, Client Component at leaf
// app/dashboard/page.tsx (Server Component - no 'use client')
import { Counter } from './Counter';
export default async function Dashboard() {
  const data = await fetchData(); // Server-side data fetching
  return (
    <div>
      <h1>Dashboard</h1>
      <StaticContent data={data} /> {/* Server Component */}
      <Counter /> {/* Small Client Component for interactivity */}
    </div>
  );
}

// app/dashboard/Counter.tsx (Client Component - only this is client-rendered)
'use client'
import { useState } from 'react';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## Composition Pattern: Pass Server Components as Children

Server Components can be passed as `children` to Client Components:

```tsx
// ClientWrapper.tsx (Client Component)
'use client'
export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  );
}

// page.tsx (Server Component)
export default async function Page() {
  const data = await fetchServerData();
  return (
    <ClientWrapper>
      {/* This entire subtree renders on the server! */}
      <ServerRenderedContent data={data} />
    </ClientWrapper>
  );
}
```

**Why this works**: `children` is passed as a serialized prop (already rendered on server).

## Anti-Patterns to Avoid

**Importing Server Components into Client Components**:

```tsx
// ERROR: Cannot import Server Component into Client Component
'use client'
import { ServerComponent } from './ServerComponent'; // ERROR!

export function ClientComponent() {
  return <ServerComponent />; // This will not work
}
```

**Passing Non-Serializable Props**:

```tsx
// ERROR: Cannot pass functions from Server to Client Component
export default function ServerPage() {
  const handleClick = () => console.log('clicked');
  return <ClientButton onClick={handleClick} />; // ERROR!
}

// GOOD: Define functions inside Client Component
'use client'
export function ClientButton() {
  const handleClick = () => console.log('clicked'); // OK
  return <button onClick={handleClick}>Click</button>;
}
```

## Quick Decision Tree

```
Need interactivity (state, events, hooks)?
├─ YES → Client Component ('use client')
├─ NO → Server Component (default)

Can you split the interactive part into a smaller component?
├─ YES → Keep parent as Server Component, make leaf a Client Component
├─ NO → Use Client Component but minimize its scope
```

## Performance Benefits

**Server Components**:
- Zero JavaScript sent to client (smaller bundles)
- Direct database/API access (no extra round-trip)
- Automatic code splitting
- Better SEO (pre-rendered HTML)

**Client Components** (use sparingly):
- Required for interactivity
- Adds JavaScript to bundle
- Requires serialization of props

For advanced patterns and edge cases, see `resources/advanced-rsc-patterns.md`.
