---
name: agent-experience-persistence
description: |
  基于 TencentDB Agent Memory（TencentCloud/TencentDB-Agent-Memory）做 Agent 经验的
  跨会话持久化：当长任务上下文被工具日志撑爆需要「卸载但可回溯」、要把对话沉淀为
  L0-L3 分层画像/场景/SOP 且要求白盒可审计、或在 OpenClaw/Hermes 宿主上零改码接入
  记忆插件时触发。边界：不做通用记忆层选型、不优化检索排序算法、不为代码库建静态
  知识图谱。
source_project: TencentCloud/TencentDB-Agent-Memory
tags: [memory, experience, layering, mermaid-canvas, openclaw, hermes, persona]
---

# agent-experience-persistence

## R | 引用

> "TencentDB Agent Memory = symbolic short-term memory + layered long-term memory. …
> The bottom layer archives raw tool outputs (refs/*.md); the middle layer extracts
> step-level summaries (jsonl); the top layer condenses state into a lightweight Mermaid
> canvas. … Lower layers preserve evidence; upper layers preserve structure." 长期线：
> "L0 Conversation → L1 Atom → L2 Scenario → L3 Persona"。

来源：<https://raw.githubusercontent.com/TencentCloud/TencentDB-Agent-Memory/main/README.md>（2026-08-25 抓取）

## I | 骨架

- 定位一句话：拒绝「暴力堆历史」和「不可逆有损摘要」，用分层+符号化让 agent 既记得住又查得回。
- 双支柱：
  - 记忆分层（progressive disclosure）：短期三层 refs/*.md 原始日志 → jsonl 步骤摘要 → Mermaid 画布（带 node_id）；长期语义金字塔 L0 Conversation → L1 Atom → L2 Scenario → L3 Persona；
  - 符号记忆（Mermaid canvas）：任务状态编码成高密度 Mermaid 符号图，全量日志外置，上下文只留几百 token 的画布。
- 无损回溯链：Persona/画布 → Scenario/jsonl → Atom/L0 原文，靠 `node_id` 与 `result_ref` 串联——上层给判断，下层给证据，「可折叠可展开，抽象且可审计」。
- 异构存储：底层事实日志进数据库（SQLite + sqlite-vec），顶层画像/画布是人读 Markdown；混合召回 BM25+向量+RRF。
- 白盒调试：全部产物落在 `~/.openclaw/memory-tdai/`，直接打开检查，调试是沿链确定性行走而非黑盒探向量分。
- 落地形态：OpenClaw 插件（装完即自动捕获/抽取/召回，支持 offload 短期压缩）、Hermes Gateway adapter（:8420，provider 目录名必须是 `memory_tencentdb`）、agent 工具 `tdai_memory_search` / `tdai_conversation_search`。
- 实测数字（README）：OpenClaw 上 token −61.38%、WideSearch 通过率相对 +51.52%、SWE-bench 50 连跑 +9.93%、PersonaMem 48%→76%。

## A1 | 案例

OpenClaw 上连续跑 50 个任务的 SWE-bench 式会话，上下文被搜索结果与报错日志吃满。动作：

1. `openclaw plugins install @tencentdb-agent-memory/memory-tencentdb` 后在配置中 `"enabled": true`；
2. 开启短期压缩：`offload.enabled=true` + 注册 `slots.contextEngine="memory-tencentdb"` + 跑一次 after-tool-call 补丁脚本；
3. 重跑长任务：上下文只剩带 node_id 的 Mermaid 任务画布（数百 token），原始日志归档到 refs/*.md；
4. 某步报错时 agent 对着 node_id grep 回原文，定位后继续。

验收：token 相对下降约六成，任务通过率不降反升；事后从 persona.md 一路能钻取到当时的原始报错文本。

## A2★ | 适用判定

情境一（触发）：「长任务上下文爆炸，要压缩/卸载中间产物但不能丢证据」——符号卸载+回溯链正是主业。
情境二（触发）：「跨会话沉淀用户画像/场景块/SOP，而且中间产物我要能直接打开看」——L0-L3 金字塔+白盒 Markdown 归口在此。
情境三（触发）：「OpenClaw/Hermes 上给现役 agent 加记忆，不想改业务代码」——插件/provider 形态即插即用。

语言信号（命中任意一条即倾向触发）：
- 「经验沉淀」「跨会话持久化」「persona / 用户画像」「场景块 / SOP 复用」
- 「Mermaid 画布」「node_id」「上下文卸载 / offload」
- 「L0 L1 L2 L3」「白盒记忆」「memory-tencentdb」

与兄弟区分：
- `mem0-memory-layer`：通用记忆层选型或跨应用共享（Cursor/Claude 等）→ 归它；本 skill 绑定 OpenClaw/Hermes 宿主的深度集成。
- `hindsight-retrieval`：核心痛点是召回排序精度与时序推理 → 归它；本 skill 卖点是无损分层回溯而非排序算法。
- `project-knowledge-graph`：「记住项目代码结构」是静态建图 → 归它；本 skill 存的是活的交互与操作经验。

## E | 执行步骤

1. 宿主判定与环境预检：OpenClaw ≥2026.3.13 或 Hermes；Node ≥22.16。完成标准：宿主与版本清单确认，非这两类宿主先评估 adapter 成本再继续。
2. 安装并声明：OpenClaw 走 plugins install + enabled；Hermes 走 provider 目录软链（目录名必须 `memory_tencentdb` 下划线）+ config.yaml 声明 + env。完成标准：OpenClaw 首轮对话即捕获；Hermes `curl :8420/health` 返回 ok/degraded。
3. 验证长期线零配置生效：正常聊几轮后检查 `~/.openclaw/memory-tdai/`。完成标准：出现 L0 对话文件与 L1 原子事实，内容人读可懂。
4. 开启短期 offload：offload.enabled + contextEngine slot + after-tool-call patch 脚本。完成标准：构造一个长任务，上下文中只剩 Mermaid 画布，grep 任一 node_id 能取回原始文本。
5. 参数调优：`pipeline.everyNConversations`、`persona.triggerEveryN`、`bm25.language=zh`。完成标准：抽取节奏与实际负载匹配，无积压也无空转。
6. 白盒回溯演练：任选一条 persona 结论，沿 Persona→Scenario→Atom→L0 全程钻取。完成标准：链路 result_ref/node_id 无断链，结论有原文证据。
7. 安全加固（可选）：设 `TDAI_GATEWAY_API_KEY` 与 CORS 白名单。完成标准：无 token 请求被 401，`GET /health` 保持开放供探活。

## B | 边界

不适用：
- 非 OpenClaw/Hermes 的自研宿主要深度定制 → adapter 成本可能高于收益，应先评估 mem0 SDK 直连等轻路线。
- 为代码库建静态结构图谱 → 转 `project-knowledge-graph`。

局限：
- 本地 storeBackend 当前仅 sqlite（TCVDB 云后端已列入已完成 roadmap 但本地版未替换）；Postgres 不受支持，勿承诺。
- OpenClaw 升级后需重跑 patch 脚本；项目生态年轻，便携迁移/自动 Skill 生成仍在 roadmap 未落地。

## 相关 skills

- `mem0-memory-layer`：跨应用通用记忆层对照方案
- `hindsight-retrieval`：召回精度优先路线
- `project-knowledge-graph`：静态语料知识图谱

## 审计信息

- V1✓ 来源核验：main 通道成功抓取全文 README，含基准数据与技术架构，可信
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://raw.githubusercontent.com/TencentCloud/TencentDB-Agent-Memory/main/README.md>
