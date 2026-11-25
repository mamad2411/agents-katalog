---
name: repeatedly-apply-skill
description: "Use when a skill should run as a bounded verification loop across a backlog: define the repeated skill, targets, pass budget, verification method, state update, and explicit stop conditions before iterating."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [iteration, agents, workflow, optimization, verification]
    related_skills: [extreme-software-optimization, profiling-software-performance, code-optimization-agent-skills]
    source: "https://x.com/doodlestein/status/2059715849196564726"
    note: "Clean-room Hermes-compatible implementation from public workflow description."
---

# Repeatedly Apply Skill

## Overview

Use this skill to apply another skill repeatedly in a controlled loop. In the code-optimization setup, this is used to keep applying `extreme-software-optimization` to the critical items uncovered by `profiling-software-performance`.

The point is disciplined iteration, not infinite work. Every pass needs a target, verification, state update, and stop condition.

## Required loop state

Before the first pass, write the loop state in one place:

- **Repeated skill** — exact skill name and why it fits this loop.
- **Backlog** — ordered targets or selection rule for the next target.
- **Pass budget** — maximum passes, time budget, or user-approved stopping point.
- **Verification method** — how each pass proves progress without hand-waving.
- **State update** — where completed, failed, skipped, and newly discovered targets are recorded.
- **Stop condition** — budget exhausted, backlog empty, marginal value flattened, verification unavailable, or user stops the loop.

Use this beyond optimization for repeated reviews, migrations, extraction, cleanup, artifact generation, and issue triage. Do not use it for open-ended improvement where no measurable verification exists.

## When to Use

Use when:

- A workflow naturally decomposes into repeated passes.
- There is a backlog of ranked targets.
- Each pass can be verified independently.
- The user asks to keep applying a skill systematically.

Don't use when:

- The task has no measurable progress signal.
- The skill has side effects that cannot be safely verified.
- The user wants a single pass only.

## Iteration Protocol

1. **Name the skill to repeat**
   - State the exact skill being applied.
   - Load it before beginning the loop.

2. **Define the target backlog**
   - Create a ranked list of targets.
   - For optimization, use profiler-ranked hotspots.
   - Each target should have evidence and an expected outcome.

3. **Set a pass budget**
   - Use a fixed number of passes, a time budget, or explicit completion condition.
   - If the user didn't specify, choose a conservative default and state it.
   - For expensive code work, default to 3 passes unless evidence strongly supports more.

4. **Run one pass at a time**
   - Pick the highest-value remaining target.
   - Apply the repeated skill exactly to that target.
   - Verify the pass according to that skill's checklist.
   - If the pass changes code, perform an adversarial branch review: look for opportunities to reduce layers, remove complexity, increase reliability, maintain repo-wide policies, verify changes, and preserve the original intent.
   - Record results before starting the next pass.

5. **Update state**
   - Mark the target done, reverted, blocked, or deferred.
   - Re-rank remaining targets based on new measurements.
   - Add new targets only if evidence emerges during the pass.

6. **Check stop conditions**
   - Stop when budget is exhausted, targets are done, progress flattens, verification fails, risk grows too high, or the user-requested goal is achieved.

7. **Summarize cumulative results**
   - Report every pass and cumulative impact.
   - Include what was not attempted and why.

## Loop Template

```text
Repeated skill: <skill-name>
Pass budget: <N/time/condition>
Backlog source: <profile/report/user list>

For each pass:
1. Target: <ranked item>
2. Apply <skill-name> to target.
3. Verify according to <skill-name> checklist.
4. Run adversarial review if code changed: reduce layers, remove complexity, increase reliability, maintain repo policies, preserve original intent.
5. Record result: kept/reverted/blocked.
6. Update backlog and metrics.
7. Continue or stop with reason.
```

## Code Optimization Defaults

When repeating `extreme-software-optimization`:

- Backlog source: ranked hotspots from `profiling-software-performance`.
- Default budget: 3 passes if unspecified.
- Required verification per pass: correctness tests plus same benchmark/workload.
- Stop early if a pass fails correctness or the benchmark cannot be reproduced.
- Re-profile after meaningful wins, because the bottleneck may move.

## Common Pitfalls

1. **Looping without a budget.** Always define a stop condition.
2. **Skipping verification between passes.** Bugs compound across iterations.
3. **Not updating the backlog.** The highest-value target can change after each pass.
4. **Combining multiple targets in one pass.** Keep attribution clear.
5. **Continuing after evidence disappears.** Stop when gains are noise.

## Verification Checklist

- [ ] Repeated skill is named and loaded.
- [ ] Backlog is ranked and evidence-based.
- [ ] Pass budget or stop condition is explicit.
- [ ] Each pass has independent verification.
- [ ] Code-changing passes include adversarial review for simplification, reliability, repo policy compliance, and original-intent preservation.
- [ ] State is updated after each pass.
- [ ] Final summary includes cumulative impact and stop reason.
