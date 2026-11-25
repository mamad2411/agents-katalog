---
name: cn-resume-optimizer
description: 面向中国职场语境的中文简历优化与 JD 对齐（支持 PDF/Word/Markdown 输入；本地提取文本→结构化→改写建议→导出 Markdown）。
metadata:
  openclaw:
    emoji: "📄"
    category: "productivity"
    tags: ["resume", "cv", "china", "ats", "jd", "pdf"]
---

# 中国职场简历优化（China Resume Optimizer）

本技能把“简历优化”拆成可审计的本地流水线：**提取文本**（PDF/Word/Markdown）→ **结构化**（教育/经历/项目/技能）→ **按中国招聘习惯打分与指出问题** → **基于目标 JD 做关键词对齐与改写** → 输出可编辑的 Markdown，并可本地导出 PDF。

本技能已补齐四段“稳定可控”的执行器（输入→结构化→输出）：

- `scripts/extract_pdf_text.py`：**PDF → 文本**（本地 PyMuPDF/fitz；不做外网调用）
- `scripts/parse_resume_cn.py`：**简历文本 → 结构化 JSON**（启发式解析；保留原文块，便于审计与回退）
- `scripts/parse_jd_cn.py`：**JD 文本 → 结构化 JSON**（职责/要求/关键词）
- `scripts/md2pdf.sh`：**Markdown → PDF**（本地 pandoc + weasyprint；优先保证中文字体渲染）

## 适用范围

- 中文简历为主（允许技术栈英文混排）。
- 目标：更贴近中国面试官的快速筛选路径（对口度、项目结果、时间线、关键信息密度）。

## 安全边界

- 默认不外发简历内容到第三方服务。
- 只在本机读写指定输入/输出文件。

## 使用方式（约定）

用户可以：
- 直接贴简历文本让我优化；或
- 发送 PDF/Word 文件，我先提取文本再优化；或
- 贴 JD（或文件路径），做“对齐版简历”。

## 输出

- `output/resume/optimized_resume.md`：改写后的简历草稿（中文语境）
- `output/resume/report.md`：问题清单 + 关键词对齐表 + 可验证指标建议

## 参考模板（必须读）

- `references/china_resume_rubric.md`：**评估 Rubric**（中国职场筛选链路：对口度/结果/可信度/结构）
- `references/china_resume_template.md`：**中文简历模板**（技术岗默认版，可据岗位改）

## 核心评分维度（中国职场）

- 抬头信息是否完整（城市/电话/邮箱/求职意向/到岗时间等按需）
- 时间线是否一致（空窗、跳槽频率、教育/工作顺序）
- 项目描述是否结果导向（指标、规模、ROI、成本/效率、稳定性）
- 技术/能力栈是否分层（熟练/掌握/了解）
- 针对 JD 的对口度（关键词出现、语义对齐、优先级排序）
- 可信度与可追问性（角色边界/产物/约束条件）

