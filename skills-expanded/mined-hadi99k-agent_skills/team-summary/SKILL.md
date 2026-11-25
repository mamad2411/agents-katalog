---
name: team-summary
description: Creates and maintains TEAM_SUMMARY.md (or TEAM_LOG.md) to track individualized work summaries for each team member or AI agent persona. Gives every contributor their own persistent section with recent accomplishments, modified files, active focus, and blockers without overwriting other members' logs.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: team-collaboration
---

# 👥 Team Member Summaries & Activity Log (`team-summary`)

## What I Do
1. **Manage `TEAM_SUMMARY.md`**: Creates and maintains a dedicated team activity file where each team member (human developer, collaborator, or specialized AI agent) has their own designated summary section.
2. **Isolate Individual Contributions**: Ensures team members update only their own work log, preventing team members or AI agents from accidentally erasing or overwriting each other's progress notes.
3. **Track Asynchronous Standups**: Provides clear visibility into:
   - What each person/agent recently built or fixed.
   - Which files they touched or currently own.
   - What they are actively working on next.
   - Any blockers or cross-member dependencies.
4. **Maintain a Team Roster**: Keeps an at-a-glance status table at the top of the file so anyone entering the project immediately knows who is working on what.

---

## When to Use Me
- When multiple developers, contributors, or AI agent sessions work on the same project.
- After finishing a task or feature sprint to record what you (or your agent persona) accomplished.
- When starting work to announce your active focus and prevent duplicate effort.
- When the user asks: *"update my team summary"*, *"log what I did in the team file"*, *"add member summary"*, or *"create TEAM_SUMMARY.md"*.

---

## 🏛️ Structure of `TEAM_SUMMARY.md`

The file is organized with a quick high-level roster followed by self-contained member sections:

```
┌─────────────────────────────────────────────────────────────┐
│             TEAM_SUMMARY.md (or TEAM_LOG.md)                │
├─────────────────────────────────────────────────────────────┤
│ 📌 Team Roster & Quick Status (At-a-glance table)           │
├─────────────────────────────────────────────────────────────┤
│ 👤 Member: [Member A / Agent Persona 1]                     │
│    - Role & Last Active                                     │
│    - 🎯 Current Focus & Next Steps                          │
│    - ✅ Recent Accomplishments (Dated logs)                  │
│    - 📂 Key Files Touched / Owned                           │
│    - 🚧 Blockers & Notes for Team                           │
├─────────────────────────────────────────────────────────────┤
│ 👤 Member: [Member B / Agent Persona 2]                     │
│    - ... (Dedicated, isolated section)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Execution Steps for the Agent

When this skill is invoked:

### Step 1: Identify the Member
Determine the identity/persona of the contributor:
1. **Human Developer**: Check `git config user.name` or ask the user (e.g., `@Hadi`, `Alice`, `Lead Dev`).
2. **AI Agent Persona**: Check `AGENT_SYNC.md` or session context (e.g., `Agent 1: Android Architect`, `Agent 2: Compose UI Specialist`, `Security Auditor Agent`).

### Step 2: Check or Create `TEAM_SUMMARY.md`
1. Check if `TEAM_SUMMARY.md` (or `TEAM_LOG.md`) exists in the project root.
2. If it does not exist, create it using the template below.

### Step 3: Update the Member's Section (Non-Destructive)
1. Search for the member's existing header: `## 👤 Member: [Member Name]`.
2. **If found**:
   - Update **Last Updated** with the current date/timestamp.
   - Update **Current Status** and **🎯 Current Focus**.
   - Prepend new accomplishments under **✅ Recent Accomplishments** (keep past highlights intact).
   - Update **📂 Key Files Touched** with recently modified file paths.
   - Update or clear **🚧 Blockers**.
3. **If not found (New Member)**:
   - Append a new `## 👤 Member: [Member Name]` section at the bottom of the file.
   - Add a new row to the **📌 Team Roster & Quick Status** table at the top.
4. **CRITICAL INVARIANT**: Never delete, alter, or overwrite another member's section.

### Step 4: Sync Team Roster
Update the member's row in the top **📌 Team Roster & Quick Status** table with their latest status and timestamp.

---

## 📋 The Master `TEAM_SUMMARY.md` Template

```markdown
# 👥 Team Member Summaries & Activity Log

> **Asynchronous standup and individual contribution log.** Every team member or AI agent maintains their own designated section here. Never overwrite another member's summary.

---

## 📌 Team Roster & Quick Status

| Member / Agent | Role / Domain | Last Updated | Current Status |
| :--- | :--- | :--- | :--- |
| **[Member Name]** | [e.g. Lead Developer / Core Architect] | YYYY-MM-DD | 🟢 [Active task / feature] |

---

## 👤 Member: [Member Name / Agent Persona]
- **Role / Ownership:** [e.g., Core Android Architecture, Compose UI, Backend API]
- **Last Updated:** [YYYY-MM-DD]
- **Status:** [🟢 Active / 🟡 Paused / 🔴 Blocked]

### 🎯 Current Focus & Next Steps
- [What this member is actively working on right now or planning next]

### ✅ Recent Accomplishments (What Was Done)
- **[YYYY-MM-DD]**:
  - [Bullet point of completed feature, bug fix, or refactor]
  - [Key architectural decision or problem resolved]

### 📂 Key Files Touched / Owned
- `path/to/file1.ext` — [Brief explanation of changes]
- `path/to/file2.ext` — [Brief explanation of changes]

### 🚧 Blockers & Notes for Team
- *None currently.* (Or describe any dependencies, questions for peers, or shared blockers)

---
```

---

## 💡 Example: Updating an Existing Member

When `@Hadi` finishes working on a new setting:

```markdown
## 👤 Member: @Hadi
- **Role / Ownership:** Lead Android Engineer
- **Last Updated:** 2026-10-18
- **Status:** 🟢 Active

### 🎯 Current Focus & Next Steps
- Implementing in-app feedback voting and review prompts.

### ✅ Recent Accomplishments (What Was Done)
- **2026-10-18**:
  - Added dock anchor alignment options (Left, Right, Top, Bottom) in `FloatSidebar.kt`.
  - Fixed landscape auto-expansion bugs and capped panel height at 90%.
  - Added haptic feedback toggles across all overlay tool buttons.
- **2026-10-15**:
  - Wired Room database migrations for category bookmarks.

### 📂 Key Files Touched / Owned
- `app/src/main/java/com/floatkit/app/ui/components/FloatSidebar.kt` — Dock layout and orientation adjustments
- `app/src/main/java/com/floatkit/app/ui/screens/SettingsScreen.kt` — Dock anchor radio group

### 🚧 Blockers & Notes for Team
- *None currently.*
```
