# Kubera — autonomous POC

Multi-agent quant firm simulation. Researchers generate signals, QSDs filter, Tech implements, auto-promoter advances strategies through paper → live_simulated → live_pending_signoff. Only the final step to **live_real** (real capital) requires human signoff.

## What "autonomous" means here

- **Across time**: a scheduler daemon ticks every N seconds, checks state, spawns headless `claude -p` sessions when there's work.
- **Per-stage**: each agent session runs end-to-end without intervention.
- **NOT autonomous**: promotion from `live_pending_signoff` to `live_real`. This gate is intentional for the POC. If you want zero-human live trading, remove it as a deliberate one-line change.

## Prerequisites

- Python 3.11+, `pip install -r requirements.txt`
- For real mode: `claude` CLI installed and authenticated via Max subscription
- **Unset `ANTHROPIC_API_KEY`** before running — Claude Code will otherwise bill through API instead of your Max plan

## Quickstart (mock mode — no claude calls)

```
pip install -e .
pip install flask
kub init
kub agent register researcher_so researcher --signal-quota 50
kub agent register researcher_bob researcher --signal-quota 50
kub agent register qsd_so qsd
kub agent register tech_so tech
kub agent register qt_so qt

# Terminal 1: scheduler (mock — simulated agent sessions)
python -m orchestrator.scheduler --mock --interval 2 --simulated-days-per-tick 5

# Terminal 2: dashboard
python -m orchestrator.dashboard
# open http://127.0.0.1:5000
```

## Real mode (spawns claude -p subprocesses)

```
unset ANTHROPIC_API_KEY
python -m orchestrator.scheduler --interval 600
```

Each tick the scheduler: auto-promotes strategies, ticks paper trading, spawns researcher/QSD/Tech sessions based on queue depth, records everything in the sessions table. Usage counts against Max plan. `firm/HALT` file pauses scheduling.

## Stages

| Stage | Who advances | How |
|---|---|---|
| submitted -> under_review | orchestrator | Structural validation |
| under_review -> approved/rejected | QSD agent | LLM judgment |
| approved -> backtested | Tech agent | Implementation + backtest |
| backtested -> paper_trading | auto-promoter | OOS + walk-forward thresholds |
| paper_trading -> live_simulated | auto-promoter | 14 days paper, paper Sharpe > 0.8 |
| live_simulated -> live_pending_signoff | auto-promoter | 30 days paper, paper Sharpe > 1.0 |
| live_pending_signoff -> live_real | **HUMAN** | Dashboard button or CLI |

## Tuning

Promotion rules live in the `promotion_rules` table, not in code:
```
sqlite3 firm/ledger.db "UPDATE promotion_rules SET min_oos_sharpe = 1.2 WHERE rule_id = 'bt_to_paper'"
```

## Kill switch

```
touch firm/HALT     # scheduler skips ticks
rm firm/HALT        # resume
```

## The bug loop (mandatory discipline for any bug fix)

**Every bug fix in this repo follows this loop. No exceptions.** Violating the letter violates the spirit.

1. **RED — write the failing test first.**
   Reproduce the bug with a test that fails before any production code changes. The test name describes the invariant being restored (e.g. `test_walk_forward_proxy_is_conservative`). Test against real code where feasible; mock only at boundaries (HTTP, external APIs).
2. **VERIFY RED — watch it fail.**
   Run the test and read the failure message. Confirm it fails for the right reason (missing behavior, not a typo or setup bug). If the test passes immediately, you're testing existing behavior — rewrite.
3. **GREEN — minimal fix.**
   Write the smallest production-code change that makes the test pass. No refactors in this step. No "while I'm in here" cleanups.
4. **VERIFY GREEN — run the new test AND the full suite.**
   - `pytest tests/test_flint_bridge.py -v` (or the scoped equivalent)
   - `python tests/test_flint_bridge.py` (the standalone runner — also counts)
   - `python smoke_test.py` (if touching orchestrator-wide state)
   All three must be green. Don't proceed otherwise.
5. **REFACTOR (optional).** Only after green. Tests stay green throughout.

**Why this matters here specifically:** Kubera's correctness guarantees are financial. A bug that silently inflates auto-promotion (like the walk-forward proxy at 0.85 — see `RUNBOOK.md §9.7`) routes noise straight to paper trading, which pollutes downstream metrics, which corrupts QSD calibration, which makes every future approval decision worse. Tests-first is the only way to prove the fix actually catches the regression before it ships.

**The "tests after" trap.** Tests written after the fix pass immediately. They prove nothing. They might be checking a property the code already had, not the property that was broken. You won't notice until the bug comes back in six months and you discover your "regression test" never actually caught the regression.

**The "revert and verify" trick.** If you're fixing a bug that already has code in place (e.g. you're tightening an existing value), the discipline is: write the test, temporarily revert the fix (`sed` is fine), run the test, confirm it fails, re-apply, confirm it passes. See `git log` for examples; the last three §9 fixes in `RUNBOOK.md` were verified this way.

**When NOT to use the loop:** throwaway prototypes, generated code, config files. If unsure, use the loop.
