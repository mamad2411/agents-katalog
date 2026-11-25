---
name: library-selection
description: Compares candidate libraries on maintenance, fit, size and risk, then recommends one with evidence instead of picking whatever is popular.
---

# Library selection

Recommend with evidence. Do not install anything while comparing.

## Steps

1. Write the requirements: what the library must do, the runtime and version it must support, license limits, bundle or install size limits, and what the project already uses that could do part of the job. Check the lockfile first: an existing dependency may already cover it.
2. Shortlist three to five candidates, including "write it ourselves" when the need is small. Use the registry, the official docs and the repository, not blog rankings.
3. For each candidate collect, with a link or command for each fact: latest release date and release cadence, last commit, open issues and how fast they are answered, number of maintainers, license, install size and dependency count, TypeScript types or equivalent, and known advisories (`npm audit`, `pip-audit`, the GitHub advisory database).
4. Test fit. In a scratch directory, write the smallest snippet that does your hardest use case with each finalist. Note how awkward it was, and any behavior that surprised you.
5. Judge risk: single maintainer, a major rewrite in progress, heavy transitive tree, native build steps, or API that leaks into your code and makes switching costly.
6. Score the finalists against the requirements in a table, then recommend one. State the deciding factor and what evidence would change the decision.
7. Give the adoption plan: pinned version, where to wrap it behind a thin module so it can be replaced, and the first usage to migrate.

## Rules

- Never recommend on popularity alone.
- Never run install scripts from an unvetted package on the real project.
- Mark any fact you could not verify.

## Report

The comparison table, the recommendation with its deciding factor, and the adoption plan.
