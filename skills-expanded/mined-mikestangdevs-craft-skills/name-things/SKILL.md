---
name: name-things
description: "Use when naming or renaming functions, variables, types, files, or modules, or when a review keeps stumbling over confusing names. Kills generic names (data, handle, process, manager, util), makes each name reveal intent and role, and aligns vocabulary with the domain. Use when two things have nearly the same name or reading code feels harder than it should."
---

# Name Things

## The failure mode this fixes

Bad names are the cheapest bug to introduce and the most expensive to live with. `data`, `handle`, `process`, `manager`, `info`, `util`, `temp`, `obj` — every one is a place where the author *gave up* on saying what the thing is. Agents are especially prone to this: they generate plausible-but-vague names at scale. The result is code that's technically correct and cognitively exhausting.

This skill makes names carry their weight: a good name tells you what something *is* and what role it plays, so you don't have to read the implementation to use it.

## When to Use This Skill

- Naming a new function, variable, type, file, or module
- Renaming during a refactor or extraction
- A review keeps tripping over what something means
- Two identifiers are confusingly similar (`user` vs `userData` vs `userInfo`)
- You're about to write a comment to explain a name — the name should do that job

**Don't use when:** the name is already domain-standard and clear (`id`, `i` in a tight loop, well-known abbreviations like `url`, `db`). Framework-idiomatic names in their conventional position (`req`/`res` in an Express handler, `ctx`, `self`/`cls`) are also exempt — fighting the ecosystem costs more than it clarifies. Don't rename for the sake of renaming.

## Instructions

### 1. Ask what role the thing plays

Names encode role. Before naming, classify:
- **Boolean** → reads as a question/state: `isReady`, `hasAccess`, `shouldRetry` (not `flag`, `status`, `check`). Phrase it positively — `isEnabled`, not `isNotDisabled`; negatives double up at the call site (`!isNotReady`)
- **Function** → verb phrase naming the effect: `chargeCard`, `parseWebhook`, `evictStaleSessions` (not `handle`, `process`, `doWork`)
- **Collection** → plural noun: `pendingInvoices` (not `list`, `arr`, `data`)
- **Transformation** → name the *output*, not the act: `cents` not `convert`, `normalizedEmail` not `fixEmail`

### 2. Run the ban list

Reject any name that is, or contains, a filler word unless it's genuinely the most precise term:

`data, info, value, item, obj, thing, stuff, temp, tmp, handle, process, manage(r), do, util(s), helper, misc, common, base, foo, result, response, res, ret, val, x/y/z (outside math/loops)`

For each, ask: "data *about what*? handle *what event*? manager *of what*?" The answer is the real name.

### 3. Make distinct things distinctly named

If two names differ only by a vague suffix (`user` / `userData` / `userInfo`), they are lying about being different. Either they're the same thing (merge the name) or they play different roles (name the role: `requestingUser` vs `targetUser`).

### 4. Match the domain's words

Use the team's and the product's actual vocabulary. If the business says "subscriber," don't invent "memberAccount." If a `CONTEXT.md` or glossary exists, names must match it. Mismatched vocabulary is how two engineers build the same thing twice.

### 5. Length follows scope

- Tiny scope (one-line lambda, tight loop) → short is fine.
- Wide scope (exported symbol, module-level, long-lived) → spell it out. A name read in 50 places earns its letters.

### 6. Propagate the rename completely

A rename isn't done until every reference moves with it. Before applying:
- Grep the whole repo for the old name and every call site, including strings used for dynamic access (reflection, serialized config, route tables, DB columns, API field names).
- Update all of them in one change, or don't rename at all — a half-propagated rename creates two vocabularies for the same thing, which is worse than the original vague name.
- For an exported/public symbol, weigh the blast radius: a rename that ripples through consumers may need a deprecation alias rather than a hard cut. When in doubt, propose and confirm before applying.

## Output format

When proposing renames, present a table so the human can scan and approve:

```
| Current      | Proposed            | Why                                   |
|--------------|---------------------|---------------------------------------|
| data         | pendingInvoices     | it's a list of invoices awaiting send |
| handle()     | retryFailedCharge() | it retries; "handle" hides the effect |
| userInfo     | requestingUser      | distinguishes from targetUser         |
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Type-in-the-name (`userObject`, `nameString`, `itemsArray`) | The type system already knows. The name should add meaning, not repeat it. |
| Comment-as-crutch (`// the list of active users` above `data`) | Move the meaning into the name; delete the comment. |
| Cute or clever names | `Thanos.snap()` is funny once and confusing forever. |
| Renaming without grep | A rename you don't propagate creates two vocabularies. Find every call site. |

## Mental Model

> A name is a one-word comment that can never go stale. If you need a comment to explain a name, the name is wrong.
