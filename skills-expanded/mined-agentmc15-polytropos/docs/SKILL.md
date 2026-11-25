# Memory skill

A durable, cross-session fact store plus a smart-retrieval layer, engineered so that having
memory **never degrades the model's answers**. That non-degradation property is the whole
design — everything below exists to defend it.

---

## What this is

`skills/memory/SKILL.md` lets a session remember durable facts (user preferences, decisions
and their rationale, environment facts, corrections) and recall only the handful that matter
for the task at hand, under a hard budget. Two stdlib-only engines do the work:

- `bin/memory_store.py` — the durable store: `add` / `update` / `remove` / `list` / `verify` /
  `review`.
- `bin/memory_recall.py` — read-only, budget-capped recall: scores the store against a query,
  applies a relevance gate, and prints only the winners.

The store lives at `memory/` under the plugin root (`PLUGIN_ROOT / "memory"`, the same
placement `journal/` uses), and it is **gitignored, private user data** — a root-anchored
`/memory/` entry in `.gitignore` (the leading slash matters: unanchored `memory/` would also
hide `skills/memory/`). Nothing in either engine reads `Path.home()`; every path derives from
the plugin root or an explicit `--memory-dir` override. The feature prices nothing — no
pricing file is read or imported by either engine.

## The non-degradation design

Memory only helps if it can never hurt. The design addresses three concrete failure modes.

### Context bloat

Recall is **pull-only and script-computed**: the corpus never enters model context. Running
`memory_recall.py --query "..."` reads every fact file, ranks them, and returns only a capped
block — at most `MAX_FACTS = 5` facts, at most `BUDGET_CHARS = 4000` characters total (both
are `memory_recall.py` module constants, overridable per call with `--max-facts` /
`--budget-chars`). Truncation is **whole-fact**: a fact that would overflow the remaining
budget is dropped entirely rather than emitted half-way, and a dropped survivor is disclosed
with an honest trailing line rather than silently vanishing:

```
(+N more above the gate — raise --max-facts/--budget-chars or read memory/index.md)
```

The one edge case — the single top-ranked survivor alone exceeds `BUDGET_CHARS` — still emits
its header line, just with a pointer instead of a body: `(body exceeds budget — read
memory/facts/<slug>.md)`. There is no hook and no session-start injection; the skill's
"effectiveness contract" section pins this in words too: never paste `memory/index.md`, the
store directory, or an uncapped fact set into context — recall always goes through
`bin/memory_recall.py` and its budget.

### Staleness

Every fact carries freshness metadata, and the engines derive one of three states from it —
`fresh`, `stale`, or `expired` — via typed soft-TTLs in `memory_store.py`:

```python
TYPE_TTL_DAYS = {
    "user": 365, "feedback": 365, "project": 90, "reference": 180, "decision": 180,
}
```

(Projects churn fastest; user preferences endure.) A fact is `expired` if its `expires` field
is a date on or before `--now` (the literal `never` never expires); otherwise it's `stale` if
`last_verified` (falling back to `created`) is older than its type's TTL; otherwise `fresh`.
Expired facts are **withheld from recall by default** (`--include-expired` opts back in, for
review flows) and the recall output discloses the count: `(N expired fact(s) withheld —
memory_store.py review to prune)`. Stale facts are not withheld — they're down-ranked (see
below) and their header line carries the literal marker:

```
— STALE, verify before relying
```

`memory_store.py verify <slug>` bumps `last_verified` without touching content (a pure
freshness refresh); `update` also bumps `last_verified`, since rewriting a fact's fields is
itself a verification. `memory_store.py review` is a read-only staleness report — expired
facts first, then stale, each group sorted by slug — that never writes anything, so it's safe
to run at any time; a fully fresh store prints `all <n> facts fresh`. All date math flows
through an explicit `--now YYYY-MM-DD` (default: today), so tests and the demo are
deterministic.

### Noise

A fact is only surfaced if it clears a hard relevance gate in `memory_recall.py`:

```python
GATE_MIN_SCORE = 1.0
GATE_MIN_TERMS = 2
```

Concretely, a fact must match at least `GATE_MIN_TERMS` distinct query terms — or have at
least one query term land as an exact token inside its `tags` field — **and** its final score
must be at least `GATE_MIN_SCORE`. A fact that clears neither condition is not surfaced, full
stop. If nothing clears the gate, `memory_recall.py` prints the pinned line and exits 0:

```
no memory above the relevance gate for this query
```

An empty recall is a **success**, not an error — the skill instructs proceeding without memory
in that case, and explicitly warns against loosening or re-running the query with broader
terms just to force a match.

## The schema

Each fact is one markdown file at `memory/facts/<slug>.md`: flat `key: value` frontmatter
between `---` fences (no YAML library exists in the stdlib, so the parser is a deliberately
trivial ~15-line grammar that splits each line on the first `": "`), followed by a free-text
markdown body.

```
---
schema: 1
name: Deploy target
description: Where we deploy the app
type: reference
tags: deploy, cloudflare
created: 2026-01-10
last_verified: 2026-01-10
expires: never
confidence: high
source: demo (synthetic)
---

Deploy to Cloudflare Workers via wrangler.
```

Field meanings:

