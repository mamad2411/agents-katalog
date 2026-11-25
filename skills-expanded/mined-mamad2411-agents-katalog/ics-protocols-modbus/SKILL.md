---
name: ics-protocols-modbus
description: "Ics Ics Protocols Modbus."
domain: cybersecurity
---

|
| Modbus TCP | Industrial protocol operating on TCP port 502, lacking authentication or encryption, making it vulnerable to command injection |
| Function Code | Single byte in Modbus PDU specifying the operation (read coils, write registers, diagnostics); monitoring for unauthorized function codes is key to detection |
| MBAP Header | Modbus Application Protocol header in TCP variant containing transaction ID, protocol ID, length, and unit ID |
| FrostyGoop | First known malware using Modbus TCP for real-world operational impact, disrupted Ukrainian district heating in 2024 |
| Unit ID | Address of the target Modbus slave device; Unit ID 0 is a broadcast affecting all slaves |
| Register Range | Specific memory addresses in the PLC; legitimate operations access known ranges; out-of-range access indicates reconnaissance or manipulation |

## Common Scenarios

### Scenario: FrostyGoop-Style Heating Control Attack

**Context**: A building automation system uses Modbus TCP to control HVAC equipment. Monitoring detects unexpected write commands to heating control registers from an IP not associated with any authorized BMS controller.

**Approach**:
1. Verify the source IP against the authorized Modbus master list
2. Check if any authorized maintenance or configuration change is in progress
3. Capture full Modbus transaction including register addresses and values being written
4. Compare written values against safe operating ranges for the heating equipment
5. If unauthorized, immediately block the source IP at the industrial firewall
6. Inspect the source device for compromise indicators (malware, unauthorized remote access)
7. Verify current setpoints on all affected controllers against known-good values
8. Restore safe setpoints if manipulation is confirmed

**Pitfalls**: Modbus lacks authentication, so the source IP is the only identifier -- attackers can spoof IPs if ARP protections are not in place. Do not assume all writes are malicious; legitimate SCADA operations include writes. Always verify against the change management log before escalating.

## Output Format

```
MODBUS INJECTION DETECTION REPORT
====================================
Analysis Period: [start] to [end]
Monitoring Point: [interface/SPAN description]

TRAFFIC SUMMARY:
  Total Modbus Packets: [count]
  Read Operations: [count]
  Write Operations: [count]
  Unauthorized Writes Detected: [count]

ALERTS:
  [CRITICAL] Unauthorized write from [IP] to PLC [IP]
    Function: Write Multiple Registers (FC 16)
    Registers: [start]-[end]
    MITRE: T0855 - Unauthorized Command Message

BASELINE DEVIATIONS:
  New Modbus masters: [list]
  Unusual function codes: [list]
  Out-of-range register access: [list]

RECOMMENDED ACTIONS:
  1. Verify source [IP] authorization status
  2. Block unauthorized sources at industrial firewall
  3. Validate PLC register values against known-good state
```
