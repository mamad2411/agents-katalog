---
name: macos-shell-portability
description: Reference for macOS shell environment differences — zsh vs bash defaults, BSD vs GNU tool behavior, and portable command patterns for agent-authored shell commands on macOS.
category: Shell & Scripting
---

# macOS Shell Portability (v1) — Reference

## 1. When to Apply

Apply this reference whenever authoring or documenting shell commands intended for execution on macOS. Specifically:

- Generating brew / mise / npm / pip command chains for macOS users
- Documenting shell snippets in SKILL.md files that target macOS
- Diagnosing shell syntax errors or tool failures on macOS (e.g., `tee --version` fails, `help tee` is unknown)
- Writing cross-platform scripts that must work on both macOS and Linux

## 2. Scope

This skill documents **differences** between macOS and Linux shell environments. It does NOT teach shell basics. It is
consumed by other skills as a portability cross-reference.

## 3. Default Shell: zsh

macOS Catalina (10.15, 2019) and later ship with **zsh** as the default login and interactive shell (previously bash).
Key differences from bash that affect agent-authored commands:

| Behavior | bash | zsh (macOS default) |
|---|---|---|
| `help <cmd>` builtin | Available (`help cd`, `help echo`) | NOT available — use `man <cmd>` instead |
| Prompt variable | `PS1` | `PROMPT` (though `PS1` is aliased for compatibility) |
| Array indices | Zero-based (`${arr[0]}`) | One-based (`${arr[1]}`) |
| Brace expansion | `{a,b}` works | `{a,b}` works (compatible) |
| Process substitution | `<(cmd)` works | `<(cmd)` works (compatible) |
| `[[ ]]` test syntax | Works (Korn-derived) | Works (same origin) |
| Default startup file | `~/.bashrc`, `~/.bash_profile` | `~/.zshrc`, `~/.zprofile` |

**Key pitfall:** Never use `help <cmd>` on macOS — it is a bash builtin, not a zsh one. Always use `man <cmd>` or `<cmd>
--help`.

## 4. BSD vs GNU Tool Differences

macOS ships BSD variants of core utilities, not GNU variants. The following table documents common flags that differ:

### 4.1 `tee`

| Flag | BSD tee (macOS) | GNU tee (Linux) |
|---|---|---|
| `--version` | FAILS with `illegal option` | Prints version |
| `--help` | Prints help (works on both) | Prints help |
| `-a` (append) | Works | Works |
| Default behavior | Overwrites output file | Overwrites output file |

**Portable pattern:** Use `man tee` for help (works on both). Never rely on `tee --version` succeeding.

### 4.2 `sed -i`

| Flag | BSD sed (macOS) | GNU sed (Linux) |
|---|---|---|
| `-i ''` | Requires empty-string arg AFTER `-i` (no space variant may work) | `-i` optional; with arg = backup extension |
| `-i` without extension | `sed -i ''` (MUST supply empty string) | `sed -i` (extension optional) |

**Portable pattern:** Prefer Python / Node scripts over `sed -i` for in-place file mutations. If `sed -i` is
unavoidable, use `sed -i ''` on macOS (empty backup extension) or detect the platform.

### 4.3 `find`

| Feature | BSD find (macOS) | GNU find (Linux) |
|---|---|---|
| `-printf` | NOT available | Available |
| `-exec {} +` | Works | Works |
| `-maxdepth` | Works | Works (both support this) |
| `-delete` | Works | Works |

**Portable pattern:** Avoid `-printf` on macOS. Use `-exec echo {} \;` or Python for custom output formatting.

### 4.4 `xargs`

| Feature | BSD xargs (macOS) | GNU xargs (Linux) |
|---|---|---|
| `-0` (null delimiter) | Works | Works |
| `-d` (delimiter) | NOT available | Available |
| `-r` (no-run-if-empty) | BSD default behavior | GNU requires `-r` |

**Portable pattern:** Use `-0` with `find ... -print0` for null-delimited pipelines (works on both). Avoid `-d`.

### 4.5 `date`

| Feature | BSD date (macOS) | GNU date (Linux) |
|---|---|---|
| `-d @<timestamp>` | NOT available (`-d` sets date, not parses) | Converts epoch to date |
| `-r <file>` | Shows file's last-modified time | NOT available |
| `+%s` | Works (epoch seconds from current time) | Works |
| `-j -f` | Parses formatted date with `-j -f` | Not needed (`-d` handles parsing) |

