---
name: meeting-intelligence
description: >
  회의 녹음파일, 기존 STT 전사본, 회의 메모를 입력받아 transcript, summary,
  decisions, action items, follow-up draft, optional TTS briefing까지 만드는
  회의 인텔리전스 스킬이다.
---

# Meeting Intelligence

## Use When

- 회의 녹음파일에서 전사, 요약, 액션아이템을 뽑아야 한다.
- 기존 STT 산출물을 재사용해 회의록을 구조화해야 한다.
- 회의 후속 메일, Slack/Notion 공유본, 음성 브리핑까지 이어가야 한다.

## Input Contract

- Required: audio path, transcript path, or pasted notes.
- Helpful metadata: meeting title, date, participants, project, confidentiality level, target audience.
- If the request mentions a previous STT run, search for that transcript first and reuse it when available.

## Privacy And Reuse Gates

1. Classify the input as public, internal, confidential, or sensitive before processing.
2. Reuse an existing transcript/STT artifact before starting a new transcription run.
3. If transcript is missing, prefer a local/offline STT path when available.
4. Ask for explicit approval before uploading private meeting audio to any external service.
5. Generate TTS briefing audio only after the text summary is reviewed or explicitly approved.

## Workflow

1. Locate input: audio file, transcript, meeting title, date, participants, confidentiality level.
2. Check for prior STT/transcript artifacts and record the selected source path.
3. Write `source_register.md` with input path, privacy class, STT reuse/local/external route, and approval state.
4. If transcript is missing, run or route STT and save the transcript as a durable artifact.
5. Segment transcript by time range or speaker if diarization exists.
6. Extract summary: agenda, context, key discussion points, risks.
7. Extract decisions and open issues separately.
8. Extract action items: owner, task, due date, dependency, source timestamp, status.
9. Draft follow-up: short recap, action table, unresolved questions, next meeting needs.
10. Optional TTS: prepare a briefing script first, then generate audio only after approval.

## Outputs

- `transcript.md`
- `source_register.md`
- `meeting_summary.md`
- `decisions_and_open_issues.md`
- `action_items.csv`
- `followup_message.md`
- `verification.md`
- optional `briefing_script.md`
- optional `briefing_audio.*`

## Verification

- Confirm every summary and decision points back to a transcript section, timestamp, or source note.
- Confirm `action_items.csv` includes owner, task, due date, dependency, source reference, and status columns.
- Mark unknown owners, dates, or dependencies as `TBD`; do not infer them without evidence.
- Record whether STT was reused, newly generated locally, externally routed with approval, or skipped.

## Stop Rules

- Do not upload private meeting audio to an external service without explicit approval.
- Do not invent owners or due dates; mark missing values as `TBD`.
- Do not skip the transcript artifact when a summary is generated from audio.
- Do not generate a voice briefing from confidential content unless the user explicitly asks for it after reviewing the text.
