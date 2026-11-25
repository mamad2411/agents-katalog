---
name: using-brainpalace
description: |
  Expert BrainPalace skill for document search with BM25 keyword, semantic
  vector, hybrid, graph, multi, compute, scan, absence, timeline, and evidence
  retrieval modes.
  Use when asked to "search documentation", "query domain", "find in docs",
  "bm25 search", "hybrid search", "semantic search", "graph search", "multi search",
  "compute query", "scan sessions", "absence query", "timeline query",
  "evidence query", "verify a claim", "find dependencies", "code relationships",
  "searching knowledge base",
  "querying indexed documents", "finding code references", "exploring codebase",
  "what calls this function", "find imports", "trace dependencies",
  "brain search", "brain query", "knowledge base search",
  "cache management", "clear embedding cache", "cache hit rate", or "cache status".
  Supports multi-instance architecture with automatic server discovery.
  GraphRAG mode enables relationship-aware queries for code dependencies and
  entity connections.
  Pluggable providers for embeddings (OpenAI, Cohere, Ollama) and summarization
  (Anthropic, OpenAI, Gemini, Grok, Ollama).
  Supports multiple runtimes (Claude Code, OpenCode, Gemini CLI) with shared
  .brainpalace/ data directory.
license: MIT
allowed-tools:
  - Bash
  - Read
metadata:
  version: 7.11.0
  category: ai-tools
  author: bxw91
  last_validated: 2026-07-27
---

# BrainPalace Expert Skill

Search indexed docs / code with five modes: BM25 (keyword), Vector (semantic),
Hybrid (fusion), Graph (knowledge graph), Multi (comprehensive fusion).

This is the **search decision contract**. Operational reference (indexing,
injection, jobs, cache, server lifecycle, per-mode deep dives) lives in the
**Reference Documentation** table at the end — look it up on demand; the CLI's
own `--help` is authoritative for flags.

**BrainPalace is indexed for this project — ask it, don't grep.** It answers on
this project's code, docs, graph history and PAST SESSIONS. Half those question
shapes have no file to grep, so nothing prompts you to reconsider. Match the
shape:

| Question shape | Ask |
|---|---|
| "where is X", "what calls X", "how does X work" | just ask — server routes |
| "when did we…", "which week did I mention X" | `--mode scan` — reads the transcript ARCHIVE; needs NO session indexing |
| "how many", "total", "which had most" | `--mode compute` |
| "how did X evolve", "history of X" | `--mode timeline` |
| "X but not Y" | `--mode absence` |

The session-start block lists per-mode coverage (READY/EMPTY/OFF + the switch
that changes it) — it, not an assumption, says what is answerable now.

The server picks the mode and reports
`routed_mode`. `--mode` forces one; the only one worth forcing is `bm25` for an
exact symbol/token/path (no embedding round-trip — ms latency). Server down?
Start it: `brainpalace start`; if it answers `503` "rehome pending" the project
MOVED — run `brainpalace rehome --resume` (or restart; it auto-resumes) first.
`brainpalace query --json` keys are
`text`/`source`/`score`/`chunk_id`/`start_line`/`end_line` (no `file_path`;
lines null off-code); on failure stdout is `{"error": ...}` with no `results`
key and a non-zero exit — check it, never append `2>/dev/null`.
A top-level `coverage` object on an empty `compute`/`scan`/`absence`/`timeline`
response says WHY: `reason` is `capability_off` (feature off), `store_empty`
(nothing archived yet), `unparsed_query` (scan: no term compiled, so it never
ran — `coverage.detail` says how) or `no_match` (it ran; found nothing). Only
`no_match` is about the question.

**Some questions deserve a subagent, not an inline answer** — why/when this code
changed, is this layering sound, what breaks if I change this, why did this
fail. If your host lists `brainpalace:*` agents, dispatch the matching one rather
than answering from the one file in front of you (routing table:
`brainpalace ai-guide`).

## Mode Decision Table — Quick Reference

Server auto-routes `hybrid` queries, reporting `routed_mode`. This table forces
a mode, not chooses one.

