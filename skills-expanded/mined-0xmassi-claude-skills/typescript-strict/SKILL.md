---
name: typescript-strict
description: >
  TypeScript strictness, clean code, and security rules. Use when writing, reviewing,
  or refactoring TypeScript code in any project. Enforces strict type safety (no any,
  no as, no unknown abuse), proper error handling patterns, import hygiene, React
  component conventions, and vulnerability prevention. Derived from 10+ production
  TypeScript projects with 100% strict mode adoption.
---

# TypeScript Strict Standard

Rules extracted from 10+ production TypeScript codebases. All projects use `strict: true`.

## CRITICAL: Type Safety Rules

### TS-01: Never use `any`

```typescript
// BAD
function process(data: any) { return data.value; }
const handler = (e: any) => console.log(e);

// GOOD
function process(data: Record<string, unknown>) { return "value" in data ? data.value : undefined; }
const handler = (e: MouseEvent) => console.log(e.target);

// ACCEPTABLE: Library integration boundaries (shadcn/ui props, Tauri responses)
// Must add a comment explaining why
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- CodeMirror extension type
```

Exceptions (document each with a comment):
- Third-party library props that genuinely require `any`
- Generic catch blocks: `catch (e: unknown)` then narrow

### TS-02: Avoid `as` type assertions

```typescript
// BAD
const user = response as User;
const el = document.getElementById("root") as HTMLDivElement;

// GOOD: use type guards
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}
if (isUser(response)) { /* response is User here */ }

// GOOD: use generics
const el = document.getElementById("root");
if (el instanceof HTMLDivElement) { /* el is HTMLDivElement here */ }

// ACCEPTABLE (rare): When you KNOW the type and can't prove it
// Must be `as unknown as T` with a SAFETY comment
const validated = session as unknown as AuthenticatedSession; // SAFETY: verified user.id exists above
```

When `as` is acceptable:
- Prisma generated types requiring cast at boundaries
- After runtime validation (Zod parse → safe to assert)
- Event target narrowing after guard: `e.target as Node` after `if (e.target)`

### TS-03: Use `unknown` over `any` for untyped data

```typescript
// BAD
function parse(input: any): Config { ... }

// GOOD
function parse(input: unknown): Config {
  if (typeof input !== "object" || input === null) throw new Error("Invalid input");
  // Narrow from unknown
}
```

### TS-04: Never use `@ts-ignore`

```typescript
// BAD
// @ts-ignore
const x = brokenLibrary.method();

// GOOD: use @ts-expect-error with explanation (if truly needed)
// @ts-expect-error: library v3 types missing this method, fixed in v4
const x = brokenLibrary.method();
```

Target: zero `@ts-ignore` across the project.

### TS-05: Minimize non-null assertions (`!`)

```typescript
// BAD
const name = user!.name;

// GOOD
if (!user) throw new Error("User required");
const name = user.name;

// ACCEPTABLE: After a guard that guarantees existence
if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
  // menuRef.current is guaranteed non-null here
}
```

Target: under 10 non-null assertions per project, each justified by a guard above.

## HIGH: Clean Code Rules

### TS-06: Use type-only imports

```typescript
// BAD
import { Agent, AgentSession } from "@/context/AppContext";

// GOOD: when only used as types
import type { Agent, AgentSession } from "@/context/AppContext";
import { useApp } from "@/context/AppContext"; // Value import separate
```

Reduces bundle size and makes dependency intent clear.

### TS-07: Use discriminated unions over boolean flags

```typescript
// BAD
type Status = { loading: boolean; error: boolean; data?: User };

// GOOD
type Status =
  | { state: "idle" }
  | { state: "loading" }
  | { state: "error"; message: string }
  | { state: "success"; data: User };
```

### TS-08: Prefer `type` over `interface` (unless extending)

```typescript
// GOOD: type for unions, intersections, mapped types
type Page = "workspace" | "github" | "settings";
type Agent = "claude" | "codex" | "opencode";
type Props = { title: string; onClose: () => void };

// GOOD: interface when you need declaration merging or extends
interface AgentNodeData extends Record<string, unknown> {
  role: AgentRole;
  isEnabled: boolean;
}
```

Default: `type` for definitions, `interface` only when you need extends/declaration merging.

### TS-09: Path aliases always

```typescript
// BAD
import { Button } from "../../../components/ui/button";

// GOOD
import { Button } from "@/components/ui/button";
```

Configure in `tsconfig.json`:
```json
{ "compilerOptions": { "paths": { "@/*": ["./src/*"] } } }
```

### TS-10: No `React.FC`: use direct function declarations

```typescript
// BAD
const PostIt: React.FC<PostItProps> = ({ folder, onSave }) => { ... };

// GOOD
export default function PostIt({ folder, onSave }: PostItProps) { ... }

// Also GOOD: arrow function with explicit props type
export const PostIt = ({ folder, onSave }: PostItProps) => { ... };
```

Avoid `React.FC` entirely.

## HIGH: Error Handling Rules

### TS-11: Structured error handling with Result pattern or Zod

```typescript
// Pattern A: Discriminated union Result
type AuthResult =
  | { session: AuthenticatedSession; error: null }
  | { session: null; error: NextResponse };

async function requireAuth(): Promise<AuthResult> {
  const session = await auth();
  if (!session) return { session: null, error: unauthorized() };
  return { session, error: null };
}

// Pattern B: Zod validation at boundaries
const parsed = serverEnvSchema.safeParse(process.env);
if (!parsed.success) {
  throw new Error(`Invalid env:\n${parsed.error.format()}`);
}
```

### TS-12: Catch blocks must narrow error type

```typescript
// BAD
try { ... } catch (err) { console.log(err.message); }

// GOOD
try { ... } catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  toast.error(`Failed: ${message}`);
}
```

