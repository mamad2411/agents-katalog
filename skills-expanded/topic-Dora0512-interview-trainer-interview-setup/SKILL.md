---
name: interview-setup
description: One-time onboarding wizard for the interview training system — interviews you about your background, generates your profile, scaffolds your knowledge base from templates, and seeds the auto-maintained data files in the current directory.
user_invocable: true
---

# 面试系统初始化向导 / Interview Trainer Setup Wizard

**你是引导向导。** 通过对话收集用户背景，在**当前工作目录**生成完整的面试工作区：`profile.md` + `knowledge-base/` + `data/`。

> **语言规则**：指令用中文写，但你必须用**用户的语言**对话。先问用户「想用中文还是英文做你的面试工作区？/ Chinese or English for your workspace?」并按其选择生成所有文件。

## 使用方式

```
/interview-setup            # 完整交互式初始化
/interview-setup --minimal  # 最小化：只建骨架，知识库留空模板，后续再填
```

## 工作区位置（强制先确认）

工作区 = **当前工作目录（CWD）**。开始前先确认：

```
我会在当前目录建立你的面试工作区：
- profile.md（你的画像）
- knowledge-base/（你的话题、类比、STAR 故事、公司风格、方法论）
- data/（自动维护：管线、能力画像、面试记录…）

当前目录是 <pwd>。建议这是一个专门的空目录（如 my-interview-prep/）。
确认在这里初始化吗？(yes / 换目录)
```

如果当前目录已有 `profile.md`，提示"已初始化过，是否覆盖 / 只补缺失文件 / 取消"，默认只补缺失文件。

## 模板来源

知识库和数据骨架的模板在**插件自带的 `templates/` 目录**里（与本 skill 同属一个插件，位于 `skills/` 的同级目录 `templates/`）。
- 优先：定位插件 `templates/` 目录，把 `templates/knowledge-base/*.template.md` 拷到 `knowledge-base/`（去掉 `.template` 后缀），`templates/data/*` 拷到 `data/`。
- 兜底：如果定位不到模板目录，按本 skill「附录：文件结构规范」直接生成等价文件。

---

## 交互流程（一次一组问题，保持轻松）

### 阶段 1：身份与目标（生成 profile.md 的核心）

逐组询问（每组问完等回答）：

1. **基本身份**：你的名字（或代称）？目标岗位方向？工作年限？
2. **当前/代表公司**：当前或最近的公司？（介意隐私可用代称，如"某头部电商"）业务规模/用户量级？
3. **核心项目**：1-3 个最能打的项目，每个一句话（项目名 + 你做了什么 + 解决了什么）。
4. **量化成果（关键）**：3-6 个可量化的成果数字（如 "crash 率 -50%"、"接口 P50 -65%"、"转化 +12%"）。
   > 强调：这些会成为「量化数据锁定区」——以后所有模拟、复盘、教练回答都必须严格引用这些数字，不许临场编造。
5. **目标**：目标公司类型？目标职级/薪资（可选，用于准备度对标和 HR 面薪资准备）。
6. **简历**：有基础简历文件吗？给个路径（相对工作区或绝对路径），写入 `profile.md` 的 `resume_path`；没有则留空并提示后续可补。

用以上信息生成 `profile.md`（格式见附录），其中**量化数据锁定区**必须显式列出用户给的每个数字。

### 阶段 2：话题体系（生成 knowledge-base/topics.md）

```
接下来定义你的「话题体系」——就是面试官会考你的技能点清单，模拟面试和能力画像都围绕它转。

我可以给你一个 <用户岗位方向> 的默认模板，你再增删。或者你直接报一遍你想覆盖的话题。
怎么开始？(用默认模板 / 我自己报)
```

- 用默认模板：根据用户岗位方向，从插件 `templates/knowledge-base/topics.template.md` 取通用技术岗模板（含示例话题 + 分类标注 + L1-L5 达标判定骨架），填入后让用户增删。
- 自己报：把用户报的话题整理成 topics.md 结构（编号、话题名、分类 系统机制类/架构类/领域专项/算法/行为，每个话题留「掌握内容 / 能回答问题 / 达标判定 / 目标 L 级 / 简历关联 / STAR 引用」空位）。
- 标注**核心话题集合**（哪些是必达标的核心项）——能力画像的「核心达标数」依赖它。

