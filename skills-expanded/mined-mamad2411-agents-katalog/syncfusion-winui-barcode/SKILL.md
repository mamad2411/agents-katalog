---
name: syncfusion-winui-barcode
description: Implement Syncfusion WinUI Barcode (SfBarcode) control to generate and display machine-readable barcodes in desktop applications. Use this when working with barcodes, QR codes, or product labeling systems. This skill covers symbology types (DataMatrix, Code39, Code128, Codabar, UPC), barcode customization, text alignment, rotation, and visual encoding for WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Barcodes (SfBarcode)

The Syncfusion WinUI Barcode control (SfBarcode) generates and displays data in machine-readable barcode formats. It supports both one-dimensional (linear) and two-dimensional barcodes with extensive customization options for appearance, text display, and symbology-specific settings.


## When to Use This Skill

Use this skill when you need to:
- Generate barcodes or QR codes in WinUI applications
- Encode text, numbers, or data into machine-readable formats
- Display product codes, inventory labels, or shipping information
- Create scannable codes for mobile devices (QR, DataMatrix)
- Implement barcode printing functionality
- Customize barcode appearance (colors, rotation, text display)
- Choose appropriate symbology for specific data types
- Configure symbology-specific settings (error correction, encoding, checksums)

## Component Overview

**Key Capabilities:**
- **15 Symbology Types:** 12 one-dimensional + 3 two-dimensional barcode formats
- **Flexible Text Display:** Customizable alignment, spacing, and visibility
- **Visual Customization:** Colors, bar widths, rotation angles
- **Symbology Settings:** Type-specific configurations (checksums, encoding, error correction)
- **XAML and Code-Behind Support:** Declarative and programmatic implementation

