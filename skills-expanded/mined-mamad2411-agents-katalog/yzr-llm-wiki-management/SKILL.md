---
name: yzr-llm-wiki-management
description: |
  当用户和本地、单用户、复利型 Markdown 个人 wiki（Karpathy 'LLM owns wiki' 模式）打交道时
  使用本 skill——覆盖：初始搭建、批量摄取 raw/ 资料（论文 / 文章 / 剪藏 / 外部代码仓 symlink
  接入）、跨页综合 / 对比 / 矛盾协调 / 答案归档回 wiki、矛盾 / 孤儿 / 过期摘要 lint、spec
  升级迁移。坚持 raw/ 用户掌控 + wiki/ LLM 拥有 + AGENTS.md 单一真源 四层纪律。
  触发："把这篇论文摄取进 wiki" / "总结 wiki 里关于 X 的内容" / "wiki 里 A 和 B 说法矛盾，
  帮我协调" / "扫一下 wiki 有没有孤儿页 / 过期摘要" / "升级 wiki / 迁移到最新 spec / 检查
  wiki 版本" / "把 X 仓库（源码）纳入 wiki" / "想搭一个 wiki 管理 X"。
  不适用：云端 / 团队协作 wiki（Notion / Confluence / Outline / GitHub Wiki——走
  yzr-outline-wiki）。
metadata:
  author: Zuoru YANG
  category: knowledge-base
  modify time: 2026-08-16
  wiki_spec_version: 0.34.0
  fixtures_check_count: 21
---

# LLM Wiki Management

