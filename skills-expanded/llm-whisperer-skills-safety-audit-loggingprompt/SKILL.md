# Audit Logging and Compliance for AI Systems

## Overview

Audit logging for LLM systems provides a comprehensive record of all system activities, model interactions, and decision-making processes. Proper audit logging is essential for security investigations, compliance requirements (GDPR, SOC 2, HIPAA), model governance, and debugging production issues. LLM-specific audit requirements include logging prompt-response pairs, model versions, tool invocations, and safety interventions.

This skill covers implementing production-grade audit logging systems that meet compliance requirements while maintaining performance and managing storage costs.

## Key Concepts

- **Structured logging**: Use consistent, machine-readable log formats (JSON) with required fields
- **Log levels**: Distinguish between debug, info, warning, error, and security-critical events
- **Retention policies**: Define how long logs are kept based on compliance requirements
- **PII handling**: Detect and redact personally identifiable information from logs
- **Log integrity**: Ensure logs cannot be tampered with after creation
- **Compliance mapping**: Map log fields to specific compliance requirements (GDPR Article 30, SOC 2 CC7)
- **Correlation IDs**: Track requests across distributed systems using unique identifiers
- **Alerting**: Automated alerts for security events and compliance violations

## Implementation Patterns

### Structured Audit Logger

```python
import json
import hashlib
import uuid
from datetime import datetime
from typing import Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SECURITY = "security"

class AuditEvent(Enum):
    # Authentication
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"

    # Model interactions
    INFERENCE_REQUEST = "inference_request"
    INFERENCE_RESPONSE = "inference_response"
    MODEL_LOADED = "model_loaded"
    MODEL_UNLOADED = "model_unloaded"

    # Safety
    SAFETY_VIOLATION = "safety_violation"
    CONTENT_FILTERED = "content_filtered"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    JAILBREAK_ATTEMPT = "jailbreak_attempt"

    # Data
    DATA_ACCESS = "data_access"
    DATA_MODIFIED = "data_modified"
    DATA_EXPORTED = "data_exported"

    # Administrative
    CONFIG_CHANGED = "config_changed"
    USER_CREATED = "user_created"
    PERMISSION_CHANGED = "permission_changed"

class AuditLogger:
    def __init__(self, service_name: str, log_path: str = "audit.jsonl",
                 enable_pii_detection: bool = True):
        self.service = service_name
        self.log_path = log_path
        self.pii_detection = enable_pii_detection
        self.buffer: list[str] = []
        self.buffer_size = 100

    def log(self, event: AuditEvent, actor: str, resource: str = None,
            details: dict = None, level: LogLevel = LogLevel.INFO,
            correlation_id: str = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service,
            "event": event.value,
            "level": level.value,
            "actor": actor,
            "resource": resource,
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "details": details or {},
            "integrity_hash": None,  # Set below
        }

        # Compute integrity hash
        entry["integrity_hash"] = self._compute_hash(entry)

        # PII redaction
        if self.pii_detection:
            entry = self._redact_pii(entry)

        log_line = json.dumps(entry)
        self.buffer.append(log_line)

        if len(self.buffer) >= self.buffer_size:
            self._flush()

    def log_inference(self, user_id: str, model: str, prompt: str,
                      response: str, tokens_used: int, latency_ms: float,
                      correlation_id: str = None):
        self.log(
            event=AuditEvent.INFERENCE_REQUEST,
            actor=user_id,
            resource=f"model:{model}",
            details={
                "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                "prompt_length": len(prompt),
                "response_length": len(response),
                "tokens_used": tokens_used,
                "latency_ms": latency_ms,
                "model": model,
            },
            correlation_id=correlation_id,
        )

    def log_safety_event(self, event: AuditEvent, user_id: str,
                         threat_level: str, reason: str,
                         prompt_hash: str = None):
        self.log(
            event=event,
            actor=user_id,
            details={
                "threat_level": threat_level,
                "reason": reason,
                "prompt_hash": prompt_hash,
            },
            level=LogLevel.SECURITY,
        )

    def _compute_hash(self, entry: dict) -> str:
        # Exclude the hash field itself
        hashable = {k: v for k, v in entry.items() if k != "integrity_hash"}
        return hashlib.sha256(json.dumps(hashable, sort_keys=True).encode()).hexdigest()

    def _redact_pii(self, entry: dict) -> dict:
        import re
        text = json.dumps(entry)
        # Redact emails
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED_EMAIL]', text)
        # Redact phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[REDACTED_PHONE]', text)
        # Redact SSN patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', text)
        return json.loads(text)

    def _flush(self):
        with open(self.log_path, "a") as f:
            for line in self.buffer:
                f.write(line + "\n")
        self.buffer.clear()
```

### Compliance Reporter

