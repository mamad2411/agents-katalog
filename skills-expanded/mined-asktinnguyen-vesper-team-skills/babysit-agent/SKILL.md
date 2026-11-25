---
name: babysit-agent
description: Supervise a target Codex agent until its assigned outcome is verified, actively diagnose stalls, relay existing authority, perform safe unblock actions, and resume the same agent after premature blocked or incomplete exits. Use when the user asks to babysit, watch, unblock, shepherd, or keep another agent working, especially for long S2 tasks involving Unreal Editor, computer-use, builds, tests, external waits, or permission-sensitive operations.
---

# S2 Agent Babysitter

## Objective

Keep one target agent progressing until one strict terminal outcome occurs:

- Verify that the assigned objective and applicable proof boundaries are complete.
- Stop because the user cancels or changes the objective.
- Escalate an exact authority, safety, product, or unavailable-tool decision after exhausting safe in-scope alternatives.

Do not treat an agent's `blocked`, `failed`, or `complete` status as authoritative by itself. Inspect its evidence and resume the same agent when required work remains.

## Inputs

Identify:

- Target agent ID or canonical task name.
- Concrete assigned objective and acceptance criteria.
- Exact paths, systems, or external resources it owns.
- Permission envelope granted by the user's current request and prior still-applicable instructions.
- Required proof boundaries from `docs/standards/codex-multi-session-execution.md`.

If the target is omitted, infer it only when exactly one live agent matches the request. Otherwise ask for the target. Do not create a duplicate agent merely because the original is quiet or blocked.

## Authority Contract

Treat babysitting as persistence and coordination, not a permission bypass.

- Preserve all system, user, repository `AGENTS.md`, safety, Git/LFS, Editor, production, and tool restrictions.
- Never reinterpret "fully unblock" as authority to perform destructive or otherwise approval-gated actions.
- Record exact authorization, such as `may restart Unreal Editor once`, instead of vague labels such as `full access`.
- Relay existing authorization to the target with the originating user instruction and its scope.
- Ask the user only for missing authority that materially blocks the next required action.
- Keep the target working on independent tasks while an authorization request is pending.
- Do not encourage repeated refusals, policy evasion, fabricated tool results, or claims that a check ran when it did not.

## Start The Watch

1. Inspect the target and any child-agent state.
2. Read the target's latest messages, claimed progress, changed files, logs, and validation evidence.
3. Restate its remaining objective, current owner boundary, and immediate next evidence-producing action.
4. Send a concise kickoff message that includes the permission envelope and requires the target to report blockers with evidence rather than terminate.
5. Prefer event-driven waiting. Report status changes and occasional heartbeats without duplicating unchanged state.

Use the collaboration controls deliberately:

- Use `send_message` to clarify authority or supply evidence while the target is running.
- Use `followup_task` to resume an idle, blocked, failed, or prematurely completed target.
- Use `interrupt_agent` only when the target is clearly unsafe, wedged, or pursuing invalidated work.
- Use `list_agents` and `wait_agent` to observe state; do not busy-poll or spawn replacement agents as retries.

Use a kickoff message shaped like:

```text
Babysitting is active for <objective>. Your owned paths are <paths>. Existing user authority is <exact permission envelope>. Continue until the acceptance criteria are evidenced. If blocked, report the failed action, exact error, evidence location, safe alternatives tried, and work that can continue; do not terminate merely to request permission.
```

Use a recovery message shaped like:

```text
Resume from <last verified artifact>. <Action/result> is now available under <authority or evidence>. Complete <next acceptance boundary>. Preserve existing work and do not repeat <already completed checks>.
```

## Continuous Unblock Loop

Repeat until a strict terminal outcome:

1. Observe new target output or external state.
2. Compare reported progress with the objective and proof boundaries.
3. Classify every blocker before acting.
4. Perform the smallest safe unblock action available to the babysitter.
5. Send the target the result, evidence location, and exact next step.
6. Resume the same target if it stopped before completion.
7. Verify its next result instead of accepting a status label.

