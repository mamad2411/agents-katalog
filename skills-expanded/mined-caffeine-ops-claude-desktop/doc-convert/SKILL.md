---
name: doc-convert
description: "Use this skill for document work — converting formats (Markdown to Word, Word to PDF, Excel to/from CSV, PDF merge/split/delete/watermark), extracting text from images and scans (OCR), pulling tables out of PDFs into Excel, turning batches of receipts or invoices into a structured spreadsheet, and summarizing or outlining long documents. 文档处理：提取文字、表格台账、格式转换。"
---

# 文档处理（Document Convert）

用户丢进一份文件、想要另一种格式或想要里面的内容时用这个技能。能力分两类，
走的路子完全不同，**先分清自己在哪一类**：

- **B 类 · 确定性转换**（格式互转、PDF 页面操作）——**一律调脚本，不要自己现写
  Python**。脚本里已经处理了中文编码、页码换算、字体缺失等一堆坑，现写必然踩回去。
- **A 类 · 需要看懂内容**（提取文字、抽表格、票据台账、长文档提炼）——脚本负责
  取料和装配，**你负责看懂**，中间用 JSON 交接。你**永远不直接生成 xlsx/docx**，
  一律产出 JSON 交给装配脚本写盘。

## 运行环境（先读这一段）

所有 Python 工作走本技能专属 venv。每个会话开始时引导一次：

```bash
# macOS / Linux —— 必须用 `source`（脚本要把 $DOC_CONVERT_PY 导回你的 shell）
source ${SKILL_DIR}/bin/ensure-python.sh
"$DOC_CONVERT_PY" -c "import pypdf, docx, openpyxl, reportlab, pdfplumber, pypdfium2, PIL; print('ok')"
```

> **Windows**：改跑 `${SKILL_DIR}\bin\ensure-python.cmd`，它末行打印
> `DOC_CONVERT_PY=<path>`，后续所有 python 命令用那个路径。

- 首次运行要下载依赖（约几分钟），之后靠哨兵文件秒过。**开始前告诉用户这次要等**。
- skill 目录在打包后的 app 里是**只读**的。永远不要往 `${SKILL_DIR}` 里写东西，
  也不要往自带 runtime 里 pip install。所有产物写到会话工作目录。

## A 类 · 需要看懂内容（走模型）

### 铁律一：你只输出 JSON，装配交给脚本

不要自己写 openpyxl、不要自己拼 docx。理由有两条，第二条更重要：

1. 你每次现写的代码都不一样，输出不稳定。
2. **确定性质检需要一个落点。**「行列对不齐」「偷偷加了一列」「一半字段没认出来」
   这些判断必须由代码执行——让你自查等于没查。

### 铁律二：拿不准就留空，绝不猜

拿不准的字段**留空**，另在 `_存疑` 里写清字段名和原因：

```json
{ "日期": "2026-03-01", "金额": null, "开票方": "某某科技有限公司",
  "来源文件": "IMG_0012.jpg",
  "_存疑": [{ "字段": "金额", "原因": "折痕遮挡，只能看到 1?8.50" }],
  "_来源": "IMG_0012.jpg" }
```

**`null` 且不在 `_存疑` 里 = 票据上本来就没这项**，与「看不清」严格区分。
把「本来就没有」也标成看不清会制造大量假警报，用户三天就学会无视所有黄格子，
标记随之失效。

⚠️ **`_来源` 和「来源文件」是两回事，别以为写了 `_来源` 就等于给表格填上了
产地。** `_来源` 只会被 `rows_to_xlsx.py` 抄进「待核对」小表（来源 / 字段 /
原因三列），**不会**写进任何数据列——一行如果没有任何 `_存疑`，`_来源`
根本不会出现在任何地方，产地信息就此彻底丢失。台账/表格本身要显示"这行数据
来自哪张图/哪一页"，必须**另外**给一个落在表头里的正常字段（就是上面例子里
新加的 `"来源文件"`）。两者缺一不可：`_来源` 服务于人工核对存疑项，
「来源文件」服务于表格本身的可追溯性。

数值型字段用 JSON number（`128.5`）而不是字符串（`"128.5"`）——
装配脚本据此决定写数值还是写文本，**只有真数值才能被 Excel 的 `=SUM()` 算进去**。

