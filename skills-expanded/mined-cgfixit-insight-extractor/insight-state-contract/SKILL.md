---
name: insight-state-contract
description: Verify Insight_Extractor JSON state round trips, malformed-state errors, failure atomicity, legacy categories, path semantics, and lazy model restoration. Use for persistence changes in cgfixit/Insight_Extractor.
---

# Insight state contract

Work in the user's active Insight_Extractor checkout. Confirm its Git root and
origin; read `AGENTS.md` and delegated guidance before edits. Resolve paths below
from that root and use its Python 3.12+ virtual environment. Diagnose for a check
request; implement changes only when the task authorizes a fix.

## Establish the current contract

Read `save_state`, `load_state`, `_reset_keyword_runtime`, embedding refresh callers,
and `extract` in `src/insight_extractor/extractor.py`; inspect `config.py`,
`exceptions.py`, CLI error handling in `__main__.py`, and state tests in
`tests/unit/test_extractor.py`. Use actual signatures and serialized fields.

At creation the state includes keyword bank, frequencies, categories, stem mode,
similarity threshold, model name, and version 1. `child_safety` is mapped to
`ai_safety`. Missing files return False. Malformed JSON is wrapped in StateLoadError,
but schema failures can leak other exceptions and partially mutate the object.
Reconfirm these observations; do not encode defects as the desired contract.

## Exercise isolated fixtures

Use `tmp_path` or `TemporaryDirectory`, explicit UTF-8, and synthetic text. Never
load or overwrite the user's real `insight_extractor_state.json`. Set
`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_HUB_DISABLE_TELEMETRY=1`.

- Round-trip supported fields and enum values, Unicode keywords, and the legacy
  category. Inspect optional/missing fields, an empty bank, and unsupported versions;
  distinguish current compatibility behavior from a proposed schema change.
- Probe malformed JSON, invalid UTF-8, a list/null/scalar root, wrong field types,
  invalid enum values, and invalid numeric settings. Cover read errors with injected
  filesystem failures instead of platform-specific permission tricks.
- Compare absolute Path, relative Path, and deprecated relative str paths from a
  scratch working directory with a distinct output_dir. The live implementation may
  resolve str relative to output_dir and Path relative to cwd; do not silently unify
  them in an unrelated fix.

## Failure atomicity

Initialize an extractor with known state and injected fake model/tokenizer objects.
Before each invalid load, snapshot keyword values, Counter values, categories,
settings, compiled pattern behavior, embedding values/dirty flag, and identities
of model/tokenizer/runtime objects. Copy mutable values; retaining only references
can hide in-place mutation. Supply some valid changed fields followed by an invalid
field so the test detects partial application, not just early parse failure.

After failure, assert the established error contract and unchanged state/runtime.
Also verify the source file was not modified. Treat a leaked exception or changed
object as a finding. File-write atomicity is a separate property; do not claim that
testing load rollback proves save_state survives interrupted writes.

## Lazy restoration

Replace the actual model-construction boundary with a sentinel that raises if called.
Load a valid state with a different model name: cached model and tokenizer should
be invalidated, embeddings cleared/marked dirty as appropriate, and regex runtime
restored without encoding or downloads. Check same-model and empty-bank cases too.
Run regex/dynamic matching immediately after load. Only then inject fake `_model`
and `_tokenizer` for a semantic call and verify embeddings correspond to restored
keywords. Injecting before load is insufficient when a changed model name clears them.

## When fixing is requested

Validate/prepare incoming state before publishing it to the live extractor, including
fallible enum conversion and regex compilation. Preserve legacy compatibility, lazy
loading, filenames, and version unless the task explicitly changes the contract.
Prefer a focused fix over a new persistence framework. Add regressions for the exact
schema failure and rollback problem, plus the successful lazy-restoration path.

Run `python -m pytest tests/unit/test_extractor.py -q --tb=short`, then repository
preflight for a code fix. Report a matrix of valid load, malformed input, rollback,
path behavior, and lazy restoration with concrete observed results and skipped
checks. Do not claim the existing optional integration suite proves these contracts.
Commit/push only within authorization already present in the task.
