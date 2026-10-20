---
name: shell-basics
description: "Linux shell basics - navigation, commands, file operations"
sasmp_version: "1.3.0"
bonded_agent: linux-expert
bond_type: PRIMARY_BOND
---

# Shell Basics Skill

## Overview

Master Linux shell fundamentals for efficient command-line usage.

## Capabilities

- **Navigation**: cd, pwd, ls, tree
- **File Operations**: cp, mv, rm, mkdir
- **Text Viewing**: cat, less, head, tail
- **Search**: find, locate, grep
- **Permissions**: chmod, chown, umask

## Examples

```bash
# Navigate and list
cd /var/log
ls -la

# Find files
find / -name "*.log" -mtime -1

# Search in files
grep -r "error" /var/log/
```

