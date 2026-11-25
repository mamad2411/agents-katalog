---
name: newsflow
description: Run configurable opencli news commands sequentially, skip failed commands, normalize JSON stories, and deduplicate globally by URL before producing daily fresh-news and per-run fresh-news markdown digests. Use when user wants repeatable multi-source news aggregation with easy command add/remove via commands.json and requires model-handled translation (no third-party translation API).
---

# Newsflow

## Execution Setup

1. Resolve `<SKILL_ROOT>` as the absolute directory containing this loaded `SKILL.md`.
2. Use the current environment's command or shell execution capability to run bundled scripts with `python3`.
3. Use the current environment's file-reading and file-writing capabilities for configuration, run artifacts, and model-produced translation JSON.
4. Substitute the resolved absolute `<SKILL_ROOT>` in every command, quote every path argument, and pass all arguments in the same command invocation. Do not rely on environment variables or shell state surviving between calls.
5. Do not detect or guess the runtime, load runtime-specific adapters, or assume a global install path or canonical repository path. This skill uses the same workflow in every environment.

## Workflow

1. Use current working directory as the output directory.
2. Read command configuration:
   - Default: `<SKILL_ROOT>/references/commands.json`.
   - Optional override: user-provided config path via `--config`.
3. Define run-scoped working paths. Do not reuse flat temp files like `.news_state/tmp_current.json`; each run must use its own artifact directory under `.news_state/runs/<run-dir>/`:

```bash
WORKDIR=<absolute current working directory>
STATE_DIR=<WORKDIR>/.news_state
RUNS_DIR=<STATE_DIR>/runs
RUN_DIR=<RUNS_DIR>/<unique-run-dir>
CURRENT_JSON_PATH=<RUN_DIR>/current.json
INCREMENTAL_JSON_PATH=<RUN_DIR>/incremental.json
TRANSLATED_JSON_PATH=<RUN_DIR>/translated.json
```

4. Run pipeline script sequentially:

```bash
python3 "<SKILL_ROOT>/scripts/run_news_pipeline.py" --config "<commands.json>" --out-json "<CURRENT_JSON_PATH>"
```

