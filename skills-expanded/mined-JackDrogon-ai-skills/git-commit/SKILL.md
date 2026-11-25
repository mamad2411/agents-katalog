---
name: git-commit
description: Generate high-quality Conventional Commit messages, improve existing commit text, and run clean staged-only git commits when the user explicitly asks to commit. Also applies to Chinese requests about commit messages or git commit workflows.
license: MIT
---

# Git Commit 提交信息写作指南

这个 skill 用于帮助用户生成**准确、简洁、符合 Conventional Commits 的提交信息**。

它既要能处理**单行提交标题**，也要能处理**完整多行提交信息**；如果用户要求的不只是“写 message”，而是**实际执行 `git commit`**，它也应该遵循一套明确、稳定的操作约束。

## 目标

使用这个 skill 来完成以下任务：
- 把用户的改动描述、diff 摘要、PR 摘要转换成提交信息
- 把已有的、不规范的提交文本改写成约定式提交格式
- 判断一个改动更适合用 `feat`、`fix`、`refactor`、`docs`、`test`、`perf`、`build`、`ci`、`style`、`chore` 中的哪一种
- 判断是否应该加 scope
- 判断是否需要 body、footer、issue 引用或 `BREAKING CHANGE:`
- 确保提交信息忠实反映改动，而不是夸大改动价值
- 在需要时基于实际 staged 结果执行一次干净、受控的 `git commit`

## 执行 git commit 时的操作约束

当任务不只是“写 commit message”，而是要**实际执行 `git commit`** 时，默认遵守以下规则：

- 生成 commit message 之前，先观察当前整个 commit 状态。
- 如果已经存在 staged / cached 的改动，就只基于这批 staged diff 生成 commit message，并且也只提交这批 staged 内容。
- 如果当前没有 staged / cached 的改动，先执行 `git add -u`，然后基于这批 newly staged 的 diff 生成 commit message，并作为本次提交来源。
- `git add -u` 只用于更新已跟踪文件，不应把新的未跟踪文件加入提交范围。
- 使用 `git commit -s`，通过 signoff 方式提交。
- 不要添加任何 Claude、Claude Code、bot、AI 生成痕迹。
- 不要在 commit message 中加入 `Generated with Claude Code`、`Co-Authored-By: Claude ...`、bot footer 或类似标记。
- 不要主动 `git add` 新文件。
- 不要把未 staged 的修改顺手一起提交，除非这些修改已经通过上述流程进入 staged 集合。

如果需要实际执行提交，优先遵循下面的行为准则：

1. 先检查是否已有 staged 改动。
2. 如果有 staged 改动，就直接以 staged diff 作为 commit message 的唯一事实来源，也是本次提交的唯一内容来源。
3. 如果没有 staged 改动，执行 `git add -u`，然后以这批 staged diff 作为 commit message 和提交的来源。
4. 不额外 stage 新文件，也不扩大提交范围到未跟踪文件。
5. 使用 `git commit -s` 提交。
6. 提交信息中保持干净，不附加任何 Claude 或 bot 身份说明。

如果用户没有明确要求执行 commit，而只是让你帮忙写 message，那么只输出 commit message 内容即可，不要默认执行 `git add` 或 `git commit`。

不过，如果用户是通过这个 skill 的直接调用入口来触发任务，并且**没有提供额外参数**，则应把这次调用本身视为“明确要求执行 commit”。在这种情况下，不需要再额外询问是否要提交，而应直接按照本 skill 的提交流程执行。

## 默认工作流

除非用户明确只要某一种结果，否则按下面顺序处理。

1. 先识别输入来源。
   - 输入可能来自用户的自然语言描述、diff 摘要、staged changes 摘要、PR 描述，或者已有的 commit message 草稿。
   - 如果要写出准确的提交信息仍然缺少关键事实，不要硬猜。优先提一个简短澄清问题，或者给出 2-3 个合理选项。

