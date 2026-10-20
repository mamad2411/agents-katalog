---
name: deliberation-engine
description: >
  This skill should be used when the user asks to "deliberate on a question",
  "get multiple AI perspectives", "run the council", "multi-model consensus",
  "compare AI answers", "get a second opinion from other models",
  "what do multiple models think", or any request that benefits from
  structured multi-model deliberation rather than a single-model response.
  Also trigger when the user uses /deliberate or mentions "council".
version: 0.7.0
---

# Deliberation Engine

Run a 3-stage multi-model deliberation pipeline against OpenRouter. Collect independent responses from multiple LLMs, have them peer-review each other anonymously, then synthesize a final consensus answer. All model calls happen via the bundled `scripts/openrouter_dispatch.py` helper, which fans out N HTTPS requests in parallel from the Cowork workspace bash sandbox.

## Prerequisites

Requires a usable OpenRouter API key. The dispatch helper (`scripts/openrouter_dispatch.py`) resolves it through `scripts/openrouter_key.py`, which checks (1) the `OPENROUTER_API_KEY` env var, (2) `$OPENROUTER_KEY_FILE`, then (3) the team-shared file at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env` — auto-discovered in either the Cowork bash sandbox vault mount or a native macOS Google Drive mount.

Verify before first use:

```bash
python3 "${COUNCIL_PLUGIN}/scripts/openrouter_key.py" --where
```

This prints the source label and path the loader resolved (e.g. `Cowork bash sandbox mount (/sessions/.../MoxyWolf Vault/.../openrouter.env)`). If it instead prints an error listing every path it tried, halt and tell the user:

- The MoxyWolf Vault is not mounted in this Cowork session — add it via Cowork → Folders, **or**
- The vault key file is missing or still has the placeholder value — ask Dorian for the team-shared key and paste it into `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env` (single line: `OPENROUTER_API_KEY=sk-or-v1-...`).

No 60-second timeout. The dispatch helper's default timeout is 180s per call, so models that need real reasoning time (DeepSeek R1, o1, Claude Opus extended thinking) are usable again.

## Pipeline Overview

```
User Query
    │
    ▼
┌─────────────────────────┐
│ PRE-STEP A: VAULT CONTEXT│  Load operational context from Obsidian vault
│ Read MEMORY.md, project  │  Enrich Stage 1 prompts with institutional knowledge
│ knowledge, past delibs   │  Optional — pipeline works without vault
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ PRE-STEP B: ROUTE QUERY  │  Smart router decides: full deliberation or single model?
│ Heuristic or learned     │  Uses pattern memory for data-driven routing
│ routing                  │
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ STAGE 1: COLLECT        │  4 parallel HTTPS calls via openrouter_dispatch.py
│ Each model responds     │  Models get role-specific system prompts
│ independently           │  + vault context block (if loaded)
│                         │  See references/stage-prompts.md for prompts
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ STAGE 2: PEER REVIEW    │  4 parallel calls — each model reviews the other 3
│ Anonymous evaluation    │  Responses labeled "Response A/B/C" (no model names)
│ Adaptive protocol       │  Voting for reasoning, consensus for knowledge
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ STAGE 3: SYNTHESIZE     │  1 call — highest-ranked model is chairman
│ Chairman merges best    │  Gets all responses + rankings + original query
│ insights into one       │  Flags agreements (high confidence) and disagreements
└─────────┬───────────────┘
          │
          ▼
