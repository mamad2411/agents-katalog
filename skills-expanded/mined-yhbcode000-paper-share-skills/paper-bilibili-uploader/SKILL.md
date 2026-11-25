---
name: paper-bilibili-uploader
description: |
  Validate and upload narrated paper videos to Bilibili with biliup. Handles required landscape-first/portrait-second submissions, series uploads, CST scheduling, diagnostics, dry-run validation, and durable upload receipts. Trigger on: "upload to bilibili", "bilibili upload", "发布到B站", "上传到B站".
user-invocable: true
argument-hint: "<paper-directory> [--dry-run]"
---

# Paper Bilibili Uploader

Use the final packaged CLI:

```bash
python <SKILLS_DIR>/paper-bilibili-uploader/scripts/upload.py "<PAPER_DIR>" --dry-run
```

(The script depends on `biliup`, `psutil`, and `requests` — see `pyproject.toml` in the skill dir; run `uv sync` there or install them in the active interpreter if imports fail.)

Remove `--dry-run` only after reviewing the resolved parts, metadata, cover, and publication time.

## Required normal-mode layout

```text
<PAPER_DIR>/video/
  *_narrated.mp4
  *_portrait_narrated.mp4
  cover.png
  video_meta.json
```

Both MP4s must be nonempty. The CLI deterministically sends every landscape video before every portrait video: P1 landscape, then P2 portrait. A missing or empty landscape, portrait, cover, or metadata file fails closed.

## Cover policy (poster ARTIFACT required; FIRST-SLIDE cover uploads)

实验室调研 (课题组) dirs — detected by a `poster_data.json` in the paper root
— still REQUIRE the paper-video-cover POSTER artifact:
`<PAPER_DIR>/poster/poster.png` must exist (missing it fails the upload closed
with a generation hint). The UPLOAD COVER, however, defaults to the deck's
FIRST SLIDE: explicit `cover_path` in `video_meta.json` wins, otherwise
`video/cover.png` (rendered by the video pipeline from the title page) is
used — the poster is NOT copied over the first-slide cover. ALL OTHER papers
(论文分享 etc.) keep the plain cover contract — explicit `cover_path` →
`video/cover.png` — and a `poster/poster.png` in the dir is IGNORED. Series
mode (`--series`) skips the lab/poster check entirely.

If a lab video was already uploaded with the wrong cover, fix it WITHOUT
re-uploading: `upload.py --edit --vid <BV> --cover <video/cover.png>` —
the member cover endpoint uploads the image and the edit submits the URL
verbatim (stripping the scheme makes the edit fail with `封面必须由页面进行上传，不支持外部链接`).
The video stays in review briefly after upload; the edit succeeds once
unlocked (state 0), otherwise poll and retry.

Generate the portrait artifact with the retained managed workflow at `~/.omp/agent/managed-skills/rednote-video-uploader/scripts/portrait_video.py` (adjust to your agent's managed-skills directory).

## Metadata contract

`video/video_meta.json` must use Bilibili's singular `tag` key:

```json
{"title":"【Venue Year】Paper — 中文亮点","tag":["论文分享","机器人"],"tid":231,"copyright":1,"desc":"【论文信息】...","cover_path":"cover.png"}
```

Validation requires a nonempty string `title`; a nonempty list of nonempty strings in `tag`; a positive integer `tid`; `copyright` exactly `1` or `2`; and a nonempty `source` when copyright is `2`. `cover_path` must resolve to a nonempty file. Do not rename `tag` to `tags`; `tags` belongs to Rednote metadata.

## Dry-run boundary

`--dry-run` performs input resolution, P1/P2 ordering, metadata patching, publication scheduling, validation, and complete command construction. It returns before any biliup subprocess can start and never writes an upload receipt.

## CST scheduling

- 00:00–22:59 publishes immediately unless metadata or `--dtime` supplies a delayed time.
- 23:00–23:59 schedules 07:00 the next day when no delayed time is already supplied.
- Explicit `--dtime` always wins; it accepts `YYYY-MM-DD HH:MM` in CST or a ten-digit Unix timestamp.

## Upload receipt

A real upload succeeds only when biliup exits zero and returns a BV identifier. The CLI writes `video/upload_result.json` exactly with `status`, `bv`, `url`, and ISO-8601 `uploaded_at` fields. A zero exit without a BV identifier fails and writes no receipt.

## Series mode

Place ordered P1–PN landscapes, `cover.png`, and `video_meta.json` in `<PAPER_DIR>/bilibili-series/video/`, then add `--series`. Series mode preserves filename order and intentionally does not require a portrait part.

## Login and diagnostics

Use the same CLI with `--login`, `--diagnose`, or `--kill-all`. Cookies live at `%USERPROFILE%/.bilibili/cookies.json`. Diagnostics use psutil process/open-file inspection, do not depend on WMIC or fsutil, and tolerate an unset `LOCALAPPDATA`.

## Related skills

- skill://paper-video-cover
- skill://rednote-video-uploader
- skill://awesome-embodied-batch-pipeline
- skill://bilibili-edit-while-in-review
- skill://blog-to-bilibili
- skill://lab-survey-to-bilibili-runbook
