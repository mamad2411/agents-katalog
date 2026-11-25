---
name: thesis-docx
description: 将浙江大学 MEM 学位论文 LaTeX 项目（zjuthesis/body 或 chapters/，可含 ref.bib/PDF）或普通 md/docx 草稿生成或审计为符合官方模板的 DOCX，优先使用 scripts/mem_docx.py（latex/draft 子命令）。仅在用户明确要运行/维护 thesis-docx 管线、把该类论文/草稿转 Word、或诊断该管线输出时使用；不要用于普通 Word 排版、通用三线表、非 ZJU MEM 论文、参考文献咨询。
---

# thesis-docx

浙大 MEM 学位论文 LaTeX 或普通草稿 -> Word(DOCX) 一键生成与审计。默认目标是可编辑
Word 导师批注稿；送审正本仍以 LaTeX 直接导出的 PDF 为准。草稿路径只做机械排版，
不改写内容。

## 硬规则

- 只改生成器、模板资产、LaTeX 源或本地 config；不要手改最终 DOCX。
- 论文正文只在 `thesis-work` worktree 改，先 `pwd`/`git status` 确认位置。
- 姓名、学号、导师等 PII 只放本地 `~/.config/wenqu-mem/*.json`，不进仓库。
- 致谢、作者简历不代写编造；可保留占位并提示人工补。
- `wenqu-mem` 是公开仓。本地 commit 可以做，未经用户同意不要 push；提交信息不要带 AI 署名尾注。
- Word/WPS 视觉验收以打开后全选 F9 更新域为准。LibreOffice 只作粗冒烟，不能作为最终页数依据。

## 先读

做非平凡修改前，先读最相关的 reference，不要把所有历史塞进提示词：

- `references/conversion-rules.md`：转换规则、字段、表格、引用、审计依据。
- `references/official-format-requirements.md`：官方 2024 模板抽取出的格式要求。
- `references/visual-qa-checklist.md`：Word/WPS 更新域后的视觉验收清单。
- `references/draft-normalizer.md`：普通 md/docx 草稿路径的结构识别和 report 规则。

需要跨会话背景时用共享记忆：

```bash
kb search "thesis-docx"
```

## 适用边界

- 应触发：用户要从 ZJU MEM LaTeX 工程生成/审计 DOCX，或把 md/docx 草稿机械排版成 MEM 规范 DOCX，或维护本目录下的生成管线。
- 不应触发：普通 Word 排版、一次性 DOCX/PDF 编辑、非 ZJU MEM 论文、参考文献咨询。
- 输入：`zjuthesis` 根目录，或普通 `draft.md` / `draft.docx`；本地 `thesis.json`；可选模板/CSL/reference docx；目标输出路径。
- 输出：生成的 DOCX、结构/样式审计结果、可选 Word 渲染 QA 报告。
- 成功标准：一键命令可重复生成；`audit_style_contract` 和 `mem_docx.py validate --json` 通过；需要视觉判断时 Word 全选 F9 后无未更新字段占位。

## 一键生成

先在 `wenqu-mem` 仓库根目录准备本地 Python 环境；后续命令优先用这个解释器：

```bash
cd /path/to/wenqu-mem
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
```

还需要系统命令：`pandoc`、LaTeX 工具链、Microsoft Word（仅 Word 渲染 QA 需要）。
macOS 常用：

```bash
brew install pandoc
```

**推荐入口 = `mem_docx.py`（或 pip 安装后的全局 `mem-docx`）——scripts/ 下唯一顶层可执行
入口，不再有 `merge_docx.py`/`format_draft_to_mem.py` 等平级薄壳脚本**。透传子命令
`latex/draft/validate/render/gate/importers/redline/comments/frontmatter/body` + 原生子命令
`check/test/doctor/clean/visual`：

```bash
export PATH="/opt/homebrew/bin:/Library/TeX/texbin:$PATH"
PY=/path/to/wenqu-mem/.venv/bin/python
SK=/path/to/wenqu-mem/skills/thesis-docx

"$PY" "$SK/scripts/mem_docx.py" latex --root /path/to/zjuthesis --out ~/Desktop/论文_混合.docx \
  --config ~/.config/wenqu-mem/thesis.json --csl "$SK/assets/gb7714-2015-numeric.csl"
"$PY" "$SK/scripts/mem_docx.py" check out.docx --chapters-dir ... --config ... --json   # 一键全体检(schema必跑,缺参的gate明示skipped)
"$PY" "$SK/scripts/mem_docx.py" test      # 跑全部 test_*.py 统一汇总
"$PY" "$SK/scripts/mem_docx.py" doctor    # 依赖体检(硬依赖缺=exit 1;node/Word/redlines/docxtpl为软依赖)
"$PY" "$SK/scripts/mem_docx.py" clean     # 运行产物退休:各运行目录保最新3个+清__pycache__/egg-info(--dry-run 先看)
"$PY" "$SK/scripts/mem_docx.py" importers draft.docx --json  # 对比 pandoc/mammoth/markitdown importer
```

