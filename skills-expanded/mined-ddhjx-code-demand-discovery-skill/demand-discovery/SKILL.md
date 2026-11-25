---
name: demand-discovery
description: 每日自动化长尾需求发现调研。当用户说「每日调研」「发现需求」「需求调研」「niche research」「demand discovery」或要求运行需求发现工作流时触发。需要 7 个 MCP 服务器：niche-reddit-mcp、niche-google-trends-mcp、niche-producthunt-mcp、niche-g2-mcp、niche-github-issues-mcp、niche-hackernews-mcp、niche-alternativeto-mcp（首次运行自动配置）。
---

# 长尾需求发现 - 每日调研工作流

目标：利用 7 个 MCP 工具，系统化发掘**需求量不够大到公司来做，但真实存在、可通过独立开发者建站解决**的长尾需求。

## 首次运行：自动环境配置

每次运行时先检查 MCP 服务器是否已配置。如未配置，自动执行以下步骤：

### 步骤 1：检查 MCP 服务器配置

检查当前平台的 MCP 配置中是否存在以下 7 个服务器：
- Claude Code / iFlow：读取 `~/.claude/settings.local.json`（或 `~/.iflow/settings.json`）的 `mcpServers`
- 其他平台：检查环境变量和 shell 中 `uvx` 是否可用

```json
{
  "mcpServers": {
    "niche-reddit-mcp": {
      "command": "uvx",
      "args": ["niche-reddit-mcp"],
      "env": {
        "REDDIT_CLIENT_ID": "",
        "REDDIT_CLIENT_SECRET": ""
      }
    },
    "niche-google-trends-mcp": {
      "command": "uvx",
      "args": ["niche-google-trends-mcp"]
    },
    "niche-producthunt-mcp": {
      "command": "uvx",
      "args": ["niche-producthunt-mcp"],
      "env": {
        "PRODUCTHUNT_TOKEN": ""
      }
    },
    "niche-g2-mcp": {
      "command": "uvx",
      "args": ["niche-g2-mcp"]
    },
    "niche-github-issues-mcp": {
      "command": "uvx",
      "args": ["niche-github-issues-mcp"],
      "env": {
        "GITHUB_TOKEN": ""
      }
    },
    "niche-hackernews-mcp": {
      "command": "uvx",
      "args": ["niche-hackernews-mcp"]
    },
    "niche-alternativeto-mcp": {
      "command": "uvx",
      "args": ["niche-alternativeto-mcp"]
    }
  }
}
```

### 步骤 2：补全缺失的 MCP 配置

**Claude Code / iFlow**：将缺失的服务器配置写入 `~/.claude/settings.local.json`（或 `~/.iflow/settings.json`）的 `mcpServers` 字段，然后提示用户重启会话。

**其他平台**：提示用户确保 `uvx` 可用（`pip install uv` 或 `curl -LsSf https://astral.sh/uv/install.sh | sh`），MCP 服务器会在调用时通过 `uvx` 自动安装运行。

### 步骤 3：凭证引导

检查需要凭证的 MCP 是否已配置：

**Reddit MCP**（需要 OAuth2）：
- 检查 `REDDIT_CLIENT_ID` 和 `REDDIT_CLIENT_SECRET` 是否非空
- 如为空，引导用户：
  > 1. 访问 https://www.reddit.com/prefs/apps
  > 2. 创建一个 "script" 类型的 app
  > 3. 获取 client_id（app 名称下方）和 client_secret
  > 4. Claude Code：填入 `~/.claude/settings.local.json` 的 `mcpServers.niche-reddit-mcp.env`；其他平台：设置环境变量 `REDDIT_CLIENT_ID` 和 `REDDIT_CLIENT_SECRET`

**Product Hunt MCP**（需要 Developer Token）：
- 检查 `PRODUCTHUNT_TOKEN` 是否非空
- 如为空，引导用户：
  > 1. 访问 https://www.producthunt.com/v2/oauth/applications
  > 2. 创建应用并获取 Developer Token
  > 3. Claude Code：填入 `~/.claude/settings.local.json` 的 `mcpServers.niche-producthunt-mcp.env`；其他平台：设置环境变量 `PRODUCTHUNT_TOKEN`

**Google Trends MCP**：无需凭证，但可能受 Google 限流影响。

**G2 MCP**：无需凭证，通过浏览器自动化工作。首次使用时会自动启动 Chrome。如需登录 G2 获取完整评论数据，运行：
```bash
uvx niche-g2-mcp --login
```

