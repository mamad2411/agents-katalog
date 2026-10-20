---
name: hunting-wmi-event-subscription-persistence
description: 'Hunts for malicious WMI permanent event subscription persistence by correlating
  __EventFilter, CommandLineEventConsumer/ActiveScriptEventConsumer, and FilterToConsumerBinding
  records from Sysmon Event IDs 19/20/21 or WMI repository exports. Activates for requests to hunt
  WMI persistence, detect event consumer backdoors, or analyze WMI subscription telemetry.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - wmi
  - persistence
  - sysmon
  - event-subscription
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1546.003
  - T1047
  - T1059
d3fend:
  - D3-PSA
  - D3-SYSM
car:
  - CAR-2014-12-001
references:
  - 'MITRE ATT&CK T1546.003 WMI Event Subscription — https://attack.mitre.org/techniques/T1546/003/'
  - 'Sysmon WMI events (19/20/21) — https://learn.microsoft.com/sysinternals/downloads/sysmon'
---

# Hunting WMI Event Subscription Persistence

## When to Use

- You have Sysmon WMI telemetry (Event ID 19 filter, 20 consumer, 21 binding) or a WMI repository
  export and want to find malicious permanent event subscriptions.
- You are investigating fileless persistence that survives reboots via WMI.

**Do not use** this for transient WMI process calls (T1047 execution) — this targets persistent
__EventFilter/__EventConsumer subscriptions specifically.

## Prerequisites

- Sysmon EID 19/20/21 events (CSV/JSON) or an exported subscription listing.

## Workflow

### Step 1: Parse and correlate triad records

```bash
python scripts/analyst.py hunt wmi_events.csv
```

Groups filters, consumers, and bindings, and flags consumers whose payload is suspicious
(`CommandLineEventConsumer` running scripts/encoded commands, `ActiveScriptEventConsumer` with
inline VBScript/JScript).

### Step 2: Assess the trigger

Inspect the `__EventFilter` query — common malicious triggers fire on logon, time intervals
(`__InstanceModificationEvent within`), or process start.

### Step 3: Confirm maliciousness

Legitimate management subscriptions exist; weight inline scripts, encoded commands, and unusual
consumer names.

### Step 4: Operationalize

Write a Sigma/EDR rule for new ActiveScript/CommandLine consumers.

## Validation

- Filter, consumer, and binding are correlated into a complete subscription where possible.
- Suspicious consumers are flagged by payload content, not consumer existence alone.
- Findings map to ATT&CK T1546.003.

## Pitfalls

- Legitimate monitoring tools (SCCM, antivirus) create subscriptions — corroborate.
- Missing the binding that links an otherwise-benign-looking filter and consumer.
- Encoded PowerShell inside a consumer obscuring intent.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the hunter.
- ATT&CK T1546.003 and Sysmon WMI events (linked in frontmatter).
