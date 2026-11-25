---
name: syncfusion-aspnetcore-image-editor
description: Implement the Syncfusion ASP.NET Core Image Editor (EJ2) component. Use this when adding image editing to an ASP.NET Core application, including cropping, rotating, annotations, fine-tuning (brightness, contrast, blur), and filter application. Covers opening/saving images, toolbar customization, redaction, resizing, and image editor event handling with ejs-imageeditor.
metadata:
  author: "Syncfusion Inc"
  category: "File Viewers & Editors"
  version: "33.1.44"
---

# Implementing Syncfusion ASP.NET Core Image Editor

The Syncfusion EJ2 Image Editor provides a rich, interactive image editing experience directly in the browser. It supports opening, editing, and saving images in PNG, JPEG, SVG, WEBP, and BMP formats. All actions—including annotations, transformations, and filters—are tracked in a 16-step undo/redo history.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/image-editor-getting-started.md)
- NuGet installation and setup
- Tag helper registration in `_ViewImports.cshtml`
- Adding stylesheet and script references — local assets (recommended) or CDN with SRI hashes
- Rendering the basic `<ejs-imageeditor>` tag
- Container CSS for proper sizing

### Opening & Saving Images
📄 **Read:** [references/open-save.md](references/image-editor-open-save.md)
- `open()` method — local file, base64, Blob, URL, File Uploader, File Manager
- Opening with custom width/height via `imageSettings`
- `export()` — save with format and quality options
- `getImageData()` — retrieve image as base64 / Blob
- `clearImage()` and `reset()` patterns
- Rendering Image Editor inside a Dialog
- Adding watermarks automatically on open
- `FileOpened`, `Saving`, and `BeforeSave` events

### Transformations (Rotate, Flip, Zoom, Pan)
📄 **Read:** [references/transform.md](references/image-editor-transform.md)
- `rotate()` — clockwise/anti-clockwise in degrees
- `flip()` — Horizontal or Vertical
- `straightenImage()` — ±45° range for alignment
- `zoom()` — magnify with optional zoom point
- `ZoomSettings` — `minZoomFactor`, `maxZoomFactor`
- Panning behavior when image exceeds canvas
- `Rotating`, `Flipping`, `Zooming`, `Panning` events

### Selection & Cropping
📄 **Read:** [references/selection-cropping.md](references/image-editor-selection-cropping.md)
- `select()` — custom, square, circle, aspect ratio types
- `crop()` — execute crop on selected region
- Maintaining original image size during cropping (`preventScaling`)
- `SelectionChanging` event — programmatic selection adjustments
- Locking selection area to prevent resizing
- Custom ratio cropping via public methods

### Annotations
📄 **Read:** [references/annotation.md](references/image-editor-annotation.md)
- `drawText()` — text with font, size, bold, italic, underline, strikethrough, fill, stroke
- Multiline text using `\n` in text content
- `drawRectangle()`, `drawEllipse()`, `drawLine()`, `drawArrow()`, `drawPath()`
- `drawImage()` — overlay images, logos, watermarks
- `freehandDraw()` — enable/disable freehand drawing mode
- `deleteShape()` / `getShapeSetting()` — manage annotations
- `FontFamily` property — add custom font families
- Z-order management (bring forward, send backward, bring to front, send to back)
- `ShapeChanging` / `ShapeChange` events

### Fine-Tune & Filters
📄 **Read:** [references/finetune-filter.md](references/image-editor-finetune-filter.md)
- `finetuneImage()` — brightness, contrast, saturation, hue, exposure, blur, opacity
- `FinetuneSettings` property for configuring available fine-tune options
- `applyImageFilter()` — cold, warm, chrome, sepia, grayscale, invert
- `FinetuneValueChanging` event
- `ImageFiltering` event with cancel support

### Resize & Redact
📄 **Read:** [references/resize-redact.md](references/image-editor-resize-redact.md)
- `resize()` — width, height, aspect ratio control
- `Resizing` event with before/after dimensions
- `drawRedact()` — blur or pixelate sensitive areas
- `selectRedact()`, `deleteRedact()`, `updateRedact()`, `getRedacts()`

### Toolbar & Quick Access Toolbar
📄 **Read:** [references/toolbar-quickaccess.md](references/image-editor-toolbar-quickaccess.md)
- Built-in toolbar items list (Open, Undo, Redo, Crop, Annotate, Filter, Save, etc.)
- `Toolbar` property — add, remove, or hide toolbar items
- `ToolbarTemplate` — replace entire toolbar with custom HTML
- `ToolbarUpdating` event — customize contextual toolbars
- `ShowQuickAccessToolbar` — toggle quick access toolbar
- `QuickAccessToolbarOpen` event — add custom items to quick access toolbar
- `ToolbarCreated` / `ToolbarItemClicked` events