可选 pip 安装（editable，之后任意目录直接敲 `mem-docx`；红线强引擎为 extras）：

```bash
"$PY" -m pip install -e "$SK/scripts"                # 基础
"$PY" -m pip install -e "$SK/scripts[redlines]"      # + Python-Redlines(WmlComparer)强引擎
```

盲审隐名前置页（作者/导师置空、保留下划线；显名默认；作者简历页 `cv` 不联动本开关，
该页本为占位，仍需人工补真实内容）：

```bash
"$PY" "$SK/scripts/mem_docx.py" latex --root /path/to/zjuthesis --out ~/Desktop/论文_盲审.docx \
  --config ~/.config/wenqu-mem/thesis.json --blind
```

普通草稿（无 LaTeX 工程）走 `draft` 子命令：

```bash
"$PY" "$SK/scripts/mem_docx.py" draft \
  --input /path/to/draft.md \
  --config ~/.config/wenqu-mem/thesis.json \
  --out ~/Desktop/论文_草稿规范化.docx
```

md 草稿可选自动编号（pandoc-crossref，按章产 `图1.1　题注` 与解析 `[@fig:x]` 引用；
二进制缺失自动降级 none 并写入报告；模板类元数据必须走 `--metadata-file`，`-M` 会静默不展开）：

```bash
"$PY" "$SK/scripts/mem_docx.py" draft --input draft.md --number-mode crossref \
  --config ~/.config/wenqu-mem/thesis.json --out out.docx
```

`draft` 同样支持 `--blind`（隐去封面/题名页作者与导师姓名）。

PDF 抽取等**已预结构化**的 md（自带显式 `#` 标题）须加 `--trust-headings`——跳过正则
自动升格（拍平表格的数字开头碎行会被误判成章标题，实测被内容门禁逐字揪出）。
PDF 本身不是直接输入：先 `pdftotext -layout` 抽取+清洗出带 `#` 标题的 md（表格需
pdfplumber/MinerU 恢复或人工重建），再走本子命令。`.docx` 草稿同理：

```bash
"$PY" "$SK/scripts/mem_docx.py" draft \
  --input /path/to/draft.docx \
  --config ~/.config/wenqu-mem/thesis.json \
  --out ~/Desktop/论文_草稿规范化.docx
```

`.docx` 草稿默认仍用 pandoc 归一化。需要排查 pandoc 对散乱 DOCX 的识别差异时，可显式试验：

```bash
"$PY" "$SK/scripts/mem_docx.py" draft \
  --input /path/to/draft.docx \
  --config ~/.config/wenqu-mem/thesis.json \
  --docx-importer mammoth \
  --out ~/Desktop/论文_草稿规范化_mammoth.docx
```

`markitdown` importer 仅作为可选实验路径，未列为必装依赖；使用前需自行安装。无论使用哪个 importer，
最终仍必须通过 `gate` 子命令的内容指纹和样式门禁。

需要横向比较 importer 时先跑 benchmark，而不是凭视觉猜：

```bash
"$PY" "$SK/scripts/mem_docx.py" importers /path/to/draft.docx \
  --workdir ~/Documents/Codex/word-work/importer-bench \
  --json
```

benchmark 会对同一 DOCX 依次跑已注册 importer，报告标题识别、摘要/关键词、参考文献、预览、
`docx2python` 诊断和失败原因；失败 importer 不拖垮整份报告。

`$PY` 必须能 import `docx`、`lxml`、`docxcompose`、`fitz`、`docx2python`、`mammoth`。若 import 失败，
回到仓库根目录重跑上面的 `.venv` 安装命令，或跑 `mem_docx.py doctor` 定位缺失项。`docxtpl/Jinja2`
是软依赖，只在模板含 Jinja 标签时启用；默认官方模板无标签，不会接管封面布局、页眉页脚或字段。

常用项目路径：

```bash
/path/to/zjuthesis
```

