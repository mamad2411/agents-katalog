---
name: syncfusion-angular-uploader
description: Implement Syncfusion Angular Uploader for single/multiple file uploads, async/chunk uploads, drag-and-drop, validation, templates, and form integration. Use this when building file upload UIs, handling server-side operations, progress tracking, or customizing file lists in Angular apps. Covers APIs, events, styling, accessibility, and localization.
metadata:
  author: "Syncfusion Inc"
  category: "Input Components"
  version: "33.1.44"
---

# Implementing Syncfusion Angular Uploader

The Syncfusion Angular Uploader (`ejs-uploader`) is a full-featured file upload component that supports asynchronous uploads, chunk uploading of large files, drag-and-drop, clipboard paste, directory upload, file validation, templates, form integration, JWT authentication, and comprehensive event handling.

## Component Overview

The Syncfusion Angular Uploader provides:

- **Async upload modes:** Auto upload (default) or manual upload with action buttons
- **Chunk upload:** Split large files into configurable byte-size chunks with retry logic
- **Sequential upload:** Process files one at a time to reduce server traffic
- **File sources:** Browse dialog, drag-and-drop, clipboard paste, directory selection
- **Validation:** File type (extensions), min/max size, custom count limits, duplicate prevention
- **Templates:** Customize the file list item structure; build fully custom upload UIs
- **Form support:** HTML form submission, template-driven forms (ngModel), reactive forms (FormGroup)
- **Accessibility:** WCAG 2.2, Section 508, keyboard navigation, screen reader support
- **Localization:** Customize all static text via L10n

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation of `@syncfusion/ej2-angular-inputs`
- Package setup, CSS imports, and Angular standalone component usage
- Adding the `<ejs-uploader>` component
- Configuring async settings (saveUrl, removeUrl)
- Handling success and failure events
- Adding a custom drop area

### Asynchronous Upload
📄 **Read:** [references/async-upload.md](references/async-upload.md)
- Multiple and single file upload modes (`multiple` property)
- Save action configuration and server-side handling
- Remove action and `postRawFile` usage
- Auto upload vs manual upload (`autoUpload` property)
- Sequential upload (`sequentialUpload`)
- Preloaded files (`files` property)
- Adding custom HTTP headers to upload requests

### Chunk Upload
📄 **Read:** [references/chunk-upload.md](references/chunk-upload.md)
- Enabling chunk upload via `asyncSettings.chunkSize`
- Pause, resume, and cancel chunk uploads
- Retry configuration (`retryCount`, `retryAfterDelay`)
- `chunkSuccess` and `chunkFailure` events
- Server-side chunk assembly implementation

