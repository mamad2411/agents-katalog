---
name: mac-editable-figure
description: >-
  Mac-native editable-figure studio — the no-CUDA replacement for Visiomaster. Turn any image,
  screenshot, AI-generated PNG, or PDF figure into an EDITABLE vector you can tweak by hand, then
  export SVG / PNG / PDF. Two reconstruction modes: (A) LLM-vision redraw — Claude reads the image
  and reproduces it as editable SVG / TikZ / Mermaid (best for flowcharts, framework diagrams,
  architecture/pipeline figures, 论文框架图/技术路线图); (B) potrace auto-trace for line art / logos /
  high-contrast monochrome. Vector PDF figures are made editable losslessly via pdf2svg. Pure CPU,
  runs on Apple Silicon / Intel Mac with no GPU. Triggers on: 可编辑图、把图变可编辑、Visiomaster、
  图转SVG、image to svg、editable figure、矢量化、redraw figure、框架图重画、导出SVG/PNG/PDF.
---

# Mac Editable Figure Studio (Visiomaster 的 Mac 改造版)

> **关于 Visiomaster 的澄清**：Visiomaster（Rss3208/Visiomaster）**不用 CUDA/显卡**——它真实技术栈是 **LLM视觉理解 + 微软 Visio COM 自动化(pywin32)**，拦路的是 **Windows + 微软 Visio**（输出 .vsdx）。网传"基于CUDA"是误解。它的方法（图→结构分解→确定性渲染脚本）本 skill 完全复刻，只把输出从 .vsdx 换成 **SVG**（跨平台、Figma/Inkscape 可编辑），因此 **Mac 不需要任何 GPU 就能做同样的事**。

本 skill 用**"LLM 视觉重建 + CPU 矢量工具链(含 vtracer 自动彩色矢量化)"**达到 Visiomaster 同样目的，全程零 GPU。

## 工具链（CPU，已装于本机）

```bash
brew install librsvg pdf2svg potrace            # rsvg-convert / pdf2svg / potrace
# vtracer(彩色自动矢量化) 装在本 skill 独立 venv: scripts/../.venv
python3 -m venv .venv && .venv/bin/pip install vtracer
```

| 工具 | 作用 |
|------|------|
| `pdf2svg` | 矢量 PDF 图 → SVG（**无损**，已有矢量图首选） |
| `vtracer` | **彩色位图 → SVG（自动，Mac CPU，最接近Visiomaster体验）** |
| `rsvg-convert` | SVG → PNG(高DPI) / PDF(投稿/LaTeX) |
| `potrace` | 单色线稿/logo → SVG（描摹） |
| `sips` | macOS 自带，位图格式预处理 |

## 三种工作流（按图的来源选）

### 流程1：已有矢量 PDF 图 → 可编辑 SVG（无损，最优）
适用：本论文 `figures/*.pdf`、TikZ 编译出的图、任何矢量 PDF。
```bash
pdf2svg input.pdf output.svg            # 多页：pdf2svg in.pdf out.svg 2
```
SVG 用 Figma / Inkscape / Boxy SVG 可视化编辑 → 改完导回：
```bash
rsvg-convert -f pdf -o output.pdf output.svg     # 回 LaTeX
rsvg-convert -f png -d 300 -p 300 -o output.png output.svg   # 回 DOCX(300dpi)
```

### 流程2：位图/截图/AI图 → 可编辑 SVG
**模式A（推荐，适合图表/流程图/框架图/技术路线图）= LLM 视觉重建**：
- 把图给 Claude（Read 图片），让它**按图重画成可编辑代码**：
  - 流程图/框架图/架构图 → **SVG** 或 **TikZ**（结构清晰、文字可改）
  - 简单结构 → **Mermaid**（最易后期改）
- 重建后用 `rsvg-convert` 导出 SVG/PNG/PDF。这是 Visiomaster 的核心能力，靠模型视觉而非 CUDA。
- 重建铁律：**只复刻可见结构与文字，不臆造数据**；颜色/字体可参数化，便于二次调整。

**模式B（彩色位图自动矢量化）= vtracer**（最接近 Visiomaster 的一键体验）：
```bash
scripts/figtool.sh vtrace input.png output.svg color   # 彩色; 单色用 binary
```
适合截图、AI生成图、彩色图表。Mac CPU，秒级完成，输出可编辑 SVG。

**模式C（单色线稿/logo）= potrace 描摹**：
```bash
scripts/figtool.sh trace input.png output.svg 0.5
```
仅擅长单色线条；彩色/复杂结构图 → 用模式A(LLM重建,结构最准) 或模式B(vtracer,色块最准)。

### 流程3：SVG ↔ 各格式互转（导出三件套）
```bash
rsvg-convert -f svg -o out.svg in.svg     # 规整
rsvg-convert -f png -d 300 -p 300 -o out.png in.svg
rsvg-convert -f pdf -o out.pdf in.svg
```

## Mac 可视化编辑器推荐
- **Inkscape**（免费开源，`brew install --cask inkscape`）— 全功能 SVG 编辑
- **Figma**（免费网页版）— 拖拽友好，团队协作
- **Boxy SVG**（App Store）— 轻量原生
- **Affinity Designer / Illustrator** — 专业付费

## 配套脚本
`scripts/figtool.sh` 封装了 pdf2svg / svg导出 / 位图描摹三类操作，见该文件。

## 与本项目其他 skill 的分工
- 出**新数据图**（柱/折线/雷达/帕累托）→ 用 `nature-figure`（R/Python，源码即可编辑）。
- 把**已有图/外部图变可编辑** → 用本 skill。
- 二者互补：nature-figure 管"生成"，mac-editable-figure 管"改造为可编辑矢量"。
