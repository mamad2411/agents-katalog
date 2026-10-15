---
name: xargs-parallel
description: Parallel execution with xargs, GNU parallel, and batch processing patterns. Use when user mentions "xargs", "parallel", "batch processing", "run in parallel", "parallel execution", "process list of files", "bulk operations", "concurrent commands", "map over files", or running commands on multiple inputs.
---

# xargs and Parallel Execution

## xargs Basics

Read from stdin and pass as arguments to a command:

```bash
# Basic usage: pass stdin lines as arguments
echo "file1.txt file2.txt" | xargs rm

# -I {} sets a placeholder for each input line
cat urls.txt | xargs -I {} curl -O {}

# -n controls how many arguments per command invocation
echo "a b c d e f" | xargs -n 2 echo
# Output:
# a b
# c d
# e f

# -t prints each command before executing (trace mode)
ls *.log | xargs -t rm

# Read arguments from a file
xargs -a filelist.txt rm
```

## xargs with find

Always use `-print0` / `-0` to handle filenames with spaces and special characters:

```bash
# Safe deletion of files matching a pattern
find . -name "*.tmp" -print0 | xargs -0 rm -f

# Count lines in all Python files
find . -name "*.py" -print0 | xargs -0 wc -l

# Change permissions on specific files
find /var/log -name "*.log" -print0 | xargs -0 chmod 644

# Grep across files found by find
find src/ -name "*.js" -print0 | xargs -0 grep -l "TODO"
```

## Parallel Execution with xargs -P

`-P N` runs up to N processes in parallel:

```bash
# Compress files using 4 parallel jobs
find . -name "*.log" -print0 | xargs -0 -P 4 -I {} gzip {}

# Download URLs in parallel (8 at a time)
cat urls.txt | xargs -P 8 -I {} curl -sO {}

# Convert images in parallel
find . -name "*.png" -print0 | xargs -0 -P 4 -I {} convert {} -resize 50% resized_{}

# Use all available cores
find . -name "*.gz" -print0 | xargs -0 -P "$(nproc)" gunzip
```

## GNU parallel Basics

GNU parallel offers more features if installed (`brew install parallel` / `apt install parallel`):

```bash
# Basic usage (similar to xargs -P)
cat urls.txt | parallel curl -sO {}

# Control job count
find . -name "*.csv" | parallel -j 8 gzip {}

# Progress bar
find . -name "*.mp4" | parallel --bar ffmpeg -i {} -vf scale=640:-1 small_{}

# Retry failed jobs
cat urls.txt | parallel --retries 3 curl -sO {}

# Distribute jobs across multiple machines (SSH)
parallel -S server1,server2 --transferfile {} gzip ::: *.log

# Keep output order matching input order
seq 10 | parallel -k 'sleep $((RANDOM % 3)); echo {}'
```

## Common Patterns

### Bulk Rename Files

```bash
# Add a prefix
ls *.jpg | xargs -I {} mv {} archive_{}

# Change extension (using parameter expansion in a subshell)
find . -name "*.txt" -print0 | xargs -0 -I {} bash -c 'mv "$1" "${1%.txt}.md"' _ {}

# Lowercase all filenames in current directory
ls | xargs -I {} bash -c 'mv "$1" "$(echo "$1" | tr "A-Z" "a-z")"' _ {}
```

### Process All Files Matching a Pattern

```bash
# Format all Go files
find . -name "*.go" -print0 | xargs -0 gofmt -w

# Lint all JS files
find src/ -name "*.js" -print0 | xargs -0 eslint --fix

# Run a script against each config file
find /etc -name "*.conf" -print0 | xargs -0 -I {} ./validate-config.sh {}
```

### Download a List of URLs

```bash
# Download all URLs from a file, 10 in parallel
cat urls.txt | xargs -P 10 -I {} curl -sfLO {}

# Download with wget, retrying failures
cat urls.txt | xargs -P 5 -I {} wget -q --retry-connrefused --tries=3 {}

# With GNU parallel and a progress bar
parallel --bar -j 10 curl -sfLO {} < urls.txt
```

### Run Tests in Parallel

```bash
# Run test files in parallel
find tests/ -name "test_*.py" | xargs -P 4 -I {} python -m pytest {} -v

# Run multiple test suites concurrently
echo "unit integration e2e" | xargs -n 1 -P 3 -I {} make test-{}
```

### Batch API Calls

