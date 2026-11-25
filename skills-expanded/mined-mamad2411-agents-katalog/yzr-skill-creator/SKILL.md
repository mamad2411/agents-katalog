---
name: yzr-skill-creator
description: |
  当用户处于 skill 生命周期时使用本 skill：从工作流 / 模板 / 流程 / 决策模式创建新 skill、
  通过 eval-and-iterate（with-skill vs baseline）改进现有 skill、独立优化某个 skill 的触发
  description、或拿写作原则审计 skill 合规性（只报告、不改写）。
  触发："我想 / 帮我 做一个 X 的 skill" / "从零做一个 skill 处理 X" / "把 XX 流程沉淀成
  skill" / "以后能用 / 新人也能用 / 按这个走"；改进 / 评估 / 迭代 XX skill；用户反馈触发
  不准或行为不对；想跑评估；只想动 frontmatter description——用户说"优化描述"是泛指
  （含正文措辞）时也触发。
  不适用：单步问询 / 写普通代码 / 改普通文档（走 yzr-writing-review 等）/ 不涉及 skill
  生命周期的事。
metadata:
  author: Zuoru YANG
  modify time: 2026-08-16
---
# yzr skill creator

这是一个用于创建、改进 skill、独立优化 skill 触发描述，并能校验 skill 写作原则符合度的 skill

## 四个入口

用户进入本 skill 通常属于以下四种之一。先判断用户属于哪一种，再介入（介入路径随条给出）：

1. **创建新 skill** —— 从零做一个 skill（"帮我做一个关于 X 的 skill" / "把这段流程沉淀成
   skill"）。介入：访谈边界 → 起草 SKILL.md（骨架从 `assets/skill-template.md` 拷贝）→
   RED 演练 → eval 验证 → viewer 评审。
2. **改进现有 skill** —— 已有一个 skill，想评估 + 迭代优化它（"改进 yzr-outline-wiki 这
   个 skill"）。介入：快照旧版 → with-skill vs baseline 同轮并行 → 读 transcript 找"模型
   在哪里挣扎"→ 改 → 重跑验证。
3. **优化某个 skill 的描述（独立入口）** —— 只想优化某个已有 skill 的 description /
   触发准确率，不动 skill 正文（"帮我优化 XX 的描述，让它该触发时触发"）。**这是独立
   入口，不需要先创建或改进那个 skill**；脚本 `optimize_description.py`
   原生支持指向任意 skill 目录，详见「工作流 / 步骤」下对应小节
4. **校验某个 skill 的写作原则（独立入口）** —— 不动手改，拿写作原则当 checklist
   审计某个已有 skill 符合多少、违反哪些（"帮我检查 XX skill 写得规不规范 / 有没有
   散弹式散落、口径冲突"）。**只报告、不改写**；要修让用户点头再动。详见
   「工作流 / 步骤」下对应小节

## 何时不使用

"何时使用 / 不适用"已在 frontmatter description，正文不重抄。本节只补**出路**：读 / 改
既有文档走对应专用 skill（`yzr-writing-review` 审改文档）；
目标产物不是 skill（已存在的脚本 / docx / 一段 prose）时直接用基础工具。

## 输入 / 输出

四个入口的输入 / 输出对照：

| 入口 | 用户输入 | skill 交付 |
| --- | --- | --- |
| 1. 创建 | 一句中文意图 + 必要边界 / 样例澄清 | 起草好的 `<skill-name>/SKILL.md` + 骨架，可选的 `eval/evals.json` |
| 2. 改进 | skill 路径 + 诉求（"评估 + 迭代" / "按反馈改写"） | 改写后的 SKILL.md + `<skill-name>-workspace/iteration-N/` 评估产物 + benchmark/viewer |
| 3. 描述优化 | 任意 skill 路径 + 一组 trigger 评估查询（配比见 `references/trigger-eval-guide.md`） | 新 `description` 候选 + before/after 触发准确率（按 `DEFAULT_HOLDOUT_RATIO` 拆分） |
| 4. 原则校验 | 任意 skill 路径 | 审计报告（每条原则 pass/fail + 证据 + 建议修法），不动手改 |

## 执行原则 / 边界

无论走哪个入口，下面这些原则贯穿全程——不是单独某一步的规则，而是 agent 在用本 skill 时应保持的判断基线：

