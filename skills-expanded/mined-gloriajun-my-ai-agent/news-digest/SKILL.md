---
name: news-digest
description: "Summarize a news article link from the daily digest, or analyze tech trends for a domain. Use when the user asks to summarize a specific article URL, or asks about recent tech trends."
metadata:
  {
    "openclaw":
      {
        "emoji": "🗞️",
        "requires": { "bins": ["curl"] }
      }
  }
---

# News Digest Skill

On-demand access to the news-digest service. Calls the news-digest HTTP API
directly with curl (this skill does NOT go through the n8n webhook).

- `link-summary`: return the stored Korean summary + metadata for an article URL
- `trends`: return the trend analysis for a domain (default `it`)

Base URL `${NEWS_DIGEST_URL}` (e.g. http://news-digest:8080) and header
`Authorization: Bearer ${INGEST_TOKEN}` are read from the shell env and required
on every call.

## Action Mapping

| User intent | action |
|---|---|
| 이 링크/기사 요약해줘, 이거 정리해줘 (URL 제공) | `link-summary` |
| 요즘 트렌드, 기술 동향, 이슈 정리, 트렌드 분석 | `trends` |

## action=link-summary

Requires `url`. If the user gave no link, ask for it before proceeding.

```bash
curl -sG "${NEWS_DIGEST_URL}/api/digest/summarize" \
  --data-urlencode "url=https://..." \
  -H "Authorization: Bearer ${INGEST_TOKEN}" \
  --max-time 20
```

- HTTP 200: present `summaryKo` as the body; header line = `title` (`sourceName`
  / `categoryName`); append `tags` as hashtags if present. If `summaryKo` is
  null, say the summary is not ready yet.
- HTTP 404 `{"error":"not_found"}`: the article is not in the digest yet. Tell
  the user it has not been collected/classified, and stop. Do NOT invent a summary.
- Any other status or timeout: tell the user the lookup failed.

## action=trends

`domain` is optional and defaults to `it`.

```bash
curl -sG "${NEWS_DIGEST_URL}/api/digest/trends" \
  --data-urlencode "domain=it" \
  -H "Authorization: Bearer ${INGEST_TOKEN}" \
  --max-time 30
```

- HTTP 200: present `content` as the trend analysis; if `basis` is present, add a
  short line stating the basis.
- HTTP 404 `{"error":"not_found"}`: no published issue for that domain. Tell the
  user and stop.
- Any other status or timeout: tell the user the request failed.

## Language

Always respond in Korean.
