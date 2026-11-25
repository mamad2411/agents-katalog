---
name: knowledge-drift-sync
description: Use before finishing any non-trivial change to Ork. Reconciles code with specs/, the user docs (docs/, What's new, README.md), decisions/, rfcs/, runbook/, the interaction map, memories, and changesets so no knowledge is left stale.
---

# knowledge-drift-sync

## Prerequisites

- The change under review: `git diff` (working tree) or `git diff main...HEAD`
  (branch).

## Workflow

1. **List what changed** in behavior or structure.
2. **Find each change's canonical home** in the table below and compare:
   - code changed behavior → update the spec in the same change;
   - a spec changed → the code implements it, or the spec says it is not built
     yet (its status line);
   - a lint-enforced rule changed → `oxlint.config.ts` and
     [specs/architecture.md](../../../specs/architecture.md) agree.
3. **Decisions:** an RFC that shipped gets an ADR, status `Implemented`, and
   moves to `rfcs/archived/`; both indexes are updated. A hard-to-reverse choice
   made without an RFC has an ADR.
4. **Interaction map:** a change in how parts interact, or a part becoming built,
   runs the [resync-map](../resync-map/SKILL.md) skill.
5. **User docs:** anything a user can see (a command, flag or output, the
   browser view, a driver's behavior, where Ork keeps things or what it sends)
   is shown in its guide under [docs/](../../../docs/README.md) and has a bullet
   in [Next release](../../../docs/whats-new/next-release.md), with an
   "Upgrade:" line when something users rely on breaks. Check `README.md` when
   it names what changed. A changeset is not a substitute: it feeds the
   changelog, What's new is what users read.
6. **Releases:** a change to shipped code carries a changeset; internal-only
   work carries an empty one
   ([runbook/development/release.md](../../../runbook/development/release.md)).
7. **Memories:** update `last-verified` on each memory you re-checked; fix or
   delete stale statements. Resolve working memories tied to this change.
8. **Checks:** `pnpm check` passes, which includes `pnpm docs:check` and
   `pnpm map:check`.
9. **Report** what was synchronized, or state "no drift" with the evidence.

## Knowledge maintenance

| If you change…                                             | Review…                                                                                                                                                      |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| the workflow schema, node types, edges, the serializer     | [specs/workflow-format.md](../../../specs/workflow-format.md), `pnpm --dir packages/schema gen:json-schema`, `examples/`, ADR-006 if the format's rules change, [docs/guides/writing-workflows.md](../../../docs/guides/writing-workflows.md) |
| the expression language                                    | [specs/expressions.md](../../../specs/expressions.md), ADR-007 if its safety rules change                                                                     |
| the graph compiler's checks or diagnostic codes            | [specs/graph-compiler.md](../../../specs/graph-compiler.md), ADR-008 for ownership rules                                                                      |
| the runtime port, a driver, Ork's MCP tools, reports       | [specs/runtime.md](../../../specs/runtime.md), [specs/messaging.md](../../../specs/messaging.md), ADR-005, ADR-010, ADR-011, [docs/guides/drivers.md](../../../docs/guides/drivers.md) |
| context layers, precedence, isolation, prompt order        | [specs/context.md](../../../specs/context.md), ADR-009, [docs/guides/skills-and-context.md](../../../docs/guides/skills-and-context.md) |
| messaging, decisions, the event store                      | [specs/messaging.md](../../../specs/messaging.md)                                                                                                            |
| feedback                                                   | [specs/feedback.md](../../../specs/feedback.md), ADR-013                                                                                                     |
| anything a user can see                                    | the guide in [docs/](../../../docs/README.md) that shows it, a bullet in [Next release](../../../docs/whats-new/next-release.md), `README.md` if it names it |
| a CLI command, its flags or output                         | [specs/cli.md](../../../specs/cli.md), `README.md`, the guide in [docs/guides/](../../../docs/README.md#guides) that shows it |
| requirements, platforms, how Ork is installed or released | [docs/getting-started/installation.md](../../../docs/getting-started/installation.md), `README.md` |
| something left out, or built a simpler way for now | [specs/gaps.md](../../../specs/gaps.md), until a gaps review decides it |
| a limit a gaps review decided to keep | its area's Limits chunk (e.g. `specs/scheduler/limits.md`), keeping its L-number |
| the UI                                                     | [specs/ui.md](../../../specs/ui.md), [docs/guides/browser-view.md](../../../docs/guides/browser-view.md)                                                     |
| packages, the dependency direction, a new package          | [specs/architecture.md](../../../specs/architecture.md), `oxlint.config.ts` boundary table, `AGENTS.md`, `.ai/memories/overview.md`                          |
| how Ork touches credentials or secrets, or what it stores  | ADR-004, `SECURITY.md`, [specs/runtime.md](../../../specs/runtime.md), [docs/guides/where-ork-keeps-things.md](../../../docs/guides/where-ork-keeps-things.md) |
| a document's size or layout                                | [docs-structure](../docs-structure/SKILL.md), `pnpm docs:check`                                                                                              |
| how components interact, or a component becoming built     | the [interaction map](../../../docs/interaction-map/README.md) via [resync-map](../resync-map/SKILL.md)                                                     |
| releases, versioning, the published package                | [runbook/development/release.md](../../../runbook/development/release.md), `.changeset/`, ADR-015, `tools/release/whats-new.ts`                              |
| scripts, CI, hooks                                         | `CONTRIBUTING.md`, `AGENTS.md`, `.ai/memories/development-workflow.md`                                                                                       |
| a dependency                                               | an ADR for a new runtime dependency; the 7-day rule in `pnpm-workspace.yaml`                                                                                 |
| the AI layer (skills, templates, memories, adapters)       | [`.ai/README.md`](../../README.md), `AGENTS.md`                                                                                                              |

## Constraints

- Follow the precedence order in [`.ai/README.md`](../../README.md); when code
  and a spec disagree and the intent is unclear, ask — do not guess.
- Fix the lower-precedence source or flag it; never silently pick one.

## Useful commands

```sh
git diff --stat main...HEAD
pnpm check
pnpm docs:check
pnpm map:check
```

## Expected output

A drift report plus the doc and code changes, in the same change.

## References

- [ADR-001](../../../decisions/ADR-001-spec-driven-development.md),
  [write-an-rfc](../write-an-rfc/SKILL.md)
