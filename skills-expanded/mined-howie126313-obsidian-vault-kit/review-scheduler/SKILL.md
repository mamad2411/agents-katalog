---
name: review-scheduler
description: |
  (macOS only) Spaced repetition review scheduler for Obsidian. Based on the Ebbinghaus forgetting curve, auto-reminds you to review articles at optimal intervals via macOS launchd + screen unlock detection.
  Triggers: "/review-scheduler", "set up review reminders", "start review scheduler", "stop review scheduler"
allowed-tools:
  - Glob
  - Read
  - Write
  - AskUserQuestion
  - Bash(which *)
  - Bash(python3 *)
  - Bash(pip3 *)
  - Bash(swiftc *)
  - Bash(mkdir *)
  - Bash(launchctl *)
---

# Review Scheduler

Manage spaced repetition review reminders for the Obsidian vault.

## Argument Parsing

Parse user input arguments (args) to determine which subcommand to run:
- No args or `start` → execute **Start Flow**
- `stop` → execute **Stop Flow**
- `status` → execute **Status Check**

---

## Start Flow

### Step 0: Platform Check

This skill requires **macOS**. Check the platform first:

```bash
uname -s
```

If the output is not `Darwin`, inform the user that this skill is macOS-only (requires launchd, Swift compiler, and osascript) and stop.

### Step 0.5: Dependency Check

Before any action, run these checks:

```bash
which python3 && python3 --version
python3 -c "import yaml; print('PyYAML OK')"
which swiftc
```

If any dependency is missing, **stop immediately and report to user**:
- Python 3 missing: suggest `brew install python3`
- PyYAML missing: suggest `pip3 install pyyaml`
- swiftc missing: suggest `xcode-select --install`

Proceed only after all checks pass.

### Step 1: Ask User for Scheduled Time

Use AskUserQuestion to ask:
> "What time would you like to receive daily review reminders? (default 9:00, format: 08:30, 21:00)"

Parse user input into Hour and Minute. If user presses enter or says "default", use 9:00.

### Step 2: Check Existing Deployment

```bash
launchctl list 2>/dev/null | grep com.obsidian-vault-kit.review
```

- If already running → inform user "Review scheduler is already active", ask if they want to update the scheduled time
- If user doesn't want to update → end
- If user wants to update → run Stop Flow first, then continue with deployment

### Step 3: Deploy Files

1. **Detect vault path**: follow [../../_shared/common-steps.md](../../_shared/common-steps.md) "Vault Detection" section, store as `$VAULT_ROOT`
2. **Detect vault name**: take the directory name of `$VAULT_ROOT`
3. **Create `.review/` directory**: `mkdir -p $VAULT_ROOT/.review`
4. **Create `reviews/` directory**: `mkdir -p $VAULT_ROOT/reviews`

5. **Deploy review_reminder.py**:
   - Read [references/review_reminder.py](references/review_reminder.py)
   - Replace `{{VAULT_PATH}}` with the actual `$VAULT_ROOT` absolute path
   - Replace `{{VAULT_NAME}}` with the actual vault name
   - Write to `$VAULT_ROOT/.review/review_reminder.py`

6. **Deploy unlock_watcher.swift**:
   - Read [references/unlock_watcher.swift](references/unlock_watcher.swift)
   - Replace `{{PYTHON_PATH}}` with the result of `which python3`
   - Replace `{{SCRIPT_PATH}}` with `$VAULT_ROOT/.review/review_reminder.py`
   - Write to `$VAULT_ROOT/.review/unlock_watcher.swift`
   - Compile: `swiftc $VAULT_ROOT/.review/unlock_watcher.swift -o $VAULT_ROOT/.review/unlock_watcher -framework Cocoa`

7. **Deploy launchd plist (scheduled task)**:
   - Read [references/com.obsidian-vault-kit.review.plist](references/com.obsidian-vault-kit.review.plist)
   - Replace `{{PYTHON_PATH}}`, `{{SCRIPT_PATH}}`, `{{HOUR}}`, `{{MINUTE}}`
   - Write to `~/Library/LaunchAgents/com.obsidian-vault-kit.review.plist`

8. **Deploy launchd plist (unlock watcher)**:
   - Read [references/com.obsidian-vault-kit.review-watcher.plist](references/com.obsidian-vault-kit.review-watcher.plist)
   - Replace `{{WATCHER_PATH}}` with `$VAULT_ROOT/.review/unlock_watcher`
   - Write to `~/Library/LaunchAgents/com.obsidian-vault-kit.review-watcher.plist`

### Step 4: Start Scheduled Tasks

```bash
launchctl load ~/Library/LaunchAgents/com.obsidian-vault-kit.review.plist
launchctl load ~/Library/LaunchAgents/com.obsidian-vault-kit.review-watcher.plist
```

### Step 5: Run Once for Verification

```bash
python3 $VAULT_ROOT/.review/review_reminder.py
```

Check whether a review note was generated (if any articles are due for review today).

### Step 6: Report Results

Report to user:
- Scheduled task is active, daily reminder at HH:MM
- Screen unlock also triggers a check
- Review notes are saved in the `reviews/` directory
- To stop, run `/review-scheduler stop`

---

## Stop Flow

### Step 1: Check If Running

```bash
launchctl list 2>/dev/null | grep com.obsidian-vault-kit.review
```

If not running → inform user "Review scheduler is not active" → end

### Step 2: Unload Tasks

```bash
launchctl unload ~/Library/LaunchAgents/com.obsidian-vault-kit.review.plist 2>/dev/null
launchctl unload ~/Library/LaunchAgents/com.obsidian-vault-kit.review-watcher.plist 2>/dev/null
rm -f ~/Library/LaunchAgents/com.obsidian-vault-kit.review.plist
rm -f ~/Library/LaunchAgents/com.obsidian-vault-kit.review-watcher.plist
```

Note: keep `.review/` directory and existing review notes in `reviews/` — do not delete user data.

### Step 3: Report

Inform user that the scheduled tasks have been stopped. Existing review notes are preserved.

---

## Status Check

```bash
# Check scheduled tasks
launchctl list 2>/dev/null | grep com.obsidian-vault-kit.review
```

```
# Recent review notes (use native Glob, no Bash needed)
Glob("*.md", path="$VAULT_ROOT/reviews")
```

Report to user:
- Whether the scheduled tasks are running
- Most recent review note filenames
- Whether today's review note exists
