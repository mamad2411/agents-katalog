---
name: syncfusion-angular-image-editor
description: Implement feature-rich image editing in Angular applications using Syncfusion Image Editor. Use this skill whenever user mentions editing images, adding annotations, applying filters, cropping, transforming, or manipulating images in Angular. Covers installation, all annotation types (text, shapes, freehand), transformations (rotate, flip, zoom), filtering, frame application, redaction, open/save functionality, undo/redo, toolbar customization, accessibility, and advanced features like z-ordering and dialog integration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Implementing Syncfusion Angular Image Editor

The Syncfusion Angular Image Editor component provides a comprehensive, feature-rich solution for image editing and annotation. It allows developers to integrate professional image editing capabilities directly into Angular applications, supporting a wide range of editing operations including annotations, transformations, filtering, and more.

## Component Overview

The Image Editor is a powerful, standalone component that provides:

- **Complete image editing suite** with 20+ built-in tools
- **Flexible annotation system** supporting text, shapes, and freehand drawing
- **Advanced transformations** including rotate, flip, straighten, zoom, and pan
- **Professional image filters** (cold, warm, chrome, sepia, invert, grayscale, etc.)
- **Fine-tuning controls** for brightness, contrast, saturation, hue, exposure, blur, and opacity
- **Frame application** with multiple frame types and customization options
- **Redaction tools** for privacy protection (blur and pixelate)
- **Multiple input/output options** including local files, base64, blob, file uploader, and file manager
- **Rich undo/redo history** (16 steps maximum)
- **Fully customizable toolbars** with contextual and quick-access options
- **Z-order management** for annotation layering
- **Mobile-friendly** with touch gestures (pinch zoom)
- **Full accessibility support** including WCAG 2.2, keyboard navigation, and screen reader compatibility
- **Multi-language support** with 150+ localization keywords

## Documentation and Navigation Guide

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Dependencies and module imports
- Basic component implementation
- CSS imports and theme configuration
- First render and initialization

### Annotations & Drawing
📄 **Read:** [references/annotations.md](references/annotations.md)
- Text annotations with formatting (bold, italic, underline, strikethrough)
- Multiline text support
- Font family and text color customization
- Freehand drawing with stroke adjustment
- Shape annotations (rectangles, ellipses, lines, arrows, paths)
- Image annotations and watermarking
- Deleting and managing annotations
- Shape styling and default customization

### Selection & Cropping
📄 **Read:** [references/selection-and-cropping.md](references/selection-and-cropping.md)
- Custom selection shapes
- Square and circle selections
- Aspect ratio selections (2:3, 3:2, 4:3, 16:9, etc.)
- Cropping selected regions
- Selection event handling
- Locking selection areas
- Custom ratio selection during cropping

### Image Transformations
📄 **Read:** [references/transform.md](references/transform.md)
- Rotating images (clockwise/counterclockwise)
- Flipping horizontally and vertically
- Straightening images with fine adjustments
- Zooming in/out with min/max zoom levels
- Panning functionality and events
- Transform event handlers
- Keyboard shortcuts for transformations

### Filtering & Fine-tuning
📄 **Read:** [references/filter-and-finetune.md](references/filter-and-finetune.md)
- Applying image filters (Cold, Warm, Chrome, Sepia, Invert, Grayscale, Black & White)
- Fine-tuning brightness and contrast
- Adjusting saturation levels
- Hue adjustments
- Exposure control
- Blur effects
- Opacity adjustments
- Filter and finetune event handling

### Frame Application
📄 **Read:** [references/frames.md](references/frames.md)
- Frame types (Mat, Bevel, Line, Hook, Inset)
- Frame color customization
- Gradient color support
- Frame size and offset configuration
- Border radius for line-type frames
- Frame line styles (solid, dashed, dotted)
- Frame changing events

### Redaction & Privacy
📄 **Read:** [references/redaction.md](references/redaction.md)
- Drawing redactions (blur and pixelate types)
- Customizing redaction properties
- Selecting specific redactions
- Updating redaction settings
- Deleting redactions
- Retrieving redaction details

