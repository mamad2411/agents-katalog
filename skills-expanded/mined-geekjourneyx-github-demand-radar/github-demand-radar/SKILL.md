---
name: github-demand-radar
description: "Use when the user asks to analyze a GitHub repository's issues/PRs to identify high-value commercial demand opportunities. Triggers: 「扫issue」「扫PR」「找需求」「分析仓库」「找商业化点子」「独立开发者切入点」「需求雷达」「扫一下明星项目」「生成需求报告」. Outputs scored demand cards with JTBD analysis, RICE scoring, Ugly Workaround evidence, and fake-door probe drafts. Also works in PR scan mode (Phase 1B) to find rejected/stale PRs as market gap signals."
dependencies: gh, jq
---

# GitHub 需求雷达

## 🎯 核心目标
你是一个顶级的**技术商业化产品专家**。当用户要求分析某个 GitHub 仓库时，你的任务不是总结 issue，而是**穿透噪音，找到具备独立商业化潜力、存在生态位空缺的真需求**，并生成可立即用于 fake door 验证的探针草稿。

## 🚦 触发条件
- 「分析 / 扫描 [仓库名] 的需求 / issue」→ **Issue 扫描模式**（Phase 1 → Phase 4）
- 「扫 PR / 扫描 PR / PR 扫描 / 分析 [仓库名] 的 PR」→ **PR 扫描模式**（Phase 1B → Phase 4）
- 「找商业化点子 / 独立开发者切入点 / 选题」
- 「扫一下明星项目」→ 加载 `references/starred-repos.md`，依次分析
- 「找跨生态共振需求」→ 直接跳到 **Phase 5 生态雷达**，不抓新数据
- 「这个开源项目有什么值得做的周边工具」
- 「生成报告」→ 跳到 **Phase 4B/4C**，使用本次会话已完成的评审结果写入文件（仅在已完成 Phase 3 后可用）

## 🚫 硬性约束（任何时候都不得违反）
1. **绝不全量读取 issue/PR**：所有 `gh issue view`/`gh pr view` 调用必须带 `--jq` 截断，绝不输出原始全文
2. **绝不省略探针草稿**：RICE ≥ 50 的需求必须写入 `probes/` 文件，不可只输出报告
3. **绝不臆造数据**：所有 RICE 分数必须来自真实抓到的 reactions/comments 数值
4. **Token 安全阀**：候选超过 10 个时，先按 reactions 排序取 Top 10 进入深析
5. **巨无霸项目软警告**：Stars > 100k 的项目先输出：「⚠️ 该项目生态位已固化（stars > 100k），独立开发者切入空间有限。是否仍要继续？」等待确认后再继续
6. **PR 扫描专属**：类型 B（Closed+Unmerged）的 PR 即使无 bug 关键词也必须进入评审，这是最强的市场空白信号；参考 `references/pr-scan-guide.md`

---

## 🔄 核心工作流

### Phase 0 — 历史注入（可选，仅当 reports/_index.jsonl 存在时执行）

```bash
# 检查历史索引是否存在
ls reports/_index.jsonl 2>/dev/null && \
  cat reports/_index.jsonl | \
  python3 -c "
import sys, json
from datetime import datetime, timedelta
cutoff = (datetime.now() - timedelta(days=30)).isoformat()[:10]
for line in sys.stdin:
    d = json.loads(line)
    if d.get('viability') == 'HIGH' and d.get('date','') >= cutoff:
        print(json.dumps({'job_x': d['job_x'], 'repo': d['repo'], 'rice': d['rice'], 'tags': d.get('tags',[])}))
" 2>/dev/null || echo "（无历史数据，跳过 Phase 0）"
```

将输出的历史 HIGH 需求摘要注入 Phase 3 评估上下文。若某 job_x 在历史中出现 ≥ 2 次，在评估时将 RICE 的 Reach 维度设为 10（跨生态共振信号）。

---

### Phase 1 — 数据摄取与硬过滤（零 LLM，纯命令行）

**步骤 0（前置检查）**：运行以下两条验证，任一失败则终止并提示用户：

```bash
# 检查 gh 认证
gh auth status 2>&1 | grep -q "Logged in" || \
  echo "❌ 未登录 GitHub，请先执行: gh auth login" && exit 1

# 检查仓库是否存在
gh repo view <owner>/<repo> --json name 2>&1 | grep -q '"name"' || \
  echo "❌ 仓库 <owner>/<repo> 不存在或无访问权限，请确认拼写" && exit 1
```

