---
name: pp-openrouter
description: "The only OpenRouter CLI built for fleet operations: budgets, anomaly alarms, and failover maps over a local usage ledger — not another chat wrapper. Trigger phrases: `which model is cheapest for this task`, `what did my crons spend on openrouter`, `check openrouter credits runway`, `is openrouter degraded right now`, `why did my openrouter cost spike`, `use openrouter`, `run openrouter`."
author: "Rick van de Laar"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - openrouter-pp-cli
---

# OpenRouter — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `openrouter-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install openrouter --cli-only
   ```
2. Verify: `openrouter-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails before this CLI has a public-library category, install Node or use the category-specific Go fallback after publish.

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

Every other OpenRouter tool wraps chat; this one governs it. A synced local mirror of models, generations, and credits powers per-cron cost attribution (usage cost-by), pre-flight budget gates (budget check), degradation watches (providers degraded), and runway projections (credits runway) that no single API call can answer. The full endpoint surface — catalog, keys admin, activity, analytics — ships alongside as typed commands.

## When to Use This CLI

Reach for this CLI when the task is operating LLM workloads over OpenRouter: attributing spend to crons or agents, gating scheduled runs on budgets, shortlisting models by capability and price, watching provider health before dispatch, or projecting credit and cap runway. It is the right tool whenever the question spans local history plus the API — anything a single raw HTTP call cannot answer.

## Anti-triggers

Do not use this CLI for:
- Interactive chat sessions or a conversational playground — use a chat client; the chat command here is agent plumbing, not a UX
- Building application inference paths — use the official OpenRouter SDKs in your app, not shell-outs to a CLI
- Org member management, SCIM provisioning, or SSO setup — use the OpenRouter dashboard
- Real-time token streaming displays — the CLI returns complete responses, not stream renderers

## Unique Capabilities

These capabilities aren't available in any other tool for this API.

### Catalog intelligence

- **`models query`** — Shortlist models by capability, price, and context window with a structured query over the synced catalog — offline and instant.

  _Reach for this instead of fetching the full catalog: it answers a shortlist question in ~200 tokens instead of hundreds of KB._

  ```bash
  openrouter-pp-cli models query "tools=true cost.completion<5 ctx>=128k" --agent
  ```
- **`models churn`** — See what changed in the model catalog between syncs: additions, removals, and repricings with deltas.

  _Use this to catch a pinned model repricing or vanishing before the invoice does._

  ```bash
  openrouter-pp-cli models churn --since 7d --agent
  ```

### Cost governance for agent fleets

- **`usage cost-by`** — Attribute spend to the cron, agent, or lineage that incurred it, over any window.

  _Use this when the question is 'which job burned the money', not 'which model'._

  ```bash
  openrouter-pp-cli usage cost-by --since 7d --agent
  ```
- **`usage anomaly`** — Flag per-model cost spikes against the trailing baseline before they compound.

  _Run this in a daily cron to catch a misbehaving lineage the day it regresses, not at invoice time._

  ```bash
  openrouter-pp-cli usage anomaly --since 24h --agent
  ```
- **`budget`** — Set spend caps per cron or agent and enforce them pre-flight with typed exit codes.

  _Gate a scheduled run on exit code 0/8 so an over-budget lineage never fires._

  ```bash
  openrouter-pp-cli budget check nightly-drafter
  ```
- **`generation explain`** — Break one generation into its cost anatomy: tokens, latency, and the delta versus the cheapest provider.

  _The next command after an anomaly fires: it turns 'cost spiked' into 'this call, this provider, this delta'._

  ```bash
  openrouter-pp-cli generation explain gen-abc123 --agent
  ```
- **`usage reconcile`** — Verify the local usage mirror against upstream daily totals and flag days that disagree.

  _Run this before trusting any local cost analysis — it is the trust root for the other usage commands._

  ```bash
  openrouter-pp-cli usage reconcile --since 7d --agent
  ```

### Provider health and dispatch

- **`providers degraded`** — See which providers or models are currently degraded before dispatching work to them.

  _Check this before dispatch to route around trouble instead of retrying into it._

  ```bash
  openrouter-pp-cli providers degraded --agent
  ```
- **`endpoints failover`** — Rank the providers serving one model by status, price, and observed latency for dispatch order.

  _Feed this to a router to pre-empt degraded providers for a specific model._

  ```bash
  openrouter-pp-cli endpoints failover deepseek/deepseek-v4 --agent
  ```

