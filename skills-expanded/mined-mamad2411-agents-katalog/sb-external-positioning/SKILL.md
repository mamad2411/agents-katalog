---
name: sb-external-positioning
description: >-
  Loads the second-brain plugin's external positioning: what is novel vs borrowed vs rejected
  relative to the memory-agent ecosystem (mem0, Letta/MemGPT, Zep/Graphiti, GraphRAG,
  Generative Agents, LongMemEval), which novelty claims are currently defendable vs not, and
  the claim discipline (what must be measured before a claim ships in a README, blog post,
  paper, talk, or marketplace listing). Load when: writing or reviewing any external-facing
  text about this project; answering "is this novel?", "what's the related work?", "how does
  this compare to mem0/Letta/Zep/GraphRAG?"; deciding whether a benchmark or capability claim
  is safe to publish; or when an old note mentions "graphify" (a phantom term — resolved
  here). Do NOT load for: how the memory mechanisms work internally (use
  sb-memory-systems-reference), open research problems and next steps (use
  sb-research-frontier), the internal evidence bar for accepting a result (use
  sb-research-methodology), or eval/test mechanics (use sb-validation-and-qa).
---

# sb-external-positioning — novel vs known, and how to claim it

This skill is the single home for two things:

1. **The comparison map** — for each major ecosystem system: what it is, what this project
   borrowed (with the verdict and landing site in this repo), and where this project differs.
2. **The claims ledger + claim discipline** — which novelty claims are defendable *today*,
   which are not yet, and what must be measured before any claim goes external.

Repo: the second-brain Claude Code plugin at this repository root. Design source of record:
`CONSTITUTION.md` + `archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md`
(called "the spec" below; its section numbers are cited as §N).

Terms used once here (owning skill in parentheses):
- **dream** — background wiki consolidation staged in `~/.second-brain/dreams/` and applied via
  a guarded accept (mechanics: sb-run-and-operate; theory: sb-memory-systems-reference).
- **FORGET** — the reversible archive-not-delete eviction phase of a dream
  (sb-memory-systems-reference).
- **PreToolUse guard** — a deterministic bash hook that can ask/deny/rewrite a tool call before
  it runs (sb-architecture-contract).
- **P0–P8** — the spec's workstreams; statuses live in sb-research-frontier. Only
  positioning-relevant statuses are repeated here, date-stamped.

---

## 1. The ecosystem comparison map

Field-position summary (project direction, stated in the maintainer-accepted context): SOTA
agent memory (mem0, Letta/MemGPT, ChatGPT memory) is predominantly *passive recall bolted onto
chat*. This project's bet is memory that (a) ACTS at tool-time, (b) orients before recall,
(c) consolidates autonomously with safety-by-construction, (d) is bi-temporal, (e) is
evaluated not vibed, and (f) lives in the harness (local files + hooks), so it is
model-agnostic and survives model swaps.

External-system descriptions below are as characterized in the spec's adversarially-verified
research streams (spec §11) plus general knowledge; arXiv IDs are given so a reader can check
the primary source. Repo-side landing sites are verified against the working tree.

