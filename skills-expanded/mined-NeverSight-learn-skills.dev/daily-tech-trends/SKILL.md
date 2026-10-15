---
name: daily-tech-trends
description: Automatically scan 8+ tech news sources (Hacker News, GitHub Trending, Product Hunt, 36Kr, etc.) to capture daily trending topics. Supports custom themes (tech, AI, startup). Perfect for content creators who need to catch hot topics quickly. Use when user wants to "check today's trends", "scan tech news", or "find hot topics".
---

# Daily Tech Trends - 每日科技热点

Automatically scan multiple tech news sources to capture trending topics. Built for Kevin's "Build fast, share fast" workflow.

## When to Use

Use this skill when:
- User wants to check today's trending topics
- User mentions: "今日热点", "科技新闻", "扫描热点", "check trends"
- User wants to find content inspiration for tweets/articles
- Morning routine: scan news before creating content

**Auto-trigger scenarios:**
- User says: "今天有什么热点"
- User says: "扫描科技新闻"
- User says: "check tech trends"

## Core Philosophy

Aligned with Kevin's core abilities:
- **捕捉热点** - 3秒钟出创意的基础
- **Build fast, share fast** - 快速获取灵感
- **病毒式传播** - 追热点是最快的涨粉方式

> "ADHD创意爆发：3秒钟出创意，快速捕捉热点" - Kevin's superpower

---

## Information Sources

### English Sources (5)
1. **Hacker News** - Tech community discussions
2. **GitHub Trending** - Popular open source projects
3. **Product Hunt** - New product launches
4. **Reddit r/technology** - Tech discussions
5. **TechCrunch** - Tech news and analysis

### Chinese Sources (3)
6. **36氪** - Chinese tech news
7. **少数派** - Digital lifestyle
8. **V2EX** - Chinese tech community

---

## Features

### 1. Multi-Source Scanning
- Automatically scan 8+ sources in parallel
- Extract top 5-10 items from each source
- Deduplicate and merge results

### 2. AI Analysis
- Categorize topics (AI, Tech, Startup, Dev Tools, etc.)
- Extract keywords
- Evaluate hotness (upvotes, comments, shares)
- Generate summaries

### 3. Custom Themes
- Filter by theme: AI, Tech, Startup, Dev Tools
- Configurable in `config/sources.json`
- Easy to add new themes

### 4. Obsidian Integration
- Save to: `D:\obsidian\AI_kevin工作区\记忆库\每日热点\`
- Format: `YYYY-MM-DD_科技热点.md`
- Include: title, link, source, category, summary

### 5. Tweet Generation (Optional)
- Integrate with `personal-tweet-generator`
- Generate tweets based on trending topics
- One-click copy to clipboard

---

## Usage

### Quick Scan (Default)
```
扫描今日热点
```

**Output:**
- Console: Top 10 trending topics
- Obsidian: Full report saved
- Screenshots: Evidence saved to `tmp/`

---

### Scan with Theme Filter
```
扫描今日 AI 热点
```

**Output:**
- Only AI-related topics
- Filtered and ranked by relevance

---

### Scan and Generate Tweets
```
扫描热点并生成推文
```

**Output:**
- Trending topics report
- 3 tweet drafts based on top topics
- Ready to copy and post

---

## Output Format

### Console Output
```
🔥 今日科技热点 (2026-01-23)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📰 Hacker News (5 条)
  1. [AI] Ghostty's AI Policy
     https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
     176 points | 89 comments

  2. [Tech] Replacing Protobuf with Rust to go 5 times faster
     https://pgdog.dev/blog/replace-protobuf-with-rust
     67 points | 39 comments

📰 GitHub Trending (5 条)
  1. [AI] microsoft/VibeVoice
     https://github.com/microsoft/VibeVoice
     ⭐ 2.3k stars today

  2. [Dev Tools] browser-use/browser-use
     https://github.com/browser-use/browser-use
     ⭐ 1.8k stars today

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 共扫描到 25 条热点
📁 报告已保存到: D:\obsidian\AI_kevin工作区\记忆库\每日热点\2026-01-23_科技热点.md
```

### Obsidian Output
```markdown
---
title: 2026-01-23 科技热点
date: 2026-01-23
type: daily_trends
sources: [hackernews, github, producthunt, 36kr, reddit, techcrunch, sspai, v2ex]
total_items: 25
categories: [AI, Tech, Startup, Dev Tools]
---

# 2026-01-23 科技热点

> 今日共扫描 8 个信息源，发现 25 条热点

## 🔥 Top 10 热点

### 1. Ghostty's AI Policy
**来源:** Hacker News | **分类:** AI | **热度:** ⭐⭐⭐⭐⭐
**链接:** https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
**摘要:** Ghostty 发布了 AI 使用政策，明确了 AI 在项目中的使用边界...

