---
name: discourse-sweep
description: >
  Runs the 30-day discourse sweep, the Phase 3 (Discernment) step of the 4D Blog Engine. It can
  resolve the topic to concrete entities (subreddits, handles, repos) first, then fires
  platform-targeted queries across reddit, X, Hacker News, Substack, dev.to, GitHub, LinkedIn
  Pulse, Facebook, Quora, podcasts and academic sources, including zero-config reddit public-JSON
  queries that capture real engagement. It ranks findings on a relevance, recency and engagement
  blend, dedupes on 70% title overlap, clusters across sources, caps any one author at three
  primaries, and writes discourse.md into the piece's 03-discernment/ folder. Triggers:
  "/4d-blog-engine:blog-discern", "run the 30-day sweep", "sweep the discourse on", "what's the
  world saying about <topic>". This is a specialist skill the orchestrator invokes, not one the
  user calls directly.
allowed-tools: [Read, Write, Bash, WebSearch, Glob]
user-invocable: false
---

# Discourse Sweep — the 30-day platform-targeted research engine

## When this skill applies

This skill should be used when running the 30-day discourse sweep step of the 4D Blog Engine — Phase 3 (Discernment). It optionally resolves the topic to concrete entities (subreddits, handles, repos) first, then fires platform-targeted queries across reddit, X, Hacker News, Substack, dev.to, github, linkedin.com/pulse, Facebook, Quora, podcasts (Apify), and academic sources (research-pipeline/literature-discovery) — including zero-config reddit public-JSON queries that capture real engagement (upvotes + comments) — then ranks the findings via a relevance/recency/engagement blend, dedupes by 70% title-overlap, applies cross-source clustering, caps any single author at 3 primaries, and writes a discourse.md to the piece's 03-discernment/ folder. Triggers: "/4d-blog-engine:blog-discern", "run the 30-day sweep", "sweep the discourse on", "what's the world saying about <topic>", "research the last 30 days for <topic>". This is a specialist skill — invoked by the 4d-blog-engine orchestrator, not directly by the user in normal usage.


> **Read this when:** Phase 3 (Discernment) has just started. The orchestrator skill has confirmed Phase 2's outline is approved and the piece directory exists. Your job is to populate `<piece>/03-discernment/discourse.md` with a ranked, themed brief of the last 30 days of conversation on this topic.

## Why this is a specialist skill

The 30-day sweep is mechanically distinct from the rest of Phase 3 (drafting, slop pass). It's a research operation with a strict separation: **the orchestrator dispatches queries; `scripts/discourse_sweep.py` does the math.** Per agricidaniel/claude-blog's discipline: the LLM agent never does deterministic ranking/dedup; the script never makes network calls.

## Inputs

The orchestrator gives you:

- `<piece>/02-description.md` — the outline, with section-by-section evidence needs
- `<piece>/01-delegation.md` — the angle and the earned secret
- `<piece>/state.md` — the piece slug and the active project

## Workflow

### Step 0.5 — Resolve entities (optional, recommended)

Concept-ported from mvanhorn/last30days-skill (MIT): before firing blind term queries, resolve the topic to the concrete places the conversation actually happens. This is an **LLM judgment step you do** — the script does no resolution. From the angle and outline, name:

- **Subreddits** where this topic lives (e.g. `ClaudeAI`, `LocalLLaMA`) — communities, not guesses; only include ones you're confident exist.
- **X / GitHub handles** of the people or projects central to the topic (person → handle, product → founder/repo).

Write them to `<piece>/03-discernment/entities.json`:

```json
{"subreddits": ["ClaudeAI", "LocalLLaMA"],
 "handles": {"x": ["steipete"], "github": ["steipete"]}}
```

If the topic has no obvious entities (abstract/broad themes), skip this step — the sweep still runs on term queries alone. Never fabricate a subreddit or handle; a wrong entity poisons the sweep. When unsure, leave it out.

