---
name: discourse-read
description: Read and summarize a Discourse forum topic thread for the current research project. Saves last-read watermark to CLAUDE.md.
argument-hint: "[--new] [--feedback] [<topic-url>]"
allowed-tools: Read, Edit, Bash
---

# Discourse Read Skill

Read posts from the project's Discourse topic and produce a structured summary. Uses the Discourse REST API via `curl`.

## Input

- **--new** (optional): Only fetch posts since the last-read watermark
- **--feedback** (optional): Focus summary on questions, critiques, and suggestions from replies
- **`<topic-url>`** (optional): Override the stored topic URL for this invocation only (not saved)

## Environment

Required (in shell env or `.env` file at repo root):
- `DISCOURSE_API_KEY` — API key from forum profile
- `DISCOURSE_API_USERNAME` — forum username

---

## Workflow

### Step 1: Load Environment

```bash
[ -f .env ] && export $(grep -v '^#' .env | xargs)
```

Check that `DISCOURSE_API_KEY` and `DISCOURSE_API_USERNAME` are set. If either is missing, stop:
```
❌ Missing credentials. Set in shell or .env:
   DISCOURSE_API_KEY=...
   DISCOURSE_API_USERNAME=...
```

---

### Step 2: Bootstrap — Resolve Topic URL

1. If a `<topic-url>` argument was provided, use it for this run only (do not save).
2. Otherwise, read `CLAUDE.md` and look for the `## Discourse` section:
   - Extract `topic_url`, `base_url`, `topic_id`, `last_read_post`
3. If no `## Discourse` section exists in `CLAUDE.md`, prompt:
   ```
   No Discourse topic configured. Enter the topic URL:
   >
   ```
   Parse the URL `https://<host>/t/<slug>/<id>` to extract:
   - `base_url`: `https://<host>`
   - `topic_id`: `<id>` (integer at end of path)
   - `topic_slug`: `<slug>`
   - `last_read_post`: `0`

   Write the `## Discourse` section into `CLAUDE.md` (append, preserving all existing content):
   ```markdown
   ## Discourse

   - **Topic URL**: <full url>
   - **Base URL**: <base_url>
   - **Topic ID**: <topic_id>
   - **Last read post**: 0
   ```

---

### Step 3: Fetch Topic Posts

Determine `start_post` based on flags:
- `--new`: use `last_read_post + 1`
- otherwise: `1`

Fetch topic metadata and first post:
```bash
curl -s -H "Api-Key: ${DISCOURSE_API_KEY}" \
     -H "Api-Username: ${DISCOURSE_API_USERNAME}" \
     "${base_url}/t/${topic_id}.json" | python3 -m json.tool
```

If `start_post > 1`, fetch only posts after the watermark using the `posts.json` stream endpoint:
```bash
curl -s -H "Api-Key: ${DISCOURSE_API_KEY}" \
     -H "Api-Username: ${DISCOURSE_API_USERNAME}" \
     "${base_url}/t/${topic_id}/posts.json?post_number_gt=${start_post}"
```

Paginate if `has_more` is true (increment `page` param) until all posts are retrieved. Cap at 200 posts per run.

If the topic returns a 404 or auth error, stop with a clear message including the status code.

---

### Step 4: Summarize

Parse the JSON response and produce a structured summary.

**Default summary:**
```
## Discourse Thread Summary
Topic: <title>
URL: <topic_url>
Posts read: <N> (post #<start> → #<end>)
Date range: <first_post_date> → <last_post_date>

### Original Post
<2–4 sentence synopsis of the opening post>

### Replies (<N> posts)
<For each reply: author, post #, 1–2 sentence summary>

### Key Themes
- <theme 1>
- <theme 2>
```

**With `--feedback` flag**, replace "Key Themes" with:
```
### Community Questions
- <question> (post #N, @username)

### Critiques
- <critique> (post #N, @username)

### Suggestions
- <suggestion> (post #N, @username)

### Action Items
- [ ] <actionable item worth adding to docs/roadmap.md>
```

If `--new` and no new posts exist:
```
✓ No new posts since post #<last_read_post>.
```

---

### Step 5: Update Last-Read Watermark

After a successful fetch, update `last_read_post` in the `CLAUDE.md` `## Discourse` section to the highest post number retrieved:

Use Edit to replace the line:
```
- **Last read post**: <old_value>
```
with:
```
- **Last read post**: <new_highest_post_number>
```

---

### Step 6: Output

Print the summary to the conversation. End with:
```
📌 Last read post updated to #<N> in CLAUDE.md
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing API credentials | Stop with setup instructions |
| 401 Unauthorized | Stop: "Check DISCOURSE_API_KEY and DISCOURSE_API_USERNAME" |
| 404 Not found | Stop: "Topic not found. Verify the topic URL in CLAUDE.md" |
| No posts after watermark | Print "No new posts since #<N>" and exit cleanly |
| Malformed URL | Stop with URL format example |
| curl not available | Stop: "curl is required" |
