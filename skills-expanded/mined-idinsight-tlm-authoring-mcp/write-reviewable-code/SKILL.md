---
name: write-reviewable-code
description: Write and refactor code so a human reviewer grasps it on the first read — descriptive names, one idea per line, small readable functions. Applies whenever writing or editing code; also use when asked to make code more readable, reviewable, or human-friendly, or to clean up terse/dense code.
---

# Write Code a Human Can Review

Optimize the code you write for the **reviewer**, not the compiler. The next person to read a diff — often reviewing on a small screen, with limited context — should follow each line without pausing to decode it. Terseness that saves you keystrokes costs them minutes.

## The test every line must pass

> A reviewer reading this line in a diff, without running it, knows what it does and why.

If a line needs mental unpacking — expanding a cryptic name, splitting a chained one-liner in their head, guessing what an intermediate value holds — it fails. Fix the name, split the line, or add a named step. This test is the point; the rules below serve it.

## Name things for the reader (the #1 fix)

Single letters and cryptic abbreviations force the reviewer to hold a translation table in their head. The reader should never have to remember that `g` is the graph and `a` is the arguments.

| ❌ Terse — reader must decode | ✅ Descriptive — reads as English |
|---|---|
| `apply: (base, a) => {` | `apply: (base, args) => {` |
| `let g = base;` | `let graph = base;` |
| `const edge = a.via ?? containmentEdgeFor(labelOf(node));` | `const edgeType = args.via ?? containmentEdgeFor(labelOf(node));` |
| `for (const e of es) {` | `for (const edgeId of parentEdgeIds) {` |
| `const p = nextPosition(g, a.toParentId, edge);` | `const position = nextPosition(graph, args.toParentId, edgeType);` |

Exceptions — short names are fine where convention makes them unambiguous: a loop index `i`, a coordinate `x`/`y`, a math variable matching the domain, or a one-line lambda param whose type is obvious (`items.map(item => item.id)`). The bar is *reader clarity*, not length — `id` beats `identifier`.

## One idea per line

A line that does three things makes the reviewer parse three things and guess whether the ordering matters. Give each step its own line and, when it earns one, its own name.

```ts
// ❌ Three operations fused — reader untangles detach, compute, attach, reposition
for (const edgeId of parentEdgeIds(g, a.nodeId, edge)) g = unlinkNodes.apply(g, { edgeId });
g = linkNodes.apply(g, { edgeType: edge, fromId: a.toParentId, toId: a.nodeId, properties: { orderInParent: p } });
g = { nodes: setPosition(g.nodes, a.nodeId, p), edges: g.edges };
```

```ts
// ✅ Each step stands alone; a named intermediate says what the value is
let graph = base;

// Detach the node from every current parent on this axis before re-attaching.
for (const edgeId of parentEdgeIds(graph, args.nodeId, edgeType)) {
  graph = unlinkNodes.apply(graph, { edgeId });
}

const position = args.position ?? nextPosition(graph, args.toParentId, edgeType);
graph = linkNodes.apply(graph, {
  edgeType,
  fromId: args.toParentId,
  toId: args.nodeId,
  properties: { orderInParent: position },
});

// Keep the node's own position field consistent with its new slot.
const nodesWithPosition = setPosition(graph.nodes, args.nodeId, position);
graph = { nodes: nodesWithPosition, edges: graph.edges };
```

Also: always brace control-flow bodies (no bare `if (...) return x;` on one line — the guard is easy to miss in review), and break long argument lists / object literals across lines.

## Rules

1. **Descriptive names over terse ones.** Name variables, params, and functions for what they hold or do. No single letters for domain concepts (`g`, `a`, `n`), no mystery abbreviations. See the exceptions above.
2. **One idea per line.** Don't chain unrelated operations. Introduce a named intermediate when it makes the next line readable — a good variable name is free documentation.
3. **Avoid nested function calls.** Don't feed one call's result straight into another (`containmentEdgeFor(labelOf(node))`) — the reader parses it inside-out. Bind the inner result to a named variable first (`const label = labelOf(node); containmentEdgeFor(label)`); the name says what the value is and the diff reads left-to-right. Exception: a single, obvious wrap where the name would just restate the call (`Object.keys(counts).length`, `new Date(timestamp)`).
4. **Small, single-purpose functions.** If a function needs a "this part does X, then Y" mental split, that's two functions. Prefer early returns over deep nesting.
5. **Brace all control flow; break long lines.** No one-line `if`/`for` bodies. Wrap long calls and object literals so each argument is on its own line.
6. **Reveal structure with whitespace.** Group related lines into paragraphs with a blank line between phases (detach → compute → attach). A wall of statements hides the shape.
7. **Match the surrounding code, toward the readable end.** Follow the file's existing conventions (per CLAUDE.md), but when the local style is itself terse, lean to the clearer end — don't add a *new* single-letter variable just because a neighbor has one.
8. **Comments are a separate concern.** This skill is about the code itself. For comment quality, the `comment-code` skill applies — the two compose.

## Process (when refactoring existing code for review)

1. Read the target. Behavior stays identical — this is a readability refactor, not a rewrite.
2. Find the lines that fail the one-read test: cryptic names, fused operations, unbraced guards, long unwrapped expressions.
3. Rename to descriptive names; split fused lines and name the intermediates; brace and wrap.
4. Add blank lines between logical phases so the structure is visible.
5. Report what you changed and confirm behavior is unchanged, so the judgment is reviewable.

## Anti-patterns to fix on sight

- Single-letter or abbreviated names for domain concepts (`g` for a graph, `a` for arguments, `res`, `tmp`).
- Multiple operations chained onto one line to save vertical space.
- Nested function calls the reader has to parse inside-out (`f(g(h(x)))`) instead of named steps.
- Bare one-line `if (...) return;` / `for (...) doThing();` where the body is easy to overlook.
- Long argument lists or object literals crammed on one line.
- Deep nesting that an early return would flatten.
- A dense wall of statements with no blank lines marking the phases.