5. Wait for step 4 to exit successfully before continuing. Never run `prepare` while the pipeline command is still in flight.
6. Prepare incremental payload:

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" prepare --current-json "<CURRENT_JSON_PATH>" --state-dir "<STATE_DIR>" --out-json "<INCREMENTAL_JSON_PATH>"
```

Prepare recovery policy:

- If `prepare` succeeds, continue normally.
- If `prepare` fails, inspect stderr for a bracketed `PREPARE_*` error code.
- For recoverable prepare codes, abandon the current run artifact directory, create a fresh `<RUN_DIR>`, rerun the pipeline from step 4, then rerun `prepare` once.
- Do not reuse the failed run's `current.json`, `incremental.json`, or `translated.json`.
- Do not retry more than once. If the second `prepare` fails, stop and report both the original and retry failures.
- Do not retry non-recoverable prepare codes; stop and report the error.
- When an automatic prepare retry happens, mention it in the final response with the first failure reason and the new run directory.

Recoverable prepare codes:

- `PREPARE_STALE_CURRENT_JSON`: the current payload is older than the latest finalized run.
- `PREPARE_RUN_ID_ALREADY_FINALIZED`: the run id has already been finalized today.
- `PREPARE_CURRENT_JSON_UNREADABLE`: the current run artifact is missing or not valid JSON.

Non-recoverable prepare codes:

- `PREPARE_BAD_ARTIFACT_PATH`: artifact paths are outside the run directory, mixed across run directories, identical, or inconsistent with stored metadata.
- `PREPARE_BAD_CURRENT_JSON`: `current.json` exists but does not match the expected pipeline payload structure.
- `PREPARE_BAD_RUN_METADATA`: run identity, timezone, or timestamp metadata is missing or invalid.
- `PREPARE_BAD_STATE`: the daily state file is invalid or cannot be parsed safely.
- `PREPARE_WRITE_FAILED`: `incremental.json` could not be written.

7. Parse incremental JSON result:
   - `run_fresh_items_raw`: this run's fresh stories after removing yesterday URLs and earlier same-day URLs.
   - `items_to_translate`: stories whose titles still need model translation for display.
   - `current_run_errors`: errors and recovered degradations from this run. When a primary command fails but a retry or fallback succeeds, the pipeline may still emit an `已恢复：...` entry here so downstream reports can surface source health issues.
   - `daily_errors`: accumulated errors and recovered degradations for the current day.
   - `run_id` / `started_at` / `finished_at`: immutable run identity fields. Downstream steps must preserve them exactly.
   - `run_output_stem`: deterministic `YYYY-MM-DD-HH-mm-ss-<sha256前12位>` stem derived from `generated_at + run_id`; use it for per-run output names.
   - `section_metadata`: immutable per-run snapshot of source display/classification/translation metadata; downstream steps must use this snapshot rather than reread a mutable config.
   - `state_snapshot`: the latest finalized daily state seen during `prepare`. `finalize` will reject stale snapshots.
8. Translate display text into Chinese in-model:
   - Create the initial deterministic plan. The script derives required fields and keeps the existing `auto` rule that any title containing a Unicode Han character (including mixed-language text) does not need title translation, while still planning an English quote or Bloomberg summary when required. This is a character check, not language detection: Japanese text containing Kanji also satisfies it.

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" plan-translations --incremental-json "<INCREMENTAL_JSON_PATH>" --translated-json "<TRANSLATED_JSON_PATH>" --out-json "<RUN_DIR>/translation-plan.json" --phase initial
```

   - Translate each `batches[*].items` in `translation-plan.json`. The plan counts only required source text from titles, quotes, and summaries. Up to `batch_source_char_limit` (currently 12,000 characters) stays in one batch; larger input is split by source-text capacity. No item is truncated or summarized to fit, and one oversized item remains intact in its own batch.
   - Write each model result as `<RUN_DIR>/translation-initial-batch-NNN.json`, using exactly the batch's `expected_urls` as its top-level URL keys. Do not add, omit, or substitute a URL.
   - Merge each batch only through the script, which checks the exact URL set and required fields before atomically updating the cumulative map:

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" merge-translation-batch --plan-json "<RUN_DIR>/translation-plan.json" --batch-id batch-NNN --batch-json "<RUN_DIR>/translation-initial-batch-NNN.json" --translated-json "<TRANSLATED_JSON_PATH>"
```

   - For every planned item whose `required_fields` includes `title`, translate `title`.
   - For Twitter quote items, translate quote text when present.
   - For Twitter items, `title` always means the main tweet `text`, and `quoted_text` always means `quotedTweet.text`. Never swap them.
   - For long Twitter posts, translate the main tweet and quoted tweet in full, preserving paragraph boundaries / numbering when practical. Do not summarize, compress, or rewrite them into a shorter takeaway sentence.
   - For Bloomberg items with `summary`, translate `summary` too; final Markdown displays the translated summary under the Bloomberg item.
   - Translation must stay in the model, not inside any script.
   - Write a JSON object into `<TRANSLATED_JSON_PATH>`:
     - Legacy format (still supported): map URL to translated title string.
     - Extended format (recommended): map URL to object with `title`, optional quote fields, and optional `summary` / `summary_zh`.
   - If `items_to_translate` is empty, still write `{}` to `<TRANSLATED_JSON_PATH>`.

9. Validate translated map before finalize:

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" validate-translations --incremental-json "<INCREMENTAL_JSON_PATH>" --translated-json "<TRANSLATED_JSON_PATH>"
```

