---
name: error-handling
description: Reference skill for pydita's error recording and reporting model. Use this skill when you need to understand how errors are accumulated in the shared errors dict, work with ErrorRecord and SEVERITY, filter errors by severity level, or produce a formatted error report using reportErrors(). Covers DitaContext.recordError() and Logger/ConsoleLogger helpers.
compatibility: Python 3.10+. Requires pydita (aenum).
---

## Overview

pydita uses a **shared mutable dict** as its error accumulator, passed by reference through every API call. Errors are never raised and swallowed silently — they are recorded as `ErrorRecord` objects keyed by a string identifier (usually an absolute file path or a key name).

All error utilities live in `pydita.loggingutils`.

---

## Core types

### `SEVERITY` enum

Ordered severity levels (ascending):

```python
from pydita.loggingutils import SEVERITY

SEVERITY.OTHER   # 0 — unclassified
SEVERITY.DEBUG   # 1 — debug trace
SEVERITY.INFO    # 2 — informational
SEVERITY.ERROR   # 3 — recoverable error
SEVERITY.WARN    # 4 — warning (higher than ERROR in pydita's ordering)
SEVERITY.FATAL   # 5 — unrecoverable
```

> **Note:** In pydita's `OrderedEnum`, `WARN` (4) is *higher* than `ERROR` (3). This is intentional — WARNings are considered more severe than recoverable ERRORs.

### `ErrorRecord`

```python
from pydita.loggingutils import ErrorRecord, SEVERITY

rec = ErrorRecord(
    err=exception,          # Exception — required
    operation="myFunc()",   # str — which function caught it
    severity=SEVERITY.ERROR,
    key="file://abs/path",  # str — the dict key this belongs to
    traceBack="...",        # str — traceback.format_exc() output
)

str(rec)  # '[ERROR] "file://path" myFunc(): <exception message>'
```

---

## Recording errors

### Direct function call

```python
from pydita import loggingutils
import traceback

errors = {}

try:
    do_something()
except Exception as e:
    loggingutils.recordError(
        errors,
        key="my-operation",
        err=e,
        operation="do_something()",
        severity=loggingutils.SEVERITY.ERROR,
        traceBack=traceback.format_exc(),
    )
```

### Via `DitaContext`

```python
ctx.recordError(
    key="some-key",
    error=exception,
    operation="myProcessor()",
    severity=SEVERITY.WARN,
)
# Delegates to loggingutils.recordError(ctx.getErrors(), ...)
```

---

## Errors dict structure

```python
errors = {
    "/abs/path/to/file.ditamap": [ErrorRecord, ErrorRecord, ...],
    "key-name":                  [ErrorRecord],
}
```

- One key can have **multiple** `ErrorRecord` objects (e.g., multiple parse errors in the same file).
- The key is any string — typically a file URI, file path, or DITA key name.

---

## Reporting errors

### Full report string

```python
from pydita import loggingutils

report = loggingutils.reportErrors(errors, showTraceBack=False)
print(report)
# Have 3 total errors:
# [ERROR] "path/to/sub.ditamap" resolveSubmap(): ...
# [WARN]  "key-name" constructKeySpace(): ...
```

### Filter by severity

```python
from pydita.loggingutils import SEVERITY

fatal_errors = {
    k: [r for r in recs if r.getSeverity() >= SEVERITY.FATAL]
    for k, recs in errors.items()
    if any(r.getSeverity() >= SEVERITY.FATAL for r in recs)
}
```

### Check for any errors above a threshold

```python
def has_errors(errors: dict, min_severity=SEVERITY.ERROR) -> bool:
    return any(
        r.getSeverity() >= min_severity
        for recs in errors.values()
        for r in recs
    )
```

---

## Logging helpers

pydita provides `Logger` (abstract) and `ConsoleLogger` (concrete) for structured log output:

```python
from pydita.loggingutils import ConsoleLogger, SEVERITY

log = ConsoleLogger(logging_level=SEVERITY.WARN)
log.debug("ignored — below WARN threshold")
log.warn("printed: [WARN] printed: ...")
log.error("printed: [ERROR] ...")
log.fatal("printed: [FATAL] ...")

# Print raw message without severity prefix
log.print("Raw message output")
```

Implement a custom logger by subclassing `Logger` and overriding `_log_message()`:

```python
from pydita.loggingutils import Logger, SEVERITY

class FileLogger(Logger):
    def __init__(self, path: str):
        super().__init__(logging_level=SEVERITY.INFO)
        self._file = open(path, "w")

    def _log_message(self, message, severity: SEVERITY):
        if severity >= self.get_logging_level():
            self._file.write(f"[{severity.name}] {message}\n")
```

---

## Best practices

| Rule | Rationale |
|------|-----------|
| Create one `errors = {}` per pipeline run | Prevents cross-contamination between independent runs |
| Pass `errors` to every pydita function | Missing it silently discards errors |
| Check `errors` after `resolveMap()` and after `KeyspaceManager()` | Both can fail silently |
| Use `traceBack=traceback.format_exc()` in `except` blocks | Makes root-cause analysis much easier |
| Filter by `SEVERITY.ERROR` or higher for pass/fail decisions | `DEBUG` and `INFO` records should not count as failures |

---

## See also

- `context-setup` — how `errors` is shared across the full pipeline
- `map-resolve` — error patterns during map resolution