### Step 1 — Generate the sweep plan

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/discourse_sweep.py plan \
  --topic "<angle from 01-delegation.md>" \
  --outline "<piece>/02-description.md" \
  --days 30 \
  --entities "<piece>/03-discernment/entities.json" \
  --out "<piece>/03-discernment/sweep-plan.json"
```

(`--entities` is optional; omit it if you skipped Step 0.5.) The plan file lists ~9 web-platform queries for the primary topic + ~9 queries per outline section, plus one `reddit_json` query per resolved subreddit and one handle-scoped query per resolved X/GitHub identity. Each query has an `executor` field naming the tool to use: `WebSearch` (term/handle queries, form `<terms> site:<platform> after:<YYYY-MM-DD>`) or `reddit_json` (a ready-to-fetch reddit URL).

### Step 2 — Execute the queries

For each query in `sweep-plan.json["queries"]`:

- **`executor: WebSearch`** (the default for all web platforms): call `WebSearch` with the query string. Capture the top 5-10 results.
- **`executor: Apify`** (for podcasts): call `mcp__Apify__call-actor` with an Apple Podcasts search actor and the topic terms. If Apify isn't connected, fall back to `WebSearch` with `site:apple.co/podcasts` and `site:open.spotify.com/episode` queries, and log the degradation.
- **`executor: research-pipeline`** (for academic): invoke the `research-pipeline/literature-discovery` skill with the topic. It returns OpenAlex + Semantic Scholar + arXiv hits.
- **`executor: reddit_json`** (entity-scoped reddit): the query is a full reddit public-JSON URL. Fetch it with Bash + curl, sending a descriptive User-Agent (Reddit rate-limits blank UAs). Zero-config — no key. Parse the JSON `data.children`; for each post capture `title`, `permalink` (prefix `https://www.reddit.com`), the created date, and set `engagement` to `score + num_comments`. If the fetch fails, is rate-limited, or returns non-JSON, **do not invent results** — log the degradation and rely on the WebSearch reddit query for that subreddit. Example:

  ```bash
  curl -sS -A "moxywolf-discourse-sweep/1.0 (research)" "<query-url>"
  ```

For each result, capture into a findings array:

```json
{
  "title": "<page title>",
  "url": "<absolute URL>",
  "platform": "<reddit|x|hn|substack|devto|github|linkedin|facebook|quora|podcasts|academic>",
  "summary": "<2-4 sentence summary in your own words>",
  "published_at": "<ISO date if extractable, else null>",
  "source_type": "<discussion|blog|primary|whitepaper|podcast|paper|other>",
  "author": "<handle/username if known (enables the per-author cap); else omit>",
  "engagement": "<integer engagement count if the source exposed one (reddit score+comments, etc.); else omit>",
  "relevance": <optional 0-1 if you can judge precisely; otherwise omit>
}
```

`author` and `engagement` are optional and additive: findings without them rank exactly as before. Only set `engagement` from a real count you retrieved — never estimate it.

Write the collected findings array to `<piece>/03-discernment/sweep-findings.json` as JSON (a single top-level array, or `{"findings": [...]}` — the ranker accepts both).

**Anti-fabrication rule** (load-bearing): **only include findings you actually retrieved.** If WebSearch returned nothing for a query, log the empty result in `sweep-findings.json` as a comment block but never invent a URL or a summary. Findings whose summary you cannot derive from real retrieved content do not exist.

### Step 3 — Rank, dedupe, cluster

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/discourse_sweep.py rank \
  --findings "<piece>/03-discernment/sweep-findings.json" \
  --topic "<angle from 01-delegation.md>" \
  --out "<piece>/03-discernment/discourse.md"