### Runway and rate-limit headroom

- **`key eta`** — Project the date your key's spend cap trips, from the observed burn rate.

  _Use this to plan the week's runs against the cap instead of discovering it mid-run._

  ```bash
  openrouter-pp-cli key eta --agent
  ```
- **`limits status`** — One view of current headroom: key-cap remaining, free-tier daily quota, and today's free-model burn.

  _Check before a free-tier dev loop or fleet dispatch to avoid opaque 429s._

  ```bash
  openrouter-pp-cli limits status --agent
  ```
- **`credits runway`** — Project days-to-zero for prepaid credits at the trailing burn rate — the 402 leading indicator.

  _A daily cron on this answers 'when do we hit 402' while there is still time to top up._

  ```bash
  openrouter-pp-cli credits runway --agent
  ```

## Command Reference

**activity** — Manage activity

- `openrouter-pp-cli activity` — Returns user activity data grouped by endpoint for the last 30 (completed) UTC days.

**audio** — Manage audio

- `openrouter-pp-cli audio create-speech` — Synthesizes audio from the input text. Returns a raw audio bytestream in the requested format (e.g. mp3, pcm, wav).
- `openrouter-pp-cli audio create-transcriptions` — Transcribes audio into text.

**benchmarks** — Benchmarks endpoints