⚠️ **例外：编号类字段一律用字符串，哪怕它全是数字。** 发票号 / 银行账号 /
身份证号 / 各类单号不是数值，是长得像数字的标识符——它们不该被求和，也不该被
四舍五入。Excel 的数字只能保 15 位有效精度，发票号常见 20 位，按 number 写进去
会被静默截断+转成科学计数法：`24312000000123456789` 会变成
`2.43120000001235E+019`，**后 5 位直接丢了，用户还看不出来**。这正是本技能要
挡住的「看起来正常、实则数字有缺陷」——遇到这类字段，无论原文是不是纯数字，
一律输出成 JSON 字符串（`"24312000000123456789"`）。

### 铁律三：批量任务边跑边落盘

一次超过约 20 张图 / 60 页，**先告诉用户大概要多久、征得同意再开工**。
识别一条就往中间文件追加一条（`.jsonl`，一行一条 JSON），别攒到最后一次性写——
中途被打断时前面的成果才不会白费，重跑只补没做完的。

### A1. 图片提取文字

```bash
# 先规格化（HEIC 解码 + 缩到模型能高效读的尺寸）
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/img_prep.py 照片.HEIC -d 处理后/
```

然后**你自己读** `img_prep.py` 输出 JSON 里 `items[].output` 给出的那个路径
（同名撞车时脚本会自动换成 `stem-2.jpg`、`stem-3.jpg`……不一定就是
`处理后/照片.jpg`，别按目录读图、别自己拼路径——部分失败重跑时目录里可能
留有同一张图的多个版本，按目录读会把它认成两张不同的图），输出 **Markdown**。

⛔ **只还原图上肉眼可见的结构**（标题、列表、简单表格）。
**不新增层级、不改写措辞、不补全句子。** 版面还原和内容创作只隔一层窗户纸，
越界就成了另一种幻觉——用户拿到的会是一份「读起来很顺、但不是原文」的东西。

看不清的字用 `【无法识别】` 占位，文末附「待核对」小节标明位置。

用户要 Word 时，把这份 Markdown 交给已有的 `md_to_docx.py`，**不要另想办法**：

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/md_to_docx.py 提取结果.md -o 提取结果.docx
```

表格会被转成真正的 Word 表格（表头加粗、带边框）。别指望合并单元格——不
支持，会原样进文字。单元格里不能用 `\|` 转义竖线——它仍会被当成列分隔符：
在数据行会直接报错拒绝，在表头行会多切出一列且不报错。表格里需要竖线时
改用全角 `｜` 等其他符号。

整张图一个字都认不出、或根本不是文字图片时，**不产出文件**，直接告诉用户。

### A2. PDF 表格转 Excel

```bash
# 1. 抽表 + 体检（有没有文字层）
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_tables.py 报价单.pdf -o 表格.json
# 只看某几页（比如报表很长，先只抽你关心的部分）：
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_tables.py 报价单.pdf --pages "3-4" -o 表格.json

