---
name: vibe-story
description: 将 Claude Code 的多个开发会话提取为时间线骨架，并生成公众号长文。当用户想把 Vibe Coding 过程写成开发分享、技术文章、公众号推文时使用此 Skill。触发词包括：开发分享、写文章、总结开发过程、vibe coding 记录、会话总结、生成推文等。
---

# Vibe Story Skill

将 Claude Code 跨多个会话的开发过程，提取为可读的时间线骨架，再生成适合公众号发布的长文。

> **适用范围**：提取层只认 Claude Code 的会话日志（`~/.claude/projects/<hash>/*.jsonl`）。
> Codex（`~/.codex/sessions/`）等其他 agent 的日志路径与格式都不同，当前**不支持**。
> 若在非 Claude Code 环境被触发，应如实告知用户暂不支持，不要硬跑（会提取出 0 条）。

## 工作流程

```
用户触发（命令后常带需求，如「写一篇 6/10 的支付功能复盘」）
  ↓
解析意图：目标项目 / 时间范围 / 主题聚焦点
  ↓
Step 1: 运行 scripts/extract_sessions.py 列出项目，确定目标
  ↓
Step 2: 提取对话骨架（过滤工具调用，只保留对话文字）
  ↓
Step 3: 输出骨架供用户确认
  ↓
Step 4: 由 Claude 依据骨架直接撰写公众号长文
  ↓
Step 5: 输出文章，告知文件路径
```

## Step 0：选择运行时（提取脚本同时提供 Python 与 Node 两个版本）

提取逻辑有两份等价实现，输出**逐字节一致**：`scripts/extract_sessions.py` 和 `scripts/extract_sessions.js`。
有谁用谁，按以下优先级探测，把结果存进 `$RUNNER` 供后续步骤复用：

```bash
SKILL_DIR=<本 skill 目录>     # 例如 ~/.claude/skills/vibe-story
if command -v python3 >/dev/null 2>&1; then
  RUNNER="python3 $SKILL_DIR/scripts/extract_sessions.py"
elif command -v node >/dev/null 2>&1; then
  RUNNER="node $SKILL_DIR/scripts/extract_sessions.js"
else
  RUNNER=""   # 两者都没有 → 见文末"降级方案"，由 Claude 直接解析 .jsonl
fi
```

两个脚本的参数完全相同（`--list / --project / --since / --output / --max-chars`）。

## 解析用户意图（动手前先做）

用户常把需求写在命令后面，例如 `/vibe-story 写一篇 6 月 10 日的支付功能复盘`。
开工前先从中抽出三件事，后续步骤据此执行：

- **目标项目**：未指明则用 Step 1 的自动匹配（命中当前工作目录）或让用户选。
- **时间范围**：如「今天 / 昨天 / 6 月 10 日 / 最近一周 / 6 月 10–12 日」。换算成 Step 2 的
  `--since`（取一个不晚于目标范围起点的值即可，`--since` 只控制起点）；范围**之外**的会话，
  在 Step 3 或撰文时再精确剔除——这样既不漏也不多。
- **主题 / 聚焦点**：如「支付功能」「那个登录 bug」。记下来，**Step 4 撰文时只挑与之相关的内容**，
  自动略过无关会话；不要把整段时间里所有事都写进去。

用户没给这些信息时，按默认流程走，并在 Step 3 与用户确认时间范围、主题、标题偏好。

## Step 1：确定目标项目

运行列表命令：

```bash
$RUNNER --list
```

输出格式示例：
```
  #    最近活跃               会话数  项目路径
  1    2025-06-08 14:32       12      /Users/duer/projects/dizhu
  2    2025-06-07 09:11        3      /Users/duer/projects/other
```

**自动匹配**：如果列表中有 path_hint 包含当前工作目录（`pwd`）的项目，直接使用，无需用户选择。否则展示列表，请用户输入序号。

## Step 2：提取骨架

**产物落在目标项目目录里**（而非 `/tmp`，避免被系统清理、也便于和项目一起留存）。
约定输出到 `<目标项目路径>/vibe-story/` 子目录——`<目标项目路径>` 即 Step 1 列表里的 path_hint。
若该目录在 git 仓库内，提醒用户可按需把 `vibe-story/` 加进 `.gitignore`。

`--since` 取自"解析用户意图"得到的时间范围（如"最近一周"→ `7d`，"6 月 10 日起"→ `2025-06-10`）；
用户没指定时间就省略，默认全部。