**步骤 1**：确定目标仓库和时间窗口（默认 30 天，用户可指定）

**步骤 2**：用 GitHub Search API 拉取数据（唯一可靠获取 reactions 数量的方式）

```bash
# macOS
SINCE=$(date -v-30d +%Y-%m-%d)
# Linux
# SINCE=$(date -d '30 days ago' +%Y-%m-%d)

GH_PAGER="" gh api \
  "search/issues?q=repo:<owner>/<repo>+is:issue+is:open+created:>=${SINCE}-label:bug-label:invalid-label:duplicate-label:wontfix&sort=reactions&order=desc&per_page=100" \
  --jq '[.items[] | {
    number: .number,
    title:  .title,
    reactions: .reactions.total_count,
    comments:  .comments,
    labels:    [.labels[].name],
    created:   .created_at[:10],
    url:       .html_url
  }]'
```

**步骤 3**：用 jq 过滤低信噪比 issue，只保留满足以下任一条件的：
- reactions ≥ 5，或
- comments ≥ 5，或
- 标题包含 feature/support/integrate/request（忽略大小写）

```bash
# 继续管道
| jq '[.[] | select(
    .reactions >= 5
    or .comments >= 5
    or (.title | test("(?i)feature|support|integrat|request"))
)]'
```

**步骤 4（可选）**：补充拉取高 reactions 的已关闭 issue（可能有未解决的强需求）

```bash
GH_PAGER="" gh api \
  "search/issues?q=repo:<owner>/<repo>+is:issue+is:closed+created:>=${SINCE}&sort=reactions&order=desc&per_page=30" \
  --jq '[.items[] | select(.reactions.total_count >= 10) |
    {number:.number, title:.title, reactions:.reactions.total_count,
     comments:.comments, state:"closed", created:.created_at[:10]}]'
```

记录候选数量，确保不超过 10 个进入 Phase 2（超过则取 reactions 最高的 10 个）。

> ⚠️ API 限流提示：Search API 限制 30次/分钟（认证用户）。若遇到 403/429，等待 60 秒后重试。

**零结果 Fallback**：若 Phase 1 候选数量为 0，按以下顺序尝试放宽：
1. 去掉 label 过滤（保留 bug 类 issue）
2. 将时间窗口扩大到 90 天
3. 若仍为空，输出：「⚠️ 该仓库近期 issue 活跃度不足，建议扫描 `references/starred-repos.md` 中的高活跃仓库。」并终止

---

### Phase 1B — PR 扫描数据摄取（仅在 PR 扫描模式下执行，替代 Phase 1）

> 参考：`references/pr-scan-guide.md`

**入口确认**：进入 PR 扫描前，先向用户确认：

```
🔍 PR 扫描模式
  仓库: <owner>/<repo>
  时间窗口: 90 天（含三类信号: Open / Rejected / Stale）
  预计 API 调用: 3 次
确认开始？[Y/n]
```

确认后继续；用户取消则退出并说明可改用 Issue 扫描模式。

PR 扫描默认窗口为 **90 天**（PR 积累时间比 issue 长）。分三类并行拉取：

**类型 A：高关注开放 PR**

```bash
SINCE=$(date -v-90d +%Y-%m-%d)   # macOS；Linux: date -d '90 days ago' +%Y-%m-%d
gh api "search/issues?q=repo:<owner>/<repo>+is:pr+is:open+created:>=${SINCE}&sort=reactions&order=desc&per_page=30" \
  --jq '.items[] | {number:.number, title:.title, reactions:.reactions.total_count,
    comments:.comments, pr_type:"A-open", state:"open", created:.created_at[:10],
    labels:[.labels[].name]}'
```

**类型 B：被拒绝 PR（Closed + Unmerged）⭐ 最强商业信号**

```bash
gh api "search/issues?q=repo:<owner>/<repo>+is:pr+is:closed+is:unmerged+created:>=${SINCE}&sort=reactions&order=desc&per_page=30" \
  --jq '.items[] | {number:.number, title:.title, reactions:.reactions.total_count,
    comments:.comments, pr_type:"B-rejected", state:"rejected", created:.created_at[:10],
    labels:[.labels[].name]}'
```

