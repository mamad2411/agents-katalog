---
name: context-aware-ops
description: >-
  Intelligent resource management with size checking and filtering to preserve
  context window.
  You MUST load this skill when managing large resources or context window limits.
license: MIT
---
# Context-Aware Operations Skill

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

This skill provides patterns and techniques for managing large files and command outputs
efficiently, preventing context window exhaustion while maintaining effective problem-solving
capabilities.

## WHEN TO USE

- Before executing commands that might produce large output
- Before reading any file in the codebase
- When debugging issues that might involve large resources
- When searching through codebases
- When working with logs, build outputs, or data files

## WHEN NOT TO USE

- For trivially small, single-file edits where the overhead of checking file size slows down the workflow unnecessarily.
- When the user explicitly demands the full output of a specific file and context limits are known to be sufficient.
- For interactive terminal sessions where pagination tools (`less`, `more`) are natively handled by the user.

## Common Pitfalls

- **Blind Dumping**: Running `cat` on a build log without checking its size, instantly blowing out the LLM's context window.
- **Truncating Crucial Errors**: Using `head` to sample a file when the actual error message resides at the very end of the stack trace (where `tail` was needed).
- **Ignoring Binary Files**: Attempting to read binary artifacts or minified JS without filtering, resulting in unreadable token noise.

## Core Principle

**Always check before you dump!**

Never blindly dump large resources into your context. Always:

1. Check the size first
2. Use filtering if needed
3. Focus on relevant portions only

## File Size Checking

### Check Line Count

```bash
# Fast line count
wc -l filename.txt

# Line count without filename
wc -l < filename.txt

# Line count with human-readable file size
wc -l filename.txt && ls -lh filename.txt
```

### Check File Size

```bash
# Human-readable size
ls -lh filename.txt

# Size in bytes (Linux)
stat -c%s filename.txt

# Size in bytes (macOS)
stat -f%z filename.txt

# Quick check if file is large
[ $(wc -l < filename.txt) -gt 500 ] && echo "Large file" || echo "Small file"
```

## Filtered File Reading

### Read Beginning and End

```bash
# First 50 lines
head -n 50 filename.txt

# Last 50 lines
tail -n 50 filename.txt

# Both ends with separator
head -n 30 filename.txt && echo "..." && tail -n 30 filename.txt
```

### Read Specific Ranges

```bash
# Lines 100-200
sed -n '100,200p' filename.txt

# Around a specific line (line 150 ± 25 lines)
sed -n '125,175p' filename.txt

# Skip first N lines, show next M
tail -n +100 filename.txt | head -n 50
```

### Search-Based Reading

```bash
# Find and show context
grep -n "pattern" filename.txt

# Show matching lines with 5 lines of context
grep -C 5 "pattern" filename.txt

# Show matching lines with line numbers
grep -n "pattern" filename.txt | head -20

# Count matches without showing content
grep -c "pattern" filename.txt
```

## Command Output Filtering

### Check Output Size First

```bash
# Count lines before showing
command | tee >(wc -l >&2) | head -20

# Or separately
output_lines=$(command | wc -l)
echo "Command produced $output_lines lines"
if [ $output_lines -gt 100 ]; then
  command | head -50
else
  command
fi
```

### Filter Common Patterns

```bash
# Show only errors and warnings
command 2>&1 | grep -E "error|warn|fail" -i

# Show only specific log levels
command | grep -E "ERROR|WARN|FATAL"

# Exclude verbose/debug lines
command | grep -v -E "DEBUG|TRACE|INFO"

# Show unique errors only
command 2>&1 | grep -i error | sort -u
```

### Paginate Large Output

```bash
# First page
command | head -n 50

# Show summary instead of full output
command | wc -l
command | head -20 && echo "... (showing first 20 lines)"
command | tail -20 && echo "... (showing last 20 lines)"
```

## Smart File Viewing Strategy

### Decision Tree

```bash
#!/bin/bash
FILE=$1

# Check if file exists
if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

# Get line count
LINES=$(wc -l < "$FILE")

# Decide how to show the file
if [ $LINES -le 100 ]; then
  # Small file - show all
  cat "$FILE"
elif [ $LINES -le 500 ]; then
  # Medium file - show with indicator
  cat "$FILE"
  echo "--- End of file ($LINES lines) ---"
elif [ $LINES -le 2000 ]; then
  # Large file - show beginning and end
  echo "--- First 50 lines of $LINES ---"
  head -n 50 "$FILE"
  echo "--- ... ---"
  echo "--- Last 50 lines ---"
  tail -n 50 "$FILE"
else
  # Very large file - show summary only
  echo "File has $LINES lines (too large to show)"
  echo "First 30 lines:"
  head -n 30 "$FILE"
  echo "---"
  echo "Last 30 lines:"
  tail -n 30 "$FILE"
  echo "---"
  echo "Use 'grep' to search for specific content"
fi
```

