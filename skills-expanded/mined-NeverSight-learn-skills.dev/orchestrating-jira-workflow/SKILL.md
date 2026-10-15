---
name: "orchestrating-jira-workflow"
description: 'Top-level orchestrator for end-to-end Jira ticket workflows. Use this skill when the user says "work on ticket PROJECT-1234", "start the Jira workflow", "handle this ticket end to end", "orchestrate PROJECT-1234", "pick up PROJECT-1234", or provides a Jira ticket key/URL without specifying a particular phase. Also trigger on "resume ticket PROJECT-1234", "where did we leave off on PROJECT-1234", "continue PROJECT-1234", or "what''s the status of PROJECT-1234". This skill coordinates all downstream skills and subagents — it never runs tool calls, CLI commands, file reads, web searches, or MCP calls directly.'
---

# Orchestrating Jira Workflow

## Purpose

Coordinate the complete lifecycle of a Jira ticket through five sequential
phases. This skill is a **pure coordinator** — it dispatches to subagents and
downstream skills, operates only on concise summaries, and never does heavy
lifting directly.

## Why This Matters

The orchestrator's context window is the most expensive resource in the system.
Every byte of raw file content, git diff, API response, or command output that
leaks into it degrades decision-making for every subsequent step. That is why
delegation is not optional — it is the architecture.

## Inputs

| Input        | Source              | Required | Example                                                     |
| ------------ | ------------------- | -------- | ----------------------------------------------------------- |
| `TICKET_KEY` | User / `$ARGUMENTS` | Yes      | `JNS-6065`                                                  |
| `JIRA_URL`   | User (optional)     | No       | `https://vukaheavyindustries.atlassian.net/browse/JNS-6065` |

Extract the ticket key from a full URL if the user provides one.

## Pipeline

```
Phase 1: Fetch           →  docs/<KEY>.md
Phase 2: Plan            →  docs/<KEY>-tasks.md
Phase 3: Clarify         →  docs/<KEY>-tasks.md (updated with decisions)
Phase 4: Create subtasks →  Jira subtasks created + plan updated with keys
Phase 5: Execute         →  Code changes, one task at a time
```

## Subagent Registry

Utility subagents handle all tool calls, file reads, and command execution.
Dispatch to these instead of doing anything directly.

| Subagent                | Path                                   | Purpose                                                                               |
| ----------------------- | -------------------------------------- | ------------------------------------------------------------------------------------- |
| `artifact-validator`    | `./subagents/artifact-validator.md`    | Check whether phase artifacts exist and are well-formed; return pass/fail summary     |
| `progress-tracker`      | `./subagents/progress-tracker.md`      | Read, create, or update the progress file; return current workflow state              |
| `ticket-status-checker` | `./subagents/ticket-status-checker.md` | Query Jira for current status, assignee, and recent activity on a ticket              |
| `codebase-inspector`    | `./subagents/codebase-inspector.md`    | Report working tree state: branch, uncommitted changes, recent commits                |
| `code-reference-finder` | `./subagents/code-reference-finder.md` | Search the codebase for symbols, patterns, or file references; return concise matches |
| `documentation-finder`  | `./subagents/documentation-finder.md`  | Locate relevant docs, READMEs, or wiki pages for a topic; return summaries            |
| `git-operator`          | `./subagents/git-operator.md`          | Execute git operations: branch, push, stash, checkout, merge, rebase, and commit work |

### How to Dispatch

Subagent `.md` files are co-located reference documents. To dispatch:

1. Read the subagent's `.md` file from the path in the registry above.
2. Spawn a subagent using the **Task tool**, passing the `.md` content as the
   prompt and the step's inputs as the user message.

   All three supported platforms use the same Task tool pattern:

   | Platform        | Dispatch method                                                                          |
   | --------------- | ---------------------------------------------------------------------------------------- |
   | Claude Code CLI | `Task(prompt=<.md content>, description=<step summary>)`                                 |
   | Cursor IDE      | `Task(subagent_type="general-purpose", prompt=<.md content + inputs>)`                   |
   | OpenCode CLI    | `Task(prompt=<.md content>, description=<step summary>)` — same semantics as Claude Code |

   On Cursor: use `subagent_type="general-purpose"` and embed the `.md` content
   directly in the prompt. This is more reliable than defining custom named
   agents, which have known dispatch issues with the Task tool.

3. Collect the returned summary. Use that summary — not raw output — for all
   downstream decisions.

Subagents run sequentially by default. Parallel dispatch is acceptable only for
independent utility calls (e.g., `codebase-inspector` + `documentation-finder`
before a task), never for dependent operations.

## Downstream Skills (Phase Handlers)

Each phase is handled by a dedicated skill. Read its SKILL.md only when
invoking it.

| Phase | Skill                  | Skill Path (relative to skills root) | Purpose                                           |
| ----- | ---------------------- | ------------------------------------ | ------------------------------------------------- |
| 1     | fetching-jira-ticket   | `../fetching-jira-ticket/SKILL.md`   | Retrieve all ticket data into a Markdown snapshot |
| 2     | planning-jira-tasks    | `../planning-jira-tasks/SKILL.md`    | Decompose ticket into a prioritized task plan     |
| 3     | clarifying-assumptions | `../clarifying-assumptions/SKILL.md` | Walk user through open questions and assumptions  |
| 4     | creating-jira-subtasks | `../creating-jira-subtasks/SKILL.md` | Push planned tasks to Jira as subtasks            |
| 5     | executing-subtask      | `../executing-subtask/SKILL.md`      | Execute one task at a time from the plan          |

## Data Contracts

Each phase produces an artifact that the next phase consumes. Always validate
via `artifact-validator` before advancing.

