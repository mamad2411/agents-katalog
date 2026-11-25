---
name: "shell-tdd"
description: "Required test-driven development practice for writing shell scripts"
---


# Test-Driven Development (TDD) for Shell Scripts

This rule defines best practices for AI assistants to follow when writing shell scripts using test-driven development (TDD). The AI should create shell scripts that are testable with shunit2, separate concerns, avoid side effects when being sourced, and allow functions to be tested in isolation. Following these guidelines ensures scripts can be reliably tested and maintained.

## TDD Workflow for AI Assistants

When asked to create shell scripts, the AI should follow this test-driven workflow:

1. **Write test first**: Before implementing functionality, write tests that define the expected behavior
2. **Run tests to see them fail**: Verify tests correctly identify missing functionality
3. **Implement minimum code to pass**: Create just enough functionality to pass the tests
4. **Run tests to confirm pass**: Verify the implementation satisfies the requirements
5. **Refactor code**: Improve the implementation while maintaining test coverage
6. **Repeat**: Iterate for each new feature or requirement

### Example TDD Approach

```sh
# STEP 1: First write the test file (test_calculator.sh)
#!/bin/sh

# Source script under test
. "$(dirname "${0}")/../calculator.sh"

# Test for add function
test_add() {
	result=$(add 5 3)
	assertEquals "Addition should work correctly" "8" "$result"
}

# Test for subtract function
test_subtract() {
	result=$(subtract 10 4)
	assertEquals "Subtraction should work correctly" "6" "$result"
}

# Load shunit2
. "$(dirname "${0}")/shunit2"

# STEP 2: Then implement the minimum functionality to pass the tests (calculator.sh)
#!/bin/sh

# Add two numbers
add() {
	echo $(($1 + $2))
}

# Subtract second number from first
subtract() {
	echo $(($1 - $2))
}

# Only run if executed directly
if [ "${0##*/}" = "calculator.sh" ]; then
	echo "Calculator utility"
fi
```

## Core Principles for Testable AI-Generated Shell Scripts

### 1. Entry Point Protection

Always protect the main execution code with a conditional that checks if the script is being executed directly:

```sh
# Define all functions first

# Only run main code if script is executed, not sourced
if [ "${0##*/}" = "script_name.sh" ]; then
	main "$@" # Call a main function with all arguments
fi
```

Where "script_name.sh" is the actual filename of your script. This works because:
- When executed directly: `$0` contains the script path/name
- When sourced: `$0` contains the name of the parent script doing the sourcing

This allows your script to be sourced for testing without executing its main behavior.

### 2. Function-Based Design

Structure scripts as collections of well-defined functions:

```sh
#!/bin/sh
# Example of a testable shell script

# Clear function documentation
# Adds two numbers
# Arguments:
#   $1 - First number
#   $2 - Second number
# Returns:
#   Sum of the two numbers
add_numbers() {
	echo $(( $1 + $2 ))
}

# Main function that orchestrates execution
main() {
	local result
	result="$(add_numbers 5 10)"
	echo "The result is: ${result}"
}

# Only run if executed directly (assuming script is named example.sh)
if [ "${0##*/}" = "example.sh" ]; then
	main "$@"
fi
```

### 3. Avoid Global Side Effects

- Never use `exit` outside of the main execution block
- Don't modify the environment in ways that can't be undone
- Use local variables when possible to avoid leaking state

```sh
# BAD - will terminate the test suite if sourced
validate_input() {
	if [ -z "${1}" ]; then
		echo "Error: Input required" >&2
		exit 1 # This will exit the test suite!
	fi
}

# GOOD - returns error code instead
validate_input() {
	if [ -z "${1}" ]; then
		echo "Error: Input required" >&2
		return 1  # Return error code instead
	fi
	return 0
}
```

### 4. Environment Preservation

Save and restore environment state when necessary:

```sh
backup_file() {
	# Save original state
	_original_dir="$(pwd)"
	
	# Perform operation
	cd "${1}" || return 1
	cp "${2}" "${2}.bak" || return 1
	
	# Restore original state
	cd "${_original_dir}" || return 1
	return 0
}
```

### 5. Testable I/O Handling

Make input/output operations testable by:

- Allowing output redirection
- Making file paths configurable
- Providing functions that can accept alternate inputs

```sh
# Hard to test - uses hardcoded file
process_data() {
	cat /etc/config.conf | grep "pattern"
}

# Testable - accepts input source as parameter
process_data() {
	config_file="${1:-/etc/config.conf}"
	grep "pattern" "${config_file}"
}
```

### 6. Mock-Friendly External Commands

Design for easy mocking of external commands in tests:

```sh
# Define how external commands are called
git_sync() {
	git clone "${1}" "${2}" || return 1
	return 0
}

# Use the function instead of calling git directly
update_repo() {
	repo_url="${1}"
	target_dir="${2}"
	git_sync "${repo_url}" "${target_dir}"
}

# In tests, you can mock git_sync:
# git_sync() { echo "Mock: git clone ${1} ${2}"; return 0; }
```

## Implementation Guidelines for Testing with shunit2

When the AI generates a shell script, it should:

1. **Always implement test files alongside production code**
2. **Generate appropriate test directory structure:**
   ```
   project/
   ├── scripts/
   │   └── example.sh
   └── tests/
	   ├── common.sh
	   └── unit/
		   └── example_test.sh
   ```
