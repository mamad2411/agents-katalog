---
name: show-diff
description: Open a tmux split running diffview.nvim so the user can review the agent's recent changes. Use proactively after non-trivial edits, or when the user asks to "show the diff", "open a diff viewer", or similar.
argument-hint: [rev-range]
---

# Show Diff

Open a new tmux pane that displays current changes via `diffview.nvim`,
so the user can review in a side-by-side viewer instead of scrolling
terminal output.

## When to use

- After making more than a handful of edits, surface them for review
- User asks to see the diff, open a diff viewer, or review the changes
- Before asking the user to approve committing a larger change

Skip when edits are tiny, when not inside tmux, or when the user has
already reviewed the changes in this turn.

## How to run

```bash
bash ~/code/seabbs/dotfiles/scripts/show-diff.sh $ARGUMENTS
```

The script opens a right-hand split running `nvim +DiffviewOpen <range>`
rooted at the repo top-level.

## Choosing the rev-range

Shortcuts the script understands:

| Argument | Expands to | Use when… |
|---|---|---|
| *(none)* | working tree vs HEAD | changes are uncommitted |
| `last` | `HEAD~1..HEAD` | reviewing just the last commit |
| `last N` or `N` | `HEAD~N..HEAD` | reviewing the last N commits |
| `pr` | `origin/<base>...HEAD` (base from `gh pr view`) | on a branch with an open PR |
| any other value | passed through verbatim | explicit rev range, e.g. `main...HEAD` |

If the agent has both committed and uncommitted work on a feature
branch with an open PR, `pr` is the fastest choice.

## Requirements

- Running inside tmux (script errors out otherwise)
- Inside a git repository
- `diffview.nvim` available in neovim (already configured in the
  user's dotfiles)

## After opening

Tell the user the pane is up and what range it shows. Do not try to
drive the nvim instance from the agent side.
