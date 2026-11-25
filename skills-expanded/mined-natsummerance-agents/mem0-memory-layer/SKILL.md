---
name: mem0-memory-layer
description: |
  基于 Mem0（mem0ai/mem0，AI 应用的通用记忆层）做记忆能力选型与接入：当用户要为 AI
  助手、客服机器人或自治 agent 增加「跨会话记住用户偏好与事实」的能力、在 Mem0 与其他
  记忆方案之间做选型对比、或用 OpenMemory MCP 让 Cursor/Claude 等多工具共享一份本地
  记忆时触发。边界：不做静态代码库知识图谱构建，不做单会话内上下文压缩与日志卸载，
  不承接已锁定 Hindsight 后的检索精度调优。
source_project: mem0ai/mem0
tags: [memory, personalization, mem0, openmemory, mcp, llm-integration]
---

# mem0-memory-layer

## R | 引用

> "Mem0 ('mem-zero') enhances AI assistants and agents with an intelligent memory layer,
> enabling personalized AI interactions. It remembers user preferences, adapts to
> individual needs, and continuously learns over time — ideal for customer support
> chatbots, AI assistants, and autonomous systems. … Single-pass ADD-only extraction —
> one LLM call, no UPDATE/DELETE. … Multi-signal retrieval — semantic, BM25 keyword,
> and entity matching scored in parallel and fused."

来源：<https://github.com/mem0ai/mem0>（README，2026-08 经仓库页摘录蒸馏）

## I | 骨架

- 定位一句话：不是检索算法论文，而是「记忆基础设施的选型与接入」——决定记忆存哪、怎么写、怎么读。
- 写入模型：`add()` 单遍 ADD-only 抽取，一次 LLM 调用完成事实提取；记忆只增不改，避免并发覆盖冲突。
- 读取模型：`search()` 多信号并行（语义向量 + BM25 关键词 + 实体匹配）打分融合；时间感知排序，能区分「现在状态 / 过去事件 / 将来计划」。
- 记忆分级：User / Session / Agent 三级状态，`user_id`、`agent_id`、`run_id` 作隔离与过滤键。
- 交付形态四条路：
  - Python / TypeScript SDK（`pip install mem0ai`）
  - Mem0 Platform 托管（app.mem0.ai，带治理、观测、GDPR）
  - OpenMemory MCP Server（本地优先，add/search/list/delete 四工具 + dashboard）
  - mem0-mcp 工具集（add_memory / search_memories / get_memory / update_memory / delete_memory 等）
- 生态集成：LangGraph、CrewAI 等框架有官方便利；默认嵌入 `text-embedding-3-small`，混合检索推荐 Qwen 系等更强嵌入模型。

## A1 | 案例

跨境电商客服机器人要「记得每个客户的过敏史与历史工单」。接入动作：

1. `pip install mem0ai` 初始化 `Memory()`（OSS 自托管向量库）或直接填平台 API key；
2. 每轮对话结束调用 `m.add(messages, user_id="cust_123")`，LLM 单遍抽出「对花生过敏」「上月退过 1024 号订单」等原子事实；
3. 新会话开场前 `m.search("过敏史", user_id="cust_123")` 注入 system prompt；
4. 收到 GDPR 删除请求时走 `delete_all_memories(user_id=...)`。

验收：三个月后新坐席系统上线，客户无需重述任何偏好，首次响应即个性化。

## A2★ | 适用判定

情境一（触发）：「给我的 AI 助手加长期记忆，让它记住我的偏好」——通用记忆层选型加接入是本 skill 主业。
情境二（触发）：团队在 Mem0 / Hindsight / 自建 RAG 之间犹豫，要对比表与迁移成本——选型咨询属本职范围。
情境三（触发）：想让 Cursor、Claude Desktop、自研 agent 共享同一份本地记忆（OpenMemory MCP）——跨工具记忆归口在此。

语言信号（命中任意一条即倾向触发）：
- 「记忆层 / memory layer」「记住我偏好 / user preferences」
- 「个性化 / personalization」「跨应用共享记忆」
- 「mem0」「OpenMemory」「MCP 记忆服务器」

与兄弟区分：
- `hindsight-retrieval`：已锁定 Hindsight，或核心诉求是召回精度与时序推理（retain/recall/reflect、四路检索融合）→ 归它；Mem0 胜在接入简单与平台治理。
- `agent-experience-persistence`：沉淀对象是 agent 的任务经验/SOP/画像分层（L0-L3、Mermaid 符号压缩）而非用户交互事实 → 归它。
- `project-knowledge-graph`：对象是静态代码库/文档的概念关系网 → 归它，与本 skill 的动态交互记忆正交。

## E | 执行步骤

1. 定义记忆主体与隔离键：user/agent/run 三级中选哪些、如何映射业务 ID。完成标准：隔离键设计写入接入文档。
2. 选部署形态：托管平台（快、有治理）vs OSS 自托管（数据不出域）vs OpenMemory 本地 MCP（个人开发流）。完成标准：给出结论加两条否决理由。
3. 接入 SDK 或挂 MCP 端点，确定 add 与 search 的调用点。完成标准：示例代码跑通——add 一段对话后 search 能命中其中事实。
4. 配置嵌入模型与混合检索参数。完成标准：构造一个只能靠关键词命中的用例，验证语义+关键词+实体三路信号确实并行生效。
5. 设计记忆生命周期：ADD-only 语义下的纠错策略（新增覆盖性事实）、删除与合规出口。完成标准：delete_memory / delete_all_memories 演练通过。
6. 真实对话回归：隔天新会话零提示召回偏好。完成标准：新会话不再要求用户重复既有信息。

## B | 边界

不适用：
- 给代码库/文档集建概念图谱（静态语料结构化）→ 转 `project-knowledge-graph`。
- 单个超长任务内的中间态压缩与日志卸载（短期上下文工程）→ 转 `agent-experience-persistence` 的符号记忆路线。

局限：
- ADD-only 意味着记忆单调增长，过期信息必须配套删除/过滤策略，否则召回被陈旧事实污染。
- 使用托管平台时用户对话事实出域，需评估数据合规；OSS 版则自担存储运维与嵌入服务成本。

## 相关 skills

- `hindsight-retrieval`：召回精度与时序推理优先时的对照方案
- `agent-experience-persistence`：经验与画像的分层持久化
- `project-knowledge-graph`：静态知识结构化

## 审计信息

- V1✓ 来源核验：raw main / HEAD / github.com 三通道均传输失败，最终以 GitHub 仓库页搜索摘录 + mem0.ai 官方页面蒸馏（基于仓库描述蒸馏成立）
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://github.com/mem0ai/mem0> ；<https://mem0.ai/openmemory> ；<https://github.com/mem0ai/mem0-mcp>
