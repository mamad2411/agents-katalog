---
name: system-informer
description: "Inspect Windows processes and memory with System Informer and native APIs; troubleshoot driver and diagnostic access."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["system-informer", "process-hacker", "ksysteminformer-sys", "ntdll-native-api", "process-memory-inspection", "windows-kernel", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# System Informer Kernel & Process Diagnostics AI Skill Guide (Claude)

## Overview & Engine Architecture
System Informer (formerly Process Hacker 3) is an advanced Windows process, memory, network, and kernel inspection utility written in native C. Operating through undocumented **NTDLL Native APIs (`NtQuerySystemInformation`, `NtQueryInformationProcess`, `NtQueryObject`)** and an optional kernel companion driver (**`KSystemInformer.sys`**), System Informer provides deep visibility into **Protected Process Light (PPL)**, thread call stacks, kernel driver object tables, virtual memory allocations, and real-time ETW disk/network streams. Claude operates as a Principal Windows Kernel Systems Engineer and Reverse Engineering Specialist, specializing in **NTDLL process inspection scripting (`ctypes`)**, **`KSystemInformer` driver debugging**, **token privilege analysis**, and **zombie process IRP deadlock triage**.

### System Informer Architecture & NTDLL Subsystem

```
┌─────────────────────────────────────────────────────────────┐
│                 System Informer Architecture                │
│                                                             │
│  User Interface & Diagnostic Dashboard                     │
│  ├── Multi-Tab Viewport (Processes, Services, Network, Disk)│
│  ├── Process Properties (Threads, Handles, Memory, Modules) │
│  └── Real-Time ETW Telemetry Graphs (CPU, IOPS, Network)    │
│                                                             │
│  Native NTDLL Subsystem & P/Invoke Layer                    │
│  ├── Native Kernel APIs (`NtQueryInformationProcess`, `PEB`)│
│  ├── Virtual Memory Scanner (`VirtualQueryEx`, `ReadVM`)    │
│  └── Token Privilege Adjuster (`SeDebugPrivilege`, `SeTcb`) │
│                                                             │
│  Kernel Mode Driver Subsystem                               │
│  ├── `KSystemInformer.sys` Companion Driver                 │
│  ├── PPL (Protected Process Light) Memory & Handle Access   │
│  └── Kernel Object Table & Callback Routine Enumeration     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Native NTDLL Python Process Inspection**: Author Python scripts utilizing `ctypes` to interface with `ntdll.dll` Native APIs, reading Process Environment Blocks (PEB), extract runtime command lines, and enumerate loaded DLL modules.
2. **`KSystemInformer` Kernel Driver Triage**: Resolve driver load failures caused by Windows Core Isolation (HVCI) or anti-cheat conflicts to restore kernel-level process termination and PPL inspection.
3. **Handle & Mutex Search Automation**: Locate locked files, named pipes, and mutex handles preventing software updates or directory deletion.
4. **Thread Call Stack & Deadlock Analysis**: Inspect kernel and user-mode thread call stacks to diagnose deadlocked IRPs (I/O Request Packets) causing unkillable zombie processes.

---

## Production Python Automation: Native NTDLL Process & Command Line Inspector (`ctypes`)

Save this script as `inspect_process_peb.py`:

```python
"""
Native Windows Process & PEB Inspector (ctypes / ntdll)
Queries low-level Process Basic Information and PEB to extract full command-line arguments and paths.
"""

import sys
import ctypes
from ctypes import wintypes

ntdll = ctypes.WinDLL("ntdll.dll")
kernel32 = ctypes.WinDLL("kernel32.dll")

# Win32 Process Access Rights
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

# NTSTATUS Struct: PROCESS_BASIC_INFORMATION
class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ExitStatus", wintypes.LONG),
        ("PebBaseAddress", ctypes.c_void_p),
        ("AffinityMask", ctypes.c_void_p),
        ("BasePriority", wintypes.LONG),
        ("UniqueProcessId", ctypes.c_void_p),
        ("InheritedFromUniqueProcessId", ctypes.c_void_p)
    ]

# UNICODE_STRING
class UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ("Length", wintypes.USHORT),
        ("MaximumLength", wintypes.USHORT),
        ("Buffer", ctypes.c_void_p)
    ]

