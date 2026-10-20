---
name: "compliance-audit-trail"
description: "Compliance audit trail design: implement immutable audit logs, change tracking, evidence collection, regulatory reporting, and continuous compliance monitoring for SOC2, HIPAA, PCI-DSS, GDPR, and FedRAMP"
---

# Compliance Audit Trail Skill

## When to activate
- Designing audit trail systems for regulated applications
- Preparing for SOC2 Type II, HIPAA, PCI-DSS, or GDPR audits
- Implementing change tracking with tamper-evident logging
- Building evidence collection workflows for compliance frameworks
- When auditors request "show me the logs" for a specific control
- Designing continuous compliance monitoring dashboards

## When NOT to use
- General application logging (use observability-designer)
- Performance monitoring without compliance requirements
- When the audit trail system is already operational and passing audits
- Simple deployment logs without regulatory context

## Instructions

### 1. Audit Trail Architecture

```yaml
audit_trail:
  principles:
    - immutable: "Logs cannot be modified or deleted after creation"
    - complete: "Every action on regulated data is logged"
    - attributable: "Every action linked to a specific identity"
    - timestamped: "Cryptographic timestamps with NTP sync"
    - searchable: "Auditors can query by user, action, resource, time range"
    
  events:
    # Authentication events
    - type: auth.login
      capture: [user_id, ip, mfa_used, success, failure_reason]
      framework: [SOC2 CC6.1, HIPAA 164.312(d)]
      
    - type: auth.logout
      capture: [user_id, session_duration, logout_type]
      framework: [SOC2 CC6.1]
      
    # Data access events
    - type: data.read
      capture: [user_id, resource_type, resource_id, fields_accessed, justification]
      framework: [HIPAA 164.312(b), GDPR Art.30, PCI 10.2]
      
    - type: data.write
      capture: [user_id, resource_type, resource_id, changes_diff, approval_id]
      framework: [SOC2 CC8.1, HIPAA 164.312(c), PCI 10.2]
      
    - type: data.delete
      capture: [user_id, resource_type, resource_id, reason, approval_id, retention_check]
      framework: [SOC2 CC8.1, GDPR Art.17]
      
    # Administrative events
    - type: admin.role_change
      capture: [admin_id, target_user, old_roles, new_roles, justification]
      framework: [SOC2 CC6.1, HIPAA 164.308(a)(3)]
      
    - type: admin.config_change
      capture: [admin_id, setting, old_value_hash, new_value_hash, change_ticket]
      framework: [SOC2 CC8.1, PCI 10.2.7]
      
    - type: admin.system_access
      capture: [admin_id, system, access_method, duration, ticket_id]
      framework: [SOC2 CC6.3, PCI 10.2.2]
```

### 2. Immutable Logging Implementation

```python
class AuditLogger:
    """Tamper-evident audit logging."""
    
    def __init__(self, storage: AuditStorage):
        self.storage = storage
        self.chain_hash = self.storage.get_latest_hash() or "genesis"
    
    async def log(self, event: AuditEvent) -> str:
        """Write an immutable audit event."""
        # Build the event record
        record = {
            "event_id": str(uuid7()),  # time-sortable UUID
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event.type,
            "actor": {
                "user_id": event.user_id,
                "session_id": event.session_id,
                "ip_address": event.ip,
                "user_agent": event.user_agent,
            },
            "resource": {
                "type": event.resource_type,
                "id": event.resource_id,
            },
            "details": event.details,
            "metadata": {
                "request_id": event.request_id,
                "trace_id": event.trace_id,
                "framework_tags": event.framework_tags,
            },
            # Hash chain for tamper evidence
            "prev_hash": self.chain_hash,
        }
        
        # Compute hash (SHA-256 of record + previous hash)
        record["hash"] = self.compute_hash(record)
        self.chain_hash = record["hash"]
        
        # Write to immutable storage
        await self.storage.append(record)
        
        # Optionally write to secondary storage (S3 Glacier, etc.)
        await self.storage.archive(record)
        
        return record["event_id"]
    
    def verify_chain_integrity(self) -> IntegrityReport:
        """Verify the hash chain hasn't been tampered with."""
        events = self.storage.read_all()
        report = IntegrityReport()
        
        for i, event in enumerate(events):
            expected_hash = self.compute_hash(
                {**event, "hash": None}
            )
            if event["hash"] != expected_hash:
                report.add_violation(
                    event_id=event["event_id"],
                    index=i,
                    issue="hash_mismatch",
                )
            
            if i > 0 and event["prev_hash"] != events[i-1]["hash"]:
                report.add_violation(
                    event_id=event["event_id"],
                    index=i,
                    issue="chain_break",
                )
        
        return report
```

