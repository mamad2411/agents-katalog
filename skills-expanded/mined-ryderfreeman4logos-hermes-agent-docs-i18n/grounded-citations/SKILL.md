---
name: grounded-citations
description: "Ground answers and documents in cited, verifiable sources."
version: 1.2.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Citations, Grounding, Sources, Web, Reports]
    category: research
    related_skills: [arxiv, pdf, reddit-reading, rss-feeds, youtube-content]
---

# 纪实性引用机制

所有源自外部来源的陈述都会附带行内编号引用以及类似Perplexity风格的`Sources:`列表。专门的账本脚本负责管理`url → [n]`的映射关系，因此这些编号和网址均来自检索结果，而非模型内存——模型仅会输出其接收到的整数编码。

在关键任务中，同一账本系统还充当事实核查链条：每个来源都会附上原文引用（除非该内容确实出现在检索到的页面文本中，否则会被拒绝）；模型自身知识库中的陈述会被标记为`[unverified]`；而若引用来源缺乏证据支撑，执行`verify --evidence`命令时相关草稿将会被判定为无效。

该功能适用于聊天回复、书面文档（Markdown、PDF、DOCX、幻灯片）以及研究报告等场景。它不支持学术领域的BibTeX处理流程——如需处理会议论文，请使用`arxiv`功能，该功能会从本功能获取数据（详情参见`references/citation-formats.md`）。

## 适用场景

凡是答案或输出内容基于您检索到的信息而非自身已知知识的情况，均可使用此功能：
- 研究分析、对比总结、新闻摘要，以及“X领域的当前发展状况”类问题
- 任何需要将外部事实进行引用、改写或汇报并保存到磁盘的文档——包括报告、简报、文档、演示文稿、维基页面等
- 需要用户对结果进行核查的事实调查任务
- 需要对不同来源的矛盾信息进行溯源的多源整合场景
当信息检索只是作为其他任务的附带操作时——例如在编码过程中快速查询语法或版本信息、进行随意交谈或进行创意写作——可省略内联引用。只有当用户很可能需要该链接时，才需提供网址。

## 先决条件

除标准工具集外无需其他条件。《scripts/sources.py》仅为基于标准库的 Python 3 文件。信息检索功能可通过已配置的方式实现，包括：网络搜索、网页提取、浏览器导航或终端操作（如 curl、各类 CLI 工具）。

引用记录存储路径为：`$/HERMES_HOME/cache/citations/ledger.json`（该路径会根据用户配置的账号信息自动调整）。如需为特定任务指定不同路径，可使用 `--ledger <路径>` 或 `HERMES_CITATION_LEDGER` 参数进行覆盖。

## 运行方式

```bash
S=~/.hermes/skills/research/grounded-citations/scripts/sources.py

python "$S" reset                                  # start a clean ledger
python "$S" add https://example.com/a --title "A"  # prints: [1]
python "$S" add https://example.com/b --title "B"  # prints: [2]
python "$S" list                                   # ledger table
python "$S" render                                 # Sources: block
python "$S" verify draft.md                        # catch bad citations
```

`add` 操作具有幂等性且经过 URL 标准化处理：同一个页面在账本中始终会返回相同的 ID，因此即便进行多次搜索/提取操作，这些 ID 也能保持稳定。

## 快速参考

| 操作 | 命令 |
|---|---|
| 为新任务创建新的账本 | `sources.py reset` |
| 注册数据源并获取其 ID | `sources.py add <url> [--title T]` |
| 一次性注册多个数据源 | `sources.py add <url1> <url2> ...` |
| 从 JSON 工具的输出中注册数据源 | `sources.py ingest results.json` |
| 为某个数据源附加原文证据 | `sources.py quote <id> --text "exact wording" --from page.txt` |
| 查看账本内容 | `sources.py list [--json]` |
| 显示“数据源”区块 | `sources.py render [--style markdown\|plain\|footnotes\|bibtex\|evidence] [--only 1,3]` |
| 仅显示草稿中引用的内容 | `sources.py render --cited-in draft.md` |
| 直接在原处重写草稿的“数据源”区块 | `sources.py render --replace-in draft.md` |
| 检查草稿中的引用情况 | `sources.py verify draft.md [--strict] [--min-coverage 0.6] [--evidence]` |

## 操作步骤

① 在需要生成有依据的答案或文档的任务开始时，**先重置账本**。如果是在已存在草稿且其中 ID 仍有效的基础上继续工作，则无需重置——重新使用同一账本可保持编号的稳定性。

② **在检索时为每个信息来源进行注册。** 每次执行 `web_search`、`web_extract`、`browser_navigate` 或 fetch 操作后，需将对应的 URL 传递给 `sources.py add` 函数（或通过 `sources.py ingest` 直接导入原始 JSON 数据）。这一操作必须在撰写正文之前完成。而试图事后凭记忆进行注册，正是该功能旨在避免的错误做法。

