---
name: skill-creator
description: 创建新 skill、修改并改进现有 skill，以及衡量 skill 的表现。当用户想从零开始创建 skill、编辑或优化现有 skill、运行评测（eval）来测试 skill、带方差分析地对 skill 性能做基准测试，或优化 skill 的 description 以获得更准确的触发效果时使用。
---

# Skill Creator

一个用于创建新 skill 并迭代改进它们的 skill。

从宏观上看，创建 skill 的流程大致如下：

- 决定你想让 skill 做什么，以及大致怎么做
- 写出 skill 的草稿
- 创建几个测试提示词，用能访问该 skill 的 claude 来运行它们
- 帮助用户从定性和定量两个角度评估结果
  - 在后台运行进行的同时，如果还没有定量评测，就起草一些（如果已有，可以原样使用，也可以在你觉得需要改动时修改）。然后向用户解释这些评测（如果它们已经存在，就解释已有的那些）
  - 使用 `eval-viewer/generate_review.py` 脚本把结果展示给用户查看，同时让他们查看定量指标
- 根据用户对结果的评估反馈重写 skill（如果定量基准暴露出明显缺陷，也据此修改）
- 重复直到你满意为止
- 扩大测试集，以更大规模再试一次

你在使用这个 skill 时的任务，是判断用户处于这个流程的哪个阶段，然后介入并帮助他们推进这些阶段。比如，用户可能会说"我想为 X 做一个 skill"。你可以帮助他们明确需求、写草稿、写测试用例、确定评估方式、运行所有提示词，如此循环。

另一种情况，用户可能已经有了 skill 的草稿。这时你可以直接进入评测/迭代环节。

当然，你应该始终保持灵活——如果用户说"我不需要跑一堆评测，跟着感觉来就行"，你完全可以照做。

然后在 skill 完成后（顺序同样可以灵活调整），你还可以运行 skill 描述优化器——我们有一个专门的脚本——来优化 skill 的触发。

明白？明白。

## 与用户沟通

使用 skill creator 的人对编程术语的熟悉程度可能天差地别。你可能还没听说（怎么可能听说呢，这事最近才开始流行）：现在有股潮流，Claude 的强大能力正激励着水管工打开终端、父母和祖父母辈去谷歌搜索"how to install npm"。当然，大部分用户可能还是相当懂电脑的。

所以请注意上下文线索，以此决定你的措辞！默认情况下，给你一个大致的参考：

- "evaluation"和"benchmark"处于边缘地带，但还可以接受
- 对于"JSON"和"assertion"这类词，你要先看到用户给出明确的信号、表明他们理解这些概念，才能不加解释地直接使用

如果有疑问，简短解释一下术语是没问题的；如果不确定用户是否能看懂，随时可以用一句简短的定义来澄清术语。

---

## 创建 skill

### 捕捉意图

从理解用户的意图开始。当前对话中可能已经包含用户想要沉淀下来的工作流（比如他们说"把这个变成一个 skill"）。如果是这样，先从对话历史中提取答案——用过的工具、步骤的顺序、用户做过的修正、观察到的输入/输出格式。空缺之处可能需要用户来补充，在进入下一步之前应让用户确认。

1. 这个 skill 应该让 Claude 能够做什么？
2. 这个 skill 应该在什么时候触发？（什么样的用户措辞/上下文）
3. 期望的输出格式是什么？
4. 我们是否应该建立测试用例来验证 skill 有效？输出可客观验证的 skill（文件转换、数据提取、代码生成、固定工作流步骤）能从测试用例中受益。输出偏主观的 skill（写作风格、艺术）通常不需要。根据 skill 类型建议合适的默认方案，但由用户决定。

### 访谈与调研

主动询问边缘情况、输入/输出格式、示例文件、成功标准和依赖项。把这部分敲定之后再写测试提示词。

