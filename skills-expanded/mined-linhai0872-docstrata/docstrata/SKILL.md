---
name: docstrata
description: "Project Context System — structured project memory for any project via layered docs and codebase index. Use for: documenting projects, writing PRD/roadmap, generating codebase repo-wiki, capturing requirements/decisions, writing dev notes, building doc navigation index, compacting bloated docs, auto-detecting stale docs after development, setting up project context for coding agents."
---

# docstrata — Project Context System

按知识性质分层，为任意项目生成/维护文档与代码库索引。定位：**项目的结构化记忆系统**——管理和提供高杠杆 context，不指挥具体执行。与工程执行 skill（如 Matt Pocock skills）兼容协作，零重叠。

wiki / repo-wiki / requirements / knowledge / dev 五层对应 CoALA 长期记忆三类（Semantic / Episodic / Procedural）。`prd` 在这之上，记前瞻产品意图，不属 CoALA 记忆。每层是一个子命令，共享同一套执行循环。`compact` 是横切收缩操作，把膨胀的层文档收回有界状态。

## 子命令路由

| 命令 | 层 / 类型 | 产出 | 何时用 |
|---|---|---|---|
| `prd` | 产品主张（前瞻 intent） | `docs/prd.md` | 固化对内的产品定位/价值/功能范围/roadmap |
| `requirements` | Episodic | `docs/requirements.md` | 还原/固化需求共识与开发计划 |
| `knowledge` | Semantic | `docs/knowledge/knowledge.md` | 整理业务原始材料为可检索索引 |
| `wiki` | Semantic | `docs/wiki.md` | 让所有人（含业务）快速理解整个系统 |
| `repo-wiki` | Semantic（代码缓存） | `docs/repo-wiki.md` | 代码库索引：架构/模块/技术栈/数据流，给 coding agent 用 |
| `dev` | Procedural | `docs/dev.md` | 记录开发推断与实践结论 |
| `index` | 检索入口 | `docs/INDEX.md` | 生成给 coding agent 的文档导航索引 + context triggers |
| `compact` | 横切操作 | 收缩已有层文档 | 层文档随迭代膨胀，手动收回有界状态 |
| `update` | 横切操作 | 检测变更 → 刷新受影响的层 | 开发后同步文档、定期检查过期 |
| `all` | 全部 | 六层 + index | 按依赖顺序一次生成 |

用户说具体层（“生成 wiki”/“还原需求”/“生成 repo-wiki”）→ 走对应层。说“全部文档” → `all`。说“compact/收缩/精简” → `compact`（可带层名，如 `/docstrata compact dev`）。说“更新/刷新/同步/update” → `update`。不明确则问用户要哪一层。

`all` 的依赖顺序：`prd` → `requirements` → `knowledge` → [`wiki`, `repo-wiki`] → `dev` → `index`。`wiki` 与 `repo-wiki` 平行（互不依赖，可并行生成）。`prd` 是最上游意图源头，`index` 是最下游派生层。跑单层时不强制先跑上游；上游文档已存在则读取引用。

`index` 详见 [references/layer-index.md](references/layer-index.md)。纯派生，不走五步循环，但遵循增量更新与 STAMP。

`compact` 详见 [references/compact.md](references/compact.md)。先压（丢可复原项 + 去重 + 按主题归并）、再拆、归档不删。手动触发，不自动跑。

`update` 详见 [references/update.md](references/update.md)。检测变更信号 → 影响面映射 → 报告 → 刷新受影响的层。支持 `--auto` 自动模式。

`all` 不强制每层都产出。无实质价值的层按 [methodology.md](references/methodology.md) 的优雅降级跳过，汇报里说明原因。宁可少而实，勿多而空。

生成完毕后输出信息健康诊断副产物（冲突/过期/缺口），见 [references/audit-report.md](references/audit-report.md)。

## 执行循环（所有层通用）

每层走这五步。**方法论细节见 [references/methodology.md](references/methodology.md)，执行前务必先读。**

1. **EXPLORE** — 读现有 `docs/` 层文档、README、代码结构、配置。识别项目类型，用对应探索策略。**主动解决 facts**：agent 能查到的缺口（技术栈、文件结构、依赖关系）在此阶段自行解决，不留给 GRILL。repo-wiki 层的 EXPLORE 调用 `scripts/scan-codebase.py` 输出的结构化 JSON。
2. **MAP** — 把探索结果映射到本层 **completeness contract**（见各层 reference），给每个维度打置信度（high/medium/low/missing）。
3. **GRILL** — 仅对 low/missing 维度中**需要人类拍板的 decisions** 提问。默认用 frontier 轮次（每轮问出所有前置条件已满足的问题），可配置为一次一个。附推荐答案。维度全达标则跳过。遇设计假设需验证时可发起 prototype（spike）。
4. **GENERATE** — 按本层固定骨架生成。已存在则**增量更新**：diff 现有内容，只重写有实质变化的段落，保留人类手改。产出文档遵循 [writing-for-agents 质量标准](references/methodology.md#generate质量标准)。
5. **STAMP** — 更新 `last-verified` 日期与变更摘要。

## 各层契约与骨架（按需加载）

执行某层时，读取对应 reference 获取 completeness contract 和 section 骨架：

- prd → [references/layer-prd.md](references/layer-prd.md)
- requirements → [references/layer-requirements.md](references/layer-requirements.md)
- knowledge → [references/layer-knowledge.md](references/layer-knowledge.md)
- wiki → [references/layer-wiki.md](references/layer-wiki.md)
- repo-wiki → [references/layer-repo-wiki.md](references/layer-repo-wiki.md)（代码库索引，EXPLORE 依赖扫描脚本）
- dev → [references/layer-dev.md](references/layer-dev.md)
- index → [references/layer-index.md](references/layer-index.md)（纯派生 + context triggers）

执行收缩时：

- compact → [references/compact.md](references/compact.md)（横切操作，不是生成层）

## 横切方法论

- [references/source-criticism.md](references/source-criticism.md)：来源可信度排序、矛盾处理、事实 vs 推断标注、打破 LLM 先验偏向。
- [references/doc-conventions.md](references/doc-conventions.md)：写作规范，含两段式、向上指针、anti-slop 约束、时间戳。
