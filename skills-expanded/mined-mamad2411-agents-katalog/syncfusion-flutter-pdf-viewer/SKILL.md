---
name: syncfusion-flutter-pdf-viewer
description: Create sample code using Syncfusion Flutter SfPdfViewer. Generate Dart/Flutter code for embedding, configuring, and loading PDF documents.
compatibility: Flutter 3.x+, syncfusion_flutter_pdfviewer
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Syncfusion Flutter SfPdfViewer – UI Sample Generator

## Generate Dart Code for the User's Project *(default)*

**Trigger keywords:** "how to", "add pdfviewer", "code sample", "show me", "example", "snippet", "integrate", "widget", "create sample", "flutter pdfviewer".

**Purpose:** Scaffold a ready-to-run Flutter project with `syncfusion_flutter_pdfviewer` integrated **and** generate the requested feature code inside it — all in one pass.

**Workflow:**

### Step 1 – Ask Clarifying Questions (once, upfront)
Before doing anything else, ask the user:
1. **Project target:** Does a Flutter project already exist, or should a new one be created?
2. **File placement:** Should the generated code go into an existing file (e.g., `main.dart`) or a new Dart file (e.g., `pdf_viewer_sample.dart`)?
3. **Platform:** Is the app targeting mobile, desktop, or web? *(Only needed to decide whether the web `index.html` step is required.)*

### Step 2 – Create a New Flutter Project *(skip if project already exists)*
Run in the terminal:
```bash
flutter create pdf_viewer_app
cd pdf_viewer_app
```

### Step 3 – Add the Syncfusion Dependency *(skip if already present in `pubspec.yaml`)*
Add under `dependencies` in `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  syncfusion_flutter_pdfviewer: ^xx.x.xx
```
Then run:
```bash
flutter pub get
```

### Step 4 – (Web only) Update `web/index.html`
If the target platform is web, add the PdfJs script inside the `<body>` tag of `web/index.html`:
```html
<script type="module" async>
  import * as pdfjsLib from 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.min.mjs';
  pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.min.mjs";
</script>
```

### Step 5 – Build and Write the Dart Code
1. Start with `references/basic-sample.md` as the base template.
2. Identify the feature(s) requested and merge the relevant snippets from `references/*.md` into the base.
3. Follow these code-generation rules:
   - Use code **exactly** as shown in the reference — do not alter API usage.
   - Add only the APIs required by the request; do not include extras.
   - Always initialise `PdfViewerController` in `initState()` when controller-based APIs are used.
4. Write the final code to the file chosen in Step 1:
   - **Existing file** (e.g., `main.dart`): use the edit tool to insert or replace code.
   - **New Dart file** (e.g., `pdf_viewer_sample.dart`): use the create file tool to create it.
   - **Never** display the code only as a code block — always write it to the file using the appropriate tool.

### Step 6 – Run the App
```bash
flutter run
```

**Notes:**
- Use the latest stable version of the package from [pub.dev](https://pub.dev/packages/syncfusion_flutter_pdfviewer).

---

### Code References

All templates and operation snippets live in `references/*.md`. Each file is a focused snippet or template the agent will combine when generating samples.

**Flow:** Always start with `references/basic-sample.md`, then merge matched features into its structure. If no keyword matches, return only the basic sample.

| File | Purpose |
|---|---|
| **basic-sample.md** | Minimal SfPdfViewer with a network/asset URL, Scaffold, and AppBar. |
| **magnification.md** | Configure zoom level, max zoom, double-tap zoom, and zoom callbacks using `PdfViewerController` and widget properties. |
| **page-navigation.md** | Navigate pages programmatically using `jumpToPage`, `nextPage`, `previousPage`, `firstPage`, `lastPage`, and `jumpTo` offset methods. |
| **text-search.md** | Search text, navigate results with `nextInstance`/`previousInstance`, cancel search, and customise highlight colors. |
| **text-selection.md** | Enable/disable text selection, customise selection color, handle `onTextSelectionChanged` callback. |
| **bookmark-navigation.md** | Open the built-in bookmark view and navigate to bookmarks programmatically using `jumpToBookmark`. |
| **scrolling.md** | Programmatic scrolling using `jumpTo` and reading current scroll offset via `scrollOffset`. |
| **pdfviewer-properties.md** | Common SfPdfViewer widget properties reference: `canShowScrollHead`, `canShowPaginationDialog`, `interactionMode`, `pageLayoutMode`, `initialZoomLevel`, `onDocumentLoaded`, `onDocumentLoadFailed`, `onPageChanged`, etc. |
| **annotation.md** | Add, remove, select, and manage text markup (Highlight, Underline, Strikethrough, Squiggly) and Sticky Note annotations using `PdfViewerController` methods and annotation callbacks. |
| **signaturepad.md** | Hide the built-in signature pad using `canShowSignaturePadDialog` and display a custom `SfSignaturePad` dialog via `onFormFieldFocusChange` to capture and assign drawn signatures to `PdfSignatureFormField`. |
| **password-protected-pdf.md** | Open encrypted PDF documents using the `password` property and handle load failures with `onDocumentLoadFailed`. |
| **link-navigation.md** | Enable/disable document link annotation navigation with `enableDocumentLinkAnnotation` and handle hyperlink taps using `onHyperlinkClicked`. |
| **form-filling.md** | Fill, edit, save, export, import, and clear AcroForm fields (text box, checkbox, radio button, combo box, list box, signature) using `PdfViewerController` methods and form field callbacks. |
| **localization.md** | Localize SfPdfViewer static UI text to any supported language using `flutter_localizations`, `syncfusion_localizations`, and `MaterialApp` locale configuration. |
| **directionality.md** | Enable right-to-left (RTL) rendering by wrapping `SfPdfViewer` with the `Directionality` widget or setting an RTL `locale` in `MaterialApp`. |
| **accessibility.md** | Make SfPdfViewer accessible via `Semantics` widget for screen readers, keyboard navigation shortcuts, large font support, and touch target standards. |
| **gesture-callback.md** | Handle tap gestures on the PDF viewer using the `onTap` callback and `PdfGestureDetails` (page number, page position, widget position). |
---
