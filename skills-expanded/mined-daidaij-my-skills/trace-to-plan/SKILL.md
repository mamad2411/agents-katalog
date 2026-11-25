---
name: trace-to-plan
description: 排查存量系统的缺陷与性能瓶颈：从现象描述、trace 日志、metrics 指标与项目代码多边信号中交叉验证定位根因，按 ROI 做修/不修决策，产出低风险优先的排序实施计划，并经 bench 验证闭环。多轮调查通过 .issue/ 线索链与 index.md 索引摘要接力推进。Use when user says "排查性能问题", "系统变慢了", "找瓶颈", "性能体检", "优化哪里", "perf investigation", "find bottlenecks", or reports slow/crashed/regressed behavior in an existing system.
description_zh: 排查存量系统缺陷与性能瓶颈：多边信号（现象/日志/指标/代码对照）交叉验证定位根因 → ROI 修/不修决策 → 低风险优先排序实施计划 → bench 验证闭环。调查状态沉淀在 .issue/ 目录（index.md 索引摘要 + 线索链），支持多轮接力、分段推进与跨分支重放修复包。触发场景："排查性能问题"、"系统变慢了"、"找瓶颈"、"性能体检"、"优化哪里"、报告现有系统慢/崩溃/回退。渐进式披露：按当前阶段按需加载 stage 指引（只给日志时不加载 bench）。
---

# Trace to Plan — 从痕迹到计划

**定位**：wayfinder 的反向。wayfinder 从目标自顶向下规划（空白工程，决策 tickets 地图 → 逐票解决）；本 skill 从现状自底向上发现（存量系统）——多边信号 → 收敛候选 → 验证决策 → 方案规划 → bench 闭环。

回答三个问题：

1. **哪里有坑** — 多源信号交叉收敛出高置信候选问题
2. **值不值得修** — ROI 决策，不是发现的问题都该修
3. **怎么修最顺** — 排序、依赖、验证方式齐备、贴合业务约束的实施计划

## 工作模式：多轮重入

性能与设计缺陷定位天然是多轮的：现象跨天出现、日志分批拿到、指标等待观测窗口。以**轮次（session）**推进，状态沉淀到 `.issue/` 目录，下轮恢复继续——不重来、不丢失。

- 每轮只做两件事：**追加线索**、**更新事实/推断**——绝不重写历史
- 状态机：`open → investigating → decided → implementing → verified → closed`
- 接续成本 = 只读 `index.md`（索引摘要），详细文件按需加载

## 阶段路由（渐进式披露）

**只加载当前阶段需要的指引**——当前只有日志时，不加载 bench 指引。按 index.md 状态与已有线索路由：

| 现状 | 加载 | 本轮目标 |
|------|------|---------|
| 无 `.issue/` | [stage-0](./stage-0-collect.md) | 初始化目录，收集首轮信号 |
| `open`，线索不足 | [stage-0](./stage-0-collect.md) + [stage-1](./stage-1-converge.md) | 继续收集，逐线索代码对照 |
| 有线索，根因未收敛 | [stage-1](./stage-1-converge.md) | 交叉验证，根因逐步逼近 |
| 根因高置信 / 最终根因 | [stage-2](./stage-2-decide.md) | 验证 + 修/不修决策 + 排序 |
| `decided` | [stage-3](./stage-3-plan.md) | 方案规划 + 可重放修复包 |
| `implementing` / `verified` | [stage-4](./stage-4-bench.md) | bench 闭环验证 |

换阶段时更新 index.md 状态，再进入下一阶段指引。

## 贯穿纪律（全阶段适用，浓缩）

1. **事实与推断分离** — 无证据编号的表述一律进 hypotheses；推断升事实必须经验证动作
2. **历史信息默认低可信** — 开发者口述只作待核实线索，经代码对照/复现核实才可升级
3. **根因渐进收敛** — 最终根因三重确认（多源独立信号 + 代码对照吻合 + 无矛盾反馈）；结论可推翻，历史不可改
4. **线索只追加** — 矛盾修正以新线索记录，不修改旧线索
5. **决策先于方案** — 根因未收敛不得决策；未决策不写方案

详细约定（.issue/ 目录结构、index.md 格式、分段保留）见 [references/issue-layout.md](./references/issue-layout.md)；交接与跨分支重放协议见 [references/handoff.md](./references/handoff.md)。

## 入口协议

1. 读 `.issue/index.md`（无则初始化目录，状态 `open`）
2. 按路由表加载当前阶段指引
3. 执行该阶段 → 追加线索 / 更新状态 → 更新 index.md → 结束本轮

## 协作关系

```
trace-to-plan（发现+决策，.issue/ 重入）
   ├─ diagnosing-bugs  阶段 2 单点深挖（红绿反馈循环）
   ├─ codegraph / grep  阶段 1 代码对照（实现验证）
   ├─ sdd-spec / sdd-implement  实施计划下游（spec + 逐票实现）
   ├─ code-review  变更后双轴验证（Standards + Spec）
   └─ grill-me  方案评审（可选，兼维护领域模型文档）
```
