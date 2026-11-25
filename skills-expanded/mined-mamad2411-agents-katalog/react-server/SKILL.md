---
name: react-server
description: "React Server Components, Server Actions, and the serialization boundary"
---

# The Two Reacts: Server and Client

Applying the React team's Server Components model -- Dan Abramov's "The Two Reacts" and the official React documentation. Core belief: **there are two Reacts now, one that runs where the data lives and one that runs where the user lives.** The server is not a performance hack. It is a first-class rendering environment with its own rules.

---

## Core Principles

### 1. Server Components vs Client Components

Server Components run once on the server, produce HTML, and ship zero JavaScript. Client Components hydrate in the browser and can hold state, handle events, and use browser APIs. Server Components are the **static skeleton**, Client Components are the **interactive muscles**.

**Not this:**
```tsx
'use client'; // Everything ships JS unnecessarily
export default function ArticlePage({ article }) {
  return (
    <article>
      <h1>{article.title}</h1>
      <p>{article.body}</p>         {/* Static -- wasted client JS */}
      <LikeButton id={article.id} />
    </article>
  );
}
```

**This:**
```tsx
// Server Component -- no directive, no JS shipped for static content
import { LikeButton } from './like-button';
export default function ArticlePage({ article }) {
  return (
    <article>
      <h1>{article.title}</h1>
      <p>{article.body}</p>
      <LikeButton id={article.id} />  {/* Only this ships JS */}
    </article>
  );
}
```

### 2. The "use client" Directive

`'use client'` does not mean "this is a client component." It means **"this is the boundary where the server tree ends and the client tree begins."** Everything imported by a `'use client'` file becomes part of the client bundle.

**Not this:**
```tsx
// 'use client' on every file -- pulls entire dependency tree into bundle
'use client'; // search-page.tsx
'use client'; // search-input.tsx
'use client'; // search-results.tsx
```

**This:**
```tsx
// search-page.tsx -- Server Component, fetches data directly
import { SearchInput } from './search-input';
export default async function SearchPage() {
  const suggestions = await db.suggestions.findMany();
  return (
    <div>
      <h1>Search</h1>
      <SearchInput suggestions={suggestions} />
    </div>
  );
}

// search-input.tsx -- the sole boundary, only interactive leaf
'use client';
import { useState } from 'react';
export function SearchInput({ suggestions }: { suggestions: string[] }) {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

Child components of a client component are automatically client -- they do not need their own directive.

### 3. The "use server" Directive

`'use server'` marks functions that execute on the server but can be called from client components. These are Server Actions -- the mutation primitive for React Server Components.

**Not this:**
```tsx
// API route + fetch just to handle a form
export async function POST(req: Request) { /* ... */ }
// client
'use client';
const handleSubmit = () => fetch('/api/comments', { method: 'POST', body: JSON.stringify({ text }) });
```

**This:**
```tsx
// actions.ts
'use server';
export async function addComment(formData: FormData) {
  await db.comment.create({ data: { text: formData.get('text') as string } });
  revalidatePath('/comments');
}

// comment-form.tsx -- works as Server Component, no JS needed
import { addComment } from './actions';
export function CommentForm() {
  return (
    <form action={addComment}>
      <input name="text" required />
      <button type="submit">Post</button>
    </form>
  );
}
```

Inline variant:
```tsx
export default async function Page() {
  async function deleteItem(formData: FormData) {
    'use server';
    await db.item.delete({ where: { id: formData.get('id') } });
  }
  return (
    <form action={deleteItem}>
      <input type="hidden" name="id" value="123" />
      <button type="submit">Delete</button>
    </form>
  );
}
```

### 4. Async Server Components

Server Components can be `async`. They `await` data directly -- no `useEffect`, no loading state at the component level.

**Not this:**
```tsx
'use client';
export default function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch(`/api/users/${userId}`).then(r => r.json()).then(d => { setUser(d); setLoading(false); });
  }, [userId]);
  if (loading) return <Spinner />;
  return <div>{user.name}</div>;
}
```

**This:**
```tsx
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await db.user.findUnique({ where: { id: userId } });
  return <div>{user.name}</div>;  // Loading handled by <Suspense> above
}
```

### 5. Server Actions and Forms

Server Actions integrate with HTML forms for progressive enhancement. Use `useActionState` for client-side form state with pending/error handling.

```tsx
// actions.ts
'use server';
export async function createPost(prevState: any, formData: FormData) {
  const title = formData.get('title') as string;
  if (!title || title.length < 3) return { error: 'Title too short' };
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
  redirect('/posts');
}
```

```tsx
'use client';
import { useActionState } from 'react';
import { createPost } from './actions';

