---
name: syncfusion-java-word
description: Create, edit, and convert Word documents (.docx) using Syncfusion DocIO. Supports to generate java code for the user's project. Use when the user mentions docx, Word processing, document generation, Syncfusion DocIO, or syncfusion java word.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Word (DOCX) Document Processing

## Overview

Create, edit, and convert Word (.docx, .html) files using the Syncfusion Word Library.
This skill supports one operational modes — generating java code for the user's project.

## Key Capabilities

- **Create & Edit:** Documents (.docx, .rtf, .txt, .xml, .html), paragraphs, headings, styles, lists, tables, shapes, images, hyperlinks, bookmarks, watermarks, headers/footers, form fields, content controls.
- **Advanced Features:** Mail merge (DataTable, JSON, XML, custom objects), track changes, comments, mathematical equations (LaTeX), compare/split/merge documents.
- **Conversion:** HTML ↔ DOCX, RTF ↔ DOCX, Text ↔ DOCX, XML ↔ DOCX
- **Security:** Password encryption/decryption, document protection with editable ranges, macro management

## Prerequisites

- Java SE 8.0(1.8) or above versions.
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Generate Code (Mode 1)
**User:** "Show me how to create a Word document with a table"

**Result:** java code snippet displayed (no files created)

**Workflow:**

#### Step 1 — Suggest to add docio jars as references

- The following jar files are required to be referenced in your Java application.
 - syncfusion®-docio
 - syncfusion®-javahelper
- Get the dependent jar files by installing file formats controls. You can find the required jars in the build installed drive.
 - Location: {ProgramFilesFolder}\Syncfusion\Essential Studio\ {Platform}\ {version}\JarFiles
 - Example: C:\Program Files (x86)\Syncfusion\Essential Studio\FileFormats\18.3.0.35\JarFiles

#### Step 2 — Generate Code from Reference Files Only

Do NOT invent, guess, or suggest any API, method, class, or packages not explicitly present in the reference files.

- Read the relevant `references/*.md` file(s) for the requested feature
- Build java code **strictly** from the APIs and snippets found in those files

---

## Code References

All templates and snippets are in the `references/` folder:

| File | Contents |
|---|---|
| **document-structure.md** | Create/load document, add sections, page setup, save to file or stream, supported formats |
| **styles-and-formats.md** | Paragraphs, headings, bullet & numbered lists |
| **paragraph-and-styles.md** | Add paragraphs, paragraph formatting, styles (built-in/custom), text formatting, tab stops, breaks, symbols, text boxes |
| **tables.md** | Create tables, cell formatting, merge cells |
| **bookmarks.md** | Create bookmarks, navigate, retrieve, insert, replace, delete content |
| **shapes.md** | Add shapes, format, rotate, group, ungroup shapes |
| **mail-merge.md** | Simple field merge, merge with regions (groups), nested merge, DataTable, dynamic objects, business objects, DataView, XML, JSON, image merge fields, merge events (MergeField, MergeImageField, BeforeClearField, BeforeClearGroupField), field mapping, retrieve merge field names, remove empty paragraphs, clear fields option |
| **form-fields.md** | Add checkboxes, dropdowns, text input fields, modify properties |
| **macros.md** | Load/save macro-enabled documents (DOTM, DOCM), check for macros, remove macros, preserve macros through conversion |
| **mathematical-equation.md** | Create equations (fraction, radical, matrix, N-array, etc.), modify existing equations, LaTeX support, equation formatting |
| **split-word-documents.md** | Split documents by sections, headings, bookmarks, placeholder text |
| **merge-word-documents.md** | Merge documents in new page, same page, maintain imported list styles |
| **compare-word-documents.md** | Compare two Word documents, set author and date, comparison options, ignore format changes |
| **html-conversions.md** | Convert HTML to DOCX, convert DOCX to HTML, XHTML validation, customize images (import/export), CSS selectors, export options, headers/footers export |
| **rtf-conversions.md** | Convert RTF to DOCX, convert DOCX to RTF, preserve formatting and content |
| **markdown-conversion.md** | Convert Markdown to DOCX, convert DOCX to Markdown, customize images, CommonMark and GitHub-flavored syntax support |
| **text-conversions.md** | Convert Text to DOCX, convert DOCX to Text, extract plain text, preserve text content |
| **xml-conversions.md** | Convert Word to XML (WordML), convert XML to Word, Word Processing XML format (2007+) |
| **encryption.md** | Encrypt with password, open encrypted doc, remove encryption, protect from editing, editable ranges |
| **watermark.md** | Text and picture watermarks, watermark layout, scaling, washout effect, remove watermark |
| **find-and-replace.md** | Find/FindAll/FindNext, Replace (string/regex), ReplaceSingleLine, and FindItem* APIs |
| **footnotes-and-endnotes.md** | Add footnotes and endnotes, set positions (bottom of page/end of section), numbering formats, separators, modify content, remove notes |
| **track-changes.md** | Enable/disable track changes, accept/reject changes, filter by reviewer, revision information |
| **comments.md** | Add/modify/remove comments, insert on specific text, access parent comments, retrieve commented items |
| **content-controls.md** | Block and inline content controls, types (rich text, plain text, checkbox, date, dropdown, picture), properties, protection, form filling, XML mapping |
| **header-footer.md** | Add/remove headers and footers, page numbers with fields (date, time), odd/even pages, first page different, borders, images, link to previous |
| **hyperlinks.md** | Web hyperlink, email hyperlink, file hyperlink, bookmark hyperlink, image hyperlink, modify hyperlink |

---

## Rules

- Use license key from `SyncfusionLicense.txt` at workspace root or env var `SYNCFUSION_LICENSE_KEY`
- Never use Python libraries (e.g., python-docx)