2. 判断提交类型。
   - 优先选择**最准确、最小化**的类型，不要默认全部都写成 `feat` 或 `fix`。
   - 默认采用**工程语义优先**的判断方式：优先描述这次提交主要做了什么工程动作。
   - 新增用户可感知能力时，优先用 `feat`。
   - 修复错误行为时，优先用 `fix`。
   - 不改变预期行为、但重组实现结构时，优先用 `refactor`。
   - 以性能提升为主时，优先用 `perf`，即使实现方式包含部分重构。
   - 纯文档、测试、构建、CI、代码风格、仓库维护等情况，优先使用对应类型。

3. 判断提交信息的形态。
   - 改动很简单时，一行标题就够了。
   - 改动的“为什么”很重要、迁移影响明显、或用户已经给了丰富背景时，应补充 body。
   - 存在 issue 关闭关系、评审信息、兼容性变化时，应补充 footer。
   - 存在破坏性变更时，应在标题里加 `!`，并在完整提交里补充 `BREAKING CHANGE:` footer。

4. 写标题行。
   - 使用 `<type>[optional scope]: <description>` 结构。
   - `description` 要具体，描述结果，不要空泛。
   - 优先使用祈使式、现在时风格，例如 `add`、`fix`、`refactor`、`implement`、`remove`、`update`、`correct`、`optimize`。
   - 标题行末尾不要加句号。

5. 只在有价值时写 body。
   - body 用来解释为什么这么改、改动的高层逻辑、关键取舍，而不是简单重复标题。
   - 如果用户本来就给了结构化亮点，可以保留为条目式描述。

6. 在需要时补充 footer。
   - 常见 footer 包括 `BREAKING CHANGE: ...`、`Closes #45`、`Refs: #123`、`Reviewed-by: Z`。
   - footer 应该只写事实，不要虚构 issue 编号、reviewer 或其他元信息。

## 约定式提交规则

生成结果时遵循这些规则：
- 标题基础结构必须是：`<type>[optional scope]: <description>`
- scope 是可选的，应该是一个简短名词，表示受影响的模块、子系统或领域，例如 `api`、`parser`、`ui`、`auth`、`pair_trading`
- 如果存在破坏性变更，可在 `:` 前加 `!`
- 如果输出的是完整提交信息，且存在 breaking change，应同时包含 `BREAKING CHANGE:` footer
- `BREAKING CHANGE` 必须大写
- 其它 footer 使用 trailer 风格，例如 `Closes #45`

## 如何选择 type

按下面逻辑判断：

- `feat`: 引入新的能力或行为
- `fix`: 修复错误行为
- `refactor`: 重构实现，但没有预期行为变化
- `perf`: 以性能优化为主
- `docs`: 只改文档
- `test`: 新增或调整测试
- `build`: 构建系统、依赖、打包、外部构建链路改动
- `ci`: CI 流程或自动化流水线改动
- `style`: 纯格式、排版、风格调整，没有逻辑变化
- `chore`: 仓库维护、杂项清理、非产品行为改动

如果一个改动跨了多个类别，优先选**最能代表这个提交主要意图**的 type。

## 如何选择 scope

scope 不是必需的，但这个 skill 默认**倾向写 scope**，只要它确实能提升辨识度。

在这些情况下一般应该加 scope：
- 某个模块名非常明确
- 某个子系统是改动焦点
- 某个领域概念在代码库中已经稳定存在
- 写上 scope 能明显提升提交历史的可检索性

好的 scope 应该：
- 简短
- 稳定
- 能提高辨识度
- 尽量贴近真实模块、子系统或业务域

尽量避免没有信息量的 scope，例如过于空泛的 `misc`、`stuff`、`update`。如果 scope 虽然能写但没有辨识度，不如不写。

## 如何写好标题行

好的标题行应该：
- 优先表达最终做成了什么结果
- 足够具体，能和附近的提交区分开
- 不要写成空泛描述，例如 `update code`、`fix stuff`、`misc changes`
- 不要夸大实际改动
- 默认不要把 PR 编号放进标题，除非用户明确要求保留

优先类似下面这种：
- `fix(auth): reject expired reset tokens`
- `refactor(cache): simplify eviction bookkeeping`
- `perf(indexer): reduce lock contention in batch writes`
- `refactor(pair_trading)!: implement time-based EMA for SpreadOracle`