export function PostForm() {
  const [state, formAction, isPending] = useActionState(createPost, null);
  return (
    <form action={formAction}>
      <input name="title" required />
      {state?.error && <p className="error">{state.error}</p>}
      <button disabled={isPending}>{isPending ? 'Saving...' : 'Create'}</button>
    </form>
  );
}
```

The form works without JS (progressive enhancement). With JS you get inline errors and pending states.

### 6. useFormStatus

Reads the parent `<form>` submission status without prop drilling. Must be called from a component **inside** the form.

**Not this:** manual `useState` for pending state, threaded as props.

**This:**
```tsx
'use client';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving...' : 'Create'}</button>;
}

export function PostForm() {
  return (
    <form action={createPost}>
      <input name="title" />
      <SubmitButton />  {/* Reusable across any form */}
    </form>
  );
}
```

### 7. useOptimistic

Shows a temporary optimistic value while an async action runs, then reverts to real state when the action completes.

```tsx
'use client';
import { useOptimistic } from 'react';
import { sendMessage } from './actions';

export function MessageList({ messages }: { messages: Message[] }) {
  const [optimistic, addOptimistic] = useOptimistic(
    messages,
    (current, newText: string) => [...current, { text: newText, sending: true }]
  );

  async function handleSend(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimistic(text);          // Show immediately
    await sendMessage(formData);  // React reverts to real state on completion
  }

  return (
    <>
      {optimistic.map((msg, i) => (
        <div key={i} style={{ opacity: msg.sending ? 0.6 : 1 }}>{msg.text}</div>
      ))}
      <form action={handleSend}>
        <input name="text" />
        <button type="submit">Send</button>
      </form>
    </>
  );
}
```

When the parent re-renders with new `messages` from the server, the optimistic value is automatically replaced.

### 8. Streaming and Suspense

Wrap slow async server components in `<Suspense>` to stream them independently. The shell renders immediately; slow parts fill in as they resolve.

**Not this:** awaiting all queries sequentially in one component -- user sees nothing until the slowest resolves.

**This:**
```tsx
import { Suspense } from 'react';
export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />         {/* Streams in ~1s */}
      </Suspense>
      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics />     {/* Streams in ~3s */}
      </Suspense>
    </div>
  );
}

async function Stats() {
  const stats = await getStats();
  return <StatsDisplay data={stats} />;
}
```

Streaming enables **selective hydration**: React prioritizes hydrating the component the user interacts with first.

### 9. The Serialization Boundary

Props from Server Components to Client Components must be serializable to JSON.

**Can cross:** strings, numbers, booleans, null, undefined, plain objects, arrays, Server Action references, Promises (via `use()`), Server Components as JSX children.

**Cannot cross:**
```tsx
<ClientComponent onClick={() => console.log('hi')} />  // function
<ClientComponent createdAt={new Date()} />              // Date
<ClientComponent user={new User('Dan')} />              // class instance
<ClientComponent tags={new Map([['a', 1]])} />          // Map/Set
```

**Fix -- serialize before the boundary:**
```tsx
export default async function Page() {
  const user = await getUser();
  return (
    <ClientComponent
      userName={user.name}                      // string
      createdAt={user.createdAt.toISOString()}   // string
      tags={Object.fromEntries(user.tags)}      // plain object
    />
  );
}
```

Server Components as children pass through fine -- they are rendered on the server and sent as serialized JSX:
```tsx
<ClientSidebar>
  <ServerRenderedNav />  {/* Rendered on server, passed as serialized JSX */}
