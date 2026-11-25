---
name: dn-decompile
description: Decompile .NET assembly. Trigger: decompile .net, c# source, ilspy, dotpeek, managed code.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\dnspy\dnSpy.exe
x-alice-class: reverse
---# dn-decompile

## Trigger
`decompile `

## Flow
```
dnSpy open -> expand assembly -> output C# source
```

## Script
`scripts/dn_decompile.py`
