# Test Logging Standards

## 🔴 MANDATORY: Test Execution Logging

**ALL test execution scripts MUST log to standardized locations with timestamp + context naming.**

---

## Core Requirements

### Log File Location Pattern

**Format:** `/logs/context/TIMESTAMP+CONTEXT.log`

**Components:**
- **Base Directory:** `logs/` (at repository root)
- **Context Subdirectory:** Category of log (e.g., `test_execution`, `performance`, `integration`)
- **Filename:** `YYYYMMDD_HHMMSS+context.log`
  - **TIMESTAMP:** `YYYYMMDD_HHMMSS` format (e.g., `20251115_093937`)
  - **CONTEXT:** Descriptive name (e.g., `test_execution`, `xunit_tests`, `k6_performance`)

---

## Directory Structure

```
logs/
├── test_execution/
│   ├── 20251115_093937+test_execution.log
│   ├── 20251115_101523+test_execution.log
│   └── 20251115_143022+test_execution.log
├── performance/
│   ├── 20251115_094500+k6_load_test.log
│   └── 20251115_110230+k6_stress_test.log
├── integration/
│   ├── 20251115_095000+xunit_integration.log
│   └── 20251115_120000+api_integration.log
└── unit/
    └── 20251115_100000+unit_tests.log
```

---

## Examples

### ✅ CORRECT:

**run-all-tests.ps1:**
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = "logs/test_execution"
$logFile = Join-Path $logDir "${timestamp}+test_execution.log"
```
Result: `logs/test_execution/20251115_093937+test_execution.log`

**k6 performance test:**
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = "logs/performance"
$logFile = Join-Path $logDir "${timestamp}+k6_load_test.log"
```
Result: `logs/performance/20251115_094500+k6_load_test.log`

**xUnit integration test:**
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = "logs/integration"
$logFile = Join-Path $logDir "${timestamp}+xunit_integration.log"
```
Result: `logs/integration/20251115_095000+xunit_integration.log`

### ❌ WRONG:

```powershell
# Wrong: No context subdirectory
$logFile = "logs/${timestamp}_test_execution.log"

# Wrong: No '+' separator
$logFile = "logs/test_execution/${timestamp}_test_execution.log"

# Wrong: Context in wrong order
$logFile = "logs/test_execution/test_execution_${timestamp}.log"

# Wrong: No timestamp
$logFile = "logs/test_execution/test_execution.log"
```

---

## Context Categories

### Standard Context Values:

**Test Execution:**
- `test_execution` - Full test suite (xUnit + k6)
- `unit_tests` - Unit tests only
- `integration_tests` - Integration tests only
- `xunit_integration` - xUnit integration tests
- `api_integration` - API integration tests

**Performance:**
- `k6_load_test` - k6 load testing
- `k6_stress_test` - k6 stress testing
- `k6_spike_test` - k6 spike testing
- `performance_baseline` - Performance baseline tests

**Deployment:**
- `deployment` - Deployment logs
- `docker_compose` - Docker Compose logs
- `container_startup` - Container startup logs

**CI/CD:**
- `ci_pipeline` - CI pipeline execution
- `cd_deployment` - CD deployment execution
- `build` - Build process logs

---

## Log File Format

### Minimum Requirements:

**Each log line MUST include:**
1. **Timestamp:** `[YYYY-MM-DD HH:mm:ss.fff]`
2. **Level:** `[INFO|WARN|ERROR|DEBUG]`
3. **Message:** Log message content

**Format:**
```
[YYYY-MM-DD HH:mm:ss.fff] [LEVEL] Message
```

**Example:**
```
[2025-11-15 09:37:46.517] [INFO] Bank Name Matching API - Test Suite
[2025-11-15 09:37:46.576] [INFO] ✅ API is healthy
[2025-11-15 09:37:48.686] [WARN] xUnit tests failed (exit code: 1)
[2025-11-15 09:38:49.698] [INFO] ✅ k6 performance tests passed
```

---

## Implementation Example

### PowerShell Script Template:

```powershell
#Requires -Version 7.0

param(
    [string]$Context = 'test_execution'
)

$ErrorActionPreference = "Stop"

# Setup logging with context subdirectory
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = "logs/$Context"

# Create context subdirectory if it doesn't exist
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Log file: logs/context/TIMESTAMP+context.log
$logFile = Join-Path $logDir "${timestamp}+${Context}.log"
$logStream = [System.IO.StreamWriter]::new($logFile, $false, [System.Text.Encoding]::UTF8)

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [ConsoleColor]$Color = [ConsoleColor]::White
    )
    
    $logTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
    $logMessage = "[$logTimestamp] [$Level] $Message"
    
    # Write to console
    Write-Host $Message -ForegroundColor $Color
    
    # Write to log file
    $logStream.WriteLine($logMessage)
    $logStream.Flush()
}

try {
    Write-Log "Starting test execution..." "INFO" Cyan
    Write-Log "Log file: $logFile" "INFO" Gray
    
    # ... test execution code ...
    
    Write-Log "Test execution complete!" "INFO" Green
} finally {
    # Always close log stream
    $logStream.Close()
}
```

---

## Log Retention

### Retention Policy:

**Keep logs for:**
- Last 30 days in active directories
- Archive older logs to `logs/archive/YYYY-MM/`

**Archive Structure:**
```
logs/
├── test_execution/
│   └── (last 30 days)
├── performance/
│   └── (last 30 days)
└── archive/
    ├── 2025-10/
    │   ├── test_execution/
    │   └── performance/
    └── 2025-11/
        ├── test_execution/
        └── performance/
```

---

## Critical Rules

### ALWAYS:
- ✅ Use `logs/context/` directory structure
- ✅ Include timestamp in filename: `YYYYMMDD_HHMMSS`
- ✅ Use `+` separator: `timestamp+context.log`
- ✅ Create context subdirectory if it doesn't exist
- ✅ Include timestamp, level, and message in each log line
- ✅ Close log stream in `finally` block (PowerShell) or cleanup handlers

### NEVER:
- ❌ Log directly to `logs/` root without context subdirectory
- ❌ Omit timestamp from filename
- ❌ Use separators other than `+` (like `_` or `-`)
- ❌ Hardcode log paths without context parameter
- ❌ Leave log streams open without cleanup

---

## Integration with CI/CD

### Environment Variables:

When running in CI/CD, set:
```bash
LOG_CONTEXT="ci_pipeline"
LOG_DIR="logs/ci_pipeline"
```

**Example:**
```powershell
$context = if ($env:LOG_CONTEXT) { $env:LOG_CONTEXT } else { 'test_execution' }
$logDir = if ($env:LOG_DIR) { $env:LOG_DIR } else { "logs/$context" }
```

---

## Related Rules

- **Audit Log Rule:** `.cursor/rules/ai-audit-log.mdc`
  - Different from test logs - audit logs track AI interactions
  - Audit logs: `logs/audit/YYYY-MM-DD.jsonl`
  - Test logs: `logs/context/TIMESTAMP+context.log`

---

**Last Updated:** 2025-11-15  
**Version:** 1.0.0  
**Rule Type:** MANDATORY - Test Logging Standards  
**Priority:** HIGH  
**Always Apply:** YES
