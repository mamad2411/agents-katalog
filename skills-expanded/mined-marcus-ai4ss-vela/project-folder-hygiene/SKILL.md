---
name: project-folder-hygiene
description: Use when the user asks to clean, organize, audit, hand off, archive, or close a project folder, or before finishing substantial file-generating work, to classify temporary files, dead files, duplicate drafts, stale outputs, and misplaced artifacts while preserving source, evidence, data, logs, and user-owned materials.
---

# Project Folder Hygiene

把项目文件夹整理成“别人接手也能看懂、后续线程继续也不会迷路”的状态。

## Canonical Project Structure

所有项目默认遵守本地项目目录合同：`skills/catalog/project_folder_contract.json`。这不是装饰性目录图，而是整理、初始化、下载、子智能体输出和复盘共用的分区规则。

通用结构：

```text
<project-root>/
├── README.md
├── AGENTS.md
├── .gitignore
├── research-map.md
├── findings-memory.md
├── material-passport.yaml
├── evidence-ledger.yaml
├── .codex/
│   ├── agents/
│   ├── dispatch/
│   ├── context-packets/
│   ├── rules/
│   ├── prompts/
│   └── templates/
├── materials/
├── references/ or literature/
├── data/
├── analysis/ or scripts/
├── outputs/
│   ├── agent-runs/
│   ├── inbox/
│   ├── reports/
│   ├── drafts/
│   ├── figures/
│   ├── tables/
│   └── exports/
├── logs/
│   ├── agent-handoffs/
│   ├── quality-gates/
│   ├── project-state/
│   └── runs/
├── memory/
├── tasks/
└── archive/
```

简单理解：

- 根目录只放项目入口、项目规则和核心台账。
- `.codex/` 放项目自己的 agent、任务卡、提示词和模板。
- `materials/`、`references/`、`literature/` 放材料和文献。
- `data/`、`analysis/`、`scripts/` 放数据和可复现处理过程。
- `outputs/` 放生成物、下载物、草稿、图表和导出包。
- `logs/` 放状态、质量检查、交接和运行记录。
- `memory/` 和 `tasks/` 放长期决策、经验和任务状态。
- `archive/` 放要保留但不再活跃的旧材料。

旧项目缺少基础结构时，先补项目合同：

```powershell
python -m skills.scripts.envctl ensure-project-contract --path "<project_root>"
python -m skills.scripts.envctl validate project-folder-contract --project-root "<project_root>" --summary
```

## Use When

- 用户说清理、整理、归档、收尾、交接、项目文件夹太乱、删除临时文件、检查死文件、检查无用目录。
- 一个线程生成了较多报告、截图、草稿、测试产物、下载物或中间文件，准备结束前需要收束。
- 项目要进入复盘、送审包、复现包、Obsidian 同步或长期维护前，需要确认目录结构干净。

## Do Not Use When

- 用户只是问一个概念、读一小段代码、或做单步命令。
- 目标根目录不清楚，且无法从当前仓库或项目上下文可靠判断。
- 清理对象包含未确认的个人资料、Zotero 库、Obsidian vault、浏览器配置、`.codex/skills/private-skill-workspace`，或仓库外路径。

## Required Inputs

- `project_root`：要整理的项目根目录。
- `purpose`：本次整理是交接、收尾、继续开发、投稿、复现、还是普通清理。
- `write_permission`：是否允许移动或删除文件。没有明确允许时只输出候选清单。

## Classification

先分类，再行动：

1. `keep_source`：tracked source、docs、schemas、scripts、templates、tests、configs、README、AGENTS、项目合同。
2. `keep_evidence`：原始数据、用户提供材料、PDF、截图证据、Zotero/Obsidian 导出、evidence ledger、material passport、质量门日志。
3. `keep_deliverable`：最终报告、正式图表、投稿包、复现包、已确认的输出。
4. `review_needed`：含义不明的数据、手工草稿、notebook、旧报告、重复版本、可能仍被引用的中间产物。
5. `safe_remove_candidate`：缓存、临时文件、空目录、失败测试残留、重复 scratch 导出、`__pycache__`、`.pytest_cache`、明显无引用的构建临时产物。
6. `move_or_archive_candidate`：有保留价值但位置错误、命名混乱、需要放入 `archive/`、`outputs/`、`logs/` 或项目约定目录的材料。

## Workflow

1. 确认 `project_root`，把所有候选路径解析成绝对路径；递归删除或移动前必须确认路径仍在 `project_root` 内。
2. 先看 Git 状态：`git status --short --branch`。没有 Git 时说明“非 Git 项目”，再用文件清单继续。
3. 用 `rg --files` 或等价命令盘点文件；排除 `.git`、`.venv`、`node_modules`、`.codegraph` 等大缓存目录，除非本次目标就是检查它们。
4. 找空目录、明显临时文件、重复草稿、失败输出、过期中间产物和孤立文件。
5. 对照 `project_folder_contract.json` 判断错位文件应该去哪里：根目录临时文件进入 `outputs/`，长期材料进入 `materials/` 或 `references/`，状态和检查进入 `logs/`，决策进入 `memory/`。
6. 对 tracked 文件、用户材料、证据文件、PDF、notebook、数据、Zotero/Obsidian 文件、日志和正式交付物，只能列为保留或待确认；不得静默删除。
7. 如允许执行清理，只处理 `safe_remove_candidate`；`review_needed` 和 `move_or_archive_candidate` 先向用户报告并等待确认。
8. 清理后重新运行文件清单、Git 状态和项目目录合同校验，确认没有无意改动。
9. 输出整理报告，写清楚：保留了什么、删除了什么、移动了什么、哪些需要用户决定、剩余风险、后续目录建议。

## Subagent Pattern

项目较大或文件类型多时，优先拆给子 agent：

- `inventory agent`：只做文件盘点和重复/临时候选识别，不写文件。
- `evidence guard agent`：检查哪些文件可能是证据、数据、PDF、日志、用户材料，防止误删。
- `structure reviewer agent`：提出目录结构和命名收束建议。

每个子 agent 必须返回候选清单、证据、风险等级和建议动作。主 agent 负责最终合并、询问用户、执行清理和复验。

## Safety Rules

- 不清理未确认的仓库外路径。
- 不删除 tracked 文件，除非用户明确点名。
- 不删除用户提供的原始材料、PDF、数据、Zotero/Obsidian 内容、质量门日志或项目合同。
- 不把“看起来没用”当成删除理由；必须有缓存、临时、重复、失败残留、空目录或明确失效证据。
- Windows 下递归删除必须使用同一个 shell 完成路径校验和删除，不拼接跨 shell 删除命令。

## Output

```markdown
# Project Folder Hygiene Report

## Scope
## Current Git State
## Keep
## Safe Removed
## Moved Or Archived
## Needs User Decision
## Remaining Risks
## Verification
## Suggested Next Structure
```
