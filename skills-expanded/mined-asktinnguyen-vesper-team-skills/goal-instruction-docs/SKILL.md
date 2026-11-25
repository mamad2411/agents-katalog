---
name: goal-instruction-docs
description: "Use when creating or reviewing long-running GOAL instructions, /goal prompts, autonomous-agent goals, or goal documents. Routes into creation or review mode and turns objectives into verifiable exit criteria, evidence, environment requirements, tracking, and finalization checks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [goals, autonomous-agents, codex, instructions, documentation, verification]
    related_skills: [writing-plans, test-driven-development, requesting-code-review, systematic-debugging]
---

# GOAL Instruction and Documentation Quality

## Overview

Use this skill to write high-quality GOAL instructions for long-running autonomous agent work, including Codex `/goal`-style tasks and similar goal modes. A GOAL instruction is not just an opening prompt: it is also the agent's **exit criteria**. The instruction should let the agent repeatedly ask, “Has the goal been achieved?” and answer with evidence.

Good GOAL work combines:

- Clear, verifiable completion criteria.
- Practical guidance and starting points.
- Tools or methods for measuring progress.
- A realistic execution environment.
- Tracking artifacts for long runs.
- Cleanup, review, and final reporting requirements.

The supporting document should be short enough to remain usable but complete enough to prevent the agent from wandering, optimizing the wrong thing, or declaring success through a loophole.

## When to Use

- The user asks for a `/goal`, GOAL prompt, long-running agent objective, or autonomous coding milestone.
- A task may run for hours or days and needs durable exit criteria.
- The task involves optimization, migration, test parity, performance, UI implementation, deployment, model/eval work, or multi-step refactoring.
- You need to convert a broad ambition into a concrete goal document.
- You are reviewing whether an existing GOAL instruction is safe, measurable, and complete.

Do **not** use this for tiny one-turn tasks where a normal instruction is enough.

## Choose the mode

- **Creation mode** — the user has an objective but no durable GOAL document yet. Produce a concise goal doc or prompt that an autonomous agent can execute.
- **Review mode** — the user already has a GOAL prompt or document. Audit it for loopholes, missing evidence, unsafe scope, vague completion criteria, and unrealistic environment assumptions.

Minimum operating path for both modes:

1. State the outcome. Done when the objective names the final observable state, not just activity.
2. Define exit criteria. Done when each criterion can be checked by the agent without guessing.
3. Define measurement and evidence. Done when commands, artifacts, screenshots, logs, benchmarks, or review outputs are named.
4. Define environment and constraints. Done when repo paths, credentials, platforms, permissions, and forbidden actions are explicit.
5. Define tracking and finalization. Done when progress artifacts and final handoff requirements are specified.

For long prompts, save the detailed goal as a Markdown document and keep the live `/goal` prompt short: point at the document and summarize the objective.

## Core Principle

A GOAL instruction should answer five questions:

1. **What outcome must exist when done?**
2. **How will the agent prove it is done?**
3. **Where should the agent start, and what should it avoid?**
4. **What environment and tools are needed for realistic progress?**
5. **How should progress and final results be documented?**

## GOAL Instruction Template

```markdown
# GOAL: <short outcome>

## Objective
<One or two sentences describing the concrete outcome.>

## Exit Criteria
The goal is complete only when all of the following are true:
- [ ] <Verifiable criterion with a metric, threshold, artifact, or test.>
- [ ] <Verifiable criterion.>
- [ ] <Regression/safety criterion.>

## Measurement and Evidence
Use the following commands, tools, dashboards, artifacts, or checks to measure progress:
- Baseline: <how to capture the starting point>
- Progress checks: <repeatable checks>
- Final evidence: <what to attach/report at the end>

## Starting Points and Guidance
Start by inspecting:
- <file, subsystem, dashboard, existing issue, benchmark, plan, etc.>

Prefer:
- <known acceptable strategies>

Avoid:
- <known traps, shortcuts, forbidden regressions>

## Environment Requirements
Use an environment that matches the target reality:
- Runtime/configuration: <prod-like flags, database, device, browser, deploy preview, etc.>
- Credentials/access: <if applicable>
- Test data: <representative dataset or allowed generated data>

## Progress Tracking
During the run:
- Commit at meaningful milestones.
- Maintain/update <progress artifact: draft PR, markdown log, HTML dashboard, graph, issue comment, Slack update, etc.>.
- Record failed attempts briefly so they can be cleaned up later.

## Finalization
Before declaring success:
- Run review/checks.
- Remove failed experiments and dead code.
- Summarize attempts, final approach, evidence, tradeoffs, and follow-ups.
```