按 Karpathy [LLM Wiki 设计哲学](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
维护一个**本地**、**复利累积**的知识库：用户只管读 + 提供资料 + 提问题，LLM 负责摘要、
交叉引用、归档、簿记这些"无聊的部分"。和 `yzr-outline-wiki` 等云端 skill 的关键区别是
**本地文件 + 三层纪律**——vs 云端 MCP 单层文档。

本 skill 提供三块交付物：

- **SKILL.md（本文）**——工作流 + 纪律的"宪法"
- **scripts/**——ingest_diff.py / lint_wiki.py / check_wiki_fixtures.py / log_format.py /
  **wiki_write.py**（机械字节写操作：log / index / touch / new / memory 五子命令，见 §设计决策
  「机械 vs 判断」的准入规则）。高频 deterministic 任务固化下来（**不**含
  setup_wiki——wiki 仓的创建由外部 workspace CLI 负责）。当前检查项数见
  `metadata.fixtures_check_count`（详见 [`references/migrate-workflow.md`](references/migrate-workflow.md) + §五 Migrate）。
- **references/**——按需加载：AGENTS.md schema 模板 + CLAUDE.md 薄壳模板、各操作详细流程、页面模板、
  wiki-spec.md（wiki 仓出生形态 + skill 读取契约）、fixtures（CLI 字节级比对金标准）、migrate-workflow.md §六
  (语义合并规则，agent 走 migration plan 时的合并依据)

## 何时不使用

"何时使用 / 不适用"已在 frontmatter description（含触发词），正文不重抄。本节只补**出路**与
正文独有负例：

- **云端协作 wiki**（Notion / Confluence / Outline Wiki / GitHub Wiki）——走
  `yzr-outline-wiki`（搜 / 读 / 写 / 编辑）。两套 skill 方向单向：本地研究沉淀 →
  云端分享，不冲突
- **一次性文档生成**（不是累积型）——直接用普通文件写入流程
- **没有 raw/ 资料 + 没有累积需求**——skill 的价值在"复利"，一次性整理用不上
- **需强结构化数据库**（带 schema / SQL / 全文检索后端）——wiki 规模 ≤ 数百页时
  index.md 足够；超过该规模再考虑迁移到专用工具
- **多人实时协作**——本 skill 假设单人使用（多账号实时协同走云端 wiki）
- **系统设计文档写作**（单篇正式设计文档）——走 `yzr-sys-design-doc`

## 输入 / 输出

### 启动时需具备的信息

| 信息 | 来源 | 备注 |
| --- | --- | --- |
| Wiki 根目录 | `LLM_WIKI_ROOT` 环境变量，或交互时问 | 例 `~/wiki/llm-systems` |
| 主题名 | setup 时一次性指定，写入 `AGENTS.md` | 例 "LLM Systems" |
| 操作类型 | 用户自然语言 | ingest / query / lint / migrate / setup |
| 触发资料 | ingest 时给文件路径或目录 | 必须在 `raw/` 内 |

### 操作产物

- **setup** → 由外部 workspace CLI 完成（按 [`references/wiki-spec.md`](references/wiki-spec.md) 落盘），
  本 skill 不实现创建逻辑；产物形态为目录结构 + AGENTS.md（SSOT）+ CLAUDE.md（薄壳）+
  wiki/index.md + wiki/log.md + MEMORY/MEMORY.md + .gitignore
- **ingest** → 新增 / 更新 `wiki/sources/<slug>.md` + 同步实体 / 概念页 + 追加
  `log.md` 条目 + 更新 `index.md`
- **query** → 对话中给出答案（带引用），**可选**把答案归档为 `wiki/comparisons/`
  或 `wiki/syntheses/<slug>.md`
- **lint** → `log` 中报告：raw/ 是否被改、孤儿页、断裂交叉引用、过期摘要、缺
  frontmatter、log.md 格式
- **migrate** → 跑 `scripts/lint_wiki.py --check-version` 输出 spec 版本 + legacy 现场
  报告；`--apply` 把 migration plan 以 JSON 输出到 stdout（不落盘）供 agent 按
  `references/migrate-workflow.md` 走 Edit/Write 修复；详见 §5 Migrate

## 设计决策

### 机械 vs 判断——写操作进脚本的准入规则

> **一个写操作进脚本（`wiki_write.py`），当且仅当：(1) 输出字节是输入的纯函数**
> （不读正文、无权衡、无用户偏好）；**(2) lint 已有对应检查能验证产物**（round-trip
> 可测：脚本产物必须 lint-clean）。**两条缺一 → 留 agent/md。迁移期一律 agent**
> （迁移 = 格式未定之时，脚本只认识当前形态）。完整论证见 git log
> （`git log --follow -- yzr-llm-wiki-management/SKILL.md`，0.31.0 提交）。

- **已固化**（五子命令都满足两条）：log 追加+截断 / index 条目增删 / touch `updated`+清
  reviewed 戳 / new 脚手架（5 必填 frontmatter + H1，slug 校验 + 拒覆盖）/
  memory 条目+索引行。**留 md**：摘要写作、entity/concept 是否新建、矛盾处理、query
  综合与归档征询、语义合并——都要读内容做判断
- **逃生舱**：手写始终合法、lint 兜底——脚本是默认路径不是闸门，agent 遇到脚本不支持
  的形态退到 Edit/Write 不算违规
- **脚本不自带内容知识**：不生成摘要、不嵌正文模板（SSOT 在 page-templates.md）、不做
  语义合并——想往脚本里加"理解"就是边界被侵蚀的信号
- **常量单一来源 + 版本防护**：wiki_write.py 从 lint_wiki.py / log_format.py import
  （VALID_TYPES / LOG_RETENTION_LIMIT / LOG_LINE_RE 等），spec 改格式变更点不增；
  启动时 wiki §八 版本与 SKILL 不一致 → 警告"先 migrate 再写"（不阻断）

### 四层架构——为什么是四层

参考 Karpathy gist 的核心论断：**"Knowledge 的累加依赖纪律，不依赖意志力"**。
四层各自承担一个责任，互相制衡：

1. **`raw/` 真相之源**——用户只管策划原始资料，对 LLM 只读。**两处写权限例外**：
   `raw/external/`（外部代码仓 symlink 接入，LLM 主导，spec §13.3）+ `raw/discussions/`
   （协作草稿层，双方可写，spec §15）。完整纪律（含"wiki 与 raw 矛盾以 raw 为准"4 条）
   在 `<wiki-root>/AGENTS.md` §一（模板见
   [`references/agents-md-template.md`](references/agents-md-template.md)），操作细则在
   核心原则 §1 + spec §13/§15。`raw/` 下子目录自由组织；
   `ingest_diff.py` 递归扫整棵 `raw/`（扩展名白名单 *.md/*.markdown/*.txt；跳过
   `assets/` + `discussions/`）。
2. **`wiki/` 复利资产**——LLM 拥有这一层（5 个内容页子目录 + index.md）。人类**不写**
   wiki 内容，只读 + 提问题。每次摄入新资料或回答新问题，wiki 都变得**更厚**而不是更乱。
3. **`MEMORY/` agent 持久化记忆（与 `wiki/` 平级）**——LLM agent 工作中沉淀的经验 /
   踩坑 / 用户偏好，用户不写。为什么放 `<wiki-root>/` 而非 `wiki/` 内：物理位置跟逻辑
   分层对齐（独立于 wiki/ 内容），将来 publish 时自然留作私有层不外传。`MEMORY.md`
   是索引单一真源（无 frontmatter），AGENTS.md 顶部 `@MEMORY/MEMORY.md` 加载，改只改
   这一处、无副本漂移。操作细则在核心原则 §9 + 工作流 §4 + spec §5。
4. **`AGENTS.md` 纪律配置（SSOT）+ `CLAUDE.md` 薄壳**——把"wiki 怎么写 / 写什么 /
   不写什么"的约定集中到 `AGENTS.md`（工具无关单一真源），是维护本 wiki 的 agent 的
   "宪法"；`CLAUDE.md` 是 `@AGENTS.md` 薄壳（`yzr-multi-agent-context` 方法：一套真源、
   多 agent 兼容）。顶部 `@MEMORY/MEMORY.md` + `@scripts/SCRIPTS.md` 两行 `@import` 收口 +
   强制 Read 指令兜底（spec §5.1 + §14.3）。没有它，LLM 会退化成普通聊天机器人；
   有它，LLM 是"纪律严明的 wiki 维护者"。

### 四个核心操作——为什么是四个

ingest / query / lint / migrate 四个操作各自**双向回报**：ingest 让 query 更好用；
query 让 wiki 更厚；lint 让 ingest 不会越积越乱；migrate 让长跑 1-2 年的 wiki 在
spec 演进时不掉队。**单独跑任一个都亏**——这就是"复利"的本质。migrate 与其他三个
不同——它是**周期触发**而非每次 wiki 操作触发（spec 升版本时才跑），但缺了它老 wiki
会**腐烂在格式层**而不是内容层，更难察觉。四者的输入 / 输出见「输入 / 输出 · 操作产物」。

## 执行原则 / 边界

### 核心原则

> **操作前置（orient ritual，所有操作通用）**：每次 ingest / query / lint 启动前，**不依赖 symlink**
> ——按以下顺序读完四件套再动手：
>
> 1. `Read <$LLM_WIKI_ROOT>/AGENTS.md`——拿到本 wiki 的主题名、边界配置、
>    Page Thresholds（纪律 SSOT 是 `AGENTS.md`；`CLAUDE.md` 是 `@AGENTS.md` 薄壳，不持纪律）。
>    AGENTS.md 不含 tag 白名单（在 `wiki/tags.md`——见本节 §核心原则 §11）。AGENTS.md
>    顶部一行 `@MEMORY/MEMORY.md` + 一行 `@scripts/SCRIPTS.md` `@import`——自动展开 `@import`
>    的 agent 透明拿到 MEMORY / scripts 全文，不展开的由 AGENTS.md 顶部强制 Read 指令兜底
>    （详见 [`references/agents-md-template.md`](references/agents-md-template.md) 顶部）。**别处由 skill
>    按需读 AGENTS.md 时** 也走相同的 `@import` 链路，
>    **不**需要单独 `Read MEMORY.md` 补齐索引（除非要看各 `<slug>.md` 正文）。
> 2. `Read <$LLM_WIKI_ROOT>/wiki/index.md`——知道有哪些页、分布在哪些类别，避免重复创建 / 漏交叉引用
> 3. `Read <$LLM_WIKI_ROOT>/wiki/log.md`（最近 ~30 行即可）——看清最近活动，避免重复
>    ingest / 漏归档旧工作
> 4. **`Read <$LLM_WIKI_ROOT>/scripts/SCRIPTS.md`**（按需）——确认本 wiki 是否有
>    项目级扩展脚本的**完整分节契约**（使用场景 / 调用约定 / 作用 / 前置依赖）；不强制（wiki 可无
>    scripts/），但**触发非标工作流前**必须先查（AGENTS.md 顶部的 `@scripts/SCRIPTS.md` import
>    已加载全文，详细契约随读出）
>
> 四件套任一未读完不写任何 wiki 内容。100+ 页的 wiki 还应在 `wiki/` 全域
> `Grep "<topic>"` 补一次——单看 index.md 可能漏掉 entity/concept 页之间的引用关系。

1. **raw/ 由用户掌控，LLM 只读**（schema 见 `<wiki-root>/AGENTS.md` §一）——LLM 从不写/删/移 `raw/` 下文件；
   用户可随时新增/更新 raw/（重新剪藏、重存 PDF 都算），改动由 ingest 重新消化（更新对应 source 页正文 +
   `updated`，`ingest_diff.py --check-stale` 按 mtime vs source `updated` 标记待重新摄取项）
   **两处写权限例外**：
   - `raw/external/` 顶层（**扁平布局**）下 LLM 可主导创建 symlink + 写 anchor 的
     `[[entry]]` 块（详 §1 批处理摄取外部代码仓子节 + wiki-spec §13.3）。`raw/external/`
     接入的 **target 仓内文件**按角色分：wiki 维护操作（ingest / query / lint / migrate）
     中只读；**用户明确要求的开发协作**（修 bug / 重构）不属 wiki 操作、不受 raw/ 只读约束
     （target 在仓外、由用户全权处置）——详 wiki-spec §13.3
   - `raw/discussions/` 用户 + LLM **双方可写**的协作草稿层（不要求 frontmatter / 不进
     index / 不写 log；`ingest_diff` 跳过、`raw-modified` lint 排除、`sources:` 不得指向它）；
     草稿消化进 wiki 两条路（消化式 / 转正式 `mv`）都需用户确认——详 wiki-spec §15
2. **wiki/ 由 LLM 撰写**——用户从不手写 wiki 页面（编辑 AGENTS.md 除外，那是 schema）
3. **AGENTS.md 是 schema 不是文档**——它承载 wiki 的纪律配置，不往里塞内容（完整纪律见
   [`agents-md-template.md`](references/agents-md-template.md) §七「本文件本身的纪律」）。
   **写新纪律先判归属**：过在场 / 状态 / 人格三测试（wiki 属性）→ 写模板；干活方法 /
   工具 / 路由 → 留本文件——判据 SSOT 见 [wiki-spec.md §2](references/wiki-spec.md#2-agentsmdssot--claudemd薄壳)
4. **每次写入必更 log.md——追加一律走 `wiki_write.py log`**（格式 + 满
   `LOG_RETENTION_LIMIT` 自动截断由脚本保证，见 §设计决策「机械 vs 判断」）；lint
   `log-format` / `log-truncation-recommended` 只兜底带外手改
5. **每页必带 YAML frontmatter——新建页走 `wiki_write.py new`**（5 必填（`title` /
   `type` / `created` / `updated` / `tags`）+ 推荐 `description`（`index.md` 条目摘要
   从它来）由脚本脚手架保证；slug 校验 + 拒覆盖）。
   **为什么是这 5 个**见 [wiki-spec.md §9](references/wiki-spec.md)（OKF 字段齐全性 × lint
   一致性的最小交集；少于 5 字段会让"抓腐烂"判定失效）。
   **例外**：
   - `wiki/index.md` = **6 键必填**（5 必填 + `okf_version`）/ `wiki/log.md` = **5 键必填**
     （均省 `description`）
   - `MEMORY/MEMORY.md` / `wiki/tags.md` = **无 frontmatter**（索引片段 + tag 白名单）
   - `MEMORY/*.md` = **仅 `title` 必填**（其余 5 字段全 optional——MEMORY 是 agent
     私有记忆，frontmatter 是可选 decoration）；`type` 若取扩到 7 类（5 内容页 + `memory` /
     `memory-entry`）；`tags` 若取**不**走 `wiki/tags.md` 白名单；`reviewed` / `reviewed_at`
     不进 lint 兜底（MEMORY 无"人工 review"语义角色）
   **权威定义**（`type` 取值 / reserved 规则 / `sources` 字段特化 / 可信度信号
   `reviewed` / `contested` / `contradictions`）见 [`references/page-templates.md`](references/page-templates.md) §一
   ——本条不重抄，lint 阈值同步以该处为准。**`tags` 管理见 §核心原则 §11**。
6. **交叉引用走相对路径**——`[link](sources/bigtable.md)`，不用绝对路径，不用 wikilink
7. **index.md 是 wiki 内容页的单一入口**——所有非 log / 非 MEMORY 的页面必须在 `wiki/index.md` 中出现
8. **query 的好答案必问"是否归档"**——能写回 wiki 的不要浪费在聊天里
9. **`MEMORY/` 是 LLM agent 的私有记忆**——遇到踩坑、发现用户偏好、跨 ingest 关联
   时主动追加；**新条目走 `wiki_write.py memory add`**（frontmatter 仅 `title` 必填 +
   原子追加 `MEMORY.md` 索引行，`memory-not-indexed` 创建期免疫）；**不在 index.md
   强制列出**。MEMORY 沉淀只改 `MEMORY.md` 这一份、无副本漂移。写入流程见工作流 §4。
10. **LLM 修改已审核页必须清 `reviewed` 戳——每次编辑后跑 `wiki_write.py touch`**
    （自动 `updated`=现在 + 删 `reviewed` / `reviewed_at`，见 §设计决策「机械 vs 判断」）；
    `lint_wiki.py` 用 `reviewed-stale` 兜底。完整生命周期规则见
    [`agents-md-template.md`](references/agents-md-template.md) §二「认知质量信号」（纪律 canonical 副本）。

11. **tag 白名单在 `wiki/tags.md`**（详
   [wiki-spec.md §9.1](references/wiki-spec.md#91-tag-白名单来源)）——LLM auto-extend bullet +
   用户审计循环（删 bullet → 下次 lint 报 `tag-not-in-taxonomy` 由用户裁定）；`wiki/tags.md` 无
   frontmatter，与 `MEMORY/MEMORY.md` 同形态。跨 spec 升级走 `lint_wiki.py --check-version --apply`。
   `agents-md-template.md`「Tag Taxonomy」段承载同一规则（纪律 canonical 副本 = 模板，wiki 侧 AGENTS.md 由它渲染）。

12. **本 wiki 自维护脚本走 `<wiki-root>/scripts/` + `SCRIPTS.md` 索引**（详
   [wiki-spec.md §14](references/wiki-spec.md#14-scripts本-wiki-仓扩展脚本目录)）——`SCRIPTS.md`
   单段形态：每脚本以 `` - `<name>` — <一句话用途> `` one-liner 起头 + `### <name> — <label>`
   子节含 4 要素契约（使用场景 / 调用约定 / 作用 / 可选前置依赖）。AGENTS.md 顶部
   `@scripts/SCRIPTS.md` `@import` 自动加载全文——agent **必须**先看该索引行知道有哪些脚本，
   再按需 `Read scripts/SCRIPTS.md` 取完整契约（`@import` 展开后即见），按"调用约定"显式执行，
   **不**自动遍历 `scripts/`；改脚本只改 `SCRIPTS.md` 这一份。`scripts/` 不走 §9 5 必填、
   不参与 `lint_wiki.py` 扫描、不复制 skill 自带脚本（版本漂移风险）。
   `agents-md-template.md`「scripts/ —— 本 wiki 仓的自维护脚本目录」段承载同一规则（canonical 副本 = 模板）。

13. **yzr 个人工作习惯**——**canonical 副本 =
    [`agents-md-template.md`](references/agents-md-template.md) §九**（纪律正文唯一维护点；
    习惯清单以该节为准，此处不枚举——增改习惯只改模板，不动本文件、不升
    `wiki_spec_version`，老 wiki 由 `agents-md-template-sync` 字节比对独立探测后重渲染）。
    触发本 skill 的会话对用户输出前先 `Read` 该段一次——这些习惯适用于一切面向用户的输出。

### 边界

- **不**编辑 `raw/` 下任何文件——LLM 只读（两处写权限例外：`raw/external/` symlink 接入 +
  `raw/discussions/` 协作草稿；完整规则见核心原则 §1 + spec §13.3/§15，**不得外推**到
  papers / articles / clippings 等其他子树——滑坡防线见 spec §15.4）
- **不**删除 `wiki/` 下的页面——用 `archived: true` 标记 + 从 index 移除；想真删直接删文件（启用 git 时用 `git rm`，未启用时用普通 `rm`）
- **不**绕过 `AGENTS.md` 自创约定——若 AGENTS.md 没说的，**先问用户**再写
- **不**在 query 时偷偷归档——必须先展示答案 + 询问用户
- **不**忽略 lint 报告——长期不 lint 的 wiki 一定会腐烂
- **不**用 git 操作破坏 raw/ 不可变性——`git clean` / `git checkout -- raw/` 仅在启用 git
  时适用；未启用 git 时没有"未提交改动"概念（lint 自动跳过此项）
- **不**对 wiki 内文件用 Read 之外的工具做"自动"修改——所有修改走 Edit / Write 并
  走 schema 约定
- **不**忽略 `scripts/SCRIPTS.md` 索引直接遍历 `scripts/` 跑脚本——必须先 `Read` 索引定位工具
  - 按段中调用约定执行（详见核心原则 §12）

### 反模式（绝对禁止）

- 在 wiki 页面里手写"先写一段话再贴图"等散文式总结（散弹式散落口径冲突的根源）
- 把同一个概念分散在多个 entities/ 文件里（必须先 search 是否已有同名页）
- 改 wiki 不追加 log 条目就收工——失去操作语义记录（正路：`wiki_write.py log`，
  见核心原则 §4）
- 跨 wiki 互引但不更新对端 index（两套 wiki 同步是用户的责任）
- 用 Obsidian-only 语法（`[[wikilink]]`、`![[embed]]`）——本 skill 假设通用 Markdown
- 把 yzr-llm-wiki-management skill 自带脚本（lint_wiki.py / ingest_diff.py / log_format.py /
  wiki_write.py / check_wiki_fixtures.py）
  复制进 `<wiki-root>/scripts/`——SSOT 在 skill 仓；本 wiki 自维护脚本必须同时更新 `SCRIPTS.md` 索引段
- 把外部代码仓接入走 `cp -r` 内嵌到 `raw/` 而非 `raw/external/` symlink——失去
  commit 锚点 + 占用空间 + 违反 spec §13 纪律
- 修改 anchor 的 `remote_url` / `commit` / `branch` 三字段——这三字段是接入意图，
  不是机器状态（详见 [`references/external-repo-rebuild.md`](references/external-repo-rebuild.md)）
- 绕过 anchor 直接 `ln -s`——没有对应 `[[entry]]` 的 symlink = lint 报
  `external-anchor-orphan`
- 在 `raw/external/` 下开 `<source-name>/` 子目录——扁平布局，
  所有 symlink 直接 in `external/`；违规子目录会被 lint 报 `external-source-name-invalid`
- 把 `raw/discussions/` 或 `raw/external/` target 的可写性**外推**到 raw/ 其他子树——
  "discussions/ 能改，papers/ 我也能改" / "target 能改，raw/ 也能改" 是典型滑坡
  （discussions/ + external/ 是**仅有的**两处例外，其余 raw/ 子树 LLM 只读；防线见 wiki-spec §15.4）
- 让 `type: source` 页的 `sources:` 指向 `raw/discussions/`——草稿不是真相源，
  lint 报 `source-in-discussions`（error）；要引用先走 wiki-spec §15.3 转正式
- 用 `raw/discussions/` 规避 ingest 纪律——把草稿内容塞进 wiki 页却不走 log / index /
  清 `reviewed` 戳，即绕开 §15.3 provenance 约束

### 反合理化三件套（纪律型 skill 必带）

> 本 skill 含 14+ 行"必须 / 禁止 / 不"+"**不**" 起始段 = 纪律型。纪律型禁令在
> LLM 压力下会被以各种合理化借口绕开——三件套只堵一类：**已被合理化的违反**。
> 未被合理化的违反（直接忽略规则）= 缺 §反模式 清单本身，与三件套无关。

#### Rationalization Table

> **baseline 实跑记录（2026-08-16，0.33.0 审计）**：3 次 RED 运行——① 带纪律 ingest
> 任务：全程合规零借口；② 无纪律 ingest 任务（Iron Law 创建场景）：仍合规（模型自带该
> 规范知识）；③ 带纪律 + 用户施压任务（"随便记一下 / 赶时间"）：产出真实借口一条（下表
> 第 1 行）+ 一处静默遗漏（frontmatter 缺必填 `tags` 字段，无借口直接漏掉）。

| 常见借口 | 为什么是错的 | 应改做什么 |
| --- | --- | --- |
| "剪藏只有一句话，按'克制建页'原则和你说的小事轻办，一个资料页够了"（2026-08-16 实跑 transcript） | 用户的"随便 / 赶时间"是态度不是豁免——写 wiki 页即触发 5 必填 / 建页阈值 / log 纪律；"轻办"是拿用户情绪当省略纪律的挡箭牌（同轮还静默漏了必填 `tags` 字段） | 流程不缩水；"克制建页"判断如实执行但**向用户说明**（"本文只有一个中心主题，暂不建概念页，出现第二篇同主题再补"），字段与 log 纪律照走 |
| "用户没明说要我做这一步" | 本 skill 的纪律点（log / lint / reviewed 戳 / 等）触发条件是**事**而非**人**——写了 wiki 页就是触发 lint，写了 source 就是清 reviewed 戳——用户没说 = 沉默 ≠ 豁免 | 先按 §执行原则走完纪律，再决定是否省略；省略要写明理由进 log 条目 |
| "这次是单页 ingest，跳过 entity/concept 同步更快" | 知识孤岛 = wiki 复利亏空——单页也一样要 cross-link；"更快"是把当前 case 凌驾于复利结构之上 | 哪怕只挂 1 个 entity 页也要同步；交叉引用是 wiki 的 ROI 核心 |
| "我把 source `cp` 进 raw/ 比走 `Write` + 创建 page 更直接" | raw/ 不可变 + raw/external/ 例外是 symlink 不是 cp——`cp` 进 raw/ 触发 `raw-external-anchor-mismatch` 一连串 finding | 用 `Edit/Write` 写 wiki/sources/`<slug>`.md；raw 是用户私有 |
| "`reviewed: true` 是一周前人标的，我没改多少内容，留着就行" | `reviewed: true` 是"这一刻内容背书"快照，**任何** LLM 对正文的修改都让它失效（包括 typos / 字段补全）——留戳 = 假装审过 | 任何 Edit/Write 后**必须**删 `reviewed` + `reviewed_at` 两字段，回到默认未审核态 |
| "外部代码仓我 cp -r 进 raw/ 也算接入，symlink 没必要" | cp -r 失去 commit 锚点 + 占用 wiki 仓磁盘 + 违反 spec §13——"也算"是把"接入意图"和"接入手段"混淆 | 走 `ln -s` 创建 symlink + 写 `.symlink-anchor.toml` 的 `[[entry]]` 块 |
| "这个 wiki 没 git，不写 log 也行" | log.md 记的是**操作语义**（ingest/query/lint）+ 近期活动速览（orient ritual 读它避免重复工作）——这是 git diff 不直接体现的；完整文件历史才靠 git | 任何 wiki 改动**必须**追加 log 条目（哪怕 wiki 无 git） |

> **表内条目两类**：第 1 行 = 实跑 transcript 逐字摘录；其余 6 条 = 从 §反模式 / §边界
> 反推的**嫌疑清单**（多次 baseline 未复现）——保留为未来实跑验证 / 替换的候补。保持
> "只收录 agent 实际说过的"原则：实跑复现即替换 / 未复现不新增（预写 = 噪声 + 信号干扰）。

#### 违反字面 = 违反精神

任何对 §核心原则 / §边界 / §反模式 三段禁令的"看起来不同但效果一致"绕法都算违反——本 skill 常见绕法前三：

- 把 `Edit` / `Write` 改为 `Read` + 手动生成新内容再 `Write`——**不算**绕开"用 Read 之外工具做自动修改"禁令，操作工具是 Write 一样算
- 把"不删除 wiki 页"解释为"先把内容拷出去再 `rm` 然后写回"——**不算**绕开不删禁令，状态效果完全等同
- 把"raw/ 由用户掌控，LLM 只读"解释为"我`cp` 进 raw/ 后立即再`rm`，窗口里我读到了内容 = 等价于只读"——**不算**，写入发生在第一步

**禁止**用"严格按字面 / 严格按精神"二选一措辞给 agent 留退路——任何"看起来不同但效果等价"都是违反。

#### Red Flags（念头清单 — 出现即停）

念头出现 ≠ 已违反；念头 = 警告 = 重读 §核心原则 / §边界 / §反模式 三段。

- "用户说'随便记一下 / 赶时间 / 别太正式'——纪律可以打折了"（2026-08-16 实跑观察）
- "我觉得这一步对当前 case 不必要"
- "用户没明说要我做这步"
- "这样更快 / 更省 token / 更高效"
- "spec 没禁止"
- "我已经做了等价的事" / "效果一样不算违反"
- "先这样留着，回头再补"
- "我自己生成字段比 frontmatter 严格写更灵活"
- "log 条目这次先跳过，反正是 wiki 不是 git"
- "raw 反正用户也天天改，我帮一下忙"
- "lint 报了一堆，反正都是 warn 不算错"

> 没有"念头清单 = 已违反"的递进——念头出现是**信号**，再走下去才成**行动**。
> 但**念头后仍继续** = 默认承担违反精神的责任。

## 工作流 / 步骤

### 0. 一次性 setup（首次使用）—— 由 workspace CLI 完成

> **职责边界**：本 skill 只负责 wiki 的**成长阶段**（ingest / query / lint）。
> wiki 仓的**创建与删除**由外部 workspace CLI 负责——CLI 命令名与参数
> 见 CLI 仓的文档，本 skill 不绑死任何 CLI 实现。
> wiki 仓的"出生形态"契约见 [`references/wiki-spec.md`](references/wiki-spec.md)——
> CLI 实现与 SKILL 之间的接口。

**基本流程**：

```bash
# 1. 调 workspace CLI 创建 wiki 仓（具体命令以 CLI 文档为准）
workspace wiki init "LLM Systems"
# CLI 按 wiki-spec.md 落盘：目录结构 + AGENTS.md（SSOT）+ CLAUDE.md（薄壳）+
# wiki/index.md + wiki/log.md + .gitignore + scripts/SCRIPTS.md +
# git 默认跳过（用户 --git opt-in 时才 init）。完整产物清单见 wiki-spec.md §1-§7。

# 2. 把原始资料放进 raw/（用户手动 / Obsidian Web Clipper / 浏览器下载）
cp ~/Downloads/some-article.md ~/wiki/<topic-name>/raw/articles/
```

**LLM agent 接管后做什么**：

1. 验证 CLI 落盘——读 `<wiki-root>/AGENTS.md` 确认主题名 + 日期替换正确；
   `wiki/index.md` / `wiki/log.md` 存在且 frontmatter 完整；`<wiki-root>/CLAUDE.md` 是薄壳
2. 跑 orient ritual（见 §执行原则 / 边界 顶部引用块）
3. 询问用户是否做首次 ingest——若是，把第一份资料路径给 agent

**为什么 setup 与日常分两层**：CLI = 出生/死亡（一次性，结构稳定），LLM = 成长（高频交互）。
最大收益是 **wiki schema 与 LLM 工作流解耦**——CLI 可独立升级实现（Python → Rust），
SKILL 不动。

### 1. Ingest（摄取新资料）

**触发**："把这篇摄取到 wiki" / `raw/` 有新文件 / 跑 `ingest_diff.py` 发现未摄取项。

**流程摘要**（agent 驱动；详细 7 步 + 批处理见
[`references/ingest-workflow.md`](references/ingest-workflow.md)；外部代码仓 5 步接入 /
漂移刷新 / 跨主机重建见 [wiki-spec §13.3](references/wiki-spec.md#133-责任切分用户--llm-共有) 与
[`references/external-repo-rebuild.md`](references/external-repo-rebuild.md)）：

1. 跑 `scripts/ingest_diff.py <wiki-root>`（日常加 `--check-stale`）找出未摄取/待重摄文件清单
2. **单篇对一下要点**——仅交互式单篇或少量场景：确认主题方向 / 重点交叉的 entity / 用户判断要保留
3. 对每个文件：Read 全文 → 提取元数据 → `wiki_write.py new --type source ...` 建骨架 →
   写正文（stale-raw 走 **Edit**,**不** Write 覆盖）→ 同步 entity/concept(只 append
   "Sources" 段) → `wiki_write.py index add` → `wiki_write.py log --op ingest` →
   **编辑过的页跑 `wiki_write.py touch`**
4. **commit**（仅启用 git 时）：节奏由用户/agent 决定，**不**自动 commit

### 批处理摄取（≥ 3 份 raw 同时摄入）

走批处理路径而非逐份。**一次聚合、一次写入、一次索引**——避免 N 次重复 search / N 次
index 更新 / N 条 log。5 步流程 + 为什么批处理 + log 标题前缀 `Bulk:` 的细节见
[`references/ingest-workflow.md`](references/ingest-workflow.md)「批处理」节。

**外部代码仓作为语料**——若用户说"把 X 仓库纳入 wiki"：**不**内嵌拷仓，走
[`wiki-spec §13`](references/wiki-spec.md#13-rawexternal外部代码仓接入可选) 的 symlink 路径
（`raw/` 总纪律的**写权限例外之一**——LLM 主导接入；另一处例外是 `raw/discussions/`
协作草稿，见 [wiki-spec §15](references/wiki-spec.md#15-rawdiscussions协作草稿层可选)）。
5 步接入（确认 symlink/target → LLM 验证 → 读
git 扩展字段 → 创建 symlink + 写 anchor → 后续 `ingest_diff` 扫描）+ 漂移刷新 + 跨主机
重建见 [`references/external-repo-rebuild.md`](references/external-repo-rebuild.md)。

### 2. Query（跨页综合）

**触发**："wiki 里有 X 吗" / "总结 wiki 中关于 Y 的内容" / "对比 A 和 B"。

**流程**：

1. **先看 index.md**——按关键词 / 类别找候选页
2. **读相关页**（不读 raw——raw 已经在 source 页里消化过）
3. **跨页综合**——用引用形式带 source 链接；矛盾处显式标注："A 说 X（来源：...），
   B 说 Y（来源：...），需要更深入调研"
4. **展示答案 + 询问归档**——如果答案有"对比 / 综合 / 发现联系"的性质，询问用户：
   "这段答案适合归档回 wiki 作为 comparisons/`<slug>`.md 吗？"
5. **用户同意后归档**——走 references/page-templates.md 的 `comparison` 或
   `synthesis` 模板 + 追加 log 条目

详细 query 流程与判定规则见 [`references/query-workflow.md`](references/query-workflow.md)。

### 3. Lint（健康检查）

**触发**："lint wiki" / 定期（频率阈值见 [lint-checklist.md §七](references/lint-checklist.md#七lint-频率)）/ 大型 wiki 主动建议。

**流程**：

1. 跑 `scripts/lint_wiki.py <wiki-root>` 做 deterministic 检查
2. 脚本覆盖（大类如下，权威清单见 [`references/lint-checklist.md`](references/lint-checklist.md)）：
   raw 不可变性 / frontmatter 字段 / 孤儿页 / 断链 / log.md 格式 / 过期摘要 / 页面体量
   / 认知质量与可信度信号（`reviewed` / `contested` / `contradictions`）/ `raw/external/`
   symlink ↔ anchor 关联（spec §13）/ fixtures 一致性（见下文「fixtures 一致性检查」段）
3. 脚本输出后 **agent 还要做半定性检查**：矛盾主张 / 缺失交叉引用 / 建议新摄取方向
4. 报告 + 询问用户哪些修

详细 checklist 见 [`references/lint-checklist.md`](references/lint-checklist.md)。

### 4. Memory（写入 LLM agent 持久化记忆）

**触发**：在 ingest / query / lint 过程中识别到值得沉淀的信息——踩坑、用户偏好、跨文档关联。

**何时写**：

- 遇到踩坑（例：raw/ PDF 频繁 OCR 错误，下次让用户先转格式）
- 发现用户偏好（例：用户偏好表格化对比、不喜散文式总结）
- 跨 ingest 关联（两 source 页指向同一论文不同章节）
- lint 报告的 recurring pattern（每次 lint 都报某 type 缺字段）

**流程摘要**（agent 主动；frontmatter 字段 / 索引同步 / 完整 vs 短条目判定的权威定义在
[spec §5](references/wiki-spec.md#5-memory) + §5.2 + 仓库根 `MEMORY/MEMORY.md` 索引自身的写法）：

1. 决定是否值得写——能否让未来 agent 工作更顺？
2. 判别条目形式：**完整**（含 why+how 上下文）→ `wiki_write.py memory add --slug ... --title ...`
   建文件 + 索引行，再 Edit 写正文；**短**（纯 reminder）→ 直接 `MEMORY/MEMORY.md` 加一行索引
3. 写正文——记录具体经验，含上下文 / 解决步骤 / 未来如何避免
4. **不**追加 log 条目 / **不**在 wiki/index.md 列出（MEMORY 不走单一入口约束）

**纪律**：

- 不删除任何 MEMORY 文件——踩坑记录沉淀下来
- 写新文件时保留原 `created` 字段；只更新 `updated`
- 用户**不**直接编辑 MEMORY/——若用户想补充，先转告 agent 由 agent 写入

### 5. Migrate（升级 wiki spec）

**触发**：用户说"升级 wiki / 迁移 / 检查 wiki 版本 / 老格式 / spec 升级 / 是否需要
reformat"；或 `lint_wiki.py` 报告 `legacy-confidence-field` 等迁移期 warn。

**职责切分**（避免与 ingest / lint 混淆）：

- **脚本**（`scripts/lint_wiki.py --check-version`，**含**自动调 `check_wiki_fixtures.py`
  扫约定文件）= 探测器，只扫不修，输出报告 / `--apply` 时 stdout 输出 migration plan
- **agent** = 修复者，按 stdout 返回的 migration plan（actions[] 自带
  remove/add_or_modify/to_action）
  用 Edit/Write 改
  frontmatter / 移文件 / 补索引 / 同步 AGENTS.md 到模板（全量重渲染，wiki-spec §10.1）；
  走 plan.fixtures_actions[] 修约定文件；
  语义合并按 [`references/migrate-workflow.md` §六](references/migrate-workflow.md#六语义合并规则) 走
- **迁移期不走 `wiki_write.py`**——迁移 = 格式流动期，机械写命令只认识当前形态
  （准入规则例外，见 §设计决策「机械 vs 判断」）
- **迁移依据 SSOT** = plan actions[] + migrate-workflow.md §六（语义合并）——
  不另设历史档案；fixtures-check 的语义合并
  走 migrate-workflow.md §六（与 §三 字节合规分离）
- **不**追加 log 条目（迁移是脚本运行，不是 wiki 操作事件）

**fixtures 一致性检查**——`--check-version` 自动调 `scripts/check_wiki_fixtures.py`
扫 wiki 仓 10 类约定文件（AGENTS.md §八 / .gitignore / index.md / log.md / tags.md /
MEMORY/MEMORY.md / MEMORY/*.md 条目 / SCRIPTS.md / .symlink-anchor.toml /
wiki_metadata.toml），finding 并入
`migration plan`（stdout JSON 输出）的 `fixtures_actions[]`（与 legacy `actions[]` 平行）。检查项数同
`metadata.fixtures_check_count`（结构探测 + 骨架字段比对两类，breakdown 见
[`references/lint-checklist.md`](references/lint-checklist.md)；其中 `agents-md-template-sync`
对 AGENTS.md 整文做**模板渲染字节比对**——不一致走全量重渲染 + 本地定制搬
MEMORY/，详见 wiki-spec §10.1）。**简要流程** + 详细步骤 + 字段清单见
[`references/migrate-workflow.md`](references/migrate-workflow.md)。

## 参考样例

5 个完整样例（setup / ingest / query / lint / migrate）见 [`references/examples.md`](references/examples.md)——按需 Read。
