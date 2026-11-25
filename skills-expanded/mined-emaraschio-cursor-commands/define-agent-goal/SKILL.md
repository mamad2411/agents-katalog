---
name: define-agent-goal
description: >-
  Turn a rough task into an agent Goal (outcome, verification with 3 to 5
  success criteria, constraints, boundaries, iteration policy, stopping
  condition, and helper goals when parallel work is implied) so an agent can
  run with minimal babysitting. Plan-only, no execution in the same turn.
  Use for Goal, delegate, run without babysitting, or before long autonomous
  work. Pair with requirement-to-implementation for code delivery afterward.
user-invocable: false
---
# Define agent goal

## Role

You turn a rough task into a **Goal** an AI agent can follow: what done means, how to verify it, what must not break, where the agent may operate, how to retry, when to ask the human, and (when parallelism is implied) what each helper agent must deliver.

This is **human-reviewed autonomy** with a **two-step handshake**: (1) you draft the Goal and wait for Goal approval; (2) you execute only after a later explicit "execute now" (or equivalent). Approving the Goal is not permission to start the task. This skill **defines** the Goal; it does not execute the task in the same turn as delivery or Goal approval.

## When to use

Use when the user wants delegation design before autonomous or long-running agent work: code, ops, inbox cleanup, error backlog triage, or cross-repo chores. For implementing a software requirement after the Goal is approved and the user later says to execute, use `requirement-to-implementation` or a new execution turn.

## User intake template

Offer this block when the user has not supplied structured input. They may paste it back filled in:

```markdown
**Task:** [what you want done]
**Context:** [files, docs, requirements, links, tickets]
**Constraints:** [scope limits, style rules, deadlines, things to avoid]
**Definition of done:** [what success looks like]
```

## Workflow

Run phases in order. Do not publish the final Goal until Phase 3 passes. **Do not execute** the task, edit code, or run destructive commands when delivering the Goal, when the user only approves the Goal, or unless the user explicitly says to skip Goal definition and execute now.

### Phase 0: Intake

1. Extract the **task** from the user message (what they want done).
2. Map any provided fields to **Task**, **Context**, **Constraints**, and **Definition of done** (from freeform text or the intake template above).
3. If the task is missing, ask one focused question before proceeding.
4. Produce a one-paragraph **task summary** restating what the agent would accomplish and for whom.
5. Decide whether the task **implies parallelism** (see below). If yes, plan for **section 7 Helper agent goals** in Phase 2. If no, omit section 7 entirely.

**Parallelism signals** (non-exhaustive): cross-repo or multi-surface work, large audits/inventories, explore-then-implement splits, fan-out across services/layers, or explicit mention of subagents/helpers. When any apply, section 7 is **required**, not optional.

**When not to open section 7:** single-repo or single-surface work that one agent can finish without fan-out; a single clear implementation path with no explore/implement split; the user explicitly wants one agent. Do not invent helpers for polish.

### Phase 1: Discovery

**Fast path:** If the user supplied all four intake fields (**Task**, **Context**, **Constraints**, **Definition of done**) and outcome, verification, boundaries, and stopping condition are unambiguous, **skip** redundant questions. Proceed to Phase 2. Ask only about gaps (for example iteration limits, helper split) or parallelism details.

**Standard path:** Ask structured clarifying questions (use `AskQuestion` when available). Cover only gaps not already answered:

- What must be true when complete (outcome)?
- How will success be verified (tests, metrics, manual checks)?
- What must not regress (constraints)?
- Which files, tools, MCP servers, accounts, or environments are in scope (boundaries)?
- How should the agent retry failed attempts (iteration policy)?
- When should the agent stop and ask the human (stopping condition)?
- If parallelism applies: how to partition work across helpers?

Aim for **4 to 6** non-obvious questions on the standard path. Skip questions the user already answered.

### Phase 2: Draft Goal

Fill the **Goal template** below. Keep the deliverable **one page** (~500 to 900 words): prefer tables and bullets over long prose.

While drafting:

- Default **narrow** boundaries; expand only with user confirmation.
- Do not grant vague autonomy (e.g. "fix everything", "full access"). Keep boundaries narrow.
- Redact secrets, tokens, credentials, PII, and PHI in examples.
- Under **section 2 Verification**, include **3 to 5 success criteria** as checkboxes (scannable, testable). Add commands or observability detail below them.
- When parallelism applies, draft one **mini-goal per helper** in section 7 with **outcome, verification, boundaries, iteration policy, and stopping condition** (inherit parent values when identical; say so explicitly).

### Phase 3: Clarify gate (hard stop)

Before finalizing:

- If outcome, **verification**, or **stopping condition** is ambiguous, **stop** and ask.
- If boundaries are unknown, **stop** and ask.
- If parallelism applies but section 7 is missing, helpers are unnamed, or a mini-goal lacks iteration/stopping, **stop** and ask.
- Do not publish the final Goal with TBD sections unless the user explicitly defers a decision; then return to Phase 1 on the next turn.

### Phase 4: Deliver

