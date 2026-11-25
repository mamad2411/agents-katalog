---
name: bash-scripting
description: General-purpose Bash scripting patterns, pitfalls, and gotchas — especially under `set -euo pipefail`. Includes file detection, user prompts, and safe glob handling.
---

# Bash Scripting Patterns

## General principles
- Use `set -euo pipefail` at the top of non-trivial scripts
- Always handle globs that might match zero files
- Distinguish TTY (`-t 0`) vs non-TTY for interactive prompts
- Use `|| true` to absorb expected non-zero exits under `set -e`

## Pitfall: `set -u` + empty array in function (`unbound variable`)

### The bug
```bash
set -euo pipefail
ITEMS=()                            # empty array
check_and_add() {
  for existing in "${ITEMS[@]}"; do  # ← unbound variable error on empty array
    [ "$existing" = "$1" ] && return
  done
  ITEMS+=("$1")
}
```
Under `set -u`, `"${ITEMS[@]}"` (substitution with `[@]` index) on an **empty** array **inside a function** triggers `ITEMS[@]: unbound variable`. Without `set -u` this works fine. Outside a function it also works. The exact combination of **function + empty array + @ index under set -u** is the trap.

`${#ITEMS[@]}` (length expansion) works fine everywhere under `set -u`, even inside functions with empty arrays.

### The fix
Guard the loop with a length check:
```bash
add_item() {
  local p="$1"
  if [ ${#ITEMS[@]} -gt 0 ]; then
    for existing in "${ITEMS[@]}"; do
      [ "$existing" = "$p" ] && return
    done
  fi
  ITEMS+=("$p")
}
```

### Variations

The same bug also triggers on:
```bash
local x="${arr[@]}"   # local + array expansion → unbound variable
```
While `${#arr[@]}` (length) and `local len=${#arr[@]}` work fine.

### Why this happens
Bash's `set -u` behavior differs between `"${#var[@]}"` (length, safe) and `"${var[@]}"` (element expansion, unsafe for empty arrays in function scope). The language spec says referencing an unset variable is an error — bash seems to treat an empty array in a function as "not meaningfully set" for element-expansion purposes.

## Pitfall: `((var++))` returns exit code 1 when var=0

### The bug
```bash
set -euo pipefail
PASS=0; FAIL=0
ok()   { echo "PASS"; ((PASS++)); }   # ← ((0)) evaluates to falsy, exit 1
fail() { echo "FAIL"; ((FAIL++)); }
```

Under `set -e`, `((PASS++))` with `PASS=0` fires `set -e` because the arithmetic expression evaluates to 0 (falsy) and returns exit code 1. This can cause unexpected `||` branch firing in chained commands like `cmd && ok || fail`.

### Root cause
Bash's `((expr))` returns exit code 1 when the expression evaluates to 0. The post-increment `var++` returns the **old** value. So `((PASS++))` when `PASS=0` → expression = 0 → exit 1.

Same applies to `((var--))` when var=1, and `((++var))` when var=-1.

### Fix
Use arithmetic substitution (always returns exit 0):
```bash
ok()   { echo "PASS"; PASS=$((PASS+1)); }
fail() { echo "FAIL"; FAIL=$((FAIL+1)); }
```

Or absorb with `|| true`:
```bash
ok()   { echo "PASS"; ((PASS++)) || true; }
```

Prefer `var=$((var+1))` — explicit, predictable on all values.

## Pitfall: `set -euo pipefail` + `ls` + empty glob

### The bug
```bash
set -euo pipefail
jar=$(ls /some/path/*.jar 2>/dev/null | head -1)   # glob matches nothing
```
When no files match, the glob literal `*.jar` is passed to `ls`. `ls` returns exit code 2. Under `pipefail`, the pipeline returns non-zero. Under `set -e`, the **subshell inside `$()` exits** immediately. The parent's `set -e` also triggers because the assignment `var=$(...)` returns the subshell's non-zero exit code. **Result: script exits silently with no message.**

### The fix
```bash
jar=$(ls /some/path/*.jar 2>/dev/null | head -1) || true
```
The `|| true` absorbs the non-zero exit at the assignment level, so `set -e` does not fire. `jar` is empty-string when no files match.

### Why alternatives don't always work
- **Failglob** (`shopt -s failglob`) — exits on unmatched globs, even worse
- **Nullglob** (`shopt -s nullglob`) — makes glob disappear, but changes global shell state
- **Shellcheck** (`SC2143`) recommends `grep -q` or `for f in *.jar; do` loops, but these also need careful handling

## Pattern: CLI flag parsing in a case-based dispatcher

