---
name: multi-platform-dev
description: Use when developing cross-platform applications that must work on Windows, Linux, and macOS. Covers shell command differences, path handling, line endings, file permissions, package managers, environment detection, platform-specific build tools, and testing strategies. Ensures code works everywhere without platform assumptions.
license: MIT
---

# Multi-Platform Development Skill — Cross-Platform Compatibility

## Overview

This skill provides comprehensive guidance for **developing applications that work across Windows, Linux, and macOS**. It covers shell command differences, path handling, line endings, file permissions, package managers, environment detection, platform-specific build tools, and testing strategies. Essential for avoiding the "works on my machine" problem.

## When to Use

**Use this skill when:**

- Writing shell scripts that must run on Windows, Linux, and macOS
- Handling file paths across different operating systems
- Managing line endings (CRLF vs LF) in cross-platform projects
- Setting file permissions portably
- Detecting the current platform in code
- Configuring package managers for different OS
- Building cross-platform CI/CD pipelines
- Writing cross-platform test scripts
- Handling environment variables across platforms
- Managing process management differences
- Configuring cross-platform development environments
- Writing platform-conditional code
- Handling cross-platform networking differences
- Managing cross-platform logging and debugging
- Creating cross-platform installer packages
- Writing cross-platform configuration files
- Handling cross-platform date/time formatting
- Managing cross-platform locale and encoding
- Writing cross-platform CLI tools
- Configuring cross-platform Docker environments

**Do NOT use this skill when:**

- Building native OS-specific applications (use platform-specific SDK)
- Writing kernel-level code (use OS-specific documentation)
- Developing mobile apps (use mobile-engineer skill)
- Creating browser-only web apps (use frontend-developer skill)
- Configuring cloud infrastructure (use terraform-iac or aws-serverless skill)
- Writing database queries (use database-design skill)
- Implementing machine learning models (use data-science skill)

**Why avoid:** Cross-platform concerns are irrelevant for platform-specific or browser-only applications. Focus on the target platform.

## Core Concepts

### Platform Detection

| Platform    | Node.js                         | Python                     | Shell   | PowerShell |
| ----------- | ------------------------------- | -------------------------- | ------- | ---------- |
| **Windows** | `process.platform === 'win32'`  | `sys.platform == 'win32'`  | N/A     | `$true`    |
| **Linux**   | `process.platform === 'linux'`  | `sys.platform == 'linux'`  | `$true` | `$false`   |
| **macOS**   | `process.platform === 'darwin'` | `sys.platform == 'darwin'` | `$true` | `$false`   |

### Shell Command Differences

| Operation            | Linux/macOS (Bash)    | Windows (CMD)            | Windows (PowerShell)                     |
| -------------------- | --------------------- | ------------------------ | ---------------------------------------- |
| **List files**       | `ls -la`              | `dir /a`                 | `Get-ChildItem -Force`                   |
| **Change directory** | `cd /path`            | `cd C:\path`             | `Set-Location C:\path`                   |
| **Copy file**        | `cp src dst`          | `copy src dst`           | `Copy-Item src dst`                      |
| **Copy directory**   | `cp -r src dst`       | `xcopy src dst /E /I`    | `Copy-Item src dst -Recurse`             |
| **Delete file**      | `rm file`             | `del file`               | `Remove-Item file`                       |
| **Delete directory** | `rm -rf dir`          | `rmdir /s /q dir`        | `Remove-Item dir -Recurse -Force`        |
| **Make directory**   | `mkdir -p dir`        | `mkdir dir`              | `New-Item -ItemType Directory -Path dir` |
| **Show current dir** | `pwd`                 | `cd`                     | `Get-Location`                           |
| **Search text**      | `grep "pattern" file` | `findstr "pattern" file` | `Select-String "pattern" file`           |
| **Pipe output**      | `cmd1 \| cmd2`        | `cmd1 \| cmd2`           | `cmd1 \| cmd2`                           |
| **Redirect output**  | `cmd > file`          | `cmd > file`             | `cmd > file`                             |
| **Environment var**  | `$VAR` or `${VAR}`    | `%VAR%`                  | `$env:VAR`                               |
| **Execute script**   | `./script.sh`         | `script.bat`             | `.\script.ps1`                           |
| **Clear screen**     | `clear`               | `cls`                    | `Clear-Host`                             |
| **Show process**     | `ps aux`              | `tasklist`               | `Get-Process`                            |
| **Kill process**     | `kill PID`            | `taskkill /PID PID /F`   | `Stop-Process -Id PID -Force`            |

### Path Handling

