---
name: wiki-experiment
description: File experiment results to the wiki following the SCHEMA Ingest procedure. Use after an experiment run produces metrics, ablations, or comparisons worth keeping as durable project memory.
---

An experiment run has produced results worth remembering. File them to the wiki so future sessions can build on them rather than re-deriving.

## What to capture

Identify the experiment from the conversation or ask the user:

- Which experiment / variant ran (e.g., MuSiQue v3 with entity-overlap rank, BM25 drift temperature sweep)
- Configuration used (parameters, seeds, dataset, scale, restart probability, type weights, softmax temperatures)
- Headline metrics. For MuSiQue, report per hop count (2 / 3 / 4 hop). Standard metrics: MRR, recall@k, multi_hop_hit@k, any-gold@pool, all-gold@pool
- What changed vs. the previous run on the same benchmark
- What was surprising or worth flagging
- Path to the experiment's `results/` directory

## Procedure

Follow the Ingest procedure defined in `.llm-wiki/SCHEMA_<repo>.md`. The steps below are pointers, not a substitute for SCHEMA:

1. Read existing wiki pages for this experiment first. Likely candidates: the benchmark page (`HotpotQA-Benchmark` or `MuSiQue-Benchmark`), the headline results page (`MuSiQue-PoC-Results` or similar), comparison pages (`Drift-Variants-MuSiQue`, `Independent-vs-Chained-Retrieval`), and the concept pages whose claims the result bears on (`Softmax-Normalization`, `Named-Entity-Concept-Extraction`, `Entity-Overlap-Ranking`, `Typed-Predicate-Ontology`, `RAG-Sanity-Check`, etc.). Integrate rather than duplicate.
2. Create or update an experiment-results page. Frontmatter: `type: synthesis` or `type: entity`; `up:` pointing to the benchmark page; typed edges (`supports:` / `criticizes:` / `extends:`) when the result confirms or refutes a prior claim on another page.
3. Page body should include: configuration, headline metrics, what changed vs. previous run, what was surprising or worth flagging, link to the experiment's `results/` directory, link to the relevant commit hash.
4. **Honest reporting.** Bad results, contradicted claims, and worsened metrics get filed truthfully, not polished. Per CLAUDE.md and the global rule: never report accuracy from projections, only from real script outputs.
5. Update concept pages whose claims this result bears on. If a new result contradicts a wiki claim, update or flag the affected page, do not leave the contradiction.
6. Fix cross-references in both directions on every affected page (`[[Page]]` in frontmatter, `[Display](Page)` in body).
7. Update `index_<repo>.md` with one-line descriptions of new pages in the right category.
8. Append a `## [YYYY-MM-DD] update | Experiment name` entry to `log_<repo>.md`. The first bullet is the attribution line `- by: <name> via claude-code`, where `<name>` is the output of `git config user.name` in the wiki repo (read it, do not invent it). Then 2 to 5 bullets describing the run. See "Log Entry Attribution" in `SCHEMA_<repo>.md`.
9. **Run the Verification Gate** at `${CLAUDE_PLUGIN_ROOT}/core/agents/verification-gate.md` over every page created or edited. Do not commit until all criteria pass. The gate catches projection-as-fact, missing corpus tags on numerical claims, missing back-references, and missing log/index entries — the failure modes the discipline-gates Universal Rationalizations table enumerates.
10. Commit in the wiki's own git repo in two steps: first stage and commit the page and index changes by name with a descriptive message, then stage and commit the `log_<repo>.md` entry on its own. One commit per log entry keeps `git blame` on the log a faithful per-entry record (see "Log Entry Attribution" in SCHEMA). Do not push unless the user requests.

A single experiment write-up typically touches 5 to 15 pages.

## When to skip

- The run was a debug rerun with no new information.
- The run failed before producing meaningful metrics. (Record the failure mode separately if it teaches something about the architecture.)
- Configuration is identical to a previous run already filed.

## After running

Tell the user which wiki pages were created or updated, summarize the headline result in one sentence, and remind that the wiki commit is local. Push only if asked.
