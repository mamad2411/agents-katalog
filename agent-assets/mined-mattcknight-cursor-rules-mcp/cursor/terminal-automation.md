---
description: Terminal Automation Rules - Critical rules for preventing command execution failures and race conditions
alwaysApply: true
---

# Terminal Automation Rules - CRITICAL

## 🚨🚨🚨 PRE-FLIGHT CHECKLIST 🚨🚨🚨

**BEFORE RUNNING ANY DOCKER COMMAND, ASK YOURSELF:**
1. ✅ Did I generate a timestamp? (`$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"`)
2. ✅ Did I create the log directory? (`New-Item -ItemType Directory -Path ".\logs\docker" -Force`)
3. ✅ Did I add `*>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_OPERATION.log"`?
4. ✅ If NO to any above → STOP AND FIX BEFORE RUNNING!

**IF YOU VIOLATE THIS RULE, THE USER WILL RIGHTFULLY BE ANGRY.**

---

## Core Principle

**NEVER use commands that require manual user intervention for pagination or interaction.**

---

## Mandatory Rules

### 1. Git Commands with Pagination

❌ **NEVER use these commands without limits:**
- `git show` (uses pager, can paginate)
- `git log` (uses pager, will paginate)
- `git log --oneline` (will paginate if > screen height)
- `git diff` (uses pager, can paginate)
- `git blame` (uses pager)
- `git branch -a` (paginates long lists)

✅ **ALWAYS use with --no-pager AND limits:**

**Git Log:**
```powershell
git --no-pager log --oneline -3     # ✅ Last 3 commits
git --no-pager log --oneline -5     # ✅ Last 5 commits (typical)
git --no-pager log --oneline -10    # ✅ Last 10 commits (max)
```

**Git Show:**
```powershell
git --no-pager show --stat HEAD     # ✅ Stats only, no full diff
git --no-pager show --stat --oneline HEAD  # ✅ Even more compact
```

**Git Diff:**
```powershell
git --no-pager diff --stat          # ✅ Summary only
git --no-pager diff --shortstat     # ✅ Very brief summary
git --no-pager diff --name-only     # ✅ File names only
```

**Git Branch:**
```powershell
git branch -a | Select-Object -First 10  # ✅ Limit branch list
```

**OR use output redirection:**
- `git show | Out-String` (PowerShell)
- `git show 2>&1` (capture all output)

### 2. File Reading Commands

❌ **NEVER use these (cause pagination or not available):**
- `less` (interactive pager)
- `more` (requires Space/Enter)
- `cat <large-file>` (may paginate)
- `head` (not available in PowerShell)
- `tail` (may have issues in PowerShell)

✅ **ALWAYS use PowerShell cmdlets with limits:**
```powershell
Get-Content <file> -TotalCount 20   # ✅ First 20 lines
Get-Content <file> -Tail 20         # ✅ Last 20 lines
Select-String "pattern" <file>      # ✅ Grep equivalent
```

### 3. Default Limits to Use

| Command Type | Default Limit | Rationale |
|--------------|---------------|-----------|
| `git log` | `-3` to `-5` | Show recent context without scrolling |
| `git show` | `--stat HEAD` | Summary sufficient, avoid full diff |
| `git branch` | First 10 | Rarely need to see all branches |
| File content | 20-50 lines | Enough context, no pagination |
| `git diff` | `--stat` | Summary shows what changed |

### 4. Interactive Prompts

❌ **NEVER use commands that prompt for input without non-interactive flags:**
- `npm install` → use `npm install --yes` or `npm ci`
- `pip install` without `-q` flag
- Commands that ask yes/no questions

✅ **ALWAYS use:**
- Non-interactive flags (`--yes`, `--force`, `-y`, `-q`)
- Automation-friendly alternatives
- Redirect stdin from `/dev/null` if needed

### 5. Docker Operations - ALWAYS Use Physical Logs ⚠️🚨🔴

**🚨🚨🚨 CRITICAL: ALL Docker Compose operations MUST write to physical log files. 🚨🚨🚨**

**THIS IS A ZERO-TOLERANCE RULE. VIOLATION = IMMEDIATE FAILURE.**

Docker commands produce massive output that:
- Gets truncated (200KiB/s log limit)
- Takes forever to stream
- Makes it impossible to see what's happening
- Wastes time waiting for output that already happened
- **USER HAS REPEATEDLY TOLD YOU THIS - STOP VIOLATING IT!**

