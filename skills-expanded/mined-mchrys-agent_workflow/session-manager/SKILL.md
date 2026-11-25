---
name: session-manager
description: Manage tmux sessions for plans, tasks, specs, and explorations with automatic Claude Code integration and intelligent state detection. Use when user asks to create/open/control/monitor/clean/unlock tmux sessions, work on plans/tasks/specs/explorations, execute plans, run explorations, write specs, implement tasks, manipulate Claude sessions in background, clean up finished sessions, or unlock blocked sessions. Features detailed Claude state detection (coding, testing, committing, pushing, completed). Triggers on keywords like execution plan, exploration, specification, implement plan, run exploration, work on spec, background session, parallel execution, monitor progress, clean sessions, unlock blocked sessions, stuck sessions, frozen sessions, session status, session tree, show sessions.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# tmux Session Manager Skill

## Objective
Automate creation, control, monitoring, cleanup, and unlocking of tmux sessions for OpenRAG development workflow with integrated Claude Code support.

## When to Use
- User asks to **execute a plan** or **work on a plan** (`.agents/plans/`)
- User wants to **run an exploration** or **conduct R&D** (`.agents/explorations/`)
- User requests to **write/update a spec** or **work on specification** (`.agents/specs/`)
- User asks to **implement a task** or **work on a task** (`.agents/tasks/`)
- User wants to **work in background** or **parallel execution**
- User requests to **create/open tmux session** for any agent workflow
- User asks to **send commands** to a Claude session in tmux
- User wants to **monitor progress** or **read output** from sessions
- User needs to **list/attach/kill/clean tmux sessions**
- User wants **Claude Code running in separate tmux session**
- User mentions **plan execution**, **exploration phase**, **spec writing**, **task implementation**
- User asks to **clean up finished sessions** or **remove completed sessions**
- User wants to **unlock blocked sessions**, **unblock stuck sessions**, or **unfreeze frozen sessions**
- User mentions **sessions waiting for input**, **sessions not responding**, or **stuck processes**
- User requests **session cleanup**, **session management**, or **session maintenance**

## Core Concepts

### Session Types
- **Plan sessions**: `openrag-plan-<name>` - For execution plans in `.agents/plans/` (plan execution, sequential tasks)
- **Exploration sessions**: `openrag-exploration-<name>` - For R&D explorations in `.agents/explorations/` (POCs, comparisons)
- **Spec sessions**: `openrag-spec-<name>` - For specifications in `.agents/specs/` (documentation, requirements)
- **Task sessions**: `openrag-task-<name>` - For tasks in `.agents/tasks/` (implementation, bug fixes)
- **General session**: `openrag` - General purpose development

### Auto-start Claude Mode
When using direct commands (`tl plan/exploration/task/specs <name>`), the system automatically sends the command "c" to activate Claude Code in bypass mode. No need to launch `claude-dev` first - the "c" command alone is sufficient and will activate Claude in bypass mode.

### Intelligent State Detection

The session manager includes detailed Claude state detection capabilities that identify precise work states by analyzing pane content. This system uses pattern matching from `smart_monitor.sh` integrated into `tmux-work-manager.sh`.

**Detected States (Priority Order):**

1. **✅ Completed** - Task finished and pushed
   - Pattern: `Push: ✅`
   - Action: Ready to clean up session

2. **📤 Pushing** - Git push in progress
   - Pattern: `git push`
   - Status: Active work

3. **💾 Committing** - Git commit in progress
   - Pattern: `git commit`
   - Status: Active work

4. **🧪 Tests Passed** - All tests passing with coverage
   - Patterns: `passed`, `coverage`, `100%`
   - Status: Active work

5. **🧪 Testing** - Running pytest
   - Pattern: `pytest`, `running tests`
   - Status: Active work

6. **💻 Coding** - Writing or editing files
   - Patterns: `Edit:`, `Write:`, `editing`, `writing`
   - Status: Active work

7. **📖 Reading** - Reading files or documentation
   - Patterns: `Read:`, `reading`, `analyzing`
   - Status: Active work

8. **🔍 Searching** - Searching codebase
   - Patterns: `Grep:`, `Glob:`, `searching`, `finding`
   - Status: Active work

9. **🤔 Thinking** - Claude processing
   - Pattern: `<thinking>`
   - Status: Active work

10. **⏸️ Idle** - Waiting for input
    - Patterns: `^>`, `|>`, `⏵⏵`, `bypass permissions`
    - Status: Waiting

**Detection System:**

The intelligent state detection system (from `.claude/agents/monitoring-agent.md`) analyzes the last 40 lines of pane content using grep patterns:

```bash
# Example detection logic (from tmux-work-manager.sh)
pane_content=$(tmux capture-pane -t "$pane" -p | tail -40)

# Priority-based detection:
if echo "$pane_content" | grep -q "Push: ✅"; then
    status="✅ completed"
elif echo "$pane_content" | grep -q "git push"; then
    status="📤 pushing"
elif echo "$pane_content" | grep -q "git commit"; then
    status="💾 committing"
# ... and so on
fi
```

**Related Agents:**

This detection system powers 5 specialized agents (see `.claude/agents/`):
- **🟦 Monitoring Agent** (`monitoring-agent.md`) - Real-time state tracking
- **🟠 Notification Agent** (`notification-agent.md`) - State-based notifications
- **🟢 Cleanup Agent** (`cleanup-agent.md`) - Auto-cleanup when completed
- **🟣 Validation Agent** (`validation-agent.md`) - Health checks
- **🟡 Session Tree Agent** (`session-tree-agent.md`) - Hierarchical display

**Slash Commands Using Detection:**
- `/monitor` - Launch intelligent monitoring (uses monitoring-agent)
- `/tree` - Display session tree with states (uses session-tree-agent)
- `/clean-session` - Clean finished sessions (uses cleanup-agent + detection)
- `/session-unlock` - Unlock blocked sessions (uses validation-agent + detection)
- `/self-kill` - Allow current session to terminate itself after moving files to done/

### 1. Create a New Session (Direct Mode with Auto-start Claude)

**For a plan (execution plan):**
```bash
cd /home/devuser/workdir/openrag && ./start-tmux-work.sh plan <partial-name>
# Example: ./start-tmux-work.sh plan wiki_markdown_export
# Use when: "execute the wiki plan", "run the implementation plan"
```

**For an exploration (R&D, POC):**

