---
name: serena-memory-hygiene
description: Audit and refresh Serena memory files so they stay concise, dated, and source-linked. Use when `.serena/memories` exists and the task maintains Serena memories, reads or changes Serena memory files, refreshes canonical project-memory/docs, or checks a memory that may be stale against canonical repo docs, manifests, source, or tests.
---

# Serena Memory Hygiene

Keep Serena memories useful without turning them into a parallel wiki. Serena
memories are retrieval indexes and handoff hints; canonical project truth lives
in repo docs, local agent instructions, manifests, build/test config, source,
and tests.

## Workflow

1. Confirm Serena context:
   - Look for `.serena/memories/`, Serena memory tools, or user-provided memory
     content.
   - If Serena is absent, say this skill is not needed.
2. Find canonical sources:
   - Prefer `AGENTS.md`, docs entrypoints, overview/status/next-step docs,
     ADRs, manifests, build/test config, source, and tests.
   - If project-memory-style docs exist, treat them as the preferred map.
   - If another docs system exists, respect it.
3. Audit memory claims:
   - Check duplicated commands, dependencies, validation status, branch/status
     notes, entrypoints, generated-output paths, module ownership, and active
     refactor details.
   - Verify duplicated facts against their canonical sources before preserving
     them.
4. Refresh memories:
   - Update canonical docs first when they are stale and the user asked for
     broader docs maintenance.
   - Otherwise, point memories at existing sources and remove volatile detail.
   - Keep memories concise, source-linked, and easy to scan.
5. Validate:
   - Run `serena memories check` when available.
   - Report changed memory files and any skipped validation.

## Freshness Header

Each maintained Serena memory should start with:

```md
Last checked: YYYY-MM-DD
Source of truth: `docs/...`, manifests, source/test paths
Update when: the concrete upstream fact changes
```

Use the header as a trust signal. If a source changed after `Last checked`,
verify the memory before relying on it.

## Content Rules

Prefer stable invariants, short source maps, pointers to canonical sources, and
`mem:` references for memory-to-memory navigation.

Avoid exact test counts, current branch names, exhaustive script/dependency
lists, long validation histories, active-refactor ownership details already in
canonical docs, and one-off task notes.

## Boundaries

- Do not require `project-memory`; only cooperate with it when its docs exist.
- Do not patch project-memory skills, templates, or setup instructions by
  default.
- Suggest a docs-memory setup only when missing canonical docs are causing
  repeated rediscovery or stale-memory risk.
- Add scripts or hooks only after repeated real failures show that instruction
  alone is insufficient.
