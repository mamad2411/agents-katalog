---
name: tooling-shell-fish
description: Use when scripting or configuring the fish shell — syntax, functions, completions, fisher, env vars.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [tooling-git-advanced, tooling-fzf, tooling-ripgrep, tooling-jq]
---

# fish — Friendly Interactive SHell

Fish is not POSIX. Don't expect `bash`/`zsh` syntax to work; it usually doesn't. In exchange you get sane defaults: autosuggestions, syntax highlighting, real arrays, an event system, scripted completions that derive from man pages. Once you adapt, it's faster to author and harder to footgun.

**Core principle:** write fish like fish. Translating bash idioms (`$?`, `[[ ]]`, `function foo() { ... }`) produces broken scripts that limp until they don't. The fish way is shorter and more consistent.

## The syntax differences that bite

| bash/zsh                                    | fish                                                                                 |
| ------------------------------------------- | ------------------------------------------------------------------------------------ |
| `var="hello world"`                         | `set var "hello world"`                                                              |
| `export PATH=/foo:$PATH`                    | `set -gx PATH /foo $PATH`                                                            |
| `if [ "$x" = "1" ]`                         | `if test "$x" = "1"` or `if string match -q 1 $x`                                    |
| `if [[ -f file ]]`                          | `if test -f file`                                                                    |
| `$?`                                        | `$status`                                                                            |
| `$()` and backticks                         | `( )` (just parens)                                                                  |
| `for x in $arr; do …; done`                 | `for x in $arr; …; end`                                                              |
| `function foo() { …; }`                     | `function foo; …; end`                                                               |
| `cmd && other`                              | `cmd; and other` (or `cmd && other` — supported since fish 3.0)                      |
| `array=( a b c )`                           | `set arr a b c`                                                                      |
| `${arr[0]}` (0-indexed)                     | `$arr[1]` (1-indexed!)                                                               |
| `*` and globbing failures expand to literal | empty glob is an error unless prefixed with `set -l files (string collect)` patterns |

**Variables are lists, always.** `set x 1 2 3` makes a 3-element list. `set y 5` makes a 1-element list. There is no "scalar." `$x[2]` is `2`. `count $x` is `3`.

## Universal vs global vs local

```fish
set -l name "local"        # this block / function only
set -g name "global"       # this shell session
set -U name "universal"    # all current and future fish shells for this user
set -gx PATH …             # export to environment (subprocesses see it)
```

`-U` writes to `~/.config/fish/fish_variables`. Powerful — `set -U fish_greeting ""` once, every fish forever silent — but dangerous: changes persist across reboots and you'll forget you made them.

## Abbreviations — better than aliases

Abbreviations expand inline as you press space — what runs is the expanded form, visible to you.

```fish
abbr -a gco git checkout
abbr -a gst git status
abbr -a gp 'git push'

# Functional abbreviation (since fish 3.6)
abbr -a --position command --function last_history_item !!
```

Why prefer them to aliases:

- The expanded form is what enters history (greppable months later)
- You see what's about to run before pressing Enter
- They work with completions for the underlying command

## Functions

```fish
function deploy --description "Deploy to env" --argument-names env
    if test -z "$env"
        echo "usage: deploy <env>" >&2
        return 1
    end
    git push origin main
    ssh "$env.example.com" 'sudo systemctl restart app'
end
```

Save in `~/.config/fish/functions/deploy.fish` (one function per file, named after the function). Fish autoloads on first call — no `source` needed.

Argument access: `$argv` is the list, `$argv[1]` is the first. Or use `--argument-names a b c` to declare names.

## Completions — derive from man pages

```fish
fish_update_completions    # parses /usr/share/man and writes completions for every tool with a man page
```

Run once after install. For tools without man pages, write a `~/.config/fish/completions/<cmd>.fish`:

```fish
complete -c mytool -s v -l verbose -d "Verbose output"
complete -c mytool -n "__fish_use_subcommand" -a "build" -d "Build the project"
complete -c mytool -n "__fish_seen_subcommand_from build" -l target -r -d "Target arch"
```

`-c` = command, `-s` = short flag, `-l` = long flag, `-d` = description, `-r` = takes a required arg, `-n` = condition.

## fisher — the package manager

```fish
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
fisher install jorgebucaran/nvm.fish         # node version manager
fisher install patrickf1/fzf.fish            # fzf integration (Ctrl-R history, etc.)
fisher install jethrokuan/z                  # frecency directory jump
fisher install meaningful-ooo/sponge         # auto-clean broken history entries
fisher list
fisher update
fisher remove <pkg>
```

Plugins are git repos with `functions/`, `completions/`, `conf.d/`. fisher just links them in.

## Env vars and PATH

```fish
set -gx EDITOR nvim
set -gx PATH /opt/homebrew/bin $PATH         # prepend
fish_add_path /opt/homebrew/bin              # smarter PATH helper (dedupes, persists)
fish_add_path -aU $HOME/.local/bin            # append, universal
```

`fish_add_path` is the recommended way to manipulate PATH — handles deduplication and persistence flags correctly.

## Useful built-ins

- `string` — modern replacement for sed/grep one-liners
  - `string split , "a,b,c"` → `a\nb\nc`
  - `string match -r '^foo(\d+)$' 'foo42'` → captures
  - `string replace -a old new $s`
- `math` — replaces `$(( ))` and `expr`
  - `math "2 * 3 + 1"` → `7`
  - `math -s 2 "10 / 3"` → `3.33`
- `read` — prompt for input; `read -P "name? " name`
- `fish_config` — opens a browser config UI for prompts, colors, abbreviations

## Common gotchas

- **Lists splice**, they don't nest. `set a 1 2; set b 3 (count $a)` → `b = 3 2`, not `b = [3, [1,2]]`. There are no nested lists.
- **Word splitting differs.** Command substitution `(cmd)` splits on newlines only, never spaces. No more quoting paranoia from bash.
- **No `&&` short-circuit in older fish**; use `; and` / `; or`. Modern fish (3.x) accepts `&&` and `||`.
- **`||` precedence with `if`**: prefer `if … ; or … ; end` for clarity.
- **`status` vs `$?`**: `$?` doesn't exist in fish; it's `$status`.

## Anti-patterns

- Copy-pasting bash scripts and tweaking — rewrite as fish, it's shorter
- Using `bash -c "…"` to "stay POSIX" instead of learning fish syntax
- `set -U` for things that should be project-local — use a `.envrc` (direnv) instead
- Functions defined inline in `config.fish` — autoload from `functions/` instead
- Re-sourcing `config.fish` "to pick up changes" — autoload is the point; functions reload on next call
- Ignoring `fish_add_path`, then duplicating PATH entries on every shell start

## Hand-off

For interactive history search and directory jumps, `Skill(tooling-fzf)`. For JSON in pipelines, `Skill(tooling-jq)`. For fast code search to wire into completions or shortcuts, `Skill(tooling-ripgrep)`. For git ergonomics in fish, `Skill(tooling-git-advanced)`.