## 1. Define Clear, Verifiable Criteria

The goal prompt should be concise and centered on completion criteria. Prefer criteria that can be checked objectively.

Good examples:

- “Reduce build and deployment time by **30%** without disabling existing production build steps.”
- “Migrate this feature from TypeScript to Rust and reach **100% test parity**.”
- “Improve application scaffolding so production Largest Contentful Paint is **below 2.5s**.”
- “Increase eval pass rate from the current baseline to **≥90%** while preserving all existing safety tests.”

A number is not always required, but measurable criteria reduce ambiguity. If the goal is qualitative, replace the number with a checklist, spec, rubric, or acceptance test.

### If the Goal Is Not Ready

Do not force a vague goal into goal mode. First ask the agent to brainstorm or plan:

- “Research the system and propose 3 possible GOAL definitions with measurable exit criteria.”
- “Create a plan file that lists implementation options, risks, and recommended metrics. After I approve it, set the GOAL based on that plan.”

A goal can be edited later, but a poor initial goal can waste many autonomous turns.

## 2. Provide Guidance When Possible

A goal like “Reduce build time by 30%” may work, but it can send the agent on a wild goose chase. Give useful starting points without over-constraining the solution.

Include:

- Suspected bottlenecks or relevant files.
- Known tools the agent may use.
- Acceptable constraints or limitations.
- Prior investigations, plans, issues, dashboards, or logs.
- Areas that are out of scope.

Example:

```markdown
Start by profiling `packages/web` production builds. We suspect most time is spent in image optimization and route generation. Use the existing CI timing logs and local `pnpm build --profile`. Do not remove production checks or skip route generation just to improve the metric.
```

If useful, have the agent first work in planning/research mode and write a plan artifact; then reference that plan in the GOAL.

## 3. Make Progress Measurable

The agent needs a way to know whether it is getting closer. For optimization tasks, this may be obvious: benchmark time, test coverage, latency, memory, bundle size, eval score, or pass rate. For other tasks, define or create measurement tools.

Useful measurement tools include:

- Benchmarks and profiling scripts.
- Test suites and coverage reports.
- Deployment logs and timing dashboards.
- Visual diff scripts for UI work.
- Screenshot comparison tools.
- Eval suites for agents/models.
- Golden fixtures or snapshot tests.
- Accessibility, performance, or security scanners.

Add guardrail checks so the agent does not satisfy the main metric by cheating:

- Do not reduce test coverage to reach 100% pass rate.
- Do not crop and inline a design image to appear pixel-perfect.
- Do not disable production build paths to reduce deployment time.
- Do not remove features, validations, logging, or safety checks unless explicitly approved.

## 4. Create a Realistic Environment

For the goal to be meaningful, the agent must operate in an environment close to the real target.

Examples:

- Deployment-time work should use preview or production-like deployments with the same build flags and relevant paths enabled.
- Latency work should use representative data, similar database shape, and realistic configuration.
- Browser UI work should run in an actual browser with console checks, screenshots, and relevant viewport/device coverage.
- Mobile performance work should use a simulator or physical device when that materially changes the result.
- ML/model/eval work should use representative datasets or clearly documented generated substitutes.

If the realistic environment is unavailable, state the limitation explicitly and define what evidence is acceptable until the environment is available.

## 5. Be Careful With Visual Goals

“Implement this UI 100% pixel perfect from this image” is tempting but risky. Visual targets can cause the agent to rabbit-hole on irrelevant details or use shortcuts.

For visual work:

- Treat images as context, not the only exit criteria.
- Break the result into component requirements, layout rules, states, responsiveness, accessibility, and design-system adherence.
- Provide or allow visual comparison tools, but do not rely only on raw screenshots.
- State which details matter and which approximations are acceptable.
- Explicitly forbid shortcuts such as inlining/cropping the reference image.

Better:

```markdown
Implement the settings page to match the reference's layout, spacing, typography hierarchy, and interactive states using the existing design system. Completion requires the checklist in `docs/settings-ui-spec.md`, no console errors, responsive behavior at 390px/768px/1440px, and screenshot diffs reviewed for major layout differences. Do not inline or crop the reference image.
```

