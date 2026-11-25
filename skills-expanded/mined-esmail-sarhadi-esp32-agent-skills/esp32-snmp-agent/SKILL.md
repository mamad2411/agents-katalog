---
name: esp32-snmp-agent
description: Use when an ESP32 must be monitored by a network management system - Zabbix, PRTG, LibreNMS - over SNMP v2c or v3. Covers the OID tree, community strings, BER encoding and why the standard agent does not fit.
license: MIT
---

# SNMP on ESP32

SNMP is how a network management system already monitors everything else. Adding
an ESP32 to that system means implementing enough of the protocol to answer GET
and send traps.

## What the manager actually asks

| Request | Meaning |
|---|---|
| GET `1.3.6.1.2.1.1.1.0` | sysDescr, a string |
| GET `1.3.6.1.2.1.1.3.0` | sysUpTime, timeticks |
| GET `1.3.6.1.2.1.1.5.0` | sysName |
| GETNEXT | walk the tree, must return the next OID |
| GETBULK | v2c only, N results at once |

A device that answers GET but not GETNEXT will appear in a discovery scan and
then fail every inventory walk. Implement both or neither.

## v2c vs v3

- **v2c** is a community string in plaintext. Fine inside a management VLAN,
  unacceptable on a routed network.
- **v3** adds USM: authentication (MD5/SHA) and privacy (DES/AES). It is the only
  version worth shipping to a customer network, and it costs memory - the
  engine ID, boots/time counters and key localisation all need to persist across
  reboots, or the manager sees "unknown engine ID" forever.

## BER is the hard part

SNMP messages are ASN.1 BER encoded: tag, length, value, with lengths that can be
short or long form. A hand-written encoder that assumes short lengths works until
a string passes 127 bytes and then silently truncates. Use a small BER helper and
test it with a long sysDescr.

## Traps and informs

A trap is fire-and-forget to UDP 162; an inform needs an acknowledgement. For an
alarm path, informs are the ones that survive a lost packet. The trap PDU carries
the enterprise OID, the agent address and varbinds - and the sysUpTime varbind is
mandatory, which is a common reason a manager rejects the trap.

## Why not the reference agent

The net-snmp agent is far too large for an ESP32. What fits is a static OID table
with a getter per entry, a BER encoder, and a trap sender. That is a few hundred
lines and is testable on the host.

## Symptom table

| Symptom | Usually |
|---|---|
| device appears, walk fails | GETNEXT not implemented |
| "no response" from the manager | wrong community, or UDP 161 blocked |
| v3 works until reboot | engine boots/time not persisted |
| long strings truncated | BER long-form length not handled |
| traps arrive with wrong time | sysUpTime varbind missing or wrong units |
| values stale | OID table returns a cached value, not a live read |

## Agent rules

- Publish the OID table with types and units; a manager needs the MIB or the
  numeric OIDs.
- Persist the v3 engine state in NVS, including the boot counter.
- Test the BER encoder with a 200 byte string before shipping.
