---
name: strategy-backtest-execution
description: |
  交易想法→Python 策略代码→服务端历史回测→Paper Trading→实盘执行→监控的全链路自托管量化交易系统：Strategy API V2、多交易所/券商适配、Agent Gateway 与 MCP 接入、租约心跳式策略运行时与 Prometheus 可观测。触发场景：把交易假设写成可回测的策略代码、搭建自托管量化栈跑模拟盘、为已验证策略配置风控限额与告警后小仓实盘。边界：工程工具链而非投资咨询；所有输出非投资建议，回测存在过拟合风险，历史表现不代表未来。
source_project: OpenByteInc/QuantDinger
tags: [quant, backtest, paper-trading, live-execution, risk-control]
related_skills: ["multi-agent-simulation"]
---

# Strategy Backtest Execution（量化策略回测到执行全链路）

## R (Reading) — 源项目核心设计

> "Turn trading ideas into Python strategies, backtests, paper trading, live execution, and monitoring — all in one self-hosted stack." 且开篇警示："Start with paper trading, use restricted API keys… This project does not provide investment advice." 法务节重申："Historical data, backtests, simulated results, AI output, indicators, and strategy examples do not guarantee future performance. Trading… can result in the loss of some or all capital."

（来源：OpenByteInc/QuantDinger GitHub README，2026-08 抓取）

## I (Interpretation) — 方法论骨架

核心洞察：**进程边界即安全边界**——HTTP 不碰交易循环，长时运行归 worker，有限任务归队列。

1. **五段闭环**：AI 研究 → Strategy API V2 策略代码 → 服务端回测/实验 → Paper Trading → 实盘执行 → 监控复盘，每段产物可审计。
2. **进程拓扑**：migration 先行退出；backend 只做 HTTP 校验与持久化命令提交；trading-worker 以**租约+心跳+fencing token** 独占策略运行时与订单会话；Celery 只承接有限可重试任务（回测/AI/报表）；cache Redis 与 durable job Redis 分离。
3. **券商适配层**：CCXT 系加密交易所（Binance/OKX/Bitget/Bybit/Gate/HTX）+ 传统券商 IBKR/Alpaca，凭据以 CREDENTIAL_ENCRYPTION_KEY 加密。
4. **Agent/MCP 安全模型**：`/api/agent/v1` 令牌哈希存储、作用域限权、限流并审计；agent 默认 **paper_only**，开实盘须四要素同时满足——交易 scope + `paper_only=false` + `AGENT_LIVE_TRADING_ENABLED=true` + 运营者限额白名单。
5. **可观测与加固**：Prometheus/Grafana/Alertmanager 可选 overlay；生产 overlay 非 root 运行、只读根文件系统、丢弃 capabilities。

## A1 (Past Application) — 源项目的典型应用

### 案例: 小团队的"想法→模拟盘→小仓实盘"流水线
- **输入**: 一条均值回归假设与三个月的 OHLCV 数据。
- **做法**: 用 Strategy API V2 写成 Python 策略 → 服务端回测做样本外分段与参数敏感性检查 → Paper Trading 跑两周核对滑点 → 配 restricted API key、仓位/频率/回撤限额 → 四要素审批后以最小仓位开实盘，Grafana 挂回撤告警。
- **结果**: 首笔真实订单与账单对账一致；实盘偏差数据回流用于修订策略假设书，全程未跳过任何风控步骤。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 策略工程化："我有交易想法，想写成 Python 策略在历史数据上回测看看。"
2. 自托管部署："搭一套自己可控的量化系统，接交易所/券商先跑模拟盘。"
3. 上实盘前风控："策略模拟盘稳定了，帮我配好限额、告警和小仓实盘开关。"

### 语言信号
- "回测 / backtest / 样本外验证"
- "Paper Trading / 模拟盘 / 滑点"
- "实盘执行 / live trading / 下单接入"
- "Strategy API / 指标开发 / 交易所 API 对接"

### 与相邻 skill 的区分
- 与 multi-agent-simulation 的区别：本 skill 处理**确定性价格序列上的策略代码与订单执行**，回答"这套规则历史上赚不赚、滑多少"；multi-agent-simulation 用数千智能体社会仿真推演**事件对群体的行为影响**，回答"这条政策出台大家会怎么反应"。要回测下单来这里，要新闻/政策的群体反应推演去那里。

## E (Execution) — 可执行步骤

1. **需求与风险定档** — 明确标的、周期、风险预算与策略失效条件，声明本流程非投资建议。完成标准: 写出含"最大可承受回撤/失效条件/退出规则"的策略假设书。
2. **数据与回测** — 接行情源，服务端回测，必做过拟合检查：样本内/外分段对比、参数敏感性扫描。完成标准: 报告含年化收益/最大回撤/夏普，且样本内外差异落在预设阈值内。
3. **Paper Trading 验证** — 模拟盘运行不少于设定周期，核对成交假设与真实滑点。完成标准: 模拟成交与回测偏差在容差内，偏差项写入假设书。
4. **风控配置** — restricted API key、仓位/频率/回撤三重限额、品种允许名单、agent 保持 paper_only 直到四要素齐备。完成标准: 四要素逐项勾选且限额经用户人工确认。
5. **小仓实盘 + 监控** — 启用实盘后接 Prometheus 告警路由。完成标准: 首笔订单与交易所账单对账一致，回撤告警可达接收人。
6. **复盘迭代** — 定期对照实盘 vs 回测归因偏差（滑点/延迟/深度）。完成标准: 复盘记录更新进策略假设书，形成版本化迭代。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- **预测某条新闻/政策对市场的群体情绪影响** → 走 multi-agent-simulation 的社会仿真推演，本 skill 只算价格序列上的规则表现。
- **代客理财、承诺收益率、荐股喊单** → 拒绝：本流程是自托管工程工具链，不提供投资咨询，无持牌资管能力。
- 无回测数据的纯直觉"梭哈计划" → 拒绝进入执行链路。

### 已知局限 / 失效模式（≥1条）
- 回测过拟合是头号风险：参数优化极易拟合历史噪声；实盘的滑点、深度、断线重连与模拟存在系统性差异。**历史表现不代表未来**，任何漂亮回测曲线都不构成对未来收益的预测。

### 伦理红线
- 所有输出均为技术研究与工程演示，**非投资建议**。用户要求"直接实盘全仓梭哈这个策略"时：必须明确警示可能损失全部本金、指出回测过拟合风险，并要求先完成风险评估（回撤预算、限额设置、Paper Trading 验证）方可继续；拒绝绕过风控步骤或关闭限额直通实盘的操作。

## 相关 skills
- contrasts-with: multi-agent-simulation（价格序列上的策略执行 vs 社会行为的平行世界推演）

---

## 审计信息
- **验证**: V1 ✓（上游 README 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: webfetch `https://raw.githubusercontent.com/OpenByteInc/QuantDinger/master/README.md`（main 分支直连失败后经 master 分支成功）