# 2. 把相关页渲染成图，供你核对
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_render.py 报价单.pdf --pages "3-4" -d 页图/
# 某一页数字实在看不清，只对那一页调高渲染倍率（上限 4，别整份提高）：
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_render.py 报价单.pdf --pages "4" -d 页图/ --scale 4
```

分流看 `表格.json` 的 `tables` 是不是空的，**不能只看 `scanned`**——
`scanned: true` 但 `tables` 非空是真实会发生的情况（整页文字层稀薄，但表格
本身靠线框/单元格结构被正常抽出来了），此时数字仍然是坐标直读的，不是看图认的。

⚠ **`scanned` 只是选中页（`--pages` 给的那几页；不给就是全文）的判定，不是整份
文档的属性**——`scanned_scope` 字段会写明这次判定的作用域（`selected_pages`
或 `all_pages`）。`--pages "3-4"` 恰好点到两页插图会把这两页报成 `scanned: true`，
不代表其余几十页也是扫描件，别把它当整份 PDF 的结论来交付。

**`tables` 非空——你只准改结构，不准改数字，跟 `scanned` 是 true 还是 false 无关。**
脚本抽出来的数字是按坐标从文件里直接读的，逐字准确；你是看图认字，会看错小数点。
你负责的是：合并跨页表头、把挤在一起的两张表拆开、剔除混进表里的页眉页脚行。
**你若觉得某个数字抽错了，不许自己改，记进 `_存疑` 交给人看。**
这时如果 `scanned` 恰好也是 true，交付仍要提醒用户"这份 PDF 整体文字层稀薄"，
但数字本身不用重新看图核对。

⚠ **「不准改数字」指的是不准改值，类型转换是必须做的**：从 `表格.json` 转成
`rows` 时，数字列的字符串要原样转成 JSON number（`"1200.50"` → `1200.50`；
去掉千分位逗号也属于只改形式不改值，比如 `"1,200.50"` → `1200.50`），文本列
保持字符串，编号类字段（发票号/账号/单号）按前面铁律二一律保持字符串不转
number。这一步不做，Excel 里的数字列会是文本，`=SUM()` 得 0——这不是「改了
数字」，是没把字符串转成该有的类型。

**`tables` 为空（此时 `scanned` 一定是 true——不是扫描件却一张表都没有，脚本已经
报错拒绝了，不会走到这一步）——只能看图读数**，此时全套「拿不准就留空」生效，
并且**交付时必须显眼地告诉用户**：「这份是扫描件，数字是认出来的不是读出来的，
请务必核对，财务用途请以原件为准。」

最后装配。`rows_to_xlsx.py` 的 `.json` 输入**必须自带表头**，形状是
`{"headers": [...], "rows": [...]}`——跟 `pdf_tables.py` 输出的
`{"tables": [...]}` 是两种形状，需要你自己转一次，不能直接把 `表格.json` 传给它：

```json
{ "headers": ["品名", "数量", "单价"],
  "rows": [ { "品名": "Widget", "数量": 10, "单价": 5.0 } ] }
```

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/rows_to_xlsx.py 整理后.json -o 表格.xlsx --sheet 明细
```

（对比 A3：`.jsonl` 逐行追加、边跑边落盘，靠 `--headers` 给表头；
这里的 `.json` 是一次性给一整份，表头写在文件自己的 `headers` 字段里。）

### A3. 票据批量转台账

```bash
# 只写目录里真有的扩展名，别把两种都写进同一条命令——
# zsh 下通配符一个都没匹配到会直接报 "no matches found" 并拒绝执行整条命令
# （bash 会把字面量原样传给脚本，脚本再把它当"文件不存在"记进 failed，
# 同样是错的）。一批票据常常就是清一色一种格式，缺哪种就别写哪种。
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/img_prep.py 票据/*.jpg -d 处理后/
# 这批里如果也有 HEIC，再单跑一次：
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/img_prep.py 票据/*.HEIC -d 处理后/
```

**顺序不能颠倒：**

1. 先认 **1–2 张**做样本，把你打算出的列摊给用户确认一次。默认列是
   **日期 / 票据类型 / 开票方 / 金额 / 税额 / 发票号 / 摘要 / 来源文件**，
   原话大意——「我打算出这几列，火车票的车次要单独一列吗？」
   最后那列「来源文件」是刚需，**不许省**：用户核对时必须知道这行来自哪张图。
   填的是 `img_prep.py` 产出的 JSON 里 `items[].source`（用户原始文件名，
   比如 `IMG_0012.HEIC`），**不是**`items[].output` 那个规格化后的 `.jpg`
   文件名——你这一步实际读的图是 `items[].output` 给出的那个路径（同名撞
   车时脚本会自动换成 `stem-2.jpg`、`stem-3.jpg`……不一定就是
   `处理后/IMG_0012.jpg`，别自己拼路径），但要写进表格的是用户认得出的
   原名。
2. 用户确认后逐张认，**每认完一张立刻追加一行**到 `台账.jsonl`。
3. 全部完成后装配：

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/rows_to_xlsx.py 台账.jsonl -o 台账.xlsx \
  --headers 日期 票据类型 开票方 金额 税额 发票号 摘要 来源文件 --sheet 台账
```

读 `.jsonl` **必须**带 `--headers`（各行字段可能不齐，靠首行猜会静默漏列）。

某张图根本不是票据：那一行照样写进去，把情况写进 `_存疑`，**不要中断整批**。
**`_存疑` 里的「字段」必须是表头里已有的列名**（比如挂在「摘要」列上：
`{"字段": "摘要", "原因": "这张不是票据，是一张会议室预订单"}`）——写
「整张图」这种表头没有的名字，`rows_to_xlsx.py` 装配时会直接报错拒绝生成，
而且是在几十张全部认完之后才炸，返工代价很大，务必在认的时候就把字段名
落在真实列上。

### A4. 长文档提炼

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/doc_text.py 年报.pdf --outdir 取料/
```