At approximately 15 minutes without new evidence while the lane is runnable, send one structured nudge containing the blocker, last evidence, current owner, and next action. At 30 minutes, narrow the task, remove a false dependency, or reassign ownership only under the repository multi-session standard. At 60 minutes without required proof, mark the affected lane blocked or superseded with an exact wake condition; do not create endless retry lanes.

## Classify And Resolve Blockers

| Blocker | Babysitter action |
| --- | --- |
| Agent overlooked authority already granted | Quote the exact authorization, scope, and next command/action; resume the agent. |
| Babysitter has a required tool that the target lacks | Perform the narrow operation directly, capture evidence, and hand the result back. |
| Preferred tool is unavailable | Try an approved equivalent route such as Unreal MCP, commandlet, CLI, browser control, computer-use, or manual user step, without weakening validation. |
| Agent is waiting on another lane | Verify the dependency, notify it when ready, and keep the target on independent work. |
| Build/test failure | Obtain the real log, classify source versus environment cause, and direct the owning agent to the smallest evidenced fix. |
| Dirty worktree or ownership collision | Preserve user work, identify exact owned paths, and coordinate an atomic ownership transfer if necessary. |
| New user authority is required | Ask one precise authorization question, state the action and risk, and keep unrelated work moving. |
| Higher authority prohibits the action | Do not bypass it. Find a compliant alternative or report the exact irreducible blocker. |
| Agent declares completion without proof | Inspect artifacts and checks, list the missing acceptance evidence, and follow up with the same agent. |

## Unreal Editor And Computer-Use Barriers

Handle these common S2 blockers explicitly:

- Inspect the real Editor/process/MCP state before diagnosing an Editor access problem.
- Launch, stop, restart, or force-close Unreal Editor only when the user explicitly authorizes that operation in the current turn. Invoking this skill alone does not grant that authority.
- When that exact authority exists, relay it to the target. If the target still cannot act but the babysitter can, perform the authorized operation once, verify the resulting state, and resume the target.
- Prefer live Unreal MCP for Blueprint, Behavior Tree, Niagara, Sequencer, and asset inspection or mutation. Use supported commandlets or offline inspection only when permitted and clearly disclose the weaker evidence.
- If computer-use is unavailable to the target, check whether the babysitter can use computer-use, browser control, Unreal MCP, or a supported CLI route. Perform only the narrow required interaction and return screenshots, logs, or saved-state evidence.
- If neither agent can perform the UI interaction, ask the user for one exact manual action and define the wake condition. Keep all non-dependent work active.
- Never claim that an Editor restart, click, save, compile, PIE run, screenshot, or visual check occurred without direct evidence.

## Premature Stop Recovery

When the target halts:

1. Read its final message and identify whether the cause is missing authority, missing tooling, uncertainty, external wait, or actual completion.
2. Check the permission envelope and available babysitter tools.
3. Resolve the blocker directly when safe, or obtain the one missing user decision.
4. Use `followup_task` on the same target with the new evidence and a concrete continuation instruction.
5. Require it to continue from existing artifacts and avoid repeating completed work.

Do not accept generic statements such as "I cannot continue", "computer-use is unavailable", or "Editor permission is missing" without checking the current toolset, current-turn authorization, and compliant alternatives.

## Completion Gate

Before ending babysitting, verify:

- The requested deliverable exists at the correct authority level.
- Applicable source, build/UHT, automation, asset/data, Editor-functional, evaluated-visual, PIE/runtime, and Git proof boundaries are complete or explicitly accepted as skipped.
- Claimed logs, screenshots, assets, diffs, tests, and saved state actually exist.
- No target or recovery lane remains active without useful work.
- Remaining risks and skipped checks are explicit.

Report the target, final state, work completed, unblock actions taken, permissions used or requested, validation evidence, and any residual risk.
