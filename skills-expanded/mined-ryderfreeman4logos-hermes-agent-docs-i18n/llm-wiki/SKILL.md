---
name: llm-wiki
description: "Karpathy's LLM Wiki: build/query interlinked markdown KB."
version: 2.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
    category: research
    related_skills: [obsidian, arxiv]
---

# Karpathy的LLM维基

通过相互关联的Markdown文件来构建并维护一个持久、不断扩展的知识库。
该架构基于[Andrej Karpathy的LLM维基模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

与传统RAG系统（每次查询都需要从头重新检索知识）不同，该维基只需构建一次知识库即可保持其最新状态。其中的交叉引用早已设定完成，矛盾之处也会被标记出来，同时所有收录的内容都会被综合呈现。

**分工协作：** 由人类负责筛选资料并指导分析工作；而智能体则负责总结内容、建立交叉引用、整理文件，并确保整体一致性。

## 何时启用此技能

当用户出现以下情况时，可使用此技能：
- 要求创建、搭建或启动一个维基或知识库
- 要求将某些资料导入、添加到或处理其维基中
- 提出问题且配置路径下已存在相关维基
- 要求对维基进行代码检查、审计或健康状况检测
- 在研究过程中提及自己的维基、知识库或“笔记”

## 维基存储位置

**位置：** 通过`WIKI_PATH`环境变量设定（例如在`${HERMES_HOME:-~/.hermes}/.env`文件中）。

若未设置该变量，则默认存储路径为`~/wiki`。

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

该维基实际上只是一个包含 Markdown 文件的目录——你可以在 Obsidian、VS Code 或任何其他编辑器中打开它。无需数据库，也不需要任何特殊的工具。 

## 架构：三层结构

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only, rotated yearly)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── entities/           # Layer 2: Entity pages (people, orgs, products, models)
├── concepts/           # Layer 2: Concept/topic pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**第一层——原始数据源：**不可更改。智能体仅可读取这些数据，绝不能对其进行修改。
**第二层——维基页面：**由智能体管理的 Markdown 文件。这些文件由智能体创建、更新并实现相互引用。
**第三层——架构规范：**`SCHEMA.md` 文件用于定义数据结构、编写规范以及标签分类体系。

## 恢复现有的维基页面（非常重要——每次会话都必须执行）

如果用户已有现有维基页面，在开始操作之前**务必先了解以下内容**：

① **阅读 `SCHEMA.md`** — 了解相关领域、编写规范以及标签分类体系。
② **阅读 `index.md`** — 了解现有的页面及其概要。
③ **查看最近的 `log.md`** — 阅读最近20-30条记录，以掌握近期活动动态。

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
# Orientation reads at session start
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

只有在完成定向设置之后，才应进行数据导入、查询或代码检查操作。这样做可以避免以下问题：
- 为已存在的实体创建重复页面
- 丢失对现有内容的交叉引用
- 违反架构规范
- 重复处理已记录的工作内容

对于规模较大的维基（页面数超过100页），在创建新内容之前，还应先针对当前主题快速执行`search_files`操作。

## 初始化新维基

当用户要求创建或启动一个维基时，请按以下步骤操作：

1. 确定维基路径（可从环境变量 `$WIKI_PATH` 中获取，或询问用户；默认值为 `~/wiki`）
2. 创建上述目录结构
3. 询问用户该维基涵盖的领域——请给出具体说明
4. 根据对应领域编写定制化的 `SCHEMA.md` 文件（参见下方模板）
5. 编写包含分节标题的初始 `index.md` 文件
6. 编写包含创建记录的初始 `log.md` 文件
7. 确认维基已准备就绪，并推荐首批需要导入的资料来源

### SCHEMA.md 模板

