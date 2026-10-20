# Claude Automation Script Patterns

**Purpose:** Claude-specific patterns for generating and optimizing automation scripts.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic scripts guide.

---

## Claude's Scripting Strengths

Claude excels at automation scripts because:

- **Cross-platform awareness** - Handles bash/zsh differences, Windows compatibility
- **Error handling** - Comprehensive error checking and user feedback
- **Idempotency** - Scripts that can run multiple times safely
- **Documentation** - Clear inline comments and usage instructions
- **Best practices** - Applies shell scripting best practices automatically

---

## Bash Script Generation with Claude

### Complete Script Request Pattern

```markdown
# Script Generation Request

## Purpose
[What the script should do]

## Requirements
- **Shell:** bash (must work on macOS and Linux)
- **Idempotent:** Can run multiple times safely
- **Error handling:** Fail fast with clear messages
- **User feedback:** Progress indicators
- **Safety:** Confirm destructive operations

## Functionality
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Inputs
- Arguments: [list expected arguments]
- Environment variables: [if any]
- Configuration: [where config comes from]

## Outputs
- Success: [what happens on success]
- Failure: [what happens on failure]
- Side effects: [files created, services started, etc.]

## Error Conditions
- [Condition 1]: [how to handle]
- [Condition 2]: [how to handle]

## Example Usage
```bash
./script-name.sh [args]
# Expected output...
```

---

Claude, generate robust bash script:
1. Strict error handling (set -euo pipefail)
2. Input validation
3. Comprehensive error messages
4. Progress feedback
5. Inline documentation
6. Idempotent operations
```

### Expected Script Pattern

```bash
#!/usr/bin/env bash
#
# script-name.sh - Brief description
#
# Usage:
#   ./script-name.sh [options] <argument>
#
# Options:
#   -h, --help     Show this help message
#   -v, --verbose  Enable verbose output
#
# Example:
#   ./script-name.sh my-argument
#
# Requirements:
#   - bash 4.0+
#   - [other dependencies]

set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'        # Safe word splitting

# Script directory (for relative paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
VERBOSE=false
DRY_RUN=false

#################################################################
# Functions
#################################################################

# Show usage information
usage() {
    sed -n '2,/^$/s/^# \?//p' "$0"
    exit "${1:-0}"
}

# Log message to stderr
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Log verbose message
log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        log "VERBOSE: $*"
    fi
}

# Error message and exit
error() {
    log "ERROR: $*"
    exit 1
}

# Success message
success() {
    log "SUCCESS: $*"
}

# Check if command exists
require_command() {
    local cmd="$1"
    if ! command -v "$cmd" &> /dev/null; then
        error "Required command not found: $cmd"
    fi
}

#################################################################
# Validation
#################################################################

# Check requirements
require_command "python"
require_command "git"

# Validate environment
if [[ ! -d "$PROJECT_ROOT/src" ]]; then
    error "Project source directory not found: $PROJECT_ROOT/src"
fi

#################################################################
# Main Logic
#################################################################

main() {
    log "Starting script execution"

    # Implementation here
    log_verbose "Performing step 1"
    # ...

    success "Script completed successfully"
}

#################################################################
# Parse Arguments
#################################################################

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            log "Dry run mode enabled"
            shift
            ;;
        -*)
            error "Unknown option: $1"
            ;;
        *)
            # Positional argument
            ARG="$1"
            shift
            ;;
    esac
done

#################################################################
# Execute
#################################################################

main "$@"
```

---

## Idempotent Script Patterns

### Pattern: Check Before Modify

```markdown
"Generate idempotent script for [operation]:

The script should:
1. Check if operation already completed
2. Skip if already done
3. Perform operation only if needed
4. Be safe to run multiple times

Example:
```bash
# Check if already exists
if [[ -f "$FILE" ]]; then
    log \"File already exists, skipping\"
    exit 0
fi

# Create file
touch \"$FILE\"
```
```

### Pattern: Cleanup on Failure

```markdown
"Add cleanup logic to script:

On failure, the script should:
1. Undo partial changes
2. Remove temporary files
3. Restore original state
4. Provide recovery instructions

Use trap for cleanup:
```bash
cleanup() {
    # Cleanup logic
}
trap cleanup EXIT ERR
```
```

---

## Error Handling Patterns

### Comprehensive Error Handling

