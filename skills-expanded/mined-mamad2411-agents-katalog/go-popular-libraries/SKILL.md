---
name: go-popular-libraries
description: "Go library selection — choose the simplest production-ready library for the task: stdlib-first evaluation, maturity and license checks, vetted category catalogs, dependency-footprint assessment, and when to decline a dependency. Use when asked for library recommendations, comparing alternatives, or adding a new dependency."
license: MIT
---

# Go Popular Libraries

**Leading word: choose.** Recommending a library is a choice with a long-term maintenance cost. The discipline: **choose** the simplest production-ready option — check the standard library first, vet maturity and license, weigh the dependency footprint — and be ready to recommend no library at all.

## Steps — recommend

1. **Assess the requirement first.** Understand the use case, performance needs, and constraints before naming any library.

   *Done when: the use case, performance needs, and constraints are stated before a library is named.*

2. **Check the standard library.** Determine whether stdlib covers the use case — including new and experimental packages; only reach for an external library when stdlib falls short.

   *Done when: stdlib coverage is either identified or explicitly ruled out.*

3. **Recommend from vetted catalogs.** Prefer the category and tool catalogs below; consult awesome-go for more; never suggest an abandoned or unmaintained library — flag it and ask the developer first.

   *Done when: every recommendation is mature, licensed, maintained, and vetted — or explicitly user-approved.*

4. **Assess the dependency footprint.** More dependencies mean more attack surface and maintenance burden; prefer the option with fewer transitive deps for simple needs.

   *Done when: the recommendation's own dependency footprint is assessed and justified.*

5. **Pick the simplest option.** Choose the simplest library that meets the requirements — over-engineering with a complex library is the failure mode, and the best library is often no library at all.

   *Done when: the chosen option is the simplest that meets requirements, with a reason.*

## Reference

### Prioritization

When recommending, rank: production-readiness (mature, well-maintained, active community) → simplicity (idiomatic Go) → performance (leverages concurrency and compiled speed) → standard-library-first (only external libs that add clear value).

### Catalogs

- [Standard Library — New & Experimental](./references/stdlib.md) — v2 packages, promoted x/exp packages, golang.org/x extensions
- [Libraries by Category](./references/libraries.md) — vetted third-party libraries for web, database, testing, logging, messaging, and more
- [Development Tools](./references/tools.md) — debugging, linting, testing, and dependency management tools
- <https://github.com/avelino/awesome-go> — wider community catalog

## Watch for

| Mistake | Fix |
| --- | --- |
| Over-engineering simple problems with complex libraries | Simplest option that meets requirements |
| Wrapper libraries that add no value | Use the standard library directly |
| Abandoned or unmaintained libraries | Check maintenance status; ask the developer first |
| Large dependency footprint for simple needs | Assess footprint; prefer fewer transitive deps |
| Ignoring standard library alternatives | Check stdlib before recommending external |

## Cross-references

- → See `go-dependency-management` for adding, auditing, and managing dependencies
- → See `samber-do` for samber/do dependency injection details
- → See `samber-oops` for samber/oops error handling details
- → See `go-stretchr-testify` for testify testing details
- → See `go-grpc` for gRPC implementation details
