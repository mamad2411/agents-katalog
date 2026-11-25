---
name: pattern-memory
description: >
  This skill manages the self-learning memory layer for the Council plugin.
  It logs deliberation outcomes, tracks model performance (including self-preference
  bias), and maintains the routing model that the smart-router uses to make decisions.
  Triggers automatically after each deliberation to log outcomes, when /council-stats
  is called to report metrics, and when the routing model needs rebuilding.
  Phase 6 implementation — persistent JSON storage with deliberation value
  tracking, routing model support, optimization experiment logging, and
  bidirectional Obsidian vault sync.
version: 0.6.0
---

# Pattern Memory

Manage the self-learning memory layer that makes the Council get smarter over time. Every deliberation outcome is logged, model performance is tracked, and routing rules are rebuilt as data accumulates. Starting in v0.6.0, pattern memory syncs to the MoxyWolf Obsidian vault for cross-linked, human-browsable knowledge persistence.

## Memory File Location

The pattern memory JSON file lives in the user's workspace folder:
`{workspace}/council-memory.json`

where `{workspace}` is the directory containing the installed Council plugin. This file persists between Cowork sessions. No database, no backend — just a JSON file that grows with use.

**Vault mirror (v0.6.0+):** Key data from `council-memory.json` is also written to the Obsidian vault as structured markdown notes. The JSON file remains the authoritative working copy; the vault notes are the durable, cross-linked, human-browsable layer on top. See Operation 7 (Sync to Obsidian Vault).

## Operations

### 1. Initialize Memory

Called on first use or when no `council-memory.json` exists. Creates the file with the empty schema:

```json
{
  "version": "1.3",
  "created": "{current ISO timestamp}",
  "last_updated": "{current ISO timestamp}",
  "last_vault_sync": null,
  "deliberations": [],
  "routing_model": {
    "last_rebuilt": null,
    "sample_size": 0,
    "routing_accuracy": null,
    "rules": []
  },
  "model_performance": {},
  "optimization_log": []
}
```

**How to execute:** Use the Cowork `Write` tool to create `council-memory.json` at the workspace path. If the file already exists, read it and validate the `version` field. Forward-compatible versions: "1.0" and "1.1" files are automatically migrated — add missing fields (`routing_accuracy: null` for 1.0→1.1, `optimization_log: []` for 1.1→1.2, `last_vault_sync: null` for 1.2→1.3) and update the version to "1.3".

### 2. Log Deliberation

Called automatically by the deliberation-engine after Stage 3 completes (Step 8). This is the core write operation.

**Inputs received from the deliberation-engine:**

- `query_text`: the original user query (used for feature extraction, NOT stored)
- `models_used`: array of model IDs that participated
- `stage1_responses`: map of model ID → response text (used for feature extraction, NOT stored)
- `rankings`: map of model ID → rank from peer review
- `chairman`: model ID selected as chairman
- `confidence`: float 0-1 derived from ranking spread
- `consensus_level`: "strong" | "moderate" | "weak" | "split"
- `protocol_used`: "voting" | "consensus"
- `cost_usd`: total cost of the deliberation
- `latency_ms`: total wall-clock time
- `reviewer_rankings_raw`: map of reviewer model ID → their ranking array (used for self-preference detection)
- `synthesis_text`: the chairman's final synthesis (used for value comparison, NOT stored)
- `top_individual_response`: the Stage 1 response from the highest-ranked individual model (used for value comparison, NOT stored)
- `routing_decision`: the smart-router's output for this query (used to track routing accuracy)
- `vault_context_loaded`: boolean indicating whether vault context was injected in Pre-Step A

**Steps:**

1. **Read the memory file** using the Cowork `Read` tool. Parse as JSON. If the file doesn't exist, run Initialize Memory first.

2. **Generate the record ID.** Format: `d_{YYYYMMDD}_{NNN}` where NNN is a zero-padded sequence number. Count existing deliberations with today's date prefix to determine the next sequence number.