```bash
case "${1:-}" in
  deploy)
    shift
    BUILD=false; PUSH=false; ALL=false
    while [ $# -gt 0 ]; do
      case "$1" in
        -b|--build) BUILD=true ;;
        -p|--push)  PUSH=true  ;;
        --all)      ALL=true   ;;
        *) usage ;;
      esac; shift
    done
    cmd_deploy
    ;;
esac
```

Then in `cmd_deploy`, check the flags to skip prompts or skip steps.

### Pattern: flag presence detection (`HAS_FLAGS`)

When a command has **both** interactive mode (no flags → prompt for each step) and flag-only mode (flags → skip prompts), detect whether any flag was given:

```bash
HAS_FLAGS=false
[ "$BUILD" = true ] && HAS_FLAGS=true
[ "$PUSH" = true ] && HAS_FLAGS=true
[ "$ALL" = true ] && HAS_FLAGS=true

# Later, per-step:
if [ "$ALL" = true ] || [ "$BUILD" = true ]; then
  do_build=true    # flag: do it, no prompt
elif [ "$HAS_FLAGS" = false ]; then
  if [ -t 0 ]; then
    echo -n "执行构建？[Y/n] "; read -r ans
    [ "$ans" != "n" ] && do_build=true
  else
    do_build=true  # non-TTY + no flags = default to yes
  fi
fi
```

This gives three clean tiers:
1. **Flag-specific** (`BUILD=true`) — just that step, no prompt
2. **No flags at all** — interactive prompts per step
3. **Non-TTY + no flags** — default to yes (backward-compatible with CI/scripts)

## Pattern: multi-source file detection with user selection

### Basic: flat search across directories

```bash
# Collect candidates
SOURCES=()
LABELS=()
for dir in "/opt/project" "$HOME/project"; do
  file=$(ls "$dir/build/*.jar" 2>/dev/null | head -1) || true
  [ -n "$file" ] && { SOURCES+=("$file"); LABELS+=("$dir"); }
done
```

### Advanced: per-directory sub-path + dedup

When each base directory has a different internal layout (e.g., `/opt/enterprise` vs `/home/dev/enterprise`):

```bash
SOURCES=()
LABELS=()

# Dedup helper — skips if path already in list
add_candidate() {
  local path="$1" label="$2"
  if [ ${#SOURCES[@]} -gt 0 ]; then
    for existing in "${SOURCES[@]}"; do
      [ "$existing" = "$path" ] && return
    done
  fi
  SOURCES+=("$path"); LABELS+=("$label")
}

for dir in "/opt" "$PROJECT_ROOT"; do
  # Root-level files (manual copy / USB stick)
  for f in "$dir"/app.jar; do [ -f "$f" ] && add_candidate "$f" "$dir"; done
  for f in "$dir"/enterprise-*.jar; do [ -f "$f" ] && add_candidate "$f" "$dir"; done

  # Build output — path differs per base
  sub="$dir/backend/target"
  [ "$dir" = "/opt" ] && sub="$dir/enterprise/backend/target"  # /opt/ → /opt/enterprise/
  jar=$(ls "$sub/enterprise-mvp-"*.jar 2>/dev/null | head -1) || true
  [ -n "$jar" ] && add_candidate "$jar" "$sub"
done
```

### Selection logic

```bash
case ${#SOURCES[@]} in
  0) warn "not found" ;;
  1) USE="${SOURCES[0]}" ;;
  *)
    echo "Pick source:"
    for i in "${!SOURCES[@]}"; do echo "  [$((i+1))] ${LABELS[$i]}"; done
    if [ -t 0 ]; then
      read -r sel; sel=${sel:-1}
    else
      sel=1  # non-TTY: auto-pick first
    fi
    USE="${SOURCES[$((sel-1))]}"
    ;;
esac
```

### UX pattern: prompt before search (not search then prompt)

When the search/scan is expensive (directory traversal, remote checks), ask YES/NO **first**, then only search if the user confirms. This avoids wasted work when the user says no:

```bash
# Bad: search first, then ask
SOURCES=$(find_candidates)          # expensive, wasted if user says no
echo -n "Use these? [Y/n] "; read -r ans
[ "$ans" = "n" ] && skip

# Good: ask first, then search
echo -n "Update backend? [Y/n] "; read -r ans
if [ "$ans" != "n" ]; then
  SOURCES=$(find_candidates)        # only runs if user said yes
fi
```

## Pattern: safe TTY detection for prompts

```bash
read_input() {
  local var="$1"; shift
  if [ -t 0 ]; then
    echo -n "$*"
    read -r "$var"
  else
    printf -v "$var" "${2:-1}"   # default value
  fi
}
```

## Pattern: `.env`-based configuration with defaults

