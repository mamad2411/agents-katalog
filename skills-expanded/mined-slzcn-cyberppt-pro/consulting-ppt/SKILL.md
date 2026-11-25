---
name: consulting-ppt
description: 生成或还原咨询风格（麦肯锡/BCG式）的高密度、全可编辑 PowerPoint。用户提到 PPT、slides、deck、汇报材料、提案，或要求把文档/研报/旧PPT/截图转成演示文稿时使用。支持三类输入、双轨渲染（默认全原生可编辑）、自适应确认门禁、12 种视觉风格与 10 个场景框架。
---

# Consulting PPT — Codex 适配层

本文件是 OpenAI Codex（CLI / Cloud）环境的适配层。核心逻辑在 `../core/`，按下表路由。
安装方式：将本仓库放入项目，在 `AGENTS.md` 中加入一行：
`制作 PPT / 演示文稿相关任务时，读取并遵循 CyberPPT-Pro/codex/SKILL.md`。

## 执行顺序与文件路由

| 阶段 | 必读文件 | Codex 工具映射 |
|---|---|---|
| 0 评分定门 | `core/GATES.md` | 评分后一句话告知档位 |
| S1 摄取 | `core/INGEST.md` | 文档解析优先用 shell 内 python（python-docx / pdfplumber / openpyxl，按需 pip install）；.pptx 用 python-pptx 抽取；截图需多模态输入可用时视觉读取，否则请用户提供文字版；C类需求在有网络权限时用内置搜索/浏览，无网络时用模型知识并标注"未核实" |
| S2 故事线 | `core/PIPELINE.md` + `core/frameworks/FRAMEWORKS.md` | 大纲用 Markdown 表格在终端展示 |
| S3 风格 | `core/styles/STYLES.md` | 样张写入 `preview-samples.html`，提示用户在浏览器打开后回复选择（1/2/3）；结构参考 `examples/sample-preview.html` |
| S4 渲染 | `core/RENDER.md` | 原生轨 **python-pptx**（`pip install python-pptx`）；中文 deck 禁用 pptxgenjs 主路径；混合轨需 playwright/puppeteer 截图，环境无浏览器则回退原生轨 |
| S5 质检 | `core/QA.md` | 有 LibreOffice 时 `soffice --headless --convert-to pdf` + `pdftoppm` 截图逐页检查；无 LibreOffice 时跳过视觉层并明确告知；内容层文本抽取检查始终执行 |

## Codex 环境的确认门实现

CLI 无选项组件——每个门以**编号选项**形式提问，一次一个问题：

```
[门C] 风格样张已生成到 preview-samples.html，请在浏览器打开查看。
候选：1) 麦肯锡深蓝  2) 增长橙  3) 暗夜高管
回复编号选择，或回复"换"查看其他风格。
```

批处理/CI 模式（用户以非交互方式运行）：所有门降级为"记录假设并继续"，
假设清单写入 `assumptions.md` 随成品交付。

## 交付

输出到工作目录：`output.pptx`（ASCII 文件名）+ `preview.html` + `assumptions.md`（如有）+
待核实数据清单（如有 AI 补充数据）。打印各文件相对路径。

## 环境差异速查

| 能力 | 有 | 无 |
|---|---|---|
| 网络权限 | C类调研，证据附URL | 模型知识 + "未核实"标注 |
| 浏览器截图 | 混合轨可用 | 回退原生轨 |
| LibreOffice | 完整视觉QA | 仅内容QA，告知用户 |
| 多模态图片输入 | 截图还原可用 | 请用户改用 pptx 原文件或文字描述 |