stdout 会给一份体检报告：`units`（页数/段数）、`chars`（字数）、
`scanned`（是不是扫描件）、`scanned_units`（哪几页没有文字层）。

**开工前先问用户要哪一档**，用人话给选项：

> 你想要哪种？① **摘要**——几段话讲清这份文件说了什么；
> ② **大纲**——章节目录式的结构，方便你定位；
> ③ **完整 Markdown**——全文一字不落转成可编辑的格式。

然后按体检报告分流：

- `scanned: true` → 这份 PDF 没有文字层（扫描件），`doc_text.py` 抽不出东西。
  **改走：先用 `pdf_render.py 年报.pdf -d 页图/` 把页渲染成 PNG，再按 A1 的
  方式自己读图**——不要直接把 PDF 丢给 `img_prep.py`，它只吃图片格式（JPG/PNG/
  HEIC），见不得 PDF，传进去会直接报错。
- `scanned: false` 但 `scanned_units` 非空 → 混合型文档（大部分页有文字层，
  个别页是插图或扫描插页）。提炼时要在覆盖范围里点名这几页没有文字层、
  内容未覆盖，不能假装读完了全文。
- `chars > 30000` → **必须分块逐块读**（每块约 8000 字，块间重叠约 200 字防切断
  句子），每块出小结，最后合并。
- 其余 → 直接读取料文件。

⛔ **两条硬规矩：**

1. 产出开头必须写明覆盖范围，例如「本摘要基于第 1–58 页全文」。
   长文档最大的风险不是总结得不好，是只读了前面一小截就开始总结——
   写明范围是在逼自己确认真的读完了。
2. 关键数字与结论**必须带出处**（取料文件里的 `[P12]` / `[§34]` 锚点就是为此存在）。
   **原文没有的数字一个都不许出现。**

要 Word 时同 A1，走 `md_to_docx.py`——表格会一并转成 Word 表格。

## B 类 · 四条能力与对应脚本

