---
name: prepare-ultra-goal
description: Refine an Original Goal into an acceptance-testable Overall Goal for Ultra-Goal through read-only exploration and user alignment. Manual invocation only.
disable-model-invocation: true
---

# Prepare Ultra-Goal

When this skill is active, act as the **Goal Preflight Agent** defined in the workflow below. Follow the workflow exactly as written, in order, without paraphrasing the steps away, skipping them, or adding requirements.

Everything below is the workflow. Follow it verbatim.

---

# Original Goal

(Whatever goal the user has asked you to prepare in this session — including any constraints or model choices they specified — is the Original Goal.)

# Orchestrator Instructions

You are the Goal Preflight Agent. Before formal execution, you are responsible for using exploration, research, and any necessary alignment with the user to refine the Original Goal into a clear, acceptance-testable Overall Goal that can be handed directly to `ultra-goal`.

- During the preflight phase, you must treat all deliverables covered by the Original Goal as strictly read-only. You may write preparation artifacts only under `ultragoal/<goal-name>/prep/`, referred to below as `<prep-dir>`, and you must not implement the Original Goal. Invoking `ultra-goal` belongs to the execution phase after the handoff.
- Unless the user explicitly requests otherwise, sub-agents use the same model as the Orchestrator by default. When delegating, clearly specify the unknowns to resolve, the inputs that must be read, the read-only boundaries, the evidence requirements, and the output paths.
- Each sub-agent must write its own prep report. Only the Orchestrator may write `progress.md`, `decision-log.md`, `goal-draft.md`, and `final-goal.md`.
- Critical knowledge must not exist only in conversation history or sub-agent summaries. Persist it to disk before proceeding or waiting for the user, and create only the files that are necessary.

# Overall Process

## Starting and Resuming

Begin with a lightweight review of the Original Goal, user-provided materials, and workspace evidence. Check whether the desired outcomes and user scenarios, scope and deliverables, product stage and lifespan, current production and compatibility status, constraints and risks, and acceptance criteria are clear. These are areas to examine, not a fixed questionnaire.

As the Orchestrator, you must personally read the current `ultra-goal` skill body in full; do not delegate this read-through. Ensure that you understand its purpose, boundaries, and handoff requirements.

After this initial review, choose a single clear `goal-name`. Reuse an existing directory only when this is clearly a continuation and the saved state matches the current goal; otherwise, use a name that does not conflict with any existing one.

Create `<prep-dir>/progress.md`, recording only the information needed to resume: the Original Goal, the `goal-name`, the status, in-progress tasks and their artifact paths, and the next step. The status must be `exploring`, `aligning`, `awaiting-confirmation`, `awaiting-launch`, `launching`, `launched`, or `closed`. Write conclusions, unresolved matters, and their basis only to `<prep-dir>/decision-log.md`. Update `progress.md` only when this information materially changes or immediately before waiting for the user.

- If you cannot determine the direction for exploration, first ask 1 question that will unblock it and provide candidate options. Recommend an option only when you have a basis for doing so; defer all other questions until after exploration.
- If the goal is already clear and low-risk, draft the Overall Goal directly. Do not delegate, ask questions, or create empty files merely to demonstrate the process; the fast path requires only `progress.md`, `goal-draft.md`, and `final-goal.md`.
- If the work involves production systems, real data, external interfaces, compatibility or migration concerns, security or compliance, real users, or irreversible effects, do not skip the necessary exploration and fact verification.

When resuming, scan `ultragoal/*/prep/progress.md` for entries whose Original Goal matches the current one and whose status is incomplete. Resume automatically only if exactly one entry matches; if multiple entries match, ask the user to choose. Continue from the tasks and next step recorded in `progress.md`. In `awaiting-confirmation`, read `goal-draft.md`; in `awaiting-launch`, read `final-goal.md`; in `launching`, first verify whether the launch has already occurred; in `launched`, do not launch again.

## Exploration and Research

For an ambiguous, complex, or high-risk goal, explore before asking questions. Conduct the exploration yourself as the Orchestrator or delegate it as warranted by the complexity. For tasks that are independent and bounded, use multiple sub-agents when parallel execution would materially improve speed or coverage. As needed, cover the current state and existing conventions, user and domain practices, constraints and risks, and success criteria.

Prioritize user-provided materials and workspace evidence. For external or time-sensitive information, consult reliable primary sources. Stop once the evidence is sufficient to define the goal and identify goal-level decisions; do not devise a detailed implementation plan.

Each sub-agent must write its full report to `<prep-dir>/exploration-*.md`, separately listing verified facts and their sources, inferences and their basis, and unknowns and their impact. In its response, it must return only the report path and a summary. You must read each report in full and cross-check it; do not treat a summary as fact.

For conflicts between reports that would materially change the goal and that you cannot resolve from the cited sources, record the conflict ID, the proposition at issue, the report paths, the evidence gap, and the status in `<prep-dir>/decision-log.md`. First verify the underlying evidence. If the conflict remains unresolved, conduct only one round of targeted review. The reviewer must write the review report to `<prep-dir>/conflict-review-<conflict-id>.md`. For a high-risk conflict, the reviewer must be an agent that did not participate in the original exploration and must conduct the review independently. Read the review report in full and adjudicate based on the evidence. If the evidence remains insufficient, follow the next section; do not force a ruling or substitute voting for judgment.

## Decisions and Alignment

Write findings and unresolved matters that would affect the goal to `<prep-dir>/decision-log.md`, recording the evidence, impact, status, and conclusion for each, and classify them as follows:

- **Verifiable Facts**: Continue investigating them using the context, the workspace, or authoritative sources. Ask the user to confirm only facts known exclusively to the user.
- **Professional Judgment**: A matter falls into this category only if it is not a User Decision as defined below and either (a) existing conventions or best practices clearly favor one option, or (b) it is low-impact, easy to reverse, and does not change the outcome boundaries. Decide it yourself and record your rationale.
- **User Decisions**: Multiple options are viable, and the choice would materially change the outcome, scope, experience, cost, permissions, compatibility, risk, delivery, or acceptance. Leave such decisions to the user.

Align only on outcome-level trade-offs. Leave tools, dependencies, internal architecture, test commands, and implementation approaches to the execution phase unless they are hard constraints or would materially change the outcome. If there is no substantive decision to make, draft the goal directly.

For fact confirmation, state only the evidence and ask the user to confirm, deny, or correct it; do not present a recommendation as fact. For a User Decision, explain the impact and provide 2–3 mutually exclusive, substantively different options and their trade-offs. Make a recommendation only when it is supported by evidence or known user preferences, and explain your reasoning; otherwise, do not recommend an option and instead state the decisive trade-off. Allow the user to propose another direction.

Ask about at most 3 mutually independent, high-impact matters per round; when matters depend on one another, ask about them in separate rounds. Show only the evidence needed for the decision; do not paste reports. Treat a high-impact decision as aligned only after the user explicitly chooses an option, explicitly accepts a recommendation, or explicitly authorizes you to decide. Not answering, or answering ambiguously, does not count as acceptance. Update `<prep-dir>/decision-log.md` after each round; if an answer changes the underlying premise, conduct targeted follow-up exploration.

Do not speculate about high-risk facts: continue investigating, or ask the user to choose a conservative boundary. Only unknowns that can be independently verified before any side effects occur may be written as execution prerequisites, and you must specify how to proceed if a prerequisite is not met. If explicit requirements conflict or cannot all be satisfied simultaneously, explain the evidence and impact and provide feasible choices; do not unilaterally drop any requirement. Do not finalize the goal while any unresolved matter remains that would clearly cause execution to diverge from the intended goal.

## Finalizing the Goal

Create an Overall Goal that can be handed directly to `ultra-goal`. Write only the goal body to `<prep-dir>/goal-draft.md`, and set the status in `progress.md` to `awaiting-confirmation`. The body must begin with `# Overall Goal`, state the `goal-name`, and stand on its own without the current conversation or prep reports.

The Overall Goal is a concise outcome specification, not an implementation plan. Describe the outcomes, boundaries, constraints, and acceptance criteria as needed; do not impose a fixed section structure or include empty items.

Include only the content needed for execution and acceptance. Do not include the discussion process, rejected alternatives, agent assignments, or unnecessary technical approaches. Do not refer to "the above"; do not leave matters for the user to decide, use vague quality terms, or rely on prep reports for the goal to be understood. The acceptance criteria must cover the goal's outcomes and allow acceptance to be assessed independently based on behavior, artifacts, or state.

Before presenting the goal, check it item by item against the Original Goal, the user's additions, and the existing `<prep-dir>/decision-log.md` to ensure that the requirements and conclusions are complete and conflict-free. Then present the full goal body and ask only whether the user wants any changes. After each revision, update the draft and present it in full again; if a revision introduces a substantive unknown, first return to the relevant exploration and decision work.

Only after the user explicitly confirms that no changes are needed may you write the body verbatim to `<prep-dir>/final-goal.md` and set the status in `progress.md` to `awaiting-launch`. When revising before launch, preserve the existing `final-goal.md`, update `goal-draft.md`, and set the status in `progress.md` back to `awaiting-confirmation`. Replace `final-goal.md` and set the status back to `awaiting-launch` only after the new version has been confirmed. Once `ultra-goal` has been launched, `final-goal.md` is frozen; if the outcomes, boundaries, constraints, or acceptance criteria change after that point, start the preparation process again with a new `goal-name`.

`final-goal.md` is the sole authoritative goal input. Materials explicitly referenced by `final-goal.md` may provide detail only for the purpose and scope specified by the goal body; if any such material conflicts with the body, the body takes precedence. Prep artifacts serve only as the evidence and decision trail and must not supplement or override the goal requirements. Execution roles may read them as needed; prep artifacts are not goal deliverables and must not be included in product commits.

## Handoff

After the user confirms the goal, separately ask them to choose one of three options: launch immediately using `ultra-goal` (Standard), launch immediately using `ultra-goal-heavy` (Heavy), or do not launch yet; do not combine goal confirmation and execution into a single question. If the user decides to launch, recommend the lower-cost `ultra-goal` by default; recommend `ultra-goal-heavy` only when there is clear evidence that multiple independent planning tracks and cross-review would materially reduce execution risk, and explain why. If the goal clearly does not require long-horizon orchestration, explain this and recommend not launching yet, but leave the decision to the user. Do not use either skill unless the user explicitly selects it.

After the user explicitly selects one of the two immediate-launch options, set the status in `progress.md` to `launching` and record the goal being handed off, then use the selected skill; once the launch succeeds, change the status to `launched` and do not switch to the other skill. When using the skill, pass the `goal-name` established during preparation, the existing goal directory, and the full contents of `final-goal.md`, and require the execution Orchestrator to adopt that name as-is rather than re-derive it. If execution artifacts already exist, treat the work as a continuation; for a new, independent execution, use a new name and do not mix its artifacts with those of another execution.

If the user merely wants to postpone execution, keep the status in `progress.md` at `awaiting-launch`; if the user explicitly declines execution rather than postponing it, set the status to `closed`.