| Field | Meaning |
|---|---|
| `schema` | Schema version (currently `1`). |
| `name` | Short human title. |
| `description` | One line — feeds both the index and the ranker (`description` field weight 2). |
| `type` | One of `FACT_TYPES = ("user", "feedback", "project", "reference", "decision")` — drives the TTL. |
| `tags` | Comma-separated lexical hooks — the save-time antidote to the ranker's synonym blindness. |
| `created` | `YYYY-MM-DD`, set on `add`. |
| `last_verified` | `YYYY-MM-DD`, bumped by `add`/`update`/`verify`. |
| `expires` | `YYYY-MM-DD` or `never`. |
| `confidence` | One of `CONFIDENCE_LEVELS = ("high", "medium", "low")` — feeds a ranking multiplier. |
| `source` | Free text: where this fact came from. |

Slugs must match `^[a-z0-9][a-z0-9-]{0,63}$`, validated before any path is composed. Unknown
frontmatter keys round-trip unchanged. `[[slug]]` wikilinks are stored verbatim in bodies, not
resolved.

`memory/index.md` is a **fully derived** artifact — one line per fact, regenerated on every
mutation (`add`/`update`/`remove`) — never hand-edited and never a source of truth. Fact files
under `memory/facts/` are the only source of truth.

## Ranking, in one paragraph

`memory_recall.py` implements a pure-stdlib lexical BM25-lite. Query and fact text are
tokenized with `re.findall(r"[a-z0-9]+", text.lower())`, dropping 1-character tokens and a
pinned stopword set. Per-fact term frequency is weighted by field —
`FIELD_WEIGHTS = {"name": 3, "tags": 3, "description": 2, "body": 1}` — then combined with a
corpus-wide inverse document frequency, `idf(t) = log(1 + (N - df + 0.5) / (df + 0.5))`, and
saturated BM25-style with `K_SAT = 1.2`: `idf(t) * wtf / (wtf + K_SAT)`. The raw score is the
sum of that term over every distinct matched query term. The raw score is then multiplied by a
staleness multiplier (`STALE_MULT = 0.6` if the fact is stale, `1.0` otherwise) and a
confidence multiplier (`CONF_MULT = {"high": 1.0, "medium": 0.9, "low": 0.7}`) to get the
final score used for the gate and ordering. Survivors sort by score descending, then
`last_verified` descending, then slug ascending — fully deterministic. The stated limitation
is that a purely lexical ranker is blind to synonyms and paraphrase (there is no doc-length
normalization at this corpus scale either, an accepted tradeoff); the mitigation is at both
ends — mandatory `tags` at save time give a fact exact-match lexical hooks independent of its
prose, and the skill instructs deriving keyword-rich queries (5–15 salient nouns/tool
names/file names) rather than pasting a whole prompt.

## Day-to-day use

**Recall**, before relying on memory for a task — derive keywords, then:

```bash
python3 bin/memory_recall.py --query "<keywords>"
```

Treat the returned block as advisory context; re-verify any fact flagged `STALE, verify before
relying` against the repo or reality before acting on it. Useful flags: `--max-facts N` /
`--budget-chars N` to tighten the cap, `--include-expired` (review flows only), `--json`, and
`--now YYYY-MM-DD` to pin date math.

**Save** a new fact:

```bash
python3 bin/memory_store.py add --name "..." --type <user|feedback|project|reference|decision> \
  --description "..." --tags a,b --body "..."
```

`add` is dedup-gated: an exact-slug collision, or token-set Jaccard similarity ≥
`DEDUP_JACCARD = 0.5` against an existing fact's name+description+body, exits 2 with `duplicate
of [<slug>] — update it instead (or pass --force)`. Prefer `update` over forcing a duplicate —
it also bumps `last_verified`:

```bash
python3 bin/memory_store.py update <slug> --description "..." --body "..." --tags a,b
```

Wrong fact → remove it immediately: `python3 bin/memory_store.py remove <slug>`.

**Review & prune**, periodically or when asked "what do you remember":

```bash
python3 bin/memory_store.py review
python3 bin/memory_store.py list
```

`review` is read-only and groups expired-then-stale facts, each with a suggested action
(verify / update / remove). `list` shows every fact with its current freshness state for a
full picture.

**Demo** (synthetic store, own temp dir, byte-stable):

```bash
python3 bin/memory_recall.py --demo
```

## Deferred by design

- **Hooks / auto-injection.** Recall is pull-only in v1 — no session-start bulk load, no
  per-turn hook, no settings.json wiring. The default posture is "ask when it helps," not
  "always inject."
- **Cross-harness parity.** Codex has a deliberately recall-only port (`codex/skills/memory/`,
  which documents `review` while the Claude skill also documents add/update/remove/list); no
  Copilot port exists yet. A future kit could mirror it there, the way `harness-parity`
  followed `codex-harness`.
- **Model-assisted re-ranking.** The ranking script never calls a model — determinism and
  zero-cost recall are the point. The skill layers judgment on top of the script's output; it
  does not ask a model to re-score the candidates.
- **Embeddings / vector search.** No pip, no network, no vector store — ranking is the pinned
  stdlib lexical algorithm described above, and nothing else.
