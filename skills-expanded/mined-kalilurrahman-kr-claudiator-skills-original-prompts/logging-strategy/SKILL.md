---
name: logging-strategy
description: Design a comprehensive logging strategy for production systems. Outputs log structure, levels, retention, aggregation, and query patterns.
argument-hint: [application type, scale, compliance requirements]
allowed-tools: Read, Write, Bash
---

# Logging Strategy

Design a production-grade logging system that aids debugging, monitoring, and compliance without drowning in noise. Not "add console.log everywhere" — structured logs, smart sampling, efficient storage, and actionable queries.

## Process

1. **Define log categories.** Application logs, access logs, audit logs, error logs, security logs.
2. **Choose structure.** Structured JSON vs plain text.
3. **Set log levels.** DEBUG, INFO, WARNING, ERROR, CRITICAL — when to use each.
4. **Plan sampling.** 100% for errors, 1-10% for high-volume INFO logs.
5. **Design retention.** Hot (7-30 days), warm (90 days), cold (1 year+), compliance (7 years).
6. **Select aggregation.** ELK Stack, Splunk, Datadog, CloudWatch Logs.
7. **Define query patterns.** Common searches, dashboards, alerts.
8. **Handle sensitive data.** PII masking, credential redaction.

## Output Format

### Logging Strategy: [Application Name]

**Scale:** [requests/day, services, team size]  
**Log Volume:** [GB/day estimated]  
**Aggregation:** [ELK/Datadog/Splunk/etc.]  
**Retention:** Hot: 30 days, Warm: 90 days, Cold: 365 days  
**Compliance:** [GDPR/HIPAA/SOC2/None]

---

## Log Categories

### 1. Application Logs
**Purpose:** Track application behavior, state changes  
**Examples:** User login, order created, cache miss  
**Volume:** High (millions/day)  
**Level:** INFO, WARNING, ERROR  
**Retention:** 30 days hot, 90 days warm  

### 2. Access Logs
**Purpose:** Track HTTP requests (API, web)  
**Examples:** `GET /api/users 200 45ms`  
**Volume:** Very high (100M+/day at scale)  
**Level:** INFO  
**Sampling:** 10% for 200 responses, 100% for errors  
**Retention:** 7 days hot (due to volume)

### 3. Error Logs
**Purpose:** Track failures requiring attention  
**Examples:** Database connection failed, unhandled exception  
**Volume:** Low (should be < 0.1% of requests)  
**Level:** ERROR, CRITICAL  
**Retention:** 90 days hot, 365 days warm  
**Alerts:** > 10 errors/min triggers PagerDuty

### 4. Audit Logs
**Purpose:** Compliance, security investigations  
**Examples:** User X deleted order Y, admin accessed user Z's data  
**Volume:** Medium  
**Level:** INFO (audit events are not errors)  
**Retention:** 7 years (compliance requirement)  
**Immutable:** Cannot be deleted or modified

### 5. Security Logs
**Purpose:** Intrusion detection, suspicious activity  
**Examples:** Failed login attempts, privilege escalation  
**Volume:** Low-medium  
**Level:** WARNING, ERROR  
**Retention:** 365 days, sent to SIEM  
**Alerts:** 5 failed logins from same IP → alert

---

## Log Structure

### Structured Logging (JSON)

