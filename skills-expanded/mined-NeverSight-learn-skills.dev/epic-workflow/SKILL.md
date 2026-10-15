---
name: epic-workflow
description: End-to-end Epic planning — grill requirements, write a PRD, decompose into GitHub issues with dependencies, and create a feature branch for autonomous implementation. Use when starting a new epic, planning a large feature, or when user says "epic workflow", "plan this feature", or "start a new epic".
metadata:
  author: CosticaPuntaru
  version: '2.2'
---

# Epic Workflow Skill

This skill guides the agent through an end-to-end process for planning large features (Epics) and generating their respective GitHub issues. It follows a strict **Requirement Drill ➔ Documentation ➔ Decomposition** pipeline.

## When to use

- When starting a new feature (Epic) that requires research and multi-issue planning.
- Specifically triggers when the user says "start a new epic", "plan this feature", or mentions "epic workflow".

## Context Management (Checkpointing)

Long-running workflows like Epics can exceed the model's context window. To maintain efficiency and accuracy:

1. **Phase Checkpointing**: After EVERY phase, summarize the findings into a dedicated Epic directory: `.agents/epics/<epic-name>/context/`. 
   - After `/grill-me`: Save to `grill-summary.md`.
   - After research: Save to `research-notes.md`.
2. **"Stateless" Resumption**: If the session gets too long, instruct the user that you are "checkpointing". Next time you start, simply `view_file` on these summaries instead of re-processing the entire chat history.
3. **Artifact-as-Truth**: Treat the generated files (PRD, Plan, Tasks) as the persistent source of truth. Read the latest file version from disk rather than relying on previous chat messages.

## Steps

### Phase 0: Epic Initialization
1. **Naming**: Propose a kebab-case name for the Epic (e.g., `team-billing-dashboard`).
2. **Discovery (Autonomous)**: Use `improve-codebase-architecture` and `codebase-cleanup-tech-debt` to map the playing field. Answer your own technical questions by reading the codebase before asking the user.

### Phase 1: Requirement Drilling (The "Grill")
3. **Initialize the Grill**
   - **Command**: `/grill-me`
   - **Goal**: Resolving all conceptual ambiguity and design tree branches before drafting.
4. **Checkpoint Findings**
   - **Action**: Save all resolved branches and user decisions to `.agents/epics/<name>/context/grill-summary.md`.

### Phase 2: Domain Alignment
5.  **Establish Ubiquitous Language**
    - **Skill**: `ubiquitous-language`.
    - **Goal**: Define canonical terms in `UBIQUITOUS_LANGUAGE.md`.

### Phase 3: Formalizing the PRD
6.  **Draft the PRD**
    - **Command**: `/write-a-prd`
    - **REQUIRED TEMPLATE**: `resources/prd.md`
    - **User Presentation & Review**: After drafting, **PRESENT the PRD content in full to the user**. Explicitly ask for their review and if they would like to make any edits before it is pushed to GitHub. Do NOT proceed to Phase 4 until the user has confirmed they are happy with the PRD.
    - **Guardrail (Recursive Grill)**: If the agent encounters a significant unresolved dependency or technical gap during drafting, they **MUST re-trigger a mini-grill** focused on that specific gap before proceeding.

### Phase 4: Planning & Decomposition
7.  **Phase-Level Planning**: Use `prd-to-plan`.
8.  **Issue Decomposition**: Use `prd-to-issues`.

### Phase 5: GitHub Issue Creation (Synchronous)
9.  **Create the Parent Epic (PRD Issue)**
    - **Pre-flight Check**: Ensure the user has approved the final PRD from Phase 3.
    - **Tool**: `gh issue create --title "PRD: <epic-title>" --body "$(cat prd.md)" --label "prd,enhancement"`.
    - **BLOCKING ACTION**: You MUST capture the resulting **Issue Number** (e.g., `#123`). This number is required for everything below.

10. **Create the Epic Feature Branch**
    - **IMMEDIATELY** after capturing the PRD issue number, create and push the feature branch:
      ```bash
      git checkout main && git pull origin main
      git checkout -b epic/123-<epic-name>
      git push -u origin epic/123-<epic-name>
      ```
    - **Naming convention**: `epic/<prd-issue-number>-<kebab-case-epic-name>` (e.g., `epic/123-team-billing-dashboard`).
    - **Why**: The daemon reconstructs this exact branch name from `Parent PRD: #123` in task bodies using the PRD issue title. The branch must exist on remote before tasks are picked up.

11. **Create Task Issues**
    - **Template**: `resources/prd-task.md`.
    - **Review Cycle**: BEFORE creating ANY task issues on GitHub, **PRESENT a summary table of all planned issues** (Title, Blocked by, and brief description) to the user. Wait for their explicit confirmation before proceeding with tool calls.
    - **Mandatory fields in every task body**:
      - `Parent PRD: #123` — used by the daemon to locate the epic feature branch.
      - `Blocked by: #<dep-issue>` — for tasks that depend on another task. Tasks with no cross-task dependency should write `Blocked by: None`.
    - **Labeling**: 
      - Read `.agenTica.js` to find the correct `ready` label (defaulting to `autobot:ready`).
      - **ASK the user**: "Should I label these tasks as 'ready' (e.g., `${READY_LABEL}`) for the autonomous daemon to pick them up immediately?"
      - Only add the `ready` label if the user confirms.
      ```bash
      gh issue create --title "Task: ..." --body "$(cat task-N.md)" --label "task,${READY_LABEL}"
      ```
    - **Create tasks in dependency order** (blockers first), capturing each issue number before creating dependent tasks.

## Dependency & Branch Chain

The daemon automatically resolves branches:
- Task with `Blocked by: None` + `Parent PRD: #123` → branches off `epic/123-<slug>` → PR targets epic branch.
- Task with `Blocked by: #124` → branches off task #124's PR branch → PR chains on top.
- The epic branch PR (created manually or by final merge) targets `main`.

## Guardrails

- **CRITICAL: Start with Research-Backed Grill**. Proactively read the codebase to answer questions before asking the user.
- **Strict Templating**: The PRD MUST follow the bundled `resources/prd.md` structure exactly.
- **Tracer Bullets**: Slices must be functional vertical slices—never horizontal/layer implementation tasks.
- **Sequential Linking**: Create and link the Parent PRD issue first before creating ANY task issues.