```bash
VAR="${VALUE:-default}"
if [ -f "$PROJECT/.env" ]; then
  source "$PROJECT/.env" 2>/dev/null
  VAR="${CONFIG_VAR:-default}"
fi
```
Always keep the bare default inside the `${VAR:-default}` expression so the script works without `.env`.

## Pattern: shared port/variable aliases

When a script needs port numbers or paths in multiple places (update, health check, etc.), define them once at the top of the function, with `.env` override support:

```bash
# Define aliases early in the function, before any code that uses them
BP=8082; FP=8088
if [ -f "$PROJECT_ROOT/docker/.env" ]; then
  source "$PROJECT_ROOT/docker/.env" 2>/dev/null
  BP="${BACKEND_PORT:-8082}"
  FP="${FRONTEND_PORT:-8088}"
fi
```

Then reference `$BP` and `$FP` everywhere. This avoids scattering hardcoded port numbers across health checks, poll loops, and verify sections. The `.env` fallback keeps the script working on machines without the file.

## Pattern: Y/n prompt with not-equal guard

```bash
# Ask user, defaulting to YES (anything except explicit 'n'/'N' counts as yes)
echo -n "Update backend？[Y/n] "; read -r ans
[ "$ans" != "n" ] && [ "$ans" != "N" ] && do_update=true
```

The `!= "n"` check (as opposed to `= "y"`) makes Enter / empty input mean YES, which is the standard convention for uppercase `Y/n`. If you want default NO, use lowercase `y/N` and check `[ "$ans" = "y" ]`.

Combine with TTY guard for CI safety:
```bash
if [ -t 0 ]; then
  echo -n "Update？[Y/n] "; read -r ans
  [ "$ans" != "n" ] && do_it=true
else
  do_it=true  # non-TTY (CI/SSh): always yes
fi
```

## Cross-platform compatibility (macOS + Linux)

### Port check: `ss` (Linux) vs `lsof` (macOS)

Linux has `ss` (fast, part of iproute2). macOS has `lsof` (part of base system). Neither exists on the other.

```bash
port_busy=false
if command -v ss &>/dev/null; then
  port_busy=$(ss -tlnp "sport = :$PORT" 2>/dev/null | grep -q .)
elif command -v lsof &>/dev/null; then
  port_busy=$(lsof -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | grep -q .)
fi
```

Check availability first, then call the right command. `command -v` is POSIX and works on both platforms.

### `grep -P` is GNU-only (not on macOS)

BSD grep (macOS) does NOT support the `-P` (Perl regex) flag — it throws `invalid option -- P`. Use `-E` (extended regex) instead; both GNU and BSD grep support it.

```bash
# BROKEN on macOS:
grep -qP "pattern1|pattern2" file

# WORKS everywhere:
grep -qE "pattern1|pattern2" file
```

### `uname` for platform branching

```bash
if [[ "$(uname)" == "Darwin" ]]; then
  # macOS-specific path
  open -a Docker 2>/dev/null  # Docker Desktop
elif command -v systemctl &>/dev/null; then
  # Linux with systemd
  systemctl start docker
fi
```

Note: `uname` returns `Darwin` on macOS. Linux returns `Linux`. For finer-grained Linux distro detection, check for specific commands (`apt`, `yum`, `systemctl`).

### Docker compose: v1 vs v2

Modern Docker Desktop bundles compose as `docker compose` (subcommand, v2). Legacy/servers may have standalone `docker-compose` (binary, v1). Detect both:

```bash
if docker compose version &>/dev/null; then
  dc_cmd="docker compose"
elif docker-compose --version &>/dev/null; then
  dc_cmd="docker-compose"
fi
```

Then use `$dc_cmd` for all compose operations instead of hardcoding either variant.

### macOS Docker Desktop auto-start

Unlike Linux (systemctl/service), macOS Docker is a GUI app:

```bash
if [[ "$(uname)" == "Darwin" ]]; then
  open -a Docker
  # Docker Desktop takes ~10s to start; add a wait loop:
  for i in {1..10}; do
    docker info &>/dev/null && break
    sleep 2
  done
fi
```

### Docker context fallback (Colima / Lima) — prefer DOCKER_HOST

On macOS, Docker may be running under **Colima** (or Lima) instead of Docker Desktop. The default Docker socket (`/var/run/docker.sock`) can be a broken symlink pointing to a Docker Desktop socket that doesn't exist, while Colima's socket lives at `~/.colima/default/docker.sock`.

**Preferred approach (`DOCKER_HOST`, no side effects):**
```bash
detect_docker_host() {
  if [ -z "${DOCKER_HOST:-}" ]; then
    local colima_sock="$HOME/.colima/default/docker.sock"
    if [ -S "$colima_sock" ]; then
      export DOCKER_HOST="unix://$colima_sock"
    fi
  fi
}
detect_docker_host
```
This is clean because `DOCKER_HOST` is process-local — it doesn't mutate the user's Docker config. Call `detect_docker_host` early (before any docker command) so every subsequent docker invocation uses the right socket.