### 3. Framework-Specific Evidence Collection

```python
class EvidenceCollector:
    """Automated evidence collection for compliance frameworks."""
    
    FRAMEWORK_EVIDENCE = {
        "SOC2": {
            "CC6.1": [
                "access_control_policy",
                "user_access_reviews",
                "authentication_logs_sample",
                "mfa_enforcement_config",
            ],
            "CC7.2": [
                "vulnerability_scan_reports",
                "penetration_test_reports",
                "security_monitoring_alerts",
                "incident_response_records",
            ],
            "CC8.1": [
                "change_management_policy",
                "change_approvals_sample",
                "deployment_logs",
                "rollback_procedures",
            ],
        },
        "HIPAA": {
            "164.312(b)": ["access_audit_logs", "access_policy"],
            "164.312(c)": ["integrity_controls", "encryption_config"],
            "164.312(d)": ["authentication_methods", "mfa_config"],
            "164.312(e)": ["transit_encryption", "tls_config"],
        },
        "PCI-DSS": {
            "Req 10": [
                "audit_trail_config",
                "log_retention_policy",
                "log_integrity_verification",
                "daily_log_review_process",
            ],
        },
        "GDPR": {
            "Art.30": [
                "processing_activities_register",
                "data_access_logs",
                "consent_records",
            ],
            "Art.32": [
                "encryption_evidence",
                "access_controls",
                "breach_notification_procedures",
            ],
        },
    }
    
    async def collect(
        self,
        framework: str,
        control: str = None,
        period: DateRange = None,
    ) -> EvidencePackage:
        """Collect evidence for a specific framework and control."""
        
        evidence_items = (
            self.FRAMEWORK_EVIDENCE[framework].get(control, [])
            if control
            else [e for evidences in self.FRAMEWORK_EVIDENCE[framework].values()
                  for e in evidences]
        )
        
        package = EvidencePackage(framework=framework, period=period)
        
        for item_name in evidence_items:
            collector = self.get_collector(item_name)
            evidence = await collector.collect(period)
            package.add_evidence(
                name=item_name,
                data=evidence.data,
                format=evidence.format,  # PDF, CSV, JSON, screenshot
                hash=self.hash_evidence(evidence.data),
                collected_at=datetime.now(timezone.utc),
                collector_version=collector.version,
            )
        
        return package
```

### 4. Continuous Compliance Monitoring

```
COMPLIANCE DASHBOARD — SOC2 + HIPAA
┌──────────────────────────────────────────────────────────┐
│ CONTROL STATUS                                            │
│ ┌──────────────┬──────────┬──────────┬────────────────┐  │
│ │ Control      │ Status   │ Evidence │ Last Verified  │  │
│ ├──────────────┼──────────┼──────────┼────────────────┤  │
│ │ CC6.1 Access │ ✅ PASS  │ 12 items │ 2026-06-13     │  │
│ │ CC7.2 Monitor│ ✅ PASS  │ 8 items  │ 2026-06-12     │  │
│ │ CC8.1 Change │ ⚠️ WARN  │ 6/7 items│ 2026-06-11     │  │
│ │ HIPAA 312(b) │ ✅ PASS  │ 5 items  │ 2026-06-13     │  │
│ │ HIPAA 312(c) │ ❌ FAIL  │ 3/4 items│ 2026-06-10     │  │
│ │ PCI Req 10   │ ✅ PASS  │ 9 items  │ 2026-06-13     │  │
│ └──────────────┴──────────┴──────────┴────────────────┘  │
│                                                           │
│ ALERTS                                                    │
│ ❌ HIPAA 312(c): Encryption at rest not verified for      │
│    analytics-db-03 (new instance, not in scan scope)      │
│ ⚠️ CC8.1: 3 changes deployed without approval tickets    │
│                                                           │
│ AUDIT TRAIL HEALTH                                        │
│ Events today: 48,291 | Chain integrity: ✅ Verified       │
│ Log retention: 365 days (meets SOC2 + HIPAA)              │
│ Gaps: None detected                                       │
└──────────────────────────────────────────────────────────┘
```