Validation workflow:
- If validate returns `ok=true`, continue to finalize.
- If validate returns `ok=false`, generate the one permitted repair plan; it contains only required fields still missing or non-Chinese, split by the same deterministic rules:

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" plan-translations --incremental-json "<INCREMENTAL_JSON_PATH>" --translated-json "<TRANSLATED_JSON_PATH>" --out-json "<RUN_DIR>/translation-repair-plan.json" --phase repair
```

- Translate and merge each repair batch with `merge-translation-batch`, using `translation-repair-batch-NNN.json` and `translation-repair-plan.json`. Do not directly edit the cumulative map or create another repair plan.
- Run `validate-translations` exactly one more time after repair.
- Validation automatically records hidden run-scoped state in `translation-validation.json`. Do not edit it. If initial validation has issues, `finalize` rejects the run until one repair plan and a second validation have been completed.
- Translation diagnostics remain in the hidden validation state; they are not rendered in Markdown or news-reader sidecar `errors`.
- Do not loop indefinitely. Even if the second validate still reports title issues, continue to finalize so news collection is not blocked; report the result as a partial translation outcome, never as full translation success. Diagnostics remain only in hidden run state, not user output errors.
- `validate-translations` checks structure and required-field coverage only; it does not score translation style/quality.

```json
{
  "https://example.com/story": "中文标题",
  "https://x.com/ivanalog_com/status/123?s=20": {
    "title": "中文正文标题",
    "quoted_text_zh": "引用推文中文翻译"
  },
  "https://www.bloomberg.com/news/articles/example": {
    "title": "中文标题",
    "summary_zh": "中文摘要"
  }
}
```

10. Finalize outputs:

```bash
python3 "<SKILL_ROOT>/scripts/run_incremental_news.py" finalize --incremental-json "<INCREMENTAL_JSON_PATH>" --translated-json "<TRANSLATED_JSON_PATH>" --state-dir "<STATE_DIR>" --out-dir "<WORKDIR>"
```

Optional export step (post-finalize):

```bash
python3 "<SKILL_ROOT>/scripts/export_outputs.py" --daily "<daily_fresh_path>" --fresh "<run_fresh_path>" --target-root "<export_root>"
```

Export rules:
- Export copies the daily Markdown, per-run fresh Markdown, and the daily `.newsreader.json` sidecar. Per-run freshNews has no sidecar and export must not require or copy one.
- Export root precedence is: `--target-root` CLI argument, `NEWSFLOW_EXPORT_ROOT`, then the legacy personal default `/Users/x/Library/Mobile Documents/iCloud~md~obsidian/Documents/DailyNews`.
- When the legacy default is used, the command prints a compatibility warning to stderr; pass an explicit root for portable use.
- If the root directory does not exist, export fails with explicit error and root path.
- Month subdirectory is auto-created as `YYYY年M月`, parsed from filenames.
- `dailyFreshNews_YYYY-MM-DD.md` and either legacy `YYYY-MM-DD-HH-mm_freshNews.md` or current `YYYY-MM-DD-HH-mm-ss-<12hex>_freshNews.md` must resolve to the same year-month.
- Export overwrites same-name files by default.
- Export failure never rolls back finalized local outputs.

Finalize recovery policy:

- If `finalize` succeeds, continue normally.
- If `finalize` fails, inspect stderr for a bracketed `FINALIZE_*` error code.
- For `FINALIZE_STATE_CHANGED_SINCE_PREPARE`, rerun `prepare` once using the same `current_json_path` stored in `incremental.json.paths.current_json_path`, the same `STATE_DIR`, and the same `INCREMENTAL_JSON_PATH`.
- After rerunning `prepare`, reuse the existing `translated.json` as a base, translate only newly missing `items_to_translate` fields, then rerun `finalize` once.
- Do not rerun the pipeline as part of finalize recovery. If the same `current.json` is rejected during the new `prepare`, stop and report that the current artifact is no longer usable against the latest state.
- Do not retry `FINALIZE_OUTPUT_EXISTS`, `FINALIZE_WRITE_FAILED`, bad artifact paths, bad JSON, bad metadata, bad state, or already-finalized runs.
- Bloomberg summary translation issues are handled before `finalize` by repairing `translated.json`; if still unresolved after one repair, `finalize` uses the original summary and keeps diagnostics in hidden run state.

Recoverable finalize codes:

- `FINALIZE_STATE_CHANGED_SINCE_PREPARE`: daily state changed after `prepare`; rerun `prepare` from the same `current.json`.

Non-recoverable finalize codes:

- `FINALIZE_BAD_ARTIFACT_PATH`: artifact paths are outside the run directory, mixed across run directories, or inconsistent with stored metadata.
- `FINALIZE_BAD_INCREMENTAL_JSON`: `incremental.json` is missing, invalid JSON, or not an object.
- `FINALIZE_BAD_TRANSLATED_JSON`: `translated.json` is missing, invalid JSON, or not an object.
- `FINALIZE_BAD_RUN_METADATA`: run identity, timezone, or timestamp metadata is missing or invalid.
- `FINALIZE_BAD_INCREMENTAL_METADATA`: date, run timestamp, paths, or state snapshot metadata is invalid.
- `FINALIZE_BAD_STATE`: the daily state file is invalid or cannot be parsed safely.
- `FINALIZE_RUN_ALREADY_FINALIZED`: this run id or generated timestamp has already been finalized.
- `FINALIZE_OUTPUT_EXISTS`: the target per-run `freshNews.md` already exists.
- `FINALIZE_WRITE_FAILED`: an output Markdown or state file could not be written.

10. Finalize writes exactly two user-facing Markdown files:
   - `dailyFreshNews_YYYY-MM-DD.md`: one rolling summary file per day.
   - `YYYY-MM-DD-HH-mm-ss-<sha256前12位>_freshNews.md`: one collision-resistant per-run fresh-news file.
   - Timezone: `Asia/Shanghai` unless user explicitly requests another timezone.
   - Finalize also writes only `dailyFreshNews_YYYY-MM-DD.newsreader.json`; it must not create a per-run `*_freshNews.newsreader.json`.
   - Do not delete a legacy per-run sidecar if one already exists. Older state entries may contain `run_sidecar_path`; accept and ignore that field, while new run records must not write it.
11. Hidden state is stored separately in the state directory, one JSON file per day.
12. Safety rules:
   - `prepare` and `finalize` now require run artifacts to live under `<STATE_DIR>/runs/<run-dir>/`.
   - `finalize` never overwrites an existing per-run fresh-news file; legacy incremental artifacts without `run_output_stem` are finalized with the newly derived stem.
   - If `prepare` sees a `current.json` older than the latest finalized run, it fails instead of returning a misleading `0 条新增`.
   - Recoverable `prepare` failures may trigger one clean retry from a new run directory; non-recoverable failures must remain hard stops.
   - If state changes after `prepare`, rerun `prepare` from the same `current.json`; do not force `finalize` and do not automatically rerun pipeline.

## State Schema Notes

- Daily state file path: `<STATE_DIR>/YYYY-MM-DD.json`.
- Top-level keys are daily aggregates and metadata, for example:
  - `date`, `timezone`, `section_order`
  - `today_seen_urls`, `today_first_seen_items`
  - `daily_errors`
  - `runs` (array of per-run summaries)
- Run artifact directory: `<STATE_DIR>/runs/<run-dir>/`.
- Pipeline payload now includes `run_id`, `started_at`, `finished_at`, and may include `current_json_path`.
- Per-run counters are stored under `runs[-1]` (latest run), not at top level.
  - Read `runs[-1].run_fresh_count` for this run's fresh count.
  - Read `runs[-1].daily_fresh_count` for current day cumulative fresh count.
  - Read `runs[-1].error_count` for this run error count.
  - Read `runs[-1].run_fresh_path` / `runs[-1].daily_fresh_path` for output files.
  - New runs also record audit fields such as `run_id`, `current_json_path`, `incremental_json_path`, `translated_json_path`, `prepared_at`, and `finalized_at`.
- If `runs` is empty, treat run-level stats as unavailable rather than `0`.

## commands.json Format

The bundled v1.2.2 default config has 19 ordered source entries, including 11 Twitter accounts.

Use JSON array of objects:

```json
[
  {
    "section": "middle-east",
    "display_name": "Reuters · Middle East",
    "source_type": "reuters",
    "source_name": "Reuters",
    "translation_policy": "always",
    "command": ["opencli", "ReutersBrowser", "news", "https://www.reuters.com/world/middle-east/", "--limit", "10", "--format", "json"]
  }
]
```

Rules:
- Keep order as desired final processing order.
- Add/remove sources by adding/removing objects only.
- `command` supports string array (recommended) or shell string.
- `display_name`, `source_type`, and `source_name` define the source metadata snapshot consumed by prepare/finalize; Twitter also requires `source_handle`.
- Optional reliability fields are supported per source:
  - `retry_once`: retry the primary command once before recording failure.
  - `fallback_command`: secondary command when primary still fails.
  - `treat_empty_as_failure`: treat zero valid rows as failure for retry/fallback.
  - `min_valid_items`: minimum valid rows required for success when empty-check is enabled.
  - `translation_policy`: translation requirement policy for this source (`always`, `auto`, `never`).
- Current policy in this skill:
  - News portal sources use `retry_once`; most also use `treat_empty_as_failure: true` and `min_valid_items: 1`.
  - Twitter sources use `retry_once` only; do not force empty-as-failure by default.
  - Reuters/Bloomberg/TechCrunch/Ars should use `translation_policy: "always"`.
  - Twitter should use `translation_policy: "auto"`.

## Output Contract

For each output Markdown file:

- Emit full `## section（N条）` sections only for non-empty groups after filtering.
- Use display-friendly section names when available, such as `Reuters · World` or `TechCrunch`.
- Add a one-line summary blockquote under each non-empty section header:
  - Format: `> N条｜最新 ...｜最早 ...｜时间倒序`
