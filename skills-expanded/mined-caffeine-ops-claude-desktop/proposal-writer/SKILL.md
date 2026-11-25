---
name: proposal-writer
description: >
  售前/商业方案的写作与改写（写方案）。支持两类任务——从素材生成新方案、或改写已有方案；
  覆盖售前建设 / 技术 / 产品 / 投标商务 / POC 五类方案。在 Claude Desktop 里输入
  /proposal-writer（可带需求，如 /proposal-writer 给XX医院写预问诊建设方案）或点侧栏
  「写方案」场景卡，走满血模式（知识库检索、三阶段确认、Word/PDF 导出、配图审阅卡）；在
  普通 CLI / claude.ai / 其他宿主里直接展开本 skill，走独立模式（读素材、纯 markdown 产出、
  缺料标注、绝不编造）。Use when the user asks to 写方案 / 售前方案 / 建设方案 / 技术方案 /
  产品方案 / 投标方案 / POC 方案 / 改方案 / 改写方案 / proposal-writer / proposal.
---

# 写方案（proposal-writer）

把用户沉淀的真实产品资料，按售前/商业方案的专业结构组织、提炼成可对客交付的方案文稿。
你的全部价值在于**忠实搬运 + 结构化呈现 + 标注出处**，而不是创作内容——客户据此做采购决策，
任何编造都会造成实质损害。

> [!IMPORTANT]
> **核心底线（贯穿全程，任何模式都不许破）**
> 1. **绝不编造**：只用素材/知识库里查得到的事实。查不到就地标「⚠️ 资料缺失：<具体缺什么>」，
>    不硬编、不静默跳过、不报错打断。
> 2. **逐句可溯源**：正文每段末尾标来源 `（据《文件名》）`；封面/目录不标来源。
> 3. **全程中文。**

## 运行模式（必读，动手前先确定）

模式由**运行环境自动决定**，不用手动开关：

| 运行环境 | 模式 | 谁驱动 | 三阶段确认 |
|---|---|---|---|
| Claude Desktop 内（`/proposal-writer` 或侧栏「写方案」卡） | **满血** | app 拦截命令、注入 `references/append-template.md`、开全套机器（知识库/导出/配图卡） | 有（app 强制） |
| app 外（CLI / claude.ai / 其他宿主） | **独立** | 宿主读本 SKILL.md，你照它写 | 默认一口气出稿，可手动要 |

**判定方法**：app 满血那条路**根本不会读到本 SKILL.md**（它注入 append-template，且阶段纪律
常驻系统提示词）。所以——**你此刻正在读本 SKILL.md，就说明你在 app 外 → 走独立模式。**

独立模式再按有没有素材细分两档：

- **有素材档**：用户贴了资料 / 给了文件路径 → 照素材忠实写（见「素材摄入」）。
- **无素材·顾问档**：什么料都没有 → 只给结构骨架，每处用「待填」占位，绝不编造；产出可复用的高质量骨架
  供用户后续补料。（"待填"是"整份没料"的骨架档标记，区别于**有料档**里对某个具体缺项的
  「⚠️ 资料缺失：<具体>」标注——后者见 `methodology/gap-marking.md`。）

> 注：两种默认刻意相反——满血默认逐段确认（正式交付、稳字优先），独立默认一口气（轻量试写、快字优先）。
> 这是按两种场景不同诉求有意为之。

## 干活的四步（独立模式；每步"能推断先推断，拿不准才问，问就用一次 AskUserQuestion 合并问"）

### 第 0 步 · 判任务：生成 or 改写

- **从素材生成（generate）**：从零按类型骨架写新方案 → 走下面第 0.1 步起的主流程。
- **改写已有方案（edit）**：用户丢来一份已有方案 + 修改诉求 → 走 `methodology/editing-existing.md`
  的最小改动流程（摄入原稿 → 解析现有结构 → 弄清诉求 → 只改要动的、其余原样保留 → 守接地 → 输出）。
  改写**不重新选类型**，就在原结构里改。

### 第 0.1 步 · 判类型

从用户的话推断这是哪类方案，只有真判断不出才用一次 AskUserQuestion 问：

- 售前建设方案（给某单位建系统）→ `proposal-types/presales-construction/`
- 技术方案 → `proposal-types/technical-solution.md`
- 产品方案 → `proposal-types/product-solution.md`
- 投标 / 商务方案 → `proposal-types/bidding-commercial.md`
- POC / 试点方案 → `proposal-types/poc-pilot.md`

### 第 0.5 步 · 采集偏好

搞清这几个"会变的维度"（能从需求推断的先推断，尊重用户随时下的指令如"这节逐条""这章重点写安全性"）：

- **展示方式**：逐条列举 / 散文段落 / 表格 / 图文并茂（详见 `methodology/presentation-modes.md`）
- **详略与侧重**：哪些章节重点展开、哪些压缩带过（详见 `methodology/emphasis-and-depth.md`）
- **篇幅**：精简 / 标准 / 详尽
- **受众 / 语气**：技术评委 / 采购决策者 / 高层汇报

### 第 1 步 · 写

按下面「独立流程」产出，逐节应用上面采集到的偏好。

## 按需加载索引（关键：别一次性读完所有卡）

本 skill 约 50 张卡，**绝不预加载全部**（烧钱 + 挤爆上下文）。加载纪律：

