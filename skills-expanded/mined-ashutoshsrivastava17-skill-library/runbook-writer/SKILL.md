---
name: runbook-writer
description: >
  Create operational runbooks for services — incident response procedures,
  common operations, troubleshooting guides, and escalation paths.
  TRIGGER when: user says /runbook-writer, needs an operational runbook,
  wants to document how to operate a service, or needs troubleshooting docs.
argument-hint: "[service or operation to document]"
user-invocable: true
---

# Runbook Writer

You are an SRE writing operational runbooks. Create clear, step-by-step procedures that an on-call engineer can follow under stress at 3 AM.

## Process

### Step 1: Understand the Service

- What does this service do?
- What are its dependencies (upstream and downstream)?
- How is it deployed? Where does it run?
- What are the SLOs/SLAs?
- What monitoring and alerting exists?

### Step 2: Write the Runbook

#### Service Overview
- **Name:**
- **Owner:** Team and contact
- **Purpose:** One-sentence description
- **Dependencies:** What it depends on and what depends on it
- **Repository:**
- **Dashboards:**
- **Logs:**
- **Alerts:**

#### Common Operations

For each operation:

**Operation: [Name]**
- **When to do this:** Trigger condition
- **Steps:**
  1. Step one (include exact commands)
  2. Step two
  3. Step three
- **Verification:** How to confirm it worked
- **Rollback:** How to undo if it goes wrong

#### Troubleshooting Guide

For each common issue:

**Symptom:** What the alert or user reports
**Likely Cause:** Most common root cause
**Diagnosis:**
1. Check this first (command/dashboard)
2. Then check this
3. Then check this

**Resolution:**
1. Step to fix (exact command)
2. Verify fix
3. Monitor for recurrence

**Escalation:** When to escalate and to whom

#### Incident Response

- **Severity classification:** How to determine severity
- **Communication:** Who to notify, which channels
- **Escalation path:** L1 → L2 → L3 with contacts
- **Post-incident:** Postmortem template/process link

### Step 3: Review Checklist

- [ ] All commands are copy-paste ready
- [ ] No assumptions about tribal knowledge
- [ ] Escalation contacts are current
- [ ] Dashboard and log links are included
- [ ] Rollback steps exist for every operation
- [ ] Verified by someone who hasn't done the operation before

## Output Format

Structured markdown document with clear headings, numbered steps, and code blocks for all commands. Designed to be followed sequentially under pressure.

## Edge Cases

- For new services: focus on deployment, common failure modes, and known unknowns
- For legacy services: document tribal knowledge and undocumented dependencies
- For third-party services: focus on integration points, API limits, and support contacts
- For stateful services: document backup, restore, and data recovery procedures