**Good:**
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "service": "order-service",
  "environment": "production",
  "request_id": "req_abc123",
  "user_id": "user_xyz",
  "event": "order_created",
  "order_id": "ord_12345",
  "amount": 149.99,
  "currency": "USD",
  "duration_ms": 247
}
```

**Bad:**
```
2024-01-15 10:30:00 INFO Order ord_12345 created by user_xyz for $149.99 (247ms)
```

**Why JSON?**
- Easy to parse and query
- Structured fields enable filtering (e.g., all orders > $100)
- Compatible with all log aggregation tools
- Supports nested objects

---

## Log Levels

### DEBUG
**When:** Development only, verbose output  
**Production:** Disabled (too much noise)  
**Example:** `Variable X has value Y`, `Entering function Z`

### INFO
**When:** Normal operations, state changes  
**Production:** Enabled, sampled for high volume  
**Example:** `User logged in`, `Order created`, `Cache hit`

### WARNING
**When:** Unexpected but handled situations  
**Production:** Enabled, 100% logged  
**Example:** `Retry succeeded`, `Deprecated API used`, `Slow query (>1s)`

### ERROR
**When:** Failures requiring attention  
**Production:** Enabled, 100% logged, triggers alerts  
**Example:** `Database connection failed`, `Payment declined`, `API timeout`

### CRITICAL
**When:** System-level failures  
**Production:** Enabled, immediate PagerDuty alert  
**Example:** `Out of memory`, `Disk full`, `All replicas down`

---

## Required Fields

Every log entry must include:

```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",  // ISO 8601, microsecond precision
  "level": "INFO",                           // DEBUG/INFO/WARNING/ERROR/CRITICAL
  "service": "order-service",                // Which microservice
  "environment": "production",               // prod/staging/dev
  "request_id": "req_abc123",                // Correlation ID
  "event": "order_created"                   // What happened (snake_case)
}
```

Optional but recommended:
```json
{
  "user_id": "user_xyz",        // If user action
  "session_id": "sess_789",     // If session-based
  "ip_address": "192.168.1.1",  // Client IP (hash for GDPR)
  "duration_ms": 247,           // Operation duration
  "error_code": "DB_TIMEOUT",   // If error
  "stack_trace": "...",         // If error (truncate to 1000 chars)
}
```

---

## Sampling Strategy

### High-Volume Endpoints
```
Problem: /api/health checked 1000x/min = 1.4M logs/day

Solution: Sample 1% of successful health checks
```

**Implementation:**
```python
import random

if endpoint == "/health" and status == 200:
    if random.random() < 0.01:  # 1% sampling
        logger.info("health_check_ok")
else:
    logger.info(f"{endpoint}_accessed", status=status)
```

### Errors: Always 100%
```python
if status >= 500:
    logger.error("server_error", status=status, path=path)
# No sampling for errors
```

### Based on Request ID
```python
# Consistent sampling: Same request_id always logged or never logged
if int(request_id[-2:], 16) < 256 * 0.1:  # 10% sample
    logger.info("request_processed", ...)
```

---

## Log Aggregation Architecture

### Option 1: ELK Stack (Self-Hosted)

**Components:**
- **Elasticsearch:** Log storage and search
- **Logstash:** Log parsing and enrichment
- **Kibana:** Dashboards and queries
- **Filebeat:** Log shipping from servers

**Flow:**
```
Application → JSON to stdout → Filebeat → Logstash → Elasticsearch → Kibana
```

**Pros:** Full control, no per-GB pricing  
**Cons:** Operational overhead, scaling complexity

---

### Option 2: Datadog (SaaS)

**Components:**
- Datadog Agent on each server
- Auto-parsing of JSON logs
- Built-in dashboards and alerts

**Flow:**
```
Application → JSON to stdout → Datadog Agent → Datadog Cloud
```

**Pros:** Managed, excellent UI, APM integration  
**Cons:** $0.10/GB ingested + retention costs

---

### Option 3: AWS CloudWatch Logs

**Components:**
- CloudWatch Logs Agent
- Log Groups (per service)
- CloudWatch Insights for queries

**Flow:**
```
Application → JSON to stdout → CloudWatch Agent → CloudWatch Logs
```

**Pros:** Native AWS integration, cheap  
**Cons:** Query UI limited, slow for large datasets

---

## Retention Strategy

### Hot Storage (7-30 days)
- **Purpose:** Active debugging, recent incident investigation
- **Storage:** Elasticsearch, Datadog, CloudWatch
- **Cost:** High ($0.10/GB/month)
- **Access:** Fast queries (< 1s)

### Warm Storage (90 days)
- **Purpose:** Historical analysis, compliance
- **Storage:** S3 Standard, compressed JSON
- **Cost:** Medium ($0.023/GB/month)
- **Access:** Slower queries (10-60s via Athena)

### Cold Storage (1+ years)
- **Purpose:** Compliance, legal holds
- **Storage:** S3 Glacier
- **Cost:** Low ($0.004/GB/month)
- **Access:** Retrieval takes hours

### Example Lifecycle
```
Day 0-30:   Elasticsearch (hot)
Day 31-90:  S3 Standard (warm)
Day 91+:    S3 Glacier (cold)
Day 365+:   Delete (unless compliance requires longer)
```

---

## Common Query Patterns

### Find all errors for a specific user
```
{
  "query": {
    "bool": {
      "must": [
        {"term": {"user_id": "user_xyz"}},
        {"range": {"level": {"gte": "ERROR"}}}
      ]
    }
  }
}
```

### Trace a request across services
```
{
  "query": {
    "term": {"request_id": "req_abc123"}
  },
  "sort": [{"timestamp": "asc"}]
}
```

### Find slow database queries
```
{
  "query": {
    "bool": {
      "must": [
        {"term": {"event": "database_query"}},
        {"range": {"duration_ms": {"gte": 1000}}}
      ]
    }
  }
}
```

### Count error types
```
{
  "aggs": {
    "error_types": {
      "terms": {"field": "error_code"}
    }
  }
}
```

---

## Sensitive Data Handling

### PII Masking

**Before:**
```json
{
  "event": "user_created",
  "email": "john.doe@example.com",
  "phone": "+1-555-123-4567",
  "ssn": "123-45-6789"
}
```

**After:**
```json
{
  "event": "user_created",
  "email_hash": "5d41402abc4b2a76b9719d911017c592",
  "phone_hash": "e99a18c428cb38d5f260853678922e03",
  "ssn": "[REDACTED]"
}
```

### Auto-Redaction (Python)
```python
import hashlib
import re