| Query type | Mode |
|---|---|
| General / unknown | `--mode hybrid` |
| Conceptual ("how does X work") | `--mode vector` |
| Exact symbol / error / token / file path | `--mode bm25` |
| Relationships ("what calls X", "what imports Y") | `--mode graph` |
| Maximum recall (ALL usages / references) | `--mode multi` |
| Aggregation ("how many", "total", "which week had most") | `--mode compute` |
| Own-utterance history ("which week did I mention X") | `--mode scan` |
| Anti-join over typed records ("X but not Y") | `--mode absence` |
| Belief/fact evolution ("how did X evolve", "history of X") | `--mode timeline` |
| Verify a claim ("verify X", "is it true that X") | `--mode evidence` — support + coverage; VERDICT is yours |

Common flags: `--top-k N` (default 5), `--threshold F` (default 0.3),
`--alpha F` (hybrid balance, 0=BM25…1=Vector, default 0.5), `--language CODE`
(per-query BM25 tokenization override; bm25/hybrid only).

Docs rank below code (`ranking.doc_weight`=0.5 default); `--source-types code`
filters.

### Before Anything Else — Project Indexed Check

Run this **first**:

```bash
brainpalace whoami    # exits 0 (indexed + server up), 1 (no project), or 2 (indexed but server down)
```

- **Exit `0`** → `.brainpalace/` exists AND server running. Skill applies.
- **Exit `1`** → no `.brainpalace/` in CWD or any ancestor. **Skill yields silently** —
  use native Glob/Grep/Read as normal. Optionally suggest `brainpalace init`. Do
  NOT print enforcement warnings; do NOT block the task.
- **Exit `2`** → indexed but server not running. Searches fail until started —
  follow "When the server is down" below.

CLI not installed (command not found) → treat as exit `1`, yield.

### Search Rule — Non-Negotiable (when indexed)

When the check passed, BrainPalace is the first entry point for codebase search.
Never use Glob, Grep, or Bash `find`/`grep`/`rg` against indexed project source — even
when you think you know the path or token (see the NUDGE rationale above). Pick
a mode, then:

```bash
brainpalace query "..." --mode <picked> --top-k 8 --json
```

After BrainPalace returns confirmed file paths, use `Read` to open them.

**Ranked, not exhaustive.** `query` returns the top-k best matches, not every
match — a question phrased "find EVERY caller / all usages" is asking for a
guarantee ranked retrieval does not make, and a defining module can rank below
its own consumers. For completeness widen (`--top-k`, `--mode multi`) and
prefer the deterministic paths: `--mode graph` and the `graph` verbs for
relationships, `--mode compute`/`absence` for set questions. The allowances
below cover the rest.

### Delegate or Answer Inline — dispatch triggers

The rule above says never grep. This one says when not to answer alone. Four
question SHAPES need history, blast radius or judgment no single file holds:
why code is this way / when it changed, whether a layer or dependency edge is
sound, what breaks if a symbol changes, an error that ALREADY happened.

**Dispatch on the PRIMARY question asked**, not on every primitive it touches —
the anchor decides. **An anchored specialist always beats the general pair**
(known target → search, no anchor → exploratory research); never a generic
search subagent, which retains grep and bypasses the index. Which agent takes
which anchor: `--tier full`, or your host's `brainpalace:*` agent list.

**Answer inline** when a file you already read, or one query, settles it. These
triggers are for what a single file cannot answer; an agent per question is the
opposite failure.

**If your host lists no `brainpalace:*` agents**, the plugin is not installed —
answer the same questions yourself via `--mode graph`, `--mode timeline`,
`brainpalace graph cochange`; do not try to spawn them.

### Parsing `--json` Output

Per-result keys are `text`, `source`, `score`, `chunk_id`, `start_line`,
`end_line` (`int | null`, null off-code) — there is NO `file_path` or
`content` field. On failure, stdout is
`{"error": ...}` (with `detail`/`hint`) and a non-zero exit, with **no**
`results` key. Never append `2>/dev/null` — diagnostics go to stderr. A
top-level `index_blocked` object means the index is STALE (paused over
budget) — never auto-approve. (Runnable parsing snippet: `--tier full`.)

A top-level `routed_mode` means the server ran a DIFFERENT mode than requested
(auto-route, or read-only → `bm25`); absent when it ran as asked.

**Allowed Glob/Grep (NOT codebase search):** inside a file BrainPalace already
returned; non-indexed paths (`~/.claude/`, `~/.config/`, `/tmp/`, dotfiles,
settings/logs); files changed since `last_indexed`; paths in `exclude_patterns`;
listing directory STRUCTURE only (`ls`, `find <path> -maxdepth N -type d`).

