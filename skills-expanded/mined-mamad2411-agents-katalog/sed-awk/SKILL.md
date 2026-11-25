---
name: sed-awk
description: Text processing with sed and awk — find-and-replace, column extraction, reformatting, and stream editing. Use when user mentions "sed", "awk", "text processing", "find and replace in files", "column extraction", "stream editing", "text transformation", "reformat output", or processing text from command-line output.
---

# sed and awk

## sed basics

### Substitute

```bash
# Replace first occurrence per line
sed 's/old/new/' file.txt

# Replace all occurrences per line
sed 's/old/new/g' file.txt

# Case-insensitive replace (GNU sed)
sed 's/old/new/gI' file.txt
```

### Delete lines

```bash
# Delete line 5
sed '5d' file.txt

# Delete lines 5 through 10
sed '5,10d' file.txt

# Delete blank lines
sed '/^$/d' file.txt

# Delete lines matching a pattern
sed '/DEBUG/d' file.txt
```

### Insert, append, and in-place editing

```bash
# Insert line before line 3
sed '3i\new line here' file.txt

# Append line after line 3
sed '3a\new line here' file.txt
```

```bash
# GNU sed: edit file in place
sed -i 's/old/new/g' file.txt

# BSD sed (macOS): requires backup extension
sed -i '' 's/old/new/g' file.txt

# Both: use backup extension for safety
sed -i.bak 's/old/new/g' file.txt
```

## sed addresses

```bash
sed '3s/old/new/' file.txt             # Line number
sed '3,7s/old/new/' file.txt           # Line range
sed '/START/,$s/old/new/' file.txt     # Pattern to end of file
sed '/BEGIN/,/END/s/old/new/' file.txt # Between two patterns
sed '1~2s/old/new/' file.txt           # Every 2nd line (GNU only)
sed '/KEEP/!d' file.txt                # Negate: all lines except match
```

## sed with regex

```bash
# Capture groups and backreferences (basic regex)
sed 's/\(foo\)\(bar\)/\2\1/' file.txt

# Extended regex (-E flag) avoids escaping parens
sed -E 's/(foo)(bar)/\2\1/' file.txt

# Reformat dates: 2024-01-15 -> 01/15/2024
sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\2\/\3\/\1/' file.txt

# Strip HTML tags
sed -E 's/<[^>]+>//g' file.html

# Trim leading and trailing whitespace
sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//' file.txt
```

### Multiple commands

```bash
# Chain with -e or semicolons
sed -e 's/foo/bar/' -e 's/baz/qux/' file.txt
sed 's/foo/bar/; s/baz/qux/' file.txt
```

## awk basics

### Print columns

```bash
# Print second column (whitespace-separated by default)
awk '{print $2}' file.txt

# Print first and third columns
awk '{print $1, $3}' file.txt

# Print last column
awk '{print $NF}' file.txt
```

### Field separator

```bash
# CSV: use comma as separator
awk -F',' '{print $2}' data.csv

# Colon-separated (e.g., /etc/passwd)
awk -F':' '{print $1, $3}' /etc/passwd

# Multiple separators
awk -F'[,;]' '{print $1, $2}' file.txt

# Set output separator
awk -F',' -v OFS='\t' '{print $1, $3}' data.csv
```

### Built-in variables

```bash
# NR: current line number; NF: number of fields in current line
awk '{print NR, NF, $0}' file.txt

# FS/OFS: input/output field separators
awk 'BEGIN{FS=","; OFS="\t"} {print $1, $2}' data.csv

# FILENAME: current input file
awk '{print FILENAME, NR, $0}' *.txt
```

## awk patterns and actions

### BEGIN and END blocks

```bash
# Header and footer
awk 'BEGIN{print "Name\tScore"} {print $1, $2} END{print "---done---"}' file.txt

# Count lines
awk 'END{print NR, "lines"}' file.txt
```

### Conditionals

```bash
# Print lines where column 3 > 100
awk '$3 > 100' file.txt

# Pattern match
awk '/ERROR/' file.txt

# Negated match
awk '!/DEBUG/' file.txt

# Conditional with field match
awk '$1 == "admin" {print $2}' file.txt

# Regex match on a field
awk '$2 ~ /^192\.168/' file.txt

# If-else
awk '{if ($3 > 90) print $1, "pass"; else print $1, "fail"}' file.txt
```

### Arithmetic

```bash
# Sum a column
awk '{sum += $2} END{print sum}' file.txt

# Average
awk '{sum += $2; n++} END{print sum/n}' file.txt

# Max value in column 3
awk 'NR==1 || $3 > max {max=$3} END{print max}' file.txt
```

## awk string functions