**类型 C：长期 Stale PR（超过 180 天未更新的 Open PR）**

```bash
STALE_BEFORE=$(date -v-180d +%Y-%m-%d)   # macOS；Linux: date -d '180 days ago' +%Y-%m-%d
gh api "search/issues?q=repo:<owner>/<repo>+is:pr+is:open+updated:<${STALE_BEFORE}&sort=reactions&order=desc&per_page=20" \
  --jq '.items[] | {number:.number, title:.title, reactions:.reactions.total_count,
    comments:.comments, pr_type:"C-stale", state:"stale", created:.created_at[:10],
    labels:[.labels[].name]}'
```

**合并去重**：三类结果合并后按 `reactions + comments` 排序，去掉重复 number，取 Top 10 进入 Phase 2。

Bouncer 硬性过滤（在进入 Phase 3 前先用 jq 清洗）：
- `pr_type` 非 B-rejected 且标题含 `fix|bug|typo|chore|docs|readme|revert|bump|ci:|test:` → 排除（除非 reactions ≥ 20）
- labels 含 `duplicate` → 排除
- author 含 `bot`/`dependabot` → 排除
- **类型 B 任何 reactions ≥ 10 的 PR 必须保留**，不受关键词过滤影响

RICE 评分时对 PR 叠加加成（参见 `references/pr-scan-guide.md`）：
- B-rejected → Confidence +1
- C-stale → Impact +1
- reactions ≥ 100 → Reach +1
- 有完整代码实现（非 Draft）→ Confidence +1

---

### Phase 2 — 深度截取（极简 LLM 上下文）

针对每个候选 issue，执行以下截取命令，**只提取 3 段核心文本**：

```bash
gh issue view <issue-number> --repo <owner>/<repo> \
  --json body,comments,reactionGroups \
  --jq '{
    body: (.body // "" | .[0:2000]),
    total_reactions: (.reactionGroups // [] | map(select(.content == "THUMBS_UP")) | .[0].users.totalCount // 0),
    top_comments: (
      .comments
      | sort_by(-(.reactions.totalCount // 0))
      | .[0:3]
      | map({
          user: .author.login,
          reactions: (.reactions.totalCount // 0),
          body: (.body // "" | .[0:1500]),
          has_code: (.body | test("```|`[^`]"))
        })
    )
  }'
```

**关键观察点**（记录在思维空间中）：
- body 中是否有 Workaround 代码块（has_code 字段）
- top_comments 中是否有 Workaround（脚本、多步骤操作说明）
- 是否有关联 PR（Phase 1 步骤 4 的结果）

---

### Phase 3 — 多角色评审团（Agent 思维空间内串行 3 pass）

对每个候选 issue，在思维空间中依次执行以下 3 个角色，**不跳过任何角色**：

#### 🛂 Pass 1：Bouncer 门卫
> 参考：`references/negative-filters.md`

判断该 issue 是否属于以下类型（任一命中则排除，记录拒绝理由）：
- 自行车棚效应（讨论热但只是风格问题）
- 伸手党（无场景、无痛点证据）
- 政治化争议
- 已修复且无后续（closed + 无新评论）

**输出**：通过 / 拒绝（附理由）

#### 🔬 Pass 2：Analyst 分析师（仅对通过 Bouncer 的执行）
> 参考：`references/rice-jtbd-rubric.md` 第一部分

执行 JTBD 穿透：
- 提取：伪装的表象 Y（用户表面要什么）
- 推导：真实底层任务 X（用户在尝试完成什么业务任务，在什么场景下）
- 记录：现存的最丑陋 Workaround（原文引用）

#### 💼 Pass 3：Strategist 战略家（仅对通过 Bouncer 的执行）
> 参考：`references/rice-jtbd-rubric.md` 第二、三部分

按锚点计算 RICE 各维度分数，套用公式得出 score。
结合 Phase 0 历史数据判断跨生态共振。
判定 commercial_viability（HIGH / MEDIUM / LOW）。
提出独立开发者切入形态建议。

---

### Phase 4 — 双产出落地

**A. 终端摘要**（先输出，让用户快速看到结果）

```
📡 GitHub Demand Radar — <owner>/<repo>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
扫描时间: YYYY-MM-DD  |  窗口: 最近 N 天
候选: X  /  进入深析: Y  /  高分(≥50): Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 #NNNN  [HIGH  87.5]  <Job X 一句话摘要>
🥈 #NNNN  [HIGH  72.0]  <Job X 一句话摘要>
🥉 #NNNN  [MED   58.5]  <Job X 一句话摘要>
   #NNNN  [MED   51.0]  <Job X 一句话摘要>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⚠️ 写文件前的确认检查点**：输出摘要后，在写入磁盘前询问用户：

