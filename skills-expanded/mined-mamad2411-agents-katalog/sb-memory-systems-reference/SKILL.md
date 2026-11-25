---
name: sb-memory-systems-reference
description: >-
  Domain-theory reference for the second-brain plugin's memory mechanisms AS BUILT HERE: BM25
  field-weighted scoring, RRF hybrid fusion and the post-RRF-boost bug class, the ONNX embedding
  pipeline and its bm25-only degradation contract, MinHash near-duplicate detection (capture
  NOOP/UPDATE, dream DEDUPLICATE, FORGET cross-check), deterministic label-propagation clustering,
  the bi-temporal edge store (assert/invalidate, supersedes), structural-importance-only
  forgetting, the REFLECT operation, the shipped PageRank code-map, and the lethal-trifecta
  consolidation security model. Load it when a task touches ranking/scoring math, similarity
  thresholds, dedup/forget/cluster/reflect semantics, graph validity intervals, or when deciding
  whether a proposed boost/weight/decay is safe — and when evaluating an idea borrowed from
  mem0/Letta/Graphiti/GraphRAG/Generative-Agents papers (the borrow ledger records each verdict).
  Do NOT load it for wiring, data paths, or hook plumbing (use sb-architecture-contract), for
  external novelty/positioning claims (use sb-external-positioning), or for live-failure triage
  (use sb-debugging-playbook).
---

# Memory-systems reference (theory as applied in this repo)

Each section: a few lines of theory, then exactly where the mechanism lives (file:line), the
project-specific parameters, and the deviation from the textbook/paper version — with the incident
that forced the deviation. Line numbers reference the working tree as of 0.33.31 (2026-07-05,
uncommitted release batch); re-verify with the one-liners in Provenance before trusting counts.

Terms used throughout (defined once):

| Term | Meaning |
|---|---|
| BRAIN_DIR | runtime state dir, default `~/.second-brain` (resolved ONLY via `mcp/src/brain-paths.ts` / lib.sh) |
| KNOWLEDGE_DIR | knowledge dir, default `~/knowledge`; the wiki lives at `$KNOWLEDGE_DIR/wiki/<category>/` |
| dream | background consolidation run on a STAGING copy of the wiki (`$BRAIN_DIR/dreams/drm_*/`); applied to live only via `dream_accept` |
| drainer | out-of-band transcript extractor `scripts/extract-drain.sh` (timer-run, outside sessions) |
| FORGET | the dream phase proposing low-value pages for reversible archiving (never hard-delete) |
| MOC | "map of content" hub page (`wiki/projects/<key>.md`, `wiki/themes/theme-<id>.md`) — generated, excluded from clustering input |
| ai-block | machine-first `<!-- ai:begin -->…<!-- ai:end -->` region inside a wiki page (claim/action fields) |

Mechanism → home, at a glance:

| Mechanism | Lives in | Key knobs (defaults) |
|---|---|---|
| BM25 + RRF hybrid search | `mcp/src/tools/knowledge-search.ts` | weights 3/2/2/1.5/1; RRF_K=60; TOP_K=8; floor ratio 0.15 |
| ONNX embeddings | `mcp/src/tools/embeddings.ts` | MiniLM-L6-v2, 384-dim; `SECOND_BRAIN_DISABLE_EMBEDDINGS=1` |
| MinHash near-dup | `mcp/src/tools/minhash.ts` (+ `scripts/wiki-redundancy.sh` shim) | k=3 shingles, 128 hashes; thresholds 0.9 / 0.7 / 0.8 per consumer |
| Label-prop clustering | `mcp/src/tools/graph-cluster.ts` + `graph-cluster-cli.ts` | minSize 4, cap 8 clusters, maxIter 20 |
| REFLECT | `agents/dream-runner.md:144-176` | `SB_DREAM_REFLECT=off` (machine-enforced) |
| Bi-temporal edges | `mcp/src/tools/graph-store.ts` + `scripts/merge-edges.sh` | 5 edge types; half-open [from,to) validity |
| FORGET scoring | `scripts/wiki-forget-score.sh` + `wiki-forget-candidates.sh` | floor 0.15, cap 5/dream, min age 30d |
| PageRank code map | `mcp/src/tools/codemap/` (SHIPPED 0.33.33–0.33.35) | damping 0.85, 30 iters; `SB_CODEMAP_TOKEN_BUDGET=2000`; `auto_codemap` on |
| Injection model | `mcp/src/tools/sanitize.ts`, agent framing, bwrap jail | P6 plan = the unbuilt remainder |

---

## 1. BM25 field-weighted scoring + RRF fusion

**Theory.** BM25 ranks documents by term frequency saturated by `k1`, length-normalized by `b`,
weighted by inverse document frequency. Field weighting scores each document zone separately and
sums with per-field multipliers, so a title hit outranks the same hit buried in prose. Reciprocal
Rank Fusion (RRF) combines two rankers without score calibration: each ranker contributes
`1/(K + rank)` per document, so only rank ORDER matters — raw score magnitudes from incompatible
scales (BM25 points vs cosine similarity) never mix.

