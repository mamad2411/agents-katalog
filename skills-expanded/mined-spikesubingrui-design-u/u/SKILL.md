---
name: u
version: 1.3.0
homepage: https://github.com/spikesubingrui-design/u
clawhub_slug: u
description: >-
  把 Obsidian 变成 OpenClaw memory + gbrain 知识图谱的可视化 GUI：单 vault、wikilink 图谱、
  memory 日记软链、DB 页面物化导出，编辑仍回灌 sync/embed；可选升华候选队列把日记里反复出现的
  话题提议成图谱页面；v1.2 附策展宪法（给写图谱的 agent 的系统提示词：收录三问／分类 rubric／
  页面密度标准／重铸模板／问答回流）；v1.3 附检索流水线（关键词+向量双引擎 RRF 融合／时间衰减／
  MMR 去冗／一跳图扩展，配评测集把召回从 0/10 修到 10/10）。触发词：obsidian脑库 / 第二大脑可视化 /
  gbrain obsidian / memory图谱 / 连点成面 / second brain vault / 知识策展 / 图谱堆积 / 召回 /
  检索融合 / RRF
metadata:
  openclaw:
    emoji: "💎"
---

# U ——「你」的记忆，终于看得见

> **问题**：OpenClaw 的 `memory_search` 和 gbrain 的 Postgres 图谱对 agent 可见，对人不可见。  
> **解法**：Obsidian 打开 gbrain wiki 作 vault，软链 `memory/` 日记进来，可选 `gbrain export` 把 DB 页面物化成 markdown——**一套文件，三路索引**。

## 何时加载本 Skill

- 用户要把 Obsidian 和 OpenClaw memory / gbrain 打通
- 用户说「第二大脑可视化」「memory 图谱」「连点成面」「想在 Obsidian 里看 agent 写的记忆」
- 用户已有 gbrain + `~/wiki`（或同类 markdown 脑库），要加 GUI

## 架构（一图流）

```
OpenClaw workspace/memory/*.md  ──symlink──►  ~/wiki/memory/     ◄── Obsidian 浏览
gbrain Postgres (426+ pages)   ──export──►  ~/wiki/**/*.md       ◄── Obsidian 图谱
Agent cron                     ──sync────►  Postgres + vectors   ◄── 后台不变
```

**安全约束（必须遵守）**：
- `memory` 必须在 `~/wiki/.gitignore` 里 → gbrain `sync` 是 git-diff 驱动，不会把日记重复入库
- `.obsidian/` 被 gbrain `isSyncable` 跳过（隐藏目录）
- 不要改 `alwaysUpdateLinks: true`，避免 Obsidian 批量重写 gbrain 的 `[[路径式]]` 链接

## Phase 0 — 确认路径

| 变量 | 默认 | 说明 |
|------|------|------|
| `WIKI_DIR` | `~/wiki` | gbrain git 仓库根 |
| `MEMORY_DIR` | `~/.openclaw/workspace/memory` | OpenClaw 日记 MD |
| `GBRAIN_BIN` | `gbrain` | CLI 在 PATH |

## Phase 1 — 一键搭建（推荐）

```bash
bash skills/u/scripts/setup-vault.sh
# 或指定路径：
WIKI_DIR=~/wiki MEMORY_DIR=~/.openclaw/workspace/memory bash scripts/setup-vault.sh
```

脚本会：创建 `memory` 软链、写入 `.gitignore`、预置 `.obsidian/app.json`（wikilink + absolute + 不自动改链）。

## Phase 2 — 物化 DB 页面（可选但强烈推荐）

若 Postgres 里页面多于磁盘 `.md`（常见于 MCP `put_page` 只写 DB）：

```bash
gbrain export --dir "$WIKI_DIR"
cd "$WIKI_DIR" && git add -A && git commit -m "materialize gbrain pages for Obsidian"
```

物化后 Obsidian 图谱 wikilink 解析率通常从 ~28% 升到 **84%**（README 同口径）。

## Phase 3 — 打开 Obsidian

1. Obsidian → **Open folder as vault** → 选 `WIKI_DIR`
2. 左侧 **Graph view**：看 people / projects / concepts / synthesis 簇
3. 打开 `memory/2026-MM-DD.md` → 右栏 **Backlinks → Unlinked mentions** 跳到引用该日记的 gbrain 页面

## Phase 4 — 验证清单

- [ ] `ls -la $WIKI_DIR/memory` 显示 symlink
- [ ] `cd $WIKI_DIR && git status` **不**出现 `memory/*.md`
- [ ] 图谱中有连线（说明 `[[projects/foo]]` 被解析）
- [ ] 编辑任意 gbrain 页面保存后 `git status` 有改动（cron 会 sync+embed）

## Phase 5 — 连点成面：升华候选（可选，v1.1）

图谱可见之后下一个问题：日记里反复提到的话题，怎么变成图谱页面？两种坏做法都见过——
agent 自己判断该记就直接写页面（错了没人把关，一直留在图里）；或者干脆没人写（图谱
永远比日记落后）。`distill-candidates.py` 走中间路线：**只提议，不下笔**。

```bash
python3 skills/u/scripts/distill-candidates.py --dry-run
```

跑起来后扫 `MEMORY_DIR` 里近 14 天的日记，对照 `WIKI_DIRS`（默认
`people,companies,projects,concepts`）里已有页面的 title/aliases 建词表，找「跨 ≥2 天
反复出现」的话题，写一份 `distill-inbox.md` 到 vault 根：A 区是已有页面没跟上的，B 区是
反复出现但还没页面的候选。**不加 `--dry-run` 才会真的落盘**；即便落盘也只写
`distill-inbox.md` 和 `.distill_heartbeat.json` 两个文件，从不碰 `memory/` 或任何图谱页面。