3. **Hash the query.** Compute a short hash of the query text for dedup detection. Use the first 8 characters of a SHA-256 hash. Compute it in the workspace bash sandbox: `echo -n "$QUERY" | shasum -a 256 | cut -c1-8` (or `python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest()[:8])' "$QUERY"`). **Never store the full query text.**

4. **Summarize the query.** Generate a natural-language summary of the query in under 80 characters. This is what appears in `/council-stats history`. Example: "Compare microservices vs monolith for early SaaS" — descriptive but not the full query.

5. **Extract query features:**

   ```json
   {
     "length": "<character count of original query>",
     "category": "<classify into one of: architecture_decision, compliance_security, code_implementation, strategy_business, creative_writing, factual_lookup, other>",
     "keywords": ["<signal words found: compare, tradeoffs, should, define, etc.>"],
     "protocol_used": "<voting | consensus>"
   }
   ```

   Classification rules (same as smart-router heuristics):
   - "compare", "tradeoffs", "pros and cons", "architecture", "design" → `architecture_decision`
   - "compliance", "security", "STIG", "CMMC", "NIST", "audit" → `compliance_security`
   - "code", "implement", "function", "bug", "error", "debug" → `code_implementation`
   - "strategy", "business", "market", "pricing", "growth" → `strategy_business`
   - "write", "draft", "creative", "blog", "content" → `creative_writing`
   - "what is", "define", "how does", "explain" → `factual_lookup`
   - Everything else → `other`

6. **Detect self-preference bias.** For each reviewer, check whether they ranked their own response (the one they authored in Stage 1) higher than the consensus ranking. Track this per-model:

   ```json
   {
     "self_preference_detected": {
       "openai/gpt-4o": false,
       "anthropic/claude-sonnet-4": true,
       "google/gemini-2.0-flash": false,
       "x-ai/grok-3": false
     }
   }
   ```

   A model shows self-preference if it ranked the response it authored >=2 positions higher than the aggregate ranking placed it. This feeds into the bias tracking in model_performance.

7. **Compute deliberation value added.** This is the key signal that teaches the router whether deliberation was worth it for this type of query. Compare the chairman's synthesis against the best individual Stage 1 response:

   **Heuristic comparison method (no extra API call):**
   - Count unique substantive points in the synthesis that don't appear in the top individual response
   - Check whether the synthesis includes insights from 3+ models (breadth)
   - Check whether the synthesis flags disagreements the individual response missed (depth)
   - Score: `value_added = (unique_points / total_points) * 0.5 + breadth_bonus * 0.3 + depth_bonus * 0.2`
   - If `value_added` > 0.3 → deliberation added meaningful value
   - If `value_added` < 0.1 → the top individual model would have been sufficient

   Store as a float 0.0-1.0 on the record. This is what the routing model rebuild uses to determine whether deliberation is worthwhile for a given category.

   **Note:** Neither the synthesis text nor the individual response is stored. Only the computed `deliberation_value_added` score is persisted.

8. **Record the routing decision.** Store what the smart-router decided for this query so we can measure routing accuracy over time:

   ```json
   {
     "routing_decision": "deliberate",
     "routing_source": "learned",
     "routing_confidence": 0.91
   }
   ```

   This allows us to answer: "When the router said single_model was sufficient, was it right?" and "When the router said deliberate, did deliberation actually add value?"

