---
name: debug-shell-startup
description: "Diagnose and fix slow interactive shell startup (zsh/bash) on macOS/Linux. Covers profiling, identifying heavy init blocks (conda, nvm, rvm, oh-my-zsh), lazy-loading patterns, broken syntax detection, and verification."
version: 1.0.0
author: Hermes Agent
tags: [shell, zsh, bash, startup, performance, conda, lazy-loading]
---

# Debug Shell Startup

## Overview

When a new terminal window/tab takes multiple seconds to become ready, the culprit is almost always one or more heavy initialization blocks in the shell's startup files (`.zshrc`, `.bashrc`, `.zprofile`, `.zshenv`). This skill provides a systematic approach to profiling, identifying, and fixing slow shell startup.

**Root cause pattern**: Most "slow terminal" reports turn out to be shell startup scripts running heavy subprocesses (conda, nvm, rvm, pyenv, oh-my-zsh, npm prefix) on every new shell — not a process "hanging" after the shell is ready.

---

## Step 1: Measure Baseline

Use `/usr/bin/time` with `zsh -i -c` (or `bash -i -c`) to measure interactive startup time. Run **3 times** — the first may be a cold start with filesystem cache, the subsequent ones show warm-cache performance.

```zsh
for i in 1 2 3; do /usr/bin/time zsh -i -c 'exit' 2>&1 | grep real; done
```

**Interpretation:**
- `< 0.2s`: Excellent. No optimization needed.
- `0.2–1.0s`: Noticeable but acceptable. Worth checking if there's low-hanging fruit.
- `1–5s`: Annoying. One or two heavy init blocks.
- `> 5s`: Defective. Likely conda, nvm, or another tool running subprocesses synchronously on every startup.

Also check the cold-start penalty (the gap between run 1 and run 2+):
- **Cold ≈ warm**: Problem is in file sourcing (too many plugins, large config files)
- **Cold >> warm**: Problem is in subprocess execution (Python binary launch, `node -e`, `npm prefix`) that hits filesystem cache on subsequent runs

---

## Step 2: Inspect Startup Files

Check all shell startup files in order of execution:

```
.zshenv      → sourced for ALL shells (login, interactive, non-interactive, scripts)
.zprofile    → sourced for login shells (terminal window/tab on macOS)
.zshrc       → sourced for interactive shells (the main config file)
.zlogin      → sourced at login shell end
```

Common locations on macOS:
- `~/.zshrc` — the main file
- `~/.zshenv` — usually minimal (PATH additions, cargo env)
- `~/.zprofile` — macOS GUI apps set PATH here

**Look for these patterns:**

1. **`conda init` block** — the `__conda_setup="$(...)` eval block. This runs `conda shell.zsh hook` which launches Python + entire conda stack. **This is #1 cause of 30s+ startup.**

2. **`nvm` / `fnm` / `n`** — NVM sources `nvm.sh` which is a large shell script, and may call `node -e` to detect version.

3. **`rvm`** — RVM sources a large shell function library.

4. **`pyenv init`** — `eval "$(pyenv init -)"` starts Python.

5. **Oh-My-Zsh** — `source $ZSH/oh-my-zsh.sh` with too many plugins can add 0.5–2s.

6. **Broken syntax** — Lines like `export A="val1"export B="val2"` (missing semicolon/newline) cause variable corruption and unexpected errors.

7. **Redundant subprocess calls** — e.g., `export PATH="$(npm prefix -g)/bin:$PATH"` runs Node.js on every startup to discover a path that's already static.

8. **Heavy completions** — Sourcing large completion scripts synchronously (e.g., `pip completion --zsh`, `rustup completions zsh`).

---

## Step 3: Identify the Culprit

### Method A: Comment-and-test (quickest)

Comment out suspect blocks one at a time and re-measure:

```zsh
# Comment out the conda init block
# __conda_setup="$('/opt/...' 'shell.zsh' 'hook' ...)"
```

Then re-run the timing test.

### Method B: zsh profiling (if A is inconclusive)

```zsh
zsh -i -c 'exit' 2>&1 | grep -E '(\.zshrc|\.zshenv|\.zprofile|nvm|conda|oh-my)'
```

Or use zsh's built-in profiling:

```zsh
ZSH_TRACE_PROMPT=1 zsh -i -c 'exit' 2>&1 | head -100
```

### Method C: Append timestamps (granular)

Add timestamp prints to `.zshrc` to find the exact slow line:

```zsh
echo "$(date +%s%3N) START" >&2
# ... block 1 ...
echo "$(date +%s%3N) AFTER CONDA" >&2
# ... block 2 ...
echo "$(date +%s%3N) DONE" >&2
```

