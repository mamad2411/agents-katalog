--- 
name: wikispec-apply
description: Use the task list for the change to implement the actual change
--- 

# Skill: wikispec-apply

Drive the agent through the full `apply` step for a wikispec change. You will use the `wikispec` tool which is a binary in the path, no need to install anything.

## Steps

1. **Determine the change name.**
   - If the user provided a change name, use it exactly.
   - If no name is provided use `wikispec list` to list all active changes. If there is only one active change, assume that we will be working on this one, otherwise ask the user to pick a change from the list

2. **Check whether apply step is runnable**
   - Use `wikispec status --change <change name>` to get the status of the current change
   - Look at the output to validate that the `apply` step is runnable#
   - If not, use the `waitingOn` field to determine the steps on which `apply` is waiting and ask the user to run the corresponding wikispec skill first

3. **Follow instructions in a loop.**
   Repeat until the step is complete:
   ```
   wikispec instructions --change <name> --step apply
   ```
   - If the output contains instructions, follow them, then call the command again.
   - If the output signals that the step is already complete, stop looping, inform the user that the apply step is done and propose to run `/wikispec-validate` next

