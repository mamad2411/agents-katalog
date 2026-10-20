# Terminal Command Isolation Protocol

## ⚠️ CRITICAL: MANDATORY TERMINAL ISOLATION ⚠️

**ABSOLUTE RULE**: Every terminal command must be executed in a NEW terminal window/tab. No exceptions whatsoever.

**This protocol exists because:**

- Asynchronous processes (dev servers, build watchers) block terminal input
- Git commands fail when terminals are busy with background processes
- Command execution appears to work but silently fails
- Terminal state pollution causes unpredictable behavior

## 1. Core Protocol Requirements

### 1.1 NEW TERMINAL FOR EVERY COMMAND

- **NEVER** reuse an existing terminal for any command
- **ALWAYS** open a fresh terminal window/tab before executing any command
- **NEVER** assume a terminal is free even if it appears idle
- **NEVER** queue commands in the same terminal

### 1.2 TERMINAL VERIFICATION CHECKLIST

Before executing any command:

- [ ] Open NEW terminal window/tab
- [ ] Verify terminal prompt is ready (shows working directory)
- [ ] Check no background processes are running
- [ ] Ensure terminal is not showing any async output

### 1.3 COMMAND EXECUTION SEQUENCE

1. **Open new terminal** (Ctrl+Shift+T or equivalent)
2. **Verify clean prompt** (no background processes)
3. **Execute single command**
4. **Wait for command completion** (exit code displayed)
5. **Close terminal when done** (optional but recommended)

## 2. Development Server Management

### 2.1 LIVE SERVER IDENTIFICATION

These commands create persistent processes that BLOCK terminals:

- `pnpm dev` / `npm run dev` / `yarn dev`
- `vite` / `vite dev` / `vite serve`
- `npx vite` / `npx vite dev`
- `python -m http.server`
- `node server.js` (or any Node.js server)
- `firebase serve` / `firebase emulators:start`

### 2.2 SERVER TERMINAL ISOLATION

- **DEDICATED TERMINAL**: Always run dev servers in dedicated terminals
- **NEVER MIX**: Never run other commands in server terminals
- **CLEAR IDENTIFICATION**: Label server terminals clearly
- **SEPARATE WORKFLOWS**: Use completely separate terminals for git/build commands

### 2.3 SERVER DETECTION INDICATORS

A terminal is BUSY if it shows:

- Continuous log output
- Server startup messages
- "Local: http://localhost:3000" or similar
- Webpack/Vite compilation messages
- Any ongoing process output

## 3. Git Workflow Isolation

### 3.1 MANDATORY GIT PROTOCOL

**EACH git command must run in a NEW terminal:**

```bash
# WRONG - All in same terminal
git checkout -b feature/new-feature
git add .
git commit -m "Add feature"
git push origin feature/new-feature

# CORRECT - Each in new terminal
# Terminal 1:
git checkout -b feature/new-feature

# Terminal 2:
git add .

# Terminal 3:
git commit -m "Add feature"

# Terminal 4:
git push origin feature/new-feature
```

### 3.2 CRITICAL GIT COMMANDS

These commands are HIGH RISK and must use new terminals:

- `git checkout` / `git switch`
- `git pull` / `git push`
- `git merge` / `git rebase`
- `gh pr create` / `gh pr merge`
- `git commit` / `git add`

### 3.3 BRANCH SWITCHING PROTOCOL

When switching branches:

1. **NEW TERMINAL**: Open fresh terminal
2. **VERIFY STATUS**: `git status` to check clean state
3. **SWITCH BRANCH**: `git checkout development`
4. **VERIFY SWITCH**: `git branch` to confirm current branch
5. **CLOSE TERMINAL**: Close when operation complete

## 4. Common Violation Scenarios

### 4.1 SCENARIO: Dev Server Running

```bash
# Terminal showing:
VITE v5.4.19  ready in 1234 ms
Local:   http://localhost:3000/
Network: use --host to expose

# USER ATTEMPTS (WRONG):
git checkout development  # COMMAND WILL NOT EXECUTE

# CORRECT APPROACH:
# 1. Leave dev server terminal running
# 2. Open NEW terminal
# 3. Execute git checkout development
```

### 4.2 SCENARIO: Build Process Active

```bash
# Terminal showing:
npm run build
Building for production...
[████████████████] 100% (processing...)

# USER ATTEMPTS (WRONG):
git push origin main  # WILL FAIL SILENTLY

# CORRECT APPROACH:
# 1. Let build complete in current terminal
# 2. Open NEW terminal for git command
```

### 4.3 SCENARIO: Multiple Git Commands

```bash
# WRONG APPROACH - Reusing terminal:
Terminal 1: git add .
Terminal 1: git commit -m "message"  # MAY FAIL
Terminal 1: git push  # MAY FAIL

# CORRECT APPROACH - New terminal each:
Terminal 1: git add .
Terminal 2: git commit -m "message"
Terminal 3: git push
```