**Here.** `knowledgeSearch()` in `mcp/src/tools/knowledge-search.ts`:

- Fields and weights (`scoreBM25`, :412-419): title 3.0, description 2.0, tags 2.0, ai-block
  values 1.5 (the "proposition-level shared intermediate"), body 1.0 with the ai-block stripped
  first so block text is never double-counted.
- Constants (:102-110): `BM25_K1=1.2`, `BM25_B=0.75`, `TOP_K=8`, relevance floor
  `MIN_SCORE_RATIO=0.15` (of the top score), `STUB_PENALTY=0.5` for auto-extracted skeletons or
  pages with <100 chars of substantive body. Tokens = lowercase alphanumeric runs (:539-541);
  bare 2- or 4-digit tokens are dropped as date noise (:107, :543-545).
- Hybrid fusion (:264-297): when embeddings load, BM25 ranking and cosine ranking are fused with
  `RRF_K=60`; a document with zero BM25 score is pinned to 0 (:291-294) so pure-vector matches
  cannot resurrect text-irrelevant pages. When embeddings are unavailable the result carries
  `degraded: 'bm25-only'` (:392) — see §2.
- Result contract: `score` is raw engine scale (BM25 or RRF depending on mode); `score_norm`
  rank-normalizes to (0,1] against the returned set (:43-48, :372-378).

### The rank-scale subtlety — why a post-RRF multiplicative boost is a bug class

RRF scores are rank-derived and tiny: adjacent ranks differ by roughly `1/(K+r) − 1/(K+r+1)`.
At K=60 a ×1.3 multiplier on an RRF score can leapfrog ~19 ranks of two-engine consensus — a
"boost" that is a modest nudge on BM25's open-ended scale is a rank bulldozer on RRF's compressed
scale. Any multiplicative factor applied AFTER fusion silently changes meaning. This repo has been
burned by the multiplicative-boost family three times:

1. **R2 graph-boost compounding (~10,000×, fixed 0.24.39).** Graph/related boosts were computed
   from ALREADY-BOOSTED scores and compounded geometrically through hub pages — "~10,000x observed
   live" (`docs/plans/2026-06-10-r2-search-serving.md:69`); exact-title pages were evicted below
   the relevance floor. Fix: boosts read a FROZEN pre-boost `baseScore` (:171) and total received
   boost is capped at ≤1× the page's own base (:257-261); a zero-base page receives zero boost.
   The floor likewise compares frozen base scores in BM25-only mode (:353-359).
2. **P7 demote (0.33.22).** Even the capped boost, measured on the real wiki (96 pages / 170
   edges), was a wash: improved a gold page's rank in 6 cases, degraded it in 6, changed nothing
   in 80 of 92 (archive/docs:CHANGELOG.md `## 0.33.22`). It is now opt-in via `SB_GRAPH_RANKING_BOOST=1`,
   default OFF (:194-199), locked by `mcp/src/tools/retrieval-guards.test.ts:114-139`.
3. **P4b access-frequency boost cut (0.33.30).** The `1 + 0.1·min(count,10)` per-result multiplier
   was removed as the recsys "rich-get-richer" hub bias — the same corruption class (CHANGELOG.md:24;
   comment at knowledge-search.ts:83-85). Access counts survive ONLY as `acc=` telemetry (§7).

**Open residual (audit 2026-07-02, medium, OPEN):** the recency boost (:308-320,
`RECENCY_BOOST_MAX=0.3` over a 90-day linear decay) still multiplies AFTER RRF fusion — exactly
the rank-scale hazard above (~19-rank override). The stub penalty (:299-306) also applies
post-fusion. Neither has been re-derived on rank scale. If you touch this code, fix or measure —
do not add a fourth post-fusion multiplier. There is also no regression lock against
re-introducing count-into-ranking (audit medium, OPEN).

**Rule of thumb encoded by this history:** boosts must (a) read frozen pre-boost inputs, (b) be
capped relative to the page's own base, (c) never resurrect zero-relevance pages, and (d) be
measured on the real corpus before shipping — a plausible boost measured as a wash gets demoted.

---

## 2. ONNX embedding pipeline + graceful bm25-only degradation

**Theory.** Local sentence embeddings (mean-pooled, L2-normalized transformer output) give
semantic recall that lexical BM25 misses; cosine similarity of normalized vectors reduces to a dot
product. The heavy native runtime is optional, so retrieval must define exact behavior when the
model is absent — silent quality cliffs are the classic failure.

**Here.** `mcp/src/tools/embeddings.ts`:

