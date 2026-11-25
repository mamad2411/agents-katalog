---
name: grok-projects-workspace
description: Use for grok-projects-workspace, projects scope, clone workspace repo, sync worktree with main repo, commit and push changes. Activate when user mentions grok-projects-workspace or wants consistent workspace across chats.
---

# Projects Scope Skill

## Purpose
This skill guarantees that every chat using it maintains a **consistent, synchronized workspace** at `/home/workdir/GrokProjects` and stays fully aligned with the remote repository at all times.

## Instructions

**Core Workflow – Execute these steps in order every time this skill is active:**

**Visual cue — folder icon (its explicit intention):**  
This `assets/folder-icon.png` reference exists for one precise reason: to embed a visual reminder that tells the user (and every future agent) to **click the folder icon in the Grok chat UI**. Doing so instantly opens the file tree directly to the synchronized workspace at `/home/workdir/GrokProjects`.  

![Folder Icon — click to open workspace](assets/folder-icon.png)

1. **Initialize / Sync Workspace** at `/home/workdir/GrokProjects` and guide the user to click the folder icon:
   ```bash
   mkdir -p /home/workdir/GrokProjects

   if [ ! -d "/home/workdir/GrokProjects/.git" ]; then
     if ! git clone https://github.com/DCx7C5/grok-projects-workspace.git /home/workdir/GrokProjects 2>/dev/null; then
       echo "⚠️ Remote unavailable. Creating local workspace..."
       cd /home/workdir/GrokProjects
       git init
       mkdir -p pipelines templates repos docs
       echo '# Grok Projects Workspace (Local Fallback)' > README.md
       echo 'Initialized locally — remote clone failed.' >> README.md
       git add .
       git commit -m "chore: initial local workspace setup"
     fi
   else
     cd /home/workdir/GrokProjects && git pull --rebase
   fi

   cd /home/workdir/GrokProjects
   ```

2. **Explicit File Path Validation** (run this immediately after every Initialize/Sync):
   ```bash
   WORKSPACE="/home/workdir/GrokProjects"
   if [ ! -d "$WORKSPACE" ]; then
     echo "❌ Workspace directory missing: $WORKSPACE"
     exit 1
   fi
   cd "$WORKSPACE" || { echo "❌ Cannot enter workspace path"; exit 1; }
   RESOLVED_PATH="$(realpath "$WORKSPACE")"
   if [ "$RESOLVED_PATH" != "/home/workdir/GrokProjects" ]; then
     echo "❌ CRITICAL PATH VALIDATION FAILED"
     echo "Expected: /home/workdir/GrokProjects"
     echo "Resolved:  $RESOLVED_PATH"
     echo "Current pwd: $(pwd)"
     exit 1
   fi
   echo "✅ Explicit file path validation passed: $(pwd)"
   # Guarantee core structure exists
   mkdir -p pipelines templates repos docs
   ```

3. **Instruct the user** to click the folder icon (see image above) to open the file tree and directly access `/home/workdir/GrokProjects` in the UI.

4. **Communicate the Sync Rule** clearly:
   - Every agent **must** keep all work fully synchronized with this repository.
   - Every change (pipelines, templates, docs, scripts, etc.) **must** be committed and pushed immediately.
   - This repository is the **single source of truth** — never work in isolation.

5. **Enforce Clean Workflow**:
   - Always `git pull --rebase` before starting new work.
   - After any meaningful change, commit with a clear message and push immediately.
   - Use `git status` and `git diff` before every commit to avoid losing work.

6. **Directory & Project Management**:
   - Keep the workspace at `/home/workdir/GrokProjects`
   - Place all DystopianOS repositories under `repos/`
   - Store shared pipelines and templates in `pipelines/` and `templates/`

7. **Handle Unnamed Projects**:
   - If a project folder in `GrokProjects` (especially under `repos/`) still has no clear name:
     - Ask the user for a proper project name
     - Rename the folder accordingly
     - Immediately commit the change with a descriptive message
     - Push it to the remote repository without delay
   - This keeps the shared workspace clean and well-organized.

8. **Migrate Legacy .grok Folder** (Robust Migration):
   ```bash
   # Check if legacy .grok exists outside GrokProjects
   if [ -d "/home/workdir/.grok" ] && [ ! -d "/home/workdir/GrokProjects/.grok" ]; then
     echo "🔄 Migrating legacy .grok folder into GrokProjects..."
     
     # Create backup if target already has content
     if [ -d "/home/workdir/GrokProjects/.grok" ]; then
       mv /home/workdir/GrokProjects/.grok /home/workdir/GrokProjects/.grok.backup.$(date +%s)
     fi
     
     mv /home/workdir/.grok /home/workdir/GrokProjects/.grok
     cd /home/workdir/GrokProjects
     git add .grok
     git commit -m "chore: migrate legacy .grok folder into workspace"
     git push
     echo "✅ .grok folder successfully migrated and committed."
   fi
   ```
   - This safely moves the old `.grok` folder (skills, config) into `GrokProjects/.grok/`
   - Creates a timestamped backup if needed
   - Automatically commits and pushes the migration
   - Centralizes all Grok configuration inside the shared workspace.

**Activation Triggers:**
- "projects scope"
- "grok-projects-workspace"
- "clone the workspace"
- "sync workspace"
- "commit and push"

This skill ensures **consistent, reliable, and synchronized** behavior across all chats working on the DystopianOS CI/CD infrastructure.