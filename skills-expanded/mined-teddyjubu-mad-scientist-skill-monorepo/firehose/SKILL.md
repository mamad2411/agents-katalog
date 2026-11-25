---

description: firehose lets the user monitor the web in real-time by creating Lucene query rules that track specific keywords, domains, or page types and stream matching results via Server-Sent Events, which is useful when they want to track brand mentions, competitor activity, news alerts, or website changes as they happen instead of polling manually.
triggers:
  - User wants to monitor web mentions of a keyword, brand, or domain
  - User asks to track changes on specific websites in real-time
  - User mentions "Firehose", "web monitoring", "real-time alerts", "track mentions", "monitor competitors"

name: firehose
---
Monitor the web in real-time. Create Lucene query rules, and every crawled page that matches gets streamed to you instantly.

---

## What This Skill Does

This skill firehose lets the user monitor the web in real-time by creating Lucene query rules that track specific keywords, domains, or page types and stream matching results via Server-Sent Events, which is useful when they want to track brand mentions, competitor activity, news alerts, or website changes as they happen instead of polling manually.

## Workflow

### 1. List Taps (Get Tap Tokens)
Your management key (`fhm_...`) can create taps. Each tap has its own token (`fh_...`) for managing rules and streaming.

```bash
cd ~/.openclaw/workspace/skills/firehose
node scripts/list-taps.js
```

### 2. Create a Tap
Taps are isolated rule containers. Create one per use case (e.g., "Brand Mentions", "Competitor Tracking").

```bash
node scripts/create-tap.js "Brand Mentions"
```

Returns the tap ID and token. **Store the token — you'll need it for rules and streaming.**

### 3. Create Rules
Rules are Lucene queries that define what pages to match. Examples:

- **Simple keyword:** `ahrefs` (matches "ahrefs" in page content)
- **Boolean:** `title:tesla AND language:"en"` (Tesla in title, English pages only)
- **Domain filter:** `domain:techcrunch.com` (only pages from TechCrunch)
- **Exclude junk:** `title:tesla AND NOT url:/.*\\/page\\/[0-9]+.*/` (no pagination URLs)
- **Recency:** `title:openai AND recent:24h` (OpenAI mentions in last 24 hours)

```bash
# Create a rule (requires tap token)
node scripts/create-rule.js <tap-token> "title:tesla AND language:\"en\"" "tesla-mentions"
```

### 4. List Rules
```bash
node scripts/list-rules.js <tap-token>
```

### 5. Stream Matches (Real-Time)
Open a Server-Sent Events stream. Prints matching pages as they're crawled.

```bash
node scripts/stream.js <tap-token>
```

**Options:**
- `--since 1h` — replay buffered events from last hour (max 24h)
- `--limit 10` — close after 10 matches
- `--timeout 60` — close after 60 seconds

### 6. Update/Delete Rules
```bash
node scripts/update-rule.js <tap-token> <rule-id> "new query" "new-tag"
node scripts/delete-rule.js <tap-token> <rule-id>
```

name: firehose
---

## Lucene Query Syntax Quick Reference

### Indexed Fields
- **`added`** (default): text from inserted content (tokenized, case-insensitive)
- **`removed`**: text from deleted content
- **`title`**: page title (tokenized, case-insensitive)
- **`url`**: full URL (exact, case-sensitive keyword)
- **`domain`**: domain (exact, case-sensitive keyword)
- **`language`**: ISO 639-1 code (`"en"`, `"fr"`, `"zh-cn"`)
- **`page_category`**: ML category label (`"/News"`, `"/Business_and_Industrial"`)
- **`page_type`**: ML type label (`"/Article"`, `"/Listing/Product"`)
- **`recent`**: recency filter (`recent:24h`, `recent:7d`, `recent:3mo`)

### Operators
- **Terms:** `ahrefs` (bare term searches `added` field)
- **Phrases:** `"quick brown fox"` (exact phrase)
- **Boolean:** `java AND programming`, `title:tesla OR added:"electric vehicle"`, `NOT malware`
- **Wildcards:** `url:*\\/category\\/*` (escape `/` as `\\/` in wildcard queries)
- **Regex:** `url:/.*\\/page\\/[0-9]+.*/` (enclosed in `/`, escape `/` inside as `\\/`)

### Common Patterns

**Brand mentions (English only, no junk URLs):**
```
title:chucky AND language:"en" AND NOT url:/.*\\/page\\/[0-9]+.*/ AND NOT url:*\\/category\\/* AND NOT url:*\\/tag\\/*
```

**Competitor tracking (domain + keyword):**
```
domain:competitor.com AND added:"new feature"
```

**News about a topic (last 24 hours):**
```
title:openai AND page_category:"/News" AND recent:24h
```

**Product listings with a keyword:**
```
added:"real estate" AND page_type:"/Listing/Property"
```

---

## Rule Object Fields (Not Part of Query)

When creating/updating rules, you can pass these fields in the JSON body:

- **`value`** (string, required): Lucene query
- **`tag`** (string, optional): label for the rule (max 255 chars)
- **`nsfw`** (boolean, default `false`): include adult content
- **`quality`** (boolean, default `true`): apply quality filters (exclude pagination/category/tag URLs, pages older than 7 days, URLs with query params)

Example:
```json
{
  "value": "title:tesla AND language:\"en\"",
  "tag": "tesla-mentions",
  "nsfw": false,
  "quality": true
}
```

name: firehose
---

## Use Cases

1. **Brand Monitoring:** Track mentions of your brand, product, or competitors across the web.
2. **Content Discovery:** Find new articles/posts about specific topics in real-time.
3. **Competitive Intelligence:** Monitor competitor domains for new pages, features, or announcements.
4. **Lead Generation:** Watch for pages matching your ICP (e.g., property listings, job postings, service pages).
5. **SEO Opportunities:** Find pages linking to competitors but not you, or track keyword trends.

---

## Authentication

- **Management Key (`fhm_...`)**: Create/list/update/delete taps. **Never expose publicly.**
- **Tap Token (`fh_...`)**: Manage rules + stream for a specific tap. Can be shared within your team.

Both use `Authorization: Bearer <token>` header.

name: firehose
---

## API Reference

Base URL: `https://api.firehose.com`

### Management Endpoints (require `fhm_...`)
- `GET /v1/taps` — list all taps
- `POST /v1/taps` — create a tap
- `GET /v1/taps/:id` — get tap details
- `PUT /v1/taps/:id` — update tap name
- `DELETE /v1/taps/:id` — revoke tap

### Tap Endpoints (require `fh_...`)
- `GET /v1/rules` — list rules
- `POST /v1/rules` — create rule
- `GET /v1/rules/:id` — get rule
- `PUT /v1/rules/:id` — update rule
- `DELETE /v1/rules/:id` — delete rule
- `GET /v1/stream?timeout=60&since=1h&limit=100` — SSE stream

---

## Event Types (SSE)

- **`connected`**: stream opened
- **`update`**: page matched a rule (payload includes `document` with `url`, `title`, `markdown`, `diff`, `page_category`, `page_types`, `language`)
- **`error`**: something went wrong
- **`end`**: stream closed (timeout/limit reached)

name: firehose
---

## Notes

- Max **25 rules per organization**
- Events buffered for ~24 hours (use `since` to replay)
- `Last-Event-ID` header for auto-resume on disconnect (browser `EventSource` API handles this)
- Quality filters are **on by default** (exclude junk URLs, 7-day recency, no query params)

---

## External References

Full API docs: [https://firehose.com/api-docs](https://firehose.com/api-docs)
