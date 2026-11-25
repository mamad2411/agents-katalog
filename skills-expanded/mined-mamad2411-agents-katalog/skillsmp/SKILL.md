---
name: skillsmp
description: 在 SkillsMP（1.6M+ 公开 SKILL.md 的索引，覆盖 Claude Code / Codex / ChatGPT）里搜 Agent Skill，按关键词、分类、职业、语言过滤，并专门挖那些「写得好但没人知道」的冷门 Skill。用户说 找个 skill、有没有现成的 skill、搜一下 skill、skillsmp、skills 市场、agent skill 搜索、find a skill、search skills、discover skills 时使用。也用于判断某个领域已经有哪些 Skill、避免重复造轮子。
---

# SkillsMP

搜 [SkillsMP](https://skillsmp.com) —— 目前最大的公开 Agent Skill 索引（1.6M+ 个
SKILL.md，来自 GitHub，覆盖 Claude Code、Codex、ChatGPT）。

**要动手写一个新 Skill 之前，先来这里搜一遍。** 别人写过的概率比你以为的高。

## 目录

```
skillsmp/
├── SKILL.md            ← 你在这里：怎么搜、怎么挖宝、两个必须知道的坑
├── .env.example        ← 复制成 .env 填 API Key（可选；.env 已被忽略，绝不提交）
└── scripts/
    ├── search.mjs      直搜。可翻页、可按分类/职业/语言过滤，可 --json
    └── treasure.mjs    ★ 挖宝。故意不按星数排，理由见下
```

## 先跑起来

不需要任何配置——**匿名就能用**（50 次/天、10 次/分钟）：

```bash
node scripts/search.mjs "关键词" --limit 20
```

想要 500 次/天，就配一个 Key：

```bash
cp .env.example .env      # 然后把 Key 填进去
```

Key 从 <https://skillsmp.com/docs/api> 生成。它是凭据，**只放 `.env`，绝不进仓库**
（仓库的 `.gitignore` 已经拦了 `*/.env`，别绕过它）。

## 两个必须知道的坑

### ★ 不是这个 Skill 的星数，是它所在仓库的星数

这是本 Skill 存在的主要理由。API 返回的 `stars` 是**包含该 Skill 的 GitHub 仓库**
的星数。实测：某条结果报 240467，而它所在仓库的真实星数是 240743 —— 对得上，确认无疑。

后果很实际：

- 一个塞在超高星仓库里的 Skill（哪怕只是整包机翻的文档）**自动继承那个星数**；
- 一个作者单独开仓库、认真写的单一用途 Skill，只有个位数星。

实测搜 `backlink` 按星排序，前四条里三条来自同一个 28562★ 的笔记仓库，
讲的是笔记系统内部的双向链接，跟外链毫无关系。**高星把语义对口的结果整个淹掉了。**

所以：`sortBy=stars` 排出来的不是「最好的 Skill」，是「住在最红仓库里的 Skill」。

### 翻页要认 `hasNext`，别认 `total`

`pagination.total` 附带一个 `totalIsExact: false`，而且实测严重偏低——百万级索引里
搜 `SEO` 只报 `total: 5`。**按 total 算页数会漏掉绝大部分结果。**
唯一可靠的翻页依据是 `hasNext`，两个脚本都已经这么做了。

## 挖宝：找「写得好但没人知道」的

既然星数不是质量信号，就别用它排。`treasure.mjs` 用四个跟仓库名气无关的信号：

```bash
node scripts/treasure.mjs "关键词" --pages 5 --max-stars 2000 --top 15
```

| 信号 | 想法 |
|---|---|
| **独立性** | 所在仓库星数越低，越说明这个 Skill 靠自己站住，不是搭便车 |
| **专注度** | 同一仓库在本次结果里出现几条。一个仓库刷出几十条，通常是批量生成或整包翻译的文档堆 |
| **描述具体度** | 好的描述会写清**什么时候该用**（触发条件、场景、反例），而不是「帮你做 X」。这是分辨用不用心最单一有效的信号 |
| **新鲜度** | 长期没动的多半已经烂掉 |

同名同作者跨多语言的条目会被去重——那是整包机翻，一个仓库能刷满整页。

**这是启发式排序，不是判决。** 脚本只负责把候选排到你眼前；
要不要用，仍然得打开那个 `SKILL.md` 读一遍。别把分数当成质量结论报给用户。

## 过滤参数

两个脚本共用：

| 参数 | 说明 |
|---|---|
| `--pages N` | 翻几页（search 默认 1，treasure 默认 5） |
| `--limit N` | 每页几条，上限 100 |
| `--sort stars\|recent` | 只有 search 有。**先读上面那条坑再决定用不用 stars** |
| `--category <slug>` | 如 `data-ai`、`devops` |
| `--occupation <slug>` | SOC 职业，如 `software-developers` |
| `--lang <code>` | `en` / `zh` / `ja` 等 ISO 码；`mul` 混合，`und` 判不出 |
| `--json` | 输出 JSON 而不是表格 |

不支持通配符（`*`），也不支持空查询。

## 配额与报错

响应头一直在报剩余量，脚本会把它打在结尾。常见错误已经翻译成人话：
`INVALID_API_KEY`（Key 无效）、`DAILY_QUOTA_EXCEEDED`（当日用完）、
`MISSING_QUERY`（没给关键词）、`INVALID_OCCUPATION` / `INVALID_LANGUAGE`（slug 不认识）。

搜索结果**尽量不要在一次任务里反复重搜同一个词**——配额是按天算的，
匿名只有 50 次。需要反复查询时用 `--json` 存一份到本地再过滤。

## 汇报纪律

把搜到的 Skill 告诉用户时：

- **说清 ★ 是仓库星数**，不要让用户以为那是这个 Skill 的受欢迎程度；
- 推荐之前**至少读一眼它的 `githubUrl`**，别只凭 description 就推荐——
  描述是作者自己写的营销文案，不是验证过的能力；
- 命中很少时如实说命中很少。这个索引有 1.6M 条，搜不到通常意味着词不对，
  换个说法再搜一次，而不是断言「不存在」。
