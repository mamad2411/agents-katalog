---
name: build-right-wayfinder
description: Maintain a durable multi-session decision map when the destination is meaningful but the implementation path cannot yet fit in one trustworthy planning session. Use only when the user explicitly invokes this skill for a foggy effort that needs research, prototypes, founder decisions, or technical decisions before feature planning.
---

# Build Right Wayfinder

Use this opt-in companion to make a destination progressively taskable without
pretending uncertainty is an implementation plan.

## Canonical Artifacts

- `docs/wayfinding/<slug>/map.md`
- `docs/wayfinding/<slug>/decisions/<id>-<slug>.md`

Markdown is canonical. External trackers may mirror links and status but cannot
replace the map or decision records.

Read `references/workflow.md` before starting or continuing a map. Use
`assets/templates/map.md` and `assets/templates/decision.md` for target-repository
artifacts.

## Workflow

1. Inspect repository instructions, current authority, existing wayfinding
   maps, and Git state.
2. State the destination and observable completion criterion. If these are not
   meaningful yet, route back to `$build-right-preflight`.
3. Create or resume the canonical map. Keep decisions, the current unblocked
   frontier, in-scope fog, and explicit out-of-scope work separate.
4. Select one frontier decision and claim it in its decision record before
   working. Never silently work an unclaimed decision.
5. Resolve at most one non-research decision per run. Research may gather
   evidence for several decisions, but must not silently resolve them.
6. Record evidence, resolution, residual uncertainty, and map changes.
7. When no frontier or fog remains, close the map and hand the resolved
   decisions to `$build-right-feature-planning`.

## Boundaries

- Do not create implementation tasks, OpenSpec changes, or product code.
- Do not turn fog into fake acceptance criteria or dependency edges.
- Do not treat a prototype, unanswered questionnaire, public inference, or
  external tracker state as product truth.
- Do not automatically commit, push, merge, publish, deploy, clean up, or alter
  production.
- Do not automatically abort or resolve an existing Git operation.
- Ask founders only for decisions; look up repository and public facts directly.

## User-Visible Status Badge

End every final response with exactly one status badge block:

```text
✅ [DONE] Status: DONE
Decision: <resolved decision or closed map>
Next action: <next frontier or feature-planning handoff>
Needs user input: <none | one founder decision>
Blocked by: <none | evidence blocker>
```

Use `🟢 [GREEN] Status: ALL GREEN` while a frontier remains actionable,
`🟡 [YELLOW] Status: NEEDS INPUT` for a founder decision,
`🟠 [ORANGE] Status: NEEDS WORK` for AI-owned research/prototype work,
`🔵 [BLUE] Status: WAITING EXTERNAL` for external evidence, and
`🔴 [RED] Status: BLOCKED` for invalid map state or conflicting authority.