9. **Build the deliberation record:**

   ```json
   {
     "id": "d_20260328_001",
     "timestamp": "2026-03-28T14:30:00Z",
     "query_hash": "a1b2c3d4",
     "query_summary": "Compare microservices vs monolith for early SaaS",
     "query_features": {
       "length": 52,
       "category": "architecture_decision",
       "keywords": ["compare", "tradeoffs"],
       "protocol_used": "voting"
     },
     "models_used": ["openai/gpt-4o", "anthropic/claude-sonnet-4", "google/gemini-2.0-flash", "x-ai/grok-3"],
     "rankings": {
       "openai/gpt-4o": 2,
       "anthropic/claude-sonnet-4": 1,
       "google/gemini-2.0-flash": 4,
       "x-ai/grok-3": 3
     },
     "chairman": "anthropic/claude-sonnet-4",
     "confidence": 0.82,
     "consensus_level": "strong",
     "cost_usd": 0.09,
     "latency_ms": 12400,
     "self_preference": {
       "anthropic/claude-sonnet-4": true
     },
     "deliberation_value_added": 0.65,
     "routing_decision": "deliberate",
     "routing_source": "heuristic_learning",
     "routing_confidence": 0.8,
     "vault_synced": false,
     "user_rating": null,
     "outcome": "accepted"
   }
   ```

   Notes:
   - `self_preference` only includes models where bias was detected (keeps the record compact). If no bias detected, the field is an empty object `{}`.
   - `deliberation_value_added` is always computed, even for the first deliberation. It's what teaches the router.
   - `routing_decision`/`routing_source`/`routing_confidence` capture what the router decided so we can measure its accuracy over time.
   - `vault_synced` tracks whether this record has been written to the Obsidian vault (set to `true` by Operation 7).

10. **Update model performance aggregates.** For each model that participated:

   - Increment `deliberations_participated`
   - Recalculate `avg_rank` as running average
   - If model was chairman, increment `chairman_selections`
   - Recalculate `win_rate` = chairman_selections / deliberations_participated
   - Track `self_preference_rate` = count of self-preference detections / deliberations_participated
   - Update `category_ranks` — a map of category → average rank in that category

   After updating, derive `best_categories` (categories where avg rank <= 1.5) and `worst_categories` (categories where avg rank >= 3.5).

   Model performance schema:

   ```json
   {
     "openai/gpt-4o": {
       "deliberations_participated": 23,
       "avg_rank": 1.8,
       "chairman_selections": 7,
       "win_rate": 0.30,
       "self_preference_rate": 0.13,
       "self_preference_count": 3,
       "category_ranks": {
         "architecture_decision": 2.1,
         "factual_lookup": 1.3,
         "code_implementation": 1.5
       },
       "best_categories": ["factual_lookup", "code_implementation"],
       "worst_categories": ["creative_writing"]
     }
   }
   ```

11. **Check if routing model needs rebuilding.** If the total number of deliberations is a multiple of 10 (10, 20, 30...) AND >= 20, trigger a routing model rebuild (see Operation 5 below). Otherwise skip.

12. **Check if vault sync is due.** If the total number of deliberations is a multiple of 5 (5, 10, 15...), trigger a vault sync (see Operation 7 below). Otherwise skip.

13. **Write the updated memory file** using the Cowork `Write` tool. Update the `last_updated` timestamp.

### 3. Capture User Rating

If the user provides feedback after a deliberation — verbal ("great answer", "that wasn't helpful", "nailed it", "way off") or explicit (thumbs up/down if the UI supports it) — update the most recent deliberation's `user_rating` field.

**Rating mapping:**

| User signal | Rating value |
|-------------|-------------|
| "great", "perfect", "nailed it", "exactly", "helpful", thumbs up | `"positive"` |
| "wrong", "off", "not helpful", "missed", "bad", thumbs down | `"negative"` |
| "okay", "fine", "decent", mixed feedback | `"neutral"` |

**Steps:**

1. Read the memory file
2. Find the most recent deliberation record (last in the array)
3. Set `user_rating` to the mapped value
4. If `user_rating` is `"negative"`, also set `outcome` to `"rejected"`
5. If `user_rating` is `"positive"`, set `outcome` to `"accepted"`
6. Write the updated file

**When to trigger:** The deliberation-engine should watch for rating signals in the user's next 1-2 messages after presenting a deliberation result. If the user immediately asks a new question or changes topic, leave the rating as `null` and set outcome to `"unknown"`.

### 4. Export Stats

Called by the `/council-stats` command. Reads the memory file and computes display metrics.

