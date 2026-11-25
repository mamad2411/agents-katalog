---
name: memrec
description: AI 记忆持久化系统。用 memrec 跨会话保存与检索项目决策、知识、上下文和用户偏好。支持 MCP（优先）与 CLI、项目隔离、混合检索（KNN+BM25）、中文分词、MMR 重排、时间线浏览、原始记录查看、软删除与 Dream 整合。触发场景：需要记录重要决策或知识、需要回忆历史结论/路径/数字、需要按时间回看进展、需要跨会话保持项目上下文、需要解释检索结果可信度。
---

# MemRec - AI 记忆持久化系统

面向 AI Agent 的本地记忆库。写入以原文直存为主，检索为混合检索；目标不是"替你想"，而是"帮你准确找回之前确认过的事实"。

## 何时使用

| 场景 | 动作 |
|------|------|
| 做出决策、确认结论、踩坑修复完成 | `mr_add` 记录（decision / knowledge） |
| 开始任务，需要历史结论、命令、路径、数字 | `mr_search` 先检索 |
| 需要用户偏好或跨项目通用约定 | `mr_search` + `scope: global` |
| 需要完整原文或分块合并 | `mr_get`（先确认 `is_deleted`） |
| 需要盘点、统计、查看 Dream 运行 | `mr_list` / `mr_timeline` / `mr_stats` / `mr_dream_report` |
| 按时间顺序回看最近发生了什么 | CLI `memrec timeline` |
| 抽取工作记录、导出被 Dream 融合前的原始条目 | CLI `memrec list --raw` / `memrec timeline --raw` |
| 用户明确要求整合/清理旧记忆 | `mr_dream`（先 `dry_run`） |
| 误删恢复 | CLI `memrec restore <id>` |

不要用它做：实时数据查询、外部知识搜索、需要 LLM 抽取/改写事实的场景。MemRec 保真优先，写入什么就存什么。

## 优先使用 MCP

MCP 模式：`memrec --mcp`（stdio）。

```json
{
  "mcpServers": {
    "memrec": { "command": "memrec", "args": ["--mcp"] }
  }
}
```

MCP 不可用时再退回 CLI。两者共享同一守护进程与数据。

## MCP 工具一览

| Tool | 用途 | 主要参数 |
|------|------|----------|
| `mr_add` | 写入记忆 | `content`、`memory_type`、`tags`、`is_global` |
| `mr_search` | 混合检索 | `query`、`top_k`、`min_score`、`scope`、`memory_type` |
| `mr_get` | 取单条完整记忆 | `id`、`merge` |
| `mr_list` | 枚举记忆 | `limit`、`skip`、`scope`、`tags`、`memory_type`、`include_deleted`、`raw`、`with_dream` |
| `mr_timeline` | 按创建时间倒序浏览 | `limit`、`skip`、`scope`、`tags`、`memory_type`、`raw`、`with_dream` |
| `mr_delete` | 软删除 | `id` |
| `mr_stats` | 统计 | 无 |
| `mr_dream` | 触发 Dream 整合 | `force`、`dry_run` |
| `mr_dream_report` | 查看 Dream 审计 | `last` |

### mr_add

```json
{
  "content": "选择 JWT 认证：access 15min + refresh 7d，密钥轮换 30d",
  "memory_type": "decision",
  "tags": ["auth", "critical"],
  "is_global": false
}
```

- `memory_type`：`decision` / `knowledge` / `context` / `preference` / `conversation`。
- `tags`：建议 `critical`（重要）、`fact`（客观事实）、`best-practice`（模式）；写入前自行去重，避免 `["dream-integrated","dream-integrated"]`。
- `is_global: true` 仅用于跨项目通用偏好/约定；项目内结论不要全局化。
- 写入默认开启去重（服务端 `duplicate_threshold` / `update_threshold`）。MCP 返回只有一行 `Added memory: <id> (...)`，不暴露 `action`/`duplicates`；需要知道是新增、跳过还是合并时，用 CLI 的 JSON 输出。

### mr_search

```json
{
  "query": "认证方案 令牌轮换",
  "top_k": 8,
  "min_score": 0.5,
  "scope": "project"
}
```

