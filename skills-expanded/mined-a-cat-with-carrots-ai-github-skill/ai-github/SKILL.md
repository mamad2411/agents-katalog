---
name: ai-github
description: GitHub repo 展示层管家 — 让 repo 在 GitHub 页面上"看起来像个能用的项目"。三件套：① README 重写（mirror 参考 repo 的结构 + 填充本 repo 内容，含 badges / 它是什么 / 为什么做它对比表 / 安装两法 / 用法 / 流程 / 文件结构 / 自定义 / 版本史 / 贡献 / 致谢 / License）② GitHub 描述润色（30-100 字一句话，卖点 + 输出 + 价值，替代「X Claude Code skill」式裸分类描述）③ Topic 标签加 10-15 个，按 6 类分（生态/受众/用途/数据源/技术/语言）。**附加两步**（用户要求时启用）：⓪ 建新 repo（git init + gh repo create + push，当目录还没 git 化或 GitHub 上还没 repo 时）④ 补 LICENSE（README 提到 MIT 但 repo 缺 LICENSE 文件时自动补全）。**与已有 git skill 区别**：那些是 git 操作层（commit/branch/PR/Actions），本 skill 是 GitHub 页面展示层（README + description + topics + 上线视觉）。务必触发：用户说"完善 repo 展示"、"润色 README"、"把 README 写成 X 风格"、"加 topic 标签"、"加 GitHub 标签"、"改 repo 描述"、"polish 我的 repo"、"rebrand 这个 repo"、"让我的 GitHub 项目看起来像个项目"、"GitHub 页面太空"、"美化 GitHub repo"、"把这个 skill 推到 GitHub"、"推到我们 GitHub 上"，或调用 /ai-github。
---

# AI GitHub — Repo 展示层管家

让你的 GitHub repo 页面**像个能用的产品**，不像随手 push 的脚本。

## 定位

**做什么**：repo 在 github.com 上的**展示层**——README + 描述 + topics + 视觉。
**不做什么**：git 操作（commit / branch / PR / merge）、Actions / Pages 部署。那些用 `claude-skill-git` / `claude-skill-github-best-practices` / `claude-skill-github-pages-deployer`。

**核心赌注**：好 README + 卖点描述 + 准 topics 决定 repo 能否被搜到 + 第一屏是否看得下去。SKILL.md 写得再好，repo 主页空荡，新用户 3 秒就关。

## 触发

下列任意触发：

- "完善 / 润色 / 美化 [repo] 展示 / README"
- "把 README 改成 X 风格"（X 是另一个 repo / skill）
- "加 / 完善 GitHub 标签 / topic"
- "改 / 写个 GitHub 描述"
- "polish 我的 GitHub" / "rebrand 这个 repo"
- "GitHub 页面太空" / "看起来不像个项目"
- `/ai-github`

**不触发**的反例：
- "帮我写个 commit message" → 用 `Claude-Skill-Git-Commit-Message`
- "创建 PR" → 用内置 `gh pr create` 或 `claude-skill-github-best-practices`
- "部署 GitHub Pages" → 用 `claude-skill-github-pages-deployer`

## 三件套（+ 两个可选附加步）

```
┌─ ⓪ Bootstrap（可选，cwd 不是 git repo 或 GitHub 上没 repo 时启用）─┐
│  git init + 首次 commit + gh repo create --source=. --push        │
│  默认 public，repo 名取 cwd basename，描述 / topics 留给 ②③ 来填   │
└──────────────────────────────────────────────────────────────────┘
              ↓
┌─ ① README 重写 ──────────────────┐
│  pull 参考 repo README + 镜像结构  │
│  填本 repo 内容（读 SKILL.md/code）│
│  badges + 它是什么 + 为什么 + ...  │
└──────────────────────────────────┘
              +
┌─ ② Description 润色 ─────────────┐
│  bare 分类 → 卖点一句话           │
│  公式：[受众] + [一句触发] → [输出]│
│        + [价值/卖点]              │
└──────────────────────────────────┘
              +
┌─ ③ Topics 加 10-15 个 ───────────┐
│  6 类分布：                       │
│  生态 / 受众 / 用途 / 源 / 技术 / 语言│
└──────────────────────────────────┘
              +
┌─ ④ LICENSE 补全（可选，README 提了 License 但 repo 缺文件时启用）─┐
│  默认 MIT，年份 = 当年，holder = git config user.name             │
│  其它 license（Apache-2.0 / GPL / BSD）需用户明示                  │
└──────────────────────────────────────────────────────────────────┘
              ↓
       commit + push + gh repo edit
```