❌ **NEVER run Docker commands without logging:**
```powershell
docker compose build                    # ❌ VIOLATION - NO LOGGING!
docker compose up                       # ❌ VIOLATION - NO LOGGING!
docker compose up --build               # ❌ VIOLATION - NO LOGGING!
docker compose up data-seeder           # ❌ VIOLATION - NO LOGGING!
docker compose down                     # ❌ VIOLATION - NO LOGGING!
docker compose logs service             # ❌ VIOLATION - NO LOGGING!
docker compose ps                       # ⚠️ OK (quick status check, no massive output)
```

✅ **ALWAYS use Tee-Object to write to organized, timestamped logs:**
```powershell
# STEP 1: Generate timestamp for log file (MANDATORY FIRST STEP)
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# STEP 2: Create component-specific log directories (MANDATORY)
New-Item -ItemType Directory -Path ".\logs\docker" -Force | Out-Null

# STEP 3: Run Docker command WITH logging (MANDATORY)
# Build all services with logging
docker compose build *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_build-all.log"

# Up with logging
docker compose up *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_up.log"

# Up --build with logging
docker compose up --build *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_up-build.log"

# Up specific service with logging (THIS IS WHAT YOU MISSED!)
docker compose up data-seeder *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_up-data-seeder.log"

# Up specific service in detached mode with logging
docker compose up -d data-seeder *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_up-data-seeder-detached.log"

# Down with logging
docker compose down *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_down.log"

# Down with volumes with logging
docker compose down -v *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_down-all.log"

# Individual service build with logging
docker compose build data-seeder *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_build-data-seeder.log"
docker compose build api *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_build-api.log"

# Logs command with logging (if output is large)
docker compose logs --tail 100 *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_logs-tail.log"
docker compose logs data-seeder *>&1 | Tee-Object -FilePath ".\logs\docker\${timestamp}_logs-data-seeder.log"
```

**MANDATORY PATTERN FOR EVERY DOCKER COMMAND:**
```powershell
# ALWAYS follow this pattern:
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "logs/docker/${timestamp}_OPERATION.log"
docker compose COMMAND *>&1 | Tee-Object -FilePath $logFile
```

**WHERE OPERATION = the action being performed:**
- `build-all` (build all services)
- `build-data-seeder` (build specific service)
- `up` (start all services)
- `up-data-seeder` (start specific service)
- `down` (stop services)
- `down-all` (stop + remove volumes)
- `logs-data-seeder` (view logs for service)

**Why `*>&1`?**
- Captures ALL streams (stdout, stderr, warnings)
- Ensures nothing is lost
- Critical for Docker which uses multiple output streams

**Log Directory Structure:**
```
logs/
├── docker/
│   ├── 20251114_093700_build-all.log
│   ├── 20251114_094500_up.log
│   └── 20251114_095200_down.log
├── data-seeder/
│   ├── 20251114_093700_build.log
│   └── 20251114_094800_build.log
├── api/
│   ├── 20251114_093700_build.log
│   └── 20251114_095000_build.log
├── mssql/
│   └── 20251114_093700_build.log
└── embedding-service/
    └── 20251114_093700_build.log
```

**Log File Naming Convention:**
- **Pattern**: `logs/{component}/{YYYYMMDD_HHMMSS}_{operation}.log`
- **Component folder**: Separate context (docker, api, data-seeder, mssql, etc.)
- **Timestamp**: `YYYYMMDD_HHMMSS` format
- **Operation**: build, up, down, test, etc.

**Why Component Folders?**
- Organize logs by component/context
- Easy to find all logs for a specific service
- Separate Docker orchestration from individual services
- Clean organization prevents log clutter

**Why Timestamps?**
- Each execution has its own log (no overwriting)
- Can compare logs from different runs
- Historical record of all operations
- Easy to identify when operation occurred

**Monitoring Logs in Real-Time:**
```powershell
# Watch latest log file for a component
$latestLog = Get-ChildItem ".\logs\docker\*_build-all.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $latestLog.FullName -Wait -Tail 30

# Check progress (specific file)
Get-Content ".\logs\data-seeder\20251114_093700_build.log" -Tail 50
```