```bash
# split string into array
awk '{split($0, parts, ":"); print parts[1]}' file.txt

# substr (1-indexed)
awk '{print substr($1, 1, 3)}' file.txt

# gsub: global substitution; sub: first occurrence only
awk '{gsub(/foo/, "bar"); print}' file.txt

# match: find pattern, then extract via RSTART/RLENGTH
awk '{if (match($0, /[0-9]+/)) print substr($0, RSTART, RLENGTH)}' file.txt

# printf for formatted output
awk '{printf "%-20s %10.2f\n", $1, $2}' file.txt

# length, tolower, toupper
awk 'length($0) > 80' file.txt
awk '{print tolower($1)}' file.txt
```

## Common recipes

### Extract column from CSV

```bash
# Simple CSV
awk -F',' '{print $3}' data.csv

# CSV with quoted fields -- use a proper parser for complex cases
awk -F'","' '{gsub(/^"|"$/, "", $2); print $2}' data.csv
```

### Reformat log lines

```bash
# Apache log: extract IP and URL
awk '{print $1, $7}' access.log

# Extract timestamp and message from syslog
sed -E 's/^([A-Z][a-z]+ [0-9]+ [0-9:]+) [^ ]+ (.+)/\1 | \2/' /var/log/syslog
```

### Bulk rename patterns across files

```bash
# Replace in all matching files
find . -name '*.py' -exec sed -i '' 's/old_func/new_func/g' {} +

# Preview first (no -i flag)
grep -rl 'old_func' --include='*.py' . | xargs sed 's/old_func/new_func/g' | head -20
```

### Swap fields

```bash
# Swap columns 1 and 2
awk '{temp=$1; $1=$2; $2=temp; print}' file.txt

# Swap with sed capture groups
sed -E 's/^([^ ]+) ([^ ]+)/\2 \1/' file.txt
```

### Remove duplicate lines

```bash
# Remove all duplicates, preserving order
awk '!seen[$0]++' file.txt

# Remove duplicates based on a specific column
awk '!seen[$2]++' file.txt
```

### Sum a column

```bash
awk '{s+=$2} END{print s}' file.txt

# Sum matching rows from a CSV
awk -F',' '/SALE/ {s+=$4} END{printf "%.2f\n", s}' data.csv
```

### More one-liners

```bash
# Print lines between two markers (exclusive)
sed -n '/START/,/END/{/START/d;/END/d;p}' file.txt

# Join lines with commas
paste -sd',' file.txt

# Add a prefix to every line
sed 's/^/PREFIX: /' file.txt

# Remove trailing carriage returns (dos2unix)
sed 's/\r$//' file.txt

# Extract values between quotes
sed -n 's/.*"\([^"]*\)".*/\1/p' file.txt

# Unique values from a column, sorted by frequency
awk '{print $1}' file.txt | sort | uniq -c | sort -rn
```

## sed vs awk: when to use which

| Task | Use |
|------|-----|
| Find-and-replace | sed |
| Delete/filter lines by pattern | sed (or grep) |
| In-place file editing | sed |
| Column extraction | awk |
| Arithmetic, aggregation | awk |
| Conditional logic per line | awk |
| Reformatting structured text | awk |

Rule of thumb: if you need columns or math, use awk. If you need search-and-replace or line deletion, use sed.

## Gotchas

### BSD vs GNU sed

| Feature | GNU sed (Linux) | BSD sed (macOS) |
|---------|----------------|-----------------|
| In-place edit | `sed -i 's/.../.../'` | `sed -i '' 's/.../.../'` |
| `\t` in replacement | Supported | Not supported (use literal tab) |
| Case-insensitive flag | `s/old/new/I` | Not available |
| Line stepping `1~2` | Supported | Not available |
| `\+`, `\?` in basic regex | Supported | Not supported (use `-E`) |

Portable approach: always use `-E` for extended regex and `-i.bak` for in-place editing on both platforms.

### Quoting in shell

```bash
# Use single quotes to prevent shell expansion
sed 's/$HOME/replaced/' file.txt       # $HOME is literal
sed "s/$HOME/replaced/" file.txt       # $HOME is expanded by shell

# To use shell variables in sed, use double quotes
name="world"
sed "s/hello/$name/" file.txt

# Escape slashes with alternate delimiters
sed 's|/usr/local/bin|/opt/bin|g' file.txt
sed 's#old/path#new/path#g' file.txt

# Pass shell variables to awk with -v
name="admin"
awk -v user="$name" '$1 == user {print $2}' file.txt

# Never embed shell variables directly in awk single-quoted blocks
# This does NOT work:
awk '$1 == "$name"' file.txt   # literal string "$name"
```