- `openrouter-pp-cli benchmarks` — Unified benchmark endpoint that aggregates scores from multiple benchmark sources (Artificial Analysis, Design Arena

**byok** — BYOK endpoints

- `openrouter-pp-cli byok create-byokkey` — Create a new bring-your-own-key (BYOK) provider credential.
- `openrouter-pp-cli byok delete-byokkey` — Delete (soft-delete) a bring-your-own-key (BYOK) provider credential by its `id`.
- `openrouter-pp-cli byok get-byokkey` — Get a single bring-your-own-key (BYOK) provider credential by its `id`.
- `openrouter-pp-cli byok list-byokkeys` — List the bring-your-own-key (BYOK) provider credentials for the authenticated entity's default workspace.
- `openrouter-pp-cli byok update-byokkey` — Update an existing bring-your-own-key (BYOK) provider credential by its `id`.

**chat** — Chat completion endpoints

- `openrouter-pp-cli chat` — Sends a request for a model response for the given chat conversation. Supports both streaming and non-streaming modes.

**classifications** — Task classification market-share endpoints

- `openrouter-pp-cli classifications` — Returns the market-share breakdown of OpenRouter traffic by task classification (e.g.

**containers** — Containers endpoints


**credits** — Credit management endpoints

- `openrouter-pp-cli credits create-coinbase-charge` — Deprecated.
- `openrouter-pp-cli credits get` — Get total credits purchased and used for the authenticated user.

**datasets** — Public OpenRouter usage datasets. Data returned by these endpoints is licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/): reuse and republish it, including commercially, with attribution to OpenRouter.

- `openrouter-pp-cli datasets get-app-rankings` — Returns the top public apps on OpenRouter ranked by token usage inside the requested date window
- `openrouter-pp-cli datasets get-rankings-daily` — Returns the top 50 public models per day by total token usage on OpenRouter
- `openrouter-pp-cli datasets get-session-cost` — Returns weekly refreshed, aggregated cost-per-session cells for the published harnesses.

**embeddings** — Text embedding endpoints

- `openrouter-pp-cli embeddings create` — Submits an embedding request to the embeddings router
- `openrouter-pp-cli embeddings list-models` — Returns a list of all available embeddings models and their properties

**endpoints** — Endpoint information

- `openrouter-pp-cli endpoints` — Preview the impact of ZDR on the available endpoints

**files** — Files endpoints

- `openrouter-pp-cli files delete` — Deletes a file owned by the requesting workspace. Deletion is irreversible.
- `openrouter-pp-cli files get-metadata` — Retrieves metadata for a single file owned by the requesting workspace.
- `openrouter-pp-cli files list` — Lists files belonging to the workspace of the authenticating API key.
- `openrouter-pp-cli files upload` — Uploads a file to be referenced in future API calls.

**generation** — Generation history endpoints

- `openrouter-pp-cli generation get` — Get request & usage metadata for a generation
- `openrouter-pp-cli generation list-content` — Get stored prompt, completion, and error content for a generation
- `openrouter-pp-cli generation submit-feedback` — Submit structured feedback on a generation the authenticated user made.

**guardrails** — Guardrails endpoints

- `openrouter-pp-cli guardrails create` — Create a new guardrail for the authenticated user.
- `openrouter-pp-cli guardrails delete` — Delete an existing guardrail. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli guardrails get` — Get a single guardrail by ID. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli guardrails list` — List all guardrails for the authenticated user.
- `openrouter-pp-cli guardrails list-key-assignments` — List all API key guardrail assignments for the authenticated user.
- `openrouter-pp-cli guardrails list-member-assignments` — List all organization member guardrail assignments for the authenticated user.
- `openrouter-pp-cli guardrails update` — Update an existing guardrail, or materialize an unconfigured workspace default guardrail.

**images** — Images endpoints

- `openrouter-pp-cli images create` — Generates an image from a text prompt via the image generation router
- `openrouter-pp-cli images list-model-endpoints` — Returns the full per-endpoint records for an image model: each endpoint's definitive supported parameters, pricing
- `openrouter-pp-cli images list-models` — Lists every image generation model with its top-level supported-parameter superset and a URL to its full per-endpoint

**key** — Manage key

- `openrouter-pp-cli key` — Get information on the API key associated with the current authentication session

**keys** — Manage keys

- `openrouter-pp-cli keys create` — Create a new API key for the authenticated user. The plaintext `key` is returned only in this response.
- `openrouter-pp-cli keys delete` — Delete an existing API key.
- `openrouter-pp-cli keys get` — Get a single API key by hash. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli keys list` — List all API keys for the authenticated user. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli keys update` — Update an existing API key.

**messages** — Manage messages

- `openrouter-pp-cli messages` — Creates a message using the Anthropic Messages API format. Supports text, images, PDFs, tools, and extended thinking.

**model** — Model information endpoints

- `openrouter-pp-cli model <author> <slug>` — Returns full details for a single model identified by its author and slug (e.g. openai/gpt-4).

**models** — Model information endpoints

- `openrouter-pp-cli models get` — List all models and their properties
- `openrouter-pp-cli models list-count` — Get total count of available models
- `openrouter-pp-cli models list-user` — List models filtered by user provider preferences, [privacy settings](https://openrouter.

**observability** — Observability endpoints

- `openrouter-pp-cli observability create-destination` — Create a new observability destination. A maximum of 5 destinations per type is allowed.
- `openrouter-pp-cli observability delete-destination` — Delete an existing observability destination. This performs a soft delete.
- `openrouter-pp-cli observability get-destination` — Fetch a single observability destination by its UUID.
- `openrouter-pp-cli observability list-destinations` — List the observability destinations configured for the authenticated entity's default workspace.
- `openrouter-pp-cli observability update-destination` — Update an existing observability destination. Only the fields provided in the request body are updated.

**openrouter-analytics** — Manage openrouter analytics

- `openrouter-pp-cli openrouter-analytics get-meta` — Returns the available metrics, dimensions, filter operators, and granularities for the analytics query endpoint.
- `openrouter-pp-cli openrouter-analytics query` — Execute an analytics query with specified metrics, dimensions, filters, and time range.

**openrouter-auth** — Manage openrouter auth

- `openrouter-pp-cli openrouter-auth create-keys-code` — Create an authorization code for the PKCE flow to generate a user-controlled API key
- `openrouter-pp-cli openrouter-auth exchange-code-for-apikey` — Exchange an authorization code from the PKCE flow for a user-controlled API key

**organization** — Organization endpoints

- `openrouter-pp-cli organization` — List all members of the organization associated with the authenticated management key.

**presets** — Presets endpoints

- `openrouter-pp-cli presets get` — Retrieves a preset by its slug with its currently designated version inline.
- `openrouter-pp-cli presets list` — Lists all presets for the authenticated user, ordered by most recently updated first.

**providers** — Provider information endpoints

- `openrouter-pp-cli providers` — List all providers

**rerank** — Rerank endpoints

- `openrouter-pp-cli rerank` — Submits a rerank request to the rerank router

**responses** — OpenAI-compatible Responses API endpoints

- `openrouter-pp-cli responses` — Creates a streaming or non-streaming response using OpenResponses API format

**scim** — SCIM endpoints

- `openrouter-pp-cli scim create-group-mapping` — Create a SCIM group-to-workspace role mapping.
- `openrouter-pp-cli scim delete-group-mapping` — Delete a SCIM group-to-workspace mapping. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli scim get-group-mapping` — Get a SCIM group-to-workspace mapping. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli scim list-group-mappings` — List SCIM group-to-workspace mappings for the organization.
- `openrouter-pp-cli scim list-groups` — List SCIM groups for the organization. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli scim update-group-mapping` — Update a SCIM group mapping role. [Management key](/docs/guides/overview/auth/management-api-keys) required.

**videos** — Manage videos

- `openrouter-pp-cli videos create` — Submits a video generation request and returns a polling URL to check status
- `openrouter-pp-cli videos get` — Returns job status and content URLs when completed
- `openrouter-pp-cli videos list-models` — Returns a list of all available video generation models and their properties

**workspaces** — Workspaces endpoints

- `openrouter-pp-cli workspaces create` — Create a new workspace for the authenticated user.
- `openrouter-pp-cli workspaces delete` — Delete an existing workspace. Workspaces with active API keys cannot be deleted; remove the keys first.
- `openrouter-pp-cli workspaces get` — Get a single workspace by ID or slug. [Management key](/docs/guides/overview/auth/management-api-keys) required.
- `openrouter-pp-cli workspaces list` — List all workspaces for the authenticated user.
- `openrouter-pp-cli workspaces update` — Update an existing workspace by ID or slug. [Management key](/docs/guides/overview/auth/management-api-keys) required.


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
openrouter-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Recipes


### Monday cost review

```bash
openrouter-pp-cli usage cost-by --since 7d --agent
```

The weekly attribution pass: spend per cron/agent tag, ready to paste into a review note.

### Anomaly to root cause in two commands

```bash
openrouter-pp-cli usage anomaly --since 24h --agent
```

When a model flags, follow with 'generation explain <id>' to get tokens, latency, and the cheapest-provider delta for the offending call.

### Pre-dispatch health gate

```bash
openrouter-pp-cli providers degraded --agent
```

Run before firing a lineage; pair with 'endpoints failover <model>' to pick the dispatch order for the model you are about to use.

### Narrow a deep endpoint payload

```bash
openrouter-pp-cli models endpoints list deepseek deepseek-v4 --agent --select data.endpoints.provider_name,data.endpoints.pricing.completion,data.endpoints.status
```

Per-model provider listings nest deeply; --select keeps the answer to the three fields a router actually needs.

### Budget-gated cron pattern

```bash
openrouter-pp-cli budget check nightly-drafter
```

Exit code 0 under cap, 8 over — gate a scheduled run on this before it fires (e.g. 'budget check X && systemctl --user start X.service').

## Auth Setup

Standard bearer auth with your inference key via OPENROUTER_API_KEY covers models, credits, key status, and chat. Two surfaces need the separate provisioning (management) key created in the dashboard: key administration (/keys) and account-wide usage rollups (/activity, analytics). A 401 or 403 on those commands with an otherwise-working key means you are holding the inference key where the management key is required — not a broken setup. Live-verified 2026-09: /activity returns 403 'Only management keys can fetch activity' on an inference key.

Run `openrouter-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  openrouter-pp-cli benchmarks --agent --select accuracy,accuracy_stddev,agentic_index
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit confirmation** — `--agent` does not imply `--yes`; pass `--yes` separately only after the target, arguments, and side effects are clear
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success, and use `--ignore-missing` only when a missing delete target should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal AND no machine-format flag (`--json`, `--csv`, `--compact`, `--quiet`, `--plain`, `--select`) is set — piped/agent consumers and explicit-format runs get pure JSON on stdout.

## Paths and state

Agents should treat the CLI's path resolver as part of the runtime contract:

- Use `--home <dir>` for one invocation, or set `OPENROUTER_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `OPENROUTER_CONFIG_DIR`, `OPENROUTER_DATA_DIR`, `OPENROUTER_STATE_DIR`, `OPENROUTER_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `OPENROUTER_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `openrouter-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "openrouter": {
        "command": "openrouter-pp-mcp",
        "env": {
          "OPENROUTER_HOME": "/srv/openrouter"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `OPENROUTER_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `OPENROUTER_HOME`, or `doctor` will not find credentials left under the former root.

## Automatic learning

This CLI ships a self-capturing learning loop. The CLI does its own bookkeeping: every invocation is journaled locally, a failed flag followed by a corrected retry auto-derives a `flag_alias` candidate, and a `teach` on a query family without a playbook auto-synthesizes a `playbook_candidate` from the session's journal. Your job is judgment only: `recall` first, act on surfaced candidates, `teach` the final answer, `playbook amend` when you observe a correction. You never record failures by hand.

### Step 1: `recall` before any discovery

Before list/search/drill commands on a new user question, run:

```bash
openrouter-pp-cli recall "<user's question>" --agent
```

The response envelope:

```json
{
  "query": "...",
  "normalized": "<normalized form>",
  "query_entities": ["..."],
  "found": true | false,
  "match_score": 0.0,
  "results": [
    { "resource_id": "...", "resource_type": "...", "venue": "...",
      "confidence": 2, "entity_match": "exact|partial|unknown",
      "source": "taught|preseed|pattern", "warnings": ["..."] }
  ],
  "mismatches": [ /* only when --debug-mismatches */ ],
  "warnings": [ /* top-level */ ],
  "candidates": [
    { "id": 12, "class": "flag_alias | playbook_candidate",
      "summary": "...", "sightings": 3, "last_seen": "...",
      "rationale": "...",
      "next_action": ["<trial command>", "openrouter-pp-cli learnings confirm 12"] }
  ],
  "playbook": {
    "query_family": "...",
    "playbook": {
      "steps": [ { "cmd": "<command with {slot} substitution>", "purpose": "..." } ],
      "entity_slots": ["$ENTITY"],
      "expected_tool_calls": 3
    },
    "slots_resolved": { "$ENTITY": { "token": "<live token>", "canonical": "<canonical>" } },
    "notes": "<workarounds + gotchas for this query family>"
  },
  "notes": "<duplicate surface for non-playbook callers>"
}
```

Empty-store short-circuit: if the store has no learnings, playbooks, or candidates yet (recall finds nothing and `learnings list` and `learnings candidates` are both empty), skip recall for the rest of this session instead of taxing every query; resume recall-first once something has been taught.

### Step 2: decision tree

Read `candidates`, `playbook`, `notes`, `results[0]`, and warnings in that order:

```
if Candidates present (warnings include "candidates_present"):
    -> candidates are try-then-confirm, never facts. Follow each candidate's
       two-step next_action verbatim: run the trial command first, then run
       `learnings confirm <id>` only after the trial verified the behavior.
       Reject a wrong candidate with `learnings reject <id>`.
    -> NEVER re-teach something recall surfaced as a candidate; confirm or
       reject that candidate instead of teaching a duplicate.
    -> candidates ride alongside playbooks and resource hits, not instead of
       them; continue with the branches below after acting on them.

if Playbook present:
    -> READ Playbook.notes verbatim FIRST (workarounds + gotchas the CLI surface doesn't expose)
    -> replay Playbook.steps in order, substituting Playbook.slots_resolved entries
       for the entity slot tokens. If a step's slot is unresolved, fall back to
       discovery for that step only.
    -> the Playbook's expected_tool_calls is a budget; if you find yourself running
       materially more, record the divergence via `openrouter-pp-cli playbook amend`
       at end-of-session.

elif Notes present (no Playbook):
    -> read Notes verbatim before any discovery step; they carry known gotchas
       for this query family even when no structured choreography exists yet.

elif Found AND Results[0].EntityMatch == "exact" AND Results[0].Confidence >= 2:
    -> skip discovery; fetch live data for Results[*].ResourceID in parallel

elif Found AND Results[0].EntityMatch == "partial":
    -> candidate hint, NOT a hit; read the resource title to validate before trusting

elif (any row in Mismatches[] when --debug-mismatches was passed):
    -> treat as cold start; the stored learning is for a different entity
       (different canonical resolved from query_entities)

else:  // Found == false, no playbook, no notes
    -> cold start; run discovery normally; teach the answer afterward (Step 4).
       If the family has no playbook yet, that teach auto-synthesizes a
       playbook candidate from this session's journal - you do not need to
       record one by hand.
```

Playbook and Notes are orthogonal to the per-resource path. A recall response can carry both a Playbook AND a `Results[]` hit - use both: the Playbook tells you which choreography to run; the resource hits short-circuit specific steps. Default to skipping `mismatches`; pass `--debug-mismatches` only when investigating cold-start surprises.

Candidate judgment details: `learnings confirm <id>` prints the candidate's full payload before materializing it - check that the printed payload matches the behavior you verified. `learnings reject <id>` tombstones the derivation signature so the same candidate does not resurface. The envelope carries only the few candidates worth acting on now; `openrouter-pp-cli learnings candidates` lists the full open set.

Graceful degradation: if `learnings confirm` is an unknown command, you are driving an older binary - ignore the candidates guidance and follow the rest of the protocol.

### Step 3: always read `warnings`

- `low_confidence`: row exists at `confidence<2`. Treat as a hint, not a skip-discovery hit.
- `resource_not_in_store`: the local store doesn't have the resource the learning points at. The match validator couldn't classify entities — direct-fetch and re-evaluate.
- `cross_alias_match` (per-result): the row was taught under a different alias and matched the live query's canonical via `entity_lookups` (e.g., a "USA" teach satisfying a "United States" recall). Trust the resource_id.
- `similar_shape_different_entity:<canonical>` (top-level): a structurally matching row exists but its canonical entity differs from the live query's. Treated as cold start; the warning carries the conflicting canonical as a hint, but the row is NOT promoted into Results.
- `ambiguous_alias` (top-level): a single query entity resolved to multiple canonicals (e.g., "Cards" → Arizona Cardinals + St. Louis Cardinals). Surface the ambiguity from context before committing to a resource.
- `candidates_present` (top-level): the envelope carries a `candidates` section. Handle it via the candidates branch in Step 2 before anything else.
- `lookup_refresh_available` (top-level): an entity in the query has no lookup row yet, but synced data could provide one. Run `openrouter-pp-cli sync` to refresh entity lookups.
- Top-level `no_learnings_for_query_family`: the table had no rows above the Jaccard floor. Pure cold start.

### Step 4: `teach &` after finalizing your response - always

Teaching is unconditional. After resolving a query the store could not answer, background-teach the final resource mapping - no call-count threshold, no judging whether it was "worth" learning. The teach is the anchor of the loop: it triggers playbook synthesis for a family without a playbook, and same-referent phrasings fold into one family so near-duplicate teaches do not fragment the store. Fire it after assembling your user-facing response but BEFORE emitting it, with a shell `&` so the call returns immediately:

```bash
openrouter-pp-cli teach --query "<user's question>" --resource-type <type> --resource <id1> --resource <id2>
# (append shell `&` to background it)
```

Silent on success. Errors only land in `teach.log` under the resolved state dir. Teach the **most specific** resource - if the user asked a broad question and you walked through parent records to find the specific answer, teach the leaf id, not the parent. The CLI uses seeded `entity_lookups` for cross-alias resolution at recall time, so a teach under one alias (e.g., "Niners") satisfies future queries under another alias (e.g., "49ers", "San Francisco") automatically.

PII rule: teach the structural question with identifiers stripped - never include names, emails, phone numbers, account ids, or other personal identifiers in taught queries or notes. The CLI scans teach queries for obvious email/phone shapes and warns, but does not block; strip before teaching rather than relying on the warning.

### Step 5: playbooks - optional flags, automatic synthesis

You do not need to decide whether a session "deserves" a playbook: a teach on a family without one auto-synthesizes a `playbook_candidate` from the session's journal, and the next session judges it via confirm/reject. Attach explicit playbook flags only when you already hold choreography worth recording verbatim - workarounds the CLI didn't surface (silently-dropped flags, undocumented params, pagination tricks, payload gotchas). Prefer the **integrated one-call form** - record the resource learning and the playbook in the same `teach` invocation:

```bash
# Common case: record both the resource learning AND the playbook in one call.
openrouter-pp-cli teach \
  --query "<user's question>" \
  --resource <id> \
  --playbook-file ~/playbooks/<shape>.json \
  --playbook-notes-file ~/playbooks/<shape>-notes.md
# (append shell `&` to background it)

# Alternate: playbook-only (no resource to record alongside).
openrouter-pp-cli teach-playbook \
  --query "<user's question>" \
  --playbook-file ~/playbooks/<shape>.json \
  --notes-file ~/playbooks/<shape>-notes.md
```

Playbook files are JSON with `steps`, `entity_slots`, `expected_tool_calls`. Notes files are markdown carrying the gotchas verbatim. File-free callers (MCP-only agents) pass the same content inline: `--playbook-json` and `--playbook-notes` on the integrated `teach` form, `--playbook-json` and `--notes` on `teach-playbook`. On the integrated `teach` form, the playbook flags are optional - omit them entirely for a resource-only teach. On the standalone `teach-playbook` form, at least one of the playbook and notes flags must be set; both empty is rejected. Playbooks are keyed on the structural query family (entities stripped) so a recipe taught from one entity-shaped query applies to every other query of the same shape, with `slots_resolved` binding the live query's canonical at recall time.

When you DO find a playbook on a future recall, treat it as ground truth: replay the steps with `slots_resolved` substitutions, skip the discovery that the choreography already documents, and read `notes` before any step.

### Step 6: `playbook amend &` when your debug response identifies a correction

If your debug-protocol response identifies a concrete correction the notes or playbook should know — a workaround, an undocumented endpoint shape, a stale field name, observed schema drift, an empty-payload fallback — fire `playbook amend` BEFORE emitting your user-facing response. Same fire-and-forget posture as `teach`.

```bash
openrouter-pp-cli playbook amend \
  --query "<exact recall query string>" \
  --add-note "<your concrete correction>"
# (append shell `&` to background it)
```

What counts as worth amending: a behavior you OBSERVED this session that future-you would benefit from knowing. Examples worth amending:

- A workaround for a CLI surface that silently drops or misorders a flag.
- An undocumented endpoint shape (response wrapped in `{meta, results}`, payload nested two levels deeper than the docs claim).
- Observed schema drift (a field renamed, an index that shifted between seasons, a category label that the API now returns lower-cased).

What does NOT belong in notes:

- The year-specific or entity-specific answer to the user's question. That's the response, not a learning.
- Per-team / per-athlete / per-row data the playbook already retrieves at runtime.
- Statements that paraphrase what the existing notes already say.

The amend command appends to the family's existing notes with a timestamped marker (`[amend YYYY-MM-DDTHH:MMZ]: <text>`). Multiple amends accumulate; the audit trail is visible. If no playbook exists yet for the family, amend creates a notes-only one (so cold-start corrections still land).

#### PII discipline for amend notes

`playbook amend` notes are designed to potentially flow upstream as shared knowledge in future versions of the Printing Press. Keep them clean of user-identifying content so the upstream-contribution path stays open without retroactive scrubbing:

- **Do NOT embed** paths to user filesystems, personal API keys or tokens, user email addresses, user GitHub handles, or specific query histories tied to a single user.
- **Acceptable**: endpoint shapes, undocumented field names, API gotchas, observed schema drift, workarounds for CLI surfaces, generalizable pagination or retry tactics.

If a correction is only meaningful with user-specific context, it belongs in a personal note, not in the playbook amend.

### Measuring the loop

`openrouter-pp-cli learnings stats` reports recall hit rate, teach-to-reuse, playbook resolution rate, and candidate confirm/reject counts from the local `learn_events` table. Rates are null until they have a denominator; everything stays on this machine. Use it to check whether the loop is earning its keep for this CLI.

### Disabling learning

- `--no-learn` on a single command short-circuits both `recall` and the `teach` write path. Use for deterministic agent flows or tests that must not be affected by accumulated learnings.
- `OPENROUTER_NO_LEARN=true` in the environment globally disables the pipeline.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
openrouter-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
openrouter-pp-cli feedback --stdin < notes.txt
openrouter-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `OPENROUTER_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `OPENROUTER_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled or recurring agent reuses the same saved flags while providing different input each run.

```
openrouter-pp-cli profile save briefing --json
openrouter-pp-cli --profile briefing benchmarks
openrouter-pp-cli profile list --json
openrouter-pp-cli profile show briefing
openrouter-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `openrouter-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Install the MCP binary from this CLI's published public-library entry or pre-built release, then register it:

```bash
claude mcp add openrouter-pp-mcp -- openrouter-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which openrouter-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   openrouter-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `openrouter-pp-cli <command> --help`.