### 1. Markdown → Word

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/md_to_docx.py 输入.md -o 输出.docx
```

支持 Markdown 常用子集（标题 / 段落 / 有序无序列表 / 表格 / 粗斜体 / 行内代码 /
围栏代码块 / 分隔线）。**不支持引用块、图片、链接语法**——遇到这些，
先把它们改写成受支持的形式再转，不要指望脚本处理。

表格每行必须以 `|` 开头，第二行必须是分隔行（如 `|---|---|`）——GFM 里
省略首竖线的写法本脚本不认，会被当成普通文本。表格数据行多于表头列数时
会报错拒绝（截断会丢内容），列数少会自动补空单元格。

### 2. Word → PDF

```bash
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/docx_to_pdf.py 输入.docx -o 输出.pdf
```

⛔ **这条有一道必须遵守的门禁。** 本机装了 LibreOffice 才能保留排版；没装时
脚本会**报错退出**，而不是悄悄降级。

收到这个报错时：**先把情况告诉用户，让他选，不要自作主张加 `--allow-textonly`。**
原话大意——

> 你电脑上没装 LibreOffice，我没法保留原来的排版。两个选择：
> ① 装一下 LibreOffice（免费）再转，排版能保住；
> ② 我直接转成纯文字版 PDF，但**表格、图片和所有排版都会丢**。
> 你要哪个？

用户明确选了②，才加 `--allow-textonly` 重跑。
用户没回答之前不要转。理由：纯文字版 PDF 看起来是个正常 PDF，用户很可能直接
拿去用（发客户、投标），发现丢了表格时已经晚了。

即便用户选了②走纯文字兜底，**这条路自己还有两道独立的拒绝**（见下面
「脚本会拒绝干活的几种情况」）：文档里提不出任何文字、或本机连中文字体都
找不到，两种情况脚本都不产出文件，不会给你一份空白 / 满纸方块的 PDF。

### 3. Excel ↔ CSV

```bash
# 方向按输入扩展名自动判定
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/excel_csv.py 输入.xlsx -o 输出.csv
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/excel_csv.py 输入.csv  -o 输出.xlsx
```

源文件有**多张工作表**时脚本会报错并列出表名，要求指定 `--sheet 表名`
（`--sheet` 只对 xlsx→csv 方向有意义）。这时问用户要哪一张，或者按他的需求
循环导出多次——**不要随便挑第一张**，那等于让用户丢数据还不知道。

导出的 CSV 带 UTF-8 BOM，Excel 双击打开中文不乱码。这是刻意的，别去掉。

⛔ **xlsx → csv 方向还有一道门禁：公式没有计算结果时脚本会拒绝导出。**
读 xlsx 拿到的是 Excel 上次保存时**缓存**下来的公式结果（这个工具不含公式
引擎，不会现算）。Excel / WPS 自己存的文件都带缓存值，但**程序生成的 xlsx
没有**——那些「合计 / 小计 / 同比」列导出来会整列是空的。脚本检测到这种
单元格就报错退出，不产出那份缺了汇总列的 CSV。

收到这个报错时**先把情况告诉用户，让他选，不要自作主张加
`--allow-empty-formulas`**。原话大意——

> 这份表里的合计类公式没有保存计算结果（多半是程序导出来的表），我直接转
> 的话那几列会是空的。两个选择：① 你用 Excel / WPS 打开它另存一次，公式就
> 有结果了，我再转；② 我照转，但那几个格子会空着。你要哪个？

用户明确选了②，才加 `--allow-empty-formulas` 重跑。

csv → xlsx 方向会做**保守的数字类型推断**：看起来是数值的格子（含千分位
写法）会写成真数值，转出来直接就能 `=SUM()`。四类格子会**刻意保留为文本**，
脚本转完会打印报告点名其中三类：前导零的（`007`）、纯整数 10 位以上的
（手机号/身份证号/发票号——转成数值会被 Excel 的 15 位精度静默截断成
科学计数法，宁可不转）、带小数但数字总位数超 15 位的（同一个精度坑的另一条
进口）；含任何非数字字符的格子也保留为文本，但作为普通文本静默处理。用户如果问"为什么这列不能求和"，把报告里的解释转达给他：在 Excel 
里选中该列改成数值格式即可，但编号类的列本来就不该参与计算。

### 4. PDF 页面操作

```bash
# 合并（按给定顺序）
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_ops.py merge a.pdf b.pdf -o 合并.pdf

# 拆分：一页一个文件
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_ops.py split 输入.pdf -d 输出目录/

# 拆分：按区间，每个区间一个文件
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_ops.py split 输入.pdf -d 输出目录/ --ranges "1-3,4-8"

# 删页
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_ops.py delete 输入.pdf -o 输出.pdf --pages "2,5-7"

# 加水印（水印是另一份 PDF 的第一页）
"$DOC_CONVERT_PY" ${SKILL_DIR}/scripts/pdf_ops.py watermark 输入.pdf -o 输出.pdf --stamp 水印.pdf
```

**页码一律 1 起、闭区间**，和用户嘴里说的一致（"删第 3 页"就是 `--pages 3`）。
越界会报错并告诉你总页数，不会静默截断。

#### 水印页从哪来

`watermark` 子命令只负责"叠加"，不负责"画"——它要的 `--stamp` 是一份**现成的**
水印 PDF。但用户说的是"给这份 PDF 加个'机密'水印"，他手上通常没有这份文件。

**这是本技能允许你自己现写 Python 的唯一例外**（开头"一律调脚本"的规矩在这里
不适用）：水印文字、字号、透明度、旋转角度因人而异，没法预先做成一个参数化脚本
覆盖所有情况，所以由你现场用 reportlab 画一页，再交给 `pdf_ops.py watermark` 去叠。

⚠️ **画水印页必须先注册中文字体**，否则中文会渲染成方块——这正是
`docx_to_pdf.py` 顶部注释警告过的坑。不要自己重新摸索找字体的逻辑，直接复用
`docx_to_pdf.py` 里现成的 `find_cjk_font()`（venv 里 reportlab 已装，两个脚本
同一个 venv）：

```python
import sys
sys.path.insert(0, "${SKILL_DIR}/scripts")
from docx_to_pdf import find_cjk_font

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path = find_cjk_font()
if font_path is None:
    # 找不到中文字体时不要硬画——中文会变方块，比没有水印更糟。
    # 告诉用户本机缺中文字体，建议装 LibreOffice 或换一台有中文字体的机器。
    raise SystemExit("本机找不到中文字体，拒绝生成水印页")

