---
name: yzr-llm-workspace-management
description: |
  当用户要管理由 yzr-llm-wiki-management 维护的多个本地 wiki 时使用本 skill：在 workspace
  层级扫描所有 wiki、生成与维护全局 INDEX.md / STATS.md / LINT.md，做跨 wiki 综合问答
  （路由 / 合成 / 对比 / 局部），维护跨 wiki 交叉引用，做 workspace 级 lint，沉淀跨 wiki
  agent 私有记忆到 MEMORY/。弥补 workspace CLI 只能管元数据不能感知内容的缺陷——CLI 负责
  确定性元数据操作，本 skill 负责需要 LLM 判断的跨 wiki 决策。
  触发："总结我所有 wiki 中关于 X 的内容" / "对比 wiki A 和 wiki B 对 Y 的看法" / "这个问题
  该查哪个 wiki" / "扫一下我的 workspace" / "workspace 整体 lint" / "记一下：用户偏好按
  时间线分 wiki" / "wiki A 的 X 在 wiki B 也有，加个链接" / "升级 workspace / 迁移到最新
  spec / 检查 workspace 版本"。
  不适用：单 wiki 的 ingest / query / lint（走 yzr-llm-wiki-management）；workspace / wiki
  元数据 CRUD（走 workspace CLI）；云端协作 wiki（走 yzr-outline-wiki）。
metadata:
  author: Zuoru YANG
  category: knowledge-base
  modify time: 2026-08-16
  workspace_spec_version: 0.8.0
---

# LLM Workspace Management

按 [`workspace-spec.md`](references/workspace-spec.md) 维护一个**本地**、**多 wiki**
工作区的"全局视图"和跨 wiki 编排能力——单个 wiki 的 ingest / query / lint 仍走
`yzr-llm-wiki-management` SKILL.md skill。本 skill 站在所有 wiki
之上，做需要跨 wiki 判断的事情。

本 skill 提供三块交付物：

- **SKILL.md（本文）**——工作流 + 边界的"宪法"
- **references/workspace-spec.md**——workspace 根 9 类文件的**归属 + skill 读取契约 + 安全约束**
  （toml 完整 schema 由 CLI 代码 SSOT，spec 不做权威定义）
