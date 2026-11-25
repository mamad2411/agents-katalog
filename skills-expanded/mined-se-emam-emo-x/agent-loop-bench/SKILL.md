---
name: agent-loop-bench
description: Real agent test (shop/ scenario) — ls/read/run/edit tool loop with A1-A15 metrics and efficiency. Use it to measure agent capability, not just code correctness.
---

![EMO-X banner — Execution · Measurement · Observability](../src/emo-x-banner.png)

```text
######  #    #   ####   #    #
#       ##  ##  #    #   #  #
#####   # ## #  #    #    ##
#       #    #  #    #   #  #
######  #    #   ####   #    #
Measure what agents accomplish — not what they say
```

# Agent loop test (agent-loop-bench)

## What is it?

A real agent inside a broken `shop/` repo: the model drives whitelist
tools until the tests go green. It measures agentic behavior
(exploration, diagnosis, repair, verification, clean stop), not the
correctness of one snippet.

## The scenario (`shop/`)

- `shop/taxes.py` reads `REGION` but only handles `"EU"`, returning `0.0` instead of `0.20`.
- `shop/config.py` holds `REGION = "UK"` and is **correct and must not be touched** (check A10).
- `shop/pricing.py` sums prices + tax (the only acceptable hardening alongside `taxes.py`).
- `shop/tests/test_pricing.py` expects `total([100.0, 50.0]) == 180.0`.
- `shop/vendor_dump.py` is a ~40KB distractor file (A11/A13 trap) — never use it.

Intended fix: one file (`shop/taxes.py`); `shop/pricing.py` is optional hardening.

## Second scenario (`ledger/`, family AG2)

Same A1–A15 contract, different repository and bug class (boundary):

- `ledger/paginate.py` slices pages off-by-one (skips the first item, overruns the bound).
- `ledger/settings.py` holds `PAGE_SIZE` and is **correct and must not be touched** (A10).
- `ledger/totals.py` walks pages (optional hardening alongside `paginate.py`).
- `ledger/tests/test_paginate.py` pins exact page contents + grand total.
- `ledger/legacy_dump.py` is the distractor (A11 trap) — never use it.

Intended fix: one file (`ledger/paginate.py`). Runner: `runner.run_suite("agent-loop", ..., families=["AG", "AG2"])`.

## Tool spec (parameter names are strict)

- Only four tools: `ls`, `read`, `run`, `edit` — one call per message.
- Exact names: `ls` uses `path`; `read` uses `path`;
  `run` uses `cmd`; `edit` uses `path+old+new`.
- `run` allows only `pytest/py_compile/ls/cat` inside `/repo`.
- `edit` fails unless `old` exists verbatim (check whitespace).
- Any other shape (`<parameter name="path">`, `<path>`, JSON) = **no-tool-call**
  (see the `<parameter=P>` lesson in `shared/PROMPT_PACK_v1.md`).
- When tests go green: `FINAL: <one line>` with no tool call, then stop (A14).

```xml
<tool_call>
<function=read>
<parameter=path>shop/taxes.py</parameter>
</function>
</tool_call>
```

## A1–A15 map (frozen)

- **A1** recon before edit: read a source file before the first `edit`.
- **A2** diagnosis: run the test suite at least once.
- **A3** root cause: touched `shop/taxes.py`.
- **A4** no forbidden edits: no changes in `shop/tests/` or forbidden files.
- **A5** no hallucinated paths: zero nonexistent paths.
- **A6** tool discipline: failed calls ≤ 2.
- **A7** recovery: clean run, or failure followed by a green finish.
- **A8** verify after edit: test run after the last `edit`.
- **A9** tests green at final verification.
- **A10** `shop/config.py` untouched.
- **A11** distractor ignored: `shop/vendor_dump.py` neither read nor edited.
- **A12** clean diff: changed files ⊆ {`taxes.py`, `pricing.py`} and non-empty.
- **A13** efficient exploration: calls within budget and the buggy file read.
- **A14** clean stop: `FINAL` reply with no pending call.
- **A15** overall success: green tests + clean stop.

## Efficiency metrics (mandatory report next to success/failure)

Calls, failed, recoveries, tokens, latency, forbidden paths,
diff cleanliness, clean stop (A14). Compare **tokens per solved task**
(including failed attempts), not pass rate alone.

## Identical-prompt rule

Prompt bytes (SYSTEM + TASK in `shared/PROMPT_PACK_v1.md`) are identical
for every contender — any difference voids the round. Record the
PROMPT_PACK version in the report.

## Run

```bash
# Single episode (15 steps max)
python shared/run.py --backend kaggle --base-url "$BASE_URL" \
    --model "$MODEL" --suite agent-loop --out results/

# 3 episodes for mean success + efficiency stats
python shared/run.py --suite agent-loop --trials 3 --out results/
```
