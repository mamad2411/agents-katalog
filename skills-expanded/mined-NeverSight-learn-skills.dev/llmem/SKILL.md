---
name: llmem
description: >
  Manage LLMem — structured memory system with SQLite-backed factual memory,
  semantic search, and background dreaming (decay, boost, promote, merge).
  Use when the user wants to: (1) add, search, update, or delete memories,
  (2) generate context for injection, (3) check memory stats, (4) run background
  consolidation/dream. Triggers on: "memory", "remember", "recall", "llmem",
  "memories", "forget", "consolidate memories", "dream".
license: MIT
---

# LLMem

LLMem is a structured memory system (Go binary). It stores factual memories in SQLite with optional embedding-based semantic search via Ollama (nomic-embed-text). Semantic search uses a sqlite-vec HNSW ANN index for sub-linear retrieval, with automatic fallback to brute-force cosine similarity if the sqlite-vec extension is not available. Memories can be connected via typed relations (`related_to`, `supersedes`, `contradicts`, `depends_on`, `derived_from`). A background dreaming/consolidation system (light, deep, REM phases) runs automatically via systemd timer to decay idle memories, boost frequent ones, promote high-value ones, and merge near-duplicates.

## Installation

- **CLI:** `~/.local/bin/llmem`
- **Config:** `~/.config/llmem/config.yaml`
- **DB:** `~/.config/llmem/memory.db`
- **Ollama:** `http://localhost:11434` (local, for embeddings)

## Session Adapter Configuration

LLMem uses a session adapter to read conversation transcripts for memory extraction. Set `session.adapter` in config.yaml:

- `opencode` (default) — reads from `~/.local/share/opencode/opencode.db`. Auto-selected if the database exists.
- `copilot` — reads from `~/.copilot/session-state/`. Auto-selected if only Copilot session data exists. Full transcripts require `--share`.
- `none` — no adapter. Context injection still works, but transcript extraction returns `no_transcript`.

```yaml
# For Copilot CLI:
session:
  adapter: copilot
copilot:
  state_dir: ~/.copilot/session-state
  share_dir: .
```

`llmem init` auto-detects the adapter type based on which session state directory exists.

## Memory Types

| Type | Use for |
|------|---------|
| fact | Objective truths, definitions, state of the world |
| decision | Choices made and their rationale |
| preference | User preferences, style choices |
| event | Things that happened at a point in time |
| project_state | Current status of a project or system |
| procedure | How-to knowledge, step sequences |
| conversation | Notable conversation outcomes or commitments |
| self_assessment | Structured introspective records — error patterns, behavioral corrections, recurring mistakes, proposed procedural updates |

## Error Taxonomy

Self-assessment memories are categorized using a standard error taxonomy. Each category identifies a class of mistake that the introspection system tracks for pattern detection:

| Category | Description |
|----------|-------------|
| NULL_SAFETY | Missing null/None/undefined checks before property access or method calls |
| ERROR_HANDLING | Missing try/except, bare except, swallowed errors, unhandled promise rejections |
| OFF_BY_ONE | Boundary errors, wrong loop bounds, fencepost errors |
| RACE_CONDITION | Concurrency issues, async/await problems, missing locks |
| AUTH_BYPASS | Missing auth checks, SSRF, injection vulnerabilities, security oversights |
| DATA_INTEGRITY | Stale derived fields, out-of-sync caches/embeddings/indexes, source-of-truth divergence |
| MISSING_VERIFICATION | Skipped test steps, unverified outputs, assumed-it-works |
| EDGE_CASE | Unhandled empty input, unexpected types, boundary values |
| PERFORMANCE | N+1 queries, unnecessary recomputation, memory leaks |
| DESIGN | Architectural issues, wrong abstraction level, coupling problems |
| REVIEW_PASSED | Clean review with no findings — positive outcome for tracking purposes |

## Structured self_assessment Format

Self-assessment memories follow a structured format with nine fields:

| Field | Required | Description |
|-------|----------|-------------|
| Category | Yes | Taxonomy category from the Error Taxonomy above (e.g. `NULL_SAFETY`, `ERROR_HANDLING`) |
| Context | No | Where and when — file, task, session date |
| What_happened | Yes | Behavioral description, not narrative |
| Outcomes | No | What were the results? Did things work on first try or require iterations? |
| What_caught_it | No | How the error was discovered (`self-review`, `test`, `user`, `CI`) |
| Estimates_vs_actual | No | Was the complexity assessment accurate? Did tasks take more or less effort? |
| Recurring | No | `yes` or `no`; if yes, reference past self_assessment IDs |
| Proposed_update | No | Specific procedural directive to prevent recurrence |
| Iteration_count | No | How many attempts before success (integer). 1 = first try, 2 = one retry, etc. |

## Key Commands

