---
name: version-partitioner
description: (NS) Partition a large master requirements.md into executable subversions with version-roadmap.md and slice requirements excerpts — without generating tasks. Use when a version has too many features for one planning cycle or the user asks to split a version — after Gate 1 requirements confirmed. Do NOT generate task-NNN files (planning per slice comes later).
depends:
  - nextstage-harness
---

# Version Partitioner

Split master `requirements.md` into subversions for sequential planning.

## Harness discovery

See `../nextstage-harness/references/artifact-layout.md` and `../nextstage-harness/references/harness-discovery.md`. Read `core-subversions` rule from harness when present.

## Scope

- **Read only:** master `{product_root}/docs/versions/{version_san}/requirements.md`
- **Do not:** generate tasks, execution-handoff, or re-run Gate 1
- **Do not load** product backend/frontend rules — structural partition only

## Algorithm

1. **Parse master** — Features, precedences, data model hints, layer tags
2. **Build DAG** — default order: schema → API → FE → tests; honor explicit precedence
3. **Group by bounded context** — cluster by domain/entity
4. **Split oversized groups** when:
   - \> 12 features with cross-dependencies, or
   - ~50 estimated tasks, or
   - ~600k token heuristic
5. **Consolidate undersized** — merge adjacent slices below ~4 tasks when safe; target **4–7 tasks** per subversion
6. **Topological sort** — folders `01-slug`, `02-slug`, …
7. **Emit artifacts:**
   - `version-roadmap.md` at version root
   - `subversions/{subversion_san}/requirements.md` — **excerpt** + link to master `../requirements.md#Feature-ID`
   - Empty `subversions/{subversion_san}/tasks/` per slice

## Roadmap table columns

| NN | slug | Features | deps | tasks est. | tokens est. | status |

Start `status` as `pending`.

## Output checklist

- [ ] `version-roadmap.md` saved
- [ ] All subversion folders with excerpt requirements + empty `tasks/`
- [ ] No `task-*.md` created
- [ ] Human can review before slice planning loop

## References

| File                                     | When                              |
| ---------------------------------------- | --------------------------------- |
| `references/version-roadmap.template.md` | Roadmap structure                 |
| `references/partition-workflow.md`       | Orchestrator loop after partition |

## Integration

After partition → Gate Roadmap (human confirms) → plan each slice (Gates 2–3, tasks) without repeating Gate 1.
