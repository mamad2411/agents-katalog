---
name: automotive-logging
description: >
  DLT (Diagnostic Log and Trace) logging skills for automotive systems Includes 1 skill files covering .
tags: [automotive, automotive-logging]
source: "https://github.com/pangzhenying2025/hermes-automotive-skills"
source_repository: "pangzhenying2025/hermes-automotive-skills"
source_path: "skills/automotive-logging/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Automotive Logging

1 skill files covering logging domain for automotive software engineering.

## Required Tools

- DLT Viewer (optional, for visualization)
- Python 3.8+
- dlt-daemon (optional, for network logging)


## Instructions

### dlt-logging

## DLT (Diagnostic Log and Trace) Guide — AUTOSAR/COVESA

### Overview

DLT is the standardized logging framework for automotive systems, defined by
AUTOSAR and maintained by COVESA. It provides structured, high-performance logging
with application/context-based filtering, binary message format for efficiency,
and support for multi-ECU log aggregation.

### Architecture

```
Application 1        Application 2        Application N
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ DLT User    │     │ DLT User    │     │ DLT User    │
│ Library     │     │ Library     │     │ Library     │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ UNIX Socket / Shared Memory
                  ┌────────┴────────┐
                  │  DLT Daemon     │
                  │  (dlt-daemon)   │
                  ├─────────────────┤
                  │ File Output     │ → /var/log/dlt/*.dlt
                  │ Network Output  │ → TCP port 3490
                  │ Serial Output   │ → /dev/ttyS0
                  └─────────────────┘
                           │ TCP/IP
                  ┌────────┴────────┐
                  │  DLT Viewer     │  (Desktop analysis tool)
                  └─────────────────┘
```

### Identification Model

DLT uses a hierarchical ID system for filtering:

- **ECU ID** (4 chars): Identifies the hardware unit (e.g., "ECU1", "GW01")
- **Application ID** (4 chars): Identifies the software application (e.g., "ADAS", "DIAG")
- **Context ID** (4 chars): Identifies the subsystem within an app (e.g., "CTRL", "SENS")

This enables precise filtering: show only ADAS.CTRL errors from ECU1.

### Log Levels

| Level | Value | Usage |
|-------|-------|-------|
| FATAL | 0x01 | System failure, requires immediate action |
| ERROR | 0x02 | Error condition, operation failed |
| WARN | 0x03 | Potential problem, degraded operation |
| INFO | 0x04 | Normal operational events |
| DEBUG | 0x05 | Detailed debug information |
| VERBOSE | 0x06 | Maximum detail (development only) |

### Message Format

DLT messages use a compact binary format for efficiency:

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Storage Hdr  │ Standard Hdr │ Extended Hdr │ Payload      │
│ (16 bytes)   │ (4 bytes)    │ (10 bytes)   │ (variable)   │
└──────────────┴──────────────┴──────────────┴──────────────┘

Storage Header: timestamp (seconds + microseconds), ECU ID
Standard Header: version, message counter, length, ECU ID
Extended Header: message info, app ID, context ID
Payload: type-safe arguments (string, int, float, raw data)
```

### Verbose vs Non-Verbose Mode

- **Verbose mode**: Payload includes type info per argument (self-describing).
  Larger messages but viewable without external database.
- **Non-verbose mode**: Payload is raw data, requires FIBEX database to decode.
  Smaller messages, used in production for bandwidth savings.

### DLT Daemon Configuration

Key configuration file: `/etc/dlt.conf`

```ini
# DLT daemon configuration
Verbose = 1                    # Enable verbose mode
DaemonFIFOSize = 65536        # FIFO buffer size
LoggingLevel = INFO            # Daemon's own log level
OfflineTraceDirectory = /var/log/dlt  # File output directory
OfflineTraceFileSize = 10000000       # Max file size (10MB)
OfflineTraceMaxSize = 100000000       # Max total size (100MB)
ECUId = ECU1                   # This ECU's identifier
```

### Multi-ECU Logging

For distributed automotive systems:
- Each ECU runs its own dlt-daemon with unique ECU ID
- Central logger connects to all ECUs via TCP port 3490
- DLT Viewer aggregates and time-correlates logs from all ECUs
- Use NTP or PTP for time synchronization across ECUs

### Integration with Python

The DLTAdapter in this project wraps the DLT protocol for Python applications.
Key patterns:
- Use context managers (`with DLTAdapter(...)`) for automatic cleanup
- Pass structured data as keyword arguments for filtering
- Use separate contexts per subsystem for independent log level control
- Integrate with Python's standard logging via DLTLoggingHandler

### Performance Considerations

- DLT overhead: ~1 microsecond per log message (shared memory transport)
- File I/O is buffered; messages may be lost on crash without flush
- Use log level filtering to reduce volume in production
- Rotate log files to prevent disk exhaustion (configure max file/total size)

### Best Practices

- Use meaningful 4-character IDs: ADAS (not APP1), CTRL (not CTX1)
- Set production log level to INFO or WARN (not DEBUG/VERBOSE)
- Always close DLT adapters to flush buffered messages
- Use DLT Viewer's filter and search for efficient log analysis
- Archive DLT files with ECU ID and timestamp for traceability
- Correlate DLT logs with CAN traces and diagnostic sessions for RCA
