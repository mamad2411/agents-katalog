---
name: posthog_experiment
description: Set up a sound PostHog A/B experiment or feature flag rollout — hypothesis, primary metric, exposure, and a sample-size check before launch.
---

# PostHog Experiment

> Unofficial, agentstack-authored. Not affiliated with or endorsed by PostHog.

Use this skill when a team wants to test a change with a PostHog experiment or roll
a feature out behind a flag, and needs the setup to actually yield a trustworthy
result.

## Workflow

1. Write the hypothesis as one falsifiable sentence: "Changing X will move
   [primary metric] by roughly Y for [population]." If you cannot state it this
   way, the experiment is not ready.
2. Choose **one primary metric** that maps directly to the goal (e.g. signup
   conversion), plus a small set of guardrail metrics that must not regress.
3. Define the exposure point — the feature flag and the event that marks a user as
   enrolled. Users must be counted from the moment they could see the change, not
   from when they convert.
4. Estimate the needed sample size and runtime from the baseline rate and the
   minimum effect worth detecting. State how long the test must run; resist
   calling it early.
5. Set the rollout: start the flag at a safe percentage, confirm assignment is
   stable per user, and verify both variants render before ramping.
6. Pre-commit to the decision rule (ship / kill / iterate) and the metrics that
   decide it, in writing, before launch.

## Conventions

- One primary metric per experiment. Multiple primaries invite cherry-picking.
- Do not peek-and-stop: respect the planned runtime and sample size.
- Keep the feature flag key descriptive and consistent with the experiment name.
- Roll out gradually (e.g. 5% → 25% → 100%) and watch guardrails at each step.

## Boundaries

- Never declare a winner before the experiment reaches its planned sample size or
  runtime — early results are noise.
- Do not change the primary metric or population mid-flight to chase significance.
- Do not flip a flag to 100% for all users without an explicit go-ahead.
