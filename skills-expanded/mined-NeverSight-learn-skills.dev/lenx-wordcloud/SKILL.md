---
name: lenx-wordcloud
description: "Generate wordcloud visualisations from Lenx task monitoring data via the lenx-mcp stdio server. Use when asked to create a word cloud, visualise keyword frequency from Lenx task data, or analyse text patterns from social media monitoring. Supports Chinese (Simplified and Traditional via jieba) and English text segmentation, keyword include/exclude filtering, and sentiment-based filtering. Triggers on: /lenx-wordcloud, wordcloud for task, generate wordcloud for lenx task, wordcloud task data."
compatibility: "Requires the MCP client/agent to have lenx-mcp stdio configured so the lenx_get_task_data MCP tool is available. Requires Python 3 with packages: wordcloud, matplotlib, Pillow, jieba."
metadata:
  author: thinkcol
  version: "1.0"
---

# Lenx Task Wordcloud

You MUST follow every step below in exact order. Do NOT skip steps. Do NOT improvise. Do NOT add your own logic. Execute each step literally, then move to the next.

## Step 1 — Parse the user prompt

Extract these values from the user's message. Do not ask clarifying questions unless Task ID is missing.

| Variable | How to extract | Default |
|---|---|---|
| `TASK_ID` | Number after "task" (e.g., `task 1528` → `1528`) | **Required** — ask if missing |
| `TIME_RANGE` | "past 24 hours", "last 7 days", "from X to Y", etc. | `past 24 hours` |
| `INCLUDE` | `--include "word1,word2"` or `include word1 and word2` | Empty (no include filter) |
| `EXCLUDE` | `--exclude "word1,word2"` or `exclude word1 and word2` | Empty (no exclude filter) |
| `SENTIMENT` | `--sentiment positive\|negative\|neutral` | Empty (no sentiment filter) |
| `MAX_WORDS` | `--max-words N` | `200` |
| `WIDTH` | `--width N` | `1920` |
| `HEIGHT` | `--height N` | `1080` |
| `COLORMAP` | `--colormap NAME` | `"viridis"` |
| `BACKGROUND` | `--background COLOR` | `"white"` |
| `EXTRA_STOPWORDS` | `--extra-stopwords "word1,word2"` | Empty |

Set this constant — do NOT change it:

```
WORK_DIR=".lenx-wordcloud-work"
```

Resolve `SKILL_DIR` to the absolute path of this skill's directory (the directory containing this SKILL.md file).

Proceed to Step 2.

## Step 2 — Check prerequisites

Confirm the current agent has access to the `lenx_get_task_data` MCP tool from a configured `lenx-mcp` stdio server.

Do NOT ask the user for `LENX_API_KEY`, `LENX_USER_ID`, or `LENX_BASE_URL`. Those credentials belong in the user's MCP client configuration and are used by the already-configured `lenx-mcp` server.

If `lenx_get_task_data` is not available, tell the user: "The lenx-mcp stdio server is not available in this MCP client. Please configure `@fastaai/lenx-mcp` in your `mcpServers` settings, then restart/reload the client." Then STOP. Do not continue.

Otherwise proceed to Step 3.

## Step 3 — Calculate timestamps

lenx-mcp expects `from`, `to`, and `search_after` as Unix timestamp **milliseconds**. Do NOT use seconds.

Run the appropriate command based on `TIME_RANGE`:

```bash
# Past 24 hours
FROM_MS=$(python3 -c "import time; print(int((time.time() - 86400) * 1000))")
TO_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
```

```bash
# Past 7 days
FROM_MS=$(python3 -c "import time; print(int((time.time() - 604800) * 1000))")
TO_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
```

```bash
# Past 30 days
FROM_MS=$(python3 -c "import time; print(int((time.time() - 2592000) * 1000))")
TO_MS=$(python3 -c "import time; print(int(time.time() * 1000))")
```

```bash
# Custom range — replace DATE_FROM and DATE_TO with ISO dates
FROM_MS=$(python3 -c "from datetime import datetime; print(int(datetime.fromisoformat('DATE_FROM').timestamp() * 1000))")
TO_MS=$(python3 -c "from datetime import datetime; print(int(datetime.fromisoformat('DATE_TO').timestamp() * 1000))")
```

Also calculate a human-readable date string for the output filename:

```bash
FROM_DATE=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($FROM_MS / 1000).strftime('%Y%m%d'))")
TO_DATE=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($TO_MS / 1000).strftime('%Y%m%d'))")
```