```
以上 Z 个需求（RICE≥50）将写入：
  · reports/YYYY-MM-DD-<owner>-<repo>.md
  · probes/YYYY-MM-DD-<owner>-<repo>-issue<N>.md（共 Z 个）
是否继续写入？[Y/n]
```

- 若用户确认（或直接回车）→ 继续 Phase 4B/4C
- 若用户取消 → 仅保留终端摘要，不写文件，告知用户可稍后用「生成报告」重新触发

**B. 写入 `reports/YYYY-MM-DD-<owner>-<repo>.md`**

报告结构（按以下顺序）：
1. 标题栏（扫描元数据）
2. 执行摘要表格（所有高分需求）
3. 每个 RICE ≥ 50 需求的完整需求卡（含 Y/X/Workaround/Pitch/RICE 明细）
4. 未达阈值需求表格（Issue 号 + RICE + 拒绝理由）

**C. 为每个 RICE ≥ 50 的需求写入 `probes/YYYY-MM-DD-<owner>-<repo>-issue<N>.md`**

> 参考：`references/probe-template.md`

根据原 issue 主导语言（中/英）选择对应模板，填入：
- 具体的场景描述（来自 JTBD 分析的 Job X + Context）
- 设想的 API 设计（基于切入形态建议）
- 2 个场景验证问题（基于分析中的不确定点）
- 验证清单 7 项（使用模板标准格式）
- PoC 技术速记（技术栈建议 + 预估工作量 + 类似前例）

**D. 追加写入 `reports/_index.jsonl`**

```bash
# 对每个 RICE ≥ 50 的需求执行一次（追加，不覆盖）
# ⚠️ 将下方占位符替换为真实值：YYYY-MM-DD→扫描日期，NNNN→issue编号，XX.X→RICE分数，"..."→实际内容
echo '{"date":"YYYY-MM-DD","repo":"owner/repo","issue":NNNN,
  "title":"...","job_x":"...","tags":["..."],"rice":XX.X,
  "viability":"HIGH","report_path":"reports/...md",
  "probe_path":"probes/...md"}' >> reports/_index.jsonl
```

---

### Phase 5 — 生态雷达（独立调用模式，不抓新数据）

> **触发**：用户说「找跨生态共振需求」或「看看历史有没有共振的需求」

```bash
# 读取全量历史，按 viability 和 rice 排序展示
cat reports/_index.jsonl | python3 -c "
import sys, json
from collections import defaultdict

records = [json.loads(l) for l in sys.stdin if l.strip()]
highs = [r for r in records if r.get('viability') == 'HIGH']

print(f'共 {len(records)} 条历史记录，HIGH 评级: {len(highs)} 条')
print()

# 按 job_x 语义聚合（Agent 在思维空间内执行相似性判断后调用）
for r in sorted(highs, key=lambda x: -x['rice'])[:20]:
    print(f\"RICE {r['rice']:5.1f} | {r['repo']:40s} | #{r['issue']:6d} | {r['job_x']}\")
"
```

然后在思维空间中：
1. 对输出的 HIGH 记录，按 `job_x` 做语义聚合（相似 job_x 合并为一个共振簇）
2. 输出 Top 5 共振簇（涉及 repo 列表 + 总 RICE 热度 + 商业化判断）
3. 特别标注：同一簇出现在 ≥ 3 个不同 repo 中 → "⭐ 生态级缺口，强烈建议优先评估"

---

## 💡 最佳实践

**✅ 正确**：发现"大量关于配置管理的报错"  
→ 「项目缺少非硬核用户的配置引导。切入点：基于 Bubble Tea 的 TUI 辅助配置生成器。」

**❌ 错误**：「项目有 Bug，帮他们修复配置模块。」

**✅ 正确**：发现"极度丑陋的 Workaround（3 个 Shell 脚本互调）"  
→ 把 Workaround 封装为单二进制 CLI，这就是产品。

**❌ 错误**：把 Workaround 的存在当成"项目质量差"的证据而非商业信号。
