---
name: robust-commands
description: >-
  Resilient command execution with automatic fallbacks and error recovery.
  You MUST load this skill when executing commands requiring resilient error
  recovery or fallbacks.
license: MIT
---

# Robust Command Execution Skill

This skill provides patterns for executing commands with automatic error
recovery, fallback mechanisms, and installation of missing dependencies.
Never give up when a command fails - try alternatives!

## WHEN TO USE

- When a command might not be installed
- When debugging command failures
- When tool availability is uncertain
- When working in different environments (containers, CI, local)
- When you need to ensure commands succeed

## WHEN NOT TO USE

- For highly sensitive or destructive commands (like `rm -rf /` or database drops) where silent fallback
  execution could be disastrous.
- Inside performance-critical inner loops where checking for tool existence on every iteration introduces unacceptable overhead.
- When working within strictly constrained, immutable environments where installing new packages is explicitly forbidden.

## Common Pitfalls

- **Masking Genuine Errors**: Catching all errors with `||` and proceeding blindly, ignoring that the
  primary command failed for a critical reason (e.g., missing permissions, not just a missing tool).
- **Infinite Loops in Fallbacks**: Creating a fallback mechanism that continuously retries a command
  without a hard cap or backoff strategy.
- **Assuming Installation Succeeds**: Trying to `apt-get install` a missing tool without verifying whether
  the script actually has root/sudo privileges to do so.

## Core Principle

**If a command doesn't work, don't just report failure - fix it!**

Process for handling command failures:

1. Check if the command exists
2. Try to install if missing
3. Try alternative commands
4. Verify prerequisites (permissions, paths)
5. Only report as blocked if all options exhausted

## Command Existence Checking

### Check if Command Exists

```bash
# Method 1: which
which command_name

# Method 2: command -v (POSIX-compliant, more reliable)
command -v command_name

# Method 3: type
type command_name

# Best practice - silent check
if command -v jq &> /dev/null; then
  echo "jq is available"
else
  echo "jq is not installed"
fi
```

### Check Multiple Alternative Commands

```bash
# Find first available command from list
for cmd in jq python3 python; do
  if command -v "$cmd" &> /dev/null; then
    echo "Using $cmd"
    break
  fi
done
```

## Installing Missing Commands

### Debian/Ubuntu Systems

```bash
# Update package lists first
apt-get update

# Install single package
apt-get install -y package-name

# Search for package
apt-cache search keyword

# Install with error handling
if ! command -v jq &> /dev/null; then
  echo "Installing jq..."
  apt-get update && apt-get install -y jq
fi
```

### Common Package Names

```bash
# JSON processing
apt-get install -y jq

# YAML processing
apt-get install -y yq

# HTTP requests
apt-get install -y curl wget

# Text processing
apt-get install -y sed gawk grep

# Build tools
apt-get install -y build-essential

# Python tools
apt-get install -y python3 python3-pip

# Node.js tools
apt-get install -y nodejs npm
```

### Python Packages

```bash
# Install with pip
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Install from requirements
pip install -r requirements.txt

# Common Python tools
pip install pyyaml requests black pylint
```

## Command Fallback Patterns

### JSON Processing

```bash
# Try jq first, fallback to python
if command -v jq &> /dev/null; then
  jq . file.json
else
  python3 -m json.tool < file.json
fi

# Or one-liner with ||
jq . file.json 2>/dev/null || python3 -m json.tool < file.json
```

### YAML Processing

```bash
# Try yq, fallback to python
if command -v yq &> /dev/null; then
  yq eval file.yaml
else
  python3 -c "import yaml, sys; print(yaml.safe_load(open('file.yaml')))"
fi
```

### HTTP Requests

```bash
# Try curl, fallback to wget
if command -v curl &> /dev/null; then
  curl -s https://example.com
else
  wget -q -O - https://example.com
fi

# Or with Python as final fallback
curl -s https://example.com 2>/dev/null || \
wget -q -O - https://example.com 2>/dev/null || \
python3 -c "import urllib.request; \
  print(urllib.request.urlopen('https://example.com').read().decode())"
```