```markdown
"Enhance error handling in script:

Current script:
[Paste script]

Add:
1. Validate all inputs upfront
2. Check command exit codes
3. Provide specific error messages
4. Suggest fixes for common errors
5. Log errors with context

Use pattern:
```bash
if ! command_that_might_fail; then
    error \"Command failed: [specific reason]
    Possible fix: [suggestion]\"
fi
```
```

### Expected Error Pattern

```bash
# Comprehensive error handling
validate_input() {
    local arg="$1"

    # Check not empty
    if [[ -z "$arg" ]]; then
        error "Argument required. Usage: $0 <argument>"
    fi

    # Check format/constraints
    if [[ ! "$arg" =~ ^[a-z-]+$ ]]; then
        error "Invalid format: '$arg'
        Expected: lowercase letters and hyphens only
        Example: my-project-name"
    fi

    # Check file/directory constraints
    if [[ -e "$arg" ]]; then
        error "Path already exists: $arg
        Please choose a different name or remove existing"
    fi
}

# Execute with validation
validate_input "$ARG"
```

---

## Progress Feedback Patterns

### User-Friendly Progress

```markdown
"Add progress indicators to long-running script:

Script performs:
1. [Long operation 1] (30 seconds)
2. [Long operation 2] (1 minute)
3. [Long operation 3] (2 minutes)

Add:
- Progress messages for each step
- Spinner for long operations
- Time estimates
- Success/failure indicators

Make it clear what's happening and how long it might take."
```

### Progress Pattern

```bash
# Progress feedback utilities
spinner() {
    local pid=$1
    local msg="$2"
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'

    while kill -0 "$pid" 2>/dev/null; do
        for i in $(seq 0 9); do
            echo -ne "\r${spin:i:1} $msg"
            sleep 0.1
        done
    done
    echo -ne "\r✓ $msg\n"
}

# Usage
log "Step 1/3: Building project..."
make build &
spinner $! "Building..."

log "Step 2/3: Running tests..."
make test &
spinner $! "Testing..."

log "Step 3/3: Packaging..."
make package &
spinner $! "Packaging..."

success "All steps completed"
```

---

## Justfile Task Generation

### Just Command Request

```markdown
# Justfile Task Generation

Generate just command for: [task]

Requirements:
- Task name: [name]
- Description: [what it does]
- Dependencies: [other tasks it depends on]
- Parameters: [if any]
- Cross-platform: Works on macOS, Linux, Windows

Example usage:
```bash
just [task-name] [args]
```

Follow patterns in existing justfile.
```

### Expected Just Pattern

```just
# Task description
task-name arg1 arg2="default":
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Performing {{task-name}}..."
    # Task logic here

# Compound task with dependencies
compound-task: dependency1 dependency2
    @echo "Running compound task"
    # Runs after dependencies complete

# Cross-platform command
install:
    #!/usr/bin/env bash
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install package
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        apt-get install package
    else
        echo "Unsupported OS"
        exit 1
    fi
```

---

## Python Utility Script Patterns

### Python Script Request

```markdown
"Generate Python utility script for [task]:

Advantages of Python for this task:
- Better error handling
- Cross-platform
- Access to project dependencies

Requirements:
- Use argparse for CLI
- Type hints
- Comprehensive error messages
- Can import from {{ package_name }}

Structure:
```python
#!/usr/bin/env python3
\"\"\"
script-name.py - Description

Usage:
    python script-name.py [options] <arg>
\"\"\"

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # Define arguments
    args = parser.parse_args()
    # Implementation

if __name__ == \"__main__\":
    main()
```
```

---

## Common Script Patterns for {{ project_name }}

### Pattern: Project Setup Script

```markdown
"Generate setup script for {{ project_name }}:

The script should:
1. Check Python version ({{ python_version }}+)
2. Create virtual environment
3. Install dependencies (pip install -e .[dev])
4. Initialize git hooks (if pre-commit)
5. Verify installation (run tests)
6. Print next steps

Idempotent: Can run multiple times safely
User-friendly: Clear progress and error messages"
```

### Pattern: Test Runner Script

```markdown
"Generate test runner script:

Features:
- Quick test (fast subset)
- Full test (all tests)
- Coverage report
- Watch mode (rerun on changes)
- Specific test selection

Usage:
```bash
./scripts/test.sh            # Quick tests
./scripts/test.sh --full     # All tests
./scripts/test.sh --watch    # Watch mode
./scripts/test.sh tests/test_file.py  # Specific file
```
```

### Pattern: Release Script

