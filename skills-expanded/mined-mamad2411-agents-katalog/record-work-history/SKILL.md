---
name: record-work-history
description: Classify and record user-provided project updates, completed work, discussions, decisions, status changes, schedules, and historical context into the correct workspace records. Use whenever the user casually drops work context that may deserve durable history; write automatically only when project, meaning, state, and destination are clear, and ask a confirmation question before writing when any material ambiguity remains.
---

# Purpose

Turn informal work updates into accurate, traceable workspace history without forcing the user to specify file paths or record types.

# Core Decision

Classify the input before writing.

Write automatically only when all material facts are clear:

- owning company or personal scope
- owning project
- what happened
- state such as planned, started, blocked, completed, deployed, verified, or discussed
- relevant date
- appropriate record destination
- privacy level when sensitive information may be involved

If any ambiguity could change the project, state, date, privacy, ownership, or destination, ask a concise confirmation question and do not write until answered.

Do not ask when the missing detail is immaterial and can be recorded explicitly as unknown.

# Source Priority

1. Treat the user's statement as the primary source.
2. Use the DB-backed `agent_mcp` virtual filesystem first for workspace records.
3. Read project metadata before project rules:
   - `ai-workspace/95-projects/active/<project>.md`
   - `ai-workspace/70-knowledge/domains/<company>/projects/<project>/rules.md`
4. Search existing task, schedule, raw log, discussion, and project history records to prevent duplicates.
5. Use local markdown only when runtime behavior requires it or the user explicitly requests local files.

# Classification

Route each fact to the smallest sufficient durable record:

| Input meaning | Primary destination |
|---|---|
| Completed implementation, deployment, verification, or business work | project history and relevant task status |
| Work performed today | `ai-workspace/40-tasks/daily/raw/YYYY-MM-DD.md` |
| New actionable work or open completion criterion | `ai-workspace/40-tasks/` |
| Date-bound appointment, deployment, or planned work | `ai-workspace/41-personal-schedule/daily/YYYY-MM-DD.md` |
| Recurring operational reminder | `ai-workspace/42-notification-reminders/entries/` |
| Exploratory conversation or unresolved question | `ai-workspace/25-discussions/` |
| Confirmed project decision or durable project event | owning project history |
| Reusable cross-project lesson | propose distillation; do not promote without approval |
| Failure or operational incident | incident record and related project history |

One update may require multiple linked records, but do not duplicate the same prose across them. Keep one authoritative history record and use concise cross-links elsewhere.

# Automatic Recording Examples

Record without asking:

- “카드톡 CT-24 개정연도 제거 운영 배포 완료했고 검색과 상세 화면 확인했어.”
  - Project, task, completion, deployment, and verification are explicit.
- “달달영어 Sprint 5 운영 배포는 6월 10일 완료.”
  - Project, event, date, and state are explicit.

# Confirmation Examples

Ask before writing:

- “배포 완료했어.”
  - Project and deployment target are unknown.
- “문의하기 건 정리해줘.”
  - Record intent and completion state are unclear.
- “어제 이야기한 거 반영됐어.”
  - Referenced topic and meaning of “반영” are unclear.
- A statement could belong to two projects or could mean either implementation completion or deployment completion.

Ask only the minimum questions needed, for example:

```txt
어느 프로젝트의 어떤 항목이 완료된 건가요? 구현 완료인지 운영 배포 완료인지도 함께 확인해 주세요.
```

# Workflow

1. Extract candidate facts without upgrading vague wording into certainty.
2. Identify the owning project and read its metadata and rules.
3. Search for an existing matching task or history record.
4. Decide whether the input is clear enough to write.
5. If ambiguous, ask the minimum confirmation question and stop before mutation.
6. If clear, update the authoritative MCP resource first.
7. Update linked task, schedule, raw log, reminder, or incident records only when the new fact changes their state.
8. Preserve prior history; append or version records instead of overwriting unrelated content.
9. Distinguish user-stated fact from inference.
10. Report exactly what was created or updated and identify anything intentionally left unchanged.

# Completion Rules

- “작업 완료” does not imply deployment completed.
- “배포 완료” does not imply post-deploy verification completed.
- “검증 완료” does not imply Dooray or task status was updated.
- A past-tense statement may be historical context rather than a request to mark an active task complete.
- Never infer an owner, deadline, project, environment, or success result that the user did not provide or existing records do not establish.

# Privacy And Safety

- Ask before storing information whose personal or company scope is unclear.
- Keep personal, customer, student, credential, medical, financial, and private contact information out of shared records unless explicitly authorized and necessary.
- Do not inspect binary attachments unless the user requested inspection.
- Do not submit external reports, send messages, change production systems, or perform destructive actions.
- Do not promote a single conversation into an organizational standard without human approval.

# Output

After automatic recording, respond with:

- interpreted project and event
- records created or updated
- resulting documented state
- unresolved follow-up, if any

After ambiguity detection, respond only with the confirmation needed to proceed and a short reason the distinction matters.

# Verification

- Project metadata and rules were checked when a project was involved.
- Existing records were searched for duplicates and current state.
- Every status claim is supported by the user statement or an existing source.
- MCP was used first for ordinary workspace records.
- Cross-links are reciprocal when required by workspace rules.
- No write occurred before confirmation when material ambiguity existed.
