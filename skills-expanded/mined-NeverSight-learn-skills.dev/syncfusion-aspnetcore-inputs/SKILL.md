---
name: syncfusion-aspnetcore-inputs
description: Complete guide to implementing the Syncfusion Inputs component in ASP.NET Core applications. Use this when working with file uploads, asynchronous processing, validation, drag-and-drop support, or enterprise-grade file handling for professional web forms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Inputs"
---

# Implementing Uploader in ASP.NET Core

The Uploader is a powerful file upload component for ASP.NET Core that handles file selection, validation, asynchronous uploads, drag-and-drop support, and progress tracking. This skill guides you through implementing Uploader in ASP.NET Core applications using Syncfusion's TagHelper syntax.

## Key Features

| Feature | Use Case |
|---------|----------|
| **Asynchronous Upload** | Non-blocking uploads with SaveUrl/RemoveUrl handlers |
| **Multiple File Upload** | Select and upload many files at once |
| **Single File Upload** | Restrict to one file per selection |
| **File Validation** | Validate extensions, size, count, duplicates |
| **Drag and Drop** | Drop files directly onto uploader area |
| **Custom Drop Area** | Define external elements as drop zones |
| **Auto Upload** | Upload files automatically or manually |
| **Progress Tracking** | Display upload progress with progress bar |
| **File Removal** | Remove uploaded files with RemoveUrl handler |
| **Chunk Upload** | Break large files into chunks for reliable upload |
| **Paste Upload** | Upload images from clipboard |
| **Directory Upload** | Upload entire folders and directory structure |
| **Form Integration** | Submit files as part of form submission |
| **Templates** | Customize file list and button appearance |
| **Localization** | Support multiple languages and cultures |
| **Error Handling** | Display upload failures with custom messages |

## Documentation Navigation Guide

### API Reference
📄 **Read:** [references/api.md](references/uploader-api.md)
- Complete list of all properties with TagHelper attribute names and defaults
- All events with callback argument details
- UploaderAsyncSettings sub-properties (save-url, remove-url, chunk-size, retry-count, retry-after-delay)
- UploaderButtonsProps sub-properties (browse, upload, clear)
- Preloaded files configuration (e-uploader-files / e-uploader-uploadedfiles)

