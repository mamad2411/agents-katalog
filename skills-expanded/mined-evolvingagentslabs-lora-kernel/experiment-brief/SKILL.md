---
name: experiment-brief
description: Pre-register a run before it starts — what is measured, why, which models and provider, what it costs, what would falsify it, and when to abort. Use before any benchmark, α measurement, training run or arm in this repository; the briefing goes before the command, never beside the report.
---

# Brief the experiment before running it

A briefing written next to the report is not a briefing. It is a justification.

## Write this file first

Create `<run-dir>/BRIEF.md` **before** the first token is generated:

```markdown
# <step id> — <one line>

**Question.** The single thing this run answers.
**Falsification.** The result that would kill the step. Written now, while the
answer is unknown.
**Arms.** Each one, and why it is being bought *now* rather than after.
**Suite.** Split, n, and why this subset carries the signal.
**Models.** Exact tags and the provider actually serving them.
**Parameters.** Temperature, `k`, max tokens, seed.
**Cost.** Estimated calls and dollars, and the ceiling at which this run stops.
**Abort rule.** The condition under which the run is killed early, decided now.
**Redesign count.** How many times this instrument has been reshaped. Three is
the stopping condition.
```

## The four rules the brief exists to enforce

1. **Buy arms in sequence.** The arm that can kill the hypothesis runs first. An
   attribution arm — the control that explains *why* — is bought only once there
   is an effect to attribute. A flat result makes every other arm unnecessary,
   which is exactly when a grid has already spent the money.
2. **Name the provider, not just the model.** A configured model is not
   necessarily the model that runs: this organisation has shipped a system where
   every model but one silently fell back to a different one.
3. **State the falsification before the run.** A condition invented after the
   numbers arrive is a description, not a test.
4. **Decide the abort rule while it is still cheap.** A run already paid for is
   not an argument for finishing it; compare what remains against what an abort
   would force you to repeat, and record which you chose.

## When the run finishes

Append the outcome to the same `BRIEF.md` — including "flat", "aborted at case
14", or "the falsification condition fired". Then update the step's row in
[`docs/PLAN.md`](../../../docs/PLAN.md), marked **[ran]**
with the run directory named.