## 工作流（6 步 + 2 可选附加步）

### Step 0：Bootstrap — 建新 repo（可选）

**何时触发**：

- cwd 不在 git repo（`git rev-parse --is-inside-work-tree` 报错）→ 整套从 0 开始
- cwd 是 git repo 但无 `origin` remote → 只需建 GitHub repo + push
- cwd 是 git repo 且有 origin，但 `gh repo view <owner>/<name>` 404 → remote URL 指向不存在的 repo，需建

**步骤**：

```bash
# 1. 检测状态
git rev-parse --is-inside-work-tree 2>&1      # not a git repository → 需 init
git remote get-url origin 2>&1                # no such remote → 需建 GitHub repo
gh repo view <owner>/<name> 2>&1              # GraphQL: Could not resolve → repo 不存在

# 2. git init（仅当不是 git repo）
git init -b main
git add -A
git commit -m "init: <repo-name> v1$([newline][newline])Co-Authored-By: ..."

# 3. 建 GitHub repo + 推
#   --source=. 把当前目录作为源；--push 自动 push；--description 先占位（②会改）
gh repo create <repo-name> --public --source=. --remote=origin --push \
  --description "<占位描述，Step 4 会覆盖>"
```

**默认值**：

- `repo-name` = cwd basename（如 `socratic-dialogue`）。用户指定优先。
- `--public`：默认公开，私有需用户明示。
- `branch` = `main`。
- `description` 占位：用 SKILL.md 第一行 description 或 cwd 名做临时占位，Step 4 会覆盖。

**触发本步的用户原话**：

- "把这个推到 GitHub"
- "推到我们的 GitHub 上"
- "建个 repo + 三件套全做"
- "新 skill 上 GitHub"

**做完进 Step 1**（此时 repo 已存在 + 已 push，后续流程正常跑）。

### Step 1：确认目标 repo + 参考风格 repo

**目标 repo**：
- 默认 = `gh repo view --json owner,name`（cwd 内）
- 用户明确指定 → 用指定 repo
- cwd 不在 git repo → 询问

**参考 repo**（README 风格模板）：
- 用户指定 → 用指定（如"按 ai-short-drama-skill 写"）
- 没指定 → 列用户已有的同 owner repo 选最像的；或推默认风格（见 `references/readme-style-guide.md`）

### Step 2：抓两边内容

**目标 repo**：
- `Read` 本地 SKILL.md（或主代码文件）—— 提取功能列表 / 工作流 / 触发词 / 限制
- `Read` 现有 README（如有）—— 看哪些段缺
- `gh repo view <owner>/<name> --json description,repositoryTopics` —— 看现状
- `Glob examples/` —— 有 example 就 surface

**参考 repo**：
- `gh api repos/<owner>/<name>/contents/README.md --jq .content | base64 -d` —— 拿原文
- 拆解结构：每段标题、有无 badges、对比表、ASCII 图、文件结构示例、版本史

### Step 3：起草新 README

**镜像结构 + 填本 repo 内容**。Section 套路（按 ai-short-drama / pm-daily-brief 实证）：

1. **标题 + tagline**（一行，含价值主张）
2. **引用句**（quote 块，"一句『X 触发』 → Y 输出"）
3. **Badges**（Skill / License / PRs Welcome）
4. **它是什么**：具象触发示例 → bullet 列输出 → punchline（"不是 X，是 Y"）
5. **为什么做它**：对比表（市面通病 vs 本 skill 改进）—— **整篇最有说服力的段**
6. **安装**：两法（Windows PowerShell + macOS/Linux）
7. **用法**：触发词列表 + ASCII 流程图
8. **核心流程速览**：每步 3-5 行
9. **输出模板**（如适用）
10. **文件结构**：tree 块
11. **自定义**：编号 5 项（路径 / 数据源 / 语言 / 二进制 / 加源）
12. **为什么是 skill 不是脚本**（如适用）
13. **已知限制**：bullet 4-6 条
14. **版本历史**：v1 → v2 → v3，每版列关键改进
15. **贡献**：列重点方向 4-5 条
16. **致谢**：上游灵感 / 工具链
17. **License**：MIT 链接

