---
name: script-patterns
description:
  This skill should be used when implementing common shell script patterns such as argument parsing,
  logging, cleanup, temp files, script directory resolution, input validation, process management,
  and portability helpers. It provides ready-to-use patterns with CORRECT and WRONG examples.
version: 0.1.0
---

# Shell Script Patterns

This skill provides production-ready patterns for common shell scripting tasks. Each pattern
includes CORRECT and WRONG examples to guide implementation.

## Argument Parsing

### getopts for Short Options

Use `getopts` when you only need short (single-character) options. This is the POSIX-standard
approach and works in both bash and sh.

```bash
# CORRECT: getopts with proper error handling
#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: backup.sh [-h] [-v] [-n COUNT] [-o DIR] <source>

Options:
  -h         Show help
  -v         Verbose output
  -n COUNT   Number of backups to keep (default: 5)
  -o DIR     Output directory (default: ./backups)
EOF
}

verbose=false
keep_count=5
output_dir="./backups"

while getopts ":hvn:o:" opt; do
    case $opt in
        h) usage; exit 0 ;;
        v) verbose=true ;;
        n) keep_count="$OPTARG" ;;
        o) output_dir="$OPTARG" ;;
        :) echo "Error: -$OPTARG requires an argument" >&2; exit 1 ;;
        *) echo "Error: Unknown option -$OPTARG" >&2; usage >&2; exit 1 ;;
    esac
done
shift $((OPTIND - 1))

# Validate required positional argument
if (( $# < 1 )); then
    echo "Error: source argument is required" >&2
    usage >&2
    exit 1
fi
source_dir="$1"
```

```bash
# WRONG: getopts without leading colon (no custom error messages)
while getopts "hvn:o:" opt; do    # Missing leading : for silent error handling
    case $opt in
        h) usage; exit 0 ;;
        v) verbose=true ;;
        # Missing : case for options requiring arguments
        # Missing * case for unknown options
    esac
done
# Missing shift to consume parsed options
```

**getopts rules**:

- Leading `:` in optstring enables silent error mode (custom error messages)
- A colon after a letter means the option takes an argument (`n:` means `-n VALUE`)
- `$OPTARG` contains the argument value (or the bad option character on error)
- Always `shift $((OPTIND - 1))` after the loop to access positional arguments

### while+case for Long Options

Use `while+case` when you need `--long-option` support. This is the standard bash approach.

```bash
# CORRECT: while+case with both short and long options
#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: deploy.sh [OPTIONS] <environment>

Options:
  -h, --help           Show this help message
  -v, --verbose        Enable verbose output
  -t, --tag TAG        Docker image tag (required)
  -r, --replicas N     Number of replicas (default: 3)
  --dry-run            Show what would happen without making changes
  --no-health-check    Skip post-deploy health check
EOF
}

verbose=false
tag=""
replicas=3
dry_run=false
health_check=true

while (( $# > 0 )); do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        -t|--tag)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --tag requires a value" >&2
                exit 1
            fi
            tag="$2"
            shift 2
            ;;
        -r|--replicas)
            if [[ -z "${2:-}" || ! "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --replicas requires a numeric value" >&2
                exit 1
            fi
            replicas="$2"
            shift 2
            ;;
        --dry-run)
            dry_run=true
            shift
            ;;
        --no-health-check)
            health_check=false
            shift
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            break
            ;;
    esac
done

# Validate required options
if [[ -z "$tag" ]]; then
    echo "Error: --tag is required" >&2
    exit 1
fi

# Validate required positional arguments
if (( $# < 1 )); then
    echo "Error: environment argument is required" >&2
    usage >&2
    exit 1
fi
environment="$1"
shift
```

```bash
# WRONG: Missing argument validation for options that take values
while (( $# > 0 )); do
    case "$1" in
        --tag) tag="$2"; shift 2 ;;    # Crashes if $2 is missing
        *) break ;;
    esac
done

# WRONG: Not handling -- for end-of-options
while (( $# > 0 )); do
    case "$1" in
        --verbose) verbose=true; shift ;;
        *) break ;;                     # "--" is treated as positional arg
    esac
done
```

