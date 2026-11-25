---
name: polaris-drop-zone
description: Shopify Polaris Drop zone component. Use this skill when building file uploads, drag-and-drop areas, image/document uploads. Lets users upload files by dragging and dropping or using a traditional button.
---

# Drop zone

## When to use

Let users upload files by dragging and dropping files into an area or activating a button. Use to allow merchants to upload files conveniently.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | any | - | Child elements to render |
| `id` | string | - | ID for file input |
| `label` | React.ReactNode | - | Label for file input |
| `labelAction` | Action | - | Action added to label |
| `labelHidden` | boolean | false | Visually hide label |
| `accept` | string | - | Allowed file types |
| `type` | 'file' \| 'image' \| 'video' | 'file' | Whether file, image, or video |
| `active` | boolean | false | Sets active state |
| `error` | boolean | false | Sets error state |
| `outline` | boolean | true | Displays outline border |
| `overlay` | boolean | true | Displays overlay on hover |
| `overlayText` | string | - | Text in overlay |
| `errorOverlayText` | string | - | Text in overlay on error |
| `allowMultiple` | boolean | true | Allow multiple files at once |
| `disabled` | boolean | false | Sets disabled state |
| `dropOnPage` | boolean | false | Allow file drop anywhere on page |
| `openFileDialog` | boolean | false | Default file dialog state |
| `variableHeight` | boolean | false | Child content can adjust height |
| `customValidator` | (file: File) => boolean | - | Custom file validations |
| `onClick` | (event: React.MouseEvent) => void | - | Click callback |
| `onDrop` | (files, acceptedFiles, rejectedFiles) => void | - | Drop callback |
| `onDropAccepted` | (acceptedFiles) => void | - | Accepted files callback |
| `onDropRejected` | (rejectedFiles) => void | - | Rejected files callback |
| `onDragOver` | () => void | - | Drag over callback |
| `onDragEnter` | () => void | - | Drag enter callback |
| `onDragLeave` | () => void | - | Drag leave callback |
| `onFileDialogClose` | () => void | - | File dialog close callback |

## Examples

```jsx
import { DropZone, LegacyStack, Thumbnail, Text } from '@shopify/polaris';
import { NoteIcon } from '@shopify/polaris-icons';
import { useState, useCallback } from 'react';

function DropZoneExample() {
  const [files, setFiles] = useState([]);

  const handleDropZoneDrop = useCallback(
    (_dropFiles, acceptedFiles, _rejectedFiles) =>
      setFiles((files) => [...files, ...acceptedFiles]),
    []
  );

  const validImageTypes = ['image/gif', 'image/jpeg', 'image/png'];

  const fileUpload = !files.length && <DropZone.FileUpload />;

  const uploadedFiles = files.length > 0 && (
    <div style={{ padding: '0' }}>
      <LegacyStack vertical>
        {files.map((file, index) => (
          <LegacyStack alignment="center" key={index}>
            <Thumbnail
              size="small"
              alt={file.name}
              source={
                validImageTypes.includes(file.type)
                  ? window.URL.createObjectURL(file)
                  : NoteIcon
              }
            />
            <div>
              {file.name}
              <Text variant="bodySm" as="p">
                {file.size} bytes
              </Text>
            </div>
          </LegacyStack>
        ))}
      </LegacyStack>
    </div>
  );

  return (
    <DropZone onDrop={handleDropZoneDrop}>
      {uploadedFiles}
      {fileUpload}
    </DropZone>
  );
}
```

## Best practices

- Inform merchants when files can't be uploaded
- Use validation errors on drag to detect issues
- Use banner component for server errors
- Provide feedback when uploading begins
- Allow dropOnPage for convenience
- Use DropZone.FileUpload for traditional upload button

## Content guidelines

- Validation errors: explicit, sentence case, concise
- Server errors: displayed as banner with file names, describe why and what to change

## Accessibility

- Built on native HTML `<input type="upload">`
- Includes visual button and drag-and-drop area
- Keyboard: Tab to focus, Enter/Space to activate

## Related components

- Banner: for upload error context
- Spinner: for upload progress feedback