### Getting Started
📄 **Read:** [references/getting-started.md](references/uploader-getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Configuring TagHelpers in _ViewImports.cshtml
- Adding stylesheets and script resources via CDN
- Registering the script manager (`<ejs-scripts>`)
- Creating your first Uploader
- Basic configuration and properties

### Asynchronous Upload
📄 **Read:** [references/async-upload.md](references/uploader-async-upload.md)
- Configuring SaveUrl and RemoveUrl endpoints
- Single vs multiple file upload modes (`multiple`)
- Sequential upload (`sequential-upload`)
- Auto-upload settings and manual upload triggers (`auto-upload`)
- Success and failure event handlers (`success`, `failure`)
- Progress tracking via `progress` event (`args.e.loaded / args.e.total`)
- Upload cancellation and retry
- Adding custom headers via `uploading` event

### File Validation
📄 **Read:** [references/file-validation.md](references/uploader-file-validation.md)
- File type validation with `allowed-extensions`
- File size constraints (`min-file-size`, `max-file-size`)
- Maximum file count restrictions via `selected` event
- Duplicate file detection and prevention
- Custom validation messages using `ej.base.L10n.load`
- Validation before and after upload

### Drag and Drop Support
📄 **Read:** [references/drag-drop-support.md](references/uploader-drag-drop-support.md)
- Default drag-and-drop behavior
- Configuring custom drop areas (`drop-area`)
- Multiple drop zones on single page
- File filtering on drop using `allowed-extensions` and `selected` event
- Paste-to-upload from clipboard (native JS clipboard events)
- Directory drag-drop support (`directory-upload`)

### Templates and Styling
📄 **Read:** [references/templates-and-styling.md](references/uploader-templates-and-styling.md)
- `template` property for custom file list item UI (`${name}`, `${size}`, `${type}`, `${statusText}`)
- Button customization via `<e-upload-buttons browse="" upload="" clear="">`
- `show-file-list` for fully custom file lists
- CSS class customization (`css-class`)
- Theme integration (Fluent, Material, Bootstrap)
- Responsive design patterns

### Advanced Patterns
📄 **Read:** [references/advanced-patterns.md](references/uploader-advanced-patterns.md)
- Chunk upload for large files (`chunk-size`, `retry-count`, `retry-after-delay`)
- Correct server-side chunk handling (`chunk-index`, `total-chunk` form keys)
- Pause/resume chunk upload
- Form submission with file uploads (`autoUpload="false"`)
- Directory upload handling (`directory-upload`)
- File removal and cleanup strategies
- Advanced error handling
- Security considerations (path traversal prevention, MIME validation)

## Quick Start Example

### Basic Uploader with Async Upload (TagHelper)

```html
<!-- Views/Home/Index.cshtml -->
<div class="form-group">
    <ejs-uploader id="uploader">
        <e-uploader-asyncsettings saveUrl="Home/Save" removeUrl="Home/Remove"></e-uploader-asyncsettings>
        <e-upload-files></e-upload-files>
    </ejs-uploader>
</div>

<div id="uploadedFiles"></div>
```

### Configuration in HomeController.cs

```csharp
using Microsoft.AspNetCore.Mvc;
using System.IO;

public class HomeController : Controller
{
    private readonly IWebHostEnvironment _webHostEnvironment;

    public HomeController(IWebHostEnvironment webHostEnvironment)
    {
        _webHostEnvironment = webHostEnvironment;
    }

    [HttpPost]
    public IActionResult Save(IFormFile[] uploader)
    {
        if (uploader != null && uploader.Length > 0)
        {
            string uploadPath = Path.Combine(_webHostEnvironment.WebRootPath, "Uploads");
            if (!Directory.Exists(uploadPath))
                Directory.CreateDirectory(uploadPath);

            foreach (IFormFile file in uploader)
            {
                string filePath = Path.Combine(uploadPath, file.FileName);
                using (FileStream fs = System.IO.File.Create(filePath))
                {
                    file.CopyTo(fs);
                    fs.Flush();
                }
            }
        }
        return Ok();
    }

    [HttpPost]
    public IActionResult Remove(string[] files)
    {
        string uploadPath = Path.Combine(_webHostEnvironment.WebRootPath, "Uploads");
        
        foreach (string file in files)
        {
            string filePath = Path.Combine(uploadPath, file);
            if (System.IO.File.Exists(filePath))
                System.IO.File.Delete(filePath);
        }
        return Ok();
    }
}
```

### In _ViewImports.cshtml (one-time setup)

```html
@addTagHelper *, Syncfusion.EJ2
```

### In _Layout.cshtml (one-time setup)

```html
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/33.1.44/fluent.css" />
    <script src="https://cdn.syncfusion.com/ej2/33.1.44/dist/ej2.min.js"></script>
</head>
<body>
    @RenderBody()
    
    <ejs-scripts></ejs-scripts>
</body>
```

## Common Patterns

### Pattern 1: Multiple File Upload with Progress

```html
<ejs-uploader id="multiUploader"
    allowedExtensions=".jpg,.png,.pdf,.doc,.docx"
    maxFileSize="5242880"
    autoUpload="false"
    multiple="true"
    progress="onProgress"
    success="onSuccess"
    failure="onFailure">
    <e-uploader-asyncsettings saveUrl="Home/Save" removeUrl="Home/Remove"></e-uploader-asyncsettings>
</ejs-uploader>

<script>
function onProgress(args) {
    console.log('Uploading: ' + args.file.name);
    let percent = Math.round((args.e.loaded / args.e.total) * 100);
    console.log('Progress: ' + percent + '%');
}

function onSuccess(args) {
    if (args.operation === 'upload') {
        console.log(args.file.name + ' uploaded successfully');
    }
}

function onFailure(args) {
    console.log('Upload failed: ' + args.statusCode + ' | ' + args.response);
}
</script>
```

### Pattern 2: Single File Upload with Validation

```html
<ejs-uploader id="singleUploader"
    allowedExtensions=".jpg,.png,.jpeg"
    maxFileSize="2097152"
    multiple="false"
    selected="onFileSelected"
    autoUpload="true">
    <e-uploader-asyncsettings saveUrl="Home/Save" removeUrl="Home/Remove"></e-uploader-asyncsettings>
</ejs-uploader>

<script>
function onFileSelected(args) {
    if (args.filesData.length > 1) {
        args.filesData.splice(1);
        alert('Only one file can be selected');
    }
}
</script>
```

### Pattern 3: Drag-Drop with Custom Area

```html
<div id="dropArea" style="border: 2px dashed #ccc; padding: 20px; min-height: 200px;">
    Drop files here
</div>

<ejs-uploader id="uploader"
    dropArea="#dropArea"
    autoUpload="true">
    <e-uploader-asyncsettings saveUrl="Home/Save" removeUrl="Home/Remove"></e-uploader-asyncsettings>
</ejs-uploader>
```

## Key Properties

| Property | TagHelper Attribute | Type | Default | Purpose |
|----------|-------------------|------|---------|---------|
| `AllowedExtensions` | `allowedExtensions` | string | `""` | File types to allow (e.g., `".jpg,.png"`) |
| `MaxFileSize` | `maxFileSize` | double | `30000000` | Maximum file size in bytes |
| `MinFileSize` | `minFileSize` | double | `0` | Minimum file size in bytes |
| `Multiple` | `multiple` | bool | `true` | Allow multiple file selection |
| `AutoUpload` | `autoUpload` | bool | `true` | Upload files automatically after selection |
| `SequentialUpload` | `sequentialUpload` | bool | `false` | Upload files one after another |
| `DropArea` | `dropArea` | string | null | CSS selector for custom drop area |
| `DirectoryUpload` | `directoryUpload` | bool | `false` | Allow folder/directory selection |
| `ShowFileList` | `showFileList` | bool | `true` | Show/hide the default file list |
| `Template` | `template` | string | null | Custom HTML template for file list items |
| `CssClass` | `cssClass` | string | `""` | Additional CSS classes on root element |
| `EnableRtl` | `enableRtl` | bool | `false` | Right-to-left rendering |
| `Locale` | `locale` | string | `""` | Localization culture code |

**AsyncSettings Sub-Properties (set via `<e-uploader-asyncsettings>`):**

| Property | TagHelper Attribute | Default | Purpose |
|----------|-------------------|---------|---------|
| `SaveUrl` | `saveUrl` | `""` | Server endpoint for saving uploaded files |
| `RemoveUrl` | `removeUrl` | `""` | Server endpoint for removing uploaded files |
| `ChunkSize` | `chunkSize` | `0` | Chunk size in bytes; enables chunk upload when > 0 |
| `RetryCount` | `retryCount` | `3` | Number of retry attempts on chunk failure |
| `RetryAfterDelay` | `retryAfterDelay` | `500` | Delay (ms) before chunk retry |

## Common Use Cases

### Use Case 1: Profile Picture Upload
- Single file, image only, auto-upload
- Reference: [references/advanced-patterns.md](references/uploader-advanced-patterns.md)

### Use Case 2: Document Management
- Multiple files, validation, chunk upload for large files
- Reference: [references/async-upload.md](references/uploader-async-upload.md)

### Use Case 3: Bulk Import
- Directory upload, form submission, error handling
- Reference: [references/advanced-patterns.md](references/uploader-advanced-patterns.md)

### Use Case 4: Media Gallery
- Multiple uploads, custom templates, drag-drop
- Reference: [references/templates-and-styling.md](references/uploader-templates-and-styling.md)

---

**Next Step:** Read [references/getting-started.md](references/uploader-getting-started.md) to begin implementing Uploader in your ASP.NET Core application.