## 5. Pre-Execution Verification

### 5.1 TERMINAL STATUS CHECK

Before ANY command, verify:

- [ ] Fresh terminal window opened
- [ ] Prompt shows current directory
- [ ] No background process output visible
- [ ] No "waiting" or "building" indicators
- [ ] Terminal accepts input immediately

### 5.2 ASYNC PROCESS DETECTION

Signs a terminal is BUSY with async processes:

- Continuous output scrolling
- Periodic status updates
- "Watching for changes..." messages
- Server listening messages
- Compilation progress indicators
- Any ongoing process that hasn't returned to prompt

### 5.3 COMMAND COMPLETION VERIFICATION

Ensure command completed by checking:

- [ ] Exit code displayed (usually 0 for success)
- [ ] Prompt returned to normal state
- [ ] No error messages present
- [ ] Expected output received

## 6. Emergency Recovery Procedures

### 6.1 WHEN COMMANDS DON'T EXECUTE

If a command appears to not execute:

1. **STOP**: Don't repeat the command
2. **NEW TERMINAL**: Open completely fresh terminal
3. **VERIFY STATE**: Check git status, file system state
4. **RE-EXECUTE**: Run the command in new terminal
5. **DOCUMENT**: Note what caused the failure

### 6.2 STUCK TERMINAL RECOVERY

If terminal becomes unresponsive:

1. **DON'T WAIT**: Don't try to "fix" the stuck terminal
2. **NEW TERMINAL**: Open fresh terminal immediately
3. **KILL PROCESS**: `Ctrl+C` or close stuck terminal
4. **CONTINUE**: Proceed with new terminal

### 6.3 GIT STATE RECOVERY

If git commands fail silently:

1. **NEW TERMINAL**: Open fresh terminal
2. **CHECK STATUS**: `git status` to verify current state
3. **VERIFY BRANCH**: `git branch` to confirm location
4. **RETRY OPERATIONS**: Re-execute failed commands
5. **PUSH VERIFICATION**: `git log --oneline -3` to verify commits

## 7. Tool-Specific Protocols

### 7.1 GITHUB CLI (gh)

```bash
# Each in NEW terminal:
# Terminal 1:
gh pr create --title "Feature" --body "Description"

# Terminal 2:
gh pr merge --squash

# Terminal 3:
gh pr list --state closed
```

### 7.2 PACKAGE MANAGERS

```bash
# Each in NEW terminal:
# Terminal 1:
pnpm install

# Terminal 2:
pnpm build

# Terminal 3:
pnpm test
```

### 7.3 BUILD TOOLS

```bash
# Each in NEW terminal:
# Terminal 1:
npx tsc --noEmit

# Terminal 2:
npx playwright test

# Terminal 3:
npx vite build
```

## 8. Success Validation

### 8.1 PROTOCOL COMPLIANCE CHECKLIST

After each command execution session:

- [ ] Every command executed in new terminal
- [ ] No commands failed due to busy terminals
- [ ] All git operations completed successfully
- [ ] No silent command failures occurred
- [ ] Terminal isolation maintained throughout

### 8.2 WORKFLOW VALIDATION

For git workflows specifically:

- [ ] Branch switches completed successfully
- [ ] All commits were actually created
- [ ] Push operations transferred to remote
- [ ] PR operations completed as expected
- [ ] No "command not found" or hanging behavior

### 8.3 FAILURE INDICATORS

Signs of protocol violation:

- Commands appear to execute but nothing happens
- Git operations don't change repository state
- Hanging behavior without error messages
- Inconsistent terminal responses
- Background processes interfering with commands

## 9. Enforcement Rules

### 9.1 ZERO TOLERANCE POLICY

- **NO EXCEPTIONS**: Every command requires new terminal
- **NO SHORTCUTS**: Even "quick" commands need new terminal
- **NO ASSUMPTIONS**: Never assume terminal is free
- **NO REUSE**: Never reuse terminals for different command types

### 9.2 MANDATORY COMPLIANCE

This protocol must be followed for:

- **ALL git commands** without exception
- **ALL build/test commands**
- **ALL package manager operations**
- **ALL deployment commands**
- **ALL debugging/diagnostic commands**

### 9.3 CONSEQUENCES OF VIOLATION

Protocol violations result in:

- Silent command failures
- Inconsistent repository state
- Failed git operations
- Wasted development time
- Potential data loss or corruption
- Broken automated workflows

---

## ✅ PROTOCOL SUMMARY

**REMEMBER**: When in doubt, open a new terminal. Terminal isolation is MANDATORY, not optional.

**GOLDEN RULE**: One command, one terminal, always.

**NEVER AGAIN**: This protocol exists to prevent the exact failures experienced previously. Follow it religiously.
