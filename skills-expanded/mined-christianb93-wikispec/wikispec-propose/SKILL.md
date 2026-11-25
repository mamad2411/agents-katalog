--- 
name: wikispec-propose
description: Create specs and designs for a new change. Use this when you need to specify a new change or continue to work on the specification of an existing change.
--- 


# Skill: wikispec-propose

Drive the agent through the full `propose` step for a wikispec change. You will use the `wikispec` tool which is a binary in the path, no need to install anything.

## Steps

1. **Determine the change name.**
   - If the user provided a change name, use it exactly.
   - If no name was provided, but the user has provided a description of what to change, propose a short kebab-case name that captures the user's intent (e.g., `add-auth`, `fix-export-bug`)
   - If no name is provided and no description is provided, assume that we will resume work on an existing active change. Use `wikispec list` to list all active changes. If there is only one name, assume that we will be working on this one, otherwise ask the user. Then skip step 2 (creation of the change) and proceed directly to step 3.

2. **Create the change.**
   Run:
   ```
   wikispec create --change <name>
   ```
   - If the command succeeds, proceed to step 3.
   - If the command fails because the change already exists, derive an alternative name (e.g., append `-2`) and retry this step.

3. **Gather context**
   - load the `wikispec-wiki` skill to understand how to operate the knowledge wiki
   - locate and read the wikis `index.md` file. Check whether any of the pages listed there are relevant for the functionality proposed by the user and read those pages.
   - run `wikispec files --change <name>`  to see whether there are already any specification files for this change, if yes read them

4. **Follow instructions in a loop.**
   Repeat until the step is complete:
   ```
   wikispec instructions --change <name> --step propose
   ```
   - If the output contains instructions, follow them, then call the command again.
   - If the output signals that the step is already complete, stop looping, inform the user that the propose step is complete and suggest to run `/wikispec-plan` next. 
