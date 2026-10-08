---
description: WAAMTO Monitoring Rules v3.0
alwaysApply: true
---
# WAAMTO Monitoring Rules v3.0

> Monitoring-specific development and QA rules.

---

# Purpose

Maintain accurate, reliable and low-overhead monitoring across the WAAMTO ecosystem.

Monitoring should provide visibility, not introduce instability.

---

# Scope

Monitoring may include:

- Server health
- Application health
- API health
- Database health
- Queue & worker health
- Storage
- Background jobs
- License Engine connectivity
- ERP instance status
- Tenant status
- Alerts
- Metrics
- Logs

Only modify the monitoring areas relevant to the task.

---

# Architecture

Keep monitoring independent from business logic.

Monitoring should observe systems, not control business workflows unless explicitly designed to do so.

---

# Health Checks

Health endpoints should be:

- lightweight
- reliable
- fast
- consistent

Avoid expensive operations inside health checks.

---

# Metrics

Reuse existing metrics whenever possible.

Only add new metrics when they provide meaningful operational value.

Avoid collecting unnecessary data.

---

# Alerts

Create alerts only for meaningful operational events.

Avoid excessive or duplicate notifications.

---

# Logging

Logs should help diagnose issues.

Log:

- errors
- warnings
- important operational events

Avoid excessive debug logging in production.

Never log secrets or sensitive information.

---

# Performance

Monitoring must have minimal impact on:

- API response time
- database performance
- application resources

Avoid unnecessary polling or expensive background tasks.

---

# Security

Protect monitoring endpoints appropriately.

Do not expose sensitive operational data to unauthorized users.

Respect existing authentication and authorization rules.

---

# Integrations

Maintain compatibility with:

- ERP
- License Engine
- Website
- Documentation
- Notification systems

Do not break existing monitoring integrations.

---

# Testing

Validate reasonably affected areas, including:

- health endpoints
- metrics
- alerts
- logs
- integrations
- dashboards (where applicable)

Test likely regression paths.

---

# Reporting

Include:

- scope
- components affected
- validation performed
- issues found
- operational impact

Keep reports concise.

---

# Completion Checklist

âœ“ Health checks verified

âœ“ Metrics validated

âœ“ Alerts reviewed

âœ“ Logging preserved

âœ“ Security maintained

âœ“ Performance acceptable

âœ“ Validation completed

If complete:

STOP.
