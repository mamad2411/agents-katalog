---
name: syncfusion-javascript-pdf
description: "Provides comprehensive guidance for implementing the Syncfusion JavaScript PDF library (@syncfusion/ej2-pdf) to create and manipulate PDF documents programmatically across TypeScript, JavaScript, Angular, React, Vue, and ASP.NET platforms. Use this when working with PDF creation, form filling, annotations, document merging/splitting, text or image extraction, or digital signatures."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Processing PDF Documents

A comprehensive skill for creating, reading, and manipulating PDF documents programmatically using the Syncfusion JavaScript PDF library. This library provides seamless integration for TypeScript, JavaScript, Angular, React, Vue, ASP.NET Core, and ASP.NET MVC applications.

## When to Use This Skill

Use this skill when the user needs to:

- **Create PDF documents** from scratch with text, images, shapes, and other graphical elements
- **Manipulate existing PDFs** by adding content, modifying properties, or extracting data
- **Add interactive features** such as forms, annotations, bookmarks, and hyperlinks
- **Secure PDFs** with digital signatures
- **Merge or split** PDF documents for document management workflows
- **Extract content** including text and images from existing PDFs
- **Add watermarks** (text or image-based) for branding or security
- **Manage document informations** including title, author, subject, keywords, and dates
- **Work with PDF layers** for complex document structures
- **Implement templates** for consistent document generation

**Platform Support:** TypeScript, JavaScript, Angular, React, Vue, ASP.NET Core, ASP.NET MVC

## Library Overview

The Syncfusion JavaScript PDF library (`@syncfusion/ej2-pdf`) is a powerful, high-performance class library that enables:

- Creating PDF documents from scratch without Adobe Acrobat
- Loading, editing, and saving existing PDF files
- Opening password-protected PDF documents
- Adding text, images, shapes, and graphical elements
- Interactive components (bookmarks, annotations, form fields)
- Document operations (merge, split, flatten)
- Content extraction (text, images)
- Security features (digital signatures, redaction)

**Key Classes:**
- `PdfDocument` - Main document object
- `PdfPage` - Individual pages
- `PdfGraphics` - Drawing surface for content
- `PdfFont`, `PdfBitmap`, `PdfBrush` - Content elements

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use this reference when the user needs to:
- Install the `@syncfusion/ej2-pdf` package
- Set up the library for TypeScript, JavaScript, Angular, React, Vue, or ASP.NET
- Understand dependencies and requirements
- Create their first PDF document
- Learn basic save and export operations

### Document Creation & Settings

📄 **Read:** [references/document-settings.md](references/document-settings.md)

Use this reference for:
- Creating `PdfDocument` instances
- Configuring page settings (size, orientation, margins, rotation)
- Setting document properties (title, author, subject, keywords, creation/modification dates)
- Enabling incremental updates
- Flattening annotations and form fields

📄 **Read:** [references/pdf-pages.md](references/pdf-pages.md)

Use this reference for:
- Adding pages to documents
- Page manipulation and navigation
- Page sections with different settings
- Managing page collections

### Content Elements

📄 **Read:** [references/text-rendering.md](references/text-rendering.md)

Use this reference when adding text:
- Drawing text with `drawString()` method
- Font types (Standard, TrueType, CJK fonts)
- Font styles, sizes, and formatting
- Text layout and wrapping
- Graphics state management (save/restore)
- Text positioning and bounds

📄 **Read:** [references/images.md](references/images.md)

Use this reference for image operations:
- Adding JPEG and PNG images
- Using `PdfBitmap` class
- Image positioning and sizing
- Inserting images into existing documents
- Base64 and Uint8Array image formats
- Clipping and graphics transformations

📄 **Read:** [references/shapes.md](references/shapes.md)

Use this reference for drawing shapes:
- Rectangles, circles, ellipses, lines
- Complex paths and curves
- Pens and brushes for styling
- Fill and stroke operations
- Graphics transformations (translate, rotate, scale)