```bash
# Add a memory
llmem add --content "content" --type fact
llmem add --content "prefer dark theme" --type preference --confidence 0.9

# Search memories (hybrid RRF fusion by default)
llmem search "query"
llmem search "query" --type decision --limit 5
llmem search "query" --fts-only        # FTS5 keyword search only (no embedder needed)
llmem search "query" --semantic-only   # Semantic (embedding) search only (requires embedder)
llmem search "query" --valid-only     # Only show valid (non-expired) memories

# List all
llmem list
llmem list --type fact --limit 20
llmem list --all                       # Include expired memories

# Get specific memory (read-only, does not update access stats)
llmem get <id>

# Update a memory
llmem update <id> --content "new content"
llmem update <id> --confidence 0.95
llmem update <id> --summary "short summary"
llmem update <id> --metadata '{"key": "value"}'

# Invalidate (soft-delete — marks as expired)
llmem invalidate <id> --reason "no longer relevant"

# Delete permanently
llmem delete <id>

# Stats
llmem stats

# Context injection for sessions
llmem context --session-id <session_id>              # Inject context for a new session
llmem context --compacting --session-id <session_id>  # Inject key memories during compaction

# Session lifecycle hooks
llmem hook --type idle --session-id <session_id>      # Memory extraction + introspection
llmem hook --type created --session-id <session_id>   # Context injection on session start
llmem hook --type ending --session-id <session_id>    # Automatic introspection on session end
llmem hook --type ending --session-id <session_id> --model glm-5.1:cloud --base-url http://localhost:11434
llmem hook --type compacting --session-id <session_id># Context during compaction

# Dream — background consolidation (decay, boost, promote, merge)
llmem dream                                               # Preview all phases (dry-run)
llmem dream --apply                                       # Execute all phases
llmem dream --phase light                                 # Run only the light phase
llmem dream --phase deep                                  # Run only the deep phase
llmem dream --phase rem                                   # Run only the REM phase
llmem dream --apply --phase deep                          # Apply only the deep phase
llmem dream --apply --report /path/to/report.html         # Generate HTML dream report

# Learn a lesson from a wrong→right correction
llmem learn --wrong "called wrong function" --right "call correctFunction() instead" --context "handler.py:42"

# Introspect — analyze a failure and store self_assessment memory

# Manual mode: specify fields directly
llmem introspect --category NULL_SAFETY --what-happened "missing null check" --context "handler.py:42" --caught-by self-review --proposed-fix "always check for None before .field"
llmem introspect --category NULL_SAFETY --what-happened "missing null check" --model glm-5.1:cloud --base-url http://localhost:11434

# Automatic mode: introspect a session transcript or arbitrary text
llmem introspect --auto --session <session-id>                      # Read transcript from OpenCode adapter
llmem introspect --auto --text "Encountered a null pointer error"   # Introspect arbitrary text
llmem introspect --auto --session <session-id> --model glm-5.1:cloud --base-url http://localhost:11434

# Track review findings as self_assessment memories (automatic post-review hook)
llmem track-review --single --category NULL_SAFETY --context "handler.py:42"  # Single finding (uses --single flag)
llmem track-review --findings /tmp/review-findings.json --context "handler.py"  # Batch mode: persist findings from JSON file
llmem track-review --clean                                                # Invalidate all existing track-review memories
llmem track-review                                                         # Clean review (no findings) → creates REVIEW_PASSED memory

# Export/import
llmem export --output memories.json
llmem import memories.json

# Embedding quality metrics
llmem metrics

# Initialize config and database
llmem init
llmem init --ollama-url http://localhost:11434
```

## Relations

Memories can be linked by typed relations: `supersedes`, `contradicts`, `depends_on`, `related_to`, `derived_from`.

Relations are managed internally by the dream system and extraction pipeline. The Go backend supports relation traversal in search (exposed via the `Retriever` API) but the CLI does not yet expose `--traverse-relations` as a flag.

### Multi-Signal Reranking

After RRF fusion, search results are automatically reranked using a blend of the RRF score and four weighted signals:

```
final_score = rrf_score * (1 - blend) + weighted_signal * blend
```

**Default blend factor: 0.3** (70% RRF, 30% signals).

**Signals and weights:**

| Signal | Weight | Formula |
|--------|--------|---------|
| Confidence | 0.4 | Direct use of `confidence` field (0.0–1.0, default 0.0) |
| Recency | 0.3 | `exp(-0.01 * days_since_access)` (0.0 if never accessed) |
| Access frequency | 0.2 | `log(1 + access_count / max(age_days, 1))` (0.0 if never accessed) |
| Type priority | 0.1 | Lookup in `TYPE_PRIORITY` dict (default 1.0 for unknown types) |

**Type priority weights:**

| Type | Priority |
|------|----------|
| decision | 1.2 |
| preference | 1.1 |
| procedure | 1.1 |
| fact | 1.0 |
| project_state | 1.0 |
| self_assessment | 1.0 |
| event | 0.9 |
| conversation | 0.7 |

## Important Notes

