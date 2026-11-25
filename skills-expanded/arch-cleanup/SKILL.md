---
name: arch-cleanup
description: Use to carve or tighten ONE architecture boundary in a repo with the living-architecture setup — take a coherent batch of grandfathered `#legacy` arrows (or extract a new node), refactor them away with verified moves (deterministic-refactor), and shrink the legacy-arrow baseline monotonically. Behaviour-preserving by definition; one slice = one branch/PR.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory> --require-config` once per session before using any `la-*` or `dr-*` command. If it reports the missing-config finding (the one naming `/la:init`), run the fast path of the `la:init` skill, then re-run this preflight; stop and show the user its output on anything it still reports, or on any other failure.

# Carve one boundary slice

A slice moves code until a batch of grandfathered edges dies, with a
deterministic gate proving nothing dangles. It is behaviour-preserving: no new
behaviour, no new tests, no OpenSpec spec deltas. The legacy-arrow ratchet plus
the green suite ARE the spec, so the /la:pr stage flow does not apply — but
each slice still gets its own branch and PR, and its own issue when the repo has a tracker.

## Procedure

1. **Pick the slice.** List the model's `#legacy` arrows (their count is
   `legacy_arrows.baseline` in `index.yaml`); propose a coherent batch — one
   importer module, one edge family (e.g. `python.core -> python.sql.render`),
   or one node extraction. Arrows live inside their language root, so a slice
   stays within one language.
   Keep it ≤ ~10 edges. Confirm the choice with the user.
2. **Read the touched elements' arc42 (and their ancestors') + LikeC4 view.** The principles decide the
   resolution per edge:
   - **move down** — the imported thing is a lower-level utility on the wrong
     side → `dr-refactor move-symbol` / `move-module` into the lower package;
   - **move up** — the importing code doesn't belong in this node → move it
     out;
   - **invert** — both sides are placed right → introduce a
     Protocol/callback in the lower layer (a real code change, not a pure
     move — keep it minimal and fully typed);
   - **legitimize** — the edge is actually correct → change the model and
     arc42 instead. Requires the user's explicit OK.

   Present the per-edge resolution table BEFORE mutating anything — this is a
   nontrivial design decision, the one permitted pause.
3. **Baseline the gate:** `la-typecheck` green (the type checker against its
   committed baseline, in the project env) — if it prints "nothing to check",
   STOP and tell the user: without a type check the moves cannot be verified,
   so offer to set one up (`commands.typecheck` and `la-typecheck
   --write-baseline`) first; `la-arch-check` green; the repo's test command (`la-config get commands.test`; if unset, the repo's documented full non-integration suite) green.
4. **Execute the moves** via the `la:deterministic-refactor` skill (dry-run →
   apply → format). The refactor's project scope must include the tests so
   test imports are rewritten too. New destination packages are created first
   (destinations must exist before moving; the language doc says what a new
   package needs).
5. **Move gate — done only when ALL pass:**
   - `la-typecheck`: **no new errors** vs baseline. A stale `from old import X`
     or `old_mod.X` surfaces here even in untyped code — module members are
     statically resolvable without annotations;
   - delete the slice's now-dead `#legacy` arrows from the model and lower
     `legacy_arrows.baseline` in `index.yaml` to match; `la-arch-check`
     green (it fails if the count, or any measured edge, disagrees with the model);
   - the repo's test command (`la-config get commands.test`; if unset, the repo's documented full non-integration suite) green;
   - grep the string-only refs no static tool sees, for every moved dotted
     path: `patch("...")`, `importlib`, `getattr(`, `__all__`, pyproject
     entry points/scripts, config files, docs.
6. **Sync views & arc42:** adjust views if the node shape changed (an
   extracted node is a child of its language root with its own
   `metadata { package '…' }`; a nested element maps to `<package>.<path>` by
   convention and may carry only `specs` metadata; views stay `of <root>`; an element whose id changed takes its arc42
   file along as `architecture/<new id>.arc42.md`); re-validate
   the model (`la-arch-diagrams` refreshes the embedded view diagrams); update
   arc42 rationale/principles if the slice established a new
   rule — ideally tagged `[enforced: <the check/test that now holds>]`.
7. Review the diff; the user commits. One slice per PR; never mix in
   behaviour changes.

## When is full compliance needed?

Full deterministic-refactor compliance (annotations everywhere, spec-bound
mocks, `@typing.override`) is **not** required for pure moves: every reference
to a moved module-level symbol resolves through a module namespace the checker
can see unannotated, and a stale `patch("old.path")` fails loudly at test
runtime because `patch` imports its target from the string. The blind spots
that remain are string refs in tests that don't execute — covered by the grep
in step 5.

The moment a slice must **rename** an attribute or method (e.g. while
inverting a dependency), that guarantee needs typed receivers: run
`la:make-refactor-target-compliant` on the blast radius first, then
`la:deterministic-refactor` for the rename.