```javascript
// ✅ GOOD: Cross-platform path handling (Node.js)
const path = require('path');

// Works on all platforms
const filePath = path.join('data', 'files', 'document.txt');
// Windows: data\files\document.txt
// Linux/macOS: data/files/document.txt

// ✅ GOOD: Path separator detection
const separator = path.sep; // '\\' on Windows, '/' on Linux/macOS

// ❌ BAD: Hardcoded paths
const badPath = '/home/user/data/file.txt'; // Fails on Windows
const badPath2 = 'C:\\Users\\user\\data\\file.txt'; // Fails on Linux/macOS
```

```python
# ✅ GOOD: Cross-platform path handling (Python)
from pathlib import Path

# Works on all platforms
file_path = Path('data') / 'files' / 'document.txt'

# ✅ GOOD: Platform detection
import sys
if sys.platform == 'win32':
    print("Windows-specific logic")
elif sys.platform == 'darwin':
    print("macOS-specific logic")
else:
    print("Linux/Unix-specific logic")

# ❌ BAD: Hardcoded paths
bad_path = '/home/user/data/file.txt'  # Fails on Windows
```

### Line Endings

| Platform        | Line Ending | Bytes              | Git Config            |
| --------------- | ----------- | ------------------ | --------------------- |
| **Windows**     | CRLF        | `\r\n` (0x0D 0x0A) | `core.autocrlf=true`  |
| **Linux/macOS** | LF          | `\n` (0x0A)        | `core.autocrlf=input` |

```git
# .gitconfig (Global settings)
[core]
    autocrlf = input  # Convert CRLF to LF on commit, keep LF on checkout

# .gitattributes (Project settings - commit to repo)
# Text files - normalize to LF
* text=auto

# Specific text files
*.js text
*.ts text
*.py text
*.md text
*.json text
*.yaml text
*.yml text

# Binary files - no conversion
*.png binary
*.jpg binary
*.gif binary
*.woff binary
*.woff2 binary
*.ttf binary
```

### File Permissions

```bash
# Linux/macOS: chmod for permissions
chmod 755 script.sh    # rwxr-xr-x (executable)
chmod 644 file.txt     # rw-r--r-- (read/write owner, read others)
chmod 600 secrets.env  # rw------- (read/write owner only)

# Windows: No direct equivalent - use ACLs
# PowerShell: Set-Acl for permissions
icacls file.txt /grant:r "Users:(R)"  # Read for all users
icacls file.txt /grant:r "Administrators:(F)"  # Full control for admins

# Cross-platform solution: Use package manager or installer
# npm: Files in bin/ are marked executable on Linux/macOS
# Python: Use setuptools with scripts= or entry_points=
```

## Cross-Platform Shell Scripts

### Bash with Windows Support (Git Bash/WSL)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Platform detection
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGW;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected platform: ${MACHINE}"

# Cross-platform path handling
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cross-platform find
if [[ "${MACHINE}" == "Linux" || "${MACHINE}" == "Mac" ]]; then
    find "${PROJECT_ROOT}/src" -name "*.ts" -type f
else
    # Windows (Git Bash/MinGW)
    find "${PROJECT_ROOT}/src" -name "*.ts" -type f
fi

# Cross-platform process killing
kill_process() {
    local pid=$1
    if [[ "${MACHINE}" == "MinGW" || "${MACHINE}" == "Cygwin" ]]; then
        taskkill //PID "${pid}" //F >/dev/null 2>&1
    else
        kill "${pid}" 2>/dev/null
    fi
}
```

### PowerShell Cross-Platform

```powershell
# Cross-platform PowerShell (works on Windows, Linux, macOS)

# Platform detection
$isWindows = $true
$isLinux = $false
$isMacOS = $false

if ($PSVersionTable.PSVersion.Major -ge 6) {
    # PowerShell Core (cross-platform)
    $platform = [System.Runtime.InteropServices.RuntimeInformation]::OSDescription
    $isWindows = $platform -match "Windows"
    $isLinux = $platform -match "Linux"
    $isMacOS = $platform -match "Darwin"
}

# Cross-platform path handling
$projectRoot = $PSScriptRoot
$filePath = Join-Path $projectRoot "data\file.txt"

# Cross-platform file operations
Copy-Item -Path "src\file.txt" -Destination "dst\file.txt" -Force
Remove-Item -Path "temp\*" -Recurse -Force
New-Item -ItemType Directory -Path "new\dir" -Force

# Cross-platform process management
Get-Process -Name "node" | Stop-Process -Force
```

### Node.js Cross-Platform Scripts

```javascript
// ✅ GOOD: Cross-platform script (package.json)
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development nodemon src/index.ts",
    "build": "tsc && electron-builder",
    "test": "cross-env NODE_ENV=test jest",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "cross-env": "^7.0.3",
    "cross-spawn": "^7.0.3"
  }
}

// ✅ GOOD: Using cross-spawn for child processes
const spawn = require('cross-spawn');

// Works on all platforms (handles path.exe on Windows)
const child = spawn('npm', ['run', 'build'], { stdio: 'inherit' });