### Subcommand Pattern

```bash
# CORRECT: Subcommand dispatch
#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: myctl <command> [args...]

Commands:
  start    Start the service
  stop     Stop the service
  status   Show service status
  logs     View service logs

Run 'myctl <command> --help' for command-specific help.
EOF
}

cmd_start() {
    echo "Starting service..."
}

cmd_stop() {
    echo "Stopping service..."
}

cmd_status() {
    echo "Service status: running"
}

cmd_logs() {
    local follow=false
    while (( $# > 0 )); do
        case "$1" in
            -f|--follow) follow=true; shift ;;
            *) break ;;
        esac
    done
    if [[ "$follow" == "true" ]]; then
        tail -f /var/log/myservice.log
    else
        tail -100 /var/log/myservice.log
    fi
}

main() {
    if (( $# < 1 )); then
        usage >&2
        exit 1
    fi

    local command="$1"
    shift

    case "$command" in
        start)   cmd_start "$@" ;;
        stop)    cmd_stop "$@" ;;
        status)  cmd_status "$@" ;;
        logs)    cmd_logs "$@" ;;
        -h|--help|help) usage ;;
        *)
            echo "Error: Unknown command '$command'" >&2
            usage >&2
            exit 1
            ;;
    esac
}

main "$@"
```

## Logging Functions

### Standard Logging Library

All diagnostic output must go to stderr so stdout remains clean for data piping.

```bash
# CORRECT: Full logging library with timestamps and colors
#!/usr/bin/env bash

# Detect color support
if [[ -t 2 ]]; then
    readonly _C_RED='\033[0;31m'
    readonly _C_GREEN='\033[0;32m'
    readonly _C_YELLOW='\033[0;33m'
    readonly _C_BLUE='\033[0;34m'
    readonly _C_BOLD='\033[1m'
    readonly _C_RESET='\033[0m'
else
    readonly _C_RED='' _C_GREEN='' _C_YELLOW='' _C_BLUE='' _C_BOLD='' _C_RESET=''
fi

log() {
    printf "${_C_BLUE}[%s]${_C_RESET} %s\n" "$(date '+%H:%M:%S')" "$*" >&2
}

warn() {
    printf "${_C_YELLOW}[%s] WARN:${_C_RESET} %s\n" "$(date '+%H:%M:%S')" "$*" >&2
}

err() {
    printf "${_C_RED}[%s] ERROR:${_C_RESET} %s\n" "$(date '+%H:%M:%S')" "$*" >&2
}

die() {
    err "$@"
    exit 1
}

success() {
    printf "${_C_GREEN}[%s] OK:${_C_RESET} %s\n" "$(date '+%H:%M:%S')" "$*" >&2
}
```

```bash
# WRONG: Logging to stdout (breaks piping)
log() {
    echo "[$(date)] $*"          # Goes to stdout, mixes with data
}

# WRONG: No timestamp (hard to debug)
log() {
    echo "$*" >&2                # When did this happen?
}

# WRONG: Using echo -e for colors (not portable)
err() {
    echo -e "\033[31mERROR: $*\033[0m" >&2    # -e not portable
}
```

### POSIX sh Logging

```sh
# CORRECT: POSIX sh logging (no color, no bash extensions)
#!/bin/sh

log() {
    printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$*" >&2
}

warn() {
    printf '[%s] WARN: %s\n' "$(date '+%H:%M:%S')" "$*" >&2
}

err() {
    printf '[%s] ERROR: %s\n' "$(date '+%H:%M:%S')" "$*" >&2
}

die() {
    err "$@"
    exit 1
}
```

### Verbose-Mode Logging

```bash
# CORRECT: Debug logging controlled by verbose flag
VERBOSE="${VERBOSE:-false}"

debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        printf '[%s] DEBUG: %s\n' "$(date '+%H:%M:%S')" "$*" >&2
    fi
}

# Usage
debug "Connecting to $host:$port"
debug "Response headers: $(curl -sI "$url")"
```