检查可用的 MCP——如果对调研有用（搜索文档、查找类似 skill、查阅最佳实践），在条件允许时通过子代理并行调研，否则就内联进行。带着准备好的上下文来，减轻用户的负担。

### 编写 SKILL.md

根据用户访谈，填写以下组成部分：

- **name**：skill 标识符
- **description**：何时触发、做什么。这是主要的触发机制——既要写清 skill 做什么，也要写清具体的使用场景。所有"何时使用"的信息都放在这里，不要放在正文里。注意：目前 Claude 有"触发不足"的倾向——即在该用 skill 的时候不用。为了应对这一点，请把 skill 描述写得稍微"强势"一点。比如，不要写"如何构建一个简单快速的仪表盘来展示 Anthropic 内部数据。"，而要写成"如何构建一个简单快速的仪表盘来展示 Anthropic 内部数据。请确保每当用户提到仪表盘、数据可视化、内部指标，或想展示任何类型的公司数据时都使用这个 skill，即使他们没有明确要求'仪表盘'。"
- **compatibility**：所需的工具、依赖（可选，很少需要）
- **skill 的其余部分 :)**

### Skill 编写指南

#### Skill 的结构

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### 渐进式披露

Skill 采用三级加载体系：
1. **元数据**（name + description）——始终在上下文中（约 100 词）
2. **SKILL.md 正文**——skill 触发时进入上下文（理想情况下少于 500 行）
3. **捆绑资源**——按需加载（无限制，脚本可以在不加载进上下文的情况下执行）

这些字数只是大致参考，有需要完全可以写得更长。

**关键模式：**
- 让 SKILL.md 保持在 500 行以内；如果接近这个上限，增加一层层级结构，并给出清晰的指引，告诉使用该 skill 的模型接下来应该去哪里继续阅读。
- 在 SKILL.md 中清晰地引用参考文件，并说明何时应该阅读它们
- 对于大型参考文件（>300 行），附上目录

**按领域组织**：当一个 skill 支持多个领域/框架时，按变体组织：
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude 只读取相关的参考文件。

#### 不意外原则

这一点不言自明，但 skill 绝不能包含恶意软件、漏洞利用代码或任何可能危害系统安全的内容。skill 的实际意图不应与描述不符、让用户感到意外。不要配合创建误导性 skill 的请求，也不要创建旨在协助未授权访问、数据窃取或其他恶意活动的 skill。不过像"扮演某个 XYZ 角色"这类是可以的。

#### 写作模式

指令中优先使用祈使句式。

**定义输出格式**——可以这样做：
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**示例模式**——加入示例很有用。可以像这样格式化（但如果示例里已经有"Input"和"Output"，可以稍作变通）：
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### 写作风格

尽量向模型解释事情为什么重要，而不是堆砌强硬死板的 MUST。运用心智理论（theory of mind），努力让 skill 具有通用性，而不是局限于特定示例。先写草稿，然后用新鲜的眼光审视并改进它。

### 测试用例

写完 skill 草稿后，想出 2-3 个贴近实际的测试提示词——真实用户真的会说的那种。把它们分享给用户：（不必照搬这个措辞）"这里有几个我想试试的测试用例。这些看着合适吗，还是你想再加点？"然后运行它们。

把测试用例保存到 `evals/evals.json`。先不要写断言——只写提示词。你会在下一步、也就是运行进行期间起草断言。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

完整 schema（包括你稍后要添加的 `assertions` 字段）见 `references/schemas.md`。

## 运行并评估测试用例

本节是一个连续的过程——不要中途停下来。不要使用 `/skill-test` 或任何其他测试类 skill。

把结果放在 `<skill-name>-workspace/`，与 skill 目录同级。在工作区内按迭代组织结果（`iteration-1/`、`iteration-2/` 等），每个迭代内每个测试用例一个目录（`eval-0/`、`eval-1/` 等）。不要一开始就把这些目录全建好——用到时再建。

### 第 1 步：在同一轮中启动所有运行（with-skill 和 baseline）

