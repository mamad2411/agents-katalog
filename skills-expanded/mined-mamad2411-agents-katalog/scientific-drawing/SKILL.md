---
name: scientific-drawing
description: |
  学术论文科学绘图技能——基于多年实战踩坑修复的经验提炼库。
  适用于创建所有类型的学术图表，包含 TikZ/matplotlib 完整规则与配色方案。

  **触发场景**（出现以下任意关键词时使用）：
  - "画图"、"绘图"、"新建图"、"生成图"、"创建图"
  - "修改图"、"更新图"、"调整图"、"图有问题"、"图不对"
  - 提及具体图名：架构图、流程图、示意图、原理图、机制图、扇形图、同心圆图、神经网络图、融合架构图
  - 提及曲线图、折线图、雷达图、热图、散点图、柱状图
  - 需要生成 .tex / .py / .svg / .pdf / .png 图形文件
  - 提及 figures/ 目录下任何子目录

  **输出目录**：`./figures/`（相对于项目根目录）
---

# 科学绘图技能

## 0. 核心约束（不可违反）

| 约束 | 规范 |
|---|---|
| **字体大小** | 正文字体小四（12pt）= `\normalsize` (TikZ) = `font.size=13` (matplotlib)；**禁止** `\small`、`\footnotesize` |
| **留白** | 不过大；standalone border `10–15pt`；matplotlib `bbox_inches="tight"` |
| **遮挡** | 所有内容不得遮挡（坐标轴 legend 除外）；文字与圆弧/节点严格分离 |
| **配色** | 顶刊克制风；示意图 ≤ 5 色相，数据图 ≤ 3–4 色相；**禁止**浅灰（`#999999`、`#CCCCCC` 等）、禁止 rainbow |
| **编译器** | TikZ 必须 **xelatex**（禁用 pdflatex） |
| **输出** | matplotlib 始终输出 SVG；TikZ 输出 PDF → 导出 SVG |

---

## 1. 决策树：选择技术路线

```
需要画什么？
│
├─ 示意图 / 原理图 / 机制图 / 架构图 / 流程图 / 网络拓扑图 / 扇形图 / 同心圆
│   └─→ TikZ（xelatex 编译）
│
├─ 数据图：曲线、折线、散点、热图、雷达、柱状、ROC
│   └─→ Python matplotlib
│
└─ 算法伪代码
    └─→ LaTeX article + algorithm2e
```

---

## 2. TikZ 快速工作流

```bash
# 1. 新建 figures/子目录/fig.tex（从下方模板开始）
# 2. 开调试网格确认位置
# 3. 编译
cd figures/子目录/ && xelatex -interaction=nonstopmode fig.tex
# 4. 预览
pdftoppm -r 200 -png fig.pdf fig_preview && mv fig_preview-1.png fig.png
# 5. 确认无遮挡后导出 SVG
pdftocairo -svg fig.pdf fig.svg
# 6. 清理
rm -f *.aux *.log *.fls *.fdb_latexmk fig_preview*.png
```

**必须包含的 preamble：**
```latex
\documentclass[border={15pt 10pt 10pt 10pt}]{standalone}
% border 顺序：left bottom right top（非 CSS 顺序！）
\usepackage{xeCJK}
\setCJKmainfont{PingFang SC}
\usepackage{tikz}
\usetikzlibrary{positioning, shapes.geometric, arrows.meta, fit, calc, backgrounds}
\usepackage{xcolor}
```

---

## 3. matplotlib 快速工作流

```bash
# 1. 新建 figures/子目录/fig.py（从下方模板开始）
# 2. 运行
python3 figures/子目录/fig.py
# 3. 验证 SVG 输出
ls figures/子目录/fig.svg
```

