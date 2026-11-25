---
name: docx
description: Create, read, edit, template, and review Word .docx files.
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [word, docx, documents, office, templates, revisions, comments]
    category: productivity
    related_skills: [pdf, xlsx, powerpoint]
---

# Docx技能

通过轻量级CLI工具，利用python-docx库实现Microsoft Word `.docx`文件的创建、读取、编辑及模板处理。该技能可处理文本、样式、列表、表格、图片、页眉/页脚、`{{token}}`模板替换、修订标记（列出/接受/拒绝）、评论（列出/添加/删除）、目录及页码字段，同时还具备文件健康状态检测功能。需要注意的是，它本身不负责文档的渲染（生成PDF需使用LibreOffice——详见“转换为PDF”部分），也不支持对旧版`.doc`格式文件的编辑。

## 适用场景

- 用户要求生成Word文档（如报告、信函、合同）。
- 需要获取`.docx`文件中的文本内容、大纲、样式或嵌入图片。
- 需要修改现有的`.docx`文件：替换文本、编辑表格单元格、插入/删除段落、应用样式、合并分散的文字块。
- 拥有包含`{{placeholders}}`占位符的`.docx`模板，需根据数据填充内容。
- 文档存在需要审核、接受或拒绝的修订标记。
- 需要读取审阅者的评论，或添加/删除自己的评论。
- `.docx`文件无法打开或行为异常，需要进行文件损坏诊断。
- 文档需要添加目录或“第X页，共Y页”的页脚。
- **不适用于**：旧版`.doc`格式、`.odt`格式，以及需实时预览布局的文档处理。

## 先决条件

- 安装了Python 3.10及以上版本，并已安装`python-docx`库：
  `pip install python-docx`（导入时使用名称`docx`；该库会自动包含lxml）。
- 对于评论的“添加”操作，若使用的是python-docx 1.2及以上版本，则会调用其内置API；在较低版本中则会自动回退到XML处理方式。
- 对于图片块：相关图片文件必须存储在本地（支持PNG/JPEG格式）。

## 使用方法

所有辅助工具均保存在当前文件所在目录下的 `scripts/` 文件夹中。可通过 `terminal` 工具来运行它们；每个工具都支持 `--help` 参数，并会将结果以 JSON 格式输出到标准输出流中。

```bash
python scripts/docx_create.py spec.json out.docx
python scripts/docx_read.py out.docx --text
python scripts/docx_edit.py replace out.docx --find old --replace new
python scripts/docx_template.py tpl.docx values.json filled.docx
python scripts/docx_revisions.py list out.docx
python scripts/docx_comments.py list out.docx
python scripts/docx_validate.py out.docx
```

## 快速参考指南

| Task | Command |
| --- | --- |
| Create from JSON spec | `docx_create.py spec.json out.docx` |
| Full text (body+tables+headers/footers) | `docx_read.py f.docx --text` |
| Heading outline + table shapes | `docx_read.py f.docx --structure` |
| Styles actually used | `docx_read.py f.docx --styles` |
| Extract embedded images | `docx_read.py f.docx --images outdir/` |
| Detect tracked changes/comments | `docx_read.py f.docx --revisions` |
| Find/replace (formatting kept) | `docx_edit.py replace f.docx --find A --replace B -o out.docx` |
| Set a table cell | `docx_edit.py set-cell f.docx --table 0 --row 1 --col 2 --text X` |
| Insert paragraph before index N | `docx_edit.py insert f.docx --index N --text X --style Normal` |
| Delete paragraph N | `docx_edit.py delete f.docx --index N` |
| Apply style to paragraph N | `docx_edit.py style f.docx --index N --style "Heading 1"` |
| Merge equal-format adjacent runs | `docx_edit.py normalize f.docx -o out.docx` |
| Insert TOC field before para N | `docx_edit.py toc f.docx --index N -o out.docx` |
| "Page X of Y" footer fields | `docx_edit.py page-numbers f.docx` |
| Fill `{{tokens}}` | `docx_template.py tpl.docx values.json out.docx --strict` |
| List revisions (id/author/date/text) | `docx_revisions.py list f.docx` |
| Accept / reject all revisions | `docx_revisions.py accept-all f.docx -o out.docx` (or `reject-all`) |
| Accept / reject one revision | `docx_revisions.py accept f.docx --id 3 -o out.docx` |
| List comments (+anchored text) | `docx_comments.py list f.docx` |
| Add comment anchored to text | `docx_comments.py add f.docx --target "phrase" --text "note" --author You` |
| Delete comment by id | `docx_comments.py delete f.docx --id 0` |
| Health-check the package | `docx_validate.py f.docx` (exit 1 on errors) |

