---
name: youtube-competitor-analyzer
description: "Find and analyze YouTube competitor channels using YouTube Data API v3. Discover competitors through keyword search, category matching, content similarity, and related channel discovery. Compare metrics, content strategies, and market positioning. Use when users want to (1) Find competitors for their YouTube channel, (2) Analyze competitor performance metrics, (3) Compare their channel against competitors, (4) Identify content gaps and opportunities, (5) Benchmark against similar creators, (6) Generate competitive analysis reports. Requires user's YouTube Data API v3 key."
---

# YouTube Competitor Analyzer

Find and analyze competitor channels using YouTube Data API v3.

## Setup

1. **API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) - enable YouTube Data API v3
2. **Input**: User's channel (for context) OR list of competitor channels to analyze directly

## API Endpoints

```
BASE_URL = https://www.googleapis.com/youtube/v3

# Search channels
GET /search?part=snippet&q={query}&type=channel&maxResults={n}&key={API_KEY}

# Channel details
GET /channels?part=snippet,statistics,contentDetails,brandingSettings&id={ids}&key={API_KEY}

# Channel videos
GET /search?part=snippet&channelId={id}&order=date&type=video&maxResults=50&key={API_KEY}

# Video details
GET /videos?part=snippet,statistics,contentDetails&id={ids}&key={API_KEY}
```

## Competitor Discovery Methods

### 1. Keyword Search
Extract keywords from user's channel (description, title, brandingSettings.keywords), search for channels:
```
GET /search?q={keyword}&type=channel&maxResults=10
```

### 2. Content Similarity
Get user's recent video titles, extract frequent words (>4 chars), search channels with those terms.

### 3. Category Search
Search within same YouTube category as user's channel.

### 4. Related Discovery
Search using user's video titles/descriptions to find channels creating similar content.

### 5. Direct Input
User provides specific channels to analyze: @handles, channel IDs, or URLs.

## Competitor Ranking

```javascript
// Size similarity (log scale)
sizeSimilarity = 1 - Math.abs(Math.log10(compSubs+1) - Math.log10(targetSubs+1)) / 10;

// Engagement per video
engagementRate = viewCount / (videoCount || 1);

// Overall score
overallScore = sizeSimilarity * 0.3 + relevanceScore * 0.7;
```

Sort by overallScore, return top 10-15.

## Comparative Analysis

For each competitor, extract:
| Metric | Description |
|--------|-------------|
| Subscribers | Direct count |
| Total Views | Channel lifetime views |
| Video Count | Total videos published |
| Views/Video | Average performance |
| Upload Frequency | Videos per month |
| Channel Age | Days since creation |

Compare user channel vs competitor averages:
- Above/below average positioning
- Growth rate comparison
- Content volume gaps

## Content Gap Analysis

Compare across competitors:
- Content types they cover vs user doesn't
- Duration preferences
- Upload schedules
- Title/thumbnail patterns
- High-performing topics

## Output Report Structure

```markdown
# Competitive Analysis Report
## Executive Summary
- Competitors found, key positioning insights
## Competitor Table
| Channel | Subs | Videos | Views | Views/Video | Score |
## Competitive Positioning
- User vs competitor averages
- Market position assessment
## Content Strategy Comparison
- What competitors do differently
- Common patterns among top performers
## Opportunities
- Content gaps to fill
- Underserved niches
- Schedule optimization
## Recommendations
- Strategic actions based on analysis
```

## Niche-Specific Search Terms

For spiritual/wellness channels:
```
meditation, mindfulness, yoga, spiritual, consciousness, wellness, self-help, awakening
```

For tech channels:
```
tech review, unboxing, tutorial, how to, comparison, tips, gadget
```

For gaming:
```
gameplay, let's play, walkthrough, gaming, stream, esports
```

## Quota Optimization

- Limit discovery to 20-30 initial channels
- Detailed analysis for top 10-15 only
- Batch video IDs (max 50 per call)
- Cache results when comparing multiple times
