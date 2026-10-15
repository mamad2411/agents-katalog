---
name: analyze-cli
description: Social media data analysis CLI — search, import, download comments/media, and run multi-step strategy analysis.
type: tool-use
---

# analyze-cli Skill

You operate the `analyze-cli` command-line tool for social media content analysis.

## Pre-execution Checks

Run these **in order** before any workflow:

1. **Verify CLI is executable**: `analyze-cli --version`
2. **Ensure daemon is running**: `analyze-cli daemon status` → `analyze-cli daemon start` if needed
3. **Read opencli skill** before using any `opencli` command
4. **Verify opencli**: `opencli --help` or `opencli doctor`

> If daemon logs a health-check failure and exits, do **not** delete the database file. Ensure no other process holds the database lock, then restart the daemon.

---

## Capabilities by Phase

### Phase 1: Data Collection

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 1 | **search_posts** | `opencli <site> <command> {query} --limit {limit} -f json` | Discover posts before importing. **Commands vary by platform** — (1) run `opencli list \| grep <keyword>` to find the platform, (2) run `opencli <platform> --help` to list available commands, (3) run `opencli <platform> <command> -h` to understand specific command usage.|
| 2 | **add_platform** | `analyze-cli platform add --id {id} --name {name}` | Register a platform if not already in `analyze-cli platform list`. |
| 3 | **import_posts** | `analyze-cli post import --platform {id} --file {path} [--task-id {tid}]` | Import search results. **Do NOT manually fetch note details before import** — let `prepare-data` enrich posts via `fetch_note` template. Duplicates are updated, not skipped. |
| 4 | **import_comments** | `analyze-cli comment import --platform {id} --post-id {id} --file {path}` | Import comments from JSON/JSONL after fetching. Duplicates skipped. |

### Phase 2: Task Setup

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 5 | **create_task** | `analyze-cli task create --name {name} [--cli-templates '{...}']` | Create task before adding steps. **Required template**: `fetch_note` (enriches post content). Optional: `fetch_comments`, `fetch_media`. |
| 6 | **add_step_to_task** | `analyze-cli task step add --task-id {tid} --strategy-id {sid} [--name {n}] [--order {n}]` | Add each strategy the user needs. |
| 7 | **list_strategies** | `analyze-cli strategy list` | Check available strategy IDs before adding steps. |

### Phase 3: Data Preparation

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 8 | **prepare_task_data** | `analyze-cli task prepare-data --task-id {tid}` | Fetch full post details, comments, and media. **Resumable** — continues from unfinished posts on retry. Fails if `cli_templates` lacks `fetch_note`. |

### Phase 4: Analysis Execution

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 9 | **run_all_steps** | `analyze-cli task run-all-steps --task-id {tid}` | **Default `--wait`**: blocks until all steps complete, printing progress. Use `--no-wait` for fire-and-forget. |
| 10 | **run_task_step** | `analyze-cli task step run --task-id {tid} --step-id {sid}` | Run a single step. **Default `--wait`**: blocks until completion. |
| 11 | **start_task** | `analyze-cli task start --task-id {tid}` | Enqueue jobs for pending targets **without** running strategy steps. |
| 12 | **reset_task_step** | `analyze-cli task step reset --task-id {tid} --step-id {sid}` | Reset a failed step to pending for retry. |

> **Progress output** (`--wait` mode):
> ```
> [10:23:45] Step: sentiment-analysis | running | 15/30 done, 1 failed
> [10:24:45] Steps progress: 2/2 completed
> ```

### Phase 5: Results & Management

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 13 | **get_task_results** | `analyze-cli task results --task-id {tid}` | After all steps complete. |
| 14 | **get_task_status** | `analyze-cli task show --task-id {tid}` | Show full task details including phases, steps, jobs, and recent failures. **Not needed when using `--wait` mode.** |
| 15 | **list_tasks** | `analyze-cli task list [--status {s}] [--query {text}]` | View existing tasks. Filter by status or search by name. |
| 16 | **list_task_steps** | `analyze-cli task step list --task-id {tid}` | Inspect step states before running. |
| 17 | **strategy_result_list** | `analyze-cli strategy result list --task-id {tid} --strategy {sid}` | Inspect per-post results. |
| 18 | **strategy_result_export** | `analyze-cli strategy result export --task-id {tid} --strategy {sid} [--format csv|json]` | Export results to file. |

