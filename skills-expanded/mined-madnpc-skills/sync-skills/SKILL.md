---
name: sync-skills
description: "适用于本仓库（npc404-skills）同步上游技能：运行 scripts/sync-skills.mjs 检测上游变化，逐个研判 diff 是否为有效更新（实质内容变化，还是排版、笔误等噪音），给出本地化建议，处理完成后推进版本记录。Use in the npc404-skills repo whenever the user wants to check or sync upstream skill sources, review upstream diffs, decide whether an upstream change is worth localizing, or advance skill versions with accept — even if they just say \"看看上游有没有更新\". 中文关键词：同步技能、技能同步、上游更新、检查上游、上游 diff、有效更新、本地化更新、推进版本、sync skills、accept。"
---

# Sync Skills（上游技能同步）

把 `scripts/sync-skills.mjs` 的检测结果变成一次有判断的同步：检测上游变化 → 研判每个 diff 是否为有效更新 → 报告并等用户确认 → 本地化或直接推进版本。

脚本本身只做版本比对和 diff 暂存，不判断内容价值；这个技能的核心工作是替用户读 diff、下判断。

## 适用范围

只在 npc404-skills 仓库内使用：先确认仓库根存在 `scripts/sync-skills.mjs`，找不到就说明不在本仓库，告知用户后停止。需要 Node 18+ 和网络访问 GitHub。

写入范围只限仓库内：本地化只改 `skills/<skill>/`（外加 `scripts/sync.config.json`、README 等仓库文件）。`~/.claude/skills/`、`~/.cc-switch/skills/` 等仓库外的安装/分发副本一律不写不删——那些由用户自行更新。同步完成后至多提示一句"分发副本可能滞后"，何时更新由用户决定。

用户只想看当前状态（不查上游）时，运行 `node scripts/sync-skills.mjs status` 即可，不要发起 check。

## 流程

### 1. 检测上游

```bash
node scripts/sync-skills.mjs check          # 全部技能
node scripts/sync-skills.mjs check <skill>  # 只查一个
```

逐技能看状态行并分流：

- `✓ 已是最新` —— 无事发生。
- `✗ 查询 commit 失败 403 …限流` —— 脚本已自动尝试 `GITHUB_TOKEN` 和 `gh auth token`，仍限流说明本机没有可用凭据（gh 未登录或未安装）。按报错里给出的重置时间告知用户稍后再试，或请用户 `gh auth login` / 提供 token。有 ✗ 行时该技能上游状态未知，不要当成"已是最新"。
- `∅ 无版本记录` —— 新增技能还没建基线。提示运行 `node scripts/sync-skills.mjs init <skill>`（init 把当前上游 HEAD 记为已同步基线，不产生 diff，之后的变化才会被 check 捕捉）。
- `● <old> → <new>` —— 上游有变化，材料已暂存：`scripts/.skill-sync/diffs/<skill>.diff` 是新旧版本的逐文件 diff，`scripts/.skill-sync/incoming/<skill>/` 是上游最新原文。进入下一步。

### 2. 研判是否有效更新（核心）

先处理一个常见边界：check 报了变化但 diff 为空（`+0 -0`）。这说明上游目录里有新 commit，但没碰到 `sync.config.json` 跟踪的文件（比如上游加了别的文件、或改了未跟踪的文档）。归为噪音，直接建议 accept；若怀疑上游新增了值得跟踪的文件，可去上游仓库看该目录的提交记录再决定是否扩充 `files`。

对每个有非空 diff 的技能读它的 diff。判断的问题是「这次上游变更对**本地版本**有没有价值」，不是「上游改了多少行」：本地文件是上游的本地化改编（中文触发词、输出语言约定、可能的删改），上游改动的段落在本地可能早已重写或删除，所以拿不准某个 hunk 是否还适用时，要对照本地 `skills/<skill>/` 的对应文件确认。

**有效更新**（值得本地化）：

- 指令、流程步骤、判断标准、边界条件的实质变化
- 新增或删除章节、文件
- 修复了本地版本同样存在的错误
- description 触发语义的变化（影响技能何时被调用）

**噪音**（本地无需跟进）：

- 排版、空白、Markdown 格式调整
- 笔误修正、措辞润色但语义不变
- 链接、徽章、上游仓库自身目录结构等与技能内容无关的改动
- 改动落在本地已刻意重写或删除的段落上（须对照本地文件确认后才能下此结论）

整个 diff 混合两类时按「有效更新」处理，本地化时只取有价值的部分。纯粹拿不准时也倾向判为有效更新，把取舍留给用户。

### 3. 报告并等确认

给用户一份简短报告，每个有变化的技能一条：分类（有效更新/噪音）、上游改了什么（一两句人话概括，不贴 diff）、建议动作（本地化 / 直接 accept）。

报告后停下来等用户确认再动手：本地化会改写 `skills/` 下的文件，accept 会推进 `scripts/state.json` 的版本记录，都不该默默发生。

### 4. 处理

**有效更新 → 本地化**：对照 diff 把上游的增量变化改写进 `skills/<skill>/` 对应文件。遵守本地约定：

- 保留本地已有的改编——中英双语 description、中文关键词、「输出语言」章节等，不要被上游原文覆盖回去
- 只融入上游的变化部分，不整体替换文件
- 上游新增了值得引入的文件时，先把文件名加进 `scripts/sync.config.json` 该技能的 `files` 数组，再落地本地化版本
- 若 description 或适用时机变了，同步更新 README.md 的技能表格

**噪音 → 不改本地文件**，直接进入 accept。

两种情况处理完都要推进版本，否则下次 check 会重复报告：

```bash
node scripts/sync-skills.mjs accept <skill>   # 逐个；或全部处理完后 accept --all
```

### 5. 收尾

提醒用户提交 `scripts/state.json`（唯一必须提交的产物），以及本次改动的 `skills/` 文件、README。`scripts/.skill-sync/` 整个目录是 gitignore 的临时区，不需要清理也不要提交。
