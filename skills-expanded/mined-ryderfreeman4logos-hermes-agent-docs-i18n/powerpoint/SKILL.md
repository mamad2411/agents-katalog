---
name: powerpoint
description: Create, read, edit .pptx decks with python-pptx.
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pptx, powerpoint, presentations, slides, office, python-pptx]
    category: productivity
    related_skills: [docx, xlsx, pdf]
---

# PowerPoint技能

利用python-pptx库创建、查看和编辑PowerPoint（.pptx）演示文稿。该技能包含五个辅助脚本，可实现基于JSON配置的演示文稿生成、结构化内容读取、直接编辑、基于模板的品牌化演示文稿制作以及幻灯片渲染功能——所有操作均在离线环境下完成，无需安装PowerPoint。

## 适用场景

- 用户需要制作幻灯片集、报告演示或项目推介演示文稿。
- 需要从他人共享的.pptx文件中提取文本、备注、表格、图表数据或图片。
- 需要更新现有演示文稿：替换文本内容、刷新或修正图表数据、更换LOGO、复制/删除/重新排序幻灯片、设置背景、页脚、超链接或演讲者备注。
- 需要根据公司的.pptx模板制作符合品牌风格的演示文稿。
- **请勿**将此技能用于传统的.ppt二进制文件——如果安装了LibreOffice，可先使用`soffice --convert-to pptx old.ppt`命令将其转换。

## 前提条件

- 安装了python-pptx的Python 3.10+版本（可通过`pip install python-pptx`安装）。
- 可选：LibreOffice（`soffice`）以及poppler工具（`pdftoppm`或`pdftocairo`），用于将幻灯片渲染为PNG格式或导出PDF文件。`pptx_render.py`会通过`shutil.which`函数检测这些工具的存在情况；若缺失，它会以优雅的方式降级处理（输出`{"rendered": false, "missing": [...]}`，并返回代码0），此时所有创建/读取/编辑操作仍可正常进行。
- 可通过终端检查相关工具是否已安装：
  `python -c "import pptx; print(pptx.__version__)"`以及`which soffice pdftoppm`。

## 运行方法

所有脚本均存放于 `scripts/` 目录中，执行时会输出 `--help` 参数信息、将结果以 JSON 格式打印到标准输出，并在出现错误时以非零状态码退出。可通过 `terminal` 命令来运行这些脚本：

```bash
python scripts/pptx_create.py deck.json out.pptx
python scripts/pptx_read.py deck.pptx --outline      # full JSON outline
python scripts/pptx_read.py deck.pptx --notes        # speaker notes
python scripts/pptx_read.py deck.pptx --images ./img # export pictures
python scripts/pptx_edit.py deck.pptx --replace-text "Old Corp" "New Corp"
python scripts/pptx_edit.py deck.pptx --chart-data update.json
python scripts/pptx_edit.py deck.pptx --duplicate-slide 2
python scripts/pptx_edit.py deck.pptx --remove-slide 3 --move-slide 2 0
python scripts/pptx_from_template.py brand.pptx out.pptx --values vals.json
python scripts/pptx_render.py deck.pptx --outdir ./render  # slide PNGs
```

使用 `write_file` 函数编写 JSON 规范文件；使用 `read_file` 函数查看脚本输出及生成的 JSON 文件。

## 快速参考

| 任务 | 命令 |
|---|---|
| 根据规范创建演示文稿 | `pptx_create.py spec.json out.pptx` |
| 16:9与4:3比例 | 在规范文件中指定 `"slide_size": "16:9"` 或 `"4:3"` |
| 以JSON格式导出大纲 | `pptx_read.py deck.pptx --outline` |
| 导出图片 | `pptx_read.py deck.pptx --images DIR` |
| 替换文本 | `pptx_edit.py deck.pptx --replace-text OLD NEW` |
| 更改图表数据 | `pptx_edit.py deck.pptx --chart-data spec.json` |
| 修改单个数据系列 | 使用相同参数，规范文件中需包含 `"ops"` 字段（详见下文） |
| 交换图片 | `pptx_edit.py deck.pptx --swap-image N NAME new.png` |
| 复制幻灯片 | `pptx_edit.py deck.pptx --duplicate-slide N` |
| 删除幻灯片 | `pptx_edit.py deck.pptx --remove-slide N` |
| 重新排序幻灯片 | `pptx_edit.py deck.pptx --move-slide FROM TO` |
| 设置幻灯片背景 | `pptx_edit.py deck.pptx --set-background N RRGGBB` |
| 设置超链接 | `pptx_edit.py deck.pptx --hyperlink N TEXT URL` |
| 显示幻灯片编号 | `pptx_edit.py deck.pptx --enable-slide-number N` |
| 设置页脚文字 | `pptx_edit.py deck.pptx --set-footer N TEXT` |
| 设置备注 | `pptx_edit.py deck.pptx --set-notes N TEXT` |
| 追加备注 | `pptx_edit.py deck.pptx --append-notes N TEXT` |
| 填充模板内容 | `pptx_from_template.py tpl.pptx out.pptx --values v.json` |
| 生成幻灯片PNG图片 | `pptx_render.py deck.pptx --outdir DIR` |