### When the Server Is Down

If `brainpalace query` returns connection-refused / `/health/` non-200 (indexed
but server not running):
1. Task needs codebase search → STOP. Tell the user: "BrainPalace server not
   running. Start it with `brainpalace start`."
2. Task does NOT need codebase search → proceed normally.
3. NEVER fall back to Glob/Grep/find for codebase search "just this once".

Server-down (`.brainpalace/` exists, process not running) is distinct from
not-indexed (no `.brainpalace/` at all → the skill yields).

**Sensitivity:** `sensitivity != "normal"` rows (records, graph nodes, session
chunks, memory — incl. private-session derivatives) are hidden by default
everywhere, incl. memory recall/boost/session-context. `--include-sensitive`
reveals (CLI). `include_sensitive` is a per-request opt-in exposed on the CLI,
on 4 MCP tools and on 6 dashboard routes: NO surface is blanket-safe — check
the call, not the surface.

Full detail: `brainpalace ai-guide --tier full` (MCP: the `ai_guide` tool).

---

## Feedback — rate a routed query

Routed answer wrong or empty? `brainpalace feedback <query_id> --not-useful`
(`query_id` is in `--json`). It re-orders the router, never your results.

---

## Parsing `--json` Output — runnable example

```bash
brainpalace query "..." --mode hybrid --top-k 8 --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
if 'error' in d: sys.exit('brainpalace error: %s' % d['error'])
for r in d['results']:
    print(r['source'], r['score'])
    print(r['text'][:500])
"
```

### `routed_mode` — did my query change mode?

A top-level `routed_mode` is present only when the server executed a different
mode than the one requested. Two causes: the **auto-router** re-routed a
`hybrid` query (to `compute`, `scan`, `absence`, `timeline`, or `graph`), or
**read-only mode** degraded it to `bm25` because no embedding call was possible.

Check it before concluding recall was poor. Four of the re-route targets
announce themselves structurally — `compute`/`scan`/`absence`/`timeline` rows
arrive in their own top-level key with `results` empty. **`graph` does not**: it
returns plain `results`, identical in shape to `hybrid`, so `routed_mode` is the
only signal that the mode changed and the ranking you are looking at came from
graph traversal rather than hybrid retrieval.

```bash
brainpalace query "what depends on QueryService" --mode hybrid --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
if 'error' in d: sys.exit('brainpalace error: %s' % d['error'])
if d.get('routed_mode'):
    print('server re-routed to:', d['routed_mode'])
"
```

### `coverage` — why is this empty?

**`coverage` (deterministic modes only).** Shape:
`{"capability": "session_archive", "available": true, "populated": true,
"reason": null, "detail": null}`. `capability` is `typed_records`
(compute/absence), `session_archive` (scan) or `graph_index` (timeline).
`reason` is null when rows were returned. This replaces the manual
`brainpalace records stats` check — the payload now carries the distinction
directly.

`reason` is one of `capability_off` (the feature is off), `store_empty`
(nothing extracted/archived yet), **`unparsed_query`** (scan only: your query
compiled to no term — it never ran) or `no_match` (it ran; your query found
nothing). **Only `no_match` is about the question.** Treating
`unparsed_query` as "the term is absent" is the specific wrong conclusion this
field exists to prevent: an explicit `--mode scan` query now compiles one term
per content word (stopwords dropped), so `unparsed_query` only fires when
EVERY word was grammar — quote a phrase (`"entity resolution"`), pass content
words, or phrase it as `did I mention X`. `detail` carries that recovery in
one sentence when there is one, and it can also be present with `reason: null`
to caveat rows that WERE returned.

---

## Content Filters — `--domain` / `--meta`

`--domain D` (repeatable, OR) scopes results to chunks ingested under that
`/ingest` domain (the reserved `domain` metadata key — an owner or app
namespace). `--meta k=v` (repeatable, AND across keys) exact-matches any
chunk metadata key, including `/ingest`'s reserved `source`/`source_id`.
Both compose with `--source-types`/`--languages`/`--file-paths` and with
sensitivity default-deny.

---

## Paused (Budget-Blocked) Indexing

