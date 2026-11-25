---
name: dispatching-subagents
description: Use when about to spawn or delegate work to a subagent (Agent/Task tool), choosing a model tier (haiku/sonnet/opus/fable) for a task, writing a delegation prompt, deciding whether something should be delegated at all, deciding whether to dispatch multiple subagents in parallel, verifying a delegated result, or after a delegated task failed twice and needs escalation.
---

> 🌐 [繁體中文（canonical）](https://github.com/tienenwu/fables/blob/main/dispatching-subagents/SKILL.md) · English mirror

# Subagent Dispatch Rules (dispatching-subagents)

Goal: the main conversation's context holds only conclusions and decisions; the execution details are outsourced. Delegation prompt templates are in `references/templates.md`; judgment scenarios are in `references/test-scenarios.md`.

## 0. When NOT to delegate (read this first, to avoid over-delegation)
- A single-point lookup where you already know the exact file and location (e.g. read the value on line N of some config file) → Read it yourself; it's cheaper than dispatching an agent.
- Conversational replies, explaining concepts, changing one or two lines → do it yourself.
- Criterion: **known exact file path or a unique keyword, and the content you expect to read is < 200 lines → do it yourself; needs a search across multiple directories or guessing at naming → delegate.**

## 1. The commander does not take the field
The following work is always dispatched to a subagent; the main conversation only receives conclusions:
- Bulk file reading / repo scanning / "find every place that uses X" → `Explore` agent (read-only, cheapest).
- Web lookups, reading docs, comparing options → `general-purpose` agent (can use WebSearch/WebFetch).
- Batch file edits (the same pattern applied in many places) → `general-purpose` agent.
- Designing an implementation approach → `Plan` agent.
- Code review → `code-reviewer` agent (with `system-architect` for a second, design-level round).

## 1.5 Parallel dispatch (parallelize when you can; serial is the exception)
- **Parallel by default**: 2+ subtasks that are independent of each other (no shared state, no ordering dependency), and are read-only or have non-overlapping write scopes → dispatch them all in one message; don't run one and wait. Typical: multi-directory searches, multi-dimension reviews (one agent for correctness, one for security), research/verification, read-back acceptance.
- **Never parallelize**: tasks that write the same files (conflicts), or where one task's input depends on another's conclusion (parallelism just wastes the run). To parallelize write-tasks, carve out mutually exclusive file scopes first; if you can't, go serial.
- **Batch cap**: ≤ 6 agents per batch. Larger fan-out (dozens) is heavyweight multi-agent orchestration (`Workflow` etc., see §3) and keeps its "only on explicit user request" gate.
- **Failure isolation**: one failed agent in a batch does not block collecting the others' results; handle the failure individually per §5 — don't re-dispatch the whole batch.

## 2. The delegation trio (every delegation prompt must contain these; templates in references/templates.md)
1. **Goal and motivation**: what to do and why (so the agent can judge for itself when it hits a fork).
2. **Acceptance criteria**: a mechanically checkable definition of done (e.g. "compiles and paste the last 5 lines of the gradle output", not "ensure quality").
3. **Report format**: return only conclusions + `file:line`; write long artifacts to a specified path and return the path.

## 3. The actually-available values for model and effort (updated 2026-07-24)
- The `Agent` tool's `model` parameter: `haiku` / `sonnet` / `opus` / `fable`. **Omitting it = inherit the main conversation's model, which is the correct default.**
- **The main loop runs on Opus by default** (the daily driver); `fable` (Fable5) is the most expensive, fastest-burning tier — reserve it for the two `fable`-tagged uses below and nothing else.
- The `Agent` tool **has no effort parameter**; effort is decided by the agent definition's frontmatter or the session's effortLevel.
- The `Workflow` tool (multi-agent orchestration) is not present in every harness; use it only when the user explicitly asks for multi-agent orchestration and the tool actually exists.
- Selection basis (cheapest to most expensive):
  - `haiku`: mechanical batch application (pattern already verified), format conversion, simple grep aggregation.
  - Omit (= same tier as main conversation, Opus by default): general search, implementation, review.
  - `opus`: root-causing hard bugs, judging a non-taste high-difficulty review (the terminus of the stuck-escalation ladder, see §5).
  - `fable`: **two uses only** — (1) taste "judgment calls" (adjudicating UI aesthetics, copy tone); (2) adjudicating an architecture trade-off / decision. Hand it enough context, take one verdict back and execute it; don't leave it in the loop doing hands-on work for long.
- **Hands-on taste polishing** (iterating a UI across many rounds while watching the rendered result) is something a subagent can't do — for that, **manually `/model`-switch the main loop to Fable5**, then switch back to Opus when done. Rule of thumb: **"needs Fable5 watching the rendered result and revising round by round" → switch the main loop; "just need one verdict / pick-one-option" → dispatch a `fable` subagent.**
- For taste/ambiguity questions that still can't be solved: get a second opinion from a different model family (`codex:rescue` etc.) → give the user options and honestly flag low confidence.

## 4. The reporting contract (write this into every delegation prompt)
- Return only: conclusions, key evidence (`file:line`, the tail of test output), and blockers hit.
- Forbidden: pasting whole files back, a play-by-play of the process.
- Artifact over ~50 lines → write it to a file (scratchpad or a specified path), return the path.

## 5. Escalation / de-escalation path
- **haiku fails once** → escalate straight to the main-conversation tier and re-dispatch; do not reason with haiku.
- **A same-tier agent fails the same subtask twice in a row** → escalate to `opus`, and put the **complete failure trace** (what it did, what it output, why that counts as failure) into the new prompt — an escalation without the trace is just swapping the model and guessing again.
- **After the pattern is solved**: write the solution up as explicit steps and de-escalate back to `haiku` to batch-apply it to the remaining locations.
- **Retry ceiling: at most 3 attempts within one model tier; the counter resets to zero when escalating to a new tier.** If the top tier also burns through its 3 → stop, and handle it per judgment.md §3's "when to ask the user".
- **Taste/architecture adjudication does not go through this stuck-escalation ladder**: it's decided by the nature of the task — dispatch a `fable` subagent from the start (see §3), not "escalate only when stuck." This ladder handles hard bugs / execution dead-ends, and its terminus is `opus` + an outside second opinion.

## 5.5 The side-effect boundary of read-only / research tasks (field lesson 2026-07-06)
When dispatching a "research / audit / read-only" task, the prompt must define which verification commands are permitted to run — **"read-only" does not automatically stop the agent from running commands with side effects.**
- ❌ Dispatching "research what could be improved in this project" with no constraints → to verify "the tests pass" the agent runs `npm test`, whose tests write to the production DB, and the research task contaminated the data.
- ✅ The prompt spells out: "read only the source and config; before running tests/build, first confirm whether it writes to production resources, and if unsure, report back and do not run it." To verify "are the tests green", prefer reading the CI record or asking the user, not running them yourself.

## 6. The doer does not verify their own work
**Scope: delegated tasks, and high-risk changes (release paths, deletions, public APIs). For a ≤3-file small fix the main conversation did itself, running compile/tests and pasting the output is enough — no separate acceptance agent needed.**
The one who did the work does not verify their own work. The **initial acceptance** of a delegated task is dispatched to a **fresh-context agent** (freshly opened, given no implementation history, only the acceptance criteria); after a failed round is fixed, the **re-verification** returns to the same verifier agent's continued session, given only the fix diff and the affected acceptance criteria — do not open a new fresh agent every round; it doesn't know what the previous round verified and will reopen old battlegrounds. Fresh is used again only for the final gate before a high-risk close. Re-verification is capped at one round; if it still fails, escalate to the user per judgment.md §3 with the full verification record instead of looping:
- File-type output → read-back: the new agent reads the file and answers "does it contain X, Y, Z".
- Code → run the tests or actually compile/execute, paste the output; if there are no tests, write a minimal reproduction.
- High-risk judgment (architecture, security, whether to delete something) → second opinion: dispatch another agent to review from the opposing stance ("try to overturn this conclusion"), or judge among multiple answers and pick the best.
- The acceptance criteria must include at least one item that "actually executes and pastes the output" — an acceptance list with only existence checks does not qualify.
- If the verification agent says it fails → go back to the implementer (carrying the verification output); do not have the main conversation stamp it approved because it "looks fine by eye".