## 操作步骤

### 1. 创建演示文稿

首先编写一个 JSON 规范文件（完整格式请参见 `pptx_create.py --help`），随后运行 `pptx_create.py`。针对每张幻灯片，可设置以下参数：`layout`（包括 title、title_content、section、two_content、title_only、blank 等选项）、`title`、`subtitle`、`bullets`（可为字符串，也可为包含层级 level 0-4、字号 pt、加粗/斜体、字体、十六进制颜色以及超链接地址 link 的字典）、`background`（纯色十六进制代码）、`footer`（文本；可启用该布局的页脚占位符）、`slide_number`（true 值；可启用该布局的幻灯片编号占位符）、`images`（图片路径及左侧/顶部位置和英寸单位的宽度/高度）、`tables`（以列表的嵌套列表形式表示的行数）、`shapes`（矩形、圆角矩形、椭圆、菱形、右箭头、人字形等形状，可指定填充色十六进制代码以及可选的文字内容）、`charts`（包括条形图、垂直条形图、折线图、饼图，需提供 categories、series 参数）以及 `notes`（演讲者备注）。

### 2. 读取演示文稿

使用命令 `pptx_read.py deck.pptx --outline` 可获取幻灯片尺寸、布局信息，以及每张幻灯片的布局名称、所有形状中的文字内容、表格单元格数据、图片信息（包括文件名、扩展名和字节大小）、图表的分类/系列/数值数据，还有演讲者备注。如需将嵌入的图片导出为独立文件，可使用 `--images DIR` 参数指定目录，之后若需要查看这些图片的内容，可对导出的图片使用 `vision_analyze` 命令进行分析。

### 3. 编辑演示文稿

`pptx_edit.py`能够一次性完成多项操作；若需保留原始文件，请使用`--output`参数。文本替换功能会遍历幻灯片形状、表格单元格以及备注内容。图片替换则会重新设置图片的关系标识，从而确保其位置和大小不受影响。删除幻灯片时会同时移除相关关系及`<p:sldId>`条目；而重新排序操作则会在`<p:sldIdLst>`内部调整`<p:sldId>`元素的顺序（python-pptx并未提供相应的公共API，因此这些操作均由脚本在XML层面完成）。使用`--duplicate-slide N`参数可复制第N张幻灯片的独立深拷贝：形状的XML结构以及图片/媒体/超链接关系都会被克隆，同时关系标识也会被重新映射，这样对副本的修改就不会影响到原始文件。该工具不支持对图表幻灯片进行操作（详见“注意事项”部分）。`--set-notes`/`--append-notes`用于编辑演讲者备注；而`--set-background`、`--hyperlink`、`--enable-slide-number`以及`--set-footer`则用于优化演示文稿的整体外观。

要更新图表，可通过`--chart-data`参数传入JSON格式的配置。完整替换的配置格式为：`{"slide": 0, "chart": 0, "categories": [...], "series": {...}}`。若需进行精确调整，可传入`"ops"`参数，其值为一个操作列表，包含`{"op": "update_series", "name": ..., "values": [...]}`、`add_series`、`remove_series`、`rename_category`（支持`from`/`to`或`index`格式）以及`set_title`等操作。由于python-pptx仅能整体替换图表的数据集（即使用`replace_data`功能），因此这些操作实际上是通过“读取现有数据→修改数据→替换数据”的流程来实现的；针对各组成部分的交互界面仅起到封装作用，任何无法表示为类别与数值序列形式的图表数据，在经过这种往返处理后都会被标准化。

### 4. 基于模板创建演示文稿

`pptx_from_template.py` 可以打开一个品牌主题的 .pptx 文件，替换所有幻灯片、表格及备注中来自值 JSON 的 `{{token}}` 占位符，同时还能根据模板预设的布局名称或索引添加新幻灯片，这些新幻灯片将自动继承母版中的字体与颜色设置。提示：如果使用的是没有幻灯片的模板，可以先用 `pptx_edit.py --remove-slide` 删除现有幻灯片。

### 5. 视觉验证