| Transition | Artifact                          | Validation                                    |
| ---------- | --------------------------------- | --------------------------------------------- |
| 1 → 2      | `docs/<KEY>.md`                   | File exists, has `## Description` section     |
| 2 → 3      | `docs/<KEY>-tasks.md`             | File exists, has `## Tasks` section, ≥2 tasks |
| 3 → 4      | `docs/<KEY>-tasks.md` (updated)   | File has `## Decisions Log` section           |
| 4 → 5      | `docs/<KEY>-tasks.md` (with keys) | File has `## Jira Subtasks` table with keys   |

## Execution

### 1. Determine Starting Phase

Dispatch `progress-tracker` with action `read` and the `TICKET_KEY`.

| Progress indicates…                   | Resume from |
| ------------------------------------- | ----------- |
| No artifacts found                    | Phase 1     |
| Phase 1 complete, Phase 2 not started | Phase 2     |
| Phases 1–2 complete, Phase 3 not done | Phase 3     |
| Phases 1–3 complete, Phase 4 not done | Phase 4     |
| Phases 1–4 complete, tasks remaining  | Phase 5     |

Tell the user what was found and which phase will start. If resuming past
Phase 1, ask for confirmation before proceeding.

### 2. Execute Phases Sequentially

For each phase, follow this cycle:

**a. Announce**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase <N>/5 — <Phase name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**b. Validate preconditions** — dispatch `artifact-validator`. Proceed only on
pass.

**c. Invoke the downstream skill** — read its SKILL.md and follow its contract.
Pass inputs explicitly: file paths, ticket key, and any context summaries from
subagents. Never rely on conversation history for critical data.

**d. Validate output** — dispatch `artifact-validator` to confirm the phase
artifact was produced correctly.

**e. Update progress** — dispatch `progress-tracker` with the phase number,
status, and a one-line outcome summary.

**f. Gate before advancing**

| Transition | Gate                                                                             |
| ---------- | -------------------------------------------------------------------------------- |
| 1 → 2      | Automatic                                                                        |
| 2 → 3      | Automatic                                                                        |
| 3 → 4      | User confirmation required — this creates Jira subtasks (external system writes) |
| 4 → 5      | User chooses which task to execute first — never auto-start execution            |
| Within 5   | After each task, user chooses next — never auto-continue                         |

For the Phase 3 → 4 gate, offer:

- "Create subtasks now"
- "Review the plan first"
- "Stop here — I'll create subtasks manually"

### 3. Phase 5 — Execution Loop

Phase 5 runs once per task, not once for the whole plan. Each iteration:

1. Dispatch `progress-tracker` → get remaining tasks.
2. Present remaining tasks to the user.
3. User selects the next task.
4. **Pre-task context** — dispatch relevant utility subagents:

   | Situation                        | Dispatch to             |
   | -------------------------------- | ----------------------- |
   | Need current ticket status       | `ticket-status-checker` |
   | Need working tree / branch state | `codebase-inspector`    |
   | Need to find relevant code       | `code-reference-finder` |
   | Need docs or config context      | `documentation-finder`  |
   | Need a feature branch            | `git-operator`          |

5. Invoke `executing-subtask`, passing context summaries from step 4 as
   explicit inputs.
6. After the task completes, dispatch `git-operator` with operation
   `commit-work` (and `GUIDANCE` summarizing what changed and why). The
   git-operator delegates to the `/commit-work` skill for atomic commits.
7. Dispatch `progress-tracker` to mark the task complete.
8. Return to step 1.

Continue until all tasks are complete or the user stops.

### 4. Final Summary

When all tasks are complete (or the user stops), dispatch `progress-tracker`
for the final state, then present:

```markdown
## Workflow Summary — <TICKET_KEY>

| Phase | Status      | Key outcome                 |
| ----- | ----------- | --------------------------- |
| 1     | ✅ Complete | Ticket fetched (N comments) |
| 2     | ✅ Complete | N tasks planned             |
| 3     | ✅ Complete | N/N questions resolved      |
| 4     | ✅ Complete | N subtasks created in Jira  |
| 5     | ✅ Complete | N/N tasks executed          |

All artifacts are in docs/<TICKET_KEY>\*.
```

## Error Handling

| Error type               | Response                                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Skill failure**        | Record via `progress-tracker`. Report to user: retry, skip, or abort.                                          |
| **Missing artifact**     | `artifact-validator` reports failure → do NOT proceed. Tell user which phase needs to run/re-run and offer it. |
| **Jira MCP unavailable** | Tell user to connect it. Offer to resume when ready.                                                           |
| **Subagent failure**     | Non-critical (e.g., `documentation-finder`): proceed without. Critical (e.g., `artifact-validator`): halt.     |
| **User interruption**    | Progress file ensures resumability. Tell user: "Say 'resume ticket <KEY>' to pick up where we left off."       |

## Orchestration Rules

These protect the context window and keep coordination reliable:

1. **Delegate everything.** Never run tool calls, bash commands, file
   reads/writes, web searches, or MCP calls directly. If you're about to run a
   command, stop — find the right subagent. Raw output in the orchestrator is
   context pollution.

2. **Verify via subagent.** Always use `artifact-validator` to check artifacts.
   Reading files "to quickly check" is how context pollution starts.

3. **One phase at a time.** Phase dependencies are strict. Partial artifacts
   cause cascading failures.

4. **Explicit handoffs.** Pass file paths, ticket keys, and context summaries
   explicitly to every dispatch. Subagents cannot see conversation history.

5. **Gate destructive actions.** Any phase modifying external systems (Jira
   writes, git push) requires explicit user confirmation.

6. **Maintain resumability.** Update `progress-tracker` after every phase and
   task. The workflow can be interrupted and resumed without loss.