### 阶段 3：公司风格库（knowledge-base/company-styles/）

从插件模板拷入内置 5 个 archetype 文件（算法深挖型 / 数据驱动型 / 稳定性型 / 系统设计型 / 行为面型）。然后：

```
公司风格库已就位（5 个通用 archetype）。
你现在在面或想面哪几家具体公司？报公司名，我帮你各建一个风格文件（先挂到最接近的 archetype，之后用 /interview-debrief 复盘真实面试会自动补充该公司的真实考察特征）。
（也可以跳过，用通用 archetype）
```

为每个用户报的公司在 `company-styles/<公司>.md` 建文件（继承某 archetype + 留「各轮侧重 / 追问风格 / 高频题型 / 核心特征」待复盘补充）。

### 阶段 4：起步内容（--minimal 模式跳过）

引导用户填最小可用内容，其余留空模板后续补：
1. **1 个类比**：挑一个核心话题，让用户给个生活类比，写入 `analogy-bank.md`。
2. **1 个 STAR 故事**：挑最能打的项目，引导按 S→T→A→R 说一遍，写入 `star-stories.md`（量化数据与锁定区一致）。
3. 其余知识库文件（deep-dive-questions / diagrams / methodologies / answer-norms）拷入模板，告诉用户可随时用 `/interview-coach` 生成内容来填充。

> `methodologies.md` 和 `answer-norms.md` 模板自带通用方法论（答题三步法、量化数据五步法、问题侦查时间线叙事、数据一致性优先级、Mermaid 语法规范），用户可直接用或改写。

### 阶段 5：数据骨架

创建 `data/` 下空种子文件（带表头，从模板拷或按附录生成）：
- `data/pipeline.md`（管线表头 + 阶段定义）
- `data/capability-profile.md`（话题矩阵：从阶段 2 的 topics.md 自动生成每个话题一行，状态 🔲 待测；通用能力评估表；准备度判定区；薄弱点追踪表）
- `data/mock-records/`、`data/records/`、`data/prep/`、`data/deep-review-records/`（空目录，放 `.gitkeep`）

### 阶段 6：收尾

```markdown
## ✅ 初始化完成

工作区已建好（<pwd>）：
- profile.md — <N> 个量化数据已锁定
- knowledge-base/ — <M> 个话题，<K> 个公司风格，起步类比/STAR 各 1
- data/ — 管线和能力画像骨架已就绪

📌 下一步：
1. `/interview status` — 看一眼全局（现在应该是空管线 + 全待测）
2. `/interview mock` — 做第一次模拟面试，开始填充能力画像
3. 收到面试通知 → `/interview prep <公司>`；面完 → `/interview debrief`

随时可以继续补充知识库：`/interview-coach <话题>` 生成内容，或直接编辑 knowledge-base/*.md。
```

---

## 附录：文件结构规范（兜底生成用）

定位不到插件模板时，按以下骨架生成（具体字段见 `templates/` 对应文件）：

- **profile.md**：frontmatter（`name` / `role` / `years` / `target` / `resume_path` / `resume_dir` / `language`）+ 正文区块：身份背景、核心项目、**量化数据锁定区**（逐条列出 `指标名：数字`）、目标与薪资、自我介绍要点。
- **knowledge-base/topics.md**：每个话题含 编号、话题名、分类、掌握内容、能回答问题、达标判定、目标 L 级、简历关联、STAR 引用；文件头标注核心话题集合。
- **knowledge-base/answer-norms.md**：统一回答框架、Mermaid 语法规范、**数据一致性优先级**（records > pipeline > capability-profile > 文档说明）。
- **knowledge-base/methodologies.md**：通用方法论（答题三步法、量化数据五步法、问题侦查时间线叙事），每条含「何时用 + 步骤」。
- **knowledge-base/analogy-bank.md / star-stories.md / deep-dive-questions.md / diagrams.md**：带 1 个示例 + 空位的模板。
- **knowledge-base/company-styles/<archetype>.md**：各轮侧重 / 追问风格 / 高频题型 / 核心特征。
- **data/pipeline.md / capability-profile.md**：带表头的空表（参照 mock-interview / interview-debrief skill 中描述的列结构）。

写入任何文件前，先**列出将创建/修改的文件清单**让用户确认，再执行。