### TS-13: Never swallow errors silently

```typescript
// BAD
try { await save(); } catch {}

// GOOD
try { await save(); } catch (err) {
  console.error("Save failed:", err);
  // At minimum log, ideally surface to user
}
```

## MEDIUM: React-Specific Rules

### TS-14: Event listener cleanup

```typescript
useEffect(() => {
  const handler = (e: KeyboardEvent) => { ... };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, []);
```

### TS-15: Tauri event listener cleanup

```typescript
useEffect(() => {
  let unlisten: (() => void) | undefined;
  listen<Payload>("pty://output", (event) => {
    // handle event
  }).then(fn => { unlisten = fn; });
  return () => unlisten?.();
}, []);
```

### TS-16: Context layering order matters

Outer context = fewer dependencies. Never make inner context depend on outer context's consumer.

## MEDIUM: Security Rules

### TS-17: Validate all external input with Zod

```typescript
// API route handler
export async function POST(request: Request) {
  const raw = await request.json();
  const parsed = createItemSchema.safeParse(raw);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.format() }, { status: 400 });
  }
  // Use parsed.data (typed and validated)
}
```

### TS-18: Environment variables validated at startup

```typescript
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
// App won't start with missing/invalid env vars
```

### TS-19: No string interpolation in SQL/HTML

```typescript
// BAD: SQL injection
const users = await db.$queryRaw`SELECT * FROM users WHERE id = ${id}`;
// This IS safe in Prisma (tagged template), but avoid raw queries when possible

// BAD: XSS
element.innerHTML = `<p>${userInput}</p>`;

// GOOD
element.textContent = userInput;
```

### TS-20: Never expose secrets to client

```typescript
// BAD: NEXT_PUBLIC_ prefix exposes to browser
NEXT_PUBLIC_DATABASE_URL=postgresql://...

// GOOD: server-only env vars have no prefix
DATABASE_URL=postgresql://...
JWT_SECRET=...
```

## HIGH: Modern Type Patterns

### TS-21: Exhaustiveness checks on unions

```typescript
function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}

type Status = "idle" | "loading" | "success" | "error";

function render(s: Status) {
  switch (s) {
    case "idle": return <Idle />;
    case "loading": return <Spinner />;
    case "success": return <Done />;
    case "error": return <Failed />;
    default: return assertNever(s); // Compile error if a case is added
  }
}
```

Add a new union member without updating `render()` and the build fails.

### TS-22: `readonly` for inputs you do not own

```typescript
// BAD: caller can mutate, function can mutate
function totalPrice(items: Item[]): number { ... }

// GOOD: input is read-only at the type level
function totalPrice(items: ReadonlyArray<Item>): number { ... }

// Component props
type Props = { readonly user: User; readonly onSave: () => void };
```

Default props and shared state to `readonly`. Mutate only your own scope.

### TS-23: `satisfies` over `as` for typed literals

```typescript
type RouteConfig = Record<string, { path: string; auth: boolean }>;

// BAD: widens, lets you typo keys
const routes = { home: { path: "/", auth: false } } as RouteConfig;

// GOOD: validates shape, keeps narrow keys
const routes = {
  home: { path: "/", auth: false },
  settings: { path: "/settings", auth: true },
} satisfies RouteConfig;

routes.home.path; // "/" inferred, not string
```

`satisfies` removes most legitimate uses of `as`.

## HIGH: Modern Runtime Patterns

### TS-24: `using` / `await using` for explicit resource management

```typescript
// Old: try/finally with manual cleanup, easy to forget
async function readConfig() {
  const handle = await fs.open(path);
  try {
    return await handle.readFile();
  } finally {
    await handle.close();
  }
}

// New: scoped disposal, runs even on throw
async function readConfig() {
  await using handle = await fs.open(path);
  return await handle.readFile();
} // close() runs here automatically
```

Any object with `Symbol.dispose` (sync) or `Symbol.asyncDispose` works. Native in TS 5.2+, runtime support in Node 22+ and modern browsers.

### TS-25: `NoInfer<T>` to anchor inference

```typescript
// BAD: T is inferred from defaultValue, not the intended source
function pick<T>(values: T[], defaultValue: T): T { ... }
pick(["a", "b"], 1); // T inferred as string | number, no error

// GOOD: defaultValue cannot widen T
function pick<T>(values: T[], defaultValue: NoInfer<T>): T { ... }
pick(["a", "b"], 1); // Error: 1 is not "a" | "b"
```

Use on parameters that should accept the inferred type but not contribute to it.

## tsconfig.json Baseline

Every project must have at minimum:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "moduleResolution": "bundler",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

For maximum strictness (Chrome extensions, security-critical, Node native TS):
```json
{
  "compilerOptions": {
    "noUncheckedSideEffectImports": true,
    "exactOptionalPropertyTypes": true,
    "erasableSyntaxOnly": true,
    "isolatedDeclarations": true
  }
}
```

`erasableSyntaxOnly` (TS 5.8+) bans enums, namespaces, and parameter properties so source runs unmodified under Node's native TypeScript stripping. `isolatedDeclarations` (TS 5.5+) requires explicit return types on exported APIs, enabling parallel build and faster type-checking.

## Version Targets

- **TypeScript 6.0** (Mar 2026) is the current stable. Lowest target is now ES2015, `target: es5` deprecated. New code should drop ES5 polyfills.
- **TypeScript 7.0 beta** (Apr 2026) ships a native compiler ported to Go, ~10x faster than 6.0 with the same type system. Migrate when stable, no source changes required.
- The `--upsert` Map/WeakMap methods (`getOrInsert`, `getOrInsertComputed`) are usable with the new lib targets.
```
