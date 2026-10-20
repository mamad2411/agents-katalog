---
name: sveltekit-advanced-routing
description: Use when implementing SvelteKit advanced routing features including route groups, optional parameters, rest parameters, parameter matchers, and layout inheritance control.
---

# SvelteKit Advanced Routing

## Specialization

Expert guidance for SvelteKit advanced routing features. Covers route groups `(group)`, optional parameters `[[param]]`, rest parameters `[...rest]`, parameter matchers, layout inheritance reset, and designing URL structures that are clean, flexible, and maintainable.

## Trigger Conditions

- Grouping routes for shared layout without adding a URL segment.
- Implementing optional URL segments or catch-all routes.
- Constraining parameter values using matchers.
- Breaking out of an inherited layout for a specific route subtree.
- Designing complex URL hierarchies with multiple layout zones (for example public vs. authenticated sections).

## Scope Boundaries

In scope:

- Route groups: `(group)` folders that do not emit URL segments but share a layout.
- Optional parameters: `[[param]]` — the segment may or may not be present.
- Rest parameters: `[...path]` — zero or more segments captured as an array or string.
- Parameter matchers: `src/params/<matcher>.ts` with `match()` export.
- Layout inheritance reset: `+layout@.svelte` and `+layout@group.svelte` syntax.
- Combining groups, optional params, and rest params in one route tree.
- Priority rules when multiple routes could match the same URL.

Out of scope:

- Basic `[param]` routing (covered by `sveltekit-routing`).
- API route handlers (`+server.ts`).
- Adapter-specific routing behaviour (covered by `sveltekit-adapters`).
- Error pages (covered by `sveltekit-errors`).

## Inputs

- Desired URL structures and their segment variability.
- Layout zone requirements (public, authenticated, admin, etc.).
- Parameter value constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Route tree design | Annotated `src/routes/` directory map with group and param types labelled |
| Matcher implementations | `src/params/<matcher>.ts` files with `match()` exports |
| Layout reset map | Which routes reset layout and to which ancestor group |
| Conflict resolution notes | Priority rationale where multiple routes could match |
| Advanced routing checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Understand one advanced feature | Single group or optional param renders correctly |
| L2 Practical Delivery | Multi-zone app with groups, optional params, and matchers | All URL patterns resolve; layout zones are correct |
| L3 Specialist Hardening | Conflict-free route tree with documented priority rules | No ambiguous matches; matcher unit tests pass |
| L4 Expert Standardisation | Advanced routing conventions for a project | Route design guide, matcher library, and layout zone policy documented |

## Feature Reference

### Route Groups `(group)`

- Folder name wrapped in parentheses: `(app)`, `(auth)`, `(marketing)`.
- Does not appear in the URL.
- Can have its own `+layout.svelte` shared by all nested routes.
- Primary use: separating authenticated routes from public routes without URL pollution.

### Optional Parameters `[[param]]`

- The segment may be present or absent; both URLs resolve to the same route.
- `params.param` is `undefined` when the segment is absent.
- Useful for locale prefixes (`[[lang]]/...`) or optional view modes.

### Rest Parameters `[...rest]`

- Captures zero or more segments.
- `params.rest` is the raw string of the captured path.
- Must be the last segment in a route; cannot be followed by other segments.
- Use for catch-all routes or proxy-like path forwarding.

### Parameter Matchers

- `src/params/<name>.ts` exports `match(value: string): boolean`.
- Applied in route definition as `[param=name]`.
- Causes the route to be skipped when `match` returns `false`, allowing fallback to the next matching route.
- Keep matchers pure and fast; do not perform I/O inside `match`.

### Layout Reset

- `+layout@.svelte` resets to the root layout.
- `+layout@(group).svelte` resets to the named group's layout.
- Useful when a sub-route needs a completely different shell (for example, a fullscreen modal or embedded view).

## Workflow

1. Map all URL patterns and identify which segments are fixed, dynamic, optional, or catch-all.
2. Identify layout zones and assign each zone to a route group folder.
3. Implement `(group)` folders; add `+layout.svelte` to each group that shares a layout.
4. Add `[[param]]` folders for optional segments; handle the `undefined` case in load functions.
5. Add `[...rest]` for catch-all routes; ensure the segment is always last in the path.
6. Create matchers in `src/params/` for parameters requiring value constraints; test each `match()` function.
7. Apply `[param=matcher]` syntax in the route folder name.
8. Identify any layout resets required; add `+layout@(group).svelte` or `+layout@.svelte`.
9. Verify route priority: specific routes beat optional and rest routes; document any ties.
10. Run the advanced routing checklist.

## Advanced Routing Checklist

- [ ] Route groups use `(group)` naming; no URL segment is emitted.
- [ ] Optional params handle the absent case (`undefined`) in all load functions and components.
- [ ] Rest params are the last segment in their route; no trailing fixed segments.
- [ ] Every matcher in `src/params/` is pure (no I/O, no side effects).
- [ ] Layout resets are intentional and documented; no accidental `@` suffix.
- [ ] No two routes produce ambiguous matches for the same URL without an explicit priority rationale.
- [ ] Matcher unit tests exist for non-trivial `match()` functions.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Route groups | Feature Reference + Workflow step 3 |
| Optional parameters | Feature Reference + Workflow step 4 |
| Rest parameters | Feature Reference + Workflow step 5 |
| Matchers | Feature Reference + Workflow steps 6–7 |
| Layout reset | Feature Reference + Workflow step 8 |
| Priority resolution | Workflow step 9 |
| Quality validation | Advanced Routing Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
