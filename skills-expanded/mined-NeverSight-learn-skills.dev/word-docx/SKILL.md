---
name: word-docx
description: >
  Create, edit, and reformat professional Microsoft Word (.docx) documents with precise
  formatting control. Use this skill whenever the user wants to: generate a Word document
  from scratch, reformat or beautify an existing .docx file, apply Chinese academic paper
  standards (论文排版), produce reports, memos, contracts, or any document requiring
  specific fonts, heading hierarchies, line spacing, margins, tables, headers/footers,
  page numbers, table of contents, or tracked changes. Trigger on phrases like
  "生成Word文档", "帮我排版", "导出为docx", "make a Word doc", "create a report",
  "format this document", "add page numbers", or any mention of .docx output.
  Always use this skill for multi-section documents — do NOT just paste text.
---

# Word DOCX Skill

Generate and edit professional `.docx` files using the `docx` npm library.
Always produce a downloadable file — never just print document text in the chat.

---

## Quick Decision Tree

```
User wants a .docx?
├── New document from scratch  → § Create New Document
├── Edit / reformat existing   → § Edit Existing Document
└── Chinese academic paper     → § Chinese Academic Preset (then Create)
```

---

## Setup (run once per session)

```bash
node --version          # must be ≥ 16
npm list -g docx 2>/dev/null || npm install -g docx
```

---

## § Create New Document

### 1. Boilerplate

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LineRuleType, LevelFormat,
  WidthType, BorderStyle, ShadingType, VerticalAlign,
  PageNumber, NumberFormat, HeadingLevel, TabStopType,
  PageBreak, TableOfContents
} = require('docx');
const fs = require('fs');

// Build sections array, then:
const doc = new Document({ styles: STYLES, numbering: NUMBERING, sections: SECTIONS });
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('output.docx', buf);
  console.log('Done');
});
```

### 2. Page Size & Margins

```javascript
// A4 (Chinese standard)
const PAGE_A4 = {
  size: { width: 11906, height: 16838 },           // twips
  margin: { top: 1440, bottom: 1440, left: 1800, right: 1800 }  // 2.54cm / 3.17cm
};

// US Letter
const PAGE_LETTER = {
  size: { width: 12240, height: 15840 },
  margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
};
```

### 3. Font & Size Reference

| Chinese Name | pt | half-points (size field) | Typical use |
|---|---|---|---|
| 小二 | 18 | 36 | 论文主标题 |
| 三号 | 16 | 32 | 一级标题 |
| 小三 | 15 | 30 | 二级标题 |
| 四号 | 14 | 28 | 三级标题 |
| 小四 | 12 | 24 | 正文 |
| 五号 | 10.5 | 21 | 参考文献、脚注 |

Font pairing rule: `font: { ascii: 'Times New Roman', eastAsia: '宋体' }` for body;
`font: { ascii: 'Arial', eastAsia: '黑体' }` for headings.

### 4. Spacing

```javascript
// Fixed line spacing 23pt (460 twips) — Chinese academic standard
const LINE_FIXED_23 = { line: 460, lineRule: LineRuleType.EXACT };

// 1.5× line spacing
const LINE_15 = { line: 360, lineRule: LineRuleType.AUTO };

// Paragraph spacing (before/after in twips, 1pt = 20 twip)
spacing: { before: 240, after: 120, ...LINE_FIXED_23 }
```

### 5. Indentation

```javascript
// First-line indent 2 chars (小四 12pt → 1 char ≈ 240 twip)
indent: { firstLine: 480 }

// Hanging indent for references
indent: { left: 480, hanging: 480 }
```

### 6. Styles Object (Chinese Academic)

```javascript
const STYLES = {
  default: {
    document: { run: { font: { ascii: 'Times New Roman', eastAsia: '宋体' }, size: 24 } }
  },
  paragraphStyles: [
    {
      id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal',
      run: { font: { ascii: 'Arial', eastAsia: '黑体' }, size: 32, bold: true },
      paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 240, after: 120 }, outlineLevel: 0 }
    },
    {
      id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal',
      run: { font: { ascii: 'Arial', eastAsia: '黑体' }, size: 30, bold: true },
      paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 180, after: 90 }, outlineLevel: 1 }
    },
    {
      id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal',
      run: { font: { ascii: 'Arial', eastAsia: '黑体' }, size: 28, bold: true },
      paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 120, after: 60 }, outlineLevel: 2 }
    },
  ]
};
```

### 7. Header & Footer with Page Numbers

```javascript
const header = new Header({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 1 } },
    children: [new TextRun({
      text: '文档标题或章节名',
      font: { eastAsia: '宋体' }, size: 21
    })]
  })]
});

