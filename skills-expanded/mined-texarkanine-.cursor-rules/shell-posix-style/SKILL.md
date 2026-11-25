---
name: "shell-posix-style"
description: "Required style guidelines for writing shell scripts where POSIX-compliance is REQUIRED"
---


# POSIX Shell Script Style Guide

## When to Use POSIX Shell

**IMPORTANT - REQUIRED POSIX COMPLIANCE:** *This rule applies when POSIX-compatibility IS a requirement.* These guidelines are specifically for shell scripts that must work across different UNIX-like systems using only POSIX-compliant features:

- **Use POSIX shell when**: You need scripts to work on various UNIX-like systems, embedded environments, or when bash availability is uncertain
- **Don't use POSIX shell when**: You can guarantee bash availability and need advanced features like arrays or associative arrays
- **Consider alternatives**: For complex scripts (>100 lines), consider using a more structured language like Python or Go
	- The complexity threshold is about maintainability by people other than the author.

## Core Requirements

### 1. Shebang and Shell Selection

**Always use POSIX sh for executable scripts:**

```sh
#!/bin/sh
# Use only POSIX-compliant features
```

**Use 'set' for POSIX shell options:**

```sh
#!/bin/sh
set -eu  # Exit on error, undefined variables (pipefail not available in POSIX)
```

### 2. File Extensions

- **Executables**: Use `.sh` extension OR no extension
	- Use `.sh` if build rules will rename the file
	- Use no extension if script goes directly into user's PATH
- **Libraries**: Must have `.sh` extension and should NOT be executable

### 3. File Header Comments

Every file must start with a description:

```sh
#!/bin/sh
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

```sh
if [ "$1" = "start" ]; then
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

```sh
if [ "$1" = "start" ]; then
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

**ALWAYS use spaces for indentation within multi-line comments:**

```sh
if [ "$1" = "start" ]; then
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

**Keep lines under 80 characters when possible:**

- DO NOT compromise readability or maintainability just to stay under 80, especially where subshells come into play
- PREFER to break sentences at sentence ends or logical subjects, rather than just at 80 characters
- PREFER to let a line go a little bit above 80 rather than having a stupid-short 2nd line

**Break lines logically, not arbitrarily at 80 characters:**

```sh
# Good - break at logical points
if [ "${enable_logging}" = "true" ] && [ -w "${log_directory}" ]; then
	echo "Logging enabled to ${log_directory}"
fi

# Bad - breaking in the middle of a logical condition
if [ "${enable_logging}" = "true" ] && [ -w "${log_directory}" \
]; then
	echo "Logging enabled to ${log_directory}"
fi
```

**Prefer slightly longer lines over awkwardly short continuation lines:**

```sh
# Good - let it go a bit over 80 rather than create a short second line
echo "Processing configuration file: ${config_file} with options: ${options}"

# Bad - creates an awkwardly short second line
echo "Processing configuration file: ${config_file} with options: \
${options}"
```

**For long commands, use line continuation with proper indentation:**

```sh
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

```sh
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

```sh
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

```sh
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

```sh
# if statements
if [ "${condition}" ]; then
	# code
elif [ "${other_condition}" ]; then
	# code
else
	# code
fi

# for loops
for file in "$@"; do
	process_file "${file}"
done

# while loops  
while read -r line; do
	echo "Processing: ${line}"
done < "${input_file}"
```

### 5. Case Statements

**Align and indent consistently:**

```sh
case "$1" in
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
		echo "Usage: $0 {start|stop|restart}" >&2
		exit 1
		;;
esac
```

## Variable and Quoting Rules

### 1. Variable Expansion

**Brace-delimit all named variables. Do not brace single-character shell specials or positional parameters unless required or avoiding confusion:**

