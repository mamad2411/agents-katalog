---
name: vim-review
description: Open the repository's working tree in Neovim Fugitive in a new tmux review pane.
---

# Vim Review

Open a review pane when explicitly invoked. This workflow opens the working tree
for the user's inspection; it does not perform a code review.

1. Resolve the exact repository or worktree directory where the requested changes were made. Ask which one to open if several repositories were changed and the request is ambiguous.
2. Identify the current Codex pane in tmux. Use `TMUX_PANE` when available and verify that it exists. Otherwise inspect the panes and ask the user to choose if the current Codex pane cannot be identified unambiguously; always target an explicit pane ID rather than tmux's active window.
3. Open a new pane to its right at roughly half the window width, with the repository as its working directory, and focus it. With `pane` and `repo` resolved, use `tmux split-window -h -l 50% -t "$pane" -c "$repo" "nvim -c 'Gedit :'"`. Preserve existing panes and editors; each request creates a new pane.
4. Verify that Neovim shows the Fugitive status for the intended repository or worktree in a single window, with no extra empty window, before reporting success. The review shows the whole working tree, including staged, unstaged, untracked, and pre-existing user changes.

If tmux is unavailable, explain that a pane cannot be opened and provide a command to run `nvim -c 'Gedit :'` manually from the resolved repository directory, quoting its path safely.
