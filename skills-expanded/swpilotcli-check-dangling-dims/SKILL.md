---
name: swpilotcli-check-dangling-dims
description: Scan all dimensions in the active SolidWorks drawing and report which ones are dangling (unattached). Lists every dimension with its type, value, and name, marking dangling ones with [!]. Outputs a summary count at the end. Use before running a repair tool, for QC checks before release, or whenever you need to know if a drawing has dangling annotations.
---

# SolidWorks Check Dangling Dimensions

Scan every dimension in the active drawing and report dangling status.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- An active `.slddrw` drawing document open in SolidWorks

## What this Skill does

1. Iterates all sheets and views in the active drawing
2. For each `DisplayDimension` annotation, checks `IAnnotation.IsDangling()`
3. Prints every dimension with view name, type, value, full name, and OK / DANGLING status
4. Prints a summary: total dimension count, dangling count, and a list of all dangling dimensions

## When to use

- **Before repair**: confirm how many dangling dimensions exist before running RepairDanglingAI
- **After repair**: verify the drawing is clean
- **QC / release check**: ensure a drawing has no dangling annotations before issuing

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-check-dangling-dims/scripts/CheckDanglingDims/CheckDanglingDims.csproj
```

Expected output:

```
Active document: AA-NDE-R.SLDDRW
==============================================
工程圖: AA-NDE-R.SLDDRW
==============================================
正在檢查 Dangling Dimensions（懸空尺寸）...

  [v] [視圖] 前視圖       | 線性尺寸  | 25.000 mm      | D1@草圖1@AA-NDE-R        | OK
  [!] [視圖] 前視圖       | 直徑尺寸  | 10.000 mm      | D2@草圖2@AA-NDE-R        | *** DANGLING（懸空）***

==============================================
檢查完成！共 32 個尺寸，其中 3 個為懸空尺寸。

以下尺寸為 Dangling（懸空），需要修復：
  [!] [視圖] 前視圖 -> 直徑尺寸 | 值: 10.000 mm | 名稱: D2@草圖2@AA-NDE-R
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for return codes and output format.

## Notes

- Read-only tool — does not modify the drawing
- Only scans `DisplayDimension` annotations; Notes and GD&T symbols are not included
- Dimension type codes: 2=線性, 3=角度, 4=弧長, 5=半徑, 6=直徑, 10=倒角, 11=水平線性, 12=垂直線性