FONT_NAME = "WatermarkCJK"
# .ttc 是字体集合，注册时要指定取第几个；我们要的都是第一个，直接传 0。
# .ttf 是单个字体，不用传这个参数。
if font_path.suffix.lower() == ".ttc":
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(font_path), subfontIndex=0))
else:
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(font_path)))

c = canvas.Canvas("水印.pdf", pagesize=A4)
c.setFont(FONT_NAME, 60)
c.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.4)
c.saveState()
c.translate(A4[0] / 2, A4[1] / 2)
c.rotate(45)
c.drawCentredString(0, 0, "机密")
c.restoreState()
c.save()
```

生成好「水印.pdf」后，正常走上面的 `pdf_ops.py watermark ... --stamp 水印.pdf`
命令去叠加，不要自己写叠加逻辑——叠加涉及页面坐标系合并，`pdf_ops.py` 已经踩过
pypdf 弃用接口的坑（见脚本内注释），现写大概率踩回去。

## 脚本会拒绝干活的几种情况

这些脚本都在评审后加了一批**主动拒绝**的护栏——遇到下面这些情况，脚本会
报错退出、**不产出文件**（不会给你一份空的 / 错的 / 半成品文件）。这些不是
bug，是刻意设计：宁可让你知道哪里出了问题，也不悄悄生成一份看起来正常、
实际有缺陷的文件让用户带着走。遇到了照着「怎么办」处理，**不要瞎试别的
参数或换脚本绕过去**。

| 情况 | 触发脚本 | 脚本怎么反应 | agent 该怎么办 |
| --- | --- | --- | --- |
| PDF 有密码保护 | `pdf_ops.py` 四个子命令（merge/split/delete/watermark）、`pdf_render.py`、`pdf_tables.py`、`doc_text.py`（措辞已统一） | 报错退出，提示文件被密码保护 | 告诉用户"这份 PDF 有密码保护，请先用阅读器去掉密码再试"。**不要试图猜密码或换别的脚本绕过** |
| 水印源 PDF 是 0 页 | `pdf_ops.py watermark` | 报错退出 | 告诉用户水印文件是空的，换一份有内容的水印 PDF |
| `merge` 传空输入列表 | `pdf_ops.py merge` | 报错退出（不会生成空 PDF） | 确认要合并的文件列表，至少给一个 |
| PDF 页码越界 | `pdf_ops.py`（split --ranges / delete） | 报错并告诉你该文件总页数 | 据此改正页码重试，拿不准就问用户 |
| 删页删到一页不剩 | `pdf_ops.py delete` | 拒绝生成空 PDF | 告诉用户删除范围覆盖了全部页，让他确认想删哪几页 |
| `--ranges` 里一个有效区间都没有（如 `","`） | `pdf_ops.py split` | 报错退出，不产出 0 页 PDF | 按 `"1-2,4-5"` 的写法重写区间（多余的逗号会被自动忽略，不用管） |
| LibreOffice 报告成功却没生成 PDF | `docx_to_pdf.py`（LibreOffice 路径） | 报错退出 | 转达原文：多半是这份文件扩展名叫 .docx、内容其实不是 Word 文档，或本机开着 LibreOffice/Word。让用户确认文件能正常打开、关掉 LibreOffice 再试 |
| `.md` 的文字编码既不是 UTF-8 也不是 GBK | `md_to_docx.py` | 报错退出 | 让用户用记事本或 VS Code 另存为 UTF-8 再试 |
| Markdown 表格某行列数多于表头 | `md_to_docx.py` | 报错并指出第几行、多了几列 | 把那一行改成与表头一致的列数再转，别删内容硬凑 |
| Excel 里的公式没有保存计算结果 | `excel_csv.py`（xlsx→csv 方向） | 报错退出，不产出缺了汇总列的 CSV | 按上面「Excel ↔ CSV」那段的原话问用户：①另存一次让公式算出结果，还是②照转但那几格空着（②才加 `--allow-empty-formulas`） |
| CSV 文件一行数据都没有 | `excel_csv.py`（csv→xlsx 方向） | 拒绝生成空 xlsx | 告诉用户这份 CSV 是空的，确认是不是选错了文件 |
| Excel 源文件有多张工作表但没指定 `--sheet` | `excel_csv.py`（xlsx→csv 方向） | 报错并列出所有工作表名 | 问用户要哪一张，或按需求循环导出多次。**不要随便挑第一张** |
| Excel 源文件是 `.xls`（旧的二进制格式） | `excel_csv.py` | 报错退出，提示这是旧格式 | 告诉用户"请先在 Excel 里另存为 .xlsx 再试" |
| Excel 工作表一行数据都没有 | `excel_csv.py`（xlsx→csv 方向） | 拒绝生成 0 字节 CSV | 告诉用户这张表是空的，确认是不是选错了工作表 |
| Word 文档里没有可提取的文字（含只有空段落的情况） | `docx_to_pdf.py`（无 LibreOffice 的兜底路径） | 拒绝生成，不产出空白 PDF | 告诉用户这份 Word 文档提不出文字内容，请确认文件是否正确 |
| 本机找不到任何中文字体 | `docx_to_pdf.py`（无 LibreOffice 的兜底路径） | 拒绝输出（满纸方块的 PDF 比没有更糟） | 告诉用户本机缺中文字体，建议装 LibreOffice 走保排版路径 |
| 一批图片一张也没处理成功 | `img_prep.py` | 报错退出 | 转达原因（多半是 HEIC 无解码器或根本不是图片），让用户确认文件 |
| HEIC 且本机无解码器 | `img_prep.py` | 该张记进 failed，不中断整批 | 告诉用户把这几张导出成 JPG 再试，别自己找别的办法转 |
| 文档是旧的 `.doc` 格式 | `doc_text.py` | 报错退出 | 让用户在 Word 里另存为 `.docx` 或 PDF |
| 文件格式不是 PDF / `.docx` / `.txt` / `.md` | `doc_text.py` | 报错退出，列出支持的格式 | 确认文件类型对不对；不支持就如实告诉用户，不要硬塞进去试 |
| 渲染倍率超过 4 | `pdf_render.py` | 报错退出 | 用默认的 2；某页认不清才对**那一页**调高，别整份提高 |
| 有文字层却一张表都没找到 | `pdf_tables.py` | 报错退出，不留空 JSON | 告诉用户这份 PDF 里没有表格，或问他要抽第几页 |
| 一行数据都没有 / 表头为空 | `rows_to_xlsx.py` | 拒绝生成空表格 | 回头检查自己产出的 JSON 是不是空的 |
| 出现表头里没有的字段 | `rows_to_xlsx.py` | 报错并指出第几行、多了哪列 | **不要偷偷加列**。并进已有列，或先跟用户确认要不要加 |
| 存疑字段超过一半 | `rows_to_xlsx.py` | 拒绝生成 | 原样转达：建议重拍（光线充足、正对、别有折痕）或改用扫描件 |
| 读 `.jsonl` 没带 `--headers` | `rows_to_xlsx.py` | 报错退出 | 补上 `--headers`，别改用 `.json` 绕过去 |
| `--sheet` 用了 `/ \ [ ] : * ?` 或长度超 31 字符，或撞上保留名「待核对」 | `rows_to_xlsx.py` | 报错退出，不写盘 | 换一个合法、不撞保留名的表名（比如把 `/` 换成 `-`，或把「待核对」换成「数据」） |
| `.json` 顶层不是 `{"headers": [...], "rows": [...]}` 这个形状（比如把 `rows` 数组直接当整个文件） | `rows_to_xlsx.py` | 报错退出，指出读到的实际类型 | 补上 `{"headers": ..., "rows": ...}` 这层包装再重试 |

统一强调一条：**这些错误信息都是写给用户看的中文，原样转达比你重新组织
语言有用。**

## 通用纪律

- **产物路径**：默认写到会话工作目录，文件名用中文描述性名字（`季度汇报.pdf`
  好过 `output.pdf`），转完把完整路径告诉用户。
- **不要吞掉脚本的报错**。上面每个脚本的错误信息都写得很具体（缺什么、
  装什么能解决、怎么强行继续），原样转达给用户比你重新组织语言有用。
- **超出这八条的需求**（PDF 转 Word 高保真版式还原、PPT 与 PDF 互转、手写体识别……）
  不属于本技能范围，如实告诉用户做不了，不要用现写脚本硬凑。