**Alternative (`docker context use`, mutates global config):**

Only use this in persistent CLI tools where the user expects the context switch to stick. It changes `~/.docker/config.json`:
```bash
if ! docker info &>/dev/null && [[ "$(uname)" == "Darwin" ]] && command -v colima &>/dev/null; then
  docker context use colima &>/dev/null
  if docker info &>/dev/null; then
    DOCKER_OK=true
  else
    docker context use default &>/dev/null  # restore
  fi
fi
```
Always restore the default context in the failure branch. Use `&>/dev/null` (not just `2>/dev/null`) because `docker context use` prints the context name to stdout.

### Summary: prefer POSIX or universally-available commands

| Operation | Linux | macOS | Universal approach |
|-----------|-------|-------|--------------------|
| Port check | `ss` | `lsof` | Detect-and-fallback |
| Regex grep | `grep -P` | ✗ | Use `grep -E` |
| Disk usage | `df -h` | `df -h` | Same, but column positions may differ |
| File descriptor | `/proc/PID/fd` | `lsof -p PID` | Detect-and-fallback |
| Random bytes | `/dev/urandom` | /dev/urandom | Same |
| sed | GNU sed | BSD sed | Use `perl -pi -e` for cross-platform |
| Readlink | `readlink -f` | `greadlink` (brew) | `realpath` or `cd + pwd` |

## Pattern: graceful degradation for Docker-dependent scripts

When a diagnostic/verification script uses Docker commands but might run on a machine without Docker, guard all Docker-dependent sections behind a single availability check:

```bash
DOCKER_OK=false
if docker info &>/dev/null; then
  DOCKER_OK=true
  # Docker info & version display
fi

# Docker-dependent sections guard:
if ${DOCKER_OK:-false}; then
  # images check / container status / health check / frontend check
fi
```

Benefits:
- Docker API errors never leak into user output
- Empty section headers are hidden, not shown with nothing below
- Port conflict detection degrades gracefully: "port occupied (Docker not running, can't verify source)" instead of "port occupied by other process"

### Port conflict detection with Docker-aware fallback

```bash
if $port_busy; then
  if ${DOCKER_OK:-false} && docker ps ... | grep -qE ...; then
    ok "port used by our container"
  elif ${DOCKER_OK:-false}; then
    fail "port occupied by other process"
  else
    warn "port occupied (Docker not running, can't verify source)"
  fi
fi
```

This avoids falsely blaming SSH tunnels or other non-conflict listeners when Docker can't confirm ownership. Apply the same pattern to any service that might be routed via SSH port forwarding.

### Template: deployment doctor script

A full template for a Dockerized service diagnostic script is available at `templates/deployment-doctor.sh` in the skill directory. It implements all the patterns above (Docker host detection, graceful degradation, cross-platform port checks, 3-way port conflict reporting) in a ready-to-customize structure.

## Verification

After editing a bash script:
```bash
bash -n script.sh          # syntax check
bash -x script.sh 2>&1     # trace execution (redir stderr to stdout)
```

For `set -e` verification of a specific line:
```bash
set -euo pipefail
result=$(command-that-may-fail 2>/dev/null) || true
[ -z "$result" ] && echo "empty — survived set -e"
```

## macOS tooling quirks

### macOS (BSD) sed: no backreference in match pattern

macOS `/usr/bin/sed` (BSD sed) does NOT support `\1` backreferences in the **pattern** (search) part of `s///`, only in the **replacement** part. This holds in both default mode and `-E` (extended regex) mode.

```bash
# WORKS:
echo "abc" | sed 's/\(a..\)/\1xxx/'             # → abcxxx  (\1 in replacement)
echo "abc" | sed -E 's/(a..)/\1xxx/'             # → abcxxx

# FAILS (no match):
echo "abc" | sed 's/\(a..\)/\1/'                 # → abc      (\1 in pattern)
echo "abc" | sed -E 's/(a..)/\1/'                # → abc      (same)
```

**Workaround:** Use a literal backreference substitute (perl, awk, or Python) for multi-file pattern-replacements, or iterate over known values:

```bash
# Instead of sed with backreference in pattern:
for f in ARCH DATABASE DEPLOY; do
  find . -name "*.md" -exec sed -i '' "s|[$f.md]($f.md|[$f.md](docs/$f.md|g" {} +
done
```

Or use `perl -pi -e` which handles backreferences correctly:
```bash
perl -pi -e 's|\[(\w+\.md)\]\(\1|[$1](docs/$1|g' *.md
```
