---
description: "Remove only artifacts created by this chat from the active workspace for a clean restart."
argument-hint: "Optional: scope notes or exclusions. Omit them to clean all artifacts created by this chat."
---

# Clean Slate Workspace

## 1. Inspect the Workspace
1. Inspect current conversation artifacts in the active workspace.
2. List all files, plans, repository memory, session memory, and temporary artifacts created in this chat.
3. Determine ownership for each artifact.

## 2. Resolution Rules
- Do not delete anything until inspection is complete and targets are listed.
- Delete only artifacts created in this chat.
- Treat ambiguous ownership as user-authored.
- Never delete or modify user-authored files or ambiguous-ownership artifacts.
- Do not touch persistent user-level memories or reusable customizations unless they were created for this workspace in this chat.
- Remove empty directories left by deletions.
- Confirm no session-created files or empty directories remain after deletion.
- If no session-created artifacts exist, state that explicitly and stop.

## 3. Safety Guards
- **Execution boundary:** Delete only after presenting the target list and receiving the user's explicit confirmation.

## 4. Review Plan Layout
Use this exact markdown schema:

### Scope
- Target: <active workspace>
- Mode: <read-only | apply-after-confirmation>

### Result
- Summary: <what was deleted and what was preserved>

### Evidence
- Deleted: <none | item1; item2>
- Preserved: <none | item1; item2>
- Uncertainties: <none | item1; item2>

### Next Action
- <single minimal next step or `none`>

### Verdict
- READY | NEEDS FIXES | BLOCKED
