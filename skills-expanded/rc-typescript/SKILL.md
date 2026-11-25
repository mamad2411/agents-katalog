---
name: rc-typescript
description: "TypeScript type design — illegal states unrepresentable, no escape hatches. Use when writing or reviewing TS. Not for framework APIs."
model: sonnet
effort: medium
---

# TypeScript

Not a language tutorial — the model already writes TypeScript. This is the **type design** the model
does not apply by default: left alone it produces loose, structurally-typed code that compiles and still
permits the bug. For framework and library API behaviour, which moves faster than any skill can track,
use the Context7 MCP; for the conventions of a specific repo, its `AGENTS.md`.

The whole discipline is one idea: **make the illegal state unrepresentable**, so the wrong code fails to
compile instead of failing in production.

## Model the state, don't flag it

Booleans multiply into states that cannot occur. Three flags describe eight states when the domain has
three.

```ts
// permits { loading: true, error: Error, data: User } — meaningless, and reachable
type State = { loading: boolean; error?: Error; data?: User };

// exactly the states that exist
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'failed'; error: Error }
  | { status: 'loaded'; data: User };
```

The discriminated union pays off at every use site: after `if (s.status === 'loaded')` the compiler
*knows* `s.data` exists, so the optional-chaining and the non-null assertions disappear on their own.

**The tell that you need one:** two optional fields where exactly one is ever set, or a comment
explaining which combination is valid.

## Exhaustiveness

A `switch` over a union must be exhaustive, and the compiler must be the thing that enforces it — so
adding a variant breaks the build at every site that needs updating, instead of silently falling through.

```ts
function label(s: State): string {
  switch (s.status) {
    case 'idle':    return 'Ready';
    case 'loading': return 'Loading…';
    case 'failed':  return s.error.message;
    case 'loaded':  return s.data.name;
    default: {
      const unreachable: never = s;   // a new variant fails to compile here
      throw new Error(`unhandled: ${JSON.stringify(unreachable)}`);
    }
  }
}
```

A `default` that returns a fallback value instead of the `never` check is how a new variant ships
unhandled.

## Parse at the boundary

Data crossing a trust boundary — HTTP response, request body, `localStorage`, env, a file, an event
payload — is `unknown` until validated. Validate once, at the edge, and let the parsed type flow inward.

```ts
const User = z.object({ id: z.string().uuid(), email: z.string().email() });
type User = z.infer<typeof User>;          // one source of truth for the shape

const res = await fetch(url);
const user = User.parse(await res.json()); // throws here, where the context is
```

Derive the type from the schema (`z.infer`), never declare both — two declarations drift, and the day
they do the compiler is on the wrong side. Past the boundary, stop re-validating: the type is the proof.

Inside your own code, no such ceremony. Validating an internal call's arguments is noise the compiler
already covers.

## No escape hatches

Each of these silences a signal that something is actually wrong. The `no-workarounds-guard` hook
rejects them mechanically; the point here is what to do instead.

| Instead of | Do |
| --- | --- |
| `as SomeType` on unvalidated data | parse it at the boundary |
| `as any` to stop an error | fix the type, or model the state properly |
| `!` non-null assertion | narrow it — `if (!x) return`, or make the type non-optional |
| `@ts-ignore` / `@ts-expect-error` | fix the cause; if a dependency's types are wrong, declare a local module type |
| `any` in a signature | `unknown` plus narrowing, or a generic |
| `object` / `{}` | the actual shape |

`as const` and `satisfies` are not escape hatches — they are the opposite:

```ts
const ROUTES = { home: '/', user: '/u/:id' } satisfies Record<string, `/${string}`>;
// keys stay literal AND the values are checked — `as Record<...>` would widen them away
```

Use `satisfies` when you want a value checked against a type **without** losing its narrow inferred
form. That is almost always what you wanted when you reached for `as`.

## Make distinct things distinct

A `string` that is a `UserId` and a `string` that is an `OrgId` are interchangeable to the compiler, so
the day they get swapped nothing complains. Brand them when the confusion is plausible and the cost is
real:

```ts
type UserId = string & { readonly __brand: 'UserId' };
const UserId = (s: string) => s as UserId;   // the one sanctioned assertion: at the constructor
```

Reserve this for identifiers that genuinely get crossed — money amounts, units, IDs of similar-looking
entities. Branding every string is ceremony.

## Nullability

Distinguish "absent" from "empty" from "not loaded yet" only when the caller behaves differently for
each. When it does not, collapse them — a type with `T | null | undefined` usually means nobody decided.
Prefer one: `T | undefined` for a value that may be missing, and make the absence impossible where you
can (a required field, a non-empty array type, a constructor that cannot produce the invalid object).

## Errors

A thrown value is `unknown` in a `catch`, and it genuinely can be anything. Narrow before using it:

```ts
catch (e) {
  const message = e instanceof Error ? e.message : String(e);
}
```

For an expected failure — validation, a 404, a business rule — a result type in the signature beats a
throw the caller cannot see: `type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }`.
Reserve throwing for the genuinely exceptional, and never swallow: an empty `catch {}` on a trusted path
is a deleted signal.

## Config

`strict: true` is the baseline; without it most of the above is unenforced. Beyond it,
`noUncheckedIndexedAccess` is the highest-value flag most projects are missing — it makes `arr[0]`
`T | undefined`, which is the truth. When a repo has these off, that is a finding to surface, not a
convention to match.