Query output (CLI `--json` and the MCP `query` tool) may carry a top-level
`index_blocked` object: `{job_id, folder_path, estimated_tokens, limit,
blocked_since}`. It means an indexing job was PAUSED by the embedding-token
budget: the server is up but the index for that folder is STALE. Nothing was
spent.

1. Tell the user: indexing is paused, results may be stale, and approving
   will spend ~`estimated_tokens` embedding tokens.
2. NEVER approve on your own — approving spends money. Ask the user first.
3. On explicit consent: `brainpalace jobs <job_id> --approve` (over MCP: the
   `jobs_approve` tool). To raise the cap instead, increase
   `indexing.max_embed_tokens_per_job` via `brainpalace config wizard` (or set
   the `INDEX_MAX_EMBED_TOKENS` env var), then approve.

---

## Subagent Dispatch — codebase search

**WHEN to delegate is decided above** — see "Delegate or Answer Inline" in the
decision contract, which routes the four anchored question shapes. This section
covers the mechanics and the harder disambiguation cases; it does not re-decide
whether to dispatch.

Whenever codebase search/exploration goes to a subagent, it goes to one of the
six BrainPalace-only agents below (`subagent_type: <name>`) — never a generic
search subagent (e.g. `Explore`) for code lookup, since those retain grep/find
and will bypass the index. All six have `Glob`/`Grep` disabled and search via
BrainPalace only, so none can quietly fall back to filesystem grep. The
PreToolUse subagent guard (`cli.subagent_guard`, on by default while the server
runs) reinforces this: it acts only on *search-shaped* `Agent`/`Task` spawns (a
prompt that asks to find, locate, trace, list callers, etc.) whose prompt lacks a
`brainpalace query --mode` directive (or the equivalent MCP query-tool `mode:`
argument). By default it `enforce`-denies such a spawn with a fix hint; non-search
spawns pass untouched and all six agents below are allowlisted. Soften to a nudge
with `cli.subagent_guard.mode: advisory` (or `BRAINPALACE_SUBAGENT_GUARD=advisory`).
For a genuine exemption, open the prompt with
`# BRAINPALACE_EXEMPT: <reason of 20+ chars>`.

**Dispatching one of these FROM a subagent: name it explicitly.** A subagent's
context does not list the available agent types, so a subagent cannot discover
these six the way your main session can — it will not spawn what it does not
know exists. It is still permitted to: passing `subagent_type:
brainpalace:code-archaeologist` from inside a subagent works. So when you
dispatch a subagent that may itself need history, migration or incident
analysis, write the agent's exact name into that subagent's prompt. Skills are
unaffected — a subagent sees the BrainPalace skills normally.

### Which agent — route by anchor and question, not by every primitive touched

Two are general-purpose; four are anchored specialists. Most real requests touch
several agents' material — route by the **primary question asked**, not by every
primitive the request happens to touch.

| Agent | Anchor | Primary question |
|---|---|---|
| `search-assistant` | a name or location | one-shot lookup: "where is X / what does the doc say" |
| `research-assistant` | any/none (fallback) | open-ended: "gather what we know about X" |
| `code-archaeologist` | a file / symbol / decision | "why is this like this, and when did it change?" |
| `architecture-reviewer` | a module / layer / dependency edge | "is this architecture sound?" |
| `migration-advisor` | a symbol / API being changed | "what breaks if I change this, and in what order?" |
| `incident-investigator` | an `Error` / failing symptom | "explain this incident" |

**Precedence — resolve in this order, stop at the first hit:**

1. **Specialist anchors first.** `code-archaeologist`, `architecture-reviewer`,
   `migration-advisor`, `incident-investigator` — if the primary question
   anchors on history, soundness, blast radius or a failure, that agent wins,
   however search-shaped the request also looks.
2. **No specialist anchor → the search pair.** Known target (a name or a path)
   → `search-assistant`. Exploratory / no anchor → `research-assistant`.
3. **Maintenance agents are never selected for a retrieval request.**
   `setup-assistant` (install/config), `chat-session-extractor`,
   `graph-triplet-extractor`, `memory-curator` (write BrainPalace's own memory
   and graph) answer no question about the codebase; they are dispatched by
   their own workflows, not by routing.

Two specialists matching means the question is two questions — split it, or ask
the one you actually need answered first.