## 6. Track Progress During Long Runs

For goals that run for hours or days, require progress artifacts so humans can regain context.

Options:

- Commit at meaningful milestones.
- Push a draft PR early, especially when preview deployments are useful.
- Maintain a markdown progress log with timestamps, baseline, experiments, results, and next steps.
- Maintain an HTML or dashboard artifact for executives or stakeholders.
- Render and update graphs that track benchmark/eval progress.
- Post major progress updates to Slack, issues, PR comments, or another agreed channel.
- Use a side chat/status query to inspect current state without derailing the main goal thread.

Progress tracking should be lightweight. The point is recoverability, not bureaucracy.

## 7. Clean Up and Finalize Results

When the goal appears achieved, the agent should not immediately hand off raw changes. Long-running goals often accumulate failed experiments, temporary tools, and partial approaches.

Require finalization:

1. Run a local review or code review pass.
2. Remove dead code, abandoned experiments, debug logs, and temporary scaffolding unless intentionally retained.
3. Re-run the final measurement and regression checks.
4. Compare final results against the baseline.
5. Summarize:
   - final outcome,
   - evidence,
   - important attempts that failed,
   - why the final approach worked,
   - residual risks,
   - follow-up recommendations.

## Quality Rubric

A strong GOAL instruction is:

- **Verifiable:** success can be checked by tests, metrics, artifacts, or reviewable criteria.
- **Scoped:** it says what is in and out of scope.
- **Guided:** it gives starting points and known constraints.
- **Measurable:** it defines baseline, progress checks, and final evidence.
- **Realistic:** it uses an environment that reflects the real target.
- **Resilient:** it includes guardrails against metric gaming and regressions.
- **Inspectable:** it produces progress artifacts for long runs.
- **Clean:** it requires review and cleanup before completion.

## Common Pitfalls

1. **Using a vague outcome as the exit criterion.** “Make it faster” is weaker than “reduce p95 API latency from baseline by 25% on representative data without increasing error rate.”
2. **Making the goal too long.** Put detailed context in a linked plan/spec; keep the GOAL itself focused on exit criteria and required guidance.
3. **No baseline.** Without a starting measurement, improvement claims are weak.
4. **No measurement tool.** If the agent cannot measure progress, it may loop or guess.
5. **Unrealistic environment.** Local-only evidence may not prove production improvement.
6. **Visual rabbit holes.** Pixel-perfect image goals can waste tokens and encourage bad shortcuts unless broken into specs and checks.
7. **Metric gaming.** The agent may satisfy the stated number by reducing coverage, disabling work, or removing functionality unless guardrails are explicit.
8. **No progress artifact.** Long runs become hard to audit if the agent only reports at the end.
9. **No cleanup phase.** Failed experiments may remain in the final diff.

## Implementation GOAL documents

When the user wants to use `/goal` but the instruction is long, create a standalone `*_GOAL.md` next to the implementation plan/spec and make the chat prompt a short pointer to it. See `references/implementation-goal-doc-pattern.md` for a reusable structure, including hard scope boundaries, pre-code inventory/contract requirements, and strict post-implementation review gates such as `$thermo-nuclear-code-quality-review`.

When the user asks to save proposed phases, resolve open questions, and then produce a concise `/goal` prompt, use `references/open-questions-review-for-goal-plans.md`: propose recommendations first, send them to a critique subagent with plan/spec context, append the synthesized decisions/evidence/gates to the durable plan, and store the concise `/goal` prompt in the plan itself.

## Verification Checklist

Before using or approving a GOAL instruction, confirm:

- [ ] The objective is concrete and concise.
- [ ] Exit criteria are explicit and verifiable.
- [ ] At least one criterion includes a number, threshold, checklist, test, or artifact.
- [ ] The baseline and final evidence are defined.
- [ ] The agent has tools or permission to create tools for measuring progress.
- [ ] Starting points and known constraints are included.
- [ ] Guardrails prevent obvious metric gaming or shortcuts.
- [ ] The execution environment is realistic or limitations are documented.
- [ ] Visual goals are decomposed into specs/checklists instead of relying only on an image.
- [ ] Long-running work has progress tracking instructions.
- [ ] Final cleanup, review, and summary are required.

## Source

Extracted and adapted from Dominik Kundel's X article, “A guide to /goal” (June 5, 2026): https://x.com/dkundel/status/2062650378089594955
