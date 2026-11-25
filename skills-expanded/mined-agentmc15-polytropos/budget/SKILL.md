---
name: budget
description: Run an execution kit on a cheaper ladder of models when the AI-Credits budget is tight — one-tier-lower dispatch with honest actual-vs-standard cost reporting. Use when the user says budget mode, run this cheaply, low on credits, or wants the savings measured.
---

You run an existing execution kit at reduced cost by demoting where the driver dispatches,
never how it verifies or reviews. Read the kit's `PLAN.md` fence before starting, same as a
normal `execute` run — budget mode changes dispatch, not scope.

## The budget ladder

| Role | Standard tier | Budget tier | How enforced |
|---|---|---|---|
| architect (planner) | frontier | strong | taught here — the driver never dispatches the planner |
| implementer | mid | cheap | enforced by `run --budget` |
| verifier | cheap | cheap (unchanged) | already the floor |
| reviewer | strong | strong (unchanged) | `review` gains no budget flag |

Savings come from exactly two moves — the planner drop and the implementer drop. The strong
reviewer is deliberately preserved: it is the defect net that catches what cheap tiers miss,
and it is also the one instrument that would detect budget mode itself backfiring.

## Run a kit in budget mode

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_execute.py run --kit <dir> --task <id> --budget [--budget-profile M]
```

Preview with `--dry-run` first — a real run spends real AI Credits. The demotion is exactly
one tier, floor cheapest: it never fabricates a rung and never jumps two. Escalation still
climbs the normal ladder on a verified failure, so the first rung up is the tier the task
would have started at under standard dispatch. Do not combine `--budget` with
`--max-escalations 0` — a demoted task that fails verify would go straight to `blocked`
instead of getting the one escalation attempt budget mode is designed around.

## Read the measurement — it can say budget mode failed

The `budget est.:` line the driver prints is a labeled estimate — a named task profile, a
single-dispatch first-try counterfactual — never a bill. `BACKFIRED` means the escalations
this run needed cost more than the demotion saved. Total a whole kit with:

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_execute.py budget --kit <dir>
```

The headline net covers only completed (`done`) runs — blocked runs and runs that made no
demotion are reported on their own separate labeled lines, never folded into that net. If the
verdict says the kit is LOSING money, drop `--budget` for the rest of that kit — believe the
ledger, not the theory. With only two roles downgraded, a single escalation can erase a whole
run's saving.

## Reviews run at full strength — use them more, not less

`review` takes no budget flag by design; it always dispatches the reviewer agent at its
standard strong tier. Budget mode's cheap implementer makes the phase review MORE valuable,
not less, so run one at every phase boundary — it is priced per phase, not per task, so the
insurance is cheap exactly when implementation quality is most likely to have dropped.

## The planner under budget

The architect drop (frontier→strong) cannot be driver-enforced — the driver never dispatches
the architect. It is taught, not enforced: pick a strong-tier model for `/architect` runs
yourself, via the `/model` picker or `--model`, choosing a candidate from

```bash
python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py models
```

never from memory — the roster and tiers can change under you.

## Same-named agent

There is no budget agent — budget mode is a skill-only capability in this bundle. The driver
still dispatches the existing implementer and reviewer custom agents; --budget changes which
tier the implementer dispatch runs on, never which agent runs it.

## Installed?

If the literal `{{POLYTROPOS_ROOT}}` text is still visible above, the bundle is not
installed — tell the user to run `python3 bin/harness_select.py install --harness copilot`
(then `/skills reload` picks the skills up in-session).
