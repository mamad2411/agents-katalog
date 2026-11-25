---
name: feature-dev
description: Guides end-to-end feature implementation — explores the codebase, resolves ambiguities via clarifying questions, compares architecture approaches, then implements and reviews the result. Use when adding a new feature, implementing a user story, building a new endpoint, or planning how to build something in an existing codebase. Do not use for bug fixes, refactoring existing code, quick one-off edits, or tasks that only need a spec or plan without implementation.
---

# Feature Development

## Core Principles

- **Ask clarifying questions**: Identify ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions. Wait for answers before proceeding. Ask early — after codebase exploration, before architecture design.
- **Read files identified by agents**: Ask agents to return 5–10 key files to read. After agents complete, read those files to build deep context before proceeding.
- **Use TodoWrite**: Track all progress throughout

---

## Phase 1: Discovery

Initial request: $ARGUMENTS

**Actions**:
1. Create todo list with all phases
2. If feature unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user

---

## Phase 2: Codebase Exploration

**Actions**:
1. Launch 2-3 code-explorer agents in parallel, each targeting a different aspect (similar features, overall architecture, UI/testing patterns). Ask each agent to return 5-10 key files to read.
    ```
    runSubagent({
       agentName: "code-explorer",
       description: "Explore similar features",
       prompt: "Find features similar to [feature] in this codebase. Trace through their implementation and return 5-10 key files to read."
    })
    ```
    See more prompt variants in [references/agent-prompts.md](references/agent-prompts.md).
2. Read all files identified by agents to build deep understanding
3. Present comprehensive summary of findings and patterns discovered

---

## Phase 3: Clarifying Questions

**Actions**:
1. Review the codebase findings and original feature request
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs
3. **Present all questions to the user in a clear, organized list** using this format:
   ```
   1. [Scope] Should this feature support X, or only Y?
   2. [Integration] Does this need to integrate with the existing Z module, or be standalone?
   3. [Error handling] What should happen when A fails — silent fallback or explicit error?
   4. [Auth] Should this endpoint require authentication?
   ```
4. **Wait for answers before proceeding to architecture design**

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.

---

## Phase 4: Architecture Design

**Actions**:
1. Launch 2-3 code-architect agents in parallel with different focuses: minimal changes, clean architecture, pragmatic balance.
   ```
   runSubagent({
     agentName: "code-architect",
     description: "Design pragmatic approach",
     prompt: "Design a pragmatic implementation of [feature] in this codebase. Reuse existing patterns where natural, introduce new abstractions only when they clearly improve clarity, and list the files to create or modify."
   })
   ```
   See more prompt variants in [references/agent-prompts.md](references/agent-prompts.md).
2. Review all approaches and form your opinion on which fits best (consider: scope size, urgency, complexity, team context)
3. Present to user using this format:
   ```
   | | Option A — Minimal | Option B — Clean | Option C — Pragmatic |
   |---|---|---|---|
   | Files changed | 1 existing file | 3 new files | 2 files (1 new) |
   | Reuses existing | Yes | No | Partially |
   | Risk | Low | Medium | Low |
   | Maintainability | Medium | High | High |

   Recommendation: Option C because [reasoning].
   ```
4. **Ask user which approach they prefer**

---

## Phase 5: Implementation

**Actions**:
1. Wait for explicit user approval before starting
2. Read all relevant files identified in previous phases
3. Implement following chosen architecture
4. Update todos as you progress

---

## Phase 6: Quality Review

**Actions**:
1. Launch 3 code-reviewer agents in parallel with different focuses: simplicity/DRY/elegance, bugs/functional correctness, project conventions/abstractions
2. Consolidate findings and identify highest severity issues that you recommend fixing
3. **Present findings to user and ask what they want to do** (fix now, fix later, or proceed as-is)
4. Address issues based on user decision

---

## Phase 7: Summary

**Actions**:
1. Mark all todos complete
2. Summarize:
   - What was built
   - Key decisions made
   - Files modified
   - Suggested next steps

---