**CRITICAL**: Before executing an exploration, it MUST be moved from `to_do/` to `in_process/`:
```bash
# First, move exploration to in_process
mv .agents/explorations/to_do/<name>.md .agents/explorations/in_process/<name>.md

# Then, launch the session
```bash
cd /home/devuser/workdir/openrag && ./start-tmux-work.sh exploration <partial-name>
# Example: ./start-tmux-work.sh exploration milvus_filtering
# Use when: "run the Milvus exploration", "conduct the filtering POC"
```

**For a spec (specification, documentation):**
```bash
cd /home/devuser/workdir/openrag && ./start-tmux-work.sh specs <partial-name>
# Example: ./start-tmux-work.sh specs api_documentation
# Use when: "write the API spec", "update the documentation spec"
```

**For a task (implementation, bug fix):**
```bash
cd /home/devuser/workdir/openrag && ./start-tmux-work.sh task <partial-name>
# Example: ./start-tmux-work.sh task export_validation
# Use when: "implement the export task", "fix the validation bug"
```

**What happens:**
- Searches for matching files (case-insensitive, partial match)
- Creates session with name pattern `openrag-{type}-<name>`
- Creates 3 windows: main (Claude), tests, logs
- Automatically starts `claude-dev` and enters bypass mode (`c` command)
- Stores metadata in `/tmp/tmux-claude-sessions/<session>.info`

### 2. Interactive Mode (Manual Selection)

```bash
cd /home/devuser/workdir/openrag && ./start-tmux-work.sh
# Then follow the interactive menu
```

This shows all available plans/tasks/specs organized by status (TODO/IN PROGRESS/DONE).

### 3. Send Commands to a Claude Session

**Using helper script:**
```bash
./tmux-claude-helper.sh send <session-name> "<message>"
# Example: ./tmux-claude-helper.sh send openrag-plan-wiki "Implement the export function"
```

**Using tmux directly:**
```bash
tmux send-keys -t <session-name>:0 "<message>" C-m
# Example: tmux send-keys -t openrag-plan-wiki:0 "Read the plan file" C-m
```

### 4. Read Output from a Session

**Read last N lines (default 50):**
```bash
./tmux-claude-helper.sh read <session-name> [lines]
# Example: ./tmux-claude-helper.sh read openrag-plan-wiki 100
```

**Read entire buffer:**
```bash
./tmux-claude-helper.sh read-all <session-name>
```

**Using tmux directly:**
```bash
tmux capture-pane -t <session-name>:0 -p -S -50  # Last 50 lines
tmux capture-pane -t <session-name>:0 -p -S -    # All lines
```

### 5. Monitor Session Continuously

```bash
./tmux-claude-helper.sh watch <session-name> [interval-seconds]
# Example: ./tmux-claude-helper.sh watch openrag-task-export 2
# Press Ctrl+C to stop
```

### 5b. Schedule Delayed Notifications

**Purpose**: Send messages to a session after a delay, useful for deployment monitoring, health checks, and periodic status updates.

**Script**: `tmux-delayed-notify.sh`

**Single Notification (one-time):**
```bash
./tmux-delayed-notify.sh <session-name> <delay-minutes> <message>
# Example: ./tmux-delayed-notify.sh openrag-deployment 5 "check if SSH is ready at 163.172.145.70"
```

**Recurrent Notification (continuous monitoring):**
```bash
./tmux-delayed-notify.sh <session-name> <delay-minutes> <message> --recurrent
# Or using short flag:
./tmux-delayed-notify.sh <session-name> <delay-minutes> <message> -r

# Examples:
# Check API health every 3 minutes
./tmux-delayed-notify.sh openrag-deployment 3 'curl http://localhost:8080/health' --recurrent

# Monitor deployment status every 5 minutes
./tmux-delayed-notify.sh monitor-session 5 'ssh user@host "systemctl status openrag"' -r

