---
name: audit-and-shrink
description: >
  Audit a codebase for duplicate code, dead code, and drifted parallel
  implementations; write a durable ranked audit markdown; rank consolidations by
  refactor value; implement highest-yield shrinks with verify-before-complete.
  AUTO-RUN the global workflow audit-and-shrink when the user asks to shrink the
  codebase, remove drift, dedupe, clean dead code, or combines
  audit-duplicate-dead-code / improve-codebase-architecture /
  frontend-code-hygiene / component-refactoring with an implement intent.
---

# Audit and Shrink

## Auto-run (do not only summarize)

When the user wants **implementation** of shrink/dedupe/drift cleanup (not a pure
explanation), **immediately** launch the workflow tool:

```text
name: audit-and-shrink
args: {
  "root": "<optional path focus e.g. packages/foo or apps/web>",
  "focus": "<optional free-text theme>",
  "dry_run": false,
  "max_clusters": 5,
  "auto_implement": true,
  "report_dir": "docs/audits",
  "write_repo_report": true,
  "report_slug": ""
}
agent_budget: 64
```

- Inventory only → `"dry_run": true` (still writes audit markdown)
- Human gate before edits → `"auto_implement": false`
- Cap implement batch with `"max_clusters"` (1–8, default 5)
- Report location → `"report_dir"` (default `docs/audits`) + optional `"report_slug"`

Tell the user the run is in `/workflows`. On completion report:

1. **Durable audit path** (`report_path`, usually `docs/audits/audit-and-shrink.md`)
2. Inventory path if separate
3. Ranked clusters / what landed / verify ok
4. Scratch summary `audit-and-shrink-report.md`

## What the workflow does

Phases (global script `~/.grok/workflows/audit-and-shrink.rhai`):

1. **Scope** — live seams, package manager, verify commands, report dir  
2. **Explore** (parallel, read-only) — duplicate · dead · drift · **catalog_ssot** · **table_drive** · **adapter_parity** · architecture · god-shell hotspots  
3. **Rank** — merge/dedupe by value; **reject feature-loss** proposals  
4. **Measure** — file counts, line footprint, blame snapshot, git provenance  
5. **AuditMd** — durable inventory markdown (template) to `report_dir` + scratch  
6. **Gate** — dry_run stops; optional await_user  
7. **Implement** — same public surface, fewer impls + regression tests for drift  
8. **Verify** — rebuild → test/typecheck/build fail-closed + one repair  
9. **Finalize** — update audit with landed table, remaining backlog, verify proof  

Playbook: [references/shrink-playbook.md](references/shrink-playbook.md) · template: [references/report-template.md](references/report-template.md)

### Audit markdown (required)

Follows [references/report-template.md](references/report-template.md) (same shape as
`audit-duplicate-dead-code` report-template):

| Section | Purpose |
|---------|---------|
| How This Audit Was Built | methodology |
| Provenance | branch, SHA, recent commits, diff stat |
| Live Seams | active entrypoints |
| Cluster Inventory | table: files / lines / **savings** / blame / status |
| Highest Value Remaining | ranked open work |
| Already Landed | this series outcomes |
| Cluster Notes | why exists / why matters / evidence / plan |
| Dropped | out of scope |
| Explore summaries | per dimension |
| Verification | fail-closed proof |
| Implementation Detail | files/tests/deltas |

**Savings ≠ footprint** — total lines and estimated savings are separate columns.

## Composed skill methodologies

| Skill | How it is used |
|-------|----------------|
| `audit-duplicate-dead-code` | Behavior clusters, import-proven dead, ranking rubric, report template |
| `improve-codebase-architecture` | Module / Seam / Depth / Locality; deletion test |
| `frontend-code-hygiene` | Render-time side effects, barrels, hooks |
| `component-refactoring` | Hotspots without micro-hooks |
| `verification-before-completion` | No success without command evidence |

## Args reference

| Arg | Default | Meaning |
|-----|---------|---------|
| `root` / `scope` | `""` | Path prefix to focus |
| `focus` | `""` | Free-text theme |
| `dry_run` | `false` | Inventory + audit md only |
| `max_clusters` | `5` | Implement batch cap (1–8) |
| `auto_implement` | `true` | Skip human gate after inventory |
| `report_dir` | `docs/audits` | Where durable markdown is written |
| `write_repo_report` | `true` | Write into the workspace (not only scratch) |
| `report_slug` | `""` | Optional filename stem (`{slug}.md`) |

## Manual invoke

```text
/workflow audit-and-shrink
/workflow audit-and-shrink dry_run=true
/workflow audit-and-shrink root=apps/web max_clusters=3
/workflow audit-and-shrink report_dir=docs/audits report_slug=forms-builder-2026-07-31
```

## Shrink without losing UI or function

**Hard invariant** (full detail in [references/shrink-playbook.md](references/shrink-playbook.md)):

> Same public surface, fewer implementations. Never remove field types, modes,
> routes, ports, or user-visible flows to “save lines.”

Preferred consolidations:

1. **Catalog SSOT** — palette / SPEC / docs / seed derived from registry or one writer  
2. **Use cases behind thin adapters** — HTTP = parse → core use-case → status map  
3. **Table-driven domain** — command/dispatch/render maps instead of twin switches (keep every case)  
4. **Adapter contract parity** — memory vs Athena same semantics + shared tests  
5. **God-module split** — same UI, inspectors/styles as siblings (locality only)  
6. **Generated artifacts** — seed JSON and field catalogs are outputs, not second sources  
7. **Import-proven dead code** only  

### Residual targets (this monorepo after first shrink runs)

| Pattern | Safe because | Typical win |
|---------|--------------|-------------|
| BuilderShell inspector split | Zero UX change | locality, ~−300 shell lines of debt |
| form-commands / form-controller handler maps | Same actions | less drift adding commands |
| Seed script sole writer of demo-seed.json | Same demo data | kill dual edit |
| SPEC field_types ↔ `ALL_FIELD_TYPES` | Same catalog | kill doc drift |
| Shared `toHttp(useCaseResult)` | Same REST shapes | thinner routes |
| Further render-registry table-drive | Same field types | less per-type paste |
| Memory/Athena CRUD helper share | Same ports | less adapter drift |
| generate-docs custom YAML bulk | Same docs set | smaller tooling |

### Explicit non-goals

- Deleting conversational / multi-step / embed / survey modes  
- Deleting field types or ports to shrink registries  
- Rewriting the UI stack  
- Micro-file explosion (one-line wrappers)

## Improvements vs first revisions

- Inventory markdown **before** implement; durable `docs/audits/`  
- Measure phase (lines ≠ savings, blame, git provenance)  
- Explore dimensions include catalog_ssot / table_drive / adapter_parity  
- Rank drops `feature_loss` proposals  
- Implement + explore prompts carry hard “no feature removal” invariant  
- Finalize fills Landed + Remaining + Verification + diffstat  

## Exceptions

- “Inventory only” / “don’t edit” → `dry_run: true`
- Single-cluster explanation, no fix → answer normally; do not launch
- “Report only” → `dry_run: true`, still writes audit markdown
