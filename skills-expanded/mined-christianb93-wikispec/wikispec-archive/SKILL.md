--- 
name: wikispec-archive
description: Archive a change
--- 


# Skill: wikispec-archive

Drive the agent through the full `archive` step for a wikispec change. You will use the `wikispec` tool which is a binary in the path, no need to install anything.

## Steps

1. **Determine the change name.**
   - If the user provided a change name, use it exactly.
   - If no name is provided and no description is provided, assume that we will resume work on an existing active change. Use `wikispec list` to list all active changes. If there is only one name, assume that we will be working on this one, otherwise ask the user. Then skip step 2 (creation of the change) and proceed directly to step 3.


2. **Follow instructions in a loop.**
   Repeat until the step is complete:
   ```
   wikispec instructions --change <name> --step archive
   ```
   - If the output contains instructions, follow them, then call the command again.
   - If the output signals that the step is already complete, stop looping and inform the user that the archive step is done and the implementation of the change is complete