对每个测试用例，在同一轮中启动两个子代理——一个带 skill，一个不带。这一点很重要：不要先启动带 skill 的运行，之后再回来补 baseline。一次性全部启动，让它们大致同时完成。

**带 skill 的运行：**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline 运行**（提示词相同，但 baseline 取决于场景）：
- **创建新 skill**：完全不带 skill。提示词相同，不给 skill 路径，保存到 `without_skill/outputs/`。
- **改进现有 skill**：用旧版本。编辑前先给 skill 拍快照（`cp -r <skill-path> <workspace>/skill-snapshot/`），然后把 baseline 子代理指向快照。保存到 `old_skill/outputs/`。

为每个测试用例写一个 `eval_metadata.json`（断言暂时可以为空）。根据每个 eval 测试的内容给它起一个有描述性的名字——不要只是"eval-0"。目录也用这个名字。如果本次迭代使用了新的或修改过的 eval 提示词，就为每个新的 eval 目录创建这些文件——不要假设它们会从之前的迭代继承过来。

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### 第 2 步：运行进行期间，起草断言

不要干等运行结束——可以好好利用这段时间。为每个测试用例起草定量断言，并向用户解释。如果 `evals/evals.json` 里已经有断言，检查一遍并解释它们检查的是什么。

好的断言是客观可验证的，并且有描述性的名字——在基准查看器里要一目了然，让人扫一眼结果就能立刻明白每条断言在检查什么。主观类的 skill（写作风格、设计质量）更适合定性评估——不要强行给需要人工判断的东西加断言。

起草好断言后，更新 `eval_metadata.json` 文件和 `evals/evals.json`。同时向用户说明他们将在查看器中看到什么——定性输出和定量基准都要讲。

### 第 3 步：运行完成时，记录耗时数据

每个子代理任务完成时，你会收到一条包含 `total_tokens` 和 `duration_ms` 的通知。立即把这些数据保存到运行目录下的 `timing.json`：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

这是捕捉这些数据的唯一机会——它通过任务通知传递，不会在其他地方持久化。每收到一条通知就立即处理，不要攒着批量处理。

### 第 4 步：评分、汇总并启动查看器

所有运行完成后：

1. **为每次运行评分**——启动一个 grader 子代理（或内联评分），让它阅读 `agents/grader.md` 并逐条对照输出评估断言。把结果保存到每个运行目录下的 `grading.json`。grading.json 的 expectations 数组必须使用 `text`、`passed`、`evidence` 这几个字段（不要用 `name`/`met`/`details` 或其他变体）——查看器依赖这些确切的字段名。对于可以程序化检查的断言，写个脚本来跑，而不是靠肉眼——脚本更快、更可靠，还能跨迭代复用。

2. **汇总成基准**——从 skill-creator 目录运行汇总脚本：
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   这会生成 `benchmark.json` 和 `benchmark.md`，包含每种配置的 pass_rate、耗时和 token 数，以及均值 ± 标准差和差值。如果是手工生成 benchmark.json，查看器所期望的确切 schema 见 `references/schemas.md`。
   把每个 with_skill 版本排在它对应的 baseline 之前。

3. **做一轮分析师检查**——阅读基准数据，挖掘汇总统计可能掩盖的模式。要看什么见 `agents/analyzer.md`（"分析基准结果"一节）——比如无论有没有 skill 都总是通过的断言（没有区分度）、方差很高的 eval（可能不稳定）、时间/token 的取舍等。

4. **启动查看器**，同时呈现定性输出和定量数据：
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   第 2 次及以后的迭代，还要传 `--previous-workspace <workspace>/iteration-<N-1>`。

   **Cowork / 无头环境：** 如果 `webbrowser.open()` 不可用或环境没有显示器，改用 `--static <output_path>` 写出一个独立的 HTML 文件，而不是启动服务器。用户点击"Submit All Reviews"时，反馈会以 `feedback.json` 文件的形式下载。下载后，把 `feedback.json` 复制到工作区目录，供下一次迭代读取。

   注意：请使用 generate_review.py 来创建查看器；没有必要自己写 HTML。