```bash
# WRONG: Verbose logging that cannot be disabled
echo "DEBUG: Connecting to $host:$port"     # Always prints, clutters output
```

## Trap Cleanup Patterns

### Basic Cleanup

```bash
# CORRECT: Trap EXIT for guaranteed cleanup
tmpdir=""
cleanup() {
    local exit_code=$?
    if [[ -n "$tmpdir" && -d "$tmpdir" ]]; then
        rm -rf "$tmpdir"
    fi
    exit "$exit_code"
}
trap cleanup EXIT

tmpdir=$(mktemp -d)
```

```bash
# WRONG: Cleanup at end of script (skipped on error)
tmpdir=$(mktemp -d)
# ... work ...
rm -rf "$tmpdir"            # Never reached if script fails!
```

### Cleanup with Background Process Management

```bash
# CORRECT: Kill child processes on exit
child_pid=""

cleanup() {
    local exit_code=$?
    if [[ -n "$child_pid" ]]; then
        kill "$child_pid" 2>/dev/null || true
        wait "$child_pid" 2>/dev/null || true
    fi
    if [[ -n "${tmpdir:-}" && -d "${tmpdir:-}" ]]; then
        rm -rf "$tmpdir"
    fi
    exit "$exit_code"
}
trap cleanup EXIT

# Start background process
long_running_command &
child_pid=$!

# Wait for it
wait "$child_pid"
child_pid=""    # Clear so cleanup doesn't try to kill completed process
```

### Error Line Reporting

```bash
# CORRECT: Report the failing line on ERR
on_error() {
    local exit_code=$?
    local line_no="$1"
    err "Failed at line $line_no with exit code $exit_code"
    err "Command: ${BASH_COMMAND}"
}
trap 'on_error ${LINENO}' ERR
```

```bash
# WRONG: Trapping ERR without useful information
trap 'echo "error" >&2' ERR     # No line number, no exit code
```

### Stacking Trap Handlers

```bash
# CORRECT: Preserve existing traps when adding new ones
existing_trap=$(trap -p EXIT | sed "s/trap -- '//;s/' EXIT//")
new_cleanup() {
    rm -f "$my_temp_file"
    eval "$existing_trap"
}
trap new_cleanup EXIT
```

## Temporary File Patterns

### Safe Temp Directory Pattern

```bash
# CORRECT: Create a temp directory and derive all temp files from it
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/myapp.XXXXXX")
trap 'rm -rf "$work_dir"' EXIT

# Derive temp files inside the directory
input_tmp="$work_dir/input.json"
output_tmp="$work_dir/output.json"
log_tmp="$work_dir/process.log"

curl -sf "$url" > "$input_tmp"
jq '.data' "$input_tmp" > "$output_tmp"
```

```bash
# WRONG: Multiple independent temp files (each needs cleanup)
tmp1=$(mktemp)
tmp2=$(mktemp)
tmp3=$(mktemp)
trap 'rm -f "$tmp1" "$tmp2" "$tmp3"' EXIT    # Easy to forget one
```

### Atomic File Writes

```bash
# CORRECT: Write to temp, then atomically move
write_file() {
    local target="$1"
    local content="$2"
    local tmpfile
    tmpfile=$(mktemp "${target}.tmp.XXXXXX")

    if printf '%s\n' "$content" > "$tmpfile"; then
        mv -f "$tmpfile" "$target"
    else
        rm -f "$tmpfile"
        return 1
    fi
}
```

```bash
# WRONG: Direct write (leaves partial file on failure)
printf '%s\n' "$content" > "$target"     # Partially written if interrupted
```

## Script Directory Resolution

### Bash Script Directory