避免类似下面这种：
- `fix bug`
- `update code`
- `refactor project`
- `refactor(pair_trading)!: implement time-based EMA for SpreadOracle (#43)`（除非用户明确要求保留 PR 编号）

## 实战工作流：从真实输入推导 commit message

很多时候，用户给的并不是已经整理好的“提交摘要”，而是下面这些原始材料：
- `git diff`
- staged changes
- PR 描述
- 零散的 bullet points
- 一段“我改了这些东西”的自然语言说明

这时不要直接从局部措辞里抓几个关键词就开始写 commit。应按下面步骤处理。

### 1. 先抽取“这次提交最主要在做什么”

优先识别这个提交的**主要意图**，而不是罗列所有文件变化。

先问自己：
- 这次提交最核心的结果是什么？
- 用户最希望别人从提交标题里先看到什么？
- 如果只能保留一条变化来代表这次提交，那会是哪一条？

标题行应优先表达这个“主意图”。

### 2. 区分主改动和附带改动

真实提交里常常会同时出现多种变化，例如：
- 重构过程中顺手修了一个小 bug
- 新功能提交里附带更新了测试和文档
- 性能优化提交里顺便做了格式整理

处理原则：
- 用 **主改动** 决定 `type`
- 默认采用**工程语义优先**的判断方式：如果主要是内部实现替换且行为不变，优先 `refactor`；如果主要收益是性能，优先 `perf`
- 用 **主改动所属区域** 决定是否需要 `scope`
- 把次要但仍然值得记录的信息放进 body
- 不要因为附带改动的存在就把标题写得过宽、过杂

例如：
- 主要是在引入新能力，顺手补了测试 → 优先 `feat`
- 主要是在修复错误行为，顺手清理结构 → 优先 `fix`
- 主要是在重构实现，顺手补注释 → 优先 `refactor`

### 3. 不要被噪声改动带偏

从 diff 推导提交信息时，常见噪声包括：
- 格式化改动
- import 顺序调整
- 少量重命名
- 注释修正
- 自动生成文件的机械变化

如果这些变化不是提交的主要目的，就不要让它们主导 commit message。

优先关注这些更能决定提交语义的信号：
- 行为是否发生变化
- API / 配置 / 数据格式是否变化
- 是否修复了错误路径
- 是否引入了新的能力
- 是否改变了核心实现策略
- 是否有用户、调用方、运维方需要关注的迁移影响

### 4. 当输入是 diff 或 staged changes 时的推荐推导顺序

如果用户给的是 diff、staged changes 或“请根据改动生成 commit message”，优先按这个顺序思考：

1. 哪些文件或模块是这次改动的中心？
2. 这些改动的主要目的是什么：新增、修复、重构、优化，还是文档/测试/构建？
3. 有无用户可感知行为变化？
4. 有无兼容性变化、配置变化、迁移成本？
5. 哪些信息适合写进标题，哪些更适合放进 body？
6. 是否需要 footer，例如 `Closes #45` 或 `BREAKING CHANGE:`？

只有在这个判断完成后，再生成最终 commit message。

### 5. 当输入是 PR summary 或 squash merge 场景时

当输入代表的是**一整个 PR 的改动集合**，而不是一个很小的单点提交时：
- 标题应概括这次 PR 的核心成果，并优先写成**结果导向**表达
- body 适合先解释 why，再吸收关键实现点、动机和影响面
- 如果 PR 内含多个小修小补，不要把所有细节都塞进标题
- 只有在用户明确提供了真实 issue / PR 相关引用信息时，才写入 footer
- 默认不要把 PR 编号直接写进标题，除非用户明确要求保留
- 如果存在 breaking change，默认使用双标记：标题加 `!`，正文写 `BREAKING CHANGE:` footer

squash merge 的标题应该更像“这次合并最终给代码库带来了什么”，而不是机械拼接每个中间提交的摘要。

## Body 写作指南

当 body 能帮助下一个读提交历史的人更快理解意图时，就应该写。

