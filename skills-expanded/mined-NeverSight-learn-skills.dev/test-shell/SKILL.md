---
name: test-shell
description: BATS shell script testing. Use when writing or running shell script tests. Covers setup/teardown, assertions, mocking, helper patterns, and coverage with kcov.
---

# Shell Testing with BATS

BATS (Bash Automated Testing System) for testing shell scripts and libraries.

## Run Commands

```bash
# Run all tests recursively
bats --recursive tests/bats/

# Run specific test file
bats tests/bats/unit/lib/test_log.bats

# Run with TAP output (for CI)
bats --tap tests/bats/

# Run with timing info
bats --timing tests/bats/

# Filter tests by name pattern
bats --filter "validate_semver" tests/bats/

# Run in parallel
bats --jobs 4 tests/bats/
```

## Directory Structure

```text
tests/
├── bats/
│   ├── unit/
│   │   └── lib/
│   │       ├── test_log.bats
│   │       ├── test_fs.bats
│   │       ├── github/
│   │       │   └── test_output.bats
│   │       └── release/
│   │           └── test_version.bats
│   └── integration/
│       └── test_actions.bats
├── helpers/
│   ├── common.bash      # Shared utilities
│   ├── mocks.bash       # Command mocking
│   └── github_env.bash  # GitHub Actions simulation
└── fixtures/
    └── json/            # Test data files
```

## Test File Template

```bash
#!/usr/bin/env bats
# SPDX-License-Identifier: MIT
# Purpose: Tests for scripts/ci/lib/example.sh

load "../helpers/common"
load "../helpers/mocks"

setup() {
    setup_temp_dir
    export LIB_DIR
}

teardown() {
    teardown_temp_dir
}

# =============================================================================
# Function group description
# =============================================================================

@test "function_name: does expected thing" {
    run bash -c 'source "$LIB_DIR/example.sh" && function_name "arg"'
    assert_success
    assert_output "expected output"
}

@test "function_name: handles edge case" {
    run bash -c 'source "$LIB_DIR/example.sh" && function_name ""'
    assert_failure
    assert_output --partial "error message"
}
```

## Assertions (bats-assert)

```bash
# Exit code assertions
assert_success              # Exit code 0
assert_failure              # Exit code != 0

# Output assertions
assert_output "exact match"
assert_output --partial "substring"
assert_output --regexp "pattern.*here"
refute_output               # Output is empty
refute_output --partial "not present"

# Line assertions (for multiline output)
assert_line "exact line"
assert_line --partial "substring in any line"
assert_line --index 0 "first line"

# Equality
assert_equal "$expected" "$actual"
```

## File Assertions (bats-file)

```bash
assert_file_exists "/path/to/file"
assert_file_not_exists "/path/to/file"
assert_dir_exists "/path/to/dir"
assert_file_contains "/path/to/file" "expected content"
```

## Setup and Teardown

```bash
# Per-test setup/teardown
setup() {
    setup_temp_dir           # Create $BATS_TEST_TMPDIR
    export LIB_DIR           # Make available to subshells
}

teardown() {
    teardown_temp_dir        # Clean up temp files
}

# Per-file setup/teardown (run once)
setup_file() {
    # Heavy one-time setup (e.g., start services)
}

teardown_file() {
    # One-time cleanup
}
```

## Mocking Commands

```bash
# In mocks.bash helper:
mock_command() {
    local cmd="$1"
    local output="$2"
    local exit_code="${3:-0}"

    local mock_dir="${BATS_TEST_TMPDIR}/mocks"
    mkdir -p "$mock_dir"

    cat > "${mock_dir}/${cmd}" <<MOCK
#!/usr/bin/env bash
echo "$output"
exit $exit_code
MOCK
    chmod +x "${mock_dir}/${cmd}"
    export PATH="${mock_dir}:$PATH"
}

# Usage in test:
@test "handles curl failure" {
    mock_command "curl" "Connection refused" 1
    run my_download_function "http://example.com"
    assert_failure
}
```

## Testing with Bash 4+ Features

macOS ships with Bash 3.2. For tests requiring Bash 4+ features:

```bash
# In common.bash:
bash4_available() {
    [[ "${BASH4_AVAILABLE:-0}" -eq 1 ]]
}

# In tests:
@test "feature requiring bash 4+" {
    if ! bash4_available; then
        skip "requires bash 4+"
    fi
    # ... test code using ${var,,} or associative arrays
}
```

## GitHub Actions Environment Simulation

```bash
# In github_env.bash helper:
setup_github_env() {
    export GITHUB_OUTPUT="${BATS_TEST_TMPDIR}/github_output"
    export GITHUB_ENV="${BATS_TEST_TMPDIR}/github_env"
    export GITHUB_STEP_SUMMARY="${BATS_TEST_TMPDIR}/step_summary"
    touch "$GITHUB_OUTPUT" "$GITHUB_ENV" "$GITHUB_STEP_SUMMARY"
}

# Assert GitHub output was set:
get_github_output() {
    local key="$1"
    grep "^${key}=" "$GITHUB_OUTPUT" | cut -d= -f2-
}

@test "sets github output" {
    setup_github_env
    run bash -c 'source "$LIB_DIR/github/output.sh" && set_github_output "key" "value"'
    assert_success
    assert_equal "value" "$(get_github_output "key")"
}
```

## Coverage with kcov

```bash
# Run with coverage
kcov --include-path=scripts/ci/lib coverage-report bats tests/bats/

# CI workflow configuration
coverage: true
coverage-threshold: 80
upload-coverage: true
```

## Best Practices

1. **One assertion focus per test** - Test one behavior, use descriptive names
2. **Use setup/teardown** - Never leave temp files behind
3. **Isolate tests** - Each test should work independently
4. **Mock external commands** - Don't depend on network/external state
5. **Group related tests** - Use comment headers to organize
6. **Test edge cases** - Empty strings, missing files, invalid input
7. **Keep tests fast** - Avoid sleep, minimize I/O

## Common Patterns

### Testing Exit Codes

```bash
@test "die: exits with code 1" {
    run bash -c 'source "$LIB_DIR/log.sh" && die "error"'
    assert_failure
    assert_equal "1" "$status"
}
```

### Testing stderr vs stdout

```bash
@test "logs to stderr" {
    run bash -c 'source "$LIB_DIR/log.sh" && log_error "msg" 2>&1'
    assert_output --partial "ERROR"
}
```

### Testing Function Exports

```bash
@test "function is exported" {
    source "$LIB_DIR/example.sh"
    run bash -c "declare -F my_function"
    assert_success
}
```

### Skipping Tests

```bash
@test "requires specific tool" {
    command -v special_tool >/dev/null || skip "special_tool not installed"
    # ... test code
}
```