## 操作步骤

1. **创建。** 使用 `write_file` 函数编写 JSON 配置文件，随后运行 `scripts/docx_create.py` 脚本。该配置文件支持以下元素：`page`（以毫米为单位指定的页面尺寸及页边距）、`header`/`footer` 字符串、`footer_page_numbers`（用于在页脚添加“第 X 页，共 Y 页”的提示）、`styles`（可自定义段落样式，包括字体、字号、粗体/斜体以及十六进制颜色值），还有各种内容块——`heading`（1 至 9 级标题）、`paragraph`（可为纯文本，也可为 `runs` 列表，其中每个元素可设置粗体/斜体/下划线格式）、`bullet_list`（项目列表）、`numbered_list`（编号列表）、`table`（表头行会以粗体显示，还包括表身行数，以及可选的内置表格样式，如“网格表”）、`image`（图像路径，可指定宽度毫米值）、`toc`（目录字段）以及 `page_break`（分页符）。完整的配置文件格式说明详见 `scripts/docx_create.py` 文件的开头部分。

2. **读取。** 使用 `scripts/docx_read.py` 脚本，并仅指定一个模式参数。`--text` 模式会以 JSON 格式返回正文段落、所有表格单元格内容以及页眉页脚文本；`--structure` 模式则输出标题层级结构以及段落、表格和章节的计数信息；`--images DIR` 模式会将 `word/media/` 目录下的所有文件复制到项目外部。
3. **编辑功能**。可使用 `scripts/docx_edit.py` 工具。该工具会遍历正文、表格（包括嵌套表格）、页眉及页脚，并保留原有的排版格式；若需跳过页眉/页脚，可添加 `--body-only` 参数。若希望保留原文档内容，可指定 `-o out.docx` 参数，否则将直接在原文件中进行编辑。`insert`/`delete`/`style`/`toc` 等操作所涉及的段落编号，均依据 `--structure`/`--text` 所定义的正文顺序来确定。对于经过大量 Word 编辑后的文档，建议先运行 `normalize` 工具，该工具会将格式相同的相邻文本块合并，从而确保后续的查找替换操作能够准确匹配。

4. **审阅修订内容**。`docx_revisions.py list` 可列出正文、表格、页眉或页脚中所有的 `w:ins` 和 `w:del` 修订记录，包括其编号、操作者、日期以及受影响的文本内容。`accept-all`/`reject-all` 可批量处理这些修订；而 `accept`/`reject --id N` 则用于处理单个修订。选择“接受”操作会将新增内容保留，同时删除被移除的文本；选择“拒绝”则反之。

5. **注释功能**。`docx_comments.py list` 可显示每条注释的编号、操作者、日期、注释内容以及该注释所关联的文档文本。使用 `add --target "某短语"` 可将新注释添加到文档中该短语的第一个出现位置（必要时会拆分文本块，同时保留原有格式）。`delete --id N` 可删除指定编号的注释及其标记，而不会影响文档中的文本内容。

6. **模板功能**。可在文档中插入类似 `{{name}}` 格式的占位符，然后使用 `scripts/docx_template.py` 工具并结合 JSON 格式的值数据进行填充。若遇到未填充的占位符，可使用 `--strict` 参数强制报错；无论是否填充完成，该工具的 JSON 输出都会列出已填充的占位符数量以及仍为空的占位符列表。
7. **验证**（始终执行）：使用 `--text` 或 `--structure` 选项重新查看输出结果，并对通过修订/注释操作生成的任何内容运行 `docx_validate.py` 脚本进行验证。

