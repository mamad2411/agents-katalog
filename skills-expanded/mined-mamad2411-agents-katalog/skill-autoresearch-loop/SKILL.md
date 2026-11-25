---
name: skill-autoresearch-loop
description: Run a bounded autoresearch loop to improve one existing skill at a time using a fixed small harness, an explicit metric, and keep-or-reject iteration decisions. Use when ratcheting skill quality without turning the process into open-ended experimentation.
---

# Skill Autoresearch Loop

Use this skill to improve one existing skill in a controlled way.

## Use when

- one skill is already useful but still awkward or inconsistent
- you want to reduce manual commands, retries, or repo-specific edits
- you can define a small repeatable harness with 3-5 scenarios
- you want a ratcheting keep-or-reject loop instead of ad hoc tweaking

## Do not use when

- the skill does not exist yet
- the workflow has no stable test harness
- the first validation path would require risky production mutation
- the goal is vague, such as "make it better somehow"

## Core rules

- improve one skill at a time
- define one primary metric before editing anything
- keep the harness fixed while iterating
- make one meaningful change per iteration
- keep the change only if the result improves without adding risk
- save run artifacts outside this repo under `~/.AGENTS-temp/<repo>/...`

## Main script

### Scaffold an autoresearch workspace

```bash
bash scripts/init-autoresearch-workspace.sh \
  <repo-name> <skill-name> [primary-metric]
```

Example:

```bash
bash scripts/init-autoresearch-workspace.sh \
  trustdev imagebuilder-bake-validate \
  "first-try success rate"
```

This creates:

- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/00-goal.md`
- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/01-harness.md`
- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/02-baseline.md`
- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/03-iteration-template.md`
- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/04-decision-log.md`
- `~/.AGENTS-temp/<repo>/autoresearch/<skill>/runs/`

## Recommended workflow

1. Pick one existing skill and one narrow primary metric.
2. Run `init-autoresearch-workspace.sh`.
3. Fill in the harness with 3-5 repeatable scenarios.
4. Record a baseline before changing the skill.
5. Make one bounded change to:
   - `SKILL.md`
   - one script
   - or one default/parameter pattern
6. Re-run the same harness.
7. Append the result to the decision log:
   - keep
   - reject
   - or defer

## Good first candidates

- `imagebuilder-bake-validate`
- `ami-validation-ssm` after extraction
- `ecs-rollout-validation` after extraction
- `cis-override-decision` after extraction

## Related references

- for metric ideas and harness patterns, read `references/metrics-and-harness.md`
- for high-level rationale, read `docs/AUTORESEARCH_FOR_SKILLS.md`
