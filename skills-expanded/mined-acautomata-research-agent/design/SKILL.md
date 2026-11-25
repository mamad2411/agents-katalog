---
name: design
description: Design small, controllable validation experiments for a paper's identified problems (from critic's output). Triggers: 验证实验设计, design validation experiments, 设计验证实验.
---

# design — 验证实验设计

## Mission

将问题分析（`critic` 产出）中的潜在问题转化为小规模、可控、可执行的验证实验设计，产出完整 9 节 Markdown 文档（## 0–## 8）。

## When to use

- 已有 `critic` 问题分析，需要把问题转成可执行的验证实验
- 用户请求"设计验证实验""怎么验证这个 claim"

不要用于：问题分析（`critic`）、生成 claude-code 提示词（`spec`）。

## 前置依赖

需要 `critic` 的问题分析文档已存在（通常在 wiki 里）。若缺失，先运行 `critic`。

## 输入

| 材料 | 必需 |
|------|------|
| 论文基础 Wiki 文档 | 是 |
| `critic` 问题分析文档 | 是 |

## 参考：实验设计准则

> 这一节是设计实验时的参考规则（按需查阅），不是按顺序执行的步骤。

- 当前阶段是"验证实验设计"，不直接下最终结论、不提出新方法
- 每个实验必须服务于一个明确的 `critic` 问题
- 优先低成本、小规模、单变量或少变量控制实验
- 优先复用原论文框架、数据集、baseline 和实验设定
- 前序分析推断写明"当前属于合理怀疑，需实验确认"

**推荐实验类型**：小规模对照、消融、替换式、参数扫描、数据划分变化、memory budget 变化、任务顺序变化、图结构变化、异质度变化、训练策略控制、评测协议对照。

**每个实验必须明确**：验证哪个问题、为什么值得验证、问题类型、自变量和控制变量、如何操作与比较、观察哪些指标、问题成立/不成立分别可能出现什么现象、结果分别意味着什么、实验成本（低/中/高）、是否适合作为第一批实验。

## 输出结构

严格按 9 节输出为一份完整 md，先写到 `raw/sources/<slug>.md`，然后调用 `ingest`（传入该 md 文件路径，`page_type: analysis`）统一写入 wiki；**不直接调用 `wiki_apply` 建页**（在 `# Title` 下空一行加 `` `category: design` `` 作为可机读类别标识，供外部统计脚本提取）：

```markdown
# {{论文标题}}：验证实验设计

`category: design`

## 0. 文档定位
## 1. 验证目标总览（3–6 条）
## 2. 实验设计原则
## 3. 核心验证实验设计（3–6 个）
## 4. 可选补充实验（2–4 个）
## 5. 实验优先级排序
## 6. 最值得优先执行的 3 个实验
## 7. 这些实验可能支撑的后续研究方向
## 8. 简短总结（100–150 字）
```

## 完成门禁

- Reply 包含全部 9 节
- 每个实验映射到一个 `critic` 问题并有预期结果
- 产出 md 已经 `ingest` 写入 wiki（含 wiki 路径），且本 skill 未直接调 `wiki_apply` 建页
- 产出 md 在 `# Title` 下空一行包含 `` `category: design` ``（作为可机读类别标识，供外部统计脚本提取）