- **元 skill 的"元"特征**：本 skill 的产物是"让 agent 在某类任务上更靠谱"的载体，不是用户最终要的文件；写每段 prose 前先问"下游 agent 读到这里会怎么想"
- **过拟合红线**：用户给的反馈只覆盖少数 prompt；要让 skill 在一百万次调用里都成立，必须从反馈归纳"意图类别"而非把 case 逐条抄进 SKILL.md
- **必须跑评估**：写完不跑 eval = 在赌运气（哪怕 1 个 case 也能暴露"skill 让模型做了无效工作"）；改进时先 `cp -r` 旧版到 workspace 做 baseline，否则"是否更好"无法量化
- **用户说"优化描述"是泛指**：默认包括 frontmatter `description` + 标题 + 章节 +
  when-to-use 措辞 + 操作步骤，不默认专指 frontmatter；用户要细分会用精确措辞
  （"只改 frontmatter" / "只动 description 字段"）。维度分清：frontmatter 只决定
  "何时调"、正文决定"怎么用"——入口 3 只动前者，入口 1/2 才动正文
- **writer 与 grader 分离**：跑评估的子 agent 跟打分的子 agent 不要合并，否则 grader
  会偏向自己刚写的版本（grader 盲评约定见 `references/agents/grader.md`）
- **指标单一来源**：脚本里有 `CONST = value` 的，prose 用 `` `CONST` `` 引用，禁止写字面量
  ——本 skill 自身在 `scripts/utils.py::DESCRIPTION_MAX_CHARS`、
  `scripts/optimize_description.py::DEFAULT_HOLDOUT_RATIO` 带头遵守（原则见
  `references/skill-writing-principles.md`）
- **与用户沟通**：skill 使用者编程背景差异大——术语（eval / holdout / baseline 等）先给
  一句人话解释

## 工作流 / 步骤

创建 / 改进一个 skill 的主要流程如下（入口 3、4 是独立入口，见本节尾部两个小节）：

1. 明确你希望这个 skill 做什么，以及大致如何实现
2. **不带 skill 跑典型 prompt 观察失败（RED 阶段）**——细节与原则见
   「创建一个 skill · baseline 演练（RED 阶段）」（典型 prompt 条数在该节，此处不重抄）；**纯参考资料型 skill 可跳过**
3. 起草一份 skill（改进场景下是编辑现有 skill）——**针对 RED transcript 观察到的具体违规做最小封堵**，不预堵"可能存在的"漏洞
4. 设计几个测试 prompt，让能访问该 skill 的 agent 在这些 prompt 上跑一遍
5. 协助用户对结果进行定性和定量两方面的评估（细节见「运行与评估测试用例」）
6. 根据用户对结果的反馈（以及定量基准中暴露出的明显缺陷）改写 skill
7. 重复上述过程，直到满意为止
8. **收敛后扩量再验证（防过拟合的最后一道闸）**：初轮几个 prompt 反复迭代收敛后，把测试集扩到 5–10 条（覆盖更广的意图类别 + 相邻负例），再跑一轮完整评估——小样本收敛 ≠ 大样本成立，扩量能暴露"过拟合到少数 case"的残留问题

使用时判断用户处于流程哪一阶段再介入：从零做 → 澄清需求、起草初稿、编测试用例、设计评估、
反复迭代；已有草稿 → 直接进评估 / 迭代。用户说"不跑评估，直接头脑风暴"时照做。

### 创建一个 skill

#### 意图识别与访谈

先理解用户的意图。当前对话可能已包含用户希望捕获的工作流（如"把这段流程沉淀成 skill"）——
若是，先从对话历史抽取答案：用到了哪些工具、步骤顺序、用户做了哪些修正、观察到的
输入/输出格式。再主动补齐缺口，梳理清楚之前先不写测试 prompt，需要确认的：

1. 这个 skill 应该让 agent 能做什么？
2. 应该在什么时机触发？（什么样的用户表述/上下文）
3. 期望的输出格式是什么？
4. 是否需要设置测试用例来验证 skill 是否可用？（可客观验证输出的 skill——文件转换、
   数据抽取、代码生成、固定工作流步骤——测试用例有益）
5. 边界情况、示例文件、成功标准、依赖项等

调研：检查可用的 MCP，对调研有帮助（搜索文档、查找类似 skill、查阅最佳实践）且支持
子 agent 时并行调研，否则直接内联进行。

#### baseline 演练（RED 阶段）

> 原则见 `references/skill-writing-principles.md`「Iron Law」。

不写 skill，先用旧版 skill（改进场景）或完全不带 skill（创建场景）跑 2–3 个典型 prompt——