- Model `Xenova/all-MiniLM-L6-v2`, `EMBEDDING_DIM=384`, fp32 (:5-7, :58). Loaded from
  `@huggingface/transformers`, which is deliberately EXTERNAL to every esbuild bundle (~490 MB
  vetted opt-in tier installed by `bin/install-vector-deps.sh`).
- **Degradation contract:** `getPipeline()` returns `null` when
  `SECOND_BRAIN_DISABLE_EMBEDDINGS=1` or the import/model load fails (:44-68); `embedTexts()` then
  returns `null`; `knowledgeSearch` catches and continues, tagging the result
  `degraded: 'bm25-only'` (knowledge-search.ts:55-56, :297, :392). Episodic search has the twin
  contract `degraded: 'text-only'`. A load FAILURE (vs explicit disable) is logged once per brain
  dir to `error-log.jsonl` with an actionable install hint (:60-67); an explicit disable writes
  only stderr (the old error-log path dropped ~500 noise rows per vitest run, :46-53).
- Embedding input is truncated to the first 512 chars of `title + description + body`
  (knowledge-search.ts:268). Vectors are cached per page path + content hash in
  `wiki/.embeddings-cache.json` (:78-91, :101-118). Audit mediums (OPEN): cache written
  non-atomically, never pruned; episodic vector-inference failure lacks a text fallback.
- CI runs entirely in degraded mode (`SECOND_BRAIN_DISABLE_EMBEDDINGS=1` + HF offline env) —
  the hybrid/RRF path is exercised only locally with the model installed; test ranking changes
  in both modes.

---

## 3. MinHash near-duplicate detection (the redundancy engine)

**Theory.** Jaccard similarity of word k-shingle sets measures near-duplication. MinHash
approximates it cheaply: for each of `n` hash functions keep the minimum hash over the shingle
set; the fraction of agreeing signature positions is an unbiased Jaccard estimate with standard
error ≤ `1/(2·sqrt(n))`. mem0 (arXiv 2504.19413) frames memory writes as ADD/UPDATE/NOOP decisions
against existing memory rather than blind appends.

**Here.** `mcp/src/tools/minhash.ts` — dependency-free and fully deterministic: word 3-shingles
(`SHINGLE_K=3`), 128 hash functions (`NUM_HASHES=128`, error ≤ ~0.044), universal-hash pairs
generated by a fixed-seed LCG (seed `0x9e3779b1`), integer-only `Math.imul` arithmetic — signatures
are byte-identical across OS and runs (:14-27, :58-68). `proseTokens` strips invisibles, ai-block,
frontmatter, generated theme/graph regions, and `[[link]]` markup first, so shared STRUCTURE cannot
fake similarity, and the "what counts as prose" definition is shared with the FORGET scorer via the
same primitives (:29-39). All-sentinel (prose-empty) signatures are excluded — two distinct stubs
would otherwise collide at sim 1.0 (:85-94). Pair detection is O(n²) all-pairs, documented as fine
for a hundreds-of-pages wiki with LSH banding named as the scale path (:96-101).

Three consumers, three thresholds (deliberately staggered — write-path strictest):

| Consumer | Threshold (env, default) | Semantics |
|---|---|---|
| Capture write-path | `SB_CAPTURE_DEDUP_THRESHOLD` = **0.9** | `captureItem` (mcp/src/tools/raw-inbox.ts:283-330): exact-hash dedup first, then MinHash vs UNPROCESSED text items only (never the wiki). New body longer → **UPDATE** in place, preserving the existing item's id + ALL provenance; else **NOOP** (drop the new capture). The mem0 ADD/UPDATE/NOOP borrow promoted to write time (0.33.29) — collapses Stop+PreCompact double-captures. Kill: `SB_CAPTURE_DEDUP=off`. |
| Dream DEDUPLICATE | `SB_REDUNDANCY_THRESHOLD` = **0.7** | Phase 2 of the dream (agents/dream-runner.md:69-82) runs `scripts/wiki-redundancy.sh` over STAGING; each pair is a **merge candidate, not an order** — "the signal proposes, you decide"; never auto-delete. Shim is fail-safe: node/bundle missing or `SB_REDUNDANCY=off` → `[]`, exit 0 (wiki-redundancy.sh:22-28). |
| FORGET cross-check | `SB_FORGET_REDUNDANCY_THRESHOLD` = **0.8** | `wiki-forget-candidates.sh:26-53`: a page is archived only when the recall-probe AND a genuine MinHash near-dup twin agree (0.33.27). Stops false-forgetting distinct same-TOPIC pages ("indexing basics" vs "advanced indexing" share tags → probe sees coverage, but they are not dups). Keeps ≥1 page per near-dup cluster (:72). Engine unavailable → announced stderr fallback to probe-only, never a silent no-op (:46). |

