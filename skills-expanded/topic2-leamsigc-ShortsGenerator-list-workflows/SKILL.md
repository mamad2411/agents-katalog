---
name: list-workflows
description: List all runnable workflows in this project with their arguments and deployment status
---

List all runnable workflows in this project with their arguments and deployment status.

## Steps

1. **Read `CATALOG.md`** at the project root
   - Parse the Workflows table
   - Filter to only workflows with status **Done** or **Deployed** (skip Planned, In Progress, Archived)
   - All needed info is in the table — do NOT read individual workflow files

2. **Display the results** using the columns from the table:

   For each workflow, show one entry like:

   ```
   {name} — {description}
     Run:  python workflows/{name}/main.py {args}
     Args: {args column from CATALOG.md}
     {[Deployed to Modal] if deploy target includes Modal, otherwise omit}
   ```

   Rules:
   - The `Args` column in CATALOG.md contains the argument names and descriptions — display them directly
   - If Args is `none` or empty, say `Args: none (interactive prompt)`
   - If the deploy target is `Local + Modal` or the status is `Deployed`, append `[Deployed to Modal]` on its own line
   - If the deploy target is just `Local`, do not add any deployment tag

3. **If no workflows match** (none are Done or Deployed), say:
   > No runnable workflows found. Use `/new-workflow` to scaffold one and `/build` to implement it.

4. **Footer:** After the list, show a count: `{n} runnable workflow(s)` and a reminder that you can run `/onboard` for full project details.