Worked disambiguation — same material, different question: *"why did renaming
this API break production"* anchors on a **failure that already occurred** →
`incident-investigator` (migration and history are evidence, not the ask).
*"what will renaming this API break"* has no failure yet, prospective only →
`migration-advisor`. *"why did this architecture become layered this way"* is a
**why/when** question → `code-archaeologist`, even though the subject is
architecture; *"is this layering still defensible"* is a **judgment** question on
the same subject → `architecture-reviewer`.

For "what does BrainPalace know about this project" (domains, record metrics,
entity/graph counts, per-mode availability) — dispatch nothing: run
`brainpalace inventory --json` directly. It is six deterministic calls
aggregating shipped surfaces, not a search task any agent should be spawned for.

---

## Multi Mode — Comprehensive Fusion

`--mode multi` combines vector + BM25 + graph via Reciprocal Rank Fusion —
documented as 3-way fusion. **The graph leg is dropped unless the storage
backend is `chroma`** — on any other backend (e.g. PostgreSQL) `multi`
silently degrades to 2-way (vector + BM25) fusion, no error, no warning in
the response. This is a documented, deliberate constraint (graph queries
require the ChromaDB backend) — not a bug, and not something to work around;
just be aware recall may be lower than "3-way fusion" implies on a
non-chroma deployment. Check the active backend if `multi` results look
surprisingly graph-thin.

---

## Compute Mode — Aggregation over Typed Records

`--mode compute` answers set-level questions (sum/count/avg/superlative) over
**typed numeric records** persisted from session distillation — not document
chunks. It is **auto-routed**: queries containing "how many", "total", "which
week had most", etc. are classified as compute-intent and routed to this mode
automatically, falling back to `hybrid` when no metric resolves or records are
empty.

**Prerequisite — session extraction:** records only exist once session
extraction has run (`extraction.mode` — `off` by default). With it off,
`compute` always returns empty, which reads exactly like "search found
nothing" rather than "the record store has never been populated." Before
telling a user compute/absence found no match, check `brainpalace records
stats` — `Total records: 0` means extraction is off or hasn't run yet, not
that the query was wrong.

**What records exist:** HIGH-confidence records are populated from session
distillation. Phase 1 derives counts automatically (files touched, tools used,
decisions, open threads — unit `count`, confidence 1.0). LLM-extracted numeric
measurements (weight, sales, etc.) are stored as PROVISIONAL until a teaching
loop validates them (Phase 4). For now, rely on `compute` for count-type
queries; treat other metrics as experimental until taught.

**Supported operations:** `sum`, `count`, `avg` (explicit), plus superlatives
(`which X had the most/least Y` → `sum` per group, ordered desc/asc, limit 1).
Grouping by `week` (ISO), `month` (`YYYY-MM`), `source`, `subject`, or `unit`.

**`--json` contract for compute:** `results` is always `[]`; rows live under
`compute`. Each row: `label` (group key or `null`), `value` (float),
`metric`, `op`, `group` (group_by or `null`), `unit`, `score`.

```bash
brainpalace query "how many files did I touch per week" --mode compute --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
if 'error' in d: sys.exit('brainpalace error: %s' % d['error'])
for row in d.get('compute', []):
    print(row['label'], row['value'], row['unit'])
"
```

Compute query mode has no switches — it is always selectable and returns empty
when no records exist. Records are extracted automatically whenever session
extraction runs (gated by `extraction.mode`); there is no separate
record toggle. The only compute knob is `compute.min_confidence` in
`.brainpalace/config.yaml`.

---

## Scan Mode — Term Counts over Session Transcripts

`--mode scan` counts a query's terms over the archived session transcripts. A
quoted phrase or a `mention/say/discuss` tell is ONE term; an **explicit**
`--mode scan` bare query contributes one term per content word (stopwords
dropped). With no bucket in the query it returns one row per matching
**session** — "which session mentioned X, and when"; with `per week`/`per
month`/`per day`/`per source` it buckets counts instead — "which week did I
say X most". Rows rank by **coverage first, then occurrences** — the session
or bucket that contains ALL of your terms outranks the one that repeats a
single term, so take the top row rather than the loudest one. Deterministic
and free (no LLM, no embedding). Empty when the session archive is off or no
term parses. Tie-break with compute: typed record metric wins.

