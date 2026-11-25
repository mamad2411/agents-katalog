---
name: cmd
description: Cross-platform command-line reference (bash/zsh on Linux/Mac, cmd/PowerShell on Windows) covering navigation, file management, search (grep/find/ripgrep), process management, piping/redirection, and running Java/JavaScript programs from the terminal. Use when the user asks "how do I X from the terminal", wants to run/debug via CLI, or needs a shell command equivalent across OSes.
---

# Skill: Command Line (CMD / Terminal)

> **Purpose**: Navigate, run, and debug from the terminal with confidence.

## When to Use
- Running Java or JavaScript programs
- File and directory management
- Searching for files or text
- Process management
- Quick debugging via terminal

---

## Essential Navigation

```bash
# Where am I?
pwd                     # Linux/Mac
cd                      # Windows (just cd shows path)

# List contents
ls -la                  # Linux/Mac (detailed)
dir                     # Windows

# Move around
cd projects/my-app      # Go into directory
cd ..                   # Go up one level
cd ~                    # Go to home directory (Linux/Mac)
cd %USERPROFILE%        # Go to home directory (Windows)

# Create / delete
mkdir src               # Create directory
mkdir -p src/main/java  # Create nested directories (Linux/Mac)

rm file.txt             # Delete file (Linux/Mac)
del file.txt            # Delete file (Windows)

rm -rf node_modules     # Delete directory (Linux/Mac)
rmdir /s /q node_modules  # Delete directory (Windows)
```

---

## Running Programs

### JavaScript (Node.js)
```bash
# Run a file
node app.js

# Run with arguments
node app.js --port 3000

# Interactive REPL
node
> 2 + 2
4
> .exit

# Run npm scripts
npm start
npm run dev
npm test
```

### Java
```bash
# Compile
javac Main.java

# Compile with multiple files
javac -d out src/*.java

# Run
java Main

# Run from output directory
java -cp out Main

# Compile and run (one-liner)
javac Main.java && java Main
```

---

## File Operations

```bash
# View file contents
cat file.txt            # Print entire file (Linux/Mac)
type file.txt           # Print entire file (Windows)

# View first/last lines
head -20 server.log     # First 20 lines
tail -50 server.log     # Last 50 lines
tail -f server.log      # Live follow (great for debugging)

# Search in files
grep "error" server.log             # Find lines with "error"
grep -r "TODO" src/                 # Search recursively in directory
grep -n "function" app.js           # Show line numbers

# Find files
find . -name "*.java"               # Find all Java files (Linux/Mac)
dir /s /b *.java                    # Find all Java files (Windows)

# Copy / Move
cp original.txt backup.txt          # Copy
mv old-name.js new-name.js          # Rename/move
```

---

## Debugging via Terminal

### Check if a Port is in Use
```bash
# Linux/Mac
lsof -i :3000

# Windows
netstat -ano | findstr :3000
```

### Check Running Processes
```bash
# Linux/Mac
ps aux | grep node

# Windows
tasklist | findstr node
```

### Kill a Process
```bash
# Linux/Mac
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

### Monitor Resource Usage
```bash
# Linux/Mac
top
htop       # Better version (install with: brew install htop)

# Windows
taskmgr    # Opens Task Manager
```

---

## Useful Real Commands

```bash
# Count lines of code in a project
find . -name "*.java" | xargs wc -l     # Linux/Mac
(Get-ChildItem -Recurse *.java | Get-Content | Measure-Object -Line).Lines  # PowerShell

# Check disk space
df -h       # Linux/Mac
wmic logicaldisk get size,freespace,caption  # Windows

# Download a file
curl -O https://example.com/file.zip

# Check internet connectivity
ping google.com

# View environment variables
env          # Linux/Mac
set          # Windows CMD
$env:PATH    # PowerShell

# Chain commands
# Run second only if first succeeds
javac Main.java && java Main

# Run second regardless
npm install; npm start

# Redirect output to file
node app.js > output.log 2>&1
```

---

## PowerShell Quick Reference (Windows)

```powershell
# Navigate
Set-Location .\src
Get-Location

# List files
Get-ChildItem -Recurse -Filter *.java

# Read file
Get-Content .\app.js

# Search in files
Select-String -Path .\src\*.java -Pattern "TODO"

# Environment variables
$env:JAVA_HOME
[System.Environment]::GetEnvironmentVariable("PATH")
```

---

## Best Practices
1. **Use tab completion** — press Tab to auto-complete file/folder names
2. **Use `&&`** — chain commands so the next only runs if the previous succeeds
3. **Use `history`** — find and reuse previous commands
4. **Create aliases** — for commands you type often
5. **Redirect output** — `> file.log` to save, `2>&1` to include errors

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| Running in wrong directory | Always `pwd` / `cd` first |
| Forgetting to compile Java | `javac` before `java` |
| Deleting without checking | `ls` the directory before `rm -rf` |
| Not reading error output | Read the full error message, it usually tells you what's wrong |
| Ignoring exit codes | `echo $?` (Linux) or `$LASTEXITCODE` (PowerShell) after commands |
