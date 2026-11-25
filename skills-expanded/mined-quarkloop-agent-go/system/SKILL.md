# service-system

The System service exposes typed local operating-system observations and
approval-gated mutation plans. Use these service functions instead of shell
commands when answering Quark System questions.

## Agent Rules

1. Prefer `system_Snapshot` for broad diagnostics.
2. Use narrower functions such as `system_ListProcesses`,
   `system_ListNetworkConnections`, or `system_GetMetrics` when the user asks a
   specific question.
3. Treat all observations as point-in-time data. Include what function was used
   and when the answer depends on live state.
4. Never expose arbitrary shell commands or raw osquery SQL as the product flow.
5. Do not call mutation functions unless the user explicitly asks for the
   change and runtime approval is available.
6. `system_KillProcess` and `system_RestartService` return approval-gated
   mutation plans; do not describe them as completed actions until execution is
   actually approved and performed.

## Service Functions

- `system_Snapshot`: broad OS/kernel/uptime/mount/disk/process/network/metric
  snapshot.
- `system_GetOSInfo`: operating-system identity and architecture.
- `system_GetKernelInfo`: kernel name, release, version, and machine.
- `system_GetUptime`: uptime seconds and boot timestamp.
- `system_ListPackages`: installed packages from an approved backend.
- `system_ListServices`: service manager units and states.
- `system_ListUsers`: local users with optional system-user filtering.
- `system_ListMounts`: mounted filesystems and options.
- `system_GetDiskUsage`: disk usage for one path or known mounts.
- `system_ListProcesses`: running processes with resource summaries.
- `system_ListPorts`: listening local ports and owners when available.
- `system_ListNetworkConnections`: local network connections and states.
- `system_ReadLogs`: bounded reads from approved log sources.
- `system_GetMetrics`: load, memory, and swap metrics.
- `system_KillProcess`: approval-gated process termination plan.
- `system_RestartService`: approval-gated service restart plan.

## osquery Guidance

osquery can be used as an optional backend after license and packaging review,
but it is an implementation detail. Agents must call typed service functions and
must not generate arbitrary SQL for direct execution.