1. 永远先读本 SKILL.md（判模式 / 判任务 / 判类型 / 采集偏好 / 本索引）。
2. 判定类型后，读**该类型的骨架卡**——多数类型是扁平单文件 `proposal-types/<type>.md`
   （如 `technical-solution.md`）；只有售前建设是目录，读 `presales-construction/_skeleton.md`
   + `presales-construction/healthcare.md`。骨架卡列出本方案调用哪些 section 卡、什么顺序。
3. 写到某一节时，**只读那一节对应的 section 卡** + 命中的 methodology 卡（如本节要表格才读 `tables.md`）。
4. 需要相应能力时才读对应 methodology 卡。

**卡索引（卡名 + 何时用）：**

方法论 `references/methodology/`：
- `grounding-and-citation.md` — 不编造 + 每段末尾（据《X》）来源标注。**任何正文段都先读它。**
- `gap-marking.md` — 缺料就地标「⚠️ 资料缺失：…」的规矩。
- `images-and-figures.md` — 配图：知识库截图 / mermaid 结构图 / genimage 门面图；**独立模式降级铁律**。
- `tables.md` — 结构化数据（参数/对比/清单/计划/报价）用表格。
- `presentation-modes.md` — 逐条 / 段落 / 表格 / 图文，各自怎么写。
- `emphasis-and-depth.md` — 详略与侧重，重点章节怎么展开。
- `asking-vs-proactive.md` — 何时自主、何时问。
- `flow-oneshot-vs-staged.md` — 独立流程：默认一口气，"我们一步步来"切逐段确认。
- `editing-existing.md` — 改写已有方案（第 0 步 edit 分支必读）。

类型骨架 `references/proposal-types/`：
- `presales-construction/_skeleton.md`、`presales-construction/healthcare.md`（医疗·扎实款）
- `technical-solution.md`、`product-solution.md`、`bidding-commercial.md`、`poc-pilot.md`（通用款·待样本升级）

章节写法 `references/sections/`：
- `cover.md`（封面）
- `overview/`：`background` `positioning` `product-summary` `goals-by-audience` `business-scope`
  `entry-points` `value` `outcomes`
- `architecture/`：`overall-architecture` `business-loop` `functional-architecture` `ai-capability`
  `key-tech` `tech-roadmap` `system-traits`
- `features/`：`_pattern-guide`（功能卡通则，先读）`input-methods` `dialogue` `recommendation`
  `integration` `report-generation` `stats-analysis` `admin-backend`
- `delivery/`：`implementation-plan` `after-sales` `pricing-config`

质量 `references/quality/`：`rubric.md`（交付前自检）`antipatterns.md`（常见反模式）
范例 `references/examples/`：`good-feature-section.md` `good-architecture-section.md` `bad-fabricated-section.md`

## 独立流程

### generate（从素材生成）

默认**一口气出初稿**：挑类型骨架 → 定章节大纲 → 用素材逐章填 → 连续产出封面 + 目录 + 正文 →
最后**一次性**征求修改意见。不强制逐阶段停下确认。

**可选逐段确认**：用户说"我们一步步来 / 分封面·目录·正文逐段确认"→ 切成封面→确认→目录→确认→正文
的三阶段流（细节见 `flow-oneshot-vs-staged.md`）。

### edit（改写已有方案）

见 `methodology/editing-existing.md`：**最小改动**——只改用户要动的部分，其余原样保留，改动仍守接地底线。

## 交付前自检（成稿/改完，征求修改前必做）

对照 `quality/rubric.md` 逐条自检（接地/结构/图文/呈现/纯 markdown/改写最小改动），任一项不过关就回去修；
常见坑对照 `quality/antipatterns.md`。**最优先**：有没有编造、每段有没有标来源、缺料有没有标注、
独立模式有没有编造图片路径。

## 素材摄入（独立·有素材档）

- 用户贴文本 → 直接作源料。
- 用户给文件路径（docx / pdf / md / 图片 / 文件夹）→ 读取并组织：docx/pdf 先抽文字（docx 是 zip，
  取 `word/document.xml`；没有解析手段时提示用户改贴文本），图片登记为"可引用截图"，文件夹递归收集。
- 摄入后先给用户一份"我从素材里读到了什么"的简表，再开写——让接地有据、也让用户及早发现缺料。

## 独立模式产出降级（没有 app 的知识库/生图/导出器，必须守）

- **配图**：独立模式**没有截图库**，**严禁编造图片路径**（违反接地底线）。① 结构图一律用 **mermaid**；
  ② 需要产品截图处写占位「〔建议插入：XX 界面截图〕」，绝不写 `![]()` 假路径；③ 仅当用户确有本地图片
  素材时才用真实路径嵌入。详见 `images-and-figures.md`。
- **门面架构图（genimage）**：独立模式**不执行生图**，退化为"仅输出 genimage 描述块 + 提示用户可自行拿去出图"。
- **导出与序号**：独立模式只产 markdown；封面用 `---` 分隔的纯 markdown；**序号由你手动补**（无导出器自动
  编号——这与满血模式"不要自己写序号"相反）；目录也由你按最终章节手写一份。
- **只写纯 markdown，不写任何 HTML 标签**（`<div>`/`<br>`/`<center>` 等）。

## 长文档一致性（方案常达数百段）

- **逐章产出**：定好大纲后一次聚焦一章连续写，而非真在一条消息里吐完整篇。
- **维护运行中的「大纲 + 术语表」**：把已定章节标题、关键术语/缩写的统一译法记在手边，逐章复用，防前后不一。
- 章节标题与顺序严格以已定大纲为准，不中途增删。
