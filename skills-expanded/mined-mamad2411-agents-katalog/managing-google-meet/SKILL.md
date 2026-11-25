---
name: managing-google-meet
description: |
  Use when working with Google Meet — google Meet management covering meeting
  spaces, calendar events with conferencing, and participant analytics. Use when
  auditing Google Meet usage, managing meeting rooms, retrieving meeting
  history, or analyzing participation patterns via Google Calendar and Meet
  APIs.
connection_type: google-meet
preload: false
---

# Managing Google Meet

Google Meet management and analytics via Google Calendar and Meet REST APIs.

## Discovery Phase

```bash
#!/bin/bash
GCAL_BASE="https://www.googleapis.com/calendar/v3"
MEET_BASE="https://meet.googleapis.com/v2"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "https://www.googleapis.com/oauth2/v2/userinfo" \
  | jq '{id, email, name}'

echo ""
echo "=== Upcoming Calendar Events with Meet Links ==="
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "$GCAL_BASE/calendars/primary/events?timeMin=$NOW&maxResults=20&singleEvents=true&orderBy=startTime" \
  | jq -r '.items[] | select(.conferenceData != null) | "\(.id)\t\(.summary[0:40])\t\(.start.dateTime // .start.date)\t\(.conferenceData.entryPoints[0].uri // "N/A")"' \
  | column -t

echo ""
echo "=== Recent Past Meetings (last 7 days) ==="
PAST=$(date -v-7d -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d "-7 days" +%Y-%m-%dT%H:%M:%SZ)
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "$GCAL_BASE/calendars/primary/events?timeMin=$PAST&timeMax=$NOW&maxResults=25&singleEvents=true&orderBy=startTime" \
  | jq -r '.items[] | select(.conferenceData != null) | "\(.summary[0:40])\t\(.start.dateTime[0:16] // .start.date)\t\(.attendees | length // 0) attendees"' \
  | column -t

echo ""
echo "=== Meet Spaces ==="
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "$MEET_BASE/spaces" \
  | jq -r '.spaces[]? | "\(.name)\t\(.meetingUri)\t\(.config.accessType // "default")"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
GCAL_BASE="https://www.googleapis.com/calendar/v3"
EVENT_ID="${1:?Calendar Event ID required}"

echo "=== Event Details ==="
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "$GCAL_BASE/calendars/primary/events/$EVENT_ID" \
  | jq '{summary, start: .start.dateTime, end: .end.dateTime, organizer: .organizer.email, attendees_count: (.attendees | length), meet_link: .conferenceData.entryPoints[0].uri, status}'

echo ""
echo "=== Attendee Responses ==="
curl -s -H "Authorization: Bearer $GOOGLE_TOKEN" \
  "$GCAL_BASE/calendars/primary/events/$EVENT_ID" \
  | jq -r '.attendees[]? | "\(.email)\t\(.responseStatus)\t\(if .organizer then "organizer" else "" end)"' | column -t
```

## Output Format

```
GOOGLE MEET OVERVIEW
User:             [name] ([email])
Upcoming Meets:   [count]
Past Week Meets:  [count]

UPCOMING MEETINGS
Event                   Start Time       Attendees  Meet Link
[summary]               [datetime]       [n]        [url]

MEETING HEALTH
Avg Attendees:     [avg]
Acceptance Rate:   [pct]%
Recurring Meets:   [count]
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

