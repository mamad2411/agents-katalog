---
name: sillage-help
description: >
  Explains the whole logic of a Sillage workspace and the vocabulary behind it — how the persona,
  target accounts, coverage/mapping, watchlists, agents, signal runs, detections and content fit
  together, and what every term means. The reference the other skills assume you already have. Use
  when the model of the product is unclear, before setting up or editing a workspace, or when a
  result doesn't make sense. Use when you hear: "how does Sillage work", "explain the logic",
  "what's a persona", "how do agents work", "what's the difference between a watchlist and the
  target list", "what does coverage mean", "why only company keywords", "what's a signal", "glossary".
metadata:
  owner: pf@getsillage.com
  version: 1.2.0
  model-tier: sonnet
  provider: Sillage MCP v2 (https://api.getsillage.com/api/mcp/v2)
  pairs-with: [sillage-onboarding, sillage-manage-workspace]
---

# How Sillage works — the logic and the glossary

Sillage watches the public web (mostly LinkedIn) for the moments that mean a company or a person is
about to need what you sell, and turns those moments into leads and ready-to-use content. This skill
is the map of _how the pieces connect_ and _what each word means_. It doesn't do anything — it makes
the doing (with `sillage-onboarding` and `sillage-manage-workspace`) make sense.

Read this when the product's model is fuzzy, when a number surprises you, or before you edit a
workspace and need to know what a change actually moves.

## The one thing to understand first

Everything hangs off **one chain**. Each stage feeds the next, and a weak early stage quietly starves
every stage after it:

```
Persona (your ICP)            ── defines who and what companies count
      │
Target Account List (TAL)     ── the companies you want to sell to
      │
      ├─ enrich_company ─►  Coverage / Company Mapping   ── the PEOPLE at each company who match the persona
      │
Watchlists                    ── separate lists you MONITOR (customers, competitors, partners, influencers, champions)
      │
Agents                        ── saved searches; each is one detection rule (keywords, job changes, or a watchlist)
      │
      └─ launch a Signal Run ─►  the agent actually goes and looks
                                     │
                                     ▼
              Signal Detections  +  Workspace Contents   ── what it found: the events, and the raw posts/articles behind them
```

So: **persona → target accounts → coverage → agents → signal runs → detections + content.** If the
persona is thin, the wrong companies qualify. If a company has no coverage, agents that rely on its
people find nobody. If no agent ever runs, there are no detections no matter how good the setup is.

## The two flows people confuse

The single most common confusion (worth internalizing):

- **Coverage / mapping** = resolving a _company_ to its _people_ — the employees whose LinkedIn
  profiles match your persona. This is what `enrich_company` builds. No coverage → no decision-makers
  to track for that company.
- **Content** = the _company page's own_ LinkedIn activity (its posts and the comments under them).
  This exists whether or not any people are mapped.

A company can have rich content and **zero mapped people**, or people mapped and **no content**. When
someone says _"we only get company keywords, never the decision-makers"_, that's this: content is
flowing but coverage is empty. The fix is coverage (`enrich_company` with the company's **domain**),
not more keywords. Full definitions in `reference/glossary.md`. Few or zero signals almost always trace
back here — `sillage-manage-workspace` has the ordered "Troubleshoot — few or zero signals" checklist.

## Agents, runs, and what comes out

An **agent** is a saved search of one **type**:

- `keyword_detection` — watches LinkedIn posts for your keywords.
- `job_posting_keyword_detection` — watches the **job postings** your tracked companies publish for your keywords.
- `job_update` — watches for people changing jobs / getting promoted.
- `competitor` / `partner` / `customer` — company **watchlist** agents (monitor a list of companies you supply).
- `influencer` / `champion` — profile **watchlist** agents (monitor a list of people you supply).

A watchlist agent detects interactions with the entities **you put on the list** — it never discovers
who a company's competitors, partners, or tech vendors are from the corpus. You build the list from
market knowledge; the agent watches it.

Creating an agent doesn't find anything by itself. You **launch a signal run** — that's the agent
going out to look. A keyword or job agent produces **one run**; a watchlist agent produces **two**
(inbound = someone engages the watched entity; outbound = the watched entity engages a target). One
run fans out to one job per target account.

What a run produces is read two ways — the same substrate, two lenses:

- **Signal Detections** — the event feed: "this person did this thing", keyed by agent / signal type.
- **Workspace Contents** — the raw corpus behind those events (the posts, comments, articles),
  filterable by company, person, and type.

The full list of the detection types and the content types is in `reference/signal-taxonomy.md`.

## When signals come back — lead with the outreach brief

Detections are the means, not the end. The moment a run returns signals, the useful move is to turn
them into a short **action brief**, not to dive back into config:

1. **Rank accounts by signal density** — a handful will dominate; those are the hot accounts.
2. **Name the person and the signal that qualifies them** — "Luigi, GM — 12 posts about a new site =
   active expansion", not just "this account had activity".
3. **Give a per-account approach angle grounded in that specific signal** — the outreach writes itself
   from the trigger.

Keep config tuning (lookback, more keywords, more agents) **secondary** — surface the brief first, then
optimize. Burying the one hot lead under a wall of "you could also add these agents" wastes a good run.

## Is a workspace even set up? — the four flags

`get_setup_state` answers this in one call, and its four booleans mirror the chain above:

| Flag                 | Means                                                           |
| -------------------- | --------------------------------------------------------------- |
| `persona_set`        | An ICP exists.                                                  |
| `list_uploaded`      | The target account list has companies in it.                    |
| `ingestion_complete` | Those accounts finished processing (coverage + content pulled). |
| `has_contents`       | There is collected content to read.                             |

All four true = the workspace is live. Any false = that's the next thing to fix. `sillage-manage-workspace`
turns this into a loop.

## When NOT to use

- You want to _do_ something (set up, edit, tune) → this skill only explains; use `sillage-onboarding` to shape
  targeting or `sillage-manage-workspace` to write and edit it.
- You need the exact fields/enums for a persona or agent call → `sillage-onboarding`'s
  `reference/what-sillage-needs.md` and `sillage-manage-workspace`'s `reference/tool-map.md` are the precise
  specs; this skill is the mental model, not the API surface.

## Where to go next

- **Glossary** — every term, defined: `reference/glossary.md`.
- **Signal & content taxonomy** — the full detection and content type list: `reference/signal-taxonomy.md`.
- **To act** — shape inputs with `sillage-onboarding`; write and edit with `sillage-manage-workspace`.
