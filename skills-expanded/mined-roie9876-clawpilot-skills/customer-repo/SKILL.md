---
name: customer-repo
description: "Scaffold a customer engagement workspace at ~/customer-engagements/{customer}/ with optional per-project subfolders. Supports '/customer-repo Contoso' (customer only) or '/customer-repo Contoso/SASE-PoC' (customer + project). Initializes a local-only git repo with push-blocking hooks. Triggers include: 'new customer', 'customer repo', 'scaffold customer', 'create customer folder', 'set up customer', 'onboard customer', or any request to create a new customer engagement workspace."
---

# /customer-repo — Customer Engagement Folder Scaffolding

Create a complete, local-only customer engagement workspace with standardized
templates, tracking files, and a git repo that blocks pushes to keep customer
data off remote servers. Supports customer-level scaffolding and optional
per-project subfolders within each customer.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the matching command syntax. See `_shared/PLATFORM.md` (skills repo root) for the full translation table. Quick reference:

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Make dir (idempotent) | `mkdir -p X` | `New-Item -ItemType Directory -Force -Path X \| Out-Null` |
| Test dir exists | `[ -d X ]` | `Test-Path X` |
| Make file executable | `chmod +x file` | (no-op on Windows — git for Windows runs hooks via sh.exe regardless) |
| Home dir | `~` or `$HOME` | `$HOME` |

On Windows, the pre-push hook still works because Git for Windows ships with `sh.exe` and runs hook scripts via it. The `chmod +x` step can simply be skipped.

## Core Principles

