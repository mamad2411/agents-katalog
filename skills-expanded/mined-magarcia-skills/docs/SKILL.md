---
name: docs
description: Find and fix repository documentation that a code change made false, including AGENTS.md, README files, docs, ADR references, command examples, APIs, configuration, and environment variables. Use after architectural or interface changes, renames, workflow changes, behavior-preserving refactors, or as the documentation stage between $implement and $ship in $build.
---

# Docs

Gate on the diff: did it change architecture, an API, CLI, configuration, environment variable, build/test/deploy workflow, or the approach the project uses? If not, give one line of reasoning and stop.

1. **Inventory** — Read every applicable `AGENTS.md` and the documentation it references. Inventory root and module READMEs, `docs/`, ADR directories, API specifications, `.env.example` and sample configuration, and in-repo diagrams. If the repository contains `CLAUDE.md`, inspect it as documentation that may also have become stale, not as Codex instruction authority.
2. **Cross-reference** — Use `rg` to search documentation for identifiers, paths, commands, and concepts removed or changed by the diff. Old identifiers are often the best signal because stale documentation still uses them. Give applicable `AGENTS.md` files priority: false commands, structure, or conventions there misdirect future work.
3. **Fix** — Update factual rot in place: commands, paths, names, snippets, configuration examples, and diagram sources. Run examples where feasible. Limit changes to documentation invalidated by the diff; do not rewrite unrelated prose.
4. **Flag** — List decisions that need human authorship and external documentation pages that remain stale. Do not mutate an external documentation system unless the user explicitly placed it in scope.

Report what was updated, confirmed accurate, or flagged.

- Write documentation as current state, without migration-history narration.
- Update the source of generated documentation, never generated output.
- Treat plausible, almost-correct documentation as higher risk than obviously obsolete material.
