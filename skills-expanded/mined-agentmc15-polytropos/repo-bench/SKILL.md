---
name: repo-bench
description: Benchmark Claude models on a repo's own real work and re-tier them from measured evidence — mined issue-fix pairs or red-validated mutation repairs, sandboxed candidates, four independent oracles. Use when the user asks to benchmark models on their repo, pick a daily driver, or re-tier models for a project. The default is a priced plan that spends nothing; a live run needs a cost ceiling the user confirms in this conversation.
allowed-tools: Bash, Read
---

# Repo bench

Run the engine that ships with this plugin. Use the `${CLAUDE_PLUGIN_ROOT}` env var Claude Code
sets for plugin-executed content; if it is unset, fall back to resolving
`../../bin/repo_bench.py` relative to this SKILL.md to an absolute path before shelling out.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" plan --repo <path> --models <ids-or-tiers>
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" run --repo <path> --models <ids-or-tiers> --live --max-usd <ceiling>
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" regrade --run <run-id> --live --max-usd <ceiling>
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" verdict --run <run-id>
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" apply --run <run-id>
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" list
python3 "${CLAUDE_PLUGIN_ROOT}/bin/repo_bench.py" demo
```

## Plan-first law — the one rule that overrides every other instinct

`plan` mines the repo, resolves candidates, and prints the exact models × tasks matrix priced
from `data/pricing.json` at run time (candidate dispatches AND judge grades, one total) — then
stops. It spends nothing. `run` without BOTH `--live` and `--max-usd` refuses structurally,
prints the same plan, and exits non-zero.

**NEVER add `--live` yourself.** When this skill is invoked, always run `plan` first, present
the plan and its total to the user exactly as printed, and only construct a `run --live
--max-usd <ceiling>` command after the user has explicitly confirmed a ceiling in THIS
conversation. A ceiling from a previous session, a guess at "what seems reasonable," or the
user simply asking a benchmarking question does not count as that confirmation. During a live
run the ceiling is re-checked before every single dispatch — candidate or judge — so a run that
hits it stops cleanly mid-matrix rather than overspending; the remaining cells are marked
skipped and the results are labelled `partial (cost-ceiling)`, never silently completed.
## Requirements when relaying results

- **`solved` means the tests oracle passed and nothing else, ever.** A judge grade or a similarity score never earns it; an unavailable oracle renders `n/a`, never a zero and never a failure.
- **Every dollar carries its basis** — `spend basis: actual`, `estimated`, or `mixed` — and a plan total is never a bill.
- **Quote the honesty labels verbatim**: `similarity … NOT a correctness verdict`, `BELOW EVIDENCE FLOOR`, `partial (cost-ceiling)`, `partial (setup failed)`, `DISAGREEMENT — signal, not error`, `n/a (unparseable)`, `STALE VERDICT`.
- **Relay the false-negative bound as an interval** — `solved lies in [lower, upper]` — the lower bound routing-grade, the upper bound diagnostic and forgeable; name any applied out-of-scope paths verbatim and let the reader judge them.
- **State oracle coverage** per verdict (cells objectively scored out of total), and call out candidates whose `solved` cells came with test-file edits or whose `not solved` cells carry reverted out-of-scope paths.
- **A setup failure or an unverifiable setup artifact is an unavailable oracle, never a failed candidate.**

`regrade` spends and carries exactly the law above — never add `--live` yourself, show the cost first, and only construct the `--live --max-usd` form after the user confirms a fresh ceiling in this conversation; read `references/regrade.md` before constructing one.

## The evidence floor

A candidate needs a structural minimum number of objectively-scored (tests-oracle-available)
tasks before its measurement is routing-grade — the same floor precedent as the passive ledger,
pinned higher because an active re-tiering decision changes routing for every future kit.
Below that floor, `verdict` still prints the raw measurement table, but the card, the envelope,
and `verdict.md` all carry **`BELOW EVIDENCE FLOOR`** stamped at the top — present it exactly
that way, never softened into something like "limited data" or "preliminary results." A
below-floor verdict is not a weaker verdict to be reported with hedges; it is explicitly
labelled as not a routing-grade verdict at all. `--min-tasks` can only RAISE the floor for a
given run, never lower it, and `apply` hard-refuses a below-floor verdict outright.

## The three legs — never average them

The repo already has two other legs of routing evidence: a PUBLISHED prior
(`bin/bench_routing.py` over the benchmark index) and OBSERVED outcomes
(`bin/routing_scorecard.py` over kits this repo has actually run). `repo_bench` is the third
leg: MEASURED-ON-DEMAND, on this specific repo's own work. `verdict` prints all three side by
side per candidate — published index (when the model appears in the benchmark data), observed
first-try rate (when the target repo's own kit ledger evidences it, `no ledger evidence`
otherwise), and this run's measured result.

**Lead with the measured verdict** when presenting results — it is the most specific evidence,
gathered on this repo, for this task shape. Show the published prior and the ledger beside it
for context. When the legs disagree — for example, this run's measured ranking inverts the
published index's order — the card prints **`DISAGREEMENT — signal, not error`**. Repeat that
framing verbatim when you relay it: a disagreement between legs is something to investigate and
mention, never something to average away or silently resolve toward whichever leg looks more
authoritative.

## Apply is a separate, explicit action

`run` measures; `verdict` renders; **`apply` is the only thing that ever changes routing, and
it is always its own explicit user action.** Never chain `run` straight into `apply`, and never
run `apply` on the user's behalf without them having seen the verdict first — `apply` prints
exactly what it is about to write (old tiers, new tiers, source run) as its own confirmation,
and there is no `--yes` flag because running the command IS the opt-in. `apply` also refuses:
when the named run has no verdict recorded yet, when the verdict is below the evidence floor,
or when any tier/daily-driver model id in the verdict is no longer present in the current
`data/pricing.json` (stale evidence — the benchmark must be re-run, not silently reapplied).

A successful `apply` writes a gitignored `prefs/repo-bench.json` with this schema:
`schema_version`, `applied_at`, `source_run`, `repo`, `tiers` (`strong`/`mid`/`weak`, each a
model id or `None`), `daily_driver` (a model id or `None`), and `labels` (carried over from the
verdict card — a below-floor verdict never reaches this file, so `labels` here never includes
the below-floor stamp). Consumption is pull-only: nothing in this plugin auto-reads this file
or auto-applies a routing change; a router that wants to use it has to go check for it.

## The tests-as-oracle exposure

Running a target repo's test suite executes arbitrary code from that repo. This kit treats that
as the same trust a user already extends when running their own tests — never more. It runs
ONLY inside a sandbox or scratch copy under the run's own working area, with its cwd there, and
only when the user explicitly supplied `--test-cmd`. `repo_bench` never invents a test command
and never runs one against this plugin repo itself. Only benchmark repos whose test suite you
would run by hand — no sandboxing theater is claimed beyond that; the honest statement of scope
IS the fence.

## References — read when

- `references/regrade.md` — read before constructing any `regrade` command: what it re-dispatches, what it refuses, and why a prior verdict goes `STALE VERDICT`.
- `references/calibration.md` — read when sizing a ceiling: `task_profiles` has measured roughly ten times low on real agentic work, and `plan` prints a calibration line from your own store.
- `references/acquisition.md` — read when choosing `--mode`, or considering `--with-gh` and the `--gh-repo` it requires.
- `references/oracles.md` — read when interpreting a cell: the four oracles, the constructed substrate behind `solved`, the false negative it buys, and the full-patch diagnostic.
- `references/setup.md` — read when the target must build or install before its tests run (`--setup-cmd`, `--setup-key`, and the three honesty rules that ride with them).
- `references/isolation.md` — read before telling a user what is and is not written outside the run directory.
- `references/subcommands.md` — read when constructing any command: every flag, per subcommand.
- `references/presenting.md` — read when writing results up: the full relay rules behind the requirements above and the test-path substring caveat.
