---
name: costs
description: "Report API-equivalent costs for Claude Code usage — per chat, skill, subagent, project, model, day, git branch, or PR. Collects fresh data from session transcripts, then reports from the cost ledger. Triggers on 'what did this chat cost', 'how much did X cost', 'costs this month', 'token spend', 'cost report', 'what did that PR/branch cost'."
---

# Costs — Usage Cost Accounting

Reports what multiplai usage *would have billed* at Claude API list prices,
from the append-only cost ledger in `<data_dir>/costs/`. Two scripts:

- `collect_costs.py` — incrementally scans `$CLAUDE_CONFIG_DIR/projects/**/*.jsonl`
  and appends priced records to the ledger. Idempotent; first run is a full
  backfill, later runs read only new bytes.
- `costs_report.py` — aggregates the ledger.

## Steps

1. **Collect first** so the report includes recent sessions:
   ```
   uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/collect_costs.py"
   ```
2. **Report** based on what the user asked:

   | User asks | Command |
   |---|---|
   | overall / this month | `costs_report.py` |
   | a specific month | `costs_report.py --month YYYY-MM` |
   | this chat / a session | `costs_report.py --session <id-prefix>` (current session id is in the transcript filename) |
   | per skill | `costs_report.py --all --by skill` |
   | per project / model / day / component | `costs_report.py --by project\|model\|day\|component` |
   | per branch | `costs_report.py --all --by branch` |
   | one branch | `costs_report.py --branch <name>` (reads all months; `--branch "(none)"` for unattributed) |
   | a PR | resolve the branch with `gh`, then `--branch` — see below |
   | cost per completed task | `costs_report.py --all --group task --pr-join --project-dir <repo>` |
   | cost per buildme block | `costs_report.py --all --group build --project-dir <repo>` |
   | cache utilization | `costs_report.py --all --report cache [--cache-threshold 0.5]` |

   All via `uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/costs_report.py" ...`.
   Add `--json` when you need to post-process numbers.

3. Present the relevant numbers concisely. Always mention once: costs are
   **API-equivalent** (list-price USD) — on a subscription nothing was actually
   billed per call.

## Cost of a PR

`costs_report.py` is deliberately `gh`-free; PR→branch resolution happens here:

1. Resolve the PR's branch:
   ```
   gh pr view <num> --repo <owner>/<repo> --json headRefName -q .headRefName
   ```
   (batch: `gh pr list --repo <owner>/<repo> --state all --json number,headRefName`)
2. Report on it:
   ```
   uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/costs_report.py" --branch <that-branch>
   ```
3. If several PRs were cut from one branch, they **share** the branch's cost —
   say so when presenting the number.

## Cost per completed task

Raw tokens and raw dollars answer "what did we spend", not "what did it cost to
get something done". Two outcome units are available:

- `--group task --pr-join` — a *task* is a branch whose PR state resolves via
  `gh` (merged / closed / open / no-pr). Rows carry cost + tokens + outcome, and
  the summary divides total cost by merged-PR count, with per-task median/p90.
  A repo `gh` cannot reach degrades to `no-pr` rather than failing the report.
- `--group build` — buildme's finer signal, joined from
  `specs/changes/*/.build-state.json`: cost per DONE block *and* cost per FAILED
  block. The failed-block figure is the retry-and-loop spend, which is where
  verification changes (adjudication, reviewer panels) either pay for themselves
  or don't.

**Framing rule — cross-model comparisons must be per-outcome, never
per-token.** Different models tokenize differently, so the same work yields
different token counts; a cheaper per-token model that loops twice is more
expensive. When comparing models or pipeline versions, quote cost per merged PR
or per DONE block. Quote per-token numbers only within one model.

## Cache utilization

`--report cache` computes, per project/skill/component, the hit ratio
`cr / (in + cr)` and the cache-write share, flagging rows under the threshold
(default 50%). The data is already in every ledger record — no collector
change, so it works on historical months.

Baseline measured 2026-07-25 over the whole ledger: **99.7% overall hit ratio**
(4.77B cached / 4.78B eligible tokens); every SDK component
(deep-research, buildme, dream, catalogs, model_client) sat at 100.0%, and
interactive at 99.7%. Cache breakpoints in the in-house pipelines were already
placed correctly — the finding is "already optimal", not a fix. Write share is
the number to watch instead: `model_client` writes 65% and `catalogs` 36%, i.e.
they re-write prefixes more often than they reuse them.

## Branch attribution caveats

- `branch` comes from the transcript's per-entry `gitBranch` field, which
  reflects the repo at the session's **cwd**. Sessions run at the workspace
  root record the workspace repo's branch (usually `main`) even when the work
  targeted a sub-project via `git -C`. Sessions run inside a worktree or
  sub-project (the default workflow for non-trivial changes) attribute
  correctly. A mid-session `git checkout` splits records across branches.
- Records collected before this feature show `(none)` until the one-time
  enrichment is run:
  ```
  uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/collect_costs.py" --backfill-branches
  ```
  Idempotent; safe to re-run. Non-git cwds and SDK-sourced records stay `(none)`.

## Notes

- Skill spans inside interactive chats are approximate by construction (a
  skill is prompt injection, not a separate API context). SDK pipeline
  components (buildme, deep-research, dream) are exact.
- Subagent traffic is `sidechain` records; `--session` shows the
  main/subagent split.
- **Prices come from the official pricing page, fetched at collect time.**
  `collect_costs.py` refreshes `<data_dir>/costs/pricing.json` from
  `platform.claude.com/docs/en/about-claude/pricing.md` before pricing
  (skipped while the cache is under a day old; `--no-refresh` opts out).
  Offline, the table bundled with `multiplai-core` is used. Records already
  in the ledger keep the price they were written with — a price correction
  changes new records only.
- Unknown models are priced at fallback rates and flagged
  `pricing_fallback: true` in the ledger. The collector prints a WARNING
  naming them; when you see it, the dollar figures for those models are a
  guess — say so in the report rather than quoting them as list price.
- Cache reads on Claude Fable 5.1 / Mythos 5.1 are 0.025× input ($0.25/MTok),
  not the 0.1× every other model uses. Records collected before 2026-09-13
  priced them at $1.00/MTok.
