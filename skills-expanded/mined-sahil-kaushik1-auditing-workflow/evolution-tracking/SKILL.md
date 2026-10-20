---
name: evolution-tracking
description: >
  Track component changes, measure marginal improvement, manage rollback.
  Used by the Evolution Manager during the long feedback loop.
---

# Evolution Tracking Skill

## Purpose

Track every change to scanner components, measure whether the change helped,
and maintain rollback capability. Prevents reverse evolution.

## Change Tracking Protocol

For every proposed component change:

```markdown
# Experiment: {ID}

## Component Modified
[Exact file path, e.g., `.claude/agents/deep-reasoner.md`]

## Change Description
[What was changed and why]

## Hypothesis
[What improvement is expected]

## Baseline Measurement
[Performance on benchmark before change]
- Hit rate: X/Y known vulnerabilities found
- False positive rate: A/B
- Cost per finding: $C

## Post-Change Measurement
[Performance on same benchmark after change]
- Hit rate: X'/Y
- False positive rate: A'/B'
- Cost per finding: $C'

## Verdict
[INHERIT / REJECT / NEEDS MORE DATA]

## Rollback Command
git checkout {commit} -- {file_path}
```

## Measurement Requirements

A change is measured by running against a **known-vulnerability benchmark**:
- Set of contracts with known bugs
- Expected findings (ground truth)
- Compare: what was found before vs. after the change

## Inheritance Criteria (ALL must be true)

- [ ] Works on 3+ different projects
- [ ] Measurable improvement in hit rate
- [ ] No regressions (nothing previously found is now missed)
- [ ] Cost per finding does not increase disproportionately
- [ ] Can be explained and attributed to the specific change
- [ ] Can be rolled back with a single git command

## Anti-Patterns This Prevents

| Anti-Pattern | How We Prevent It |
|-------------|-------------------|
| Global prompt dumping | Changes are LOCAL to one component |
| No measurement | A/B testing is mandatory |
| No rollback | Git-based rollback always tracked |
| Accumulating mutations | Only proven changes are inherited |