- `top_k`：建议 5-10；过大只会把低相关结果和 token 一起带进来。
- `min_score`：默认 0.5。MiniLM 模型建议显式 0.75；`MEMREC_MIN_SCORE` 可改默认值。
- `scope`：`project` 仅当前项目、`global` 仅公共记忆、`all` 跨项目。省略时按项目根 `.mr_pid` 推断（存在→project，否则→global）。
- 结果只含 200 字符 `content_preview`；需要全文时对少量命中调用 `mr_get`。

### mr_get

- 返回 `MemoryView`（对外协议视图），只含正文、类型、摘要、标签、重要性、时间、归属、分块与软删状态；`embedding`、`access_count`、`last_accessed`、`metadata` 等内部字段不再返回。
- 返回可能带 `is_deleted: true`。软删除记录不能作为证据；需要时先用 CLI `memrec restore <id>`。
- `merge: true` 用于分块记忆，按 `chunk_index` 拼接全文。

### mr_list / mr_timeline

- 参数：`limit`（默认 20）、`skip`、`scope`、`tags`、`memory_type`、`include_deleted`、`raw`、`with_dream`；返回 `MemoryView` 列表，单条已不含向量。
- `mr_list` 按存储顺序；`mr_timeline` 固定按 `created_at` 倒序，与 CLI `timeline` 语义一致。
- `raw=true` 直读存储层、保留被 Dream 融合软删的源记录，默认按 `metadata.source_ids` 排除融合产出；`with_dream=true` 一并返回。
- 需要人类可读的单行时间线输出时用 CLI `memrec timeline`。

### timeline / mr_timeline

用于回答"最近发生了什么""上一轮做到哪了"，而不是按相关性找答案。

```bash
memrec timeline -l 20 --human              # 最近 20 条，按创建时间倒序
memrec timeline -l 20 --skip 20 --human    # 继续往前翻
memrec timeline -p --human                 # 仅当前项目
memrec timeline -a --human                 # 跨所有项目
memrec timeline --type-filter decision     # 只看决策
memrec timeline --raw --human              # 原始记录时间线：含被融合软删的源记录
memrec timeline --raw --with-dream --human # 原始记录 + Dream 融合产出
```

- 排序由服务端在过滤后、分页前完成，`created_at` 并列时以记忆 ID 保证翻页稳定，因此 `--skip` 不会漏条或重复。
- `--raw` 直读存储层，适合抽取工作记录等需要逐条原始数据的场景；默认排除 `metadata.source_ids` 标记的融合产出，`--with-dream` 可一并返回。
- 人类可读输出每条的格式为：本地时间、类型、单行内容预览，下一行是 ID、标签与重要性。
- MCP 用 `mr_timeline`（参数与 `mr_list` 对齐），CLI 用 `memrec timeline`；两者都只提供时间维度，找具体结论仍应使用 `mr_search`。
- 需要存储层原始逐条记录时，两者都支持 `raw` / `raw + with_dream`。

### mr_delete / mr_stats

- `mr_delete` 是软删除，不物理删除。
- `mr_stats` 返回 `total` / `active` / `deleted`；`total` 含删除态，评估库大小时看 `active`。

### mr_dream / mr_dream_report

- `mr_dream` 会整合旧记忆，可能合并、改写或软删原条。只在用户明确要求"整合/清理记忆"时调用，且先 `dry_run: true` 预览。
- `force: true` 绕过 24h / 新记忆数量门槛；不要用 `force` 代替正常门控。
- `mr_dream_report` 用于审计最近运行：候选、簇、边、门控结果、质量指标。

### MCP Resources

| URI | 内容 |
|-----|------|
| `memrec://stats` | 记忆统计 |
| `memrec://project` | 当前项目信息 |

## 检索结果怎么读

`mr_search` 返回的每个命中包含：

| 字段 | 含义 | 使用建议 |
|------|------|----------|
| `score` | 校准相关度 0-1 | 主判断指标；向量单路=余弦，全文单路=覆盖率，双路=noisy-OR |
| `vector_score` | 原始向量余弦（仅向量命中） | 高表示语义相近；为 null 表示该条不是向量召回 |
| `fts_score` | 原始 BM25（仅全文命中） | 只用于判断词项命中；跨查询不可比，不要拿它当阈值 |
| `coverage` | 查询词覆盖率（仅全文命中） | 高表示查询词覆盖充分；单路低于 0.30 会被丢弃 |
| `rank_score` | 加权 RRF 名次分 | 同分裁决用，一般忽略 |
| `content_preview` | 前 200 字符 | 不足以判断时再 `mr_get` |
| `edge_hint` | 图扩散来源 | 表示经 Dream 语义边到达，不是直接命中 |
| `is_chunked` / `chunk_*` | 分块信息 | 需要全文用 `mr_get merge:true` |