**GitHub Issues MCP**（可选 Token，提高速率限制）：
- 检查 `GITHUB_TOKEN` 是否非空
- 无 token 也可使用（60 请求/小时），有 token 可达 5000 请求/小时
- 如需配置，引导用户：
  > 1. 访问 https://github.com/settings/tokens
  > 2. 创建 Personal Access Token（Classic），勾选 `public_repo` 权限
  > 3. Claude Code：填入 `~/.claude/settings.local.json` 的 `mcpServers.niche-github-issues-mcp.env`；其他平台：设置环境变量 `GITHUB_TOKEN`

**Hacker News MCP**：无需凭证，使用公开的 Algolia HN API。

**AlternativeTo MCP**：无需凭证，解析 AlternativeTo 公开页面。

凭证未配置的 MCP 在调研时会被跳过，不影响其他 MCP 正常工作。

## 数据目录

所有输出写入 skill 安装目录下的 `output/` 子目录：
- `output/tracker.md` — 品类轮换状态
- `output/findings-index.md` — 累积发现排行榜
- `output/reports/YYYY-MM-DD-<品类>.md` — 每日调研报告

首次运行时自动创建目录结构（`mkdir -p <skill-dir>/output/reports`）。

> 注：`<skill-dir>` 指 skill 的安装位置，如 `~/.claude/skills/demand-discovery/`、`~/.hermes/skills/demand-discovery/` 等。各平台安装位置不同，但输出始终在 skill 目录下的 `output/`。

## 工作流（5 阶段）

### 阶段 1：准备

1. 读取 `output/tracker.md`（位于 skill 安装目录下）
2. 按品类轮换表（见 `references/niche-rotation.md`）找到下一个未调研或最久未调研的品类
3. 读取该品类对应的关键词配置
4. 宣布：「今日调研品类：[品类名]（轮换位置 N/26）」

如果用户指定了品类，则跳过轮换直接使用用户指定的品类。

### 阶段 2：痛点挖掘（Reddit MCP）

用 niche-reddit-mcp 的工具搜索用户痛点：

1. **搜索痛点帖子**
   ```
   reddit_search_pain_points(
     subreddits: [品类对应的子版块],
     keywords: [品类对应的痛点关键词],
     time_filter: "month",
     sort: "relevance",
     limit: 20
   )
   ```

2. **深入高信号帖子** — 挑选得分最高的 3 个帖子：
   ```
   reddit_get_post_details(post_url: "...", comment_limit: 15)
   ```
   从评论中提取具体的抱怨、功能请求、"I wish" 表述。

3. **搜索替代品讨论** — 针对结果中出现频率最高的 2-3 个工具名：
   ```
   reddit_search_alternatives(tool_name: "...", limit: 10)
   ```

**记录**：每个独立需求/痛点、来源帖子 URL、帖子得分、评论数。

> 注意：如果 niche-reddit-mcp 不可用（未配置凭证），跳过此阶段，在报告中标注「Reddit 数据缺失」。

### 阶段 3：竞品差评分析（G2 MCP）

用 niche-g2-mcp 的工具分析竞品差评：

1. **搜索品类产品**
   ```
   g2_search_products(query: "[品类搜索词]", limit: 5)
   ```

2. **提取差评** — 对评论数最多的前 3 个产品：
   ```
   g2_get_reviews(
     product_slug: "...",
     rating_filter: "low",
     sort: "most_recent",
     limit: 10
   )
   ```
   从 pros/cons 中提取：反复出现的抱怨、缺失的功能、用户流失原因。

3. **了解竞争格局**
   ```
   g2_get_alternatives(product_slug: "[头部产品]", limit: 5)
   ```

**记录**：差评中的高频痛点、涉及产品名、差评数量。

> 注意：G2 有 CAPTCHA 保护，如触发需要用户手动在浏览器中验证。如果 niche-g2-mcp 不可用，跳过此阶段。

### 阶段 4：趋势发现（Product Hunt MCP）

用 niche-producthunt-mcp 发现新兴替代方案：

1. **搜索品类产品**
   ```
   ph_search_products(query: "[品类关键词]", limit: 10)
   ```

2. **查看热门产品详情** — 对投票数最高的前 3 个产品：
   ```
   ph_get_product_details(product_slug: "...")
   ```
   关注：用户评论中的赞美点和批评点、产品的差异化卖点。

3. **发现趋势话题**
   ```
   ph_get_trending_topics(limit: 10)
   ```
   筛选与今日品类相关的趋势话题。

**记录**：新产品方向、投票数、用户反馈信号。