```bash
PROJ=<目标项目路径>            # 例如 /Users/you/projects/dizhu
mkdir -p "$PROJ/vibe-story"
$RUNNER \
  --project <序号或hash> \
  [--since <按用户意图>] \
  --output "$PROJ/vibe-story/skeleton.md"
```

提取完成后告知用户：提取了多少条消息、覆盖多少个会话、时间跨度。

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--since` | 限制时间范围 | `7d` / `30d` / `2025-01-01` |
| `--project` | 项目序号或 hash | `1` 或 `a3f2b1c0` |
| `--max-chars` | 单条消息最大字符数，0=不截断（默认）。仅在骨架过大需精简预览时设置 | `300` |

## Step 3：展示骨架摘要

将骨架内容按会话分组，每个会话展示前 3 条消息作为预览，询问用户：
- 时间范围是否正确？
- 是否需要排除某些会话？
- 文章标题有无偏好？

## Step 4：生成文章

**首选方式（推荐）**：在当前 Claude Code 会话内，由 Claude 直接撰写文章——
Claude 就在现场，能完整读骨架、能回读原始 `.jsonl` 补关键细节、能和用户来回改稿，
质量最高且无需任何 API key。

撰写前先读 `references/article-style.md`（文章风格的唯一事实源），按其要求写作，
写入 `<目标项目路径>/vibe-story/article.md`（与骨架同目录）。

**按主题筛选**：若"解析用户意图"得到了聚焦点（如"支付功能""那个登录 bug"），
撰文时**只挑与之相关的会话内容**，把同一时间段里的无关支线略过；用户没给主题就完整还原。
若指定的具体日期/范围比 `--since` 拉取的更窄，也在此按目标范围收口。

> 提示：骨架默认不截断，最终的分析报告/交付物通常就在最长的几条消息里——
> 那往往是文章最有料的部分，别漏掉。

**可选回退**：仅当需要脱离会话、用脚本批量生成时使用（需先 `export ANTHROPIC_API_KEY=...`）。
该脚本同样读取 `references/article-style.md`，风格与首选方式一致：

```bash
python {SKILL_DIR}/scripts/generate_article.py \
  --skeleton "$PROJ/vibe-story/skeleton.md" \
  [--title "用户提供的标题"] \
  --output "$PROJ/vibe-story/article.md"
```

## Step 5：输出结果

展示完整文章内容，并告知：
- 骨架文件：`<目标项目路径>/vibe-story/skeleton.md`
- 文章文件：`<目标项目路径>/vibe-story/article.md`

询问用户是否需要调整风格或重新生成。

---

## 既没有 Python 也没有 Node 时的降级方案

提取脚本只是为了"省事"，并非不可替代。骨架的真正数据源就是
`~/.claude/projects/<项目hash>/*.jsonl` 这些纯文本文件，Claude 完全能自己读懂。

若 Step 0 探测下来 `$RUNNER` 为空（两种运行时都没有）：
1. **首选**：Claude 直接读取项目目录下的 `.jsonl`，自行筛选 `type` 为 `user`/`assistant`、
   跳过 `isSidechain`/`isMeta` 的记录，从 `message.content` 取文字，按 `timestamp` 排序，
   手工拼出与脚本等价的骨架。逻辑见 `extract_sessions.py` 的 `extract_from_jsonl`（JS 版同名函数）。
2. Step 4（撰文）本就由 Claude 完成，**完全不需要任何运行时**。

也就是说：**Python、Node 都没有，这个 skill 依然能跑通**，只是提取那一步从"跑脚本"
变成"Claude 手动解析"。脚本在则用脚本（更快更稳），都不在则降级。

## 路径说明

`{SKILL_DIR}` 指本 Skill 所在目录。执行脚本前，先用 `find` 或已知路径定位 `scripts/` 目录：

```bash
# 常见安装位置
~/.claude/skills/vibe-story/scripts/
/path/to/skill/vibe-story/scripts/
```

## 注意事项

- 提取脚本有 Python 与 Node 两版，均零依赖（Python 3.10+ / Node 16+），有谁用谁（见 Step 0）
- 两版输出逐字节一致；改提取逻辑时**两个文件都要同步改**
- Windows 路径：`%APPDATA%\Claude\projects\`，Mac/Linux：`~/.claude/projects/`
- 会话超过 50 个时建议加 `--since 30d`
- 首选由 Claude 在会话内直接撰写文章（Step 4），无需配置 key
- `generate_article.py` 仅作脱离会话的回退方案，需设置 `ANTHROPIC_API_KEY` 环境变量
