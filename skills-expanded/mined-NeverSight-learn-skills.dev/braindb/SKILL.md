---
name: braindb
description: Memory recall and save. Use at every conversation start and whenever the user shares personal information, expertise, project context, preferences, or decisions worth remembering long-term.
allowed-tools: Bash Read
---

## BrainDB — Persistent Memory System

You have access to a persistent memory database at `http://localhost:8000`. Use it to remember things about the user across sessions.

### Health check and always-on rules:
!`curl -sf http://localhost:8000/health > /dev/null 2>&1 && curl -s http://localhost:8000/api/v1/memory/rules || echo "BRAINDB_DOWN"`

### Skill version sync:
!`REPO=$(cat ~/.claude/skills/braindb/.repo_path 2>/dev/null); if [ -n "$REPO" ] && [ -f "$REPO/skills/braindb/SKILL.md" ] && ! diff -q ~/.claude/skills/braindb/SKILL.md "$REPO/skills/braindb/SKILL.md" > /dev/null 2>&1; then echo "SKILL_UPDATE_AVAILABLE: $REPO/skills/braindb/SKILL.md"; fi`

**If the output above contains `SKILL_UPDATE_AVAILABLE`**, a newer version of this skill exists in the local braindb repo (updated via `git pull`). Update it now:
```bash
cp <path shown in the output>/skills/braindb/SKILL.md ~/.claude/skills/braindb/SKILL.md
```
Tell the user: "I've updated the braindb skill to the latest version from the repo. The update will take effect on the next skill invocation." Then continue with the current task normally.

---

**If the output above contains `BRAINDB_DOWN`**, the memory database is not running. Do this:

#### Step 1 — Ask the user
> BrainDB isn't running. Do you want me to start it for you?

#### Step 2 — Find the braindb repo

A braindb repo is identified by having **ALL** of these:
- A `docker-compose.yml` at the root
- A `braindb/` Python package directory (contains `main.py`)
- A `pyproject.toml` whose `name = "braindb"`

Search in this order:
1. The current working directory: does `./docker-compose.yml` exist AND `./braindb/main.py` exist?
2. Parent directories up to 3 levels
3. Common locations (use the Glob tool):
   - `~/source/repos/**/braindb/docker-compose.yml`
   - `~/repos/**/braindb/docker-compose.yml`
   - `~/projects/**/braindb/docker-compose.yml`
4. If still not found, ask the user for the absolute path.

#### Step 3 — Start it and cache the repo path

From the braindb repo root:
```bash
cd <braindb-repo-path> && docker compose up -d
```

This builds if needed and starts the `braindb_api` container. The container runs `alembic upgrade head` on startup, then `uvicorn braindb.main:app --host 0.0.0.0 --port 8000`.

**Also save the repo path** so future skill invocations can check for updates:
```bash
echo "<braindb-repo-path>" > ~/.claude/skills/braindb/.repo_path
```

**Note**: the first start (build) can take 1-2 minutes. Subsequent starts take ~5 seconds.

#### Step 4 — Wait and verify

```bash
# Wait up to 30 seconds for it to come up
for i in 1 2 3 4 5 6; do
  sleep 5
  curl -sf http://localhost:8000/health > /dev/null 2>&1 && break
done
curl -s http://localhost:8000/health
```

If the final curl returns `{"status":"ok"}`, you're live.

#### Step 5 — Proceed or fall back

- **If healthy**: continue with the recall workflow below.
- **If user declined** or the start failed: proceed with the task WITHOUT memory. Don't keep retrying. Don't block the conversation.

#### Troubleshooting if startup fails

- `docker compose up -d` fails with "network not found" → the compose file references an external network. Check `docker network ls` for `local-network`, create if missing: `docker network create local-network`.
- `alembic upgrade head` fails → the database connection from `.env` isn't reachable. Tell the user to check `.env` and that their PostgreSQL is running.
- Health check never responds → check logs: `docker logs braindb_api --tail 30`

---

## TOOL PRIORITY (read this first)

