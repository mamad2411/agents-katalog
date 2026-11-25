---
name: ost-repo-readme-summary
description: 'Write repo_readme_summary.md for any open-source library in the open_supports/ system. Use when adding a new support package or updating an existing summary. Produces a concise 5-part structured document distilled from the official README.'
argument-hint: 'GitHub owner/repo of the target library, e.g. colbymchenry/codegraph'
---

# 编写 open_supports 仓库摘要（repo_readme_summary.md）

## When to Use

- 为 `open_supports/` 新增支持包时，填充 `repo_readme_summary.md`
- 官方 README 有重大版本更新时，同步更新现有摘要

## Pre-read

执行前读取以下内容，按优先级顺序：

1. 目标库的**官方 GitHub README**（主文件）
2. 官方文档网站（如有）
3. 该支持包的 **`.ost-refs/` 目录**（如存在）— 了解本地路径约定或特殊配置

> **下游说明**：`repo_readme_summary.md` 直接作为 `ost-install-script`（写安装脚本）和 `ost-skill-for-setup`（写安装技能）的参考输入。**Part 2 的准确性和完整性对这两个技能的产出质量有直接影响**，是本文档最重要的部分。

## GitHub Source Policy

读取 GitHub 仓库事实、README、目录、release、issue、PR 或文件内容时，优先使用 GitHub connector / GitHub app 的结构化工具；若工具不可见，先通过 `tool_search` 搜索 GitHub 工具。仍不可用时，再考虑 `gh` CLI、GitHub 官方 API 或官方文档网站。

`curl` / raw GitHub URL 只用于官方安装命令本身，或作为明确记录的 fallback。不要把安装文档中的 `curl | sh` 习惯扩展为 README、仓库结构或 release 信息的默认获取方式。

作为 workflow 阶段子代理返回结果时，必须包含：

- `sources_used`: 来源类别和关键路径摘要
- `fallbacks`: 降级原因摘要；没有降级时返回空数组

## Clarification / Blocking

如果执行本阶段所需信息无法从官方 README、官方文档或 `.ost-refs/` 中可靠判断：

1. 不要猜测关键行为
2. 向 workflow 返回一个澄清问题
3. 标明 blocked 字段：
   - `stage`: `repo_readme_summary`
   - `reason`
   - `question`
   - `suggested_default`（如有）
4. 等用户回答后再继续本阶段

典型阻塞点：

- 官方 README 与文档网站给出的安装命令冲突
- 官方没有说明更新或验证命令，且无法从 CLI 文档可靠推出
- `.ost-refs/` 指定了本地约定，但与官方默认流程冲突
- 用户要求收录的平台或客户端超出官方支持范围

## 文件头格式

```markdown
# {LibraryName} — 仓库核心介绍

> 官方仓库：[{owner}/{repo}](https://github.com/{owner}/{repo})
> 官方文档：[...](...)   ← 有则保留，无则删除此行
```

## 文档结构（5 部分）

按以下顺序编写：

| # | 部分标题 | 内容定位 |
|---|---------|---------|
| 1 | **概览** | 一句话定位 + 核心能力（3~5 条）+ 官方仓库 / 文档链接 |
| 2 | **安装与更新** | 前置依赖（含版本要求）、**全部**官方安装方式（逐平台分列）、更新命令、验证命令；见下方专项要求 |
| 3 | **使用示例** | 最小可运行示例 + 有限理解性注释；只帮助快速读懂，不展开多场景教程 |
| 4 | **注意事项** | 已知限制、常见问题、版本兼容性、实际坑点 |
| 5 | **补充与延伸** | 非核心内容精炼指引；安装相关深度内容（CI / 非交互式安装、手动安装、高级配置、卸载）**必须在此给出原文链接**，不复制大段原文 |

## Part 2 专项要求（安装与更新）

此部分直接影响下游脚本和技能的产出质量，要求最严格。

**完整性**
- 列出官方文档中的**所有**安装方式（curl、npm、pip、brew、手动下载等），不因存在「推荐方式」而省略其他
- 多步骤安装流程（如：CLI 安装 → 接入 Agent → 初始化项目）必须分步标注，不合并为一条

**平台差异**
- macOS、Linux、WSL、Windows 有不同命令时，**分别列出**，不用「同 Linux」「...」等省略
- WSL 若与 Linux 行为存在差异（如配置路径、PATH 写入），单独标注

