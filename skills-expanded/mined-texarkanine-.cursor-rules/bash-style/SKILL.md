---
name: "bash-style"
description: "Required style guidelines for writing shell scripts where POSIX-compliance is not an explicit requirement"
---


# Bash Script Style Guide

## When to Use Shell

Shell should only be used for small utilities or simple wrapper scripts:

- **Use shell when**: You're mostly calling other utilities and doing relatively little data manipulation
- **Don't use shell when**: Performance matters, or you're writing scripts longer than 100 lines
- **Consider rewriting**: Scripts with non-straightforward control flow logic should be rewritten in a more structured language

The complexity threshold is about maintainability by people other than the author.

**IMPORTANT - LACK OF POSIX COMPLIANCE:** *This rule only applies when POSIX-compatibility is NOT a requirement.* These guidelines are specifically for bash-based shell scripts that can leverage bash-specific features and "bashisms."

## Core Requirements

### 1. Shebang and Shell Selection

**Always use bash for executable scripts:**

```bash
#!/bin/bash
# Minimal flags approach - use 'set' for shell options instead
```

**Use 'set' for shell options:**

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined variables, pipe failures
```

### 2. File Extensions

- **Executables**: Use `.bash` extension OR no extension
	- Use `.bash` if build rules will rename the file
	- Use no extension if script goes directly into user's PATH
- **Libraries**: Must have `.bash` extension and should NOT be executable

### 3. File Header Comments

Every file must start with a description:

```bash
#!/bin/bash
#
# Backup utility for PostgreSQL databases
# Performs incremental backups and uploads to S3
#
# Usage: backup_postgres.sh [database_name]
# 
# Copyright 2024 Company Name
# Author: developer@company.com
```

## Formatting Standards

### 1. Indentation

**Use tabs for initial indentation:**

```bash
if [[ "${1}" == "start" ]]; then
	echo "Starting service..."
	if systemctl start myservice; then
		echo "Service started successfully"
	else
		echo "Failed to start service" >&2
		return 1
	fi
fi
```

**Use spaces for subsequent indentation:**

This is rare; usually only used for visual alignment.

```bash
if [[ "${1}" == "start" ]]; then
	echo "Starting service..."
	if systemctl start myservice; then
		# the following lines align function inputs w/ spaces
		report_start    "myservice"
		log             "myservice started"
		monitor_service "myservice"
	else
		echo "Failed to start service" >&2
		return 1
	fi
fi
```

**ALWAYS use spaces for indentation within multi-line comments!**

```bash
if [[ "${1}" == "start" ]]; then
	echo "Starting service..."
	if systemctl start myservice; then
		echo "Service started successfully"
	else
		echo "Failed to start service" >&2
		# we aren't sure why it failed b/c the service
		# doesn't integrate w/ systemctl properly. Could be
		#   - bad config
		#   - network error
		#   - intermittent i/o
		return 1
	fi
fi
```


### 2. Line Length

Keep lines under 80 characters **when possible:**

- DO NOT compromise readability or maintainability just to stay under 80, especially where subshells come into play
- PREFER to break sentences at sentence ends or logical subjects, rather than just at 80 characters
- PREFER to let a line go a little bit above 80 rather than having a stupid-short 2nd line

**Break lines logically, not arbitrarily at 80 characters:**

```bash
# Good - break at logical points
if [[ "${enable_logging}" == "true" ]] && [[ -w "${log_directory}" ]]; then
	echo "Logging enabled to ${log_directory}"
fi

# Bad - breaking in the middle of a logical condition
if [[ "${enable_logging}" == "true" ]] && [[ -w "${log_directory}" \
]]; then
	echo "Logging enabled to ${log_directory}"
fi
```

**Prefer slightly longer lines over awkwardly short continuation lines:**

```bash
# Good - let it go a bit over 80 rather than create a short second line
echo "Processing configuration file: ${config_file} with options: ${options}"

# Bad - creates an awkwardly short second line
echo "Processing configuration file: ${config_file} with options: \
${options}"
```

**For long commands, use line continuation with proper indentation:**

```bash
# Good - logical breaks with consistent indentation
command \
	--option1 value1 \
	--option2 value2 \
	--option3 value3