```

The ranker:

- Scores each finding on a blend of relevance, banded recency, and (when present) engagement. Without an engagement count: `combined_score = relevance×0.6 + recency×0.4` (unchanged). With one: `relevance×0.48 + recency×0.32 + engagement×0.2`, where `engagement` is the raw count log-normalized to [0,1] — so an upvoted-and-discussed thread outranks a same-relevance post nobody engaged with, but engagement never overwhelms substance.
- Dedupes via 70% title-token overlap, keeps the highest-scoring as the primary of each cluster.
- Adds a +0.1 source-diversity bonus to clusters surfacing from ≥2 platforms.
- Caps any single `author` at 3 primaries so one loud voice can't dominate the brief; capped items are retained under `capped_by_author`, never silently dropped.
- Writes `discourse.md` (human-readable) and `discourse.json` (sidecar for downstream steps).

### Step 4 — Council synthesis pass (optional but recommended)

The 30-day sweep is **recall-heavy**. The Council deliberation pass is the de-noiser. Invoke:

```
/council:deliberate --prompt "Given these findings, the angle, and the outline,
which findings move the post from generic to specific? Which contradict each
other? Which represent consensus vs minority view across platforms? Return a
ranked, themed brief with 3-5 themes." --input "<piece>/03-discernment/discourse.md"
```

Capture Council's output to `<piece>/03-discernment/discourse-themed.md`. This becomes the file the writer (research-pipeline/content-writer) reads when drafting.

If Council is unavailable (no OpenRouter key, etc.), log the degradation in `sources-verification.md` and use the unfiltered `discourse.md` directly. State this clearly.

### Step 5 — Apply source-quality tiers

Read `references/source-quality-tiers.md` if not already loaded. For each primary finding in `discourse.md`, assign a tier (1-5) based on the platform and the source character. Write a `<piece>/03-discernment/sources-verification.md` that lists each citable source with its tier, its FLOW-evidence-triple checklist (year anchor + inline citation form + retrieval date), and a verification state (`[V]/[S]/[F]`) that downstream citation verification will fill in.

**Tier 4-5 sources do not advance to the writer.** Drop them with a one-line "rejected (tier 4-5)" note.

### Step 6 — Hand off to the writer

Once `discourse-themed.md` and `sources-verification.md` exist, return control to the orchestrator with a status report:

```
Discourse Sweep complete.
- Findings retrieved: <N>
- Clusters after dedupe: <M>
- Tier 1-3 citable: <K>
- Tier 4-5 rejected: <L>
- Council synthesis: <ran|degraded>
- Output: <piece>/03-discernment/discourse-themed.md
```

The orchestrator then invokes `research-pipeline/content-writer` to do the actual draft, then `bibtex-builder/bibtex-from-urls` to generate `bibliography.bib` from the Tier 1-3 sources.

## What this skill does NOT do

- It does not draft the post — that's `research-pipeline/content-writer`.
- It does not verify citations — that's `research-pipeline/citation-verifier`.
- It does not build the bibliography — that's `bibtex-builder`.
- It does not run the slop pass — that's `scripts/prose_lint.py` + the Tier-2 LLM sub-agent (invoked from the discern command).

It does one thing: turn the outline + angle into a ranked, themed brief of the last 30 days.

## Degradation behaviors

- **Reddit JSON fetch fails / rate-limited / non-JSON:** drop the `reddit_json` result for that subreddit and rely on the WebSearch reddit query instead. Log it. Never invent reddit hits or engagement counts.
- **No entities resolved (Step 0.5 skipped):** the sweep runs on term queries alone, exactly as before entity resolution existed. This is a valid, non-degraded path for abstract topics.
- **Apify not connected:** fall back to WebSearch with `site:apple.co/podcasts` queries. Log it.
- **research-pipeline/literature-discovery not installed:** skip academic; emit a warning in `sources-verification.md`.
- **Council not configured:** skip Step 4; use unfiltered `discourse.md`. Log it.
- **WebSearch rate-limited or empty result for a query:** log the empty result; do not invent findings.

In all degradation cases, the sweep continues with what it can retrieve. Half a sweep is better than a fabricated full sweep.
