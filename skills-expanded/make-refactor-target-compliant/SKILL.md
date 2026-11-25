---
name: make-refactor-target-compliant
description: Use BEFORE renaming a symbol/attribute (Python or TypeScript) to make its blast radius verifiable — type the code that might reference it (untyped params/vars that could hold the class, classes with matching attribute names, overrides not marked as such) so the post-rename type-check gate is sound.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Make a refactor's blast radius compliant

A rename is only provable over code the type checker can resolve. This closes
the blind spots first, so the `la:deterministic-refactor` gate afterwards is sound.
The idioms for each language are in
`<this skill's base directory>/../../languages/<language>.md`.

## Steps

1. **Identify the target:** the symbol, and for a member rename the attribute
   NAME and its owning class.
2. **Enumerate blind spots (checking machinery):**
   - `dr-compliance --attr NAME <repo>` → `attr-blindspot` sites: `x.NAME` where
     `x` is untyped. Each names the receiver to type.
   - LSP `workspaceSymbol` / `findReferences` on the class and on NAME to map
     the real reference set; compare against what the checker resolves today.
   - Grep `\.NAME\b` for accesses on receivers the checker treats as untyped
     (untyped locals, results of untyped calls) — the "right-looking" names.
3. **Make them resolvable (do NOT rename yet):**
   - Type the flagged parameters/variables with the owning class (or its
     interface/protocol); type the class's own attributes.
   - Mark the overrides in the hierarchy.
   - Type any test doubles of the class (`dr-mock-lint`).
4. **Re-check until the blast radius is typed:**
   - `dr-compliance --attr NAME <repo>` reports no `attr-blindspot`;
   - `la-typecheck` shows no new errors over the touched files.
5. **Then run `la:deterministic-refactor`.** Every real reference is now
   type-visible; anything left is a genuinely dynamic string reference, which
   that skill's grep step catches.

The `attr-blindspot` report and the `\.NAME\b` grep are heuristics for *finding*
candidates. The guarantee still comes from the type checker after the rename —
this skill's job is to shrink the checker's untyped surface over the blast
radius to zero.