③ **在起草时即添加引用信息。** 在每一句提及了相关信息来源的句子之后，立即标注对应的括号内编号。

```
Ice floats because it is less dense than liquid water.[1][2]
```

- 括号前不得留空格，每个标识符需单独置于括号内。  
- 每句最多包含3个标识符，需逐句标注引用，不可在文末一次性列出所有引用。  
- 仅可使用账本返回的标识符，严禁自行编造标识符或URL。  
- 基于个人知识的陈述无需标注引用。  
- 当存在矛盾信息时，应同时呈现两种观点，并为每种观点分别标注标识符。  
- 需严格按照来源提供的内容标注精确的数字、日期和名称；若找不到相关来源，应明确标注（如“未找到X的来源”），而非随意填补。

④ **添加“来源”板块**：通过运行 `sources.py render --cited-in <draft>` 命令，即可根据账本自动生成标识符与URL的对应关系，无需手动输入。对于非Markdown格式的输出目标，需选择相应的`--style`选项，并参照`references/citation-formats.md`中的规范确定引用位置（Word文档中使用脚注，PDF/LaTeX文档中使用尾注，演示文稿中添加“来源”幻灯片，Wiki输出则每页列出来源）。

⑤ **提交前务必验证**：运行 `sources.py verify <draft>` 命令，若遇到未知标识符、与账本内容不符的“来源”板块，或（在使用`--min-coverage`选项时）正文引用不足的情况，该命令将返回非零退出码。需针对这些问题进行修正后再重新运行验证。

⑥ **在聊天中回复时**，也需遵循相同步骤：先注册来源信息，行内标注引用，最后列出已生成的“Sources:”列表。对于简短回复，可直接使用 `sources.py render --only <ids>` 命令生成对应板块，无需将其保存到文件中。

## 多平台检测功能

“人们对X有什么评价？”或“在网络上搜索X”的需求并不属于`web_search`功能范畴。该系统会跨多种信息来源并行收集数据，然后针对每条信息的来源平台，对其真实性进行综合分析：

| 信息来源类型 | 路由路径 | 提供的内容 |
|---|---|---|
| 公开网络 | `web_search` → `web_extract` | 官方文档、文章及公告 |
| 社区讨论 | `reddit-reading`（包含`search`、`thread`功能） | 用户真实体验、反馈问题及解决方案 |
| 博客/版本发布记录/变更日志 | `rss-feeds`（包含`read`、`discover`功能） | 带日期的原始帖子及版本历史记录 |
| 视频内容 | `youtube-content` | 操作指南、演示视频及演讲内容 |
| 代码资源 | 使用`terminal`结合`gh search repos`/`gh search issues`命令 | 实现代码及未解决的漏洞 |
| X/Twitter平台 | `xurl`（需具备API访问权限） | 平台公告及开发者交流内容 |

`reddit-reading`和`rss-feeds`这两个功能为可选配置。如果尚未安装，可在使用前通过`hermes skills install official/social-media/reddit-reading`或`hermes skills install official/research/rss-feeds`命令进行安装。

在数据接收时（步骤②），需将每条路径下的所有URL都记录到日志中。同时要区分观点与事实：Reddit上的帖子仅能说明用户*报告*了某些情况，并不能证明其真实性；这类内容应与原始信息结合分析，或被标记为情感倾向数据。应明确指出各平台的覆盖缺口（例如“在Reddit上未找到3月之后的新相关内容”），而非擅自缩小搜索范围只关注有效信息。

## 事实核查模式

在那些需要能够核实信息来源的场景中——如医疗、法律、金融、安全领域，或是涉及争议性索赔的情况，以及用户要求进行事实核查时——请将引用方式升级为提供实际证据：

① **为每个信息来源附上原文引文。** 在提取完某页内容后，将其文本保存到文件中，并附上支撑相应论点的具体句子：

```bash
python "$S" quote 1 --text "Ice is about 9% less dense than liquid water." --from page1.txt
```

除非该语句在证据文本中出现原样，否则将被拒绝作为有效证据（系统不会区分空白字符、大小写以及 Markdown 标记——提取出的文本中的内联链接，如 `_[ERAP1](https://…)_`，会与读者看到的普通文本保持一致），因此意译内容或记忆有误的数字绝不能冒充证据。应直接复制粘贴已获取的文本，切勿重新输入。请按照读者看到的原样引用句子——匹配系统会帮您识别出提取工具添加的标记，因此您无需在引用中刻意还原链接语法或转义后的星号。

② **用 `[unverified]` 标记基于模型知识的主张。**对于那些无法找到来源的关键性主张，系统会为其添加明确的标记，而非引用信息。