只调前置页（跳过重建正文）：

```bash
"$PY" "$SK/scripts/mem_docx.py" frontmatter \
  --root /path/to/zjuthesis \
  --out front.docx \
  --config ~/.config/wenqu-mem/thesis.json \
  [--blind]
```

前置页默认使用 `assets/zju-mem-frontmatter-master.docx` 这个脱敏预清理母版，只替换封面字段、
摘要、关键词和 Word 字段开关。旧 `build_docx.py` 生成器已删除；如需回看历史，用 git 找回。

只调 pandoc 正文（跳过前置页）：

```bash
"$PY" "$SK/scripts/mem_docx.py" body \
  --root /path/to/zjuthesis \
  --skip-front-matter \
  --out body.docx \
  --reference-doc "$SK/assets/zju-reference.docx" \
  --csl "$SK/assets/gb7714-2015-numeric.csl"
```

`frontmatter`/`body` 两个子命令分别透传给 `thesis_docx.pipeline.frontmatter`/
`thesis_docx.pipeline.body`；两者也都保留独立可执行能力，等价地可用
`python3 -m thesis_docx.pipeline.frontmatter` / `python3 -m thesis_docx.pipeline.body` 调试单个工序。

## 管线结构

`mem_docx.py latex`（`thesis_docx.pipeline.merge`）串联两条路线：

1. 以 `python3 -m thesis_docx.pipeline.frontmatter` 子进程从 `assets/zju-mem-frontmatter-master.docx` 渲染前置页：封面、声明、授权、题名页、摘要、目录、罗马页码；如果母版缺失或渲染失败，`latex` 子命令直接失败，避免悄悄回到旧生成器。
2. 以 `python3 -m thesis_docx.pipeline.body --skip-front-matter` 子进程生成正文：第 1 章到参考文献/附录/致谢/简历，保留 OMML 公式、gb7714 参考文献和 `.aux` 真编号。
3. docxcompose 合并后执行分节、字段、样式、字体、参考文献、后置分页、附录副题、三线表和审计收口。

`mem_docx.py draft`（`thesis_docx.pipeline.draft_format`）复用后半段：

1. `draft.md` 直接进入 markdown 归一化；`draft.docx` 先用 pandoc 转 markdown 并抽媒体到固定工作目录。
2. 从草稿抽取中文摘要/英文摘要/关键词/Keywords，交给 `thesis_docx.pipeline.frontmatter.render_frontmatter` 渲染前置页；抽不到时用占位并提示人工补。
3. 正文 markdown 走 `thesis_docx.pipeline.body.markdown_to_docx(..., number_sections=False)`，不让 pandoc 改可见标题文本。
4. 继续复用 `thesis_docx.pipeline.merge.compose` + `thesis_docx` 包内后处理 + `audit_style_contract` + `thesis_docx.qa.content_gate`。
5. 每次运行在固定工作目录写出 `normalized.md`、`body.md`、`body-source.txt`、
   `abstracts.json`、`draft_normalize_report.json` 和 `body_quality_report.json`。

`scripts/` 下只有两个顶层可执行文件：`mem_docx.py`（统一 CLI 分发器）与各 `test_*.py`
（测试文件）；其余全部实现在 `scripts/thesis_docx/` 包内，直接使用包路径：

- `domain/abstracts.py`：从 LaTeX/PDF 抽取中英文摘要和关键词，供前置页路径复用。
- `domain/draft.py`：普通 md/docx 草稿的结构识别、摘要抽取、工作目录和 normalize report。
- `support/config.py`：封面、章节和字体的默认配置，供生成与验证共用。
- `support/template.py`：可选 docxtpl/Jinja 安全标量预渲染，只允许封面标量变量。
- `ooxml/contract.py`：从官方模板抽取样式合约。
- `ooxml/fields.py`：Word complex field sibling-run 生成。
- `ooxml/field_dsl.py`：bookmark/REF/TC/PAGE/STYLEREF RawOpenXML 小 DSL PoC；先供测试和后续 Lua/filter 前移使用，不替换稳定主线。
- `zju_docx_semantics.lua`：Pandoc 阶段的 CJK softbreak 清理、题注样式标记、TC 短目录项预插入。
- `ooxml/styles.py`：标题、正文族、TOC、题注样式修复。
- `ooxml/fonts.py`：按语境处理中文正文/摘要、英文摘要、题注、参考文献字体槽。
- `ooxml/postprocess.py`：参考文献（挤段自动拆分——PDF 抽取稿条目无空行连成一整段时按
  `[n]` 边界拆；citeproc 每条独立成段永不触发）、后置分页、附录英文副题、
  **正文引用→上标+点击跳转**（`link_citations_to_bibliography`：文献条目打书签
  `bib_ref_n`，正文 `[n]/[n,m]/[n-m]` 包内部超链接锚到条目并加 vertAlign 上标，
  与 LaTeX 正本 biblatex 上标口径一致；无对应条目的记号不动；须在
  fix_script_mixed_runs 之后跑，两条管线均自动生效）。
