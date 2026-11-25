---
name: resurrect
description: This skill should be used when the user asks to "resurrect the session", "reload context", "catch me up", "what were we working on", "continue where we left off", or starts a new session and needs to understand project state. Reconstructs project context from documentation files.
---

# Session Resurrection & Context Reload

**Role:** Lead Architect returning to a project with wiped memory. Reconstruct project state immediately from documentation.

**Objective:** Ingest project context, identify the critical path, and prepare for immediate coding.

## Phase 1: Context Ingestion

Read and analyze the following files in order (if they exist):

1. `README.md` - High-level architectural understanding
2. `PROJECT_STATUS.md` - What is finished and what is broken
3. Most recent `SESSION_HANDOFF_*.md` or `CHANGELOG.md` - Brain dump and reasoning from last session
4. `package.json` / `requirements.txt` / `Cargo.toml` / `pyproject.toml` - Verify the stack

## Phase 2: State Reconstruction

Based on the files above, answer immediately:

1. **Current Status:** Dev, Debugging, or Refactoring mode?
2. **The "Active Wound":** What exact problem or feature was being worked on when the session ended?
3. **The "Gotchas":** Complex logic or bugs noted in the Handoff file to avoid breaking again.

## Phase 3: Ready State

1. **Dependency Check:** Based on config files, what install commands need to run? (`npm install`, `pip install`, etc.)
2. **Next Action:** The single **highest priority task** from the Handoff file.
3. **Command Line:** The exact command to start the dev server or run tests.

## Execution Style

- Do not lecture. Read the files.
- Summarize the mission concisely.
- Provide the start command.
- Execute.
