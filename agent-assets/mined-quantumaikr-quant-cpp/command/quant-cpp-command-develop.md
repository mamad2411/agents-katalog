---
description: Autonomous development — implement the next WBS item using the Karpathy loop
argument-hint: Optional specific module to work on (e.g., polar, qjl, foundation)
---

# Develop

Autonomous single-agent development loop following the Karpathy AutoResearch pattern.

## Protocol

You are an autonomous development agent for quant.cpp.
Follow this loop exactly:

### Step 1: Assess
- Run `bash score.sh --quick` to see current score
- Read `docs/wbs_v0.1.md` to find the next unchecked `- [ ]` item

If the user specified a module ($ARGUMENTS), focus only on WBS items related to that module.

### Step 2: Implement
- Read `program.md` and `CLAUDE.md` for specifications
- Read the relevant reference code in `refs/` before implementing
- Implement the WBS item (create/edit files)
- Follow module ownership rules from CLAUDE.md — only modify files you own

### Step 3: Verify
- Run `bash score.sh --quick`
- If score improved or stayed the same: proceed
- If score dropped: revert your changes and try a different approach
- Ensure all tests pass: `cd build && ctest --output-on-failure`

### Step 4: Commit
- Mark the WBS item as `[x]` in `docs/wbs_v0.1.md`
- Stage only the files you changed (not refs/, not .score_history)
- Commit with a descriptive message

### Step 5: Report
- Show the user: what was implemented, score before → after, next item

### Rules
- ONE WBS item per invocation. Small, correct, incremental.
- Never modify files in `refs/`, `program.md`, or `score.sh`
- Always read reference code before implementing algorithms
- If build fails, fix the build before doing anything else
