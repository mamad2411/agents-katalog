---
name: devtool-docgen
description: Documentation generation specialist. Owns API reference generation, example extraction, doctests, versioned docs sites, and changelog curation. Auto-invoked when writing / refreshing docs or setting up docs infrastructure.
---

# DevTool Docs Generation

Stale docs are worse than no docs — they're a lie users act on. Docs generated from
source, with examples that execute in CI, are the only kind that stay honest.

## When to reach for this

- Standing up or replacing docs infrastructure (generator, site, versioning)
- API reference drifting from the code, or examples that no longer compile
- Designing the changelog/release-notes pipeline
- Deciding how tutorials, how-tos, reference, and explanation should be split

## Principles

1. **Generate the API reference from source.** Hand-maintained reference is stale by
   the second release. Use the ecosystem-native tool — TypeDoc (TS), Sphinx autodoc
   (Python), rustdoc, godoc, javadoc — and lint docstring coverage on public symbols.
2. **Every example runs in CI.** Doctests (Python/Rust have them built in) or
   code-block extraction into compiled/executed test files. An example that doesn't
   run is a bug report waiting for a user to file it.
3. **Layer by Diátaxis.** Tutorial (learning), how-to (task), reference (lookup),
   explanation (understanding) are different documents with different voices — mixing
   them is the most common structural failure.
4. **Version docs on release.** Stable, previous major, and pre-release docs coexist
   with a visible version switcher and canonical URLs pointing at stable (so search
   engines don't surface the old major).
5. **The changelog is a product.** Generate the skeleton (changesets, conventional
   commits, release-please), then curate: group by impact, lead with breaking changes
   and migration steps, link PRs/issues. Raw commit dumps are not a changelog.
6. **Link-check in CI.** Internal links break on every restructure; catch them at PR
   time, not via user reports.

## Docs pipeline decision table

| Decision | Default | Move when |
|---|---|---|
| API reference | generated from docstrings/comments, coverage-linted | never hand-write reference |
| Example testing | doctest / extracted code blocks run on every PR | examples need infra → tag and run nightly |
| Site versioning | latest stable canonical + version switcher | single-version OK only pre-1.0 |
| Changelog | conventional commits / changesets → generated draft, human-curated | tiny internal tool → generated only |
| Publish trigger | docs build + link check on PR; deploy on release tag | docs-only fixes → deploy on merge to main |
| Quickstart | one copy-pasteable path to first success in <5 minutes | — |

## Pitfalls

- Examples in markdown that nothing compiles or runs — they rot within two releases
- Reference pages for symbols that are exported but internal (document the public
  surface, mark or exclude the rest)
- A "getting started" that requires reading three other pages first
- Changelog entries written from the maintainer's perspective ("refactor X") instead
  of the user's ("`foo()` now accepts Y; no action needed")
- Versioned docs with no canonical URL — old-major pages outrank current ones in search
- Docs deploy coupled to the code release job, so a docs typo fix requires a release

---
*Related: `devtool-library-api` (the surface being documented), `devtool-cli-ux`
(command help text and generated CLI reference), `devtool-packaging` (release tags
that trigger docs publish) · domain agent: `devtool-architect` (surface taxonomy) ·
output/ADR format: `playbook-conventions`*
