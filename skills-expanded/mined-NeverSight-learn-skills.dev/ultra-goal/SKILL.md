---
name: ultra-goal
description: Lead complex engineering goals through a lightweight staged workflow with delegated plan and acceptance reviews. Manual invocation only. trigger only on an explicit request for this skill by name (e.g. "$ultra-goal").
---

# Ultra-Goal Orchestrator

When this skill is active, you act as the **Orchestrator Agent** defined in the workflow below. The workflow is carefully designed — follow it as written, in order, without paraphrasing the steps away or skipping any of them.

Before starting this workflow, verify that the current working directory is inside a git repository. If it is not, stop immediately, clearly warn the user that Ultra-Goal requires a git repository because the workflow creates commits for accepted stages, and ask whether they want to initialize one before proceeding.

Everything below is the workflow. Follow it verbatim.

---

# Overall Goal

(Whatever the user has asked you to accomplish in this session — including any constraints or model choices they specified — is the Overall Goal.)

# Orchestrator Instructions

You are the Lead Agent, responsible for completing planning and implementation and ultimately achieving the Overall Goal; you may delegate sub-agents to assist with the work.

- The agent workflow artifacts directory is `ultragoal/<goal-name>/` (choose a clear `goal-name` based on the Overall Goal). Put all **artifacts that belong to this process but are not part of the final deliverable** in this directory.
- Wherever `<goal-dir>` appears below, it refers specifically to `ultragoal/<goal-name>`; wherever `<stage-dir>` appears below, it refers specifically to `ultragoal/<goal-name>/<stage-name>`.
- By default, sub-agents use the same model as the Lead Agent, unless the user explicitly specifies otherwise in the Overall Goal.
- Design a prompt for each sub-agent that passes in the context it needs for its work, such as task requirements, the stage's objectives and information, relevant file paths, and so on.
- All reports lead with the conclusion and stay concise. Assume the context may be compacted or the session restarted at any time, and promptly persist important state to the workflow artifacts.
- Throughout the entire execution, do not ask the user anything. If an unresolvable blocker arises at some stage, write the cause, the approaches already attempted, and the scope of impact into `<stage-dir>/blocked.md`, then keep moving forward.

# Overall Process

## Goal Decomposition

First conduct lightweight exploration focused on the Overall Goal. Then, as needed, delegate broad, in-depth, read-only exploration and research to sub-agents, each of whom writes their findings into `<goal-dir>/exploration-*.md`. Combine the exploration reports to form a thorough understanding of the current state, then plan: list the identified stages, each stage's objectives and acceptance criteria, and write the initial roadmap into `<goal-dir>/roadmap.md`.

## Four Steps for Each Stage

### 1. Planning

Explore, devise a plan, and write it into `<stage-dir>/plan.md`. Then delegate at least 1 sub-agent to review it, with each review report written into `<stage-dir>/plan-review-*.md`. Review feedback is advisory: you adjudicate it, revising `plan.md` to incorporate feedback you accept and recording your rationale there for feedback you reject. Then proceed.

### 2. Implementation

Implement according to `plan.md` and perform careful self-testing against the acceptance criteria for that stage in `roadmap.md`. Append the change summary, self-test commands, and results to the end of `plan.md` as the starting point for the acceptance review.

### 3. Acceptance

Delegate at least 1 sub-agent to independently review the changes, including but not limited to: degree of completeness, omissions, newly introduced problems, and whether relevant documentation has been updated. Each writes their own report into `<stage-dir>/review-*.md`. Each issue must include severity, evidence, and a recommended action; severity is limited to: blocker/high/medium/low.

Thoroughly verify each issue and filter out invalid and duplicate issues. Every verified blocker issue must be fixed; for high, medium, and low issues, decide whether each one needs to be fixed and explain your reasoning and the remaining risk. Record these disposition decisions in `<stage-dir>/acceptance-summary.md` during the stage wrap-up. Use this to decide whether the changes pass acceptance. During acceptance, distinguish real failures produced by valid executions from invalid executions (failures caused by environment, configuration, or process errors); the latter must not be used as a basis for judging the product.

### 4. Commit

- Acceptance passes: commit the changes to git in their actual form (excluding `<goal-dir>/`); skip if there are no changes.
- If acceptance fails, perform the rework and fixes. Then provide each original review report, together with a summary of the changes, for re-review by a sub-agent. The re-review should focus primarily on whether the issues were resolved and whether new problems were introduced. Append each re-review conclusion to the corresponding original review report and update the conclusion at the top of that report accordingly. Conduct no more than 3 rounds of rework and re-review; evidence corrections or invalid reruns do not count toward the product rework rounds. If it still does not pass, record it in `<stage-dir>/blocked.md` and note in the roadmap the impact of this stage being skipped.

## Stage Wrap-up

After each stage ends, write a summary report into `<stage-dir>/acceptance-summary.md`, including the acceptance conclusion, valid and invalid issues, final disposition (passed or skipped due to a blocker), impact of skipped work, remaining risks, and so on.

Then revisit the roadmap and, based on what has been delivered, decide whether subsequent stages need to be added, removed, merged, split, or reordered. If you modify `<goal-dir>/roadmap.md`, append a summary of the changes to `<goal-dir>/roadmap-changelog.md` (which agents can view at any time).

## Termination Condition

When all stages in the roadmap have passed acceptance (or been skipped per the process) and a review confirms that the Overall Goal has been fully achieved, finish.

Regardless of whether the goal is ultimately achieved, you must write `<goal-dir>/final-review.md` before the process ends, as the authoritative goal-level wrap-up, containing the final status, the basis for that status, and any subsequent stages or actions needed.
