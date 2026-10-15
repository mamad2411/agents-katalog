---
name: pyyupsk
description: Use when setting up projects, writing TypeScript/React/Vue components, configuring tooling, or applying pyyupsk's opinionated JS/TS coding patterns and conventions.
license: MIT
metadata:
  author: pyyupsk
  version: "2.3"
---

# Core Conventions

## CLI Tools

Prefer modern CLI tools over traditional counterparts in all bash commands, scripts, and terminal instructions.

| Tool      | Replaces       | Purpose                        |
| --------- | -------------- | ------------------------------ |
| `fd`      | `find`         | File search                    |
| `rg`      | `grep`         | Content search                 |
| `bat`     | `cat`          | File viewing                   |
| `eza`     | `ls`           | Directory listing              |
| `dust`    | `du`           | Disk usage                     |
| `duf`     | `df`           | Disk free                      |
| `procs`   | `ps`           | Process listing                |
| `dog`     | `dig`          | DNS lookup                     |
| `curlie`  | `curl`         | HTTP requests                  |
| `z`       | `cd`           | Directory navigation           |
| `xxd`     | `od`/`hexdump` | Hex dumps                      |
| `btop`    | `top`/`htop`   | System monitor                 |
| `tldr`    | `man`          | Quick reference (prefer first) |
| `delta`   | —              | Git diffs                      |
| `lazygit` | —              | Git TUI                        |
| `yazi`    | —              | File browsing                  |
| `atuin`   | —              | Shell history                  |
| `fzf`     | —              | Fuzzy finding                  |

## Tooling

- **Biome** — primary linter and formatter for JS/TS projects
- **ESLint** with `@pyyupsk/eslint-config` — use when Biome doesn't fully support the target (e.g. Vue, special plugins)
- No Prettier — Biome handles formatting; ESLint handles what Biome can't
- **Bun** as runtime and package manager — never `npm`/`yarn`/`pnpm` unless forced
- **`$schema`** in all config files — prefer local `node_modules/` path over HTTPS URL

```json
{ "$schema": "./node_modules/@biomejs/biome/configuration_schema.json" }
```

### `@pyyupsk/eslint-config`

Flat config package built on `typescript-eslint` + `eslint-plugin-unicorn`. Use `defineConfig` as the entry point:

```ts
// eslint.config.ts
import { defineConfig } from "@pyyupsk/eslint-config";

export default defineConfig();
```

**Options:**

```ts
defineConfig({
  ignores: ["dist/**"], // additional ignore patterns (gitignore auto-applied)
  perfectionist: true, // import/export sorting (recommended-natural preset)
  stylistic: true, // @stylistic formatting (single quotes, 2 spaces, no semi)
  vue: true, // Vue flat/recommended + typescript-eslint parser
  vue: { unocss: true }, // also enable @unocss/eslint-plugin
});
```

**Core rules always enabled:**

| Rule                                             | Effect                                |
| ------------------------------------------------ | ------------------------------------- |
| `@typescript-eslint/consistent-type-definitions` | Enforces `type` over `interface`      |
| `@typescript-eslint/no-explicit-any`             | Bans `any`                            |
| `prefer-object-has-own`                          | `Object.hasOwn` over `hasOwnProperty` |
| `unicorn/prefer-at`                              | `.at(-1)` over `[arr.length - 1]`     |
| `unicorn/prefer-number-properties`               | `Number.isNaN` / `Number.isFinite`    |
| `unicorn/prefer-string-replace-all`              | `replaceAll` over `replace`           |
| `unicorn/prefer-structured-clone`                | `structuredClone` over JSON clone     |

**Stylistic defaults** (when `stylistic: true`): single quotes, 2-space indent, no semicolons, trailing commas on multiline.

## Project Structure

All projects use `src/` as root. Files/folders: lowercase, at most one `-` (e.g. `some-thing.tsx`) — never multiple dashes. Hooks: camelCase (`useSomething.ts`).

```tree
src/
├── app/route/_components/   # scoped, not shared outside route
├── components/<category>/   # shared, grouped by category (never flat)
├── components/ui/           # shadcn/ui only
├── hooks/useSomething.ts
├── lib/  types/  utils/
└── assets/fonts/index.ts    # export const sans, mono
```

## TypeScript

### Never use `any`

```ts
// ❌
const val = thing as any;
// ✅ find the library type first; last resort only:
const val = thing as unknown as CustomType;
```

### Props

```tsx
// type over interface; Readonly<> always
type ButtonProps = { variant: "primary" | "secondary" };
function Button({ variant }: Readonly<ButtonProps>) {}

// children via PropsWithChildren — never add children manually
function Card({ title, children }: PropsWithChildren<CardProps>) {}

// extending HTML elements
import type { ComponentPropsWithoutRef } from "react";
type ButtonProps = ComponentPropsWithoutRef<"button"> & { variant?: string };
```

### Static values & type utilities

```ts
const VARIANTS = ["primary", "secondary", "ghost"] as const;
type Variant = (typeof VARIANTS)[number]; // extract array item type

// satisfies — type safety without widening
const theme = { primary: "#3b82f6" } satisfies Record<string, string>;

// derive types — never define manually when you can extract
type FilterState = ReturnType<typeof useFilters>;

// extract return type from Convex backend functions
import type { FunctionReturnType } from "convex/server";
import type { api } from "@/convex/_generated/api";
type Category = FunctionReturnType<typeof api.categories.get>;
type CategoryGroup = FunctionReturnType<typeof api.categoryGroups.list>[number];
```