| System (paper) | Verdict here | Landing site / evidence |
|---|---|---|
| mem0 (2504.19413) | ADOPTED (partially, deliberately narrowed) | `mcp/src/tools/raw-inbox.ts:283-330`; CHANGELOG 0.33.29 |
| Letta / MemGPT (2310.08560) | ADOPTED the reliable half (background consolidation, paging boundary) | spec §3; `hooks/hooks.json` PreCompact → `scripts/pre-compact.sh` (07bb5de); CHANGELOG 0.33.18 (Stop-capture/drainer half) |
| Zep / Graphiti (2501.13956) | ADOPTED (bi-temporal validity model) | `mcp/src/tools/graph-store.ts`; `scripts/merge-edges.sh` |
| GraphRAG / GraphRAG-Bench (2506.05690) | ADOPTED THE SKEPTICISM (measure, then demote) | CHANGELOG 0.33.22; `mcp/src/tools/retrieval-guards.test.ts:114-139` |
| Generative Agents (2304.03442) | ADOPTED reflection, REJECTED its cadence | `agents/dream-runner.md:144-176`; CHANGELOG 0.33.28 |
| LongMemEval (2410.10813) | ACCEPTED as the eval bar; suite NOT built yet | spec §6 P8; `tests/test-knowledge-eval.sh` (smaller regression gate) |
| ARC incremental capture (2601.12030, preprint) | ADOPTED (per-turn capture > threshold-triggered) | spec §3; CHANGELOG 0.33.18 |
| CaMeL dual-LLM (2503.18813) | ACCEPTED, PLAN-QUEUED (P6 remainder) | `archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md` |
| Aider repo-map (tree-sitter + PageRank) | ACCEPTED with modification; P3a Phases 1-3 SHIPPED (PageRank code-map live), Phases 4-5 (code↔wiki edges, tree-sitter tier) still queued | `mcp/src/tools/codemap/`; `archive/docs:docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md` |
| Cross-encoder reranker (Anthropic contextual retrieval) | ACCEPTED in spec (P3b), NOT STARTED — no plan, no code | spec §6 P3; `grep -ril rerank mcp/src scripts` is empty |
| MinHash near-dup LSH (standard technique; no single paper) | ADOPTED as the P4 redundancy engine | `mcp/src/tools/minhash.ts`; `scripts/wiki-redundancy.sh`; CHANGELOG 0.33.26 |
| Path-test discipline (vercel-labs/skills, designer-skills deep-scan) | ADOPTED (traversal-vector matrix, 0.33.23) | `mcp/src/path-guard.test.ts`; CHANGELOG 0.33.23 |
| Usage-frequency ranking/forgetting (recsys) | REJECTED twice, constitution-enshrined | CHANGELOG 0.33.25, 0.33.30; `CONSTITUTION.md:42-45` |
| Rewrite / migrate-to-hermes | REJECTED (evolve-over-rewrite) | spec §0 and §9 ("relocates accretion; forfeits cross-platform fixes") |

### 1.1 mem0 — ADD/UPDATE/NOOP salience write path

**What it is:** a memory layer that LLM-extracts salient facts from conversations and resolves
each new fact against existing memories with ADD / UPDATE / DELETE / NOOP operations over a
vector store; shipped as a hosted platform + OSS library.

**Borrowed (verdict: ADOPTED, narrowed):** the op-resolution idea, applied at *capture time*
without an LLM. As of 0.33.29, `captureItem` collapses a MinHash near-duplicate
(sim ≥ `SB_CAPTURE_DEDUP_THRESHOLD`, default 0.9) of an existing UNPROCESSED raw-inbox item
into one item — keep the longer body (UPDATE) or drop the new one (NOOP). Kill switch
`SB_CAPTURE_DEDUP=off`. Scoped to the not-yet-drained inbox only, never the wiki
(`mcp/src/tools/raw-inbox.ts:289-330`). The P6 plan re-uses `op: add|update|noop` as the
candidate-fact field its deterministic writer resolves via local BM25.

**Where this project differs:**
- **No DELETE at the write path.** mem0's op set includes DELETE; here deletion is deliberately
  routed to the separate, reversible FORGET pipeline (archive + restore, never hard-delete).
- **Deterministic resolution.** Capture-time dedup is MinHash (fixed seeds, byte-identical
  across OSes), not an LLM judgment — auditable and free.
- **Local-first files, no vector-DB service.** Storage is markdown + JSONL under `$HOME`.

### 1.2 Letta / MemGPT — paging and self-editing memory

**What it is:** MemGPT introduced virtual-context management — the model pages memory in/out of
context and self-edits its memory via in-band tool calls; Letta continues it as an agent
framework, including "sleep-time agents" that process memory in the background.

**Borrowed (verdict: ADOPTED the reliable half):**
- The paging boundary: PreCompact capture = summarize-before-evict at the compaction boundary
  (spec §3: "PreCompact = safety-net (summarize-before-evict, MemGPT paging boundary)").
- Sleep-time/background consolidation: the dream is exactly out-of-band consolidation on a
  timer, dispatched outside the interactive session.

**Where this project differs:** memory maintenance is *harness-level, not model-level*. The
model is never required to remember to call a memory tool mid-task (the field's dominant
failure mode for self-editing memory); capture is hook-driven (Stop/PreCompact fire
regardless), consolidation is timer-driven, and injection is deterministic bash. Memory lives
in plain local files, so personalization survives model swaps and works with any model the
harness runs — see CONSTITUTION.md's mission framing. Positioning sentence you may use:
"capture and consolidation are guaranteed by hooks, not by the model's discipline."