# Check logs every 2 minutes
./tmux-delayed-notify.sh openrag-logs 2 'tail -20 /var/log/openrag.log' --recurrent
```

**What the --recurrent flag does:**
- Automatically re-schedules the notification after each execution
- Creates a continuous monitoring loop
- Each notification displays: "Prochaine notification dans X min"
- Runs indefinitely until session is closed or process is killed

**Use Cases for Recurrent Notifications:**

1. **Deployment Monitoring**: Check if services are ready every few minutes
2. **Health Checks**: Periodically verify API endpoints are responding
3. **Log Monitoring**: Regularly tail logs to catch errors
4. **Status Updates**: Monitor long-running processes or migrations
5. **Availability Checks**: Continuously verify SSH access or server availability

**Stopping Recurrent Notifications:**
- Close the tmux session: `tw clean <session-name>`
- Kill the background process: Check `/tmp/tmux-delayed-notifications/*.info` for PID
- Or simply attach to the session and Ctrl+C if it's actively running a command

**Notification Info Location**: `/tmp/tmux-delayed-notifications/<id>.info`

### 5c. Async Notification Queue System (For Swarm Coordination)

**🎯 NEW: Non-blocking notification system for swarm agents**

When working with swarms (multiple parallel Claude sessions), use the **async notification queue** instead of direct `tmux send-keys` to avoid blocking and conflicts.

**Key Benefits:**
- ✅ Non-blocking: Push notifications without waiting
- ✅ No conflicts: Multiple agents can notify in parallel
- ✅ Batch processing: Consume all notifications at once
- ✅ Audit trail: Complete history with timestamps
- ✅ Auto-reminders: Only when notifications pending

**🔧 Usage:**

**Push a Notification (Non-blocking):**
```bash
source .agents/scripts/utils/async-notification-queue.sh

# Push notification to a session
push_notification "target-session-name" "request" "Need help with authentication" \
  --priority HIGH --from "$TMUX_SESSION"

# Notification goes to queue, returns immediately
# Target session will be reminded to check with /check-notif
```

**Consume Notifications (In Target Session):**
```bash
# Manual consumption (use in Claude sessions)
/check-notif

# Or via bash:
source .agents/scripts/utils/async-notification-queue.sh
consume_notifications "$TMUX_SESSION"
```

**Broadcast to Multiple Sessions:**
```bash
# Broadcast to all sessions matching pattern
broadcast_notification "plan-*" "info" "Deployment complete" \
  --priority NORMAL --from "coordinator"
```

**Check Queue Status:**
```bash
# View pending notifications
view_queue_status "session-name"
```

**🎨 Swarm Notification Mode (Auto-check every 3 minutes):**

For swarm agents that need to monitor notifications automatically:

```bash
source .agents/scripts/utils/swarm-notification-mode.sh

# Enable auto-check (every 3 minutes)
enable_swarm_notification_mode

# Claude session will auto-check for notifications
# Reminder appears only when notifications pending

# Disable when done
disable_swarm_notification_mode

# List all sessions in notification mode
list_notification_mode_sessions
```

**📋 Notification Types:**
- `request` - Help request from another agent
- `offer` - Assistance offer to another agent
- `info` - Informational update
- `status` - Status update
- `task` - Task assignment
- `completion` - Work completion notice

**📊 Priority Levels:**
- `URGENT` - Requires immediate attention
- `HIGH` - Important, check soon
- `NORMAL` - Standard notification
- `LOW` - Informational only

**🔗 Integration with Swarm Orchestrator:**

The swarm orchestrator automatically uses the notification queue:

```bash
source .agents/scripts/utils/swarm-orchestrator.sh

# Start swarm with auto-notification mode
start_swarm_orchestrator "my-swarm" \
  "session1" "session2" "session3" \
  --enable-notifications

# All swarm agents will:
# 1. Auto-enable swarm notification mode
# 2. Use notification queue for communication
# 3. Auto-consume notifications every 3 minutes
```

**📚 See Also:**
- **Complete Guide:** `.agents/docs/async-notification-queue.md`
- **Swarm Collaboration:** `.agents/docs/swarm-collaborative-system.md`
- **Quick Reference:** `.agents/docs/swarm-quick-reference.md`

### 6. Get Session Information

```bash
./tmux-claude-helper.sh info <session-name>
# Shows: session name, file path, work type, windows, attached clients
```

### 7. List All Active Sessions

```bash
./tmux-claude-helper.sh list
# Or simply:
tmux ls
```

### 8. Control Signals

**Send Ctrl+C (interrupt):**
```bash
./tmux-claude-helper.sh ctrl-c <session-name>
# Or: tmux send-keys -t <session-name>:0 C-c
```

**Send Ctrl+D (EOF):**
```bash
./tmux-claude-helper.sh ctrl-d <session-name>
# Or: tmux send-keys -t <session-name>:0 C-d
```

**Clear screen:**
```bash
./tmux-claude-helper.sh clear <session-name>
# Or: tmux send-keys -t <session-name>:0 C-l
```

### 9. Attach to Existing Session

```bash
tmux attach -t <session-name>
# Example: tmux attach -t openrag-plan-wiki
# Detach with: Ctrl+B then D
```

### 10. Close a Session Properly

**Using `tw clean` (Recommended):**
```bash
# Interactive mode - prompts for session name
./start-tmux-work.sh clean

# Direct mode - close specific session
./start-tmux-work.sh clean <session-name>
# Example: ./start-tmux-work.sh clean openrag-plan-wiki
```

**What `tw clean` does:**
- Verifies session exists
- Kills the tmux session
- Removes session metadata from `/tmp/tmux-claude-sessions/<session>.info`
- Provides confirmation message

**Alternative - Kill without cleanup:**
```bash
tmux kill-session -t <session-name>
# Example: tmux kill-session -t openrag-plan-wiki
# Note: This doesn't remove metadata files
```

### 11. Clean Up Finished Sessions Automatically

**Using the `/clean-session` slash command:**

This command systematically checks all active sessions and closes those that are completed:

```bash
# In Claude Code, run:
/clean-session
```

**What it does:**
1. Lists all active tmux sessions
2. For each session, reads the last 100 lines of output
3. Analyzes output for completion indicators:
   - "Task completed"
   - "Done"
   - "Finished"
   - Claude prompt showing idle state
   - Error messages indicating session should be closed
4. **CRITICAL**: Moves task/plan/exploration files to `done/` folder
5. Closes finished sessions using `tw clean`
6. Provides summary report

**Manual cleanup process:**
```bash
# 1. List all sessions
tmux ls

# 2. For each session, check if finished
./tmux-claude-helper.sh read <session> 100

# 3. Analyze output for completion
# Look for: "Task completed", "Done", idle prompts, etc.

# 4. CRITICAL: Move file to done folder BEFORE closing session
./tmux-claude-helper.sh info <session>  # Get file location

# For tasks:
mv .agents/tasks/in_process/<name>.md .agents/tasks/done/<name>.md

# For plans:
mv .agents/plans/in_process/<name>.md .agents/plans/done/<name>.md

# For explorations:
mv .agents/explorations/in_process/<name>.md .agents/explorations/done/<name>.md

# 5. Close finished sessions
./start-tmux-work.sh clean <session-name>
```

**Why move to done/ first?**
- Maintains workflow integrity (to_do → in_process → done)
- Marks work as officially complete
- Prevents losing track of completed work
- Follows .agents/ directory structure conventions

### 12. Unlock Blocked Sessions or Clean Finished Ones

**Using the `/session-unlock` slash command:**

This command checks all sessions and takes appropriate action based on their state:

```bash
# In Claude Code, run:
/session-unlock
```

**What it does:**
1. Lists all active tmux sessions
2. For each session, reads the last 100 lines of output
3. Determines session state:
   - **Finished** → Cleans session (moves to done/ + tw clean)
   - **Blocked/Stuck** → Unlocks with appropriate message
   - **Active** → Leaves alone
4. Verifies unlock actions worked
5. Provides detailed summary report

**Session States:**

#### Finished Session
**Indicators**: "Done", "Completed", all tests passed, explicit completion message

**Action**: Clean the session
```bash
# 1. Move to done/
mv .agents/{type}/in_process/<name>.md .agents/{type}/done/<name>.md

# 2. Clean session
tw clean <session-name>
```

#### Blocked/Stuck Session
**Indicators**:
- Claude waiting for user input or decision
- Error without retry attempt
- Process frozen (no output for extended time)
- "What would you like me to do?" messages
- Test failure with no retry

**Action**: Unlock with appropriate message

**Example unlock strategies:**

```bash
# If waiting for decision:
./tmux-claude-helper.sh send <session> "Use approach 1 and continue autonomously"

# If error occurred:
./tmux-claude-helper.sh send <session> "Analyze the error, fix it, and retry the operation"

# If process frozen:
./tmux-claude-helper.sh ctrl-c <session>
sleep 2
./tmux-claude-helper.sh send <session> "Please continue with the next step"

# If test failed:
./tmux-claude-helper.sh send <session> "Fix the failing test and run the test suite again"

# Generic unblock:
./tmux-claude-helper.sh send <session> "Continue autonomously with the work. Make decisions as needed."
```

#### Active Session
**Indicators**: Recent output, progress messages, tests running, files being edited

**Action**: Leave alone (no intervention needed)

**Difference between `/session-unlock` and `/clean-session`:**
- `/clean-session`: Only cleans **finished** sessions
- `/session-unlock`: **Unlocks blocked** sessions AND cleans **finished** ones

**Use `/session-unlock` when:**
- Sessions appear stuck or frozen
- Claude is waiting for input in multiple sessions
- You want to restart stalled work
- Mixed situation (some finished, some blocked)

**Use `/clean-session` when:**
- You only want to remove finished sessions
- Pure cleanup operation
- No sessions appear blocked

### 13. Automated Session Verification (All Sessions)

**Purpose**: Automatically check ALL sessions and take intelligent actions based on their state - clean finished ones, unblock stuck ones, leave active ones alone.

This is the most comprehensive session management approach, combining cleaning and unlocking in a single automated workflow.

**When to Use**:
- Periodic maintenance of all sessions
- After long periods of parallel work
- When you want to ensure all sessions are progressing
- Automated monitoring workflows
- CI/CD pipelines or automated workflows

**Implementation Pattern**:

```bash
#!/bin/bash
# Automated session verification for all sessions

# 1. Get all active sessions
SESSIONS=$(tmux ls 2>/dev/null | cut -d: -f1)

if [ -z "$SESSIONS" ]; then
    echo "No active sessions found"
    exit 0
fi

echo "Checking all sessions..."

for session in $SESSIONS; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Session: $session"

    # 2. Read last 100 lines
    OUTPUT=$(./tmux-claude-helper.sh read "$session" 100 2>/dev/null)

    # 3. Determine session state
    if echo "$OUTPUT" | grep -qiE "(✅.*completed|✅.*done|All tasks completed|Finished successfully)"; then
        echo "   State: FINISHED"
        echo "   Action: Cleaning session..."

        # Get file location
        INFO=$(./tmux-claude-helper.sh info "$session" 2>/dev/null)
        FILE_PATH=$(echo "$INFO" | grep "Fichier:" | awk '{print $2}')

        if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
            # Move to done/
            DONE_PATH=$(echo "$FILE_PATH" | sed 's/in_process/done/')
            mkdir -p "$(dirname "$DONE_PATH")"
            mv "$FILE_PATH" "$DONE_PATH"
            echo "   ✅ Moved: $FILE_PATH → $DONE_PATH"
        fi

        # Clean session
        ./start-tmux-work.sh clean "$session" 2>/dev/null
        echo "   ✅ Session cleaned"

    elif echo "$OUTPUT" | grep -qiE "(waiting for|what should|which approach|confirm|approve|\\[Y/n\\]|\\[y/N\\]|error:|failed:)" && \
         ! echo "$OUTPUT" | grep -qiE "(creating|generating|writing|reading|processing|analyzing|implementing|running)"; then
        echo "   State: BLOCKED/STUCK"
        echo "   Action: Sending unblock message..."

        # Determine appropriate unblock message based on context
        if echo "$OUTPUT" | grep -qiE "(\\[Y/n\\]|\\[y/N\\]|confirm|approve)"; then
            # Confirmation prompt
            ./tmux-claude-helper.sh send "$session" "yes"
            echo "   ✅ Sent: yes (confirmation)"
        elif echo "$OUTPUT" | grep -qiE "(what should|which approach|how should)"; then
            # Decision needed
            ./tmux-claude-helper.sh send "$session" "Choose the most appropriate approach and continue autonomously"
            echo "   ✅ Sent: decision guidance"
        elif echo "$OUTPUT" | grep -qiE "(error:|failed:)"; then
            # Error occurred
            ./tmux-claude-helper.sh send "$session" "Analyze the error, fix it, and retry the operation"
            echo "   ✅ Sent: error recovery"
        else
            # Generic unblock
            ./tmux-claude-helper.sh send "$session" "Continue with the work autonomously"
            echo "   ✅ Sent: continue command"
        fi

    else
        echo "   State: ACTIVE"
        echo "   Action: Leaving alone (working...)"
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Session verification complete"
```

**Key Features**:

1. **Intelligent State Detection**:
   - **Finished**: Looks for completion markers (✅, "completed", "done", "finished successfully")
   - **Blocked**: Detects confirmation prompts, questions, errors without progress indicators
   - **Active**: Identifies ongoing work (creating, writing, analyzing, implementing, running)

2. **Context-Aware Unlocking**:
   - **Confirmation prompts** (`[Y/n]`, `[y/N]`) → Sends "yes"
   - **Decision questions** ("What should I do?", "Which approach?") → Sends decision guidance
   - **Errors** ("error:", "failed:") → Sends error recovery instructions
   - **Generic stuck** → Sends continue command

3. **Safe File Management**:
   - Automatically detects file location using `info` command
   - Moves files from `in_process/` to `done/` before cleaning
   - Creates target directory if needed
   - Preserves original filename

4. **Comprehensive Reporting**:
   - Shows state for each session
   - Displays action taken
   - Confirms file moves and cleanups
   - Summary at the end

**Usage Examples**:

**Example 1: Manual one-time verification**
```bash
# Save the script above as verify-all-sessions.sh
chmod +x verify-all-sessions.sh
./verify-all-sessions.sh
```

**Example 2: Periodic automated verification (cron)**
```bash
# Run every 10 minutes
*/10 * * * * cd /home/devuser/workdir/openrag && ./verify-all-sessions.sh >> /tmp/session-verification.log 2>&1
```

**Example 3: Continuous monitoring loop**
```bash
# Monitor sessions every 5 minutes continuously
while true; do
    ./verify-all-sessions.sh
    echo "Waiting 5 minutes before next check..."
    sleep 300