┌─────────────────────────┐
│ STEP 8: LOG + VAULT     │  Log to pattern-memory JSON
│ Write decision record   │  Write vault decision record (if vault loaded)
│ to Obsidian vault       │  Append to deliberation log
└─────────────────────────┘
```

## Execution Steps

### Pre-Step A: Load Vault Context (Obsidian Integration)

Before routing or collecting responses, check whether the MoxyWolf Obsidian vault is accessible. If it is, load context that will enrich the deliberation.

**Vault discovery (same resolution order as obsidian-update skill):**

1. Check if the Cowork workspace mount contains `_System/MEMORY.md` at any depth — that's the vault root
2. Check `/sessions/*/mnt/GoogleDrive-dorianc@moxywolf.com/Shared drives/MoxyWolf Shared Files/MoxyWolf Vault/`
3. Search Google Drive via `google_drive_search` for folder `MoxyWolf Vault`
4. If none found: proceed without vault context. Set `vault_context_loaded: false`. The pipeline works fine without it — vault context is additive, not required.

**If vault is found, call the memory-system's Council Integration Sub-operation A:**

The memory-system returns a structured context block containing:

1. **`memory_summary`** (~500 tokens) — operational context from MEMORY.md: active projects, current priorities, shorthand decoder, relationships. Gives models awareness of Dorian's current situation and terminology.
2. **`project_context`** — if the user's query references a known project (match against project names in MEMORY.md or folder names in `${VAULT}/Projects/`), the relevant project index summary: current phase, recent decisions, open questions.
3. **`recent_deliberations`** — last 5 entries from `${VAULT}/_Shared Knowledge/Agents and Plugins/council-deliberation-log.md` for continuity.

**How context is injected into Stage 1:**

Add an `[OPERATIONAL CONTEXT]` block to the system prompt for every Stage 1 model call. Insert it between the role prompt and the user query:

```
[OPERATIONAL CONTEXT — from MoxyWolf Obsidian Vault]
Active projects: {list from memory_summary}
Current priorities: {P0/P1 from memory_summary if available}
Relevant project context: {project_context summary, or "No specific project match"}
Recent Council decisions: {last 3 deliberation summaries from recent_deliberations, or "No prior deliberations"}
[END CONTEXT]
```

Keep the context block under 500 tokens. Summarize aggressively. The goal is orientation, not data dump.

**Set `vault_context_loaded: true`** and store `${VAULT}` path on the pipeline state. These are used by Step 8d to determine whether to write a vault decision record after the deliberation.

---

### Pre-Step B: Route the Query

Before entering the pipeline, call the smart-router skill to decide whether this query warrants full deliberation.

1. **Skip routing if:** the user explicitly called `/deliberate` (the command itself implies "I want full deliberation"). In this case, set `routing_decision: "explicit_command"` and proceed to Step 1.

2. **Call the smart-router.** Pass the user's query text. The router returns a decision object (see smart-router SKILL.md for the full schema).

3. **If `decision` is `single_model`:** Skip the full pipeline. Jump to the **Single-Model Shortcut** (below).

4. **If `decision` is `deliberate`:**
   - Use `recommended_models` from the router if provided (overrides default lineup unless user specified `--models`)
   - Use `recommended_protocol` as a hint for Step 3
   - Carry `query_features` through to Step 8 for logging
   - Note any `bias_warnings` for inclusion in the output footer
   - Proceed to Step 1.

### Single-Model Shortcut

When the router decides a single model is sufficient, bypass the full pipeline:

1. Select the model from `routing_decision.recommended_models[0]`
2. Call `OPENROUTER_CREATE_CHAT_COMPLETION` with the Strategist system prompt (or the role prompt matching the model's slot if it has one). **If vault context is loaded**, include the `[OPERATIONAL CONTEXT]` block in the system prompt.
3. Present the response in a simplified format:

```
## Council Response (Single Model)

**Query:** [original query]
**Model:** [model name]
**Routed by:** [routing_source] (confidence: [routing_confidence])

---

[Model's response]

---

**Cost:** $[cost] | **Router status:** [learning_status]
💡 *The router determined full deliberation wasn't needed for this query type. Use `/deliberate` to force a full council.*
```

4. **Log the outcome.** Even single-model responses get logged to pattern memory so the router can learn from the outcome:
   - Set `deliberation_value_added: null` (not computable — there was no multi-model synthesis to compare against. The schema allows null for single-model routes. The routing model rebuild excludes null records when calculating category value scores.)
   - Set `routing_decision: "single_model"`, `routing_source`, `routing_confidence` from the router
   - Record `cost_usd`, `latency_ms`, `models_used: [single_model_id]`
   - Watch for user rating as usual (Step 8c)
   - If the user subsequently re-asks the same question with `/deliberate` (forcing full council), that's a strong negative signal for the routing decision — update the original record's `outcome` to `"rejected"` and `user_rating` to `"negative"`

5. **Return.** Do not proceed to Step 1.

---

### Step 1: Resolve Model Lineup

Read the model lineup from `references/model-configs.md`. The default is 4 models. If the user specified `--models` or `--size`, adjust accordingly. If the smart-router provided `recommended_models` in the Pre-Step, use that lineup instead (but respect explicit `--models` overrides from the user).

Map each model to its role slot:

| Slot | Purpose |
|------|---------|
| Analyst | Precise, structured, data-driven responses |
| Strategist | Nuanced, contextual, sees the bigger picture |
| Challenger | Contrarian perspective, finds edge cases |
| Synthesist | Cross-domain lateral thinking |

### Step 2: Stage 1 — Collect Responses

Build a jobs file with one entry per model. Each job has:

- `id`: slot label, e.g. `"stage1-analyst"` (used as the output filename)
- `model`: the OpenRouter model ID from the lineup (e.g., `openai/gpt-4o`)
- `messages`: array with a system message (role-specific prompt from `references/stage-prompts.md`, **plus the `[OPERATIONAL CONTEXT]` block if `vault_context_loaded: true`**) and a user message (the query, plus any context the user provided)
- `temperature`: 0.7 (balanced creativity)
- `max_tokens`: 2000

Write the jobs array to `${WORKSPACE_OUTPUTS}/council-{session_id}/stage1-jobs.json`, then dispatch via the bundled helper:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/openrouter_dispatch.py" \
    --jobs "${WORKSPACE_OUTPUTS}/council-${SID}/stage1-jobs.json" \
    --out  "${WORKSPACE_OUTPUTS}/council-${SID}/stage1" \
    --timeout 180 \
    --max-workers 6
```

The helper writes `stage1/{id}.json` for each job (containing the full OpenRouter response on `ok: true`, or an error message on `ok: false`) plus a `stage1/_summary.json` with per-job timing. Read each `{id}.json` to extract `response.choices[0].message.content`.

Label them internally as Response A, B, C, D — strip all model identifiers before peer review.

**If `--deep` flag is set (MoA two-round collection):**

After Round 1 completes, run a second collection round. In Round 2, each model receives:

- Its original role-specific system prompt
- The original user query
- **All Round 1 responses** (anonymized as "Perspective A/B/C/D") prepended to the user message with this header:

```
The following perspectives were independently generated by other analysts. Use them as additional context — incorporate, challenge, or build on them as you see fit. Then provide your own complete response to the question.

[Perspective A]
{round1_response_A}

[Perspective B]
{round1_response_B}

[Perspective C]
{round1_response_C}

[Perspective D]
{round1_response_D}

---

Now provide your response:
```

Write a new `stage1-round2-jobs.json` with the same 4 models but the enriched messages, then dispatch via `openrouter_dispatch.py` with `--out stage1-round2/`. The Round 2 responses replace the Round 1 responses for all downstream steps (peer review and synthesis operate on the enriched Round 2 output).

This is the Mixture-of-Agents (MoA) pattern: each agent sees all previous layer outputs before producing its own. Research shows this yields stronger responses than independent generation, particularly for complex reasoning queries. Cost: adds 4 extra API calls (~$0.03-0.05).

The `--deep` flag can be combined with `--thorough` (CI round would run on the Round 2 responses).

### Step 3: Classify Query Type

Before Stage 2, classify the query to select the review protocol:

- **Reasoning query** (architecture decisions, tradeoffs, strategy, "should I", "compare", "best approach"): Use **voting protocol**
- **Knowledge query** (factual, compliance, definitions, "what is", "define", "how does"): Use **consensus protocol**
- **Default**: Voting (larger accuracy gain per ACL 2025 research)

This classification is done by Claude locally — no extra API call needed. Examine the query keywords and intent.

### Step 4: Stage 2 — Peer Review

Build 4 more jobs in `stage2-jobs.json`. Each job has:

- `id`: `"stage2-reviewer-{slot}"`
- `model`: the same model ID that authored the corresponding Stage 1 response (so each model reviews the *other* three)
- `messages`: a system message with the review prompt from `references/stage-prompts.md` (voting or consensus variant based on Step 3), then a user message containing the original query + the three anonymized peer responses ("Response A/B/C") — **exclude the reviewer's own response**

**Voting protocol** instructions: "Rank the three responses from best to worst on accuracy, completeness, and relevance. Return a JSON object: `{rankings: [{response: 'A', rank: 1, rationale: '...'}, ...]}`"

**Consensus protocol** instructions: "Identify points of agreement and disagreement across the three responses. For each claim, note whether it appears in multiple responses. Return a JSON object: `{agreements: [...], disagreements: [...], synthesis_notes: '...'}`"

Dispatch in parallel:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/openrouter_dispatch.py" \
    --jobs "${WORKSPACE_OUTPUTS}/council-${SID}/stage2-jobs.json" \
    --out  "${WORKSPACE_OUTPUTS}/council-${SID}/stage2" \
    --timeout 180
```

Read the JSON output from each reviewer for ranking aggregation in Step 5.

### Step 5: Aggregate Scores

Parse the Stage 2 responses.

**For voting:** Calculate average rank for each response across all reviewers. The response with the lowest average rank (best) determines the chairman model for Stage 3.

**For consensus:** Identify claims that appear in 3+ responses (high confidence) vs. claims with disagreement (flag for synthesis). Select the model whose response had the most unique agreements as chairman.

Format the score matrix for inclusion in the Stage 3 prompt.

### Step 6: Stage 3 — Synthesis

Build a single-job `stage3-jobs.json` using the chairman model (highest-ranked from Stage 2). The chairman receives:

- The original query
- All 4 responses with their labels
- The aggregate rankings or consensus map
- The synthesis prompt from `references/stage-prompts.md`

Set `max_tokens: 3000` in the job (synthesis needs room to be thorough), then dispatch via the same helper (it handles single jobs identically to batches):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/openrouter_dispatch.py" \
    --jobs "${WORKSPACE_OUTPUTS}/council-${SID}/stage3-jobs.json" \
    --out  "${WORKSPACE_OUTPUTS}/council-${SID}/stage3" \
    --timeout 240
```

Read `stage3/synthesis.json` (or whatever `id` you used) to extract the final response text.

### Step 7: Format and Present

Present the final output to the user in this structure:

```
## Council Deliberation

**Query:** [original query]
**Models:** [list of 4 models used]
**Chairman:** [winning model] (selected by peer review)
**Protocol:** [Voting | Consensus]
**Confidence:** [High | Medium | Low] (derived from ranking spread or agreement level)
[If vault context was loaded:]
**Vault context:** Loaded (project: [project name if matched], [N] prior deliberations)

---

[Chairman's synthesized answer]

---

**Where models agreed:** [key consensus points]
**Where models disagreed:** [flagged disagreements — the user should evaluate these]

<details>
<summary>Individual responses (click to expand)</summary>

**Analyst ([model name]):** [abbreviated response]
**Strategist ([model name]):** [abbreviated response]
**Challenger ([model name]):** [abbreviated response]
**Synthesist ([model name]):** [abbreviated response]

</details>

**Cost:** $[total] | **Latency:** [total]ms | **Models queried:** [count]
```

### Step 8: Log Outcome to Pattern Memory

After presenting results, log the deliberation outcome to persistent storage. This step runs automatically — do not skip it.

**8a. Prepare the log payload.** Collect the following from the pipeline run:

- `query_text`: the original user query (for feature extraction only — not persisted)
- `models_used`: the model IDs from Step 1
- `rankings`: the aggregated rankings from Step 5
- `chairman`: the chairman model ID from Step 5
- `confidence`: the confidence score from Step 5
- `consensus_level`: derived from ranking spread — "strong" (std_dev < 0.5), "moderate" (0.5-1.0), "weak" (1.0-1.5), "split" (> 1.5)
- `protocol_used`: "voting" or "consensus" from Step 3
- `cost_usd`: sum of all API call costs (if available from OpenRouter response metadata, otherwise estimate from model-configs.md pricing)
- `latency_ms`: wall-clock time from Step 2 start to Step 7 completion
- `reviewer_rankings_raw`: the raw per-reviewer ranking arrays from Step 4 (used for self-preference detection)
- `synthesis_text`: the chairman's Stage 3 output (for value-added computation — NOT stored)
- `top_individual_response`: the Stage 1 response from the highest-ranked model (for value-added computation — NOT stored)
- `routing_decision`: from the Pre-Step smart-router output (the decision, source, and confidence)
- `vault_context_loaded`: boolean from Pre-Step A

**8b. Call pattern-memory Log Deliberation.** Follow the pattern-memory skill's Operation 2 procedure:

1. Read `council-memory.json` from the workspace (or create it if this is the first deliberation)
2. Generate the record ID, query hash, summary, and features
3. Detect self-preference bias from the raw reviewer rankings
4. Build the deliberation record
5. Update model performance aggregates
6. Check if routing model needs rebuilding (every 10th deliberation, >= 20 total)
7. Write the updated memory file

**8c. Watch for user rating.** After presenting the deliberation result, monitor the user's next 1-2 messages for rating signals:

- Positive signals: "great", "perfect", "exactly", "helpful", "thanks" (with enthusiasm), explicit approval
- Negative signals: "wrong", "not helpful", "missed the point", "bad answer", rejection
- Neutral signals: "okay", "fine", mixed feedback
- No signal: user asks a new question or changes topic → leave rating as `null`, outcome as `"unknown"`

If a rating signal is detected, call pattern-memory Operation 3 (Capture User Rating) to update the most recent record.

**8d. Write Vault Decision Record (Obsidian Integration).**

Only runs if `vault_context_loaded: true` from Pre-Step A. This step writes the deliberation outcome to the Obsidian vault as a proper decision record, cross-linked and searchable.

1. **Determine the vault path.** If the user's query maps to a known project (check `query_features.category` and any project references in the vault context), target `${VAULT}/Projects/[Project]/11-Knowledge/`. If cross-cutting or no project match, target `${VAULT}/_Shared Knowledge/Agents and Plugins/`.

2. **Prepare the decision record.** Build a vault note with:

   ```yaml
   ---
   title: "Council: [query summary, 60 chars max]"
   date: YYYY-MM-DD
   project: [project-name or null]
   type: decision
   tags: [council, deliberation, [category from query_features]]
   participants: [dorian]
   status: active
   deliberation_id: [record ID from 8b]
   ---
   ```

   Body content:
   - **Query:** the original question
   - **Chairman:** model name + selection rationale (peer review ranking)
   - **Key agreements:** bullet list of consensus points
   - **Key disagreements:** bullet list of flagged disagreements
   - **Outcome:** what was accepted, what was rejected, what changed
   - **Cost:** total deliberation cost
   - Cross-links: `[[_Shared Knowledge/Agents and Plugins/council-deliberation-log|Deliberation Log]]`, `[[_Shared Knowledge/Agents and Plugins/council-model-performance|Model Performance]]`

3. **Call memory-system Sub-operation B** to write the decision record and append a log entry. Pass:
   - `record_type: "decision_record"` for the note
   - `record_type: "deliberation_log_entry"` for the log row
   - The memory-system handles deduplication, frontmatter validation, project index updates, and log table management.

4. **Error handling:** If the vault write fails (permissions, drive not mounted, API error), log a warning but do NOT fail the deliberation — the user already has their answer and the pattern-memory JSON log succeeded. Vault persistence is best-effort.

---

## Options

| Flag | Values | Default | Effect |
|------|--------|---------|--------|
| `--size` | `small`, `medium`, `large` | `medium` | 2, 4, or 6 models |
| `--fast` | flag | off | Skip peer review — collect + synthesize only |
| `--deep` | flag | off | MoA two-round collection — models see each other's Round 1 responses (+4 calls) |
| `--models` | comma-separated model IDs | from config | Override model selection |
| `--budget` | dollar amount | `0.15` | Max cost for this deliberation |
| `--thorough` | flag | off | Add Collective Improvement round (+4 calls) |
| `--template` | template name | none | Use a pre-built deliberation template (see `references/templates.md`) |
| `--no-vault` | flag | off | Skip vault context loading and vault write (Pre-Step A and Step 8d) |

## Error Handling

- If a model call fails or times out, proceed with the remaining models. A deliberation with 3 models is still valuable. The dispatch helper writes one JSON per job — `{id}.json` with `ok: false` indicates a failed model; surface those errors in the output footer.
- If fewer than 2 models respond in Stage 1, abort and tell the user which models failed (read `_summary.json` for the per-job picture).
- If the OpenRouter key can't be resolved, the dispatch helper exits with code 2 and a stderr message listing every path it tried. Surface that to the user along with the two likely fixes (mount the MoxyWolf Vault, or paste the team-shared key into `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/openrouter.env`).
- If estimated cost exceeds `--budget`, warn the user before proceeding.
- If vault is not accessible in Pre-Step A, proceed without vault context — log a note in the output footer.

## Cost Estimation

Per deliberation at default settings (4 models, medium):
- Pre-Step A (vault context): $0.00 (local reads, no API calls)
- Stage 1: 4 calls × ~1K input + ~2K output tokens ≈ $0.03-0.05
- Stage 2: 4 calls × ~8K input + ~500 output tokens ≈ $0.03-0.04
- Stage 3: 1 call × ~10K input + ~3K output tokens ≈ $0.02-0.03
- Step 8d (vault write): $0.00 (local writes, no API calls)
- **Total: ~$0.08-0.12 per deliberation**

With `--deep` (adds MoA Round 2): add ~$0.03-0.05
With `--thorough` (adds CI round): add ~$0.02-0.04
With `--deep --thorough` (both): add ~$0.05-0.09
With `--fast` (skips Stage 2): subtract ~$0.03-0.04

## Composio fallback — apps with no native MCP

If a step in this skill needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed, reach the app through Composio's Tool Router rather than giving up or asking the user to do it by hand. Discover the tool with `COMPOSIO_SEARCH_TOOLS`, authenticate with `COMPOSIO_MANAGE_CONNECTIONS` if needed, then execute. See the `composio` plugin's `composio-tools` skill for the full pattern.

Native MCP connectors still come first — this is a fallback for reach, not a replacement for the native paths this skill already uses.
