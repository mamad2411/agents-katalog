---
name: youtube-audit
description: Analyze a YouTube channel with evidence-first metadata, transcripts, performance fields, portfolio shape, and repeated content-quality patterns
type: research
version: v0.5
argument-hint: "<channel URL or handle> [--count N]"
interview_depth: none
---

# YouTube Audit — Evidence-First Channel Analysis

Invoke as `$youtube-audit`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

Two CLI tools are required. Neither needs API keys.

- **yt-dlp**: Lists channel videos as JSON. Install: `brew install yt-dlp` or `pip install yt-dlp`.
- **youtube-transcript-api**: Fetches transcripts via Python. If the active Python is externally managed, such as Homebrew Python on macOS under PEP 668, install this package in a project-local virtual environment instead of the system Python.

Check `yt-dlp` before proceeding. The transcript dependency should be handled through a project-local `.venv` when it is missing.

## Process

### 1. Parse Arguments

- `$ARGUMENTS` must contain a YouTube channel URL or handle (e.g. `@handle`).
- Optional `--count N` sets how many recent videos to fetch (default 20, max 50).
- If no channel is provided, ask the user for one and stop.
- Normalize handles to channel video URLs when needed: `@handle` -> `https://www.youtube.com/@handle/videos`.
- Validate that `yt-dlp` is available first:

```bash
command -v yt-dlp
```

- Select the Python interpreter for transcript fetching. Prefer a workspace-local virtual environment when present; if one is not present, create it before checking the transcript import:

```bash
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
TRANSCRIPT_PYTHON=.venv/bin/python
"$TRANSCRIPT_PYTHON" -c "from youtube_transcript_api import YouTubeTranscriptApi; print('ok')"
```

- If the import check fails, install the missing package into the project-local virtual environment, then rerun the import check:

```bash
.venv/bin/python -m pip install youtube-transcript-api
"$TRANSCRIPT_PYTHON" -c "from youtube_transcript_api import YouTubeTranscriptApi; print('ok')"
```

- Store the selected interpreter path and use it for every transcript-fetching command in this audit.
- If package installation fails because network access is unavailable or denied, stop and report the exact safe install commands below:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install youtube-transcript-api
```

Do not recommend installing `youtube-transcript-api` into Homebrew/system Python with `python3 -m pip install ...`, and do not recommend `--break-system-packages`. The local-venv path avoids PEP 668 `externally-managed-environment` failures on Homebrew Python.

### 2. Archive Previous Audit

If `research/youtube/youtube-audit-*.md` or legacy `research/youtube-audit-*.md` already exists for the same channel (check the `> Channel:` header in existing files):

1. Copy the existing file to `docs/history/archive/YYYY-MM-DD/HHMMSS/research/youtube-audit-*.md`.
2. Preserve the archived snapshot exactly.
3. Then proceed to overwrite the canonical path.

New files do not need archive snapshots.

### 3. Fetch Video List

Create:

```text
research/youtube/data/<slug>/
```

Run full metadata export, not flat playlist metadata:

```bash
yt-dlp --dump-json --playlist-end N "CHANNEL_URL/videos"
```

Persist the raw newline-delimited response exactly to:

```text
research/youtube/data/<slug>/videos-YYYY-MM-DD.jsonl
```

Parse each JSON object for at least:

| Field | Notes |
| --- | --- |
| `id`, `webpage_url`, `title`, `description` | Identity and audit links |
| `channel`, `channel_id`, `uploader`, `uploader_id` | Channel identity |
| `upload_date`, `timestamp` | Used for recency and views/day |
| `duration` | Used for views/minute |
| `view_count`, `like_count`, `comment_count` | Performance |
| `tags`, `categories`, `chapters` | Positioning and packaging signals |
| `thumbnail`, `thumbnails` | Packaging review signal |

Build a video table sorted by upload date (newest first). Report total videos found.

### 4. Fetch Transcripts

Use the same Python interpreter that passed the import check. If `.venv/bin/python` exists and passed the import check, run transcript fetching with `.venv/bin/python`; otherwise use the Python executable that passed the import check. Fetch transcripts sequentially and persist raw transcript JSON:

```python
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path
import json, sys, time

video_ids = json.loads(sys.argv[1])
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
results = {}
errors = []

