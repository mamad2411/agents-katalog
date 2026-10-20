---
name: auto-code-reviewer
description: "Review pull requests or pipeline changes using the initiative's configured reviewer mode."
---

# Auto Code Reviewer

This initiative has opted in to **Auto Code Reviewer**. When a review flow is dispatched to your workspace task, inspect the configured review target, evaluate code changes, and produce findings ordered by severity.

## When to run

- A user or hook triggered the Auto Code Reviewer flow for this initiative.
- The run configuration names branches, pull requests, pipelines, or repositories to inspect.
- You have read access to the relevant GitHub repositories and CI metadata through your assigned tools.

## The loop

1. **Resolve the target.** Read the workspace task description and `input_context.optInFlow.runConfig` (or the human-readable run configuration summary). Identify the PR(s), branch(es), or pipeline run(s) to review.
2. **Gather evidence.** Use GitHub tools to load the diff, linked issues, CI status, and any configured pipeline/workflow results. Do not guess at file contents.
3. **Review systematically.** Evaluate correctness, security, performance, test coverage, and maintainability. Prefer concrete line-level references.
4. **Produce findings.** Order items by severity (`critical`, `high`, `medium`, `low`, `nit`). Each finding needs: title, location, impact, and a suggested fix or question.
5. **Summarize residual risks.** Close with what still needs human judgment (merge decision, rollout timing, missing tests).

## Hard rules

- This is a **review** flow unless the user explicitly asked you to push fixes. Do not open PRs or merge by default.
- Respect repository allow-lists and pipeline names from initiative opt-in settings.
- If the target is ambiguous (multiple open PRs, missing branch), ask one clarifying question before reviewing the wrong artifact.
- If GitHub or CI tools are unavailable, stop and report the blocker — do not fabricate findings.
