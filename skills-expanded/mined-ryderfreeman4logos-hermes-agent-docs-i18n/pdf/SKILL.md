---
name: pdf
description: "PDF files: create, read, merge, fill, OCR, edit text."
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pdf, documents, forms, ocr, text-extraction, reportlab, pypdf, pdfplumber, pymupdf, marker]
    category: productivity
    related_skills: [docx, xlsx, powerpoint]
---

# PDF技能

该技能可利用pypdf、reportlab和pdfplumber库，实现从结构化规范生成PDF文件、创建并填充AcroForm表单（包含布局校验与视觉标注）、提取文本/表格/元数据、合并/拆分/旋转页面及添加水印或印章、导出页面图像、管理元数据与附件，以及执行加密/解密操作。另有两项功能被整合至参考文档中（在执行相关任务前需先阅读对应文档）：

- **扫描版/仅含图像的PDF文件及OCR处理**（pymupdf快速处理路径，marker-pdf高质量处理路径，脚本scripts/extract_pymupdf.py与scripts/extract_marker.py）：`references/ocr-extraction.md`
- **通过自然语言指令编辑现有PDF中的文本**（nano-pdf CLI工具）：`references/nano-pdf-editing.md`

## 适用场景

- 将报告、发票或多页文档生成为PDF格式。
- 根据JSON规范创建可填写的AcroForm表单（包含文本框、复选框、单选框和下拉菜单），并先对布局进行校验。
- 从PDF文件中提取文本、表格（JSON/CSV格式）、元数据或表单字段内容。
- 合并、拆分、旋转PDF页面，提取部分页面内容，在指定坐标处添加水印或文本/图像印章，设置书签或压缩PDF文件。
- 将页面导出为PNG格式以便可视化查看或传递给OCR工具处理；设置/清除文档元数据；添加/提取文件附件。
- 填写AcroForm表单或将其内容扁平化；使用密码对文件进行加密/解密。
- **不适用于仅含扫描图像的PDF文件**（请参考`references/ocr-extraction.md`），也不适用于需要像素级精确渲染的HTML转PDF场景（此时应使用无头浏览器）。

## 先决条件

- 需要 Python 3.10+ 及相应库 `pypdf`、`reportlab`、`pdfplumber`：
  `python -m pip install pypdf reportlab pdfplumber`
- 如需进行页面光栅化处理（即使用 `pdf_page_image.py` 进行叠加渲染），可选安装 `python -m pip install pypdfium2`，或确保 PATH 环境变量中已配置 Poppler 的 `pdftoppm` 工具。若上述任一工具缺失，脚本将依次尝试使用 `pypdfium2` 和 `pdftoppm`，若均无法使用，则会返回结果 `{"rendered": false, "missing": [...]}` 并以状态码 0 退出。
- 每个辅助脚本都会在运行时动态检查依赖项，若发现缺少某项库，便会提示用户进行安装。

## 运行方式

所有辅助脚本均位于 `scripts/` 目录下，均为基于 argparse 的命令行工具——可通过 `terminal` 工具来运行它们，且每个脚本都支持 `--help` 参数。这些脚本严格以 UTF-8 编码读写 JSON 数据，将处理结果以 JSON 格式输出到标准输出流，若执行失败则会以非零状态码退出。

