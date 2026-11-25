---
name: write-react
description: React coding conventions for this codebase. Use when writing or reviewing React components, when asked about component structure, section ordering, Tailwind CSS usage, state management patterns, conditional rendering, list rendering, or React 19 conventions. Covers component section layout (🔖🧩🪝🏗💪🏁🎨), Tailwind CSS with theme tokens, TanStack Router file-based routing, lexico-components usage, and testing with Vitest + RTL.
license: MIT
---

# Write React

All projects use **React 19** with the new JSX transform — no `React` import needed.

```typescript
// ✅ CORRECT: No React import (React 19)
import { useState } from "react";

export const Counter = (): ReactElement => {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
};
```

## Component Structure

Organize every component with these emoji-marked sections **in order**:

| Section | Emoji | Contents |
| ------- | ----- | -------- |
| Type | 🔖 | Props interface, types |
| Component | 🧩 | Component declaration |
| Hooks | 🪝 | useState, useEffect, custom hooks |
| Setup | 🏗 | Computed values, memoized callbacks |
| Handler | 💪 | Event handlers |
| Early returns | 🏁 | Loading, error states |
| Render | 🎨 | JSX return |

```typescript
import { useState, useEffect, useCallback } from "react";
import { type ReactElement } from "react";

// 🔖 Type
export interface UserCardProps {
  userId: string;
  className?: string;
}

// 🧩 Component
export const UserCard = (props: UserCardProps): ReactElement => {
  const { userId, className } = props;

  // 🪝 Hooks
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void fetchUser(userId).then(setUser);
  }, [userId]);

  // 🏗 Setup
  const displayName = user?.name ?? "Unknown User";
  const handleClick = useCallback(() => {
    console.log("User clicked", user);
  }, [user]);

  // 💪 Handler
  const handleRefresh = (): void => {
    setLoading(true);
    void fetchUser(userId).then(setUser).finally(() => { setLoading(false); });
  };

  // 🏁 Early returns
  if (loading) return <Spinner />;
  if (!user) return <ErrorMessage />;

  // 🎨 Render
  return (
    <Card className={className}>
      <h2>{displayName}</h2>
      <Button onClick={handleClick}>View Profile</Button>
      <Button onClick={handleRefresh}>Refresh</Button>
    </Card>
  );
};
```

## lexico-components

All UI components come from the shared component library. **Never duplicate UI code.**

```typescript
// ✅ CORRECT
import { Button, Card, Input, Label, cn } from "@codebase/lexico-components";

// ❌ WRONG: Copying component code into lexico
```

Never modify files in `packages/lexico-components/src/components/ui/` (shadcn-generated). Compose custom components in `packages/lexico-components/src/components/` instead.

## Styling with Tailwind CSS

### Utility-First CSS

```typescript
// ✅ CORRECT: Tailwind utility classes
<div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md">

// ❌ AVOID: Inline styles
<div style={{ display: "flex", padding: "1rem" }}>
```

### Theme Tokens

Use CSS variables for themed colors to support dark mode:

```typescript
// ✅ CORRECT: Theme-aware classes
<button className="bg-primary text-primary-foreground hover:bg-primary/90">

// ❌ AVOID: Hardcoded colors (breaks dark mode)
<button className="bg-blue-600 text-white">
```

### Conditional Classes with `cn()`

```typescript
import { cn } from "@codebase/lexico-components";

<button
  className={cn(
    "rounded font-medium transition-colors",
    { "bg-primary text-primary-foreground": variant === "primary" },
    { "px-4 py-2": size === "md" },
    className,
  )}
>
```

## TanStack Router (lexico)

There is no dedicated SSR skill; the router conventions live here. Key patterns:

```typescript
// routes/word.$id.tsx
export const Route = createFileRoute("/word/$id")({
  loader: async ({ params }) => {
    return { word: await getWordDetails({ wordId: params.id }) };
  },
  component: WordDetailPage,
});

function WordDetailPage(): ReactElement {
  const { word } = Route.useLoaderData();
  return <h1>{word.text}</h1>;
}
```

## State Management

| Scenario | Pattern |
| -------- | ------- |
| Component-local state | `useState` |
| Server/fetched data | TanStack Router loaders |
| Expensive computations | `useMemo` |
| Stable callbacks | `useCallback` |

## Common Patterns

### Conditional Rendering

```typescript
// Short-circuit with &&
{isLoggedIn && <UserMenu />}

// Ternary for if-else
{isLoading ? <Spinner /> : <Content />}

// Nullish coalescing for defaults
{user?.name ?? "Guest"}
```

### List Rendering

```typescript
// ✅ CORRECT: Stable key from data ID
{users.map((user) => <UserCard key={user.id} user={user} />)}

// ❌ WRONG: Index as key (unstable on reorder/insert)
{users.map((user, index) => <UserCard key={index} user={user} />)}
```

### Event Handlers

```typescript
// ✅ Arrow function for parameterized handlers
<button onClick={() => handleClick(user.id)}>Click</button>

// ❌ AVOID: bind() in render (new function every render)
<button onClick={handleClick.bind(null, user.id)}>Click</button>
```

## Testing React Components

Use Vitest + React Testing Library:

```typescript
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { UserCard } from "./user-card.js";

describe("UserCard", () => {
  it("renders user name", () => {
    render(<UserCard userId="123" />);
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });
});
```