```markdown
"Generate release automation script:

Steps:
1. Validate working directory clean
2. Run tests
3. Update version in files
4. Update CHANGELOG
5. Create git tag
6. Push to remote
7. Create GitHub release (via gh CLI)

Safety:
- Confirm before each destructive operation
- Rollback on failure
- Validate at each step"
```

---

## Script Testing with Claude

### Generate Test Cases

```markdown
"Create test cases for script:

Script: [path to script]
[Paste script]

Generate test scenarios:
1. Happy path (valid inputs)
2. Error cases (invalid inputs)
3. Edge cases (empty, special characters)
4. Idempotency (run twice, same result)

Use bats (Bash Automated Testing System) or plain bash assertions."
```

### BATS Test Pattern

```bash
#!/usr/bin/env bats
# test-script.bats

setup() {
    # Setup test environment
    export TEST_DIR="$(mktemp -d)"
}

teardown() {
    # Cleanup
    rm -rf "$TEST_DIR"
}

@test "script succeeds with valid input" {
    run ./scripts/script-name.sh valid-arg
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = "Expected output" ]
}

@test "script fails with invalid input" {
    run ./scripts/script-name.sh invalid!arg
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Invalid format" ]]
}

@test "script is idempotent" {
    # Run once
    run ./scripts/script-name.sh test-arg
    [ "$status" -eq 0 ]

    # Run again, should still succeed
    run ./scripts/script-name.sh test-arg
    [ "$status" -eq 0 ]
}
```

---

## Script Optimization

### Performance Optimization

```markdown
"Optimize slow script:

Current runtime: [X minutes]
Target: [Y minutes]

Script:
[Paste script]

Bottlenecks:
- [Slow operation 1]
- [Slow operation 2]

Optimize:
1. Parallelize independent operations
2. Cache expensive computations
3. Reduce file I/O
4. Optimize subprocess calls

Show before/after timing."
```

### Safety Optimization

```markdown
"Make script safer:

Current script:
[Paste script]

Safety concerns:
- [Concern 1]
- [Concern 2]

Add safety features:
1. Input validation
2. Destructive operation confirmation
3. Dry-run mode
4. Backup before modifications
5. Atomic operations
6. Rollback on failure"
```

---

## Troubleshooting Scripts

### Debug Request Pattern

```markdown
"Debug failing script:

Script: [path]
Error:
```
[Paste error output]
```

Context:
- OS: [macOS/Linux/Windows]
- Shell: [bash version]
- Environment: [relevant env vars]
- Recent changes: [what changed]

Expected behavior: [what should happen]
Actual behavior: [what happens]

Claude, diagnose and fix."
```

---

## Cross-Platform Considerations

### Platform-Specific Code

```markdown
"Make script cross-platform:

Current script (Linux-only):
[Paste script]

Needs to work on:
- macOS
- Linux
- Windows (Git Bash)

Handle differences in:
- Commands (gnu vs bsd)
- Paths (/ vs \)
- Line endings
- Available tools

Use platform detection:
```bash
if [[ \"$OSTYPE\" == \"darwin\"* ]]; then
    # macOS
elif [[ \"$OSTYPE\" == \"linux-gnu\"* ]]; then
    # Linux
elif [[ \"$OSTYPE\" == \"msys\" ]]; then
    # Windows Git Bash
fi
```
```

---

## Best Practices for Claude Script Requests

### ✅ Do's

1. **Specify requirements** - Shell, compatibility, constraints
2. **Provide examples** - Show expected usage and output
3. **Request idempotency** - Scripts that can run multiple times
4. **Ask for error handling** - Comprehensive error checking
5. **Include documentation** - Usage comments and help text
6. **Request validation** - Input validation upfront
7. **Ask for feedback** - Progress messages for long operations

### ❌ Don'ts

1. **Don't skip validation** - Validate inputs before processing
2. **Don't ignore errors** - Handle all error conditions
3. **Don't hard-code paths** - Use variables and detection
4. **Don't assume tools** - Check dependencies exist
5. **Don't forget cleanup** - Use trap for cleanup
6. **Don't skip documentation** - Scripts need usage docs

---

**See Also:**
- [../CLAUDE.md](../CLAUDE.md) - Project-level Claude patterns
- [AGENTS.md](AGENTS.md) - Generic scripts guide
- [../../claude/FRAMEWORK_TEMPLATES.md](../../claude/FRAMEWORK_TEMPLATES.md) - Task templates in pattern library

---

**Version:** 3.3.0
**Last Updated:** 2025-10-26
