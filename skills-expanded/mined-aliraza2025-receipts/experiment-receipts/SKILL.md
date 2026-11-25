---
name: experiment-receipts
description: Plans and reads out product experiments (A/B tests, variant tests, usability pilots) with the decision stated first, a precise primary metric, sample size as a planning assumption, guardrails, a privacy-scoped event contract, and a clear split between what was verified and what was simulated. Use when the user designs an A/B test, picks an experiment metric, estimates sample size, instruments analytics events, or writes an experiment readout.
---

# Experiment receipts

An experiment plan should let a skeptical reader see the decision, the metric, and exactly what has and has not been checked. This skill writes the plan and the readout.

## Workflow

1. **Decision first.** Write the decision as a question with two outcomes, e.g. "Should intake show every field at once or guide the user through steps?"
2. **Primary metric.** Define it precisely: eligible population, exposure event, success event, counting rule (each participant once), and what success is not (e.g. reaching review is not approval or revenue).
3. **Sample size as an assumption.** Run `scripts/sample_size.py` with a stated baseline and minimum detectable effect. Label the output "planning assumption" until a pilot gives a real baseline.
4. **Guardrails.** Metrics that must not get worse (errors, handoffs, time to complete) and the business rules both arms must share.
5. **Event contract.** Allowlist the event names and properties. Exclude free text, names, contact details, and anything not needed for the metric.
6. **Stopping rule.** Fix eligibility, exclusions, horizon, and the stopping rule before collecting randomized traffic.
7. **Readout.** Use the template. Keep "verified", "simulated", and "not yet run" in separate sections.

## Sample size script

```bash
python3 scripts/sample_size.py --baseline 0.40 --mde 0.15
# per arm: 173 (two-sided alpha 0.05, power 0.80)
```

Options: `--alpha` (default 0.05), `--power` (default 0.80). The script uses the standard two-proportion normal approximation and only the Python standard library.

## Readout template

```markdown
# [Experiment name] readout

**Decision:** ...
**Primary metric:** ... (definition)
**Guardrails:** ...

## Verified
- Implementation facts that were actually tested (assignment repeatable, events delivered, properties stripped)

## Simulated or illustrative
- Anything produced with synthetic data, with a note that its rates are authored, not observed

## Not yet run
- Real-user sessions, powered test, business outcomes

## Result
- [Only observed results, with n per arm, interval, and date. If none: "No real-user results yet."]

## Next decision
- ...
```

## Example (planning)

Baseline completion 40%, minimum detectable effect 15 percentage points, two-sided 5% significance, 80% power: about 173 participants per arm. Plan for 200 per arm as headroom, and revisit after a usability pilot. These are assumptions, not results.

## Rules

- Never report a synthetic simulation's conversion rates as evidence that a variant works.
- A missing user identifier is not enrollment.
- Count exposure before success; ignore success events that precede exposure.