**Portable pattern:** For epoch-to-date conversion on macOS, use `date -r <timestamp>`. For date-to-epoch, use `date -j
-f "%Y-%m-%d" "2026-06-23" "+%s"`. Prefer Python `datetime` for cross-platform date work.

### 4.6 `grep`

| Feature | BSD grep (macOS) | GNU grep (Linux) |
|---|---|---|
| `-P` (Perl regex) | NOT available (unless `ggrep` installed) | Available |
| `-o` (only-matching) | Works | Works |
| `-r` (recursive) | Works (but prefer the built-in `grep` tool) | Works |

**Portable pattern:** Avoid `-P`. Use extended regex with `-E` instead (works on both).

## 5. Common Shell Pitfalls

### 5.1 `; &&` Parse Error

This pattern produces a shell parse error on zsh AND bash:

```bash
export VAR=value; && command
#                ^^--- error: nothing between ; and &&
```

The `;` is a command terminator — it ends the `export` command. The `&&` expects a command on its left. After `;` there
is nothing, so `&&` has nothing to chain to.

**Correct forms:**

```bash
# Option A: chain with && (export must succeed)
export VAR=value && command

# Option B: independent statements (run regardless)
export VAR=value; command

# Option C: mixed — export unconditionally, chain subsequent commands
export VAR=value; command1 && command2 && command3
```

Option C is the pattern used by `brew-upgrade-command-assembly` — the `export HOMEBREW_DOWNLOAD_CONCURRENCY=1;` is a
standalone statement (the env var is set, exit code is irrelevant), and all subsequent `brew upgrade && brew cleanup`
pairs are chained with `&&`.

### 5.2 Missing `help` Builtin

On macOS (zsh), `help cd` fails with `zsh: command not found: help`. Use `man cd` instead. In bash, `help` lists shell
builtins; in zsh, `run-help` is the equivalent (often unbound by default).

### 5.3 `--version` on BSD Tools

Many BSD tools on macOS reject `--version`:

```bash
tee --version   # "illegal option -- -"
sed --version   # "illegal option -- -"
```

Use `<tool> --help` (which both BSD and GNU accept), or `man <tool>`, instead of `--version`.

## 6. Portable Command Patterns

When writing shell commands for macOS (and optionally Linux cross-compatibility):

| Goal | Portable Pattern | Avoid |
|---|---|---|
| Get tool help | `man <tool>` or `<tool> --help` | `<tool> --version` (BSD fails) |
| Get shell help | `man <builtin>` | `help <builtin>` (zsh fails) |
| Pipe with output capture | `command 2>&1 \| tee output.log` | `command &> output.log` (bash 4+ only) |
| In-place file edit | Use Python `pathlib.Path.write_text()` or Node.js | `sed -i` (BSD/GNU differ) |
| Parse date | Use Python `datetime` | `date -d` (BSD incompatible) |
| Suppress errors | `2>/dev/null` (works on both) | N/A |
| Time command | `command` prefixed with `time` (zsh has a `time` reserved word) | N/A |

## 7. Cross-References

- [`brew-upgrade-command-assembly`](../../brew-upgrade-command-assembly/SKILL.md) — brew upgrade chain assembler that
uses the `export ...; cmd1 && cmd2 && cmd3` pattern (§5.1)
- [`brew-upgrade-workflow`](../../brew-upgrade-workflow/SKILL.md) — composer that discovers outdated leaves and
delegates to the assembler
- [`repo-scratch-output-capture`](../../repo-scratch-output-capture/SKILL.md) — silent stdout/stderr capture to
`scratch/` (alternative to `tee` for background probes)
- [`is-this-command-safe`](../../is-this-command-safe/SKILL.md) — shell command safety vetting that classifies `tee
overwrite` as `MUTATES`

## 8. Traceability

- **Origin Conversation**: Session 2026-06-23 — user on macOS hit `; &&` parse error in a brew upgrade chain, then
discovered `tee --version` fails and `help` is unavailable on zsh. The three gaps (zsh defaults, BSD tools, `; &&`
pitfall) were extracted into this reference skill.
