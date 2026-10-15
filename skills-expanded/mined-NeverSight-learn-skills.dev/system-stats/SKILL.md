---
name: system-stats
description: >
  Reports a snapshot of host machine resources — OS, hostname, CPU model and
  core count, memory used/total, disk used/total, and uptime. Use when user
  asks about local system state ("how much memory am I using?", "what's the
  CPU?", "show disk usage", "what OS is this?", "uptime?").
---

## When to use

Trigger on queries about the local machine's hardware or resource state:
- "How much RAM is being used?"
- "What's the CPU on this box?"
- "Show me disk usage."
- "What OS am I running?"
- "How long has this been up?"

Do **not** use for: network info, GPU info, process lists, remote machines.

## How to run

Detect host OS and execute the matching block via the shell tool. Run all six probes (OS, hostname, CPU, memory, disk, uptime), then format the result.

### Linux

```bash
. /etc/os-release 2>/dev/null; echo "OS: ${PRETTY_NAME:-Linux}"
echo "Hostname: $(hostname)"
echo "CPU: $(awk -F: '/model name/ {print $2; exit}' /proc/cpuinfo | sed 's/^ *//') ($(nproc) cores)"
awk '/MemTotal/ {t=$2} /MemAvailable/ {a=$2} END {printf "Memory: %d MB used / %d MB total\n", (t-a)/1024, t/1024}' /proc/meminfo
df -h / | awk 'NR==2 {print "Disk: "$3" used / "$2" total ("$5" used)"}'
echo "Uptime: $(uptime -p)"
```

### macOS

```bash
echo "OS: macOS $(sw_vers -productVersion)"
echo "Hostname: $(hostname)"
echo "CPU: $(sysctl -n machdep.cpu.brand_string) ($(sysctl -n hw.ncpu) cores)"
PAGE=$(sysctl -n hw.pagesize); T=$(sysctl -n hw.memsize)
U=$(vm_stat | awk '/Pages active|Pages wired/ {gsub(/\./,""); s+=$NF} END {print s}')
echo "Memory: $((U*PAGE/1048576)) MB used / $((T/1048576)) MB total"
df -h / | awk 'NR==2 {print "Disk: "$3" used / "$2" total ("$5" used)"}'
echo "Uptime: $(uptime | sed 's/^.*up //; s/, *[0-9]* user.*//')"
```

### Windows (PowerShell)

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($env:SystemDrive)'"
$uptime = (Get-Date) - $os.LastBootUpTime
$memUsedMB = [int](($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1024)
$memTotalMB = [int]($os.TotalVisibleMemorySize / 1024)
$diskUsedGB = [int](($disk.Size - $disk.FreeSpace) / 1GB)
$diskTotalGB = [int]($disk.Size / 1GB)
$pct = [int]((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100)

"OS: $($os.Caption)"
"Hostname: $env:COMPUTERNAME"
"CPU: $($cpu.Name) ($($cpu.NumberOfLogicalProcessors) cores)"
"Memory: $memUsedMB MB used / $memTotalMB MB total"
"Disk: ${diskUsedGB}G used / ${diskTotalGB}G total ($pct% used)"
"Uptime: $($uptime.Days)d $($uptime.Hours)h $($uptime.Minutes)m"
```

## Output format

Always present in this exact 6-line shape, in this order:

```
OS: <name + version>
Hostname: <host>
CPU: <model> (<n> cores)
Memory: <used> MB used / <total> MB total
Disk: <used>G used / <total>G total (<pct>% used)
Uptime: <Xd Yh Zm>  OR  <human-readable like "up 2 hours, 15 minutes">
```

## Notes

- Always probe live system. Never cache or fabricate.
- If a probe fails (e.g., `/etc/os-release` missing), fall back to a sensible default (`Linux`, `unknown`) for that single field — don't abort the whole report.
- On Windows under Git Bash, prefer the PowerShell block via `powershell.exe -NoProfile -Command "..."`.
