---
name: svg-flowchart
description: Generates clean, publication-ready flowcharts as SVG code. Use when the user asks to draw a flowchart/流程图, requests SVG flowchart output, or needs a论文风格流程图 from steps/decisions/modules. Supports converting from structured text, natural language, or JSON spec to SVG; optional SVG-to-PDF export for LaTeX. Produces academic, low-saturation styling and can save SVG/PDF files into the repo.
---

# SVG 流程图绘制（学术风格）

## 适用场景（触发）

- 用户提到“流程图 / flowchart / 画流程图 / 用 SVG / 生成 svg 代码”
- 需要论文/报告中可直接插入的流程图（风格稳重、线条克制、可打印）

## 目标输出

- 默认输出 **SVG 代码**，并 **保存为 `.svg` 文件**（项目内可引用）
- SVG 应满足：`viewBox` 完整、可缩放、不依赖外部字体资源、中文可读、对齐规整

## 转化为 SVG 的多种方式

本技能支持从多种输入**转化为**标准 SVG 文件，便于论文插图与版本管理。

| 输入形式 | 转化方式 | 输出 |
|----------|----------|------|
| **结构化文本**（节点清单 + 连线清单） | Agent 按规范抽取 DAG，计算布局，写出 SVG 代码并保存 | `{{THESIS_DIR}}/figures/flows/<名称>.svg`（默认 `论文章节/figures/flows/`） |
| **自然语言描述**（“先 A 再 B，若 C 则 D…”） | Agent 抽取节点与连线，生成 SVG 并保存 | 同上 |
| **JSON spec 文件** | 使用 `render_flowchart.py --spec <spec.json> --out <out.svg>` | 指定路径的 `.svg` |
| **已有 SVG** | 使用 `validate_flowchart_style.py` 做样式规范检查与修正建议 | 不改变格式，仅校验 |

**推荐**：复杂/多列流程图优先用 JSON spec + `render_flowchart.py`，可保证端口偏移、分组框与中文实体编码一致。

## 导出为 PDF（供 LaTeX 使用）

XeLaTeX 的 `\includegraphics` 对 SVG 的 BoundingBox 支持有限，建议将流程图**导出为 PDF** 后再插入论文，可避免编译报错。

**方式一：使用本技能提供的脚本（优先尝试 cairosvg，否则提示用 Inkscape）**

脚本路径以仓库内 **`{{SKILLS_ROOT}}/svg-flowchart/scripts/`** 为准（本仓库默认 `.opencode/skills/svg-flowchart/scripts/`）。目录占位符见仓库根目录 [README.md](../../../README.md)。

```bash
python .opencode/skills/svg-flowchart/scripts/svg2pdf.py <input.svg> [output.pdf]
# 未指定 output 时，生成与 input 同名的 .pdf
python .opencode/skills/svg-flowchart/scripts/svg2pdf.py 论文章节/figures/flows/示例流程.svg
```

**方式二：Inkscape 命令行**（若已安装并加入 PATH）

```bash
inkscape --export-type=pdf "论文章节/figures/flows/流程图.svg" -o "论文章节/figures/flows/流程图.pdf"
```

**方式三**：在 Inkscape / 浏览器中打开 SVG，另存为 PDF，保存到 `figures/flows/` 下与 SVG 同名。

导出 PDF 后，在 LaTeX 中使用 `\includegraphics[width=...]{figures/flows/流程图.pdf}` 即可。

## 推荐工作流（更美观、更稳定）

当流程图包含**分组框/多列结构/多条汇入箭头**时，优先采用脚本自动排版（可避免“箭头重叠、对齐不齐、中文乱码”等问题）：

```bash
python .opencode/skills/svg-flowchart/scripts/render_flowchart.py --spec <spec.json> --out <out.svg>
```

脚本会自动：

- 按分组列布局（适合“三层数据流/三模块框图”）
- 端口偏移（同一节点多条入边不叠在同一点）
- 全量将中文转换为 HTML 数字实体，减少 Windows/查看器的编码坑

**样式自检（可选）**：生成或修改 SVG 后，可用样式检测脚本检查是否符合技能规范（配色、线条圆角、viewBox、禁止渐变/阴影等）：

