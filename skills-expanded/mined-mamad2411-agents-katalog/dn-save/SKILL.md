---
name: dn-save
description: Save modified .NET assembly. Trigger: save module, write assembly, compile .net, output dll.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\dnspy\dnSpy.exe
x-alice-class: reverse
---# dn-save

## Trigger
`save module, write assembly, compile `

## Flow
```
dnSpy -> File -> Save Module -> verify
```

## Script
`scripts/dn_save.py`