**`--json` contract for scan:** `results` is always `[]`; rows live under
`scan`. A session row (the default, no bucket in the query) carries
`session_id`, `archived_date`, `archive_path`, `matched_sessions` (the
pre-cap total), plus `label`, `value`, `unit`, `term`, `score`, with `group`
null. **`excerpt`/`excerpt_ts` are null over MCP** — an excerpt is arbitrary
raw transcript text (a tool result, a file's contents from a Write call), so
it is opt-in and only the interactive CLI opts in. Open `archive_path` when
you need the text; the located fields answer "which session, when" without
it. A bucket row (`per week` etc.) carries `label`
(bucket key), `value`, `unit`, `term`, `group`, `score`, with every session
field null. Both shapes also carry `terms` (every term the query compiled
to), `counts` (per-term occurrences), `coverage` (`|matched| / |terms|` — 1.0
for a single-term query), `matched_terms` and `missing_terms` — the fraction
is checkable, not a bare number.

---

## Absence Mode — Anti-Join over Typed Records

`--mode absence` — anti-join over typed records: subjects present under one
partition value (`metric`/`source`/`domain`) but absent under another
("distance but not duration"). Deterministic, no LLM. Empty when no two
stored values resolve, or nothing qualifies (e.g. no records exist). Same
record-store prerequisite as compute — see "Prerequisite — session
extraction" above; `brainpalace records stats` tells "store is empty" apart
from "nothing is absent."
Auto-routed after compute and scan — a query carrying a compute or scan tell
alongside an absence tell routes there instead (e.g. "did I discuss gmail but
not session" is scan, not absence, because it carries "did i discuss").

**`--json` contract for absence:** `results` is always `[]`; rows live under
`absence`. Each row: `label` (the missing subject), `present_in`,
`absent_from`, `partition` (`metric`/`source`/`domain`), `score` (reserved,
always `0.0`).

---

## Timeline Mode — Edge-Validity / Supersession History

`timeline` — walk an entity's edge-validity/supersession history in the graph:
how a belief/fact evolved ("how did the auth decision evolve", "history of
auth.py"). Deterministic, no LLM. Requires the graph index (`ENABLE_GRAPH_INDEX`);
empty when the named entity resolves to no graph node or has no edges.
Auto-routed after compute, scan, and absence — a query carrying one of those
tells alongside a timeline tell routes there instead.

**`--json` contract for timeline:** `results` is always `[]`; rows live under
`timeline`. Each row: `subject`, `predicate`, `object`, `valid_from`,
`valid_until` (`null` = still valid), `valid`, `score`.

---

## Session Memory — Optional, Separately Gated

Recall of prior AI-coding sessions (past-session transcript chunks and distilled
decisions) is an **optional feature, gated independently** of document search.
The SessionStart context block reports its state either way — on OR off, naming
the switch — because "no line" is unreadable: it cannot be told apart from "this
project has no session data", and that reading is why the feature goes unused.
Act on the block you actually receive, never on a fixed expectation.

**Two independent capabilities, and the difference decides whether `scan`
works.** *Archiving* copies raw transcripts into `.brainpalace/`; *indexing*
embeds them. `--mode scan` reads the **ARCHIVE** — it answers with indexing
switched off, and a context line saying session indexing is off is NOT a reason
to skip it. Only semantic recall of transcript chunks needs the index. When
either is off, disabled data stays hidden from results (it is never silently
stale), but the coverage rows still say so. Manually-saved memory
(`brainpalace remember`) is always available via `brainpalace recall`.

Curated memory is writable in full, not just as one line of text: `memorize`
takes `memory_type` (decision|fact|preference|requirement|issue|note),
`confidence` (0.0-1.0 — it scales the memory's ranking boost), `sensitivity`
and `evidence` refs. Its `origin` defaults to `ai`, which is what you are;
pass `user` only when relaying someone's own words.

Retire a memory with `memory_obsolete` rather than `memory_delete` — naming a
replacement records it as superseded, which the ranker reads; deleting it
loses the history. `memories_list` filters by tag, section, or the `source_id`
a memory's evidence addresses.

To ask what one source produced, use `source_timeline` (chunks, memories,
records, references and edges from that source id, in time order) or
`graph_edges` (every edge derived from one file, superseded ones included).

`entity_profile` assembles what is known about one person — aliases, links,
graph relations and curated memories — each item carrying the address you can
follow to check it. It is read-only and assembled per call; there is no stored
profile document to go stale. Filter the memory half with `types` and
`status`. A person whose `sensitivity` is not `normal` is not returned at all,
and the 404 is deliberately the same one an unknown id gets.

Before writing a memory that may already exist, ask `memories_similar` — it
returns what the write-time deduplicator would have collided with, ranked, and
changes nothing. `memory_confirm` restates that a memory is still true without
touching its text or its confidence.

`graph_timeline` gives one entity's edge history directly. `graph_contradictions`
reports where the same subject has two live edges with the same predicate and
different objects — a deterministic scan, not an inference, so it flags
candidates and leaves the judgement to you.

---

## Reference Catalog — Lazy-Tier Pointers

AI clients may search references: `brainpalace references search "<query>"`
semantically searches summary text over the lazy-tier reference catalog
(pointer + summary entries for sources fetched-and-extracted on demand — not
yet embedded as full document chunks). Top matches also surface inline in
`hybrid`/`vector`/`multi`/`graph` results, tagged `type: reference`, so you
may see one without searching for it directly. `brainpalace references
resolve <id>` prints the stored pointer + summary; ingest the resolved body
as searchable text via `brainpalace ingest` when you need it in full.

---

## When Not to Use

This skill focuses on **searching and querying**. Do NOT use for installation,
API-key configuration, server setup, or provider configuration — use the
`configuring-brainpalace` skill. Assumes BrainPalace is already installed,
configured, and running with indexed documents.

---

## Reference Documentation

Per-mode deep dives, tuning, and examples (links resolve in the plugin skill):

| Guide | Description |
|-------|-------------|
| [BM25 Search](references/bm25-search-guide.md) | Keyword matching, `--language` override, threshold tuning |
| [Vector Search](references/vector-search-guide.md) | Semantic similarity for concepts |
| [Hybrid Search](references/hybrid-search-guide.md) | Combined keyword + semantic, `--alpha` tuning |
| [Graph Search](references/graph-search-guide.md) | GraphRAG, relationship/dependency queries, traversal depth |
| [Server Discovery](references/server-discovery.md) | Auto-discovery, multi-instance sharing, lifecycle |
| [Provider Configuration](references/provider-configuration.md) | Environment variables and API keys |
| [Integration Guide](references/integration-guide.md) | Scripts, Python API, CI/CD, cache management |
| [API Reference](references/api_reference.md) | REST endpoints, indexing/folders/jobs, eviction summary |
| [Troubleshooting](references/troubleshooting-guide.md) | Common issues and solutions |

Operational commands not covered above are self-documenting via `--help`:
`brainpalace index|folders|jobs|cache|inject|types <…> --help`. Content-injection
authoring (the `process_chunk` protocol) is specified in `docs/INJECTOR_PROTOCOL.md`.

---

## Graph verbs (path / impact / co-change)

Beyond `--mode graph` retrieval, three CLI verbs answer structural questions
directly (SQLite graph store only — no embedding call, works on any backend):

```bash
brainpalace graph path <src> <dst> --json    # shortest edge paths between two nodes
brainpalace graph impact <node> --json       # what transitively depends on the node
brainpalace graph cochange <file> --json     # files that change together (git history)
```

Reference nodes by canonical id (absolute file path, or `path:fqname` for a
symbol) or by a unique display name; an ambiguous name fails with the
candidate ids listed. On failure stdout is `{"error": ...}` with a non-zero
exit — same contract as `query --json`. `cochange` needs `git_indexing`
enabled.

---

## Cross-instance search (household multi-instance)

Cross-instance search: `query --also <path-or-url>` (repeatable) fans a query
out to sibling BrainPalace instances and RRF-merges the results, tagging each
`--json` result with an `"instance"` key (`"local"` or the sibling's
path/URL); a down sibling warns on stderr and is skipped (local results still
render).

---

## Limitations

- Vector/hybrid/graph/multi modes require an embedding provider configured
- Graph mode requires additional memory (~500MB extra); GraphRAG is enabled by default (`graphrag.enabled: true` / `ENABLE_GRAPH_INDEX`), disable with `ENABLE_GRAPH_INDEX=false`
- Supported formats: Markdown, PDF, plain text, code files (Python, JS, TS, Java, Go, Rust, C, C++)
- Not supported: Word docs (.docx), images
- Server requires ~500MB RAM for typical collections (~1GB with graph)
- Ollama requires local installation and model download
