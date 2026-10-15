---
name: sf-wiki
description: 更新 SpecForge 项目 Wiki；用于用户要求“回写知识库、更新 wiki、同步 Wiki”，或 close 前需要把 work item 的长期事实沉淀到 .specforge/wiki/*.md 时。
---

# sf-wiki

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

`sf-wiki` 维护项目当前长期事实，不复制 work item 过程流水账。Wiki 是项目记忆，也是后续任务的入口地图，不是 implementation report、verification report 或 release note 的第二份副本。

如果用户目标是“先理解整个存量项目 / 建立项目画像 / 扫描大型代码库”，优先路由 `sf-steering`。`sf-wiki` 负责把已确认事实或完成 work item 的结论同步成当前 wiki。

## 必读

- `references/wiki-sync-rules.md`：回写判断、目标文件选择、frontmatter、index 对账、gate 决策。
- `.specforge/core/workflows/stages/wiki-sync/SKILL.md`
- `.specforge/core/artifacts/templates/wiki-sync.md`
- `.specforge/core/standards/wiki.md`
- `.specforge/core/standards/workflow.md`
- `.specforge/core/standards/engineering.md`
- 涉及设计系统或 PC 端业务系统规范时读取 `.specforge/core/standards/design.md` 和 `.specforge/core/standards/pc-ui-design-spec.md`。
- 涉及第三方 skill 长期事实时读取 `.specforge/core/skills/ORCHESTRATION.md`，只沉淀已被 SpecForge artifact 证实的稳定内容。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/instructions.mjs
```

2. 如果 ready artifact 是 `wiki_sync`，生成 evidence：

```bash
node .specforge/core/scripts/create-artifact.mjs wiki_sync
```

3. 如果 `.specforge/wiki/` 缺少基础文件，先补齐：

```bash
node .specforge/core/scripts/sync-wiki.mjs
```

4. 若当前没有 active work item，但用户明确要求更新 wiki，可进入 Lightweight wiki 更新；必须写清来源证据，不能凭口头印象改当前事实。

## 执行序列

### A. 收集来源

优先读取 active work 的最终产物：

- `00-intake/brief.md`
- `00-intake/prd.md`（存在时）
- `01-spec/requirements.md`
- `01-spec/gap-report.md`（存在时）
- `01-spec/ui-design.md`（存在时）
- `01-spec/technical-design.md`（存在时）
- `00-steering/codebase-intelligence.md`（存在时）
- `02-spec-review/spec-review-v1.md`（存在时）
- `03-implementation/report.md`
- `04-code-review/code-review-v1.md`
- `05-verification/report.md`
- `06-close/release.md` / `rollback.md`（存在时）

### B. 判断是否回写

1. 提取候选长期事实。
2. 按 `references/wiki-sync-rules.md#回写矩阵` 判断目标文件。
3. 只影响一次性实现、临时日志、测试输出、截图或局部无复用备注时，在 `06-close/wiki-sync.md` 写 N/A 理由，不更新 wiki。
4. 改变长期产品、架构、接口、数据、运行、设计系统、术语、风险时，必须更新对应 wiki 文件。

### C. 更新 wiki

1. 优先更新现有 current 文件，不创建日期版、v2 版、work item 版。
2. 确需新增时使用短名：`module-<name>.md`、`api-<domain>.md`、`design-system.md`。
3. 每个更新文件都保留并刷新 frontmatter：`title`、`kind`、`owner`、`last_updated`、`source_work`、`status`。
4. 按 `references/wiki-sync-rules.md#Wiki 质量清单` 检查信息密度；架构、模块、API、数据、运维类文件不能只写概述，还要能支持后续任务从 wiki 入手定位代码。
5. 对缺失事实执行一次补证：用 `rg` / provider / 关键配置读取查找路由、模型、migration、服务入口、脚本和测试。仍无法确认的，写 `未确认` 并同步到 `08-risks.md`。
6. 更新 `.specforge/wiki/00-index.md` 的摘要、当前文件索引和最后同步时间。
7. 在 `06-close/wiki-sync.md` 记录更新文件、写入事实、来源证据、不更新原因、未确认缺口和下游重新验证要求。

### D. 更新 gate

批准：

```bash
node .specforge/core/scripts/gate.mjs wiki_sync APPROVED --evidence 06-close/wiki-sync.md
```

缺少事实证据或冲突未解决：

```bash
node .specforge/core/scripts/gate.mjs wiki_sync REQUEST_CHANGES
```

## 判定表

| 条件 | 状态 |
|---|---|
| verification 未批准，且处于 close 前 wiki_sync | 停止，回 `sf-verify` |
| 只是一次性过程记录、日志、截图、临时调试 | 不更新 wiki，写 N/A 理由 |
| 长期产品 / 架构 / API / 数据 / 运行 / 设计系统 / 风险变化 | 更新对应 wiki |
| artifact 与现有 wiki 冲突且无法判断最新事实 | `REQUEST_CHANGES` |
| 会产生重复 current 文件 | 停止，合并到唯一目标文件 |

## 完成标准

- `06-close/wiki-sync.md` 写明影响或不影响。
- 更新的 wiki 文件 frontmatter 完整，`status: current` 正确。
- 同一知识项只有一个 current 文件。
- `.specforge/wiki/00-index.md` 反映最新 current 文件列表。
- wiki 只包含当前事实；旧事实被更新，必要背景进入 `06-decisions.md`。
- 架构 / API / 数据 / 运维文件满足最低完整度；不足项已明确标注 `未确认`，并在 `08-risks.md` 或 `06-close/wiki-sync.md` 记录补证路径。
- 架构 / 模块 / API / 数据 / 运维文件包含后续任务可用的入口路径、关键符号 / 路由、上游下游、测试位置、运行命令或推荐检索词。
- wiki_sync gate 状态与 evidence 一致。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不把临时日志、测试输出、截图或实现流水账复制进 wiki。
- 不创建按日期、版本号或 work item 命名的 wiki 文件。
- 不用 wiki 替代 work item evidence。
- 不把第三方 skill 的模板、persona 或建议当成项目事实；只有经 SpecForge artifact 确认后才可沉淀。
