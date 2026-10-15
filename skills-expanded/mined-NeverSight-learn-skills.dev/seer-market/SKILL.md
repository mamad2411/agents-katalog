---
name: seer-market
version: 0.3.0
description: Search, browse, and analyze topics, threads, claims, and market regime
metadata: {"requires":{"bins":["seer-q"]}}
---

# Seer Market Intelligence

> Read [seer-shared](../seer-shared/SKILL.md) for response format, the web UI, and common rules.

## Command Reference

### Entity lookup

```bash
seer-q search "QUERY"           # Fuzzy search across topics, threads, assets
seer-q topic TOPIC_ID           # Topic detail: thesis, bias, all threads within it
seer-q thread THREAD_ID         # Thread detail: snapshot, all claims, evidence counts
```

### List / browse

```bash
seer-q market                   # Global regime + all topics with thread counts
seer-q topics                   # List all topics with thread counts
seer-q threads                  # List all threads (newest activity first)
seer-q threads --topic ID       # Threads in a specific topic
seer-q threads --status active  # Filter by status (active/weakening/divided/resolved)
seer-q claims                   # Latest 100 claims (newest first)
seer-q claims --thread ID       # Claims for a specific thread
seer-q claims --status current  # Filter by status (pending/current/stale/discarded)
seer-q claims --mode observed   # Filter by mode (observed/interpreted/forecast/attributed)
seer-q sources                  # Latest 100 ingested sources
seer-q sources --decision process  # Only processed sources
seer-q sources --tier 1         # Only tier-1 sources
```

### Snapshots

```bash
seer-q snapshot                 # Latest global regime snapshot
seer-q snapshot --history       # Regime snapshot history (default 10)
seer-q snapshot --history --limit 5  # Limit history count
```

### Usage & audit

```bash
seer-q usage                    # Token usage summary (--since P, default 24h)
seer-q decisions                # Decision log (--stage S, --run ID, --entity-type T, --entity-id I, --limit N)
```

## Query Strategy

Map the user's question to the right command sequence:

| User intent | Commands |
|---|---|
| Overall market / "how's the market" | `seer-q market` |
| List all topics | `seer-q topics` |
| Hottest/most active topic | `seer-q topics` → pick highest `thread_count` or most recent activity |
| Specific sector deep-dive (e.g., "AI infra") | `seer-q search "KEYWORDS"` → `seer-q topic ID` |
| Specific angle/trade (e.g., "NVIDIA bear case") | `seer-q search "KEYWORDS"` → `seer-q thread ID` |
| Analyze an asset (e.g., "analyze NVIDIA") | `seer-q search "ASSET"` → fetch relevant topic + multiple thread details |
| Latest events / recent claims | `seer-q claims` → summarize the newest entries |
| Claims for a thread | `seer-q claims --thread ID` |
| Recent sources / what was ingested | `seer-q sources` |
| Bull/bear case for X | `seer-q search "X"` → `seer-q thread ID` → focus on `risk_case`, contradicting claims |
| Market regime history / trend | `seer-q snapshot --history` |
| Global regime details | `seer-q snapshot` |
| Threads in a topic | `seer-q threads --topic ID` or `seer-q topic ID` (which includes threads) |

## Key Response Fields

**Market/Topics:**
- `regime_summary` — one-line market regime
- `standing_thesis` — topic thesis
- `standing_digest` — topic summary
- `bias` — bullish/bearish/neutral/mixed/unclear
- `thread_count` — number of threads in topic
- `view_url` — link to the interactive map (always share — opens the topic on a 3D sphere the user can click around)

**Threads:**
- `thesis` — thread thesis
- `bias`, `status` — current stance and lifecycle
- `snapshot` — detailed analysis: `assessment`, `conviction`, `catalysts`, `outcomes`, `risk_case`, `what_breaks_it`, `assets_exposed`, `top_contradiction`
- `supporting_count`, `contradicting_count` — evidence balance
- `view_url` — link to the interactive map (always share — opens the map focused on this thread in its topic context)

**Claims:**
- `statement` — the claim text
- `claim_mode` — observed/interpreted/forecast/attributed
- `thread_role` — support/contradiction
- `event_date` — when the event occurred
- `status` — pending/current/stale/discarded
- `asset_mentions` — related assets
- `source_id` — link to source

**Sources:**
- `title`, `url` — source identity
- `source_tier` — 1 (highest) to 3
- `gate_decision` — process/drop
- `published_at`, `ingested_at` — timing

**Global snapshot:**
- `regime_summary` — one-liner
- `snapshot.verdict` — stance + rationale
- `snapshot.major_drivers` — key market drivers
- `snapshot.key_uncertainties` — what could change

## Examples

User: "how's the market"
-> `seer-q market`
-> Summarize regime_summary, verdict, top topics by thread count
-> Share the market view_url — mention they can click into topics and explore the driver network there
-> Share each topic's view_url as you mention them

User: "latest 10 events"
-> `seer-q claims`
-> Take first 10 from response (already sorted newest-first)
-> Summarize each claim: statement, event_date, asset_mentions
-> No view_url on individual claims

User: "hottest topic right now"
-> `seer-q topics`
-> Find topic with highest thread_count or most recent thread activity
-> `seer-q topic ID` for detail
-> Summarize thesis, bias, top threads
-> Share the topic view_url — the user can explore all its threads visually on the map

User: "analyze NVIDIA"
-> `seer-q search "NVIDIA"`
-> Fetch each relevant topic and thread
-> Synthesize: bull case (supporting threads), bear case (contradicting/risk), key catalysts
-> Include view_urls as you go so the user can click into any angle that interests them

User: "what's the bear case for AI"
-> `seer-q search "AI"`
-> Find bearish/weakening threads
-> `seer-q thread ID` for the most relevant
-> Focus on risk_case, what_breaks_it, contradicting claims
-> Share thread view_url — the map shows the evidence balance visually

User: "recent sources"
-> `seer-q sources`
-> Summarize: title, tier, published_at, gate_decision
-> Group by decision (processed vs dropped) if useful

User: "how has the market regime changed"
-> `seer-q snapshot --history`
-> Show regime_summary progression over time
-> Note any shifts in stance

User: "what claims support thread X"
-> `seer-q claims --thread ID`
-> Filter/highlight claims with thread_role=support
-> Summarize key supporting evidence
-> Share thread view_url if available