### Utility & Recovery

| # | Tool | Command | When to Use |
|---|------|---------|-------------|
| 19 | **retry_failed_queue_jobs** | `analyze-cli queue retry [--task-id {tid}]` | Re-run only failed jobs. |
| 20 | **reset_queue_jobs** | `analyze-cli queue reset [--task-id {tid}]` | **Blunt instrument**: force-reset all non-pending jobs. Prefer `queue retry`. |
| 21 | **pause_task / resume_task / cancel_task** | `analyze-cli task pause|resume|cancel --task-id {tid}` | Control running tasks. |
| 22 | **list_posts / search_posts_db** | `analyze-cli post list [--platform {id}]` / `analyze-cli post search --platform {id} --query {text}` | Browse imported data. |
| 23 | **daemon management** | `analyze-cli daemon start [--fg]` / `stop` / `restart` / `status` | Manage daemon lifecycle. CLI auto-restarts daemon if version mismatch detected. |

### Advanced: Create Strategy

| # | Tool | Description |
|---|------|-------------|
| 24 | **create_strategy** | Generate a new analysis strategy via conversation. See JSON Rules below. |

---

## Execution Modes

Both `task prepare-data` and `task run-all-steps` / `task step run` support two execution modes. Choose based on whether the user wants to wait for completion or move on:

| Mode | Flag | Behavior | Use When |
|------|------|----------|----------|
| **Blocking (default)** | `--wait` | Command blocks until completion and prints live progress. Agent sees output and can report results immediately. | **Recommended for interactive workflows.** User wants real-time feedback. |
| **Non-blocking** | `--no-wait` | Command returns immediately after enqueueing jobs. Agent must check status later. | User wants to fire-and-forget, or is running multiple tasks in parallel. |

> `prepare-task-data` is always blocking (it has no `--no-wait` flag). `run-all-steps` and `step run` default to `--wait`.

---

## Standard Workflow

Data preparation and analysis are executed **back-to-back** in the standard flow:

```
search_posts(query) → add_platform(if new) → create_task(with fetch_note template)
  → import_posts(with --task-id) → add_step_to_task(for each strategy)
  → prepare_task_data(blocks until done)
  → run_all_steps --wait(blocks until all steps complete, prints progress)
  → get_task_results
```

### Template Discovery (Dynamic Query)

Since OpenCLI supports 100+ platforms and commands change over time, **always discover the correct commands dynamically** instead of relying on hard-coded examples.

**Step 1: Find the site name**
```bash
opencli list | grep -i <platform_name>
# e.g., opencli list | grep -i xiaohongshu → xiaohongshu
```

**Step 2: Discover available commands**
```bash
opencli <site> --help
# e.g., opencli xiaohongshu --help → search, note, comments, download, ...
```

**Step 3: Check command signature (critical!)**
```bash
opencli <site> <command> --help
# e.g., opencli xiaohongshu note --help
# Output: "note-id  Full Xiaohongshu note URL with xsec_token"
#         → requires {url} variable
```

**Step 4: Build templates based on command signature**
- If help says `"<note-id>"` or `"<post-id>"` (short ID) → use `{note_id}`
- If help says `"Full URL"` or `"URL"` → use `{url}` (always preferred when ambiguous)

### Template Variables

| Variable | Value | Use When |
|----------|-------|----------|
| `{post_id}` | Internal database post ID | Rarely needed by external commands |
| `{note_id}` | `metadata.note_id` → `url` → `post_id` (fallback chain) | Commands that accept short IDs |
| `{url}` | Full post URL from import data | **Default choice** — most OpenCLI commands accept full URLs |
| `{limit}` | Hardcoded `100` | Pagination limit for fetch_comments |
| `{download_dir}` | Configured download directory | Media file storage path |

> **Rule of thumb**: When in doubt, use `{url}`. It is the most universally accepted format across platforms.

### Example: Full Analysis Flow (Dynamic Discovery)