- **Go binary** — `llmem` is now a compiled Go binary at `~/.local/bin/llmem`, symlinked from `/usr/local/bin/llmem`. No Python virtualenv needed.
- **Invalidate, don't delete** unless the memory was wrong. Invalidated memories stay for reference but aren't returned in searches.
- **Embeddings** require Ollama running with `nomic-embed-text` pulled. If Ollama is down, semantic search falls back to FTS5-only.
- **ANN vector index** — semantic search uses sqlite-vec (`vec0` virtual table) for fast ANN retrieval, with automatic fallback to brute-force cosine similarity if sqlite-vec is not available.
- **Confidence** is 0.0-1.0. Higher = more certain. Facts from the user directly should be 0.9+, auto-extracted should be 0.7.
- **Context generation** is what gets injected into the system prompt for context. Use `llmem context --session-id <id>` to preview what gets injected.
- **Session hooks** use `llmem hook --type <idle|created|ending|compacting> --session-id <id>`. The idle hook processes the session's transcript, extracts memories, and runs introspection automatically. The ending hook performs automatic introspection on the session transcript and stores a `self_assessment` memory; use `--model` and `--base-url` to configure the LLM for introspection.
- **Access tracking** — `llmem get` is read-only and does not update `access_count` or `accessed_at`. Search operations automatically track access — each returned result's `access_count` and `accessed_at` are updated (best-effort).
- **Calibration status metadata** — procedure memories created by behavioral insights receive `calibration_status` (trend: `decreasing`, `stable`, or `increasing`) and `calibrated_at` metadata when calibration runs. Stale procedures get `stale_procedure: true` and `stale_at` metadata. These are visible via `llmem get <id>`.
- **Review outcome tracking** — `llmem track-review` persists review findings as `self_assessment` memories. Three modes: `--single` for a single finding, `--findings <file>` for batch from JSON, or no flags for a clean review (creates `REVIEW_PASSED` memory). Use `--clean` to invalidate all existing track-review memories before storing new ones.


## Dream — Background Consolidation

The dream system is an automated memory maintenance pipeline that runs three phases:

- **Light** — finds near-duplicates using cosine similarity (configurable threshold, default 0.92). Produces merge candidates for the deep phase.
- **Deep** — decays idle memories (confidence decreases over time), boosts frequently accessed memories, promotes high-scoring memories, and merges near-duplicates using LLM-assisted merge with fallback to concatenation.
- **REM** — extracts themes and clusters from memory, writes a human-readable dream diary to `~/.config/llmem/dream-diary.md`. Self-assessment memories are grouped by error taxonomy category (e.g. "2 self_assessment memories about NULL_SAFETY") for pattern detection. When a category has 3+ occurrences (configurable via `skill_patch_threshold`), the REM phase generates three outputs: (1) a **procedural memory** (Tier 1 — automatic, low confidence), (2) a **behavioral insight** entry in `proposed-changes.md` (Tier 2 — human review), and (3) a **skill patch** entry in `proposed-changes.md` marked with `[SKILL PATCH]` (Tier 3 — human review). Skill patches are structured markdown snippets with Detection Rule, Checklist, Pitfall, and Verification sections that can be appended to existing skills or used as mini-skills. They are NOT auto-applied — they require human review and deployment. When behavioral insights are generated, **calibration tracking** compares self_assessment error rates (or average iteration counts) before and after each adaptation was introduced, marking them as effective (decreasing) or ineffective (stable/increasing). Procedure memories that are never accessed and older than `stale_procedure_days` are aggressively decayed (confidence reduced at double the normal decay rate). The dream diary includes a `### Calibration` section with per-category effectiveness and stale procedure counts.

**Default mode is dry-run** — use `--apply` to actually make changes. Without it, `llmem dream` only previews what would happen. Use `--report /path/to/report.html` to generate an HTML dream report.

**Scheduling**: A systemd user timer (`llmem-dream.timer`) runs `llmem dream --apply` nightly at 3am. See `harness/llmem-dream.service` and `harness/llmem-dream.timer`.

**Dream config** lives under the `dream:` key in `~/.config/llmem/config.yaml`:

| Key | Default | Description |
|-----|---------|-------------|
| `similarity_threshold` | 0.92 | Cosine similarity for near-duplicate detection |
| `decay_rate` | 0.05 | Confidence reduction per decay interval |
| `decay_interval_days` | 30 | Days per decay interval |
| `decay_floor` | 0.3 | Minimum confidence after decay |
| `confidence_floor` | 0.3 | Memories at or below this are invalidated |
| `boost_threshold` | 5 | Access count that triggers confidence boost |
| `boost_amount` | 0.05 | Confidence boost amount |
| `diary_path` | ~/.config/llmem/dream-diary.md | Path to dream diary file |
| `report_path` | (none) | Path for HTML dream report output |
| `behavioral_threshold` | 3 | Minimum self_assessment occurrences to trigger behavioral insight |
| `behavioral_lookback_days` | 30 | Days of self_assessment memories for behavioral insights |
| `auto_link_threshold` | (none) | Cosine similarity threshold for auto-linking related memories |
