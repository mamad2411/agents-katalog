---
name: agent-skill-kit-dependency-resolver
description: Resolve and topologically sort skill dependencies, enforce the spec §3.3 inversion rule (project→app→team→org), warn on unpinned versions, and fail-closed on incompatible range conflicts. Use when the user asks to check skill dependencies, sort skills by build order, detect cycles, or audit skill version pinning.
tier: org
license: Apache-2.0
compatibility: requires `skills-ref` CLI; reads SKILL.md files only — no network
---

# Agent Skill Dependency Resolver

Wraps the `skills-ref deps` CLI. Walks a skill root, builds the dependency graph, runs DFS toposort, and reports order, cycles, inversions, unpinned warnings, and version-range conflicts.

## When to use

- "Sort these skills in build order"
- "Are there any dependency cycles in my skills tree?"
- "Does any skill violate the org→team→app→project inversion rule?"
- "Are all my skill dependencies pinned?"
- "Two skills disagree on a dependency version — show me the conflict"

## Invocation

`skills-ref deps <root> [--format json|human] [--strict] [--extra-tiers a,b,c]`

## Output sections

| Section      | Meaning                                                              |
| ------------ | -------------------------------------------------------------------- |
| `order`      | Topological order — earlier skills build first.                      |
| `cycles`     | Each cycle as a list of names forming the closed walk.               |
| `missing`    | In-repo dependencies whose target skill does not exist in the tree.  |
| `inversions` | Edges where `from.tier < to.tier` (forbidden by §3.3).               |
| `conflicts`  | `E020_CONFLICTING_RANGES` — two callers want incompatible ranges.    |
| `unpinned`   | `W020_UNPINNED_DEPENDENCY` — in-repo dep with no version pin.        |

## Exit codes

| Code | Meaning                                              |
| ---- | ---------------------------------------------------- |
| 0    | clean                                                |
| 1    | cycle, inversion, or conflict present                |
| 2    | missing in-repo dependency target (or `--strict` warns) |

## Tier-rank table

The §3.3 inversion check uses a numeric rank table — a skill at rank R may only depend on skills at rank ≤ R:

| Tier      | Rank |
| --------- | ---- |
| company   | -2   |
| enterprise| -1   |
| org       | 0    |
| team      | 1    |
| app / application | 2 |
| project   | 3    |

Cross-repo edges are not ranked (the remote skill's tier is unknown without network access).

## Reference

The resolver is implemented twice — `.agents/skills/agent-skill-kit-commons/packages/mjs/` and `.agents/skills/agent-skill-kit-commons/packages/py/`. Both share the fixture suite under `.agents/skills/agent-skill-kit-commons/fixtures/deps/` and the cross-runtime parity harness.