## Working with Logs

### Efficient Log Analysis

```bash
# Find errors in log
grep -i error logfile.log | head -20

# Show recent errors
tail -1000 logfile.log | grep -i error

# Count error types
grep -i error logfile.log | awk '{print $NF}' | sort | uniq -c | sort -rn

# Show errors with timestamps
grep -i error logfile.log | awk '{print $1, $2, $NF}' | head -20

# Find exceptions with context
grep -B 3 -A 10 "Exception" logfile.log | head -50
```

### Log Sampling

```bash
# Show every Nth line (sample large log)
awk 'NR % 10 == 0' large.log | head -100

# Show random sample
shuf -n 50 large.log

# Show first occurrence of each unique error
grep -i error large.log | awk '!seen[$0]++' | head -20
```

## Working with Code

### Search Code Efficiently

```bash
# Find function definitions (Python example)
grep -n "^def " *.py

# Find class definitions with context
grep -A 5 "^class " *.py | head -50

# Find TODO/FIXME comments
grep -rn "TODO\|FIXME" --include="*.py" | head -20

# Count occurrences per file
grep -rc "pattern" . | grep -v ":0$" | sort -t: -k2 -rn
```

### Browse Large Codebases

```bash
# List all Python files with line counts
find . -name "*.py" -exec wc -l {} + | sort -rn | head -20

# Find files containing pattern with size check
for f in $(grep -l "pattern" *.py); do
  lines=$(wc -l < "$f")
  echo "$f: $lines lines"
done

# Show structure without dumping content
find . -type f -name "*.py" | head -30
tree -L 3 --filesfirst 2>/dev/null || find . -type d | head -20
```

## Context Window Budget Management

### Track Usage Mentally

- Small files (<100 lines): ~100 tokens per file
- Medium files (100-500 lines): ~500 tokens per file
- Large files (500-2000 lines): Consider partial reading
- Very large files (>2000 lines): Never dump completely

### Prioritization Strategy

1. **Critical**: Files directly related to the bug/feature
2. **Important**: Dependencies and related modules
3. **Nice-to-have**: Context and documentation
4. **Skip**: Tangentially related or very large files

### When Context is Running Low

```bash
# Instead of full file, show:
# 1. File summary
wc -l filename && head -20 filename

# 2. Function/class list
grep -E "^(def|class|function|export)" filename

# 3. Specific section only
sed -n '/start_marker/,/end_marker/p' filename

# 4. Just the relevant function
awk '/^def target_function/,/^def [^t]/' filename.py
```

## Advanced Techniques

### Pipe Chains for Efficiency

```bash
# Find, filter, and limit in one go
find . -name "*.log" -exec grep -l "ERROR" {} \; | head -10

# Search multiple files, show unique results
grep -rh "pattern" . | sort -u | head -20

# Complex filtering in stages
cat large.txt | \
  grep -i "keyword" | \
  grep -v "noise" | \
  sort -u | \
  head -30
```

### Binary Search for Large Files

```bash
# Find approximate location of pattern
total_lines=$(wc -l < large.txt)
middle=$((total_lines / 2))

# Check first half
head -n $middle large.txt | grep -q "pattern" && echo "In first half" || echo "In second half"

# Then narrow down further
```

### Incremental Reading

```bash
# Read file in chunks
chunk_size=100
current=0
total=$(wc -l < file.txt)

# Read first chunk
sed -n "1,${chunk_size}p" file.txt

# If needed, read next chunk
current=$((current + chunk_size))
sed -n "${current},$((current + chunk_size))p" file.txt
```

## What to Avoid

1. **Don't**: `cat huge_file.log`
   **Do**: `head -100 huge_file.log && echo "... (showing first 100 of $(wc -l < huge_file.log) lines)"`

2. **Don't**: `npm install --verbose`
   **Do**: `npm install 2>&1 | grep -E "error|warn" -i || echo "Install successful"`

3. **Don't**: `git log`
   **Do**: `git log --oneline -20` or `git log --oneline | head -20`

4. **Don't**: `docker logs container`
   **Do**: `docker logs --tail 100 container` or `docker logs container 2>&1 | grep -i error`

5. **Don't**: `./run_tests.sh`
   **Do**: `./run_tests.sh 2>&1 | tee >(wc -l >&2) | grep -E "fail|error|pass" -i | head -50`

## Remember

- **Size matters**: Always check before you dump
- **Filter first**: Use grep, head, tail, sed, awk
- **Focus**: Only show what's relevant to the current task
- **Summarize**: When in doubt, show a summary rather than everything
- **Iterate**: You can always come back for more details if needed

## Related Skills

- **shell**:
  You MUST load this skill when handling shell commands with performance monitoring or timeouts.

Your context window is precious - use it wisely!
