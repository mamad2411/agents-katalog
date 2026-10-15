---
name: research-writing-assistant
description: 面向中文科研论文的AI写作助手。支持头脑风暴、章节写作、文献综述、Python图表、LaTeX输出。
allowed-tools: Read Write Edit Bash WebSearch
---

# 科研写作助手 (Research Writing Assistant)

面向本科与研究生论文写作的执行型 Skill，重点解决：
- **头脑风暴**：7轮问答确认论文类型、学科、题目、研究背景、方法、章节结构
- **写作去AI化**：约束机械过渡词、空壳强调句、主观化表达
- **章节化输出**：每章输出到 `chapters/` 目录的独立文件
- **LaTeX支持**：用户提供模板后可输出可编译的 LaTeX 项目
- **环境自动化**：Miniconda + 虚拟环境 + 绘图依赖

## 新架构（v3.0）

本 Skill 已升级为模块化技能架构，支持多平台：

| 平台 | 配置 |
|------|------|
| Claude Code | `.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Codex | `.codex/INSTALL.md` |
| OpenCode | `.opencode/INSTALL.md` |
| Gemini CLI | `GEMINI.md` |

## 技能列表

### 核心流程技能

| 技能 | 路径 | 说明 |
|------|------|------|
| using-research-writing | `skills/using-research-writing/` | 入口技能，规则和路由 |
| brainstorming-research | `skills/brainstorming-research/` | 头脑风暴，7轮问答 |
| writing-chapters | `skills/writing-chapters/` | 章节写作 |
| latex-output | `skills/latex-output/` | LaTeX 输出 |

### 写作支持技能

| 技能 | 路径 | 说明 |
|------|------|------|
| writing-core | `skills/writing-core/` | 核心写作规范 |
| writing-humanities | `skills/writing-humanities/` | 文科写作 |
| writing-medical | `skills/writing-medical/` | 医学写作 |
| writing-law | `skills/writing-law/` | 法学写作 |
| literature-review | `skills/literature-review/` | 文献综述 |

### 工具技能

| 技能 | 路径 | 说明 |
|------|------|------|
| figures-python | `skills/figures-python/` | Python 数据图表 |
| figures-diagram | `skills/figures-diagram/` | 流程图/架构图 |
| peer-review | `skills/peer-review/` | 自审检查 |
| statistical-analysis | `skills/statistical-analysis/` | 统计分析 |
| prompts-collection | `skills/prompts-collection/` | 提示词集合 |
| environment-setup | `skills/environment-setup/` | 环境配置 |

## 执行门禁

<EXTREMELY-IMPORTANT>
任何论文写作任务开始前，必须先调用 `skills/using-research-writing/` 确定流程。
不允许跳过头脑风暴直接写作。
</EXTREMELY-IMPORTANT>

### 标准流程

1. **头脑风暴** → 调用 `brainstorming-research`
   - 确认论文类型（7种）
   - 确认学科领域
   - 确认题目、研究背景、方法
   - 确认章节结构
   - 检测 LaTeX 模板
   - 创建 plan/ 和 chapters/

2. **章节写作** → 调用 `writing-chapters`
   - 每章独立文件
   - 去 AI 化检查
   - 用户确认后继续

3. **LaTeX 输出**（可选）→ 调用 `latex-output`
   - 用户提供模板
   - 输出 .tex 文件
   - 可直接编译

## 模块兼容（向后兼容）

原有 `modules/` 目录仍然保留，可通过以下方式使用：

| 场景 | 模块 |
|------|------|
| 通用写作 | `modules/writing-core.md` |
| 文科写作 | `modules/writing-humanities.md` |
| 医学写作 | `modules/writing-medical.md` |
| 法学写作 | `modules/writing-law.md` |
| 文献综述 | `modules/literature-review.md` |
| 翻译润色 | `modules/prompts-collection.md` |
| 自审检查 | `modules/peer-review.md` |
| Python图表 | `modules/figures-python.md` |
| 流程图 | `modules/figures-diagram.md` |
| 环境配置 | `modules/environment-setup.md` |
| LaTeX指南 | `modules/latex-guide.md` |

## 输出规范

### 去 AI 化
- 禁用机械过渡词：首先、其次、最后、此外
- 禁用空壳强调句：值得注意的是、需要指出的是
- 语气客观，使用"本文"、"本研究"

### 格式规范
- 段落之间空一行
- 正文不使用加粗
- 论文正文优先连贯段落，不使用列表堆砌

### 引用规范
- 绝不编造文献
- 引用必须可追溯

## 文献与事实规则

1. 绝不编造文献。
2. 英文文献可检索后引用，中文文献优先让用户提供来源。
3. 任何引用必须可追溯（作者、年份、出处至少完整两项）。

## 版本信息

- 版本：3.0.0
- 更新日期：2026-03-19
- 维护目标：可执行、可追踪、流程化、多平台适配