需根据用户的领域进行相应调整。该架构规范能够约束智能体的行为，确保一致性：

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source. This lets a reader trace each
  claim back without re-reading the whole raw file. Optional on single-source pages where the
  `sources:` frontmatter is enough.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence`与`contested`为可选字段，但针对观点性强或变化迅速的主题，建议使用这些字段。Lint工具会标记出`contested: true`且`confidence: low`的页面以便人工审核，从而防止那些站不住脚的论断悄无声息地变成被广泛认可的维基事实。

### 原始内容/前置数据

原始来源也会包含一小段前置数据，以便在重新导入时能够检测内容偏差：

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

`sha256:` 标签可让未来在重新导入相同 URL 时，若内容未发生变化则跳过处理；而一旦内容发生变动，则会标记出差异。该标签仅对内容主体（即 `---` 结尾之后的所有内容）进行计算，不会涉及前置元数据。

## 标签分类体系
请为该领域定义 10–20 个顶层标签。在使用新标签之前，请先将其添加至此列表中。

以人工智能/机器学习领域为例：
- 模型相关：model、architecture、benchmark、training
- 人物/机构：person、company、lab、open-source
- 技术方法：optimization、fine-tuning、inference、alignment、data
- 其他类别：comparison、timeline、controversy、prediction

规则：页面上的每个标签都必须出现在此分类体系中。如果需要新增标签，需先将其添加至此列表，然后再使用。这样可以避免标签数量无序增长。

## 页面创建标准
- 当某个实体/概念出现在 2 个及以上来源中，或是一个来源的核心内容时，**创建新页面**
- 当某来源提及了已有页面已涵盖的内容时，**将该内容添加到现有页面中**
- 对于偶尔回顾的提及、次要细节或领域之外的内容，**不要创建新页面**
- 当页面内容超过约 200 行时，**拆分页面**，通过交叉链接将内容划分为多个子主题
- 当页面内容被完全替代时，**将其归档**，移至 `_archive/` 目录并从索引中删除

## 实体页面
每个重要的实体对应一个页面。页面应包含以下内容：
- 概述/定义
- 关键事实与时间节点
- 与其他实体的关联关系（[[wikilinks]]）
- 参考来源

## 概念页面
每个概念或主题对应一个页面。页面应包含以下内容：
- 定义/解释
- 当前的认知水平
- 存在的未解问题或争议点
- 相关概念（[[wikilinks]]）
## 对比页面
提供并列分析内容，应包含以下要素：
- 对比的对象及其原因
- 对比维度（建议以表格形式呈现）
- 最终结论或综合分析
- 参考来源

## 更新策略
当新信息与现有内容存在冲突时：
1. 先核对日期——通常较新的来源具有优先效力
2. 若确实存在矛盾，需同时标注两种观点，并注明对应日期和来源
3. 在前置信息中标记该矛盾点：`contradictions: [页面名称]`
4. 在代码检查报告中标出，以便用户审核
```

### index.md Template

The index is sectioned by type. Each entry is one line: wikilink + summary.

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

**扩展规则：** 当某个分类下的条目数量超过50个时，应依据首字母或子域名将其拆分为多个子分类。而当所有分类的条目总数超过200个时，则需创建一个 `_meta/topic-map.md` 文件，按主题对页面进行归类，以便更快捷地导航。

### log.md 模板

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## 核心操作

### 1. 数据摄取

当用户提供来源内容（URL、文件或粘贴文本）时，需将其整合到维基中：

① **捕获原始来源内容：**
   - URL → 使用 `web_extract` 工具提取 Markdown 格式，并保存至 `raw/articles/` 目录
   - PDF → 同样使用 `web_extract`（该工具支持处理 PDF 文件），保存至 `raw/papers/` 目录
   - 粘贴的文本 → 保存到相应的 `raw/` 子目录中
   - 为文件起一个具有描述性的名称，例如：`raw/articles/karpathy-llm-wiki-2026.md`
   - **添加原始元数据**（包括 `source_url`、`ingested` 以及内容部分的 `sha256` 值）。当再次摄取相同 URL 的内容时，需重新计算该内容的 sha256 值，并与之前存储的数值进行比对——若一致则跳过处理；若存在差异，则标记为内容变动并更新元数据。这一操作在每次重新摄取时执行成本极低，却能有效检测出来源内容的隐性变化。

② **与用户探讨核心要点**——即哪些内容值得关注，哪些对相关领域具有重要意义。（在自动化或定时任务场景下可跳过此步骤，直接进入下一步。）

③ **检查已有内容**——搜索 `index.md` 文件，并使用 `search_files` 工具查找与所提及实体或概念相关的现有页面。这正是持续完善的维基与大量重复内容之间的区别所在。

④ **编写或更新维基页面：**
- **新实体/概念**：仅当其满足 `SCHEMA.md` 中规定的页面创建标准（至少在2个来源中被提及，或为某个来源的核心内容）时，才创建对应页面。  
- **现有页面**：可添加新信息、更新事实内容，并刷新 `updated` 日期。若新增信息与现有内容存在矛盾，需遵循更新规则进行处理。  
- **交叉引用**：每篇新建或更新的页面都必须通过 `[[wikilinks]]` 标签链接至至少2篇其他页面，并确保现有页面也能相互关联。  
- **标签使用**：仅可使用 `SCHEMA.md` 中定义的分类标签。  
- **来源标注**：对于整合了3个以上来源内容的页面，需在源自特定来源的陈述段落后添加 `^[raw/articles/source.md]` 标记。  
- **置信度设置**：对于观点性较强、变化较快或仅基于单一来源的陈述，应在页面的前置信息中将其置信度设置为 `medium` 或 `low`；除非该陈述有来自多个来源的充分支持，否则不得标记为 `high`。  

