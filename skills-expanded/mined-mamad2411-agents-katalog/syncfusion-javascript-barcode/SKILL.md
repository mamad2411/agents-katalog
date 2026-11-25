---
name: syncfusion-javascript-barcode
description: Generate scannable barcodes in web apps using Syncfusion JavaScript Barcode Generator (linear barcodes, QR Code, Data Matrix). Trigger for barcode rendering, sizing/margins, colors, text display, error correction, quiet zones, encoding options, validation, and exporting to PNG/JPG/PDF for e-commerce, inventory, labels, and document workflows.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Barcode Generators

**When to use this skill:** You're building a web application that needs to generate, customize, and export barcodes (linear codes, QR codes, or Data Matrix codes). This includes point-of-sale systems, inventory management, ticketing systems, healthcare applications, or any solution requiring scannable codes.

---

## Barcode Library Overview

The Syncfusion Barcode Generator library (`@syncfusion/ej2-barcode-generator`) provides three main barcode types:

- **BarcodeGenerator**: Create linear 1D barcodes (Code39, Code128, Codabar, Code11, Code32, Code93, Code128A/B/C)
- **QRCodeGenerator**: Create 2D QR codes with optional logos and error correction
- **DataMatrixGenerator**: Create 2D Data Matrix codes for industrial and retail applications

All three use the same core API: initialize with configuration, append to DOM, customize, and export.

---

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- Project configuration for System.js or bundlers
- Creating your first barcode with each generator type
- CSS imports and theming
- Basic DOM appending pattern

### Barcode Types & Selection
📄 **Read:** [references/barcode-types.md](references/barcode-types.md)
- Linear barcode types: Code39, Code39 Extended, Code11, Codabar, Code32, Code93, Code128
- Character set limitations for each type
- When to use each barcode format
- Selection guide based on use case

### QR Code Generation
📄 **Read:** [references/qr-code-generation.md](references/qr-code-generation.md)
- QR code basics (versions, modules, capacity)
- Creating QR codes with displayText
- Adding logos/icons to QR codes
- Error correction levels (Low, Medium, Quarter, High)
- Dynamic resizing and version management

### Data Matrix Barcodes
📄 **Read:** [references/data-matrix-codes.md](references/data-matrix-codes.md)
- Data Matrix overview and use cases
- Creating Data Matrix codes
- Encoding numeric vs. alphanumeric data
- Size selection and layout patterns
- Integration with inventory systems

### Customization & Styling
📄 **Read:** [references/customization-styling.md](references/customization-styling.md)
- Barcode colors (foreColor, backgroundColor)
- Dimensions (width, height, responsive sizing)
- Display text customization (font, visibility, alignment)
- Render modes (SVG vs. Canvas)
- Advanced styling with CSS and theme integration

### Export & Printing
📄 **Read:** [references/export-printing.md](references/export-printing.md)
- Export to image formats (JPG, PNG)
- Export as Base64 string for storage
- Print functionality
- Download handling in browser
- Server-side integration patterns

### Validation & Events
📄 **Read:** [references/validation-events.md](references/validation-events.md)
- Input validation before barcode generation
- ValidateEvent handling
- Error prevention and edge cases
- Event-driven barcode updates
- Real-time validation patterns

---

## Quick Start Example

```typescript
import { BarcodeGenerator } from '@syncfusion/ej2-barcode-generator';

// Linear barcode (Code128)
const barcode = new BarcodeGenerator({
  width: '200px',
  height: '150px',
  type: 'Code128',
  value: 'SYNCFUSION',
  mode: 'SVG',
  displayText: { visibility: true }
});

barcode.appendTo('#barcode');

// For QR Code
import { QRCodeGenerator } from '@syncfusion/ej2-barcode-generator';

const qrCode = new QRCodeGenerator({
  width: '200px',
  height: '200px',
  value: 'Your value here',
  displayText: { visibility: false },
  mode: 'SVG'
});

qrCode.appendTo('#qrcode');

// For Data Matrix
import { DataMatrixGenerator } from '@syncfusion/ej2-barcode-generator';

const dataMatrix = new DataMatrixGenerator({
  width: '200px',
  height: '200px',
  value: 'Syncfusion',
  mode: 'SVG'
});

dataMatrix.appendTo('#datamatrix');
```

---

## Common Patterns

**Pattern 1: Type Selection**
- Use `Code128` for general-purpose alphanumeric barcodes (most flexible)
- Use `QRCodeGenerator` for URLs, contact info, or when logo branding is needed
- Use `DataMatrixGenerator` for industrial labeling and small-space encoding
- Use `Code39` for legacy systems or when ASCII is sufficient

**Pattern 2: Customization Pipeline**
```typescript
const barcode = new BarcodeGenerator({
  type: 'Code128',
  value: data,
  width: '200px',
  height: '150px',
  mode: 'SVG',
  foreColor: '#000000',
  backgroundColor: '#ffffff',
  displayText: { text: label }
});

barcode.appendTo('#element');
```

**Pattern 3: Dynamic Export**
```typescript
// Export to image with filename
barcode.exportImage('mybarcode', 'PNG');

// Export as Base64 for server submission
const base64 = await barcode.exportAsBase64Image('JPG');
```

**Pattern 4: Responsive Sizing**
```typescript
const barcode = new BarcodeGenerator({
  width: '100%',     // Responsive to container
  height: '150px',
  type: 'Code128',
  value: productCode
});
```

---

## Key Props

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `type` | string | 'Codabar' | Barcode type (Code39, Code128, etc.) |
| `value` | string | '' | Data to encode in barcode |
| `width` | string | '200px' | Barcode width (px or %) |
| `height` | string | '150px' | Barcode height |
| `mode` | string | 'SVG' | Render mode (SVG or Canvas) |
| `foreColor` | string | '#000000' | Barcode color |
| `backgroundColor` | string | '#ffffff' | Background color |
| `displayText` | object | `{}` | Display text config (visibility, text, font) |
| `logo` (QR only) | object | `null` | Logo config (imageSource, width, height) |
| `errorCorrectionLevel` (QR only) | number | 0 | Error correction: 0=Low, 1=Medium, 2=Quarter, 3=High |

---

## Common Use Cases

1. **Point of Sale**: Generate product barcodes on-the-fly with Code128
2. **Inventory**: Create shipment labels with Data Matrix for tracking
3. **Marketing**: Generate QR codes pointing to promotional URLs
4. **Healthcare**: Encode patient data in Code39 (legacy system compatible)
5. **E-commerce**: Generate order numbers as Code128 barcodes for packing
6. **Ticketing**: Create QR codes for event tickets with logo branding
7. **Document Management**: Embed Data Matrix in PDFs for sorting/filing

---

## Next Steps

Start with [Getting Started](references/getting-started.md) to set up the library, then select your barcode type using [Barcode Types](references/barcode-types.md). For customization needs, see [Customization & Styling](references/customization-styling.md). For export/print workflows, see [Export & Printing](references/export-printing.md).
