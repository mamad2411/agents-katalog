---
name: comment-code
description: Refactor and add concise, human-first comments to code while keeping architecture in design docs. Use when asked to comment code, add/clean up comments, write docstrings, improve code readability, or strip bloated/academic/outdated comments — for a file, a diff, or a specific code block.
---

# Code Commenting Directive

Write comments a developer **grasps in one read** — concrete, local, immediately useful — then stop. Do not alter executable behavior.

## The test every comment must pass

> Someone opening this file for the first time understands the comment **in one read, with no other tab open and no design-doc lookup.**

If it needs a second read, domain background, or context from elsewhere to parse — rewrite it concretely or delete it. This test is the whole point; the rules below serve it.

## Make it concrete (the #1 fix for a vague comment)

The most common failure is **abstraction**: the comment restates a *property* ("subject-agnostic ordering", "derives identity from the graph") instead of naming a *case the reader can picture*. Ground every non-trivial comment in something specific — a real value, a real caller, a concrete `e.g.`, or the exact thing that breaks. **Lead with the concrete example, then generalize** — not the reverse.

| ❌ Abstract — restates the property | ✅ Concrete — names the case |
|---|---|
| `// derives the node identity from the graph` | `// copy an existing Activity node's shape so a new Activity matches it` |
| `// enforces transactional idempotency` | `// stops a double charge if the user double-clicks Checkout` |
| `// handles the boundary condition` | `// empty list → return 0 (don't divide by length)` |
| `// mirror kept for faithful re-export` | `// maths stores order in BOTH raw.position AND raw.metadata.order — write both` |
| `// guard against invalid state` | `// apply() runs before validate(), so a bad id must return base, not throw` |

Quick gut-check: if the comment could be pasted onto a different function and still sound true, it's too abstract.

## Comment the trip hazards, not everything

Skim the code and find the **20% of lines a newcomer would stumble on** — the surprising default, the ordering dependency, the guard that looks pointless, the workaround, the off-by-one. Comment *those*. Leave self-explanatory code bare; a comment on obvious code is noise that hides the signal.

## Rules

1. **Explain WHY, not WHAT.** Never narrate syntax (`// increment i`). Explain intent, edge cases, gotchas, and workarounds — the stuff the code itself can't say.
2. **Comments are local; architecture goes in docs.** Keep comments about *this* code's execution and gotchas. When an explanation needs system-wide design context or the history of a refactor, cut it and point to a Design Doc / ADR / README (`// full rationale: docs/design-notes/x.md`). Don't paste the design doc into the header.
3. **Plain developer language.** Direct and grounded. No academic or jargon-dense phrasing when a concrete sentence works.
4. **Concise interface docstrings.** For public interfaces, a standard docstring (JSDoc/PEP 257/GoDoc/Rustdoc): params, return, side effects, errors thrown. No filler.
5. **High signal-to-noise.** Brief. Delete dead code and stale/obsolete comments. TODOs as `// TODO(username): description`.
6. **Light touch — minimize churn.** A comment that already passes the one-read test stays as-is. Only rewrite what's genuinely bloated, abstract, wrong, or stale. Don't reword good comments just to touch them.
7. **Top-of-file headers use a block comment.** The file overview goes in ONE block comment (`/* … */` in C/JS/TS/Go/Rust/CSS, `""" … """` in Python, `=begin/=end` in Ruby) — a title line, then the concrete "what this file is + why", then any doc pointer. Not a stack of `//` lines. Inline and per-declaration comments stay in the language's line/doc form.

   ```ts
   /*
    * <module> · <one-line title>
    *
    * <concrete "what + why", one-read>. Full rationale: docs/design-notes/x.md.
    */
   ```

## Process

1. Read the target file/block.
2. List the trip-hazard lines (the non-obvious ones) and, briefly, why each is confusing — this is what you'll comment.
3. For each: write the shortest comment that names the concrete case and passes the one-read test.
4. Trim existing comments that are abstract, bloated, stale, or duplicate the code; move system-design prose to a doc pointer.
5. Apply the edits (comments only). Report what you commented and why, so the judgment is visible.

## Anti-patterns to strip on sight

- Abstract restatement with no concrete case ("ensures consistency", "handles the edge case").
- Restating the code (`// loop over items`).
- A paragraph of architecture/refactor history in a header — belongs in a doc.
- Stale comments describing code that changed.
- Redundant docstrings that repeat the signature with no added meaning.
