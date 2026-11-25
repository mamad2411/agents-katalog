---
name: gpt-6-x-agent-router
description: Use when the user requests GPT-6-series agent routing with GPT-6.2 Sol or GPT-6.2 Astra as parent. Prefer Sol for routine work and Astra for specific difficult problems. Route prescribed Computer Use steps to GPT-6.1 Terra and interactive diagnosis to GPT-6.2 Sol or Astra under the parent's authority.
---

# GPT-6.X Agent Router

## Usage agreement

This skill targets the GPT-6 series and routes only to the subagent configurations listed below. The name does not imply support for every model in that family or for future model families.

Both GPT-6.2 Sol and GPT-6.2 Astra can serve as the parent model. Recommend GPT-6.2 Sol at High for ordinary goals or XHigh for complex goals. This is user setup guidance, not a startup gate.

Start the requested work immediately after invocation:
- Do not query, infer, or verify the parent model or its reasoning effort.
- Do not inspect configuration, session logs, or usage limits to confirm model identity.
- Do not ask the user to confirm their model again or switch the main chat's model.
- The user controls the actual parent model; this skill does not select or guarantee it.

This skill changes the division of work, not the task's authorization. Discussion, planning, and read-only review remain read-only. File changes and external actions retain the current task's authorization requirements.

Apply this routing policy to the remaining stages of the current goal until it is completed or the user changes the requirements.

## Parent responsibilities

Understand the goal, establish constraints, choose how to execute, coordinate dependencies, handle feedback, and deliver the result.

Complete small, straightforward tasks directly when the parent can do so reliably. Route Computer Use execution as described below. Create a general-purpose subagent when independent execution, parallel work, or keeping substantial investigation output out of the main context offers a concrete benefit.

Default to GPT-6.2 Sol for general-purpose subagents regardless of which model is the parent. Do not schedule GPT-6.2 Astra subagents for mandatory opening plans, continuous supervision, or final reviews. Every GPT-6.2 Astra subagent assignment must address a specific unresolved problem.

## Allowed subagent configurations

Explicitly supply both the model and reasoning effort on every spawn. Use only these combinations:

| Configuration | `model` | `reasoning_effort` | Primary use |
| --- | --- | --- | --- |
| GPT-6.2 Sol High | `gpt-6.2-sol` | `high` | Routine engineering work and focused interactive UI diagnosis. |
| GPT-6.2 Sol XHigh | `gpt-6.2-sol` | `xhigh` | Bounded work requiring complex reasoning, including diagnosis across several interacting UI states. |
| GPT-6.2 Astra High | `gpt-6.2-astra` | `high` | Difficult tradeoffs, checking premises or task decomposition, conflicting evidence, or a key problem GPT-6.2 Sol cannot effectively advance. |
| GPT-6.2 Astra XHigh | `gpt-6.2-astra` | `xhigh` | The hardest key problems, including strongly conflicting constraints, difficult root-cause analysis, and deep reasoning about a core design. |
| GPT-6.1 Terra High | `gpt-6.1-terra` | `high` | Prescribed Computer Use steps on simple interfaces. |
| GPT-6.1 Terra XHigh | `gpt-6.1-terra` | `xhigh` | Prescribed Computer Use steps on complex interfaces under the same grant. |

Do not use other models or effort levels, and do not omit parameters in reliance on parent inheritance. The user's latest explicit restrictions on model use take precedence over these defaults.

## Choosing a configuration

For work outside Computer Use, start with GPT-6.2 Sol High unless the task provides a concrete reason for another configuration.

Use GPT-6.2 Sol XHigh for a specific reasoning challenge, such as:
- State transitions, concurrency ordering, transaction consistency, or a complex algorithm.
- Coupled modules where a local change must preserve behavior elsewhere.
- Several plausible causes that must be eliminated using evidence.
- Verification requiring meaningful counterexamples or subtle boundary analysis.

