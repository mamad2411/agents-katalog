---
name: flomo-local-api
description: Query, summarize, export, create, and edit a user's flomo memos through local desktop auth and the flomo API, without Chrome UI automation. Use when the user wants fast memo lookup, tag filtering, markdown export, lightweight memo creation, or direct text edits to existing memos.
---

# Flomo Local API

## Overview

Use this skill for fast flomo access when local desktop auth is available.

This is the default recommendation for `mac` users. If local desktop auth is missing or broken, fall back to `flomo-web-crud` instead of trying to fake the API path.

When the user wants to create or revise a memo:
1. **Tag reuse is required**: Prefer the user's existing flomo tag system over inventing new tags. Aim for existing-tag reuse in at least 95% of memo-writing cases.
2. **Plain text only**: flomo does not support Markdown rendering. Never use `**bold**`, `- [ ]` checkboxes, `# headers`, or other markdown syntax in memo content. Use plain text formatting instead.

This skill supports direct text edits to existing memos through the same local auth flow, including when the user provides a flomo memo URL like `https://v.flomoapp.com/mine/?memo_id=...`.

## Preconditions

- `flomo.app` has been logged in on this Mac before
- Local flomo storage exists under `~/Library/Containers/com.flomoapp.m/...`
- The request can be handled with local auth and API access

## Use This Skill When

- The user asks to search flomo memos by keyword, tag, or time range
- The user asks what they have been thinking about recently
- The user wants monthly markdown export or tag statistics
- The user wants to create a simple memo without Chrome UI automation
- The user wants to edit an existing text memo by slug or by flomo memo URL without opening the Web UI
- The user wants faster querying than Chrome UI automation
- The user wants a draft memo that fits their existing flomo tag taxonomy before creating it

## Do Not Use This Skill When

- The user wants to delete a memo
- The user wants to operate through the live Web UI
- The local desktop login state is missing or broken and the request cannot be completed from local auth

## Default Workflow

1. Use `scripts/flomo_local_api.py`.
2. Prefer `query` for direct lookup.
3. Prefer `summarize` for reflective prompts such as "最近在想什么".
4. Prefer `export-monthly` when the user wants markdown output.
5. Before creating or editing a memo with tags, inspect the user's existing tag taxonomy with `tags`.
6. Draft memo body first, then choose 1-4 tags by reusing existing tags that are already in the system.
7. Prefer `create` for lightweight memo creation without attachments.
8. Prefer `edit` for updating the text content of an existing memo by slug or `memo_id` URL.
9. Treat delete as out of scope unless the skill is expanded again later.

## Commands

### Command Template

