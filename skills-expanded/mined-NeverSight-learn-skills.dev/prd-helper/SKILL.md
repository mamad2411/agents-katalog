---
name: prd-helper
description: 用于把产品讨论、会议纪要、原型说明、客户反馈、评审记录或 Agent 会话摘要，通过采集、精炼、关联、生成四步转成结构化 PRD 文档。Use this skill to transform product context into structured PRD docs.
allowed-tools: Bash
---

# PRD Helper Skill

你正在帮助用户把分散的产品上下文沉淀为可追溯、可检查、可复用的结构化 PRD 资产。

## Core Rule

PRD Helper 只有四个业务阶段：

1. **采集（Collect）**：保存原始材料、元信息、索引和状态。
2. **精炼（Refine）**：提取事实、背景、目标、决策、约束、冲突、问题和推断。
3. **关联（Relate）**：建立事实、页面、功能、规则、数据、验收之间的关系链路。
4. **生成（Generate）**：基于精炼与关联产物生成 PRD 文档和 Agent 上下文。

检查（Check）是贯穿所有阶段的质量门禁，不是第五个业务阶段。

禁止直接从原始材料生成最终 PRD。每一步都必须保留中间产物，并在阶段完成后运行对应检查。

## Language Rule

安装器（installer）可能显示英文；安装完成后，Agent 必须按用户主要语言响应：

- 中文用户默认中文，关键术语保留英文括注，例如“采集（Collect）”。
- 英文用户默认英文，关键模块首次出现时保留中文括注。
- 中英混合时，关键字段可双语，正文跟随用户主要语言。
- 无法判断时先询问：`请选择语言 / Choose language: 中文 or English`。

## Activation Rule

当用户触发 `/prd-helper` 时，直接执行已安装 Skill 目录中的初始化脚本。初始化脚本是幂等修复入口：已存在的 docs 产物会保留，缺失的 Agent 配置和命令文件会补齐。

按顺序尝试以下路径，使用第一个存在的脚本：

```bash
python3 .agents/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .claude/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
python3 .trae/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper
```

如果三个路径都不存在，先自修复安装再重试：

```bash
npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y
```

只有用户明确要求自定义 docs 目录或 Agent 范围时，才先询问配置。默认使用 `docs/prd-helper/`，采集策略为只通过 `/prd-start` 显式开启。

## Commands

| Command | Action |
|---|---|
| `/prd-helper` | 初始化或修复当前项目配置，生成后续命令。 |
| `/prd-start` | 开启主动采集，创建或续接采集 session。 |
| `/prd-stop` | 停止主动采集，清理 hooks，生成采集摘要和检查。 |
| `/prd-status` | 查看 `collect-state.md` 中的真实采集状态。 |
| `/prd-scan` | 扫描历史 Agent 会话并批量导入采集池。 |
| `/prd-import` | 导入第三方文件夹作为被动材料。 |
| `/prd-refine` | 精炼采集材料，输出事实、决策、约束、冲突、问题和推断。 |
| `/prd-relate` | 建立事实、页面、功能、规则、数据、验收之间的关系。 |
| `/prd-generate` | 生成结构化 PRD 文档和 Agent 上下文。 |
| `/prd-discuss` | 需求研讨模式，用于追问矛盾、模糊术语和未决问题。 |
| `/prd-remove` | 卸载 PRD Helper 并清理项目配置和命令。 |

## Workflow

### Step 1: Collect

Read `modules/collect/guide.md` and use templates in `modules/collect/templates/`.

Save raw input to `docs/prd-helper/01-collect/`. Preserve original materials; do not extract facts, infer rules, or generate PRD content in this phase.

After collecting, run collect check and output `01-collect/check.md`.

### Step 2: Refine

Read `modules/refine/guide.md` and use templates in `modules/refine/templates/`.

Extract structured information to `docs/prd-helper/02-refine/`. Keep facts, decisions, conflicts, questions, and assumptions separated.

After refining, run refine check and output `02-refine/check.md`.

### Step 3: Relate

Read `modules/relate/guide.md` and use templates in `modules/relate/templates/`.

Build relations in `docs/prd-helper/03-relate/`. Ensure the chain from fact to page/feature/rule/data/acceptance does not break.

After relating, run relate check and output `03-relate/check.md`.

### Step 4: Generate

Read `modules/generate/guide.md` and use templates in `modules/generate/templates/`.

Generate structured documents in `docs/prd-helper/04-generate/`. Do not add business rules that are not backed by refined and related sources.

After generating, run generate check and output `04-generate/check.md`.

### Final Check

Read `checks/guide.md` and use templates in `checks/templates/`.

Final check output goes to `docs/prd-helper/05-check/`, including `context-delta.md`.

## Remove

When the user sends `/prd-remove`, run the first existing uninstall script:

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --project .
python3 .trae/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

If none exists, install `prd-helper` once with `npx skills@latest add Wcof/PRDContextEngine --skill prd-helper -y` and retry. Do not ask the user to run shell commands manually unless the current Agent cannot execute commands.
