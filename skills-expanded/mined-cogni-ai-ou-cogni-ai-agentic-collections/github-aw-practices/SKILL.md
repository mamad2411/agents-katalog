---
name: github-aw-practices
description: 'Organizational practices, rollout strategies, and A/B experiment specifications for maintaining repositories with GitHub Agentic Workflows (gh-aw).'
license: MIT
---

# Skill: github-aw-practices

This skill provides organizational practices, rollout strategies, and A/B experiment specifications for maintaining
repositories with GitHub Agentic Workflows (gh-aw).

## WHEN TO USE

- When planning the rollout of a new GitHub Agentic Workflow across an organization.
- When configuring A/B experiments to test prompt variations in production.
- When establishing centralized repository practices for AI agents.

## WHEN NOT TO USE

- For debugging syntax errors within a specific workflow file (use `github-aw-syntax` or `github-aw-troubleshooting` instead).
- When writing the actual prompts for the agent (use `ai-prompt-writer`).
- For generic GitHub Actions that do not involve AI agents.

## Common Pitfalls

- **Immediate Production Writes**:
  Giving a new, untested agentic workflow full write access to the main branch
  without going through a staged or shadow evaluation phase.
- **Unbounded Triggers**:
  Allowing any user to trigger expensive AI workflows via issue creation without implementing
  integrity filtering or safe-outputs.
- **Ignoring A/B Stats**:
  Running an A/B experiment but failing to actually collect or analyze the metrics needed
  to determine the winning variant.

## A/B Experiments

The experiments section of the workflow frontmatter enables statistical A/B testing by defining named experiments,
each with a set of variant values. At runtime the activation job selects one variant per experiment using a balanced
round-robin counter and exposes the selection to the workflow prompt.

### Declaring Experiments

Add an `experiments` map to the workflow frontmatter. Each key names an experiment; the value is either a simple array
of variants (bare-array form) or a rich object with additional metadata fields.

### A/B Experiments Specification (Version: 1.0.0, Status: Draft)

This specification defines the A/B experiment system for GitHub Agentic Workflows (gh-aw). It covers the experiments:
frontmatter schema, variant selection algorithms, state persistence backends, expression and template integration,
activation job structure, audit CLI integration, and statistical analysis requirements.

Conforming implementations provide operators with a zero-infrastructure mechanism to conduct controlled experiments on
agentic workflow behavior using only workflow frontmatter declarations, without any external service dependency.

## Maintaining Repos with Agentic Workflows

Open-source maintainers face a unique challenge when running agentic workflows: anyone can open an issue or PR,
triggering agent runs that consume compute and tokens — but not every contributor is equally trustworthy. gh-aw
addresses this with two complementary safety mechanisms:

- **Safe-outputs** — The primary mechanism for controlling what an agent can do. Every GitHub mutation (opening issues,
  commenting, creating PRs) must be explicitly declared; anything not listed is blocked.
- **Integrity filtering** — The primary mechanism for controlling what content the agent sees. Content from untrusted
  authors is filtered from the agent's context before the run starts.

Together they form a defense-in-depth model: integrity filtering keeps untrusted content out of the agent's context,
and safe-outputs ensure the agent can only produce authorized side-effects.

## Organization Practices

Organization Practices collects guidance that matters at team and enterprise scale such as:

- Safe rollout strategies before production writes are enabled
- Workflow sharing across repositories and organizations
- Centralized ownership models for workflow infrastructure
- Platform conventions for versioning, review, and promotion

## Safe Rollout

Safe rollout is the practice of increasing workflow autonomy in steps instead of enabling direct production writes
immediately.

The main question is not whether a workflow is useful, but whether it is trusted enough to act on the live system.
In practice, teams usually move through a ladder: report-only first, then staged behavior, then a more realistic
safe-write technique if needed, and finally direct production writes.

### Rollout Ladder

The usual progression is:

1. Start in report-only mode.
2. Enable staged behavior when proposed writes need to be previewed.
3. Use shadow evaluation when preview mode is not enough and the real write path needs to be exercised safely.
4. Promote the same workflow to direct production writes.

`staged` and `shadow evaluation` are not interchangeable:

- Staged mode is sufficient when the question is what the workflow would do.
- Shadow evaluation is needed when the question is whether the real write path behaves correctly on a safe
  non-production target.

## Sharing Workflows

Sharing workflows across an organization involves several independent layers. Each layer can be adopted independently;
teams do not need all of them at once.

The recommended enterprise pattern is to maintain one central agentic-workflows repository with versioned workflow
templates and shared components. Consuming repositories then use `gh aw add` to install full workflows and `imports:`
to pull in common modules.

## References

- [A/B Experiments](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/experiments.md)
- [A/B Experiments Specification](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/experiments-specification.md)
- [Maintaining Repos with Agentic Workflows](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/maintaining-repos.md)
- [Organization Practices](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/organization-practices.mdx)
- [Safe Rollout](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/safe-rollout.md)
- [Sharing Workflows](https://github.com/github/gh-aw/blob/v0.74.3/docs/src/content/docs/practices/sharing-workflows.md)

## Related Skills

- **gh-aw**: To run and manage GitHub Agentic Workflows.
- **github-aw-syntax**: For detailed syntax reference of Agentic Workflows.