**文件头部必须（每个脚本复制）：**
```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as _fm
import os, sys

_SANS_PATH = "/Users/sunyue/Library/Fonts/SourceHanSansCN-Regular.ttf"
_fm.fontManager.addfont(_SANS_PATH)           # 必须在 rcParams 之前

plt.rcParams['font.family']        = 'sans-serif'
plt.rcParams['font.sans-serif']    = ['Source Han Sans CN', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size']          = 13       # 小四 ≈ 13pt（正文对齐）
plt.rcParams['axes.titlesize']     = 20
plt.rcParams['axes.labelsize']     = 16
plt.rcParams['xtick.labelsize']    = 13
plt.rcParams['ytick.labelsize']    = 13
plt.rcParams['legend.fontsize']    = 13
plt.rcParams['figure.dpi']         = 150

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_SCRIPT_DIR, ".."))   # 调整层级
from color_palette import BLUE, RED, BLACK, GRID_COLOR, GRID_ALPHA, SPINE_COLOR, SPINE_WIDTH
```

**axes 标准样式（每个图必须）：**
```python
ax.spines[["top", "right"]].set_visible(False)
for sp in ["left", "bottom"]:
    ax.spines[sp].set_color(SPINE_COLOR)
    ax.spines[sp].set_linewidth(SPINE_WIDTH)
ax.tick_params(axis="both", width=2.0, length=6, colors=BLACK, pad=5)
ax.grid(True, ls=":", lw=2.0, color=GRID_COLOR, alpha=GRID_ALPHA)
```

**保存（必须 SVG + bbox_inches="tight"）：**
```python
plt.tight_layout()
plt.savefig(os.path.join(_SCRIPT_DIR, "fig.svg"), format="svg", bbox_inches="tight")
```

**legend（禁止同时传 prop 和 fontsize）：**
```python
ax.legend(loc="upper right", frameon=True, framealpha=0.85,
          edgecolor=BLACK, prop={'size': 13})   # ← 只用 prop，不加 fontsize=
```

---

## 4. 配色速查

**推荐：IEEE/Springer 深蓝 + 深灰**
```latex
\definecolor{colPrimary}{RGB}{31,73,125}    % IEEE 深蓝
\definecolor{colSecondary}{RGB}{64,64,64}   % 深灰
\definecolor{colArrow}{RGB}{30,30,30}       % 近黑箭头
```

**Nature 低饱和（扇形图/饼图）**
```latex
\definecolor{clrGreen}{HTML}{8FBCB2}   % 灰绿
\definecolor{clrBlue} {HTML}{8AAAC8}   % 灰蓝
\definecolor{clrPurple}{HTML}{A99DC4}  % 灰紫
\definecolor{clrWarm} {HTML}{C8AD8A}   % 灰暖
```

**Python 主色板（`figures/color_palette.py` 统一导入）**
```python
BLUE="#1D4ED8"  RED="#DC2626"  GREEN="#16A34A"  AMBER="#F59E0B"  PURPLE="#7C3AED"
```

**禁止色**：`#999999`、`#CCCCCC`、`#EEEEEE` 等浅灰；纯原色 `#FF0000`、`#00FF00`；4 色以上混用。

---

## 6. 多Agent绘图-审查迭代工作流（必须遵守）

> **核心原则**：每张图必须经过独立审查 agent 用 `look_at` 读取 PNG 并逐条确认通过，才算完成。主 Agent **禁止自审自查**——不得在不调用审查 agent 的情况下声称图已完成。

### 6.1 Agent 分工

| Agent 角色 | 职责 | 允许工具 | 禁止工具 |
|---|---|---|---|
| **绘图 Agent** | 编写 .tex/.py、编译/运行、生成 PNG 预览；可用 `look_at` 自查明显错误并自行修正 | Write, Edit, Bash, look_at | — |
| **审查 Agent** | 调用 `look_at` 读取 PNG，逐条核查检验清单，返回 PASS / FAIL + 参数级修改建议 | look_at | Write, Edit, Bash |
| **主 Agent（你）** | 分发任务、接收结果、协调迭代；收到 PASS 后导出 SVG | task(), background_output() | — |

### 6.2 完整执行流（必须按此顺序）