5. **告诉用户**，大意是："我已经在浏览器里打开了结果。有两个标签页——'Outputs'可以逐个点击查看测试用例并留下反馈，'Benchmark'展示定量对比。看完之后回到这里告诉我一声。"

### 用户在查看器中看到的内容

"Outputs"标签页一次展示一个测试用例：
- **Prompt**：给出的任务
- **Output**：skill 产出的文件，尽可能内联渲染
- **Previous Output**（第 2 次迭代起）：折叠区域，展示上一次迭代的输出
- **Formal Grades**（如果运行了评分）：折叠区域，展示断言通过/失败情况
- **Feedback**：一个文本框，输入时自动保存
- **Previous Feedback**（第 2 次迭代起）：上次的评论，显示在文本框下方

"Benchmark"标签页展示统计摘要：每种配置的通过率、耗时和 token 用量，以及按 eval 的细分和分析师观察。

通过上一步/下一步按钮或方向键导航。完成后，用户点击"Submit All Reviews"，所有反馈会保存到 `feedback.json`。

### 第 5 步：阅读反馈

用户告诉你看完之后，读取 `feedback.json`：

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

反馈为空意味着用户觉得没问题。把改进重点放在用户有具体意见的测试用例上。

用完后关掉查看器服务器：

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## 改进 skill

这是整个循环的核心。你已经跑完测试用例，用户也审阅了结果，现在要根据他们的反馈把 skill 改得更好。

### 如何思考改进

1. **从反馈中归纳。** 这里的大方向是：我们要创建的 skill 是要被用上百万次的（也许是字面意义上的百万，谁知道呢，说不定更多），会用在各种各样的提示词上。现在你和用户只是在一小撮示例上反复迭代，因为这样推进更快——用户对这些示例了如指掌，能快速评估新输出。但如果你和用户共同开发的 skill 只对这几个示例有效，那就毫无价值。遇到顽固问题时，与其加入细碎、过拟合的改动，或者压得死死的 MUST，不如试试换个思路，用不同的比喻，或者推荐不同的工作模式。试一试的成本相对低，说不定就碰上了绝佳方案。

2. **保持提示词精简。** 删掉那些不出力的内容。一定要读运行转录，而不只是最终输出——如果发现 skill 让模型浪费大量时间做无用功，可以试着删掉 skill 里导致这种行为的部分，看看效果如何。

3. **解释原因。** 努力解释你要求模型做的每件事背后的**原因**。今天的 LLM 很*聪明*，有良好的心智理论，配上好的脚手架（harness），它们能超越机械指令，真正把事情做成。即使用户的反馈很简短或带着情绪，也要真正去理解任务、理解用户为什么这么写、他们实际写了什么，然后把这种理解传递到指令里。如果你发现自己在大写 ALWAYS 或 NEVER，或者使用超级僵硬的结构，那是一个黄色预警信号——尽量换个写法，解释推理过程，让模型理解你要求的东西为什么重要。这是一种更人性化、更强大也更有效的方式。

4. **留意跨测试用例的重复工作。** 阅读测试运行的转录，注意子代理们是否各自独立写了相似的辅助脚本，或对某件事采用了同样的多步骤做法。如果 3 个测试用例都导致子代理写了一个 `create_docx.py` 或 `build_chart.py`，这就是很强的信号：skill 应该把这个脚本打包进去。写一次，放进 `scripts/`，并告诉 skill 去用它。这样以后每次调用都不用重新造轮子。

这个任务相当重要（我们可是在努力创造每年数十亿的经济价值！），你的思考时间不是瓶颈；慢慢来，认真琢磨。我建议先写一版修改草稿，然后以全新的眼光重新审视并改进。尽最大努力设身处地理解用户想要什么、需要什么。