### Frames, Localization, Accessibility & Undo-Redo
📄 **Read:** [references/frames-localization-accessibility.md](references/image-editor-frames-localization-accessibility.md)
- `drawFrame()` — mat, bevel, line, hook, inset frame types
- `UploadSettings` — restrict file extensions and file sizes
- `Locale` property — internationalization with translation objects
- WCAG 2.2 AA compliance, keyboard shortcuts
- `undo()` / `redo()` methods and `AllowUndoRedo` property (16-step history)

### API Reference
📄 **Read:** [references/api.md](references/image-editor-api.md)
- All properties: `AllowUndoRedo`, `CssClass`, `Disabled`, `Height`, `Width`, `Theme`, `Locale`
- Complex settings objects: `ZoomSettings`, `FinetuneSettings`, `SelectionSettings`, `UploadSettings`, `FontFamily`
- All events with their argument types
- Client-side JavaScript methods

---

## Quick Start

### 1. Install NuGet Package

```bash
Install-Package Syncfusion.EJ2.AspNet.Core
```

### 2. Register Tag Helper (`~/Pages/_ViewImports.cshtml`)

```cshtml
@addTagHelper *, Syncfusion.EJ2
```

### 3. Add CSS & Script (`~/Pages/Shared/_Layout.cshtml`)

**Local Assets Only (Required for Security Compliance)**

