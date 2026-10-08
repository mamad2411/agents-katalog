---
name: normalize-yonsei-courses
description: Query authorized Yonsei Underwood handbook rows directly, then normalize them or fallback screenshot, PDF, spreadsheet, pasted table, export, or JSON into stable course-planning data. Use when course data has Korean or English fields, campus aliases, Korean weekday/time strings, mixed section identifiers, or needs validation before conflict checking and timetable construction.
---

# Normalize Yonsei Courses

Convert official Underwood handbook rows into deterministic planning data.
User-provided files remain a fallback, not the default collection step.

## Prepare the input

First call `yonsei_student` with `intent: "courses"`, `action: "search"`, and
pass known search conditions such as `year`, `semester`, `campus`, `college`,
`department`, and `keyword`. Put a college or catalogue category such as
`Engineering`, `College of Engineering`, or `공과대학` in `college`; reserve
`department` for a department within that college. Use
`primary_result.courses` from the official public `수업 → 수강편람` query.
This query runs through direct HTTPS JSON, does not launch a browser, and does
not require login, Accessibility, Screen Recording, or Computer Use setup. The
separate registration site and personal mileage history remain login-dependent
and may be period-limited; that does not make the public handbook unavailable.

Do not use general web search for live handbook rows. If `yonsei_student` is
not available, tell the student that `yonsei-student-companion` is missing or
inactive instead of waiting on web search. If the tool returns a temporary
failure, report it once and stop rather than repeating the same query. When
`primary_result.result_limited` is true, explain that the official page capped
the result, distinguish `course_count` (rows read from the current grid) from
`official_result_count`, and ask for a department or keyword before running
another query. Do not call `yonsei_bridge_connect` for a catalogue-only search.

If the direct official query fails, or the user intentionally attaches a
course-catalogue screen, PDF, spreadsheet, or pasted table, extract recognized
course fields into a private temporary JSON file. Do not ask the user to write
JSON or capture the handbook. Preserve unreadable or missing times as unknowns,
ask only for information required by the requested plan, and never guess
official period-to-clock mappings.

## Run

Pass a JSON object with a `courses` array:

```bash
python3 "$SKILL_DIR/scripts/normalize_courses.py" --input courses.json
```

Each row may use English keys or common Korean keys such as `학정번호`, `분반`, `교과목명`, `학점`, `강의시간`, and `캠퍼스`. Accept meeting strings such as `월수 10:00-11:15`, `화 13:00~14:50 @ 국제`, or structured meeting objects.

Treat the emitted `yonsei-normalized-courses/v1` JSON as the handoff contract for downstream skills. The normalizer preserves only recognized planning-envelope fields (`requirements`, `fixed_course_ids`, `constraints`, `preferences`, search limits, `blocked_times`, and `travel_minutes`) so the output can be passed directly to the builder, audit, or schedule checker. Show warnings to the user; never silently treat missing meeting times or unknown campuses as conflict-free.

## Boundaries

- Prefer the direct official Underwood handbook. Do not ask for a screenshot
  while that direct path works.
- The normalization script itself transforms supplied rows; only
  `yonsei_student` may claim that rows came from the official handbook query.
- Reject period-number notation such as `월1,2` because the official period-to-clock mapping is not packaged.
- Preserve source URLs when supplied, but do not fetch them.
- Never submit, cancel, or modify a registration.
