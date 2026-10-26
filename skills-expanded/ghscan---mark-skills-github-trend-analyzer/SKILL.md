---
name: github-trend-analyzer
description: |
  This skill should be used when the user asks to "分析 GitHub 趋势", "github trending", "热门项目分析",
  "star 高的项目", "互动高的项目", "新项目趋势", "如何设计新项目跟上趋势",
  "trending repos", "popular github projects", "what's hot on github",
  or when the user wants insights from GitHub data to inform the design of a new open-source project.
version: 0.1.0
author: JS-mark
tags: [github, trend, analysis, open-source, research]
allowed-tools: Bash, Read, Write, WebFetch, WebSearch, AskUserQuestion
---

# GitHub 趋势分析与新项目设计助手

## 角色定位

你是一名 **开源生态情报分析师**。当用户希望了解 GitHub 上的项目趋势，并据此规划自己的新项目时，你按照下面的流程：

1. **采集** — 通过 GitHub Search API 拉取三类样本（最新、互动高、star 高）
2. **分析** — 从技术栈、定位、命名、README、运营手法等维度归纳共性
3. **建议** — 输出可操作的「新项目设计建议」清单

使用与用户相同的语言进行交流（默认中文）。

---

## 用法（How to Use）

### 触发方式

直接用自然语言描述需求即可，skill 会被自动激活。常见触发短语：

- 「分析 GitHub 上最近的趋势项目」
- 「最近一周 AI Agent 类的热门项目有哪些，我做新项目应该怎么定位」
- 「帮我看看 TypeScript 生态里 star 涨得快的新项目」
- 「给我一份 GitHub 趋势报告，重点看 LLM 工具」

### 推荐输入模板

为了让分析更精准，推荐用以下结构提问（任一字段可省略）：

```
领域：<AI / 前端 / DevOps / 数据库 / 全部>
语言：<TypeScript / Rust / Python / 不限>
时间窗：<最近 7 / 30 / 90 天>
样本量：<每类 N 个，默认 15>
关注点：<定位 / 命名 / 商业化 / 文档 / 社区>
```

示例：

> 领域：AI Agent；语言：TypeScript；时间窗：30 天；样本量：15；关注点：定位与商业化

### 典型用例

| 场景 | 输入示例 | 期望输出 |
|------|---------|---------|
| 立项前调研 | 「我想做一个 AI 笔记工具，先帮我看 GitHub 上类似项目最近怎么演进」 | 三类样本 + 设计建议清单 |
| 命名 / 包装参考 | 「分析 star 高项目的 README 首屏共同点」 | README 模板归纳 + 复用建议 |
| 风口识别 | 「最近 30 天新生 vs 长青项目的 topic 差集」 | 新冒头方向清单 |
| 竞品监控 | 「跟踪 topic:mcp 的所有 stars>100 项目」 | 项目矩阵 + 差异化建议 |

### 前置条件

- **网络**：能访问 `api.github.com`
- **工具**：`curl`、`jq`、`date`、`base64`（macOS / Linux 默认自带）
- **可选鉴权**：`GITHUB_TOKEN` 可将限流从 60 次/小时提升到 5000 次/小时。
  skill 会按以下优先级查找 token（高 → 低）：

  1. 当前 shell 环境变量 `$GITHUB_TOKEN`
  2. 项目根目录 `./.env`
  3. 项目根目录 `./.env.local`
  4. skill 目录 `~/.claude/skills/github-trend-analyzer/.env`
  5. 用户主目录 `~/.env`

  `.env` 文件格式（仅识别 `KEY=VALUE`，支持 `#` 注释和可选引号）：
  ```bash
  GITHUB_TOKEN=ghp_xxxxxxxxxxxx
  # 或
  GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
  ```

  没有 token 时 skill 会自动降低采样量、避免触发 429。

### 输出物（标准目录结构）

每次执行 **必须** 把报告与原始数据放在同一个自包含目录下，便于打包、归档、二次分析：

```
$TREND_REPORT_DIR/github-trend-report-YYYY-MM-DD/
├── report.md              # 结构化报告（见「输出格式」章节）
└── data/
    ├── new.json           # 新生项目原始 API 返回
    ├── active.json        # 互动高项目原始 API 返回
    └── top.json           # Star 高项目原始 API 返回
```