这个 skill 默认偏好：**body 先写 why，再写关键实现点**。

Body 不应该重复标题，也不应该把 diff 逐行翻译成英文。它主要用于记录标题和代码本身不容易直接表达的信息，例如：
- 为什么要做这次改动
- 这次改动解决了什么问题
- 高层实现策略是什么
- 有哪些关键影响、取舍或副作用
- 是否存在迁移、兼容性或性能影响

适合写 body 的情况包括：
- 改动背后的动机很重要
- 具体实现变化并不直观
- 用户已经提供了技术亮点或设计说明
- 有迁移影响、配置影响、运行时影响需要解释

好的 body 可以包含：
- 为什么要做这次改动
- 高层实现说明
- 关键取舍
- 已经结构化的信息点，例如 Key Technical Highlights

不要只是把标题换一种说法再重复一遍。优先让第一段或前两行先解释 why，再用后续段落或条目补关键实现点。

### Body 的三种形态

根据提交复杂度选择合适的 body 形态，不要默认所有提交都写成长篇正文。

#### 1. 轻量 body
适用于：
- 小 bug fix
- 小范围 refactor
- 简单 feature 补充

写法：
- 用一小段说明 why/context 即可
- 不必强行列小标题或 bullet points

示例：
```text
Prevent stale responses from overwriting the latest request state
when multiple requests race during fast user input.
```

#### 2. 标准 body
适用于：
- 一般 feature
- 一般 refactor
- 普通性能优化
- 需要一些背景的 bug fix

写法：
- 第一段写 why/context
- 第二段写 2-4 个关键实现点

示例：
```text
Count-based EMA behaves poorly when market data arrives at uneven
intervals, which can distort smoothing and produce unstable spread
signals during low-activity periods.

Key changes:
- Replace count-based decay with time-based decay.
- Interpret `window` as a duration in seconds.
- Reduce branching in the hot update path.
```

#### 3. 重型 body
适用于：
- breaking change
- 重要架构重构
- 明确的性能优化
- 高风险基础设施改动
- squash merge / 大 PR 汇总提交

写法：
- 第一段写 why/context/problem
- 第二段写 technical highlights、strategy、benchmarks 或 trade-offs
- 第三段在需要时写 impact、migration 或 operational notes

只在内容真的足够复杂时才使用这种形态。

### 不同 type 的 body 重点

不同 type 的提交，body 关注点不同。生成正文时优先匹配对应 type 的写法，而不是所有类型都套同一种模板。

#### `fix`
重点写：
- 问题在什么条件下出现
- 根因是什么
- 为什么这个修复是正确的

优先回答：
- 什么情况下会出错？
- 错误为什么会发生？
- 这次改动如何阻止它再次发生？

常用句式：
- `... can happen when ...`
- `... fails because ...`
- `... prevents ... by ...`

#### `refactor`
重点写：
- 为什么值得重构
- 重构后的结构优势是什么
- 是否保持行为不变
- 是否提升了可维护性、扩展性或可测试性

优先回答：
- 之前的结构问题是什么？
- 新结构解决了什么长期维护问题？
- 是否只是内部实现变化而不影响外部行为？

当改动看起来“影响很大”，但核心仍然是替换内部实现策略、重组结构、调整内部语义，而不是新增面向用户的新能力时，默认仍优先考虑 `refactor`，而不是 `feat`。

常用句式：
- `Simplifies ... by ...`
- `Separates ... from ...`
- `Keeps behavior unchanged while ...`

#### `perf`
重点写：
- 性能瓶颈是什么
- 采用了什么优化策略
- 收益是否能量化

优先回答：
- 慢在哪里？
- 为什么新的实现更快？
- 是否有 benchmark、复杂度变化、分配减少、锁竞争下降等证据？

如果有数据，尽量写进 body，并优先单独整理成 `Performance impact:` 或 `Benchmarks:` 这样的结构化小节。默认不要只把性能数字顺手塞进普通段落里；当存在可量化指标时，优先让读者一眼就能看出“瓶颈是什么、收益是什么、行为是否保持不变”。即使没有完整 benchmark，也应尽量提供方向性收益说明。如果优化没有改变原有行为，这一点也值得显式写出。

