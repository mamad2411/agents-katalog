---
name: syncfusion-flutter-pdf
description: Create and manipulate PDF documents using Syncfusion Flutter PDF library. Supports two modes — generate Dart code for the user's Flutter project or provide code snippets. Use when the user mentions PDF creation, drawing, tables, images, text, annotations, bookmarks, encryption, or Syncfusion Flutter PDF.
compatibility: Requires Flutter SDK and the syncfusion_flutter_pdf pub package. Designed for Flutter Mobile, Web, and Desktop platforms.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# PDF Document Processing Using Syncfusion Flutter PDF Library
Create, edit, and save PDF documents (.pdf) using the Syncfusion Flutter PDF library.
This skill supports generating Dart code snippets for Flutter projects targeting mobile, web, and desktop platforms.

---

### Generate Dart Code for the User's Flutter Project *(default)*

**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "main.dart", "example code", "generate code for", "codesnippet".

**Workflow:**

#### Step 1 — Detect the Platform and Suggest the Correct Package
- Inspect the workspace project files (`pubspec.yaml`, `main.dart`, etc.) to identify the Flutter platform target (mobile, web, desktop).
- Tell the user to add `syncfusion_flutter_pdf` to their `pubspec.yaml` **before** generating any code.

#### Step 2 — Generate Code from Reference Files Only
Do NOT invent, guess, or suggest any API, class, method, or property not explicitly present in the reference files.
- Read the relevant `references/*.md` file(s) for the requested feature
- Build Dart code **strictly** from the APIs and snippets found in those files
- Use the correct save/launch pattern for the target platform:
  - **Mobile** → `getApplicationSupportDirectory()` + `OpenFile.open()`
  - **Desktop** → `getApplicationSupportDirectory()` + `OpenFile.open()`
  - **Web** → base64 + JavaScript download or `web` package approach
- Do **not** create or run any standalone Dart script

---

## Code References

All snippets are in the `references/` folder:

| File | Contents |
|---|---|
| **document-structure.md** | Create/load document, page settings, orientation, margins, sections, save to file/stream, incremental update, compression, open encrypted PDF, dispose |
| **pages.md** | Add/insert/remove/rotate pages, get page count, set margins, sections with different page settings, get client size |
| **flow-layout.md** | Chain elements using PdfLayoutResult, paginate text across pages, PdfLayoutFormat options |
| **text.md** | Draw text (drawString, PdfTextElement), standard/TrueType/CJK fonts, RTL text, multicolumn text, pens and brushes |
| **images.md** | Insert JPEG/PNG images (PdfBitmap), apply transparency and rotation, insert from web URL |
| **shapes.md** | Draw polygon, line, curve, path, rectangle, pie, arc, bezier, ellipse |
| **tables.md** | Create PdfGrid, add columns/headers/rows, cell/row/column customization, built-in styles, pagination, multiple tables |
| **lists.md** | Ordered lists (PdfOrderedList), unordered lists (PdfUnorderedList), sub-lists |
| **header-footer.md** | Add headers and footers (PdfPageTemplateElement), automatic fields (page number, page count, date/time), composite fields |
| **bookmarks.md** | Add/insert/remove/modify bookmarks (PdfBookmark), child bookmarks, destination, color, text style |
| **annotations.md** | Rectangle, ellipse, line, polygon, URI, document link, text web link, text markup, popup annotations; flatten, modify, remove annotations; import/export FDF/XFDF/JSON |
| **hyperlinks.md** | Web navigation links (PdfTextWebLink), URI annotations, internal document navigation (PdfDocumentLinkAnnotation), destination modes |
| **watermarks.md** | Text and image watermarks with transparency and rotation, apply to all pages via PdfPageTemplateElement stamp |
| **pdf-templates.md** | Create PdfTemplate, draw templates on pages, extract page as template using createTemplate, stamp overlays with PdfPageTemplateElement |
| **digital-signature.md** | PdfSignatureField, PdfCertificate, sign new/existing PDF, signature appearance, external signer, multiple signatures, timestamp, LTV |
| **text-extraction.md** | Extract text (full/page/range), extract text lines/words/characters with bounds and font info, find text with MatchedItem |
| **pdf-conformance.md** | PDF/A-1b, PDF/A-2b, PDF/A-3b conformance levels, embedded fonts requirement, attachment relationships for PDF/A-3b |
| **attachments.md** | Add/remove file attachments (PdfAttachment), attach from base64, extract and save to disk, PDF/A-3b attachment metadata |
| **layers.md** | Add/toggle/remove layers (PdfPageLayer), nested layers (PdfLayer), visibility control, flatten layers |
| **forms.md** | AcroForm fields: text box, combo box, radio button, list box, check box, signature, button; fill/modify/flatten/remove fields; import/export FDF/XFDF/JSON/XML |
| **encryption.md** | RC4 and AES encryption, user/owner passwords, permissions (print, copy, edit), protect existing PDF, change/remove password |

---

## Rules

- Output files go in `./output/` directory
- Temp `.dart` scripts must be created inside `{skill-root}/flutter/pdf/scripts/` — never in the workspace root or customer `scripts/` folder
- Never leave temp `.dart` files after execution
- Always call `document.dispose()` after saving
- All units in PDF are in **points** (not pixels)
- Use `PdfLayoutResult` to chain elements and avoid content overlap

## Prerequisites

- Flutter SDK installed
- Add to `pubspec.yaml`:
  ```yaml
  dependencies:
    syncfusion_flutter_pdf: ^xx.x.xx
  ```
- Run: `flutter pub get`
- Import in Dart code:
  ```dart
  import 'package:syncfusion_flutter_pdf/pdf.dart';
  ```