- **scripts/**——`check_workspace_fixtures.py`（**CLI 产物合规的可执行真源**：fixtures 一致性
  检查，输出修复动作；spec 文档是它的说明，不一致时以探测器为准。亦作 migrate 探测器使用。
  standalone，Python 3.7+；端到端测试 `test_check_workspace_fixtures.py`）

## 何时不使用

"何时使用 / 不适用"已在 frontmatter description（含触发词），正文不重抄。本节只补**出路**：

- **单个 wiki 的 ingest / query / lint**（含单 wiki 内 cross-page Q&A）——走
  `yzr-llm-wiki-management` 的对应流程
- **workspace / wiki 元数据 CRUD**（init / add / remove / config / enter / model ...）——
  走 workspace CLI（如 `llmw`），本 skill 不调也不代跑
- **云端协作 wiki**（Notion / Confluence / Outline Wiki / GitHub Wiki）——走
  `yzr-outline-wiki`
- **一次性文档生成**——直接用普通文件写入流程

## 输入 / 输出

### 启动时需具备的信息

| 信息 | 来源 | 备注 |
| --- | --- | --- |
| Workspace 路径 | `$LLMW_WORKSPACE` 环境变量，或默认 `~/yzr_llm_wiki_workspace`，或交互时问 | workspace CLI 通常在 `enter` 时设好本变量 |
| 操作类型 | 用户自然语言 | `scan` / `query` / `link` / `lint` / `migrate` |
| Query 范围（仅 query） | 用户自然语言或显式指定 wiki 名 | 不指定走全局 INDEX 路由 |

### 操作产物

- **scan** → 写 `<workspace>/INDEX.md`（人类可读概览）+ `<workspace>/STATS.md`（结构化统计），
  按 [spec §4 / §5](references/workspace-spec.md) 落盘
- **query** → 对话中给出答案（带每 wiki 引用）；可选落 `<workspace>/cross_queries/<slug>.md`
  （需用户确认后归档；格式见 [spec §7](references/workspace-spec.md#7-cross_queriesskill-维护可选)）
- **link** → 在涉及跨 wiki 引用的 wiki 各自的 source / entity 页追加跨 wiki 链接（走
  `yzr-llm-wiki-management` 的 ingest 流程，不直接写 wiki 文件）
- **lint** → 写 `<workspace>/LINT.md`（最近一次报告，每次 lint 覆盖；格式见
  [spec §8](references/workspace-spec.md#8-lintmdskill-维护可选)）+ 对话中总结
- **migrate** → 跑 `scripts/check_workspace_fixtures.py` 输出 drift 报告（每条 finding
  带修复动作）；agent 按报告修复后的最新 spec 兼容 workspace；详见 §6 Migrate

## 执行原则 / 边界

### 与 workspace CLI 的边界

**本 skill 不调 workspace CLI**。原因：

1. workspace CLI 只读 / 写三份元数据 + 启动 session——本 skill 读 workspace.toml /
   wiki_metadata.toml **直接读**比解析 CLI 输出更可靠（CLI 输出是给人看的，文本可能改）
2. 本 skill 不修改 workspace.toml / wiki_metadata.toml——告诉用户跑 `llmw wiki ...`，
   人类执行。CLI 的元数据写入是用户驱动的决策，skill 不越权
3. workspace CLI 已通过 `wiki enter` 把 session 启动好（包含 model overlay）；
   本 skill 在 session 内只做内容层决策，不需要再 `enter`
4. **依赖单向 DAG（无环）**：本 skill 与 workspace CLI 都只依赖 spec 文件对齐契约
   （workspace-spec.md 本仓自有；wiki-spec.md 在 `yzr-llm-wiki-management` 仓）；本 skill
   **不**直接依赖 workspace CLI 的代码或二进制，运行时只委托 `yzr-llm-wiki-management`（下节）

### 与 yzr-llm-wiki-management 的边界

**本 skill 委托单 wiki 操作给 `yzr-llm-wiki-management`**：单 wiki 的 ingest / query / lint /
写跨 wiki 链接到某 wiki 的 source 页，一律转交其对应流程——本 skill **不直接**编辑
`<wiki>/wiki/**`（保持 wiki 内 log.md 同步、frontmatter 必填等不变量）。本 skill 自己做
**workspace 层**的事：scan 聚合 / route 路由 / 跨 wiki 综合与对比 / 跨 wiki 链接建议 /
workspace lint / 跨 wiki memory。

### 文件归属（不变量，强制）

| 文件 / 目录 | 维护方 | 本 skill 的态度 |
| --- | --- | --- |
| `<workspace>/workspace.toml` | workspace CLI | 只读（迁移例外见 §6） |
| `<workspace>/CLI 内部配置 *.toml`（模型注册表 / 运行时等） | workspace CLI | 只读（甚至不读；不感知 model 配置） |
| `<workspace>/.gitignore` | workspace CLI | 只读（迁移例外见 §6） |
| `<workspace>/AGENTS.md`（SSOT） | 用户（CLI init 时拷 SSOT 模板） | 只读（schema 宪法；改前先与用户确认；迁移例外见 §6）；**作用域 = 跨 wiki**，wiki 子目录内不加载（见"加载作用域边界"小节） |
| `<workspace>/CLAUDE.md`（薄壳） | 用户（CLI init 时拷薄壳模板） | 只读（迁移例外见 §6）；**作用域 = 跨 wiki**，wiki 子目录内不加载（同上） |
| `<workspace>/INDEX.md` | 本 skill | 写 |
| `<workspace>/STATS.md` | 本 skill | 写 |
| `<workspace>/cross_queries/` | 本 skill | 写 |
| `<workspace>/LINT.md` | 本 skill | 写 |
| `<workspace>/MEMORY/` | CLI init 建骨架（目录 + MEMORY.md）+ 本 skill | CLI init 写 MEMORY.md 索引；skill 写 `*.md` 经验 + 同步索引 |
| `<wiki>/wiki_metadata.toml` | workspace CLI | 只读 |
| `<wiki>/wiki/{entities,concepts,sources,...}` | `yzr-llm-wiki-management` | 通过它写 |
| `<wiki>/MEMORY/` | `yzr-llm-wiki-management` | 通过它写（单 wiki 私有记忆） |
| `<wiki>/AGENTS.md`（SSOT） | 用户（CLI init 时拷 SSOT 模板） | 只读 |
| `<wiki>/CLAUDE.md`（薄壳） | 用户（CLI init 时拷薄壳模板） | 只读 |
| `<wiki>/raw/` | 用户 | 只读 |

完整归属表见 [spec §1](references/workspace-spec.md#1-目录结构)。**违反归属 = bug**：
本 skill 写 `workspace.toml` 属越权；CLI 写 `INDEX.md` 属越权；skill 写
`<workspace>/AGENTS.md` / `CLAUDE.md` 属越权（用户宪法；spec 升级迁移例外见 §6 +
spec §17.2）。**MEMORY 跨边界混淆**：本 skill **禁止**写
`<wiki>/MEMORY/`，单 wiki 记忆归 `yzr-llm-wiki-management`；同样禁止把跨 wiki 观察
写到单 wiki MEMORY——按 [spec §9 scope 边界](references/workspace-spec.md#9-workspace-memoryskill-维护)。

## 工作流 / 步骤

### 0. 启动检查

每次进入本 skill 时：

1. 定位 workspace 路径：`$LLMW_WORKSPACE` → 默认 `~/yzr_llm_wiki_workspace` → 交互问
   （同「启动时需具备的信息」表）
2. 验证 `<workspace>/workspace.toml` 存在——不存在提示用户 "workspace 还没 init，
   跑 `llmw init` 初始化"（**不**替用户跑）
3. **加载跨 wiki MEMORY 索引**：在 workspace 根工作时经 `<workspace>/AGENTS.md` 的
   `@MEMORY/MEMORY.md` import 自动加载；非根目录工作 / 原生读 AGENTS.md 不展开 `@` 的 agent →
   显式 `Read <$LLMW_WORKSPACE>/MEMORY/MEMORY.md` 补齐（加载机制见
   [spec §9.1](references/workspace-spec.md#91-memorymemorymd索引)）
4. **加载作用域边界**：`<workspace>/AGENTS.md` / `CLAUDE.md` 只约束**跨 wiki 工作**——当
   agent cwd 在 `<wiki>/` 子目录内、改跑 `yzr-llm-wiki-management` 时，本 skill 纪律
   （含跨 wiki MEMORY）**不**接管，由 `<wiki>/AGENTS.md` 单 wiki 纪律生效（模板顶部有
   scope 声明；警惕 MEMORY scope 混淆：workspace `MEMORY/` = 跨 wiki，`<wiki>/MEMORY/` =
   单 wiki；log 写入归属：wiki 内 ingest 写 `<wiki>/wiki/`，非 workspace 级 INDEX / STATS）
5. **不**自动跑 `scan`——等用户给操作意图

### 1. Scan / refresh-index

**触发**："扫一下 workspace" / "更新 INDEX.md" / 用户说"workspace 该刷新了"。

**流程**：

1. **版本比对**（spec §14）：读 `<workspace>/workspace.toml` 的 `templates_version`，
   workspace_spec 分量与本 skill `metadata.workspace_spec_version` 不一致 → **警告用户**
   "workspace spec 落后（X → Y），建议先走 §6 Migrate"（不阻断；用户确认继续才往下扫）
2. 读 `<workspace>/workspace.toml` 拿 `[wikis]` 注册表
3. 对每个 wiki：
   - 读 `<wiki>/wiki_metadata.toml`（CLI 维护）
   - 读 `<wiki>/AGENTS.md` §0（拿主题名）+ §一（拿边界）
   - 读 `<wiki>/wiki/index.md`（已有内容 + 段落骨架）
   - 扫 `<wiki>/wiki/{entities,concepts,sources,comparisons,syntheses}/` 拿 page counts
   - 扫 `<wiki>/raw/` 递归拿原始资料数（仅 `find` + 计数，不读内容）
   - 读 `<wiki>/wiki/log.md` 末条拿 last activity
   - 读 `<wiki>/MEMORY/` 拿 memory files 数（仅文件名）
4. 读 `<workspace>/MEMORY/MEMORY.md` 索引（知晓已有跨 wiki 记忆，供 query 路由 / scan 报告
   引用）；按 wiki name 字母序聚合，写 `<workspace>/INDEX.md`（格式见
   [spec §5](references/workspace-spec.md#5-indexmdskill-维护)）+ `<workspace>/STATS.md`
   （格式见 [spec §6](references/workspace-spec.md#6-statsmdskill-维护)）
5. 原子写（POSIX `tmp + fsync + rename`）
6. 对话中报告："已刷新 INDEX.md / STATS.md，X 个 wiki，Y 个 page，Z 个原始资料"

**何时不做 scan**：用户只想做 query → 先用现有 INDEX.md；INDEX.md 缺失或明显过期
（覆盖不到新增 wiki）再提示先 scan。

### 2. Query（跨 wiki Q&A）

**触发**："总结我所有 wiki 中关于 X 的内容" / "对比 A 和 B 对 Y" / "X 该查哪个 wiki"。

**4 种模式**（按用户意图 + 是否指定 wiki 范围自动判定）：

| 模式 | 触发关键词 | 流程 |
| --- | --- | --- |
| **route** | "应该查哪个 wiki" / "属于哪个 wiki" | 读 INDEX.md → 按 topic / tag / description 匹配 → 返回 1–3 个候选 wiki 名 + 理由 |
| **synthesis** | "总结所有" / "综合所有 wiki" / "跨 wiki 总结" | route → 每候选 wiki query → 合并 + 标注每 wiki 来源 |
| **compare** | "对比 A 和 B" / "A 和 B 的区别" | 读 wiki-A 与 wiki-B 的 `wiki/index.md` → query 双侧 → diff 风格对比 |
| **local** | "只看 wiki X" / "在 X 里查 Y" | 走 `yzr-llm-wiki-management` query（单 wiki） |

**判定规则**：

- 用户显式指定 1 个 wiki → **local**
- 用户显式指定 2 个 wiki 且带"对比 / 区别 / 异同" → **compare**
- 用户说"哪个 / 属于哪里 / 应该放哪" → **route**
- 其余 → **synthesis**

**good query 必有"是否归档"环节**——参考 `yzr-llm-wiki-management` query 流程 SKILL.md
的"是否归档"原则。归档位置：

- 答案涉及**单 wiki** → 归档到 `<wiki>/wiki/syntheses/<slug>.md`（走 `yzr-llm-wiki-management`）
- 答案涉及**多 wiki** → 归档到 `<workspace>/cross_queries/<slug>.md`（本 skill 直接写，
  格式见 [spec §7](references/workspace-spec.md#7-cross_queriesskill-维护可选)）

### 3. Link（跨 wiki 交叉引用）

**触发**："wiki A 里的 entity X 在 wiki B 也存在，加链接" / "扫一下跨 wiki 重复 entity"。

**流程**：

1. **扫描**：对每个 wiki 的 `wiki/entities/` + `wiki/concepts/`，提取所有 entity name
   （frontmatter `title` 或文件名 slug）
2. **去重聚合**：跨 wiki 同名 / 近义（用 description 比对）的 entity 收集为候选对
3. **建议**：对话中列出候选对，让用户选哪些要加跨 wiki 链接
4. **写入**：用户确认后，对每个涉及的 wiki，调用 `yzr-llm-wiki-management` 的 ingest
   流程更新对应 entity / concept 页——追加"跨 wiki 引用"段，引用路径用相对 workspace
   根（例 `[huawei_storage wiki 的 storage-architecture](../huawei_storage_wiki/wiki/concepts/storage-architecture.md)`）

**不变量**：本 skill **不直接**编辑 `<wiki>/wiki/**`——一律通过 `yzr-llm-wiki-management`
的 ingest 流程（保持 wiki 内的 log.md 同步、frontmatter 5 必填、不变量等）。

### 4. Lint（workspace 级）

**触发**："workspace lint" / "workspace 健康检查" / 定期（如每次 scan 时顺带）。

**流程**：

1. **workspace 级 deterministic 检查**（agent 内联 / 后续拆脚本）：
   - 重复 entity 跨 wiki（同名 + 不同 slug 的对）
   - 失效跨 wiki 链接（cross_queries/*.md 的 `sources` 路径不存在；`<wiki>/wiki/**`
     中的 `../<another-wiki>/...` 路径不存在）
   - 未注册的 wiki 子目录（磁盘上有 `<wiki>/AGENTS.md` 但 workspace.toml 没有注册）
   - workspace.toml 注册但磁盘上不存在的 wiki（孤儿注册）
   - STATS.md 与 INDEX.md 的 wiki 列表是否一致
   - MEMORY 索引一致性：扫 `<workspace>/MEMORY/*.md`（排除 `MEMORY.md`），任一文件未在
     `MEMORY/MEMORY.md` 索引列出 → 报 `memory-not-indexed`（severity = info，与 wiki 侧
     lint-checklist §14 对齐）
2. **本 skill 做的半定性检查**：
   - 主题重叠的 wiki 是否需要合并
   - tag 体系是否混乱（同名 tag 含义不同 / 同含义 tag 命名不一）
3. **本 skill 不做的**：单 wiki 内部 lint（重复 entity / 缺 frontmatter / 矛盾主张等）
   ——转交 `yzr-llm-wiki-management`
4. **输出**：写 `<workspace>/LINT.md`（格式见
   [spec §8](references/workspace-spec.md#8-lintmdskill-维护可选)）+ 对话中报告

**何时不做 lint**：用户只问 query → 不 lint；用户说"扫一下" → scan 而非 lint。

### 5. Memory（跨 wiki agent 私有记忆）

**触发**：在 scan / query / link / lint 过程中识别到**跨 wiki**值得沉淀的信息时主动写。

**写 / 不写**：只写**跨 wiki 视角**的经验（关联 / 组织偏好 / lint 模式 / 综合经验）；
单 wiki 踩坑、跨 wiki 综合答案本身、一次性观察都**不**写——完整清单与 scope 边界见
[spec §9.3](references/workspace-spec.md#93-何时写--不写)。

**流程**：

1. 识别一个值得沉淀的跨 wiki 观察
2. **scope 自检**——确认是跨 wiki 视角（不只涉及单个 wiki）
3. **判别条目形式**（完整 vs 短条目，判别尺度见 [spec §9](references/workspace-spec.md#9-workspace-memoryskill-维护)）：
   完整条目 → 走步骤 4-6；短条目 → 直接到步骤 6
4. 生成 slug（kebab-case 短标题，例 `user-prefers-time-based-wikis`）——仅完整条目需要
5. 检查目标 MEMORY 文件是否已存在（仅完整条目）：
   - 不存在 → `Write` 新文件（frontmatter 5 必填：`title` / `type`（用 `workspace-memory`） /
     `created` / `updated` / `tags`；推荐 `wikis` 数组 + `description`）
   - 已存在 → `Edit` 更新正文 + `updated` 字段，`created` 保留原值
6. **同步 `MEMORY.md` 索引一行**：完整条目 `- <slug> — 一句话摘要 → [正文](<slug>.md)`；
   短条目 `- <一句话事实>`（无链接、无对应 .md；索引经 AGENTS.md `@` import 常驻可达）——
   漏写 = 下次读不到，lint `memory-not-indexed` 兜底
7. **不**追加 `INDEX.md`（MEMORY 是 agent 私有入口）也**不**写 log.md（无 workspace-level log）

**MEMORY 骨架不由 skill 建**：`<workspace>/MEMORY/` 目录 + `MEMORY.md` 索引由 **CLI init** 创建
（[spec §9](references/workspace-spec.md#9-workspace-memoryskill-维护) §9.1）；skill 不重建（已存在即
跳过），只在写跨 wiki 经验时追加 `*.md` + 同步索引。

**MEMORY 与单 wiki MEMORY 的清晰边界**：

| 场景 | 写哪 |
| --- | --- |
| "wiki A 的 ingest 总是失败，因为 raw/ 里有特殊字符" | `<A>/MEMORY/ingest-special-char-pitfall.md`（单 wiki 经验） |
| "用户偏好把所有 storage 相关放 A wiki，把 LLM 相关放 B wiki" | `<workspace>/MEMORY/user-storage-vs-llm-preference.md`（跨 wiki 偏好） |
| "跨 wiki 综合答案：对比 A 与 B 的性能优化方法" | `<workspace>/cross_queries/perf-compare-a-b.md`（答案本身，不是 memory） |

### 6. Migrate（升级 workspace spec）

**触发**："升级 workspace / 迁移 / 检查 workspace 版本 / 老格式 / spec 升级"；或 §1 scan
版本比对发现 `templates_version` 落后。

**职责切分**：`scripts/check_workspace_fixtures.py` = **探测器**（只扫不修，输出带 `fix`
动作的 drift 报告；修复面恒定 ≤ 4 个结构文件、不落 plan 文件、零中间产物——机制见
[spec §17.3](references/workspace-spec.md#173-检测与修复流程)）；agent（本节）= **修复者**，
按报告 `fix` 动作执行，所有权开口严格按 [spec §17.2](references/workspace-spec.md#172-迁移例外所有权开口)；
迁移依据 SSOT = 报告 `fix` 动作（`to_action` 自含）+ [spec §17](references/workspace-spec.md#17-升级迁移skill-维护)。
**不**写 INDEX.md / STATS.md / LINT.md——迁移不是 scan / lint 事件。

**流程**：

1. **跑探测**：

   ```bash
   python3 scripts/check_workspace_fixtures.py "$LLMW_WORKSPACE"
   ```

   `--json` 供程序化消费；退出码 0 全过 / 1 有 error / 2 运行错误（check 清单见
   [spec §17.3](references/workspace-spec.md#173-检测与修复流程)）
2. **dry-run 报告**（默认必走）：按 finding 分组列"哪些文件需改、依据报告 fix.to_action"；
   询问用户：应用全部 / 部分应用 / 仅看清单
3. **执行修复**（用户确认后，按 `fix.type` 逐项落，具体动作以报告 `fix.to_action` 为准）：
   - `workspace-fix-agents-md-resync`——提取 §六 4 变量（无「当前配置」表时 fallback H1 +
     散文行）→ 渲染 [`workspace-agents-md-template.md`](references/workspace-agents-md-template.md)
     （版本用目标值）→ diff 旧文件，多出的本地定制逐条与用户裁定（搬 `MEMORY/` 或丢弃）→
     Write 覆盖（**不**做局部 Edit）
   - `workspace-fix-agents-version`——单 Edit 版本行（若 resync 同报，走 resync 一并覆盖，
     不做本步）
   - `workspace-fix-claude-md-resync` / `-create`——按
     [`workspace-claude-md-template.md`](references/workspace-claude-md-template.md) 渲染
     Write（唯一变量 `{{WORKSPACE_DISPLAY_NAME}}`）
   - `workspace-fix-gitignore-skeleton`——单 Edit 补缺失段 / 托管块规则（**不动**用户自定义规则）
   - `workspace-fix-memory-index-init` / `-skeleton`——按
     [`canonical/memory-index.md`](references/canonical/memory-index.md) 逐字创建，或单
     Edit 补骨架（**不动** `## 索引` 下成长条目）
   - `workspace-fix-templates-version`——**收尾** Edit `workspace.toml` 的
     `templates_version` 单字段（其余不动）
4. **验证**：重跑脚本——0 error 收尾；仍有 finding 报告残留 + 转人工
5. **不**触发各 wiki 的 migrate——报告里 `wiki_spec` 分量落后时**提示**用户逐个 wiki
   走 `yzr-llm-wiki-management` §5 Migrate（跨 skill 委托，不代跑）

**边界**：

- **不**改 CLI 内部配置 toml（模型注册表等）/ 各 `<wiki>/` 内任何文件
- **不**在迁移过程中跑 scan / query / link / lint（保持职责单一）
- **`templates_version` 的 wiki_spec 分量只展示不比对**——各 wiki 版本归
  `yzr-llm-wiki-management` 管，本 skill 不读兄弟 skill 的版本
- **`current > skill`**（workspace 比 SKILL 新）：**不**阻断，告警用户升级 SKILL 仓；**不**改 workspace

## 参考样例

### 样例 1：跨 wiki 综合问答

> 用户："我所有 wiki 中关于 RAID 有什么记录？"

1. skill 读 `<workspace>/INDEX.md` → 找到 `huawei_storage_wiki` 的描述含"存储"
2. mode = **synthesis**（用户说"所有 wiki 中"）
3. 转交 `yzr-llm-wiki-management` 给 `huawei_storage_wiki` 做 query："RAID"
4. 拿到答案（带 source 页引用），对话中给用户，附"只涉及 1 个 wiki，是否归档到
   `huawei_storage_wiki/wiki/syntheses/raid-overview.md`？"
5. 用户确认 → 走 `yzr-llm-wiki-management` 写 synthesis 页 + log 条目

### 样例 2：跨 wiki 对比

> 用户："`huawei_storage_wiki` 和 `test` wiki 在性能优化上有什么不同？"

1. skill 读 INDEX.md → 两个 wiki 都在
2. mode = **compare**（两个 wiki + "不同"）
3. 分别转交 `yzr-llm-wiki-management` 给两个 wiki query："性能优化"
4. 对比两份答案，按主题维度 diff（共识 / 分歧 / 一方独有）
5. 询问是否归档为 `<workspace>/cross_queries/storage-vs-test-perf.md`（用户确认后写）

### 样例 3：路由

> 用户："我刚下了一篇 LLM inference 论文，应该放哪个 wiki？"

1. skill 读 INDEX.md + 读每个 wiki 的 description / tags
2. mode = **route**
3. 返回："`huawei_storage_wiki` 主题是存储，不相关；`test` wiki 主题是 test，也不相关；
   建议新建一个 wiki（`llmw wiki --name=llm-inference add ...`）"
4. **不**自动跑 `llmw wiki add`——告诉用户跑 CLI 命令

## 参考文件

- **必读**：[`references/workspace-spec.md`](references/workspace-spec.md)——workspace 根
  9 类文件的归属 + skill 读取契约（含 §4 AGENTS.md / CLAUDE.md + §9 MEMORY/）
- **必读**：[`references/workspace-agents-md-template.md`](references/workspace-agents-md-template.md)——
  `<workspace>/AGENTS.md`（SSOT）的 canonical 模板字节金标准（CLI init 时按此拷）；薄壳 `<workspace>/CLAUDE.md`
  见 [`workspace-claude-md-template.md`](references/workspace-claude-md-template.md)
- **必读**：`yzr-llm-wiki-management` SKILL.md 的 `references/wiki-spec.md`——
  单 wiki 内的目录 / frontmatter / 命名约束（本 skill 操作 wiki 时遵循）
- **委托目标**：`yzr-llm-wiki-management` SKILL.md——
  单 wiki ingest / query / lint / memory 工作流（本 skill 的单 wiki 操作委托给它）
- **CLI 文档**：workspace CLI 仓（命令 `llmw`，仓路径由用户在外部维护）——本 skill
  **不直接调**，但用户的 `init / add / remove / config / enter / model ...` 命令参考此处