```
The refactor likely predates the 2.0 release.[unverified]
```

`verify --min-coverage` 选项会将标记为 `[unverified]` 的句子也算作已验证——其目标是为每一个论断确定来源，而非要求每句话都有引用依据。如果某个关键论断能够被核实，就应当进行核实；而 `[unverified]` 标记则用于表示确实无法核实的情形。若某份事实核查结果中充斥着 `[unverified]` 标记，其摘要中也应明确说明这一点。

③ **通过第二种独立来源对有争议的事实进行交叉验证。** 当两个来源的观点不一致时，需分别引用这两种观点，并标注各自的编号及引文内容，同时说明你更倾向于哪种观点及其原因。一个来源仅能提供单方面信息，而两个独立来源则能起到相互印证的作用。

④ **利用证据审核机制进行验证，并呈现证据区块：**

```bash
python "$S" verify report.md --evidence --min-coverage 0.5
python "$S" render --style evidence --replace-in report.md
```

如果引用的任何来源均未附上对应引用文本，使用`--evidence`选项将会导致草稿被判定为不合格。该选项的呈现方式会在每个来源的URL下方直接显示其引用内容，因此最终输出会以“主张 → 来源 → 精确的支撑文本”的形式呈现，完全避免凭空猜测。若需直接修改现有的“来源”板块，可使用`--replace-in <draft>`命令（该操作具有幂等性，即便后续又添加了更多引用文本，再次运行也不会出现问题）；而`--cited-in`选项则会将结果输出到标准输出流中。这两个选项都会显示`## Sources`标题（若使用`--style plain`选项，则会显示为`Sources:`）。

**`--min-coverage`所统计的内容**：覆盖率指的是“标明了来源信息的句子数以及普通叙述句数”。所谓普通叙述句，是指位于“来源”板块之后的非空行片段，且长度需在4个单词以上；同时会排除标题（`#`）、表格行（`|`）以及代码块中的内容，引文标记也会被剔除。来源信息可通过`[n]`格式的引用或`[unverified]`标记来标明，因此同时包含这两种标记的句子会被计入一次统计。在确定具体阈值之前，可先运行`verify`命令且不设置阈值，然后查看`info: stats:`行中的统计数值。

## 常见误区

- **在撰写完成后才进行注册**：数据库中的内容必须直接来源于工具的输出，而不能从草稿中重新构建——否则又会重新引入编号机制原本旨在消除的、基于错误URL产生的虚假信息风险。
- **在任务执行过程中重新编号**：绝不可手动编辑草稿中的编号。这些编号是数据库中的唯一标识；如果草稿中引用了`[4]`，那么该来源就必须始终保持为`[4]`。只有在切换不同任务时才应运行`reset`命令。
- **在“来源”板块中手动输入URL**：务必先使用`render`命令生成内容。手动输入的URL属于未经验证的主张。
- **将搜索片段当作完整页面内容引用**。`web_search` 描述仅能反映其字面内容。若某项陈述需要具体内容支撑，应先使用 `web_extract` 提取目标页面文本，再引用该内容。
- **过度引用**。单句中最多可使用三个引用标识；若每个分句都添加引用，会导致文本难以阅读，且无法明确哪处来源承担了主要信息。
- **在代码或配置文件中引用日志记录**。来源说明应放在正文文档或文档头部，而非生成的代码之中。
- **并行子智能体**。每个子智能体都有独立的操作目录；如果需要合并它们的输出，需使用 `--ledger`（或 `HERMES_CITATION_LEDGER`）将所有子智能体指向同一个日志记录，否则它们的引用标识将会冲突。
- **从片段而非完整页面引用内容**。证据引用必须来自提取到的页面文本，而非搜索结果描述——应先执行 `web_extract` 提取文本，保存后再用 `quote --from` 指定该文件作为引用来源。
- **通过 `quote --text` 进行意译**。逐字匹配检查会拒绝此类引用；正确的做法是找到原文句子，而非反复改写直到内容匹配。
- **滥用 `[unverified]` 作为替代方案**。该标记仅用于那些确实无法找到来源的极少数陈述；如果多数句子都使用此标记，说明任务需要更多信息检索，而非更多标记。
- **手动编辑“来源”板块**。应使用 `render --replace-in <draft>` 命令进行替换；自行截取文件可能会导致内容过时或重复，进而被 `verify` 工具识别为异常。

## 验证

```bash
python "$S" verify report.md --strict --min-coverage 0.5
```

绿色状态表示：草稿中的每一个 `[n]` 都存在于账本中，“来源”板块列出了所有被引用的编号及其对应的账本网址，且包含来源信息的句子比例达到了设定阈值。即便退出代码为0，也请仔细查看警告信息——未被引用的已注册来源通常意味着某项表述在编辑过程中丢失了其出处信息。
