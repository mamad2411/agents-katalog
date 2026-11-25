---
name: dotnet-bypass
description: Bypass .NET authorization. Trigger: dotnet auth, .net license, unity license, mono bypass.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\dnspy\dnSpy.exe
x-alice-class: crack
---# dotnet-bypass

## Trigger
`dotnet auth, `

## Flow
```
dnSpy open -> find auth class -> edit IL -> save module
```

## Script
`scripts/dotnet_bypass.py`
