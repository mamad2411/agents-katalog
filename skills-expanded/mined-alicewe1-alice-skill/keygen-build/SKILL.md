---
name: keygen-build
description: Reverse algorithm and build credential generator. Trigger: keygen, serial, generate key, algorithm reverse, credential.
tool: Python
x-alice-class: crack
---# keygen-build

## Trigger
`keygen, serial, generate key, algorithm reverse, credential`

## Flow
```
Ghidra extract algorithm -> Python keygen -> test against original
```

## Script
`scripts/keygen_build.py`