```bash
python scripts/pdf_create.py spec.json -o out.pdf         # build PDF from JSON spec
python scripts/pdf_make_form.py formspec.json -o form.pdf # build fillable AcroForm from JSON spec
python scripts/pdf_form_layout.py formspec.json           # lint form layout BEFORE building
python scripts/pdf_form_layout.py formspec.json --render-overlay boxes.png [--pdf form.pdf]
python scripts/pdf_read.py doc.pdf --text                 # per-page text (JSON)
python scripts/pdf_read.py doc.pdf --tables --csv-dir t/  # tables to JSON + CSV files
python scripts/pdf_read.py doc.pdf --meta                 # metadata, page sizes, encrypted/scanned flags
python scripts/pdf_read.py form.pdf --fields              # form fields: name, type, value
python scripts/pdf_merge.py a.pdf b.pdf -o merged.pdf [--bookmarks]
python scripts/pdf_split.py doc.pdf --pages 1-3,7 -o part.pdf [--rotate 90]
python scripts/pdf_fill_form.py form.pdf --fields-json values.json -o filled.pdf [--flatten]
python scripts/pdf_secure.py doc.pdf --encrypt -o enc.pdf --user-password your-password
python scripts/pdf_secure.py enc.pdf --decrypt -o dec.pdf --password your-password
python scripts/pdf_watermark.py doc.pdf --stamp mark.pdf -o stamped.pdf [--under]
python scripts/pdf_stamp.py doc.pdf -o out.pdf --text "DRAFT" --x 150 --y 400 \
    --font-size 60 --rotation 45 --opacity 0.3 --color "#cc0000" [--pages 1-3]
python scripts/pdf_stamp.py doc.pdf -o out.pdf --image sig.png --x 400 --y 60 --width 120
python scripts/pdf_page_image.py doc.pdf --pages 1-3 --dpi 150 --out-dir imgs/
python scripts/pdf_meta.py doc.pdf --set-meta --title "T" --author "A" -o out.pdf
python scripts/pdf_meta.py doc.pdf --attach data.csv -o out.pdf
python scripts/pdf_meta.py doc.pdf --list-attachments | --extract-attachments dir/
```

## 快速参考指南

| 任务 | 工具 | 命令/API |
|---|---|---|
| 创建文档（包含标题、表格、图片） | reportlab platypus | `pdf_create.py spec.json -o out.pdf` |
| 构建可填写表单 | reportlab acroForm | `pdf_make_form.py formspec.json -o form.pdf` |
| 检查表单布局及叠加图片 | 纯 Python + PIL | `pdf_form_layout.py formspec.json [--render-overlay o.png]` |
| 提取每页文本 | pdfplumber | `pdf_read.py f.pdf --text` |
| 将表格转换为 JSON/CSV 格式 | pdfplumber | `pdf_read.py f.pdf --tables` |
| 获取元数据、文件大小、加密信息及扫描文档相关数据 | pypdf + pdfplumber | `pdf_read.py f.pdf --meta` |
| 合并文档（并生成大纲） | pypdf | `pdf_merge.py a.pdf b.pdf -o m.pdf` |
| 分割、提取页面或旋转页面 | pypdf | `pdf_split.py f.pdf --pages 2-5 --rotate 90` |
| 列出表单字段、填写表单或展平表单结构 | pypdf | `pdf_read.py --fields`, `pdf_fill_form.py` |
| 加密/解密文档（AES-256算法） | pypdf | `pdf_secure.py --encrypt/--decrypt` |
| 为PDF页面添加水印或印章 | pypdf | `pdf_watermark.py f.pdf --stamp w.pdf` |
| 在指定坐标处添加文本或图片印章 | reportlab + pypdf | `pdf_stamp.py f.pdf --text "在此签名" --x 400 --y 60` |
| 将页面转换为PNG格式（用于预览或传递给OCR工具） | pypdfium2 或 pdftoppm | `pdf_page_image.py f.pdf --pages 1-3 --out-dir imgs/` |
| 设置/清除元数据及附件 | pypdf | `pdf_meta.py --set-meta / --attach / --extract-attachments` |
| 压缩文档内容流 | pypdf | `pdf_split.py f.pdf --pages 1-N --compress` |

## 操作流程

1. **先进行检测。** 运行 `pdf_read.py file.pdf --meta` 命令。查看 `encrypted` 字段（若为 true，则需先用 `pdf_secure.py --decrypt` 解密），以及 `likely_scanned_pages` 字段。如果页面仅为图像，可使用 `pdf_page_image.py --pages <scanned> --dpi 300 --out-dir imgs/` 将其导出为 PNG 格式，再提交给 `references/ocr-extraction.md` 该技能进行处理——切勿将空文本误报为“无内容”。

2. **创建文档。** 使用 `write_file` 函数编写 JSON 规范文件（包含 `heading`、`paragraph`、`table`、`image`、`pagebreak` 等元素；可可选填 `title`/`author` 元数据，页码会自动添加），随后运行 `pdf_create.py`。如果布局格式很重要，可对生成的页面图像使用 `vision_analyze` 工具进行视觉验证。