1. Post the final Goal in chat using the template headings (sections 1 to 6, plus section 7 when parallelism applies).
2. End with the **two-step approval handshake** (use this wording):

   > **Approve or edit this Goal before I execute.** I will not start until you confirm.
   >
   > After you approve the Goal, say **execute now** (or equivalent) in a later message to begin the work. Goal approval alone is not permission to execute.

3. Include a **copyable intake template** (prefilled from this session where possible) so the user can reuse it for similar tasks.
4. **Save policy:** Always auto-write under `<host-repo-root>/agent-goals/<kebab-slug>.md` without asking.
   - Create `agent-goals/` at the **repository root** (never under `docs/`).
   - Ensure `/agent-goals/` is in the host `.gitignore` before writing; never stage or commit Goals.
   - Host-repo = the repo the Goal's work targets in a multi-root workspace.
   - Do **not** use `docs/agent-goals/` (legacy).
   - Use a kebab-case slug from the goal title (e.g. `reduce-flaky-tests-service-a.md`).
5. Stop after Goal delivery (and the auto-write). Do not start the underlying task until a later explicit **execute now** (or the user explicitly skips Goal definition and orders execution).

## Goal template

Use this structure for the final deliverable:

```markdown
# Agent goal: <short title>

## 1. Outcome
What must be true when complete.

## 2. Verification

### Success criteria
- [ ] <criterion 1 (testable)>
- [ ] <criterion 2>
- [ ] <criterion 3>
<!-- 3 to 5 total; add 4th/5th only when needed -->

### How to verify
Commands, checks, observability, or manual steps that prove the criteria.

## 3. Constraints
What must not regress (behavior, SLOs, data, compliance).

## 4. Boundaries
Files, directories, tools, MCP servers, accounts, environments the agent may use.

## 5. Iteration policy
How to retry (max attempts, order of fixes, when to stop retrying).

## 6. Stopping condition
When to pause and ask the human (blockers, spend limits, ambiguity, production impact).

## 7. Helper agent goals
<!-- Required when the task implies parallelism; omit section entirely when single-agent. -->

### Helper: <name or role>
- **Outcome:** ...
- **Verification:** ...
- **Boundaries:** ... (inherits parent constraints unless narrower)
- **Iteration policy:** ... (or "inherit parent")
- **Stopping condition:** ... (or "inherit parent")

<!-- Repeat per helper. Task/subagent prompts must embed the mini-goal, not just "explore X". -->
```

Populate every required section with concrete content. Use "TBD" only when the user explicitly defers; then do not treat the Goal as final.

## Safety

- Do not execute the task, edit code, or run destructive commands in the same turn as delivering the Goal, or after Goal approval alone, unless the user explicitly says to skip Goal definition and execute now, or later says **execute now**.
- Never imply a native Codex Goals API or product feature; this is a portable Goal document for Cursor agents.
- No secrets, tokens, or PII in the Goal body.
- Always write to `<host-repo-root>/agent-goals/` (gitignored); never `docs/agent-goals/`.

## Distinction from other commands

- **`requirement-to-implementation`**: approved requirement → codebase plan → implement → document. This skill defines **how** an agent may run; RTI **builds** software after a separate approval and a later execute step.
- **`agent-risk-review`**: permission brief for tools/accounts (allowed / forbidden). This skill defines **task** outcome and verification, not IAM policy.
- **`scoped-audit`**: large read-heavy cataloging with verify-before-report. This skill is task-agnostic delegation design, not a repo-wide audit orchestrator.
- **`structure-prompt`**: turns a rough ask into a runnable prompt for another model. This skill defines **delegation boundaries** for an agent run; it also returns a reusable intake template, not a production prompt.

## Guardrails

- **Clarify gate before publish.** Stop at the Clarify gate and ask before finalizing when outcome, verification, stopping, or boundaries are ambiguous.
- **3 to 5 success criteria.** Include 3 to 5 success criteria as scannable, testable checkboxes under Verification.
- **Complete every Goal section with bounded autonomy.** Clarify first, fill all six sections (plus section 7 when parallel), and keep boundaries narrow instead of granting vague autonomy.
- **Require helper goals when work is parallel.** Add one mini-goal per helper with outcome, verification, boundaries, iteration policy, and stopping condition (inherit parent when identical).
- **Do not invent section 7 for single-agent work.** Omit section 7 when work is single-repo or single-surface with no fan-out.
- **Two-step handshake: Goal approval is not execute.** Deliver the Goal and stop; acknowledge approval and wait for a later **execute now** (unless they explicitly skip Goal definition and order execution).
- **Save: always auto-write to root `agent-goals/` (gitignored).** Write `<host-repo-root>/agent-goals/<kebab-slug>.md` with `/agent-goals/` in `.gitignore`; never `docs/agent-goals/`.
- **Do not claim a native Goals product feature.** Present this as a portable Goal document for Cursor agents.
- **Prefer the intake fast path.** Skip redundant discovery and draft the Goal when all four intake fields are present and unambiguous.

## Additional resources

- End-user notes: [reference.md](reference.md)
