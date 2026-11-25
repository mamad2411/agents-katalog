---
name: mneme-agent-brain
description: Use when an agent needs to build, label, retrieve from, surface thoughts from, or safely write temporary memory into a Mneme graph-backed Markdown vault.
version: 2.1.0
author: Mneme contributors
license: MIT
platforms:
  - linux
  - macos
metadata:
  hermes:
    category: memory
    tags:
      - mneme
      - memory
      - graph
      - retrieval
      - agent-brain
    config:
      env:
        MNEME_LABEL_PROVIDER: Optional label provider, for example ollama or hermes.
        MNEME_LABEL_MODEL: Optional model name for provider-backed labelling.
        MNEME_LABEL_COMMAND: Optional command that reads a labelling prompt on stdin and emits JSON.
        MNEME_BRAIN_DEPTH: Optional labelling depth preset: smoke, default, deep, or full.
        MNEME_SURFACE_LIMIT: Optional number of thoughts to return from the final surface check.
---

# Mneme Agent Brain

## Overview

Mneme turns a Markdown vault into an auditable SQLite neural map for agents. Use it as a local-first brain: ingest notes, consolidate graph structure, maintain durable world-model state, label clusters/nodes/synapses/relationships through a swappable model harness, retrieve prompt-time context, surface thoughts, and add temporary graph memory without editing existing Markdown.

The default philosophy is evidence first. Retrieval may include candidate synapses, but candidate-only edges are not facts. Temporary agent memory must use a `mneme://` source path so it can be removed as one unit.

## Mandatory Agent Contract

Before using Mneme memory in any user-facing answer or action, run:

```bash
mneme agent preflight --db "$DB" --prompt "$PROMPT"
```

The agent must obey the returned `agent_rules`.

Hard rules:

1. Do not use Mneme memory as factual grounding unless `contract.status` is `pass`.
2. Always inspect `truth_policy` before using a retrieved item.
3. `candidate_only` means possible, unvalidated, and never phrased as fact.
4. `provenance_not_fact` means the edge is useful for navigation or source context, not real-world truth.
5. `source_contained_observation` means the source contains the observation; freshness still matters.
6. Killed or excluded edges must never be surfaced, relied on, or recreated.
7. Old open loops are historical until fresh source evidence or explicit user confirmation makes them live.
8. User dismissal weakens surfacing by default. Kill only when the user or evidence says the relationship is false.
9. Temporary agent memory must use `mneme://` and must be removable as one unit.
10. Do not edit Markdown notes unless the user explicitly asks for vault writeback.
11. Current world-model assertions outrank candidate graph edges when they conflict.
12. Open, missed, or unverifiable predictions are operational state. Inspect them before actions that depend on expected future evidence.
13. `world.contradictions` means newly perceived evidence disagrees with current durable state. Preserve both sides, keep candidate challengers tentative, and resolve from source evidence or user confirmation.
14. Graph-edge contradiction checks require explicit single-value metadata (`conflict_policy: exclusive` or `cardinality: one`). Never infer cardinality from predicate wording.

## When To Use

- A Hermes agent needs context from a Mneme database before answering or acting.
- You need to refresh a vault graph and build the working brain labels.
- You want retrieval-backed thought surfacing rather than a random graph walk.
- You need to add short-lived test or working memory without modifying existing vault notes.
- You need to validate that retrieval, synapses, clusters, labels, and surfaced thoughts work together.
- You need a state/action/prediction loop: current assertions, future expectations, and durable records of external side effects.

Do not use this skill to make unreviewed edits to user Markdown. Use `mneme remember add/remove` for temporary graph memory, and use `mneme note` or `mneme resolve` only when the user explicitly wants vault writeback.

## Required Repository Shape

Hermes skills are installed from a directory containing this `SKILL.md`. Supporting files live beside it:

```text
skills/mneme-agent-brain/
  SKILL.md
  references/install-update.md
  references/operator-flow.md
  scripts/mneme_brain_smoke.sh
```

If this skill is installed from a repo tap, run Mneme commands from the Mneme checkout or set `MNEME_REPO` to that checkout before using the helper script.

For copy-based Hermes installs and updates, follow `references/install-update.md`.

## Cortex Commands

When `mneme status --json` reports `"set_up": true`, the LLM-driven cortex is installed. Use `mneme ask "$PROMPT" --json` for memory-backed answers, `mneme reflect --json` while idle, and `mneme thoughts --json` to see what it raised. Ground answers in `evidence`, and never act on items whose `trust` is `suspicious`. Exit code `2` means a `file` mind is waiting for task answers. The full rules are in the `mneme` skill under "Cortex Path". The graph commands below work on the separate graph database.

## Core Commands

Build or refresh the graph:

```bash
mneme update --vault "$VAULT" --db "$DB"
```

Build local neural memory and activate it when an embedding provider is available:

```bash
mneme index --db "$DB" --provider ollama --model nomic-embed-text
mneme think --db "$DB" --provider ollama --model nomic-embed-text --prompt "$PROMPT"
```

Treat latent activation as a lead. Only active, source-backed synapses may become factual thought paths.

Build the working brain:

```bash
mneme consolidate --db "$DB" --label-provider ollama --label-model gemma4:e4b
mneme brain label --db "$DB" --targets cluster,node,synapse,relationship --label-provider ollama --label-model gemma4:e4b
mneme brain report --db "$DB"
```