---

## Step 4: Apply Fixes

### Fix #1: Conda — Lazy Loading (most impactful)

**Replace** the full conda init block with:

```zsh
# >>> conda initialize (LAZY) >>>
# Only adds conda to PATH; runs conda init on first `conda` command
export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"
conda() {
  unfunction conda
  if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
    . "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
  fi
  conda "$@"
}
# <<< conda initialize <<<
```

**How it works**: On shell start, only `$PATH` is set (no subprocess). The `conda` shell function replaces the `conda` command. When you first type `conda`, it removes its own function definition (to avoid recursion), sources `conda.sh`, and then runs the real `conda` with your arguments. This is transparent — `conda activate base`, `conda install`, etc. all work as expected.

**Why conda is slow**: `conda shell.zsh hook` launches CPython, loads the conda package, and calls `activate.py` which scans the filesystem for environment scripts. On cold boot (no filesystem cache), this takes 20–30 seconds. The lazy function eliminates this entirely.

**Pitfall**: If Homebrew has installed a different `conda` at `/opt/homebrew/bin/conda`, PATH priority can cause the wrong one to run after lazy init. Either ensure miniconda is first in PATH, or uninstall the brew conda.

### Fix #2: Fix Broken Syntax

Check for concatenated export lines like:
```zsh
export A="val1"export B="val2"    # BAD
export JAVA_HOME=$(cmd)           # OK on its own line
```
Split onto separate lines:
```zsh
export A="val1"
export B="val2"
```

Use `zsh -n ~/.zshrc` to validate syntax after changes.

### Fix #3: Remove Redundant Subprocess Calls

```zsh
# BAD — runs `npm prefix -g` (launches Node) every startup
export PATH="$(npm prefix -g)/bin:$PATH"

# GOOD — use the static path directly
export PATH="$HOME/.npm-global/bin:$PATH"
```

### Fix #4: NVM Lazy Loading

```zsh
# Replace `source ~/.nvm/nvm.sh` with:
export NVM_DIR="$HOME/.nvm"
nvm() {
  unfunction nvm
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
  nvm "$@"
}
```

### Fix #5: Disable Conda auto-activation (alternative)

If you do want conda available but don't need the base env activated:

```zsh
conda config --set auto_activate_base false
```

Then replace the full conda init block with just sourcing `conda.sh` — much lighter than running `conda shell.zsh hook`:

```zsh
. "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
```

This is faster than `conda init` but still sources the conda shell functions. For maximum speed, use the lazy function from Fix #1 instead.

---

## Step 5: Verify

1. Validate syntax: `zsh -n ~/.zshrc`
2. Measure again:
   ```zsh
   for i in 1 2 3; do /usr/bin/time zsh -i -c 'exit' 2>&1 | grep real; done
   ```
3. Verify affected commands still work:
   ```zsh
   conda --version
   nvm --version    # if applicable
   ```
4. Test in a **new terminal window/tab** (not just in-session):

---

## Common Pitfalls

| Pitfall | Symptoms | Fix |
|---------|----------|-----|
| Conda lazy function errors | `conda: function definition file not found` | Ensure the `conditional()` syntax is correct — final `conda "$@"` inside the function body must NOT use `command conda "$@"` if you already `unfunction conda` |
| Homebrew conda conflicts | Wrong conda binary used after lazy init | Uninstall brew conda (`brew uninstall conda`) or adjust PATH order |
| `auto_activate_base` still true | Conda tries to activate base even with lazy loading | `conda config --set auto_activate_base false` |
| Line continuation errors on macOS | `.zshrc` parsing fails silently | macOS `.zshrc` doesn't accept Windows line endings; run `sed -i '' $'s/\r$//' ~/.zshrc` |
| `eval "$(something)"` in subshell | Double fork + eval is slow | Replace with sourcing a file or lazy function |

## Verification Commands

```zsh
# Syntax check
zsh -n ~/.zshrc && echo "SYNTAX OK"

# Timing (cold → warm)
echo "=== TIMING ===" && for i in 1 2 3; do /usr/bin/time zsh -i -c 'exit' 2>&1 | grep real; done

# Verify lazy functions
zsh -i -c 'type conda'    # should show "conda is a shell function"

# Environment sanity
zsh -i -c 'echo "JAVA_HOME=${JAVA_HOME:-UNSET}"'
zsh -i -c 'echo "PATH appears ok"'
```

## References

- `references/slow-zsh-startup-conda.md` — Session transcript and exact commands for diagnosing and fixing conda-related slow startup