3. **Create comprehensive test functions for each unit of functionality**
4. **Build proper test fixtures with setUp and tearDown functions**
5. **Use appropriate assertions from shunit2**
6. **Write high-quality tests that are reliable, fast, and easy to maintain**

### Example Test Setup

```sh
# In tests/common.sh
source_script() {
	# Save original environment if needed
	_ORIGINAL_ENV_VARS="$(env)"
	
	# Source the script
	# shellcheck disable=SC1090
	. "${1}"
	
	# Verify it was sourced correctly
	if [ $? -ne 0 ]; then
		echo "Error: Failed to source ${1}" >&2
		return 1
	fi
	
	return 0
}
```

### Example Test File

```sh
#!/bin/sh
# Test file: test_example.sh

# Load common test utilities
. "$(dirname "${0}")/common.sh"

# Source the script under test
source_script "$(dirname "${0}")/../example.sh"

# Test function
test_add_numbers() {
	result="$(add_numbers 5 7)"
	assertEquals "Addition should work correctly" "12" "${result}"
}

# Load and run shunit2
. "$(dirname "${0}")/shunit2"
```

## Common Pitfalls

1. **Unconditional exits**: Using `exit` outside the main execution block will terminate test suites

	```sh
	# AVOID THIS - will break tests
	cleanup() {
		if [ ! -f "${1}" ]; then
			echo "Error: File not found" >&2
			exit 1  # BAD - will exit test suite
		fi
	}
	```

2. **Hardcoded environment assumptions**: Making assumptions about the environment

	```sh
	# AVOID THIS - assumes current directory
	process_files() {
		for file in *.txt; do  # Bad - depends on current directory
			process_file "${file}"
		done
	}

	# BETTER - accepts directory as parameter
	process_files() {
		dir="${1:-.}"  # Default to current directory but allows override
		for file in "${dir}"/*.txt; do
			process_file "${file}"
		done
	}
	```

3. **Global state modifications**: Modifying global state without restoring it

	```sh
	# AVOID THIS - changes global state without restoring
	set_environment() {
		set -e  # Will affect test environment
		export DEBUG=true  # Modifies global environment
	}

	# BETTER - localize and document effects
	set_environment() {
		# Save original state to allow restoration
		_original_debug="${DEBUG}"
		
		# Make changes
		export DEBUG=true
		
		# Return function to restore state
		restore_environment() {
			export DEBUG="${_original_debug}"
		}
	}
	```

4. **Untestable output**: Writing directly to stdout/stderr without redirection options

	```sh
	# AVOID THIS - direct output hard to test
	display_status() {
		echo "Status: ${1}"
	}

	# BETTER - allows output redirection
	display_status() {
		echo "Status: ${1}" >&${2:-1}  # Default to stdout but allows redirection
	}
	```

5. **Test function exit codes**: In shunit2 test functions, the exit code of the last command becomes the function's return value

	```sh
	# AVOID THIS - grep failure becomes test failure
	test_something() {
		# ... test code ...
		grep -q "pattern" "$file" && fail "Pattern should not exist"
		# If grep doesn't find pattern, it returns 1, which shunit2 interprets as test failure
	}

	# BETTER - explicitly return success
	test_something() {
		# ... test code ...
		grep -q "pattern" "$file" && fail "Pattern should not exist"
		return 0  # Explicitly return success to prevent false failures
	}
	```

	**Key point**: Always end test functions with `return 0` & rely on explicit invocations of `fail` to surface test failures.

## Implementation Checklist

When implementing shell scripts, always:

1. ✅ **Write test cases first** before implementing functionality
2. ✅ **Create a main function** and protect it with entry point detection
3. ✅ **Decompose logic into testable functions** with single responsibilities
4. ✅ **Use return codes instead of exit** for error handling
5. ✅ **Parameterize file paths and environment assumptions**
6. ✅ **Include clear function documentation** with args and return values
7. ✅ **Generate complete test structure** with common.sh and test files
8. ✅ **Include examples of test mocking** for external dependencies

## Real-World Test Example

```sh
#!/bin/sh
# tests/unit/functions_test.sh

# Load common test utilities
. "$(dirname "${0}")/../common.sh"

# Set up test environment
setUp() {
	# Create temporary test directory
	TEST_DIR="$(mktemp -d)"
	cd "${TEST_DIR}" || fail "Failed to change to test directory"
	
	# Create test files
	echo "test content" > test_file.txt
}

# Clean up test environment
tearDown() {
	# Return to original directory
	cd / || fail "Failed to change directory"
	
	# Remove test directory
	rm -rf "${TEST_DIR}"
}

# Source the script under test
source_script "$(dirname "${0}")/../../my_script.sh"

# Test backup_file function
test_backup_file() {
	# Call function
	backup_file "${TEST_DIR}" "test_file.txt"
	
	# Assert backup was created
	assertTrue "Backup file should exist" "[ -f 'test_file.txt.bak' ]"
	
	# Assert content was preserved
	assertEquals "Backup content should match original" \
		"$(cat test_file.txt)" "$(cat test_file.txt.bak)"
}

# Load and run shunit2
. "$(dirname "${0}")/../../shunit2"
```