**写作铁律**：
- 中文为主（除非 repo 用英文社区），技术术语保留英文
- 信息密度高，禁止"令人激动""革命性"形容词
- 对比表 ≥ 8 行才有说服力，少了砍掉
- 触发示例必须**具象**，不写"一句话需求"
- 版本史每版列**关键改进**而非"修了 bug"

详见 `references/readme-style-guide.md`。

### Step 4：起草 GitHub 描述

**裸分类描述**（bad）：
> AI产品经理每日情报简报 Claude Code skill

**卖点描述**（good）：
> AI 产品经理每日情报简报 Claude Skill — 一句『今天有啥新的』 → 三源融合（PH/GH/HN）+ 用户画像加权 + TL;DR 60 秒摘要 + Top 3-5 深读 + 全列表 [跟进/关注/噪音] triage，中文 Markdown/PDF 双输出

**公式**：
```
[名称] [类别] — [触发短语] → [核心输出 + 关键卖点 1-3 个] + [产物形态]
```

详见 `references/description-formula.md`。**长度上限 350 字符**（GitHub 限制），中文超 100 字基本到顶。

### Step 5：起草 Topics（10-15 个）

**6 类分布**（每类 1-3 个）：

| 类 | 例 | 必有？ |
|---|---|---|
| **生态** | `claude-skill` `claude-code` `anthropic` | 必 |
| **受众** | `ai-product-manager` `developer` `designer` | 推 |
| **用途/动作** | `daily-brief` `code-review` `repo-management` | 必 |
| **数据源/集成** | `producthunt` `github-api` `webfetch` | 视情况 |
| **技术** | `prompt-engineering` `llm` `markdown-to-pdf` | 推 |
| **语言/区域** | `chinese` `english` | 视情况 |

**topic 命名规范**：全小写 + 连字符。GitHub 自动归一。

详见 `references/topic-taxonomy.md`。

### Step 6：应用 + commit + push

```bash
# 1. 写 README
# (Edit / Write)

# 2. commit
git add README.md
git commit -m "$(cat <<'EOF'
docs: rewrite README in <reference-repo> style

<2-3 sentence summary>

Co-Authored-By: ...
EOF
)"

# 3. push
git push origin HEAD

# 4. 改描述
gh repo edit <owner>/<name> --description "<新描述>"

# 5. 加 topics
gh repo edit <owner>/<name> \
  --add-topic <topic1> \
  --add-topic <topic2> \
  ...
```

**验证**：`gh repo view <owner>/<name> --json description,repositoryTopics`

### Step 7：补 LICENSE（可选）

**何时触发**：

- README 提到 License（"MIT" / "Apache-2.0" / "GPL-3.0" 等）**但** repo 根目录无 `LICENSE` / `LICENSE.md` / `LICENSE.txt` 文件
- 或用户明说"加 LICENSE"

**步骤**：

```bash
# 1. 检测
ls LICENSE LICENSE.md LICENSE.txt 2>/dev/null   # 都不存在 → 需补

# 2. 取身份信息
year=$(date +%Y)
holder=$(git config user.name)                  # 也可问用户用 GitHub username

# 3. 选 license（默认 MIT；其他需用户明示）
#    MIT 全文模板见下方"license 模板"段
#    Apache-2.0 / GPL-3.0 走 `gh api /licenses/<key> --jq .body` 取标准文本

# 4. 写文件 + commit + push
git add LICENSE
git commit -m "chore: add <SPDX-id> LICENSE"
git push origin HEAD
```

**MIT 模板**（复制即用，替换 `{year}` `{holder}`）：

```
MIT License

Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**铁律**：

- README 写 MIT，repo 必须有 LICENSE 文件 —— 否则 GitHub 侧栏不显示 license、社区工具(deps.dev / Snyk)误判为"无许可"=保留所有权利。
- 不要在用户没明说的情况下硬塞非 MIT。MIT 是 skill / 个人项目的默认，其他要问。
- 不要把 LICENSE 写进 Step 6 同一 commit —— 单独 commit `chore: add LICENSE` 更干净。

**汇报模板**：
```
✅ <repo> 展示层升级完成