**Summary stats:**

```
Total deliberations: {count}
Total cost: ${sum of all cost_usd}
Average cost: ${mean cost_usd}
Average latency: {mean latency_ms}ms
Average confidence: {mean confidence}

Top categories:
  1. {category} — {count} deliberations
  2. {category} — {count} deliberations
  ...

Rating breakdown:
  Positive: {count} ({percentage}%)
  Negative: {count} ({percentage}%)
  Neutral: {count} ({percentage}%)
  Unrated: {count} ({percentage}%)

Router status: {always-deliberate | learning (N/20 samples) | active (N rules)}
Vault sync: {never | last synced YYYY-MM-DD HH:MM | N records pending sync}
```

**Model leaderboard:**

```
Model Performance:
┌──────────────────────────┬──────┬──────────┬──────────┬───────────────┐
│ Model                    │ Rank │ Win Rate │ Chairman │ Self-Pref Rate│
├──────────────────────────┼──────┼──────────┼──────────┼───────────────┤
│ anthropic/claude-sonnet-4│ 1.4  │ 43%      │ 10       │ 8%            │
│ openai/gpt-4o            │ 1.8  │ 30%      │ 7        │ 13%           │
│ x-ai/grok-3              │ 2.6  │ 17%      │ 4        │ 4%            │
│ google/gemini-2.0-flash  │ 3.2  │ 9%       │ 2        │ 22%           │
└──────────────────────────┴──────┴──────────┴──────────┴───────────────┘

Best by category:
  architecture_decision → anthropic/claude-sonnet-4 (avg rank 1.2)
  factual_lookup → openai/gpt-4o (avg rank 1.3)
  code_implementation → openai/gpt-4o (avg rank 1.5)
```

**History (last 10):**

```
Recent Deliberations:
  d_20260328_003 | 2m ago    | "RBAC for multi-tenant SaaS"           | Chairman: claude-sonnet-4 | ★★★★ | $0.09
  d_20260328_002 | 15m ago   | "AuthenticAaron business viability"    | Chairman: claude-sonnet-4 | ★★★  | $0.11
  d_20260328_001 | 1h ago    | "Microservices vs monolith for SaaS"   | Chairman: gpt-4o          | ★★★★ | $0.07
```

Confidence displayed as stars: ★★★★★ = 0.9-1.0, ★★★★ = 0.7-0.89, ★★★ = 0.5-0.69, ★★ = 0.3-0.49, ★ = 0-0.29

**Cost breakdown:**

```
Cost Report:
  Total spend: $2.34
  This session: $0.27

  By size:
    small (2 models):  avg $0.04  |  12 deliberations
    medium (4 models): avg $0.09  |  18 deliberations
    large (6 models):  avg $0.16  |  3 deliberations

  By stage:
    Stage 1 (Collect):   ~42% of cost
    Stage 2 (Review):    ~38% of cost
    Stage 3 (Synthesis): ~20% of cost

  Budget: ${budget_remaining} remaining of ${budget_total}/month
```

### 5. Rebuild Routing Model

Triggered automatically when deliberation count hits a multiple of 10 (and >= 20). Can also be triggered manually via `/council-config rebuild-router`.

**Algorithm:**

1. Read all deliberation records from memory
2. Group by `query_features.category`
3. For each category with >= 3 samples:
   a. Calculate **deliberation value score** (see formula below)
   b. If value score > 0.6 → rule: `deliberate` for this category
   c. If value score < 0.4 → rule: `single_model` for this category, with `preferred_model` set to the model with the best avg_rank in that category
   d. If between 0.4-0.6 → no rule yet (keep deliberating to gather more signal)
4. For each rule, set confidence = min(0.95, (sample_count / total_deliberations) * value_score * 2)
5. Write the new rules to `routing_model` in the memory file
6. Update `last_rebuilt` timestamp and `sample_size`
7. Compute **routing accuracy**: for all past deliberations where the router made a decision, check whether the decision aligned with the outcome. If `routing_decision` was `single_model` but `deliberation_value_added` > 0.3 (deliberation would have helped), that's a miss. If `routing_decision` was `deliberate` but `deliberation_value_added` < 0.1, that's waste. Log accuracy percentage.