### 5. Change Tracking with Approval Workflow

```python
class ChangeTracker:
    """Track all changes with approval evidence."""
    
    async def track_change(self, change: ChangeRequest):
        """Log a change with full audit context."""
        
        # Pre-change: capture current state
        before_state = await self.capture_state(change.resource)
        before_hash = self.hash_state(before_state)
        
        # Verify approval exists
        approval = await self.approval_store.get(change.approval_id)
        if not approval or approval.status != "approved":
            raise ComplianceError(
                f"Change {change.id} lacks valid approval. "
                f"Required for control CC8.1."
            )
        
        # Execute change
        result = await self.executor.execute(change)
        
        # Post-change: capture new state
        after_state = await self.capture_state(change.resource)
        after_hash = self.hash_state(after_state)
        
        # Write audit event with full context
        await self.audit_logger.log(AuditEvent(
            type="admin.config_change",
            user_id=change.executor_id,
            details={
                "change_id": change.id,
                "change_ticket": change.ticket_url,
                "approval_id": approval.id,
                "approver_id": approval.approver_id,
                "before_hash": before_hash,
                "after_hash": after_hash,
                "diff_summary": self.compute_diff(before_state, after_state),
                "rollback_procedure": change.rollback_plan,
                "test_results": change.test_results,
            },
            framework_tags=["SOC2:CC8.1", "PCI:10.2.7"],
        ))
```

### 6. Log Retention Policies

| Framework | Retention Requirement | Hot Storage | Archive |
|---|---|---|---|
| SOC2 | 1 year minimum, 3 years recommended | 90 days | S3 Glacier (3 years) |
| HIPAA | 6 years | 1 year | S3 Glacier (6 years) |
| PCI-DSS | 1 year, 3 months immediately available | 90 days | S3 Glacier (1 year) |
| GDPR | As long as necessary, with justification | 90 days | Encrypted archive |
| FedRAMP | 3 years | 1 year | GovCloud S3 (3 years) |

## Example

**Preparing for SOC2 Type II audit — evidence collection:**

```
AUDIT PREPARATION: SOC2 Type II
PERIOD: 2025-07-01 to 2026-06-30
AUDITOR: Deloitte

EVIDENCE PACKAGE:
| Control | Evidence Item | Status | Format | Items |
|---------|--------------|--------|--------|-------|
| CC6.1   | Access reviews | ✅ Ready | PDF    | 12 quarterly reviews |
| CC6.1   | MFA enforcement| ✅ Ready | Config | Screenshot + policy  |
| CC7.2   | Vuln scans     | ✅ Ready | PDF    | 12 monthly scans     |
| CC7.2   | Pen test       | ✅ Ready | PDF    | Annual pen test 2026 |
| CC8.1   | Change approvals| ⚠️ Gap | CSV    | 3 changes missing tickets |
| CC8.1   | Deploy logs    | ✅ Ready | JSON   | 847 deployments      |
| A1.1    | Availability   | ✅ Ready | Report | 99.97% uptime        |

GAPS TO RESOLVE:
  1. CC8.1: 3 changes without approval tickets → retroactive documentation needed
  2. CC7.2: April scan report missing → re-run or locate backup

AUDIT TRAIL INTEGRITY: ✅ Hash chain verified (0 violations in 847,291 events)
ESTIMATED COMPLETION: 2 days to resolve gaps
```

## Anti-Patterns

- **Mutable logs:** Logs that can be edited or deleted — use append-only + hash chains
- **Missing attribution:** "System changed config" — always capture WHO did WHAT and WHEN
- **No evidence collection:** "We comply" without proof — collect and hash evidence continuously
- **Retention gaps:** Logs expire before the audit period — align retention with framework requirements
- **Alert fatigue:** Every event triggers an alert — use risk-based alerting (anomalous patterns only)
- **Siloed audit data:** Security, infrastructure, and application logs in separate systems — unify under one audit trail
