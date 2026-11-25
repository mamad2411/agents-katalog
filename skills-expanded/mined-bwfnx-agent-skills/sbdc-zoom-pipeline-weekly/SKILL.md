---
name: sbdc-zoom-pipeline-weekly
description: Monday 6pm ET: scan SBDC Zoom archive, draft 03/04/05 for new transcript-backed sessions, leave status for {{USER}}'s review.
---

> **Schedule:** Monday 6pm ET
> **Needs:** workspace files, Zoom
> **Helper scripts (yours, not included):** _wiki-infrastructure/zoom_training_media_archive.py

Process the SBDC AI Co-Working / training Zoom pipeline for any NEW sessions. Work only inside the staged archive at `{{WORKSPACE_ROOT}}/sbdc-advising/raw/training-media/zoom-archive/`. Stages: `01_Raw Zoom Exports`, `02_Transcripts`, `03_Reviewed Summaries`, `04_Claromentis Drafts`, `05_Wiki Inputs`; manifest at `00_Master Index\zoom-training-media-manifest.csv`; per-folder `metadata.json` in each `01_Raw Zoom Exports\<session>\`.

STEP 1 — Register new raw folders. From `{{WORKSPACE_ROOT}}` run:
`python {{WORKSPACE_ROOT}}/_wiki-infrastructure/zoom_training_media_archive.py scan`
then `python {{WORKSPACE_ROOT}}/_wiki-infrastructure/zoom_training_media_archive.py spotcheck`
(In the Linux sandbox the archive is under `/sessions/<session>/mnt/{{WORKSPACE_ROOT}}/...`; use python3 there.)

STEP 2 — Find sessions that NEED processing. A session needs processing when it has a transcript OR caption file present in its `01_Raw Zoom Exports\<session>\` folder AND is missing one or more of these three deliverables:
- `03_Reviewed Summaries\<session>-reviewed-summary.md`
- `04_Claromentis Drafts\<session>-claromentis-draft.md`
- `05_Wiki Inputs\<session>-wiki-input.md`
Detect readiness by MISSING deliverable files, NOT by review_status (status is intentionally left at archive_only in this workflow). Skip any session that already has all three. Skip the "Tag up meeting notes" row and any non-Zoom loose files.

STEP 3 — For each session needing processing, using TRANSCRIPT and CHAT EVIDENCE ONLY (do not infer or borrow content from other sessions):
1. If `02_Transcripts\<session>\<session>-transcript.md` (or `-captions.md` when only a caption/cc.vtt exists) is missing, convert the raw `.transcript.vtt`/`.cc.vtt` to markdown into `02_Transcripts\<session>\`.
2. Create the `03` reviewed summary, `04` Claromentis draft, and `05` wiki-input packet, matching the exact structure/sections of the existing files in each stage (open a recent example such as `20260727_...` or `20260202_...` and follow its format, headings, and metadata-table conventions).

STEP 4 — Handle missing transcripts. If a session has archived video/audio but NO transcript or caption file, do NOT generate content. Leave/keep its manifest `review_status` as `wiki_input_pending_transcript` and create only a pending-transcript placeholder `05` packet in the same style as `20260209_chatgpt-co-working-hour_v1-wiki-input.md` (which says "do not inject content" and lists recovery steps). Report it under pending transcript recovery.

GUARDRAILS (hard):
- Do NOT change `review_status` for processed sessions — leave it `archive_only` so {{USER}} reviews the drafts before sign-off. You MAY update the `notes`/`updated_utc` metadata fields to note that drafts were created, and `transcript_status` if you converted a transcript.
- Do NOT edit `sbdc-advising/wiki/*.md`, do NOT rebuild SBDC-Wiki.html, do NOT publish, git push, send email, or delete anything.
- Never delete files; if something must be removed, move it to `{{WORKSPACE_ROOT}}/DELETE/`.
- The zoom-archive folder is gitignored, so there is nothing to commit — do not attempt git operations.

FINAL REPORT: list processed sessions (with the files created), skipped (already complete), pending transcript recovery, ambiguous/non-session files, all changed files, and a verification check (confirm each processed session now has all three 03/04/05 files and that no `review_status` was flipped). If no new sessions were found, say so plainly and stop.