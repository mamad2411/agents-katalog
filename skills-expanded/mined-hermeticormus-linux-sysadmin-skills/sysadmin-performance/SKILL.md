---
name: sysadmin-performance
description: Analyze and optimize performance on a Debian/Ubuntu Linux system by assessing CPU, memory, disk, network, and processes, finding the bottleneck, then applying targeted tuning with before-and-after measurement. Use when a machine is slow and you need to find why.
license: MIT
---

# System performance analysis

Analyze and optimize performance on a Debian/Ubuntu Linux machine. Measure before forming an opinion; tune the bottleneck, not a guess. Confirm before any change that alters kernel parameters, kills processes, or disables services.

## Performance analysis steps

### 1. Current-state assessment

CPU:

```bash
top -bn1 | head -20
mpstat 1 5
```

Look at usage patterns, per-process CPU, and load average.

Memory:

```bash
free -h
vmstat 1 5
```

Look at RAM usage, swap usage, and memory pressure.

Disk:

```bash
df -h
iostat -x 1 5
```

Look at free space, I/O performance, and per-disk utilization.

Network:

```bash
ifstat 1 5
netstat -s
```

Look at throughput, packet statistics, and errors or drops.

Processes:

```bash
ps aux --sort=-%mem | head -10
ps aux --sort=-%cpu | head -10
```

Look for resource hogs, zombie processes, and process states.

### 2. Identify the bottleneck

Common bottlenecks: CPU saturation, memory exhaustion, disk I/O wait, network congestion, process limits. Name which one the measurements point to before tuning.

### 3. Optimization strategies

For CPU: identify CPU-intensive processes, check for runaway processes, consider `nice`/`renice`, review cron jobs, optimize application code.

For memory: check for leaks, review swap usage, adjust swappiness, kill memory hogs, add RAM if genuinely needed.

For disk: check usage, clean up old files, tune the I/O scheduler, consider an SSD, check for a failing disk with `smartctl`.

For network: check bandwidth, review firewall rules, tune network settings, check for attacks.

### 4. System tuning

Kernel parameters in `/etc/sysctl.conf`: `vm.swappiness`, `fs.file-max`, `net.core` parameters.

Service optimization: disable unused services, tune service configs, review startup items.

Resource limits in `/etc/security/limits.conf`: open-file limits, process limits, memory limits.

### 5. Monitoring setup

Set up ongoing monitoring: `htop` for a real-time view, logging for historical data, alerts for issues, and recorded performance baselines.

### 6. Before-and-after comparison

Benchmark before changes, apply optimizations, benchmark after, and document the result.

Guide me through systematic performance analysis and give specific recommendations for this system.

---

See full content at https://github.com/HermeticOrmus/linux-sysadmin-skills.
