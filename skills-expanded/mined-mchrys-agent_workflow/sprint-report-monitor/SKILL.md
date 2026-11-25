---
name: sprint-report-monitor
description: Monitor and generate Sprint Execution Reports for swarm sessions with formatted progress bars, task status, metrics, and automatic daemon control. Trigger on "sprint report", "swarm progress", "task monitoring", "execution status", or "progress tracking" keywords. Provides continuous monitoring every 5 minutes with visual ASCII reports.
allowed-tools: Bash, Read, Grep, Glob
---

# Sprint Report Monitor Skill

## Objective

Generate and monitor formatted Sprint Execution Reports for swarm sessions, providing real-time visibility into task progress, agent status, deliverables, and blockers with beautiful ASCII-formatted reports.

## When to Use

Activate this skill when the user:
- Asks for "sprint report", "execution report", or "progress report"
- Mentions "swarm progress", "swarm status", or "swarm monitoring"
- Requests "task monitoring", "task status", or "task tracking"
- Asks about "execution status", "deployment progress", or "plan progress"
- Wants to see "progress bars", "visual reports", or "formatted status"
- Mentions "start monitoring", "continuous reports", or "auto-reports"
- Asks to check "blockers", "next actions", or "overall metrics"

## Instructions

### 1. Generate Instant Sprint Report

When user asks for immediate report:

```bash
# Generate and display report
.agents/scripts/utils/generate-sprint-report.sh .agents/plans/in_process/<plan-file>.md

# Or send to specific session
/home/devuser/openrag-agents/.agents/scripts/utils/tmux-claude-helper.sh send <session-name> \
  "$(.agents/scripts/utils/generate-sprint-report.sh <plan-file>)"
```

### 2. Start Continuous Monitoring (Daemon)

When user requests continuous/automatic reporting:

```bash
# Start daemon (reports every 5 minutes)
.agents/scripts/utils/start-sprint-report-daemon.sh <target-session> <plan-file>

# Example:
.agents/scripts/utils/start-sprint-report-daemon.sh noota_op-plan-test_s3_ \
  .agents/plans/in_process/test_s3_system_and_deployment_automation.md
```

### 3. Check Daemon Status

```bash
# Check if daemon is running
.agents/scripts/utils/status-sprint-report-daemon.sh

# View real-time logs
tail -f /tmp/sprint-report-daemon.log
```

### 4. Stop Monitoring

```bash
# Stop daemon gracefully
.agents/scripts/utils/stop-sprint-report-daemon.sh
```

### 5. Analyze Report Output

When presenting the report to the user:
1. **Highlight key metrics**: Overall progress, tasks completed/in-progress
2. **Identify blockers**: Point out any ❌ BLOCKERS section content
3. **Show next actions**: Summarize upcoming work from NEXT ACTIONS section
4. **Calculate ETA**: Sum up remaining task ETAs
5. **Track agents**: List which agents are working on what

For complete CLI reference and examples, see:
- [reference.md](reference.md) - Full command reference
- [examples.md](examples.md) - Detailed usage scenarios

## Expected Output

Provide the user with:

### Formatted Sprint Report Display
```
╔════════════════════════════════════════════════════════════════════╗
║                    📊 SPRINT EXECUTION REPORT                      ║
║                    Swarm: S3 & Deployment System                   ║
║                    Date: 2025-11-21 15:00:26                       ║
╠════════════════════════════════════════════════════════════════════╣
║  🎯 Sprint Goal: Complete S3 Multi-Profile & Auto-Deployment      ║
║  Progress: ██████████████░░ 85%                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  📋 TASK STATUS                                                    ║
║  ✅ Task 1-4: COMPLETE                                             ║
║  🔄 Task 5-7: IN PROGRESS                                          ║
╠════════════════════════════════════════════════════════════════════╣
║  📊 OVERALL METRICS                                                ║
║  Tasks Completed: 4/7 (57%)                                        ║
║  Overall Progress: ██████████████░░ 85%                            ║
║  Active Agents: 5                                                  ║
║  Files Created: 12 | Modified: 4                                   ║
╚════════════════════════════════════════════════════════════════════╝
```

### Summary Analysis
- **Progress**: X/Y tasks complete (Z% overall progress)
- **Active Work**: List agents and their current tasks
- **Blockers**: Highlight any critical issues (if any)
- **ETA**: Estimated completion time based on remaining tasks
- **Recommendations**: Suggest actions if blockers detected

### Daemon Status (if applicable)
- **Status**: Running/Stopped
- **PID**: Process ID
- **Uptime**: How long daemon has been running
- **Reports Sent**: Count from logs
- **Next Report**: Time until next automatic report

## Error Handling

1. **Missing plan file**: Ask user to specify correct plan path
2. **Session not found**: List available sessions with `tmux ls`
3. **Daemon already running**: Show status and ask if user wants to restart
4. **Daemon not running**: Offer to start it
5. **Permission errors**: Check file permissions and paths

## Integration Points

This skill works with:
- **Auto-Validator Daemon**: Messages validated every 2 minutes
- **Session Manager**: Uses tmux-claude-helper.sh for communication
- **Swarm Sessions**: Monitors all parallel task execution sessions
- **Plan Files**: Reads `.agents/plans/in_process/*.md` for task details

## Performance Notes

- Report generation: ~1 second
- Daemon overhead: Minimal (~0.1% CPU)
- Report interval: 5 minutes (configurable in start script)
- Log rotation: Manual (consider adding if logs grow large)
