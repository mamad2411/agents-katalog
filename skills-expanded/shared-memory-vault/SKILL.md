---
name: shared-memory-vault
description: A memory governance engine for multi-agent cloud knowledge bases — one knowledge base shared by every agent and every device, with consistency guaranteed. Nine automations on a shared Markdown knowledge base: ① session archiving & indexing ② incremental update decisions (diff + changelog) ③ provenance / confidence tagging ④ periodic reflection ⑤ write-after change awareness ⑥ semantic retrieval ⑦ cross-project memory linking (A-MEM style) ⑧ forgetting-curve scoring (MemoryBank style) ⑨ governance benchmark. One-command bootstrap generates the knowledge-base skeleton; governance actions fire automatically across the session lifecycle. All scripts are pure Python standard library with zero third-party dependencies, runnable standalone or on a schedule. Trigger words: shared memory, multi-agent collaboration, cross-device knowledge base, consistency, knowledge base governance, memory archiving, incremental update, provenance, reflection, memory linking, forgetting curve, governance benchmark, vault init, memory retrieval.
agent_created: true
---

# shared-memory-vault — Multi-Agent Memory Governance Engine

> Packages "session blackboard + layered knowledge + nine governance automations" into a self-bootstrapping, long-running, pure-Markdown memory governance layer.
> Any agent using this skill can build a shared multi-agent knowledge base on any file-sync directory and automatically gain nine governance capabilities.

## Shared knowledge-base root (user-defined)

```
Vault = <your cloud-synced directory>  (any cloud/sync drive, or any local synced folder)
```

> How to recognize a knowledge-base root: the directory contains both a navigation home (`MOC.md` or equivalent) and a `user memory/` folder.
> The carrier is vendor-agnostic — pure Markdown files only; cross-device sync is the user's choice.

## Core structure (machine zone / human zone)

| Zone | Ownership | Content | Governance rule |
|---|---|---|---|
| `user memory/` | machine | protocol (AGENT_PROTOCOL + MEMORY + FRONTMATTER_SPEC) | the highest authority for all behavior |
| `work memory/<sessionID>/` | machine | daily log (append) + project notes + reflections | one per session |
| `context/<sessionID>/` | machine | session blackboard CONTEXT.md (collaboration core) | 3-turn compression; archiving per ① |
| `context/_archive/` | machine | completed + expired sessions | move-only, never delete |
| `context/_index.md` | machine | index of all sessions (topic/status/updated) | read on open |
| `references/` | human | knowledge assets (layered, see below) | **readable; writing requires user authorization** |
| `_templates/` `_attachments/` `other/` | human | templates / attachments / misc | read-only by default |

### references layered knowledge (four categories)

```
references/
├── notes/       raw layer: original study/work notes (categorized by topic)   ← source of truth
├── learning/    learning layer: distilled notes → topic libraries + theory traces
├── work/        work layer: work-material distillation → project-specific + general methodology
└── reading/     reading layer: book-list distillation → topic categories
```

> Layers progress and cross-reference each other; libraries interconnect via wikilinks so the graph grows.

## Nine governance automations

> Each = "what action + which script + when it fires". Scripts use only the Python standard library and live in this skill's `scripts/`.

### ① Session archiving & indexing
- Action: sessions with `status=done` whose `updated` is older than a threshold (default 30 days) are moved into `context/_archive/` (**move-only, never delete**); rebuild `context/_index.md`.
- Scripts: `vault-archive.py` (archive), `vault-index.py` (index).
- Trigger: on open + optional schedule. Three tiers: active (HOT) / done ≤ threshold (WARM) / archived (COLD).

### ② Incremental update decisions (replaces full overwrite)
- Action: before compression, judge each item of the 8 sections as `+` add / `~` modify / `-` delete / `·` NOOP; write a "## Change Log" (keep latest 5); if someone else already changed it (newer `updated`), re-apply your diff on their latest version.
- Red line: `-` only removes "items you wrote this session that are now stale"; others' todos default to `·` (keep).
- Script: `context-update.py` (`log` records a change / `merge` checks conflict).

### ③ Provenance / confidence tagging (prevents shared misconception)
- Action: prefix key facts and decisions with `[U]` user-stated / `[I]` agent-inferred / `[E]` external-system (read-only) / `[D]` decision (with rationale); inferences get `confidence: high|medium|low`; low-confidence items are treated only as "hypothesis to verify", never as established fact.
- Script: `provenance-check.py` (audits for missing/low-confidence provenance).

### ④ Periodic reflection (compression → abstraction)
- Action: at milestones / session end, read multiple logs + related CONTEXT, and write a reflection into `work memory/<project>/MEMORY.md` under `## Reflection`. Four elements: patterns / lessons / reusable decisions / hints for the next agent.
- Script: `reflect.py` (aggregates logs + generates a reflection skeleton).
- Trigger: milestone / session end / schedule.