- `ooxml/postprocess_links.py`：正文文献/图表交叉引用超链接与书签实现，`postprocess.py` 保留兼容入口。
- `ooxml/tables.py`：题注数据表三线表、列宽、noWrap；表格检查和报告拆到 `table_checks.py` / `table_reports.py`。
- `ooxml/hygiene.py`：文档卫生——`scrub_doc_metadata` 清 docProps 元数据
  （creator/lastModifiedBy/Company 置空、revision 归 1；**显名盲审都清**——实锤过
  lastModifiedBy 带真名、Company 带公司名 = 文件属性泄漏通道）；
  `fix_caption_keep_with_next` 题注防拆页（表题样式 keepNext + 图段落 keepNext 粘住下方图题）。
- `ooxml/postprocess.py` 另含 `link_figure_table_refs`：图/表交叉引用点击跳转——题注打书签
  `fig_ref_2_1`/`tab_ref_C_1`，正文"图X.Y/表C.1"包内部超链接（不上标）；**跨 run 拼接匹配**
  （语境字体拆分会把"图"与数字隔开，单 run 匹配为 0 命中——实测教训）；目标不存在不动、幂等。
- `qa/audit.py`：最终 OOXML fail-closed 样式门禁；具体断言拆到 `audit_assertions.py`。
- `qa/content_gate.py`：全文 SHA + 段落块指纹 + 差异分类的内容零改写门禁。
- `qa/importer_benchmark.py`：DOCX importer registry benchmark。
- `qa/content_gate.py`：草稿路径内容一致性门禁。
- `qa/validate.py`：LaTeX 源结构、页码、字段、表格、引用和模板残留总验证。
- `qa/render_word.py`：Microsoft Word 渲染截图/字段刷新 QA，LibreOffice 仅为 fallback。
- `qa/redline.py`：两版 DOCX 对照生成带 Word 修订标记的红线稿（builtin/redlines 双引擎）。
- `qa/comments_export.py`：DOCX 批注/修订回流为 LaTeX TODO 表；含 `extract_comments` / `map_to_latex` / `render_todo_md` 三个核心函数 + CLI `main`。

## 关键不变量

### 资产分层

- `assets/` 放可公开复用并可进 git 的脱敏资产：`gb7714-2015-numeric.csl`、`zju-reference.docx`、官方规范模板、前置页母版。DOCX 资产提交前必须 scrub 元数据，并扫描正文 XML 中不得含姓名、学号、导师、绝对路径或 AI 署名尾注。
- `local-assets/` 放本机覆盖资产，已被 `.gitignore` 忽略，不上传公开仓：真实草稿样本、视觉基准、临时渲染件，或需要临时覆盖公开脱敏母版的私有版本。
- 运行时统一由 `thesis_docx.support.assets` 定位资产，查找顺序固定为 `local-assets/` 优先、`assets/` 兜底；缺少硬依赖时 `mem_docx.py doctor` 会报出具体文件和当前来源。
- 本机如需覆盖公开脱敏母版：

```bash
mkdir -p "$SK/local-assets"
cp "/path/to/浙江大学工程管理硕士学位论文规范要求-2024.docx" "$SK/local-assets/"
cp "/path/to/zju-mem-frontmatter-master.docx" "$SK/local-assets/"
```

