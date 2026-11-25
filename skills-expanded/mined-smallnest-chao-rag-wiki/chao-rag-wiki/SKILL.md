---
name: chao-rag-wiki
description: "Use when building or querying a RAG knowledge base over the local raw/ document corpus using turbovec vector search. Triggers: 'build rag', 'rag query', 'search my docs', 'what do my notes say about', '索引 raw', 'rag 检索', or any mention of 'chao-rag-wiki' / 'rag wiki'."
---

# Chao RAG Wiki

Build a vector index over the documents in `raw/` and answer questions by
retrieving the most relevant chunks. Retrieval is **hybrid**: dense semantic
search (**turbovec** `TurboQuantIndex`) fused with lexical **BM25** keyword
search and literal **full-text** matching via Reciprocal Rank Fusion, with an
optional **LLM rerank** second stage. turbovec keeps the whole corpus in a few
MB of RAM; BM25 and full-text are built on the fly at query time from the stored
chunk texts.

Embeddings come from any **OpenAI-compatible** `/embeddings` endpoint, selected
by `RAG_EMBED_*` env vars (default: Qianfan `bge-large-zh`, 1024-d). See
*Embedding provider* below.

Unlike `karpathy-llm-wiki` (which compiles raw sources into hand-curated
articles), this skill leaves `raw/` untouched and answers questions directly
from semantic retrieval — no manual compilation step.

## Embedding provider

The embedding client (`embed.py`) is provider-agnostic — it POSTs the standard
OpenAI `{"model","input"}` body to whatever endpoint you configure:

| Env var | Default | Meaning |
|---------|---------|---------|
| `RAG_EMBED_BASE_URL` | `https://qianfan.baidubce.com/v2` | API base (no `/embeddings`) |
| `RAG_EMBED_API_KEY`  | — | Bearer key; falls back to `QIANFAN_API_KEY`, then `OPENAI_API_KEY` |
| `RAG_EMBED_MODEL`    | `bge-large-zh` | model name |
| `RAG_EMBED_DIM`      | `1024` | expected vector dimension |
| `RAG_EMBED_BATCH`    | `16` | inputs per request |

Provider examples (export, then build):
- **Qianfan** (default) — set `RAG_EMBED_API_KEY` (or the legacy `QIANFAN_API_KEY`).
- **OpenAI** — `RAG_EMBED_BASE_URL=https://api.openai.com/v1`,
  `RAG_EMBED_API_KEY=$OPENAI_API_KEY`,
  `RAG_EMBED_MODEL=text-embedding-3-small`, `RAG_EMBED_DIM=1536`.
- **Voyage** (Anthropic recommends Voyage for embeddings — Claude itself has no
  embedding API) — `RAG_EMBED_BASE_URL=https://api.voyageai.com/v1`,
  `RAG_EMBED_MODEL=voyage-3`, `RAG_EMBED_DIM=1024`.
- **OneAPI / OpenRouter / local vLLM** — point `BASE_URL`/`KEY`/`MODEL` at the
  gateway; same OpenAI-compatible shape.

The build records `model` + `base_url` in `manifest.json`. **Querying must use
the same model the index was built with** — dense/hybrid mode re-embeds the
query, so a mismatch is rejected with an error (switch back or rebuild). Pure
`--mode bm25` needs no embedding and works regardless. Changing
provider/model/dim requires a full rebuild.

## Layout

The corpus (`raw/`) and index (`.rag/`) live under a single **root**: the
`RAG_ROOT` env var if set, otherwise the current working directory. So by
default everything is relative to where you run the scripts; set
`export RAG_ROOT=/path/to/wiki` to point the skill at a fixed location
regardless of cwd. `--raw` / `--out` still override per-invocation.

```
$RAG_ROOT (or cwd)/
  raw/                     # source corpus (read-only) — .md / .txt / .markdown
  .rag/                    # generated index (created here, gitignore-able)
    index.tv               # turbovec quantized vector index
    meta.json              # row -> {path, title, heading, text}
    vectors.npy            # raw embeddings (reused on --update)
    manifest.json          # build config (model, base_url, dim) + per-file hashes
```

Helper scripts live in `scripts/` relative to this file:
- `setup_check.py` — first-run preflight: deps, API key, live endpoint check.
- `embed.py` — provider-agnostic OpenAI-compatible embedding client.
- `ragpaths.py` — resolves the RAG root (`RAG_ROOT` env var, else cwd).
- `bm25.py` — dependency-free BM25 (CJK-aware) for lexical retrieval.
- `fulltext.py` — dependency-free literal substring / regex matcher.
- `rerank.py` — optional LLM listwise reranker (provider-agnostic chat API).
- `build_rag.py` — chunk + embed + write the index.
- `query_rag.py` — hybrid/dense/bm25 search, optional `--rerank`.

