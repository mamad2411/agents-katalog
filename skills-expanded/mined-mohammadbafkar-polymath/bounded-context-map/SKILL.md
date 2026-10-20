---
name: bounded-context-map
description: Map a domain into DDD bounded contexts + a context map (customer-supplier, conformist, anti-corruption layer, shared kernel) with per-context ubiquitous language.
---

# bounded-context-map

> Carve a domain into bounded contexts before anyone draws service boundaries. A context map shows how contexts relate and where models must NOT leak.

## When to use

- A new system or a large feature spans several subdomains and the team keeps arguing over what a word means ("order", "account", "user").
- A monolith is being considered for decomposition and you need the domain boundaries first (the technical split is `service-decomposition`).
- A workflow invokes `polymath-architecture:bounded-context-map`.

Not this when: you already have one context and need its internals — that is `aggregate-design`. For the written decision record, hand off to `polymath-writing:adr`.

## Inputs

- A domain description, key business capabilities, and the teams that own them.
- Existing model names that collide or are overloaded.

## Procedure

1. **List subdomains** and classify each: *core* (the differentiator — invest here), *supporting* (needed, not special), *generic* (buy/adopt off the shelf). Effort follows this classification.
2. **Draw bounded contexts** — one model boundary per context. A term means exactly one thing inside a context; the same word may legitimately differ across contexts. Name each context after its language, not its database.
3. **Define the ubiquitous language** per context: 5–15 terms with one-line definitions. Flag every term whose meaning changes at a boundary — those boundaries are real.
4. **Map the relationships** between contexts, choosing the pattern honestly:
   - *Partnership* — two contexts succeed or fail together; coordinate releases.
   - *Customer–Supplier* — downstream's needs are in the upstream's backlog.
   - *Conformist* — downstream accepts the upstream model as-is (no leverage).
   - *Anti-corruption layer (ACL)* — downstream translates the upstream model so it can't pollute the local one. Default when integrating with legacy/3rd-party.
   - *Shared kernel* — a small shared model both own jointly; minimize its size.
   - *Open-host / Published language* — upstream offers a stable public contract to many.
5. **Mark integration direction and conformance pressure** on each edge (upstream/downstream). Downstream-of-many is a coupling risk; flag it.
6. **Name the risks**: contexts with no clear owner, a core subdomain treated as generic, or a shared kernel that is quietly growing.

## Output

- A one-page context map: contexts (with core/supporting/generic), relationship edges with patterns and direction, and the per-context ubiquitous-language table.
- A short "boundaries that will hurt" list — overloaded terms and ownerless contexts.

## Quality bar

- Every context has exactly one owning team and one language.
- Every cross-context edge names a relationship pattern — "they just call each other" is not a pattern.
- At least one term is shown meaning different things in two contexts, or you have probably drawn one context, not several.