常用句式：
- `Reduces ... from ... to ...`
- `Avoids ... in the hot path`
- `Cuts allocation / lock contention / repeated scans`

#### `feat`
重点写：
- 新能力解决了什么问题
- 对现有流程有什么影响
- 是否引入新的使用方式、约束或配置

优先回答：
- 这个新能力让用户或系统多做了什么？
- 它如何嵌入现有流程？
- 是否要求调用方采用新的方式使用？

常用句式：
- `Adds support for ...`
- `Allows ... to ...`
- `Integrates ... into the existing ... flow`

### Body 的风格要求

- 保持客观、专业，避免第一人称
- 优先使用完整自然句，而不是流水账
- 列表只在信息天然结构化时使用，例如 technical highlights、benchmarks、migration notes、side effects
- 默认控制每行长度在约 72 个字符附近，以提高终端和 `git log` 可读性；必要时可为可读性适度浮动
- 重点记录代码不容易直接表达的内容，尤其是兼容性、性能、副作用和迁移影响

## 破坏性变更处理

当改动会对使用者、运维配置、集成方或外部接口产生不兼容影响时：
- 在标题中加入 `!`
- 在完整提交信息中加入 `BREAKING CHANGE:` footer
- footer 要明确说明使用方需要做什么迁移或修改

这个 skill 默认采用**双标记**风格：只要确认是 breaking change，就同时使用标题中的 `!` 和正文中的 `BREAKING CHANGE:` footer。

推荐写法：

```text
refactor(pair_trading)!: implement time-based EMA for SpreadOracle

Replace count-based EMA with time-based EMA so smoothing behaves correctly
when market data arrives at uneven intervals.

BREAKING CHANGE: EMA_WINDOW now expects a duration in seconds instead of a tick count.
```

## Issue / Trailer Footer

只有在用户明确提供了真实引用信息时才写 footer。

默认偏好如下：
- 真正关闭 issue 时，优先使用 `Closes #45`
- 只是补充背景引用时，优先使用 `Refs: #123`
- 默认不要把 PR 编号写进标题；除非用户明确要求，否则不要附加 `(#43)` 这种信息

常见格式：
- `Closes #45`
- `Refs: #123`
- `Reviewed-by: Z`
- `Co-authored-by: Name <email@example.com>`

不要凭空捏造 issue 编号、reviewer、co-author。

## 信息不充分时的处理方式

当信息不完整时，不要装作知道全部事实。优先采用下面三种方式之一：
- 提一个简短澄清问题
- 先给一个**推荐方案**，再给 1-2 个 commit message 备选，并说明差异
- 给出 best-effort 草稿，同时明确标出假设点

如果已经有足够信息支持一个更合理的默认判断，不要只把多个候选平铺并列。这个 skill 更偏好“给出推荐 + 说明为什么推荐 + 再提供备选”，这样既避免硬猜，也能帮助用户更快做决定。

## 输出模式

根据用户请求，选择最合适的输出形式。

### 模式 A：只输出标题行
适用于用户只想要一条简短 commit message。

输出严格为一行：

```text
<type>[optional scope]: <description>
```

### 模式 B：输出完整提交信息
适用于以下情况：
- 用户明确要完整 commit message
- 改动本身比较复杂
- 用户给了较多背景信息
- 存在 breaking change、issue footer、迁移说明等信息

结构如下：

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

### 模式 C：给出多个候选方案
适用于以下情况：
- 改动同时可能属于多个 type
- scope 选择不唯一
- 用户没有提供足够上下文，但仍希望快速得到可选 commit

默认先给出一个**推荐方案**，再补 1-2 个备选，并简要说明差异。不要只机械并列多个版本；这个模式的价值在于帮助用户更快判断哪一个最符合当前提交意图。

## 面向用户时的推荐输出格式

默认优先这样回复：

### 推荐提交信息
```text
...
```

