---
name: youtube-own-channel-analyzer
description: "Comprehensive YouTube channel analysis using YouTube Data API v3. Analyze your own channel's performance metrics, content strategy, upload patterns, engagement rates, video performance, and growth trends. Use when users want to (1) Analyze their YouTube channel performance, (2) Get insights on video engagement and metrics, (3) Understand upload patterns and optimal posting times, (4) Identify top-performing content types, (5) Generate channel health reports, (6) Track subscriber and view growth patterns. Requires user's YouTube Data API v3 key."
---

# YouTube Own Channel Analyzer

Analyze your YouTube channel's performance using the YouTube Data API v3.

## Setup

1. **API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) - enable YouTube Data API v3
2. **Channel ID**: Accept channel ID (UC...), @handle, or full URL

## API Endpoints

```
BASE_URL = https://www.googleapis.com/youtube/v3

# Channel details
GET /channels?part=snippet,statistics,contentDetails,brandingSettings&id={channelId}&key={API_KEY}

# Channel videos (paginated)
GET /search?part=snippet&channelId={channelId}&order=date&type=video&maxResults=50&key={API_KEY}

# Video details (batch up to 50 IDs)
GET /videos?part=snippet,statistics,contentDetails&id={videoIds}&key={API_KEY}
```

## Analysis Workflow

### 1. Resolve Channel ID
```
@handle → Search API with handle, get channelId from result
/channel/UC... → Extract directly
/c/name or /user/name → Use forUsername parameter
```

### 2. Fetch Data
- Channel: snippet, statistics, contentDetails, brandingSettings
- Videos: Paginate through search results, then batch video details

### 3. Analyze

**Content Types** - Categorize by title/description patterns:
| Type | Pattern |
|------|---------|
| Tutorial | tutorial, how to, guide, learn |
| Review | review, unbox, first look, comparison |
| Vlog | vlog, day in, life, daily |
| Educational | explain, education, lesson |
| Gaming | gameplay, game, gaming, stream |
| Music | music, song, cover, lyrics |

**Duration Buckets**: Short (<5min), Medium (5-15min), Long (15-30min), Very Long (30+min)

**Performance Metrics**:
- View-to-sub ratio: views/subscribers (benchmark: 10-20%)
- Engagement rate: (likes+comments)/views (benchmark: 1-5%)
- Like rate: likes/views (benchmark: 3-7%)
- Comment rate: comments/views (benchmark: 0.5-2%)
- Viral threshold: views > 5x subscribers
- Underperforming: views < 10% subscribers

**Upload Patterns**: Track day-of-week, hour-of-day, consistency (stddev of days between uploads)

**Title Analysis**: Track numbers, emojis, questions, brackets, caps usage, common words

## Output Report Structure

```markdown
# Channel Analysis Report
## Executive Summary
- Subscribers, views, videos, avg engagement, upload consistency
## Channel Overview
- Basic info, statistics table, description, keywords
## Content Analysis
- Category breakdown table, duration distribution, title patterns
## Performance Metrics
- Engagement metrics vs benchmarks table
## Upload Patterns
- Optimal day/hour, distribution charts
## Engagement Analysis
- Top 5 high-engagement videos, bottom 5 needing improvement
## Recommendations
- Content optimization, upload frequency, title suggestions
```

## Helper: Parse Duration
```javascript
// PT1H2M3S → seconds
const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
return (parseInt(match[1])||0)*3600 + (parseInt(match[2])||0)*60 + (parseInt(match[3])||0);
```

## Quota Notes
- Search: 100 units per call
- Channels/Videos: 1 unit per call
- Daily limit: 10,000 units (default)
- Batch video IDs (max 50) to optimize
