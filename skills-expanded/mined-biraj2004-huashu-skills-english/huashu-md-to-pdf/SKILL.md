---
name: huashu-md-to-pdf
description: |
  Convert Markdown documents into professional Apple-style PDF white papers.
  Supports full Markdown syntax (code blocks, tables, blockquotes, lists, etc.).
  Auto-generates cover page, table of contents, and headers/footers.
  Use cases: technical documentation, white papers, tutorials, reports — any Markdown document requiring professional typesetting.
---

# Markdown to PDF Skill

Convert Markdown documents into professional Apple-design-style PDF white papers.

## Core Features

1. **Professional typesetting**: Book-quality layout with automatic handling of page breaks and widow/orphan control
2. **Apple design language**: SF font system, modern minimalist style, professional colour palette
3. **Full table of contents**: Automatically extracts chapter structure, dual-column layout, clickable page jumps
4. **Complete Markdown support**: Code blocks, tables, blockquotes, lists — all rendered correctly

## How to Use

### Basic Usage

```bash
# Convert a single file
python scripts/convert.py input.md

# Specify output filename
python scripts/convert.py input.md -o "My White Paper.pdf"

# Custom title and author
python scripts/convert.py input.md --title "Technical White Paper" --author "Huashu"
```

### Markdown Document Requirements

Your Markdown document should follow this structure:

```markdown
# Document Title

## 1. Chapter One
### 1.1 Section One
### 1.2 Section Two

## 2. Chapter Two
### 2.1 Section One
```

**Key rules**:

- Main chapters: `## 1. Title` (number + full stop + space + title)
- Sub-sections: `### 1.1 Title` (number.number + space + title)
- This structure is required for the table of contents to generate correctly

## Design Features

### Cover Design

- Light grey gradient background
- Large title: 64pt, clean and modern
- Subtitle and metadata information

### Table of Contents Design

- Dual-column layout, fits on one page
- Main chapters in bold, sub-sections indented
- Clickable links that jump to the corresponding section

### Body Typesetting

- SF font family (Apple design language)
- Line height 1.7 for comfortable reading
- Chapters automatically start on a new page
- Widow and orphan control

### Code Blocks

- Light grey background + fine border
- 8px border radius
- SF Mono monospace font
- Automatic page break prevention

### Tables

- Clear grid lines
- Light grey header row
- Automatic header repeat (for tables that span multiple pages)

## Configuration Options

To customise the style, edit the CSS variables in `scripts/convert.py`:

```python
# Primary colour
PRIMARY_COLOR = '#06c'      # Apple blue
TEXT_COLOR = '#1d1d1f'      # Main text black
GRAY_COLOR = '#86868b'      # Light grey

# Font sizes
COVER_TITLE_SIZE = '64pt'
H2_SIZE = '22pt'
H3_SIZE = '17pt'
BODY_SIZE = '11pt'
```

## Frequently Asked Questions

### Q: Why is the table of contents empty?

A: Ensure your Markdown uses the correct chapter format:

- `## 1. Title` instead of `## Title`
- `### 1.1 Title` instead of `### Title`

### Q: Code blocks not displaying correctly?

A: Ensure you're wrapping with three backticks:

````markdown
```python
def hello():
    print("Hello")
```text
````

### Q: Table formatting is broken?

A: Use standard Markdown table syntax:

```markdown
| Column 1 | Column 2 |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-md-to-pdf
description: |
  Convert Markdown documents into professional Apple-style PDF white papers.
  Supports full Markdown syntax (code blocks, tables, blockquotes, lists, etc.).
  Auto-generates cover page, table of contents, and headers/footers.
  Use cases: technical documentation, white papers, tutorials, reports — any Markdown document requiring professional typesetting.
---

# Markdown to PDF Skill

Convert Markdown documents into professional Apple-design-style PDF white papers.

## Core Features

1. **Professional typesetting**: Book-quality layout with automatic handling of page breaks and widow/orphan control
2. **Apple design language**: SF font system, modern minimalist style, professional colour palette
3. **Full table of contents**: Automatically extracts chapter structure, dual-column layout, clickable page jumps
4. **Complete Markdown support**: Code blocks, tables, blockquotes, lists — all rendered correctly

## How to Use

### Basic Usage

```bash
# Convert a single file
python scripts/convert.py input.md

# Specify output filename
python scripts/convert.py input.md -o "My White Paper.pdf"

# Custom title and author
python scripts/convert.py input.md --title "Technical White Paper" --author "Huashu"
```

### Markdown Document Requirements

Your Markdown document should follow this structure:

```markdown
# Document Title

## 1. Chapter One
### 1.1 Section One
### 1.2 Section Two

## 2. Chapter Two
### 2.1 Section One
```

**Key rules**:

- Main chapters: `## 1. Title` (number + full stop + space + title)
- Sub-sections: `### 1.1 Title` (number.number + space + title)
- This structure is required for the table of contents to generate correctly

## Design Features

### Cover Design

- Light grey gradient background
- Large title: 64pt, clean and modern
- Subtitle and metadata information

### Table of Contents Design

- Dual-column layout, fits on one page
- Main chapters in bold, sub-sections indented
- Clickable links that jump to the corresponding section

### Body Typesetting

