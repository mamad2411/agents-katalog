---
name: meeting-minutes
description: Generate Chinese meeting minutes from meeting audio, Tongyi Tingwu transcripts, optional PPT/PPTX materials, and user-provided background. Use when Codex needs to transcribe recordings with speaker labels, process an existing transcript plus audio for review, extract PPT talking points, and draft formal sales/technical meeting minutes in the user's preferred style.
---

# Meeting Minutes

Use this skill to turn a meeting recording, background notes, and optional PPT/PPTX material into a formal Chinese meeting record.

## Inputs

Require:

- Meeting audio path.
- Background information: meeting time/place if known, customer organization, customer attendees, internal attendees, exchange topic, and special context.

Optional:

- Existing transcript. If provided, use it and keep the audio as review evidence.
- PPT/PPTX used in the meeting. Extract text as supporting material; do not let PPT replace the transcript.

## Workflow

1. Create a run folder under the current workspace:
   `outputs/meeting-minutes-YYYYMMDD-HHMMSS/`.
2. If no transcript is provided, run:
   `python <skill>/scripts/tingwu_transcribe.py "<audio-path>"`.
   This uploads the audio to OSS, submits a Tongyi Tingwu offline task with diarization, downloads raw JSON, writes `transcript.md`, and deletes temporary OSS audio after completion.
3. If a PPT/PPTX is provided, run:
   `python <skill>/scripts/extract_ppt_notes.py "<pptx-path>" --output "<run-folder>/ppt-notes.md"`.
4. Read `references/templates.md`, the transcript, PPT notes if present, and the user's background.
5. Assess transcript quality before drafting. Check for: obvious gaps, repeated ASR mistakes, broken technical terms, unclear speaker turns, contradictions with user's background/PPT. Flag ALL uncertain segments in `review-notes.md` with timestamps and reasons. Do NOT attempt audio review — the current model (DeepSeek) is text-only. 通义听悟 already provides high-quality Chinese ASR; the transcript is the authoritative source.
6. Draft `meeting-minutes.md` in Chinese. Prefer polished meeting minutes over verbatim notes. When transcript has gaps, use context from the user's background and PPT notes to fill in, but mark any inferred content in review-notes.md.
7. Write `review-notes.md` listing: uncertain names/orgs, speaker mappings, likely ASR mistakes, segments with poor transcript quality (with timestamps), content inferred from context (not transcript), and recommendations for which segments the user should manually replay. This file serves as the user's guide for manual audio review.
8. Export Word:
   `python <skill>/scripts/render_docx.py "<run-folder>/meeting-minutes.md" "<run-folder>/meeting-minutes.docx"`.
9. Before finishing, compare the minutes against the checklist in `references/templates.md`.

## Configuration

Tongyi Tingwu transcription reads secrets from `~/.codex/meeting-minutes.env`.

Required keys:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `TINGWU_APPKEY`
- `OSS_BUCKET`
- `OSS_ENDPOINT`
- `OSS_REGION`

Optional:

- `TINGWU_ENDPOINT` defaults to `tingwu.<OSS_REGION>.aliyuncs.com`; for Beijing use `tingwu.cn-beijing.aliyuncs.com`.

Never print or paste secrets into the chat.

Before running bundled scripts in a fresh workspace, ensure Python dependencies are available:

`python -m pip install -r <skill>/scripts/requirements.txt`

## Drafting Rules

- Default to the "售前交流记录表" template.
- Switch to the long seminar template only when the background clearly says the meeting was a 研讨会、专家会、论坛、专题会议, or similar.
- Preserve speaker labels as `说话人1/2/3` unless the transcript and background make identity mapping obvious.
- Treat the transcript as the primary working text, and PPT as supporting context. 通义听悟 provides high-quality Chinese ASR with diarization — trust it as the authoritative source.
- Do NOT attempt to process the original audio (current model is text-only). Instead, flag any suspect transcript segments in `review-notes.md` with timestamps so the user can manually review.
- Focus the final minutes on customer needs, technical answers, opportunity clues, constraints, and follow-up actions.
- In "二、客户需求探讨", start with one concise overview sentence summarizing the customer's overall demand before numbered details.
- Do not invent names, dates, commitments, budgets, or product capabilities. Mark uncertainty in `review-notes.md`.

## Error Handling

- If Tongyi Tingwu reports `AudioDurationQuotaLimit`, tell the user the account lacks enough audio transcription quota.
- If the process stops while the Tingwu task is still running, keep the OSS object path from the script output and tell the user it may need manual cleanup.
- If PPT extraction has sparse output, continue with transcript and background; note the limitation in `review-notes.md`.