- **创建场景**：完全不带 skill 跑 prompt，让 agent 用基础能力自由发挥，记录它**怎么违反**（哪些规则被跳 / 哪些步骤被漏 / 用了什么借口逐字摘抄）。
- **改进场景**：用当前版本的 skill 跑 prompt，记录**还错在哪**（旧 skill 没堵住的口子 / agent 找出的新借口）。

这些 transcript 作为起草 skill 的**输入**——skill 不是凭空设计，是**针对观察到的违规做最小封堵**。
后续 Rationalization Table + Red Flags 的素材都来自这里。**纯参考资料型 skill 跳过**。

#### 起草 SKILL.md

基于用户访谈的结果，填充以下组件。YAML frontmatter 的字段描述：要求精简、明确，
不要过于冗长，也不要过于模糊：

1. `name`：skill 的名字
2. `description`：按 `assets/skill-template.md` 的 frontmatter 占位符填——格式三组件
   （场景一句 + 触发： + 不适用：）与写法原则的 SSOT 在
   `references/skill-writing-principles.md`「description 优化原则」，不在此重抄
3. `allowed-tools`：限制使用的工具，可选字段，如果没有，则置空
4. `metadata`：用户自定义字段，当前主要是作者（Zuoru YANG）、最后修改时间、skill 分类标签等信息

后面为 skill 的正文——**骨架从 `assets/skill-template.md` 拷贝**，逐节填充（规范节名 / 顺序 /
各类型豁免的 SSOT 在 `scripts/utils.py::CANONICAL_BODY_SECTIONS`，变体规则见
`references/skill-template-guide.md`「变体」）。先填全骨架再按「精简与粒度约束」删节，不要"想到哪写到哪"——
SKILL.md 格式统一靠的就是这份骨架。

起草完成后先跑预检再进入测试用例：
`python -m scripts.quick_validate <skill-dir>`（frontmatter 合法性 + 正文结构 + description
格式标记；WARN 级提示不阻断）。

#### 写作骨架指南

通用骨架 / 写作模式模板见 `references/skill-template-guide.md`；写作风格与语言原则见
`references/skill-writing-principles.md`「正文写作原则」——不在此重抄 agent 通识。

#### 测试用例

写完 skill 草稿后，设计几个测试 prompt（条数与「baseline 演练（RED 阶段）」同量级）——真实用户实际会说的话
跟用户确认：这是我准备跑的几个测试用例，你看这样 OK 吗？要不要再补几个？然后跑起来

测试用例存到 `eval/evals.json`（结构见 `references/schemas.md`）。先不写断言，只写
prompt，等下一步再起草断言。

### 运行与评估测试用例

本节是连续流程，不要中途停下来。

- workspace 在 `<skill-name>-workspace/`（与 skill 目录同级），按
  `iteration-N/eval-<N>/{with_skill|without_skill|old_skill}/outputs/` 嵌套（后两者是
  baseline 角色）；目录边做边建
- with-skill 与 baseline 在**同一轮**并行启动（不要串行）；baseline 类型：
  - 入口 1（创建）→ `without_skill/`
  - 入口 2（改进）→ `old_skill/`（编辑前先 `cp -r` 快照旧版到 `skill-snapshot/`）

5 步细节（启动 + 起草断言 + 采时序 + 评分聚合 + 读反馈、viewer 口径、
`eval_metadata.json` / `timing.json` / `grading.json` schema、`aggregate_benchmark.py` /
`generate_review.py` 用法）见 `references/eval-pipeline.md`。

### 改进 skill

跑过测试用例、用户评审过结果后，根据反馈迭代——迭代原则（从反馈归纳泛化 / 保持精简 /
解释"为什么" / 找跨用例重复工作进 `scripts/`）见 `references/skill-writing-principles.md`
「精简与粒度约束」+「解释为什么」+「机械操作脚本化」三条，此处不重抄。

#### 迭代循环

完成改进后：(1) 应用改动 → (2) 跑新 `iteration-<N+1>/`（**含** baseline，baseline
取值：创建场景始终 `without_skill`；改进场景：用户最初版本 or 上一轮迭代，由你判）→
(3) `--previous-workspace` 启动 reviewer → (4) 等用户评审完 → (5) 读 `feedback.json`
继续循环。

#### 堵 loophole（REFACTOR 阶段）

> 原则见 `references/skill-writing-principles.md`「Iron Law」+「反合理化」。