A pre-provisioned virtualenv with `turbovec`, `numpy`, `requests` sits at
`<skill>/.venv`. **Always invoke the scripts with `<skill>/.venv/bin/python`.**

Requires an embedding API key: `RAG_EMBED_API_KEY` (falls back to the legacy
`QIANFAN_API_KEY`, already set for this user) — see *Embedding provider* above
to use a different one.

## First run — configure the embedding model

**On the first use of this skill in a project** (no `.rag/` exists yet, or the
user is clearly setting it up for the first time), do NOT jump straight to
building. The skill depends on an online embedding model, so guide the user
through configuration first:

1. **Ensure the venv + deps exist** (see Setup below).

2. **Run the preflight check** — it verifies deps, the API key, and that the
   embedding endpoint actually responds with the right vector dimension:

   ```bash
   <skill>/.venv/bin/python <skill>/scripts/setup_check.py
   ```

3. **Read its output and act on each `[!!]` line:**
   - **`no embedding API key set`** — the user must pick a provider and set a
     key. The default is Qianfan (`bge-large-zh`, 1024-d) via `RAG_EMBED_API_KEY`
     (or the legacy `QIANFAN_API_KEY` fallback);
     for another provider set `RAG_EMBED_BASE_URL` + `RAG_EMBED_API_KEY` +
     `RAG_EMBED_MODEL` + `RAG_EMBED_DIM` (see *Embedding provider* for OpenAI /
     Voyage / gateway examples). Have them export it in their shell profile
     (`~/.zshrc`) so it persists. **Never hard-code the key into any file.**
     Re-run the check after they set it.
   - **embedding call failed / unreachable** — likely a bad key, wrong model
     name, or no network to the endpoint. Surface the exact message.
   - **dimension mismatch** — the chosen model returns a different size; tell
     them to set `RAG_EMBED_DIM` to the reported value before building.

4. **Only once the check prints `READY`**, proceed to Build.

The default Qianfan `bge-large-zh` is the tested path, but any
OpenAI-compatible embedding provider works (see *Embedding provider*). This
skill uses an **online** embedding API by design (no local model).

## Setup (run once, or if the venv is missing)

If `<skill>/.venv/bin/python` does not exist:

```bash
python3 -m venv <skill>/.venv
<skill>/.venv/bin/pip install -q turbovec numpy requests
```

---

## Build

Trigger: "build the rag", "index raw/", "rebuild the index", "add new docs".

If this is the first build in the project, run *First run — configure the
embedding model* above first. Then, from the project root (where `raw/` lives)
— or with `RAG_ROOT` exported, from anywhere:

```bash
<skill>/.venv/bin/python <skill>/scripts/build_rag.py
```

`--raw` / `--out` default to `$RAG_ROOT/raw` and `$RAG_ROOT/.rag` (or `./raw`
and `./.rag` when `RAG_ROOT` is unset); pass them explicitly to override.

- Walks `raw/` recursively, splits each file on markdown headings into
  ~1200-char chunks, embeds them, and writes `.rag/`.
- Progress prints to stderr; the corpus here is ~775 files / a few thousand
  chunks and takes a few minutes (network-bound on the embedding API).

**Incremental update (continuous indexing)** — `raw/` grows daily. After files
are added, edited, or deleted, re-run with `--update`. The build hashes every
file's content and only (re)embeds the **new or changed** ones; unchanged files
reuse their cached vectors from `vectors.npy`, and deleted files drop out of the
index automatically. A no-op `--update` (nothing changed) costs no embedding
calls and rewrites nothing.

```bash
<skill>/.venv/bin/python <skill>/scripts/build_rag.py \
  --raw raw --out .rag --update
```

The scan line reports exactly what changed, e.g.
`scan: files=776 | +1 new  ~0 changed  =775 unchanged  -0 removed`.

**Dry run** — preview what an update would do without embedding or writing:

```bash
<skill>/.venv/bin/python <skill>/scripts/build_rag.py \
  --raw raw --out .rag --check
```

**Automate daily** — to keep the index fresh without thinking about it, the
user can add a cron/launchd job (or a git post-merge hook) that runs the
`--update` command above. It is safe to run repeatedly: a no-op exits in
seconds. If the user asks to "set this up to run automatically" or "index every
day", offer to configure it via the `update-config` skill (a hook) or a cron
entry, and confirm the schedule with them first.

Tell the user when the build finishes: the scan summary (new/changed/unchanged/
removed) and how many chunks were freshly embedded vs reused.

---

## Query

Trigger: "what do my docs say about X", "rag query …", "search my notes for …".

1. If `.rag/index.tv` is missing, tell the user to build first (do not
   auto-build a multi-minute job without asking).

