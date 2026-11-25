---
name: tooling-fzf
description: Use when adding fzf to a workflow — fuzzy finding, key bindings, tmux integration, --preview flag.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [tooling-shell-fish, tooling-ripgrep, tooling-jq, tooling-git-advanced]
---

# fzf — Fuzzy Finding for Everything

`fzf` is a generic interactive filter for any line-oriented input. Pipe stuff in, pick interactively, get the chosen line(s) out. That's the whole thing. The magic is composition: `find | fzf`, `git log | fzf`, `docker ps | fzf`, `cat ~/notes | fzf`. Once installed, it absorbs every "I need to pick one of these" workflow.

**Core principle:** any list is a candidate for `fzf`. Don't write a custom TUI; pipe to `fzf`. Don't grep-and-eyeball; `rg --files | fzf`. The composition wins.

## Install + shell integration

```sh
brew install fzf
$(brew --prefix)/opt/fzf/install   # installs key bindings + completions
```

After the installer runs, three key bindings exist in your shell:

| Binding    | What it does                                                     |
| ---------- | ---------------------------------------------------------------- |
| **Ctrl-T** | Insert selected file path(s) into the current command line       |
| **Ctrl-R** | Fuzzy-search shell history; selected entry replaces current line |
| **Alt-C**  | `cd` to a fuzzy-selected directory                               |

These three alone justify installing `fzf`. Ctrl-R is the gateway drug.

For fish: `fisher install patrickf1/fzf.fish` for nicer integration than the upstream installer.

## Basic usage

```sh
ls | fzf                              # pick one filename
ls | fzf -m                           # multi-select (Tab to toggle)
ls | fzf --query "test"               # pre-filled query
ls | fzf -1                           # auto-select if exactly one match
ls | fzf -0                           # exit with error if no match

# Use in a command
vim $(fzf)
cd $(find . -type d | fzf)
```

The selected line(s) print to stdout; everything else (UI, prompts) goes to stderr.

## `--preview` — the killer feature

```sh
# Preview file contents (uses bat for syntax-highlighted previews if installed)
rg --files | fzf --preview 'bat --color=always {}'

# Preview directory contents
find . -type d | fzf --preview 'ls -la {}'

# Preview git log entry
git log --oneline | fzf --preview 'git show --color=always {1}'

# Adjust preview window
... --preview '...' --preview-window 'right:60%:wrap'
... --preview '...' --preview-window 'down:50%:border-top'
```

`{}` is the current line. `{1}`, `{2}` are space-separated fields. `{q}` is the current query.

Toggle the preview window with `--bind 'ctrl-/:toggle-preview'`. Scroll preview with `--bind 'ctrl-u:preview-up,ctrl-d:preview-down'`.

## Configuration via env vars

```fish
set -gx FZF_DEFAULT_COMMAND 'rg --files --hidden --glob "!.git/*"'
set -gx FZF_DEFAULT_OPTS '--height 40% --layout=reverse --border --info=inline'
set -gx FZF_CTRL_T_COMMAND "$FZF_DEFAULT_COMMAND"
set -gx FZF_CTRL_T_OPTS '--preview "bat --color=always {}"'
set -gx FZF_CTRL_R_OPTS '--reverse --preview "echo {}" --preview-window down:3:wrap'
set -gx FZF_ALT_C_COMMAND 'fd --type d'
set -gx FZF_ALT_C_OPTS '--preview "ls {}"'
```

`FZF_DEFAULT_COMMAND` is what runs when you invoke `fzf` with no stdin. Set it to `rg --files` and Ctrl-T becomes "pick from all tracked source files" instead of `find` walking node_modules.

## Common recipes

### Fuzzy `git checkout`

```sh
git branch --all | grep -v HEAD | sed 's/.* //' | fzf | xargs git checkout
```

### Fuzzy `kill`

```sh
ps -ef | sed 1d | fzf -m | awk '{print $2}' | xargs kill -9
```

### Pick a file from `git status` and open it

```sh
git -c color.status=always status --short | fzf --ansi --multi --nth 2.. | awk '{print $2}' | xargs $EDITOR
```

### Pick a Docker container to attach to

```sh
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | fzf | awk '{print $1}' | xargs -I{} docker exec -it {} sh
```

### Find a string then jump to it

```sh
rg --column --line-number --no-heading --color=always "" | \
  fzf --ansi --delimiter : \
      --preview 'bat --color=always {1} --highlight-line {2}' \
      --preview-window 'up,60%,+{2}/2' | \
  awk -F: '{print "+"$2, $1}' | xargs $EDITOR
```

Type to search literally across the whole repo; preview shows the file with the matching line centered.

## Multi-select and actions

```sh
... | fzf -m                                # Tab toggles selection
... | fzf --bind 'ctrl-a:select-all'        # custom keybind
... | fzf --bind 'ctrl-r:reload(...)'       # reload the source command
... | fzf --bind 'ctrl-e:execute(vim {})'   # execute without exiting fzf
```

`execute(...)` runs while fzf stays open — useful for "edit one, pick another."

## tmux integration

```sh
fzf-tmux              # opens fzf in a tmux popup instead of consuming the pane
fzf-tmux -p           # popup window (centered, doesn't resize panes)
fzf-tmux -p 80%       # popup at 80% size
fzf-tmux -d 40%       # split below at 40% height
```

In `FZF_DEFAULT_OPTS`, set `--tmux 'center,80%'` (fzf 0.48+; check `fzf --version`) to make every fzf invocation use a tmux popup automatically when in a tmux session.

## Performance

`fzf` ranks millions of lines in milliseconds. Bottlenecks are usually the input command:

- `find /` walks the whole disk — slow
- `rg --files` walks .gitignore-aware, fast
- `fd` is even faster, especially with `-H` for hidden

For huge inputs (>1M lines), `--no-sort` disables sort to ship results instantly; rank by entry order.

## Anti-patterns

- Writing a custom TUI menu when `fzf` would do
- Forgetting `--ansi` when input contains color codes (you'll see `\033[31m` literal)
- Using Ctrl-R for one command then turning it off — it's strictly better than the default
- Defaulting `FZF_DEFAULT_COMMAND` to `find . -type f` (walks ignored dirs) instead of `rg --files`
- Multi-select with `-m` but pipeline assumes one line — use `xargs -d '\n'` or NUL-separate with `--print0`
- Using fzf in a script with no stdin — it'll hang waiting for input

## Hand-off

For the source command (`rg --files`, `rg --column` for live search), `Skill(tooling-ripgrep)`. For shell-side bindings and abbreviations, `Skill(tooling-shell-fish)`. For JSON-shaped inputs (e.g., `gh pr list --json | jq -r ...` into fzf), `Skill(tooling-jq)`. For git-specific pickers (branches, refs, log), `Skill(tooling-git-advanced)`.