- Separate adjacent non-empty sections with `---`.
- Do not emit standalone `（0条）` section headers for empty groups.
- Instead, append a summary section at the end:
  - `## 本次无更新的分组（X个）`
  - List each empty group as a bullet using its display name, or `- 无` when there are none.

Example non-empty section:

```markdown
## Reuters · World（3条）

> 3条｜最新 2026-04-09 10:00:00｜最早 2026-04-09 08:00:00｜时间倒序

### [中文标题](https://...)
- 发布时间：YYYY-MM-DD HH:MM:SS
```

Example empty-group summary:

```markdown
## 本次无更新的分组（2个）

- Bloomberg
- Reuters · World
```

Constraints:
- Missing time must be `页面未显示`.
- Bloomberg summaries should be rendered in Chinese when translation is available. The translation map may use `summary` or `summary_zh`; `summary_zh` is preferred for clarity.
- If a non-Chinese Bloomberg summary is present but its translated summary is missing or still non-Chinese after one repair attempt, `finalize` writes the original source summary without adding a user-visible error.
- Preserve first-seen order: command order first, then source order.
- Global dedupe key is absolute URL exact match.
- Daily filtering removes yesterday's URLs.
- Per-run filtering removes yesterday's URLs and URLs seen earlier the same day.
- Twitter (`twitter user-posts --json`) is supported:
  - Every Twitter command in `references/commands.json` must declare `source_type: "twitter"`, `source_handle`, and `source_name`; these fields identify the configured collection account and flow into every normalized item and sidecar entry.
  - Keep collection identity separate from content authorship: `source_handle` / `source_name` identify whose timeline was collected, while `author_screen_name` / `author_name` and the item URL identify the actual content author for originals, reposts, replies, and quotes.
  - Add or remove Twitter accounts only through `commands.json`; do not maintain a section-name allowlist in scripts.
  - `text` -> output title.
  - `author.name` can be used as `section` via commands config.
  - URL auto-generated as `https://x.com/{screenName}/status/{id}?s=20`.
  - `createdAtLocal` -> 发布时间.
  - `quotedTweet.text` renders as blockquote.
  - The translation map must keep the same split: main tweet translation in `title`, quoted tweet translation in canonical `quoted_text_zh`.
  - `quoted_text` is accepted for legacy artifacts only when `quoted_text_zh` is absent. If both keys are present, the canonical key wins; distinct Chinese values are a validation conflict.
  - Long Twitter posts should be translated in full; do not collapse them into a short summary sentence.
  - If `quoted_text_zh` is provided, only Chinese quote text is rendered (no bilingual block).
  - Recommended translation policy: only translate non-Chinese text.
- Add final block:

```markdown
## errors

### 1. section
- 命令：`...`
- 错误：...
```

## Validation Checklist

1. Pipeline runs all commands sequentially.
2. Failed command does not stop later commands.
3. Duplicate URLs are removed globally, keeping first occurrence.
4. Translation is model-handled, not external translation API.
5. Non-empty sections include display names and summary blockquotes; empty sections are grouped under `本次无更新的分组`.
6. Finalize writes `dailyFreshNews_YYYY-MM-DD.md` and `YYYY-MM-DD-HH-mm-ss-<sha256前12位>_freshNews.md`, not `*_fullNews.md`.
7. Reusing stale pipeline JSON or attempting to overwrite an existing run file must fail loudly.
