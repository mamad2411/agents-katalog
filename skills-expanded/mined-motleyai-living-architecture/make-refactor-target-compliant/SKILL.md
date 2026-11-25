---
name: make-refactor-target-compliant
description: Use BEFORE renaming a symbol/attribute (Python or TypeScript) to make its blast radius verifiable — type the code that might reference it (untyped params/vars that could hold the class, classes with matching attribute names, overrides not marked as such) so the post-rename type-check gate is sound.
---

**Preflight:** run `dr-doctor --plugin <this skill's base directory>` once per session before using any `dr-*` command; if it fails, stop and show the user its output.

# Make a refactor's blast radius compliant

A rename is only provable over code the type checker can resolve. This closes
the blind spots first, so the `dr:deterministic-refactor` gate afterwards is sound.
The idioms for each language are in
`<this skill's base directory>/../../languages/<language>.md`.

## Steps

1. **Identify the target:** the symbol, and for a member rename the attribute
   NAME and its owning class.
2. **Enumerate blind spots:**
   - `dr-compliance --select attr-blindspot,string-blindspot --attr NAME <repo>` (one `--attr`
     per name a rename map renames) → `x.NAME`, `getattr(x, "NAME")` and the
     like where `x` is untyped. Each names the receiver to type.
   - A `dr-refactor` dry-run of the rename lists the stand-ins: classes outside
     the hierarchy that declare NAME. Make a real implementation a subclass or
     a `Protocol` implementation now, or classify it at the rename (`--with` /
     `--without`, see `dr:deterministic-refactor`).
3. **Make them resolvable (do NOT rename yet):**
   - Type the flagged parameters/variables with the owning class (or its
     interface/protocol); type the class's own attributes.
   - Mark the overrides in the hierarchy.
   - Type any test doubles of the class (`dr-mock-lint`).
4. **Re-check until the blast radius is typed:**
   - the same `dr-compliance --select attr-blindspot,string-blindspot` command reports nothing;
   - `dr-typecheck` shows no new errors over the touched files.
5. **Then run `dr:deterministic-refactor`.** Every real reference is now
   type-visible; what is left is a string the rename lists as a `leftover`
   or the language doc names.

The guarantee still comes from the type checker after the rename; this
skill's job is to shrink the checker's untyped surface over the blast radius
to zero.