for vid in video_ids:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid)
        (out_dir / f"{vid}.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        results[vid] = " ".join(entry["text"] for entry in transcript)
    except Exception as e:
        errors.append({"id": vid, "reason": str(e)})
    time.sleep(1.5)

summary = {"transcripts": results, "errors": errors}
(out_dir / "transcripts-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
json.dump(summary, sys.stdout)
```

- Fetch sequentially with 1.5s delay to avoid rate limiting.
- Skip videos without transcripts and log the reason.
- If more than 80% lack transcripts, warn the user and ask whether to proceed.
- Do not fabricate transcript text; transcript gaps are evidence quality limits.

### 5. Prepare Analysis Context

Build structured records per video:

| Field | Computation |
| --- | --- |
| Title, date, URL, duration, views, likes, comments | Direct from metadata |
| Age in days | From upload date to current date |
| Views/day | `view_count / max(age_days, 1)` |
| Views/minute | `view_count / max(duration_minutes, 1)` |
| Like rate | `like_count / view_count` when both exist |
| Transcript coverage | `yes`, `no`, or `partial` |
| Archetype | Format pattern such as founder update, interview, tutorial, analysis, vlog, launch, reaction, teardown |
| Content role | Strategic role such as acquisition, trust-building, proof, education, launch support, community retention, cleanup candidate |

If total transcript text exceeds 80,000 words, truncate each transcript to preserve:
- First 500 words (hook and intro)
- Last 300 words (outro and CTA)
- Trim the middle proportionally across all videos to fit the budget

### 6. Analyze Content

Analyze performance and content in one pass.

### Performance And Portfolio Fields

Include:

- Total videos analyzed, transcript coverage, total views, median views, top video, bottom video.
- Views/day and views/minute leaders.
- Top-video concentration: top 1, top 3, and top 5 share of analyzed views.
- Portfolio distribution by archetype and content role.
- Packaging signals from titles, thumbnails, tags, descriptions, and chapters.
- Cleanup candidates: videos with poor fit, weak performance relative to channel median, stale positioning, or inconsistent audience promise. Mark as `keep`, `refresh`, `unlist/private candidate`, or `needs human review`; do not recommend deletion as an automated action.

### Content Quality Patterns

Split into positive patterns (double down) and critical patterns (fix).

**Every finding must cite evidence from 2+ videos to qualify as a pattern.** Single-video observations are not patterns — discard them.

Analyze across these dimensions:

| Dimension | What to look for |
| --- | --- |
| Positioning | Who is this channel for? Is it consistent? Does the creator own a niche? |
| Hooks | First 30 seconds — do they create curiosity, state a problem, or waste time? |
| Interview style | If applicable — question quality, follow-ups, guest chemistry, interruptions |
| Credibility | Does the creator demonstrate expertise? Name-drop experiences? Show receipts? |
| Topic selection | Are topics timely, evergreen, niche, or scattered? Do they match the audience? |
| Pacing | Does the content drag or rush? Are there dead zones? |
| Editing signals | Verbal cues for cuts, chapters, graphics. Does the script feel edited or rambling? |
| Startup rigor | If startup/business content — are frameworks used? Is advice actionable or generic? |
| Audience trust | Does the creator build trust or erode it? Sponsorship handling, honesty, consistency |
| Portfolio fit | Does each video serve a clear role in the channel strategy? |
| Packaging | Do title, thumbnail, topic, and opening promise align? |

### 7. Write Report

Save to `research/youtube/youtube-audit-<slug>-YYYY-MM-DD.md`:

```markdown
# YouTube Audit — [Channel Name]

> Channel: [URL]
> Videos analyzed: N
> Transcripts available: N of M
> Date: YYYY-MM-DD
> Raw metadata: research/youtube/data/<slug>/videos-YYYY-MM-DD.jsonl
> Raw transcripts: research/youtube/data/<slug>/transcripts/

## Videos Analyzed

| # | Title | Date | Views | Likes | Views/day | Views/min | Duration | Archetype | Role | Transcript |
|---|-------|------|-------|-------|-----------|-----------|----------|-----------|------|------------|
| 1 | [Title](URL) | YYYY-MM-DD | N | N | N | N | Xm | [type] | [role] | Yes/No |
| ... | | | | | |

## Performance Snapshot

- **Total views analyzed**: N
- **Median views**: N
- **Top 1 concentration**: N%
- **Top 3 concentration**: N%
- **Views/day leader**: [video]
- **Views/minute leader**: [video]

## Portfolio Shape

| Archetype | Videos | View share | Notes |
|---|---:|---:|---|
| ... | | | |

| Content role | Videos | View share | Notes |
|---|---:|---:|---|
| ... | | | |

## Positive Patterns (Double Down)

### [Pattern Title]
- **Frequency**: Found in N of M videos
- **Evidence**: [Video 1 title] — "[quote or description]"; [Video 2 title] — "[quote or description]"
- **Recommendation**: [What to keep doing or amplify]

### ...

## Critical Patterns (Fix)

### [Pattern Title]
- **Severity**: High / Medium / Low
- **Frequency**: Found in N of M videos
- **Evidence**: [Video 1 title] — "[quote or description]"; [Video 2 title] — "[quote or description]"
- **Impact**: [Why this hurts the channel]
- **Recommendation**: [Specific fix]

### ...

## Cleanup Candidates

| Video | Recommendation | Evidence | Human check |
|---|---|---|---|
| [Title](URL) | Keep / Refresh / Unlist-private candidate / Needs human review | [performance + fit evidence] | [what to inspect before action] |

## Summary

### Top 3 Strengths
1. [Strength] — [one-line why]
2. [Strength] — [one-line why]
3. [Strength] — [one-line why]

### Top 3 Weaknesses
1. [Weakness] — [one-line why]
2. [Weakness] — [one-line why]
3. [Weakness] — [one-line why]

### Strategic Recommendation
[2-3 sentences: the single most impactful change the channel should make, grounded in the patterns found]
```

Create the `research/youtube/` and `research/youtube/data/<slug>/` directories if they do not exist.

### 8. Summarize In Thread

After saving the report, output: top 3 strengths, top 3 weaknesses, performance/portfolio headline, strategic recommendation, report path, and raw data paths.

## Constraints

- **Pattern-only reporting**: Every finding must have evidence from 2+ videos. No single-video observations.
- **Sequential fetching**: Do not parallelize transcript fetches — use 1.5s delay to avoid IP rate limiting.
- **No API keys**: Both tools work unauthenticated against public data. Do not ask the user for API keys.
- **Smart truncation**: When truncating, always preserve hooks (first 500 words) and outros (last 300 words).
- **Honest coverage**: If transcripts are sparse, say so. Do not fabricate transcript content or hallucinate quotes.
- **Raw evidence first**: Always persist raw `yt-dlp` JSONL and transcript JSON before writing analysis.
- **No automated destructive content advice**: Cleanup candidates are review recommendations, not instructions to delete content.
- **Stay in analysis mode**: Do not propose video ideas, scripts, or content calendars. The job is to audit what exists.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default next-step routing, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/youtube-audit-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
