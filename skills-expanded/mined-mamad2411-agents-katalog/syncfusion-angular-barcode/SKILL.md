---
name: syncfusion-angular-barcode
description: "Use Syncfusion EJ2 Angular Barcode/QR components to generate and customize barcodes in Angular. Trigger for Code39/Code128, EAN/UPC, QR Code, Data Matrix, label printing, inventory/product tags, colors/sizing/text, logo overlays, rendering, and export (PNG/SVG/PDF)."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Barcode Generation

## When to Use This Skill

Use this skill when you need to:
- **Create linear barcodes** (Code39, Code128, Code11, Codabar, Code32, Code93) for product identification and inventory management
- **Generate QR codes** for URLs, contact info, and quick data sharing
- **Encode Data Matrix codes** for compact, high-density encoding (healthcare, logistics)
- **Customize barcode appearance** (colors, dimensions, display text, logos)
- **Export barcodes** as image files (PNG, JPG) or base64 strings
- **Add logos to QR codes** for branding and visual enhancement

## Important: API Verification Required
 
**API Verification Required**: Always verify API class names, properties, and signatures by reading reference files (`references/*.md`) BEFORE generating code examples. Do not assume or infer class names.

**Real-world scenarios:**
- Product labeling systems for retail/inventory
- Mobile payment & authentication (QR codes)
- Healthcare/pharmaceutical tracking (Data Matrix)
- Document management & archiving
- Marketing campaigns using branded QR codes

---

## Component Overview

The Syncfusion Angular Barcode Generator supports three barcode families with extensive customization:

### Barcode Types

| Type | Use Case | Character Set | Industry |
|------|----------|---------------|----------|
| **Linear (Code39, Code128, Code11, Codabar, Code32, Code93)** | Product IDs, serial numbers, inventory | Alphanumeric (varies by type) | Retail, Warehouse, Telecom |
| **QR Code** | URLs, contact info, payments | Full Unicode | Marketing, Mobile, Finance |
| **Data Matrix** | Compact encoding, small labels | Numeric/Alphanumeric | Healthcare, Manufacturing, Logistics |

### Key Capabilities

- ✅ **7 linear barcode types** with symbol validation
- ✅ **Full customization** (colors, dimensions, fonts, margins)
- ✅ **Logo support** for QR codes via `QRCodeLogo`
- ✅ **Multiple export formats** (PNG, JPG, Base64)
- ✅ **Automatic version selection** for QR codes
- ✅ **Display text** customization below barcodes

---

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation & package setup (`@syncfusion/ej2-angular-barcode-generator`)
- Ivy vs ngcc package selection
- Basic component setup & imports
- Creating first Code128 barcode & QR code
- Project configuration & CSS

### Linear Barcodes (Code39, Code128, etc.)
📄 **Read:** [references/linear-barcodes.md](references/linear-barcodes.md)
- Code39 (standard alphanumeric)
- Code39 Extended (full ASCII support)
- Code128 (high-density encoding with 3 character sets)
- Code11 (telecommunications)
- Codabar (libraries, blood banks)
- Code32 (pharmaceutical/cosmetics)
- Code93 & Code93 Extended
- Character set limitations & validation
- When to choose each type

### QR Codes
📄 **Read:** [references/qr-codes.md](references/qr-codes.md)
- QR code versions (1-40) & capacity
- Basic QR code generation
- Color customization (foreColor, backgroundColor)
- Dimension control (width, height)
- Display text below QR code
- Adding logos & icons (`QRCodeLogo` with `imageSource`)
- Logo positioning & sizing
- Image sources (local files, URLs, base64)
- Error correction levels

### Data Matrix Codes
📄 **Read:** [references/data-matrix-barcodes.md](references/data-matrix-barcodes.md)
- Data Matrix overview & advantages
- Use cases (healthcare, logistics, compact encoding)
- Square vs rectangular symbols
- Dimension customization
- Color & appearance options
- Display text configuration
- When to use vs QR codes

### Customization & Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Shared customization properties (all barcode types)
- Color customization (foreColor, backgroundColor)
- Dimensions & scaling (width, height)
- Margins & padding
- Display text properties & positioning
- CSS class customization
- Responsive barcode sizing
- Advanced styling across all types

### Exporting Barcodes
📄 **Read:** [references/exporting-barcodes.md](references/exporting-barcodes.md)
- Export as image file (PNG, JPG)
- Export as base64 string
- Download functionality & file naming
- Integration with backend systems
- Use cases (printing, storage, sharing)

---

## Quick Start Example

### Basic Code128 Barcode