Set the script path from the current environment instead of a hardcoded user directory:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/flomo-local-api"
SCRIPT="$SKILL_ROOT/scripts/flomo_local_api.py"
```

### Query

Use for direct search by keyword, tag, date range, or recent window.

```bash
python3 "$SCRIPT" query --keyword "openclaw" --limit 10
python3 "$SCRIPT" query --tag "Proj/mf" --days 30
python3 "$SCRIPT" query --start-date 2026-03-01 --end-date 2026-03-11 --format markdown
```

`query` results include both `slug` and the corresponding flomo memo URL so later edit steps can reuse them directly.

### Summarize

Use for "我最近在关注什么 / 最近状态如何" style requests.

```bash
python3 "$SCRIPT" summarize --days 30
python3 "$SCRIPT" summarize --days 90 --limit 80
```

### Export Monthly

Use when the user wants a monthly markdown dump plus `tag-stats.md`.

```bash
python3 "$SCRIPT" export-monthly
python3 "$SCRIPT" export-monthly --output-dir ~/download/flomo-markdown-export-monthly
```

### Tags

Use when the user wants to create or edit a memo and you need to reuse the existing tag system instead of inventing new tags.

```bash
python3 "$SCRIPT" tags --roots-only --limit 20
python3 "$SCRIPT" tags --query "agent" --limit 20 --min-total-count 2
python3 "$SCRIPT" tags --prefix "area/ai/agent" --limit 20 --format markdown --min-total-count 2
python3 "$SCRIPT" tags --query "设计" --days 365 --limit 20 --min-total-count 2
```

Recommended pattern for memo writing:

1. Draft the memo body without tags first.
2. Extract 2-5 likely concepts from the memo.
3. Start with one cheap scan: `tags --roots-only --limit 12`.
4. Then make at most 2 focused lookups, usually one concrete entity query and one abstract theme query. If the memo names a specific project, person, product, or proper noun, spend the first focused lookup on that exact entity string before abstract theme queries. Prefer `--min-total-count 2`.
5. If a root is obvious, prefer one `--prefix` lookup inside that subtree over spraying many synonym queries.
6. Reuse 1-4 existing tags, preferring mature path tags with repeated usage.
7. Stop once you have 2 strong tags and at most 1-2 optional supporting tags. Do not keep searching just to exhaust every possible synonym.
8. If the best hit is a singleton leaf under an unfamiliar root, widen once and prefer a broader, better-established parent or nearby mature sibling.
9. If the memo clearly centers on a named project, person, or product and an existing `Proj/*`, `p/*`, or product tag exists, include that concrete taxonomy tag before adding more generic thematic tags.
10. When an exact or near-exact named-entity tag is found, treat it as required evidence, not optional flavor. Do not drop it in favor of only abstract theme tags.
11. Only create a new tag when there is no close existing tag. If you do, tell the user briefly why reuse was not possible.

Search budget:

- Default budget is 3 tag lookups total:
  - 1 roots-only scan
  - 1 focused entity/theme lookup
  - 1 optional disambiguation lookup
- Going beyond 3 lookups needs a clear reason, such as no mature match after the first pass.
- Avoid synonym fan-out like querying `prompt`, `eval`, `policy`, `rules`, `safety`, `design`, `comment` one by one unless earlier results were genuinely inconclusive.

### Create

Use when the user wants to quickly create a text memo from local auth.

**Text Formatting Note**: flomo does not render Markdown syntax. Use plain text formatting instead:
- For emphasis: use `「」` quotes or ALL CAPS instead of `**bold**`
- For lists: use simple bullets like `•` or `1.` instead of markdown list syntax
- Do NOT use checkboxes or todo lists in flomo memos
- Keep paragraphs separated by blank lines for readability

```bash
python3 "$SCRIPT" create --content "测试 memo #codex/demo"
printf '第一行\n\n第二段 #codex/demo\n' | python3 "$SCRIPT" create --stdin
```

### Edit

Use when the user wants to update the text of an existing memo and already has either the memo `slug` or a flomo memo URL.

**Text Formatting Note**: Same as `create` — flomo does not render Markdown. Use plain text formatting.

```bash
python3 "$SCRIPT" edit --slug "MTIzMDgzNzgz" --content "更新后的 memo 内容 #codex/demo"
python3 "$SCRIPT" edit --url "https://v.flomoapp.com/mine/?memo_id=MTIzMDgzNzgz" --content "更新后的 memo 内容 #codex/demo"
printf '第一行修改后\n\n第二段也更新\n' | python3 "$SCRIPT" edit --slug "MTIzMDgzNzgz" --stdin
```

## Output Conventions

- `query --format json` returns structured memo hits
- `query --format markdown` returns a readable markdown list
- `summarize` returns memo counts, top tags, and supporting memos
- `export-monthly` writes one markdown file per month plus `tag-stats.md`
- `tags` returns existing tag rows with `tag`, `depth`, `parent`, `direct_count`, `total_count`
- `create` returns the created memo payload with parsed markdown and tags
- `edit` returns the updated memo payload with parsed markdown and tags

## Safety Rules

- Only use `create` when the user explicitly asks for a new memo
- Only use `edit` when the user explicitly asks to modify an existing memo
- Do not invent new tags casually; check existing tags first with `tags`
- Do not delete flomo memos from this skill
- Do not persist extra raw dumps unless the user explicitly asks
- Treat summaries as patterns from memo evidence, not diagnoses
- Never use Markdown syntax in memo content
- Never create task lists or checkboxes in flomo memos

## Resources

### scripts/

- `scripts/flomo_local_api.py`: CLI for flomo query, summarize, export, lightweight create, and text edit
