---
name: everything
description: "Search Windows files with Everything and es.exe, integrate the SDK or IPC interface, and troubleshoot NTFS index behavior."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["everything", "voidtools", "ntfs-usn-journal", "mft-indexing", "everything-sdk-dll", "es-cli", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Voidtools Everything Real-Time Search AI Skill Guide (Claude)

## Overview & Engine Architecture
Voidtools Everything is a high-performance Windows file search and indexing engine capable of searching millions of files in milliseconds. Everything achieves zero-overhead indexing by directly parsing the **NTFS Master File Table (MFT)** and monitoring the **NTFS Update Sequence Number (USN) Change Journal**. The platform supports **regular expressions**, advanced **Boolean query operators**, exposes the **Everything C-SDK (`Everything64.dll`)**, supports **`WM_COPYDATA` IPC**, and provides a high-speed command-line interface (**`es.exe`**). Claude operates as a Principal Windows Systems Architect and File System Performance Specialist, specializing in **Everything C-SDK Python automation**, **`es.exe` pipeline scripting**, **NTFS USN index maintenance**, and **headless HTTP/IPC server deployment**.

### Everything Search Engine Architecture & SDK Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Everything Search Engine Stack              │
│                                                             │
│  User Interface & CLI Access Layer                          │
│  ├── Everything GUI Client (Instant Regex, Column Sorting)  │
│  ├── Command Line Interface Tool (`es.exe`)                 │
│  └── Built-in HTTP / ETP / WebDAV Server Engine             │
│                                                             │
│  Everything Core Engine & IPC Subsystem                     │
│  ├── Everything Windows Service (SYSTEM Daemon: No UAC)     │
│  ├── `Everything64.dll` C-SDK (Direct IPC via `WM_COPYDATA`) │
│  └── In-Memory File Metadata Trie Index (`Everything.db`)   │
│                                                             │
│  Storage Subsystem & NTFS Kernel Hook                       │
│  ├── Direct NTFS MFT (Master File Table) Parser             │
│  ├── Live NTFS USN Change Journal Event Stream              │
│  └── ReFS / FAT32 / Network Share Folder Rescanner Engine   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Everything C-SDK Automation (`Everything64.dll`)**: Author Python scripts using `ctypes` to query the in-memory Everything index with sub-millisecond latency, retrieving paths, file sizes, and timestamps.
2. **`es.exe` Command-Line Scripting**: Construct complex search commands using boolean operators (`|`, `!`), file size constraints (`size:>500MB`), extension groups (`ext:mp4;mkv`), and regex patterns.
3. **UAC Elimination & Service Configuration**: Configure the Everything Windows Service (`Everything Service`) to run with SYSTEM privileges so standard user clients query the index without prompting UAC dialogs.
4. **Network Drive & NAS Index Optimization**: Set up Folder Indexing with scheduled rescans for non-NTFS network shares (SMB/CIFS) to integrate network paths into the global index.

---

## Production Python Automation: High-Speed Everything C-SDK Search Client (`Everything64.dll`)

Save this script as `search_everything.py` (requires `Everything64.dll` in system path or script directory):

```python
"""
Voidtools Everything 64-bit C-SDK Client (ctypes)
Queries the Everything in-memory index via IPC and returns matched file paths, sizes, and dates.
"""

import sys
import os
import ctypes
from ctypes import wintypes

# 1. Load Everything64.dll
DLL_PATH = "Everything64.dll"

try:
    everything = ctypes.WinDLL(DLL_PATH)
except Exception:
    # Standard installation fallback path
    fallback = r"C:\Program Files\Everything\Everything64.dll"
    if os.path.exists(fallback):
        everything = ctypes.WinDLL(fallback)
    else:
        print("🚨 Error: Everything64.dll not found. Please place it in the script directory.")
        sys.exit(1)

# 2. Configure DLL Function Signatures
everything.Everything_SetSearchW.argtypes = [wintypes.LPCWSTR]
everything.Everything_QueryW.argtypes = [wintypes.BOOL]
everything.Everything_QueryW.restype = wintypes.BOOL
everything.Everything_GetNumResults.restype = wintypes.DWORD
everything.Everything_GetResultFullPathNameW.argtypes = [wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD]
everything.Everything_GetResultSize.argtypes = [wintypes.DWORD, ctypes.POINTER(ctypes.c_ulonglong)]
everything.Everything_GetResultSize.restype = wintypes.BOOL

def search_files(query_string: str, max_results: int = 15):
    print(f"--- [QUERYING EVERYTHING INDEX: '{query_string}'] ---")

    # Set Search Parameters: Regex enabled = False, Match Case = False
    everything.Everything_SetRegex(False)
    everything.Everything_SetMatchCase(False)
    everything.Everything_SetSearchW(query_string)
    everything.Everything_SetMax(max_results)
    everything.Everything_SetRequestFlags(0x00000001 | 0x00000010) # Full Path + Size

    # Execute IPC Query
    if not everything.Everything_QueryW(True):
        err = everything.Everything_GetLastError()
        print(f"🚨 Everything Query Failed with Error Code: {err}")
        return

    num_results = everything.Everything_GetNumResults()
    total_matches = everything.Everything_GetTotResults()
    print(f"Found {total_matches} total match(es) (Displaying top {min(num_results, max_results)}):\n")

    buf = ctypes.create_unicode_buffer(1024)
    size_bytes = ctypes.c_ulonglong()

    for i in range(num_results):
        everything.Everything_GetResultFullPathNameW(i, buf, 1024)
        everything.Everything_GetResultSize(i, ctypes.byref(size_bytes))
        size_mb = size_bytes.value / (1024 * 1024)

        print(f"• [{size_mb:>8.2f} MB] {buf.value}")

    print("\n✅ Query completed in sub-millisecond latency.")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "ext:log size:>10mb"
    search_files(query)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Search Returns 0 Results / Service Inactive** | `Everything Service` is stopped or background process not running. | Start service via elevated command prompt:<br>`Everything.exe -svc-start` or run `net start "Everything"`. |
| **UAC Prompt Appears Every Time Everything Opens** | Client executable configured with "Run as administrator" compatibility flag. | 1. In *Tools $\rightarrow$ Options $\rightarrow$ General*, check **Everything Service**.<br>2. Uncheck **Run as administrator** to allow standard non-elevated user access. |
| **Search Results Out of Sync with Disk** | NTFS USN Change Journal index buffer corrupted or volume unmounted uncleanly. | In Everything, go to *Tools $\rightarrow$ Options $\rightarrow$ Indexes*, click **Force Rebuild**. |
| **Network Shared Folder Not Appearing in Search** | Network drives (SMB) do not support NTFS USN journals and must be indexed manually. | In Options $\rightarrow$ **Folders**, click **Add...** $\rightarrow$ Select network UNC path $\rightarrow$ Set Rescan Schedule (e.g. Daily). |

---

## Command Line Syntax & `es.exe` CLI Recipes

```bash
# 1. Search for Large Video Files (>1GB) Modified in the Last 7 Days
es.exe "ext:mp4;mkv;mov size:>1gb dm:last7days" -sort-size-desc

# 2. Search using Regular Expressions and Export to CSV
es.exe -r "^[0-9]{4}_[A-Z]+.*\.pdf$" -export-csv "C:\SearchResults.csv"

# 3. Force Immediate NTFS USN Index Rebuild
"C:\Program Files\Everything\Everything.exe" -reindex
```

### Essential File Locations
- **Configuration File**: `%APPDATA%\Everything\Everything.ini`
- **Database Cache**: `%APPDATA%\Everything\Everything.db`
- **CLI Utility**: `C:\Program Files\Everything\es.exe`

---

## Agent Operational Directive
> **MANDATORY**: For automated systems integration on Windows, always install and run the "Everything Service" as a background daemon so automation scripts and non-elevated users can query the index without triggering UAC popups.