2. Retrieve the top chunks as JSON (hybrid is the default and best general
   choice):

   ```bash
   <skill>/.venv/bin/python <skill>/scripts/query_rag.py \
     --out .rag --query "USER QUESTION" -k 8 --json
   ```

   **Retrieval modes** (`--mode`):
   - `hybrid` (default) — fuses dense (semantic), BM25 (keyword), and full-text
     (literal) with Reciprocal Rank Fusion. Use for almost everything.
   - `dense` — vector search only. Best for paraphrased / conceptual questions
     where wording won't match.
   - `bm25` — keyword search only. Best for exact terms, rare tokens, code
     identifiers, names, error strings — anything where the literal string
     matters more than meaning.
   - `fulltext` — literal substring match only (case-insensitive), or a regex
     with `--regex`. Stricter than BM25: it fires only when the *verbatim* query
     string appears in a chunk. Best for exact phrases, code identifiers, error
     strings, and names. In `hybrid` this leg simply contributes nothing when
     there's no literal hit, so it boosts exact matches without hurting
     paraphrased queries.

   In `--json` (and the plain view) each hit carries its own `dense`, `bm25`,
   and `fulltext` sub-scores alongside the fused `score`, so you can see why it
   ranked. `fulltext` is a raw match count (integer); `dense`/`bm25` are their
   respective retriever scores. The fused `score` is an RRF value (small,
   ~0.01–0.05); compare hits to each other, not to an absolute threshold.
   `--rrf-k` tunes fusion (default 60; lower sharpens the top ranks).

   **`--rerank` (optional second-stage LLM rerank)** — retrieval is fast but
   approximate; an LLM judge is slower but understands the query better. Add
   `--rerank` to re-score a wider candidate pool (default top 20, tune with
   `--rerank-pool`) by true relevance, then take the top-k from that reordering:

   ```bash
   <skill>/.venv/bin/python <skill>/scripts/query_rag.py \
     --out .rag --query "USER QUESTION" -k 8 --rerank --json
   ```

   - Adds one chat-LLM call (~10s); use it when precision matters more than
     latency, or when raw retrieval looks noisy / off-topic.
   - Reranked hits carry a `rerank` score (0–10) and the response sets
     `"reranked": true`. **Order results by `rerank` when present.**
   - Best-effort: if the rerank call fails it logs `rerank skipped: …` and
     falls back to retrieval order — never errors out.
   - Works with any `--mode` (including `bm25`, which needs no embeddings).
   - Provider via `RAG_RERANK_*` env (defaults to the embedding endpoint +
     `ernie-3.5-8k`); see *Embedding provider* / Conventions.

3. **Synthesize the answer yourself** from the returned chunks — do not just
   dump them. Read the `text` fields, write a coherent answer, and cite sources
   as markdown links to the raw files, e.g. `[标题](raw/topic/file.md)`.
   - Prefer retrieved content over your own training knowledge.
   - If the chunks don't actually answer the question, say so — don't
     hallucinate from thin matches. In hybrid mode the fused `score` is an RRF
     rank value; lean on the per-hit `dense`/`bm25` sub-scores (and the
     `rerank` score if present) to judge relevance, and treat unrelated hits
     with skepticism.
   - Raise `-k` for broad/synthesis questions, lower it for pinpoint lookups.

4. For a quick human-readable dump (debugging, "just show me the matches"),
   drop `--json` (add `--full` for untruncated chunk text).

---

## Conventions

- `raw/` is read-only. This skill never modifies source documents.
- The index lives in `.rag/` under the RAG root (`RAG_ROOT` env var, else cwd).
  Safe to delete and rebuild.
- Embedding `model` + `base_url` + `dim` are recorded in `manifest.json`;
  dense/hybrid queries verify the live `RAG_EMBED_MODEL` matches and error on
  mismatch (turbovec also stores `dim`/`bit_width` in the `.tv`).
- turbovec returns row ids in insertion order, which map 1:1 to `meta.json`
  rows — that is how a hit becomes a source file + heading.
- BM25 and full-text need no index file, rebuild, or API key — they are
  constructed at query time from `meta.json` chunk texts, so they work on any
  existing index offline. `fulltext` matches the verbatim query (or a regex with
  `--regex`); `bm25` matches tokenized terms.
- Provider config is all env vars (see *Embedding provider*): `RAG_EMBED_*`.
  No keys are ever hard-coded or written into the index. Must rebuild if you
  change provider/model/dim.
- Rerank provider is separate: `RAG_RERANK_BASE_URL` / `RAG_RERANK_API_KEY` /
  `RAG_RERANK_MODEL` (default: the embedding endpoint + key chain, model
  `ernie-3.5-8k`). It's a chat completion endpoint, not an embeddings one, and
  is only used when `--rerank` is passed.
