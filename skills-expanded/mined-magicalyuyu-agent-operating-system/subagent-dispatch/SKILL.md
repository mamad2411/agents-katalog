---
name: subagent-dispatch
description: "[治理] 决定是否/如何派发子代理时的决策表。触发条件：任务前判断自己做还是委派、用哪种委派形态。替代 v1 的 subagent-dispatch-rule 十条律。"
---

# 子代理调度决策表（v1 十条律压缩版）

## 是否委派

| 场景 | 判断 |
|---|---|
| 单文件简单修改、与用户澄清、意图不确定 | **不委派**，主会话直接做 |
| 大范围探索/审计、对抗性审查、上下文隔离型分析 | **必须委派**（上下文收益明确） |
| 其他 | 默认不委派；委派时一句话说明理由即可，无需逐条论证 |

## 用哪种形态

| 形态 | 适用 |
|---|---|
| `subagent`（spawn） | 自包含的独立任务，需完整 prompt（调研/审计/实现） |
| `subagent_fork`（fork） | 建立在本会话上下文上的后续分析/复审/红队 |
| `workflow` | 大规模 fan-out（多文件、多分片、pipeline）；脚本写编排逻辑 |
| `AgentTeams` | 需要任务 DAG、质量门（requirements→…→review）、多轮协作 |
| `goal` | 单一长目标的自动续跑（不是委派，是自驱） |

## 成本路由

适用前提：你有多档可用模型且成本差异显著。批量低推理分片（枚举/统计/文本整理/识图）在主动编排（workflow/AgentTeams 指令）中指定低成本批量模型 provider；推理与决策留主模型。各平台自身的调度决策与模型选择不归本约定管。

## 质量门禁默认化

行为不变量 1（对抗审查）的默认载体：**AgentTeams review kind**——attempt_id/verdict/findings 是运行时强制（verdict=needs_revision 自动触发 repair+review 循环，勿手工重建），比提示词约定硬（Spec Kit reviewer-owned checklist 同思想）。fork 红队保留给快速轻量场景。review 只对最新实现版本裁决。

## gotchas

- 红队审查用 fork（继承上下文）优于 spawn（要重述全部背景）
- workflow 的 agent() 返回 null = 该片失败，须 filter(Boolean) 并重试
- 子代理崩溃不传染父级；被中断的代理可用 send_message 续轮
- **廉价模型负向约束不稳**（实证×2）：低成本批量模型对"禁止创建清单外文件"遵守不稳（实测：瘦身任务擅自切碎片）、对含糊列项会自行发挥（实测：工具被误归档）——给低成本批量模型的任务必须：白名单式正向指令 + 产出后磁盘复核
- 廉价模型 manifest 可能虚报/漏报（扫描异常值、重复行），关键数字以主会话独立复核为准
- **workflow 子代理 prompt ≤1500 字**（会话数据分析：调研子代理单会话 100-127KB，prompt 占大头；goal 13 轮中 3 轮在干等子代理）——长背景拆成"先看 X 文件"的指令而非全量贴入
- **委派文件创建任务必须内联目标路径**（双轮盲测：子代理对 file-placement skill/内核不变量的自主遵守率仅 3/5，spawn 子代理尤其不稳）——prompt 里直接写"创建到 {标准路径}"，落位正确性不托付给子代理自觉；产出后跑 scripts/check_placement.py 兜底
