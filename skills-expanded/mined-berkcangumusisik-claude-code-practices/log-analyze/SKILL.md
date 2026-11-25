---
name: log-analyze
description: Analyzes log output or a log file to find errors, patterns, and anomalies
argument-hint: [log-file-path]
user-invocable: true
allowed-tools: Bash Read
effort: low
---

## Log Analysis

Source: **$1** (or read from stdin if not specified)

```bash
# If file provided
cat "$1" 2>/dev/null | tail -500

# Or last N lines of common log locations
tail -200 logs/app.log 2>/dev/null || journalctl -n 200 2>/dev/null
```

Analyze for:

### Errors & Exceptions
- Stack traces and their frequency
- Error codes and HTTP status patterns
- Repeated errors (same error > 3x = systemic issue)

### Performance Signals
- Slow requests (response time > 1s)
- Timeout patterns
- Memory/CPU warnings

### Anomalies
- Sudden spike in error rate
- Unusual request patterns (potential abuse)
- Auth failures in bulk

### Timeline
- When did errors start?
- Correlation with deployments or traffic spikes?

---

Produce a concise summary:
- **Root cause hypothesis** (most likely reason for issues)
- **Immediate action** (if critical)
- **Lines to investigate** (with context)