const footer = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ children: [PageNumber.CURRENT], font: { eastAsia: '宋体' }, size: 21 }),
    ]
  })]
});

// Attach to section:
sections: [{ properties: { page: PAGE_A4 }, headers: { default: header }, footers: { default: footer }, children: [...] }]
```

### 8. Tables

```javascript
// CRITICAL: always set columnWidths AND per-cell width (both in DXA)
// A4 content width with 3.17cm margins = 11906 - 3600 = 8306 twips
const BORDER = { style: BorderStyle.SINGLE, size: 1, color: 'AAAAAA' };
const BORDERS = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER };

new Table({
  width: { size: 8306, type: WidthType.DXA },
  columnWidths: [2000, 3306, 3000],   // must sum to 8306
  rows: [
    new TableRow({
      tableHeader: true,
      children: ['列1','列2','列3'].map((txt, i) =>
        new TableCell({
          borders: BORDERS,
          width: { size: [2000,3306,3000][i], type: WidthType.DXA },
          shading: { fill: 'D5E8F0', type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({
            children: [new TextRun({ text: txt, bold: true, font: { eastAsia: '黑体' }, size: 24 })]
          })]
        })
      )
    }),
    // data rows ...
  ]
})
```

### 9. Table of Contents

```javascript
// Headings MUST use HeadingLevel enum (not custom styles) for TOC to work
new TableOfContents('目  录', {
  hyperlink: true,
  headingStyleRange: '1-3',
})
// Then use:
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('一、引言')] })
```

### 10. Bullet & Numbered Lists

```javascript
// NEVER use unicode bullet chars — always use numbering config
const NUMBERING = {
  config: [
    { reference: 'bullets',
      levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'ordered',
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ]
};

new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: [new TextRun('项目')] })
```

---

## § Edit Existing Document

Use the unpack → edit XML → repack workflow:

```bash
# 1. Unpack
python scripts/office/unpack.py document.docx unpacked/

# 2. Edit XML in unpacked/word/document.xml
#    Use str_replace for targeted changes — do NOT write Python scripts for this

# 3. Repack & validate
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

For simple text replacements in known paragraphs, use `office:edit_docx_paragraph` MCP tool instead.

### Tracked Changes

```xml
<!-- Insertion -->
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>new text</w:t></w:r>
</w:ins>

<!-- Deletion -->
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>old text</w:delText></w:r>
</w:del>
```

---

## § Chinese Academic Preset

Standard settings for Chinese university papers (本科/硕士论文):

| Element | Spec |
|---|---|
| Paper | A4，上下2.54cm，左右3.17cm |
| 论文主标题 | 小二（18pt）黑体，居中，段前12pt |
| 一级标题 | 三号（16pt）黑体，居中 |
| 二级标题 | 小三（15pt）黑体，左对齐 |
| 三级标题 | 四号（14pt）黑体，左对齐 |
| 正文 | 小四（12pt）宋体，首行缩进2字，两端对齐 |
| 行距 | 固定值23磅 |
| 摘要标签 | 小四黑体加粗（"摘要："），后接宋体内容 |
| 参考文献 | 五号宋体，悬挂缩进2字 |
| 页眉 | 五号宋体居中，下边框单线 |
| 页脚 | 五号宋体居中，阿拉伯数字页码 |

Apply `STYLES` from § Create > Style Object, add header/footer from § 7, use `LINE_FIXED_23` everywhere.

---

## § Validate

Always validate after generating:

```bash
python scripts/office/validate.py output.docx
```

Fix any errors before delivering the file.

---

## Critical Rules (Never Violate)

- **Never use `\n`** — use separate `Paragraph` objects
- **Never use unicode bullets** (`•`, `·`) as raw text — use `LevelFormat.BULLET`
- **Tables need dual widths** — `columnWidths` on table AND `width` on each cell
- **Use `WidthType.DXA`** — never `PERCENTAGE` (breaks in Google Docs)
- **Use `ShadingType.CLEAR`** — never `SOLID` (causes black backgrounds)
- **TOC requires `HeadingLevel` enum** — not custom style names
- **`outlineLevel`** required in heading style paragraph props for TOC
- **PageBreak must be inside a Paragraph** — standalone breaks invalid XML
- **ImageRun requires `type`** field — always specify `'png'` / `'jpg'`
- **All files go to `/mnt/user-data/outputs/`** then call `present_files`
