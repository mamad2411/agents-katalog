---
name: ppt-100T-gen
description: 根据内置 PPT 模板生成成品演示文稿。用户描述主题与内容后，本 skill 推荐合适的设计风格模板，复用模板页面并原位替换文字，输出保留原始设计/配色/图形的 .pptx 文件。当用户想"做 PPT""生成幻灯片""按模板做演示文稿""选个风格做汇报/计划书/总结"时使用。
---

# PPT 生成器

基于 14 个内置中文 PPT 模板，按用户选定的风格生成成品演示文稿。
核心策略：**复用模板已有页面 + 原位替换文字**，完整保留模板的设计、配色、图形、动画。

## 资源位置

- 模板目录：`assets/templates/`（14 个 .pptx）
- 模板目录索引：`assets/manifest.json`（风格标签/配色/适用场景/页数）
- 脚本：`scripts/inspect_template.py`、`scripts/build.py`（脚本不可命名为 inspect.py，会遮蔽标准库导致 lxml 导入失败）
- Python：用 `python`（非 `python3`），已装 `python-pptx`。

> 路径以本 SKILL.md 所在目录为基准。运行脚本时用绝对路径或相对本 skill 目录的路径。

## 工作流

### 第 1 步：理解需求并推荐模板
1. 读取 `assets/manifest.json`。
2. 结合用户场景（如"融资计划书""工作总结""公司介绍""团队培训"），从 manifest 的 `scenes`/`style_tags` 匹配出 2–4 个候选。
3. 用 `AskUserQuestion` 让用户选择，每个选项给出：标题 + 风格(`style_tags`) + 配色(`color`) + 适用场景。
   - 若用户已明确点名某模板或某风格，可跳过提问直接用。
   - 当前环境无 LibreOffice，**不提供缩略图**，用文字描述风格即可。

### 第 2 步：收集内容
让用户在对话中自然描述：主题/标题、各部分要点、团队/数据/产品等。不要求固定格式。
内容不足时主动追问关键缺口（如封面标题、各章节标题、正文要点）。

### 第 3 步：读取模板结构
对选定模板运行：
```
python <skill>/scripts/inspect_template.py "<skill>/assets/templates/<文件名>" --out /tmp/struct.json
```
得到每页的 `index / page_type_guess / shapes[{shape_id, kind, font_pt, text, ...}]`。
- `index` 从 0 起，对应 build 的 `keep_slides` / `replacements` 键。
- `font_pt` 大的通常是标题，小的是正文/装饰。
- `text` 是模板占位示例文字（如"点击添加标题""单击此处输入"），需替换成用户内容。

### 第 4 步：映射内容 → 生成 build_spec.json
根据用户内容量决定保留哪些页：
- **必留**：封面、（可选目录）、结尾页。
- 按内容多少挑选合适的内容页/团队页/数据页；内容多则多留，少则精简。
- 为每个要改的 shape 写 `{shape_id, text}`；多行文本用 `\n`。
- 未提及的 shape 保持模板原样。装饰性文字（英文副标题、序号）可保留或替换。

`build_spec.json` 示例：
```json
{
  "keep_slides": [0, 1, 4, 7, 23],
  "replacements": {
    "0": [{"shape_id": 20, "text": "AI 视觉创业融资计划"}, {"shape_id": 24, "text": "智瞳科技"}],
    "4": [{"shape_id": 36, "text": "核心团队"}]
  }
}
```
把它写到临时文件（如 `/tmp/spec.json`）。

### 第 5 步：生成成品
```
python <skill>/scripts/build.py --template "<skill>/assets/templates/<文件名>" --spec /tmp/spec.json --out "<输出目录>/<主题>.pptx"
```
默认输出到用户当前工作目录，文件名用主题命名。把最终路径告诉用户。

### 第 6 步：交付与微调
告知输出路径与页数。提示用户可继续调整：换页、改文案、增删页面 → 修改 spec 重新跑 build。

## 自动排版（autofit）
build.py 在替换文本后会**自动适配排版**，无需手工逐条精简文案：
- 所有文本框强制开启**自动换行**（word_wrap），长文本在框内换行而非横向溢出。
- 按「文本量 vs 文本框尺寸」估算所需行数，放不下时**整体等比缩小字号**（保留同框内标题/正文的相对大小），并冻结「随文字自适应」的框以免撑大挤压版面；单行短文本（标题、数字、标签）不缩。
- 末了再设为 PowerPoint 原生「溢出时缩小文字」作为兜底，用户后续编辑也不会溢出。

spec 可选开关（默认即最佳，一般无需设置）：
```json
{ "autofit": true, "min_font_pt": 9, "keep_slides": [...], "replacements": {...} }
```
- `autofit`：是否启用自动适配（默认 true）。
- `min_font_pt`：自动缩字的下限（默认 9pt），到下限仍放不下则交给 PowerPoint 兜底。

> 仍建议正文每段控制在 ~30 字内：autofit 能防溢出，但过长会把字缩得偏小，精炼文案观感更好。

## 注意事项
- `keep_slides` 仅决定保留哪些原始页；输出顺序 = 原始顺序中被保留的页（本版本不重排页面顺序）。
- `shape_id` 不存在或无文本框时 build.py 会告警跳过，不崩溃。
- 文本替换保留首个 run 的字体/字号/颜色，不破坏模板样式；多段文本框会逐段替换并清除多余旧段落（避免「（添加二级标题）」等占位残留）。
- 图表页（charts）目前保留模板示例数据，不自动改图表数值。
- Windows 下 Python 路径用 `C:/...` 或 `G:/...` 正斜杠形式，避免 `/c/...` 这类 git-bash 路径（python 不识别）。
- 生成前确认输出文件未被 PowerPoint/WPS 打开，否则保存会因占用失败（PermissionError）。
