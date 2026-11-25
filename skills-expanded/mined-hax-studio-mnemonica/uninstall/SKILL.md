---
name: uninstall
description: This skill should be used when the user asks to "uninstall mnemonica", "remove mnemonica from this project", "stop using mnemonica here", or wants Mnemonica's block and optionally its documentation removed from a project.
---

# Mnemonica: uninstall

Remove exactly what Mnemonica added to a project — never more. This mirrors `setup`'s
non-destructive install in reverse: the CLAUDE.md block is safe to remove without asking
(removing what this plugin itself added is the same risk category as adding it), but
`knowledge/` holds real, accumulated documentation that took real reconciliation work to
build, so deleting it follows the same "ask before deleting" rule as any other module
deletion in `knowledge-conventions.md` — do not treat uninstall as a blanket exemption from
that rule.

If the user's invocation includes extra wording (for example, "uninstall but keep the
knowledge folder"), treat it as answering Step 2 in advance rather than asking again — but do
not let it skip Step 1's confirmation-free block removal into something riskier than
described here, and do not let it turn into deleting anything else in the project.

## Step 1: Remove the CLAUDE.md block

Run `${CLAUDE_PLUGIN_ROOT}/scripts/remove-mnemonica-block.sh <project-root>`.

- Exit 2 (`NO_CLAUDE_MD`) or 3 (`NO_BLOCK`): there is nothing installed to remove here. Tell
  the user and stop — do not proceed to Step 2 or touch `knowledge/` in this case, since
  there is no evidence Mnemonica actually manages this project's `knowledge/` folder (it may
  predate Mnemonica, or belong to something else entirely).
- Exit 0 (`BLOCK_REMOVED` or `FILE_REMOVED`): the block is gone; if it was the only content in
  `.claude/CLAUDE.md`, the file itself was removed too. Every other line in the file, if any
  remained, is untouched — verify this by rereading the file rather than assuming the script
  did the right thing.

## Step 2: Ask about `knowledge/`

Ask the user, explicitly, whether to also delete the `knowledge/` folder and its contents.
Do not delete it without an answer, and do not default to deleting it. Mention how many
module files are in there so the decision is informed (losing N module files' worth of
documentation is a bigger ask than losing one). If the user declines or doesn't say, leave
`knowledge/` exactly as it is — an orphaned `knowledge/` folder with no CLAUDE.md pointer to
it is harmless clutter, not a broken state, and is trivial to remove by hand later.

## Step 3: Leave everything else alone

Never touch `README.md` — it was never Mnemonica's to manage in the first place. Never touch
any part of `.claude/CLAUDE.md` outside what Step 1 already removed.

## Step 4: Report

State plainly what was removed (the block, the file if it was removed entirely, `knowledge/`
if the user confirmed) and what was left in place, so there's no ambiguity about the
project's state afterward.