```bash
# CORRECT: Resolve script directory (handles symlinks in directory path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# CORRECT: Fully resolve symlinks (script itself is a symlink)
resolve_script_dir() {
    local source="${BASH_SOURCE[0]}"
    while [[ -L "$source" ]]; do
        local dir
        dir="$(cd "$(dirname "$source")" && pwd)"
        source="$(readlink "$source")"
        # Resolve relative symlink
        [[ "$source" != /* ]] && source="$dir/$source"
    done
    cd "$(dirname "$source")" && pwd
}
SCRIPT_DIR="$(resolve_script_dir)"
```

```bash
# WRONG: Using $0 in bash (unreliable when sourced)
SCRIPT_DIR="$(dirname "$0")"           # Wrong if script is sourced

# WRONG: Using pwd (depends on where script is called from)
SCRIPT_DIR="$(pwd)"                    # Wrong if called from another directory
```

### POSIX sh Script Directory with Fallback

```sh
# CORRECT: POSIX sh with readlink fallback
#!/bin/sh
set -eu

resolve_script_dir() {
    local dir
    dir="$(cd "$(dirname "$0")" && pwd)"

    # Try to resolve symlinks
    if command -v readlink >/dev/null 2>&1; then
        local resolved
        resolved="$(readlink -f "$0" 2>/dev/null)" || resolved=""
        if [ -n "$resolved" ]; then
            dir="$(cd "$(dirname "$resolved")" && pwd)"
        fi
    fi

    printf '%s' "$dir"
}

SCRIPT_DIR="$(resolve_script_dir)"
```

## Input Validation Patterns

### Numeric Validation

```bash
# CORRECT: Validate integers
is_positive_integer() {
    local value="$1"
    [[ "$value" =~ ^[1-9][0-9]*$ ]]
}

validate_port() {
    local port="$1"
    if ! [[ "$port" =~ ^[0-9]+$ ]] || (( port < 1 || port > 65535 )); then
        die "Invalid port: $port (must be 1-65535)"
    fi
}
```

```bash
# WRONG: No validation
port="$1"
curl "http://localhost:$port/"    # What if port is "abc"?
```

### Path Validation

```bash
# CORRECT: Validate file/directory paths
validate_input_file() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        die "File not found: $file"
    fi
    if [[ ! -r "$file" ]]; then
        die "File not readable: $file"
    fi
}

validate_output_dir() {
    local dir="$1"
    if [[ -e "$dir" && ! -d "$dir" ]]; then
        die "Not a directory: $dir"
    fi
    mkdir -p "$dir" || die "Cannot create directory: $dir"
    if [[ ! -w "$dir" ]]; then
        die "Directory not writable: $dir"
    fi
}
```

### Whitelist Validation

```bash
# CORRECT: Validate against known-good values
validate_environment() {
    local env="$1"
    case "$env" in
        development|staging|production) return 0 ;;
        *) die "Invalid environment: $env (must be development, staging, or production)" ;;
    esac
}

validate_log_level() {
    local level="$1"
    case "$level" in
        debug|info|warn|error|fatal) return 0 ;;
        *) die "Invalid log level: $level" ;;
    esac
}
```

```bash
# WRONG: No whitelist validation
environment="$1"
# Using unvalidated input directly in a URL or command
curl "https://${environment}.example.com/api"    # What if env contains "evil.com/"?
```

## Process Management Patterns

### Wait for Service Ready

```bash
# CORRECT: Wait with timeout and backoff
wait_for_ready() {
    local url="$1"
    local timeout="${2:-60}"
    local interval="${3:-2}"
    local elapsed=0

    log "Waiting for $url (timeout: ${timeout}s)"

    while (( elapsed < timeout )); do
        if curl -sf "$url" > /dev/null 2>&1; then
            log "Service is ready (${elapsed}s)"
            return 0
        fi
        sleep "$interval"
        (( elapsed += interval ))
    done

    err "Service not ready after ${timeout}s: $url"
    return 1
}

# Usage
wait_for_ready "http://localhost:8080/health" 30
```