📝 README: N → M 行（+M-N），结构镜像 <reference>
📋 Description: 「<前>」→「<后>」
🏷️ Topics: K → K+P（新增 P 个，6 类分布：生态 X / 受众 Y / 用途 Z / 源 W / 技术 V / 语言 U）

🔗 https://github.com/<owner>/<name>
```

## 失败模式与避免

- **照搬参考 repo 内容**：mirror **结构**，不抄文字。每段都用本 repo 实际功能填
- **对比表凑行数**：行数不够（< 8）就砍表，列 bullet 替代。烂对比表比没对比表更损
- **Badges 加成 LinkedIn 风**：基础 3 个够（Skill / License / PRs）。CI / coverage / npm 之类按真实情况加
- **Topics 撒盐**：>15 个 GitHub 也只展示前 ~12。挑准比加多重要
- **描述塞所有功能**：1 句话最多 3 个卖点，多了变流水账
- **触发示例写"一句话需求"**：必须具象，写"今天有啥新的" 不写"用户输入"
- **版本史写"修了 bug"**：每版列**关键改进**——加了什么字段、解决了什么 pain
- **README 用英文，repo 中文受众**（或反向）：跟实际用户语言对齐
- **改完不 push**：本地 README 改了不 push，GitHub 页面没变化——白干
- **gh repo edit 后不验证**：description 偶有截断，topics 偶有归一改名，跑一次 `gh repo view` 确认
- **覆盖参考 repo 的卖点**：参考是结构模板，不是卖点模板。本 repo 的卖点是本 repo 的功能，不是参考的

## 与现有 skill 协作

| 任务 | 用哪个 |
|---|---|
| 写 commit message | `Claude-Skill-Git-Commit-Message` |
| 写 PR / 处理 PR | `claude-skill-github-best-practices` 或内置 `gh pr create` |
| PR 内联评论 | `claude-skill-github-pr-inline-comments` |
| 部署 Pages | `claude-skill-github-pages-deployer` |
| Actions workflow | `claude-skill-github-actions` |
| 重写 commit author | `claude-skill-git-author-update` |
| 原子 commit / staging | `faceleg/claude-skill-git` |
| **README + 描述 + topics 三件套** | **`ai-github`（本 skill）** |

## 启动指令

**先跑 3 个检测**（决定要不要进 Step 0 / Step 7）：

```bash
git rev-parse --is-inside-work-tree 2>&1      # 是 git repo 吗？
gh repo view --json owner,name 2>&1            # GitHub 上有 repo 吗？
ls LICENSE LICENSE.md LICENSE.txt 2>/dev/null  # 有 LICENSE 吗？
```

**第一句话回应模板**：

```
收到。本 skill 三件套：① README 重写 ② Description 润色 ③ Topics 加标。
附加两步：⓪ Bootstrap 建新 repo / ④ 补 LICENSE。

检测结果：
- cwd git repo: <yes / no>
- GitHub repo: <存在 / 不存在>
- LICENSE 文件: <有 / 无>

确认 3 项：

1. 目标 repo：<cwd 推断 / 需建> 还是其他？
2. 参考风格：用哪个 repo 的 README 当结构模板？（默认：你 owner 下最 polished 的那个）
3. 范围：三件套全做？要不要带上 ⓪ Bootstrap / ④ LICENSE？

回答后启动流程（按需 0 → 1 → ... → 6 → 7）。
```

## 边界

- **建新 repo 仅在用户明说时做**——默认假设 repo 已存在；用户说"推到 GitHub" / "新 skill 上 GitHub"才走 Step 0
- **不改代码**——只改 README + GitHub metadata + LICENSE
- **不替你写 SKILL.md**——本 skill 是 README 的事，SKILL.md 用 `skill-creator`
- **不发 release / tag**——那是 `version-bump` / `ship` 的事
- **LICENSE 默认 MIT，其他需明示**——MIT 是 skill / 个人项目默认；Apache-2.0 / GPL / BSD / 商业 license 必须用户主动选，避免误选