> 注意：如果 niche-producthunt-mcp 未配置 token，跳过此阶段。

### 阶段 5：开源需求挖掘（GitHub Issues MCP）

用 niche-github-issues-mcp 发现开源社区的功能请求：

1. **搜索品类相关 Issue**
   ```
   gh_search_issues(
     query: "[品类关键词] feature request",
     labels: ["feature-request", "enhancement"],
     sort: "reactions",
     per_page: 20
   )
   ```

2. **查找热门仓库** — 找到该品类最热门的仓库：
   ```
   gh_search_repos(query: "[品类关键词]", sort: "stars", per_page: 5)
   ```

3. **深入 Top 仓库的 Issue** — 对 star 数最高的 2-3 个仓库：
   ```
   gh_get_repo_issues(
     owner: "...", repo: "...",
     labels: "feature-request,enhancement",
     sort: "reactions",
     per_page: 15
   )
   ```

4. **Issue 详情** — 挑选反应数最高的 3 个 issue：
   ```
   gh_get_issue_details(owner: "...", repo: "...", issue_number: N, comment_limit: 10)
   ```

**记录**：高反应 issue 的需求描述、反应数、评论数、相关仓库。

> 注意：无 GITHUB_TOKEN 时速率限制为 60 请求/小时，可能需要减少查询量。

### 阶段 6：开发者讨论分析（Hacker News MCP）

用 niche-hackernews-mcp 发现开发者社区的讨论和痛点：

1. **搜索品类相关讨论**
   ```
   hn_search(
     query: "[品类关键词]",
     tags: "story",
     sort: "popularity",
     time_range: "month",
     per_page: 20
   )
   ```

2. **搜索 Ask HN 讨论** — 发现社区主动求助的问题：
   ```
   hn_get_ask_hn(per_page: 20, time_range: "month")
   ```
   筛选与今日品类相关的帖子。

3. **查看 Show HN** — 发现开发者正在构建什么：
   ```
   hn_get_show_hn(per_page: 20, time_range: "month")
   ```
   筛选与今日品类相关的帖子。

4. **深入高分帖子** — 对得分最高的 2-3 个帖子：
   ```
   hn_get_story_details(story_id: N, comment_limit: 15)
   ```

**记录**：讨论主题、得分、评论数、社区对痛点的共识。

### 阶段 7：替代品需求分析（AlternativeTo MCP）

用 niche-alternativeto-mcp 了解软件替代需求：

1. **搜索品类软件**
   ```
   alt_search(query: "[品类关键词]", per_page: 10)
   ```

2. **获取热门软件的替代品** — 对 likes 最高的 2-3 个软件：
   ```
   alt_get_alternatives(software_slug: "...", per_page: 10)
   ```
   关注哪些替代品最受欢迎，哪些需求未被满足。

3. **软件详情** — 对最相关的产品：
   ```
   alt_get_software_details(software_slug: "...")
   ```
   获取标签、平台、定价信息。

**记录**：替代品数量、用户偏好的替代方向、尚未覆盖的平台或功能。

> 注意：AlternativeTo 通过 HTML 解析工作，页面结构变化可能影响数据提取。

### 阶段 8：流量验证（Google Trends MCP）

用 niche-google-trends-mcp 验证前 3 个阶段发现的需求：

1. **提取关键词** — 从前面阶段整理出 5-8 个需求相关的搜索关键词

2. **验证搜索热度**（每批最多 5 个关键词）：
   ```
   trends_interest_over_time(
     keywords: ["keyword1", "keyword2", ...],
     timeframe: "12m"
   )
   ```

3. **发现关联查询** — 对最有潜力的 2 个关键词：
   ```
   trends_related_queries(keyword: "...", timeframe: "12m")
   ```

4. **横向对比**
   ```
   trends_compare(keywords: ["top1", "top2", "top3"], timeframe: "12m")
   ```

**记录**：热度值（0-100）、趋势方向（上升/稳定/下降）、关联上升查询。

> 注意：pytrends 可能受 Google 限流影响。如遇 429 错误，跳过此阶段并在报告中标注。

## 阶段 9：分析汇总 & 输出报告

### 综合评分

对每个发现的需求，按评估方法论（见 `references/estimation-methodology.md`）计算：