```bash
# WRONG: Infinite loop with no timeout
while ! curl -sf http://localhost:8080/health; do
    sleep 1
done
# Never exits if service is permanently down
```

### Lock File Pattern

```bash
# CORRECT: Directory-based lock (atomic on all filesystems)
acquire_lock() {
    local lockdir="$1"
    if ! mkdir "$lockdir" 2>/dev/null; then
        local pid
        pid=$(cat "$lockdir/pid" 2>/dev/null || echo "unknown")
        # Check if the lock holder is still alive
        if [[ "$pid" != "unknown" ]] && kill -0 "$pid" 2>/dev/null; then
            err "Lock held by active process $pid"
            return 1
        fi
        warn "Removing stale lock (pid=$pid)"
        rm -rf "$lockdir"
        mkdir "$lockdir" || { err "Cannot acquire lock"; return 1; }
    fi
    echo $$ > "$lockdir/pid"
    trap 'rm -rf "'"$lockdir"'"' EXIT
}

# Usage
acquire_lock /var/lock/myapp.lock || exit 1
```

```bash
# WRONG: File-based lock (race condition between check and create)
if [[ -f "$lockfile" ]]; then
    echo "Locked" >&2
    exit 1
fi
echo $$ > "$lockfile"          # Race: another process may create between check and write
```

### Retry with Exponential Backoff

```bash
# CORRECT: Retry with backoff and max attempts
retry() {
    local max_attempts="$1"
    local delay="$2"
    shift 2

    local attempt=1
    while true; do
        if "$@"; then
            return 0
        fi

        if (( attempt >= max_attempts )); then
            err "Failed after $max_attempts attempts: $*"
            return 1
        fi

        warn "Attempt $attempt/$max_attempts failed, retrying in ${delay}s"
        sleep "$delay"
        (( attempt++ ))
        (( delay = delay * 2 > 60 ? 60 : delay * 2 ))    # Cap at 60 seconds
    done
}

# Usage
retry 5 2 curl -sf "https://api.example.com/data"
retry 3 1 docker pull "myapp:latest"
```

```bash
# WRONG: Retry without limit
while ! curl -sf "$url"; do
    sleep 1                     # Runs forever on permanent failure
done

# WRONG: Retry without backoff
for i in {1..5}; do
    curl -sf "$url" && break
    sleep 1                     # Constant delay, no backoff
done
```

## Portability Helper Patterns

### Cross-Platform stat

```bash
# CORRECT: Portable file size
file_size() {
    local file="$1"
    if stat -f%z "$file" 2>/dev/null; then
        return 0    # macOS
    elif stat -c%s "$file" 2>/dev/null; then
        return 0    # Linux
    else
        wc -c < "$file" | tr -d ' '    # Fallback
    fi
}
```

### Cross-Platform sed In-Place

```bash
# CORRECT: Portable sed -i
sed_inplace() {
    if [[ "$(uname -s)" == "Darwin" ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Usage
sed_inplace 's/old/new/g' config.txt
```

### Cross-Platform Readlink

```bash
# CORRECT: Portable readlink -f
resolve_path() {
    local target="$1"
    if command -v realpath &>/dev/null; then
        realpath "$target"
    elif command -v greadlink &>/dev/null; then
        greadlink -f "$target"    # macOS with coreutils
    elif readlink -f "$target" 2>/dev/null; then
        return 0                  # Linux readlink -f
    else
        # Manual resolution
        cd "$(dirname "$target")" && printf '%s/%s' "$(pwd)" "$(basename "$target")"
    fi
}
```

### Portable Date Formatting

```bash
# CORRECT: ISO 8601 timestamp that works everywhere
timestamp() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# CORRECT: Epoch seconds (works on both Linux and macOS)
epoch_seconds() {
    date '+%s'
}
```

```bash
# WRONG: GNU date-only syntax
date -d "2 hours ago" '+%Y-%m-%d'     # Fails on macOS
date --iso-8601=seconds                # GNU extension
```

## Configuration File Patterns

### .env File Loading

