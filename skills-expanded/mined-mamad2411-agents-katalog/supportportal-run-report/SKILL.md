---
name: supportportal-run-report
description: Use when diagnosing a live SupportPortal run in the current compose environment and you need both timing trace details and the answer chain that explains why the customer saw that reply.
---

# SupportPortal Run Report

## Overview

Run one real SupportPortal client trace and output a single Chinese report that combines `Time Trace` and `Answer Chain`. By default this skill batch-runs the repo `real_case/real_user_questions.txt`, but it also supports one-off live questions with `--message`.

## When To Use

- You need one report that explains both latency and answer behavior after a SupportPortal change.
- You need to know whether RAG actually worked, whether `rag_unavailable` happened, and what the best available customer reply would be even if the final persisted assistant message is missing.
- You need to explain review, intake, investigation, or engineer fallback behavior without switching between two older skills.
- You want the raw trace artifact path under `/tmp/supportportal-traces` for follow-up inspection.

## Workflow

1. Run `scripts/run_supportportal_run_report.py`.
2. Let the wrapper stop early if `/health` is unhealthy.
3. By default it reads the repo `real_case/real_user_questions.txt`, runs all non-empty lines, and prints one merged markdown report with a case summary plus per-case sections.
4. For each case, read the report in this order:
   - `Best Available Customer Reply`
   - `Time Trace`
   - `Answer Chain`
   - `RAG Verdict / Direct Probe`
5. If the trace did not persist a final assistant message, the wrapper still prints a non-empty reply and labels its source as one of:
   - `ticket_message`
   - `final_result`
   - `direct_probe`
   - `predicted_clarify`
   - `predicted_investigation`
   - `diagnostic_placeholder`
6. If lexical retrieval looks slow and you want deeper BM25/FTS detail without a benchmark, rerun with `--profile-lexical`.

## Defaults

- `mode="batch"`
- `real_case_file="<repo_root>/real_case/real_user_questions.txt"`
- `product="audio_video_calling"`
- `base_url="http://127.0.0.1:8080"`
- `repo_root="current SupportPortal worktree if detected, otherwise /Users/xieziling/Desktop/personal_proj/SupportPortal"`
- `output_dir="/tmp/supportportal-traces"`

## Commands

Run from the SupportPortal repo root so the project-local skill scripts are used:

```bash
python3 .codex/skills/supportportal-run-report/scripts/run_supportportal_run_report.py
python3 .codex/skills/supportportal-run-report/scripts/run_supportportal_run_report.py --message "How to join channel"
python3 .codex/skills/supportportal-run-report/scripts/run_supportportal_run_report.py --message "what should I do when I got black screen"
python3 .codex/skills/supportportal-run-report/scripts/run_supportportal_run_report.py --message "How to join channel" --profile-lexical
```

## Output Contract

The wrapper prints one merged markdown report to `stdout` with:

- environment health summary
- request metadata
- a always-non-empty `Best Available Customer Reply` plus `reply_source`
- `Time Trace` module timings and optional lexical profiling
- `Answer Chain` route / review / intake / investigation explanation
- RAG health verdict and direct-probe attribution when needed
- raw trace artifact path

## Resources

### scripts/

- `run_supportportal_run_report.py`: main batch/single-run wrapper
- `trace_compat.py`: compatibility fallback when the live ticket message schema lacks the newer `meta` column

## Notes

- Real compose environment only; do not swap to `TestClient`.
- Do not run benchmark flows from this skill.
- If `RAG_SERVICE_SHARED_TOKEN` is not in the current shell, the wrapper reads the repo `.env` first and then falls back to the running container env.
- Default batch mode ignores blank lines in `real_case/real_user_questions.txt`.