接受某条候选后，是你（或让 agent）去更新/新建那个页面——这一步刻意留给人，跳过它才是
自动记忆系统最容易埋雷的地方。

可选接进 cron，让队列每天自动刷新（仍然只提议）：

```bash
# OpenClaw
openclaw cron create --no-agent --script skills/u/scripts/distill-candidates.py "0 3 * * *"
```

## Phase 6 — 策展宪法：有用的图谱，不是好看的堆积（v1.2）

队列（Phase 5）解决「谁来把关」，还剩「按什么标准写」。放着不管，vault 的第二种死法是：
页面越攒越多、个个看着完整，但没有一页会在未来某次真实提问时被命中——看似完美的知识点堆积。

`references/knowledge-curation.md` 是一份**给写图谱的 agent 的系统提示词**，建/改/分类
任何页面前先读它。核心判据一句话：**一页知识有用，当且仅当它会被未来的真实提问命中并接住。**

- **收录三问**（任一为否不建页）：改变行动吗？会被再问吗？胜过模型自带知识吗？
- **分类 rubric**：每个目录一条判据 + 正反例，治「agent 分类不准」
- **密度标准**：重写优先于追加；头三行定生死；每页必带「本页要能回答」小节（2–5 个真实问题）
- **⭐ 问答回流**：agent 综合出好答案时在日记记一行 `⭐page-candidate: <拟题>`（中文
  `⭐候选页:` 亦可），v1.2 的 distill-candidates.py 会把它提进队列 B 区置顶；建页后把 ⭐
  改成 ✅ 即不再上榜。**禁止绕过队列直接建页。**
- **D 区重铸候选**：脚本自动扫出「贴满更新膏药」的增生页，接受后按宪法 §5 模板熔铸成
  稠密单篇（验收：短 30%+ 且信息零丢失）
- 进阶（需自己接线，宪法 §6 有做法）：检索日志 miss→建页信号、45 天零命中→退役提案、
  每月矛盾体检

把宪法接进你的 agent 指令（AGENTS.md / CLAUDE.md）只需一行：

```markdown
建/改 wiki 页前先读 skills/u/references/knowledge-curation.md（收录三问+rubric+密度标准）；重写优先于追加。
```

## Phase 7 — 检索流水线：从"两路合并"到真正召回（v1.3）

策展宪法解决"写什么"，还有一半没解决："查得到吗"。实测过：把 `memory_search`
（关键词）和 `gbrain query`（向量）朴素合并、按分数排序、切 top20——对真实提问
（"XX是谁"这类完整问句）**10 条测试用例 0 条命中，MRR 为 0**。根因：向量引擎对
多词中文/疑问句直接返回零结果，即使同一实体用单个词查询能到 0.7+ 分。

`scripts/recall.mjs` 重写为六步流水线，同一评测集从 0/10 做到 10/10（MRR 0→0.75）：

1. **查询归一化**——原句 + 剥疑问词核心句 + 从你自己 wiki 的 title/aliases 建的
   实体表抽实义词 + CJK 前缀 n-gram
2. **双引擎分工**——关键词引擎慢，只发原句+2个实义词；向量引擎快，发全部变体
3. **RRF 融合**（k=60）——不同引擎的分数不可比，但排名可比，免归一化
4. **时间衰减 + 频次**——按内容类别设半衰期，下限 0.5 防止强命中被埋没
5. **MMR 去冗**（λ=0.7）——避免 top-K 塞满近重复片段
6. **一跳图扩展**——命中页的出链页顺带打折带出

```bash
bun scripts/recall.mjs "<query或完整问句>"
```

**配套评测工具** `scripts/recall-eval.mjs`——"感觉变准了"不是结论，跑一遍数字
才是。从 `ops/recall-eval.example.jsonl`（虚构样例）起步，换成你自己的真实问题：

```bash
bun scripts/recall-eval.mjs --eval ops/recall-eval.jsonl
```

**改 `recall.mjs` 任何参数前，先跑一遍评测集，别凭感觉。** 完整设计动机、每步
"为什么"见 `references/retrieval-pipeline.md`。

可选：定期跑评测集的健康检查 cron，通过率跌破阈值才告警、全绿静默——防
embedding 过期、引擎挂掉、参数改坏这类不会自己吱声的静默退化。

## Agent 写入纪律（与 AGENTS.md 记忆桥接一致）

用户在 Obsidian 手改 markdown 后：
- gbrain 侧：link-maintenance / auto-ingest cron 会 `sync --no-embed` + `embed --stale`
- memory 侧：仍在 `workspace/memory/`，由 `memory_search` 索引，**不要**把 memory 提交进 wiki git

## 故障排除

| 症状 | 处理 |
|------|------|
| 图谱很空、大量悬空链接 | 跑 `gbrain export --dir $WIKI_DIR` |
| memory 在 git 里出现 | 确认 `.gitignore` 含 `memory` |
| Obsidian 把链接改成 `[text](path)` | 检查 `useMarkdownLinks: false` |
| `[[Naval Ravikant]]` 不解析 | 显示名链接；给目标页加 frontmatter `aliases` |

## 相关

- `skills/brain-ops` — gbrain 写入规范
- `skills/memory-setup-openclaw` — memory_search 配置
- `skills/planning-with-files` — 长任务落盘到 memory

详细架构与 mermaid 图见 `references/architecture.md`。