Known audit gap (medium, OPEN): the FORGET gate's availability check conflates "engine available"
with "engine succeeded" (the shim's error path also emits `[]`).

---

## 4. Deterministic label-propagation clustering + the generated-page exclusion

**Theory.** Label propagation detects communities by iteratively adopting the plurality label of
one's neighbors. It is near-linear and incremental-friendly (Graphiti chose it over Leiden for
that reason) but NON-deterministic in textbook form (random visit order, random tie-breaks) and
oscillates on bipartite structure. An LLM pipeline consuming clusters needs identical output every
run, or idempotence checks downstream are meaningless.

**Here.** `mcp/src/tools/graph-cluster.ts` (:1-14 narrates the determinism recipe): synchronous
rounds (next labels computed from the previous round only), nodes iterated in lexicographic slug
order, tie-break = keep own label if among the tied plurality (also kills 2-cycle oscillation)
else smallest slug, fixed `maxIter=20` cutoff, community id = lexicographically-smallest member
slug. `memberHash` = djb2 over sorted members + per-member content hashes (:142-146), so an
unchanged cluster is provably unchanged — the idempotence key for SUMMARIZE and REFLECT.

The CLI (`mcp/src/tools/graph-cluster-cli.ts`) builds the graph from staging pages' `related:` +
body `[[links]]` (never live `graph/edges.jsonl`), keeps clusters ≥ `SB_SUMMARIZE_MIN_CLUSTER`
(default 4), caps at `SB_SUMMARIZE_MAX_PAGES` (default 8, largest-first, :81-89). Invoked via the
`scripts/graph-cluster.sh` shim, which machine-enforces the kill switches: `--gate reflect` honors
`SB_DREAM_REFLECT=off`, default gate honors `SB_DREAM_SUMMARIZE=off`, each independently returning
`[]` (graph-cluster.sh:23-26) — the skip does not depend on LLM compliance.

### The REFLECT feedback-loop incident (the worked warning)

