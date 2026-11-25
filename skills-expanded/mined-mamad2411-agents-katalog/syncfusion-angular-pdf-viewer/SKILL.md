---
name: syncfusion-angular-pdf-viewer
description: Implements the Syncfusion Angular PDF Viewer (PdfViewerComponent) for embedding, configuring, and loading PDF documents. Use this when rendering PDFs in an Angular application, embedding viewer controls, or generating TS/CSS code for PDF display and interaction.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular PDF Viewer UI Sample Generator

## Mandatory 3-Step workflow (Strict Enforcement)

**EVERY query MUST follow these steps sequentially:**

```
STEP 1: Workspace Detection ? STEP 2: Read Reference File ? STEP 3: Generate Code
```

### Blocking Rules

1. **NO code generation** until Steps 1 & 2 are complete
2. **NO assumptions** - Always verify workspace AND read reference files first
3. **NO undocumented APIs** - Use ONLY APIs from reference files

**Violation = STOP and restart with proper protocol**

---

## Mandatory Workflow

### STEP 1: Workspace Detection *(REQUIRED - DO THIS FIRST)*

**Execute these tools:**
```
1. file_search: **/{package.json,angular.json,tsconfig.json}
2. list_dir: src/app/
3. read_file: package.json (if exists)
```

**Report to user:**
```
?? STEP 1 COMPLETE:
- Workspace: [Empty / Angular X.X project detected]
- Files found: [list]
- Decision: [Create new / Use existing]
```

### STEP 2: Read Reference File *(REQUIRED - DO THIS SECOND)*

**Execute these steps:**
```
1. Match user query to Reference File Routing Guide below
2. Use read_file on: references\[filename].md
3. Extract ALL steps/APIs from reference file
```

**Report to user:**
```
?? STEP 2 COMPLETE:
- Reference file: [filename.md]
- Steps found: [list sequential steps]
- APIs validated: [list properties/methods used]
```

### STEP 3: Generate Code *(EXECUTE ONLY AFTER STEPS 1 & 2)*

**Validation checklist:**
- [ ] Every API cross-referenced against reference file
- [ ] No invented/assumed properties used
- [ ] Angular patterns followed (component bindings, lifecycle hooks)
- [ ] If API not in reference file ? DELETE it

**If feature not in reference file:**
```
? FEATURE NOT SUPPORTED
The requested [feature/API] is not documented.
Available alternatives: [list from reference files]
```

---

## Reference File Routing Guide

### Core Setup
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "basic", "create sample", "getting started", "load PDF" | **basic-sample.md** | Minimal PDFViewer setup |
| "configuration", "server settings", "locale" | **general-properties.md** | Core viewer properties |
| "disable", "hide features", "enable/disable", "read-only" | **enable-properties.md** | Feature toggles |

### Navigation
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "page navigation", "next/previous page", "go to page" | **page-navigation.md** | Page controls |
| "bookmarks", "table of contents", "TOC", "outline" | **bookmark-navigation.md** | Bookmark navigation (use ViewChild) |
| "hyperlinks", "external links", "URL navigation" | **hyperlink-navigation.md** | Link handling |
| "thumbnails", "preview pages", "thumbnail panel" | **thumbnail-navigation.md** | Thumbnail panel |

### Viewing & Interaction
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "zoom", "magnification", "fit to page", "scale" | **magnification.md** | Zoom controls |
| "text selection", "panning", "scroll mode" | **interaction-mode.md** | Interaction modes |
| "select text", "copy text" | **text-selection.md** | Text selection |
| "search", "find in PDF", "highlight search" | **text-search.md** | Search functionality |

### Toolbar & Context Menu
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "customize toolbar", "hide toolbar items", "remove buttons" | **toolbar-settings.md** | Toolbar configuration |
| "show/hide toolbar dynamically", "toggle toolbar" | **toolbar-methods.md** | Programmatic toolbar control |
| "right-click menu", "context menu", "custom menu" | **contextmenu.md** | Context menu |

### Annotations
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "annotation colors", "annotation styles", "customize annotations" | **annotation-settings.md** | Annotation appearance |
| "annotation events", "when annotation added", "annotation callbacks" | **annotation-events.md** | Annotation lifecycle |
| "annotation labels", "shape labels", "measurement labels" | **shape-label-settings.md** | Label customization |
| "ink annotation", "freehand drawing", "signature", "sketch", "handwritten notes" | **ink-annotation.md** | Ink annotations |
| "redaction", "redact content", "black out text" | **redaction-annotation.md** | Redaction annotations |

### Forms
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "form field defaults", "form field styles" | **form-field-settings.md** | Form field config |
| "form field events", "field changes", "validation" | **form-field-events.md** | Form field events |

### Document Actions
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "download PDF", "save PDF", "export" | **download.md** | Download functionality |
| "print PDF", "print document" | **print.md** | Print functionality |
| "reorder pages", "rotate pages", "add/remove pages" | **organize-pages.md** | Page manipulation |

### Advanced
| User Query Keywords | Reference File | Purpose |
|---|---|---|
| "load programmatically", "API methods", "extract text" | **api-methods.md** | Programmatic control |
| "event list", "all events", "event reference" | **events.md** | Complete event list |

---

## Toolbar Item Name Validation (CRITICAL)

**When generating toolbar configurations:**
1. **ALWAYS read `toolbar-settings.md` first**
2. **Use ONLY names from these sections:**
   - "Available Primary Toolbar Items"
   - "Available Annotation Toolbar Items"
   - "Available Form Designer Items"
3. **Character-by-character validation required** - No typos allowed

**Common mistakes to prevent:**
- ? `AnotatetionEditTool` ? ? `AnnotationEditTool`
- ? `CalibrationOption` ? ? `CalibrateTool`
- ? `ShapeAnnotationOption` ? ? `ShapeTool`

---

## Settings Configurations

### Rule 1: Simple Settings (1-3 properties) ? Inline
```typescript
public annotationSelection = {
  selectionBorderColor: 'blue',
  resizerSize: 8
};
```

### Rule 2: Complex Settings (4+ properties or enums) ? Import enums
```typescript
import { AnnotationResizerLocation, CursorType } from '@syncfusion/ej2-angular-pdfviewer';

public annotationSelection = {
  selectionBorderColor: '#0000ff',
  resizerSize: 8,
  resizerLocation: AnnotationResizerLocation.Corners | AnnotationResizerLocation.Edges,
  resizerCursorType: CursorType.grab
};
```

---

## Protocol Violation Handling

| Violation | Fix |
|---|---|
| Skipped Step 1 | Re-run: Use file_search and list_dir first |
| Skipped Step 2 | Re-run: Use read_file on reference file |
| Used undocumented API | Delete it, check reference for alternatives |
| Didn't report findings | Report: "I checked X, found Y, now doing Z" |

**If user calls out violation: IMMEDIATELY acknowledge, apologize, and restart with proper protocol.**

---

## Enforcement Checklist

**Before generating code, verify:**
- [ ] Step 1 executed (workspace detection) and reported
- [ ] Step 2 executed (reference file read) and reported
- [ ] Every API validated against reference file
- [ ] No undocumented APIs used
- [ ] Angular patterns followed

**Reference files are SOURCE OF TRUTH - everything must trace back to them.**