Swap the labelling model without changing the graph logic:

```bash
mneme brain label --db "$DB" --targets cluster,node,synapse,relationship --label-provider hermes --label-command "hermes label --json"
```

Retrieve context:

```bash
mneme retrieve --db "$DB" --prompt "$PROMPT" --max-items 8
```

Inspect world-model state before acting on memory-backed context:

```bash
mneme state list --db "$DB" --status current
mneme state conflicts --db "$DB"
NOW=$(python3 -c 'from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())')
mneme predict due --db "$DB" --before "$NOW"
mneme world watch --db "$DB" --lead 1d
mneme world tick --db "$DB" --before "$NOW" --dry-run
```

Write predictions when a source-backed resolution creates an expectation that later evidence should appear or not appear. Use `mneme resolve` with a `predictions[]` array when the prediction belongs to the same research payload, or `mneme predict add --file prediction.json` for standalone expectations. Omit `id` unless a stable external ID exists; Mneme derives deterministic content-hash IDs. Use `world watch` as a read-only pre-failure radar for open predictions due soon with no matching evidence. When the expectation must be satisfied before a related event, use structured `match_json.gate` criteria and a deterministic `time_field` (`observed_at` or `metadata.<path>`); never infer the event deadline from prose.

Retrieval and preflight apply `valid_until` at read time. Treat `lapsed_state_assertion` as historical evidence, not current truth. Use `--as-of` for reproducible historical replay; do not mutate durable state merely because a read-time validity window elapsed.

Record durable action ledger entries when an integration performs a side effect:

```bash
mneme action record --db "$DB" --file action.json
```

Side-effectful actions must set `side_effect_level` to a non-`none` value and include `external_ref` or `tool_call_id`; otherwise Mneme rejects the action as unauditable. Add an optional `verify` block with explicit `sense_type` when the action should spawn its own deterministic verification prediction.

Canonicalize fragmented subject names with aliases:

```bash
mneme alias add "the landlord" "St James" --db "$DB"
mneme alias merge "the landlord" "St James" --db "$DB" --dry-run
mneme alias ls --db "$DB"
```

Run the scored retrieval guardrail after scorer/world-model retrieval changes:

```bash
mneme eval retrieval --demo --min-score 0.9
```

Surface thoughts from retrieval:

```bash
mneme surface --db "$DB" --prompt "$PROMPT" --limit 5
```

Add and remove scoped graph memory without touching Markdown:

```bash
mneme remember add --db "$DB" --file /tmp/mneme-memory.json
mneme surface --db "$DB" --prompt "temporary validation memory"
mneme remember remove --db "$DB" --source-path mneme://test/validation
```

## Hermes Readiness Flow

When Hermes needs to prove a database is ready, run the complete harness:

```bash
MNEME_LABEL_PROVIDER=ollama MNEME_LABEL_MODEL=gemma4:e4b \
  scripts/hermes_brain_ready.sh "$DB" "$PROMPT"
```

The script must complete these steps:

1. `mneme consolidate`
2. `mneme brain label`
3. `mneme brain report`
4. `mneme contract check`
5. `mneme world tick --dry-run`
6. `mneme retrieve`
7. `mneme surface`
8. `mneme agent preflight`

Use `MNEME_BRAIN_DEPTH=smoke` for quick validation, `default` for normal runs, `deep` for a broader active frontier, and `full` only when the database is small enough or runtime is acceptable.

## Safe Temporary Memory

Use `mneme://` source paths for agent-created graph memory:

```json
{
  "source_path": "mneme://test/hermes-validation",
  "nodes": [
    {"ref": "task", "type": "task", "name": "Hermes validation"}
  ],
  "observations": [
    {"node": "task", "kind": "fact", "text": "Hermes validation should surface.", "score": 5}
  ]
}
```

Rules:

- `source_path` is required and must start with `mneme://`.
- Edges and observations may only reference nodes from the same payload.
- Remove temporary memory with `mneme remember remove`.
- Existing Markdown nodes and wikilinks must not be edited during tests unless the user explicitly asks.

## Reading Surfaced Results

`mneme surface` returns thought objects with:

- `title`, `insight`, `action`, and graph `path`
- `surface.kind`, `surface.source_path`, `surface.score`, `surface.truth_policy`
- optional `surface.cluster` and `surface.brain_label`
- `suggested_actions`

Treat `graph_memory_review` as a keep-or-forget prompt for `mneme://` memory. Treat `synapse_review` as a request to validate or kill a candidate edge before trusting it.

## Verification Checklist

- [ ] `mneme doctor` passes or the explicit `--vault` and `--db` paths are correct.
- [ ] `scripts/hermes_brain_ready.sh "$DB" "$PROMPT"` exits 0.
- [ ] `mneme agent preflight --db "$DB" --prompt "$PROMPT"` returns `contract.status: pass`.
- [ ] `mneme world tick --db "$DB" --before "$NOW" --dry-run` returns `dry_run: true` and leaves the original DB unchanged.
- [ ] `mneme retrieve` returns relevant items with `truth_policy`.
- [ ] `mneme surface` returns thoughts with `surface` metadata.
- [ ] Temporary `mneme://` memory can be added, surfaced, removed, and verified as zero remaining rows.
- [ ] No private vault paths, note names, generated SQLite files, or thought images are committed.

See `references/install-update.md` for Hermes install/update steps and
`references/operator-flow.md` for the runtime operator runbook.
