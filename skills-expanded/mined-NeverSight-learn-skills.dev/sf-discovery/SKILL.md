---
name: sf-discovery
description: 对新请求执行深度探索、缺陷根因分析或预研；用于 brief 不足以支撑后续 artifact，或 ready artifact 为 gap_report / research 时。
---

# sf-discovery

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

把原始诉求升级为有分析证据支撑的 brief，或生成 bugfix 的 `gap_report`、discovery workflow 的 `research`。如果分析发现缺的是用户取舍而不是事实证据，暂停并向用户提问。它不写业务实现代码。

## 启动

1. 读取 `.specforge/AGENTS.md`。
2. 读取 `.specforge/registry.yaml`，确认当前 active work item。
3. 读取 `00-intake/original-request.md` 和已有 `brief.md`（如存在）。
4. 运行 `node .specforge/core/scripts/doctor.mjs`。
5. 运行 `node .specforge/core/scripts/instructions.mjs` 判断当前 ready artifact。

## 内部技能母本

开始 discovery 前，读取 `.specforge/core/workflows/stages/discovery/SKILL.md`。brief 的必含内容、停止条件和完成标准以内置母本为准。

## 关联标准

- `.specforge/core/standards/workflow.md`：上下文加载、scope、非目标和写入边界。
- `.specforge/core/standards/product.md`：分析深度、代码探索、外部研究、候选功能、用户选择和澄清。
- `.specforge/core/skills/ORCHESTRATION.md`：第三方研究参考的选择、来源核验和归一化要求。

## 第三方 Skill 联动

需要跨来源综合、引用编号、来源可信度标注、共识 / 争议拆解或研究空白整理时，按需读取 `.specforge/core/skills/research/deep-research/SKILL.md`。

- `deep-research` 只提供研究组织方法；当前事实、法规、版本、价格、新闻、漏洞和竞品状态必须另行查可靠来源。
- 研究结论必须写入 `01-spec/research.md` 或 `00-intake/brief.md`，并保留来源、日期、可信度和未解决问题。

## 动作

1. 按 `.specforge/core/standards/product.md` 判断分析深度：`light`、`standard` 或 `deep`。
2. 按深度执行代码库探索；绿地项目也要记录"无既有实现"和项目规范。
3. 需要新框架、第三方库或版本敏感事实时执行外部官方资料研究；不触发时写明跳过理由。
4. 对产品、页面、全栈应用，如果缺少 MVP / 方向取舍，暂停并向用户提问；如果只是补充事实证据，生成候选功能池，按 `MVP / 可选增强 / 后续版本` 分组并给出推荐组合，再向用户澄清并记录答案。
5. 如果 ready artifact 是 `gap_report`，运行 `node .specforge/core/scripts/create-artifact.mjs gap_report`，并写清复现、当前行为、期望行为、根因、修复策略和回归测试。
6. 如果 ready artifact 是 `research`，运行 `node .specforge/core/scripts/create-artifact.mjs research`，并写清研究问题、来源、实验、发现、决策和未解决问题。
7. 其他 discovery 场景更新 `00-intake/brief.md`。

## 停止条件

- 请求边界无法判断。
- 产品 / 页面 / 全栈应用的 MVP 功能组合尚未被用户确认，且复杂度超过简单小改。
- 需要用户在多个方案中做取舍，但尚未完成 `sf-brainstorm`。
- `standard` / `deep` 缺少代码库探索证据或明确跳过原因。
- `deep` 缺少外部研究证据或明确跳过原因。
- 涉及生产、安全、权限或数据风险但缺少关键事实。

## 完成标准

- `brief.md` / `gap-report.md` / `research.md` 包含足以支撑下一步的分析证据。

## 不做

- 不写 requirements 或 design。
- 不实现任何代码。
- 不把未确认选项伪装成已确认需求。