```
Step 1 ── 主 Agent 启动绘图 Agent（run_in_background=false）
          task(category="unspecified-high", run_in_background=false,
               description="绘制 [图名]", prompt="[见 §6.4 绘图 Agent 首次模板]")
          → 获得 session_id_draw（保存！）
          → 获得 fig.png 路径

Step 2 ── 主 Agent 启动审查 Agent（run_in_background=false）
          task(category="unspecified-low", run_in_background=false,
               description="审查 [图名]", prompt="[见 §6.4 审查 Agent 模板，含 fig.png 绝对路径]")
          → 获得 session_id_review（保存！）
          → 获得 PASS 或 FAIL+问题列表

Step 3 ── 若 PASS → 主 Agent 执行导出 SVG（pdftocairo -svg），任务完成
          若 FAIL → 继续 Step 4

Step 4 ── 主 Agent 续接绘图 Agent（session_id=session_id_draw）
          task(session_id=session_id_draw, run_in_background=false,
               prompt="审查结果 FAIL，问题如下：\n[粘贴 FAIL 列表]\n请修改并重新生成 fig.png。")
          → 获得新 fig.png

Step 5 ── 主 Agent 续接审查 Agent（session_id=session_id_review）
          task(session_id=session_id_review, run_in_background=false,
               prompt="图已更新，请重新 look_at([fig.png绝对路径]) 并逐条核查。")
          → 获得新一轮 PASS 或 FAIL

Step 6 ── 重复 Step 4–5，最多 3 轮。
          超过 3 轮仍 FAIL → 主 Agent 直接介入阅读 FAIL 列表，判断是否需要架构重设计（非渐进修改）
```

> **严格规则**：
> - 每轮审查必须用新的 `look_at` 调用（不得凭记忆或上轮结论判断）
> - 绘图 Agent 每次修改后必须重新生成 PNG（不得复用旧图）
> - 主 Agent 不得跳过审查步骤直接声称"图已完成"

### 6.3 审查 Agent 检验清单（每次 look_at 后逐条核查，输出 □✓ / □✗）

```
【字体】
□ 所有文字是否清晰可读（与正文字号相当）？
□ 是否存在疑似 \small / \footnotesize 的过小字号？
□ 中文是否正常显示（无方块乱码）？

【遮挡】（最高优先级，任意一项 ✗ 即 FAIL）
□ 是否有文字压在圆弧/线条/节点边框上？
□ 是否有节点互相重叠（非刻意）？
□ 是否有箭头穿过文字或节点内容？
□ legend/图例是否遮挡关键数据区域？

【布局与留白】
□ 图形边距是否合适（standalone border 10–15pt，不过大也不被裁剪）？
□ 各列/各行间距是否均匀，无明显疏密不均？
□ 是否有内容超出图形边框被裁剪？

【配色】
□ 是否使用了浅灰（视觉接近 #999999 / #CCCCCC 的低对比色）？
□ 色相数量是否在限制内（示意图 ≤5，数据图 ≤4）？
□ 标注文字颜色是否与对应线条/元素保持一致？

【整体】
□ 图的信息是否清晰传达（结构/流程/层次一目了然）？
□ 图形整体是否对称/平衡（无明显偏斜）？
```

**审查 Agent 返回格式（严格遵守）**：
```
PASS — 所有 □✓，无问题。
或
FAIL
□✓ 字体：文字清晰可读
□✓ 字体：中文正常
□✗ 遮挡：标注"发射波束"文字压在虚线箭头线上 → 建议 yshift=-20pt（当前 -8pt 不足）
□✗ 字体：右下角"输出"节点文字偏小，疑似 \small → 改为 \normalsize
□✓ 布局：边距合适
□✗ 留白：右侧空白过多（目测约 3cm）→ border right 从 20pt 缩至 10pt
□✓ 配色：无浅灰，色相数量合规
□✓ 整体：信息传达清晰
```

### 6.4 主 Agent 分发 prompt 模板