### 为什么这样写
- type: ...
- scope: ...
- 为什么需要或不需要 body/footer

如果用户想看备选，再补充：

### 备选方案
```text
...
```

如果任务是**实际执行 `git commit`**，默认把回复组织成更接近 workflow 的形式，而不是只给一条 message。

这里的“实际执行 `git commit`”包括两种情况：
- 用户在自然语言中明确要求你实际执行提交，而不只是写 commit message
- 用户是通过这个 skill 的直接调用入口触发任务，并且**没有提供额外参数**；这种情况下，这次调用本身就等价于明确授权，应直接执行 commit，不需要再次确认

默认回复结构如下：

### 推荐提交命令
```bash
git commit -s -m "..."
```

### 推荐提交信息
```text
...
```

### 提交范围说明
- 本次提交只基于当前 staged / cached 改动
- 不纳入未 staged 修改或未跟踪文件
- 不附加任何 Claude、bot、AI 或 co-author 标记

这样可以把“写什么 message”和“这次提交到底应包含什么”一起讲清楚，避免回答退化成纯文案建议。

## 示例

**示例 1**
输入：Added polish language support.
输出：
```text
feat(lang): add polish language
```

**示例 2**
输入：Fixed racing requests by tracking the latest request id and ignoring stale responses.
输出：
```text
fix: prevent racing of requests

Introduce a request id and a reference to the latest request so stale
responses can be ignored safely.
```

**示例 3**
输入：Replaced count-based EMA with time-based EMA for SpreadOracle. The config now expects seconds instead of tick count. Closes #45.
输出：
```text
refactor(pair_trading)!: implement time-based EMA for SpreadOracle

Replace count-based EMA with time-based EMA to address uneven data arrival
rates in high-frequency trading scenarios.

BREAKING CHANGE: EMA_WINDOW now expects a time duration in seconds instead of a tick count.
Closes #45
```

**示例 4**
输入：Optimized the order matching loop by replacing repeated linear scans with a priority queue. This reduces latency under heavy load.
输出：
```text
perf(orderbook): optimize matching with priority queue

Linear scans across bid and ask levels become a bottleneck during
high-volume bursts, adding avoidable latency to order execution.

Key changes:
- Replace repeated scans with priority-queue based selection.
- Reduce work in the hot path during dense order flow.
- Keep matching semantics unchanged while improving throughput.
```

**示例 5**
输入：Split cache eviction logic out of the main store implementation so the code is easier to test and maintain. Behavior stays the same.
输出：
```text
refactor(cache): extract eviction policy from store logic

The current store implementation mixes eviction decisions with storage
updates, which makes the code harder to test and reason about.

Key changes:
- Separate eviction policy from core store mutations.
- Keep cache behavior unchanged for existing callers.
- Make policy-specific logic easier to extend and unit test.
```

**示例 6**
输入：The API now requires scoped access tokens instead of the old global token format. Existing clients must send `Authorization: Bearer <token>` with a scoped token generated from the new auth flow.
输出：
```text
feat(api)!: require scoped access tokens for authenticated requests

The previous global token model makes it difficult to restrict access
by capability and service boundary, which weakens API isolation.

Key changes:
- Reject legacy global tokens for authenticated API routes.
- Require scoped bearer tokens issued by the new auth flow.
- Align token validation with service-level access boundaries.

BREAKING CHANGE: Clients must migrate from legacy global tokens to
scoped bearer tokens and send them in the Authorization header.
```

## 这个 skill 应该擅长的事情

这个 skill 应该稳定处理以下场景：
- 把原始改动说明整理成规范的 Conventional Commit
- 把随意写的 commit message 改写成标准格式
- 准确区分 `feat`、`fix`、`refactor` 等类型
- 判断什么时候应该写 body
- 正确添加 `BREAKING CHANGE:` 和 issue footer
- 在信息不足时给出多个高质量备选，而不是盲猜一个看起来很完整但不够准确的结果
- 从 diff、staged changes、PR summary 中提炼主意图并生成合适的 commit message
- 在 squash merge 场景下概括整组改动，而不是简单拼接中间提交
