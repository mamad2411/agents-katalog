---
name: agents-md-sync
description: "Prune and route AGENTS.md trees for durable, high-signal context."
---

# Maintain agent guidance

Use this skill when the root or nested `AGENTS.md` tree may have drifted,
grown, or started constraining agents unnecessarily. The goal is not to
document the whole repository. It is to keep inherited context small,
durable, and useful at every scope.

## Place context deliberately

Before adding guidance, classify it:

| Destination | Admission test |
|---|---|
| Root `AGENTS.md` | Broadly applicable, non-obvious, durable, and costly when missed |
| Scoped `AGENTS.md` | The same, but limited to one subtree |
| Skill | A workflow loaded for a recognizable task |
| Existing docs or source | Detailed reference material or implementation truth |
| Nowhere | Generic advice or facts an agent can discover cheaply |

Prefer the narrowest destination. Do not repeat the same instruction at
multiple levels.

## Seed scopes sparingly

A stable, major subtree may have a stub `AGENTS.md` before it has local
guidance. A stub provides an obvious extension point and states only that the
area currently adds no instructions beyond its parent. Do not copy root rules
into it.

Seed area boundaries, not every package. Replace a stub only when guidance
passes the same admission test as any other scoped instruction.

## Audit procedure

1. Inventory the root and nested guidance tree. Read the affected guide, its
   parents, and its children fully; inspect their Git diff and relevant
   history. Use commit history to find likely drift, not as a requirement to
   summarize every intervening commit.
2. Check concrete claims against their owning source, manifest, tests, or
   official dependency contract. Distinguish shipped behavior from plans.
3. Identify content that is duplicated, readily discoverable, local to one
   area, task-specific, temporary, ideological, or phrased more absolutely
   than the underlying risk requires.
4. Remove obsolete context. Move local guidance to a scoped guide and
   workflows to skills. Link to detailed references rather than compressing
   their contents into a parent guide. Leave intentional stubs free of local
   rules.
5. Add new guidance only when a recurring or high-cost failure cannot be
   prevented more precisely by code, tests, schemas, or tooling. Place it at
   the narrowest stable scope.
6. Read the result as one instruction set. Resolve overlap and conflicts, and
   prefer clear outcomes over prescribed agent process.

## Editing principles

- Prefer deletion and routing over denser prose. A soft size target can prompt
  review, but do not optimize for a hard line count.
- Hard language is appropriate for security, destructive operations, data
  isolation, provenance, authentication, and publish integrity. Elsewhere,
  preserve room for task context and engineering judgment.
- Specs, issues, PRs, mockups, tests, and other repositories can all be useful
  references. Do not present planned behavior as shipped, and prefer
  executable or source-backed evidence for current contracts.
- Avoid freshness dates that imply more verification than Git history proves.
- Keep `AGENTS.md` canonical and preserve the `CLAUDE.md` symlink.

## Finish

Check the changed guides, their links, inheritance, and scope boundaries.
Confirm that removing a detail did not remove a genuine high-risk gotcha,
that moved guidance is discoverable from its parent, and that stubs have not
accumulated generic rules. Then verify:

```bash
test -L CLAUDE.md && test "$(readlink CLAUDE.md)" = "AGENTS.md"
git diff --check -- AGENTS.md '**/AGENTS.md' .agents/agents-md-sync/SKILL.md
```