### Open & Save Operations
📄 **Read:** [references/open-and-save.md](references/open-and-save.md)
- Opening images from multiple sources (local, base64, blob, uploader, file manager, treeview)
- Saving with format selection (PNG, JPEG, SVG, WEBP, BMP)
- Image quality control for JPEG format
- Exporting as different formats
- Converting to base64, byte arrays, and blob
- Watermark application during open/save
- Custom save dialogs and server uploads
- Image settings for custom dimensions

### Undo & Redo Operations
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- Implementing undo functionality
- Implementing redo functionality
- Understanding history limitations (16 steps)
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y)

### Toolbar Customization
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items and their functions
- Adding custom toolbar items
- Showing/hiding toolbar
- Enabling/disabling specific items
- Contextual toolbar customization
- Toolbar templates for complete customization
- Toolbar events (toolbarCreated, toolbarItemClicked, toolbarUpdating)

### Quick Access Toolbar
📄 **Read:** [references/quick-access-toolbar.md](references/quick-access-toolbar.md)
- Quick access toolbar visibility control
- Adding custom items to quick access toolbar
- Customizing annotation-specific actions
- Event handling for toolbar operations

### Z-Order & Layering
📄 **Read:** [references/z-order.md](references/z-order.md)
- Bringing annotations forward
- Sending annotations backward
- Bringing annotations to front
- Sending annotations to back
- Managing multiple annotation layers

### Accessibility & Compliance
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 compliance standards
- Keyboard shortcuts and navigation
- Screen reader support
- Color contrast standards
- Mobile accessibility support
- RTL (Right-to-Left) support

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Complete properties reference with types and defaults
- All methods with parameters and return types
- All events with descriptions
- Event arguments reference
- Filter, finetune, shape, and frame types
- Selection shapes and export formats
- Usage examples for properties and events

### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Setting locale configuration
- Customizing UI text in multiple languages
- Translation keywords and values
- Supporting international audiences

### Image Restrictions & Validation
📄 **Read:** [references/image-restrictions.md](references/image-restrictions.md)
- Specifying allowed file extensions
- Setting minimum file size limits
- Setting maximum file size limits
- Validation error messages
- Upload settings configuration

### Image Resizing
📄 **Read:** [references/resize.md](references/resize.md)
- Resizing image dimensions
- Aspect ratio preservation
- Resize event handling
- Custom dimension specifications

### End-User Capabilities
📄 **Read:** [references/end-user-capabilities.md](references/end-user-capabilities.md)
- User-facing features and workflows
- Opening images through UI
- Zoom operations via toolbar, pinch, mouse wheel, keyboard
- Panning functionality
- Toolbar-based transformations
- Annotation creation and editing
- Filter and fine-tune application
- Save and export workflows

### How-To Guides

📄 **Read:** [references/clear-image.md](references/clear-image.md) - Clearing editor state for dialog reuse

📄 **Read:** [references/fit-to-width-height.md](references/fit-to-width-height.md) - Dynamic zoom fitting

📄 **Read:** [references/render-in-dialog.md](references/render-in-dialog.md) - Modal dialog integration

📄 **Read:** [references/reset-image.md](references/reset-image.md) - Reverting to original state

## Quick Start Example

```typescript
import { Component } from '@angular/core';
import { ImageEditorModule } from '@syncfusion/ej2-angular-image-editor';

@Component({
  imports: [ImageEditorModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div style="width: 550px; height: 350px;">
      <ejs-imageeditor 
        #imageEditor
        [toolbar]="['Open', 'Undo', 'Redo', 'Crop', 'Annotate', 'Finetune', 'Filter', 'Resize', 'Save', 'Reset']"
      ></ejs-imageeditor>
    </div>
    <button (click)="openImage()">Open Image</button>
  `
})
export class AppComponent {
  @ViewChild('imageEditor') imageEditor: any;

  openImage() {
    this.imageEditor.open('path-to-image.png');
  }