### 迭代循环

改进 skill 之后：

1. 把改进应用到 skill 上
2. 把所有测试用例重跑到新的 `iteration-<N+1>/` 目录，包括 baseline 运行。如果你在创建新 skill，baseline 始终是 `without_skill`（不带 skill）——这跨迭代保持不变。如果你在改进现有 skill，自行判断用什么做 baseline 合理：用户最初带来的版本，或上一次迭代的版本。
3. 启动审阅器，用 `--previous-workspace` 指向上一次迭代
4. 等用户审阅并告诉你他们看完了
5. 阅读新反馈，再次改进，如此重复

一直继续，直到：
- 用户表示满意
- 反馈全为空（一切看起来都不错）
- 不再有实质性进展

---

## 进阶：盲测对比

当你想在两个 skill 版本之间做更严格的对比时（比如用户问"新版本真的更好吗？"），有一套盲测对比系统。细节见 `agents/comparator.md` 和 `agents/analyzer.md`。基本思路是：把两个输出交给一个独立代理，不告诉它哪个是哪个，让它判断质量。然后分析胜者为何胜出。

这一步是可选的，需要子代理，大多数用户用不到。人工审阅循环通常已经足够。

---

## 描述优化

SKILL.md frontmatter 中的 description 字段是决定 Claude 是否调用 skill 的主要机制。创建或改进 skill 之后，主动提出优化描述以获得更准确的触发效果。

### 第 1 步：生成触发评测查询

创建 20 条评测查询——应触发和不应触发的混合。保存为 JSON：

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

这些查询必须真实，是 Claude Code 或 Claude.ai 用户真的会输入的内容。不是抽象的请求，而是具体、有相当多细节、有针对性的请求。比如文件路径、关于用户工作或处境的个人背景、列名和值、公司名、URL。带点背景故事。有些可以是小写，或包含缩写、错别字、口语表达。长短混合，多关注边缘情况，而不是非黑即白的（用户有机会确认这些查询）。

差的例子：`"格式化这份数据"`、`"从 PDF 中提取文字"`、`"创建一个图表"`

好的例子：`"ok，我老板刚发给我一个 xlsx 文件（在我的下载文件夹里，名字大概是 'Q4 sales final FINAL v2.xlsx'），她想让我加一列，用百分比显示利润率。收入在 C 列，成本应该在 D 列"`

对于**应触发**的查询（8-10 条），考虑覆盖面。同一意图要有不同措辞——有些正式，有些随意。要包含用户没有明确说出 skill 名或文件类型、但显然需要它的情况。加入一些不常见的用例，以及本 skill 与其他 skill 竞争但应该胜出的情况。

对于**不应触发**的查询（8-10 条），最有价值的是"差一点点"的那些——与 skill 共享关键词或概念、但实际需要别的东西的查询。想想相邻领域、朴素关键词匹配会误触发但不该触发的含糊措辞，以及查询涉及 skill 能做的某件事、但在该上下文中另一个工具更合适的场景。

要避免的关键一点：不应触发的查询不要明显不相关。把"写一个斐波那契函数"作为 PDF skill 的负例就太简单了——它什么都测不出来。负例应该真的有迷惑性。

### 第 2 步：与用户一起审阅

使用 HTML 模板把评测集呈现给用户审阅：

1. 从 `assets/eval_review.html` 读取模板
2. 替换占位符：
   - `__EVAL_DATA_PLACEHOLDER__` → 评测项的 JSON 数组（不要加引号——这是 JS 变量赋值）
   - `__SKILL_NAME_PLACEHOLDER__` → skill 的名字
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → skill 当前的描述
3. 写到临时文件（例如 `/tmp/eval_review_<skill-name>.html`）并打开：`open /tmp/eval_review_<skill-name>.html`
4. 用户可以编辑查询、切换是否应触发、增删条目，然后点击"Export Eval Set"
5. 文件会下载到 `~/Downloads/eval_set.json`——检查 Downloads 文件夹里最新的版本，以防有多个（比如 `eval_set (1).json`）