📄 **Read:** [references/lists.md](references/lists.md)

Use this reference for creating lists:
- Ordered and unordered lists
- Nested list structures
- Custom list markers
- List formatting options

📄 **Read:** [references/templates.md](references/templates.md)

Use this reference for reusable content:
- Creating page templates
- Dynamic content stamping
- Template positioning and layout
- Reusing content across pages

### Interactive Features

📄 **Read:** [references/annotations.md](references/annotations.md)

Use this reference for annotations:
- Annotation types (free text, ink, stamp, etc.)
- Adding and configuring annotations
- Annotation properties and appearance
- Flattening annotations to static content

📄 **Read:** [references/bookmarks.md](references/bookmarks.md)

Use this reference for navigation:
- Creating document bookmarks
- Nested bookmark hierarchies
- Bookmark navigation and linking
- Modifying existing bookmarks

📄 **Read:** [references/form-fields.md](references/form-fields.md)

Use this reference for interactive forms:
- Form field types (text, checkbox, radio, dropdown, button)
- Adding and configuring form fields
- Field validation and properties
- Filling form data programmatically
- Importing/exporting form data
- Flattening forms to remove interactivity

📄 **Read:** [references/hyperlinks.md](references/hyperlinks.md)

Use this reference for linking:
- Adding web hyperlinks
- Document internal navigation links
- Link annotations and appearance
- Navigation actions

### Document Operations

📄 **Read:** [references/merge-documents.md](references/merge-documents.md)

Use this reference for merging:
- Combining multiple PDF files
- Importing pages from other documents
- Preserving bookmarks during merge
- Merging workflows

📄 **Read:** [references/split-documents.md](references/split-documents.md)

Use this reference for splitting:
- Splitting PDFs by page range
- Extracting specific pages
- Creating separate documents from pages

📄 **Read:** [references/watermarks.md](references/watermarks.md)

Use this reference for watermarks:
- Text watermarks
- Image watermarks
- Watermark positioning and layout
- Opacity and rotation settings

📄 **Read:** [references/layers.md](references/layers.md)

Use this reference for layer management:
- Creating PDF layers (Optional Content Groups)
- Layer visibility control
- Adding content to layers
- Removing or flattening layers

### Data Extraction

📄 **Read:** [references/text-extraction.md](references/text-extraction.md)

Use this reference for extracting text:
- Extracting text from PDF pages
- Text extraction layouts
- Text bounds and positioning
- Extracting from specific regions

📄 **Read:** [references/image-extraction.md](references/image-extraction.md)

Use this reference for extracting images:
- Extracting images from PDF documents
- Image data formats
- Saving extracted images
- Required package: `@syncfusion/ej2-pdf-data-extract`

### Security & Protection

📄 **Read:** [references/digital-signatures.md](references/digital-signatures.md)

Use this reference for security:
- Adding digital signatures
- Certificate-based signing
- Signature appearance customization
- Validation and verification
- Timestamp servers

📄 **Read:** [references/redaction.md](references/redaction.md)

Use this reference for content removal:
- Redacting sensitive text
- Shape redaction
- Redaction annotations
- Permanent content removal

## Quick Start Example

```typescript
import { PdfDocument, PdfPage, PdfGraphics, PdfFont, PdfFontFamily, PdfFontStyle, PdfBrush } from '@syncfusion/ej2-pdf';

// Create a new PDF document
let document: PdfDocument = new PdfDocument();

// Add a page
let page: PdfPage = document.addPage();

// Get graphics from the page
let graphics: PdfGraphics = page.graphics;

// Set font
let font: PdfFont = document.embedFont(PdfFontFamily.helvetica, 20, PdfFontStyle.regular);

// Create a brush
let brush = new PdfBrush({r: 0, g: 0, b: 0});

// Draw text
graphics.drawString('Hello World!', font, {x: 20, y: 20, width: 200, height: 50}, brush);

// Save the document
document.save('output.pdf');

// Clean up
document.destroy();
```