- SF font family (Apple design language)
- Line height 1.7 for comfortable reading
- Chapters automatically start on a new page
- Widow and orphan control

### Code Blocks

- Light grey background + fine border
- 8px border radius
- SF Mono monospace font
- Automatic page break prevention

### Tables

- Clear grid lines
- Light grey header row
- Automatic header repeat (for tables that span multiple pages)

## Configuration Options

To customise the style, edit the CSS variables in `scripts/convert.py`:

```python
# Primary colour
PRIMARY_COLOR = '#06c'      # Apple blue
TEXT_COLOR = '#1d1d1f'      # Main text black
GRAY_COLOR = '#86868b'      # Light grey

# Font sizes
COVER_TITLE_SIZE = '64pt'
H2_SIZE = '22pt'
H3_SIZE = '17pt'
BODY_SIZE = '11pt'
```

## Frequently Asked Questions

### Q: Why is the table of contents empty?

A: Ensure your Markdown uses the correct chapter format:

- `## 1. Title` instead of `## Title`
- `### 1.1 Title` instead of `### Title`

### Q: Code blocks not displaying correctly?

A: Ensure you're wrapping with three backticks:

````markdown
```python
def hello():
    print("Hello")
```text
````

### Q: Table formatting is broken?

A: Use standard Markdown table syntax:

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```

### Q: How do I change the font?

A: Edit the CSS in `scripts/convert.py` and modify the `font-family` property.

### Q: The generated PDF is too large?

A: Check whether there are large images — consider compressing them or using external links.

## Dependency Installation

First-time use requires installing Python dependencies:

```bash
pip3 install markdown2 weasyprint
```

If you encounter WeasyPrint installation issues (macOS):

```bash
brew install pango
pip3 install weasyprint
```

## Examples

### Generate Technical Documentation

```bash
python scripts/convert.py tech-guide.md -o "Technical Guide.pdf"
```

### Generate a White Paper

```bash
python scripts/convert.py whitepaper.md --title "Product White Paper" --author "Team"
```

## Script Reference

- `scripts/convert.py` — Main conversion script
- `scripts/styles.css` — CSS style definitions (embedded in script)
- `templates/cover.html` — Cover template (embedded in script)

## Technical Implementation

This Skill uses:

- **markdown2**: Markdown parsing (with extended syntax support)
- **WeasyPrint**: HTML to PDF conversion (with CSS3 support)
- **Apple design system**: SF fonts, professional colour palette, modern typesetting

## Changelog

### v1.0 (2025-12-24)

- Initial release
- Full Markdown syntax support
- Apple design style
- Automatic table of contents generation
- Book-quality typesetting

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Value 1  | Value 2  |
```

### Q: How do I change the font?

A: Edit the CSS in `scripts/convert.py` and modify the `font-family` property.

### Q: The generated PDF is too large?

A: Check whether there are large images — consider compressing them or using external links.

## Dependency Installation

First-time use requires installing Python dependencies:

```bash
pip3 install markdown2 weasyprint
```

If you encounter WeasyPrint installation issues (macOS):

```bash
brew install pango
pip3 install weasyprint
```

## Examples

### Generate Technical Documentation

```bash
python scripts/convert.py tech-guide.md -o "Technical Guide.pdf"
```

### Generate a White Paper

```bash
python scripts/convert.py whitepaper.md --title "Product White Paper" --author "Team"
```

## Script Reference

- `scripts/convert.py` — Main conversion script
- `scripts/styles.css` — CSS style definitions (embedded in script)
- `templates/cover.html` — Cover template (embedded in script)

## Technical Implementation

This Skill uses:

- **markdown2**: Markdown parsing (with extended syntax support)
- **WeasyPrint**: HTML to PDF conversion (with CSS3 support)
- **Apple design system**: SF fonts, professional colour palette, modern typesetting

## Changelog

### v1.0 (2025-12-24)

- Initial release
- Full Markdown syntax support
- Apple design style
- Automatic table of contents generation
- Book-quality typesetting

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Value 1  | Value 2  |
```

### Q: How do I change the font?

A: Edit the CSS in `scripts/convert.py` and modify the `font-family` property.

### Q: The generated PDF is too large?

A: Check whether there are large images — consider compressing them or using external links.

## Dependency Installation

First-time use requires installing Python dependencies:

```bash
pip3 install markdown2 weasyprint
```

If you encounter WeasyPrint installation issues (macOS):

```bash
brew install pango
pip3 install weasyprint
```

## Examples

### Generate Technical Documentation

```bash
python scripts/convert.py tech-guide.md -o "Technical Guide.pdf"
```

### Generate a White Paper

```bash
python scripts/convert.py whitepaper.md --title "Product White Paper" --author "Team"
```

## Script Reference

- `scripts/convert.py` — Main conversion script
- `scripts/styles.css` — CSS style definitions (embedded in script)
- `templates/cover.html` — Cover template (embedded in script)

## Technical Implementation

This Skill uses:

- **markdown2**: Markdown parsing (with extended syntax support)
- **WeasyPrint**: HTML to PDF conversion (with CSS3 support)
- **Apple design system**: SF fonts, professional colour palette, modern typesetting

## Changelog

### v1.0 (2025-12-24)

- Initial release
- Full Markdown syntax support
- Apple design style
- Automatic table of contents generation
- Book-quality typesetting

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