SENSITIVE_FIELDS = ['email', 'phone', 'ssn', 'credit_card']

def sanitize_log(data):
    for field in SENSITIVE_FIELDS:
        if field in data:
            if field == 'ssn':
                data[field] = '[REDACTED]'
            else:
                data[f"{field}_hash"] = hashlib.md5(data[field].encode()).hexdigest()
                del data[field]
    return data

logger.info("user_created", **sanitize_log(user_data))
```

---

## Performance Considerations

### Avoid Blocking on Log Write
```python
# Bad: Synchronous logging blocks request
logger.info("order_created", order_id=order.id)  # Waits for I/O

# Good: Async logging
import logging.handlers
handler = logging.handlers.QueueHandler(queue)
logger.addHandler(handler)
```

### Batch Log Shipping
```
Ship logs every 10s or 1000 logs (whichever first)
Reduces network overhead
```

### Compress Logs
```
gzip JSON logs before sending to S3
Reduces storage cost by 70-90%
```

---

## Monitoring Log System Health

### Metrics to Track
- `logs_ingested_per_second` — Is log volume normal?
- `log_shipping_lag` — Are logs arriving delayed?
- `log_parse_errors` — Are logs malformed?
- `elasticsearch_disk_usage` — Running out of space?

### Alerts
- Log ingestion drops by 50% → Service might be down
- Log shipping lag > 5 minutes → Investigate backlog
- Elasticsearch disk > 80% → Add capacity or increase retention

---

## Testing Logging

### Unit Tests
```python
def test_logging_structure(caplog):
    logger.info("test_event", user_id="123")
    
    log = json.loads(caplog.records[0].getMessage())
    assert log["event"] == "test_event"
    assert log["user_id"] == "123"
    assert "timestamp" in log
    assert "level" in log
```

### Load Testing
```
Simulate 10,000 requests/sec
Verify log system handles load without dropping logs
```

---

## Best Practices

### DO:
- Log in JSON format
- Include request_id in every log
- Log errors with full context (stack trace, inputs)
- Sample high-volume INFO logs
- Aggregate logs centrally
- Set up alerts on error rate spikes
- Redact sensitive data automatically

### DON'T:
- Log passwords, tokens, API keys
- Log full request/response bodies (too large)
- Use string interpolation (use structured fields)
- Log in loops (creates log spam)
- Block requests waiting for log writes
- Keep all logs forever (cost)

## Rules

- Every log entry must be valid JSON with timestamp, level, service, event fields.
- Error logs (ERROR, CRITICAL) must be 100% retained, never sampled.
- Logs containing PII must be hashed or redacted before storage (GDPR compliance).
- Request tracing requires correlation ID (request_id) in every log entry.
- Log retention must balance cost and compliance: 30 days hot is usually sufficient for debugging.
- High-volume endpoints (> 100 req/s) must use sampling (1-10%) for INFO logs.
- Log aggregation must be centralized — no SSHing into servers to read logs.
- Stack traces must be truncated to 1000 characters to avoid log bloat.
- Log levels must be consistent: INFO for normal operations, ERROR for failures, never use ERROR for expected behavior.
- If log volume exceeds 100 GB/day, evaluate sampling strategy and retention policy — storage costs will be significant.
