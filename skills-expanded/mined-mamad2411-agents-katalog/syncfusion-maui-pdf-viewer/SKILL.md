---
name: syncfusion-maui-pdf-viewer
description: Implements Syncfusion .NET MAUI SfPdfViewer for cross-platform PDF viewing, navigation, annotations, form filling/validation, text search/selection, e-signatures, redaction, printing, and toolbar/UI customization. Use when working with PDF viewer setup, document annotations, form fields, or signature workflows in MAUI apps.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing .NET MAUI PDF Viewer

A comprehensive skill for implementing and customizing the Syncfusion .NET MAUI PDF Viewer (SfPdfViewer) control. The PDF Viewer provides powerful document viewing and management capabilities including navigation, annotations, form filling, text operations, signatures, redaction, and printing with a built-in customizable toolbar.

## When to Use This Skill

Use this skill when you need to:
- View and navigate PDF documents in .NET MAUI applications
- Load PDFs from file, stream, URL, or Base64
- Add and manage annotations (ink, shapes, stamps, text markups, sticky notes)
- Fill and validate PDF form fields; import/export form data (XFDF, FDF, JSON, XML)
- Search and select text within PDF documents
- Add electronic signatures (handwritten, image-based, text)
- Redact sensitive content permanently
- Print PDF documents with quality settings
- Customize toolbars, appearance, and localization
- Migrate from Xamarin.Forms PDF Viewer to .NET MAUI

## Component Overview

**SfPdfViewer** is a comprehensive PDF viewing and management control for .NET MAUI with these capabilities:

- **Document Management:** Load (file/stream/URL/Base64/picker) with password support, save with flattening, print with quality settings
- **Annotations:** Ink, shapes, stamps, sticky notes, text markups, free text, eraser with full editing support
- **Forms & Text:** All AcroForm types, validation, import/export (XFDF/FDF/JSON/XML), async search, text selection
- **Signatures & Redaction:** Electronic signatures (handwritten/image/text), text/area/page-based redaction
- **Navigation & UI:** Page layouts, zoom, bookmarks, hyperlinks, customizable toolbar (desktop/mobile), localization, RTL, liquid glass effect

## Documentation and Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/basic-sample.md](references/basic-sample.md)
- Installation, NuGet package, and handler registration (ConfigureSyncfusionCore)
- Basic PDF Viewer implementation (XAML & C#), DocumentSource binding
- Loading PDFs from different sources and platform-specific setup

### Document Operations
📄 **Read:** [references/document-operations.md](references/document-operations.md)
- Loading PDFs (file picker, URL, Base64, streams) with password support
- Saving with modifications and annotation flattening
- Printing with quality settings and page range selection

### Annotations
📄 **Read:** [references/annotations.md](references/annotations.md)
- Adding/removing annotations (AddAnnotation, RemoveAnnotation)
- Ink, shapes, stamps, sticky notes, text markups, free text, ink eraser
- Annotation properties (color, opacity, bounds, stroke, rotation) and events

### Form Fields
📄 **Read:** [references/form-fields.md](references/form-fields.md)
- Viewing, accessing, and filling all AcroForm field types
- Field validation, import/export (XFDF, FDF, JSON, XML), flattening
- Form field events and interaction handling

### Navigation & Viewing
📄 **Read:** [references/viewing.md](references/viewing.md)
- Page navigation (GoToPage, PageNumber), layout modes (Single, Continuous)
- Bookmarks, hyperlinks, zoom (ZoomMode, ZoomFactor), FitMode options
- Coordinate conversion (PageToClient, ClientToPage)

### Text Search
📄 **Read:** [references/text-search.md](references/text-search.md)
- Async text search (SearchTextAsync), match navigation (GoToNextMatch, GoToPreviousMatch)
- Search highlighting, case-sensitive/whole-word options, custom search UI

### Text Selection
📄 **Read:** [references/text-selection.md](references/text-selection.md)
- Enabling text selection, SelectedText property, clipboard copy
- Selection customization (colors, opacity), TextSelectionChanged event

### Electronic Signatures
📄 **Read:** [references/electronic-signature.md](references/electronic-signature.md)
- Handwritten, image-based, and text signatures
- Signature field management, appearance customization, validation workflows

### Redaction
📄 **Read:** [references/redaction.md](references/redaction.md)
- Text/area/page-based redaction (RedactText, RedactArea, RedactPage)
- Permanent content removal, appearance customization, saving redacted documents

### Toolbar Customization
📄 **Read:** [references/toolbar-customization.md](references/toolbar-customization.md)
- Desktop vs mobile toolbar layouts
- Add/remove/hide/reorder toolbar items, AnnotationToolbarItemClicked event
- Custom toolbar creation and visibility control

### UI Settings & Localization
📄 **Read:** [references/ui-settings.md](references/ui-settings.md)
- Localization, FlowDirection for RTL layouts, culture-specific formatting
- Liquid glass effect, theme customization, platform-specific UI adjustments

### Gesture Events & Interaction
📄 **Read:** [references/gesture-events.md](references/gesture-events.md)
- DocumentTapped event with PageNumber and Position
- Touch gesture handling, custom interactions, event-driven workflows

### Migration from Xamarin
📄 **Read:** [references/migration-xamarin-to-maui.md](references/migration-xamarin-to-maui.md)
- API differences, property/method mappings, namespace changes
- Handler registration differences, breaking changes, migration checklist
