---
name: multi-agent-office
description: |
  基于 Munder Difflin（chaitanyagiri/munder-difflin，多智能体办公协作仿真桌面应用）
  组建与运营 agent 团队：当用户要同时指挥多个不同引擎的终端 agent 分工协作并可视化
  监督、要「对一个主管说需求由它路由分派+审批上抛」、或要给自动化编队配预算熔断与
  人工门禁时触发。边界：不做单 agent 的工程流程装机与插件安装（那是 harness OS 的
  活），不适用 headless 服务器环境。
source_project: chaitanyagiri/munder-difflin
tags: [multi-agent, orchestration, office-simulation, hive, god-agent, circuit-breaker]
---

# multi-agent-office

## R | 引用

> "Munder Difflin takes the terminal-agent CLIs you already run — claude, agy, codex,
> grok, kimi, qwen, opencode, crush, pi, and copilot — and turns them into a
> self-coordinating team: each agent gets long-term memory, a mailbox, and a desk on a 2D
> office floor — and your clone (Michael) routes work between them while you watch."

来源：<https://github.com/chaitanyagiri/munder-difflin>（README，2026-08-25 抓取）

## I | 骨架

- 定位一句话：把已有的终端 coding CLI 变成一支互相通信的「员工」队伍——Electron + React + Pixi.js 办公楼层可视化，node-pty 跑真进程，xterm.js 原样渲染。
- 组织结构：GOD agent（Michael's office）是唯一主管——读所有请求、例行事务自己裁决保持自治、仅把关键项（花钱/破坏性操作/扩大 scope）升级进你的审批队列；你只对 Michael 说话，「他是楼层的老板，你是他的老板」。
- 协作原语（the hive）：per-agent memory；原子文件 mailbox（各写各的 outbox/，router 投递进 inbox/）；共享 blackboard 黑板；append-only event log；single-committer git（agent 一律不碰 git，防 index.lock 损坏）。
- 控制安全三件套：human gates（spend/scope/destructive 上抛）；circuit breaker 失控梯子 steer → constrain → stop；per-agent token 预算 + transcript 实际成本账本 + OTel 遥测。
- 指挥中心：依赖感知 kanban、定时 mission + heartbeat、Monaco IDE 与 CHANGES/HISTORY/COMPARE git rails、Slack/webhook 进出（可spawn 一次性 worker）、shareable hires 角色导入。
- 记忆层：markdown-first 记忆 + 语义召回索引（毫秒级），condensation 防止无限膨胀；另有 Enterprise Knowledge Graph 供查询自有文档制度。

## A1 | 案例

一次内容生产冲刺：三个引擎并行。动作：

1. `npm install && npm run dev` 启动，onboarding 后落楼层；
2. Add agent 依次 spawn `claude`（写稿）、`codex`（写测试）、`qwen`（整理资料），GOD 自动入座 Michael 办公室；
3. 对 Michael 说：「A 写发布博客、B 给核心模块补测试、C 把会议纪要归档成 wiki」——任务出现在 kanban，信封开始在工位间飞行；
4. C 因资料格式反复报错进入循环，breaker 触发：先 steer 提示格式规范，无效则 constrain 收窄权限，仍无效 stop 并换人接手；
5. B 申请安装付费依赖 → 进 Approvals 队列，你批准后放行。

验收：收工时账本花费与预算一致，event log 可回放全程分工轨迹，产物三份齐备。

## A2★ | 适用判定

情境一（触发）：「同时开多个不同引擎的 agent 分工干活，还要直观看到谁在忙什么」——多进程编队+楼层可视化是定义性场景。
情境二（触发）：「只想对一个主管入口说话，任务自动分派、拿不准才来问我批准」——GOD agent 路由+审批队列归口在此。
情境三（触发）：「担心自动化编队失控烧钱/乱删东西，要预算上限和强制刹车」——human gates + circuit breaker 是本职。

语言信号（命中任意一条即倾向触发）：
- 「多智能体办公室」「agent 团队」「蜂群 / hive」「多角色协作仿真」
- 「GOD agent」「Michael」「mailbox / 黑板 / blackboard」
- 「头像楼层」「munder-difflin」「熔断 / 断路器 / 人工审批门禁」

与兄弟区分：
- `ecc-harness-os`：单个 CLI agent 的流程规范化、技能包安装、体检修复 → 归兄弟；本 skill 是多进程多角色的编排与监督。
- 记忆四兄弟：只要记忆组件不要编队 → 归它们；hive 内置记忆是附带品，不替代专用记忆层选型。

## E | 执行步骤

1. 环境预检：OS 支持、Node ≥18、C/C++ 工具链（mac 装 Xcode CLT）、PATH 上至少一个受支持 agent CLI。完成标准：Settings→Prerequisites 页全绿或缺项清单明确。
2. 安装启动：git clone → `npm install`（postinstall 重建 node-pty）→ `npm run dev`。完成标准：onboarding 向导走完，落到办公楼层。
3. 组队 spawn：按角色×引擎 Add agent；确认 GOD 就座。完成标准：楼层头像数与预期一致，任一会话可交互输入。
4. 自然语言派活：向 Michael 下达分工。完成标准：kanban 出现对应任务卡，outbox/inbox 有消息流量，信封动画开始。
5. 设防配置：per-agent token 预算、审批阈值。完成标准：人为构造一次 spend 类请求，确认落入 Approvals 队列而非直接执行。
6. 干预演练：挑一个循环刷错的会话走 steer→constrain→stop 三档梯子。完成标准：三档各执行一次且行为符合阶梯预期。
7. 收尾复盘：对照 durable cost ledger 核对本轮花费，导出 event log 归档。完成标准：成本报表与账本对平，产物清点无遗漏。

## B | 边界

不适用：
- 单 agent 的工程流程规范化/技能包安装 → 转 `ecc-harness-os`。
- headless 服务器/CI 流水线：Electron GUI 应用需要桌面环境，无头场景应直接用编排框架代码。

局限：
- v0.4.5 working prototype，UI 与接口迭代快，操作路径可能随版本漂移。
- Electron 升级后 node-pty 需重跑 npm install 重建原生模块；Apple Silicon 语义记忆曾因 CoreML NaN 全坏，须 ≥0.4.5。
- 打包像素美术为 LimeZu 商业授权，二次分发必须保留署名；官方构建默认发送匿名遥测，敏感环境用 DO_NOT_TRACK 或源码构建关闭。

## 相关 skills

- `ecc-harness-os`：单 agent 工程纪律装机的姊妹场景
- `mem0-memory-layer` / `hindsight-retrieval` / `agent-experience-persistence`：需要独立记忆层时的专业方案
- `project-knowledge-graph`：给团队共享的项目结构知识库

## 审计信息

- V1✓ 来源核验：github.com 页面成功抓取全文 README，架构图/hive 设计/控制面细节完整可信
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://github.com/chaitanyagiri/munder-difflin>