**需求量评分（0-100）**：
- Reddit 信号 x 20%：`min((帖子平均得分 * 2 + 平均评论数 * 3), 100)`
- G2 信号 x 15%：`min(相关差评数 * 5, 100)`
- GitHub Issues 信号 x 15%：`min((issue 反应数 * 3 + 评论数 * 2), 100)`
- Hacker News 信号 x 15%：`min((帖子得分 / 5 + 评论数 * 2), 100)`
- Trends 信号 x 15%：Google Trends 热度值（已是 0-100）
- PH 信号 x 10%：`min(平均投票数 / 5, 100)`
- AlternativeTo 信号 x 10%：`min(替代品数量 * 3 + likes / 10, 100)`

缺失数据源的权重重新分配到其他可用数据源。

**趋势判断**：
- 上升：近 6 个月 vs 前 6 个月热度增长 > 20%
- 稳定：变化在 +/- 20% 以内
- 下降：下降 > 20%

**可行性评分（1-5）**：
| 分数 | 标准 |
|------|------|
| 5 | 无明显竞品，技术门槛低，2 周内可出 MVP |
| 4 | 1-2 个小竞品，中等复杂度，2-4 周 MVP |
| 3 | 有竞品但存在差异化空间，1-2 月 MVP |
| 2 | 拥挤赛道但有未覆盖细分，需大量投入 |
| 1 | 大公司主导，进入壁垒高 |

### 输出报告

将报告写入 `output/reports/YYYY-MM-DD-<品类slug>.md`，格式：

```markdown
# 需求发现报告：[品类名]
**日期**：YYYY-MM-DD
**品类**：[品类名]
**轮换位置**：N/26

## 摘要
[2-3 句概述发现了什么]

## 发现需求一览

| # | 需求描述 | 细分品类 | 证据来源 | 需求量评分 | 趋势 | 可行性 | 备注 |
|---|---------|---------|---------|-----------|------|-------|------|
| 1 | [描述] | [细分] | Reddit: [url]（得分/评论）; G2: [产品]（N条差评）; GH: [repo#N]（N反应）; HN: [id]（N分）; Alt: [slug]（N替代品）; Trends: [热度]; PH: [产品]（N票） | [0-100] | [上升/稳定/下降] | [1-5] | [关键洞察] |

## Top 3 机会详解

### 1. [需求名称]
- **用户痛点**：[直接引用用户原话或总结]
- **现有方案**：[有什么产品、为什么不够好]
- **潜在产品形态**：[独立开发者可以做什么]
- **证据来源**：[所有 URL 列表]
- **评分依据**：[各分项得分明细]
- **可行性理由**：[为什么独立开发者能做]

### 2. [...]
### 3. [...]

## 数据统计
- Reddit 帖子扫描数：N
- G2 产品分析数：N
- G2 差评阅读数：N
- GitHub Issues 检查数：N
- GitHub 仓库分析数：N
- Hacker News 帖子扫描数：N
- AlternativeTo 软件检查数：N
- Product Hunt 产品检查数：N
- Google Trends 关键词验证数：N

## 关联上升查询
[来自 trends_related_queries 的上升查询，可为后续调研种子]
```

### 更新跟踪文件

1. 更新 `output/tracker.md` 中该品类的调研日期和 top 发现
2. 将评分 >= 30 且可行性 >= 3 的需求追加到 `output/findings-index.md`

## 容错规则

- 任何 MCP 不可用时，跳过对应阶段并在报告中标注
- 至少 1 个 MCP 可用即可产出报告（评分权重自动重分配）
- 遇到 CAPTCHA / 429 / 超时等错误，记录错误信息后继续
- 不要因单个工具失败而中断整个工作流

## PyPI 包信息

本 skill 依赖以下 7 个 PyPI 包，通过 `uvx` 自动安装运行：

| PyPI 包名 | MCP 服务器名 | 用途 | 需要凭证 |
|-----------|------------|------|---------|
| `niche-reddit-mcp` | niche-reddit-mcp | Reddit 痛点挖掘 | Reddit OAuth2 |
| `niche-google-trends-mcp` | niche-google-trends-mcp | Google Trends 流量验证 | 无 |
| `niche-producthunt-mcp` | niche-producthunt-mcp | Product Hunt 趋势发现 | PH Developer Token |
| `niche-g2-mcp` | niche-g2-mcp | G2 竞品差评分析 | 无（浏览器自动化） |
| `niche-github-issues-mcp` | niche-github-issues-mcp | GitHub 开源需求挖掘 | GitHub Token（可选） |
| `niche-hackernews-mcp` | niche-hackernews-mcp | Hacker News 讨论分析 | 无 |
| `niche-alternativeto-mcp` | niche-alternativeto-mcp | 替代品需求分析 | 无 |