### File Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Restricting file types with `allowedExtensions`
- Min/max file size constraints (`minFileSize`, `maxFileSize`)
- Limiting upload count via the `selected` event
- Preventing duplicate file uploads
- MIME type validation before upload
- Image/* validation on drag-and-drop

### File Sources
📄 **Read:** [references/file-sources.md](references/file-sources.md)
- Paste images from clipboard
- Directory (folder) upload with `directoryUpload`
- Drag-and-drop with built-in and custom drop areas
- Custom drop area styling (`.e-upload-drag-hover`)
- Triggering file browse from an external button

### Templates & Custom UI
📄 **Read:** [references/templates-and-custom-ui.md](references/templates-and-custom-ui.md)
- File list template with the `template` property
- Building a completely custom upload UI (hiding default list with `showFileList`)
- Customizing action buttons with HTML elements (`buttons` property)
- Customizing the progress bar appearance
- Preview images before uploading
- Resize images before uploading to server

### Form Integration
📄 **Read:** [references/form-integration.md](references/form-integration.md)
- Using Uploader inside HTML forms (synchronous submission)
- Template-driven forms with `ngModel`
- Reactive forms with `FormGroup`
- Required field validation (`required` attribute)
- Reset behavior with form reset

### Styling & Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- Customizing the uploader wrapper dimensions
- Styling the browse button
- Customizing the drop area text
- Customizing the file list container
- Hiding the default drop area
- CSS class reference for key Uploader elements

### Accessibility & Localization
📄 **Read:** [references/accessibility-and-localization.md](references/accessibility-and-localization.md)
- WCAG 2.2, Section 508, keyboard shortcuts
- Screen reader and RTL support
- Localizing all static labels and messages with L10n

### Advanced How-To Patterns
📄 **Read:** [references/advanced-patterns.md](references/advanced-patterns.md)
- Upload files programmatically with the `upload()` method
- Invisible (background) upload
- Adding additional form data with `customFormData`
- JWT authentication for upload/remove requests
- Show confirmation dialog before removing files
- Get total size of selected files
- Sort selected files in the file list
- Open and edit uploaded files from the server
- Convert uploaded images to binary format

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Complete properties, methods, and events reference
- AsyncSettingsModel, ButtonsPropsModel, FilesPropModel
- All event argument types and their fields

## Quick Start Example

Minimal file uploader with async upload (Angular 21+ standalone):

```typescript
import { Component } from '@angular/core';
import { UploaderModule } from '@syncfusion/ej2-angular-inputs';

@Component({
  imports: [UploaderModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <ejs-uploader
      [asyncSettings]="asyncSettings"
      [autoUpload]="false"
      (success)="onSuccess($event)"
      (failure)="onFailure($event)">
    </ejs-uploader>
  `
})
export class AppComponent {
  public asyncSettings = {
    saveUrl: 'https://your-api/upload/save',
    removeUrl: 'https://your-api/upload/remove'
  };

  onSuccess(args: any): void {
    console.log('Upload operation:', args.operation, 'File:', args.file.name);
  }

  onFailure(args: any): void {
    console.error('Upload failed:', args.file.name);
  }
}
```

**CSS Theme Setup** (`styles.css`):
```css
@import 'node_modules/@syncfusion/ej2-base/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import 'node_modules/@syncfusion/ej2-angular-inputs/styles/material3.css';
```

## Common Patterns

### Pattern 1: Auto Upload with Drag-and-Drop
```typescript
// Automatically uploads dropped or browsed files
<ejs-uploader
  [asyncSettings]="asyncSettings"
  [dropArea]="dropElement"
  [multiple]="true"
  (success)="onSuccess($event)">
</ejs-uploader>
```

### Pattern 2: Chunk Upload for Large Files
```typescript
<ejs-uploader
  [asyncSettings]="chunkSettings"
  (chunkSuccess)="onChunkSuccess($event)"
  (chunkFailure)="onChunkFailure($event)">
</ejs-uploader>

// In component:
chunkSettings = {
  saveUrl: 'https://your-api/upload/save',
  removeUrl: 'https://your-api/upload/remove',
  chunkSize: 500000  // 500 KB chunks
};
```

### Pattern 3: Validated Upload (Type + Size)
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  allowedExtensions=".jpg,.png,.pdf"
  [minFileSize]="1024"
  [maxFileSize]="5000000">
</ejs-uploader>
```

### Pattern 4: Preloaded Files
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  [files]="preloadedFiles">
</ejs-uploader>

// In component:
preloadedFiles = [
  { name: 'report', size: 200000, type: '.pdf' },
  { name: 'photo', size: 500000, type: '.jpg' }
];
```

### Pattern 5: JWT-Authenticated Upload
```typescript
<ejs-uploader
  [asyncSettings]="asyncSettings"
  (uploading)="addAuthHeader($event)"
  (removing)="addAuthHeader($event)">
</ejs-uploader>

addAuthHeader(args: any): void {
  args.currentRequest.setRequestHeader('Authorization', `Bearer ${this.token}`);
}
```

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `[asyncSettings]` | AsyncSettingsModel | `{saveUrl:'',removeUrl:''}` | Server save/remove URLs and chunk config |
| `[autoUpload]` | boolean | `true` | Upload immediately on file selection |
| `[multiple]` | boolean | `true` | Allow selecting multiple files |
| `[allowedExtensions]` | string | `''` | Comma-separated allowed extensions (e.g., `.jpg,.png`) |
| `[minFileSize]` | number | `0` | Minimum file size in bytes |
| `[maxFileSize]` | number | `30000000` | Maximum file size in bytes (~28.6 MB) |
| `[files]` | FilesPropModel[] | `[]` | Preloaded files from server |
| `[dropArea]` | string \| HTMLElement | `null` | Custom drop target element or selector |
| `[directoryUpload]` | boolean | `false` | Enable folder/directory upload |
| `[sequentialUpload]` | boolean | `false` | Upload files one at a time |
| `[showFileList]` | boolean | `true` | Show/hide default file list |
| `[template]` | any | `null` | Custom file list item template |
| `[buttons]` | ButtonsPropsModel | `{browse,clear,upload}` | Customize button text/HTML |
| `[enabled]` | boolean | `true` | Enable or disable the component |
| `[cssClass]` | string | `''` | Additional CSS classes on root element |
| `[enableRtl]` | boolean | `false` | Right-to-left rendering |
| `[enableHtmlSanitizer]` | boolean | `true` | Prevent XSS in filenames |
| `[dropEffect]` | DropEffect | `'Default'` | Drag effect: Copy, Move, Link, None |

## Key Events

| Event | When it Fires | Key Args |
|-------|---------------|----------|
| `(selected)` | Files selected or dropped | `filesData`, `cancel`, `modifiedFilesData` |
| `(uploading)` | Before each file upload starts | `fileData`, `currentRequest`, `customFormData`, `cancel` |
| `(success)` | Upload or remove succeeds | `file`, `operation` (`upload`\|`remove`), `event` |
| `(failure)` | Upload or remove fails | `file`, `operation`, `event` |
| `(progress)` | Upload progress | `file`, `event` (loaded, total) |
| `(removing)` | Before file remove request | `filesData`, `postRawFile`, `currentRequest` |
| `(beforeRemove)` | Before remove confirmation | `filesData`, `cancel` |
| `(beforeUpload)` | Before upload process | `fileData`, `customFormData` |
| `(change)` | File list changes | `file` |
| `(clearing)` | Before clear all action | `cancel` |
| `(chunkSuccess)` | Each chunk uploads OK | `chunkIndex`, `totalChunk`, `chunkSize`, `file` |
| `(chunkFailure)` | Each chunk fails | `chunkIndex`, `totalChunk`, `chunkSize`, `file`, `cancel` |
| `(chunkUploading)` | Before each chunk upload | `fileData`, `currentRequest`, `customFormData` |
| `(pausing)` | Chunk upload paused | `file`, `chunkIndex` |
| `(resuming)` | Chunk upload resumed | `file`, `chunkIndex` |
| `(canceling)` | Upload canceled | `file` |
| `(fileListRendering)` | Before each file item renders | `element`, `fileInfo` |
| `(actionComplete)` | All files processed | `fileData` |
| `(created)` | Component initialized | — |

## Key Methods

| Method | Purpose |
|--------|---------|
| `upload(files?, custom?)` | Programmatically start upload for selected or specific files |
| `remove(fileData?, custom?, postRawFile?)` | Remove a file from list or server |
| `cancel(fileData?)` | Cancel an in-progress chunk upload |
| `pause(fileData?, custom?)` | Pause a chunk upload |
| `resume(fileData?, custom?)` | Resume a paused chunk upload |
| `retry(fileData?, fromCanceledStage?, custom?)` | Retry a failed or canceled upload |
| `clearAll()` | Clear all files from the list |
| `getFilesData(index?)` | Get file data array shown in the list |
| `createFileList(fileData)` | Programmatically create file list items |
| `sortFileList(filesData?)` | Sort file list alphabetically |
| `bytesToSize(bytes)` | Convert bytes to human-readable KB/MB string |
| `destroy()` | Destroy the component and detach events |

## Common Use Cases

**Use Case 1: Profile Photo Upload**
- `multiple="false"`, `allowedExtensions=".jpg,.png,.gif,.webp"`, `maxFileSize=5000000`
- Use `selected` event to preview before upload
- Auto upload with progress indicator

**Use Case 2: Document Upload Portal**
- Multiple files, `allowedExtensions=".pdf,.doc,.docx,.xlsx"`
- Chunk upload for large files with pause/resume
- Sequential upload to manage server load

**Use Case 3: Image Gallery Batch Upload**
- Multiple files, directory upload enabled
- Preview thumbnails using `selected` event + FileReader
- Sort by file name before upload

**Use Case 4: Secure File Upload (API-Authenticated)**
- JWT token injected via `uploading` event header
- Custom `customFormData` to pass metadata
- Server validates token before saving

**Use Case 5: Form with Required File**
- `autoUpload=false`, synchronous form submission
- Required attribute validation with `data-required-message`
- Template-driven or reactive form binding

## Next Steps

1. **Getting Started** → Install package and render basic uploader
2. **Async Upload** → Configure save/remove URLs and upload modes
3. **Validation** → Add extension and size constraints
4. **Chunk Upload** → Handle large files with pause/resume
5. **Templates** → Customize file list appearance
6. **Form Integration** → Bind to Angular forms
7. **Advanced Patterns** → JWT auth, programmatic upload, custom UI
8. **API Reference** → Full properties, methods, events list

---

**For detailed implementation, start with [references/getting-started.md](references/getting-started.md)**