```sh
# Good - named variables always braced
echo "Hello ${name}!"
echo "File: ${file}.backup"

# Good - specials and positional parameters unbraced
echo "Positional: $1 $2"
echo "Count: $#, status: $?"
main "$@"

# Braces required or avoiding confusion
echo "${10}"      # multi-digit positional requires braces
echo "${1}0${2}"  # digit follows the expansion

# Bad
echo "Hello $name!"
echo "File: $file.backup"
echo "Positional: ${1}"  # unnecessary braces
```

### 2. Quoting

**Quote variables to prevent word splitting:**

```sh
# Good
if [ -f "${config_file}" ]; then
	cp "${config_file}" "${backup_dir}/"
fi

# Bad - can break with spaces in filenames
if [ -f $config_file ]; then
	cp $config_file $backup_dir/
fi
```

**Quote all strings except in specific contexts:**

```sh
# Good
echo "Starting process: ${process_name}"
grep "pattern" "${file}"

# Arithmetic context using expr
count=$(expr ${count} + 1)
if [ "${count}" -gt 10 ]; then
	echo "Count exceeded limit"
fi
```

## Function Standards

### 1. Function Names

**Use lowercase with underscores (snake_case):**

```sh
# Single function
process_file() {
	file="$1"
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

```sh
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
	log_file="$1"
	format="${2:-text}"
	
	# Validate input
	if [ ! -f "${log_file}" ]; then
		echo "Error: Log file '${log_file}' not found" >&2
		return 1
	fi
	
	if [ "${format}" != "text" ] && [ "${format}" != "json" ]; then
		echo "Error: Invalid format '${format}'. Use 'text' or 'json'" >&2
		return 2
	fi
	
	# Process the file
	case "${format}" in
		json)
			grep "ERROR" "${log_file}" \
				| sed 's/^.*ERROR: //' \
				| sort -u \
				| awk '{print "{\"error\": \"" $0 "\"}"}'
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
	dm_message="$1"  # dm_ = display_message prefix
	echo "INFO: ${dm_message}"
}
```

### 3. Variable Scope

**Use function-specific variable prefixes (no `local` in POSIX):**

Since POSIX shell doesn't have `local`, all function variables are global. Use consistent prefixes to avoid conflicts. Initialize function variables to sane defaults.

```sh
summarize_log() {
	# Use function name prefix to avoid conflicts (sl_ = summarize_log)
	sl_log_file="$1"
	sl_line_count=""

	# Separate declaration and assignment for command substitution
	sl_line_count=$(wc -l < "${sl_log_file}")

	echo "INFO: ${sl_log_file} contains ${sl_line_count} lines"
}

# Alternative naming schemes:
validate_input() {
	vi_input="$1"          # vi_ = validate_input
	vi_format="${2:-text}"
	# ... function logic
}

my_package_parse_config() {
	mppc_config_file="$1"  # mppc_ = my_package_parse_config  
	mppc_section="$2"
	# ... function logic
}
```

## Naming Conventions

### 1. Variables

**Use lowercase with underscores (snake_case):**

```sh
user_name="john_doe"
config_file="/etc/myapp/config.conf"
temp_directory="/tmp/myapp_$$"
```

### 2. Constants and Environment Variables

**Use uppercase with underscores:**

```sh
readonly CONFIG_DIR="/etc/myapp"
readonly MAX_RETRIES=3
export LOG_LEVEL="INFO"
```

### 3. Loop Variables

**Name descriptively:**

```sh
# Good
for user_id in user1 user2 user3; do
	process_user "${user_id}"
done

# Bad
for i in user1 user2 user3; do
	process_user "${i}"
done
```

## Error Handling and Return Values

### 1. Check Return Values

**Always check command return values.**

Under `set -eu`, a bare failing command exits the shell before any following `if [ $? -ne 0 ]` check can run. Handle failures inline:

- `if ! cmd; then ...; fi` when you only care about the failure path
- `if cmd; then ...; else ...; fi` when success and failure both need work
- `if ! var=$(cmd); then ...; fi` for the same pattern with command substitution

```sh
if ! mv "${source_file}" "${dest_dir}/"; then
	echo "Error: Unable to move ${source_file} to ${dest_dir}" >&2
	exit 1