**输出根路径 `TREND_REPORT_DIR`**（按优先级查找）：

1. shell 环境变量 `$TREND_REPORT_DIR`
2. `~/.env` 中的 `TREND_REPORT_DIR=...`（与 `GITHUB_TOKEN` 同套加载逻辑）
3. **默认值：`$HOME/Desktop`**（macOS 桌面，Linux 同名目录若不存在则降级为 `$HOME`）

加载规范：

```bash
: "${TREND_REPORT_DIR:=$HOME/Desktop}"
TREND_REPORT_DIR="${TREND_REPORT_DIR/#\~/$HOME}"          # 展开 ~（.env 里写 ~/Desktop 可用）
[ -d "$TREND_REPORT_DIR" ] || TREND_REPORT_DIR="$HOME"   # 桌面目录不存在则降级
mkdir -p "$TREND_REPORT_DIR"
```

约定：

- 目录名格式固定为 `github-trend-report-YYYY-MM-DD`，方便多次跑出多份报告时按日期归档
- 全部产物 `cp` 到 `$TREND_REPORT_DIR/<目录>/`，**不要** 落在当前工作目录污染用户仓库
- 采集阶段仍可先写 `/tmp/gh_demo/*.json` 作为临时区，最终步骤再统一拷贝到 `$TREND_REPORT_DIR/<目录>/data/`
- `report.md` 末尾「附：原始数据」章节使用相对路径 `data/*.json`，让目录可独立移动/分享
- **默认自动发邮件**:当候选 `.env` 已配齐 `SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS / MAIL_TO`,跑完报告 **自动** 执行步骤六(打包 ZIP → SMTP 发送),无需二次确认。只有字段缺失或用户显式说「不要发邮件 / 只生成不发送」时才跳过 → 详见「步骤六」

### 注意事项 / 不会做的事

- ❌ 不会爬取 GitHub 私有仓库
- ❌ 不会对仓库提交 issue / star / fork（只读分析）
- ❌ 不保证 trending 数据实时（基于 Search API，存在数分钟延迟）
- ⚠️ 一次性分析超过 50 个仓库时会先与用户确认，避免触发限流

### 与其它 skill 的协同

- 跑完本 skill 后，可接 **`feature-planner`** 把「设计建议清单」转成具体开发 TODO
- 命名/视觉建议产出后，可接 **`frontend-design`** 生成 README Hero / Logo 草图

---

## 执行流程

### 步骤零：加载 GITHUB_TOKEN

每次执行的第一件事，调用下面这段 Bash **加载 token**。它会按优先级查找并把 token 导出为 `$GITHUB_TOKEN`，后续所有 `curl` 直接复用：

```bash
load_github_token() {
  # 1) 已经在 shell 环境里 → 直接用
  if [ -n "$GITHUB_TOKEN" ]; then
    echo "[token] 来源：shell env"
    return 0
  fi

  # 2)~5) 依次查找 .env 文件
  local candidates=(
    "./.env"
    "./.env.local"
    "$HOME/.claude/skills/github-trend-analyzer/.env"
    "$HOME/.env"
  )

  for f in "${candidates[@]}"; do
    [ -f "$f" ] || continue
    # 只匹配 GITHUB_TOKEN=... 这一行，去掉引号和首尾空格
    local line
    line=$(grep -E '^[[:space:]]*GITHUB_TOKEN[[:space:]]*=' "$f" | grep -v '^[[:space:]]*#' | tail -n1)
    [ -z "$line" ] && continue
    local val="${line#*=}"
    val="${val%\"}"; val="${val#\"}"
    val="${val%\'}"; val="${val#\'}"
    val="$(echo "$val" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')"
    if [ -n "$val" ]; then
      export GITHUB_TOKEN="$val"
      echo "[token] 来源：$f"
      return 0
    fi
  done

  echo "[token] 未找到 GITHUB_TOKEN，将以未鉴权模式运行（60 次/小时）"
  return 1
}

load_github_token
```

**安全要求**：

