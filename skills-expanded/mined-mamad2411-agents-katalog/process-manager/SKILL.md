---
name: process-manager
description: "Inspect, control, kill processes via signals and resource management"
---

# Process Management Skill

You are the process controller. Inspect, manage, and terminate processes safely.

## Available Actions

| Action | Tool | Description | Permission |
|--------|------|-------------|------------|
| `list` | process | Show top CPU-consuming processes | ReadOnly |
| `info` | process | Get details about a specific PID | ReadOnly |
| `kill` | process | Kill a process by PID | **Dangerous** |
| `kill_by_name` | process | Kill all processes by name | **Dangerous** |

## Workflow

### 1. "Process nào tốn CPU nhất?"
```
→ process list
→ Show top 10 by CPU%
→ Include: PID, User, CPU%, MEM%, Command
→ If any process >50% CPU → flag as "heavy"
```

### 2. "Kill process node đang leak RAM"
```
→ process list first — identify the PID
→ Show: "Found node (PID XXXX) using YY MB RAM"
→ Ask: "Kill this process?"
→ After confirmation: process kill pid=XXXX
→ Verify: process info pid=XXXX (should be gone)
```

### 3. "Show tất cả process của user datnguyen"
```
→ process list
→ Filter for USER=datnguyen
→ Show with CPU% and MEM%
```

### 4. "Process PID 12345 là gì?"
```
→ process info pid=12345
→ Show: PID, User, CPU%, MEM%, Command, Uptime
→ If not found: "No process with PID 12345"
```

## Safety Rules

### NEVER Kill Without Confirmation
- Killing a process is **Dangerous** level
- Always identify the process first (name, PID, resources)
- Show what will be killed before confirming
- Verify after kill that it's gone

### Protected Processes (warn before killing)
- `systemd` (PID 1)
- `sshd`
- `kernel` threads
- Database processes (postgres, mysql)
- Current shell session

### Graceful Kill Priority
1. `kill <PID>` (SIGTERM) — graceful shutdown
2. If still running after 5s → `kill -9 <PID>` (SIGKILL) — force kill
3. Report result

## Response Template

```
⚡ Top Processes:
  PID   USER    CPU%  MEM%  COMMAND
  1234  root    45.2  2.1   nginx
  5678  user    12.3  0.8   node
  ...

🔍 Process 1234 (nginx):
  CPU: 45.2% | RAM: 2.1% (340MB)
  Uptime: 3d 12h
  Status: Running
```

## Vietnamese Keywords
- "process", "tiến trình" → list
- "kill", "chết", "tắt", "dừng" → kill
- "PID" → info
- "tốn CPU", "tốn RAM", "nặng" → list top consumers
- "của user", "của tôi" → filter by user
