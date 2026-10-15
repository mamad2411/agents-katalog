---
name: syncfusion-aspnetcore-barcodes
description: "Implement Syncfusion ASP.NET Core Barcode components including BarcodeGenerator (1D codes like Code39, Code128, Codabar), QR Code Generator, and DataMatrix Generator. Use this when rendering barcodes, implementing QR codes with logo embedding, or generating DataMatrix codes. This skill covers barcode type selection, color and dimension customization, display text configuration, and export functionality (JPG, PNG, Base64)."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# ⚠️ STRICT USAGE RULES — MANDATORY FOR ALL CODE GENERATION

These rules are **non-negotiable**. They must be followed for **every** code generation request using this skill.

## Rule A — Use Only Provided Reference Files

- You must always read **`references/getting-started.md`** for every request
- Read other reference files **only if they directly match the user's query**:
  - `barcode-types.md` → 1D linear barcodes (Code39, Code128, Codabar, etc.)
  - `qr-code.md` → QR codes with optional logo embedding
  - `data-matrix.md` → DataMatrix barcodes
  - `customization.md` → color, size, display text properties
  - `export.md` → PNG/JPG/Base64 export functionality
- **No external knowledge** is allowed:
  - ❌ Do NOT use internet documentation
  - ❌ Do NOT use training-data assumptions
  - ✅ If a feature cannot be confirmed from reference files, apply Rule B

## Rule B — No Guessing, No Inference

If a feature, property, API, or behavior is **not explicitly documented** in the reference files:

**You must NOT:**
- Invent properties or methods
- Infer missing APIs or parameters
- Assume deprecated or undocumented features exist
- Generalize from other Syncfusion components

**Instead, respond with:**
```
⚠️ NOT DOCUMENTED: [feature name] is not covered in the reference files.
Skipping this feature to avoid generating incorrect code.
```

---

# Barcode Components Overview

Syncfusion EJ2 ASP.NET Core provides three barcode components via tag helpers:

| Component | Tag Helper | Best For | Key Properties |
|---|---|---|---|
| **BarcodeGenerator** | `<ejs-barcodegenerator>` | Linear 1D barcodes (Code39, Code128, Codabar, etc.) | `type`, `value`, `foreColor`, `width`, `height` |
| **QR Code Generator** | `<ejs-qrcodegenerator>` | 2D QR codes, URLs, large payloads | `value`, `width`, `height`, `foreColor`, `logoUrl` |
| **DataMatrix Generator** | `<ejs-datamatrixgenerator>` | 2D labels, print media, compact storage | `value`, `width`, `height`, `foreColor` |

All three support:
- ✅ Custom colors (`foreColor`)
- ✅ Dimension control (`width`, `height`)
- ✅ Display text customization
- ✅ Export to PNG/JPG/Base64

---

# Navigation Guide

**Always read `references/getting-started.md` first**, then read only files relevant to the request.

| Reference File | Read When the Query Involves |
|---|---|
| 📄 [getting-started.md](references/getting-started.md) | **Every request** — NuGet setup, tag helper registration, CDN, script manager |
| 📄 [barcode-types.md](references/barcode-types.md) | 1D barcodes, Code39, Code128, Codabar, Code11, Code32, Code93, barcode selection guidance |
| 📄 [qr-code.md](references/qr-code.md) | QR code rendering, logo embedding, error correction, versioning (v1–v40) |
| 📄 [data-matrix.md](references/data-matrix.md) | DataMatrix overview, rendering, use cases |
| 📄 [customization.md](references/customization.md) | Color (`foreColor`), dimensions (`width`/`height`), display text, rendering mode |
| 📄 [export.md](references/export.md) | Image export (PNG/JPG), Base64 export, export methods |

---

# Quick Start

## 1. Install NuGet Package

```powershell
Install-Package Syncfusion.EJ2.AspNet.Core
```

## 2. Register Tag Helper (`~/Pages/_ViewImports.cshtml`)

```cshtml
@addTagHelper *, Syncfusion.EJ2
```

## 3. Add CDN Resources (`~/Pages/Shared/_Layout.cshtml`)

```cshtml
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
    <script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>
</head>
<body>
    ...
    <ejs-scripts></ejs-scripts>
</body>
```

## 4. Basic Examples

### BarcodeGenerator (Code128)
```cshtml
<ejs-barcodegenerator id="barcode"
    width="200px"
    height="150px"
    type="Code128"
    value="SYNCFUSION"
    mode="SVG">
</ejs-barcodegenerator>
```

### QR Code
```cshtml
<ejs-qrcodegenerator id="qrcode"
    width="200px"
    height="200px"
    value="https://syncfusion.com"
    mode="SVG">
</ejs-qrcodegenerator>
```

### DataMatrix
```cshtml
<ejs-datamatrixgenerator id="datamatrix"
    width="200px"
    height="150px"
    value="Syncfusion"
    mode="SVG">
</ejs-datamatrixgenerator>
```

---

# Common Patterns

## Choose Barcode Type by Content

| Use Case | Recommended Type | Reason |
|---|---|---|
| Numeric only, short data | Codabar or Code11 | Compact, simple |
| Alphanumeric, uppercase | Code39 | Industry standard for labels |
| Full ASCII, variable length | Code128 | Most versatile, widely supported |
| Pharmaceutical (Italian) | Code32 | Specialized regulatory requirement |
| Dense alphanumeric data | Code93 | Better compression than Code39 |
| URL or large payload | QR Code | Handles complex data, scannable by phones |
| Label/print media with compact storage | DataMatrix | Industry standard for logistics |

## Customize Colors (All Generators)

```cshtml
<ejs-barcodegenerator id="barcode"
    width="200px" height="150px"
    type="Code128" value="SYNCFUSION"
    foreColor="red" mode="SVG">
</ejs-barcodegenerator>
```

## Embed Logo in QR Code

```cshtml
<ejs-qrcodegenerator id="qrcode"
    width="200px" height="200px"
    value="https://syncfusion.com"
    logoUrl="logo.png"
    mode="SVG">
</ejs-qrcodegenerator>
```

## Export Barcode on Button Click

```cshtml
<button onclick="exportBarcode()">Export as JPG</button>

<script>
  function exportBarcode() {
    var barcode = document.getElementById("barcode").ej2_instances[0];
    barcode.exportImage('MyBarcode', 'JPG');
  }
  
  function exportAsBase64() {
    var barcode = document.getElementById("barcode").ej2_instances[0];
    var base64String = barcode.exportAsBase64Image('PNG');
    console.log(base64String);
  }
</script>
```

## Hide Display Text

```cshtml
<ejs-barcodegenerator id="barcode"
    width="200px" height="150px"
    type="Code128" value="SYNCFUSION"
    displayText.visibility="false"
    mode="SVG">
</ejs-barcodegenerator>
```

---

## When to Use This Skill

✅ Rendering any barcode type in ASP.NET Core  
✅ Choosing between BarcodeGenerator, QR Code, and DataMatrix  
✅ Customizing barcode appearance (color, size, text)  
✅ Embedding a logo in a QR code  
✅ Exporting barcodes as images or Base64 strings  
✅ Selecting appropriate barcode type for use case