// ❌ BAD: Platform-specific commands
const { exec } = require('child_process');
exec('ls -la');  // Fails on Windows without Git Bash/WSL
```

## Package Managers

### Cross-Platform Package Management

| Task                | npm/yarn/pnpm       | pip                         | apt (Debian/Ubuntu)                       | brew (macOS)         | chocolatey (Windows)      |
| ------------------- | ------------------- | --------------------------- | ----------------------------------------- | -------------------- | ------------------------- |
| **Install package** | `npm install pkg`   | `pip install pkg`           | `sudo apt install pkg`                    | `brew install pkg`   | `choco install pkg`       |
| **Update package**  | `npm update pkg`    | `pip install --upgrade pkg` | `sudo apt update && sudo apt upgrade pkg` | `brew upgrade pkg`   | `choco upgrade pkg`       |
| **Remove package**  | `npm uninstall pkg` | `pip uninstall pkg`         | `sudo apt remove pkg`                     | `brew uninstall pkg` | `choco uninstall pkg`     |
| **List packages**   | `npm list`          | `pip list`                  | `dpkg --list`                             | `brew list`          | `choco list --local-only` |
| **Search packages** | `npm search query`  | `pip search query`          | `apt search query`                        | `brew search query`  | `choco search query`      |

### Development Environment Setup

```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install -y nodejs npm python3 python3-pip git curl
nvm install --lts

# macOS (Homebrew)
brew install node python git curl
nvm install --lts

# Windows (Chocolatey)
choco install nodejs-lts python git curl
nvm install --lts

# Windows (Scoop)
scoop install nodejs-lts python git curl
```

## Cross-Platform CI/CD

### GitHub Actions Matrix

```yaml
name: Cross-Platform CI

on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 22]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Platform-specific tests
        if: matrix.os == 'windows-latest'
        run: npm run test:windows

      - name: Platform-specific tests
        if: matrix.os == 'ubuntu-latest'
        run: npm run test:linux
```

## Cross-Platform Testing Strategy

### Platform Detection in Tests

```javascript
// Jest test with platform detection
describe('File operations', () => {
  const isWindows = process.platform === 'win32';

  test('should handle paths correctly', () => {
    const path = require('path');
    const testPath = path.join('data', 'test.txt');

    if (isWindows) {
      expect(testPath).toMatch(/\\/);
    } else {
      expect(testPath).toMatch(/\//);
    }
  });

  // Skip tests that don't work on Windows
  test.skipIf(isWindows)('should set file permissions', () => {
    // chmod tests only on Linux/macOS
  });
});

// Python test with platform detection
import unittest
import sys

class TestCrossPlatform(unittest.TestCase):
    def test_path_handling(self):
        from pathlib import Path
        path = Path('data') / 'test.txt'
        self.assertTrue(isinstance(path, Path))

    @unittest.skipIf(sys.platform == 'win32', "Linux/macOS only")
    def test_file_permissions(self):
        # chmod tests only on Linux/macOS
        import os
        os.chmod('test.txt', 0o755)
```

## Production Checklist

Before deploying cross-platform applications:

- [ ] Platform detection implemented
- [ ] Path handling uses platform-agnostic methods
- [ ] Line endings normalized (LF in Git)
- [ ] Shell commands work on all target platforms
- [ ] File permissions handled portably
- [ ] Environment variables accessed correctly
- [ ] Package managers documented for each platform
- [ ] CI/CD tests run on all platforms
- [ ] Platform-specific tests skipped appropriately
- [ ] Documentation includes platform-specific instructions
- [ ] Error messages are platform-agnostic
- [ ] Logging works across platforms
- [ ] Build artifacts are platform-specific when needed
- [ ] Installation scripts work on all platforms
- [ ] Configuration files are platform-agnostic

## Real-World Impact

**Before this skill:**

- "Works on my machine" bugs
- Shell scripts failing on Windows
- Path errors in production
- Line ending conflicts in Git
- Platform-specific assumptions in code

**After this skill:**

- Cross-platform compatibility from day one
- Shell scripts working on all platforms
- Path handling that never fails
- Clean Git history with normalized line endings
- Platform-aware code with proper fallbacks

## Cross-References

- **`docker-containerization`** - For containerized cross-platform deployment
- **`github-actions-cicd`** - For cross-platform CI/CD pipelines
- **`devops-pipeline`** - For deployment automation
- **`testing-strategy`** - For cross-platform test coverage

## References

- [Node.js process.platform](https://nodejs.org/api/process.html#processplatform)
- [Python sys.platform](https://docs.python.org/3/library/sys.html#sys.platform)
- [Git Line Endings](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
- [PowerShell Cross-Platform](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell)
- [Cross-env Documentation](https://github.com/kentcdodds/cross-env)