# Bad - breaks at arbitrary character limits
command --option1 value1 --option2 value2 \
--option3 value3
```

**For long strings, use here documents:**

```bash
# Good - here document for multi-line content
cat <<EOF
This is a long message that would exceed the 80 character limit 
if written on one line.
EOF

# Bad - awkward line continuation for strings
echo "This is a long message that would exceed \
the 80 character limit if written on one line."
```

**Break sentences at natural boundaries:**

```bash
# Good - break at sentence boundaries using heredoc
cat <<EOF
Starting backup process for database ${db_name}.
This may take several minutes depending on database size.
EOF

# Bad - break mid-sentence at character limit
cat <<EOF
Starting backup process for database ${db_name}. This may take
several minutes depending on database size.
EOF
```

### 3. Pipelines

Put pipelines on separate lines when they become long:

```bash
# Short pipeline - single line is fine
ps aux | grep nginx

# Long pipeline - break it up
command1 \
	| command2 \
	| command3 \
	| command4
```

### 4. Control Flow

**Use proper spacing and alignment:**

```bash
# if statements
if [[ "${condition}" ]]; then
	# code
elif [[ "${other_condition}" ]]; then
	# code
else
	# code
fi

# for loops
for file in "${files[@]}"; do
	process_file "${file}"
done

# while loops  
while read -r line; do
	echo "Processing: ${line}"
done < "${input_file}"
```

### 5. Case Statements

**Align and indent consistently:**

```bash
case "${1}" in
	start)
		start_service
		;;
	stop)
		stop_service
		;;
	restart)
		stop_service
		start_service
		;;
	*)
		echo "Usage: ${0} {start|stop|restart}" >&2
		exit 1
		;;
esac
```

## Variable and Quoting Rules

### 1. Variable Expansion

**Always use braces for variable expansion:**

```bash
# Good
echo "Hello ${name}!"
echo "File: ${file}.backup"

# Bad
echo "Hello $name!"
echo "File: $file.backup"
```

### 2. Quoting

**Quote variables to prevent word splitting:**

```bash
# Good
if [[ -f "${config_file}" ]]; then
	cp "${config_file}" "${backup_dir}/"
fi

# Bad - can break with spaces in filenames
if [[ -f $config_file ]]; then
	cp $config_file $backup_dir/
fi
```

**Quote all strings except in specific contexts:**

```bash
# Good
echo "Starting process: ${process_name}"
grep "pattern" "${file}"

# Arithmetic context doesn't need quotes
(( count = count + 1 ))
if (( count > 10 )); then
	echo "Count exceeded limit"
fi
```

## Function Standards

### 1. Function Names

**Use lowercase with underscores (snake_case):**

```bash
# Single function
process_file() {
	local file="${1}"
	# implementation
}
```

### 2. Function Structure and Documentation

**Use consistent formatting with comprehensive documentation:**

Any function that is not both obvious and short must have a function header comment. All functions in libraries must have a function header comment regardless of length or complexity.

All function header comments must describe the intended API behavior using these required sections (always present, even if not applicable):

- **Description**: What the function does
- **Globals**: List of global variables used and modified  
- **Arguments**: Arguments taken
- **Outputs**: Output to STDOUT or STDERR
- **Returns**: Returned values other than the default exit status

```bash
# Processes a log file and extracts error messages
#
# Globals:
#   LOG_LEVEL - Used to determine verbosity (read-only)
#   ERROR_COUNT - Modified to track total errors found
# Arguments:
#   $1 - Path to log file (required)
#   $2 - Output format: 'json' or 'text' (optional, defaults to 'text')
# Outputs:
#   Error messages to STDOUT
#   Error details and warnings to STDERR
# Returns:
#   0 on success
#   1 on file not found
#   2 on invalid format
process_log_file() {
	local log_file="${1}"
	local format="${2:-text}"
	
	# Validate input
	if [[ ! -f "${log_file}" ]]; then
		echo "Error: Log file '${log_file}' not found" >&2
		return 1
	fi
	
	if [[ "${format}" != "text" && "${format}" != "json" ]]; then
		echo "Error: Invalid format '${format}'. Use 'text' or 'json'" >&2
		return 2
	fi
	
	# Process the file
	case "${format}" in
		json)
			grep "ERROR" "${log_file}" \
				| sed 's/^.*ERROR: //' \
				| sort -u \
				| jq -R '{"error": .}'
			;;
		text)
			grep "ERROR" "${log_file}" \
				| sed 's/^.*ERROR: //' \
				| sort -u
			;;
	esac
	
	return 0
}