`pptx_render.py deck.pptx --outdir ./render` 会通过 `soffice --headless` 将演示文稿转换为 PDF 格式，再利用 `pdftoppm`（或 `pdftocairo`）将每张幻灯片拆分为独立的 PNG 文件。生成的 JSON 文件会列出所有 PNG 文件的路径——可使用 `vision_analyze` 工具逐一查看这些文件。如果缺少上述任一工具，脚本将输出 `{"rendered": false, "missing": [...]}` 及相关提示并以代码 0 退出；此时可退而使用 `pptx_read.py` 生成的 JSON 大纲，该大纲仅能验证内容与结构，无法检查视觉效果。

## 转换为 PDF

如果已安装 LibreOffice，可直接将处理完成的演示文稿导出为 PDF 格式：

```bash
soffice --headless --convert-to pdf --outdir ./out deck.pptx
```

处理结果将保存在 `./out/deck.pdf` 文件中。对于主机上未安装的字体，系统会自动替换，因此在发送 PDF 之前请务必执行渲染验证（步骤 5）。目前没有纯 Python 的离线 .pptx→PDF 转换方案；如果系统中没有安装 `soffice`，应直接说明情况，而不要尝试强行替代。

## 常见问题

- **文本分段问题**：PowerPoint 会在拼写检查及编辑边界处将段落文本拆分成多个片段。`--replace-text` 参数会首先合并格式相同的相邻片段，因此跨这些片段出现的匹配内容会被完整保留格式地替换。只有当匹配内容涉及*格式确实不同*的片段时，段落才会被重写为第一个片段的格式——请在替换后检查相关幻灯片。
- **图表幻灯片无法复制**：每个图表都包含独立的 XLSX 工作簿部分，系统不支持可靠地复制此类图表，因此 `--duplicate-slide` 参数会直接拒绝复制图表幻灯片，以避免损坏整个演示文稿。建议在新的幻灯片中重新创建图表。外部超链接以及图片/媒体引用会被保留，而布局和备注相关内容则会被重新生成。
- **图表操作仅为封装层**：python-pptx 实际上是替换整个数据集；`"ops"` 参数仅通过 `replace_data` 函数对现有图表数据进行处理，因此无法更改图表的*类型*。
- **重排序需在 XML 层级进行**：python-pptx 不提供专门的重排序接口。`--move-slide` 参数会直接操作 `<p:sldIdLst>` 元素，虽然对于普通演示文稿是安全的，但操作后仍建议重新读取演示文稿以确认结果。
- **不支持在多个演示文稿之间复制幻灯片**——仅可在同一演示文稿内进行复制，因为该场景下各幻灯片的布局和母版是共享的。
- 启用页脚/幻灯片编号功能时会从对应幻灯片布局中复制占位符；对于没有这些占位符的布局，使用 `--set-footer` 会报出明确的错误信息（建议改用文本框）。
- 超链接适用于整个演示文稿序列；`--hyperlink` 选项会将该幻灯片上包含指定文本的所有序列项都设为超链接。
- 默认的 python-pptx 模板比例为 4:3；除非规格另有规定，否则创建脚本会使用 16:9 的比例。自定义模板则保留其原有的尺寸比例。
- 不同模板对应的布局索引各不相同。对于品牌专用模板，需先列出所有布局名称：`pptx_read.py template.pptx --outline`（可查看 `layouts_available` 输出）。
- 空白布局的 `slide.shapes.title` 属性值为 None——创建脚本已处理了这种情况，但在编写自定义的 python-pptx 代码时需牢记这一点。
- 在编写规格文件时，请始终指定 `encoding="utf-8"`，因为诸如 `{{city}}` 这样的占位符可能会被非 ASCII 字符填充。

## 验证

1. 在完成任何创建或编辑操作后，运行 `pptx_read.py OUT.pptx --outline`，并检查幻灯片数量、文本内容、表格信息、备注内容以及图表数值是否与预期一致。  
2. 使用 `--images DIR` 参数后再通过文件大小检查，可确认图片是否已正确嵌入文档中。  
3. 通过 `pptx_render.py deck.pptx --outdir ./render` 命令渲染所有幻灯片，随后使用 `vision_analyze` 工具逐一查看生成的 PNG 文件——该工具能够检测出轮廓分析无法发现的元素重叠、文本截断以及颜色问题。若缺少相应的渲染工具，脚本会给出提示，此时仍应以轮廓分析结果为准。  
4. 所附带的测试套件即构成了完整的验证标准：运行 `python -m pytest tests/ -q` 即可进行测试（需安装 python-pptx 和 pytest 工具）。
