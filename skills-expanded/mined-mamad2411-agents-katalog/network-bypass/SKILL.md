---
name: network-bypass
description: Intercept network-based verification. Trigger: network verify, online check, http auth, server auth, hosts redirect.
tool: Frida + hosts
x-alice-class: crack
---# network-bypass

## Trigger
`network verify, online check, http auth, server auth, hosts redirect`

## Flow
```
identify endpoint -> A) hosts B) local server C) Frida hook -> output bypass
```

## Script
`scripts/network_bypass.py`
