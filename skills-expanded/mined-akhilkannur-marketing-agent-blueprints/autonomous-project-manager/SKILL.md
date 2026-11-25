--- 
name: autonomous-project-manager
description: "This is the 'Master Blueprint' for long-running autonomous tasks. Modeled after the 'Ralph Wiggum' pattern, it forces the agent to maintain persistent memory and state files for an entire portfolio of projects."
version: 1.0.0
category: Strategic Ops
---

# The Autonomous Project Manager


## Core Instructions
You are a highly specialized AI agent focusing on Strategic Ops. Your mission is:
This is the 'Master Blueprint' for long-running autonomous tasks. Modeled after the 'Ralph Wiggum' pattern, it forces the agent to maintain persistent memory and state files for an entire portfolio of projects.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `project_goals.csv` exist?
2.  **If Missing:** Create `project_goals.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
2.  **If Missing:** Create `project_goals.csv` using the `sampleData`.
3.  **If Present:** Load the project list.

**Phase 2: The Setup Loop**
For each project in the CSV:
1.  **Check Memory:** Does `[Project_Name]_memory.md` exist? If not, create it with the `Tech_Stack` and `Goal`.
2.  **Check Progress:** Does `[Project_Name]_progress.txt` exist? If not, initialize it with `STATUS: INITIALIZING`.
3.  **Decompose:** Create `[Project_Name]_todo.md` with a checklist of atomic steps based on the `Goal`.

**Phase 3: The Execution Loop**
For each project where `progress.txt` is not `COMPLETE`:
1.  **Read Todo:** Get the first unchecked item in `[Project_Name]_todo.md`.
2.  **Execute:** Perform the specific action (e.g., `write_file`).
3.  **Verify:** Check if the action was successful.
4.  **Reflect:** Append any technical hurdles or "lessons" to `[Project_Name]_memory.md`.
5.  **Update State:** Update the todo list and the progress file.

**Phase 4: Portfolio Report**
1.  **Create:** `portfolio_status.csv` with columns: `Project_Name`, `Status`, `Last_Lesson`.
2.  **Report:** "Successfully updated [X] projects. Check the individual project folders for detailed logs."

---
*Blueprint ID: autonomous-project-manager*
*Source: [Real AI Examples](https://realaiexamples.com)*

