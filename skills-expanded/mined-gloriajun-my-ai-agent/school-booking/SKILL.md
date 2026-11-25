---
name: school-booking
description: "Book, check, or cancel a school practice room or lesson room. Use when the user requests to reserve, book, schedule, list, check, or cancel a practice room or lesson room at school."
metadata:
  {
    "openclaw":
      {
        "emoji": "🏫",
        "requires": { "bins": ["curl"] }
      }
  }
---

# School Booking Skill

> **IMPORTANT**: For EVERY user request, you MUST call the `exec` tool to run the curl command first.
> Do NOT respond before exec is called — you have no knowledge of the booking result without the webhook call.

Handles school practice room and lesson room reservations: add, list, and delete.

---

## Action Mapping

Determine `action` from user intent:

| User intent | action |
|-------------|--------|
| 예약, 잡아줘, 신청, 등록 | `add` |
| 조회, 확인, 리스트, 목록, 뭐 있어 | `list` |
| 취소, 삭제 | `delete` |

All requests use: `POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action={action}"`

---

## action=add (예약 등록)

### Required fields

| Field | Key  | Format     |
|-------|------|------------|
| Date  | date | YYYY-MM-DD |
| Time  | time | HH:MM (24h)|

If `date` or `time` is missing, ask the user before proceeding.

### Optional fields — include ONLY when explicitly stated by the user

| Field    | Key          | Format                        | Default if omitted |
|----------|--------------|-------------------------------|--------------------|
| Type     | type         | `lesson` / `practice`         | `lesson`           |
| Duration | duration     | 30 / 60 / 90 / 120 (minutes)  | omit               |
| Room     | room         | string (e.g. `"2"`)           | omit               |
| Recurring| is_recurring | true / false                  | false              |
| Count    | recurring_count | integer, 1-12              | 4, only if is_recurring is true |

### Auto-included fields

Always include these in every webhook call body:

| Field      | Key          | How to get the value |
|------------|--------------|----------------------|
| Thread ID  | thread_id    | Slack `thread_ts` of the current conversation |
| Channel ID | channel_id   | Extract from `chat_id`: `agent:main:slack:channel:CXXXXXXX` → `CXXXXXXX` |
| Message TS | message_ts   | `message_id` from the current message runtime context |

**IMPORTANT:**
- No mention of repetition means exactly one reservation: leave `is_recurring` false and omit `recurring_count`. The count has no effect unless `is_recurring` is true.
- Never ask for `room` or `is_recurring` — room is assigned automatically by the backend.
- `is_recurring` defaults to false unless the user explicitly says "매주", "반복" or similar.
- When `is_recurring` is true, read the count from the request ("8회" / "8주" / "8번" → `recurring_count: 8`) and send it. A count above 12 is rejected by the backend, so ask for a number in 1-12 instead of sending it.
- When `is_recurring` is true but no number was given, omit `recurring_count`. The backend then creates 4 reservations, so the reply must say 기본 4건 rather than implying the series continues indefinitely.
- "레슨실" → `type: lesson`, "연습실" → `type: practice`. Never put facility name in `room`.
- Always include `thread_id`, `channel_id`, and `message_ts` in every webhook call.
- As soon as `date` and `time` are known, call the webhook immediately.

### Date / Time handling

- Infer year from current date in context if not specified.
- If the date appears to have already passed this year, ask the user to confirm the intended year.
- Convert 12-hour expressions to 24h: 오후 N시 → N+12:00 (오후 12시 → 12:00), 오전 N시 → N:00.
- Always include the day of week when expressing a date (e.g. 2026년 4월 22일 수).

### curl examples

```bash
# Minimum (date + time)
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=add" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"date":"YYYY-MM-DD","time":"HH:MM","thread_id":"<slack_thread_ts>","channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'

# With type
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=add" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"date":"YYYY-MM-DD","time":"HH:MM","type":"lesson","thread_id":"<slack_thread_ts>","channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'

# With room and duration
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=add" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"date":"YYYY-MM-DD","time":"HH:MM","type":"lesson","room":"2","duration":60,"thread_id":"<slack_thread_ts>","channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'

# With recurring (8 reservations, including the first)
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=add" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"date":"YYYY-MM-DD","time":"HH:MM","is_recurring":true,"recurring_count":8,"thread_id":"<slack_thread_ts>","channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'
```

