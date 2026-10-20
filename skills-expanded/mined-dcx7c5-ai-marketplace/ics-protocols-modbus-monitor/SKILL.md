---
name: ics-protocols-modbus-monitor
description: "indicators. Block FC 43 from non-engineering subnets at OT firewall."
domain: cybersecurity
---

### Alert 2: Device Enumeration Detected

**Timestamp**: 2026-03-15 14:20:05 to 14:20:47 UTC
**Severity**: HIGH
**Source**: 10.1.2.20
**Targets**: 10.1.1.50, 10.1.1.51, 10.1.1.52, 10.1.1.53, 10.1.1.54 (+10 more)
**Function Code**: 43 (Read Device Identification)
**Baseline**: FC 43 never observed from this source

**Context**: Sequential scanning of 15 devices in 42 seconds. Device
identification responses reveal PLC vendor, model, and firmware versions
for all scanned devices.

**Recommended Action**: Investigate source workstation for compromise
indicators. Block FC 43 from non-engineering subnets at OT firewall.
```
