---
name: mig-rgctl
description: MigIQ-specific code knowledge graph analysis using rgctl. Use during MigIQ migrations when you need to index a codebase, validate graph artifacts, or query structure for prompt-building, planning, containerization, or execution. Prefer this over the generic rgctl skill inside MigIQ workflows — it documents MigIQ phase commands, required artifacts (.rgctl/, communities, migration_plan.json v2), and discover flags per stage. Trigger when migiq, mig-prompt-builder, mig-plan, mig-containerize, or mig-execute need graph analysis.
---

# MigIQ rgctl Analysis

MigIQ wraps the [rgctl](https://github.com/rgctl/rgctl) CLI with phase-specific discover flags, artifact checks, and query recipes.

Also install upstream skills (`rgctl install --skill`): **rgctl**, **rgctl-migrate** (`/rgctl:migrate`), and optionally **rgctl-review** for post-wave call-path checks.

**Workflow reference:** [references/workflow.md](references/workflow.md)

## Quick Start

From the **application repo root** (not `migiq-workspace/`):

```bash
# MigIQ Phase 1 — full migration analysis
rgctl discover . --with-cfg --with-security --with-taint \
  --with-dashboard --with-harmonic --export-migration-hints \
  --migration-preset hybrid_default --migration-order scheduled
```

Do **not** use `rgctl -r PATH discover .` — the trailing `.` ignores `-r`.

## Validate Index Exists

Before any MigIQ skill queries the graph:

```bash
rgctl -f json metrics --pagerank
```

If this fails, run `discover` (see workflow.md for flags by phase) and STOP.

**Never** pipe rgctl through `2>/dev/null` — parse JSON from **stdout** (`schema_version`); keep stderr visible.

### Keep the graph current (required)

Whenever a MigIQ phase (or execute wave) **changes application source files**, refresh the index **before** the next phase, wave, or graph query:

```bash
rgctl update   # or: rgctl update --files path1,path2
# Confirm:
rgctl -f json status   # expect index_current: true
```

Do this after every batch of edits — not only when `status` already looks stale. Prefer `update` over a full cold `discover` for ordinary dirty trees.

### Staleness (existing index)

```bash
rgctl -f json status
# If index_current is false:
rgctl update   # or: rgctl update --files path1,path2
```

### Artifact locations

| Mode | Where artifacts live |
|------|----------------------|
| **Canonical** | `{repo}/.rgctl/` after `rgctl discover .` |
| Legacy only | `~/.rgctl/cache/<reponame>/.rgctl/` — obsolete; re-run `discover .` or copy into `{repo}/.rgctl/` |

### Communities (subsystem mapping)

```bash
rgctl -f json communities list
rgctl -f json gql --macro-name all_communities unused
```

If `communities list` is empty, re-run discover with `--with-harmonic` (included in Phase 1 above).

### Migration plan (schema v2)

After `--export-migration-hints`:

- **Primary:** `{repo}/.rgctl/migration_plan.json`
- Optional dashboard copy: `{repo}/.rgctl/dashboard/migration_plan.json`

Parse **`.steps[]`**, ignore synthetic `label == "root"`. Bound chat output:

```bash
jq '[.steps[] | select(.label != "root") | {
  step, label, schedule_step, priority_rank, avg_pagerank, avg_harmonic
}] | .[0:20]' .rgctl/migration_plan.json
```

Do **not** use v1 `packages[]`. Prefer slash command **`/rgctl:migrate`** for a full Strangler-Fig brief outside MigIQ orchestration.

## What MigIQ Skills Deduce from rgctl

| Capability | rgctl feature | Used by |
|------------|---------------|---------|
| Languages, frameworks, build tools | discover + GQL | mig-prompt-builder, mig-plan |
| Architecture (monolith vs modules) | communities list, pagerank | mig-prompt-builder, mig-plan |
| Hotspots / god nodes | metrics `--pagerank`, `--harmonic` | mig-prompt-builder, mig-plan, mig-execute |
| External dependencies | GQL USES/DEPENDSON, semantic search | mig-prompt-builder, mig-containerize |
| Migration ordering | `migration_plan.json` v2 `.steps[]`, Kantra | migiq, mig-plan |
| Security / secrets | `--with-security` | mig-containerize, mig-deploy |
| Containerization blockers | semantic + taint (`--with-taint`) | mig-containerize |
| Refactor blast radius | `blast-radius`; lazy `slice` / `cpg flows` | mig-execute |
| Keep graph current after edits | `rgctl update` after every phase/wave that changes app sources | migiq, mig-execute, mig-test-gen, mig-containerize |
| Post-wave verify | `update`, `find` legacy imports, optional `review paths` | mig-execute |

## Lighter Discover Profiles

```bash
# Containerization / deploy readiness (no migration plan)
rgctl discover . --with-cfg --with-security --with-taint --with-harmonic

# After small edits (index already exists)
rgctl update

# Java framework migration rules (Quarkus, Spring Boot 3+)
rgctl discover . -l java --with-kantra --kantra-target quarkus
```

**CFG honesty:** Phase 1 keeps `--with-cfg` for taint/mutations/batch inspect. One-off `slice` / `cpg flows` can use **lazy** CFG — do not claim every slice needs a whole-repo rediscover.

## When to Use mig-rgctl vs upstream

| Situation | Skill |
|-----------|-------|
| Inside `/migiq` or any MigIQ skill | **mig-rgctl** (this skill) |
| General structure / migration brief outside MigIQ | **rgctl** / **rgctl-migrate** |
| PR / wave call-path deltas | **rgctl-review** |