**绘图 Agent（首次）**：
```
TASK: 根据以下要求创建 [图名] 的 TikZ/matplotlib 代码，编译并生成预览 PNG。

EXPECTED OUTCOME:
- 文件已创建：[绝对路径/fig.tex] 或 [绝对路径/fig.py]
- 编译/运行成功（无 Error、无 Warning 级字体缺失）
- PNG 已生成：[绝对路径/fig.png]（-r 200 分辨率）

REQUIRED TOOLS: Write, Edit, Bash

MUST DO:
- 从 scientific-drawing/SKILL.md §2（TikZ）或 §3（matplotlib）模板出发
- TikZ 用 xelatex 编译；matplotlib 用 python3 运行
- TikZ 生成 PNG 命令：
    pdftoppm -r 200 -png fig.pdf fig_preview && mv fig_preview-1.png fig.png
- 严格遵守 references/elements.md 和 references/tikz-rules.md 所有规则
- 每次小改后立即重新编译确认，不批量改动后才编译

MUST NOT DO:
- 不导出 SVG（审查通过后由主 Agent 执行）
- 不使用 \small、\footnotesize、pdflatex
- 可用 look_at 自查明显问题并自行修正，但最终质检由审查 Agent 独立完成

CONTEXT:
- 图的需求：[具体描述]
- 技能路径：[skill-root-path]/
- 输出目录：[figures/子目录/]
```

**审查 Agent（每轮）**：
```
TASK: 视觉审查 [绝对路径/fig.png]，逐条核查标准检验清单，返回 PASS 或 FAIL+问题列表。

EXPECTED OUTCOME:
- 对 §6.3 每条检查项输出 □✓ 或 □✗
- 若存在 □✗，每条给出：问题描述 + 定位到 TikZ/matplotlib 参数级别的修改建议

REQUIRED TOOLS: look_at（仅此一项）

MUST DO:
- 第一步必须调用 look_at，参数 file_path=[绝对路径/fig.png]，goal="检查字体大小、文字遮挡、节点重叠、边距留白、配色"
- 按 §6.3 检验清单顺序逐条输出结果
- 对每个 □✗ 给出具体参数修改建议（如：yshift=-20pt、border right=10pt、改 \normalsize）

MUST NOT DO:
- 不修改任何代码文件
- 不执行任何编译或运行命令
- 不根据代码推断图的外观——必须基于 look_at 实际图像内容判断

CONTEXT:
- 图片路径：[绝对路径/fig.png]
- 原始需求：[...]
- 检验清单：见 scientific-drawing/SKILL.md §6.3
```

**绘图 Agent（迭代修改，必须续接 session_id）**：
```
task(
  session_id="[上一轮绘图 Agent 的 session_id]",
  run_in_background=False,
  prompt="""审查 Agent 返回 FAIL，问题如下：
[粘贴完整 FAIL 列表，含每条 □✗ 和参数级修改建议]

请按上述问题逐条修改 fig.tex/fig.py，重新编译，重新生成 fig.png。
修改完成后，输出：已修改项目列表 + 新 fig.png 的绝对路径。"""
)
```

**审查 Agent（续接审查，必须续接 session_id）**：
```
task(
  session_id="[上一轮审查 Agent 的 session_id]",
  run_in_background=False,
  prompt="""绘图 Agent 已完成修改，新图已生成。
请重新调用 look_at([绝对路径/fig.png]) 并按 §6.3 检验清单重新逐条核查，返回新一轮 PASS 或 FAIL+问题列表。
注意：必须基于新图实际内容判断，不得复用上轮结论。"""
)
```

---

- **TikZ 布局与模板**：[references/tikz-rules.md](references/tikz-rules.md)
  - 何时读：多列布局 / y 坐标管理 / 调试网格 / 布局级 Bug 速查表
- **各要素绘制规则**：[references/elements.md](references/elements.md)
  - 何时读：节点形状 / 箭头（fan-in、fan-out、交叉标注）/ 层标签 / fit框 / 背景层 / 扇形图 / 同心圆 / 分隔线 / 要素级 Bug 速查表
- **matplotlib 全规则**：[references/matplotlib-rules.md](references/matplotlib-rules.md)
  - 何时读：字体注册 / legend / spines / 输出 / 踩坑修复
- **配色规范**：[references/color-standards.md](references/color-standards.md)
  - 何时读：选色原则 / 图形类型选色 / TikZ 色板 / 标注文字配色 / Python 降饱和工具
- **配色 JSON 参考库**：[references/color-palettes.json](references/color-palettes.json)
  - 何时读：需要具体 hex 值 / 选主题色板（`themes.*`）/ 定性、顺序、发散色板数组
- **编译与导出**：[references/compile-export.md](references/compile-export.md)
  - 何时读：编译命令 / PDF→SVG / 清理 / macOS cairo 问题