**Value score formula:**

```
value_score = (
  0.35 * avg_deliberation_value_added +
  0.25 * positive_rating_rate +
  0.20 * avg_confidence +
  0.10 * (1 - ranking_spread_normalized) +
  0.10 * (1 - chairman_consistency)
)
```

Where:
- `avg_deliberation_value_added` = mean `deliberation_value_added` across deliberations in this category — **the primary signal.** This directly measures whether deliberation produced a better answer than the best individual model would have.
- `positive_rating_rate` = count of positive ratings / count of rated deliberations (unrated excluded)
- `avg_confidence` = mean confidence across deliberations in this category
- `ranking_spread_normalized` = std_dev of rankings / max_possible_std_dev (high spread = models disagreed significantly, which often means deliberation surfaced valuable disagreements)
- `chairman_consistency` = how often the same model wins chairman for this category (high consistency = one model dominates, suggesting single-model might suffice — hence the `1 -` inversion)

**Why `deliberation_value_added` is weighted highest:** User ratings are sparse (many deliberations go unrated) and subjective. Confidence scores measure model agreement, not answer quality. The value-added score directly answers the question the router needs: "Did involving multiple models produce something meaningfully better than the best single model would have?"

**Garbage collection (runs as part of rebuild):**

When the deliberation count exceeds 500, archive old records to keep the file manageable:

1. Keep the most recent 200 deliberations in full
2. For records 201-500: compress to summary records (keep id, timestamp, category, rankings, deliberation_value_added, cost — drop query_summary and keywords)
3. For records 500+: aggregate into the model_performance stats and remove individual records

This keeps the file under ~200KB even with heavy use.

### 6. Log Optimization Experiment

Called by the `/council-optimize` command after each experiment in the autoresearch loop.

**Inputs received from the optimization loop:**

- `experiment_id`: format `opt_YYYYMMDD_NNN`
- `run_id`: groups experiments from the same optimization run, format `run_YYYYMMDD_HHmmss`
- `variable_modified`: which prompt variable was changed
- `modification_type`: one of `sharpen`, `constrain`, `expand_scope`, `restructure`, `remove`
- `description`: human-readable description of the change
- `baseline_pass_rate`: pass rate before modification (float 0-1)
- `modified_pass_rate`: pass rate after modification (float 0-1)
- `criteria_delta`: object mapping each criterion (C1-C5) to its change in pass rate
- `decision`: `keep`, `revert`, or `skip`
- `cost_usd`: cost of running this experiment
- `benchmark_count`: number of benchmark queries used
- `benchmark_ids`: array of deliberation record IDs used as benchmarks

**Steps:**

1. Read the memory file
2. If `optimization_log` doesn't exist (pre-1.2 file), create it as an empty array and update the version to "1.2"
3. Append the experiment record to `optimization_log`
4. Update `last_updated` timestamp
5. Write the updated file

**Stats integration:** The `/council-stats` command can display optimization history:

```
Optimization History:
  Last run: 2026-03-28 | 12 experiments | baseline 68% → final 84%
  Changes kept: 4 | reverted: 5 | skipped: 3
  Total optimization spend: $1.08
```

### 7. Sync to Obsidian Vault

Writes key pattern memory data to the MoxyWolf Obsidian vault as structured, cross-linked markdown notes. The vault becomes the human-browsable, searchable layer on top of the JSON working copy.

**Trigger conditions:**
- Automatically after every 5th deliberation (checked in Operation 2, step 12)
- Manually via `/council-config sync-vault`
- Automatically during routing model rebuild (Operation 5)