```bash
python .opencode/skills/svg-flowchart/scripts/validate_flowchart_style.py <file.svg> [<file2.svg> ...]
# 严格模式（禁止 filter/阴影）：
python .opencode/skills/svg-flowchart/scripts/validate_flowchart_style.py --strict <file.svg>
```

检测到不规范项会列出并返回非零退出码；全部通过则输出 `OK`。

## 先收集输入（最少 6 项）

让用户用下面任一方式给信息；缺失项自行补全为合理默认，并在输出前用 1 句话声明默认假设。

1. **标题**（可空）
2. **节点清单**：每个节点 `id`、`label`、`type`
3. **连线清单**：`from -> to`，判断分支写 `yes/no`（或“是/否”）
4. **方向**：`vertical`（默认）或 `horizontal`
5. **字号**：默认 14（正文）/ 12（辅助）
6. **保存路径**：默认 `{{THESIS_DIR}}/figures/flows/<slug>.svg`（见仓库根 [README.md](../../../README.md)）

可接受两种输入格式：

**A. 结构化（优先）**

```text
标题：……
方向：vertical
节点：
- start: 开始 (start)
- a: 数据准备 (process)
- b: 生成速度场 (process)
- c: 是否可达？ (decision)
- d: 输出路径与时间代价矩阵 (process)
- end: 结束 (end)
连线：
- start -> a
- a -> b
- b -> c
- c(是) -> d
- c(否) -> end
```

**B. 自然语言**

把步骤、判断点、输入输出按顺序描述即可；你负责抽取成节点与连线。

## 绘制规范（默认学术风格）

### 画布与布局

- **默认垂直布局**：节点居中对齐，统一间距（推荐：`gapY=40~48`，避免连线与节点贴太近）
- 尺寸策略：先按节点数估算高度，再设置 `viewBox="0 0 W H"`；同时 `width="100%"`，确保可缩放；四边留白 `pad≥28`
- 单列流程优先；分支仅在 `decision` 节点处做左右分叉（保持对称）

#### 多列分组版式（建议用于论文框图）

- **列间距**：`col_gap=70~90`，确保组框之间留白，连线不挤
- **组框**：包住全部所属节点后四周再加 20~28px 内边距；标题放在组框内左上角（比“悬在框外”更规整）
- **连线策略**：先画连线、再画节点，避免线压字；优先正交折线（elbow），多条入/出边做端口偏移

### 图形语义（type → 形状）

- `start`/`end`：圆角胶囊（pill）
- `process`：圆角矩形（rounded rect）
- `decision`：菱形（diamond）
- `data`（可选）：平行四边形（parallelogram）

### 线条与箭头

- 统一线宽 `stroke-width=1.5~1.6`；颜色可用灰色系（`#64748B`、`#94A3B8`）或**柔和的有色线**（如淡蓝 `#7DD3FC`、淡绿 `#6EE7B7`、淡紫 `#C4B5FD`），与节点色系协调即可
- 箭头使用 `marker-end`，填充与线条同色，尺寸克制（markerWidth/Height 6~7）
- **圆角线条**：`stroke-linecap="round"`、`stroke-linejoin="round"`，避免生硬直角
- 分支线优先正交折线（elbow），必要时做端口偏移避免多线重合

### 配色与字体（清新学术，可淡彩）

- **不必拘泥灰色**：节点与分组可采用**清新淡雅的淡彩色**，低饱和、明度偏高即可，整体保持学术感
- **推荐淡彩色板**（填充用，描边取同色系深 1–2 档）：
  - 淡蓝：`#E0F2FE` / `#BAE6FD`，描边 `#0EA5E9` / `#0284C7`
  - 淡绿：`#DCFCE7` / `#BBF7D0`，描边 `#16A34A` / `#15803D`
  - 淡紫：`#EDE9FE` / `#DDD6FE`，描边 `#7C3AED` / `#6D28D9`
  - 淡杏/橙：`#FFEDD5` / `#FED7AA`，描边 `#EA580C` / `#C2410C`
  - 淡青：`#CFFAFE` / `#A5F3FC`，描边 `#0891B2` / `#0E7490`
  - 灰色系（仍可用）：节点 `#F1F5F9`，描边 `#475569`；分组 `#F8FAFC`，描边 `#E2E8F0`
