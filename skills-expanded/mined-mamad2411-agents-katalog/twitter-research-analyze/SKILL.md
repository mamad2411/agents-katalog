---
name: twitter-research-analyze
version: 3.0.0
description: |
  Analyze state — reads the scraped topic posts from raw-posts.json (10+
  posts across many accounts), scores target audience segments 1-10 based on
  engagement signals, generates social media post drafts and video script
  drafts from top-performing posts, and identifies content patterns.

allowed-tools:
  - Bash
  - Read
  - Write
  - ChromeDevTools
---

# Twitter/X Research — Analyze State (v3)

Scores audiences, generates content drafts, and identifies winning patterns. The output
files are consumed by `twitter-research-report` (`node "$CLAUDE_SKILL_ROOT/scripts/report-html.js" <timestamp>`).

## Preconditions

- Scrape completed: `.twitter-research/<YYYY-MM-DD_HHMMSS>/raw-posts.json`
- Config exists: `.twitter-research/<timestamp>/config.json`

## Steps

### 1. Load data

```bash
node -e "const d=require('./.twitter-research/<YYYY-MM-DD_HHMMSS>/raw-posts.json'); console.log(JSON.stringify({topic:d.topic, distinctAccounts:d.distinctAccounts, posts:d.posts.map(p=>({handle:p.handle, likes:p.likes, retweets:p.retweets, url:p.url, text:p.text.substring(0,120)}))},null,2))"
```

### 2. Audience segmentation & scoring

For each `targetAudienceKeyword` in config, score 1-10 using: relevance, engagement
rate, content affinity, monetization potential, competition level (lower = better).
Find matching posts per segment and note pain points + content angles.

Save to `audience-scores.json`:
```json
{
  "analysisTimestamp": "<YYYY-MM-DD HH:MM:SS>",
  "segments": [
    {
      "segment": "social media manager",
      "finalScore": 9,
      "breakdown": {"relevance": 10, "engagementRate": 9, "contentAffinity": 8, "monetization": 9, "competitionLevel": 7},
      "verdict": "✅ Best Prospect",
      "painPoints": ["..."],
      "contentAngles": ["..."],
      "whyScore": "...",
      "matchingTweetsCount": 8
    }
  ],
  "contentPatterns": {"topHookTypes": [], "bestFormats": [], "contentCalendar": {}},
  "totalPostsAnalyzed": 10,
  "distinctAccountsAnalyzed": 7,
  "topic": "<topic>"
}
```

### 3. Generate social media post drafts

For the top topic posts, adapt each winning angle to the user's brand voice
(headline, body, CTA, hashtags, best time). Generate via the backend API if available:

```bash
curl -s -X POST http://localhost:8080/api/script \
  -H "Content-Type: application/json" \
  -d '{"videoSubject":"<topic>","extraPrompt":"<build a viral social post adapting the top tweet>","aiModel":"g4f","scriptTemplate":"viral_shorts"}'
```

If the API is unavailable, write drafts manually based on each tweet's structure and angle.

### 4. Generate video script drafts

If `contentFormat` includes video, generate 30-60s scripts: hook → problem → solution → social proof → CTA.

### 5. Save to content-drafts.json

```json
{
  "generatedAt": "<YYYY-MM-DD HH:MM:SS>",
  "postDrafts": [{"rank": 1, "sourceHandle": "@h", "sourceUrl": "...", "targetSegment": "...", "headline": "...", "body": "...", "cta": "...", "hashtags": ["#a"], "format": "social_post"}],
  "videoScripts": [{"rank": 1, "sourceHandle": "@h", "sourceUrl": "...", "targetSegment": "...", "hook": "...", "body": "...", "cta": "...", "format": "video_script"}]
}
```

## Report Completion

```
✅ Twitter/X Research Analysis Complete!
Session: .twitter-research/<timestamp>/
Audience segments scored: <N> (top: <segment> <score>/10)
Content drafts: <N> posts · <N> scripts
Next step: skill twitter-research-report
```