判断要点：

1. `score` 高且 `vector_score` 有值：语义命中，可信度较高。
2. `score` 高但 `vector_score` 为 null：词项/覆盖率命中；看 `coverage`，低覆盖要警惕"只撞上一个词"。
3. `score` 在 0.5 附近且 `vector_score` 也在 0.5 附近：边界命中，建议换关键词或放宽 `scope` 再查一次。
4. 结果为 `edge_hint`：这是图扩散结果，仍需用原文验证。

当前检索参数默认值：混合权重 `alpha=0.5`、MMR 开启且 `lambda=0.5`、时间衰减与来源权重尚未接入排序（配置存在但未生效）。CLI `search` 未暴露 alpha/MMR 开关；需要隔离验证时用 `memrec eval --alpha/--no-mmr`。

## 记忆模型

### 类型

| 类型 | 用途 |
|------|------|
| `decision` | 关键决策、方案取舍 |
| `knowledge` | 已确认知识、事实、最佳实践 |
| `context` | 项目配置、环境、技术栈 |
| `preference` | 用户偏好（通常 global） |
| `conversation` | 对话记录（默认） |

### 标签

- `critical`：重要且应优先保留/检索。
- `fact`：客观事实、数字、路径、命令。
- `best-practice`：可复用模式。
- 其余标签按项目/主题自定，保持短、稳定、可复用；写入前先去重。

### 作用域与 `.mr_pid`

- 项目记忆：守护进程在项目根（优先 git root）维护 `.mr_pid`，格式为 `memrec_project_id=<uuid>` + `created_at`，首次非全局写入时自动创建。
- 全局记忆：`project_id = None`（不是全零 UUID），通过 `--global` / `is_global: true` 写入。
- 默认读取范围：`.mr_pid` 存在→project，否则→global。**常见陷阱**：在尚未注册的目录里只读不写时，默认范围是 global，容易漏掉项目记忆；先完成一次非全局写入生成 `.mr_pid`，或检索时显式用 `scope: all`。
- 非全局写入不会落到 global：守护进程会在项目根自动创建 `.mr_pid` 并写入项目。若发现写入被归到别的项目，检查调用方传入的 `working_dir`（git root 是否多副本）。
- `.mr_pid` 不应提交到 git，加入 `.gitignore`。

### 删除与恢复

- `mr_delete` / `memrec delete` 为软删除；`memrec restore <id>` 恢复并重新加入检索索引。
- `memrec list --deleted` 查看软删除原始记录。
- `memrec list --raw` 查看原始全集：活跃记录 + 被 Dream 融合软删的源记录，默认排除融合产出；加 `--with-dream` 连同融合产出一起返回。`timeline` 同样支持。
- `memrec get` 可能返回已删除记录；使用前检查 `is_deleted`。

## CLI 参考

```bash
memrec add "内容" --mtype <type> [--tag <tag>]... [--global] [--source <source>] [--scope <scope>] [--no-dedup] [--human]
memrec search "关键词" [-p|-g|-a] [-k <num>] [--min-score <f>] [--mtype <type>] [--human]
memrec get <id> [--merge] [--human]
memrec list [-l <num>] [--skip <num>] [-p|-g|-a] [--tag <tag>]... [--type-filter <type>] [--deleted] [--raw] [--with-dream] [--human]
memrec timeline [-l <num>] [--skip <num>] [-p|-g|-a] [--tag <tag>]... [--type-filter <type>] [--raw] [--with-dream] [--human]
memrec delete <id> [--human]
memrec restore <id> [--human]
memrec stats
memrec version
memrec dream [--force] [--dry-run] [--human]
memrec dream-report [--last <num>] [--human]
memrec eval <dataset.jsonl> [--k <num>] [--alpha <f>] [--no-mmr] [--human]
memrec scene create|get|list|delete|add-memory|remove-memory|update-heat ...
```

