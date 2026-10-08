# Abstracted Mathlib Review Skill

Distilled only from `skills/SKILL_MASTER.json` and `skills/merged/rule_clusters.json`.
This file keeps only governing rules. Operational detail remains in the source corpora and in `skills/_distill_views/`.

## Mathematical Semantics And Abstraction

- Preserve source mathematics; do not accept an abstraction upgrade that changes the object, the notion, or the domain of validity.
- Start from the best existing owner abstraction in mathlib or the project; typechecking alone is not evidence that the chosen level is right.
- When the source notion is more general than the canonical owner, keep the source-facing notion and add a canonical `toXxx` bridge instead of collapsing it.
- Expose real mathematical objects directly; do not hide them behind `...Data`, `...Package`, chosen witnesses, or implementation wrappers unless that packaging is mathematically essential.
- Prefer invariant, structural, universal, and functorial interfaces over coordinate, presentation, realization, or index-heavy encodings.
- Keep concrete models as specializations or views of an intrinsic interface, not as the public root object.
- Separate core data from auxiliary properties when that sharpens the object and improves reuse.
- Repeated casts, transports, index repair, or bookkeeping in the public API are evidence that the abstraction level is still too low.

## API Ownership And Public Surface

- Put each declaration, instance, and theorem under its natural owner namespace and in the lowest dependency layer where it belongs.
- Reuse canonical declarations directly; wrappers, shadow APIs, and same-shape aliases need real new mathematical content or they should disappear.
- The public API should have one obvious entry point; derived views belong as lemmas, coercions, or `toXxx` bridges rather than competing roots.
- Do not let proof convenience, implementation boundaries, or temporary porting scaffolding determine the public interface.
- Remove redundant public parameters when they can be derived internally; do not keep constructor clutter for the implementation's sake.
- Keep the public surface smaller than the implementation: local helpers stay local, debugging metadata stays private, and reusable vocabulary alone earns an alias.
- If a canonical type expression is already readable, expose it directly instead of naming it with a one-off `abbrev`.
- When a new owner abstraction lands, migrate the nearby obvious call sites in the same change so the codebase stops speaking two dialects.

## Statement Design And Generality

- Use the weakest honest assumptions that make the result true and reusable; stronger hypotheses belong only on lemmas that really need them.
- Generalize along the real mathematical axis, not by threading arbitrary implementation parameters through the statement.
- Remove unused, redundant, or derivable variables and hypotheses instead of letting theorem headers fossilize old proof states.
- Choose statement shapes that downstream rewriting, `simp`, and typeclass search can consume without transport or elaboration scaffolding.
- Prefer canonical normal forms in conclusions and hypotheses so users do not need local bookkeeping to apply the theorem.
- Reuse one strong theorem plus ergonomic bridges instead of cloning trivial special cases under new names.
- When both bundled and unbundled or abstract and concrete consumers matter, provide the general theorem and the minimal companion wrappers both styles need.
- Make names reflect theorem shape faithfully: equivalence, equality, implication, transport, and specialization should be legible from the name.

## Families, Completeness, And Bridges

- Land natural families together: restricted and unrestricted, bundled and unbundled, additive and multiplicative, pointwise and global, local and global.
- Treat missing bridge lemmas as API holes, not as optional follow-up cleanup.
- When a theorem has an obvious dual, converse, symmetry, or transport form that users will immediately need, assess the whole family before merging one fragment.
- Prefer a small complete family over a large pile of disconnected special lemmas.
- When the core shape of a theorem or definition changes, re-audit neighboring declarations and existing call sites that should now follow the new pattern.
- Preserve easy recovery of familiar special cases even after generalizing the core API.
- Add coercions, equivalences, `↔` lemmas, or `toXxx` maps where they are the natural route between adjacent abstractions.
- If a repeated downstream workaround can be eliminated by a bridge once, add the bridge and delete the workaround pattern.

## Proof Architecture And Reuse

- Proof structure should reveal the mathematical idea; tactic accidents and elaboration residue should not dominate the readable shape.
- Remove dead helper facts, no-op rewrites, vestigial branches, and temporary scaffolding once the proof is stable.
- Prefer direct arguments over contradiction, transport, or bookkeeping detours when both are mathematically equivalent.
- Extract helper lemmas to name reusable ideas, not to hide trivial one-off lines.
- After introducing a genuinely reusable lemma, simplify neighboring proofs that manually replay the same argument.
- Keep the main line visually obvious and isolate degenerate, exceptional, or side-condition branches.
- Prefer proof shapes that remain stable under small changes to simp sets, elaboration, or instance search.
- Shorter is better only when it remains more transparent, not merely denser.