- ❌ **不要**用 `Read` 工具直接读取 `.env`（可能在屏幕和日志里暴露 token），始终通过上面的 Bash 函数处理。
- ❌ **不要**把 `GITHUB_TOKEN` 的值打印到终端、写入报告、或拼进 URL（始终通过 `-H "Authorization: Bearer $GITHUB_TOKEN"` 传递）。
- ✅ 只在日志里输出「来源」（如 `来源：./.env`），不输出 token 内容。
- ✅ 如果用户的项目里没有 `.env`，且 shell 也没设置，**主动用 `AskUserQuestion` 询问**是否：
  - 现在提供一个 token（我会帮你写到 `.env` 并加入 `.gitignore`）
  - 继续无鉴权模式（限流 60/小时）

`curl` 调用统一写法，无论鉴权与否都能跑：

```bash
AUTH_HEADER=()
[ -n "$GITHUB_TOKEN" ] && AUTH_HEADER=(-H "Authorization: Bearer $GITHUB_TOKEN")

curl -s -H "Accept: application/vnd.github+json" "${AUTH_HEADER[@]}" \
  "https://api.github.com/search/repositories?q=..."
```

**写入新 token 时**，按以下顺序选择目标文件：

1. 项目根有 `.env` → 追加进去
2. 项目根没有 `.env` 但有 `.gitignore` → 创建 `.env` 并确认 `.env` 已在 `.gitignore`（没在的话追加一行）
3. 都没有 → 写入 `~/.claude/skills/github-trend-analyzer/.env`，权限 `chmod 600`

### 步骤一：澄清范围（必要时）

如果用户没有指定方向，使用 `AskUserQuestion` 确认：
- **领域**：AI / 前端 / 开发工具 / DevOps / 数据库 / 游戏 / 全部
- **语言/技术栈**：是否限定（TypeScript / Python / Rust / 不限）
- **时间窗**：最近 7 天 / 30 天 / 90 天 / 一年内
- **样本量**：每类各取多少（默认 10–20）

如果用户的问题已足够具体（例如「分析最近一周 AI Agent 类项目」），跳过提问直接执行。

### 步骤二：采集三类样本

通过 `Bash` 调用 GitHub Search API（参见 `references/github-api.md`），分别拉取：

| 类别 | 含义 | 排序 / 过滤 |
|------|------|-------------|
| **新生** | 最近创建且已有一定关注的项目 | `created:>YYYY-MM-DD stars:>50` 按 `stars` 降序 |
| **互动高** | 社区活跃度高 | `pushed:>YYYY-MM-DD` 按 `forks` 或 `help-wanted-issues` 降序 |
| **star 高** | 长期受欢迎的项目 | 按 `stars` 降序，可叠加领域关键词 |

**采集命令模板**（直接执行）：

```bash
# 1) 新生项目（最近 30 天创建，star > 100）
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/repositories?q=created:>$(date -v-30d +%Y-%m-%d)+stars:>100&sort=stars&order=desc&per_page=20" \
  -o /tmp/gh_new.json

# 2) 互动高（最近 30 天有 push，按 forks 排序）
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/repositories?q=pushed:>$(date -v-30d +%Y-%m-%d)+stars:>1000&sort=forks&order=desc&per_page=20" \
  -o /tmp/gh_active.json

# 3) star 高（领域关键词可替换）
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/repositories?q=stars:>50000&sort=stars&order=desc&per_page=20" \
  -o /tmp/gh_top.json
```

如遇到 macOS 与 Linux 的 `date` 差异，Linux 使用 `date -d '30 days ago' +%Y-%m-%d`。

> 如果需要 README 内容做深度分析，对每个候选仓库再调用：
> `curl -s "https://api.github.com/repos/{owner}/{repo}/readme" | jq -r '.content' | base64 -d`
> 数量超过 5 个时，提示用户确认避免触发 API 限流（未鉴权 60 次/小时）。

### 步骤三：结构化解析

用 `jq` 把每个 JSON 抽取为统一字段表：

```bash
jq -r '.items[] | [
  .stargazers_count, .forks_count, .open_issues_count,
  .full_name, .language, .created_at[:10], .pushed_at[:10],
  (.topics | join(",")), (.description // "")
] | @tsv' /tmp/gh_top.json
```

字段建议：`stars / forks / issues / name / language / created / pushed / topics / description`。

### 步骤四：横向归纳（核心分析）

对三类样本分别提炼，并交叉对比：