  addAnnotation() {
    this.imageEditor.drawText(50, 50, 'Sample Text', 'Arial', 12, false, false, '#000000');
  }

  rotateImage() {
    this.imageEditor.rotate(90);
  }

  saveImage() {
    this.imageEditor.export('edited-image', 'png');
  }
}
```

## Common Patterns

### Pattern 1: Open Image & Add Annotations
```typescript
// Open image from file
this.imageEditor.open('image.png');

// Add text annotation
this.imageEditor.drawText(100, 100, 'Important', 'Arial', 16, true, false, '#FF0000');

// Add rectangle
this.imageEditor.drawRectangle(50, 50, 200, 150, 2, '#0000FF', '#FFFFFF');

// Add freehand drawing
this.imageEditor.freehandDraw();
```

### Pattern 2: Apply Filters & Fine-tuning
```typescript
// Apply filter
this.imageEditor.applyImageFilter('Sepia');

// Fine-tune brightness
this.imageEditor.finetuneImage('Brightness', 50);

// Fine-tune contrast
this.imageEditor.finetuneImage('Contrast', -30);

// Fine-tune saturation
this.imageEditor.finetuneImage('Saturation', 40);
```

### Pattern 3: Crop & Transform
```typescript
// Select region for cropping
this.imageEditor.select('Custom', 50, 50, 300, 200);

// Crop the selected region
this.imageEditor.crop();

// Rotate after cropping
this.imageEditor.rotate(90);

// Flip horizontally
this.imageEditor.flip('Horizontal');
```

### Pattern 4: Customized Toolbar
```typescript
toolbar: [
  'Open',
  'Undo',
  'Redo',
  'Crop',
  'RotateLeft',
  'RotateRight',
  'HorizontalFlip',
  'VerticalFlip',
  'Annotate',
  'Finetune',
  'Filter',
  'Frame',
  'Redact',
  'Resize',
  'Save',
  'Reset'
];
```

### Pattern 5: Save with Different Formats
```typescript
// Save as PNG (default)
this.imageEditor.export('myImage', 'png');

// Save as JPEG with quality
this.imageEditor.export('myImage', 'jpeg', 90);

// Get base64 data
const base64Data = this.imageEditor.getImageData();

// Save as blob
this.imageEditor.getImageData().then(data => {
  const blob = this.dataURLtoBlob(data);
  // Send to server
});
```

## Key Props & Configuration

| Property | Type | Description | When to Use |
|----------|------|-------------|------------|
| `toolbar` | array | List of toolbar items to display | Customize visible tools |
| `toolbarTemplate` | template | Custom template for entire toolbar | Complete toolbar redesign |
| `uploadSettings` | object | File validation rules (extensions, size) | Restrict upload formats/sizes |
| `zoomSettings` | object | Min/max zoom factor configuration | Control zoom boundaries |
| `fontFamily` | array | Additional font families for text | Add custom fonts |
| `locale` | string | Language for UI text | Multi-language support |
| `height` | string/number | Component height | Layout sizing |
| `width` | string/number | Component width | Layout sizing |
| `showQuickAccessToolbar` | boolean | Show quick access toolbar | Control quick toolbar visibility |

## Common Use Cases

1. **Photo Editing App** - Full-featured image editor with all tools
2. **Document Annotation** - Highlight, mark, and comment on documents
3. **Social Media Content** - Apply filters, frames, and text to images
4. **Privacy Protection** - Redact sensitive information before sharing
5. **Profile Picture Editor** - Crop, rotate, and apply filters to avatars
6. **Real Estate Listings** - Rotate, frame, and annotate property photos
7. **Feedback & Collaboration** - Annotate screenshots for team communication
8. **Template Design** - Layer annotations with z-order for custom layouts
9. **Form Image Capture** - Crop, rotate, and optimize mobile camera captures
10. **Watermark Application** - Add text and image watermarks for branding

## Reference Files

All detailed documentation is organized by feature in the `references/` folder. Each reference file is self-contained and covers specific functionality in depth.

See individual reference files for code examples, event handling, and advanced configurations.
