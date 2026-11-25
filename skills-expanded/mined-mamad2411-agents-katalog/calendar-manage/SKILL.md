---
name: calendar-manage
description: "Manage calendar events using CalDAV protocol."
metadata:
  openclaw:
    emoji: "📆"
---

# Calendar Management

Manage calendar events via CalDAV.

## List Events

```bash
curl -X REPORT "$CALDAV_URL/calendars/$USER/default/" \
  -H "Content-Type: application/xml" \
  -u "$CALDAV_USER:$CALDAV_PASSWORD" \
  -d '<?xml version="1.0"?><c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav"><d:prop><d:getetag /><c:calendar-data /></d:prop><c:filter><c:comp-filter name="VCALENDAR"><c:comp-filter name="VEVENT" /></c:comp-filter></c:filter></c:calendar-query>'
```

## Tips for AI Agents

- CalDAV is the standard protocol supported by most calendar servers.
- Use iCalendar format (.ics) for event data.
- Radicale, Baikal, and Nextcloud all support CalDAV.