### 2. microsoft/VibeVoice
**来源:** GitHub Trending | **分类:** AI | **热度:** ⭐⭐⭐⭐⭐
**链接:** https://github.com/microsoft/VibeVoice
**摘要:** 微软开源的语音合成项目，今日获得 2.3k stars...

...

## 📊 分类统计

- AI: 8 条
- Tech: 7 条
- Startup: 5 条
- Dev Tools: 5 条

## 💡 推文灵感

基于今日热点，可以创作以下主题的推文：
1. Ghostty 的 AI 政策对开源项目的启示
2. 微软 VibeVoice 的技术亮点
3. Rust 替换 Protobuf 的性能提升案例

---

*本报告由 daily-tech-trends skill 自动生成*
*扫描时间: 2026-01-23 09:00*
```

---

## Technical Implementation

### Architecture
```
User Request
    ↓
SKILL.md (trigger detection)
    ↓
scripts/scan_trends.ts (parallel scanning)
    ↓
scripts/analyze_trends.ts (AI analysis)
    ↓
scripts/save_to_obsidian.ts (save report)
    ↓
Output (console + Obsidian + screenshots)
```

### Key Scripts

**1. scan_trends.ts**
- Use Dev Browser to visit each source
- Extract titles, links, metadata
- Handle rate limiting and errors
- Return structured data

**2. analyze_trends.ts**
- Categorize topics using AI
- Extract keywords
- Evaluate hotness
- Generate summaries
- Filter by theme (if specified)

**3. save_to_obsidian.ts**
- Format data as Markdown
- Save to Obsidian vault
- Create backlinks
- Update index

### Configuration

**config/sources.json**
```json
{
  "sources": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/",
      "selector": ".titleline > a",
      "limit": 10,
      "enabled": true
    },
    {
      "name": "GitHub Trending",
      "url": "https://github.com/trending",
      "selector": "h2.h3 a",
      "limit": 10,
      "enabled": true
    },
    ...
  ],
  "themes": {
    "AI": ["ai", "machine learning", "llm", "gpt", "claude", "openai"],
    "Tech": ["tech", "technology", "software", "hardware"],
    "Startup": ["startup", "funding", "vc", "entrepreneur"],
    "Dev Tools": ["developer", "tool", "framework", "library"]
  }
}
```

---

## Scheduled Task

### Windows Task Scheduler

**Daily at 9:00 AM:**
```cmd
schtasks /create /tn "每日科技热点扫描" /tr "cd ~/.claude/skills/daily-tech-trends && npm run scan" /sc daily /st 09:00
```

**Manual trigger:**
```bash
cd ~/.claude/skills/daily-tech-trends
npm run scan
```

---

## Integration with Other Skills

### With personal-tweet-generator
```
1. Scan trends
2. Select top 3 topics
3. Generate tweets using personal-tweet-generator
4. Preview with tweet-previewer
5. Copy and post
```

### With conversation-saver
```
1. Scan trends
2. Save conversation about trends
3. Build knowledge base
```

---

## Error Handling

### Network Errors
- Retry with exponential backoff
- Skip failed sources
- Continue with available data

### Rate Limiting
- Respect robots.txt
- Add delays between requests
- Use caching when possible

### Parsing Errors
- Log errors for debugging
- Use fallback selectors
- Notify user of issues

---

## Performance

**Scan Time:**
- 8 sources in parallel: ~10-15 seconds
- Sequential: ~60-90 seconds

**Resource Usage:**
- Memory: ~200MB (Chromium instances)
- CPU: Low (mostly waiting for network)
- Disk: ~5MB per day (reports + screenshots)

---

## Future Enhancements

### Phase 2
- [ ] Add more sources (Ars Technica, MIT Tech Review)
- [ ] Email/WeChat notifications
- [ ] Trending chart visualization
- [ ] Historical trend analysis

### Phase 3
- [ ] Custom source configuration UI
- [ ] Real-time monitoring (not just daily)
- [ ] Collaborative filtering (learn from user preferences)
- [ ] API endpoint for other tools

---

## Troubleshooting

**Q: Scan fails for some sources?**
A: Check if selectors are still valid. Websites change their HTML structure.

**Q: Too many irrelevant topics?**
A: Adjust theme keywords in `config/sources.json`

**Q: Scan is too slow?**
A: Reduce `limit` in config or disable some sources

---

## Credits

**Created by:** Kevin + Claude (AI助手)
**Created on:** 2026-01-23
**Version:** 1.0.0
**License:** MIT

**Inspired by:**
- Kevin's "捕捉热点" superpower
- "Build fast, share fast" philosophy
- ADHD-friendly automation

---

*"3秒钟出创意，快速捕捉热点" - Kevin's core ability*
