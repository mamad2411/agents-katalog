---
name: scheduled-collect-enrich-digest
description: "Collect items from a connected source score and summarize them against a brief and emit a ranked digest."
metadata:
  category: runtime-based
  tag:
    - "digest"
    - "monitoring"
  output-type: text
  runtime:
    - "aevatar-workflow"
version: "1.0"
---


# Scheduled collect → enrich → digest

This skill runs a prebuilt aevatar workflow (`scheduled_collect_enrich_digest`) that turns
one connected source into a ranked, AI-summarized digest. It is the native aevatar
re-expression of the common "data scraper agent" pattern — **collect → enrich → store** —
with the engine's own constraints respected (see *Scope* below).

A run does three things, in order:

1. **Collect** — one `nyxid_proxy` call runs a Tavily web search (`tavily-search-chrono-ai`) for the brief.
2. **Enrich** — one batched `llm_call` scores (0–100) and one-line-summarizes every item against the run brief.
3. **Digest** — the ranked result is frozen as the workflow output and is watchable in the observatory.

There is no per-run database write in v1 — **the run is the record**. Delivery and persistence
are optional extensions (see *Scope*).


## Protocol (follow in order)

1. **Confirm the source is connected.** This instance is wired to the nyxid connector
   `tavily-search-chrono-ai` (Tavily web search, ChronoAI org-shared). Call `nyxid_services`
   `{"action":"list"}` and confirm that slug is present and `allowed`. If it is missing, stop —
   connect Tavily (or retarget the workflow to another source) before running.
2. **The prompt is the search query.** There are no placeholders to fill for the default (Tavily)
   source — `collect` already searches `tavily-search-chrono-ai`. Compose the run prompt as a single
   clean query line: the topic plus any recency window ("aevatar workflow updates, last 7 days"). It
   is both the Tavily query and the ranking brief, and — because the engine has **no clock** — the
   only place a date/window can enter. *(To retarget another source, edit the `collect` body +
   `extract_items` path in the YAML.)*
3. **Run it.** Call `aevatar_start_workflow` with `workflow_id: "scheduled_collect_enrich_digest"`
   and `inputs.prompt` set to the query/brief. A clean `run_finished` with no `run_error` means it
   executed end to end; then scan the digest output for error-shaped content.
4. **Report honestly.** Return the ranked digest and the observatory link. State that you verified
   it ran **structurally**; do not claim the scoring is objectively correct.

### Scheduling

The engine does not schedule itself. "Recurring" means an **external trigger** (a scheduled agent
or any cron caller) invokes `aevatar_start_workflow` on an interval, each time passing a fresh brief
with the current window. Set that trigger up separately; this skill is the thing it calls.


## Inputs

| Input | Where | Purpose |
|---|---|---|
| `prompt` | `inputs.prompt` | The search query + relevance criteria + any date/window. Required — it is the Tavily query, the ranking brief, and the only clock. |
| source (slug/path/array-path) | hardcoded in the YAML | Wired to `tavily-search-chrono-ai` → `POST /search` → `results[]`. Edit the `collect` body + `extract_items` path to retarget. |

## Output

A single ranked digest (text), highest score first, one line per item:
`<score> — <title> — <one-line why it matters> — <url>`. Also persisted as the run record in the observatory.


## Scope (what this draft deliberately does and does not do)

- **Does:** single-source collect, one batched enrich pass, deterministic extraction, ranked digest, observatory visibility.
- **Does not (v1):**
  - **Cross-run dedup / "only new since last time".** That needs state that outlives a run, which in aevatar belongs to an **actor / read-model**, not a stateless workflow. Do not fake it with in-workflow memory.
  - **Feedback learning** (ECC's "gets smarter from your decisions"). Same reason — persistent preference state is an actor concern, a future companion skill, not this pipeline.
  - **Multi-source fan-out.** Add sources by composing collect steps (or a `parallel`/`foreach` over a source list) — kept to one source here for a clean first run.
  - **Delivery / storage to an external store.** Append a final `tool_call` (e.g. post the digest to a chat connector, or write to a store the user has) once the digest path is verified.

See `DESIGN.md` for the full ECC → aevatar mapping, connector dependencies, and verification checklist.
