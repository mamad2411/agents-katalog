---
name: naming-helper
description: Proposes and audits names for code identifiers, APIs, files, and config keys — generating consistent, intention-revealing candidates that follow the project's existing conventions (case style, domain vocabulary) and avoiding misleading or abbreviation-heavy names.
when_to_use: User asks 'what should I call this', to rename for clarity, to name a function/variable/endpoint/flag/table, or to audit a diff for naming consistency before review.
---

## When to Use

- "What should I call this?" / "Better name for X?" / "Rename this for clarity."
- Naming a new function, variable, class, endpoint, CLI flag, env var, DB table/column, or config key.
- Auditing a diff or file for naming consistency before code review.

Skip when: the name is dictated by an external contract (HTTP spec header, third-party API field, framework magic name like `getServerSideProps`) — match the contract exactly, don't "improve" it.

## Steps

1. **Infer conventions before proposing.** Grep the surrounding scope, do NOT guess:
   - Case style per kind — run e.g. `rg '\b(fn|def|func|function|const|let|var)\s+\w+' <dir>` and tally: are functions `camelCase`, `snake_case`, `PascalCase`? Booleans `is*/has*/should*`? Constants `SCREAMING_SNAKE`? Endpoints kebab or snake? Env vars `UPPER_SNAKE`?
   - Domain vocabulary — does the codebase say `user` or `account`, `cancel` or `void`, `delete` or `remove`? Reuse the term already in use; don't introduce a synonym.
   - Verb register for siblings — list the neighbors (`rg 'def (get|fetch|load|read|find)_' <module>`) and match the dominant verb instead of mixing.
2. **Propose 2-3 candidates per item, each with a one-line rationale**, then mark the recommended one. Format:
   ```
   processData()  →
     1. normalizeOrderRows()   ← recommend: says WHAT (normalize) + ON WHAT (order rows)
     2. cleanOrders()          ← "clean" is vague, what does clean mean here?
     3. transformOrderData()   ← "Data" is a noise word; "transform" hides intent
   ```
3. **Apply the quality bar** to filter candidates:
   - Intention-revealing: name answers why it exists / what it returns, not how it's implemented.
   - Searchable: no single-letter (except loop indices `i/j` in ≤3-line scopes) and no ambiguous 2-char names.
   - Pronounceable, no encoded type (`strName`, `arrItems`, `bIsValid` — drop the prefix).
   - No noise words: `Data`, `Info`, `Manager`, `Helper`, `Object`, `Stuff`, `tmp`, `do*`, `handle*` unless they add real meaning.
   - No misleading terms: `userList` that's a `Set`/`Map`; `getX()` that mutates or does I/O; `isReady` that returns a count.
   - Length scales with scope: tight loop var short; module-level export descriptive.
4. **Consistency check across siblings.** Flag mixed vocabularies for the same concept:
   - Verb drift: `getUser` + `fetchOrders` + `loadCart` in one module → pick one verb.
   - Antonym pairs must match: `open/close`, `begin/end`, `add/remove`, `start/stop` — not `add/delete`.
   - Singular/plural per cardinality: `user` returns one, `users` returns a collection.
   - Same prefix family: if one flag is `--dry-run`, a sibling should be `--no-cache`, not `--skipCache`.
5. **Audit mode** (when given a diff/file): scan only changed/added identifiers → output a table `current → suggested | reason`. **Names only — never change behavior, signatures' arg order, or types.** If a rename touches a public/exported symbol, list every call-site that must change and say so explicitly; do not silently break callers.

## Common Errors

- **Inventing a convention instead of detecting one.** If you didn't grep, you don't know the case style — a `camelCase` suggestion in a `snake_case` file is an instant reject. Detect first.
- **Renaming public API / serialized keys as if they're free.** A DB column, JSON field, env var, or exported function rename is a breaking change + (for columns) a migration. Flag it as breaking, don't bundle it into a "cleanup."
- **Reserved words & collisions.** Check the target name isn't a language keyword (`class`, `type`, `enum`, `default`), a builtin (`id`, `list`, `dict`, `len`, `type`), or already taken in the same scope. A name that shadows a builtin is worse than the original.
- **Over-shortening.** `cfg`, `usr`, `ctx`, `req/res` are fine ONLY if already idiomatic in this codebase; otherwise expand. Never abbreviate to save typing — searchability beats brevity.
- **Boolean inversions.** Renaming `disabled` → `enabled` (or vice-versa) flips meaning at every call site. If you flip polarity, that's a behavior change — flag it, don't do it silently.
- **Hungarian / type-encoded names** survive in legacy spots; match the file's existing pattern even if you dislike it — consistency within a file beats global purity.

## Verify

- Recommended name is in the file's detected case style (re-grep one neighbor to confirm).
- Name reuses existing domain vocabulary, no new synonym introduced.
- No collision: the name isn't already declared in scope and isn't a keyword/builtin.
- Verb/antonym/cardinality matches its siblings.
- For audit/rename output: every breaking rename (public symbol, serialized key, env var, column) is explicitly tagged as breaking with its call-sites/migration noted; no behavior, type, or signature was altered — names only.