## 转换为 PDF 格式

无需编写脚本。只要安装了 LibreOffice，即可直接在后台进行转换：

```bash
soffice --headless --convert-to pdf --outdir outdir/ file.docx
```

请先检查相关软件是否可用（`command -v soffice || command -v libreoffice`）。如果两者均不存在，则应告知用户当前环境不支持 PDF 转换，而非临时凑合处理——因为 python-docx 无法渲染 PDF，而要保证布局精度则必须使用专业的渲染工具。

## 常见问题

- **分次运行导致的标记拆分**。Word 经常会将文本拆分为多个处理单元。替换功能会合并匹配到的这些单元（替换内容会沿用第一个单元的格式）；因此先运行 `docx_edit.py normalize` 可以减少后续所有编辑中的文本拆分现象。
- **修订记录的处理**。`docx_revisions.py` 能够处理大部分基于处理单元级别的插入和删除操作。段落标记、表格行的修改、格式变更记录以及文档移动操作虽然能被 `--revisions` 参数检测到，但不会自动处理——详情请参阅 `references/revisions-and-comments.md`，此类修订需手动交由 Word 处理。
- **评论的关联机制**。回复及“已解决”状态存储在 `commentsExtended.xml` 文件中，而该功能会忽略此文件；它所添加的评论仅为普通顶层评论。
- **字段内容由 Word 计算**。`toc`、`page-numbers` 以及 `toc`/`footer_page_numbers` 等格式选项仅会写入*字段代码*。实际的内容和编号需在打开文档时由 Word/LibreOffice 填充（Word 可能会提示更新字段）；python-docx 从不进行此类计算，因此在字段内容生成前会显示占位文本。
- **验证属于健康检查，而非模式验证。**  
  `docx_validate.py` 会检查 ZIP 文件结构、必需组件、关联目标、图像魔数以及引用的样式。这并非 XSD 验证——即使文件通过验证，其中仍可能包含 Word 不支持的 XML 内容。

- **样式名称必须存在。** 若应用文档中未定义的样式，将会引发 `KeyError` 错误。默认模板中已预置了 `Heading 1`、`List Bullet`、`List Number`、`Table Grid` 等内置样式；自定义样式则需先在创建规范中进行定义。

- **编号列表会重新计数。** `List Number` 功能依赖于 Word 的默认编号规则，因此同一文档中的多个独立列表可能会连续编号而非重新开始。对于需要精确控制多列表编号的场景，请及时提醒用户注意这一点。

- **单元格写入会覆盖原有格式。** `set-cell` 函数通过 `cell.text = ...` 的方式设置内容，这会导致该单元格内的所有格式设置被重置为纯文本格式。

- **编码问题。** 所有的 JSON 规范文件和值文件都会以 UTF-8 编码形式被读取；在编写自定义处理代码时，切勿依赖系统的默认区域设置。

- **切勿直接解压后使用 sed 修改 XML 文件。** 应通过脚本（或 python-docx 库）来进行编辑；直接在 `document.xml` 文件中替换文本很容易导致文件损坏。仅应对 JSON 格式的输入文件使用 `patch`/`write_file` 函数，而绝不能用于 `.docx` 文件本身。

## 验证流程

- 在创建、编辑或处理模板后，运行 `docx_read.py out.docx --text`，并确认预期的字符串已出现（而旧字符串已消失）。  
- 在接受或拒绝修改后，`docx_revisions.py list` 的输出应为 `[]`（或仅包含您有意保留的标识符）；在处理注释后，`docx_comments.py list` 应能反映相应变化，且使用 `--text` 生成的输出内容必须保持不变。  
- 对于结构正常的文档包，`docx_validate.py out.docx` 执行后会以状态码 0 和 `"ok": true` 的结果退出——请在进行任何修改、注释处理或字段操作后运行该命令。  
- 对于使用 `--strict` 参数运行的模板，需检查 `unfilled_tokens == []` 是否成立。  
- 结构检查：使用 `--structure` 可查看预期的标题层级结构与表格样式；使用 `--styles` 可确认自定义样式是否已正确应用。