### Text Processing

```bash
# Line counting alternatives
wc -l file.txt 2>/dev/null || \
cat file.txt | wc -l 2>/dev/null || \
awk 'END {print NR}' file.txt

# Grep alternatives
grep "pattern" file.txt 2>/dev/null || \
awk '/pattern/' file.txt 2>/dev/null || \
python3 -c "import sys; \
  [print(line, end='') for line in open('file.txt') if 'pattern' in line]"
```

## Permission Handling

### Check File Permissions

```bash
# Check if file is readable
if [ -r file.txt ]; then
  cat file.txt
else
  echo "File not readable"
fi

# Check if file is writable
if [ -w /tmp/file.txt ]; then
  echo "data" > /tmp/file.txt
else
  echo "File not writable"
fi

# Check if file is executable
if [ -x script.sh ]; then
  ./script.sh
else
  echo "File not executable"
fi
```

### Fix Permissions

```bash
# Make file readable
chmod +r file.txt

# Make file writable
chmod +w file.txt

# Make file executable
chmod +x script.sh

# Common permission patterns
chmod 644 file.txt    # rw-r--r--
chmod 755 script.sh   # rwxr-xr-x
chmod 600 secret.key  # rw-------
```

### Handle Permission Denied

```bash
# Try normal command, fall back to sudo if needed
cat /etc/secret 2>/dev/null || sudo cat /etc/secret

# Check if sudo is available
if command -v sudo &> /dev/null && sudo -n true 2>/dev/null; then
  sudo command
else
  echo "Cannot elevate privileges"
fi
```

## Path Verification

### Check if File/Directory Exists

```bash
# Check file exists
if [ -f file.txt ]; then
  echo "File exists"
fi

# Check directory exists
if [ -d /path/to/dir ]; then
  echo "Directory exists"
fi

# Check path exists (file or directory)
if [ -e /path/to/something ]; then
  echo "Path exists"
fi
```

### Create Missing Paths

```bash
# Create directory if missing
mkdir -p /path/to/dir

# Create file if missing
touch file.txt

# Create with error handling
if [ ! -d /path/to/dir ]; then
  mkdir -p /path/to/dir || {
    echo "Failed to create directory"
    exit 1
  }
fi
```

## Complete Robust Command Pattern

### Template for Any Command

```bash
#!/bin/bash

# Function to run command with fallbacks
run_robust() {
  local cmd=$1
  shift
  local args="$@"

  # Check if command exists
  if ! command -v "$cmd" &> /dev/null; then
    echo "Command '$cmd' not found. Attempting to install..."

    # Try to install
    case "$cmd" in
      jq)
        apt-get update && apt-get install -y jq
        ;;
      yq)
        apt-get update && apt-get install -y yq
        ;;
      curl)
        apt-get update && apt-get install -y curl
        ;;
      *)
        echo "Don't know how to install '$cmd'"
        return 1
        ;;
    esac

    # Check again after install
    if ! command -v "$cmd" &> /dev/null; then
      echo "Failed to install '$cmd'"
      return 1
    fi
  fi

  # Run the command
  "$cmd" $args
}

# Usage
run_robust jq . file.json
```

## Error Recovery Strategies

### Retry with Backoff

```bash
# Retry command up to N times
retry_command() {
  local max_attempts=3
  local timeout=2
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt of $max_attempts..."

    if "$@"; then
      return 0
    fi

    echo "Command failed. Retrying in ${timeout}s..."
    sleep $timeout
    timeout=$((timeout * 2))
    attempt=$((attempt + 1))
  done

  echo "Command failed after $max_attempts attempts"
  return 1
}

# Usage
retry_command curl -f https://api.example.com
```

### Timeout Protection