**MANDATORY Workflow:**
1. **Create logs directory** (if it doesn't exist)
2. **Start Docker operation** with `Tee-Object` to log file
3. **Monitor log file** with `Get-Content -Wait -Tail N`
4. **Check results** in log file after completion

**Never Waste Time:**
- Physical logs let you see what already happened
- No waiting for streaming output
- No lost output due to truncation
- User can monitor progress in real-time by opening the log file

### 6. Long-Running Commands

For commands expected to run indefinitely:
- Set `is_background: true` in the tool call
- Don't use blocking commands in foreground

### 7. Testing Commands Before Execution

**Before running any git or file command, ask yourself:**
- ❓ Could this output be more than 20-30 lines?
- ❓ Does this require scrolling?
- ❓ Will the user need to press a key?

**If ANY answer is "yes" or "maybe":**
- ✅ Add `-N` limit to git commands
- ✅ Pipe to `Select-Object -First N`
- ✅ Use `--stat` instead of full output
- ✅ Use `--name-only` for file lists

### 8. Testing Commands First

When unsure if a command will paginate or prompt:
- Test with small inputs first
- Add output limiting to prevent pagination
- Use `--help` to check for non-interactive flags

---

## Examples

### Common Violations & Fixes

#### Violation 1: Checking Recent Commits

❌ **WRONG - May paginate:**
```powershell
git log --oneline
```

✅ **CORRECT - Always limited:**
```powershell
git --no-pager log --oneline -5
```

#### Violation 2: Showing Commit Details

❌ **WRONG - Full diff paginates:**
```powershell
git show HEAD
```

✅ **CORRECT - Stats only:**
```powershell
git --no-pager show --stat HEAD
```

#### Violation 3: Viewing File Changes

❌ **WRONG - Full diff paginates:**
```powershell
git diff
```

✅ **CORRECT - Summary only:**
```powershell
git --no-pager diff --stat
```

#### Violation 4: Long File Content

❌ **WRONG - May be too long:**
```powershell
cat large-file.txt
```

✅ **CORRECT - Limited lines:**
```powershell
Get-Content large-file.txt -TotalCount 30
```

#### Violation 5: Interactive Package Managers

❌ **WRONG:**
```bash
npm install
pip install package
```

✅ **CORRECT:**
```bash
npm install --yes
pip install -q package
```

---

## PowerShell Specific

### Output Capture

Use `Out-String` to force non-interactive output:

```powershell
git show | Out-String
Get-Content file.txt | Out-String
```

### Redirects

Use `2>&1` to capture all output:

```powershell
command 2>&1
```

### Race Condition Mitigation - CRITICAL ⚠️

**Cursor has race conditions with PowerShell command execution.**

Commands complete before output can be captured, resulting in:
- Empty output despite successful execution
- "Command was interrupted" errors
- Incomplete responses

✅ **ALWAYS add 1-second delay after command completion:**

```powershell
# PowerShell
Copy-Item -Path source -Destination dest; Start-Sleep -Seconds 1; Write-Host "Done"
mkdir directory; Start-Sleep -Seconds 1; echo "Created"
```

**This is MANDATORY for all PowerShell commands to ensure output is captured.**

**For Unix/Linux shells:**

```bash
# Add delay after critical commands
command && sleep 1 && echo "Done"
```

---

## Git Command Execution Pattern - MANDATORY ⚠️

**ALL git commands MUST follow this pattern:**

1. Execute git command
2. Sleep 1 second (prevents race conditions)
3. Write host context of what was completed

### Standard Pattern

**PowerShell:**
```powershell
# Pattern: git <command>; Start-Sleep -Seconds 1; Write-Host "✅ Git <operation> completed: <context>"

# Examples:
git init --initial-branch=develop; Start-Sleep -Seconds 1; Write-Host "✅ Git repository initialized: develop branch created"
git add .; Start-Sleep -Seconds 1; Write-Host "✅ Git staging completed: all files staged"
git commit -m "message"; Start-Sleep -Seconds 1; Write-Host "✅ Git commit completed: Initial commit (53 files, 19327 insertions)"
git push origin develop; Start-Sleep -Seconds 1; Write-Host "✅ Git push completed: pushed to origin/develop"
git branch feature/new-feature; Start-Sleep -Seconds 1; Write-Host "✅ Git branch created: feature/new-feature"
```

**Unix/Linux:**
```bash
# Pattern: git <command> && sleep 1 && echo "✅ Git <operation> completed: <context>"

# Examples:
git init --initial-branch=develop && sleep 1 && echo "✅ Git repository initialized: develop branch created"
git add . && sleep 1 && echo "✅ Git staging completed: all files staged"
git commit -m "message" && sleep 1 && echo "✅ Git commit completed: Initial commit (53 files, 19327 insertions)"
git push origin develop && sleep 1 && echo "✅ Git push completed: pushed to origin/develop"
```

### Context Information to Include

The `Write-Host`/`echo` message should include:
- **Operation type**: What git operation was performed (init, add, commit, push, etc.)
- **Key details**: Relevant information from the command output
  - For commits: number of files changed, insertions/deletions
  - For push: destination branch/remote
  - For branches: branch name created/checked out
  - For init: branch name or repository details

### Examples with Context

```powershell
# Commit with detailed context
git commit -m "Initial commit"; Start-Sleep -Seconds 1; Write-Host "✅ Git commit completed: Initial commit - 53 files changed, 19327 insertions(+)"

# Push with remote context
git push --set-upstream origin develop; Start-Sleep -Seconds 1; Write-Host "✅ Git push completed: pushed to origin/develop, upstream set"

# Branch creation with context
git checkout -b feature/PROJ-123-new-feature; Start-Sleep -Seconds 1; Write-Host "✅ Git branch created: feature/PROJ-123-new-feature checked out"

# Status check (if needed)
git status; Start-Sleep -Seconds 1; Write-Host "✅ Git status checked: working tree clean"
```

### Why This Pattern?

1. **Race Condition Prevention**: The 1-second delay ensures output is captured before Cursor processes the result
2. **Clear Feedback**: User immediately knows what completed and key details
3. **Consistency**: All git operations follow the same pattern for predictable behavior
4. **Debugging**: Context messages help identify what happened if something goes wrong

### When Context is Unavailable

If git command output is not available (e.g., for init, remote add):
```powershell
# Still follow pattern, use operation name
git remote add origin <url>; Start-Sleep -Seconds 1; Write-Host "✅ Git remote added: origin configured"
```

---

## Command Chaining Rules

### Never Chain Commands

❌ **BAD:**
```powershell
Copy-Item "a.md" "b.md"; Copy-Item "c.md" "d.md"
```

✅ **GOOD:**
```powershell
# Execute one command, wait, then next
Copy-Item "a.md" "b.md"
Start-Sleep -Seconds 1
Copy-Item "c.md" "d.md"
Start-Sleep -Seconds 1
```

### Single Operation Per Command

- One file copy at a time
- One directory creation at a time
- One validation check at a time

### Limit Recursive Operations

❌ **BAD:**
```powershell
Get-ChildItem -Recurse  # Without limits
```

✅ **GOOD:**
```powershell
Get-ChildItem -Depth 1  # or -Depth 2
```

---

## Environment Variables

Set these in shell if needed:

**Unix/Linux:**
```bash
export GIT_PAGER=cat
export PAGER=cat
```

**PowerShell:**
```powershell
$env:GIT_PAGER = "cat"
```

---

## Error Handling

**If ANY command fails:**
1. Acknowledge immediately: "❌ Error occurred"
2. Explain what went wrong
3. Provide options to user
4. DON'T continue silently

---

## Progress Updates

**For operations > 30 seconds:**
- Warn user: "This may take 1-2 minutes"
- Provide progress: "Creating file 3 of 10..."
- Give timeout guidance if appears stuck

---

## Zero Tolerance

- Commands requiring manual intervention waste time
- Pagination breaks automation
- Interactive prompts block execution
- Always assume user is unavailable to interact
- Race conditions cause incomplete output

---

## Priority Order

When showing information, prioritize:
1. **Brevity** - Show only what's needed
2. **Limits** - Always cap output
3. **Stats** - Summaries over full content
4. **Feedback** - Clear output messages

## Remember

> **The user should NEVER need to press ANY key to continue.**
> 
> If they do, you have failed automation.

**Critical Rules:**
1. Always add 1-second delay after PowerShell commands to prevent race conditions
2. Always limit git command output to prevent pagination
3. Never use interactive commands without non-interactive flags
4. **MANDATORY for git commands**: Execute → Sleep 1 second → Write host context of completion

**IF IN DOUBT, LIMIT THE OUTPUT.**

It's better to show less and have the user ask for more, than to show too much and require pagination.

---

## Best Practices

1. **Test commands first** - Verify non-interactive behavior
2. **Use delays** - Prevent race conditions with output capture
3. **Check for flags** - Always look for non-interactive options
4. **Limit output** - Prevent pagination with output limiting
5. **Handle errors** - Acknowledge failures immediately
6. **One command at a time** - Sequential execution prevents issues
