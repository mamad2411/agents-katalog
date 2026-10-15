---
name: hook-lab
description: "Use when the user gives a TikTok/Instagram Reels/YouTube Shorts URL (or runs /analyze <url>) and wants to know why the video works — extracts metadata and transcript, then breaks down hook, script structure, style tags, viral factors, and rewrite angles for Chinese platforms."
---

# /analyze — 短视频内容拆解

## Input

`$ARGUMENTS` = 一个视频 URL（TikTok / Instagram Reels / YouTube Shorts）。

如果用户没有提供 URL，问他要。

## Step 1: Extract

运行提取脚本：

```bash
python3 ~/.claude/skills/hook-lab/scripts/analyze-video.py "$ARGUMENTS"
```

脚本返回 JSON，包含：
- `platform`: tiktok / instagram / youtube
- `metadata`: 标题、描述、作者、播放量、点赞、评论、时长等
- `transcript`: 视频字幕/转写文本（可能为 null）

### 提取失败的回退策略

如果 `metadata._error` 存在，按以下顺序尝试回退：

**回退 1 — WebFetch**：
用 WebFetch 工具访问视频 URL，prompt 设为：
> "Extract all video metadata: title, description, author name, author handle, view count, like count, comment count, share count, duration, and any transcript/caption text visible on the page."

**回退 2 — 用户提供信息**：
如果 WebFetch 也拿不到数据，请用户提供：
- 视频的文案/字幕文本（可以从视频里手动复制）
- 基本数据（播放量、点赞数等，截图也行）

拿到任何数据后继续分析，在输出开头注明数据来源和完整度。

## Step 2: Analyze

基于提取到的数据，进行以下分析。用中文输出。

### 2.1 基础数据面板

用表格展示关键指标：平台、作者、时长、播放量、点赞、评论、转发。
计算互动率 = (like + comment) / view。

### 2.2 Hook 分析（前 3 秒）

从 transcript 的前 1-3 句提取 hook 文案，分析：
- **Hook 类型**: curiosity gap / shocking stat / bold claim / question / visual hook / pattern interrupt
- **Hook 强度判断**: 为什么能让人停下来
- **可优化空间**: 如果 hook 不够强，给出改写建议

如果没有 transcript，从 description 和 title 推断 hook 策略。

### 2.3 脚本结构拆解

将 transcript 按叙事结构分段：

| 段落 | 时间估算 | 内容 | 作用 |
|------|----------|------|------|

典型结构：Hook → Problem/Context → Solution/Reveal → Proof/Example → CTA

分析脚本节奏：信息密度是否合理、转折点在哪、哪里容易流失观众。

### 2.4 风格与格式标签

给视频打标签（多选）：
- **呈现方式**: talking head / voiceover / text-on-screen / skit / montage / screencast / interview
- **内容类型**: educational / entertainment / storytelling / review / tutorial / hot-take / news
- **情绪基调**: 紧迫 / 好奇 / 幽默 / 震惊 / 共鸣 / 权威

### 2.5 为什么这条视频能爆

综合分析 2-3 个核心原因。要具体，不要泛泛而谈。
比如不要说「因为内容好」，要说「开头用了具体数字制造反差（$0 → $10K），3 秒内给出明确价值承诺」。

### 2.6 可借鉴的改写方向

给出 3 个具体的改写角度，每个包含：
- **角度**: 一句话概述
- **Hook 示例**: 写出改写后的 hook 文案
- **适合平台**: TikTok / Instagram / 小红书 / 视频号

改写方向要考虑中文创作者的场景。

## Step 3: Output

按上面 2.1-2.6 的顺序输出完整分析。格式用 markdown 表格和分段标题，清晰可读。

最后附一行：
> 数据来源：yt-dlp 提取 | 分析模型：Claude

## Step 4: 记录到结果库

分析完成后，往 `~/.claude/skills/hook-lab/results/analyzed-videos.md` 追加一条记录（直接 Append，不要覆盖已有内容），格式：

```markdown
## [YYYY-MM-DD] 作者 — 标题/主题 (平台)

- URL: <原始链接>
- 数据: 播放 X / 赞 X / 评论 X / 转发 X
- Hook 类型: ...
- 为什么能爆: 一句话核心结论
- 可借鉴方向: 一句话核心结论

---
```

这个文件是跨视频对比的素材库——后续如果用户要"把分析过的几条放一起找规律"，直接读这个文件，不用重新跑提取。

## Notes

- 如果没有 transcript，在输出开头注明「未能提取字幕，以下分析基于元数据和描述文本」，分析照做但标注信息置信度较低
- 不要编造数据，metadata 里没有的指标标注「N/A」
- 互动率计算如果缺少 view_count 就跳过
- 全程用中文输出，技术术语保留英文（hook、CTA、talking head 等）
