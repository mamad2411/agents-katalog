---
name: al-base-app
description: Look up pages, actions, action categories, fields, and other objects from the Microsoft BC Base Application .app package. Use this skill when working on AL extensions that target standard BC pages or objects and you need to verify action group names, category names, field names, or page structure — for example to correctly hide or extend print/send groups.
---

The Base Application .app package is a NAVX-wrapped ZIP. Use the workflow below to extract and inspect it without any external tools.

## Package Location

The `.alpackages` folder is typically at the workspace root. Use the most recent Base Application version:

```powershell
Get-ChildItem "<workspace>\.alpackages" -Filter "Microsoft_Base Application_*.app" |
    Sort-Object Name -Descending |
    Select-Object -First 1 -ExpandProperty FullName
```

## Extraction Workflow

The NAVX format is a ZIP starting at byte offset 40. Extract with pure PowerShell:

```powershell
$appPath = "<path to .app>"
$bytes   = [System.IO.File]::ReadAllBytes($appPath)
$zipPath = "$env:TEMP\BaseApp_inspect.zip"
[System.IO.File]::WriteAllBytes($zipPath, $bytes[40..($bytes.Length - 1)])
```

## Reading a Specific File

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)

# List entries matching a pattern
$archive.Entries | Where-Object { $_.Name -like "*PostedSalesCreditMemo*" } | Select-Object FullName

# Read a specific entry
$entry  = $archive.Entries | Where-Object { $_.FullName -eq "src/Sales/History/PostedSalesCreditMemo.Page.al" }
$reader = New-Object System.IO.StreamReader($entry.Open())
$content = $reader.ReadToEnd()
$reader.Dispose()
$archive.Dispose()
```

## Common Inspection Queries

### Find all action category group names
```powershell
$content -split "`n" | Select-String "group\(Category_" 
```

### Find the promoted Print/Send group
```powershell
$lines = $content -split "`n"
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match "Print/Send") {
        # Print surrounding context
        $lines[($i-5)..($i+5)] | ForEach-Object -Begin { $n=$i-4 } { "${n}: $_"; $n++ }
    }
}
```

### Show lines around a keyword with context
```powershell
$lines = $content -split "`n"
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match "Category_Category7|Print|Send") {
        Write-Host "$($i+1): $($lines[$i])"
    }
}
```

### Show a line range
```powershell
$lines[1204..1234] | ForEach-Object -Begin { $i = 1205 } { "${i}: $_"; $i++ }
```

## Common Base App Source Paths

| Object | Path |
|---|---|
| Posted Sales Invoice | `src/Sales/History/PostedSalesInvoice.Page.al` |
| Posted Sales Credit Memo | `src/Sales/History/PostedSalesCreditMemo.Page.al` |
| Sales Order | `src/Sales/Document/SalesOrder.Page.al` |
| Sales Invoice | `src/Sales/Document/SalesInvoice.Page.al` |
| Sales Quote | `src/Sales/Document/SalesQuote.Page.al` |
| Purchase Order | `src/Purchases/Document/PurchaseOrder.Page.al` |
| Posted Purchase Invoice | `src/Purchases/History/PostedPurchaseInvoice.Page.al` |

Paths follow the pattern `src/<Module>/<Subfolder>/<ObjectName>.<Type>.al`.  
Use `$archive.Entries | Where-Object { $_.Name -like "*<keyword>*" }` when unsure of the path.

## Key Rule for Page Extensions

Always verify the **exact** `group(Category_...)` name before using `modify(...)` or `addbefore(...)`/`addafter(...)` in a pageextension. Different pages use different category numbers for the same logical group (e.g. Print/Send is `Category_Category6` on page 132 but `Category_Category7` on page 134).
