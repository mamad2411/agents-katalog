---
name: swpilotcli-diagnose-ic-rigidity
description: Diagnose whether candidate sketch points belong to the same rigid body in the active SolidWorks sketch. Compares point movement and pairwise distances between two nearby dimension states. Use before computing IC when you need to verify that your tracked points are valid on the same body.
---

# swpilotcli-diagnose-ic-rigidity

Check whether candidate points stay rigid together across a small dimension change.

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-diagnose-ic-rigidity/scripts/DiagnoseIcRigidity/DiagnoseIcRigidity.csproj
```