每次迭代结束 + 读 transcript 后：(1) 识别新合理化（agent 又用什么借口绕禁令）；
(2) 加进 Rationalization Table（**只**补 agent 实际说过的——预写"可能存在"借口是反模式）；
(3) 对应红旗征兆若有缺则补 Red Flags；(4) agent 是否用看似不同但效果一致的手法绕禁令
→ 在"违反字面 = 违反精神"里加新案例；(5) 重测同批 prompt，新借口应不再出现；
仍出现 = 回 GREEN 重写。

#### Concision review（每轮迭代必做）

下轮改动前对每段答「精简与粒度约束」三问（哪段必需？哪段是 agent 常识冗余？哪段是 case 抄进去的
过拟合？），处理顺序按修法优先级——见 `references/skill-writing-principles.md`「精简与粒度约束」。

停止条件：用户满意 / 反馈全空 / 看不到有意义的进展。

### 描述优化（独立入口）

> 优化原则见 `references/skill-writing-principles.md#description-优化原则`
> （`optimize_description.py` 运行时也读这一节）。

直接优化某个已有 skill 的 description，提升触发准确率。`--skill-path` 原生支持
任意 skill 目录——刚创建/改进完想顺手优化也一样走这套流程。

#### 第 1 步：生成触发评估查询

生成评估查询（数量 / should-trigger 配比 / 写作指南见 `references/trigger-eval-guide.md`），
存为 JSON。

#### 第 2 步：与用户过一遍

用 `assets/eval_review.html` 模板把评估集呈现给用户审阅（占位符替换与下载反馈的
机械步骤见 `references/trigger-eval-guide.md`）。

#### 第 3 步：运行优化循环

告诉用户：这一步会花一些时间，我会在后台跑优化循环，并定期检查进度。
把评估集存到 workspace，然后后台运行:

```bash
python -m scripts.optimize_description \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --max-iterations 5 \
  --verbose
```

`--model` 可选：省略时 `claude -p` 用本机 claude CLI 的默认模型（不强绑定具体模型）；
要指定时传 `--model <id>`。跑的过程中定期 tail 输出，告知用户当前在第几轮、分数长什么样。
脚本自动把评估集按 `DEFAULT_HOLDOUT_RATIO` 拆训练 / 保留测试（SSOT 在
`scripts/optimize_description.py`）。结束时会打印 before/after 摘要（stderr），
JSON 结果走 stdout。

#### 第 4 步：应用结果

从 JSON 输出取 `best_description`，更新到 skill 的 SKILL.md frontmatter。
向用户展示 before/after，并汇报分数

### 原则校验（独立入口）

拿写作原则当 checklist，审计某个已有 skill 符合多少、违反哪些——frontmatter 合法性 /
指标散落 / 口径冲突 / 章节覆盖 / 触发措辞等，产出 pass/fail 报告。**只审计、不改写**；
要修让用户点头再动或转入口 2。

#### 怎么校验

1. 把 `references/skill-writing-principles.md` 当 checklist（description 优化原则 + 正文
   写作原则 + 末尾「审计速查」表，逐条核对）。
2. 读目标 skill 的 `SKILL.md`（必要时连带 `references/` / `scripts/`）。
3. 逐条核对 → 通过 / 违反（附证据：文件:行 + 具体内容）。能程序化的查：

   | 类别 | 操作 |
   | --- | --- |
   | frontmatter 合法性 + description 固定格式标记（触发： / 不适用：） | `python -m scripts.quick_validate <skill-dir>` |
   | 正文结构一致性（规范节缺失 / 乱序 / 额外节） | `python -m scripts.quick_validate <skill-dir> --tier <default\|reference\|meta>`——WARN 不 fail；节名 SSOT 在 `scripts/utils.py::CANONICAL_BODY_SECTIONS` |
   | 跨 skill 双向依赖 | `python -m scripts.check_skill_dependencies <repo-root>`（"互提" ≠ "互依"，是否成环靠 agent 读正文确认） |
   | 跨文件 link anchor 漂移（spec 演进 / 段号变 / 章节删后无人察觉） | `python -m scripts.check_anchor_health <skill-dir>` 或 `--repo-root` 全扫（`--json` 机器可读 / `--include-templates` 审模板） |

   其余 grep 类检查（正文长度 / 跨文件重复 / 常量引用 / 链接路径基准 / Iron Law / 三件套 /
   形式匹配 / 版本史 / 精简）集中在 principles 末尾「审计速查」表，逐条执行。

4. 产出报告（**只审计、不改写**）——每条 pass / fail + 证据 + 建议修法。

#### 审查深度标准（入口 4 默认口径）

