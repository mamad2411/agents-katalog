---
description: 给所有 Claude Code session 跑 DeepSeek 提取「一句话摘要 + 3-5 个标签」,结果写 /tmp/mirror/summaries.json。mirror viewer 自动展示。默认增量(只跑没摘要的),传 --all 全量重跑。Use when Daisy types /summarize-sessions 或问"总结 session / 给 session 加摘要 / 给 session 加标签"。
when_to_use: Triggered by /summarize-sessions, "总结 session", "给 session 加摘要 / 标签", "看看每个 session 干了啥". Skip 如果她已经知道哪个 session 是哪个。
disable-model-invocation: false
allowed-tools: Read Bash(python3:*)
arguments: mode
---

# Summarize-Sessions — 给所有 session 加摘要 + 标签

跑 DeepSeek 读完整 session,输出:
- `summary`: 一句话(<= 50 字)说明 session 讨论了什么、落到什么结论
- `tags`: 3-5 个关键词标签(短词)

结果累积到 `/tmp/mirror/summaries.json`,mirror viewer index 表自动读取展示。

## 触发后的动作

### 1. 解析参数

- `$ARGUMENTS` = `--all` → 全量重跑(包括已有摘要的)
- `$ARGUMENTS` 空 → 增量(只跑还没摘要的)
- `$ARGUMENTS` = `--sid <session-id>` → 只跑指定 session

### 2. 跑主脚本

直接执行:

```bash
python3 ~/.claude/skills/summarize-sessions/summarize.py $ARGUMENTS
```

主脚本自给自足:
- 自动找 DeepSeek key(env DEEPSEEK_API_KEY → ~/.deepseek)
- 读 `~/.claude/mirror/search-index.json` 拿每个 session 的 msgs
- 读 `~/.claude/mirror/summaries.json` 看已有(增量模式跳过)
- 对每个待处理 session 调 DeepSeek API,提取 summary + tags
- 累积写回 `/tmp/mirror/summaries.json`
- 跑完触发 `python3 /tmp/jsonl2html.py --all /tmp/mirror` 重新渲染

### 3. 报告进度

跑完后给 Daisy 报:
- 处理了 N 个 session
- 跳过 M 个(已有摘要)
- 失败 K 个(列 sid)
- 总耗时 / 估计花费

### 4. 一致性约束

- **绝不在新文件里写 key**(memory `feedback_warn_before_pasting_secrets.md`)
- 失败的 session 不阻塞已成功的(每条独立写盘)
- LLM 输出必须是合法 JSON,不合法重试 1 次后放弃
- 增量是默认,Daisy 不主动说 `--all` 就别全量重跑(浪费 token)

## 成本预算

- 一次 backfill 28 个 session ≈ ¥0.4
- 单 session 增量 ≈ ¥0.015
- 一年 1000 session ≈ ¥15

## 失败 fallback

- DeepSeek API 挂了:报错,不污染已有 summaries
- key 找不到:报错让 Daisy 手动 `export DEEPSEEK_API_KEY=xxx` 再跑
- search-index.json 不存在:让 Daisy 先跑 `python3 /tmp/jsonl2html.py --all /tmp/mirror` 生成