## Simplification, Rewriting, And Automation

- Automation should discharge routine work, not supply the semantic content of the argument.
- Before adding tactic layers, fix the missing lemma, missing bridge, bad normal form, or bad theorem shape that made the proof awkward.
- Add `@[simp]` only when a lemma pushes toward a canonical and broadly useful simplification.
- Do not teach `simp` facts that are true but non-terminal, bidirectional, or ambiguous about what counts as simpler.
- Keep rewrite orientation and normal forms consistent across related declarations in the same API family.
- Prefer explicit rewrites, `rw`, and `simpa` when they expose intent more clearly or more stably than ambient automation.
- Repeated `simp; exact`, `erw`, `change`, cast repair, or transport repair is evidence that the surrounding API still needs abstraction work.
- Automation-facing declarations should minimize incidental parameters, casts, transports, and hidden elaboration burdens.

## Naming, Syntax, And Readability

- Naming, namespaces, notation, binder order, and proof surface are part of API quality, not post hoc cosmetics.
- Follow the surrounding mathlib or project naming family before inventing a new local scheme.
- Keep related declarations aligned in variable order, argument polarity, namespace placement, and bridge naming so users can predict the next lemma.
- Prefer the shortest unambiguous form that still reads idiomatically; avoid unnecessary qualification and elaboration scaffolding once the code is stable.
- Use stable descriptive names over placeholders, numeric suffixes, or one-off abbreviations, and keep public names readable as mathematics rather than implementation history.
- Treat surface syntax choices as review-worthy only when they affect semantics, maintainability, or house style.
- Write code in the local dialect mathlib expects, not a custom dialect that forces readers to decode each file anew.
- Use sections, local notation, and opened namespaces to clarify structure, not to obscure ownership or create ambiguous public names.

## Documentation, Diagnostics, And Compatibility

- Document the mathematical meaning and intended use first; the type signature already carries the raw syntax.
- Comments should explain non-obvious intent, invariants, workarounds, or migration obligations, not narrate routine code.
- Keep module docs, declaration docs, examples, and cross-references synchronized with the actual API after refactors.
- When a workaround, deprecation, or compatibility shim remains, explain the stable reason it still exists.
- Preserve and correctly update live compatibility metadata such as `#align`, porting notes, and provenance markers until the underlying migration story truly changes.
- Remove stale comments, resolved TODOs, obsolete porting notes, and dead suppressions promptly once they stop being true.
- Diagnostics should name the exact local failure and expected correction, not merely echo a parser or elaborator symptom.
- When a reviewer will naturally ask "why is this shape necessary?", answer that in the code, docs, or PR text instead of making them reconstruct it.

## Dependencies, Tooling, And Performance

- Imports and module placement are part of the design: keep dependencies as light and local as the mathematics allows.
- After moving, generalizing, or deleting code, re-audit imports, module boundaries, and compatibility aliases in the same change.
- Prefer reusable pure utilities and shared helpers over duplicated script-local logic, shell-fragile glue, or ad hoc IO wrappers.
- Meta code and tooling should preserve goal state, context, and typed structure explicitly instead of relying on stringly conventions.
- Fix performance by removing wasted work, elaboration friction, and duplicated computation before raising budgets, timeouts, or heartbeats.
- Keep debug tracing in trace infrastructure and reserve user-facing errors for actual semantic failures.
- Teach tooling about autogenerated declarations, formatting contracts, and expected syntactic forms instead of piling on manual exceptions.
- Remove linter suppressions, temporary imports, and workaround flags only after verifying that the underlying issue is gone in the active toolchain.

## Review Scope And Change Hygiene

- Each diff should carry one coherent mathematical or engineering idea whenever possible.
- Explain why the change improves the codebase, not only what text was edited.
- Do not bury semantic changes inside large cosmetic rewrites or unrelated modernization.
- Review and clean the full local pattern, not only the one line or file that first triggered the comment.
- A bug fix is not finished without a regression test that exercises the broken path, and user-visible output changes deserve message-level tests.
- Before review, remove accidental whitespace churn, editor noise, stale experiments, and other unintentional edits.
- A change is not complete until obvious downstream call sites, docs, imports, and compatibility surfaces have been revisited.
- The best refinement reduces surface area, clarifies intent, and increases reuse at the same time.
