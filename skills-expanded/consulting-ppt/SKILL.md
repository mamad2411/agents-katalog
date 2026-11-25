---
name: consulting-ppt
description: 生成或还原咨询风格（麦肯锡/BCG式）的高密度、全可编辑 PowerPoint。只要用户提到制作 PPT、幻灯片、slides、deck、汇报材料、路演材料、提案，或要求把文档/研报/数据/旧PPT/截图转成演示文稿，或提到"咨询风格""行动性标题""SCR""还原成可编辑PPT"，都必须使用本 skill——即使用户没有明确说"咨询风格"。支持三类输入（文档数据、旧PPT/截图还原、一句话需求）、双轨渲染（默认全原生可编辑，可选混合底图）、自适应确认门禁、12 种咨询视觉风格与 10 个场景内容框架。
---

# Consulting PPT — Claude 适配层

本文件是 Claude（claude.ai / Claude Code / Cowork）环境的适配层。
**核心逻辑全部在 `../core/` 中，按下表在对应阶段读取，不要凭记忆跳过。**

## 执行顺序与文件路由

| 阶段 | 必读文件 | Claude 工具映射 |
|---|---|---|
| 0 评分定门 | `core/GATES.md` | 评分后在回复中一句话告知档位（如"按标准档执行，共 3 个确认点"） |
| S1 摄取 | `core/INGEST.md` | 上传文件在 `/mnt/user-data/uploads/`；.pptx 用 pptx skill 的 `extract-text`；截图直接视觉读取；C类需求用 web_search 调研 |
| S2 故事线 | `core/PIPELINE.md` + `core/frameworks/FRAMEWORKS.md` | 大纲以紧凑表格形式在对话中展示 |
| S3 风格 | `core/styles/STYLES.md` | 样张用 HTML artifact / `preview.html` 呈现（**本环境无图像生成，样张一律 HTML，参考 `examples/sample-preview.html` 的卡片结构**） |
| S4 渲染 | `core/RENDER.md` | 原生轨用 **python-pptx**（中文 deck 禁用 pptxgenjs 主路径）；同时必读平台 pptx skill（`/mnt/skills/public/pptx/SKILL.md`）的字体与QA约束，两者冲突时以 pptx skill 为准；混合轨底图截图能力缺失时（无无头浏览器）自动回退原生轨并告知用户 |
| S5 质检 | `core/QA.md` | PPTX→PDF→截图：`soffice --headless --convert-to pdf` + `pdftoppm`；有子代理（Cowork/Claude Code）时视觉QA交给子代理 |

## Claude 环境的确认门实现

- 有选项交互组件（如 ask_user_input）时，门A/门C 用选项组件；门B 大纲用表格+"通过/改哪页"。
- 每个门只问一个问题，遵守 `GATES.md` 的问法规范。
- 移动端用户：样张 HTML 卡片按 640px 宽度可读设计。

## 交付

1. 产出到 `/mnt/user-data/outputs/`：`output.pptx`（ASCII 文件名）+ `preview.html`。
2. 用文件呈现工具（present_files）交付，附一句话说明；含 AI 补充数据时附待核实清单。
3. 中文文件名会在部分移动端下载失败——文件名一律 ASCII，中文标题放封面。

## 环境差异与降级

| 能力 | 有 | 无 |
|---|---|---|
| 联网搜索 | C类需求做调研，证据标注URL | 用模型知识，证据标注"未核实"并显著提示 |
| 无头浏览器截图 | 混合轨可用 | 混合轨不可用，回退原生轨 |
| 子代理 | 视觉QA用子代理 | 自查，逐页对照 QA.md 清单 |
| LibreOffice | 正常QA截图 | 跳过视觉QA第二层，告知用户未做渲染校验 |
