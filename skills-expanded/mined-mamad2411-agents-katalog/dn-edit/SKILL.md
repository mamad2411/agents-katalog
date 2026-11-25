---
name: dn-edit
description: Edit IL in .NET assembly. Trigger: edit il, modify il, il code, opcode, msil edit.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\dnspy\dnSpy.exe
x-alice-class: reverse
---# dn-edit

## Trigger
`edit il, modify il, il code, opcode, msil edit`

## Flow
```
dnSpy -> right-click -> Edit Method (IL) -> output original + patched IL
```

## Script
`scripts/dn_edit.py`