**Common Use Cases:**
- Product labeling (UPC, EAN codes)
- Inventory management (Code39, Code128)
- Shipping labels (GS1-128, DataMatrix)
- QR codes for URLs, contact info, Wi-Fi credentials
- Document tracking (Code93, PDF417)
- Healthcare labels (Code32 pharmaceuticals)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use this when you need to:
- Install the Syncfusion.Barcode.WinUI NuGet package
- Set up a new WinUI project with barcode control
- Add namespace imports (XAML: `using:Syncfusion.UI.Xaml.Barcode`, C#: `using Syncfusion.UI.Xaml.Barcode`)
- Create your first barcode with basic configuration
- Understand the minimal code required (Value + Symbology)

**Topics Covered:**
- Creating WinUI 3 desktop application
- NuGet package installation
- Namespace configuration in XAML and C#
- Basic SfBarcode declaration
- Setting symbology (CodabarBarcode example)
- Initial working example

### Symbology Types
📄 **Read:** [references/symbology-types.md](references/symbology-types.md)

Use this when you need to:
- Choose the correct barcode type for your data
- Understand differences between 1D and 2D barcodes
- Learn which characters each symbology supports
- Implement specific barcode types (Codabar, Code39, Code128, QR, DataMatrix, etc.)
- Encode different data types (numeric-only, alphanumeric, full ASCII, binary)

**Covered Symbologies:**
- **1D Barcodes:** Codabar, Code11, Code32, Code39, Code39Extended, Code93, Code93Extended, Code128A/B/C, UPC, GS1Code128
- **2D Barcodes:** QRBarcode, DataMatrixBarcode, Pdf417Barcode
- Character set tables for each type
- Industry-specific use cases

### Text Customization
📄 **Read:** [references/text-customization.md](references/text-customization.md)

Use this when you need to:
- Show or hide the encoded text below the barcode
- Adjust spacing between barcode and text
- Align text horizontally (Left, Center, Right)
- Align text vertically (Top, Bottom)
- Control text visibility with ShowValue property

**Customization Options:**
- Value property (encoded text)
- ShowValue (display toggle)
- TextSpacing (gap between bars and text)
- HorizontalTextAlignment
- VerticalTextAlignment

### Visual Customization
📄 **Read:** [references/visual-customization.md](references/visual-customization.md)

Use this when you need to:
- Change barcode colors (Background, Foreground)
- Adjust bar width ratios (Module property)
- Enable auto-sizing for QR and DataMatrix codes
- Rotate barcodes (0°, 90°, 180°, 270°)
- Ensure scanner readability with proper contrast

**Customization Features:**
- Background and Foreground colors
- Module width for 1D barcodes
- AutoModule for 2D barcodes
- RotationAngle with BarcodeRotation enum
- Scanner contrast considerations

### Symbology-Specific Settings
📄 **Read:** [references/symbology-settings.md](references/symbology-settings.md)

Use this when you need to:
- Configure checksum options for 1D barcodes
- Set encoding format for DataMatrix barcodes
- Choose matrix size for DataMatrix
- Configure QR code version and error correction level
- Set input mode for QR codes
- Add start/stop symbols for barcode readers

**Configuration Options:**
- **1D Settings:** EnableCheckSum, ShowCheckSum, EncodeStartStopSymbols
- **DataMatrix:** Encoding (ASCII/ASCIINumeric/Auto/Base256), MatrixSize (30+ size options)
- **QR Code:** QRVersion (1-40 or Auto), ErrorCorrectionLevel (Low/Medium/Quartile/High), InputMode (Numeric/AlphaNumeric/Binary)

## Quick Start

### Minimal Barcode Implementation

**XAML:**
```xml
<Page xmlns:syncfusion="using:Syncfusion.UI.Xaml.Barcode">
    <Grid>
        <syncfusion:SfBarcode x:Name="barcode" 
                               Value="48625310"
                               Height="150">
            <syncfusion:SfBarcode.Symbology>
                <syncfusion:CodabarBarcode />
            </syncfusion:SfBarcode.Symbology>
        </syncfusion:SfBarcode>
    </Grid>
</Page>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Barcode;

SfBarcode barcode = new SfBarcode();
barcode.Value = "48625310";
barcode.Height = 150;
barcode.Symbology = new CodabarBarcode();
Root_Grid.Children.Add(barcode);
```

### QR Code for URL

```xml
<syncfusion:SfBarcode x:Name="qrCode" 
                       Value="http://www.syncfusion.com"
                       Height="200"
                       Width="200">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:QRBarcode />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

## Common Patterns

### Pattern 1: Product Label Barcode (UPC)
```xml
<syncfusion:SfBarcode Value="012345678905" 
                       Height="150" 
                       Width="300"
                       HorizontalTextAlignment="Center">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:UpcBarcode />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

### Pattern 2: Inventory Code (Code39 with Checksum)
```xml
<syncfusion:SfBarcode Value="ITEM12345" Height="120">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:Code39Barcode EnableCheckSum="True" 
                                   ShowCheckSum="True" />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

### Pattern 3: Shipping Label (DataMatrix)
```xml
<syncfusion:SfBarcode Value="SHIP2024-A45678" 
                       Width="200" 
                       Height="200"
                       ShowValue="False"
                       AutoModule="True">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:DataMatrixBarcode Encoding="Auto" 
                                       MatrixSize="Auto" />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

### Pattern 4: Rotated Barcode for Vertical Labels
```xml
<syncfusion:SfBarcode Value="VERTICAL123" 
                       RotationAngle="Angle90"
                       Height="250" 
                       Width="150">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:Code128BBarcode />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

### Pattern 5: QR Code with Error Correction
```xml
<syncfusion:SfBarcode Value="https://example.com/product/12345" 
                       Width="250" 
                       Height="250"
                       ShowValue="False">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:QRBarcode ErrorCorrectionLevel="High" 
                               QRVersion="Auto" />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

### Pattern 6: Custom Colored Barcode
```xml
<syncfusion:SfBarcode Value="COLORED123" 
                       Background="LightYellow"
                       Foreground="DarkBlue"
                       Height="150">
    <syncfusion:SfBarcode.Symbology>
        <syncfusion:Code128CBarcode />
    </syncfusion:SfBarcode.Symbology>
</syncfusion:SfBarcode>
```

## Key Properties

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| **Value** | string | The text/data to encode in the barcode |
| **Symbology** | BarcodeBase | The barcode type (Codabar, QR, DataMatrix, etc.) |
| **ShowValue** | bool | Display encoded text below barcode (default: true) |
| **Module** | double | Bar width ratio for 1D barcodes |
| **AutoModule** | bool | Auto-size 2D barcodes based on control size |
| **RotationAngle** | BarcodeRotation | Rotate barcode (Angle0/90/180/270) |
| **Background** | Brush | Barcode background color |
| **Foreground** | Brush | Barcode bars/dots color |
| **TextSpacing** | double | Space between barcode and text |
| **HorizontalTextAlignment** | TextAlignment | Text horizontal alignment (Left/Center/Right) |
| **VerticalTextAlignment** | BarcodeTextAlignment | Text vertical position (Top/Bottom) |

### Symbology Selection Guide

**For numeric-only data:**
- Code11, Code32, UpcBarcode, Code128C

**For alphanumeric data:**
- Code39, Code93, Code128A/B

**For full ASCII characters:**
- Code39Extended, Code93Extended

**For compact 2D codes:**
- QRBarcode (URLs, text)
- DataMatrixBarcode (small labels)

**For high-capacity data:**
- Pdf417Barcode (IDs, transport)

**For international products:**
- UpcBarcode, GS1Code128Barcode

## Common Use Cases

### Use Case 1: Product Packaging
Generate UPC barcodes for retail products with centered text display.

**When:** Creating product labels, retail packaging, price tags  
**Symbology:** UpcBarcode  
**References:** [getting-started.md](references/getting-started.md), [symbology-types.md](references/symbology-types.md)

### Use Case 2: Warehouse Inventory
Create scannable codes for inventory tracking with alphanumeric identifiers.

**When:** Asset tracking, warehouse management, stock control  
**Symbology:** Code39, Code128  
**References:** [symbology-types.md](references/symbology-types.md), [symbology-settings.md](references/symbology-settings.md)

### Use Case 3: QR Codes for Mobile Scanning
Generate QR codes for URLs, contact information, or Wi-Fi credentials.

**When:** Marketing materials, business cards, product authentication  
**Symbology:** QRBarcode  
**References:** [symbology-types.md](references/symbology-types.md), [symbology-settings.md](references/symbology-settings.md)

### Use Case 4: Shipping Labels
Create compact DataMatrix codes for shipping and logistics.

**When:** Package tracking, postal services, logistics  
**Symbology:** DataMatrixBarcode, GS1Code128Barcode  
**References:** [symbology-types.md](references/symbology-types.md), [symbology-settings.md](references/symbology-settings.md)

### Use Case 5: Pharmaceutical Labels
Generate Code32 barcodes for medication packaging and tracking.

**When:** Healthcare, pharmaceutical industry, prescription labels  
**Symbology:** Code32Barcode  
**References:** [symbology-types.md](references/symbology-types.md)

### Use Case 6: Document Management
Encode document IDs with PDF417 for archiving and retrieval systems.

**When:** Document tracking, archival systems, identification cards  
**Symbology:** Pdf417Barcode  
**References:** [symbology-types.md](references/symbology-types.md)

## Additional Resources

- **NuGet Package:** `Syncfusion.Barcode.WinUI`
- **Namespace:** `Syncfusion.UI.Xaml.Barcode`
- **Official Documentation:** https://help.syncfusion.com/winui/barcode/
- **GitHub Examples:** https://github.com/SyncfusionExamples/syncfusion-winui-barcode-examples