Use GPT-6.2 Astra High when stronger judgment could resolve a specific obstacle, such as:
- The current approach or task decomposition may rely on a false premise.
- Several reasonable approaches require a consequential tradeoff that GPT-6.2 Sol cannot adequately justify.
- Conflicting evidence prevents a reliable conclusion.
- Evidence-based attempts by GPT-6.2 Sol have not advanced a key part of the task.

Use GPT-6.2 Astra XHigh for the most demanding forms of these problems, particularly when constraints conflict and a consequential conclusion is difficult to validate.

Choose an appropriate configuration directly; do not require a fixed escalation sequence. File count, code length, elapsed time, or an ordinary test failure alone does not justify escalation.

Missing permissions, unavailable environments, insufficient information, and unclear user goals need their corresponding remedy. Changing models does not resolve these blockers.

## Computer Use routing

Route each UI assignment by what the operator must decide:

- **GPT-6.1 Terra** is the default for clicks, navigation, known reproduction steps, and checks against an expected result. Use High for simple interfaces and XHigh when observation or navigation is more demanding but the goal and checks are still clear. Terra's assignment stays within the Computer Use skill and its required runtime operations; it can choose local interaction details and report observations.
- **GPT-6.2 Sol** operates the interface when interpreting live evidence and deciding what to inspect next are part of the same investigation. For example, if saving fails and the next check depends on the dialog, application state, and logs, let Sol collect and interpret that evidence as it works. Start at High for a focused diagnosis; use XHigh when several interacting states or plausible causes must be tracked.
- **GPT-6.2 Astra** may operate the interface when the interactive diagnosis itself presents a specific difficult problem, such as contradictory evidence or a hard root-cause judgment. Choose High or XHigh by reasoning difficulty. Assign Astra directly when the evidence warrants it; a Terra or Sol attempt is not required.

The parent may handle interactive diagnosis directly or assign it to a Sol or Astra subagent. If the reasoning can be done from existing screenshots, logs, or Terra's observations, analyze the evidence without taking over the interface. If a scripted check reveals an unexpected result, Terra reports it; the parent switches operators only if choosing the next UI action requires diagnosis.

Before anyone operates the interface, the parent sets the objective, permitted actions and scope, decisions the operator can make independently, and whom to ask when a decision exceeds that grant. Every operator must read and follow the applicable Computer Use skill and runtime instructions, and have access to those tools in the current Codex session. If the tools are unavailable, report the limitation. When authority is missing or unclear, stop the affected action and report the observed state, evidence, and decision needed to the parent or its designated decision-maker. Only the parent may revise the grant within the user's authorization and platform permissions. Neither the model nor XHigh expands that grant.

Keep one active operator for a shared interface. Before switching operators or reasoning effort, have the previous operator stop UI actions and report the current state, completed steps, evidence, and pending decisions. Pass those details and the applicable grant to the replacement, who checks the current state before acting. Do not replay completed actions blindly. A handoff alone does not authorize closing the application or interrupting ongoing tasks.

## Delegating work

Use the native subagent tools available in the current chat. Do not create separate user-owned chats, launch another Codex process, or switch to a paid API to implement delegation.

With the `collaboration` interface:
- Create subagents with `spawn_agent`.
- Explicitly set `model` and `reasoning_effort` to an allowed combination.
- Set `fork_turns: "none"` and provide the necessary context in the task message.
- Continue work with the same configuration through follow-up messages or `followup_task`.
- To change model or effort, create a subagent with the required configuration. Do not claim that the existing agent's configuration has changed.

Give each work package:
- Its objective and expected deliverable.
- User requirements, constraints, and important original wording that must be preserved.
- Relevant files or source locations and established facts.
- Allowed actions and scope, including whether the assignment is read-only or may edit files.
- Dependencies, interface agreements, and acceptance criteria.
- Previous attempts, existing results, and unresolved questions.
- Conditions that require pausing the affected work and reporting to the parent or its designated decision-maker.

Delegate independently verifiable outcomes. Do not mechanically split reading files, changing functions, and running commands into different agents.