这一步很重要——糟糕的评测查询会导致糟糕的描述。

### 第 3 步：运行优化循环

告诉用户："这需要一些时间——我会在后台运行优化循环，并定期查看进度。"

把评测集保存到工作区，然后在后台运行：

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

使用你系统提示中的模型 ID（即驱动当前会话的那个模型），这样触发测试才符合用户的实际体验。

运行期间，定期 tail 输出，向用户汇报进行到第几轮迭代、得分如何。

它会自动完成整个优化循环：把评测集按 60% 训练集、40% 留出测试集划分，评估当前描述（每条查询跑 3 次以获得可靠的触发率），然后根据失败情况调用 Claude 提出改进建议。每个新描述都会在训练集和测试集上重新评估，最多迭代 5 次。完成后，它会在浏览器中打开一份 HTML 报告，展示每轮迭代的结果，并返回包含 `best_description` 的 JSON——按测试集得分而非训练集得分选出，以避免过拟合。

### skill 触发机制的工作原理

理解触发机制有助于设计更好的评测查询。skill 以 name + description 的形式出现在 Claude 的 `available_skills` 列表中，Claude 根据描述决定是否查阅某个 skill。需要知道的重要一点是：Claude 只会在自己无法轻松处理的任务上查阅 skill——像"读取这个 PDF"这样简单的一步式查询，即使描述完全匹配也可能不会触发 skill，因为 Claude 用基础工具就能直接处理。复杂、多步骤或专业性强的查询，在描述匹配时会可靠地触发 skill。

这意味着你的评测查询应该有足够的实质内容，让 Claude 确实能从查阅 skill 中受益。像"读取文件 X"这样的简单查询是糟糕的测试用例——无论描述写得多好，它们都不会触发 skill。

### 第 4 步：应用结果

从 JSON 输出中取出 `best_description`，更新 skill 的 SKILL.md frontmatter。向用户展示前后对比并报告得分。

---

### 打包与呈现（仅当 `present_files` 工具可用时）

检查你是否有 `present_files` 工具的访问权限。如果没有，跳过这一步。如果有，打包 skill 并把 .skill 文件呈现给用户：

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

打包完成后，把生成的 `.skill` 文件路径告知用户，让他们安装。

---

## Claude.ai 专属说明

在 Claude.ai 中，核心工作流是一样的（草稿 → 测试 → 审阅 → 改进 → 重复），但因为 Claude.ai 没有子代理，有些机制需要调整。以下是适配方式：

**运行测试用例**：没有子代理意味着无法并行执行。对每个测试用例，先读 skill 的 SKILL.md，然后自己按照其中的指令完成测试提示词。一次做一个。这不如独立子代理严格（skill 是你写的，运行它的也是你，你掌握全部上下文），但作为健全性检查是有用的——人工审阅环节也会弥补这一点。跳过 baseline 运行——直接用 skill 按要求完成任务即可。

**审阅结果**：如果打不开浏览器（比如 Claude.ai 的 VM 没有显示器，或你在远程服务器上），完全跳过浏览器审阅器。改为直接在对话中呈现结果。对每个测试用例，展示提示词和输出。如果输出是用户需要查看的文件（比如 .docx 或 .xlsx），把它保存到文件系统并告诉用户位置，让他们下载查看。内联征求反馈："这个看起来怎么样？有什么要改的吗？"

**基准测试**：跳过定量基准测试——它依赖 baseline 对比，没有子代理就没有意义。专注收集用户的定性反馈。

**迭代循环**：与之前相同——改进 skill、重跑测试用例、征求反馈——只是中间没有浏览器审阅器。如果你有文件系统，仍然可以把结果按迭代目录组织。