fi

if sort "${input_file}" > "${temp_file}"; then
	mv "${temp_file}" "${output_file}"
else
	echo "Error: Failed to sort ${input_file}" >&2
	rm -f "${temp_file}"
	exit 1
fi

if ! disk_usage=$(du -sk "${backup_dir}"); then
	echo "Error: Failed to check disk usage for ${backup_dir}" >&2
	exit 1
fi
```

### 2. Pipeline Error Handling

**Use intermediate variables/files for reliable pipelines when needed:**

The verbose approach should only be used when pipeline reliability is critical. For simple cases, normal pipes are acceptable.

**Use variables for safe content (no special shell characters):**

```sh
# Safe content: numbers, simple text, known formats
if ! file_list=$(find "${dir}" -name "*.txt"); then
	echo "Error: find command failed" >&2
	exit 1
fi

echo "${file_list}" | while read -r file; do
	process_file "${file}"
done
```

**Use temporary files for unsafe content (quotes, backticks, dollar signs, etc):**

```sh
# Unsafe content: user input, arbitrary text, complex data
temp_file=$(mktemp)
if grep "complex pattern with $variables" "${input_file}" > "${temp_file}"; then
	# Process the temp file
	while read -r line; do
		echo "Found: ${line}"
	done < "${temp_file}"
	rm -f "${temp_file}"
else
	echo "Error: grep command failed" >&2
	rm -f "${temp_file}"
	exit 1
fi
```

**Simple pipelines can remain simple when reliability isn't critical:**

```sh
# Simple case - let it fail if it fails
ps aux | grep nginx | awk '{print $2}'