Pass necessary context and evidence locations rather than the entire conversation or unrelated logs. Distinguish facts, hypotheses, and unverified conclusions; do not present the parent's assumptions as facts.

## Parallel work and file ownership

Start with one subagent. Add parallel work only when assignments can progress independently. By default, run at most two subagents concurrently, subject to the environment's actual limits.

Assign file ownership for editing tasks. Give a file to only one writer at a time, and sequence changes with dependencies.

Tell subagents to complete their assignment without spawning further agents. Keep additional delegation under the parent's control.

While waiting, the parent may handle independent work that does not conflict with an assignment. Do not duplicate delegated work.

## GPT-6.2 Astra assignments

Give GPT-6.2 Astra the original goal, key constraints, relevant evidence, and the specific difficulty. Explicitly allow it to:
- Identify incorrect premises.
- Challenge the current task decomposition.
- Point out missing constraints or acceptance criteria.
- Recommend reframing the problem.

Do not restrict GPT-6.2 Astra to validating a conclusion the parent already prefers.

As needed, assign GPT-6.2 Astra a design judgment, a focused review, or implementation of a difficult part. Once that problem is resolved, return routine implementation, testing, and documentation to GPT-6.2 Sol.

Request a conclusion with supporting evidence, conditions under which it applies, unresolved uncertainty, and instructions for subsequent execution and verification. Do not retain GPT-6.2 Astra on routine work merely to preserve its context.

## Feedback, escalation, and blockers

Ask subagents to execute, verify, and fix ordinary failures autonomously within their assigned role and authorization instead of seeking permission for each step. A UI operator reports any step outside its grant before acting; Terra reports problems that require diagnosis.

When a premise fails, the scope needs to expand, the evidence cannot support a conclusion, or one evidence-based correction still produces no progress, require a report with:
- The current blocker.
- Established facts and evidence locations.
- Attempted approaches and their results.
- The specific decision or reassignment needed from the parent.

Use that report to gather facts, narrow the task, revise the approach, or select another allowed configuration. Do not repeatedly spawn agents with unchanged input or require a new agent to redo valid completed work.

Tell the user promptly when a known blocker prevents a required outcome. Continue independent authorized work and identify the affected requirement in the final handoff if it remains unmet or unverified.

If the selected model or effort is unsupported, quota is exhausted, or the worker cannot start:
- Do not repeatedly probe or silently substitute a model or effort.
- Briefly report the actual error.
- Continue authorized work that does not depend on the missing result.
- Explain options for blocked work and ask only when a user decision is necessary.

Select models autonomously under these rules. Do not add a confirmation step for every delegation. Existing authorization requirements and platform approvals still apply.

## Verification and delivery

Require proportionate verification from execution subagents and a concise report of:
- Completed outputs and their file or evidence locations.
- Checks actually performed and their results.
- Incomplete, failed, or unverified aspects.
- Anything the parent must address.

Inspect key outputs, scope, interfaces, and verification evidence. For tasks with multiple explicit requirements, check each against the delivered evidence before marking the task complete. Distinguish checks that passed, failed, were skipped, or were inconclusive. Do not routinely repeat the worker's entire investigation or test run.

Add independent review or repeat checks only for a concrete concern, significant risk, or new change. GPT-6.2 Astra is not a mandatory delivery gate.

When expert conclusions conflict with observed results, return the evidence for reconciliation. Do not conceal the disagreement or rewrite conclusions without justification.

Before delivery, ensure relevant execution has finished and clean up temporary validation processes started for this task according to the current project's rules.

Use normal progress updates to explain meaningful assignments briefly. When calling a GPT-6.2 Astra subagent, identify the specific problem it will address without producing a lengthy routing log.

Report results, verification, and remaining limitations. If Computer Use was used, name the operator and any handoff; mention when GPT-6.2 Astra handled a difficult assignment. Do not claim quota savings, cost reductions, or speed improvements without actual measurement.