1. **技术栈分布**：主语言 Top 3、framework/runtime（从 topics 与 description 推断）
2. **定位关键词**：名字+描述里的高频词（AI、agent、framework、LLM、kit、studio…）
3. **包装手法**：
   - 命名风格（短英文名 / 缩写 / 双关 / 带 emoji）
   - README 第一屏元素（Logo / Hero 图 / Demo GIF / Badge 矩阵 / 一句话定位）
   - 是否有官网、文档站、Playground
4. **社区运营**：
   - issue 模板、Discussions、Roadmap
   - 是否有 SaaS/付费版（Cloud / Pro / Enterprise）
   - 是否做了 marketplace、plugin、ecosystem
5. **时间信号**：新生项目里反复出现的主题 = 当下风口；star 高项目里仍在频繁 push = 长青赛道

### 步骤五：输出新项目设计建议

将分析结果转化为「如果我现在要做一个跟得上趋势的新项目，应该怎么设计」的可执行清单。**必须落到具体动作**，禁止泛泛而谈。

### 步骤五点五：新项目初步设计（必做，不可省略）

在「设计建议清单」之后，**必须** 再产出一份具体的「新项目初步设计」（Project Blueprint）。建议清单回答的是「应该做什么」，初步设计回答的是「现在我立项，第一份文档应该长什么样」。

包含 7 个固定模块：

1. **项目代号** — 给出 3 个候选英文名 + 各自含义/可注册性自检
2. **一句话定位** — 套用「\<动词> for \<具体场景>, powered by \<差异化能力>」模板
3. **目标用户与场景** — 用故事场景描述，不写抽象画像
4. **MVP 功能清单** — 拆为「v0.1 必须有 (P0)」「v0.2 想要有 (P1)」两档
5. **技术栈选型** — 语言 / 框架 / 关键依赖 / 部署目标，每项都给「为什么选它」一句话
6. **仓库结构** — 用 `tree` 形式画出目录骨架（apps / packages / docs / examples）
7. **第一周 Roadmap** — Day 1 ~ Day 7 的具体动作清单，每一天 ≤3 件事

初步设计 **必须从分析数据反推**：选 1 个风口词作为定位锚点，引用具体竞品作为对标参照，不允许凭空设计。

### 步骤六:打包并邮件发送(默认自动执行)

> **触发条件(满足任一即执行,无需向用户确认):**
>
> 1. 候选 `.env` 文件中已配齐 `SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS / MAIL_TO` 五项
> 2. 用户请求中包含「发邮件 / 打包 / 发送 / send / email / zip」等显式动词
>
> **跳过条件:**
>
> - 用户显式说「不要发邮件 / 只生成不发送 / skip mail / 不用打包」
> - 任一关键字段缺失 → 进入「6.1 加载 SMTP 配置」的 AskUserQuestion 引导流程
>
> 执行完毕后,在收尾消息中给出「✅ 已发送至 <MAIL_TO>」确认即可,不要再问「需不需要发」。

当用户说「发送到邮箱」「打包发邮件」「ZIP 一下发给我」时执行：

#### 6.1 加载 SMTP 配置

复用步骤零的 `.env` 优先级查找逻辑，但目标变量是：

```bash
SMTP_HOST=smtp.qq.com          # 必填
SMTP_PORT=465                   # 必填，常见 465(SSL) / 587(STARTTLS)
SMTP_USER=you@qq.com            # 必填
SMTP_PASS=xxxxxxxxxxxxxxxx      # 必填，QQ/163 用「授权码」非登录密码
SMTP_FROM=you@qq.com            # 选填，默认等于 SMTP_USER
SMTP_TLS=ssl                    # 选填，ssl|starttls；默认按端口推断（465→ssl，其它→starttls）
MAIL_TO=mark@example.com        # 选填，缺省则用 AskUserQuestion 询问
```

加载函数与 token 同款，把上述变量逐个 `export`。**禁止把 SMTP_PASS 打印到终端**，只输出「来源：xxx」。

如果任何必填项缺失，**必须** 用 `AskUserQuestion` 引导用户补全；并询问是否把这些值写入 `~/.claude/skills/github-trend-analyzer/.env`（`chmod 600`）以便下次复用。

#### 6.2 打包

