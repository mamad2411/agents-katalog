---
name: time-entry-markdown-presentation
description: Domain-agnostic primitive for formatting time entries (start/end times, title, description) into a markdown table with calculated durations and optional summary rows (actual total, targeted, remaining).
category: Data-Processing
---

# Time Entry Markdown Presentation Skill (v1)

This skill provides a generic primitive: take structured time entries with start/end times and descriptions, calculate durations, and render a clean markdown table. Supports optional summary rows for actual vs targeted time tracking.

The skill ships an executable script under `scripts/` — agents SHOULD invoke it directly rather than re-deriving the logic from prose (per [`AGENTS.md` §Reminder 5](../../../AGENTS.md) of the root registry).

***

## 1. Input Format

The script accepts a JSON array via stdin. Each entry object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start` | string | yes | Start time in `HH:MM` or `HH:MM:SS` format |
| `end` | string | yes | End time in `HH:MM` or `HH:MM:SS` format |
| `title` | string | yes | Short entry title (appears in the Title column) |
| `description` | string | no | Longer description (appears in the Description column) |

### Example

```json
[
  {"start": "06:30", "end": "13:25", "title": "Feature implementation", "description": "Core feature work"},
  {"start": "13:26", "end": "13:34", "title": "Phone call", "description": "Call with <colleague>"}
]
```

***

## 2. Output

A markdown table with four columns:

| Time | Duration | Title | Description |
|------|----------|-------|-------------|

### Duration calculation

- Each entry's duration is computed as `end - start` in hours and minutes.
- If `end` is earlier than `start`, midnight crossing is assumed (adds 24 hours).
- Format: `Xh Ym` (e.g., `6h 55m`). Entries under one hour: `Xm` (e.g., `8m`).

### Summary rows (optional)

| CLI flag | Default | Description |
|----------|---------|-------------|
| `--targeted` | (none) | Expected total time, e.g. `--targeted "6h"` |
| `--label-actual` | `Actual total` | Label for the total row |
| `--label-targeted` | `Targeted` | Label for the targeted row |
| `--label-remaining` | `Remaining` | Label for the remaining row |

When `--targeted` is provided, three summary rows are appended: Actual total, Targeted, and Remaining (prefixed with `-` if negative, i.e., over target).

***

## 3. Invocation

### Direct script invocation

```bash
# Create entries JSON file or pipe inline
echo '[
  {"start":"06:30","end":"13:25","title":"Feature implementation","description":"..."},
  {"start":"15:30","end":"17:35","title":"Colleague catchup","description":"..."}
]' | python3 scripts/format-time-entries.py --targeted "6h"
```

### From a composer skill

Composer skills MUST resolve the script relative to their own location, not the caller's cwd:

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_SCRIPT="$SCRIPT_DIR/../../time-entry-markdown-presentation/scripts/format-time-entries.py"

if [ ! -f "$BASE_SCRIPT" ]; then
  echo "ERROR: base script not found at $BASE_SCRIPT" >&2
  exit 1
fi

cat <<<"$JSON_PAYLOAD" | python3 "$BASE_SCRIPT" --targeted "$TARGETED"
```

***

## 4. Environment & Dependencies

| Requirement | Check | Notes |
|-------------|-------|-------|
| Python 3.12+ | `python3 --version` | Tier 1 default per [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md) |
| `json` (stdlib) | — | Available in all Python 3 distributions |

No third-party packages required.

***

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|----------|----------------------|
| *(project-specific composer)* | Pipes raw daily log entries (parsed from free-form text) into `scripts/format-time-entries.py` with `--targeted`; consumes the rendered table for the daily report. If your organization provides a shared skill library, check there for the project-specific parsing layer. |

***

## 6. Related Skills

| Skill | Relationship |
|-------|-------------|
| [`work-log-processing`](../work-log-processing/SKILL.md) | Handles rough→formatted TXT transformation (upstream of this presentation layer). The two skills form a pipeline: rough notes → structured entries → markdown table. |

***

## 7. Related Conversations & Traceability

This skill was derived from a daily work log formatting workflow demonstrated in an earlier session. Refer to the source conversation for operational context. If your organization provides a shared skill library, the companion composer skill may be available there.