def inspect_process(pid: int):
    print(f"--- [INSPECTING PROCESS PID: {pid} VIA NTDLL] ---")

    h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h_process:
        err = kernel32.GetLastError()
        print(f"🚨 Failed to open process PID {pid} (Win32 Error: {err}). Run as Administrator.")
        return

    try:
        pbi = PROCESS_BASIC_INFORMATION()
        ret_len = wintypes.ULONG()

        # Call NtQueryInformationProcess (ProcessBasicInformation = 0)
        status = ntdll.NtQueryInformationProcess(
            h_process,
            0,
            ctypes.byref(pbi),
            ctypes.sizeof(pbi),
            ctypes.byref(ret_len)
        )

        if status != 0:
            print(f"🚨 NtQueryInformationProcess failed with NTSTATUS: {hex(status)}")
            return

        print(f"• Exit Status:        {pbi.ExitStatus}")
        print(f"• PEB Base Address:   {hex(pbi.PebBaseAddress) if pbi.PebBaseAddress else 'None'}")
        print(f"• Parent PID:         {pbi.InheritedFromUniqueProcessId}")

        if pbi.PebBaseAddress:
            # Read ProcessParameters Pointer from PEB (Offset 0x20 on 64-bit)
            params_ptr = ctypes.c_void_p()
            bytes_read = ctypes.c_size_t()
            peb_offset = 0x20 # 64-bit RTL_USER_PROCESS_PARAMETERS offset

            kernel32.ReadProcessMemory(
                h_process,
                ctypes.c_void_p(pbi.PebBaseAddress + peb_offset),
                ctypes.byref(params_ptr),
                ctypes.sizeof(params_ptr),
                ctypes.byref(bytes_read)
            )

            if params_ptr.value:
                # Read CommandLine UNICODE_STRING (Offset 0x70 on 64-bit RTL_USER_PROCESS_PARAMETERS)
                cmd_unicode = UNICODE_STRING()
                cmd_offset = 0x70

                kernel32.ReadProcessMemory(
                    h_process,
                    ctypes.c_void_p(params_ptr.value + cmd_offset),
                    ctypes.byref(cmd_unicode),
                    ctypes.sizeof(cmd_unicode),
                    ctypes.byref(bytes_read)
                )

                if cmd_unicode.Length > 0 and cmd_unicode.Buffer:
                    buf = ctypes.create_unicode_buffer(cmd_unicode.Length // 2)
                    kernel32.ReadProcessMemory(
                        h_process,
                        ctypes.c_void_p(cmd_unicode.Buffer),
                        buf,
                        cmd_unicode.Length,
                        ctypes.byref(bytes_read)
                    )
                    print(f"• Command Line:       '{buf.value}'")

        print("✅ Process low-level inspection completed successfully.")

    finally:
        kernel32.CloseHandle(h_process)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_process_peb.py <PID>")
        sys.exit(1)
    inspect_process(int(sys.argv[1]))
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`KSystemInformer.sys` Fails to Load** | Windows Core Isolation (HVCI Memory Integrity) blocking driver signature. | In System Informer Settings $\rightarrow$ General, check driver signing status or run `sc start KSystemInformer`. |
| **Antivirus Process Shows `<Access Denied>`** | Process is executing as **Protected Process Light (PPL)**, which blocks user-mode handle access. | Enable `KSystemInformer` kernel driver in Settings $\rightarrow$ **Advanced** to bypass user-mode handle filters. |
| **Handle Search Hangs System Informer GUI** | A synchronous I/O handle (e.g. stalled named pipe) blocked `NtQueryObject`. | In Handle Search dialog, uncheck **Search Named Pipes** to prevent blocking queries. |
| **Process Cannot Be Killed (Zombie Process)** | A thread inside the process is blocked indefinitely waiting on uncompleted kernel IRP. | Inspect thread call stacks in Process Properties $\rightarrow$ **Threads** tab to identify the faulty driver. |

---

## Command Line Syntax & System Informer Recipes

```bash
# 1. Launch System Informer and Open System Information HUD
"C:\Program Files\SystemInformer\SystemInformer.exe" -c -sysinfo

# 2. Select and Highlight Specific Process ID
"C:\Program Files\SystemInformer\SystemInformer.exe" -selectpid 4328

# 3. Query Active Network Sockets via PowerShell
Get-NetTCPConnection | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess
```

### Essential File Locations
- **Application Config**: `%APPDATA%\SystemInformer\settings.xml`
- **Kernel Driver**: `C:\Program Files\SystemInformer\KSystemInformer.sys`

---

## Agent Operational Directive
> **MANDATORY**: When attempting to inspect Protected Process Light (PPL) processes or kernel threads, ensure `KSystemInformer.sys` is active and System Informer is running with elevated `SeDebugPrivilege`.
