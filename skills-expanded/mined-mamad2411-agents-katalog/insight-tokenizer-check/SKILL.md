---
name: insight-tokenizer-check
description: Check Insight_Extractor tokenizer chunk termination, invalid token budgets or overlap, token coverage, and lazy loading. Use for tokenizer bugs or regressions in cgfixit/Insight_Extractor, not general NLP tuning.
---

# Insight tokenizer check

Work in the user's active Insight_Extractor checkout. Confirm the Git root and
origin; read its `AGENTS.md` and delegated guidance before edits. Resolve all paths
below from that root and use its Python 3.12+ virtual environment. A check request
authorizes diagnosis; implement a fix only when the user requests one.

## Trace the actual boundary

Read `src/insight_extractor/tokenizer.py`, `tests/unit/test_tokenizer.py`, and callers
of `chunk_text`, `tokenize_sentences`, and `extract_semantic_keywords` in
`src/insight_extractor/extractor.py`. Inspect live signatures before proposing tests.
At creation, `chunk_text` advances by `max_tokens - overlap`, while sentence splitting
passes overlap 50. Treat these as starting clues, not proof they remain unchanged.

## Reproduce without hanging the test runner

Set `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_HUB_DISABLE_TELEMETRY=1`.
Inject a deterministic object into `SentenceTokenizer._tokenizer`; its `encode`
should return identifiable integer tokens, and `decode` should record token slices.
Reuse the existing fake's interface; never load HuggingFace assets for these checks.

Before probing suspect arguments, bound the experiment. Prefer a fake `decode`
that raises a dedicated diagnostic exception after a small fixed call budget on a
tiny input (for example, eight calls for six tokens). Report that exception as a
nontermination signal, never as valid production rejection. For a defect that can
loop before decode, use `subprocess.run([...], timeout=5)` with the same interpreter;
the subprocess must terminate on timeout. Do not use an unbounded thread or sleep.

Check distinct cases:

- Ordinary chunking, overlap zero, final partial chunk, and exact budget boundary.
- Zero/negative budgets, negative overlap, overlap equal to or above the budget,
  and non-integer arguments where supported validation is under review.
- Empty and short text as well as input exceeding the budget: the short-input
  shortcut can conceal invalid arguments.
- `tokenize_sentences` with budgets below, equal to, and above 50 on long sentences.

Assert termination, each chunk's token budget, ordered token coverage with only the
requested overlap, and no dropped tail when overlap is zero. Decoded text need not
round-trip byte-for-byte with a real tokenizer; compare recorded token slices.
Separate current observed behavior from the desired validation contract.

## When fixing is requested

Define whether invalid input should raise or be normalized, using existing contracts
and the user's request. Put validation before tokenization and short-input returns;
make the sentence caller's overlap compatible with valid small budgets. Preserve
default behavior and avoid unrelated sentence-scoring changes. Add focused regression
tests that fail safely on the old code, including the zero-overlap tail case.

Patch constructors at their actual import site when checking laziness; the runtime
module need not expose `AutoTokenizer` because its top-level import is TYPE_CHECKING-only.
Verify construction remains lazy and injected-tokenizer calls never load a model.

Run `python -m pytest tests/unit/test_tokenizer.py -q --tb=short`, then repository
preflight for a code fix. Report arguments/input, bounded reproduction, expected
versus actual results, checks run, and remaining failures. Fake-tokenizer success
does not establish real-model compatibility. Do not commit, push, or download models
without authorization already present in the task.
