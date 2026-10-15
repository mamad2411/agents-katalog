---
name: syncfusion-react-uploader
description: Implement the Syncfusion React Uploader (UploaderComponent) for file upload scenarios. Use this when working with file uploads, drag-and-drop uploads, chunk or resumable uploads, file validation, or async upload configuration. This skill covers asyncSettings, preloaded files, upload templates, JWT-secured uploads, and form integration.
metadata:
  author: "Syncfusion Inc"
  category: "Inputs"
  version: "33.1.44"
---

# Implementing Syncfusion React Uploader

The Syncfusion React **UploaderComponent** provides a rich file upload control with async upload, drag-and-drop, chunk upload with pause/resume/cancel, validation, templates, form integration, and accessibility support.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup for React
- License registration
- Basic `UploaderComponent` usage in JSX/TSX
- CSS theme imports
- Drop area configuration
- Success and failure event handling

### Asynchronous Upload
📄 **Read:** [references/async-upload.md](references/async-upload.md)
- `asyncSettings` with `saveUrl` and `removeUrl`
- Multiple vs. single file upload (`multiple`)
- Auto upload vs. manual upload (`autoUpload`)
- Sequential upload (`sequentialUpload`)
- Preloaded files (`files` property)
- Adding custom HTTP headers via `uploading`/`removing` events
- Server-side save/remove action examples

### Chunk Upload
📄 **Read:** [references/chunk-upload.md](references/chunk-upload.md)
- Enabling chunk upload with `asyncSettings.chunkSize`
- Retry configuration (`retryCount`, `retryAfterDelay`)
- Pause and resume chunked uploads (`pause`, `resume` methods)
- Cancel uploads (`cancel` method)
- `chunkSuccess` and `chunkFailure` events
- Server-side chunk handling (C#)

### Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Allowed file extensions (`allowedExtensions`)
- File size limits (`minFileSize`, `maxFileSize`)
- Maximum file count using `selected` event
- Duplicate file prevention
- Drag-and-drop image validation

### File Sources
📄 **Read:** [references/file-source.md](references/file-source.md)
- Clipboard paste upload
- Directory/folder upload (`directoryUpload`)
- Drag-and-drop with custom drop area (`dropArea`)
- Customizing drop area appearance

### Templates and Customization
📄 **Read:** [references/template-customization.md](references/template-customization.md)
- File list `template` property
- Custom upload UI with `showFileList: false`
- Customizing action buttons (`buttons` property)
- Progress bar customization
- Hiding the default drop area
- Style and appearance overrides

### Advanced How-To Scenarios
📄 **Read:** [references/advanced-how-to.md](references/advanced-how-to.md)
- Programmatic file upload (`upload` method, `getFilesData`)
- Invisible/background upload
- Image preview before uploading
- Resize images before upload
- Sort selected files
- Check file size / MIME type before upload
- Confirm dialog before file removal
- Open/edit uploaded files
- Trigger file browser from external button
- Convert uploaded image to binary
- JWT authentication for secure upload
- Form support (HTML form, template-driven, reactive)
- Localization (custom locale strings)
- Accessibility and keyboard navigation

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- All properties (`allowedExtensions`, `asyncSettings`, `autoUpload`, `buttons`, `cssClass`, `directoryUpload`, `dropArea`, `dropEffect`, `enabled`, `files`, `htmlAttributes`, `locale`, `maxFileSize`, `minFileSize`, `multiple`, `sequentialUpload`, `showFileList`, `template`, and more)
- All methods (`upload`, `remove`, `cancel`, `pause`, `resume`, `retry`, `clearAll`, `getFilesData`, `bytesToSize`, `createFileList`, `sortFileList`)
- All events (`uploading`, `success`, `failure`, `selected`, `removing`, `change`, `progress`, `chunkSuccess`, `chunkFailure`, `chunkUploading`, `actionComplete`, `beforeRemove`, `beforeUpload`, `canceling`, `clearing`, `fileListRendering`, `pausing`, `resuming`, `created`)

## Quick Start Example

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSuccess = (args: any) => {
    console.log('Upload operation:', args.operation, 'File:', args.file.name);
  };

  const onFailure = (args: any) => {
    console.error('Upload failed:', args.file.name);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      autoUpload={false}
      success={onSuccess}
      failure={onFailure}
    />
  );
}
```

## Common Patterns

### Auto Upload with Validation
```tsx
<UploaderComponent
  asyncSettings={{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }}
  allowedExtensions=".pdf,.doc,.docx"
  maxFileSize={5000000}
  multiple={true}
/>
```

### Manual Upload with Custom Buttons
```tsx
<UploaderComponent
  asyncSettings={{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }}
  autoUpload={false}
  buttons={{ browse: 'Choose File', clear: 'Clear All', upload: 'Upload All' }}
/>
```

### Chunk Upload for Large Files
```tsx
<UploaderComponent
  asyncSettings={{
    saveUrl: '/api/upload/save',
    removeUrl: '/api/upload/remove',
    chunkSize: 500000   // 500 KB chunks
  }}
/>
```

## Key Decision Guide

| Need | Property/Event |
|---|---|
| Server URLs | `asyncSettings.saveUrl` + `asyncSettings.removeUrl` |
| Auto vs manual upload | `autoUpload` (default: `true`) |
| Large file upload | `asyncSettings.chunkSize` |
| Restrict file types | `allowedExtensions` |
| Limit file size | `maxFileSize` / `minFileSize` |
| Preload files from server | `files` prop |
| Upload one at a time | `sequentialUpload: true` |
| Entire folder upload | `directoryUpload: true` |
| Custom drop target | `dropArea` |
| Custom file list UI | `template` or `showFileList: false` |
| Add auth headers | `uploading` event → `args.currentRequest.setRequestHeader()` |
| Send extra form data | `uploading` event → `args.customFormData` |
