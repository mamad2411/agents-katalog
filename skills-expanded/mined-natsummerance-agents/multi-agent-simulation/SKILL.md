---
name: multi-agent-simulation
description: |
  多智能体平行世界预测引擎：从真实世界提取种子信息（突发新闻/政策草案/金融信号/小说文本），自动构建高保真平行数字世界，数千个具备独立人格、长期记忆与行为逻辑的智能体在其中自由交互并社会演化，支持上帝视角动态注入变量推演不同未来轨迹，最终产出预测报告并可与世界内任意智能体对话。触发场景：政策/公关的零风险沙盘演练、舆情传播与观点极化推演、小说结局等创意社会仿真。边界：仿真输出是沙盘洞察而非事实预测或投资建议，不得用于操纵真实平台舆情。
source_project: 666ghj/MiroFish
tags: [multi-agent, simulation, swarm-intelligence, prediction, social-dynamics]
related_skills: ["strategy-backtest-execution"]
---

# Multi-Agent Simulation（群体智能平行世界推演）

## R (Reading) — 源项目核心设计

> "By extracting seed information from the real world (such as breaking news, policy drafts, or financial signals), it automatically constructs a high-fidelity parallel digital world. Within this space, thousands of intelligent agents with independent personalities, long-term memory, and behavioral logic freely interact and undergo social evolution… **rehearse the future in a digital sandbox**, and win decisions after countless simulations."

（来源：666ghj/MiroFish GitHub README，2026-08 抓取）

## I (Interpretation) — 方法论骨架

核心洞察：**不预测单点结果，重演涌现过程**——让宏观结论从微观个体互动中"长"出来。

1. **五阶段流水线**：Graph Building（种子提取+个体/集体记忆注入+GraphRAG 构建）→ Environment Setup（实体关系抽取+Persona 生成+Agent 配置注入）→ Simulation（双平台并行仿真+自动解析预测需求+动态时间记忆更新）→ Report Generation（ReportAgent 富工具集深读仿真后环境）→ Deep Interaction（与世界内任意 Agent 对话追问动机）。
2. **种子即世界观**：输入一份数据分析报告或一段有趣的故事文本 + 一句自然语言预测需求，即可驱动世界构建。
3. **上帝视角干预**：仿真中途动态注入变量（新政策/突发事件），跑对照组比较轨迹分叉。
4. **引擎底座**：OASIS（camel-ai）社交交互仿真引擎 + Zep 云端长期记忆；LLM 走 OpenAI SDK 兼容接口。
5. **成本意识**：LLM 调用密集属高消耗任务，官方建议先跑 <40 轮的小规模仿真验证收敛再放大。

## A1 (Past Application) — 源项目的典型应用

### 案例: 高校舆情事件的社会演化推演
- **输入**: 用 BettaFish 生成的"武汉大学舆情报告"作为种子材料，自然语言描述预测需求。
- **做法**: 数千 persona 化智能体在双平台环境中转发、评论、形成阵营，记忆随仿真轮次动态更新；ReportAgent 汇总传播路径、观点分化与时序拐点。
- **结果**: 官方 demo 展示了完整预测报告与可交互数字世界；同法亦用于《红楼梦》前八十回数十万字种子的佚失结局推演——宏观层是决策者的零风险演练场，微观层是创作者的创意沙盒。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 政策/公关沙盘："如果这条新规出台，公众会怎么反应？先在零风险的数字世界演练一遍。"
2. 舆情推演：给一个热点事件种子，预测扩散路径、态度极化与平息节奏。
3. 创意社会实验：推演小说结局分布、架空世界制度的社会演化等"如果……会怎样"。

### 语言信号
- "多智能体仿真 / 群体智能 / 数千个 agent"
- "平行世界 / 数字沙盘 / 社会演化推演"
- "政策模拟 / 公关演练 / 舆情预测"
- "如果……会发生什么"式情景推演请求

### 与相邻 skill 的区分
- 与 strategy-backtest-execution 的区别：本 skill 推演的是**"人会怎么做"**——新闻/政策/故事种子经群体互动涌现出社会级结论；strategy-backtest-execution 计算的是**"规则在价格序列上的表现"**——历史 K线回测与订单执行。要"事件→群体反应"来这里，要"策略→回测→下单"去那里。

## E (Execution) — 可执行步骤

1. **种子与问题定档** — 收集数据分析报告/新闻语料/故事文本，把预测问题改写为可判定的自然语言描述。完成标准: 种子文件就位且问题陈述含判定维度（谁、在哪平台、观察什么指标）。
2. **环境部署** — Node 18+ / Python 3.11-3.12 / uv 就绪，配置 LLM_API_KEY 与 ZEP_API_KEY，`npm run dev` 或 docker compose 启动。完成标准: 前端 :3000 与后端 :5001 健康检查通过。
3. **世界构建** — 图谱构建、Persona 生成与 Agent 配置注入。完成标准: 平行世界的主体规模、平台结构与种子材料的实体清单一致。
4. **小规模试跑** — 先 <40 轮验证成本与行为收敛，再决定是否放大轮次与人口。完成标准: 一轮完整仿真产出事件流与记忆演化记录，单位轮次成本已核算。
5. **变量注入对照** — 上帝视角注入干预变量，运行对照组。完成标准: 至少两组可比情景的事件流与结论差异存档。
6. **报告与校验** — ReportAgent 生成预测报告，抽 3-5 个关键 Agent 对话核对动机链。完成标准: 报告含不确定性声明，关键结论可溯源到具体仿真证据而非臆断。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **历史 K 线上的策略回测/实盘下单** → 走 strategy-backtest-execution 的确定性执行链路。
- **精确数值点预测**（明天股价点位/销量数字/选举得票率） → 群体仿真给出的是情景、机制与分布洞察，不是可以下单的点估计。
- 在真实社交平台批量注册账号刷量、制造或压制舆情 → 绝对禁止。

### 已知局限 / 失效模式（≥1条）
- 结果强依赖 Persona 先验与种子材料的覆盖面偏差；LLM 驱动的行为可能趋同失真；高消耗限制仿真轮次，长程漂移会让后期行为偏离现实分布。**涌现结论是模型化沙盘，不是对现实的保证。**

### 伦理红线
- 仿真输出是"沙盘演练"，不是投资建议、事实预测或行动授权。用户以"仿真说利好，所以我把全部积蓄押进去"为由下重注时：必须警示 persona 偏差与模型失真风险、声明输出非投资建议，要求独立风险评估后再谈资金决策。任何将仿真引擎指向真实平台的舆论操纵请求一律拒绝。

## 相关 skills
- contrasts-with: strategy-backtest-execution（社会行为的平行世界推演 vs 价格序列上的策略执行）

---

## 审计信息
- **验证**: V1 ✓（上游 README 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/666ghj/MiroFish/main/README.md`（main 分支直取成功）