```bash
# CORRECT: Safe .env file loader
load_dotenv() {
    local env_file="${1:-.env}"
    if [[ ! -f "$env_file" ]]; then
        return 0
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and blank lines
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue

        # Remove 'export ' prefix if present
        line="${line#export }"

        # Extract key and value
        local key="${line%%=*}"
        local value="${line#*=}"

        # Validate key format
        [[ "$key" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]] || continue

        # Strip surrounding quotes
        value="${value#\"}"
        value="${value%\"}"
        value="${value#\'}"
        value="${value%\'}"

        export "$key=$value"
    done < "$env_file"
}
```

```bash
# WRONG: Sourcing .env directly (insecure, executes arbitrary code)
source .env                  # If .env contains "$(rm -rf /)", it runs
. .env                       # Same problem
```

### INI-Style Config Parsing

```bash
# CORRECT: Simple INI parser
parse_ini() {
    local file="$1"
    local section=""

    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ -z "$line" || "$line" =~ ^[[:space:]]*[#\;] ]] && continue

        # Section header
        if [[ "$line" =~ ^\[([a-zA-Z0-9_-]+)\] ]]; then
            section="${BASH_REMATCH[1]}"
            continue
        fi

        # Key-value pair
        if [[ "$line" =~ ^([a-zA-Z_][a-zA-Z0-9_]*)=(.*)$ ]]; then
            local key="${BASH_REMATCH[1]}"
            local value="${BASH_REMATCH[2]}"
            # Strip inline comments
            value="${value%%#*}"
            # Trim trailing whitespace
            value="${value%"${value##*[![:space:]]}"}"

            if [[ -n "$section" ]]; then
                printf '%s_%s=%s\n' "$section" "$key" "$value"
            else
                printf '%s=%s\n' "$key" "$value"
            fi
        fi
    done < "$file"
}

# Usage: eval "$(parse_ini config.ini)"
# Produces: section_key=value variables
```

## Signal Handling Patterns

### Graceful Shutdown

```bash
# CORRECT: Handle SIGTERM and SIGINT for graceful shutdown
shutdown_requested=false

handle_signal() {
    log "Shutdown requested, finishing current work..."
    shutdown_requested=true
}

trap handle_signal SIGTERM SIGINT

# Main processing loop checks the flag
while [[ "$shutdown_requested" == "false" ]]; do
    process_next_item || sleep 1
done

log "Graceful shutdown complete"
```

```bash
# WRONG: Immediate exit on signal (may leave work half-done)
trap 'exit 1' SIGTERM SIGINT

while true; do
    process_next_item       # Interrupted mid-operation
done
```

### Signal Forwarding to Child Processes

```bash
# CORRECT: Forward signals to child process
child_pid=""

forward_signal() {
    if [[ -n "$child_pid" ]]; then
        kill -TERM "$child_pid" 2>/dev/null || true
    fi
}
trap forward_signal SIGTERM SIGINT

some_long_command &
child_pid=$!
wait "$child_pid"
exit_code=$?
child_pid=""
exit "$exit_code"
```

## Summary Checklist

When implementing shell script patterns:

- [ ] Argument parsing validates all input before use
- [ ] Logging functions send diagnostics to stderr
- [ ] Color output checks for terminal with `[[ -t 2 ]]`
- [ ] Trap EXIT handles cleanup for all temporary resources
- [ ] Temp files use `mktemp` in a single temp directory
- [ ] Atomic writes use temp-then-move pattern
- [ ] SCRIPT_DIR uses `${BASH_SOURCE[0]}` (bash) or `$0` (sh)
- [ ] Lock files use `mkdir` for atomic creation
- [ ] Retries have max attempts, backoff, and timeout
- [ ] Service readiness checks have timeouts
- [ ] .env loading validates key format, strips quotes, avoids sourcing
- [ ] Cross-platform helpers detect OS and provide fallbacks
- [ ] Signal handlers allow graceful shutdown of long-running processes

These patterns are the building blocks of reliable shell automation.
