---
name: system_info
description: Get system information, check processes, disk usage, network status
triggers: [system, processes, disk, memory, cpu, ram, network, ip, battery, uptime, df, ps, macos, система, диск, память, сеть, аптайм]
tools: [shell]
platform: macos
---

## System information (macOS)

Use shell commands to read system state.

### General

macOS version:

```
sw_vers
```

Hostname and user:

```
whoami && hostname
```

Uptime:

```
uptime
```

### Processes

List processes (truncated):

```
ps aux | head -20
```

Find a process:

```
pgrep -fl "process_name"
```

Top by CPU:

```
ps -Arco pid,pcpu,comm | head -10
```

### Disk

Overall usage:

```
df -h
```

Directory size:

```
du -sh /path/to/directory
```

### Memory & CPU

Memory:

```
vm_stat | head -10
```

CPU model:

```
sysctl -n machdep.cpu.brand_string
```

### Network

IPv4 addresses:

```
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Connectivity:

```
ping -c 3 google.com
```

### Battery

```
pmset -g batt
```

### Rules

1. Pipe verbose output through `head` / `tail`.
2. Avoid commands that destabilize the system.
3. Never kill processes without explicit user confirmation.
4. Prefer short, focused commands over huge dumps.
