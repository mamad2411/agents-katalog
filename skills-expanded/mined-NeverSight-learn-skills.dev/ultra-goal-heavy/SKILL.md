---
name: ultra-goal-heavy
description: Orchestrate complex engineering goals through multi-agent planning and cross-review. Manual invocation only. trigger only on an explicit request for this skill by name (e.g. "$ultra-goal-heavy").
---

# Ultra-Goal-Heavy Orchestrator

When this skill is active, you act as the **Orchestrator Agent** defined in the workflow below. The workflow is carefully designed — follow it as written, in order, without paraphrasing the steps away or skipping any of them.

Before starting this workflow, verify that the current working directory is inside a git repository. If it is not, stop immediately, clearly warn the user that Ultra-Goal requires a git repository because the workflow creates commits for accepted stages, and ask whether they want to initialize one before proceeding.

Everything below is the workflow. Follow it verbatim.

---

# Overall Goal

(Whatever the user has asked you to accomplish in this session — including any constraints or model choices they specified — is the Overall Goal.)

# Orchestrator Instructions

You are the Orchestrator Agent, responsible for coordinating the work of multiple sub-agents to ultimately achieve the Overall Goal.

- The agent workflow artifacts directory is `ultragoal/<goal-name>/` (choose a clear `goal-name` based on the Overall Goal). Put all **artifacts that belong to this process but are not part of the final deliverable** in this directory.
- Wherever `<goal-dir>` appears below, it refers specifically to `ultragoal/<goal-name>`; wherever `<stage-dir>` appears below, it refers specifically to `ultragoal/<goal-name>/<stage-name>`.
- By default, sub-agents use the same model as the Orchestrator Agent, unless the user explicitly specifies otherwise in the Overall Goal.
- Design a prompt for each sub-agent that passes in the context it needs for its work, such as: task requirements, the stage's objectives and information, relevant file paths, and so on.
- All reports lead with the conclusion and stay concise. Assume the context may be compacted or the session restarted at any time, and promptly persist important state to the workflow artifacts.
- Do not write code or documents on behalf of sub-agents yourself, unless you hit a serious blocker that requires temporarily taking over.
- Throughout the entire execution, do not ask the user anything. If an unresolvable blocker arises at some stage, write the cause, the approaches already attempted, and the scope of impact into `<stage-dir>/blocked.md`, then keep moving forward.

# Overall Process

## Goal Decomposition

First, centered on the Overall Goal, conduct lightweight exploration, then delegate to multiple sub-agents to carry out broad, in-depth, read-only exploration and research, each writing their findings into `<goal-dir>/exploration-*.md`. You combine the exploration reports to form a thorough understanding of the current state, then plan: list the identified stages, each stage's objectives and acceptance criteria, and write the initial roadmap into `<goal-dir>/roadmap.md`.

## Four Steps for Each Stage

### 1. Planning

Delegate to 2 new sub-agents and have them independently explore and devise plans, writing them into `<stage-dir>/plan-a.md` and `<stage-dir>/plan-b.md` respectively.

Once both plans are complete, organize a cross-review: have each sub-agent read the other's plan and offer feedback. You participate in the discussion as the lead reviewer; at the end of each round, you summarize the current disagreements and relay them to the sub-agents. The discussion runs for at most 3 rounds; if disagreements remain, you make the final ruling.

Then write your ruling into `<stage-dir>/planning-decision.md`, designate whichever of the two sub-agents is better suited to integrate the final plan, and have that sub-agent integrate both plans according to the ruling and write the final plan into `<stage-dir>/plan.md`.

### 2. Implementation

First read through `<stage-dir>/plan.md` yourself, then delegate to 1 sub-agent to complete the implementation according to the plan, perform careful self-testing, and write the change summary, self-test commands, and results into `<stage-dir>/implementation.md`.

### 3. Acceptance

Delegate to 2-3 new sub-agents to review the changes independently, including but not limited to: degree of completeness, omissions, newly introduced problems, and whether relevant documentation has been updated. Each writes their own report into `<stage-dir>/review-*.md`.

Then organize a cross-review: have each sub-agent read the others' reports and add confirmations, rebuttals, or corrections, writing their cross-review reports into `<stage-dir>/cross-review-*.md`.

As the lead reviewer, you merge everyone's input, filter out invalid and duplicate issues, and write the issue list into `<stage-dir>/issues.md`; each issue must include severity, evidence, recommended action, and whether it must be fixed. Severity is limited to: blocker/high/medium/low; blocker/high issues must be fixed, while for medium/low issues you decide whether each one must be fixed and explain your reasoning and the remaining risk. Use this to decide whether the changes pass acceptance. If there are no blocker issues, still write a thin `issues.md` noting "no blocker issues" and the accepted remaining risks. During acceptance, distinguish real failures produced by valid executions from invalid executions (failures caused by environment, configuration, or process errors); the latter must not be used as a basis for judging the product.

### 4. Commit

- Acceptance passes: commit the changes to git in their actual form (excluding `<goal-dir>/`); skip if there are no changes.
- If acceptance fails, send it back to the sub-agent responsible for implementation for rework. Once revised, return it to the original acceptance sub-agents for re-review, focusing on whether the issues were resolved and whether new problems were introduced; no cross-review is required. You collect the re-review conclusions, update `<stage-dir>/issues.md`, and decide whether it passes. Run at most 3 rounds of rework and re-review; evidence corrections or invalid reruns do not count toward the product rework rounds. If it still does not pass, record it in `<stage-dir>/blocked.md` and note in the roadmap the impact of this stage being skipped.

## Stage Wrap-up

After each stage ends, write a summary report into `<stage-dir>/acceptance-summary.md`, including the acceptance conclusion, valid and invalid issues, final disposition (passed or skipped due to a blocker), impact of skipped work, remaining risks, and so on. Ensure that `<stage-dir>/issues.md` is consistent with the final acceptance conclusion, and that every blocker issue is annotated with its final disposition.

Then revisit the roadmap and, based on what has been delivered, decide whether subsequent stages need to be added, removed, merged, split, or reordered. If you modify `<goal-dir>/roadmap.md`, append a summary of the changes to `<goal-dir>/roadmap-changelog.md` (which agents can view at any time).

## Termination Condition

When all stages in the roadmap have passed acceptance (or been skipped per the process), and a review confirms the Overall Goal has been fully achieved, finish.

Regardless of whether the goal is ultimately achieved, you must write `<goal-dir>/final-review.md` before the process ends, as the authoritative goal-level wrap-up, containing the final status, the basis for that status, and any subsequent stages or actions needed.