## Common Workflows

### Create Invoice or Report

1. Create document with custom page settings
2. Add company logo (image)
3. Add header text with formatting
4. Create tables with borders (shapes + text)
5. Add totals and footer
6. Save and download

**Start with:** [references/getting-started.md](references/getting-started.md), then [references/text-rendering.md](references/text-rendering.md) and [references/images.md](references/images.md)

### Fill and Flatten PDF Form

1. Load existing PDF document with form fields
2. Fill form fields programmatically
3. Flatten form to make it non-editable
4. Save modified document

**Start with:** [references/form-fields.md](references/form-fields.md)

### Extract Data from PDF

1. Load existing PDF document
2. Extract text from specific pages
3. Extract images if needed
4. Parse and process extracted data

**Start with:** [references/text-extraction.md](references/text-extraction.md) and [references/image-extraction.md](references/image-extraction.md)

### Merge Multiple PDFs

1. Create main document
2. Import pages from source documents
3. Optionally add bookmarks for sections
4. Save combined document

**Start with:** [references/merge-documents.md](references/merge-documents.md)

### Add Digital Signature

1. Load document or create new one
2. Configure digital signature with certificate
3. Set signature appearance and position
4. Save signed document

**Start with:** [references/digital-signatures.md](references/digital-signatures.md)

## Platform-Specific Considerations

### TypeScript/JavaScript
- Direct import from `@syncfusion/ej2-pdf`
- Browser or Node.js environment
- File saving via browser download or Node.js fs

### Angular/React/Vue
- Component-based integration
- Handle file downloads in component lifecycle
- State management for document generation

### ASP.NET Core/MVC
- Server-side PDF generation
- Return PDF as file result
- Memory stream handling

For platform-specific setup details, see [references/getting-started.md](references/getting-started.md)

## Key Props and Methods

### PdfDocument
- `addPage(settings?)` - Add new page
- `getPage(index)` - Access existing page
- `save(filename)` - Save document
- `destroy()` - Clean up resources
- `embedFont()` - Load font for use

### PdfGraphics
- `drawString(text, font, bounds, brush)` - Draw text
- `drawImage(image, bounds)` - Draw image
- `drawRectangle(pen, bounds)` - Draw rectangle
- `save()` - Save graphics state
- `restore(state)` - Restore graphics state

### PdfPage
- `graphics` - Get drawing surface
- `size` - Get page dimensions
- `rotation` - Get/set rotation

For complete API details, refer to the specific reference files.

## Common Use Cases

1. **Automated Report Generation** - Create branded reports with charts, tables, and formatted text
2. **Invoice Creation** - Generate professional invoices with line items and totals
3. **Certificate Generation** - Create certificates with templates and custom text
4. **Form Filling** - Programmatically fill PDF forms for bulk processing
5. **Document Assembly** - Merge multiple PDFs into consolidated documents
6. **Data Extraction** - Extract text and images from PDFs for processing
7. **Digital Signing** - Apply digital signatures for document authentication
8. **Watermarking** - Add branding or security watermarks to documents
9. **Redaction** - Remove sensitive information before sharing
10. **Archive Creation** - Convert documents to PDF/A format for long-term storage

## Troubleshooting Tips

- **Missing fonts**: Ensure font is embedded before use with `document.embedFont()`
- **Image not displaying**: Verify image format (JPEG/PNG) and data (base64/Uint8Array)
- **Large files**: Use incremental updates or split operations
- **Memory issues**: Call `document.destroy()` after saving
- **Extract features not working**: Install `@syncfusion/ej2-pdf-data-extract` package

## Related Resources

- Package: `@syncfusion/ej2-pdf`
- Add-on: `@syncfusion/ej2-pdf-data-extract` (for extraction features)
- Dependencies: `@syncfusion/ej2-compression`, `@syncfusion/ej2-base`