# Simple utility function demonstrating all required sections
#
# Globals:
#   None
# Arguments:
#   $1 - Message to display (required)
# Outputs:
#   Formatted message to STDOUT
# Returns:
#   Always returns 0 (default exit status)
display_message() {
	local message="${1}"
	echo "INFO: ${message}"
}
```

### 3. Local Variables

**Always use local variables in functions:**

```bash
process_data() {
	local input_file="${1}"
	local output_file="${2}"
	local temp_file
	
	# Separate declaration and assignment for command substitution
	temp_file="$(mktemp)"
	
	# Process data
	sort "${input_file}" > "${temp_file}"
	mv "${temp_file}" "${output_file}"
}
```

## Naming Conventions

### 1. Variables

**Use lowercase with underscores (snake_case):**

```bash
user_name="john_doe"
config_file="/etc/myapp/config.conf"
temp_directory="/tmp/myapp_$$"
```

### 2. Constants and Environment Variables

**Use uppercase with underscores:**

```bash
readonly CONFIG_DIR="/etc/myapp"
readonly MAX_RETRIES=3
declare -xr LOG_LEVEL="INFO"
```

### 3. Loop Variables

**Name descriptively:**

```bash
# Good
for zone in "${availability_zones[@]}"; do
	deploy_to_zone "${zone}"
done

# Bad
for i in "${availability_zones[@]}"; do
	deploy_to_zone "${i}"
done
```

## Error Handling and Return Values

### 1. Check Return Values

**Always check command return values:**

```bash
# Using if statement
if ! mv "${source_file}" "${dest_dir}/"; then
	echo "Error: Unable to move ${source_file} to ${dest_dir}" >&2
	exit 1
fi

# Using $? variable
cp "${file}" "${backup_location}"
if (( $? != 0 )); then
	echo "Error: Failed to backup ${file}" >&2
	exit 1
fi
```

### 2. Pipeline Error Handling

**Use PIPESTATUS for pipeline error checking:**

```bash
tar -czf - "${directory}" | ssh user@host "cat > backup.tar.gz"
if (( PIPESTATUS[0] != 0 || PIPESTATUS[1] != 0 )); then
	echo "Error: Backup pipeline failed" >&2
	exit 1
fi

# For complex pipelines, capture PIPESTATUS immediately
long_command | filter_command | output_command
return_codes=( "${PIPESTATUS[@]}" )
if (( return_codes[0] != 0 )); then
	echo "Error: long_command failed" >&2
elif (( return_codes[1] != 0 )); then
	echo "Error: filter_command failed" >&2
