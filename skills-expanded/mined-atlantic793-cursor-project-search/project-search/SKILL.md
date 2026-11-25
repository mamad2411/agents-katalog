---
name: project-search
description: >-
  Pre-project similar-tech survey across the open web, with GitHub open-source
  repos as the primary source, plus docs, papers, blogs, forums, and model hubs
  when relevant. Compares candidates in chat with links, authority signals, and
  borrowable ideas — does not write survey markdown files. Use when the user
  says /project_search, @project-search, 开调研, 技术调研, 全网搜类似, 先搜开源,
  找类似项目, or asks to research related repos/articles before planning.
  Also treat legacy /project_imitate and @project-imitate as this skill.
  Do NOT use for teaching (project-learn) or time estimates (project-progress).
license: MIT
compatibility: >-
  Requires network access to GitHub and general web sources, plus either the
  GitHub CLI (gh) or web search capability. Works in any agent that follows the
  Agent Skills open standard (Cursor, Claude Code, Codex, etc.).
metadata:
  author: Atlantic793
  version: "0.3.0"
  source: https://github.com/Atlantic793/cursor-project-search
disable-model-invocation: true
---

# Project Search（全网类似技术调研）

开题或做计划前，帮你在**全网**找可借鉴的类似技术/项目/文章，以 **GitHub 开源仓库为主**，其它来源按需补充。在对话里给链接、靠谱信号、可借鉴点。不写业务代码、不 clone、不上课、**不生成调研用 Markdown 文件**。

## 平台兼容

