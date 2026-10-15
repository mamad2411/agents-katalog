---
name: cleanup-plan
description: Deletes a plan folder and its files, and clears the active pointer if needed.
disable-model-invocation: true
---

You are executing the "/cleanup-plan" protocol.

1. **Scan Plans:** List all subdirectories inside `.plan/`. If there are none, tell me: *"No plans to clean up."* Then stop.
2. **Read Active:** Check `.plan/.active` to know which plan is currently focused.
3. **Ask Which to Delete:** Display the list of available plans (marking the active one) and ask: *"Which plan would you like to delete? This will permanently remove all its files."*
4. **Confirm:** Before deleting, ask: *"Are you sure you want to delete **[plan-name]**? This cannot be undone. (yes/no)"*
   - If no: abort and tell me: *"Cleanup cancelled."*
5. **Delete:** Remove the entire `.plan/[plan-name]/` folder and all its contents.
6. **Clear Active if Needed:** If the deleted plan was the active one, clear `.plan/.active` (write an empty string or delete the file).
7. **Confirm:** Tell me: *"Plan **[plan-name]** has been deleted."* If active was cleared, add: *"Run `/list-plans` to set a new active plan."*