You now have `FROM_MS`, `TO_MS`, `FROM_DATE`, and `TO_DATE`. Proceed to Step 4.

## Step 4 — Fetch ALL data into JSONL via MCP

**YOU — the main agent — MUST NOT fetch pages yourself.** Raw MCP page results can be large and will pollute your context. Dispatch exactly one fetch subagent to do the MCP pagination using the tool's direct-to-disk `output_path` parameter, then convert the resulting JSONL to TSV.

**4A — Create work directory**

```bash
mkdir -p .lenx-wordcloud-work
```

**4B — Dispatch fetch subagent**

Call the Task tool once with this prompt. Replace `{TASK_ID}`, `{FROM_MS}`, and `{TO_MS}`:

```
Use the configured lenx-mcp stdio MCP tool `lenx_get_task_data` to fetch all Lenx monitoring data for task {TASK_ID} from Unix timestamp milliseconds {FROM_MS} to {TO_MS}.

Do not ask for Lenx credentials. They are already configured in the MCP client. Do not return raw records in your final response.

The `lenx_get_task_data` tool supports an `output_path` parameter that writes results as JSONL directly to disk, avoiding large response payloads in your context.

Fetch pages using these arguments:
- task_id: {TASK_ID}
- from: {FROM_MS}
- to: {TO_MS}
- size: 1000
- output_path: .lenx-wordcloud-work/all_posts.jsonl

For the FIRST page, use output_mode: "overwrite" (creates a fresh file).
For each subsequent page, use output_mode: "append" (adds to the existing file).
- search_after: omit on the first call; for later calls, use the `unix_timestamp` millisecond value of the last record from the previous page

The tool auto-appends .jsonl if the path doesn't end with it, so the actual file will be all_posts.jsonl.

Retry failed MCP tool calls up to 3 times with exponential backoff (2s, 4s, 8s). Continue until all available pages are fetched (fetched >= total) or the last page has fewer than 1000 records.

When done, write `.lenx-wordcloud-work/fetch_metadata.json` with exactly:
{
  "total_records": <total from lenx_get_task_data>,
  "complete": true
}

Final response: one sentence only, with total records and the filename. Do not include raw records.
```

Wait until the fetch subagent returns.

**4C — Verify fetch completed**

Run this command:

```bash
python3 - <<'PY'
import json
with open('.lenx-wordcloud-work/fetch_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)
print(meta['total_records'])
print('yes' if meta.get('complete') else 'no')
PY
```

Assign stdout line 1 to `TOTAL_RECORDS`, line 2 to `COMPLETE`.

If `COMPLETE` is not `yes`, STOP and report that data fetching did not complete.

If `TOTAL_RECORDS` is `0`, tell the user "No data found for task {TASK_ID} in the specified time range" and STOP.

**4D — Convert JSONL to TSV**

Run this command to extract only the fields we need (`sentiment_score`, `lang_abbr`, `post_message`) from the JSONL into the TSV format that generate_wordcloud.py expects:

```bash
python3 - <<'PY'
import json

jsonl_path = '.lenx-wordcloud-work/all_posts.jsonl'
tsv_path = '.lenx-wordcloud-work/posts.tsv'
count = 0

with open(jsonl_path, 'r', encoding='utf-8', errors='replace') as inf, \
     open(tsv_path, 'w', encoding='utf-8') as outf:
    for line in inf:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        # Extract fields with defaults
        message = record.get('post_message', '')
        score = str(record.get('sentiment_score', ''))
        lang = record.get('lang_abbr', '')
        
        # Clean message: replace tabs/newlines with spaces, truncate to 500 words
        message = message.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
        words = message.split()
        if len(words) > 500:
            message = ' '.join(words[:500])
        
        # Write TSV: sentiment_score\tlang_abbr\tpost_message
        outf.write(f"{score}\t{lang}\t{message}\n")
        count += 1

print(f"Converted {count} records")
PY
```

Verify the posts file exists:
```bash
wc -l .lenx-wordcloud-work/posts.tsv
```

The line count should equal `TOTAL_RECORDS`. Proceed to Step 5.

## Step 5 — Generate the wordcloud

Run this exact command. Substitute all `{}` variables.

```bash
python3 "SKILL_DIR/scripts/generate_wordcloud.py" \
  --input ".lenx-wordcloud-work/posts.tsv" \
  --output ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.png" \
  --metadata ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.json" \
  --max-words {MAX_WORDS} \
  --width {WIDTH} \
  --height {HEIGHT} \
  --colormap "{COLORMAP}" \
  --background "{BACKGROUND}" \
  {INCLUDE_FLAG} \
  {EXCLUDE_FLAG} \
  {SENTIMENT_FLAG} \
  {EXTRA_STOPWORDS_FLAG}
```

