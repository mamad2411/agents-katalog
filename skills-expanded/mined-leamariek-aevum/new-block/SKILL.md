---
name: new-block
description: Scaffold a new Aevum block (block.yaml plus its paired narrative plan), fill it in with the user, and validate it with preflight.
disable-model-invocation: true
argument-hint: <BLOCK_ID> "<Title>" <owner>
---

Create block `$ARGUMENTS` and take it to a clean preflight.

1. Scaffold both artefacts:

   ```bash
   bash scripts/new-block.sh $ARGUMENTS
   ```

2. Read `.claude/templates/block.yaml` for the schema and list the agents
   under `.claude/agents/`: each task's `agent:` must be one of them.

3. Interview the user with AskUserQuestion until you can fill the block:
   the goal, the clusters and their order, each task's surface
   (`files_touched_globs`) and acceptance criteria, and kill criteria if
   the block has a deadline. Push for acceptance criteria a script can
   check (a command and its expected result, a regex over a file), since
   Gate 3a verifies them mechanically. Skip what the code already answers.

4. Write `docs/blocks/<BLOCK_ID>/block.yaml` and the narrative plan under
   `docs/plans/`. Set `base_sha` to the current tip of `base_branch`.
   Leave `status: draft`.

5. Validate and fix until the only blocker left is `status is 'draft'`
   (activation happens at dispatch):

   ```bash
   python3 scripts/block-preflight.py <BLOCK_ID>
   ```

6. Capture the Gate-1 baseline:

   ```bash
   bash scripts/capture-baseline.sh <BLOCK_ID>
   ```

Finish by telling the user the block is ready for review and that
`/dispatch <BLOCK_ID>` (`/aevum:dispatch` with the plugin) activates and launches it. Do not commit.