> 用户要求"最严 / 仔细审查"时按此执行；日常原则校验也建议照此深度——只跑速查表机械
> 检查会漏掉"某段是 agent 常识冗余 / 单 case 疤痕组织"这类判断题。

- **全量范围**：`SKILL.md` + `references/` + `scripts/` + `assets/` + `eval/` 每个文件逐行读，
  无抽样；`references/canonical/` 与 `fixtures/*.txt` 是字节金标准，不碰内容，只审自包含注释
  （"与哪份 SSOT 重复 + 理由"）是否齐全
- **逐段精读判据**：每段过「精简与粒度约束」删除测试（"删掉这句，称职 agent 会做错吗？"）+
  等价三问；审计速查表（`references/skill-writing-principles.md`）逐条判——description 组与正文组都要过，
  不只跑程序化项；**精简结论须列出"考虑过删但保留"的边缘段 + 一句保留理由**（删除测试为何
  通过），不能只给"全过"汇总——否则"全过"不可验证。**保留理由必须是删除测试的正面答案**：
  "删掉它，agent 会在哪个具体场景做错？"——禁止用"合理分工 / 与详述不冲突 / 不违规"这类
   合规性措辞当保留理由（合规 ≠ 必要；不违规 ≠ 该留）。**默认值 = 删**：对每个块（无论新旧
   体裁）先假设删、找不到保留理由就砍——删除测试必须**存量回测**（含 ASCII 图 / 表格等"结构
   重工"产物，分层图 / 归属表 / 边界节承载同一信息时只留一份），禁止只对有重复嫌疑的块跑测试
   （增量审计会把旧结构默认放行）；"作者刻意设计的"不构成保留理由。**正确性以验证证据为准**（速查表
  Iron Law 证据行）：审计者不凭精读断言建议对错，无 baseline / eval 证据的纪律型 / 模式型
  内容按"未经验证"报，不主观判"对 / 错"
- **脚本逐行标准**：死代码 / 冗余 import / 参数遮蔽 / 未转义注入（`</script>` 类）/ 字面量
  重抄常量 / 应计算却硬编码的值
- **报告分级**：fail 按 P1 真实 bug / P2 代码质量 / P3 口径散落分级，每条附
  `文件:行` 证据 + 修法；**P4 观察项必须给"保留 vs 砍"的明确建议**——保留者附删除测试
  正面理由，建议砍者直接进修复清单，不允许"观察项 = 默认不动"的死档；pass 项计数汇总
  （要展开逐条列出时再说）
- **修复流**：逐项等用户确认 → 修（只动仓库源，不手拷 vendored）→ quick_validate +
  markdownlint + ruff 验证 → commit + push（用户经 npx 同步 vendored）→ git 确认

## 参考样例

> 入口判断 + 介入路径已在「四个入口」逐条给出——此处只留一个最典型的映射做直观示例：
>
> 用户："这个 yzr-outline-wiki skill 在上传大文档时总吞换行，你帮我改进一下"
>
> → 入口 2（改进）：快照旧版 → with-skill vs baseline → 看 transcript 找"模型在哪里挣扎" → 改 → 重跑验证

## 参考文件

`references/agents/` 目录包含专用子 agent 的指令。需要启动相关子 agent 时读取。

- `references/agents/grader.md` —— 如何对照输出评估断言
- `references/agents/benchmark-analyzer.md` —— 如何分析 benchmark 聚合结果（评估流程第 4 步）

`references/` 补充文档:

- `references/schemas.md` —— evals.json、grading.json 等的 JSON 结构
- `references/trigger-eval-guide.md` —— 描述优化的查询写作指南 + 触发原理 + 审阅页步骤
- `references/skill-template-guide.md` —— 通用写作骨架 / 模板 / 变体规则
- `references/skill-writing-principles.md` —— description + 正文写作原则 + 末尾审计速查表（SSOT）
- `references/eval-pipeline.md` —— 评估测试用例的机械细节（workspace 布局 / schema / 命令）

`assets/`:

- `assets/skill-template.md` —— 可拷贝的 SKILL.md 正文骨架（起草新 skill 时用）
- `assets/eval_review.html` —— 描述优化第 2 步的查询评审页模板

`scripts/` 常量 SSOT:

- `scripts/utils.py::CANONICAL_BODY_SECTIONS` —— 正文规范节名 / 顺序 / 豁免（节名列表唯一真源）
- `scripts/utils.py::DESCRIPTION_MAX_CHARS` —— description 长度硬上限
