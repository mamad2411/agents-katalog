---
name: youtube-ai-digest
description: 浏览关注频道的 AI 相关 YouTube 视频，获取字幕，用 Claude 生成中文摘要，输出 Markdown 日报。当用户说"找 AI 视频"、"看看最近有什么 AI 新闻"、"YouTube 上有什么 AI 相关视频"、"帮我整理 AI 视频"、"今天有什么 AI 内容"、"AI 视频摘要"、"youtube ai digest"、"summarize youtube"、"AI 播客"等，都应该触发此 skill。也适用于用户想了解最新 AI 动态但没有指定来源的情况。
---

# YouTube AI Digest

浏览关注频道的 AI 相关 YouTube 视频，获取字幕，用 Claude 生成中文摘要，输出 Markdown 日报。

## 快速开始

Skill 根目录：`~/.claude/skills/youtube-ai-digest/`

### 标准工作流（推荐）

```bash
# 第一步：获取最近 3 天的 AI 相关视频
cd ~/.claude/skills/youtube-ai-digest
python scripts/fetch_videos.py --days 3

# 第二步：展示列表，让用户选择感兴趣的视频（编号选择）

# 第三步（单视频）：获取字幕并由 Claude 生成摘要
python scripts/get_transcript.py --video-id VIDEO_ID
# 然后读取字幕文件，Claude 对内容做中文总结

# 第三步（批量日报）：批量处理所有视频
python scripts/digest_all.py --days 3 --limit 10
# 然后读取生成的日报文件，Claude 对每段字幕生成中文摘要
```

## Claude 的 AI 摘要职责

**当获取到字幕内容后，Claude 应主动完成以下工作，无需用户再次指示：**

1. 阅读字幕全文（或 digest_all.py 生成的日报文件）
2. 对每个视频用中文输出：
   - **核心观点**（2-3 句话，直接说结论）
   - **关键要点**（3-5 条 bullet，具体内容而非泛泛描述）
   - **值得关注的原因**（为什么这个视频重要）
3. 如果字幕质量差或内容重复，如实告知用户

摘要风格：简洁、有信息量，避免"视频介绍了……"这类废话式开头，直接给出内容。

## 配置频道

编辑 `~/.claude/skills/youtube-ai-digest/data/channels.json`：

```json
{
  "channels": [
    {"name": "Two Minute Papers", "id": "UCbfYPyITQ-7l4upoX8nvctg"},
    {"name": "Yannic Kilcher", "id": "UCZHmQk67mN31gbHey6BVyNw"},
    {"name": "AI Explained", "id": "UCNJ1Ymd5yFuUPtn21xtRbbw"}
  ]
}
```

## Scripts 说明

### fetch_videos.py
获取关注频道最近 N 天的 AI 相关视频（**已修复时间过滤**，使用 `--dateafter`）

```bash
python scripts/fetch_videos.py --days 3          # 最近 3 天
python scripts/fetch_videos.py --days 7          # 最近 7 天
python scripts/fetch_videos.py --days 3 --all    # 不过滤，返回所有视频
python scripts/fetch_videos.py --keyword "GPT"   # 自定义关键词
```

输出：`data/videos.json`（含上传日期、时长、频道等元信息）

### get_transcript.py
获取单个视频的字幕

```bash
python scripts/get_transcript.py --video-id VIDEO_ID
```

输出：`data/transcript_VIDEO_ID.txt`（带时间戳）和 `.json`

### digest_all.py（新增）
批量处理所有视频，生成带字幕的日报 Markdown，**Claude 读取后完成摘要填写**

```bash
python scripts/digest_all.py --days 3            # 处理最近 3 天，最多 10 个
python scripts/digest_all.py --days 7 --limit 5  # 只处理 5 个
python scripts/digest_all.py --no-transcript     # 只生成列表，不获取字幕
```

输出：`data/output/ai_digest_YYYYMMDD.md`

### generate_report.py
生成单个视频的详细报告（含封面图下载）

```bash
python scripts/generate_report.py --video-id VIDEO_ID --output ~/reports/
```

## Output Format（日报）

```markdown
# AI 视频日报 2026-03-22

> 最近 3 天，共 8 个 AI 相关视频

---

## 1. [视频标题]

- **频道**: Two Minute Papers
- **日期**: 2026-03-21
- **链接**: https://youtube.com/watch?v=...

### 内容摘要（Claude 填写）

NVIDIA 的新模型在自动驾驶感知任务上取得突破，核心是……

**关键要点：**
- 使用了 X 架构，解决了 Y 问题
- 在 Z 数据集上超越 SOTA 15%
- 实际部署挑战在于……

**值得关注：** 这是首次在……
```

## 常见使用场景

| 用户说 | Claude 应该做 |
|--------|--------------|
| "找最近 AI 视频" | fetch_videos.py --days 3，列出结果 |
| "帮我整理成日报" | digest_all.py，然后读文件生成摘要 |
| "总结第 3 个视频" | get_transcript.py 获取字幕，Claude 总结 |
| "最近 Anthropic 相关的" | fetch_videos.py --keyword "anthropic" |