Where:
- `INCLUDE_FLAG` is `--include "word1,word2"` if `INCLUDE` is set, else empty string
- `EXCLUDE_FLAG` is `--exclude "word1,word2"` if `EXCLUDE` is set, else empty string
- `SENTIMENT_FLAG` is `--sentiment {SENTIMENT}` if `SENTIMENT` is set, else empty string
- `EXTRA_STOPWORDS_FLAG` is `--extra-stopwords "word1,word2"` if `EXTRA_STOPWORDS` is set, else empty string

Verify the output files exist:

```bash
ls -la ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.png"
ls -la ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.json"
```

Proceed to Step 6.

## Step 6 — Copy output to working directory

```bash
cp ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.png" "./wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.png"
cp ".lenx-wordcloud-work/wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.json" "./wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.json"
```

Set `OUTPUT_PNG` to `./wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.png`.
Set `OUTPUT_META` to `./wordcloud_task_{TASK_ID}_{FROM_DATE}_{TO_DATE}.json`.

Proceed to Step 7.

## Step 7 — Cleanup

```bash
rm -rf .lenx-wordcloud-work
```

Verify cleanup:
```bash
ls .lenx-wordcloud-work 2>/dev/null && echo "ERROR: work dir still exists" || echo "cleanup OK"
```

After this, the ONLY files remaining are `OUTPUT_PNG` and `OUTPUT_META`.

Proceed to Step 8.

## Step 8 — Respond to user

Read the metadata JSON file:

```bash
python3 - <<'PY'
import json
with open('OUTPUT_META', 'r', encoding='utf-8') as f:
    meta = json.load(f)
# Pretty-print
print(json.dumps(meta, indent=2, ensure_ascii=False))
PY
```

Substitute `OUTPUT_META` with the actual file path.

Say exactly three things:

1. **File path:** "Wordcloud saved to: `{OUTPUT_PNG}`"
2. **Summary:** Present a concise summary from the metadata — total posts used, sentiment distribution, top words, any filters applied.
3. **Metadata:** "Task {TASK_ID} | {TIME_RANGE} | {TOTAL_RECORDS} records | Wordcloud generated with {MAX_WORDS} max words | Filters: {INCLUDE or 'none'} / {EXCLUDE or 'none'} / sentiment: {SENTIMENT or 'none'}"

Do NOT mention chunks, subagents, MCP pagination, or any internal process.

**DONE.** Do not continue past this step.

---

## Reference — lenx-mcp stdio configuration

This skill expects the user's MCP client to expose the `lenx_get_task_data` tool from a configured `lenx-mcp` stdio server. Example MCP client configuration:

```json
{
  "mcpServers": {
    "lenx": {
      "command": "npx",
      "args": ["-y", "@fastaai/lenx-mcp"],
      "env": {
        "LENX_API_KEY": "your-api-key",
        "LENX_USER_ID": "your-user-id",
        "LENX_BASE_URL": "https://open.lenx.ai"
      }
    }
  }
}
```

Credential handling:
- Do not ask the user to re-enter credentials if `lenx_get_task_data` is already available.
- Do not read MCP config files to extract credentials.
- Do not log or copy credential values into generated files.

Only the `lenx_get_task_data` MCP tool is required by this skill.

## Reference — Wordcloud visual parameters

| Flag | Default | Description |
|---|---|---|
| `--max-words` | `200` | Maximum number of words to display |
| `--width` | `1920` | Image width in pixels |
| `--height` | `1080` | Image height in pixels |
| `--colormap` | `"viridis"` | Matplotlib colormap name |
| `--background` | `"white"` | Background color |

## STRICT — Rules you MUST NOT break

1. Follow Steps 1–8 in exact order. Do not skip. Do not reorder. Do not add steps.
2. **YOU (the main agent) MUST dispatch the fetch subagent in Step 4.** Do NOT fetch MCP data yourself.
3. NEVER read raw MCP page results yourself. Always delegate to the subagent.
4. ALWAYS clean up `.lenx-wordcloud-work` before responding. The only artifacts are the PNG and JSON files.
5. If the fetch subagent fails, re-dispatch it. Do not restart the entire process.
6. Do NOT stop early. Complete ALL steps through Step 8.