**Vault discovery:** Same resolution as deliberation-engine Pre-Step A:
1. Check Cowork workspace mount for `_System/MEMORY.md`
2. Check Google Drive mount path
3. Search Google Drive via `google_drive_search` for `MoxyWolf Vault`
4. If none found: skip sync, log warning, set `last_vault_sync` to `null` with note `"vault_unavailable"`

**If vault is found, write/update three files via memory-system Sub-operation B:**

**a. Model Performance Reference Note**

Pass to memory-system:
- `record_type: "model_performance"`
- `content`: formatted leaderboard table (same format as Export Stats), category strengths per model, self-preference rates, total deliberations per model
- `frontmatter`:
  ```yaml
  title: "Council Model Performance"
  date: YYYY-MM-DD
  type: reference
  tags: [council, model-performance, ai-verification]
  status: active
  ```
- This is a living reference document — always overwritten with latest data

**b. Routing Intelligence Note**

Pass to memory-system:
- `record_type: "routing_intelligence"`
- `content`: current routing rules with confidence levels, routing accuracy percentage, categories that benefit most from deliberation vs. single-model, cost savings achieved from single-model routes, router mode and learning status
- `frontmatter`:
  ```yaml
  title: "Council Routing Intelligence"
  date: YYYY-MM-DD
  type: reference
  tags: [council, smart-router, routing]
  status: active
  ```
- Living reference, always overwritten

**c. Deliberation Log Entries**

For each deliberation record where `vault_synced: false`:
- Pass to memory-system as `record_type: "deliberation_log_entry"`
- Row data: `| {id} | {date} | {query_summary} | {chairman short name} | {confidence_stars} | ${cost} | {rating or "—"} |`
- After successful write, set `vault_synced: true` on the record in `council-memory.json`

**After sync completes:**
1. Update `last_vault_sync` timestamp in the memory file's root object
2. Write the updated memory file
3. Log to user (if interactive): "Vault synced: updated model performance, routing intelligence, and {N} new deliberation log entries."

**Error handling:** If vault write fails, log warning but don't fail. The JSON file is authoritative; vault notes are best-effort persistence.

## Privacy

- **Query content is never stored** — only hashed fingerprints, category classifications, and keyword flags
- The full deliberation text stays ephemeral (in the Cowork conversation, not the file)
- Only structural metadata needed for learning is persisted
- Self-preference tracking uses model IDs and boolean flags only — no response content

## Schema Reference

See `references/memory-schema.md` for the full JSON Schema used to validate the memory file.

## Integration Points

- **deliberation-engine Pre-Step A**: loads vault context for Stage 1 prompt enrichment (reads via memory-system Sub-operation A)
- **deliberation-engine Pre-Step B**: smart-router calls pattern-memory to read routing rules
- **deliberation-engine Step 8**: calls Log Deliberation after every pipeline run (includes value-added computation)
- **deliberation-engine Step 8c**: watches for user rating signals after presenting results
- **deliberation-engine Step 8d**: writes vault decision record via memory-system Sub-operation B
- **smart-router Step 2**: reads `routing_model.rules` and `model_performance` for learned routing and dynamic model selection
- **smart-router Step 4d**: reads `self_preference_rate` for bias warnings
- **obsidian-update Step 2.5**: Council Verification Gate — pattern-memory provides deliberation history and model performance data when obsidian-update requests Council verification of extraction quality
- **memory-system Sub-operation B**: accepts structured data from pattern-memory Operation 7 and writes to vault in correct format with frontmatter validation and deduplication
- **Vault sync (Operation 7)**: writes model performance, routing intelligence, and deliberation logs to the Obsidian vault every 5 deliberations
- **/council-stats command**: calls Export Stats for all display modes (now includes vault sync status)
- **/council-config rebuild-router**: manually triggers Rebuild Routing Model (also triggers vault sync)
- **/council-config sync-vault**: manually triggers vault sync
- **/council-config set router**: changes router mode (learned/always_deliberate/always_shortcut)
- **/council-optimize**: calls Log Optimization Experiment after each autoresearch experiment; reads deliberation records for benchmark selection