BrainDB's power is the graph + embeddings + ranking. Use it; do not fall back
to flat SQL.

1. **`POST /api/v1/memory/context`** (multi-query) — the default for ALL
   **query-driven** recall, discovery, and understanding ("what do we know
   about X?"). BOTH the fuzzy and embedding pathways are **keyword-mediated**
   (the query matches against keyword entities, entities surface via
   `tagged_with`). A two-level diversity quota (per-search-term +
   per-keyword halving) keeps results balanced. Then graph traversal + decay
   + ranking.
2. **`GET /api/v1/memory/tree/<id>?max_depth=N`** — reveals an entity's
   neighbourhood as a nested JSON tree: root keyed by `entity_type`,
   `children` arrays per node, 1-N hops out, keyword + retired-wiki
   noise filtered by default, `_truncated` marker as a last child if
   more remain. Especially useful when you have an entity ID (from a
   previous recall) and want its graph context — often a sharper choice
   than another `/memory/context` call about the same entity. On hub
   entities (wikis with many connections) pass `max_depth=3` to see
   narrative chains.
3. **`POST /api/v1/agent/query` with "delegate to a subagent…"** — for
   multi-step investigation/disambiguation; the agent researches and returns
   a summary.
4. `GET /api/v1/entities…`, `GET /api/v1/entities/<id>/relations` — direct
   lookups (list-by-filter, single-hop relations).
5. **Wikis** — first-class entity type, curated topic pages assembled by an
   internal maintainer + writer pipeline from facts/thoughts tagged with the
   same keyword. To browse: `GET /api/v1/entities?entity_type=wiki`. Full body:
   `GET /api/v1/entities/<id>`. Wikis also surface naturally in `/memory/context`.
   Write paths are documented in the WIKIS section below.
6. **`POST /api/v1/memory/sql` ⚠ exception only — aggregates only.** A flat
   SELECT has no embeddings/graph/ranking. Use it solely for a specific
   structured/aggregate question (counts, GROUP BY, activity-log joins) the
   above cannot express. **Never** for recall, discovery, similarity, or
   understanding. **Never** for "what's around this entity" — that's
   `/memory/tree`.

If you're about to use `/memory/sql` to *find* or *understand* something,
stop — that's a `/memory/context` or `/memory/tree` (or delegated
`/agent/query`) job.

### Previews vs full body

`/memory/context` (and `/memory/search`, `GET /entities`) return **short
previews** per item (~1K); a clipped item ends with
`--truncated (N more) -- full body: get_entity("<id>")`. That's intended —
decide from previews, then read only what you need:

- Full single entity: `GET /api/v1/entities/{id}`.
- Large body: page it — `GET /api/v1/entities/{id}?offset=0&limit=8000`, then
  follow `content_meta.next_offset` until it is `null`. For big documents,
  prefer `POST /api/v1/agent/query` with "delegate to a subagent to read and
  distil entity <id>" so the heavy content never enters this conversation.
- Fact `notes` may include a byte range like `(bytes 245760-252960)` — pass directly as `GET /api/v1/entities/{id}?offset=245760&limit=7200` to read the exact source slice the fact was extracted from.

## RECALL — Before Responding

### Step 1: Formulate targeted queries

Analyze the user's message. Extract the **core topics** that need memory context. Create **multiple targeted queries** — do NOT paste the raw user message.

**Query strategy** — BrainDB's retrieval is keyword-mediated, so:

- Prefer **multiple narrow queries** (single keywords / bare names) over one long sentence. Keywords are short, so a short query matches them cleanly; a long phrase dilutes pg_trgm similarity against the keyword.
- The per-search-term quota reserves slots for EACH query you pass, so adding a bare keyword as one of your queries guarantees it surfaces (it doesn't compete with the broader phrases).
- Use terms that match how entities are STORED. Common keyword conventions: `user-profile`, `expertise`, `project-decision`, `user-preference`.

Examples (narrow + one broader angle, mixed):

| User says | Queries |
|-----------|---------|
| "help me refactor this React component" | `["user-profile", "React", "user-preference code style refactoring"]` |
| "let's work on the IR pipeline" | `["investor-relations", "IR", "deployment workflow"]` |
| (new conversation, no specific topic) | `["user-profile", "expertise", "working style"]` |
| "what's the best way to deploy this?" | `["deployment", "infrastructure", "production services"]` |

Always include a `"user-profile"` query on the first message of a conversation — you need to know who you're talking to.

### Step 2: Call the multi-query context endpoint

```bash
curl -s -X POST http://localhost:8000/api/v1/memory/context \
  -H "Content-Type: application/json" \
  -d '{"queries": ["narrow1", "narrow2", "one broader phrase"], "max_depth": 3}'
```

`max_results` defaults to 30 — leave it unless you specifically want fewer.

### Step 3: Evaluate results and retry if weak

If you got **0 results**, your query terms didn't match stored content. Reformulate with more specific terms that would actually appear in entity content or keywords.

**If results are weak — Retry 1:** Reformulate queries with different terms.
- "machine learning" missed? Try `"ML artificial intelligence data science"`
- Too specific? Broaden: `"user-profile technical background"` instead of `"user-profile Python metaprogramming"`
- Too broad? Narrow: `"React hooks state management"` instead of `"frontend development"`

**If still weak — Retry 2:** Final broad sweep:
```json
{"queries": ["user-profile expertise", "project-decision", "user-preference"], "max_results": 15}
```

After 2 retries, accept what you have and proceed.

### Step 4: Use results naturally

**NEVER paste raw JSON API responses into the conversation.** Parse results silently and use the content to inform your response. When you need to show the user what's in memory, format it as clean bullet points or a markdown table — not JSON.

Let recalled facts inform your response. **Do NOT announce** "I found in memory that..." unless sharing the memory is directly relevant. If you know the user is senior in ML, calibrate your explanations accordingly — don't narrate that you remembered it.

---

## SAVE — After Responding

After each interaction, evaluate what you learned. The policy is **RECALL → ASK → SAVE.**

### Saving philosophy — always ASK the user first

Always recall first. If what the user shared is **net-new** (not already in
`/memory/context`), **ASK the user** before saving:

> "I haven't seen this before — should I save it as a fact / thought / rule?
> (I'd tag it with keywords X, Y; importance Z.)"

Only persist after the user confirms. The user has the final say on what
becomes long-term memory. Auto-saves without confirmation dilute signal and
accumulate junk; user-confirmed memory is higher-signal and traceable.

**Exception** — behavioural rules the user explicitly stated as rules ("from
now on, always X"; "never do Y") can be saved without an extra confirmation —
they already said it. Just surface the action: "Saving that as a rule."

Once the user agrees:

- **Create RELATIONS for every new entity.** Connect it to existing entities
  found during recall. Multiple relations per entity is ideal — the graph's
  value comes from density.
- **Thoughts (your own inferences about the user) — ASK before persisting,
  same as facts.** A thought is still memory; the user should agree it
  belongs there.

### What to save as

| Information | Type | Certainty | Importance | Source | Required keywords |
|-------------|------|-----------|------------|--------|-------------------|
| Core identity (role, company) | fact | 0.9 | 0.9 | `user-stated` | `"user-profile"` |
| Strong expertise area | fact | 0.8-0.9 | 0.8 | `user-stated` | `"user-profile"`, `"expertise"` |
| Preference / working style | fact | 0.7-0.8 | 0.7 | `user-stated` | `"user-preference"` |
| Behavioral correction | rule | — | 0.8 | `user-stated` | category: `"behavior"` |
| Project decision | fact | 0.7-0.9 | 0.6-0.8 | `user-stated` | `"project-decision"` |
| Your inference about user | thought | 0.5-0.7 | 0.5 | `agent-inference` | `"inference"` |
| Casual mention | fact | 0.5-0.6 | 0.4 | `user-stated` | topic-specific |
| URL / reference | source | — | 0.5-0.7 | varies | topic-specific |
| Local file / document / dataset | datasource | — | 0.6-0.8 | `document` | topic-specific |
| Info from another person/system | fact | 0.6-0.8 | 0.5-0.7 | `third-party` | topic-specific |

### How to save

```bash
# Save a fact (user told you something)
curl -s -X POST http://localhost:8000/api/v1/entities/facts \
  -H "Content-Type: application/json" \
  -d '{"content": "...", "certainty": 0.8, "source": "user-stated", "keywords": ["user-profile", "topic"], "importance": 0.7}'

# Save a thought (your inference)
curl -s -X POST http://localhost:8000/api/v1/entities/thoughts \
  -H "Content-Type: application/json" \
  -d '{"content": "...", "certainty": 0.6, "source": "agent-inference", "context": "what triggered this inference", "keywords": ["inference", "topic"], "importance": 0.5}'

# Save a behavioral rule
curl -s -X POST http://localhost:8000/api/v1/entities/rules \
  -H "Content-Type: application/json" \
  -d '{"content": "...", "source": "user-stated", "category": "behavior", "priority": 70, "always_on": false, "keywords": ["user-preference", "topic"], "importance": 0.8}'

# Save a source (URL bookmark — external links, web pages)
curl -s -X POST http://localhost:8000/api/v1/entities/sources \
  -H "Content-Type: application/json" \
  -d '{"content": "description of the source", "source": "third-party", "url": "https://...", "keywords": ["topic"], "importance": 0.5}'

# Save a datasource (file, document, or dataset with content to read)
curl -s -X POST http://localhost:8000/api/v1/entities/datasources \
  -H "Content-Type: application/json" \
  -d '{"content": "description of the file/document", "source": "document", "file_path": "/path/to/file", "keywords": ["topic"], "importance": 0.6}'
```

**source vs datasource**: Use `source` for lightweight URL bookmarks. Use `datasource` for local files, documents, datasets — anything with a `file_path` or content to read.

### Content guidelines

- **Concise**: 1-2 sentences max. Write `"Dimitris has 10+ years Python experience, primarily data science and ML."` — not a paragraph.
- **Full terms in content**: Write "machine learning" not "ML". Put abbreviations in keywords: `["machine-learning", "ML"]`.
- **Standalone**: Content must make sense without this conversation. Write `"Prefers simple code over abstractions"` — not `"User said they don't like what I did."`
- **Both forms in keywords**: Include full terms AND abbreviations: `["machine-learning", "ML", "artificial-intelligence", "AI"]`.

### Before saving: check for duplicates

Look at your recall results. If a fact already exists covering the same information:
- **Skip** if identical
- **Update notes** on the existing entity via PATCH if the new info adds nuance
- **Create new** only if genuinely different information

### After saving: create relations

Connect every new entity to at least one existing entity found during recall:

```bash
curl -s -X POST http://localhost:8000/api/v1/relations \
  -H "Content-Type: application/json" \
  -d '{"from_entity_id": "<new_id>", "to_entity_id": "<existing_id>", "relation_type": "elaborates", "relevance_score": 0.7, "description": "why these are related"}'
```

Relation types: `supports`, `contradicts`, `elaborates`, `refers_to`, `derived_from`, `similar_to`, `is_example_of`, `challenges`

### Finding relation targets beyond recall

Recall is scoped to the current conversation topic. Good relation targets often exist outside those results. Before settling for no relations, actively search for candidates:

- List entities by keyword: `curl -s "http://localhost:8000/api/v1/entities?keyword=user-profile&limit=30"`
- List by type: `curl -s "http://localhost:8000/api/v1/entities?entity_type=fact&limit=30"`
- Check existing relations: `curl -s http://localhost:8000/api/v1/entities/<UUID>/relations`
- Explore the graph tree: `curl -s http://localhost:8000/api/v1/memory/tree/<UUID>?max_depth=2`

### Use a subagent for relation discovery

To avoid polluting your main context with large JSON results, **delegate relation discovery to a subagent**. The subagent searches BrainDB, finds candidates, creates the relations, and returns a brief summary. Your main context stays clean.

Spawn a subagent with a task like:
> "Search BrainDB for entities that should be related to this new entity: [content summary].
> Check `GET /api/v1/entities?entity_type=fact&limit=30` and `GET /api/v1/entities?entity_type=thought&limit=30`.
> For each good match, create a relation via `POST /api/v1/relations` with appropriate type and relevance.
> Return a summary of relations created (entity IDs, types, descriptions)."

This pattern keeps the graph dense without flooding the main conversation.

### What NOT to save

- Ephemeral task details (specific error messages, temp file paths, "currently debugging X")
- Things already in the database (you just checked!)
- Information that will be stale by next session

---

## EXPLORE — Listing and Browsing

### List entities by type / keyword / source
```bash
curl -s "http://localhost:8000/api/v1/entities?entity_type=fact&limit=50"
curl -s "http://localhost:8000/api/v1/entities?keyword=user-profile&limit=50"
curl -s "http://localhost:8000/api/v1/entities?source=user-stated&limit=50"
```

### View entity relations
```bash
curl -s http://localhost:8000/api/v1/entities/<UUID>/relations
```

### Explore entity graph tree
```bash
curl -s http://localhost:8000/api/v1/memory/tree/<UUID>?max_depth=2
```

### Delete an entity or relation
```bash
curl -s -X DELETE http://localhost:8000/api/v1/entities/<UUID>
curl -s -X DELETE http://localhost:8000/api/v1/relations/<UUID>
```

### Activity log — when and how things happened

Every create/update/delete/search/context/ingest is logged. Query it to understand history and context.

```bash
# Recent activity (last 20)
curl -s "http://localhost:8000/api/v1/memory/log?limit=20"

# Filter by operation
curl -s "http://localhost:8000/api/v1/memory/log?operation=create&limit=20"
curl -s "http://localhost:8000/api/v1/memory/log?operation=ingest&limit=20"

# History for a specific entity
curl -s "http://localhost:8000/api/v1/memory/log?entity_id=<UUID>"

# Since a timestamp
curl -s "http://localhost:8000/api/v1/memory/log?since=2026-04-08T00:00:00Z"
```

Use this to answer "when did I learn this?" or "what was I working on yesterday?"

### Read-only SQL — EXCEPTION tool, aggregations only

⚠ Not a recall/discovery tool (see TOOL PRIORITY at the top). A flat SELECT
throws away embeddings, graph and ranking — everything BrainDB is good at.
Use it **only** for a specific structured/aggregate question the dedicated
endpoints cannot express (counts, GROUP BY, activity-log joins). For finding
or understanding anything, use `/memory/context` or a delegated `/agent/query`.
Only `SELECT` and `WITH` queries are allowed; 5s timeout; 1000 row limit.

```bash
# Count entities by source
curl -s -X POST http://localhost:8000/api/v1/memory/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT source, COUNT(*) FROM entities GROUP BY source"}'

# Find high-importance facts added recently
curl -s -X POST http://localhost:8000/api/v1/memory/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT id, content FROM entities WHERE importance > 0.7 AND created_at > now() - interval \"7 days\" ORDER BY created_at DESC"}'

# Join log with entities
curl -s -X POST http://localhost:8000/api/v1/memory/sql \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT l.timestamp, l.operation, e.content FROM activity_log l JOIN entities e ON e.id = l.entity_id ORDER BY l.timestamp DESC LIMIT 20"}'
```

Reiterate: `/memory/context` (+ delegated `/agent/query`) is the default for
everything. `/memory/sql` is the rare exception for true aggregations only.

---

## WIKIS — Auto-Curated Topic Pages

Wikis are canonical topic pages BrainDB assembles automatically from
facts/thoughts tagged with the same keyword. An internal maintainer runs
every 60s, scans for orphan keywords (a keyword with members but no wiki
yet), and decides per-orphan: **attach** (the topic already has a wiki),
**create** (mint a new one), **consolidate** (merge duplicates), or
**skip** (not a wiki-worthy subject). Approved suggestions then become wiki
bodies via the wiki writer. You usually don't need to do anything — saving
facts with consistent keywords is enough; the pipeline materialises the
wikis on its own.

### Recall — browse and read wikis

```bash
# List all wikis (most recent first), previews only
curl -s "http://localhost:8000/api/v1/entities?entity_type=wiki&limit=50"

# Read a wiki body in full
curl -s http://localhost:8000/api/v1/entities/<UUID>
```

Wikis surface in `/memory/context` automatically — you don't have to ask
for them separately when doing topic recall.

### Write — indirect (default): let the pipeline decide

1. Save your facts with the right keyword (the subject's bare name —
   `keywords=["Sawki"]`, not `["Sawki the employee"]`).
2. (Optional) Nudge the pipeline so the maintainer evaluates the new
   keyword *now* rather than on the next scheduler tick:

```bash
curl -s -X POST http://localhost:8000/api/v1/wiki/cron
```

The cron is **idempotent** (safe to call any time). It enqueues triage
jobs for orphan keywords; the scheduler then runs maintain → write on
its next 60s tick. The maintainer can still decide to **skip** the
orphan if the subject isn't worth a wiki (e.g. an infrastructural
keyword) — that's expected and not an error.

Inspect what's pending:

```bash
curl -s "http://localhost:8000/api/v1/wiki/jobs?status=pending&limit=20"
```

### Write — direct (power user, rare): bypass the pipeline

When you need full control over the body and you know exactly what the
wiki should say, you can create one directly:

```bash
curl -s -X POST http://localhost:8000/api/v1/wikis \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Sawki\n\nFull markdown body here...",
    "canonical_name": "Sawki",
    "disambiguation": "Team member, distinct from other people with similar names",
    "language": "en",
    "member_keyword_ids": ["<keyword-uuid>"],
    "keywords": ["Sawki", "Egypt", "Petros"],
    "importance": 0.7,
    "source": "user-stated"
  }'
```

⚠ This **bypasses the maintainer's dedup logic.** If a wiki for that
subject already exists, you'll create a duplicate that someone (or the
next `consolidate` maintainer decision) has to clean up. Prefer the
indirect path unless you specifically know why the pipeline can't do
what you need.

`member_keyword_ids` requires existing keyword UUIDs. Find them via:

```bash
curl -s "http://localhost:8000/api/v1/entities?entity_type=keyword&content=<name>"
```

We intentionally do NOT document `POST /wiki/maintain` or `POST
/wiki/write` here — they're claim-based (take no target) and only make
sense as scheduler-internal steps.

---

## INGEST — Files from `data/sources/`

The repo has a `data/sources/` directory for local files. To ingest a file (reads content, hashes it, counts words, creates a datasource entity):

```bash
curl -s -X POST http://localhost:8000/api/v1/entities/datasources/ingest \
  -H "Content-Type: application/json" \
  -d '{"file_path": "data/sources/article.md", "keywords": ["finance","ml"], "importance": 0.7, "source": "document"}'
```

`file_path` is resolved relative to the container working directory (the repo root mounted at `/app`), so `data/sources/article.md` works. Absolute paths also work if mounted.

For auto-ingest on new files, nothing to run — the `watcher` sidecar container polls `data/sources/` every ~7s and ingests new files automatically, then runs the agent-driven fact-extraction pipeline (see `braindb/ingest_watcher.py`). Drop a file into `data/sources/` and it just works; watch progress with `docker logs braindb_watcher -f`.

---

## Error Handling

- If BrainDB is **unreachable** (connection refused): proceed without memory. Do not error out or keep retrying.
- If a **save fails** (400/500): move on. Do not block the conversation over a failed save.
- If the API **returns empty results**: that's normal for a new database. Save what you learn — future recalls will find it.