遵循 [Agent Skills 开放标准](https://agentskills.io)，可在 Cursor、Claude Code、Codex、Gemini CLI 等遵守该标准的 agent 中使用，无需改文件。安装路径见仓库 README。

各平台行为差异：

- Cursor：`disable-model-invocation: true` 生效，仅显式口令/`@project-search` 触发
- Claude Code / Codex 等：忽略该字段，可能自动触发；若不想自动触发，用各自的配置文件控制（如 Claude Code 的 `allowed-tools` 与权限设置）
- 搜索工具按平台适配：Cursor/Claude Code 用 WebSearch，Codex 用 web_search，GitHub 部分优先 `gh search repos`（已装 GitHub CLI 时）

## 与其它 Skill 的边界

| 本 Skill 管 | 不管 |
|-------------|------|
| 全网类似技术调研（GitHub 为主） | 原理课、`LEARNING.md` → `project-learn` |
| 候选筛选、权威程度、借鉴点（对话交付） | 用时预估 → `project-progress` |

没听到本 Skill 口令时：不要主动开调研。

## 口令

| 用户说 | 你做 |
|--------|------|
| `/project_search` / `@project-search` / `开调研` / `技术调研` / `全网搜类似` / `先搜开源` / `找类似项目` | 走完整调研流程，结果只在对话里交付 |
| `/project_imitate` / `@project-imitate` | 同上（旧名兼容） |
| `深入 XX-xx`（如 `GH-02`、`WEB-01`） | 再打开该链接，补强简介和可借鉴点；关注等级提升为"推荐关注" |
| `排除 XX-xx` | 关注等级改为"不推荐关注"；之后排序里靠后 |
| `采纳 XX-xx` | 关注等级提升为"最推荐关注"；必要时更新"我的建议" |
| `需求改成…再搜` / `再搜…` | 更新需求摘要/搜索词后增量再搜；保留用户已点名的关注等级 |
| `只留 GitHub` / `偏论文` / `只要中文博客` | 本轮收窄来源 |

## 工作流

1. **听清要什么**（一两句）：交付物、技术偏好、必须有/不能有。已说清就直接搜。
2. **定搜索轴**：任务类型 + 技术栈 + 关键机制；中英文至少各一轮。
3. **联网搜（GitHub 优先，其它按需）**：
   - **GitHub（主）**：优先用 `gh search repos`（若环境已装 GitHub CLI），没有 `gh` 就用环境自带的网页搜索工具搜 `site:github.com`；入选的读 README/简介
   - **联网搜索**：用当前环境可用的搜索工具（Cursor/Claude Code 的 WebSearch、Codex 的 web_search 等）
   - **官方文档 / 标准站**：语言或框架文档、RFC 等（当需求偏 API/用法时）
   - **论文与预印本**：arXiv、OpenReview、Semantic Scholar 等（方法/模型类需求）
   - **模型与数据枢纽**：Hugging Face、Papers with Code（ML 相关时）
   - **技术博客与社区**：Dev.to、Medium、公司工程博客、掘金/CSDN/知乎等（作补充，不默认当主证据）
   - **问答站**：Stack Overflow、GitHub Discussions（排错/选型争议时）
4. **挑**：先贴需求，再比权威程度与可维护性。主列表大约 5–10 条；明显不沾边的别硬塞，可在"没选进来的"里一行带过。
5. **对话交付**：按下方结构汇报；先结论（更建议看哪几条），再列候选。
6. **收尾**：告诉用户可以说 `深入 GH-02` / `排除 WEB-01` / `需求改成…再搜`。

不要为了"来源多"而凑数。GitHub 上若已有高质量可运行仓库，博客帖只作辅证。

## 链接（硬性）

凡是**外界来源**（GitHub、CSDN、掘金、知乎、文档站、arXiv、Hugging Face、Stack Overflow、博客等），每条候选**必须给出可打开的完整 URL**。

规则：

- 用真实 `https://…` 链接；GitHub 用仓库页（如 `https://github.com/owner/repo`），CSDN/博客用文章页，不要只写站名或仓库短名
- 对话里写成可点击形式，例如：`链接：https://github.com/owner/repo` 或 Markdown `[owner/repo](https://github.com/owner/repo)`
- **没有可靠链接就不要进主列表**；若只能模糊提到，放到"没选进来的"并写明"无可靠链接"
- 禁止编造 URL；搜不到就标 `链接：未知（未核到）` 且不得当作主/辅参考
- `深入 XX-xx` 时复述并沿用同一条链接；若发现更准确的页面（README、论文 PDF），可追加，不要删掉主链接

## 说话与行文

- 私人助手提建议：直接、短句、少套话
- 先给结论，再指到候选 ID
- 遵守文末《输出语气规范》：引号用 `""`；段落空一行
- 字段结构保持稳定，方便用户点名追问

## 搜索质量

- 关键词拆成：任务类型 + 技术栈 + 关键机制
- 对不上需求的再火也不进主列表
- 差不多贴边时：可运行性、维护活跃、文档清晰、许可证友好的排前面
- 同一思路多条结果：留代表性一条，其余一句合并

## 权威程度（每条都要写，不许编）

写能核对的信号 + 一句人话解读；没有就写 `未知`。

| 来源类型 | 优先写的信号 |
|----------|----------------|
| GitHub | Stars、Forks、最近提交/Release、License（有再写） |
| 论文 | 发表/预印本年份、引用或会议名（能核对再写） |
| HF / PwC | downloads、likes、关联论文或基准 |
| 博客/社区 | 阅读/点赞（页面可见再写）、作者是否官方/维护者 |
| 文档站 | 是否官方、版本是否对应当前栈 |

写法示例：

- `权威程度：12.4k stars · 2.1k forks · 近 1 月有提交 — 当主参考更稳`
- `权威程度：ICLR 2024 · 引用未核 — 方法可看，工程成熟度另找仓库`

## 候选 ID

稳定前缀，换链接不要复用旧 ID：

- `GH-01`… — GitHub 仓库（主）
- `DOC-01`… — 官方/规范文档
- `PAPER-01`… — 论文/预印本
- `HF-01`… — Hugging Face 等模型/数据集卡
- `WEB-01`… — 博客、教程、问答帖、其它网页

## 单条候选（对话里每条写短）

**关注等级**（四档，从高到低）：

| 等级 | 含义 | 怎么触发 |
|------|------|----------|
| `最推荐关注` | 重点采纳，优先抄它的思路 | `采纳 XX-xx` |
| `推荐关注` | 值得深入细看 | `深入 XX-xx` |
| `可关注` | 一般候选，作为备选 | 初始默认 |
| `不推荐关注` | 已排除，往后排 | `排除 XX-xx` |

每条候选按关注等级从高到低排序汇报。

单条字段：

1. **链接**（完整 URL，必填）+ **关注等级**
2. **权威程度**
3. **这是啥**：2–4 句
4. **为啥值得你看**：对照需求，别写"很火"
5. **你可以借鉴的部分**：2–5 条可落地点（结构、流程、目录、接口、训练配方等）
6. **不太值得你借鉴的部分**：1–2 句边界

写法示例：

```text
### GH-01 · owner/repo
- 链接：https://github.com/owner/repo
- 关注等级：可关注
- 权威程度：…
```

```text
### WEB-01 · 某篇 CSDN 教程
- 链接：https://blog.csdn.net/…/article/details/…
- 关注等级：可关注
- 权威程度：…
```

不要只写名字不给链接；也不要大段贴源码。License 只提醒，不做法务结论。

## 汇报骨架（对话用）

候选按关注等级从高到低排列：`最推荐关注` → `推荐关注` → `可关注` → `不推荐关注`。

```text
## 需求摘要
（一两句）

## 我的建议
（先看哪 2–3 个 ID，一句话为什么）

## 候选
### GH-01 · …（最推荐关注）
- 链接：https://github.com/…
- 关注等级：最推荐关注
- 权威程度：…
- 你可以借鉴的部分：…
- 不太值得你借鉴的部分：…
…

### WEB-01 · …（推荐关注）
- 链接：https://blog.csdn.net/… 或其它完整 URL
- 关注等级：推荐关注
…

## 没选进来的（可选）
- … — 原因

## 你可接着说
深入 GH-xx / 排除 WEB-xx / 需求改成…再搜
```

## 追问与改稿

- 点名某个 ID：只加深那条，并口述状态变化
- 改需求再搜：用新 ID 或写明替换了谁；已定的关注等级尽量保留

## 刻意不做

- 生成 `PROJECT_IMITATE.md` / `PROJECT_SEARCH.md` 或任何调研落盘 Markdown
- 问"要不要新建 Markdown"
- 只报仓库名/文章标题却不给 URL
- 自动 clone / 把别人代码抄进仓库
- 没触发时主动调研
- 维护 `LEARNING.md` 或做进度预估（除非用户同时开了对应 Skill）

## 启用时的短开场

```text
开调研了。以 GitHub 开源为主，需要时再补文档、论文、博客等。

每条外界来源都会带完整链接。结果只在对话里给，不写调研 md。

之后可以说深入 GH-xx、排除 WEB-xx，或改需求再搜。
```

## 输出语气规范

面向用户的对话按这里来。代码、命令、固定口令模板、表格字段名除外。
（本规范由 `project-shared/output-voice.md` 内联而来，仓库内无外部依赖。）

### 总调

像有见识的普通人在认真聊一件具体的事。短句优先。一次说清一件事。少排比、少总结腔。

本 Skill 的角色：私人助手给调研建议；先结论，再指到 GH/WEB/PAPER 等编号；不落盘调研文件。

### 标点（面向用户时）

- 引用口令、短词、强调时用中文双引号 `""`，例如："懂了"、"先做别讲"
- **不要用**直角引号
- 文件名、代码、口令本身优先用行内代码，例如 `` `开调研` ``

### 行距（面向用户时）

- 段落与段落之间空一行
- 讲解块之间空一行
- 不要整屏挤成一块；也不要连续空三行以上

### 少用或不用（一出现就改）

- 空话连接：此外、综上所述、总的来说、值得注意的是、不难发现、众所周知、不可否认
- 踩雷词：说白了、本质上、这意味着、换句话说、让我们来看看、在当今…的时代
- 产品腔：赋能、闭环、抓手、对齐认知、高度契合、落地闭环
- 句式："不是 A，而是 B" → 直接写你要说的那句
- 三段式硬开场："首先…其次…最后…" → 打散
- 假例子："比如有一次…" → 优先本项目、用户刚提过的、或标"例子待补"
- 空泛工具名 → 写具体名字（GitHub、`gh search`、`curl` 等）

### 鼓励怎么写

- 先给能用的结论或状态，再补依据
- 长短句交错；重要的一句可以单独成行
- 承认不确定
- 用具体数字、路径、ID、步骤名
- 收尾用下一步动作，不要升华

### 自检（写完扫一眼）

1. 有没有连续三句同一句式排比？
2. 有没有"综上所述 / 本质上 / 说白了"？
3. 例子是具体的还是编的？
4. 结尾是下一步，还是空感慨？
5. 段落之间是否空了一行？
