---
name: typed-api-hooks-forms
description: >-
  Use when adding API hooks (useUser, usePost) on an SWR project, or any time
  the task includes Zod + react-hook-form on the client. For new Lovable
  projects, prefer TanStack Query (tanstack-query-alternative) — Lovable's
  default. Not for styling-only changes or auth provider setup.
---

# Typed API hooks and forms

This skill covers the **forms half** (Zod + react-hook-form) and an SWR-based hooks pattern. Pick one cache library per project:

| If the project uses | Use this skill plus |
|---------------------|--------------------|
| **TanStack Query** (Lovable default) | [`tanstack-query-alternative`](../tanstack-query-alternative/) for hooks, this skill for forms |
| **SWR** | This skill end-to-end |

**Never mix** TanStack Query and SWR in the same app.

## Stack defaults

| Concern | Use |
|--------|-----|
| Client cache (TanStack project) | `@tanstack/react-query` — see [`tanstack-query-alternative`](../tanstack-query-alternative/) |
| Client cache (SWR project) | [SWR](https://swr.vercel.app) (`useSWR`) |
| Backend | Supabase client + generated `Database` types |
| Forms | `react-hook-form` + `@hookform/resolvers/zod` + **Zod** |
| UI wiring | shadcn `Form`, `FormField`, `FormMessage` |

Install only if missing: cache library, `zod`, `react-hook-form`, `@hookform/resolvers`.

---

## 1. Data layer layout

```
src/
  lib/
    supabase.ts          # createClient (or existing)
  types/
    database.ts          # generated Supabase types (do not hand-edit)
  api/
    users.ts             # pure fetchers (no React)
    posts.ts
  hooks/
    useUser.ts           # thin useSWR wrappers
    usePosts.ts
```

**Rules**

- **Fetchers** live in `api/` — async functions that return typed data or throw.
- **Hooks** live in `hooks/` — only `useSWR` + argument handling + derived return shape.
- **Never** call `supabase.from(...)` directly inside components; go through a hook.

---

## 2. Type safety (required)

1. Regenerate or use existing `Database` types from Supabase (`supabase gen types typescript`).
2. Type every fetcher return value:

```ts
import type { Database } from "@/types/database";

type User = Database["public"]["Tables"]["users"]["Row"];
type Post = Database["public"]["Tables"]["posts"]["Row"];

export async function fetchUser(id: string): Promise<User | null> {
  const { data, error } = await supabase
    .from("users")
    .select("*")
    .eq("id", id)
    .maybeSingle();
  if (error) throw error;
  return data;
}
```

3. For joined/nested selects, define an explicit type (do not use `any`):

```ts
export type PostWithAuthor = Post & {
  author: Pick<User, "id" | "display_name" | "avatar_url">;
};
```

4. Hook return types must be explicit or inferred from the fetcher — never `data: any`.

5. Mutations: type insert/update payloads with `TablesInsert` / `TablesUpdate` from generated types.

---

## 3. SWR hooks pattern

### Stable cache keys

Use **tuple keys** so SWR dedupes identical requests across the tree:

```ts
// hooks/useUser.ts
import useSWR from "swr";
import { fetchUser } from "@/api/users";

export function useUser(userId: string | null | undefined) {
  const key = userId ? (["user", userId] as const) : null;
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchUser(userId!));
  return { user: data ?? null, error, isLoading, refresh: mutate };
}
```

```ts
// hooks/usePosts.ts
export function usePosts(filters: { authorId?: string; status?: string }) {
  const key = ["posts", filters] as const;
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchPosts(filters));
  return { posts: data ?? [], error, isLoading, refresh: mutate };
}
```

**Naming**: `useUser`, `usePost`, `usePosts`, `useComments` — entity name matches the hook; plural hook returns arrays.

### Do not

- Put unstable objects in keys without normalizing (e.g. new `{}` every render). Serialize filters: `["posts", authorId, status]`.
- Duplicate keys for the same resource (`"user-" + id` vs `["user", id]`).
- Fetch inside `useEffect` when a hook already exists for that resource.

### Global SWR config (optional)

If many hooks share behavior, wrap the app once:

```ts
<SWRConfig value={{ revalidateOnFocus: false, dedupingInterval: 2000 }}>
```

---

## 4. One fetch when the same data is needed in many places

**SWR dedupes by key** — multiple components calling `useUser(id)` with the same `id` share one request. Ensure keys match.

When **several UI surfaces always need the same Supabase graph together**, prefer **one fetcher** with a single `.select()` that includes every column and relation needed, instead of three parallel hooks hitting the same row:

```ts
// api/posts.ts — one round trip
export async function fetchPostDetail(postId: string): Promise<PostWithAuthorAndComments> {
  const { data, error } = await supabase
    .from("posts")
    .select(`
      *,
      author:users!posts_author_id_fkey ( id, display_name, avatar_url ),
      comments ( id, body, created_at, author:users ( id, display_name ) )
    `)
    .eq("id", postId)
    .single();
  if (error) throw error;
  return data;
}
```

```ts
export function usePostDetail(postId: string | null | undefined) {
  const key = postId ? (["post-detail", postId] as const) : null;
  return useSWR(key, () => fetchPostDetail(postId!));
}
```

**Choose one strategy**

| Situation | Approach |
|-----------|----------|
| Same entity, same fields, many components | One hook + shared SWR key |
| Same table, different filters | One `usePosts(filters)`; distinct keys per filter tuple |
| List page + detail page need overlapping rows | List hook for list; detail hook with richer `select` — do not refetch list fields in a second hook on the detail page unless you need independent cache TTL |
| Multiple components need full post + author + comments on one screen | Single `fetchPostDetail` / `usePostDetail` |

After mutations, call `mutate` on every affected key (or `mutate(key => Array.isArray(key) && key[0] === 'posts')` for broad invalidation).

---

## 5. Mutations

Keep mutations in `api/` (e.g. `createPost`, `updateUser`). From components:

1. Call mutation function.
2. `await refresh()` from the hook, or `mutate` global keys for that entity.
3. Surface errors to the UI (toast or form-level).

Do not leave lists stale after create/update/delete.

---

## 6. Forms — Zod + react-hook-form (required)

Every new or edited form must use a **Zod schema** and **react-hook-form** with `zodResolver`.

### Schema

```ts
import { z } from "zod";

export const postFormSchema = z.object({
  title: z.string().min(1, "Title is required").max(120),
  body: z.string().min(1, "Body is required"),
  status: z.enum(["draft", "published"]),
});

export type PostFormValues = z.infer<typeof postFormSchema>;
```

Reuse `PostFormValues` for props and API payloads. Align enums and max lengths with the database/check constraints.

### Form component

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { postFormSchema, type PostFormValues } from "@/schemas/post";

export function PostForm({ defaultValues, onSubmit }: {
  defaultValues?: Partial<PostFormValues>;
  onSubmit: (values: PostFormValues) => Promise<void>;
}) {
  const form = useForm<PostFormValues>({
    resolver: zodResolver(postFormSchema),
    defaultValues: { title: "", body: "", status: "draft", ...defaultValues },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {/* remaining fields */}
        <Button type="submit" disabled={form.formState.isSubmitting}>
          Save
        </Button>
      </form>
    </Form>
  );
}
```

### Do not

- Validate only with HTML `required` or manual `if (!title)` checks.
- Duplicate schema rules in component state.
- Use untyped `useForm()` without `PostFormValues`.
- Submit `FormData` without parsing through the Zod schema when the rest of the app uses this pattern.

### Edit forms

Set `defaultValues` from the SWR hook (`usePost`, `useUser`). Reset when async data arrives:

```ts
useEffect(() => {
  if (post) form.reset(postFormSchema.parse(mapPostToForm(post)));
}, [post, form]);
```

Map DB nullables to form defaults explicitly in `mapPostToForm`.

---

## 7. Implementation checklist

Before finishing, confirm:

- [ ] Fetchers in `api/` are typed; hooks in `hooks/` use stable tuple keys.
- [ ] No duplicate Supabase round trips for the same screen when one joined `select` suffices.
- [ ] Components use hooks (`useUser`, `usePosts`, …), not raw Supabase calls.
- [ ] Forms use Zod + `zodResolver` + typed `useForm<…>`.
- [ ] Mutations invalidate or `mutate` the right SWR keys.
- [ ] Loading and error states exposed from hooks and shown in UI.

---

## 8. Avoid

- `useEffect` + `fetch` for server data that SWR should own.
- Inline Supabase queries in JSX/event handlers (except rare one-off admin scripts).
- `any`, `@ts-ignore`, or untyped `data` from Supabase.
- Multiple incompatible cache keys for the same resource.
- Forms without Zod (when this skill applies).

For deeper copy-paste templates, see [examples.md](examples.md).