Download the Syncfusion EJ2 distribution from the [official release](https://www.syncfusion.com/downloads/aspnetcore) and host locally:

```html
<head>
     <!-- CSS hosted locally in wwwroot/lib/ej2/ -->
     <link rel="stylesheet" href="/lib/ej2/fluent2.css" />
</head>
<body>
    ...
    <!-- JavaScript hosted locally in wwwroot/lib/ej2/ -->
    <!-- IMPORTANT: Do NOT load from external CDN — use local assets only -->
    <script src="/lib/ej2/ej2.min.js"></script>
    <ejs-scripts></ejs-scripts>
</body>
```

> **⚠️ Security Policy:** External CDN loading is not permitted. All Syncfusion runtime assets must be hosted locally in your application.

### 4. Render Image Editor (`~/Pages/Index.cshtml`)

```cshtml
<div class="e-img-editor-sample">
    <ejs-imageeditor id="image-editor"></ejs-imageeditor>
</div>

<style>
    .e-img-editor-sample {
        height: 80vh;
        width: 100%;
    }
</style>
```

---

## Common Patterns

### Open an Image Programmatically

**Option A: Local Image File (Recommended)**
```cshtml
<ejs-imageeditor id="image-editor" created="onCreated"></ejs-imageeditor>

<script>
function onCreated() {
    var imageEditor = document.getElementById('image-editor').ej2_instances[0];
    // Reference local image in wwwroot/images/
    imageEditor.open('/images/nature.png');
}
</script>
```

**Option B: User-Uploaded Image (Base64)**
```cshtml
<ejs-uploader id="fileUpload" selected="onFileSelected"></ejs-uploader>
<ejs-imageeditor id="image-editor"></ejs-imageeditor>

<script>
function onFileSelected(args) {
    if (args.filesData.length > 0) {
        var reader = new FileReader();
        reader.onload = function() {
            // Pass base64-encoded local data (no external fetch)
            var imageEditor = document.getElementById('image-editor').ej2_instances[0];
            imageEditor.open(reader.result);
        };
        reader.readAsDataURL(args.filesData[0].rawFile);
    }
}
</script>
```

### Export / Save Image

```cshtml
<button onclick="saveImage()">Save</button>
<ejs-imageeditor id="image-editor" created="onCreated"></ejs-imageeditor>

<script>
function onCreated() {
    var imageEditor = document.getElementById('image-editor').ej2_instances[0];
    // Load local image
    imageEditor.open('/images/nature.png');
}

function saveImage() {
    var imageEditor = document.getElementById('image-editor').ej2_instances[0];
    imageEditor.export('PNG');  // saves as PNG to local device
}
</script>
```

### Handle FileOpened Event

```cshtml
<ejs-imageeditor id="image-editor" fileOpened="onFileOpened"></ejs-imageeditor>

<script>
function onFileOpened(args) {
    console.log('Opened file:', args.fileName, 'Type:', args.fileType);
}
</script>
```

### Restrict Upload File Types

```cshtml
<ejs-imageeditor id="image-editor">
    <e-imageeditor-uploadsettings allowedExtensions=".jpg, .png, .webp"
                                  minFileSize="10000"
                                  maxFileSize="5000000">
    </e-imageeditor-uploadsettings>
</ejs-imageeditor>
```

---

## Key Properties at a Glance

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `height` | string | "100%" | Editor height |
| `width` | string | "100%" | Editor width |
| `allowUndoRedo` | bool | true | Enable undo/redo (16 steps) |
| `disabled` | bool | false | Disable the control |
| `showQuickAccessToolbar` | bool | true | Show annotation quick access toolbar |
| `theme` | Theme | Bootstrap5 | Shape selection appearance theme |
| `locale` | string | "en-US" | Localization culture |
| `imageSmoothingEnabled` | bool | false | High-quality rendering smoothing |
| `toolbar` | object | default items | Toolbar items array |
| `toolbarTemplate` | string | null | Custom toolbar template selector |

---

## Security & Trust Boundary

### ⚠️ CRITICAL: Never Load External URLs

**DO NOT** use `imageEditor.open()` or `drawImage()` with external/untrusted URLs:

```javascript
// ❌ FORBIDDEN — Loads remote content from untrusted sources
imageEditor.open('https://untrusted-external-cdn.com/bridge.png');
imageEditor.open('https://example.com/user-uploads/image.jpg');  // Arbitrary external URL
imageEditor.drawImage('https://external-site.com/logo.png', 10, 10, 100, 50);

// ✅ SAFE — Use only local/trusted sources
imageEditor.open('/images/local-image.png');  // Local file in wwwroot
imageEditor.open(base64DataUrl);              // Base64 encoded (local data)
imageEditor.open(blobUrl);                    // Blob URL from File input
imageEditor.drawImage('/images/company-logo.png', 10, 10, 100, 50);  // Local asset
```

External URLs create **supply-chain and injection risks** that cannot be fully mitigated.

---

### Runtime & Content Security

**CRITICAL POLICY:** This skill requires all runtime code and content to be sourced locally.

#### **Requirement 1: Local Runtime Assets Only (W012)**
The Syncfusion EJ2 runtime library **MUST** be hosted locally:
- ✅ Download from [official Syncfusion release](https://www.syncfusion.com/downloads/aspnetcore)
- ✅ Host in `wwwroot/lib/ej2/`
- ✅ Reference as `/lib/ej2/ej2.min.js` (local path only)
- ❌ **DO NOT** load from any external CDN or remote URL

#### **Requirement 2: Local Content Only (W011)

#### **Content Security Practices**

##### **1. Load Images as Base64 or Blob (Recommended)**
Load user-uploaded files locally and pass as base64 or Blob to avoid any external fetches:

```javascript
// ✅ SAFE: Load user file locally as base64
function selected(args) {
    if (args.filesData.length > 0) {
        var reader = new FileReader();
        reader.onload = function() {
            imageEditor.open(reader.result);  // Base64 data, not URL
        };
        reader.readAsDataURL(args.filesData[0].rawFile);
    }
}
```

##### **2. Server-Side Image Validation**
Validate all image uploads server-side before processing:

```csharp
// ASP.NET Core controller
[HttpPost]
public IActionResult ValidateImage(IFormFile file)
{
    // Whitelist allowed MIME types only
    var allowedTypes = new[] { "image/png", "image/jpeg", "image/webp", "image/bmp" };
    if (!allowedTypes.Contains(file.ContentType))
        return BadRequest("Invalid image format");
    
    // Enforce file size limits (e.g., max 5MB)
    if (file.Length > 5 * 1024 * 1024)
        return BadRequest("File too large");
    
    return Ok();
}
```

##### **3. Local Assets Only for Overlays**
When using `drawImage()` for logos or watermarks, reference only local assets:

```javascript
// ✅ SAFE: Local asset in wwwroot/images/
imageEditor.drawImage('/images/company-logo.png', 10, 10, 100, 50);

// ❌ FORBIDDEN: External URLs not permitted
// imageEditor.drawImage('https://external-site.com/logo.png', ...);  
```

##### **4. Implement Content Security Policy**
Restrict all content sources to local/trusted origins:

```html
<!-- Enforce local-only content loading -->
<meta http-equiv="Content-Security-Policy" 
      content="script-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline';">
```

---

### Trust Assessment

| Factor | Assessment |
|--------|------------|
| **Vendor** | Syncfusion Inc. — established enterprise component vendor, widely adopted |
| **Protocol** | All CDN resources served over **HTTPS** with certificate pinning possible |
| **Transparency** | Regular security updates and CVE disclosures via Syncfusion support channels |
| **Monitoring** | Check Syncfusion security bulletins and NuGet package advisory database |
| **Undo/Redo** | 16-step history is local-only; no cloud sync or external telemetry |

---

### Best Practices

✅ **Runtime Asset Security**
- Host all Syncfusion runtime assets locally in `wwwroot/lib/ej2/`
- Never load from external CDN or remote servers
- Update to latest stable version regularly
- Monitor [Syncfusion security advisories](https://www.syncfusion.com/security)
- Verify package integrity using NuGet package signatures

✅ **Content & Image Security**
- Load all images as base64 or Blob (local data only)
- Validate file type, size, and content server-side
- Never trust user-supplied URLs directly
- Reference only internal assets for overlays (logos, watermarks)
- Use `wwwroot/images/` for all application images

✅ **Compliance & Monitoring**
- Implement strict CSP: `script-src 'self'; img-src 'self' data:`
- Perform security scans during CI/CD pipeline
- Audit dependencies with `snyk`, `dotnet list package --vulnerable`, etc.
- Maintain inventory of all local hosted assets
- Test security updates in staging before production deployment

---

## Related Skills

- [Implementing Syncfusion ASP.NET Core Components](./SKILL.md) — Parent library skill