```python
class ComplianceReporter:
    """Generates compliance reports from audit logs."""

    def __init__(self, log_path: str):
        self.log_path = log_path

    def generate_gdpr_report(self, start_date: str, end_date: str) -> dict:
        """Generate GDPR Article 30 compliance report."""
        logs = self._load_logs(start_date, end_date)

        data_access_events = [l for l in logs if l["event"] == "data_access"]
        data_export_events = [l for l in logs if l["event"] == "data_exported"]
        safety_events = [l for l in logs if l["level"] == "security"]

        return {
            "report_type": "GDPR_Article_30",
            "period": {"start": start_date, "end": end_date},
            "summary": {
                "total_events": len(logs),
                "data_access_events": len(data_access_events),
                "data_export_events": len(data_export_events),
                "security_events": len(safety_events),
                "unique_actors": len(set(l["actor"] for l in logs)),
            },
            "data_processing_activities": {
                "inference_requests": len([l for l in logs if l["event"] == "inference_request"]),
                "pii_redactions_applied": len([l for l in logs if "[REDACTED" in json.dumps(l)]),
            },
            "security_incidents": safety_events[:50],
        }

    def generate_soc2_report(self, start_date: str, end_date: str) -> dict:
        """Generate SOC 2 compliance evidence."""
        logs = self._load_logs(start_date, end_date)

        return {
            "report_type": "SOC2_CC7",
            "period": {"start": start_date, "end": end_date},
            "controls": {
                "CC7.1_detection": {
                    "security_events_detected": len([l for l in logs if l["level"] == "security"]),
                    "failed_logins": len([l for l in logs if l["event"] == "login_failure"]),
                    "rate_limit_events": len([l for l in logs if l["event"] == "rate_limit_exceeded"]),
                },
                "CC7.2_monitoring": {
                    "total_logged_events": len(logs),
                    "log_integrity": self._verify_integrity(logs),
                },
                "CC7.3_response": {
                    "safety_violations": len([l for l in logs if l["event"] == "safety_violation"]),
                    "content_filtered": len([l for l in logs if l["event"] == "content_filtered"]),
                },
            },
        }

    def _load_logs(self, start_date: str, end_date: str) -> list[dict]:
        logs = []
        try:
            with open(self.log_path) as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if start_date <= entry.get("timestamp", "") <= end_date:
                        logs.append(entry)
        except FileNotFoundError:
            pass
        return logs

    def _verify_integrity(self, logs: list[dict]) -> dict:
        valid = 0
        invalid = 0
        for log in logs:
            stored_hash = log.get("integrity_hash")
            log_copy = {k: v for k, v in log.items() if k != "integrity_hash"}
            computed = hashlib.sha256(json.dumps(log_copy, sort_keys=True).encode()).hexdigest()
            if stored_hash == computed:
                valid += 1
            else:
                invalid += 1

        return {
            "total_checked": valid + invalid,
            "valid": valid,
            "invalid": invalid,
            "integrity_rate": round(valid / max(valid + invalid, 1), 4),
        }
```

### Retention Policy Manager

```python
from datetime import datetime, timedelta

class RetentionPolicy:
    def __init__(self):
        self.policies: dict[str, timedelta] = {
            "debug": timedelta(days=7),
            "info": timedelta(days=90),
            "warning": timedelta(days=365),
            "error": timedelta(days=365),
            "security": timedelta(days=2555),  # 7 years for compliance
        }

    def should_retain(self, log_entry: dict) -> bool:
        level = log_entry.get("level", "info")
        timestamp = datetime.fromisoformat(log_entry.get("timestamp", ""))
        retention = self.policies.get(level, timedelta(days=90))
        return datetime.utcnow() - timestamp < retention

    def cleanup(self, log_path: str):
        """Remove logs that exceed retention policy."""
        retained = []
        removed = 0

        with open(log_path) as f:
            for line in f:
                entry = json.loads(line.strip())
                if self.should_retain(entry):
                    retained.append(line)
                else:
                    removed += 1

        with open(log_path, "w") as f:
            f.writelines(retained)

        return {"retained": len(retained), "removed": removed}
```

### Alert System

```python
class AuditAlertSystem:
    """Generates alerts for security and compliance events."""

    def __init__(self):
        self.alert_rules: list[dict] = []
        self.alert_history: list[dict] = []

    def add_rule(self, name: str, condition: dict, severity: str,
                 notification_channels: list[str]):
        self.alert_rules.append({
            "name": name,
            "condition": condition,
            "severity": severity,
            "channels": notification_channels,
        })

    def evaluate_log(self, log_entry: dict) -> list[dict]:
        alerts = []
        for rule in self.alert_rules:
            if self._matches_condition(log_entry, rule["condition"]):
                alert = {
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "log_entry": log_entry,
                    "timestamp": datetime.now().isoformat(),
                    "channels": rule["channels"],
                }
                alerts.append(alert)
                self.alert_history.append(alert)
        return alerts

    def _matches_condition(self, entry: dict, condition: dict) -> bool:
        for key, expected in condition.items():
            if key == "event" and entry.get("event") != expected:
                return False
            if key == "level" and entry.get("level") != expected:
                return False
            if key == "min_count_per_hour":
                # Check frequency
                recent = [a for a in self.alert_history
                         if a.get("log_entry", {}).get("event") == entry.get("event")
                         and (datetime.now() - datetime.fromisoformat(a["timestamp"])).seconds < 3600]
                if len(recent) < expected:
                    return False
        return True
```

## Best Practices

1. Use structured JSON logging with consistent field names across all services
2. Include correlation IDs to track requests across distributed systems
3. Log all security-relevant events: authentication, authorization, safety interventions, data access
4. Implement PII detection and redaction in the logging pipeline
5. Use integrity hashing to detect log tampering
6. Define retention policies based on compliance requirements (GDPR, SOC 2, HIPAA)
7. Set up automated alerts for security events and anomalies
8. Generate compliance reports automatically on schedule
9. Store logs in append-only storage to prevent modification
10. Test audit logging as part of your CI/CD pipeline

## Common Pitfalls

- Logging sensitive data without redaction — violates privacy regulations
- Not including enough context in logs — makes debugging and investigation difficult
- Missing security event logging — creates blind spots for incident response
- Not verifying log integrity — tampered logs undermine the entire audit system
- Storing logs indefinitely without retention policies — creates compliance risk
- Not testing log completeness — important events may be silently dropped
- Logging too verbosely — excessive logging increases costs and reduces signal-to-noise
- Not correlating logs across services — makes distributed debugging impossible

## References

- GDPR Article 30: Records of Processing Activities
- SOC 2 Trust Services Criteria CC7
- HIPAA Audit Log Requirements
- OWASP Logging Cheat Sheet