```bash
: "${TREND_REPORT_DIR:=$HOME/Desktop}"
TREND_REPORT_DIR="${TREND_REPORT_DIR/#\~/$HOME}"
[ -d "$TREND_REPORT_DIR" ] || TREND_REPORT_DIR="$HOME"
DIR="$TREND_REPORT_DIR/github-trend-report-$(date +%Y-%m-%d)"
ZIP="${DIR}.zip"
[ -d "$DIR" ] || { echo "目录不存在：$DIR"; exit 1; }
rm -f "$ZIP"
# 在 TREND_REPORT_DIR 内打包，使 ZIP 内只含 github-trend-report-YYYY-MM-DD/ 这一层
( cd "$TREND_REPORT_DIR" && zip -r "$(basename "$ZIP")" "$(basename "$DIR")" >/dev/null )
ls -la "$ZIP"
```

#### 6.3 发送邮件（带附件）

调用 `references/send-report.py`（见参考文档），用 Python 标准库 `smtplib + email`，无需额外依赖：

```bash
python3 "$(dirname "${BASH_SOURCE[0]:-$0}")/references/send-report.py" \
  --to "$MAIL_TO" \
  --subject "GitHub 趋势报告 $(date +%Y-%m-%d)" \
  --body-file "$DIR/report.md" \
  --attach "$ZIP"
```

成功后向用户确认：

- ✅ 已发送至：\<MAIL_TO>
- 📎 附件：\<ZIP 文件名> (\<size> KB)
- 📧 主题：\<主题>
- 🔐 SMTP：\<SMTP_HOST>:\<SMTP_PORT> (\<TLS 模式>)

#### 6.4 错误处理

- 鉴权失败（535）→ 提示用户检查 SMTP_PASS 是否为「授权码」而非登录密码
- 连接超时 → 提示检查 SMTP_HOST / 端口 / 网络
- 附件过大（>25MB） → 询问是否拆分或仅发 `report.md`

---

## 输出格式

