---
name: hindsight-retrieval
description: |
  基于 Hindsight（vectorize-io/hindsight，面向「会学习」agent 的记忆系统）做高精度
  记忆检索与回忆接入：当用户抱怨召回不准/时序混乱、要显式控制 retain/recall/reflect
  的存取时机、给编码 agent 装 per-repo 长期项目记忆、或部署调优其四路混合检索时触发。
  边界：不承接通用记忆层选型（未定技术栈时），不做静态代码库知识图谱，不做经验分层
  沉淀与符号压缩。
source_project: vectorize-io/hindsight
tags: [memory, retrieval, hindsight, rag-alternative, longmemeval, mcp]
---

# hindsight-retrieval

## R | 引用

> "Hindsight™ is an agent memory system built to create smarter agents that learn over
> time. … It eliminates the shortcomings of alternative techniques such as RAG and
> knowledge graph and delivers state-of-the-art performance on long term memory tasks.
> … Recall performs 4 retrieval strategies in parallel: Semantic (vector similarity),
> Keyword (BM25), Graph (entity/temporal/causal links), Temporal — merged via reciprocal
> rank fusion and a cross-encoder reranking model."

来源：<https://raw.githubusercontent.com/vectorize-io/hindsight/HEAD/README.md>（2026-08-25 抓取）

## I | 骨架

- 定位一句话：把「记住」升级为「学习」——不是存聊天记录，而是形成可精炼、可反思的信念体系。
- 四类记忆：world facts（世界事实）/ experiences（自身经历）/ observations（多证据支撑的信念，带引文与 proof count，新证据只精炼不覆盖）/ mental models & knowledge pages（对固定问题的常驻答案，读取≈数据库读，零检索零 LLM）。
- 三大操作：
  - `retain`：LLM 抽取事实/时间/实体/关系 → 规范化为实体、时间序列与索引；
  - `recall`：语义 + BM25 + 图 + 时间四路并行召回 → RRF 融合 → cross-encoder 重排 → 按 token 预算裁剪；
  - `reflect`：跨记忆深思考，生成 disposition-aware 回答（如项目风险盘点、外联话术归因）。
- banks 隔离：一 bank 一「大脑」，严格无泄漏；bank 携带背景与 disposition traits（怀疑度/字面度/共情度）影响 reflect 推理；多语言默认保真（张伟 stays 张伟）。
- 部署谱系：Docker（推荐）/ pip `hindsight-api` / Helm / Hindsight Cloud / 嵌入式 `hindsight-all`；存储 PostgreSQL+pgvector 或 Oracle 23ai。
- 接入捷径：LLM wrapper 两行接管存取（`wrap_openai`/`wrap_anthropic`）；60+ 现成集成；每 bank 一个内置 MCP 端点 `/mcp/{bank_id}/`；Memory Defense 对 retain 做 45 模式的密钥/PII 脱敏或拦截。

## A1 | 案例

售后支持 agent 总忘记三周前对客户的承诺。动作：

1. `docker run ghcr.io/vectorize-io/hindsight:latest` 起 server（8888 API / 9999 UI）；
2. 建 bank `support-acme`，设 disposition：skepticism 适中、empathy 高；
3. 每轮会话 `client.retain(bank_id="support-acme", content=对话摘要, timestamp=...)`；
4. 坐席提问走 `recall("我们答应过 ACME 什么交付条件？")`——时序路保证按日期排序命中；
5. 周会前跑一次 `reflect("ACME 有哪些未兑现承诺与机会点？")`，observations 已把散落事实合并成带证据链的信念。

验收：LongMemEval 类问题（跨时间、跨主题指代）命中率显著高于原纯向量库；每次 recall 结果附证据引文。

## A2★ | 适用判定

情境一（触发）：「记忆系统召回不准、时间线混乱，想要更准的检索」——四路融合+重排正是本 skill 卖点。
情境二（触发）：「我想在代码里显式决定什么时候存、什么时候取、什么时候深思」——retain/recall/reflect 显式 API 是本职。
情境三（触发）：「给 Claude Code/opencode 等编码 agent 装 per-repo 项目记忆」——`hindsight-coding-agents install` 一条命令归口在此。

语言信号（命中任意一条即倾向触发）：
- 「hindsight」「retain / recall / reflect」「memory bank」
- 「召回精度」「LongMemEval」「reciprocal rank / 重排」
- 「mental model」「知识页 knowledge pages」「时序检索」

与兄弟区分：
- `mem0-memory-layer`：还在选型、要跨应用共享记忆、要最省事的通用层 → 归它；本 skill 假设已进入实施且精度优先。
- `agent-experience-persistence`：诉求是经验分层沉淀与符号压缩（L0-L3、Mermaid 画布、白盒 Markdown）→ 归它；本 skill 卖点是排序与信念精炼而非分层审计。
- `project-knowledge-graph`：静态语料建概念图谱 → 归它；本 skill 处理动态增长的交互记忆。

## E | 执行步骤

1. 需求定性：确认是动态对话/任务记忆而非静态建图或纯选型。完成标准：需求定性一句话记录在案，误判即转兄弟 skill。
2. 部署 server：Docker 默认路径（或 pip/Helm/Cloud/嵌入式）。完成标准：API 健康检查通过（自托管 :8888 返回正常；嵌入式则 `server.url` 可连）。
3. 设计 bank 划分与 disposition traits：按用户/项目/职能切分。完成标准：bank 清单+背景说明成文，抽查确认无跨 bank 数据泄漏。
4. 选客户端（python/node/go/CLI/REST）接 retain 与 recall。完成标准：retain 十条样本后 recall 命中 ≥8 条，含一条纯关键词命中。
5. 分流查询类型：需要深思的问题切 reflect；高频固定问题建 mental model / knowledge pages。完成标准：一次 reflect 产出跨记忆连接的新结论；一个 mental model 读取延迟为数据库读级别。
6. 生产加固：外部 PostgreSQL、启用 Memory Defense 秘钥/PII 策略、接 Prometheus 监控。完成标准：构造含 fake token 的 retain 被 `[REDACTED:...]` 或拦截。
7. 编码 agent 场景收尾：`npx @vectorize-io/hindsight-coding-agents install <target>`。完成标准：目标 agent 冷启动即注入 per-repo 记忆与知识页。

## B | 边界

不适用：
- 静态代码库/文档集的结构化图谱构建 → 转 `project-knowledge-graph`。
- 尚未决定技术栈、只要「最省事通用记忆层」的选型结论 → 转 `mem0-memory-layer`。

局限：
- 召回质量受 retain 阶段 LLM 抽取质量制约，垃圾进垃圾出；换强模型需重估成本。
- 自托管需养护 PostgreSQL+pgvector 与监控告警；Intel Mac 需换 `hindsight-all-slim`。

## 相关 skills

- `mem0-memory-layer`：通用记忆层选型对照方案
- `agent-experience-persistence`：经验分层持久化路线
- `project-knowledge-graph`：静态语料结构化

## 审计信息

- V1✓ 来源核验：main 通道传输失败，HEAD 通道成功抓取全文 README，内容完整可信
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://raw.githubusercontent.com/vectorize-io/hindsight/HEAD/README.md> ；<https://hindsight.vectorize.io>
