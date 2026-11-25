---
name: loom-bench
description: Runs and reports a Loom benchmark — when a paid run is allowed, which harness answers the question, proving the treatment ran, judging a delta against noise. Use when asked to benchmark, measure recall or answer accuracy, A/B a setting, or update docs/benchmarks/results.md. Not for test or CI speed.
argument-hint: "<question to answer>"
metadata:
  internal: true
---

# Loom benchmarks

## 0. Ask first

A benchmark run spends provider money and hours of wall clock. Offline harnesses and `--help` are free; anything that ingests or judges is not. In Claude Code every `bench/*.py` and `make bench*` command asks first, `--help` included. "Keep the bench numbers" means the existing numbers.

Before a paid run, even one the requester asked for, reply with the question, the harness and arms, the item count and repeats, the provider and judge, and whether the treatment can change anything on that dataset (read the code path first: a setting that scores every row of the dataset alike cannot move the result). Start only after a yes to that plan. Use the provider keys the requester's environment already has; never copy a key from another checkout's `.env`. A run never outlives the session that started it: stop its server, its ClickHouse and the harness before you report.

A benchmark is the confirm step, never exploration: the diagnosis (failing items, their shared pattern, the change and the result it predicts) comes first, and every named part of the change is built before the run.

## 1. Pick the harness

Name the question first ("does rerank X raise recall@10 on multi-hop without losing single-hop?"), then the harness and the arms that answer it: [running](../../../docs/benchmarks/running.md) lists them, [methodology](../../../docs/benchmarks/methodology.md) says what each measures. Prefer one paired run (`--ask-arms`, `--repeats 3 --gate`) over two separate runs: one ingest, per-item deltas.

## 2. Run against the code you mean

```bash
PYTHONPATH=$PWD .venv/bin/python bench/<harness>.py --help
curl -s "$LOOM_BASE_URL/v1/health" | jq '{build_commit, status}'   # your build, when started with LOOM_BUILD_COMMIT (loom-dev-setup §5)
```

- The server is a private one started from this worktree (`loom-dev-setup`) with real providers; fake providers make every score meaningless.
- A cached answer path can replay an older build's answers: confirm the cache key covers the setting under test, or turn the cache off for the run.
- Bench namespaces are erased at the end of the run; pass `--keep-namespaces` only when a re-score is planned.

## 3. Prove the treatment ran

Before reading a single score, check from the run's own output or the server's ledger that arm B did what B means: the setting was applied, the tool was called, the leg returned rows. A "no difference" or a big win from an arm that never ran is the most common false result. A "regression" whose items were scored against zero ingested memories is an ingest failure, not a code change: check the ClickHouse log for out-of-memory or DNS errors before reading the scores.

## 4. Judge the delta

- A change ships on the **lower bound** of the paired, clustered bootstrap, not the mean ([the verdict](../../../docs/benchmarks/methodology.md#the-verdict)).
- `unresolved` inside the null band is noise; outside it the run is under-powered — add items, not repeats.
- An A/A run of the same arm twice is the noise reference for a new harness or judge. At n = 30 a same-config pair swings ±13 pp, a few items either way ([how wide the interval is](../../../docs/benchmarks/methodology.md#how-wide-the-interval-is)); a few-point delta between two passes is judge noise plus a re-ingest until the bound says otherwise.
- recall@K and judged QA accuracy are separate axes; never set one beside the other ([recall and answer accuracy](../../../docs/benchmarks/methodology.md#recall-and-answer-accuracy-are-separate-axes)).
- Report every category, including the one that went down.

## 5. Write it up

- The PR body carries the numbers, the command that reproduces them, the model and judge, and the item count.
- Quote a headline number only from `docs/benchmarks/results.md`, never from memory or an old run.
- `docs/benchmarks/results.md` names files by bench and sections by model, never by commit or date (history is rewritten; commit ids rot).
- A measurement never goes in a code comment.
- Keep run outputs (`bench/matrix_runs/`, `MATRIX_RESULTS.md`, `/tmp/*.csv`) out of commits.