fi
```

### 3. Error Reporting

**Send errors to STDERR with timestamps:**

```bash
# Error reporting function
err() {
	echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# Usage
if ! create_backup "${database}"; then
	err "Failed to create backup for database: ${database}"
	exit 1
fi
```

### 4. Returning Values

**When returning status from a function, use numerical return codes:**

```bash
# Good - status uses exit codes
is_even() {
	# Checks if the input number is even
	if (( ${1} % 2 == 0 )); then
		return 0 # it's even
	else
		return 1 # it's not even
	fi
}

# Bad - unnecessary string use for status
file_exists() {
	# Checks if the given file exists
	if [[ -f "${1}" ]]; then
		echo "true" # it exists
	else
		echo "false" # it doesn't exist
	fi
}
```

**When returning strings from a function with stdout, ensure that the function only ever returns the proper string:**

```bash
# Good - redirect useful output from stdout to stderr
mentions_cursor() {
	git fetch --all >&2
	if grep -q -lr "cursor"; then
		echo "true"
	else
		echo "false"
	fi
}

# Good - redirect unneeded stdout to /dev/null
mentions_cursor() {
	if grep -lr "cursor" . >/dev/null; then
		echo "true"
	else
		echo "false"
	fi
}

# Bad - silence output with a flag (cannot guarantee ALL stdout is silenced)
mentions_cursor() {
	if grep -q -lr "cursor"; then
		echo "true"
	else
		echo "false"
	fi
}

# Bad - output will contain extraneous content, not just the function's intended return value
mentions_cursor() {
	if grep -lr "cursor"; then
		echo "true"
	else
		echo "false"
	fi
}
```

## Feature Usage Guidelines

### 1. Command Substitution

**Use $(...) instead of backticks:**

```bash
# Good
current_date="$(date '+%Y-%m-%d')"
file_count="$(find "${dir}" -type f | wc -l)"

# Bad
current_date=`date '+%Y-%m-%d'`
file_count=`find "${dir}" -type f | wc -l`
```

### 2. Test Constructs

**Prefer [[ ]] over [ ]:**

```bash
# Use [[ ]] for bash-specific features
if [[ "${file}" =~ \.txt$ ]]; then
	echo "Text file detected"
fi

if [[ -n "${variable}" && "${variable}" != "default" ]]; then
	process_variable "${variable}"
fi

# String testing examples
if [[ -z "${string}" ]]; then          # Empty string
	echo "String is empty"
fi

if [[ "${string1}" == "${string2}" ]]; then  # String equality
	echo "Strings are equal"
fi

# File testing
if [[ -f "${file}" ]]; then            # File exists and is regular file
	echo "File exists"
fi

if [[ -d "${directory}" ]]; then       # Directory exists
	echo "Directory exists"
fi
```

### 3. Arithmetic

**Use (( )) for arithmetic operations:**

```bash
# Arithmetic evaluation
(( total = count * price ))
(( i += 1 ))

# Arithmetic conditions
if (( count > threshold )); then
	echo "Threshold exceeded"
fi

# Avoid external tools for simple arithmetic
# Good: (( result = 10 * 5 ))
# Bad: result="$(expr 10 \* 5)"
```

### 4. Arrays

**Use bash arrays when appropriate:**

```bash
# Declare and populate arrays
declare -a files
files=( "/path/one" "/path/two" "/path/three" )

# Better: direct assignment
files=( 
	"/path/one" 
	"/path/two" 
	"/path/three" 
)

# Iterate over arrays
for file in "${files[@]}"; do
	echo "Processing: ${file}"
done

# Array length
echo "Total files: ${#files[@]}"
```

## Main Function Pattern

**Use main function for excecutable scripts with multiple functions:**

```bash
#!/bin/bash

# Function definitions
setup_environment() {
	# Setup code
}

process_arguments() {
	# Argument processing
}

cleanup() {
	# Cleanup code
}

# Main function
main() {
	setup_environment
	process_arguments "$@"

	# Main script logic here

	cleanup
}

# IMPORTANT - Only run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	main "$@"
fi
```

## Security Considerations

### 1. Avoid SUID/SGID

**Never use SUID/SGID on shell scripts:**

```bash
# Use sudo for elevated access instead
if ! sudo systemctl restart nginx; then
	echo "Error: Failed to restart nginx" >&2
	exit 1
fi
```

### 2. Validate Inputs

**Always validate and sanitize inputs:**

```bash
validate_input() {
	local input="${1}"

	# Check if input is provided
	if [[ -z "${input}" ]]; then
		echo "Error: Input required" >&2
		return 1
	fi

	# Validate format (example: alphanumeric only)
	if [[ ! "${input}" =~ ^[a-zA-Z0-9_]+$ ]]; then
		echo "Error: Invalid input format" >&2
		return 1
	fi

	return 0
}
```

## Built-in Preferences

**Prefer bash built-ins over external commands:**

```bash
# Good - using bash built-ins
string_length="${#variable}"
substring="${variable:0:10}"
replacement="${variable/pattern/replacement}"

# Avoid external commands when built-ins work
# Good: (( result = x + y ))
# Bad: result="$(expr "${x}" + "${y}")"

# Good: if [[ "${string}" =~ pattern ]]; then
# Bad: if echo "${string}" | grep -q pattern; then
```

## Advanced Features

### 1. Wildcard Expansion

**Be careful with filename expansion:**

```bash
# Good - explicit globbing with safeguards
for file in /path/to/files/*.txt; do
	[[ -f "${file}" ]] || continue  # Skip if no matches
	process_file "${file}"
done

# Good - disable globbing when not needed
set -f  # Disable globbing
echo "This * will not expand"
set +f  # Re-enable globbing

# Avoid unquoted expansion in dangerous contexts
# Bad: rm ${files}  # Could expand unexpectedly
# Good: rm "${files[@]}"  # Array expansion
```

### 2. Process Substitution

**Use process substitution instead of pipes to while:**

```bash
# Good - using process substitution
while read -r line; do
	echo "Processing: ${line}"
done < <(some_command)

# Avoid - pipe to while (creates subshell)
some_command | while read -r line; do
	echo "Processing: ${line}"
	# Variables set here won't persist outside the loop
done
```

### 3. Here Documents and Here Strings

**Use here documents for multi-line strings:**

```bash
# Here document
cat <<EOF
This is a multi-line
string that can contain
variable substitutions: ${variable}
EOF

# Here document with no substitution
cat <<'EOF'
This text is literal:
${variable} will not be expanded
EOF

# Here string (single line)
grep "pattern" <<<"${string_to_search}"
```

## Common Pitfalls to Avoid

1. **Don't use aliases in scripts** - Use functions instead
2. **Avoid eval** - Find alternative approaches
3. **Don't ignore return values** - Always check command success
4. **Avoid pipes to while loops** - Use process substitution or arrays
5. **Extraneous stdout in functions that return strings** - redirect or discard all output except the return value
6. **Don't use ls for file operations** - Use globs or find instead
	```bash
	# Bad: using ls
	for file in $(ls *.txt); do
		process_file "${file}"
	done

	# Good: using globs
	for file in *.txt; do
		[[ -f "${file}" ]] || continue  # Skip if no matches
		process_file "${file}"
	done
	```

## Testing and Validation

**Write testable shell scripts:**

```bash
#!/bin/bash
# calculator.sh - Example of testable shell script

add() {
	echo $(( $1 + $2 ))
}

subtract() {
	echo $(( $1 - $2 ))
}

main() {
	case "${1}" in
		add) add "${2}" "${3}" ;;
		sub) subtract "${2}" "${3}" ;;
		*)   echo "Usage: ${0} {add|sub} num1 num2" >&2; exit 1 ;;
	esac
}

# Only run main if executed directly, not when sourced for testing
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	main "$@"
fi
```

**Example test file (using bats or similar):**

```bash
#!/usr/bin/env bats
# test_calculator.bats

# Source the script under test
source "$(dirname "$BATS_TEST_FILENAME")/calculator.sh"

@test "add function works correctly" {
	result="$(add 5 3)"
	[ "$result" -eq 8 ]
}

@test "subtract function works correctly" {
	result="$(subtract 10 4)"
	[ "$result" -eq 6 ]
}
```

## ShellCheck Integration

**Always use ShellCheck for static analysis:**

```bash
# Install ShellCheck
# Ubuntu/Debian: apt-get install shellcheck
# macOS: brew install shellcheck
# Or use online at: https://www.shellcheck.net/

# Run ShellCheck on your scripts
shellcheck myscript.sh

# Disable specific warnings when justified
# shellcheck disable=SC2034  # Unused variable
readonly UNUSED_VAR="value"

# Disable for entire file (use sparingly)
# shellcheck disable=SC1091  # Can't follow source
```

**Common ShellCheck fixes:**

```bash
# SC2086: Quote variables to prevent word splitting
# Bad:
cp $file $destination

# Good:
cp "${file}" "${destination}"

# SC2155: Declare and assign separately
# Bad:
local var="$(command_that_might_fail)"

# Good:
local var
var="$(command_that_might_fail)"
```