- **Local-only data.** Customer engagement data never leaves the local machine via git. The repo is initialized with a pre-push hook that blocks all pushes. No remote is ever configured.
- **Idempotent.** If the customer or project folder already exists, report what's there and offer to fill any gaps (missing files or directories) rather than overwriting.
- **OneDrive backup.** Remind the user to back up the folder via their OneDrive for Business sync folder (typically `~/OneDrive - <YourCompany>/` on macOS/Linux or `%USERPROFILE%\OneDrive - <YourCompany>\` on Windows — exact path varies per tenant). This keeps customer data on a managed, NDA-safe location.
- **Names from input.** Accept the customer name (and optional project name) from the user's prompt or ask if not provided. Never guess or fabricate names.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### No Required Sibling Skills

This is a foundation skill — it has no sibling skill dependencies. Other skills
depend on `/customer-repo`, not the other way around.

### Required Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) |
|------|---------------|-----------------|-----------------|-------------------|
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |

Install git before proceeding if missing. Git is required to initialize customer
engagement repos with version control.

---

## Step 1: Collect Names

Parse the user's input for a **customer name** and an optional **project name**.

**Accepted input formats:**
- `/customer-repo Contoso` → customer only, no project.
- `/customer-repo Contoso/SASE PoC` → customer + project (separated by `/`).
- `/customer-repo Contoso SASE PoC` → customer + project (separated by space — treat the first token as customer, the rest as project).

**If nothing provided:**
- Ask: "What is the customer name for this engagement?"

**If only a customer name is provided:**
- Proceed with customer-only scaffolding.
- After scaffolding, ask: "Want to add a project under this customer now? (e.g., `/customer-repo {customer-name}/project-name`)"

**Slugify each name independently for its folder:**
- Lowercase
- Replace spaces with hyphens
- Remove special characters (keep only `a-z`, `0-9`, `-`)
- Example: "Contoso Ltd." → `contoso-ltd`, "SASE PoC" → `sase-poc`

Set:
- `{customer-name}` → display name (e.g., "Contoso Ltd.")
- `{customer-slug}` → folder name (e.g., `contoso-ltd`)
- `{project-name}` → display name (e.g., "SASE PoC") — may be empty
- `{project-slug}` → folder name (e.g., `sase-poc`) — may be empty

## Step 2: Create Folder Structure

**First, ensure the base directory exists:**

```bash
mkdir -p ~/customer-engagements
```

**Then check if the customer folder already exists:**

```bash
ls ~/customer-engagements/{customer-slug}/ 2>/dev/null
```

### Case A: Customer folder does NOT exist

Create the customer-level structure:

```bash
mkdir -p ~/customer-engagements/{customer-slug}
mkdir -p ~/customer-engagements/{customer-slug}/communications
```

If a project name was also provided, create the project structure too:

```bash
mkdir -p ~/customer-engagements/{customer-slug}/projects/{project-slug}/meetings
mkdir -p ~/customer-engagements/{customer-slug}/projects/{project-slug}/decisions
mkdir -p ~/customer-engagements/{customer-slug}/projects/{project-slug}/communications
```

**Conditionally create `architecture/`:** Only if the project has NO registered
`work_repos` in `crm-mapping.json`. If a work repo exists, the architecture
artifacts live there — creating `architecture/` would be redundant.

```bash
# Only if no work_repo is registered for this project:
mkdir -p ~/customer-engagements/{customer-slug}/projects/{project-slug}/architecture
```

### Case B: Customer folder ALREADY exists

- List the existing files and directories.
- Report to the user: "Customer folder already exists at ~/customer-engagements/{customer-slug}/ with these files: ..."

**If a project name was provided:**
- Check if `projects/{project-slug}/` already exists.
  - If it does NOT exist: create the project subfolder and its files (skip to project creation below).
  - If it DOES exist: check for missing files/directories within the project. Offer to fill gaps. If everything is present, report: "Project '{project-name}' is already fully scaffolded under {customer-name}."

**If no project name was provided:**
- Identify any missing customer-level files or the `projects/` directory.
- Ask: "Want me to fill in the missing items, or add a new project?"
- If the customer folder is fully complete, report: "Customer folder already fully scaffolded." List existing projects if any. Ask: "Want to add a new project?"

**Idempotency rule:** Only create what's missing. Never overwrite existing files.

### Target Structure

```
~/customer-engagements/{customer-slug}/
├── README.md              ← customer-level overview
├── stakeholders.md        ← shared across all projects
├── communications/        ← customer-level chat threads, email exchanges, communication history
├── projects/
│   ├── {project-slug}/
│   │   ├── README.md      ← project scope, status, links
│   │   ├── followups.md   ← action items for this project
│   │   ├── meetings/      ← meeting prep briefs and notes
│   │   ├── decisions/     ← architectural and project decisions
│   │   ├── communications/ ← project-specific chat summaries, key email exchanges
│   │   └── architecture/  ← (only if no work_repo registered) diagrams and technical docs
```

**Design principle:** `customer-engagements/` is the **relationship layer** — activity
logs, communications, meetings, follow-ups, decisions. When a project has a dedicated
work repo (e.g., `~/SASE/`), that repo IS the architecture source of truth.
`architecture/` is only created for lightweight engagements with no work repo.

## Step 3: Populate Template Files

Write each template file using the `write` tool. Only create files that don't already exist (idempotency).

### Customer-Level Files

#### README.md — `~/customer-engagements/{customer-slug}/README.md`

```markdown
# {customer-name}

**Engagement start:** {YYYY-MM-DD}
**Account folder:** ~/customer-engagements/{customer-slug}/

## Overview

<!-- Brief description of the customer relationship and engagement context. -->

## Projects

<!-- List of active projects under this customer. -->

## Key Links

<!-- Add links to relevant resources: Teams channels, SharePoint sites, project boards, etc. -->

## Backup

Back up this folder regularly via your OneDrive for Business sync folder
(typically `~/OneDrive - <YourCompany>/` — adjust to your local sync path).

> **⚠️ Privacy Notice:** This folder contains customer-specific engagement data.
> Do not push to any remote git repository. Do not share outside the engagement team.
> All data must remain local or within the approved OneDrive backup path.
```

#### stakeholders.md — `~/customer-engagements/{customer-slug}/stakeholders.md`

```markdown
# Stakeholders — {customer-name}

| Name | Role | Email | Notes |
|------|------|-------|-------|
| <!-- Add stakeholder --> | <!-- Role --> | <!-- email@example.com --> | <!-- Notes --> |

## Internal Team

| Name | Role | Email | Notes |
|------|------|-------|-------|
| <!-- Add team member --> | <!-- Role --> | <!-- email@example.com --> | <!-- Notes --> |
```

### Project-Level Files

Only created when a project name is provided.

#### README.md — `~/customer-engagements/{customer-slug}/projects/{project-slug}/README.md`

```markdown
# {project-name}

**Customer:** {customer-name}
**Project type:** <!-- PoC | Pilot | ADS | Engagement | Workshop -->
**Start date:** {YYYY-MM-DD}
**Status:** Active

## Overview

<!-- Brief description of this specific project/engagement. -->

## Key Links

<!-- Project-specific links: repos, dashboards, shared docs, etc. -->
```

#### followups.md — `~/customer-engagements/{customer-slug}/projects/{project-slug}/followups.md`

```markdown
# Follow-ups — {project-name} ({customer-name})

## Open

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| <!-- Describe the action item --> | <!-- Who owns it --> | <!-- YYYY-MM-DD --> | 🔴 Open |

## Closed

| Action | Owner | Due | Status | Closed |
|--------|-------|-----|--------|--------|
| <!-- Completed items move here --> | <!-- Owner --> | <!-- Due --> | ✅ Done | <!-- YYYY-MM-DD --> |
```

## Step 4: Initialize Git Repo with Push-Blocking Hook

**Initialize git** (skip if `.git/` already exists in the customer folder):

```bash
cd ~/customer-engagements/{customer-slug}
git init
```

**Create the pre-push hook** that blocks all pushes.

Write the following to `.git/hooks/pre-push`:

```bash
#!/bin/sh
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  PUSH BLOCKED: Customer data must remain local.            ║"
echo "║                                                            ║"
echo "║  This repository contains customer engagement data that    ║"
echo "║  must not be pushed to any remote repository.              ║"
echo "║                                                            ║"
echo "║  Back up via your OneDrive for Business sync folder        ║"
echo "║  instead (e.g. ~/OneDrive - <YourCompany>/).               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
exit 1
```

**Make the hook executable** (POSIX only — skip on Windows):

```bash
# macOS / Linux / WSL / Git Bash
chmod +x "$HOME/customer-engagements/{customer-slug}/.git/hooks/pre-push"
```

```powershell
# Windows PowerShell — not needed. Git for Windows runs hook scripts via bundled
# sh.exe regardless of file mode. Skip this step.
```

**Create a commit covering whatever was created:**

```bash
cd ~/customer-engagements/{customer-slug}
git add -A
git commit -m "Initial scaffold for {customer-name} engagement"
```

If a project was added to an existing customer repo, use:

```bash
git add -A
git commit -m "Add project: {project-name}"
```

## Step 5: Print Summary

Adapt the summary based on what was created.

### Customer + Project Created

```
✅ Customer engagement workspace created

📁 Customer: ~/customer-engagements/{customer-slug}/
📄 Customer-level files:
   - README.md (engagement overview + privacy notice)
   - stakeholders.md (contact tracking table)
📂 Directories:
   - communications/ (chat threads, email exchanges, communication history)

📂 Project: ~/customer-engagements/{customer-slug}/projects/{project-slug}/
📄 Project-level files:
   - README.md (project scope, type, status)
   - followups.md (open/closed action items)
📂 Directories:
   - meetings/ (meeting prep briefs and notes)
   - decisions/ (architectural and project decisions)
   - communications/ (project-specific chat summaries, key email exchanges)
   - architecture/ (only if no work_repo — diagrams and technical docs)

🔒 Git: Initialized with push-blocking pre-push hook
📦 Commit: "Initial scaffold for {customer-name} engagement"

💡 Reminder: Back up this folder via your OneDrive for Business sync folder
   (typically ~/OneDrive - <YourCompany>/ — adjust to your local path).
```

### Customer Only Created (No Project)

```
✅ Customer engagement workspace created

📁 Customer: ~/customer-engagements/{customer-slug}/
📄 Files created:
   - README.md (engagement overview + privacy notice)
   - stakeholders.md (contact tracking table)
📂 Directories:
   - communications/ (chat threads, email exchanges)
🔒 Git: Initialized with push-blocking pre-push hook
📦 Commit: "Initial scaffold for {customer-name} engagement"

💡 Run `/customer-repo {customer-name}/project-name` to add a project.

💡 Reminder: Back up this folder via your OneDrive for Business sync folder
   (typically ~/OneDrive - <YourCompany>/ — adjust to your local path).
```

### Project Added to Existing Customer

```
✅ Project added to {customer-name}

📂 Project: ~/customer-engagements/{customer-slug}/projects/{project-slug}/
📄 Files created:
   - README.md (project scope, type, status)
   - followups.md (open/closed action items)
📂 Directories:
   - meetings/ (meeting prep briefs and notes)
   - decisions/ (architectural and project decisions)
   - communications/ (project-specific chat summaries, key email exchanges)
   - architecture/ (only if no work_repo — diagrams and technical docs)
📦 Commit: "Add project: {project-name}"
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `~/customer-engagements/` does not exist | Create it with `mkdir -p`. Continue. |
| Customer folder already exists | List contents. Offer to fill gaps or add a project. Do not overwrite. |
| Customer folder exists and is complete (no project requested) | Report "Folder already fully scaffolded." List existing projects. Ask if they want to add a project. |
| Customer + project both already exist and are complete | Report "Project '{project-name}' is already fully scaffolded under {customer-name}." Show the file listing. Stop. |
| `git init` fails | Warn the user but continue — the folder and files are still usable without git. |
| `git commit` fails | Inform the user. The files are written; only versioning is missing. |
| User provides empty or invalid customer name | Ask again. Do not proceed with an empty slug. |
| User provides empty project name after `/` | Treat as customer-only. Ignore the trailing slash. |
| Disk space or permission error on write | Report the error and stop. Do not partially scaffold. |