```html
<!-- app.component.html -->
<ejs-barcodegenerator 
  #barcode
  type="Code128" 
  value="123456789" 
  width="200px" 
  height="150px">
</ejs-barcodegenerator>
```

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-angular-barcode-generator';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {}
```

### QR Code with Custom Color

```html
<ejs-barcodegenerator 
  type="QRCode" 
  value="https://example.com" 
  [foreColor]="'#FF0000'"
  width="200px" 
  height="200px">
</ejs-barcodegenerator>
```

---

## Common Patterns

### Pattern 1: Choose Barcode Type by Use Case

**User needs to encode:**
- Product/inventory? → **Code128** (high-density, retail standard)
- Legacy system? → **Code39** (widely supported)
- Pharmaceutical? → **Code32** (industry standard)
- URL/contact? → **QR Code** (compact, mobile-friendly)
- Small label? → **Data Matrix** (high-density, space-efficient)

### Pattern 2: Customize for Different Backgrounds

```typescript
// Light background
@barcode type="Code128" foreColor="#000000" backgroundColor="#FFFFFF"

// Dark background
@barcode type="Code128" foreColor="#FFFFFF" backgroundColor="#000000"

// Branded QR code
@barcode type="QRCode" [qRCodeLogo]="logoConfig" foreColor="#1976D2"
```

### Pattern 3: Export & Download

```typescript
export class BarcodeComponent {
  @ViewChild('barcode') barcode: BarcodeGeneratorComponent;
  
  downloadBarcode() {
    this.barcode.exportImage('barcode','PNG');
  }

  getBase64() {
    const base64String = this.barcode.toDataURL('image/png');
    // Send to server or store
  }
}
```

### Pattern 4: Branded QR Codes with Logo

```html
<ejs-barcodegenerator 
  type="QRCode" 
  value="https://mysite.com"
  #qrCode>
</ejs-barcodegenerator>
```

```typescript
export class BrandedQRComponent implements OnInit {
  @ViewChild('qrCode') qrCode: BarcodeGeneratorComponent;
  
  ngOnInit() {
    (this.qrCode.qrcodelogo as QRCodeLogo) = {
      imageSource: 'assets/logo.svg',
      width: 50,
      height: 50
    };
  }
}
```

---

## Key Props Summary

| Property | Type | Use When | Default |
|----------|------|----------|---------|
| `type` | string | Selecting barcode type (Code128, QRCode, DataMatrix) | Code128 |
| `value` | string | Setting encoded data | "" |
| `width` | string | Controlling barcode width (px, %) | Auto |
| `height` | string | Controlling barcode height (px, %) | Auto |
| `foreColor` | string | Setting barcode color (#RGB or name) | #000000 |
| `backgroundColor` | string | Setting background color | #FFFFFF |
| `displayText` | object | `{ visibility: false }` | Adding human-readable label below barcode | "" |
| `margin` | object | Adding space around barcode | {left: 0, right: 0, top: 0, bottom: 0} |
| `qRCodeLogo` | object | Adding logo to QR code (imageSource, width, height) | undefined |
| `mode` | string | Rendering mode (SVG or Canvas) | SVG |

---

## Common Use Cases

### Use Case 1: Retail Product Labeling System

```typescript
// Create multiple product barcodes with customization
products.forEach(product => {
  <ejs-barcodegenerator 
    type="Code128"
    [value]="product.sku"
    [displayText]="{ text: 'Product SKU: 123456789', visibility: true }"
    foreColor="#333333"
    width="150px"
    height="100px">
  </ejs-barcodegenerator>
});
```

### Use Case 2: Mobile QR Code with Branding

```typescript
// QR code for app promotion with branded logo
<ejs-barcodegenerator 
  type="QRCode"
  value="https://appstore.com/myapp"
  [qRCodeLogo]="{ imageSource: 'assets/app-icon.png', width: 40, height: 40 }"
  [foreColor]="'#1976D2'"
  width="250px"
  height="250px">
</ejs-barcodegenerator>
```

### Use Case 3: Healthcare Tracking with Data Matrix

```typescript
// Compact Data Matrix for pharmaceutical packaging
<ejs-barcodegenerator 
  type="DataMatrix"
  [value]="medicineTrackingCode"
  [displayText]="{ text: 'Product SKU: 123456789', visibility: true }"
  width="80px"
  height="80px">
</ejs-barcodegenerator>
```

---

## Next Steps

- Start with [getting-started.md](references/getting-started.md) to install the package
- Choose your barcode type guide based on use case
- Customize using [customization.md](references/customization.md)
- Export barcodes using [exporting-barcodes.md](references/exporting-barcodes.md)