**描述优化**：本节需要 `claude` CLI 工具（具体来说是 `claude -p`），它只在 Claude Code 中可用。如果你在 Claude.ai 上，跳过这部分。

**盲测对比**：需要子代理。跳过。

**打包**：`package_skill.py` 脚本在任何有 Python 和文件系统的地方都能运行。在 Claude.ai 上，你可以运行它，用户可以下载生成的 `.skill` 文件。

**更新现有 skill**：用户可能是要你更新一个现有 skill，而不是创建新的。这种情况下：
- **保留原名。** 记下 skill 的目录名和 `name` frontmatter 字段——原样使用，不要改。例如，如果已安装的 skill 是 `research-helper`，就输出 `research-helper.skill`（而不是 `research-helper-v2`）。
- **编辑前先复制到可写位置。** 已安装 skill 的路径可能是只读的。复制到 `/tmp/skill-name/`，在那里编辑，并从副本打包。
- **如果手动打包，先在 `/tmp/` 中暂存**，然后再复制到输出目录——直接写入可能因权限问题失败。

---

## Cowork 专属说明

如果你在 Cowork 中，主要需要知道的是：

- 你有子代理，所以主工作流（并行启动测试用例、跑 baseline、评分等）都能正常运作。（不过，如果遇到严重的超时问题，串行而不是并行运行测试提示词也是可以的。）
- 你没有浏览器或显示器，所以生成评测查看器时，使用 `--static <output_path>` 写出一个独立的 HTML 文件，而不是启动服务器。然后给用户提供一个链接，让他们点击在浏览器中打开 HTML。
- 不知为何，Cowork 环境似乎总让 Claude 在跑完测试后不愿意生成评测查看器，所以再强调一遍：无论你是在 Cowork 还是 Claude Code 中，跑完测试后，在你自己修订 skill 并尝试修正之前，都应该始终生成评测查看器，让人类先看示例，使用 `generate_review.py`（不要自己写定制 HTML）。先道个歉，但我要全大写了：在*自己*评估输入*之前*，先生成评测查看器。要尽快把结果摆到人类面前！
- 反馈的机制不同：由于没有运行中的服务器，查看器的"Submit All Reviews"按钮会把 `feedback.json` 作为文件下载下来。然后你可以从那里读取它（可能得先请求访问权限）。
- 打包是可用的——`package_skill.py` 只需要 Python 和文件系统。
- 描述优化（`run_loop.py` / `run_eval.py`）在 Cowork 中应该能正常工作，因为它通过子进程使用 `claude -p`，而不是浏览器，但请把它留到 skill 完全做完、用户也认可状态良好之后再做。
- **更新现有 skill**：用户可能是要你更新一个现有 skill，而不是创建新的。遵循上面 claude.ai 一节的更新指引。

---

## 参考文件

agents/ 目录包含专门子代理的指令。需要启动相应子代理时再阅读它们。

- `agents/grader.md` —— 如何对照输出评估断言
- `agents/comparator.md` —— 如何在两个输出之间做盲测 A/B 对比
- `agents/analyzer.md` —— 如何分析一个版本为何胜过另一个

references/ 目录有补充文档：
- `references/schemas.md` —— evals.json、grading.json 等的 JSON 结构

---

再强调一遍核心循环：

- 弄清 skill 要做什么
- 起草或编辑 skill
- 用能访问该 skill 的 claude 运行测试提示词
- 与用户一起评估输出：
  - 创建 benchmark.json 并运行 `eval-viewer/generate_review.py`，帮助用户审阅结果
  - 运行定量评测
- 重复，直到你和用户都满意
- 打包最终 skill 并交付给用户

如果你有 TodoList 这类东西，请把步骤加进去，确保不会遗漏。如果你在 Cowork 中，请专门把"创建 evals JSON 并运行 `eval-viewer/generate_review.py`，让人类能审阅测试用例"放进你的 TodoList，确保它得到执行。

祝顺利！
