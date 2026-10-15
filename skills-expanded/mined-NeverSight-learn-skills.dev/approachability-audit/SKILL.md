---
name: approachability-audit
description: Review code from the perspective of a new TypeScript developer. Use when the user asks whether code feels wrong, too indirect, too clever, hard to follow, or wants a pass focused on unnecessary abstractions, misleading names, layered type tricks, and first-read clarity.
---

# Approachability Audit

Read the code like a smart but newly onboarded TypeScript developer.

Related skills: use `post-implementation-review` for the full second-read
ritual after implementation, `refactoring` for caller counting and inlining
mechanics, and `cohesive-clean-breaks` when a readability issue points to the
wrong public boundary.

The goal is not "make it shorter" or "make it more abstract." The goal is:

- make the first read cheaper
- make ownership boundaries obvious
- remove tricks that only exist for the type system
- keep real domain or validation boundaries intact

## What to Look For

- Names that imply a more important concept than the code actually represents
- Types that pretend to be runtime truths but are only inference shims
- Client-only hacks living in server packages, or server concerns leaking into browser/shared code
- Single-use helpers that hide simple control flow
- Tiny wrappers that add vocabulary but not clarity
- Multiple files for one concept when readers really need one place to look
- "Smart" generic helpers where direct code would be easier to trust
- Ad-hoc `as` assertions outside a clear parse or interop boundary
- JSDoc that restates code instead of explaining why the boundary exists

## What Not to "Fix"

- Real parse boundaries at JSON, file, or network edges
- Runtime validation that protects unsafe input
- Shared contracts that genuinely belong in one place
- Repetition that is cheaper than an extra abstraction

## Review Method

1. Start with the entrypoint a caller uses first.
2. Trace the minimum path needed to understand the behavior.
3. Count the hops:
   - if understanding one field or behavior requires jumping across multiple files, ask whether that indirection earns its keep
4. Mark each abstraction as one of:
   - `earns its keep`
   - `probably inlineable`
   - `wrong ownership boundary`
   - `misleading name`
   - `type-system workaround`
5. Prefer fixes that:
   - move code to the right owner
   - rename things honestly
   - collapse fake layers
   - replace cleverness with one explicit boundary

## Output Shape

When reporting findings, prioritize:

1. The one or two biggest readability or ownership smells
2. Why a new TypeScript developer would stumble there
3. The smallest fix that improves trust in the code

When editing code:

- keep commits surgical
- add or improve JSDoc on public boundaries
- do not add a new abstraction unless it reduces total cognitive load
- prefer explicit names like `*Bridge`, `*Contract`, `*Parser`, `*Factory`, `*State`

## Heuristics

### Good smell

```ts
export type SessionContract = { ... };
```

Portable type, honest name, obvious job.

### Bad smell

```ts
export type AppAuth = {
  options: { plugins: [...] }
};
```

If this is not the real auth type, do not name it like it is.

### Good workaround

```ts
export type CustomSessionClientBridge = { ... };
```

If a library forces a type trick, keep it local and name it as a bridge.

## Success Criteria

The code should leave a new teammate thinking:

- "I know which file owns this concept."
- "I know which type is a real contract and which one is just library glue."
- "I don't have to reverse-engineer the architecture from naming accidents."