Generator output fed back into generator input breaks idempotence. REFLECT (0.33.28) writes
`reflection-<id>` pages INTO content categories (learnings/concepts). The CLI's walk excluded only
the `projects/` and `themes/` DIRS (:31) — so on the NEXT dream a reflection page joined its own
cluster: `member_hash` changed every run (the LLM re-reflected every dream), and when
`reflection-<id>` sorted lexicographically first it BECAME the cluster id, spawning
`reflection-reflection-<id>` / `theme-reflection-<id>` growth each run. Fixed as of 0.33.31:
pages with `generated: true` frontmatter are excluded from clustering INPUT
(graph-cluster-cli.ts:69-76 — the comment narrates the loop), regression-locked in
`tests/test-graph-cluster-shim.sh` ("drop the generated:true filter … and members gain
'reflection-a'"). General rule: any self-referential memory op needs explicit input/output
separation, same family as the R2 frozen-base fix (§1) and the autofix↔regenerate churn loop.

---

## 5. Reflection (the Generative Agents borrow)

**Theory.** Generative Agents (arXiv 2304.03442) showed via ablation that synthesizing
higher-level insights from clusters of related memories — reflection — measurably improves agent
behavior; the one memory op in this design with peer-reviewed ablation support. The paper triggers
reflection via an importance accumulator (~150), which presumes a continuous agent loop.

**Here.** Dream Phase 5b (agents/dream-runner.md:144-176), shipped 0.33.28. Deviations from the
paper, each deliberate:

- **Cadence:** per-dream, NOT the importance accumulator ("assumes a continuous agent loop we
  don't have" — archive/docs:CHANGELOG.md:60-62). Idempotence via `member_hash`: an unchanged cluster is never
  re-reflected (checked in BOTH `learnings/` and `concepts/`).
- **Eligibility before writing:** reflect only when ≥ half the cluster members are actionable
  (learnings/issues/decisions) AND a genuine cross-cutting practice emerges; else write NOTHING.
  SUMMARIZE indexes ("these pages are about X"); REFLECT synthesizes the practice ("the rule these
  learnings add up to").
- **Grounding-citation requirement:** the body ends with `Grounded in: [[member-a]], [[member-b]]`
  and `related:` lists every member — a synthesized rule stays traceable and can be retired if
  later contradicted. Frontmatter carries `generated: true`, `reflection: true`, `member_hash`.
- Pages land in EXISTING categories (`learnings/reflection-<id>.md` or
  `concepts/reflection-<id>.md`) — never a new `reflections/` dir (P4 collapses categories, not
  adds). Authoring is confined to the `<!-- reflect:begin -->…<!-- reflect:end -->` region; the
  ai-block is NOT authored here (single-path rule — the live knowledge-maintainer backfills it).
- Kill switch `SB_DREAM_REFLECT=off` is machine-enforced by the shim (§4), not prose.

---

## 6. PageRank code map (P3a) — SHIPPED 0.33.33–0.33.35

**Status: shipped** (verified 2026-07-13 at 0.33.37): the `mcp/src/tools/codemap/` module family
(scan-sources, extract, pagerank, build-graph, serialize, store, drift + `code-map-cli`), two
read-only MCP tools `code_map`/`code_neighbors` in `mcp/src/server.ts`, autonomous out-of-band
regeneration in the drainer (`scripts/extract-drain.sh`, config key `auto_codemap`, default on —
0.33.34), and SessionStart spine injection (`session-load.sh` §0d, kill switch
`SB_CODEMAP_ORIENT` — 0.33.35, placed BEFORE the forced USER.md/PROJECT.md sections after live
verification caught it being budget-starved when placed last). Shaping plan:
`archive/docs:docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md`. Remaining P3a: Phase 4
(layer-5 code↔wiki edges), Phase 5 (opt-in WASM tree-sitter tier).

**Theory.** PageRank ranks graph nodes by stationary visit probability of a random surfer with
damping; on a file-import graph it surfaces the files everything depends on — Aider's repo-map
uses exactly this to pick which files/symbols fit a token budget.

**As built:** deterministic PageRank — damping 0.85, fixed 30 iterations OR L1-convergence
epsilon 1e-6, sorted accumulation order (never Map insertion order — a tested contract,
`pagerank.ts`); pure-JS/regex Tier-0 extractor for ts/js/py (node-gyp native tree-sitter
REJECTED; WASM deferred to Phase 5); token-capped `map.md` under `SB_CODEMAP_TOKEN_BUDGET`
(default 2000; chars/4 estimate, budget×0.95 stop, never-exceed tested at the boundary); stored
per-project under `BRAIN_DIR/projects/<slug>/codemap/`, deliberately NOT in the wiki graph
(separate store, separate tools — `knowledge_neighbors` untouched). Drift (`drift.ts`, one
predicate shared by CLI and both tools): stored `git_rev` ≠ HEAD, nogit-mtime fallback,
dirty-tree always re-checks; query-time answers carry an honest `stale` flag. Incident worth
keeping: the first cut ingested COMMITTED build artifacts — 17 tracked `mcp/dist` bundles ate
42% of the map budget until the ignore-dirs list applied to BOTH enumeration paths (0.33.33
adversarial review, empirically proven on this repo).

---

## 7. Bi-temporal edge store (the Graphiti borrow) — history is never deleted

**Theory.** Zep/Graphiti (arXiv 2501.13956): knowledge changes, and LLMs are bad at suppressing
superseded facts they can still see. A bi-temporal store separates WHEN a fact was true
(`valid_from`/`valid_to`) from WHEN it was recorded (`recorded_at`), and never deletes: an edge is
INVALIDATED (interval closed), so both "what is true now" and "what was true then" stay queryable,
and `supersedes` edges make replacement explicit. The repo calls this "the graph's real
justification".

**Here.** `mcp/src/tools/graph-store.ts`:

- Source of truth = append-only `$KNOWLEDGE_DIR/graph/edges.jsonl`; one JSON record per line with
  `op: assert|invalidate`, `from`, `to`, `type` ∈ {requires, affects, relates, part_of,
  supersedes}, optional `valid_from`/`valid_to`, `recorded_at` (:4-20).
- `foldToCurrent` (:90-117) replays records in `recorded_at` order keyed by (from,type,to): an
  assert ONLY opens an interval (a stray `valid_to` on an assert is ignored — closing is
  exclusively invalidate's job); invalidate closes; a later assert re-opens fresh. `validAt`
  (:119-133) is half-open [from, to) at date granularity — an edge invalidated on day D is not
  valid at D.
- Torn-line tolerance: `loadEdges` skips unparseable/invalid lines, never fatal (:63-79); appends
  are single O_APPEND writes, so the concurrent-writer failure mode is a dropped edge, never a
  crash (:193-204).
- Bash twin: `scripts/merge-edges.sh` appends extractor-proposed `op:assert` lines with endpoint
  + type validation; unresolvable endpoints go to `graph/edges-quarantine.jsonl`, conflicts to
  `graph/conflicts.jsonl` (:2-27). The JSONL line format is the shared bash↔TS contract.
- `neighbors` (:157-191) is the blast-radius BFS behind `knowledge_neighbors` (`direction:'in'` =
  what breaks), with per-hop decay 0.3 and type weights requires/affects 1.0, part_of 0.8,
  supersedes 0.6, relates 0.5, and point-in-time reconstruction via `as_of`.

**Why never deleted, mechanically:** dreams snapshot `wiki/` ONLY — `graph/edges.jsonl` is
deliberately NOT snapshotted, because an append-only log cannot be merged back after live sessions
appended during the dream; the dream writes nothing to `graph/` (dream-runner.md:84-100). Edge
curation is owned by live paths (capture extraction, `knowledge_relate`, knowledge-maintainer).
Retirement everywhere in this repo mirrors this pattern (soft `valid_to`, reversible) — the P2
plan reuses it for learned guardrail retirement.

**Scope after P7:** the graph survives as `knowledge_neighbors` + bi-temporal `supersedes`
metadata + the project-scoping neighbourhood; its search-RANKING boost is demoted to opt-in-off
(§1). GraphRAG-Bench (arXiv 2506.05690) skepticism — graphs frequently underperform plain RAG at
small corpus scale except for genuine multi-hop — was confirmed empirically here.

---

## 8. Forgetting — structural importance only, redundancy-gated, reversible

**Theory.** Naive forgetting decays by recency (Ebbinghaus-flavored) or evicts by low usage
frequency. Both are rejected here: goal-agnostic recency decay demonstrably hurts (spec cites
arXiv 2511.21726), and usage frequency is the recsys rich-get-richer hub bias — the same signal
family behind the ~10,000× ranking corruption (§1). The safe formulation is a CONJUNCTION: evict
only what is BOTH structurally unimportant AND redundantly covered, reversibly.

**Here.**

- **Score** (`scripts/wiki-forget-score.sh`): structural importance only — connectivity (inbound
  `[[links]]`, weight `SB_FORGET_W_CONNECTIVITY=0.25`, saturating at 3 links) + category weight
  (`SB_FORGET_W_CATEGORY=0.20`; protected categories learnings/decisions/concepts/security/themes/
  projects score 1.0, discounted entities/sources/issues 0.5, else 0.2) + a stub floor for
  <200-byte prose bodies (ai-block stripped first so a uniform block can't lift stubs). Lower =
  more forgettable.
- **What was deliberately CUT (0.33.25):** the access-count term (was weight 0.30) and the recency
  term (was 0.25). Access counts are read but emitted ONLY as `acc=` telemetry in the reasons
  column (:60-64); recency survives ONLY as (a) the `PROTECT:age` <30-day hard floor
  (`SB_FORGET_MIN_AGE_DAYS`) and (b) the age-DESC tie-break in the final sort — "recency may break
  ties, never drive eviction" (:2-16, :86-88). The old `SB_FORGET_W_ACCESS`/`_W_RECENCY` knobs are
  inert. Weights kept at 0.25/0.20 so the eviction boundary is unchanged for the pages FORGET
  actually targets (old unaccessed orphans had both cut terms at 0); the behavioral change is
  precisely that a frequently-read low-importance orphan is no longer rescued. Enshrined in
  CONSTITUTION.md:42-45 ("NOT raw usage frequency — that is the rich-get-richer hub-bias
  footgun").
- **Candidates** (`scripts/wiki-forget-candidates.sh`): score < `SB_FORGET_FLOOR` (0.15),
  unprotected (no PROTECT:category/age/linked flag), capped at `SB_FORGET_MAX_PER_DREAM` (5), then
  TWO orthogonal gates: a live recall-probe (remove the page from a corpus copy; a sibling must
  still answer its topic query at ≥ `SB_FORGET_PROBE_MIN_SCORE` 0.1) AND the MinHash near-dup
  cross-check at 0.8 with keep-one-per-cluster (§3). Recall guard can't run → exit 2 → the dream
  skips the FORGET phase entirely (fail-safe). Net contract: **a unique page can never be
  evicted, regardless of score.**
- **Reversibility:** the dream only writes `forget-manifest.tsv`; archiving happens at accept time
  as a MOVE into `$BRAIN_DIR/wiki-archive/` + a JSONL event log; `scripts/wiki-restore.sh`
  reverses it; `wiki_archive_ttl_days: 0` default = archived pages are never auto-deleted;
  `auto_accept=safe` refuses FORGET dreams outright.
- Known audit mediums (OPEN): FORGET archiving exists only as dream-skill prose (a direct MCP
  `dream_accept` or `auto_accept=all` silently drops the archive step); no retirement path yet for
  stale `theme-*`/`reflection-*` pages.

---

## 9. Prompt-injection / lethal-trifecta model for consolidation

**Theory.** Willison's lethal trifecta: an agent holding (1) untrusted input, (2) access to
private data / write capability, and (3) a network/exfiltration channel is exploitable regardless
of prompt quality — injection DETECTORS hit ≤100% evasion, so "99% is a failing grade in appsec".
CaMeL (arXiv 2503.18813) breaks the trifecta by construction: a quarantined LLM reads untrusted
content and emits only structured data; a privileged component with real capabilities never sees
raw untrusted text. A consolidating memory system is a delayed-trigger poisoning substrate: text
read today is distilled into pages auto-injected into every future session.

**Constitutional constraint** (CONSTITUTION.md:46-52): consolidation treats ingested content as
DATA to summarize, never instructions; the privileged writer consumes only structured,
provenance-tagged output, never raw transcript; the injection scanner is telemetry, NOT a trust
boundary.

**Which legs are cut TODAY (as of 0.33.31) — and which are not:**

| Leg | Today's mitigation | Status |
|---|---|---|
| Untrusted input | `stripInvisible` (`mcp/src/tools/sanitize.ts`) removes the Unicode Tags block U+E0000–E007F + ZWSP/word-joiner/BOM at raw-inbox write+read, transcript→dream staging, episodic read (P6a/b, 0.33.20/21). Bidi (Trojan-Source) + variation-selector channels explicitly deferred (sanitize.ts:11-13). "Untrusted input — DATA, not instructions" framing in all three consolidation agents (dream-runner.md:23-29), machine-locked by `mcp/src/agent-grants.test.ts` (literal-string assertion + least-privilege grant checks). | PARTIAL — sanitization narrows channels; framing is advisory by definition |
| Write capability | Dreams write STAGING only; live apply requires `dream_accept` behind five independent guards; the unattended maintainer (`scripts/maintain-llm-drain.sh`) runs the headless LLM inside bubblewrap with ONLY the dream dir writable — "enforced by the KERNEL, not a prompt" (:1-20) — and leaves the dream completed-UNACCEPTED. Nested headless spawns refuse all 11 destructive MCP write tools (`SB_NESTED_SPAWN=1`, 0.32.0). | LARGELY CUT on the unattended Linux path; bwrap-less OSes simply never run it |
| Network / exfil | NOT cut: the headless run is a `claude -p` with network up and the OAuth credential ro-bound — "token readable + network up ⇒ exfil possible in ANY OAuth-headless run" (documented residual since 0.24.26; re-flagged OPEN by the 2026-07-02 audit). | OPEN |

**The P6-quarantine plan (PLAN-QUEUED, zero code —
`archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md`)** is the CaMeL install: Stage A =
quarantined summarizer (`claude -p`, network up, transcripts read-only, emits only
`candidate-facts.jsonl` with `provenance.trust:"untrusted"`); Stage B = privileged writer as a
DETERMINISTIC Node CLI under bwrap `--unshare-net` with transcripts NOT mounted at all — the only
design where the write stage is genuinely netless, since both stages cannot be LLMs AND have the
writer severed (plan :39-54, :81-95). Accepted cost: LLM-heavy merge/theme/reflect prose authoring
defers to attended `/second-brain:maintain` on the unattended path (the budgeted ~7-pt CaMeL
utility cost). Two fenced wrong paths to respect when working near this: a blanket `--unshare-net`
on the whole pipeline breaks the API-dependent summarizer; and the prompt-level "DATA, not
instructions" framing is defense-in-depth, NOT the boundary — the kernel jail is; never relax the
jail because the prompt "already says it".

**Scanner status:** `scripts/tool-return-scanner.sh` (PostToolUse) flags suspected injection via
additionalContext and never blocks — telemetry only, per the constitution; P6 T7 rewords its docs
to say so explicitly.

---

## 10. Borrow ledger — every imported idea, its source, and the verdict here

| Borrow | Source | Verdict here | Landing site |
|---|---|---|---|
| ADD/UPDATE/NOOP salience write path | mem0 (2504.19413) | ADOPTED (capture write-path 0.33.29; re-planned as the P6 writer's op field; maintainer "Mem0-style" reconciliation) | raw-inbox.ts:283-330; agents/knowledge-maintainer.md:74 |
| Reflection op | Generative Agents (2304.03442) | ADOPTED; importance-accumulator cadence REJECTED (per-dream + member_hash instead) | dream-runner.md:144-176 |
| MinHash near-dup (LSH family) | standard technique | ADOPTED, deterministic + dependency-free | minhash.ts; §3 consumers |
| Bi-temporal invalidate-don't-delete, `supersedes` | Zep/Graphiti (2501.13956) | ADOPTED; kept through the P7 demote; pattern reused for P2 rule retirement | graph-store.ts; merge-edges.sh |
| Label propagation over Leiden | Graphiti's choice | ADOPTED, made fully deterministic | graph-cluster.ts:1-14 |
| GraphRAG skepticism | GraphRAG-Bench (2506.05690) | ADOPTED as P7 justify-or-demote; measured 6/6/80 wash → ranking boost off by default | CHANGELOG `## 0.33.22`; retrieval-guards.test.ts:114-139 |
| CaMeL quarantine / dual-LLM | 2503.18813 + Willison trifecta | ACCEPTED, PLAN-QUEUED (P6 remainder); deterministic-writer variant chosen over two LLMs | P6 plan §Architecture |
| Incremental > threshold capture | ARC (2601.12030; 31% vs 24–27% ablation) | ADOPTED (Stop-hook incremental + PreCompact safety net, 0.33.18) | spec §3; stop-extract.sh |
| Sleep-time consolidation | Letta/MemGPT sleep-time agents | VALIDATED-KEEP (dream = background consolidation; in-band "remember-to-remember" tool calls rejected as the field's dominant failure mode) | dream pipeline |
| Repo-map = tree-sitter + PageRank | Aider | ADOPTED-with-modification, SHIPPED 0.33.33–0.33.35 (P3a): PageRank yes; tree-sitter demoted to opt-in WASM (deferred), pure-JS regex default | mcp/src/tools/codemap/; §6 |
| Cross-encoder reranker | Anthropic contextual-retrieval + field nDCG results | ACCEPTED in spec (P3b), NOT STARTED — no plan doc, no code | spec §6 P3 |
| Usage-frequency ranking/forgetting | recsys frequency boosting | REJECTED twice (P4b search cut 0.33.30; FORGET terms cut 0.33.25); constitutionally enshrined | §1 incident C; §8 |
| Ebbinghaus/recency decay as eviction driver | classic forgetting curves | REJECTED as a score input ("goal-agnostic decay demonstrably hurts", spec citing 2511.21726); kept only as age-floor + tie-break | §8 |

---

## When NOT to use this skill

- Wiring, hook tables, data geography, resolver discipline → **sb-architecture-contract**.
- "Is this novel vs mem0/Letta/Zep?" positioning claims → **sb-external-positioning**.
- A live search/dream/forget failure to triage → **sb-debugging-playbook**; the full incident
  narratives behind §1/§4 → **sb-failure-archaeology**.
- Adding a flag or changing a default → **sb-config-and-flags** (add-a-flag checklist).
- Designing the P6 campaign itself → **sb-autonomous-consolidation-campaign**.

## Provenance and maintenance

Derived from the working tree at 0.33.31 (uncommitted release batch on top of commit `6fba312` =
0.33.30), authored 2026-07-05. Every mechanism section was verified by reading the cited source
files in full; incident facts cross-checked against `archive/docs:CHANGELOG.md`, `CONSTITUTION.md`,
`docs/plans/2026-06-10-r2-search-serving.md`, and the plan docs under `archive/docs:docs/superpowers/plans/`.
Open-residual claims come from the 2026-07-02 deep audit (88 confirmed findings) — re-verify in
code before relying on them.

Re-verification one-liners (run from repo root, git-bash/Linux/macOS):

```bash
# BM25 weights + RRF constant + floor still as documented
grep -nE 'weight: [0-9.]+|RRF_K =|MIN_SCORE_RATIO' mcp/src/tools/knowledge-search.ts
# Graph ranking boost still default-off (P7)
grep -n 'SB_GRAPH_RANKING_BOOST' mcp/src/tools/knowledge-search.ts mcp/src/tools/retrieval-guards.test.ts
# Recency-after-RRF residual still present? (open audit medium)
grep -n 'RECENCY_BOOST_MAX' mcp/src/tools/knowledge-search.ts
# Degradation contracts
grep -rn "degraded" mcp/src/tools/knowledge-search.ts mcp/src/tools/episodic-search.ts | grep -E 'bm25-only|text-only'
# MinHash parameters + the three thresholds
grep -nE 'SHINGLE_K|NUM_HASHES' mcp/src/tools/minhash.ts; grep -rn 'SB_CAPTURE_DEDUP_THRESHOLD\|SB_REDUNDANCY_THRESHOLD\|SB_FORGET_REDUNDANCY_THRESHOLD' mcp/src scripts | grep -v test
# Generated-page clustering exclusion (REFLECT loop fix) + its regression lock
grep -n 'generated:' mcp/src/tools/graph-cluster-cli.ts; bash tests/test-graph-cluster-shim.sh
# FORGET score inputs (should show connectivity+category only; acc= telemetry)
grep -nE 'W_CONNECTIVITY|W_CATEGORY|acc=' scripts/wiki-forget-score.sh
# Bi-temporal fold semantics unchanged
grep -nE 'assert|invalidate|valid_to' mcp/src/tools/graph-store.ts | head -20
# PageRank code map still shipped? (expect: codemap module files + pagerank hits)
ls mcp/src/tools/codemap 2>/dev/null; grep -rln 'pagerank' mcp/src/ || echo "codemap MISSING — §6 is stale"
# P6 quarantine still unbuilt? (no candidate-facts/consolidate-writer sources = plan-only)
ls mcp/src/tools/candidate-facts.ts mcp/dist/tools/consolidate-writer-cli.bundle.js 2>/dev/null || echo "P6 still plan-only"
# Agent injection-framing + grant locks still enforced
cd mcp && npx vitest run src/agent-grants.test.ts
# Current version stamp for re-dating this skill
jq -r .version .claude-plugin/plugin.json
```

Volatile facts to re-stamp on next edit: env-knob defaults (grep the named var) and the
OPEN/PLANNED statuses of the recency-after-RRF residual, P3b, and P6 (check CHANGELOG
headings newer than 0.33.31 first). P3a shipped 0.33.33–0.33.35 (§6 re-verified 2026-07-13
at 0.33.37); the 6/6/80 P7 measurement is a frozen historical fact.