```bash
# Run command with timeout
timeout 30s long_running_command || {
  echo "Command timed out after 30 seconds"
}

# Or with fallback
timeout 10s risky_command || echo "Command failed or timed out"
```

### Capture and Handle Errors

```bash
# Capture both stdout and stderr
output=$(command 2>&1) || {
  echo "Command failed with output:"
  echo "$output"
  # Try alternative
  alternative_command
}

# Check exit code explicitly
command
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo "Command failed with exit code $exit_code"
  # Handle error
fi
```

## Environment Detection

### Detect Operating System

```bash
# Detect OS
if [ -f /etc/os-release ]; then
  . /etc/os-release
  echo "OS: $NAME"
  echo "Version: $VERSION"
fi

# Or use uname
case "$(uname -s)" in
  Linux*)
    echo "Linux system"
    ;;
  Darwin*)
    echo "macOS system"
    ;;
  *)
    echo "Unknown system"
    ;;
esac
```

### Detect Package Manager

```bash
# Find available package manager
if command -v apt-get &> /dev/null; then
  PKG_MANAGER="apt-get"
elif command -v yum &> /dev/null; then
  PKG_MANAGER="yum"
elif command -v brew &> /dev/null; then
  PKG_MANAGER="brew"
else
  echo "No known package manager found"
fi
```

### Detect Container/CI Environment

```bash
# Check if running in Docker
if [ -f /.dockerenv ]; then
  echo "Running in Docker"
fi

# Check if running in GitHub Actions
if [ -n "$GITHUB_ACTIONS" ]; then
  echo "Running in GitHub Actions"
fi

# Check if running in GitLab CI
if [ -n "$GITLAB_CI" ]; then
  echo "Running in GitLab CI"
fi
```

## Common Command Alternatives

### File Operations

```bash
# Read file
cat file.txt || head -n 99999 file.txt || \
  python3 -c "print(open('file.txt').read())"

# Write file
echo "data" > /tmp/file.txt || python3 -c "open('/tmp/file.txt', 'w').write('data')"

# Append to file
echo "data" >> file.txt || python3 -c "open('file.txt', 'a').write('data\n')"
```

### Network Operations

```bash
# Download file
curl -O url || wget url || \
  python3 -c "import urllib.request; urllib.request.urlretrieve('url', 'file')"

# Check if URL is reachable
curl -I url || wget --spider url || \
  python3 -c "import urllib.request; urllib.request.urlopen('url')"
```

### Archive Operations

```bash
# Extract tar.gz
tar -xzf file.tar.gz || python3 -m tarfile -e file.tar.gz

# Create tar.gz
tar -czf archive.tar.gz files/ || python3 -m tarfile -c archive.tar.gz files/

# Extract zip
unzip file.zip || python3 -m zipfile -e file.zip .
```

## Best Practices

1. **Always check first**: Use `command -v` before executing
2. **Silent checks**: Redirect stderr to /dev/null for checks
3. **Prefer POSIX**: Use `command -v` over `which`
4. **Install when missing**: Don't ask user if you can install
5. **Try alternatives**: Have fallbacks for common commands
6. **Handle permissions**: Check and fix permissions as needed
7. **Verify paths**: Ensure files/directories exist before using
8. **Graceful degradation**: Try best option first, fall back progressively
9. **Clear feedback**: Tell user what you're trying and why
10. **Document workarounds**: Note unusual solutions for future reference

## Remember

- **Never give up**: If one approach fails, try another
- **Be resourceful**: Many tools can accomplish the same task
- **Think creatively**: Python/shell scripts can replace missing tools
- **Install proactively**: Don't wait for failures to install tools
- **Test assumptions**: Verify command exists before using it
- **Handle errors**: Always have a fallback plan

## Related Skills

- **shell**:
  You MUST load this skill when handling shell commands with performance monitoring or timeouts.

Commands fail for many reasons - most are fixable!