⑤ **更新导航**：  
- 按字母顺序将新页面添加到 `index.md` 的相应分类下；  
- 更新索引页眉中的“总页面数”及“最后更新日期”；  
- 在 `log.md` 中添加如下格式的记录：`## [YYYY-MM-DD] ingest | Source Title`，并在该条目中列出所有被创建或更新的文件。  

⑥ **报告变更内容**——向用户列出所有被创建或更新的文件。  

单个来源通常会触发5至15篇wiki页面的更新，这是正常且期望的现象，属于累积效应所致。  

### 2. 查询  

当用户就wiki的知识领域提出问题时：

① **阅读 `index.md`** 以找到相关页面。  
② **对于页面数量超过100个的维基**，还需在所有 `.md` 文件中通过 `search_files` 搜索关键术语——仅依赖索引可能会遗漏相关内容。  
③ 使用 `read_file` 函数读取相关页面。  
④ 根据收集到的信息整合出答案，并注明所参考的维基页面：“基于 [[page-a]] 和 [[page-b]]……”  
⑤ **保存有价值的答案**——如果答案是深度对比、深入分析或创新性整合内容，可在 `queries/` 或 `comparisons/` 目录下创建新页面；切勿保存简单的查询结果，仅保留那些重新生成会非常耗时的答案。  
⑥ 在 `log.md` 中记录查询内容以及是否已保存结果。  

### 3. 代码检查  

当用户要求对维基进行代码检查、健康状况检测或审计时：  

① **孤立页面**：查找没有其他页面通过 `[[wikilinks]]` 链接指向的页面。
```python
# Use execute_code for this — programmatic scan across all wiki pages
import os, re
from collections import defaultdict
wiki = "<WIKI_PATH>"
# Scan all .md files in entities/, concepts/, comparisons/, queries/
# Extract all [[wikilinks]] — build inbound link map
# Pages with zero inbound links are orphans
```

② **失效的维基链接**：查找指向不存在页面的 `[[links]]` 链接。

③ **索引完整性**：所有维基页面都应出现在 `index.md` 中。需将文件系统内容与索引条目进行比对。

④ **前置数据验证**：每篇维基页面都必须包含所有必填字段（标题、创建时间、更新时间、类型、标签、来源）。这些标签必须属于预定义的分类体系。

⑤ **过时内容**：那些 `updated` 时间比最新提及相同实体的来源内容早超过90天的页面。

⑥ **矛盾信息**：针对同一主题但存在相互冲突内容的页面。需找出那些虽共享相同标签/实体却陈述不同事实的页面，并将所有带有 `contested: true` 或 `contradictions:` 前置数据的页面标记出来，以便用户审核。

⑦ **质量预警信号**：列出 `confidence: low` 的页面，以及仅引用单一来源且未设置置信度值的页面——这些页面需要进一步核实信息真实性，或将其置信度下调至 `medium` 级别。

⑧ **来源文件变动**：对于 `raw/` 目录中带有 `sha256:` 前置数据的每个文件，都需要重新计算其哈希值，并标记出不一致的情况。此类差异表明该原始文件可能已被修改（本不应发生，因为 `raw/` 目录中的文件是不可变的），或是从已变更地址获取的。这虽不属于严重错误，但仍值得上报。

⑨ **页面长度**：将行数超过200行的页面标记出来，这些页面可能需要被拆分。

⑩ **标签审计**：列出所有正在使用的标签，并标记出那些不在 `SCHEMA.md` 分类体系中的标签。

⑪ **日志轮转**：当 `log.md` 的记录数量超过500条时，需对其执行轮转操作。

⑫ **报告检测结果**，需注明具体的文件路径及建议采取的措施，并按严重程度分类
  （断链 > 孤立页面 > 来源偏差 > 争议页面 > 过时内容 > 样式问题）。

⑬ **添加到 log.md 文件中**：`## [YYYY-MM-DD] lint | 发现 N 个问题`

## 维基操作指南

### 搜索

```bash
# Find pages by content
search_files "transformer" path="$WIKI" file_glob="*.md"

# Find pages by filename
search_files "*.md" target="files" path="$WIKI"

# Find pages by tag
search_files "tags:.*alignment" path="$WIKI" file_glob="*.md"

# Recent activity
read_file "$WIKI/log.md" offset=<last 20 lines>
```

### 批量导入