### 1.3 Zep / Graphiti — bi-temporal knowledge graph

**What it is:** Zep is an agent-memory service; Graphiti is its temporal knowledge-graph
engine (paper 2501.13956). Its signature idea is bi-temporality: facts carry both event
validity time and ingestion time, and new facts *invalidate* old ones instead of overwriting.

**Borrowed (verdict: ADOPTED — named in the borrow record as "the graph's real justification…
the fix for 'LLMs can't suppress superseded facts'"):** the validity model, implemented
dependency-free in `mcp/src/tools/graph-store.ts` — an append-only `edges.jsonl` with
`assert`/`invalidate` ops, `valid_from`/`valid_to` intervals plus `recorded_at` (genuinely
bi-temporal), folded to current state; edge type `supersedes` is first-class
(`EDGE_TYPES = ['requires','affects','relates','part_of','supersedes']`, graph-store.ts:5-6).
The pattern is re-used for P2 rule retirement and P3a code-link staleness (both plan-queued).
The `supersedes`/neighbors machinery was explicitly KEPT through the P7 ranking demote
(spec §6 P7: "Keep bi-temporal `supersedes` regardless").

**Where this project differs:** no graph database, no service — a JSONL log folded on read;
and after P7 (below) the graph is *metadata + blast-radius only*, not a retrieval tier.

**Phantom-term note:** the term "graphify" appears in ZERO repo files (verified
`grep -ri graphify` → no matches, 2026-07-05). If you meet it in old notes or transcripts,
the referent is the Zep/Graphiti bi-temporal borrow above. Do not propagate the term.

### 1.4 GraphRAG — the skepticism this project operationalized

**What it is:** Microsoft GraphRAG builds an LLM-extracted entity graph + community summaries
to answer corpus-level questions. GraphRAG-Bench (2506.05690) found graphs "frequently
underperform plain RAG" below ~100K docs except for genuine multi-hop questions (spec §6 P7).

**What this project did with it (verdict: ADOPTED THE SKEPTICISM — P7 "justify-or-demote"):**
this is the project's flagship *measure-before-believing* story. Chronology, with the number
discipline that external text MUST preserve:

1. **The corruption (fixed 0.24.39):** graph/related ranking boosts computed from
   already-boosted scores compounded geometrically through hub pages — "~10,000x observed
   live" (`docs/plans/2026-06-10-r2-search-serving.md:69` and `:208`) — evicting exact-title
   pages below the relevance floor. Fix: boosts from a frozen pre-boost snapshot, capped at
   ≤1× base.
2. **The measurement (0.33.22):** the *surviving, capped* boost was measured over the real
   wiki (96 pages / 170 edges): it improved a gold page's rank in 6 cases, degraded it in 6,
   changed nothing in 80 of 92 — a wash — and provably cannot improve recall (zero-base pages
   get zero boost). CHANGELOG 0.33.22.
3. **The demote (0.33.22):** graph ranking boost is now opt-in via `SB_GRAPH_RANKING_BOOST=1`,
   default OFF, locked by a behavioral test (`mcp/src/tools/retrieval-guards.test.ts:114-139`).
   `knowledge_neighbors` blast-radius and bi-temporal `supersedes` are unchanged.

**Precision rule:** the literal ~10,000× figure belongs to the 0.24.39 *compounding-boost
incident*, NOT to the 0.33.22 demote measurement (which showed a wash) and NOT to the
access-frequency boost (capped at 2×, cut in 0.33.30 as the same rich-get-richer *class*).
Conflating these in external text is a claim-discipline defect. Full incident detail:
sb-failure-archaeology.

### 1.5 Generative Agents — reflection, grounded

**What it is:** Park et al. (2304.03442) — agents with a memory stream, retrieval scored by
recency/importance/relevance, and periodic *reflection* that synthesizes higher-level insights
from clusters of low-level memories; the spec calls reflection "the one memory op with
peer-reviewed ablation support" (spec §3).

**Borrowed (verdict: ADOPTED as dream Phase 5b REFLECT, 0.33.28):** per eligible actionable
cluster (learnings/issues/decisions), the dream writes ONE `reflection-<id>` page distilling
the cross-cutting practice, ending with a `Grounded in: [[member-a]], [[member-b]], …`
citation line so the synthesized rule stays traceable and retirable if contradicted
(`agents/dream-runner.md:144-176`). Idempotent via `member_hash`; kill switch
`SB_DREAM_REFLECT=off`, machine-enforced (the cluster script returns `[]`).

**Where this project differs / what was rejected:**
- The Generative-Agents *importance-accumulator cadence* was REJECTED — it assumes a
  continuous agent loop this system does not have; cadence here is per-dream + cluster
  eligibility (CHANGELOG 0.33.28).
- Their recency/importance retrieval scoring was NOT adopted (see the usage-frequency
  rejection, §1.8).
- Cautionary tale for external honesty: the first REFLECT shipped with a feedback loop
  (reflection pages re-entered the next dream's clustering input, defeating idempotence and
  able to spawn `reflection-reflection-<id>` growth); fixed as of 0.33.31 by excluding
  `generated: true` pages from clustering input (CHANGELOG 0.33.31). If you cite REFLECT
  externally, cite it as-of ≥0.33.31.

### 1.6 LongMemEval — the accepted (not yet met) eval bar

**What it is:** a benchmark (2410.10813) for chat-assistant long-term memory: information
extraction, multi-session and temporal reasoning, knowledge updates, and abstention.

**Position here (verdict: ACCEPTED as the bar; the suite does NOT exist yet):** spec §6 P8
commits to a "LongMemEval-shaped recall suite" — 20–50 hand-authored
(fact, gold-answer, planted-session) triples, decomposing retrieval-vs-reading (force-fed
ceiling vs real-retrieval actual), with abstention and knowledge-update first-class, and
exact-match assertions over LLM-judge ("judges pass ~63% of wrong-but-plausible answers").

**What exists instead, as of 0.33.31 (2026-07-05):**
- `mcp/src/tools/retrieval-guards.test.ts` (P8a/b, shipped 0.33.22) — deterministic canary
  rank-#1, knowledge-update overwrite-wins, episodic search→read round-trip, abstention on an
  absent term, graph-boost default-off.
- `tests/test-knowledge-eval.sh` — release gate: recall@2 = 1.0 over a curated 12-query
  fixture corpus (`tests/fixtures/eval-queries.jsonl`, count verified).

These are *regression gates*, not a benchmark result. See §2 for what this forbids you to
claim. Eval mechanics and how to extend them: sb-validation-and-qa.

### 1.7 Two smaller borrows (ledger completeness — credit these when relevant)

- **MinHash near-duplicate LSH** — a standard locality-sensitive-hashing technique, not tied
  to one paper. Adopted as the P4 redundancy engine: word 3-shingles → 128-hash signatures,
  integer-only and deterministic (`mcp/src/tools/minhash.ts`; CHANGELOG 0.33.26). One engine,
  three thresholds: capture NOOP/UPDATE at 0.9 (`SB_CAPTURE_DEDUP_THRESHOLD`), dream
  DEDUPLICATE candidates at 0.7 (`SB_REDUNDANCY_THRESHOLD`, `wiki-redundancy-cli.ts:42`),
  FORGET precision gate at 0.8 (`SB_FORGET_REDUNDANCY_THRESHOLD`,
  `scripts/wiki-forget-candidates.sh:35`). Externally citable stance: "the signal proposes,
  it never auto-deletes."
- **Cross-platform path-test discipline** — adapted from `vercel-labs/skills` via the
  designer-skills deep-scan (CHANGELOG 0.33.23): every traversal vector fed in BOTH
  forward-slash and backslash form so a regression fails on either OS, plus the `assertWithin`
  containment invariant (every vector either throws or stays inside base). Landing site:
  `mcp/src/path-guard.test.ts`. A methodology borrow — credit it when describing the test
  discipline, not a capability claim.

### 1.8 Deliberate rejections worth stating externally

- **Usage-frequency ranking and forgetting — rejected twice, constitution-enshrined.** The
  access-count search boost was cut (0.33.30) and the FORGET access/recency score terms were
  cut (0.33.25) as the recsys "rich-get-richer" hub bias; `CONSTITUTION.md:42-45` bans raw
  usage-frequency forgetting. Recency survives only as a tie-break. This is a *differentiator*
  vs recency/importance-scored memory stacks — state it as a design position with the
  evidence, not as a benchmark win.
- **From-scratch rewrite / migration to hermes-agent — rejected.** Spec §0: two independent
  research streams validated evolve-over-rewrite ("A second from-scratch rewrite would
  re-accrete (v1.0 proves it)"); spec §9: migration "relocates accretion; forfeits
  cross-platform fixes". The governance answer is the surface-budget ratchet (§2.1 item 3).
- **In-band self-editing memory tool calls — not adopted** (see §1.2).

---

## 2. Novelty-claims ledger — as of 0.33.31 (2026-07-05, working tree)

The 0.33.31 release existed only as uncommitted working-tree changes at authoring time
(`jq -r .version .claude-plugin/plugin.json` → 0.33.31; HEAD was the 0.33.30 release commit).
Re-check statuses with the Provenance commands before republishing any of this.

### 2.1 Defendable today (with the exact honest wording)

1. **Deterministic tool-time guardrails wired into PreToolUse, audit-logged.**
   Shipped: `scripts/persona-tool-guard.sh` matching `scripts/persona-rules.default.json`
   (ask/deny/rewrite actions; resource-scope allowlist; self-edit protection on the guard's
   own rule file and hook scripts), every verdict appended to `audit-log.jsonl`; plus
   symlink-guard, wiki-write-guard, flow-guard. **Honest wording:** "rule-based guardrails
   that fire at tool-time with an audit trail." **Do NOT say "learned" guardrails** — the
   pipeline that graduates transcript-derived practice into new rules is P2, plan-queued,
   zero code (`persona-rules.learned` appears only in the plan doc; verified). What exists on
   the learning side is REFLECT's grounded *prose* practices (§1.5), not firing rules.
   **Platform caveat:** all three path-matching guards were silently fail-open on Windows
   until the 0.33.31 fix (`sb_normalize_path` funnel; CHANGELOG 0.33.31) — any per-platform
   protection claim needs the per-platform test evidence.
2. **Bi-temporal, local-first knowledge base with reversible forgetting.**
   Validity-interval edge log with `supersedes` (§1.3); FORGET archives to
   `~/.second-brain/wiki-archive/` with a JSONL event log and `scripts/wiki-restore.sh`;
   `wiki_archive_ttl_days: 0` default = archived pages are never auto-deleted. **Honest
   wording:** "invalidate-don't-delete history; every eviction is reversible."
3. **Surface-budget-governed agent harness.** `.claude-plugin/surface-budget.json` (as of 0.33.31:
   skills 18, agents 9, scripts 52, tests 153) is a ratchet enforced by
   `scripts/validate-plugin.sh` (R8): live counts may not grow without a same-commit,
   git-blameable budget bump; CONSTITUTION.md is the enforced mission artifact. This
   anti-accretion forcing function is unusual in the plugin/agent ecosystem and is safe to
   present as a governance contribution. (CONSTITUTION.md cites validate-plugin.sh R8 correctly as of 0.43.0.)
4. **Evidence-based feature demotion as method.** The P7 story (§1.4): instrument a fashionable
   feature (graph ranking) on the real corpus, publish the numbers, demote to opt-in when it
   measures as a wash. The *method* is defendable and reproducible; present the numbers with
   the precision rule.
5. **Deterministic, offline, cross-OS memory operations.** MinHash near-dup signatures are
   integer-only (`Math.imul`, fixed seeds — byte-identical across OSes, CHANGELOG 0.33.26);
   clustering is deterministic; CI runs fully offline (`SECOND_BRAIN_DISABLE_EMBEDDINGS=1`,
   `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` — `.github/workflows/ci.yml:42-44`); committed
   bundles are byte-compared (`tests/test-bundle-current.sh`). **Honest wording:** "the memory
   pipeline degrades gracefully to a deterministic, dependency-free floor."

### 2.2 NOT defendable yet — label planned/open, never imply shipped

| Claim you might be tempted to make | Why it is not defendable (as of 0.33.31) | Status label to use |
|---|---|---|
| "SOTA recall" / any benchmark number | No LongMemEval-shaped suite exists (P8 mostly missing); the 12-query gate is a regression gate on a curated fixture, not a benchmark | planned (P8) |
| "Learned guardrails" / "learns your practices into active rules" | P2 is plan-queued, zero code | planned (P2) |
| "Fully-autonomous safe consolidation" | dream accept is human-reviewed or narrowly auto-accepted; the P6 quarantine/dual-LLM split is plan-queued; the unattended `auto_maintain` path is Linux-only (bwrap) and historically fragile (0.24.41) | open — the campaign target (sb-autonomous-consolidation-campaign) |
| "Injection-proof memory" | Sanitization strips invisible-Unicode channels (0.33.20/21) but the injection scanner is telemetry NOT a trust boundary (CONSTITUTION.md), and the kernel-boundary writer split is unbuilt | mitigated / planned (P6) |
| "Reranked retrieval" / nDCG gains | P3b not started — no plan doc, no code | candidate (P3b) |
| "Beats mem0/Zep/Letta on memory benchmarks" | No comparative eval run here; the spec itself treats vendor benchmark claims (LoCoMo/DMR) as "mutually disputed … marketing" (spec §11) | do not make |
| "Guards protect on all platforms" | No Windows CI lane exists; Windows assurance = local suite runs + stubbed-cygpath CI tests | qualified per-platform |

---

## 3. Claim discipline — measure before you claim

### 3.1 The measurement table

Before any external claim in the left column, produce the middle column; the right column says
what instrument exists as of 0.33.31 (2026-07-05).

| Claim class | Required measurement | Instrument today |
|---|---|---|
| Recall / memory quality | LongMemEval-shaped triples with retrieval-vs-reading decomposition (force-fed ceiling vs actual), abstention + knowledge-update cases, exact-match assertions | MISSING (P8); only `tests/test-knowledge-eval.sh` (12 queries, recall@2=1.0 gate) + `retrieval-guards.test.ts` |
| Guard protection | Inject the violation each guard targets, per guard, per platform ("a check that always passes is itself a silent failure" — spec §6 P8) | Partial: guard shell tests feed real violation vectors incl. Windows-form via stubbed cygpath (0.33.31); no systematic all-guards liveness harness |
| Token overhead ("lightweight") | Measured bytes/tokens per injection point, dated | Method exists — P1c measured the per-turn UserPromptSubmit injection at ~662 B / ~165 tokens, no wiki body (2026-06-30; CHANGELOG 0.33.30; spec §8) |
| Cross-platform correctness | A CI lane or live run per named platform | Linux + macOS(bash 3.2/BSD) CI only; NO Windows lane — Windows claims require local `bash tests/run-all.sh` evidence |
| Determinism / reproducibility | Byte-identical outputs across OS/runs | MinHash determinism vitest; deterministic clustering; `tests/test-bundle-current.sh` byte-compare |
| Reversible forgetting (§2.1 item 2) | An archive→restore round-trip on a real page: FORGET-archive it, `bash scripts/wiki-restore.sh <slug>`, reindex, confirm the page is back at its original path and findable; plus the never-auto-delete default | Partial: `scripts/wiki-restore.sh` shipped (`--list`; exit 0 ok / 1 not found / 2 usage); auto-revive locked by `tests/test-merge-auto-restore.sh` (extraction revives an archived slug instead of duplicating); `wiki_archive_ttl_days: 0` default (`scripts/ensure-dirs.sh:38`). NO dedicated round-trip regression test — run the round-trip yourself before claiming |
| Governance ratchet (§2.1 item 3) | Show the gate FIRES: in a scratch tree, add a surface file without a budget bump → `validate-plugin.sh` must fail "surface budget exceeded" (`scripts/validate-plugin.sh:205`) | Partial: the gate runs in CI on every push (plugin-validator step); the exceeded branch itself has NO regression test (verified 2026-07-05: `tests/test-validate-plugin.sh` fixtures set every budget to 99, exercising only the passing path) — demonstrate the failure live before claiming |
| Autonomy safety | Spec §8 P6 criteria: privileged writer with no network egress and no raw-transcript access, verified | MISSING — P6 remainder plan-queued |

### 3.2 Wording rules

- **Every number carries provenance:** version + date + the command or file:line that produced
  it (model: "measured over the real wiki, 96 pages/170 edges, 0.33.22"). Numbers without a
  reproduction path do not ship.
- **Statuses are one of:** shipped (version) / mitigated (residual named) / planned (plan doc
  path) / candidate (spec-only) / open. Never "coming soon", never present-tense for queued work.
- **Preprint figures are directional.** The spec's own caveat (§11): most quantitative research
  figures are 2026 preprints, "directional, not load-bearing"; peer-reviewed ablations
  (e.g. Generative Agents reflection) are the robust citations. Mirror that hierarchy.
- **Never cite vendor memory benchmarks as ground truth** (LoCoMo/DMR — disputed; spec §11).
- **Comparisons name the axis, not the winner:** "unlike X, consolidation here is hook-driven"
  is fine; "better than X" requires a comparative eval that does not exist (§2.2).
- **The ~10,000× precision rule** (§1.4) applies to every retelling of the graph story.
- **Reproducibility standard for any published result:** deterministic, offline, no-network —
  runnable via the repo's own gates (`cd mcp && npm ci && npm test`, `bash tests/run-all.sh`,
  `bash scripts/validate-plugin.sh`) with embeddings disabled, so a stranger can reproduce
  without a GPU, a model download, or an API key.

### 3.3 Review checklist for external text

Run this before publishing README/blog/paper/listing copy:

- [ ] Every capability claim maps to a §2.1 item or carries a §2.2 status label.
- [ ] Every number has version + date + source; volatile counts re-verified (Provenance below).
- [ ] No "learned guardrails", no benchmark numbers, no "fully autonomous" (until P2/P8/P6 ship).
- [ ] Graph story told with the precision rule; borrow credits named (mem0, Graphiti,
      Generative Agents, CaMeL, Aider) — this project's credibility rests on honest borrowing.
- [ ] Platform claims qualified (no Windows CI lane).
- [ ] Nothing contradicts CONSTITUTION.md or routes around validate-plugin.sh gates.

---

## 4. Writing a positioning one-pager

Use `references/one-pager-template.md` (sibling file) — a fill-in template for a README
section, blog post, or paper related-work block, pre-wired with the §2.1 defendable claims,
the §2.2 forbidden list, and a reproduce-it command block. Keep the filled result consistent
with this skill; when they diverge, this skill's ledger wins and the one-pager is stale.

---

## Provenance and maintenance

Derived from repo evidence only: `CONSTITUTION.md`; the spec
(`archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md`, esp. §3,
§5, §6, §8–§11); plan docs under `archive/docs:docs/superpowers/plans/2026-06-30-*`; `archive/docs:CHANGELOG.md`
0.24.39–0.33.31; `docs/plans/2026-06-10-r2-search-serving.md`; and the cited source files
(`raw-inbox.ts`, `graph-store.ts`, `retrieval-guards.test.ts`, `dream-runner.md`,
`persona-tool-guard.sh`, `persona-rules.default.json`, `ci.yml`, `surface-budget.json`,
`test-knowledge-eval.sh`). Authored 2026-07-05 against version 0.33.31 (0.33.31 was an
UNCOMMITTED working-tree release batch at authoring time; HEAD was the 0.33.30 commit).
The "field position" framing in §1 is maintainer-accepted project direction, not a repo file.

Re-verify volatile facts before reuse (run from repo root, git-bash/Linux/macOS):

```bash
jq -r .version .claude-plugin/plugin.json                      # plugin version
grep -n 'SB_CAPTURE_DEDUP' mcp/src/tools/raw-inbox.ts          # mem0-borrow capture dedup still present
grep -n 'supersedes' mcp/src/tools/graph-store.ts              # bi-temporal borrow still present
grep -rn 'SB_GRAPH_RANKING_BOOST' mcp/src/tools/retrieval-guards.test.ts  # P7 demote still locked
grep -rl 'persona-rules\.learned' scripts mcp/src || echo "P2 still queued (no code)"
grep -ril rerank mcp/src scripts || echo "P3b still not started"
ls mcp/src/tools/minhash.ts mcp/src/path-guard.test.ts scripts/wiki-restore.sh  # §1.7 + §3.1 landing sites still present
grep -ri graphify --exclude-dir=node_modules --exclude-dir=.claude . || echo "graphify still phantom"
awk 'END{print NR}' tests/fixtures/eval-queries.jsonl          # golden-query count (was 12)
cat .claude-plugin/surface-budget.json                                    # budget counts (skills/agents/scripts/tests)
git log --format=%s --grep=.^release:. -5                      # newest release records (CHANGELOG.md removed 0.34.0)
grep -rn 'LongMemEval' tests/ mcp/src || echo "P8 suite still missing"
```

If any command's output contradicts a statement above, update the statement and re-stamp the
date; statuses (P2/P3a/P3b/P6/P8) are the most drift-prone facts in this skill.
