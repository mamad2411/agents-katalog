---
name: social-search-digest
description: "Read-only X Twitter search producing a ranked summarized digest of recent posts."
metadata:
  category: runtime-based
  tag:
    - "social"
    - "digest"
  output-type: text
  runtime:
    - "aevatar-workflow"
version: "0.1"
---


# Social search digest (X / Twitter, read-only)

This skill runs a prebuilt aevatar workflow (`social_search_digest`) that turns a
search query into a ranked, AI-summarized digest of **recent public posts on X
(Twitter)**. It is **READ-ONLY**: it searches and reads only — it never posts,
replies, likes, or writes anything (a publish side-effect is deliberately out of
scope; see *Scope*).

A run does three things, in order:

1. **Search** — one `nyxid_proxy` call runs an X recent-search (`api-twitter`,
   `GET /tweets/search/recent`) for the query.
2. **Rank + summarize** — one batched `llm_call` scores (0–100) and one-line-summarizes
   every post against the run query.
3. **Digest** — the ranked result is frozen as the workflow output and is watchable in
   the observatory.

There is no per-run database write — **the run is the record**. Delivery and persistence
are optional extensions (see *Scope*).


## Protocol (follow in order)

1. **Confirm the source is connected.** This instance is wired to the nyxid connector
   `api-twitter` (X API v2, ChronoAI org-shared, bearer injected by nyxid). Call
   `nyxid_services` `{"action":"list"}` and confirm that slug is present and `allowed`.
   If it is missing, stop — connect X (or retarget the workflow to another source)
   before running.
2. **The prompt is the search query.** There are no placeholders to fill for the default
   (X) source — `search` already queries `api-twitter`. Compose the run prompt as a
   single clean, **URL-safe** query line: the topic plus any recency words. It is both the
   X search query and the ranking brief, and — because the engine has **no clock** — the
   only place a date/window can enter. Keep it one line with no `"` or newline characters:
   the query is interpolated both into the request URL and into the tool's JSON arguments,
   so a quote or line break would break the call. X recent-search already returns only the
   recent window, so "recent" is implicit; for tighter scoping, use X query operators
   (e.g. `lang:en`, `-is:retweet`) inside the query line. *(To retarget another source,
   edit the `search` body + `extract_posts` path in the YAML.)*
3. **Run it.** Call `aevatar_start_workflow` with `workflow_id: "social_search_digest"`
   and `inputs.prompt` set to the query. A clean `run_finished` with no `run_error` means
   it executed end to end; then scan the digest output for error-shaped content.
4. **Report honestly.** Return the ranked digest and the observatory link. State that you
   verified it ran **structurally**; do not claim the scoring is objectively correct, and
   make clear nothing was posted.

### Scheduling

The engine does not schedule itself. "Recurring" means an **external trigger** (a scheduled
agent or any cron caller) invokes `aevatar_start_workflow` on an interval, each time passing
a fresh query. Set that trigger up separately; this skill is the thing it calls.


## Inputs

| Input | Where | Purpose |
|---|---|---|
| `prompt` | `inputs.prompt` | The search query + relevance criteria. Required — it is the X search query, the ranking brief, and the only clock. Must be a single, URL-safe, quote-free line. |
| source (slug/path/array-path) | hardcoded in the YAML | Wired to `api-twitter` → `GET /tweets/search/recent?query=<q>&max_results=10` → `data[]`. Edit the `search` body + `extract_posts` path to retarget. |

## Output

A single ranked digest (text), highest score first, one line per post:
`<score> — <one-line why it matters> — <post text, trimmed>`. Also persisted as the run
record in the observatory.


## Scope (what this draft deliberately does and does not do)

- **Does:** single-query X recent-search, one batched rank/summarize pass, deterministic
  extraction, ranked digest, observatory visibility. **READ-ONLY.**
- **Does not:**
  - **Post / reply / write anything.** The source X API supports posting, threads, likes,
    and DMs; all write paths are intentionally excluded. This skill only reads — keep it
    that way so it is safe to run unattended and stays a clean, generic read tool. Posting
    is a side-effect that belongs in a separate, explicitly write-scoped skill.
  - **Cross-run dedup / "only new since last time".** That needs state that outlives a run,
    which in aevatar belongs to an **actor / read-model**, not a stateless workflow. Do not
    fake it with in-workflow memory.
  - **Author/timeline pulls, engagement analytics, media.** Only recent-search is wired.
    Add other read endpoints (e.g. user timeline, user lookup) by composing more
    `tool_call` steps — kept to one endpoint here for a clean first run.
  - **Hard counts.** Scoring/summarizing is qualitative, so `llm_call` is correct; any hard
    count ("12 matching posts") must come from a `transform`, never the LLM. v1 emits a
    qualitative ranked list and avoids asserting counts.
  - **Delivery / storage to an external store.** Append a final `tool_call` (e.g. post the
    digest to a chat connector, or write to a store the user has) once the digest path is
    verified.

See `DESIGN.md` for the full ECC → aevatar mapping, connector dependencies, why posting is
excluded, and the verification checklist (including "active but not live-probed").
