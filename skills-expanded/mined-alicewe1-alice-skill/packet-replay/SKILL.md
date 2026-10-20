---
name: packet-replay
description: Replay and modify network packets. Trigger: replay, resend, forge packet, spoof, modify packet, craft packet.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\network_analyzer.py
x-alice-class: pentest
---# packet-replay

## Trigger
`replay, resend, forge packet, spoof, modify packet, craft packet`

## Flow
```
network_analyzer.py analyze -> output Python replay script
```

## Script
`scripts/packet_replay.py`
