---
name: verify-no-model
description: Prove a change to the extraction pipeline actually works end-to-end WITHOUT downloading the BERT model — FakeModel/FakeTokenizer injection, regex-only API paths, CLI run from a scratch directory, and when to escalate to real integration tests via [run-integration]. Use after changing extractor.py, stemmer.py, tokenizer.py, constants.py, or models.py, or when the user asks "does it still work?" in a sandboxed environment.
---

# verify-no-model — end-to-end verification without BERT

Unit tests passing is necessary but not sufficient — this skill exercises the real
pipeline. The constraint: `all-MiniLM-L6-v2` is a ~90MB download and unit tests /
sandboxes must never trigger it. The model loads **lazily**: constructing
`InsightExtractor` or `SentenceTokenizer` is safe; the download fires only on first
access to `extractor.model` / `tokenizer.tokenizer` (triggered by `extract()`,
`extract_semantic_keywords()`, `extract_key_sentences()`,
`update_thread_keywords(auto_expand=True)`, `count_tokens()`).

**Always run from a scratch directory, never the repo root** — the CLI and default API
write `insights_extracted.md` + `insight_extractor_state.json` into CWD and *reload*
any state file already present (committing these artifacts has happened before, and
stale state contaminates later runs).

## Level 1 — model-free API paths (regex + dynamic keyword pipelines)

These paths never touch the model and verify most changes to `constants.py`,
`stemmer.py`, and the regex half of `extractor.py`:

```bash
mkdir -p /tmp/ie-verify && cd /tmp/ie-verify
python - << 'EOF'
from insight_extractor.extractor import InsightExtractor

extractor = InsightExtractor(seed_keywords=["ransomware", "CVE", "exploit"],
                             output_dir="/tmp/ie-verify")
text = open("/path/to/repo/sample_input.txt", encoding="utf-8").read()

regex_hits = extractor.extract_regex_entities(text)      # static patterns
dynamic_hits = extractor.extract_dynamic_entities(text)  # stemmer patterns
positions = extractor.extract_keywords_with_positions(text)
matches = extractor.stemmer.find_matches(text)           # list[MatchInfo] — attributes!

print({k: v[:3] for k, v in regex_hits.items()})
print({k: v[:3] for k, v in dynamic_hits.items()})
print(f"{len(positions)} positioned matches, {len(matches)} stemmer matches")
EOF
```

Check the output like CI's smoke test does: assert on **specific expected values**
(e.g. a CVE id you know is in the input), not just non-emptiness. Remember
`seed_keywords=[]` falls back to all 363 `THREAD_SEEDS` — pass a real list to control
the test.

## Level 2 — full pipeline with fakes (semantic paths, report, state)

The sanctioned pattern from `tests/unit/test_extractor.py`: inject stand-ins directly
on the private attributes. This exercises `extract()`, Markdown report generation,
dynamic expansion, and state save/load — the complete orchestration — with zero
downloads:

```bash
cd /tmp/ie-verify
python - << 'EOF'
from typing import Any
import numpy as np
from insight_extractor.extractor import InsightExtractor

class FakeModel:
    def encode(self, texts: Any, *_a: Any, **_k: Any) -> np.ndarray:
        items = [texts] if isinstance(texts, str) else texts
        return np.array([[float(i), 1.0, 0.5, 0.25] for i, _ in enumerate(items, 1)])

class FakeTokenizer:
    def tokenize_sentences(self, text: str, *, max_tokens: int = 512) -> list[str]:
        return [p.strip() for p in text.split(".") if len(p.strip()) > 10]

extractor = InsightExtractor(seed_keywords=["ransomware", "CVE", "exploit"],
                             output_dir="/tmp/ie-verify", similarity_threshold=0.0)
extractor._model = FakeModel()
extractor._tokenizer = FakeTokenizer()

result = extractor.extract(
    "Ransomware operators exploited CVE-2026-1234 via phishing. "
    "The exploit touched 192.168.1.10 and ransom@example.com."
)
assert "CVE_ID" in result.regex_entities
assert result.semantic_keywords and result.key_sentences

md = extractor.save_results_to_markdown(result)
extractor.save_state(md.parent / "state.json")
fresh = InsightExtractor(seed_keywords=["x"], output_dir="/tmp/ie-verify")
fresh._model = FakeModel()  # BEFORE load_state — see injection-order gotcha below
assert fresh.load_state(md.parent / "state.json")
print("full pipeline OK ->", md)
EOF
```

Fake-shape rules: `encode()` must return a 2-D `np.ndarray` with one row per input and
a **consistent width** (keyword and chunk embeddings feed one `cosine_similarity`
call); `tokenize_sentences` returns `list[str]`. With fakes, similarity *values* are
meaningless — verify shapes, model fields, report sections, and state round-trip, never
score magnitudes.

Note the injection order gotcha: `load_state()` with keywords present calls
`_recompute_keyword_embeddings()`, which touches `.model` — inject the fake **before**
calling `load_state()` on an instance you don't want downloading.

## Level 3 — read the artifacts

Open `/tmp/ie-verify/insights_extracted.md` and check every section renders:
header fields, Regex Entities, Dynamic Keyword Matches, Semantic Keywords table,
Key Sentences table, Newly Expanded Keywords, Keyword Statistics. A formatting bug in
`save_results_to_markdown` (pipe-escaping, truncation at 120/200 chars) is invisible to
the assertions above but obvious in the file.

Then clean up: `rm -rf /tmp/ie-verify` — and confirm `git status` in the repo shows no
generated files.

## Level 4 — when fakes are not enough: `[run-integration]`

Escalate to real-model integration tests when the change affects what fakes replace:

- model loading itself (`model` property, `ModelLoadError` paths, `model_name` handling)
- real tokenization (`AutoTokenizer` usage, `chunk_text` token math, `max_tokens` logic)
- embedding semantics (threshold tuning, normalization, similarity behavior)
- dependency bumps of torch / transformers / sentence-transformers / accelerate

Mechanism: include the literal tag `[run-integration]` in the commit message, or ask
the owner to trigger `workflow_dispatch` — CI then runs `pytest tests/integration/`
with cached HF weights. If the current environment can download the model, you may run
`pytest tests/integration/ -v --tb=short` locally instead. If neither is possible,
push with the tag and **report in the PR body** that integration verification is
pending CI.

## Exit report

State what was verified at which level and what was not:

```
verify-no-model: L1 regex+dynamic ✓ (CVE-2026-48710 found in sample_input) |
L2 full pipeline w/ fakes ✓ (report + state round-trip) | L3 report sections ✓ |
L4 not needed (no model-path changes)
```