```
📊 GitHub 趋势分析报告

━━━ 采样信息 ━━━
- 时间窗：YYYY-MM-DD ~ YYYY-MM-DD
- 领域：<领域 / 全部>
- 样本：新生 N / 互动高 N / star 高 N

━━━ 三类样本一览 ━━━

【新生项目 Top 10】（创建 < 30 天）
| Stars | 项目 | 语言 | Topics | 一句话定位 |
| ... |

【互动高 Top 10】（forks / issue 活跃）
| Forks | 项目 | … |

【Star 高 Top 10】
| Stars | 项目 | … |

━━━ 趋势归纳 ━━━

1. 技术栈：
   - 主语言分布：TypeScript 45% / Python 25% / Rust 15% …
   - 高频框架/runtime：…

2. 主题与定位（高频关键词）：
   - 新生：agent, MCP, RAG, llm-tool…
   - 长青：framework, ui, database…

3. 包装与品牌：
   - 命名：85% 用 ≤2 词短英文名；30% 带 emoji
   - README 首屏：Hero 图 70% / Demo GIF 60% / Badge 矩阵 90%
   - 官网：62% 拥有独立站点

4. 社区与商业化：
   - Discussions 启用率 …
   - 付费版形态：Cloud / Self-hosted / Sponsor …

━━━ 给「新项目」的设计建议 ━━━

🎯 定位
- [ ] 选定 1 个尚未拥挤但增长明显的细分（基于「新生项目」高频主题去重 star 高项目重叠）
- [ ] 用一句话定义产品：<动词 + 名词 + 差异化短语>，对标 X 但聚焦 Y

🏷️ 命名 & 视觉
- [ ] 取 ≤2 词的短英文名，可读、可记、能注册同名 npm/域名
- [ ] 准备 Logo + 首屏 Hero / Demo GIF（参考 Top X 的 README 模板）
- [ ] Badge 矩阵：版本 / build / license / discord / 下载量

🧱 技术选型
- [ ] 主语言：<根据样本推荐>，理由：<生态 / 性能 / 趋势>
- [ ] 关键依赖：…
- [ ] 单仓 vs 多包：建议 <pnpm workspace / single repo>

📚 文档与 DX
- [ ] README 首屏 30 秒看懂：定位 / 安装 / Quick Start / Demo
- [ ] 独立文档站（VitePress / Nextra / Mintlify）
- [ ] Playground / Sandbox 在线试用
- [ ] CLI 一键脚手架（npx create-xxx）

🌱 社区运营
- [ ] 启用 Discussions、设 Issue/PR 模板、给一份 ROADMAP.md
- [ ] 提供官方 Discord / Slack / 微信群入口
- [ ] 至少 5 篇 Examples，覆盖典型场景
- [ ] 第一周内联系 3–5 个相关 awesome-list 提交收录

💰 商业化（可选）
- [ ] 预留 Cloud / Pro 升级路径（不必现在做）
- [ ] 设计可被 Sponsor / OpenCollective 接的捐赠入口

━━━ 🚀 新项目初步设计（Project Blueprint） ━━━

▎ 1. 项目代号（候选 3 个）
  - <name-A>：<含义>，npm/域名可注册性 = 待确认
  - <name-B>：…
  - <name-C>：…
  推荐：<name-X>，因为 <理由>

▎ 2. 一句话定位
  <动词> for <具体场景>, powered by <差异化能力>
  对标：<样本中的真实仓库 owner/repo>
  差异：<本项目相对它的不同点>

▎ 3. 目标用户与场景
  场景 1：<某类用户在 …… 时遇到 …… 问题，本项目通过 …… 解决>
  场景 2：…

▎ 4. MVP 功能清单
  v0.1 (P0，阻塞发布)：
    - <feature-1>：…
    - <feature-2>：…
    - <feature-3>：…
  v0.2 (P1，发布后迭代)：
    - <feature-4>：…
    - <feature-5>：…

▎ 5. 技术栈选型
  - 语言：<选型>，理由：<一行>
  - 框架：<选型>，理由：<一行>
  - 关键依赖：<…>
  - 部署目标：<CLI / Desktop / SaaS / Self-host>

▎ 6. 仓库结构（建议）
  <repo>/
  ├── apps/         # 用户可见入口
  ├── packages/     # 可复用核心
  ├── docs/         # VitePress / Mintlify
  └── examples/     # 至少 5 个

▎ 7. 第一周 Roadmap
  Day 1: 仓库初始化 + 命名敲定 + 域名注册
  Day 2: 跑通最小 hello-world + 第一份 README
  Day 3: 实现 P0 feature-1
  Day 4: 实现 P0 feature-2
  Day 5: 文档站上线 + Demo GIF
  Day 6: 提交到 3 个 awesome-list + Discord 开通
  Day 7: ProductHunt / HN 预热文案

━━━ 风险与避坑 ━━━
- ⚠️ <例：避免与 Top X 同名/同定位的红海赛道>
- 💡 <例：从 hooks/CLI 这类低门槛切入，再扩展到完整 framework>
```

---

## 关键原则

1. **数据驱动**：所有结论必须能追溯到第二步采集的具体仓库；杜撰被视为失败。
2. **可执行性**：建议清单里的每条都必须是用户「明天可以动手」的事，不能停留在概念。
3. **三类对比**：单看 star 高会得到「长青项目」的偏见，必须把「新生」和「互动高」叠加，识别真实风口。
4. **API 限流**：未鉴权时 60 次/小时；鉴权后 5000 次/小时。在 Bash 中检测 `X-RateLimit-Remaining`，必要时让用户提供 `GITHUB_TOKEN`：
   ```bash
   curl -s -H "Authorization: Bearer $GITHUB_TOKEN" ...
   ```
5. **READMEs 抽样**：对 README 内容分析时，先在三类样本中各挑 3 个最有代表性的，避免一次拉太多。
6. **时间敏感**：使用 `date` 命令动态生成时间窗，永远不要硬编码日期。
7. **领域感**：相同字段在不同领域含义不同（例如「games」类 fork 多但二次开发少），分析结论需带领域标签。
8. **避免幸存者偏差**：star 高的项目结论要标注「这是已成功者的共性，不等于做这些就会成功」。

---

## 参考文档

- `references/github-api.md` — GitHub Search API 字段、限流、常用查询表达式
- `references/analysis-template.md` — 分析维度 checklist（技术栈 / 命名 / README / 社区 / 商业化）
- `references/send-report.py` — 邮件发送脚本（仅依赖 Python 3 标准库）
