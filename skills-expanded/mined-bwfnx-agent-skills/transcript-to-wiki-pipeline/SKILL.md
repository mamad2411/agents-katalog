---
name: transcript-to-wiki-pipeline
description: Process SBDC Zoom training transcript Markdown files through the archive pipeline. Use when asked to turn new SBDC AI Co-Working Hour or training transcripts into reviewed summaries, Claromentis article drafts, wiki ingestion packets, or to batch-process pending files in `sbdc-advising/raw/training-media/zoom-archive/02_Transcripts`.
---

# Transcript To Wiki Pipeline

Use this skill to process one transcript, or all pending transcripts, through the SBDC Zoom training archive pipeline.

## Locations

Archive root:

`sbdc-advising/raw/training-media/zoom-archive/`

Pipeline folders:

- `01_Raw Zoom Exports/` - raw Zoom assets and session metadata
- `02_Transcripts/` - input Markdown transcripts
- `03_Reviewed Summaries/` - session review output
- `04_Claromentis Drafts/` - one Claromentis-ready article per meeting
- `05_Wiki Inputs/` - curated packets for scheduled wiki ingestion
- `00_Master Index/zoom-training-media-manifest.csv` - status tracker

## Quick Start

Run the helper to inspect status:

```powershell
python "scripts\scan_pipeline.py" --archive "sbdc-advising\raw\training-media\zoom-archive"
```

Then process each `needs_processing` transcript.

## Per-Transcript Workflow

For each transcript in `02_Transcripts/{session_id}/{session_id}-transcript.md`:

1. Read the transcript and manifest row.
2. Create `03_Reviewed Summaries/{session_id}-reviewed-summary.md`.
3. Create `04_Claromentis Drafts/{session_id}-claromentis-draft.md`.
4. Create `05_Wiki Inputs/{session_id}-wiki-input.md`.
5. Update the manifest review/status fields.

Use `apply_patch` for file edits when working inside the workspace.

## Output Requirements

### 03 Reviewed Summary

Write a human-readable review of the meeting. Include:

- Metadata table
- Executive summary
- What happened
- Key workflows demonstrated
- Tools and platforms discussed
- Advisor takeaways
- Claromentis draft building blocks
- Follow-up actions
- Source traceability

### 04 Claromentis Draft

Write one publishable internal article per meeting. Include:

- Draft metadata
- Short summary
- Draft article body
- Practical next steps for advisors
- Internal editor notes

Use a practical internal SBDC tone. Do not write a combined series article unless explicitly requested.

### 05 Wiki Input

Write a curated packet for the SBDC wiki ingestion task. Include:

- Ingestion metadata
- Recommended target wiki articles
- Ingestion summary
- Wiki-ready additions
- Cross-link suggestions
- Facts and terms to preserve
- Source note

This file should be wiki-like and structured for ingestion, not newsletter-like.

## Missing Transcript Rule

If the manifest shows `missing_source_transcript`, or there is raw audio/video but no Markdown transcript:

- Do not infer session content.
- Do not summarize from surrounding sessions.
- Create or preserve only placeholder/pending files if the user asks for one artifact per meeting.
- Mark the manifest as pending transcript recovery.

Use language such as:

`Do not inject substantive session content until a transcript is recovered or audio is transcribed and reviewed.`

## Manifest Statuses

Use these review status values:

- `reviewed_summary_created` - step 3 complete only
- `claromentis_draft_created` - step 4 complete
- `claromentis_draft_pending_transcript` - step 4 placeholder only
- `wiki_input_created` - step 5 complete
- `wiki_input_pending_transcript` - step 5 placeholder only

Preserve existing manifest columns and source-file names. Update only the transcript/review status and notes needed for the pipeline state.

## Batch Mode

When asked to run weekly or batch mode:

1. Run `scripts/scan_pipeline.py`.
2. Process rows marked `needs_processing`.
3. Skip rows marked `complete`.
4. For rows marked `missing_transcript`, create pending placeholders only if missing.
5. Report processed, skipped, pending, and errors.

Do not rebuild the SBDC wiki unless actual `sbdc-advising/wiki/*.md` files were changed. Creating `05_Wiki Inputs` files alone prepares the scheduled wiki injection task; it does not itself modify the wiki.