```bash
# POST each JSON file to an API endpoint
find data/ -name "*.json" -print0 | xargs -0 -P 5 -I {} \
  curl -s -X POST -H "Content-Type: application/json" -d @{} https://api.example.com/ingest

# Process user IDs from a file
cat user_ids.txt | xargs -P 10 -I {} \
  curl -s "https://api.example.com/users/{}" -o "responses/{}.json"
```

### Parallel Image Compression

```bash
# Compress PNGs in parallel with pngquant
find . -name "*.png" -print0 | xargs -0 -P "$(nproc)" -I {} pngquant --force --quality=65-80 {} --output {}

# Resize JPEGs with ImageMagick
find photos/ -name "*.jpg" -print0 | xargs -0 -P 4 -I {} \
  convert {} -resize 1920x1080\> -quality 85 optimized/{}
```

### Bulk Git Operations Across Repos

```bash
# Pull latest in all repos under a directory
find ~/projects -maxdepth 2 -name ".git" -type d -print0 | \
  xargs -0 -P 8 -I {} git -C "{}/.." pull --ff-only

# Check status of all repos
find ~/projects -maxdepth 2 -name ".git" -type d | \
  xargs -I {} bash -c 'echo "=== $(dirname {}) ===" && git -C "{}/.." status -s'

# Garbage collect all repos in parallel
find ~/projects -maxdepth 2 -name ".git" -type d -print0 | \
  xargs -0 -P 4 -I {} git -C "{}/.." gc --quiet
```

## Handling Filenames with Spaces

```bash
# -0 expects null-delimited input (pair with find -print0)
find . -name "*.txt" -print0 | xargs -0 wc -l

# -d '\n' treats newlines as delimiters (not spaces)
ls | xargs -d '\n' -I {} echo "File: {}"

# On macOS (BSD xargs lacks -d), use -0 with tr
ls | tr '\n' '\0' | xargs -0 -I {} echo "File: {}"
```

## Dry Run Before Executing

```bash
# Preview what would be deleted
find . -name "*.bak" -print0 | xargs -0 echo rm

# Use -p to prompt before each execution
find . -name "*.tmp" -print0 | xargs -0 -p rm

# With -t to trace commands as they run
find . -name "*.log" -print0 | xargs -0 -t gzip
```

## Error Handling

```bash
# xargs exits with 123 if any command fails
find . -name "*.sh" -print0 | xargs -0 -P 4 bash  # check $?

# GNU parallel: halt on first failure
cat jobs.txt | parallel --halt now,fail=1 process_job {}

# GNU parallel: halt when 20% of jobs fail
cat jobs.txt | parallel --halt soon,fail=20% process_job {}

# Capture per-job exit codes with GNU parallel
cat jobs.txt | parallel --joblog joblog.txt process_job {}
# joblog.txt contains exit status for every job
```

## xargs vs for Loops vs while read

**Use xargs when:**
- Processing output from `find` or another command
- You want built-in parallelism (`-P`)
- Batching multiple arguments per invocation (`-n`)

**Use `while read` when:**
- You need complex logic per iteration (if/else, multiple commands)
- The loop body uses shell variables that must persist across iterations

**Use `for` loops when:**
- Iterating over a known, small list of items
- Glob expansion is sufficient (`for f in *.txt`)
- Readability matters more than performance

```bash
# for loop -- simple, readable, no parallelism
for f in *.txt; do wc -l "$f"; done

# while read -- complex logic per item
find . -name "*.csv" | while read -r f; do
  count=$(wc -l < "$f")
  [ "$count" -gt 1000 ] && echo "Large: $f ($count lines)"
done

# xargs -- fast, parallel, concise
find . -name "*.csv" -print0 | xargs -0 -P 4 wc -l
```

## Resource-Aware Parallelism

```bash
# Use nproc to match available CPU cores
find . -name "*.gz" -print0 | xargs -0 -P "$(nproc)" gunzip

# Use half the cores to leave room for other work
find . -name "*.log" -print0 | xargs -0 -P "$(( $(nproc) / 2 ))" gzip

# GNU parallel: percentage-based, relative, or load-based limits
parallel -j 50% gzip ::: *.log         # 50% of cores
parallel -j -2 gzip ::: *.log          # cores minus 2
parallel --load 80% process_job ::: *  # limit by load average

# Limit concurrency for I/O-bound tasks (network, disk)
cat urls.txt | xargs -P 5 -I {} curl -sO {}

# Monitor parallel job resource usage
parallel --joblog jobs.log -j 4 heavy_task ::: input_* && column -t jobs.log
```