在同时导入多个数据源时，建议采用批量处理方式：
1. 首先读取所有数据源
2. 确定所有数据源中的所有实体与概念
3. 对这些实体和概念进行一次性检索（仅一次搜索，而非多次）
4. 一次性创建或更新对应页面（避免重复操作）
5. 最后在结束时更新一次 `index.md` 文件
6. 记录包含该批次操作信息的单条日志

### 归档处理

当内容被完全替代或领域范围发生变化时：
1. 若不存在 `_archive/` 目录，则创建该目录
2. 将对应页面连同其原始路径一起移动到 `_archive/` 目录中（例如：`_archive/entities/old-page.md`）
3. 从 `index.md` 中删除该页面的链接
4. 更新所有曾引用该页面的页面——将维基链接替换为纯文本并加上 “(已归档)” 标注
5. 记录此次归档操作

### 与 Obsidian 的集成

该wiki目录可直接作为Obsidian知识库使用：
- `[[wikilinks]]` 会显示为可点击的链接
- 图谱视图可用于可视化知识网络结构
- YAML前置数据可用于支持Dataview查询功能
- `raw/assets/` 文件夹用于存放通过 `![[image.png]]` 引用的图片

为获得最佳使用效果：
- 将Obsidian的附件存储文件夹设置为 `raw/assets/`
- 在Obsidian设置中启用“维基链接”功能（通常默认已开启）
- 安装Dataview插件，以便执行诸如 `TABLE tags FROM "entities" WHERE contains(tags, "company")` 这样的查询语句

如果同时使用Obsidian技能，需将 `OBSIDIAN_VAULT_PATH` 设置为与wiki目录相同的路径。

### Obsidian无头模式（服务器及无头设备）

在无显示器的设备上，建议使用 `obsidian-headless` 而非桌面版应用程序。该版本通过 Obsidian Sync 进行数据同步，无需图形界面——非常适合那些在服务器端编写维基内容的智能体，同时让 Obsidian 桌面版在另一台设备上读取这些内容。

**设置步骤：**
```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault for the wiki
ob sync-create-remote --name "LLM Wiki"

# Connect the wiki directory to the vault
cd ~/wiki
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

**通过 systemd 实现持续后台同步：**
```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=%h/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
# Enable linger so sync survives logout:
sudo loginctl enable-linger $USER
```

这样一来，当您在笔记本电脑或手机上的 Obsidian 中浏览同一个知识库时，该智能体便可以同时向服务器上的 `~/wiki` 文件夹进行写入操作——更改内容会在几秒钟内同步显示。 

## 常见问题

- **切勿修改 `raw/` 目录中的文件**——这些源数据是不可更改的，如有更正应记录在维基页面中。  
- **务必先了解结构**——在每次新会话执行操作前，先阅读 SCHEMA、索引及最新日志。跳过此步骤会导致内容重复和交叉引用缺失。  
- **必须及时更新 index.md 和 log.md**——忽视此要求会令维基系统功能退化，因为这两份文件是导航系统的核心支撑。  
- **不要为临时提及创建页面**——需遵循 SCHEMA.md 中规定的页面创建标准，仅在脚注中出现一次的名称无需单独创建实体页面。  
- **创建页面时必须添加交叉引用**——孤立存在的页面将无法被检索到，每页至少需链接至另外2个页面。  
- **必须使用前置数据**——它有助于实现搜索、过滤以及内容新鲜度检测功能。  
- **标签必须来自预定义的分类体系**——随意添加的标签只会造成信息混乱，应先在 SCHEMA.md 中新增标签，再予以使用。  
- **保持页面易读性**——一个维基页面应在30秒内即可读完，内容长度建议控制在200行以内，详细分析内容可移至专门的深度探讨页面。  
- **大规模更新前请先确认**——若某次数据导入会影响到10个及以上现有页面，需先与用户确认操作范围。  
- **定期轮换日志文件**——当 log.md 的记录数超过500条时，将其重命名为 `log-YYYY.md` 并重新开始记录。Agent应在代码检查阶段自动检测日志大小。  
- **明确处理矛盾内容**——切勿擅自覆盖原有数据，而应同时记录双方观点并标注日期，通过前置数据标出，以便用户审核。  

## 相关工具

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) 是一个基于 Node.js 的命令行工具，它秉承 Karpathy 的设计理念，可将各种源代码编译成概念维基。该工具兼容 Obsidian，因此那些希望使用定时任务或命令行驱动的编译流程的用户，可以直接将其指向该技能所维护的同一存储库。不过，它也存在一定的局限性：页面生成工作由该工具自行完成（从而取代了智能体在页面创建时的决策能力），且更适用于处理规模较小的语料库。若您需要智能体参与内容筛选与整理，请使用此技能；而若希望对整个源代码目录进行批量编译，则建议选用 llmwiki。