done
```

**Example 4: Verification before important operations**
```bash
# Verify all sessions before starting new work
./verify-all-sessions.sh
echo "Sessions verified. Starting new deployment..."
./start-tmux-work.sh plan deployment
```

**Sample Output**:

```
Checking all sessions...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Session: openrag-task-authentication
   State: FINISHED
   Action: Cleaning session...
   ✅ Moved: .agents/tasks/in_process/authentication.md → .agents/tasks/done/authentication.md
   ✅ Session cleaned
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Session: openrag-plan-deployment
   State: BLOCKED/STUCK
   Action: Sending unblock message...
   ✅ Sent: yes (confirmation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Session: openrag-exploration-performance
   State: ACTIVE
   Action: Leaving alone (working...)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session verification complete
```

**Integration with Slash Commands**:

You can create a custom slash command to run this verification:

```bash
# .claude/commands/verify-sessions.md
---
description: Verify all tmux sessions and take appropriate actions
---

Run automated session verification for all active sessions:
- Clean finished sessions (move to done/ + close)
- Unblock stuck sessions with appropriate messages
- Leave active sessions alone

Execute: ./verify-all-sessions.sh
```

**Advanced: Selective Verification**

Verify only specific session patterns:

```bash
# Only verify plan sessions
for session in $(tmux ls 2>/dev/null | grep "openrag-plan-" | cut -d: -f1); do
    # ... verification logic ...
done

# Only verify task sessions
for session in $(tmux ls 2>/dev/null | grep "openrag-task-" | cut -d: -f1); do
    # ... verification logic ...
done

# Only verify sessions matching pattern
PATTERN="openrag-(plan|task)-deployment"
for session in $(tmux ls 2>/dev/null | grep -E "$PATTERN" | cut -d: -f1); do
    # ... verification logic ...
done
```

**Best Practices**:

1. **Run regularly**: Set up periodic verification (every 5-10 minutes) for long-running parallel workflows
2. **Verify before new work**: Clean up finished sessions before starting new ones
3. **Monitor the logs**: Keep verification output in log files for debugging
4. **Customize unblock messages**: Adapt the unblock logic for your specific workflow
5. **Test detection patterns**: Adjust regex patterns based on your Claude output patterns
6. **Combine with notifications**: Use with delayed notifications for comprehensive monitoring

**Comparison with Slash Commands**:

| Feature | `/clean-session` | `/session-unlock` | Automated Verification |
|---------|-----------------|-------------------|----------------------|
| Clean finished | ✅ | ✅ | ✅ |
| Unblock stuck | ❌ | ✅ | ✅ |
| Context-aware unlocking | ❌ | ✅ | ✅ |
| Periodic automation | ❌ | ❌ | ✅ |
| Custom patterns | ❌ | ❌ | ✅ |
| Scriptable | ❌ | ❌ | ✅ |

**When to Use Each**:

- **`/clean-session`**: Quick cleanup of finished sessions (interactive, manual)
- **`/session-unlock`**: Handle mixed situations with blocked and finished sessions (interactive, manual)
- **Automated Verification**: Continuous monitoring, CI/CD, unattended workflows, periodic maintenance

## Workflow Examples

### Example 1: Execute a Plan in Background

**User request**: "Execute the wiki markdown export plan"

```bash
# 1. Create session with auto-start Claude
./start-tmux-work.sh plan wiki_markdown_export

# 2. Claude starts automatically, detach to let it work
# Press Ctrl+B then D (user does this)

# 3. Monitor progress from another terminal
./tmux-claude-helper.sh read openrag-plan-wiki_markdown_export 100

# 4. Send additional instructions if needed
./tmux-claude-helper.sh send openrag-plan-wiki_markdown_export "Run the tests when done"

# 5. Watch continuously
./tmux-claude-helper.sh watch openrag-plan-wiki_markdown_export 3
```

### Example 1b: Run an Exploration

**User request**: "Run the Milvus filtering exploration"

```bash
# 1. Create exploration session
./start-tmux-work.sh exploration milvus_filtering

# 2. Send initial instruction
./tmux-claude-helper.sh send openrag-exploration-milvus_filtering "Read the exploration document and create POCs"

# 3. Monitor progress
./tmux-claude-helper.sh watch openrag-exploration-milvus_filtering 5
```

### Example 2: Parallel Execution (Plans, Explorations, Specs, Tasks)

**User request**: "Work on the export plan, Milvus exploration, and API spec in parallel"

```bash
# Create multiple sessions for parallel work
./start-tmux-work.sh plan export_implementation
# Detach: Ctrl+B D

./start-tmux-work.sh exploration milvus_context_filtering
# Detach: Ctrl+B D

./start-tmux-work.sh specs api_documentation
# Detach: Ctrl+B D

./start-tmux-work.sh task validation_logic
# Detach: Ctrl+B D

# List all sessions
tmux ls

# Monitor each session
./tmux-claude-helper.sh read openrag-plan-export_implementation 50
./tmux-claude-helper.sh read openrag-exploration-milvus_context_filtering 50
./tmux-claude-helper.sh read openrag-spec-api_documentation 50
./tmux-claude-helper.sh read openrag-task-validation_logic 50
```

### Example 3: Interactive Development with Claude

```bash
# 1. Start session
./start-tmux-work.sh plan implementation

# 2. From another terminal, interact with Claude
./tmux-claude-helper.sh send openrag-plan-implementation "Read .agents/plans/in_process/implementation.md and start with first task"

# 3. Wait and read response
sleep 10
./tmux-claude-helper.sh read openrag-plan-implementation 150

# 4. Continue conversation
./tmux-claude-helper.sh send openrag-plan-implementation "Looks good, continue with tests"

# 5. Monitor until completion
./tmux-claude-helper.sh watch openrag-plan-implementation 5

# 6. When completed, clean up
./start-tmux-work.sh clean openrag-plan-implementation
```

### Example 4: Clean Up Multiple Finished Sessions

**User request**: "Clean up all finished sessions"

**Using Claude Code `/clean-session` command:**
```bash
# In Claude Code
/clean-session

# Claude will:
# 1. List all active sessions
# 2. Check each session's output
# 3. Identify finished sessions
# 4. Close them with tw clean
# 5. Provide summary
```

**Manual process:**
```bash
# 1. List all sessions
tmux ls

# Output might show:
# openrag-plan-wiki: 3 windows (created Mon Oct 28 10:00:00 2024)
# openrag-task-auth: 3 windows (created Mon Oct 28 11:00:00 2024)
# openrag-exploration-milvus: 3 windows (created Mon Oct 28 12:00:00 2024)

# 2. Check each session
./tmux-claude-helper.sh read openrag-plan-wiki 100
# Output shows "✅ All tasks completed successfully!"
# Decision: Close this one

./tmux-claude-helper.sh read openrag-task-auth 100
# Output shows "⚙️ Running tests..."
# Decision: Keep this one

./tmux-claude-helper.sh read openrag-exploration-milvus 100
# Output shows "❌ Error: Cannot connect to Milvus"
# Decision: Close this one

# 3. CRITICAL: Move files to done/ before closing
# For plan
./tmux-claude-helper.sh info openrag-plan-wiki
# Shows: Fichier: .agents/plans/in_process/wiki_markdown_export.md
mv .agents/plans/in_process/wiki_markdown_export.md .agents/plans/done/wiki_markdown_export.md

# For exploration
./tmux-claude-helper.sh info openrag-exploration-milvus
# Shows: Fichier: .agents/explorations/in_process/milvus_filtering.md
mv .agents/explorations/in_process/milvus_filtering.md .agents/explorations/done/milvus_filtering.md

# 4. Close finished sessions
./start-tmux-work.sh clean openrag-plan-wiki
./start-tmux-work.sh clean openrag-exploration-milvus

# 5. Verify remaining sessions
tmux ls
# Output: openrag-task-auth: 3 windows (created Mon Oct 28 11:00:00 2024)
```

### Example 5: Unlock Blocked Sessions

**User request**: "Unlock any blocked sessions"

**Using Claude Code `/session-unlock` command:**
```bash
# In Claude Code
/session-unlock

# Claude will:
# 1. Check all sessions
# 2. Identify blocked/stuck and finished sessions
# 3. Unlock blocked ones with appropriate messages
# 4. Clean finished ones
# 5. Provide detailed report
```

**Manual process for mixed scenario:**
```bash
# 1. List all sessions
tmux ls
# Output:
# openrag-task-validation: 3 windows
# openrag-plan-deployment: 3 windows
# openrag-exploration-performance: 3 windows

# 2. Check Session 1
./tmux-claude-helper.sh read openrag-task-validation 100
# Output shows: "❌ Test failed. What should I do? Fix or skip?"
# State: BLOCKED (waiting for decision)

# Unlock strategy: Provide clear guidance
./tmux-claude-helper.sh send openrag-task-validation "Fix the failing test. Analyze the error, implement a fix, and rerun tests until passing."

# 3. Check Session 2
./tmux-claude-helper.sh read openrag-plan-deployment 100
# Output shows: "✅ Deployment complete. All services running."
# State: FINISHED

# Clean strategy: Move to done and close
./tmux-claude-helper.sh info openrag-plan-deployment
mv .agents/plans/in_process/deployment.md .agents/plans/done/deployment.md
tw clean openrag-plan-deployment

# 4. Check Session 3
./tmux-claude-helper.sh read openrag-exploration-performance 100
# Output shows: "[hanging process - no output for 5 minutes]"
# State: BLOCKED (frozen process)

# Unlock strategy: Interrupt and restart
./tmux-claude-helper.sh ctrl-c openrag-exploration-performance
sleep 2
./tmux-claude-helper.sh send openrag-exploration-performance "The previous command was stuck. Skip it and continue with the next step in the exploration."

# 5. Verify unlocks after 10 seconds
sleep 10

./tmux-claude-helper.sh read openrag-task-validation 50
# Should show: "Analyzing test error... Implementing fix..."

./tmux-claude-helper.sh read openrag-exploration-performance 50
# Should show: "Continuing with next step..."

# 6. Final status
tmux ls
# Output:
# openrag-task-validation: 3 windows (now active)
# openrag-exploration-performance: 3 windows (now active)
```

### Example 6: Automated Session Verification

**User request**: "Set up automated monitoring for all my parallel sessions"

**Scenario**: You have 5 sessions running in parallel and want them to be automatically verified and managed without manual intervention.

```bash
# Step 1: Create the verification script
cat > verify-all-sessions.sh <<'SCRIPT'
#!/bin/bash
# Automated session verification for all sessions

SESSIONS=$(tmux ls 2>/dev/null | cut -d: -f1)

if [ -z "$SESSIONS" ]; then
    echo "No active sessions found"
    exit 0
fi

echo "Checking all sessions..."

for session in $SESSIONS; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Session: $session"

    OUTPUT=$(./tmux-claude-helper.sh read "$session" 100 2>/dev/null)

    if echo "$OUTPUT" | grep -qiE "(✅.*completed|✅.*done|All tasks completed|Finished successfully)"; then
        echo "   State: FINISHED"
        echo "   Action: Cleaning session..."

        INFO=$(./tmux-claude-helper.sh info "$session" 2>/dev/null)
        FILE_PATH=$(echo "$INFO" | grep "Fichier:" | awk '{print $2}')

        if [ -n "$FILE_PATH" ] && [ -f "$FILE_PATH" ]; then
            DONE_PATH=$(echo "$FILE_PATH" | sed 's/in_process/done/')
            mkdir -p "$(dirname "$DONE_PATH")"
            mv "$FILE_PATH" "$DONE_PATH"
            echo "   ✅ Moved: $FILE_PATH → $DONE_PATH"
        fi

        ./start-tmux-work.sh clean "$session" 2>/dev/null
        echo "   ✅ Session cleaned"

    elif echo "$OUTPUT" | grep -qiE "(waiting for|what should|which approach|confirm|approve|\\[Y/n\\]|\\[y/N\\]|error:|failed:)" && \
         ! echo "$OUTPUT" | grep -qiE "(creating|generating|writing|reading|processing|analyzing|implementing|running)"; then
        echo "   State: BLOCKED/STUCK"
        echo "   Action: Sending unblock message..."

        if echo "$OUTPUT" | grep -qiE "(\\[Y/n\\]|\\[y/N\\]|confirm|approve)"; then
            ./tmux-claude-helper.sh send "$session" "yes"
            echo "   ✅ Sent: yes (confirmation)"
        elif echo "$OUTPUT" | grep -qiE "(what should|which approach|how should)"; then
            ./tmux-claude-helper.sh send "$session" "Choose the most appropriate approach and continue autonomously"
            echo "   ✅ Sent: decision guidance"
        elif echo "$OUTPUT" | grep -qiE "(error:|failed:)"; then
            ./tmux-claude-helper.sh send "$session" "Analyze the error, fix it, and retry the operation"
            echo "   ✅ Sent: error recovery"
        else
            ./tmux-claude-helper.sh send "$session" "Continue with the work autonomously"
            echo "   ✅ Sent: continue command"
        fi

    else
        echo "   State: ACTIVE"
        echo "   Action: Leaving alone (working...)"
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Session verification complete"
SCRIPT

chmod +x verify-all-sessions.sh

# Step 2: Run initial verification
./verify-all-sessions.sh

# Output example:
# Checking all sessions...
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 Session: openrag-task-api-auth
#    State: FINISHED
#    Action: Cleaning session...
#    ✅ Moved: .agents/tasks/in_process/api_auth.md → .agents/tasks/done/api_auth.md
#    ✅ Session cleaned
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 Session: openrag-plan-deployment
#    State: BLOCKED/STUCK
#    Action: Sending unblock message...
#    ✅ Sent: yes (confirmation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 Session: openrag-task-logging
#    State: ACTIVE
#    Action: Leaving alone (working...)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Session verification complete

# Step 3: Set up continuous monitoring (runs every 5 minutes)
nohup bash -c 'while true; do ./verify-all-sessions.sh; sleep 300; done' > /tmp/session-verification.log 2>&1 &

# Step 4: Monitor the verification log
tail -f /tmp/session-verification.log

# Step 5: Stop continuous monitoring when done
pkill -f "verify-all-sessions.sh"
```

**Alternative: Use with cron for scheduled verification**

```bash
# Add to crontab (runs every 10 minutes during work hours)
# Edit crontab
crontab -e

# Add this line:
*/10 9-18 * * 1-5 cd /home/devuser/workdir/openrag && ./verify-all-sessions.sh >> /tmp/session-verification.log 2>&1

# This runs verification:
# - Every 10 minutes
# - Between 9 AM and 6 PM
# - Monday through Friday
```

**Practical Use Case - Full Deployment Workflow**

```bash
# 1. Start 5 parallel deployment tasks
./start-tmux-work.sh task infrastructure-setup
./start-tmux-work.sh task database-migration
./start-tmux-work.sh task api-deployment
./start-tmux-work.sh task frontend-build
./start-tmux-work.sh task monitoring-setup

# 2. Detach from all sessions (Ctrl+B D after each)

# 3. Start automated verification
nohup bash -c 'while true; do ./verify-all-sessions.sh; sleep 180; done' > deployment-monitor.log 2>&1 &
echo "Automated monitoring started. Check: tail -f deployment-monitor.log"

# 4. Go do other work, the system will:
#    - Clean finished tasks automatically
#    - Unblock stuck tasks
#    - Leave active tasks alone
#    - Move completed files to done/

# 5. Later, check final status
tail -100 deployment-monitor.log
tmux ls  # Should show only active sessions

# 6. Stop monitoring when all done
pkill -f "verify-all-sessions.sh"
```

**Benefits of Automated Verification**:

1. **Hands-free operation**: No need to manually check each session
2. **Continuous progress**: Blocked sessions are unblocked automatically
3. **Clean workspace**: Finished sessions are cleaned immediately
4. **File management**: Files automatically moved to done/ folder
5. **Audit trail**: All actions logged for review

**When to Use Automated Verification**:

- Running 5+ parallel sessions
- Long-running tasks (hours/days)
- CI/CD pipelines
- Overnight or weekend processing
- Want to minimize manual intervention
- Need audit trail of session management

## Error Handling

1. **Session already exists:**
   - Script will prompt to attach to existing session
   - Or use `tmux kill-session -t <name>` first to recreate

2. **No matching file found:**
   - Check file exists in `.agents/plans/`, `.agents/tasks/`, or `.agents/specs/`
   - Use partial name matching (case-insensitive)
   - Try interactive mode: `./start-tmux-work.sh`

3. **Session not found (when reading/sending):**
   - Verify session exists: `tmux ls`
   - Check session name matches pattern: `openrag-{plan|task|spec}-<name>`

4. **Claude not responding:**
   - Check if Claude started correctly: `./tmux-claude-helper.sh read <session> 50`
   - Send Ctrl+C and restart: `./tmux-claude-helper.sh ctrl-c <session>`
   - Attach manually: `tmux attach -t <session>`

## File Locations

### Core Scripts (openrag-agents)

- **Session manager**: `.claude/scripts/tmux-work-manager.sh`
  - Main TUI with intelligent state detection
  - Session tree view with parent-child relationships
  - Session filtering, creation, attachment, cleanup

- **Helper scripts**: `.claude/scripts/`
  - `tmux-claude-helper.sh` - Helper commands (send, read, info, watch)
  - `tmux-aliases.sh` - Shell aliases and functions
  - `create-tmux-work.sh` - Parallel resource creation

**Organized Scripts by Category:**

- **Monitoring** (`.claude/scripts/monitoring/`):
  - `smart_monitor.sh` - Intelligent Claude state detection
  - `active_deploy_monitor.sh` - Deployment monitoring
  - `deployment_monitor.sh` - Deployment progress tracking
  - `continuous_monitor.sh` - Continuous session monitoring
  - `monitor_sessions.sh` - Session status monitoring

- **Notifications** (`.claude/scripts/notifications/`):
  - `notif_deploy.sh` - Deployment notifications
  - `tmux-delayed-notify.sh` - Delayed/recurrent notifications

- **Cleanup** (`.claude/scripts/cleanup/`):
  - `cleanup_agents.sh` - Agent cleanup operations
  - `cleanup_scripts.sh` - Script cleanup operations
  - `organize_md.sh` - Markdown file organization

- **Validation** (`.claude/scripts/validation/`):
  - `check_plan_status.sh` - Plan execution status
  - `check_status_once.sh` - One-time status check
  - `check_all.sh` - Comprehensive health check
  - `validate_sessions.sh` - Session validation
  - `validate_all_pastes.sh` - Paste validation
  - `console_validation.sh` - Console output validation

- **Session Tree** (`.claude/scripts/session-tree/`):
  - `show-sessions-tree.sh` - Display session hierarchy
  - `show-tree.sh` - Tree view display

### Legacy Scripts (openrag)

- **Session scripts**: `/home/devuser/workdir/openrag/`
  - `start-tmux-work.sh` - Legacy session manager (use `tw` instead)
  - Symlinks to openrag-agents scripts for compatibility

### Metadata & State

- **Session metadata**: `/tmp/tmux-sessions-metadata/<session>.info`
  - `session_name` - Session name
  - `session_type` - Type (task/plan/exploration/spec/open)
  - `parent_session` - Parent session name (for tree view)
  - `created_at` - Unix timestamp

- **Task events**: `/tmp/task_events.txt` - Event log
- **Task states**: `/tmp/task_states.txt` - State tracking

### Agent Workflows

- **Plans**: `.agents/plans/{to_do|in_process|done}/*.md` - Execution plans
- **Explorations**: `.agents/explorations/{to_do|in_process|done}/*.md` - R&D and POCs
- **Specs**: `.agents/specs/{to_do|in_process|done}/*.md` - Specifications
- **Tasks**: `.agents/tasks/{to_do|in_process|done}/*.md` - Implementation tasks

### Agent Documentation

- **Agents**: `.claude/agents/`
  - `monitoring-agent.md` - 🟦 Blue - State tracking
  - `notification-agent.md` - 🟠 Orange - Notifications
  - `cleanup-agent.md` - 🟢 Green - Cleanup operations
  - `validation-agent.md` - 🟣 Purple - Health checks
  - `session-tree-agent.md` - 🟡 Yellow - Tree views

- **Commands**: `.claude/commands/`
  - `monitor.md` - `/monitor` command
  - `notify.md` - `/notify` command
  - `cleanup.md` - `/cleanup` command
  - `validate.md` - `/validate` command
  - `tree.md` - `/tree` command

## Shell Aliases (after `source tmux-aliases.sh`)

```bash
tw                          # Launch interactive session manager
tw clean [session]          # Close session properly (with metadata cleanup)
tl                          # List sessions
tl plan <name>              # Execute plan directly with auto-start Claude
tl exploration <name>       # Run exploration directly with auto-start Claude
tl specs <name>             # Open spec directly with auto-start Claude
tl task <name>              # Implement task directly with auto-start Claude
ta <session>                # Attach to session
tk <session>                # Kill session (without metadata cleanup)

# Helper functions
tmux-claude-send <session> <message>
tmux-claude-read <session> [lines]
tmux-claude-clear <session>
tmux-claude-ctrl-c <session>
tmux-claude-info <session>
```

## Best Practices & Critical Rules

### CRITICAL: File Movement Before Session Closure

**ALWAYS move files to `done/` folder BEFORE closing any session:**

1. **For completed tasks:**
   ```bash
   mv .agents/tasks/in_process/<name>.md .agents/tasks/done/<name>.md
   ```

2. **For completed plans:**
   ```bash
   mv .agents/plans/in_process/<name>.md .agents/plans/done/<name>.md
   ```

3. **For completed explorations:**
   ```bash
   mv .agents/explorations/in_process/<name>.md .agents/explorations/done/<name>.md
   ```

4. **For specs:**
   - Specs usually stay in their location
   - Update the workflow/progress section in the spec instead

**Why this is critical:**
- Maintains the .agents/ workflow integrity (to_do → in_process → done)
- Prevents losing track of completed work
- Marks work as officially complete in the project structure
- Allows other team members/Claude instances to see what's finished

**Workflow when closing sessions:**
1. Check session is finished: `./tmux-claude-helper.sh read <session> 100`
2. Get file location: `./tmux-claude-helper.sh info <session>`
3. **Move file to done/**: `mv .agents/{type}/in_process/<name>.md .agents/{type}/done/<name>.md`
4. Close session: `tw clean <session>`

### Other Best Practices

**Session Creation:**
- **Use descriptive names**: When creating resources, use clear prompts
- **Auto-start leveraged**: Direct commands (`tl`) auto-start Claude in bypass mode
- **Detach for background**: Use `Ctrl+B, D` to keep work running in background

**Session Monitoring:**
- **Monitor parallel sessions**: Check progress regularly with helper scripts
- **Read sufficient context**: Use 50-150 lines for proper analysis
- **Watch for completion**: Look for "Done", "Completed", test results

**Session Maintenance:**
- **Clean up regularly**: Use `/clean-session` for routine cleanup
- **Unlock when stuck**: Use `/session-unlock` when sessions appear blocked
- **Move before close**: ALWAYS move files to done/ before closing
- **Verify before action**: Check session state thoroughly before acting

**Session Control:**
- **Be conservative**: When in doubt, keep session open
- **Don't interrupt active work**: Only unlock truly blocked sessions
- **Provide clear guidance**: When unlocking, give specific directions
- **Verify unlock success**: Check that unlock message worked

## Intelligent Automated Monitoring

### Advanced Session Manager: `intelligent-session-manager.sh`

**Purpose**: Fully autonomous monitoring system that handles workflows from spec creation through task execution and git commits.

**Features**:

#### 1. **Auto-Detection** (every 30 seconds)
- ✅ **Confirmation Prompts**: `[Y/n]`, `[y/N]`, `Continue?`, `Do you want to proceed?`, `Would you like`, `Should I`, `confirm`, `approve`
- ✅ **Stagnation Detection**: 3 identical cycles (90 seconds) = stuck/frozen
- ✅ **Active Work Detection**: `Creating`, `Generating`, `Writing`, `Reading`, `Processing`, `in_progress`, `working on`, `analyzing`, `implementing`

#### 2. **Autonomous Actions**
- ✅ **Auto-respond to confirmations**: Automatically responds `yes` to confirmation prompts
- ✅ **Auto-continue when stagnant**: Sends contextual "Continue" messages based on work type:
  - For specs: "Continue with the specification and move it to done/ when complete"
  - For plans: "Continue with the plan creation and list all tasks in order"
  - For tasks: "Continue with task implementation and run tests"
- ✅ **Hands-off when active**: Leaves actively working sessions completely alone
- ✅ **Auto-progress workflows**: Automatically creates next phase when current completes:
  - Specs done → Creates execution plans
  - Plans done → Starts executing first task
  - Task done → Starts next task in sequence

#### 3. **File Management**
- ✅ **Auto-move to done/**: Moves completed work from `in_process/` to `done/` automatically
- ✅ **Git integration**: Triggers commit requests when work completes
- ✅ **Phase transitions**: Seamlessly progresses through workflow phases

#### 4. **Real-time Monitoring**
- Check interval: 30 seconds (configurable)
- Stagnation threshold: 3 cycles = 90 seconds (configurable)
- Display: Last 10 lines of output per session
- Metrics tracked:
  - Cycle count per session
  - Stagnant count (resets when progress detected)
  - Session state (active/blocked/finished)
  - Work phase (spec/plan/task)

#### 5. **State Management**

**Session States**:
- **Active**: Recent output, progress indicators → Leave alone
- **Blocked/Stagnant**: No change for 90s → Auto-continue with context
- **Waiting**: Confirmation prompt → Auto-respond "yes"
- **Completed**: Done indicators → Move to done/ + git commit trigger

**Stagnation Tracking**:
```bash
# Each session maintains:
LAST_OUTPUT[$session]      # Last captured output
STAGNANT_COUNT[$session]   # Number of identical cycles
CYCLE_COUNT[$session]      # Total monitoring cycles

# Reset when:
- New output detected (different from LAST_OUTPUT)
- Active work indicators found
- Auto-continue message sent
```

### Usage of Intelligent Monitor

**Starting the monitor:**
```bash
# Start in background
nohup ./intelligent-session-manager.sh > intelligent-monitor.log 2>&1 &

# Or with custom pattern
nohup ./intelligent-session-manager.sh "openrag-(plan|task).*deployment" > monitor.log 2>&1 &
```

**Default monitoring pattern**:
```bash
# Monitors sessions matching:
openrag-(create-spec|create-plan|task).*(multi|scaling)

# Catches:
- openrag-create-spec-create_specification_for_multi_method_deployment_s
- openrag-create-spec-create_specification_for_dynamic_auto_scaling_syst
- openrag-create-plan-multi-method-deployment
- openrag-task-deploy-multi-method-system
- etc.
```

**Monitoring what it does**:
```bash
# Watch live log
tail -f intelligent-monitor.log

# Or with watch command
watch -n 10 'tail -20 intelligent-monitor.log'
```

**Stopping the monitor**:
```bash
# Find process
ps aux | grep intelligent-session-manager

# Kill it
pkill -f intelligent-session-manager.sh
```

### Parallel Workflow Creation

**Creating multiple resources in parallel:**

When user requests creation of multiple specs/plans/tasks/explorations, use:

```bash
# Create specs in parallel
./create-tmux-work.sh spec "Multi-method deployment specification" &
./create-tmux-work.sh spec "Auto-scaling system specification" &

# Create plans in parallel
./create-tmux-work.sh plan "Deployment implementation plan" &
./create-tmux-work.sh plan "Scaling implementation plan" &

# Create tasks in parallel
./create-tmux-work.sh task "Implement deployment scripts" &
./create-tmux-work.sh task "Implement scaling scripts" &
./create-tmux-work.sh task "Add load balancer integration" &
```

**Example workflow orchestration:**

```bash
# 1. Create two specs in parallel
./create-tmux-work.sh spec "Create specification for multi-method deployment" &
./create-tmux-work.sh spec "Create specification for auto-scaling system" &

# 2. Start intelligent monitor
nohup ./intelligent-session-manager.sh > workflow-monitor.log 2>&1 &

# 3. Monitor will automatically:
#    - Wait for specs to complete
#    - Move specs to done/
#    - Create execution plans
#    - Wait for plans to complete
#    - Move plans to done/
#    - Execute tasks sequentially
#    - Commit changes
#    - Mark workflows complete
```

### Auto-Detection Examples

**Confirmation Prompt Detection:**
```bash
# Session output contains:
"Would you like to proceed with this approach? [Y/n]"

# Monitor detects → Auto-responds:
./tmux-claude-helper.sh send <session> "yes"
```

**Stagnation Detection:**
```bash
# Cycle 1: "Reading file..."
# Cycle 2: "Reading file..."  (STAGNANT_COUNT = 1)
# Cycle 3: "Reading file..."  (STAGNANT_COUNT = 2)
# Cycle 4: "Reading file..."  (STAGNANT_COUNT = 3 → THRESHOLD!)

# Monitor sends contextual continue:
./tmux-claude-helper.sh send <session> "Continue with the specification..."
```

**Active Work Detection:**
```bash
# Session output contains:
"Creating specification document..."
"Writing section 3: Technical Requirements"

# Monitor detects active work → Leaves alone
# Resets STAGNANT_COUNT to 0
```

**Completion Detection:**
```bash
# Session output contains:
"✅ Specification completed successfully"
"All sections written and reviewed"

# Monitor detects completion → Actions:
1. Move file: mv .agents/specs/in_process/*.md .agents/specs/done/
2. Create next phase: ./create-tmux-work.sh plan "..."
3. Log: "📁 Spec completed and moved to done/"
```

## Expected Output

### When Creating a Session
Provide:
- **Session type**: Plan execution / Exploration run / Spec writing / Task implementation
- Session name created (e.g., `openrag-plan-wiki_export`)
- Associated file path (e.g., `.agents/plans/in_process/wiki_export.md`)
- Window layout (main, tests, logs)
- Auto-start Claude confirmation (if applicable)
- Commands to interact with the session
- Context about what the plan/exploration/spec/task is about

### When Reading Session Output
Provide:
- Clear separation with visual markers
- Sufficient context (last 50-150 lines typically)
- Analysis of Claude's response if relevant
- Progress indicators (e.g., "Step 2 of 5 completed")

### When Monitoring Sessions
Provide:
- Periodic updates on progress
- Alerts for errors or completion
- Summary of actions taken
- For plans: Which task in the plan is being executed
- For explorations: Which POC or comparison is running
- For specs: Which section is being written
- For tasks: Implementation status

### When Cleaning Up Sessions (`/clean-session`)
Provide:
- Total sessions checked
- List of finished sessions identified
- For each finished session:
  - Session name
  - File location (from info)
  - Move command executed
  - Cleanup result
- Sessions kept active (with reasons)
- Final count: X cleaned, Y active

### When Unlocking Sessions (`/session-unlock`)
Provide:
- Total sessions checked
- For each session:
  - Session name
  - State identified (Finished/Blocked/Active)
  - Action taken:
    - **If Finished**: Move command + cleanup result
    - **If Blocked**: Unlock strategy used + message sent
    - **If Active**: "Left alone - actively working"
- Verification results for unlocked sessions
- Summary report:
  - X sessions cleaned
  - Y sessions unlocked (with unlock methods)
  - Z sessions active (left alone)
  - Any failed actions

## Quick Reference Summary

### Session Lifecycle Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `tw` | Launch interactive menu | Manual session selection |
| `tl plan <name>` | Execute plan | Auto-start Claude for plan |
| `tl exploration <name>` | Run exploration | Auto-start Claude for R&D |
| `tl task <name>` | Implement task | Auto-start Claude for task |
| `tl specs <name>` | Open spec | Auto-start Claude for spec |
| `tw clean <session>` | Close session properly | Single session cleanup |
| `/clean-session` | Clean all finished | Batch cleanup operation |
| `/session-unlock` | Unlock blocked + clean finished | Mixed scenario (blocked + done) |

### Session State Management

| State | Indicators | Action | Command |
|-------|-----------|--------|---------|
| **Finished** | "Done", "Completed", tests passed | Clean (move to done/ + close) | `tw clean` or `/clean-session` |
| **Blocked** | Waiting for input, error, frozen | Unlock with message | `/session-unlock` |
| **Active** | Recent output, progress messages | Leave alone | None |

### Session Monitoring

| Command | Purpose |
|---------|---------|
| `tmux ls` or `tl` | List all sessions |
| `./tmux-claude-helper.sh read <session> [lines]` | Read session output |
| `./tmux-claude-helper.sh info <session>` | Get session metadata |
| `./tmux-claude-helper.sh watch <session>` | Monitor continuously |
| `ta <session>` | Attach to session |

### Session Control

| Command | Purpose |
|---------|---------|
| `./tmux-claude-helper.sh send <session> <msg>` | Send message to Claude |
| `./tmux-claude-helper.sh ctrl-c <session>` | Interrupt process |
| `./tmux-claude-helper.sh clear <session>` | Clear screen |

### Critical Workflow for Closing Sessions

```bash
# 1. Verify finished
./tmux-claude-helper.sh read <session> 100

# 2. Get file location
./tmux-claude-helper.sh info <session>

# 3. CRITICAL: Move to done/ first
mv .agents/{type}/in_process/<name>.md .agents/{type}/done/<name>.md

# 4. Close session
tw clean <session>
```

### Slash Commands

| Command | Use Case |
|---------|----------|
| `/clean-session` | Clean up all finished sessions (pure cleanup) |
| `/session-unlock` | Unlock blocked sessions + clean finished ones (mixed scenario) |

**Rule of thumb:**
- All sessions done? → `/clean-session`
- Some sessions stuck? → `/session-unlock`
- One specific session? → `tw clean <session>`

## Additional Resources

- Full documentation: `README-TMUX.md`
- Quick reference: `TMUX-CHEATSHEET.md`
- Workflow guide: `TMUX-WORK-GUIDE.md`
- Session cleanup guide: `SESSION-CLEANUP-GUIDE.md`
- Helper script: `./tmux-claude-helper.sh --help`
- Slash commands: `.claude/commands/clean-session.md`, `.claude/commands/session-unlock.md`

For detailed reference commands and advanced usage, see [reference.md](reference.md).

### 9. Create New Resources (Parallel Creation with Claude)

**Script**: `create-tmux-work.sh`

This creates new resources (tasks, explorations, specs, plans) in parallel tmux sessions with Claude assistance.

**Syntax:**
```bash
# Without custom name (auto-generated from description):
./create-tmux-work.sh <type> "<description>"

# With custom name:
./create-tmux-work.sh <type> <name> "<description>"

# With custom working directory (path):
./create-tmux-work.sh <type> "<description>" --path /path/to/directory

# With git worktree (auto-resolves path):
./create-tmux-work.sh <type> "<description>" --worktree branch-name

# Combined (name + path or worktree):
./create-tmux-work.sh <type> <name> "<description>" --path /path/to/directory
./create-tmux-work.sh <type> <name> "<description>" --worktree branch-name
```

**Resource Types:**
- `task` → `.agents/tasks/to_do/`
- `exploration` → `.agents/explorations/to_do/`
- `spec` → `.agents/specs/to_do/`
- `plan` → `.agents/plans/to_do/`
- `refacto` → `.agents/refacto/to_do/`

**Examples:**

```bash
# Task with auto-generated name
./create-tmux-work.sh task "Fix authentication bug in login endpoint"
# Creates: fix_authentication_bug_in_login_endpoint.md

# Task with custom name
./create-tmux-work.sh task auth-fix "Fix authentication bug in login endpoint"
# Creates: auth-fix.md

# Exploration
./create-tmux-work.sh exploration api-security "Compare API key protection strategies"
# Creates: api-security.md

# Spec
./create-tmux-work.sh spec indexer-ui "Indexer UI with drag-drop upload"
# Creates: indexer-ui.md

# Plan
./create-tmux-work.sh plan deployment-prod "Production deployment with Terraform"
# Creates: deployment-prod.md

# Task with custom path
./create-tmux-work.sh task "Deploy terraform modules" --path /home/devuser/workdir/openrag/terraform
# Session works in terraform/ directory

# Task with worktree
./create-tmux-work.sh task "Fix scoped chat" --worktree integration
# Auto-resolves to /home/devuser/workdir/worktree/integration

# Exploration in specific worktree
./create-tmux-work.sh exploration load-test "Test deployment performance" --worktree test-deployment
# Session in test-deployment worktree
```

**What Happens:**
1. Creates `.md` file in appropriate `to_do/` directory
2. Launches tmux session named `openrag-create-{type}-{name}`
3. Starts Claude automatically in bypass mode
4. Loads `.agents/{type}/rules.md` for guidance
5. All tmux windows (main, tests, logs) start in specified directory
6. Attaches to session for monitoring

**Working Directory:**
- Default: PROJECT_ROOT (current repository)
- `--path <dir>`: Custom directory path
- `--worktree <branch>`: Auto-resolves git worktree path
- Validation: Directory must exist before session creation

**Session Naming:**
- Without name: `openrag-create-task-fix_authentication_bug`
- With name: `openrag-create-task-auth-fix`

**Slug Generation (Auto-Name):**
- Converts to lowercase
- Replaces special chars with underscores
- Truncates to 50 characters max

**Parallel Creation:**
Multiple resources can be created simultaneously:

```bash
# Launch in background with &
./create-tmux-work.sh task "Fix auth" &
./create-tmux-work.sh exploration "Compare DBs" &
./create-tmux-work.sh spec "API docs" &

# Monitor all
tmux ls
```

**Integration with Helpers:**

```bash
SESSION="openrag-create-task-auth-fix"

# Send additional context
./tmux-claude-helper.sh send "$SESSION" "Include security considerations"

# Read progress
./tmux-claude-helper.sh read "$SESSION"

# Watch continuously
./tmux-claude-helper.sh watch "$SESSION"
```

**Slash Commands:**
- `/create-task [name] "description"` - Create task
- `/create-exploration [name] "description"` - Create exploration
- `/create-spec [name] "description"` - Create spec
- `/create-plan [name] "description"` - Create plan
- `/create-session` - General command with full documentation

**Example Flow:**

User: "Create a task named auth-fix to implement JWT authentication"

Claude runs:
```bash
./create-tmux-work.sh task auth-fix "Implement JWT authentication with refresh tokens"
```

Result:
- File: `.agents/tasks/to_do/auth-fix.md`
- Session: `openrag-create-task-auth-fix`
- Claude: Active and waiting for your input