```bash
# 1. Discover platform commands
opencli list | grep -i xiaohongshu        # → xiaohongshu
opencli xiaohongshu --help                # → search, note, comments, ...
opencli xiaohongshu note --help           # → requires "Full note URL"

# 2. Search
opencli xiaohongshu search "上海美食" --limit 10 -f json > posts.json

# 3. Setup
analyze-cli platform add --id xhs --name "小红书"
analyze-cli task create --name "上海美食分析" \
  --cli-templates '{"fetch_note":"opencli xiaohongshu note {url} -f json","fetch_comments":"opencli xiaohongshu comments {url} --limit 100 -f json"}'

# 4. Import
analyze-cli post import --platform xhs --file posts.json --task-id <task_id>

# 5. Add strategies
analyze-cli task step add --task-id <task_id> --strategy-id sentiment-topics --name "情感分析"
analyze-cli task step add --task-id <task_id> --strategy-id risk-detection --name "风险检测"

# 6. Prepare data (blocks, resumable)
analyze-cli task prepare-data --task-id <task_id>

# 7. Run analysis (blocks with progress output)
analyze-cli task run-all-steps --task-id <task_id>
# → [10:23:45] Steps progress: 0/2 completed | running: 情感分析
# → [10:24:12] Steps progress: 1/2 completed | running: 风险检测
# → [10:24:45] Steps progress: 2/2 completed

# 8. Results
analyze-cli task results --task-id <task_id>
```

### Alternative: Non-blocking Mode

If the user wants to start the analysis and check back later (e.g., running multiple tasks in parallel):

```bash
# Data preparation still blocks
analyze-cli task prepare-data --task-id <task_id>

# But analysis runs in background
analyze-cli task run-all-steps --task-id <task_id> --no-wait
# → "All steps processed" (returns immediately)

# Check status later
analyze-cli task status --task-id <task_id>
```

### Recovery from Failure

```bash
# If a step fails after all retries:
analyze-cli task step reset --task-id <tid> --step-id <sid>
analyze-cli task step run --task-id <tid> --step-id <sid> --wait
```

---

## JSON Rules for create_strategy

**Required fields:**

- `id`: lowercase `a-z0-9_-`, e.g. `monetization-v1`
- `name`, `version` (default `"1.0.0"`)
- `target`: `"post"` only
- `needs_media`: `{ enabled: true/false, media_types, max_media, mode }` if enabled
- `prompt`: must include `{{content}}`; include `{{media_urls}}` if `needs_media.enabled`
- `output_schema`: standard JSON Schema, `type: "object"`, each property needs `type`

**Prompt variables (whitelist only):**

- `{{content}}` (required), `{{title}}`, `{{author_name}}`, `{{platform}}`, `{{published_at}}`, `{{tags}}`, `{{media_urls}}`

> Do NOT use `{{likes}}`, `{{collects}}`, `{{comments}}`, etc. They are not substituted.

**Prompt quality:** Append a JSON output-format hint to ensure pure JSON response (no markdown code blocks).

**Example:**

```json
{
  "id": "monetization-v1",
  "name": "Monetization Potential",
  "version": "1.0.0",
  "target": "post",
  "needs_media": { "enabled": true, "media_types": ["image"], "max_media": 5, "mode": "all" },
  "prompt": "Analyze the monetization potential of this post.\n\nContent: {{content}}\nAuthor: {{author_name}}\n\n{{media_urls}}\n\nReturn pure JSON only: { \"score\": number, \"category\": string }",
  "output_schema": {
    "type": "object",
    "properties": {
      "score": { "type": "number" },
      "category": { "type": "string" }
    }
  }
}
```

**Error recovery for strategy import:**

- Validation fails → read exact error, fix field, retry (max 2 retries)
- Same version exists → ask to bump version or change ID
- After approval: `analyze-cli strategy import --json '<json>'`, then `analyze-cli strategy show --id <id>`

---

## Global Rules

1. **Never write temporary polling scripts** looping `analyze-cli task status`. Use built-in `--wait` mode.
2. **Never use direct database access** (e.g., `node -e` scripts opening DuckDB). Always use CLI commands.
3. **Rate limit (429) recovery**: workers auto-requeue with exponential backoff. Only intervene when status becomes `failed` after all retries.
4. **Platform check first**: always `analyze-cli platform list` before `platform add` to avoid "already exists" errors.
5. **Do NOT manually fetch note details before import**: let `prepare-data` handle enrichment via the `fetch_note` template.