3. **提取内容。** 使用 `--text` 参数可获取每页文本的 JSON 列表；使用 `--tables` 参数则可得到每页的行数组，同时还能生成 CSV 文件。可使用 `read_file` 命令读取提取结果——切勿直接查看二进制格式的 PDF 文件。

4. **对文档进行操作。** `pdf_merge.py` 可用于合并多个 PDF 文件，且每个源文件可添加一个书签；`pdf_split.py` 能处理页面范围分割（采用从 1 开始计数的方式，例如 `1-3,5,9-`），支持以 90° 为间隔旋转页面，同时还具备压缩功能。若需添加水印，可先通过 `pdf_create.py` 创建单页水印 PDF，再使用 `pdf_watermark.py` 将其叠加到文档上；对于简短的水印文字（如“请在此签名”）、对角线格式的“草稿”标记或角落标签，可使用 `pdf_stamp.py`，并在其中指定具体的文本或图像位置。
5. **构建表单**。编写一个符合格式规范的 JSON 文件（PDF 中的字段需包含 `label_box`/`entry_box` 属性，详情参见 `references/forms.md`），使用 `pdf_form_layout.py` 对其进行代码检查并修复所有报错问题；如有需要，可借助 `vision_analyze` 工具查看 `--render-overlay` 生成的 PNG 文件，最后通过 `pdf_make_form.py` 生成表单，并使用 `pdf_read.py --fields` 命令验证结果。

6. **填写表单**。首先列出所有字段（使用 `--fields` 参数）以确认其具体名称和类型，接着使用 `write_file` 函数编写格式为 `{"FieldName": "value"}` 的 UTF-8 JSON 文件（复选框的值应为 `true`/`false`；单选框/下拉选项的值必须与字段的导出设置一致），之后再运行 `pdf_fill_form.py` 进行填写。最后再次使用 `--fields` 参数读取文件，以确认数据已正确填入。

7. **元数据与附件**。`pdf_meta.py --set-meta` 用于设置标题、作者、主题和关键词等元数据（即 DocInfo）；`--clear-meta` 用于删除这些元数据；而 `--attach`/`--list-attachments`/`--extract-attachments` 则用于处理嵌入在文件中的附件的上传、列表查看及提取操作。

8. **安全性**。系统采用独立的用户密码/所有者密码以及 AES-256 算法对文件进行加密。若需移除已知晓的密码，可使用 `--decrypt` 命令生成未加密的副本。

9. 在报告成功之前，请务必先进行**验证**（详见下文）。

## 常见问题