- 官方模板资产默认在 `assets/浙江大学工程管理硕士学位论文规范要求-2024.docx`。
- 前置页运行时母版默认在 `assets/zju-mem-frontmatter-master.docx`；它是已经清理好说明框、封面布局、题名页、目录字段和前置页分节的稳定 DOCX，运行时只做变量替换。
- 图/表目录使用前置页 `TOC \h \z \f F/T` 加正文隐藏 `TC` 短中文条目，避免双语长题注进目录。
- 复杂字段必须是 sibling runs，不要退回单 run 字段。
- 前置页用静态页眉；正文按一级标题自动分节并写入静态章名页眉，避免 WPS 在章首页把 STYLEREF 解析成“文档中未找到关联章节样式”。
- 中文正文/摘要里出现的 `A公司`、`PDCA`、`Checklist` 等英文缩写仍按中文语境用仿宋；英文摘要/英文题名用 Times New Roman；参考文献按中英文脚本拆分。
- 三线表只审计有正式题注的数据表；公式、注释、空布局表可跳过。
- 合并后正文 10pt 或字体框空白通常是 `basedOn` 悬空（不限 `Normal`，也见 `DefaultParagraphFont/TableNormal`），修复在 `thesis_docx.ooxml.styles.fix_style_inheritance`（按样式名重指，找不到真身则删除悬空 basedOn）。
- **OOXML 顺序规范化**：分散的 OOXML 手术会把 spacing/sz/tblW/headerReference 等 append 到 schema 非法位置（Word/WPS 容忍但不合规）；`merge.normalize_ooxml_order` 在 compose 收尾统一按 CT_* 顺序重排（含 settings/m:mathPr、VML shape id 去重），`qa/schema_check.py`（node OpenXmlValidator + Python 结构检查双层）在 validate 链 fail-closed 防复发。新增 OOXML 写入代码优先用 `ooxml/package.py` 的 sort_* 工具收口。
- **中文语境 run 显式 `w:hint="eastAsia"`**：中西共用字符（中文引号/括号）Word 无 hint 按 ascii 字体渲染、WPS 倾向 eastAsia——同一文档两端字形不一致；语境字体与表格文字统一补 hint。
- 官方模板字体考古：封面顶栏名义 `仿宋_GB2312`（模板 fontTable 自带 altName=仿宋，作者机器已无此字体），本管线统一写 `仿宋` 更稳；声明/授权标题 `方正小标宋简体`（altName=微软雅黑）按模板保留——WPS 多自带方正字体、Word 无则回退微软雅黑，**两端渲染字形不同属官方模板固有，非管线 bug**。
- md 草稿的自动编号走 pandoc-crossref（`--number-mode crossref`，文本编号、与 LaTeX 路径 .aux 口径一致）；docx 乱排草稿维持保留原编号文本，不猜测散文里的交叉引用。
- 散乱 DOCX 的标题识别是保守规则：确定的章/节标题才提升；中文序号、加粗短行等疑似标题只写入 `draft_normalize_report.json`，需要人工确认。
- DOCX 草稿诊断会用 `docx2python` 补充页眉、页脚、脚注、尾注、图片和文本规模指标；这只增强报告，不替代默认 pandoc 正文归一化。
- 内容门禁报告包含 `sha256(normalized_visible_text)` 指纹；source/target 指纹不一致时视为内容改写风险。

## 验证

语义/字段 smoke test：

```bash
"$PY" "$SK/scripts/test_docx_semantics.py"
```

草稿 normalizer 测试：

```bash
"$PY" "$SK/scripts/test_draft_normalizer.py"
```

结构门禁（含 OOXML schema 双层校验：node OpenXmlValidator 全量 XSD + Python 结构
检查——rels/rid/fldChar/basedOn 悬空 + paraId 唯一性 + 孤儿脚注 + 书签配对为 error，
标题跳级/表格列数不一致为 warning 不掀 ok）：

```bash
"$PY" "$SK/scripts/mem_docx.py" validate ~/Desktop/论文_混合.docx \
  --chapters-dir /path/to/zjuthesis/body/graduate/master \
  --config ~/.config/wenqu-mem/thesis.json \
  --json
```

红线稿（两版 DOCX → 带 Word 修订标记的对照稿）——双引擎：

```bash
"$PY" "$SK/scripts/mem_docx.py" redline 旧版.docx 新版.docx --out 红线稿.docx                 # builtin(默认)
"$PY" "$SK/scripts/mem_docx.py" redline 旧版.docx 新版.docx --out 红线稿.docx --engine redlines  # 强引擎
```

- `builtin`：移植自 SecurityRonin/docx-mcp compare.py（MIT，出处已注明），零依赖，
  段落 LCS+词级 diff，630 段 0.008s；中文整句级 del+ins；表格不参与 diff。
- `redlines`：Python-Redlines/Docxodus（WmlComparer .NET8 AOT，wheel 自包含免装 .NET，
  macOS arm64 实测可用），更细粒度+表格 diff，冷启动约 2-3s。装法
  `pip install 'mem-docx[redlines]'`（extras 已锁 `python-redlines[docxodus]`——裸装
  python-redlines 缺比较引擎不可用）。代码里 detect_moves 与 simplify_move_markup
  **锁死成对**（拆开会产生 Word 报"内容不可读"的 moveFrom/moveTo 标记）。

