---
name: review-agent-production-readiness
description: >-
  Review an OpenAI Agents SDK design, prototype, evaluation system, or deployment plan for production readiness. Assess architecture, tool safety, approvals, failures, evaluations, observability, rollout, cost, privacy, and human control. Do not use this skill as the source for current SDK syntax. Do not use it for systems without agents.
---

# Review Agent Production Readiness

## Workflow

1. Define the review scope. Include the goal, inputs, outputs, tools, state, side effects, approvals, runtime, users, and deployment stage. Review only. Do not implement changes unless the user asks.
2. Inspect the available evidence. Check code, external prompt files, tool schemas, and evaluation results. Check traces, logs, deployment configuration, runbooks, dashboards, and incident notes. Mark unavailable evidence as unknown.
3. Read [the production-readiness checklist](references/production-readiness-checklist.md) and apply only the relevant review areas.
4. Test the architecture against specific harms. Include unsafe actions, incorrect results, privacy exposure, uncontrolled cost, high latency, and failures that operators cannot diagnose or reverse.
5. Separate verified launch blockers from follow-up hardening and personal design preferences. Cite files, lines, traces, or named artifacts when possible.

## Verify Current Information

Use the official OpenAI Agents SDK documentation or the official Agents SDK skill when a conclusion depends on current information. This information includes SDK APIs, model behavior, tracing, sandbox semantics, evaluation configuration, and deployment commands. Record the documentation URL and access date in a full report. Do not use examples in this skill as a source for version-sensitive syntax.

## Output Format

Include only applicable sections. Keep the report proportional to the scope and findings. Start with findings in severity order. Then report architecture suitability, evaluation gaps, operations gaps, and an ordered correction plan. If evidence does not support a launch blocker, state this result. Also identify unknowns.

For a full report, read the [worked readiness review](examples/readiness-review-output.md). For a design-only request, adapt its headings into a tailored pre-launch checklist.