说明：

- `add` 的 `--mtype` 必填；`--tag` 可重复；`--source` 取值 `user`（默认）/`system`/`inferred`/`external`，仅作元数据，当前不参与排序。
- `add --scope` 仅设置记忆的 scope 元数据（project/global），不改变项目归属；项目归属由 `--global` 与 `.mr_pid` 决定（`workspace` 已废弃，不要新写）。
- `add` 默认去重；`--no-dedup` 跳过。需要查看 `action`（added/skipped/updated）与 `duplicates` 时用默认 JSON 输出。
- `search` 的范围三态互斥；默认按 `.mr_pid` 推断。`--mtype` 过滤记忆类型。
- `list` 的 `--type-filter` 不是 `--type`；`--tag` 可重复且要求全部命中。
- `timeline` 与 `list` 参数对齐，但固定按创建时间倒序；输出时间为本地时区。只读，不改变任何记忆。
- `--raw` 直读存储层、保留软删记录；`--with-dream` 仅在 `--raw` 下生效，用于包含 Dream 融合产出。人类可读输出对软删记录标记 `[DELETED]`。
- `eval` 为只读评测：`--alpha` 控制向量权重（0=纯全文，1=纯向量），`--no-mmr` 关闭多样性重排。
- `scene` 是主题聚合，按需使用，不影响主检索。

## 工作流

1. **任务开始**：用 2-3 个不同措辞的查询 `mr_search`；先 `scope: project`，需要跨项目时再 `scope: all`。`top_k` 保持 5-8。
2. **判断结果**：读 `score` + `vector_score`/`coverage`；对关键条目 `mr_get`，检查 `is_deleted`，引用原文中的数字、路径、命令。
3. **做出决策/完成修复**：`mr_add` 写入自包含内容（结论 + 关键依据 + 文件/行号 + 日期），打 `critical`/`fact` 标签。
4. **纠错**：优先新增一条带"【更正】"前缀的 decision/knowledge，并在内容中写清被更正的旧结论；不要只依赖旧条。
5. **结束**：需要时 `mr_stats` 确认写入生效；不要例行调用 `mr_dream`。

## 常见坑

1. **默认读取范围是 global**：未注册 `.mr_pid` 的目录里，检索默认只查全局记忆；用 `scope: all` 或先完成一次非全局写入，避免漏掉项目记忆。
2. **把 `fts_score` 当相似度**：BM25 无固定量纲；判断相关性看 `score` 与 `coverage`。
3. **把 0.5 当"中等相关"**：0.5 只是默认阈值；边界命中应换词重查，而不是直接采信。
4. **期望 `summary` 一定有值**：只有 Dream 整合等流程会生成摘要；普通记忆没有该字段，判断内容以 `content` 为准。
5. **把软删记录当证据**：`is_deleted: true` 的记录不可用于结论；必要时先恢复。`--raw` 结果天然包含软删记录（人类输出带 `[DELETED]`），导出后需按 `is_deleted` 过滤。
6. **混淆 raw 与普通视图**：`--raw` 默认排除融合产出，看到的是原始逐条记录；需要融合摘要时用普通 `list`/`timeline`，需要完整链路时加 `--with-dream`。
7. **重复标签/重复记忆**：写入前规范化 tags；服务端去重有阈值，不保证完全拦截。
8. **例行 Dream**：Dream 会合并/软删原条，属于维护操作，不是普通写入。
9. **MCP server 版本滞后**：升级 memrec 后需重启 MCP server，才能看到新增的 `vector_score` 等字段。

## 最佳实践

1. 决策即记录，内容自包含，保留数字、路径、命令、日期。
2. 重要信息用 `critical`；客观事实用 `fact`；可复用模式用 `best-practice`。
3. 用户偏好用 `preference` + `is_global`；项目结论不要全局化。
4. 检索优先于枚举；`mr_list` 只用于盘点，不用于找答案。
5. 关键结论必须 `mr_get` 核对原文与 `is_deleted` 后再使用。
6. 不把 MemRec 当外部知识库；它只负责"你之前存过什么"。
7. 抽取工作记录时用 `memrec timeline --raw`：它保留融合前的逐条原始记录；导出后按 `is_deleted` 过滤，需要融合摘要时另用普通时间线。
