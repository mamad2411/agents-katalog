---
name: new-workflow
description: Scaffold a new standalone workflow with directory structure and plan template
argument-hint: <workflow-name>
disable-model-invocation: true
---

Scaffold a new standalone workflow.

## Input

The user may provide a workflow name as the argument: $ARGUMENTS

**Before doing anything else, you MUST gather ALL of the following inputs.** Use the `AskUserQuestion` tool to ask for every missing piece of information. If the user provided a workflow name as the argument, you still MUST ask the remaining questions — the name alone is NOT enough to proceed.

Required inputs (ask for ALL that are not yet known):

1. **Workflow name** — kebab-case, e.g., `pdf-summarizer` (skip only if provided as $ARGUMENTS)
2. **One-line description** — what the workflow does in one sentence
3. **Detailed description or specification** — can be left blank, but you must explicitly offer the option
4. **Deploy target** — Local only, or Local + Modal
5. **Modal mode(s)** — ask this ONLY if deploy target includes Modal: Webhook, Scheduled, Manual, or a combination (e.g., Webhook + Scheduled)

**Do NOT skip any of these.** Do NOT proceed to the Steps section until you have answers for all five inputs (or four if Local-only, since Modal mode does not apply).

## Steps

1. **Validate the name**
   - Must be kebab-case (lowercase, hyphens only)
   - Must not already exist in `workflows/`

2. **Create the workflow directory** at `workflows/$ARGUMENTS/`

3. **Scaffold files:**

   **`workflows/$ARGUMENTS/README.md`**
   ```markdown
   # {workflow-name}

   {description}

   ## Usage

   ```bash
   python workflows/{workflow-name}/main.py
   ```

   ## Environment Variables

   This workflow loads env vars from the root `.env` first, then from `workflows/{workflow-name}/.env` (overrides).

   See the root `.env.example` for shared vars. Copy this workflow's `.env.example` to `.env` only if you need workflow-specific overrides.

   ## Deploy Target

   {target}
   ```

   **`workflows/$ARGUMENTS/main.py`**
   - If Local only: use the local-only template
   - If Modal webhook mode: use the webhook template
   - If Modal scheduled/manual mode (no webhook): use the scheduled template
   - If Modal webhook + scheduled: use the combined template
   - Include a docstring explaining what the workflow does

   **`workflows/$ARGUMENTS/.env.example`**
   - Only include workflow-specific vars that are NOT already in the root `.env.example`
   - If all vars are covered by the root `.env.example`, add a comment-only file explaining that
   - Always include a comment header explaining the override behavior

4. **Add new dependencies to root `requirements.txt`**
   - If the workflow needs packages not already in the root `requirements.txt`, add them
   - Do NOT create a per-workflow `requirements.txt`

5. **Create plan file** at `.agent/plans/$ARGUMENTS.md`
   - Use the template from `.agent/plans/_template.md`
   - Pre-fill the workflow name, description, and deploy target
   - Leave implementation details for the user to fill in

6. **Update CATALOG.md**
   - Add a new row to the Workflows table
   - Status: `Planned`
   - Fill in complexity, deploy target, Modal mode (or N/A if local-only), and description
   - Set `Args` to `TBD` (will be filled in once the workflow is implemented)

7. **Report what was created**
   - List all files created
   - Note any new dependencies added to root `requirements.txt`
   - Remind the user to fill in the plan before running `/build`