**命令准确性**
- 所有命令**逐字照录**官方文档，不改写、不简化
- 前置依赖若有版本要求（如 `Node.js ≥ 18`、`Python ≥ 3.10`），必须保留具体版本号，不写「需要 Node.js」等模糊表述

**更新与验证**
- 更新命令独立列出，不与安装命令合并（即使只是 `tool upgrade`）
- 验证命令应确认工具**可用**；优先选择执行最小功能的命令（如 `tool version` 或 `tool help`）；若官方只提供 `--version`，保留并注明

**安装作用域契约（必填）**

在 Part 2 的安装命令之后增加 `### 安装作用域与目标目录`，以表格记录下游脚本、setup Skill 和用法示例必须复用的事实：

| 字段 | 必填内容 |
|---|---|
| 分类 | `A` 仅全局、`B` 项目本地／CWD 敏感、`C` 原生路径参数、或 `D` 双模式 |
| 官方默认 | 不带可选 flag 的官方命令及其真实写入范围 |
| 项目目录 | 是否需要；默认 `.` 是否成立；CWD 是否决定结果；或官方原生路径 flag 的精确名称 |
| 执行要求 | `A` 直接全局、`B` 必须在目标目录子 shell 执行、`C` 必须传原生路径、`D` 分别说明两个分支 |
| 官方证据 | 具体一手文档链接及支撑该结论的命令 |

- 不能从官方资料确认分类、默认值、CWD 行为或路径参数时，必须在本阶段阻塞澄清；不以「一般 CLI 行为」补全。
- `B` 必须明示本地命令的结果由 CWD 决定，以及封装脚本需要接收、验证目标项目目录，并用子 shell 保持调用端 CWD。
- `C` 必须明示原生路径参数，后续脚本不得用自行 `cd` 覆盖它。
- `D` 必须同时记录 global/project 两分支和**官方默认**，不能默认假设 local。

---

## Part 3 专项要求（使用示例）

此部分用于快速理解库的主要用法，不承担完整教程职责。

- 保留最小可运行示例，优先选择官方 README 的第一条主路径
- 可添加简短注释说明“这条命令 / 代码在做什么”和“成功后应看到什么”
- 注释必须服务于快速理解，不展开背景、原理或多场景教程
- 若库有复杂的安装后工作流，由可选 `ost-usage-examples` Skill 生成 `usage_examples.md`

## 编写原则

**快速原则（Parts 1~4）**

- 只保留能让人**立即读懂、立即操作**的核心内容
- 不展开细节；细节用链接指向原库
- 每条内容对应一个可执行动作或可判断的事实

**补充增强原则（Part 5）**

- 与前 4 部分用 `---` 分隔线显式隔开
- 每个条目只写关键结论或操作要点
- 细节给出原库链接，不复制大段原文

## Quality Checklist

完成后对照检查：

- [ ] Part 1：一句话能说清楚这个库是干什么的
- [ ] Part 2：所有官方安装方式均已列出，未因「推荐方式」省略其他
- [ ] Part 2：平台差异逐一分列（macOS / Linux / WSL / Windows），未用「同上」等省略
- [ ] Part 2：所有命令逐字照录官方文档，未改写或简化
- [ ] Part 2：前置依赖含具体版本号（官方有版本要求时）
- [ ] Part 2：更新命令独立列出，未与安装命令合并
- [ ] Part 2：多步骤安装已分步标注，步骤边界清晰
- [ ] Part 2：已包含安装作用域与目标目录表，分类为 A/B/C/D 之一
- [ ] Part 2：已记录官方默认、目标目录／CWD 或原生路径参数，以及可点击的一手证据链接
- [ ] Part 2：双模式库同时说明 global/project 分支，且未把项目本地模式误写为全局默认
- [ ] Part 3：示例代码最小化，可直接运行
- [ ] Part 3：示例包含有限理解性注释，能说明用途或预期结果
- [ ] Part 3：没有扩展成多场景教程；详细用例留给可选 `usage_examples.md`
- [ ] Part 4：注意事项都是实际存在的限制，无泛泛描述
- [ ] Part 5：安装相关深度内容（CI、非交互式安装、手动安装、高级配置、卸载）均给出原文链接
- [ ] Part 5：没有大段复制原文
- [ ] 全文没有「详情请查阅官方文档」类无效表述（要么给具体链接，要么不写）
