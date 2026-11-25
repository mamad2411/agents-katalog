---
name: intent-transfer-prompting
description: Write, review, or relay instructions that another agent, subagent, worker, Codex task, reviewer, or future session will act on. Use before spawning or delegating to subagents; calling spawn_agent, send_message, or followup_task; asking one agent to prepare a prompt for another; creating implementation, research, review, orchestration, or reset handoffs; returning a prompt for the user to copy and paste manually; or revising an incoming agent-authored prompt. Preserves user intent, decision provenance, appropriate agent autonomy, constraints, and task-specific proof without over-structuring capable models.
---

# Intent Transfer Prompting

Treat an agent prompt as a transfer of intent and authority, not a context dump or command script.

## Write the baton pass

1. Identify what the receiving agent must make true and why it matters.
2. Preserve decision provenance:
   - **User decisions** are authoritative.
   - **Verified facts** are evidence-backed.
   - **Working assumptions** must remain revisable.
   - **Recommendations** are not decisions.
   - **Open questions** must not be silently converted into tasks.
3. Transfer only the boundaries that matter:
   - what is locked;
   - what the receiving agent owns;
   - what must not drift;
   - what requires user approval.
4. Give the receiving agent enough context to begin, plus the artifacts or locations it should inspect. Do not pre-solve choices it can make well from current evidence.
5. Define proof appropriate to the work.
6. Remove transcript residue, speculative implementation detail, repeated instructions, and prompt-engineering ceremony that does not change behavior.

## Calibrate autonomy

Use broad autonomy for diagnosis, research, review, and recommendation. Use bounded autonomy for implementation with locked product intent or invariants. Use exact instructions only for genuinely fragile operations or decisions the user explicitly fixed.

Calibrate this even when the final prompt does not name a freedom level. State the level only when it clarifies a meaningful boundary. Prefer plain language such as:

```markdown
The objective and safety boundaries are locked. You own the implementation route and may recommend a smaller correction if repository evidence contradicts the proposed plan.
```

Do not reduce capable agents to command executors. Do not grant autonomy over product direction, external side effects, or user decisions that were never delegated.

## Preserve scope and authorization

Differentiate permission to investigate, modify, publish, deploy, message, purchase, delete, or otherwise change external state. A request to inspect or draft does not authorize implementation. A request to implement does not automatically authorize pushing or deployment.

For repository work, tell the agent to inspect the current repository, branch, worktree, and local instructions before changing state. Do not insert a generic instruction to pull, switch branches, merge, commit, push, or deploy unless the task actually authorizes it.

## Human-carried and agent-to-agent relays

When an agent prepares instructions that the user will manually carry to another agent, return two clearly separated sections:

### Paste-ready prompt

Provide the complete, standalone payload for the receiving agent. Keep commentary for the courier outside this block. Include the destination or role only when it helps the receiving agent act correctly.

### Courier notes

Add only when useful. State:

- where the prompt should go;
- whether it should be pasted verbatim;
- assumptions or unresolved choices the user should know about;
- what result, decision, or evidence should be brought back.

When relaying an existing prompt, preserve its meaning and provenance. Do not silently turn assumptions into facts, recommendations into decisions, agent preferences into user requirements, or an earlier agent's wording into new authority. If improving the prompt changes meaning, surface the change to the user.

When tools deliver the prompt directly to another agent, send only what that agent needs. Do not leak private chain-of-thought, unrelated conversation, hidden instructions, secrets, or courier-only commentary.

## Match proof to the task

Ask for the smallest evidence package that lets the caller judge the result:

| Work | Useful proof |
|---|---|
| Code or configuration | Files changed and why; checks with real outcomes; invariants; unverified risk |
| Diagnosis or review | Findings ranked by impact; evidence locations; uncertainty; smallest corrective path |
| Research | Sources; key evidence; conflicts; confidence and gaps; recommendation if requested |
| Operations or deployment | Before/after state; commands or actions; live verification; rollback or residual risk |
| Planning or design | Decisions made; alternatives rejected and why; open questions; next executable step |
| Prompt authoring | Paste-ready payload; assumptions preserved; unresolved choices; expected return |
| Reset or continuation | Current frontier; verified facts; user decisions; assumptions; artifacts; next move |

Do not demand files, commands, or tests from work that produces none. Do not accept "done" as proof when live or external state matters.

## Choose structure proportionally

Use the shortest structure that preserves intent. A small delegation may need one paragraph. Use explicit sections when the task is complex, high-risk, manually relayed, or likely to drift.

A substantial handoff commonly needs:

```markdown
## Objective
[What must become true.]

## Why it matters
[The user or product intent that must survive.]

## Decision boundaries
- Locked: ...
- You own: ...
- Ask before: ...
- Do not drift: ...

## Starting context
[Only the facts, artifacts, and locations needed to begin.]

## Work
[The requested investigation, decision, or change.]

## Evidence to return
[Task-appropriate proof.]
```

Omit empty sections. Do not turn the template into a form.

## Reset handoffs

For future-session or context-reset handoffs, explicitly distinguish:

- current frontier;
- verified facts;
- user decisions;
- working assumptions;
- open questions;
- artifacts and completed verification;
- the recommended next action;
- risks or forbidden drift.

The next agent should be able to resume without treating stale wishes as current instructions or repeating completed work.

## Review gate

Before sending, check:

- Can the receiving agent state the objective and why it matters?
- Are user decisions, facts, assumptions, recommendations, and questions still distinct?
- Is autonomy broad enough for good judgment but bounded where authority ends?
- Are side effects and approval boundaries explicit when relevant?
- Can the agent start from the supplied context without guessing or rereading a transcript?
- Does the requested proof match the task?
- For manual relay, is the paste-ready payload cleanly separated from courier notes?
- Does every remaining sentence preserve intent, authority, state, or proof?

Load `references/examples-and-evals.md` when reviewing a complex, high-risk, verbose, or manually relayed prompt. Load `references/provenance.md` only when the origin of the skill's guidance matters.