### Modern String / Array / Object Methods

Prefer modern, non-mutating alternatives (Sonar-aligned):

```ts
// ❌
str.replace("foo", "bar")
str.match(/foo(\d+)/)       // use RegExp.prototype.exec instead
arr.sort((a, b) => a.localeCompare(b))
arr.reverse()
arr.splice(1, 1)
arr[0] = "new"
arr[arr.length - 1]
str[str.length - 1]
isNaN(value)
isFinite(value)
obj.hasOwnProperty(key)
JSON.parse(JSON.stringify(obj))

// ✅
str.replaceAll("foo", "bar")
/foo(\d+)/.exec(str)
arr.toSorted((a, b) => a.localeCompare(b))
arr.toReversed()
arr.toSpliced(1, 1)
arr.with(0, "new")
arr.at(-1)
str.at(-1)
Number.isNaN(value)
Number.isFinite(value)
Object.hasOwn(obj, key)
structuredClone(obj)
```

### UUIDs

```ts
// ❌
import { v4 as uuidv4 } from "uuid";

// ✅
crypto.randomUUID();
```

## Naming Conventions

- Handler **props**: `on` prefix — `onSubmit`, `onClick`
- Internal handlers: `handle` prefix — `handleSubmit`, `handleClick`

## Patterns

### Function declarations

```ts
// ❌ arrow functions for functions/components
const fetchUser = async (id: string) => { ... }
const Button = () => { ... }

// ✅ function declarations
async function fetchUser(id: string) { ... }
function Button() { ... }

// ✅ const only for values
const API_URL = "https://api.example.com"
```

### Early returns

```tsx
// ❌ nested ternaries
return loading ? <Spinner /> : error ? <Error /> : <Content />;

// ✅ early returns
if (loading) return <Spinner />;
if (error) return <Error />;
return <Content />;
```

### Error handling — `safe()` tuple

Never throw inside business logic. Return errors as values:

```ts
export async function safe<T>(promise: Promise<T>): Promise<[Error, null] | [null, T]> {
    try {
        return [null, await promise]
    } catch (e) {
        return [e instanceof Error ? e : new Error(String(e)), null]
    }
}

// usage
const [err, user] = await safe(fetchUser(id))
if (err) return <Error message={err.message} />
return <UserCard user={user} />
```

### Async/await — never `.then()`

```ts
// ❌ fetchUser().then(u => console.log(u))
// ✅ const user = await fetchUser()
```

### `cn()` — conditional only

```tsx
// ❌ static string, no cn() needed
<div className="flex items-center gap-2" />

// ✅ conditional or composed
<div className={cn("flex items-center gap-2", isActive && "bg-accent", className)} />
```

### Custom hooks over inline logic

```tsx
// ❌ fetch inside component
// ✅ extract to hook
function useUser(id: string) { ... }
function UserCard() {
    const { user } = useUser(id)
    return <div>{user?.name}</div>
}
```

### No barrel `export *`

```ts
// ❌ export * from "./Button"  // circular deps, breaks tree-shaking
// ✅ import { Button } from "@/components/ui/button"
```

### Singletons for third-party clients

```ts
let client: Resend | undefined;
function getResend() {
  if (!client) client = new Resend(process.env.RESEND_API_KEY!);
  return client;
}
export const resend = getResend();
```

## Next.js

```tsx
// Root layout — suppressHydrationWarning on <html>, fonts on <body> only
export default function RootLayout({ children }: PropsWithChildren) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(sans.variable, mono.variable)}>{children}</body>
    </html>
  );
}
// Base styles in CSS: body { @apply min-h-screen bg-background font-sans antialiased; }

// Fonts — src/assets/fonts/index.ts
export const sans = Geist({ subsets: ["latin"], variable: "--font-sans" });

// "use client" — push boundary as deep as possible, never at page level
// Server Actions — for mutations, not API routes
// Metadata — always export metadata/generateMetadata, never <head> tags
```

## Vue (Composition API)

`<script setup lang="ts">` only. Order inside script:

1. `type` / `interface`
2. `defineProps` / `defineEmits`
3. router/route composables — `useRouter`, `useRoute`, `useI18n`, etc.
4. data composables — `useLazyAsyncData`, `useFetch`, `useAsyncData`, etc.
5. `ref` / `reactive`
6. `computed`
7. functions — callee before caller (helpers before the handlers that call them)
8. lifecycle hooks — `onMounted`, `onUnmounted`, etc.; `watch` / `watchEffect` last

## State Management

**Zustand** (React) — one store per domain, file named `useXxxStore.ts` (camelCase, same as hooks):

```ts
const initialState = { search: "", status: "all" as const };
export const useFilterStore = create<FilterStore>((set) => ({
  ...initialState,
  setSearch: (search) => set({ search }),
  reset: () => set(initialState),
}));
```

**Pinia** (Vue) — Option Stores, one per domain, named `useXxxStore`.

## Git

Conventional Commits: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `test`, `perf`

Branch names reflect content not process: `feat/user-profile-sync` not `simplify/code-cleanup`

Prefer `git worktree` over `git stash`.

## package.json

Sort `scripts` alphabetically (A–Z).
