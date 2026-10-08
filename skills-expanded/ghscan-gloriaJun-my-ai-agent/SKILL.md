---
name: news-detail
description: "Fetch full article content or community comment reactions for a given URL. Use when the user asks for more details about a news article or wants to know how people reacted in comments."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl"] }
      }
  }
---

# News Detail Skill

Handles three types of requests:
- `article-summary`: Fetch the article content and return a detailed summary
- `comment-summary`: Fetch community comments (Hacker News or GeekNews) and summarize reactions
- `search-summary`: Search news by keyword using Brave Search and return a synthesized summary

---

## Action Mapping

Determine `action` from user intent:

| User intent | action |
|-------------|--------|
| 더 자세히, 본문 요약, 내용 알려줘, 자세한 내용 | `article-summary` |
| 댓글, 반응, 커뮤니티 반응, 사람들 반응, HN 댓글 | `comment-summary` |
| ~뉴스 알려줘, ~최신 동향, ~관련 뉴스 찾아줘, 키워드 검색 | `search-summary` |

All requests use: `POST "${N8N_WEBHOOK_BASE_URL}?type=news&mode=detail&action={action}"`

---

## Required fields

### article-summary / comment-summary

| Field | Key | Format | Description |
|-------|-----|--------|-------------|
| URL | url | string | The article URL or HN/GeekNews link from the news summary |

If `url` is missing, ask the user to provide the link before proceeding.

### search-summary

| Field | Key | Format | Description |
|-------|-----|--------|-------------|
| 검색어 | query | string | 뉴스를 검색할 키워드 |

If `query` is missing, ask the user for a search keyword before proceeding.

---

## action=article-summary

Fetches the article at the given URL and returns a detailed Korean summary.

### curl example

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=news&mode=detail&action=article-summary" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"url":"https://..."}'
```

**Success**: `status === "ok"` AND `summary` field is present.

On success, present the `summary` as-is. If `title` is present, use it as a header.

**Failure**: `status` ≠ `"ok"` → inform the user the article could not be fetched. Include the `message` field if present.

---

## action=comment-summary

Fetches comments from Hacker News (via HN API) or GeekNews for the given URL and summarizes the community reactions.

### curl example

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=news&mode=detail&action=comment-summary" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"url":"https://..."}'
```

**Success**: `status === "ok"` AND `summary` field is present.

On success, present the `summary` as-is. The summary will describe the overall tone, key discussion points, and notable opinions from the community.

**Failure**: `status` ≠ `"ok"` → inform the user the comments could not be fetched. Include the `message` field if present.

---

## action=search-summary

Searches news articles via Brave Search using the given keyword and returns a synthesized Korean summary.

### curl example

```bash
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=news&mode=detail&action=search-summary" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"query":"MCP 최신 동향"}'
```

**Success**: `status === "ok"` AND `summary` field is present.

On success, present the `summary` as-is.

**Failure**: `status` ≠ `"ok"` → inform the user the search failed. Include the `message` field if present.

---

## Language

Always respond in Korean.