</ClientSidebar>
```

### 10. The use() Hook

`use()` reads a Promise or Context during render. It replaces `useContext` and enables consuming promises from Server Components.

**Context (replaces useContext -- can be called conditionally):**
```tsx
'use client';
import { use } from 'react';
import { ThemeContext } from './theme';

function Button({ showIcon }: { showIcon: boolean }) {
  if (showIcon) {
    const theme = use(ThemeContext);  // Conditional -- useContext cannot do this
    return <button className={theme}>Click</button>;
  }
  return <button>Click</button>;
}
```

**Promise from Server Component:**
```tsx
// Server Component -- starts fetch, does NOT await
export default function Page() {
  const commentsPromise = fetchComments();
  return (
    <Suspense fallback={<CommentsSkeleton />}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  );
}

// Client Component -- consumes with use()
'use client';
import { use } from 'react';
function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  const comments = use(commentsPromise);  // Suspends until resolved
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}
```

---

## Anti-Patterns

### Fetching on the Client When the Server Has the Data
If data is available at request time, fetch in a Server Component. Client `useEffect` adds a round trip, loading states, and more JS.

### Wrapping Entire Pages in "use client"
One `onClick` does not justify making the entire page client. Extract the interactive part into a leaf.

### Building API Routes for Server Actions
Server Actions replace API routes for UI-initiated mutations. Only use Route Handlers for webhooks, third-party integrations, or external API consumers.

### Passing Non-Serializable Props Across the Boundary
Functions, classes, Date objects, Maps, Sets cannot be props to client components. Serialize to plain values.

### Treating "use client" as "Runs Only in Browser"
Client Components render on the server during SSR and hydrate in the browser. They run in both environments. Do not assume `window` exists during initial render.

### Using useEffect for Data Available at Render Time
If a Server Component can fetch it, do not use `useEffect`. Server fetch is faster (closer to data), ships less JS, needs no loading state.

---

## Decision Framework

### Server Component or Client Component?

| Need | Component Type |
|------|---------------|
| Display data from DB or API | Server Component |
| Static content, markdown, text | Server Component |
| onClick, onChange, onSubmit | Client Component |
| useState, useReducer, useEffect | Client Component |
| Browser APIs (window, localStorage) | Client Component |
| Third-party client library (chart, map) | Client Component |

### How to Handle Mutations

| Scenario | Approach |
|----------|----------|
| Form submission from UI | Server Action |
| Programmatic mutation from client | Server Action called directly |
| Webhook from external service | Route Handler |
| File upload/download | Route Handler |
| Public API endpoint | Route Handler |

### Where to Put the Client Boundary

1. Start with everything as Server Components
2. Identify interactive parts (state, events, browser APIs)
3. Extract those into the smallest possible client components
4. Pass server-rendered content as `children` when possible

---

## Code Review Checklist

- [ ] No `'use client'` on components that only display data
- [ ] Client boundary pushed to the smallest interactive leaf
- [ ] Server Components fetch data directly -- no `useEffect` for initial data
- [ ] Server Actions used for mutations, not custom API routes
- [ ] Props crossing the boundary are serializable (no functions, Dates, classes)
- [ ] Async server components wrap slow children in `<Suspense>`
- [ ] `useFormStatus` used instead of manual pending state tracking
- [ ] `useOptimistic` used for instant feedback on mutations
- [ ] `use()` used to consume promises from server, not `useEffect` + `useState`
- [ ] Server Actions validate input -- they are public endpoints

---

## Sources

- Abramov, "The Two Reacts" (overreacted.io)
- React documentation: Server Components, Server Actions, use() hook
- React RFC: React Server Components
- Markbage, React Server Components architecture

---

*"A React component is either a Server Component or a Client Component. Server Components run where the data is. Client Components run where the user is."* -- Dan Abramov, "The Two Reacts"