### ⑤ Write-after change awareness (blackboard)
- Action: after each CONTEXT.md overwrite, `vault-index.py` updates the `_index.md` row `updated` + appends `context/_changes.log` (NDJSON, one `{ts,session,action,target}` per line).
- Read order on open: protocol → dashboard (with recent changes) → this session's CONTEXT.

### ⑥ Semantic retrieval
- L1 (zero-dependency): `search.py` filters by frontmatter (`--topic/--status/--since`), enough for 100–200 sessions.
- L2 (optional, local vectors): local embeddings + a vector store (multilingual model); index artifacts are not committed or dual-written.

### ⑦ Cross-project memory linking (A-MEM style)
- Action: scan `work memory/` MEMORY.md files and link similar sessions via character-bigram Jaccard similarity, writing each note's `## Related Memories` section + a global `work memory/_links.md`.
- Value: breaks "each project's memory is isolated", making cross-project experience retrievable.
- Script: `link-memory.py` (idempotent; re-runs don't duplicate).

### ⑧ Forgetting-curve scoring (MemoryBank style)
- Action: compute a retention score as `importance × exp(-decay_rate × days since last access) × frequency boost`; below threshold → suggest archiving (move-only, keep original).
- Replaces "fixed-day cutoff": high importance decays slowly, low importance decays fast, frequent access resists forgetting.
- Script: `decay-score.py` (outputs ranking + archive suggestions).
- Optional frontmatter: `importance`, `last_access`, `access_count`.

### ⑨ Governance benchmark
- Action: compute governance health (provenance coverage / archive timeliness / change-log coverage / reflection coverage / index completeness / linking coverage) → Governance Score (0–100).
- Value: quantifies "memory quality", filling the "no benchmark for governance" gap.
- Script: `governance-score.py` (prints report, `--out` writes a file).

## Lifecycle SOP (every session runs this automatically)

1. **Open**: read the protocol trio → run `vault-index.py --vault <Vault>` to refresh the index → read `context/_index.md` + this session's CONTEXT.md (inherit if present).
2. **Set up**: create `context/<sessionID>/CONTEXT.md` (five frontmatter fields + 8 sections) + `work memory/<sessionID>/YYYY-MM-DD.md`; tag key facts with provenance per ③.
3. **Work**: every 3 turns, update CONTEXT.md incrementally with `context-update.py log` (keep frontmatter, bump `updated`, append change log).
4. **Distill**: at milestones/end, run `reflect.py` + `link-memory.py`; writing knowledge into references requires explicit user request.
5. **Handoff**: complete todos + decision rationale → set status to done → run `vault-archive.py` (if expired) + `vault-index.py` (write change log).

## Script cheatsheet

| Script | Purpose | Example |
|---|---|---|
| `vault-init.sh` | bootstrap the skeleton | `bash scripts/vault-init.sh --dir <path>` |
| `vault-index.py` | rebuild index + write change log | `python3 vault-index.py --vault <Vault>` |
| `vault-archive.py` | archive expired sessions | `python3 vault-archive.py --vault <Vault> --days 30` |
| `context-update.py` | incremental update / changelog / merge | `python3 context-update.py --context <path> log --mark + --section todo --summary "..."` |
| `provenance-check.py` | provenance audit | `python3 provenance-check.py --vault <Vault>` |
| `reflect.py` | reflection generation | `python3 reflect.py --work <dir> --out <file>` |
| `search.py` | frontmatter retrieval | `python3 search.py --vault <Vault> --status done --since 7` |
| `link-memory.py` | cross-project linking | `python3 link-memory.py --vault <Vault> --threshold 0.15` |
| `decay-score.py` | forgetting-curve scoring | `python3 decay-score.py --vault <Vault> --score-threshold 0.2` |
| `governance-score.py` | governance benchmark | `python3 governance-score.py --vault <Vault> --out report.md` |

## Five iron rules (apply to every action)

1. Never build a private memory/knowledge base — write everything to the shared repository
2. `references/` is readable; writing requires user authorization
3. External systems (collaboration platforms / online docs / email) are read-only
4. Never touch personal directories
5. Before any batch write/edit/delete (>1 item), show the detailed list and get confirmation

## Install & bootstrap

1. Install this skill into your agent's skills directory (e.g. `~/.workbuddy/skills/shared-memory-vault/`).
2. Bootstrap: `bash scripts/vault-init.sh --dir "<your cloud-synced directory>"` generates the skeleton (protocol + templates + index) in one command.
3. From then on, each session follows the lifecycle SOP; optionally schedule archiving / reflection / linking / scoring / retrieval.