**Success**: `status === "ok"` AND `reservations` array is non-empty.

On success, output the `message` field as a header, then list all items in `reservations` using the same format as action=list. For each item:
- `date` is the 이용일 (YYYY-MM-DD); derive day of week from it
- Time: `start_time` ~ `end_time`
- Map `facility_type`: `"lesson"` → 레슨실, `"practice"` → 연습실
- Map `room_number`: digit string (e.g. `"3"`) → "N호"; `"자동선택"` → "자동배정"
- Format: `- #<id> <date> <요일> <start_time> ~ <end_time> (<facility_type>: <room>)`

Example output (reservations only):
```
예약이 등록되었습니다. (총 8건)

- #42 2026-04-14 월 16:30 ~ 18:00 (레슨실: 3호)
- #43 2026-04-21 월 16:30 ~ 18:00 (레슨실: 3호)
...
```

Example output (with skipped dates):
```
예약이 등록되었습니다. (총 7건, 1건 스킵)

- #42 2026-04-18 토 16:30 ~ 18:00 (레슨실: 3호)
...

스킵된 날짜:
- 2026-05-05 화 — 공휴일 (어린이날)
```

If `skipped` is absent or empty, omit the "스킵된 날짜" section entirely. Format `skipped[].date` as `YYYY-MM-DD 요일`, and append ` — {reason}`.

**Failure**: `status` ≠ `"ok"`, or `reservations` is absent or empty → inform the user the booking did not go through. Include the `message` field if present.

---

## action=list (예약 조회)

### Optional fields

| Field | Key  | Format     | Description        |
|-------|------|------------|--------------------|
| Date  | date | YYYY-MM-DD | Filter by date; omit for all reservations |

### curl examples

```bash
# All reservations
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=list" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'

# Filter by date
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=list" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"date":"YYYY-MM-DD","channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'
```

Present the results as a list sorted by `date` (이용일, earliest first). Show only the first 5 items; if there are more, append "외 N건이 더 있습니다." on a separate line.

Start with the total count header: "총 N건의 예약이 있습니다."

For each item, use format: `- #<id> <date> <요일> <start_time> ~ <end_time> (<facility_type>: <room>)`
- `date` is the 이용일 (YYYY-MM-DD); derive day of week from it
- `start_time` ~ `end_time`: from respective API fields
- type+room: map `facility_type` ("lesson"→레슨실, "practice"→연습실); if `room_number` is a digit string (e.g. "3") use "N호" (e.g. "레슨실: 3호"); if `room_number` is "자동선택" use "자동배정" (e.g. "레슨실: 자동배정"). Never output raw JSON.

Example output (truncated):
```
총 12건의 예약이 있습니다.

- #8 2026-04-27 월 14:30 ~ 16:30 (레슨실: 3호)
- #9 2026-04-28 화 16:30 ~ 18:00 (레슨실: 자동배정)
...
외 7건이 더 있습니다.
```

---

## action=delete (예약 취소)

### Required fields

| Field | Key | Format  |
|-------|-----|---------|
| Reservation ID(s) | ids | integer array |

If the user does not provide an ID, call `action=list` first to retrieve reservations, then ask the user which one to cancel.

**IMPORTANT**: 취소 요청은 항상 `ids` 배열로 단일 webhook 요청을 사용한다. 개별 curl 반복/병렬 실행 금지.

### curl examples

```bash
# 단일 취소
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=delete" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"ids":[3],"channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'

# 복수 취소
curl -X POST "${N8N_WEBHOOK_BASE_URL}?type=booking&mode=school&action=delete" \
  -H "Content-Type: application/json" \
  --max-time 30 \
  -d '{"ids":[8,9,12],"channel_id":"<CHANNEL_ID>","message_ts":"<MESSAGE_TS>"}'
```

Only confirm cancellation after receiving a success response from the webhook.

---

## Language

Respond in the same language the user used.