# Only add complexity when you need the reliability
find /var/log -name "*.log" | head -10
```

### 3. Error Reporting

**Send errors to STDERR with timestamps:**

```sh
# Error reporting function
err() {
	echo "[$(date '+%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# Usage
if ! create_backup "${database}"; then
	err "Failed to create backup for database: ${database}"
	exit 1
fi
```

### 4. Returning Values

**When returning status from a function, use numerical return codes:**

```sh
# Good - status uses exit codes
is_even() {
  # Checks if the input number is even
  if [ $(expr $1 % 2) -eq 0 ]; then
	return 0 # it's even
  else
	return 1 # it's not even
  fi
}

# Bad - unnecessary string use for status
file_exists() {
  # Checks if the given file exists
  if [ -f "$1" ]; then
	echo "true" # it exists
  else
	echo "false" # it doesn't exist
  fi
}
```

**When returning strings from a function with stdout, ensure that the function only ever returns the proper string:**

```sh
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

```sh
# Good
current_date=$(date '+%Y-%m-%d')
file_count=$(find "${dir}" -type f | wc -l)

# Bad
current_date=`date '+%Y-%m-%d'`
file_count=`find "${dir}" -type f | wc -l`
```

### 2. Test Constructs

**Use [ ] or test for POSIX compatibility:**

```sh
# Use [ ] for POSIX compatibility
if [ "${file}" != "${file%.txt}" ]; then
	echo "Text file detected"
fi

if [ -n "${variable}" ] && [ "${variable}" != "default" ]; then
	process_variable "${variable}"
fi

# String testing examples
if [ -z "${string}" ]; then          # Empty string
	echo "String is empty"
fi

if [ "${string1}" = "${string2}" ]; then  # String equality (use = not ==)
	echo "Strings are equal"
fi

# File testing
if [ -f "${file}" ]; then            # File exists and is regular file
	echo "File exists"
fi

if [ -d "${directory}" ]; then       # Directory exists
	echo "Directory exists"
fi
```

### 3. Arithmetic

**Use `expr` for calculations and `test` for comparisons:**

**Calculations with `expr` (POSIX-compliant):**

```sh
# Basic arithmetic with expr
total=$(expr ${count} \* ${price})    # Note: asterisk must be escaped
i=$(expr ${i} + 1)
difference=$(expr ${end} - ${start})
remainder=$(expr ${number} % 10)

# Complex expressions require escaped parentheses
result=$(expr \( ${a} + ${b} \) \* ${c})

# String operations with expr
length=$(expr length "${string}")
substring=$(expr substr "${string}" 2 3)  # from position 2, length 3
```

**Comparisons with `test` (using `[`):**

```sh
# Numeric comparisons
if [ "${count}" -gt "${threshold}" ]; then     # greater than
	echo "Threshold exceeded"
fi

if [ "${result}" -eq 0 ]; then               # equal
	echo "Success"
elif [ "${result}" -lt 0 ]; then             # less than
	echo "Negative result"
else
	echo "Positive result"
fi

# Available comparison operators:
# -eq (equal), -ne (not equal)
# -gt (greater than), -ge (greater than or equal) 
# -lt (less than), -le (less than or equal)
```

### 4. Lists and Collections

**Avoid arrays entirely - use alternative approaches:**

POSIX shell has no arrays. Use these alternatives sparingly and only when necessary.

**Positional parameters (limited use):**

`set --` replaces the current positional parameters: at script top level it destroys the script's own `$@`. Inside a function, positional parameters are local to the function and restored when it returns, so wrap temporary `set --` work in a function. Do not save and restore via `"$*"` and unquoted `set --` — that word-splits and glob-expands:

```sh
process_paths() {
	# pp_ = process_paths prefix
	set -- "/path/one" "/path/two" "/path/three"

	for pp_file in "$@"; do
		echo "Processing: ${pp_file}"
	done

	echo "Total files: $#"

	# Access and consume items from the front
	pp_first_file="$1"
	shift  # Remove first item; $@ now has the remaining items
}

process_paths
```

**Space-separated strings (when safe):**

```sh
# Only use when you're certain values contain no spaces/special chars
file_list="file1.txt file2.txt file3.txt"

for file in ${file_list}; do  # Note: no quotes - intentional word splitting
	echo "Processing: ${file}"
done
```

**Newline-separated processing:**

```sh
# Process items one by one from command output
find /path -name "*.txt" | while read -r file; do
	echo "Processing: ${file}"
done

# Or with here document
{
	echo "item1"
	echo "item2" 
	echo "item3"
} | while read -r item; do
	echo "Processing: ${item}"
done
```

## Main Function Pattern

**Use main function for executable scripts with multiple functions:**

```sh
#!/bin/sh

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

# Only run main if script is executed directly
# Note: BASH_SOURCE is not available in POSIX shell
if [ "${0##*/}" = "script_name.sh" ]; then
	main "$@" # Call a main function with all arguments
fi
```

## Security Considerations

### 1. Avoid SUID/SGID

**Never use SUID/SGID on shell scripts:**

```sh
# Use sudo for elevated access instead
if ! sudo systemctl restart nginx; then
	echo "Error: Failed to restart nginx" >&2
	exit 1
fi
```

### 2. Validate Inputs

**Always validate and sanitize inputs:**

```sh
validate_input() {
	input="$1"

	# Check if input is provided
	if [ -z "${input}" ]; then
		echo "Error: Input required" >&2
		return 1
	fi

	# Validate format using case statement (POSIX-compliant pattern)
	case "${input}" in
		*[!a-zA-Z0-9_]*)
			echo "Error: Invalid input format" >&2
			return 1
			;;
	esac

	return 0
}
```

## Built-in Preferences

**Prefer POSIX built-ins over external commands:**

```sh
# Good - using POSIX parameter expansion
string_length=${#variable}
# Note: POSIX has limited parameter expansion compared to bash

# Use external commands when necessary
result=$(expr "${x}" + "${y}")

# Use case for pattern matching instead of regex
case "${string}" in
	*pattern*)
		echo "Pattern found"
		;;
esac
```

## Advanced Features

### 1. Wildcard Expansion

**Be careful with filename expansion:**

```sh
# Good - explicit globbing with safeguards
for file in /path/to/files/*.txt; do
	[ -f "${file}" ] || continue  # Skip if no matches
	process_file "${file}"
done

# Good - disable globbing when not needed
set -f  # Disable globbing
echo "This * will not expand"
set +f  # Re-enable globbing
```

### 2. Working with Lists

**Avoid list-like operations when possible:**

```sh
# Process items directly from command output (preferred)
process_files() {
	find "$1" -name "*.txt" | while read -r file; do
		echo "Processing: ${file}"
		# Note: variables set in while loops persist within the loop
		# but may not persist outside due to subshell behavior
	done
}

# If you must store multiple items, use functions for each operation
process_predefined_items() {
	ppi_counter=0  # Function prefix: ppi_ = process_predefined_items
	
	# Process each item individually  
	process_item "item1"
	ppi_counter=$(expr ${ppi_counter} + 1)
	
	process_item "item2" 
	ppi_counter=$(expr ${ppi_counter} + 1)
	
	process_item "item3"
	ppi_counter=$(expr ${ppi_counter} + 1)
	
	echo "Processed ${ppi_counter} items"
}
```

### 3. Here Documents

**Use here documents for multi-line strings:**

```sh
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
```

## Common Pitfalls to Avoid

1. **Don't use bash-specific features** - Stick to POSIX
2. **Avoid complex parameter expansion** - Use external tools when needed
3. **Don't ignore return values** - Always check command success
4. **Avoid complex pipelines** - Use intermediate files/variables
5. **Extraneous stdout in functions that return strings** - redirect or discard all output except the return value
6. **Don't use arrays** - Use positional parameters or space-separated lists
	```sh
	# Bad: bash-specific array
	files=( file1.txt file2.txt file3.txt )

	# Good: POSIX-compatible list via function-local positional parameters
	process_file_list() {
		set -- file1.txt file2.txt file3.txt
		for pfl_file in "$@"; do
			process_file "${pfl_file}"
		done
	}
	```

## Testing and Validation

**Write testable POSIX shell scripts:**

```sh
#!/bin/sh
# calculator.sh - Example of testable POSIX shell script

add() {
	expr $1 + $2
}

subtract() {
	expr $1 - $2
}

main() {
	case "$1" in
		add) add "$2" "$3" ;;
		sub) subtract "$2" "$3" ;;
		*)   echo "Usage: $0 {add|sub} num1 num2" >&2; exit 1 ;;
	esac
}

# Only run main if executed directly
case "$0" in
	*/calculator.sh|calculator.sh) main "$@" ;;
esac
```

**Test with different shells:**

```sh
# Test with dash (POSIX-compliant)
dash myscript.sh

# Test with various POSIX shells
sh myscript.sh
ksh myscript.sh
```

## ShellCheck Integration

**Use ShellCheck with POSIX checking:**

```sh
# Check for POSIX compliance
shellcheck --shell=sh myscript.sh

# Common POSIX-related ShellCheck fixes:
# SC2039: In POSIX sh, 'local' is undefined
# SC2039: In POSIX sh, arrays are undefined
# SC2039: In POSIX sh, [[ ]] is undefined
```

**Common POSIX compliance fixes:**

```sh
# SC2039: Use of 'local'
# POSIX alternative: use function-specific variable naming
my_func() {
	# Instead of: local my_var="value"
	mf_my_var="value"  # Use function prefix
}

# SC2039: Use of arrays
# POSIX alternative: use positional parameters, inside a function
# so the script's own arguments are preserved
# Instead of: arr=( one two three )
set -- one two three
```