批注回流（导师批注/修订 → 映射回 LaTeX 源的 TODO 表；锚点文本 NFKC 归一+去 LaTeX
命令噪声，先精确匹配后 difflib 滑窗模糊匹配 ratio≥0.6，置信度 exact/fuzzy/none）：

```bash
"$PY" "$SK/scripts/mem_docx.py" comments 导师批注版.docx \
  --tex-dir /path/to/zjuthesis/body/graduate/master --out todo.md
```

草稿路径内容门禁：

```bash
"$PY" "$SK/scripts/mem_docx.py" gate \
  --source /path/to/body-source.txt \
  --source-format txt \
  --output ~/Desktop/论文_草稿规范化.docx \
  --output-start-heading "第1章 绪论"
```

Word 渲染 QA：

```bash
"$PY" "$SK/scripts/mem_docx.py" render ~/Desktop/论文_混合.docx \
  --output-dir ~/Documents/Codex/word-work/thesis-docx-renders/current \
  --pages 1,8,11,12,27,89,102
```

`render` 默认把 QA 文件放在固定 `~/Documents/Codex/word-work/...`，
避免 macOS Word 反复弹 `/private/tmp` 沙盒授权。若报告里有
`unupdated_field_markers`，说明目录/图目录/表目录没有真正刷新，不能用那次截图验收。

Windows 下 `render` 子命令（`thesis_docx.qa.render_word`）自动转 `qa/render_com.py`
（pywin32 COM：`Fields.Update`+TOC 逐个 Update+`ExportAsFixedFormat`，`--engine word|wps`；
页图/域检测用 fitz 跨平台）。**该分支按 word-mcp-live/thesis-typeset 的已验证
COM 模式编写，尚未在 Windows 真机实测**，首次使用先跑单文件核对报告。

## Agent 工作流（确定性轨道 + 决策点）

本 skill 的设计是「py 走轨道，agent 站决策点」：转换/门禁/渲染由脚本确定性完成，
agent 的判断只落在下列决策点，且**永远通过可重跑的输入回写**（改 LaTeX/md 源、改
config、改生成器），绝不手改最终 DOCX——保证每份产物可复现、门禁可复跑。

| 决策点 | 读什么 | 动什么 | 重跑什么 |
|---|---|---|---|
| 可疑标题裁决 | `draft_normalize_report.json` 的 warnings | 改草稿 md（升/不升标题） | `mem_docx.py draft` |
| 门禁失败归因 | `check --json` 各 section 的 errors | 改源/改 config/改生成器（判定是内容问题还是管线 bug） | `check` |
| 未定位批注 | `todo.md` 中 confidence=none 条目 | 通读论文语境手动补 LaTeX 定位 | — |
| 视觉复核 | `render` 产出的页图 PNG | 对照 `references/visual-qa-checklist.md` 逐页看图（多模态） | 修后重渲 |
| 红线稿审读 | `redline` 产物 | 判断哪些修订需要回应，配合 thesis-review-response 流程 | — |

## 触发自测

- 应触发：`把 thesis-work 里的浙大 MEM 论文重新生成 DOCX 并审计。`
- 不应触发：`帮我把这个普通 Word 合同排版一下。`
- 边界：`只有 PDF，没有 LaTeX 源，能不能转成规范 DOCX？` -> 不直接使用本 skill，先说明输入不足。
- 边界：`把乱排 docx 草稿排成 MEM 规范，但不要改内容。` -> 使用本 skill 的 `mem_docx.py draft` 路径。
- 回归：`图目录更新后显示整段中英双语题注。` -> 使用本 skill 检查 TC 短目录项和 Word F9 流程。

## 交付习惯

- 每轮非平凡修改后重跑能覆盖改动的最小门禁；影响最终 DOCX 时重跑一键生成。
- 项目提供 `scripts/thesis_quality.py` 时，DOCX 生成与自身校验完成后调用
  `thesis-quality-gate` 的 `doctor`；正式交付再运行对应阶段的 `gate`，让结果
  绑定当前 DOCX/PDF 哈希。
- 结束时写共享 checkpoint：

```bash
kb checkpoint --title "<title>" --directory "projects" --tags "checkpoint,codex,thesis-docx" --content "<summary>"
```
