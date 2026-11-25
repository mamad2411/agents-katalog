---
name: ccr-self-learning
description: "Mine a repository's outcome-labeled Copilot Code Review (CCR) history into durable, typed review learnings and propose them as generated skills + scoped memories. Joins CCR comments with their outcomes (resolved-with-change = accepted; deleted/ignored = rejected; human reply = engaged; thumbs up/down) to extract suppression learnings (stop flagging X here), convention learnings (this repo enforces Y), and focus learnings (lean into Z), each with evidence, acceptance delta, and confidence. Shadow mode: proposes only, applies nothing — writes proposals to a run directory for human review via artifact-placement. Triggers: CCR self-learning, code review learning, mine review outcomes, what should CCR learn, suppression convention focus learnings, dreaming CCR, CodeIQ review learning."
user-invocable: true
allowed-tools: bash, view, grep, glob
---

# CCR Self-Learning (CodeIQ)

Close the review learning loop: turn a repo's **outcome-labeled CCR history** into durable,
typed learnings that would make future reviews better, and propose them as **generated skills +
scoped memories**. This is the Dreaming side of the CodeIQ/CCR MVP
([`CCR_CodeIQ_MVP.md`](https://github.com/github/codeiq-graph/blob/main/docs/CCR_CodeIQ_MVP.md))
— specifically its **M1 "shadow" milestone**: mine and generate candidates with **no review
impact**. It maps onto the same `miner -> curator` discipline as `repository-memory-miner` /
`repository-memory-curator`, with CCR's review corpus as the evidence and CCR's learning
taxonomy as the schema.

**Three learning types** (from the PRD):
- **suppression** — a comment category chronically rejected here ("stop flagging style on
  generated/migration paths").
- **convention** — a pattern humans repeatedly enforce that CCR misses ("wrap errors with `%w`",
  "table-driven tests").
- **focus** — a category whose comments cluster as accepted ("lean into authz in this repo").

## ⚠️ Capability gaps this skill runs ahead of (read first)

The current Dreaming system **cannot yet reach CCR's evidence**, so this skill runs against a
**pre-materialized export** today. See `references/CAPABILITY-GAPS.md` for the full gap analysis.
The blocking gaps:

- **G1 — evidence connector.** The labeled corpus lives in CCR's findings store (CosmosDB, keyed
  by repo/owner) + session telemetry. Dreaming's evidence sources (local files, GitHub MCP,
  agent `session_store_sql`, Slack/WorkIQ) do **not** include it.
- **G2 — authenticated egress.** The Dreaming sandbox firewall blocks `gh api`/`curl`; only the
  GitHub MCP server is reachable. CCR's corpus + the memory-storage API are first-party Copilot
  backends needing authenticated calls.

**Until G1/G2 land**, supply the corpus as a JSONL **export** in the shape of
`assets/corpus.schema.json` (the connector contract). Downstream apply (writing skills/memories,
governance gating, base-SHA materialization, ExP measurement) are gaps **G4–G6** and are out of
scope here — this skill stops at "propose to a run dir", which is the inspectable, revocable
trust surface the PRD asks for.

## Inputs

- **Corpus** — path to the outcome-labeled JSONL export (`--corpus`). For a dry run / demo, use
  the bundled `assets/sample-corpus.jsonl`.
- **Target repo** — the repo the corpus belongs to (informational; the corpus carries `repo`).
- **Output directory** — a fresh `ccr-learning-run-<timestamp>/` outside any checkout.

## Helper scripts

Invoke by absolute path as `"$SKILL_DIR/scripts/…"`. Pure stdlib, deterministic, no network.

| Script | Purpose |
| --- | --- |
| `scripts/aggregate_outcomes.py` | Aggregate the corpus into signals: per-category acceptance/rejection + delta, rejected-comment path clusters, and human-enforced conventions. Does the counting; no thresholds. |
| `scripts/score_learnings.py` | Validate the agent-authored `learnings.json`, apply evidence + confidence thresholds, dedup, and decide **skill vs memory**. |
| `assets/corpus.schema.json` | The connector contract (what G1 must deliver). |
| `assets/sample-corpus.jsonl` | A realistic stub for end-to-end dry runs. |

## Procedure

Set up once:

```bash
SKILL_DIR="<this skill's directory>"
CORPUS="<path to corpus.jsonl>"               # or "$SKILL_DIR/assets/sample-corpus.jsonl"
RUN_DIR="$(pwd)/ccr-learning-run-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUN_DIR"
```

### Step 1 — Aggregate the corpus (deterministic)

```bash
"$SKILL_DIR/scripts/aggregate_outcomes.py" --corpus "$CORPUS" --out "$RUN_DIR/aggregates.json"
```

`view` `aggregates.json`. Read `totals.baseline_acceptance_rate`, then `by_category` (each row
carries a `signal` hint of `suppression` / `focus` / `neutral`), `by_path_prefix` (where rejected
comments cluster), and `human_conventions` (what humans enforce).

### Step 2 — Author candidate learnings (agent reasoning)

From the aggregates, write `$RUN_DIR/learnings.json` (array) using the schema in
`score_learnings.py`'s header. Rules:

- One learning per durable signal — do **not** mirror every aggregate row. Combine related rows.
- **suppression** from `by_category.signal == "suppression"` or a `by_path_prefix` cluster
  (e.g. style on `generated/`, `db/migrate/`, `lockfiles/`).
- **convention** from `human_conventions` (e.g. "%w error wrap", "table-driven tests").
- **focus** from `by_category.signal == "focus"` (e.g. `security-authz` with high acceptance).
- Every learning needs **citations** (the `examples` comment ids back the claim), an honest
  `confidence` (use evidence volume + how clean the signal is), and `evidence_count`.
- Set `scope: repo` unless the signal is clearly org-wide. Optionally hint `materialize_as`.

### Step 3 — Curate (threshold, dedup, skill-vs-memory)

```bash
"$SKILL_DIR/scripts/score_learnings.py" --learnings "$RUN_DIR/learnings.json" \
  --out "$RUN_DIR/curated.json" --summary "$RUN_DIR/learnings-summary.md"
```

Fix any hard validation errors (exit 1) and re-run. Durable convention/focus learnings with
enough evidence become **skill** proposals (a `proposed_skill_dir` is assigned); the rest become
**memory** proposals. `held` learnings (below threshold) are kept for transparency.

### Step 4 — Render the proposals

For each curated learning:

- **`materialize_as: memory`** → append a record to `$RUN_DIR/proposed-memories.jsonl` using the
  repository-memory candidate schema (`subject`, `fact` = the statement, `citations`, `reason`,
  `scope`). These mirror what the memory pipeline would store.
- **`materialize_as: skill`** → author `$RUN_DIR/<proposed_skill_dir>/SKILL.md` as a small
  review-guidance skill: frontmatter (`name` = dir, double-quoted `description` with triggers,
  `user-invocable: true`) + a body stating the convention/focus, when it applies, and concrete
  examples drawn from the citations. This is a **proposal for human review**, never installed by
  this skill.

## Output contract

Write to `$RUN_DIR` and report absolute paths. Produce:

1. **`learnings-summary.md`** — the human-facing deliverable: the promoted-learnings table, the
   skill-vs-memory split, held learnings + why, and a **🚩 Gaps** note (corpus is an export, not a
   live connector; apply path is gapped; small-sample caveats).
2. **`curated.json`** — the validated, thresholded, deduped learnings.
3. **`proposed-memories.jsonl`** and any **`<proposed_skill_dir>/SKILL.md`** proposals.
4. **`aggregates.json`** — the deterministic evidence the learnings were drawn from.

Do not commit, do not open a PR, do not write to any memory store or `.github/skills/`. Surfacing
the proposals as a `Dreaming`-labeled issue via `/artifact-placement` is the separate downstream
step the standard automation prompt runs after this skill.

## Always do

- Ground every learning in corpus citations; set confidence honestly by evidence volume + cleanliness.
- Keep suppression learnings **coverage-neutral** — suppress noise categories/paths, never a
  security-relevant category.
- Note the export-vs-connector caveat and small-sample risk in the summary.

## Never do

- Never apply a learning (write a memory, install a skill, change a review). Shadow mode only.
- Never propose suppressing a `security-*` category — that risks silencing real bugs (PRD guardrail).
- Never invent a learning unsupported by the aggregates, or emit one without citations.
- Never block on user confirmation — this runs unattended.

## Source

Taxonomy and flywheel from `github/codeiq-graph` `CCR_CodeIQ_MVP.md`. Miner/curator structure
adapted from this plugin's `repository-memory-miner` / `repository-memory-curator`. Full gap
analysis: `references/CAPABILITY-GAPS.md`.
