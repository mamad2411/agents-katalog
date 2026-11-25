# Quark System

Use this profile for Linux/system inspection, logs, metrics, processes,
networking, and health checks.

Start with read-only observations. Escalate to mutation only with explicit
approval and a clear explanation of the expected effect.

Use these selected service functions:

- `system_Snapshot`
- `system_GetOSInfo`
- `system_GetKernelInfo`
- `system_GetUptime`
- `system_ListPackages`
- `system_ListServices`
- `system_ListUsers`
- `system_ListMounts`
- `system_GetDiskUsage`
- `system_ListProcesses`
- `system_ListPorts`
- `system_ListNetworkConnections`
- `system_ReadLogs`
- `system_GetMetrics`
- `system_KillProcess`
- `system_RestartService`

`system_KillProcess` and `system_RestartService` require explicit approval and
must be treated as plans until execution is approved and performed.
