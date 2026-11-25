---
name: insight-optimizer
description: Make 1-3 measured, minimal optimization to Insight_Extractor's regex, dynamic-stemmer, state, or keyword-expansion paths without changing public behavior or lazy model loading.
---

# Codex optimizer (Insight_Extractor)

This is a measured optimization workflow, not a broad refactor.  
Target repo: `CGFixIT/Insight_Extractor` (Python 3.12+, Pydantic v2, lazy SentenceTransformer).  
Source of truth order: live source → `CLAUDE.md` → `docs/SPEC.md` → `README.md`.  
Start a new change from current `origin/main` on a `codex/` branch; preserve an existing task branch. Trace every caller of a shared helper before touching it.

## Hard Constraints (never violate)

- Do **not** touch BERT / SentenceTransformer behavior unless you have a reproducible model-backed benchmark. Unit tests must stay model-free (`extractor._model = FakeModel()` injection).
- Do **not** add dependencies.
- Do **not** change public signatures, default thresholds, report format, or state JSON schema.
- Do **not** remove or weaken lazy model loading (`model` / `tokenizer` properties).
- Do **not** break exact match order, deduplication, span fidelity, or exception paths.
- Preserve the keyword-mutation sequence after any change:
  Follow the current mutation path in `update_thread_keywords`; `load_state` rebuilds regex runtime and marks embeddings dirty without loading a model. Do not make state loading eager.
- Line length ≤ 100. Prefer `pathlib.Path` + `encoding="utf-8"`. No f-strings in log calls.
- Use `# ponytail:` comments for deliberate ceilings.

## Candidate Hot Paths (ranked by real cost in current code)

1. **`DynamicKeywordStemmer` compilation & matching** (`stemmer.py`)
   - `compile_keywords` / `compile_keywords_incremental` (chunking at `max_pattern_length=50_000`, snapshot comparison).
   - `_resolve_source_keyword` (exact lookup → ordered substring fallback; linear scan still present).
   - `find_matches` + `ChunkedKeywordPattern.finditer` (multi-pattern sort + span dedup).
   - `_get_keyword_lookup` cache invalidation on every mutation.

2. **`KeywordPatternRegistry.extract_all`** (`stemmer.py`)
   - Static pattern compile cache (`_compiled_static_patterns`).
   - Dynamic regeneration path after keyword growth.
   - Per-label `seen` sets.

3. **`InsightExtractor.extract_regex_entities`** (`extractor.py`)
   - Per-instance `_compiled_regex_patterns` dict.
   - Repeated `findall` + order-preserving dedup over `REGEX_PATTERNS`.

4. **State path** (`extractor.py`)
   - `save_state` / `load_state` (pretty JSON, no compression, no integrity hash).
   - Full stemmer + registry rebuild on every load.

5. **TF-IDF candidate selection in `update_thread_keywords`**
   - Fresh `TfidfVectorizer(max_features=200, ngram_range=(1,3))` on every call.
   - Candidate embedding + cosine filter against `_keyword_embeddings`.
   - Fallback “add one highest-TF-IDF term” logic.

## Loop (strict)

1. Establish a deterministic, model-free baseline:
   - Relevant unit tests (`tests/unit/test_stemmer.py`, `test_extractor.py` stubs).
   - `timeit` or repeated-input micro-benchmark on the exact hot path (fixed seed text, fixed keyword bank size).
2. Identify the actual allocation, recompilation, or linear scan.  
   Do **not** invent a cache or abstraction.
3. Make the smallest local change that preserves:
   - exact output order,
   - deduplication semantics,
   - match spans,
   - exception behavior.
4. Add or update **one** focused unit test that locks the preserved behavior.
5. Re-run:
   - the same baseline benchmark,
   - `preflight` (ruff + mypy + unit tests),
   - `verify-no-model`.
6. Keep the change only when:
   - the measurement is reproducible, and
   - the diff is smaller than the operational complexity it introduces.

If the baseline shows no meaningful bottleneck, stop and report exactly:

> no safe optimization identified

Do not manufacture a cache, configuration knob, or “money-mode” behavior to create a diff.

## Evidence Required in Final Report

- Benchmark input (text size / keyword count) and repetition count.
- Before / after wall time or allocation delta (same machine, same Python).
- Exact tests + gates run.
- Model / integration checks skipped and why.
- Any remaining `# ponytail:` ceiling.

## Known Ceilings (do not “fix” without proof)

```python
# ponytail: linear scan retained in _resolve_source_keyword fallback;
#           build an indexed matcher only after profiling proves it matters

# ponytail: ChunkedKeywordPattern still sorts all matches;
#           true streaming merge only after real multi-chunk workloads appear

# ponytail: TfidfVectorizer rebuilt every update_thread_keywords call;
#           rolling corpus only after multi-document expansion is measured
```