- **核心/起点节点**：可用同色系稍深（如 `#E0E7FF`+`#4F46E5`）或淡彩中选一作为强调
- **主文字**：`#1E293B` 或深灰；辅助/边标注：`#64748B` 或与连线同色系
- **字体**：`font-family="Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif"`
- 避免高饱和、荧光色；同一图内色相不宜过多（2–3 种主色即可）

### 美观要点（必守）

- **无重叠**：节点与节点、文字与连线、边标注与箭头之间留足间距；先算坐标再画线
- **端口偏移**：同一节点多条入边或出边时，在节点边缘错开落点（±10~24px），避免多线叠在一点
- **对齐规整**：同列节点水平居中、垂直等距；分组框包住全部所属节点并留 20~28px 内边距
- **中文编码**：手写 SVG 时中文优先用 HTML 数字实体（如 `&#x8F93;&#x5165;`），或统一 UTF-8 保存，减少查看器乱码
- **viewBox 完整**：宽高覆盖全部图形与边标注，四边留 pad≥24~28

## 生成 SVG 的步骤（务必按序）

1. **从输入抽取 DAG**：节点、连线、分支标签（是/否）
2. **确定布局参数**：节点宽高（默认 `w=320, h=56`），边距（`pad=28`），间距
3. **计算坐标**：
   - 单列：`x = (W-w)/2`，`y = pad + i*(h+gapY)`
   - 分支：在菱形后拆成左右两列（`xLeft/xRight`），并在汇合处回到主列
4. **输出 SVG**：`<defs>`（marker + CSS）→ **先画连线** → 再画分组框（若有）→ **再画节点**（避免线压字）
5. **保存文件**：按用户/默认路径写入 `.svg`
6. **回传**：给出保存路径 + SVG 代码（便于用户复制）

## 输出模板（直接复用）

生成 SVG 时遵循此骨架（可增删）；配色可采用**灰色系**或**清新淡彩**（见上节色板），下例为淡蓝主色示例：

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 900 700">
  <defs>
    <style>
      .node { fill:#E0F2FE; stroke:#0EA5E9; stroke-width:1.5; }
      .node-core { fill:#BAE6FD; stroke:#0284C7; stroke-width:1.6; }
      .node-decision { fill:#EDE9FE; stroke:#7C3AED; stroke-width:1.5; }
      .label { fill:#1E293B; font-size:14px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
      .label-sub { fill:#64748B; font-size:12px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
      .edge { fill:none; stroke:#0EA5E9; stroke-width:1.5; stroke-linecap:round; stroke-linejoin:round; }
      .edge-label { fill:#475569; font-size:12px; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
      .group { fill:#F0F9FF; stroke:#7DD3FC; stroke-width:1.2; }
      .group-title { fill:#0369A1; font-size:13px; font-weight:600; font-family:Microsoft YaHei UI, Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#0EA5E9"/>
    </marker>
  </defs>
  <!-- edges first -->
  <!-- groups (optional) -->
  <!-- nodes -->
</svg>
```

灰色系版本：节点 `fill:#F1F5F9; stroke:#475569`，连线 `stroke:#64748B`，分组 `fill:#F8FAFC; stroke:#E2E8F0`。

## 质量自检（输出前 10 秒检查）

- [ ] **无重叠**：节点与节点、文字与连线、边标注与箭头之间无压盖；必要时增大 gap 或平移标注
- [ ] 节点对齐与间距一致，文本不溢出（长标签换行：`<tspan x="..." dy="...">`）
- [ ] 箭头方向正确，分支线清晰，分支标签靠近对应边；多入/多出时使用端口偏移
- [ ] `viewBox` 覆盖全部内容且四边留白（无裁切）
- [ ] 风格克制：无渐变、无阴影、线条圆角（stroke-linecap/join round），配色**低饱和**（灰色或清新淡彩均可）

**可选**：对生成的 SVG 运行 `validate_flowchart_style.py` 做样式规范检测，确保无遗漏。

## 示例

需要样例参考时，见 `examples.md`。

