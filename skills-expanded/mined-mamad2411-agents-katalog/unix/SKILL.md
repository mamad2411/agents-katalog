---
name: unix
description: >
  Expert guidance on Unix operating system commands and administration. Use for: file system 
  operations, process management, text processing, networking, shell scripting, user management, 
  permissions, environment configuration, system monitoring, and automation.
license: MIT
compatibility: opencode
metadata:
  audience: developers, system-administrators
  category: systems-administration
  tags: [unix, bash, shell, linux, command-line]
---

# Unix & Linux — Command Reference

Covers: **File Operations · Process Management · Text Processing · Networking · Scripting · System Administration**

-----

## File System Operations

### File Navigation and Listing

The Unix file system follows a hierarchical tree structure with the root directory "/" at the top. Understanding how to navigate this structure efficiently is fundamental to working with Unix systems. Modern Unix systems maintain a consistent directory structure following the Filesystem Hierarchy Standard (FHS).

Common directories include: /bin for essential binaries, /etc for system configuration, /home for user directories, /var for variable data like logs, /tmp for temporary files, /usr for user programs, and /proc for process information.

```bash
# Basic navigation
cd /home/user/projects          # Change directory
cd ~                           # Go to home directory
cd -                           # Go to previous directory
pwd                            # Print working directory
ls                             # List files
ls -la                         # List all files with details
ls -lh                         # Human-readable file sizes
ls -lt                         # Sort by modification time
ls -lS                         # Sort by file size
ls -R                          # Recursive listing
ls -1                          # One file per line
ls -d */                       # List directories only

# Using ls with various options
ls -a                          # Show hidden files (starting with .)
ls -A                          # Show hidden files except . and ..
ls -F                          # Append file type indicators (* / @ |)
ls --color=auto                # Colorize output by type

# Advanced listing
ls -l | grep '^d'              # List directories only
ls -l | awk '{print $9}'       # List just filenames
ls -t | head -n 10             # 10 most recently modified files
find . -type f -ls             # Detailed listing with find
```

### File Creation and Manipulation

```bash
# Create files
touch newfile.txt              # Create empty file
touch -t 202312251200 file     # Create with specific timestamp
echo "content" > file.txt      # Create with content (overwrite)
echo "content" >> file.txt     # Append content
printf "Line1\nLine2\n" > f    # Create with newlines
cat > file.txt << EOF          # Here-document creation
Multi-line
content
here