- **扫描版 PDF**：由于 `extract_text()` 函数返回空值且页面仅包含图像，因此不存在文本层。此类情况请参考 `references/ocr-extraction.md` 的相关说明，切勿自行伪造文本内容。
- **展平限制**：`pdf_fill_form.py --flatten` 功能利用了 pypdf 的展平功能，可将表单控件的外观转换为页面内容。该功能对普通文本字段和复选框较为可靠，但对于一些特殊类型的控件（如富文本、自定义外观流以及某些单选组），则可能导致内容丢失或显示异常。建议使用 `vision_analyze` 工具对展平后的结果进行视觉核查；若需确保绝对可靠的展平效果，可考虑采用外部渲染工具（如 Ghostscript 或 `pdftoppm` 结合重新组装技术）作为备用方案。
- **需要显示外观标志**：在完成表单填写后，只有当存在相应的外观流时，查看器才会渲染出字段的值。该填充脚本会设置 AcroForm 的 “NeedAppearances” 标志，促使符合标准的查看器重新生成这些外观流；不过部分简化版的查看器会忽略这一标志——因此，若对显示精度有较高要求，建议先进行展平处理。
- **非拉丁字符表单值**：表单数据会以 UTF-16 编码正确存储，但由于字段的默认字体可能不包含某些字符，即便数据已成功传输，查看器仍可能显示为空白。建议使用 `--fields` 参数进行验证，而不仅仅依赖视觉检查。
- **压缩效果预期**：`--compress` 参数仅能对内容流进行压缩处理，通常能带来的压缩率在 0% 到 20% 之间；对于以图像为主或已经过压缩的内容流，该功能则毫无作用。它并不能替代图像降采样处理（这类任务应由 Ghostscript 承担）。
- **权限标志并非强制约束**：所有者密码设置的权限位（如禁止打印、禁止复制）仅属于建议性要求，查看器可选择是否遵守；包括 pypdf 在内的任何库都可能读取并移除这些权限设置。唯有用户密码才能通过加密机制真正控制内容的访问权限。切勿将权限标志视为真正的安全保障。
- **表格提取为启发式处理**：pdfplumber会通过横线或文字对齐方式来识别表格；无边框或合并单元格的表格可能需要调整`table_settings`参数或进行手动清理。
- **页面索引**：辅助CLI工具以1为起始页码，而pypdf API则采用0为起始页码。相关脚本会自动完成页码转换，无需重复转换。
- **旋转文字提取**：pdfplumber的行分组功能会导致旋转字体出现混乱（例如45°角度的“DRAFT”字样会被误识别为独立字母）；建议使用pypdf的`extract_text()`函数或渲染后的图像来核对旋转文字内容。
- **单选组**：ReportLab要求每个单选组至少包含2个`radio()`控件，填充字段需要使用带斜杠的导出值（如“/red”），且对于单选组而言，flatten fidelity功能的处理效果最差——详情请参阅`references/forms.md`。
- **元数据范围**：`pdf_meta.py`仅会写入传统的DocInfo字典；嵌入的XMP元数据（如有）将保持不变，且在某些查看器中可能会显示不同的数值。
- **PDF/A格式不在支持范围内**：pypdf和ReportLab均无法生成或验证符合标准的PDF/A文件。如果需要满足归档要求，需通过`terminal`工具调用Ghostscript（例如使用合适的ICC配置文件执行`gs -dPDFA=2 -dPDFACompatibilityPolicy=1 -sColorConversionStrategy=UseDeviceIndependentColor -sDEVICE=pdfwrite -o out.pdf in.pdf`命令），然后再用veraPDF进行验证——这两者均为外部安装程序，且最终结果仍需验证，不可直接认定合格。
- 旋转角度必须是90度的倍数；在进行任何其他操作之前，必须先解密加密过的输入文件。

## 验证

- 在创建、合并或拆分文档后：运行 `pdf_read.py out.pdf --meta`，确认页面总数以及页面旋转时的旋转角度。  
- 在提取内容后：检查 JSON 文件是否非空，并抽查其中的特定字符串或单元格内容。  
- 表单设计循环：执行 `pdf_form_layout.py spec.json` 后，其输出状态码必须为 0；随后运行 `--render-overlay boxes.png --pdf form.pdf` 生成叠加图，再使用 `vision_analyze` 工具对该 PNG 文件进行分析（红色区域表示带有字段名称的输入框，蓝色区域表示标签框），检查是否存在重叠、错位或标签与对应字段分离的问题。重复执行“设计规范校验 → 叠加图生成”步骤，直至结果符合要求。  
- 在表单构建完成后：运行 `pdf_read.py form.pdf --fields`，即可查看所有包含类型及选项的表单字段信息。  
- 在完成表单填写后：运行 `pdf_read.py filled.pdf --fields`，并对比各字段的值（包括非 ASCII 字符在内的精确匹配）。  
- 在添加印章后：重新提取文本（对于旋转方向的印章可使用 pypdf 工具），或通过 `pdf_page_image.py` 生成页面图像，再使用 `vision_analyze` 进行检查。  
- 在修改元数据或附件后：分别运行 `pdf_read.py --meta` 和 `pdf_meta.py --list-attachments`，并重新提取附件以进行字节级比对。  
- 在文档加密后：执行 `--meta` 命令会显示 `"encrypted": true`，且未输入密码则无法打开文件；解密后，文本提取结果应与原始内容一致。  
- 对于任何涉及视觉元素的场景（如水印、扁平化表单等），均需先生成图像，再使用 `vision_analyze` 工具进行检测。
