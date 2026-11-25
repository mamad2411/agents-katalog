---
name: calendar-api
description: "Calendar API skill. Use when working with Calendar for calendars, channels, colors. Covers 37 endpoints."
version: 1.0.0
generator: lapsh
---

# Calendar API
API version: v3

## Auth
OAuth2 | OAuth2

## Base URL
https://www.googleapis.com/calendar/v3

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /colors -- verify access
3. POST /calendars -- create first calendars

## Endpoints

37 endpoints across 5 groups. See references/api-spec.lap for full details.

### calendars
| Method | Path | Description |
|--------|------|-------------|
| POST | /calendars | Creates a secondary calendar. |
| DELETE | /calendars/{calendarId} | Deletes a secondary calendar. Use calendars.clear for clearing all events on primary calendars. |
| GET | /calendars/{calendarId} | Returns metadata for a calendar. |
| PATCH | /calendars/{calendarId} | Updates metadata for a calendar. This method supports patch semantics. |
| PUT | /calendars/{calendarId} | Updates metadata for a calendar. |
| GET | /calendars/{calendarId}/acl | Returns the rules in the access control list for the calendar. |
| POST | /calendars/{calendarId}/acl | Creates an access control rule. |
| POST | /calendars/{calendarId}/acl/watch | Watch for changes to ACL resources. |
| DELETE | /calendars/{calendarId}/acl/{ruleId} | Deletes an access control rule. |
| GET | /calendars/{calendarId}/acl/{ruleId} | Returns an access control rule. |
| PATCH | /calendars/{calendarId}/acl/{ruleId} | Updates an access control rule. This method supports patch semantics. |
| PUT | /calendars/{calendarId}/acl/{ruleId} | Updates an access control rule. |
| POST | /calendars/{calendarId}/clear | Clears a primary calendar. This operation deletes all events associated with the primary calendar of an account. |
| GET | /calendars/{calendarId}/events | Returns events on the specified calendar. |
| POST | /calendars/{calendarId}/events | Creates an event. |
| POST | /calendars/{calendarId}/events/import | Imports an event. This operation is used to add a private copy of an existing event to a calendar. |
| POST | /calendars/{calendarId}/events/quickAdd | Creates an event based on a simple text string. |
| POST | /calendars/{calendarId}/events/watch | Watch for changes to Events resources. |
| DELETE | /calendars/{calendarId}/events/{eventId} | Deletes an event. |
| GET | /calendars/{calendarId}/events/{eventId} | Returns an event based on its Google Calendar ID. To retrieve an event using its iCalendar ID, call the events.list method using the iCalUID parameter. |
| PATCH | /calendars/{calendarId}/events/{eventId} | Updates an event. This method supports patch semantics. |
| PUT | /calendars/{calendarId}/events/{eventId} | Updates an event. |
| GET | /calendars/{calendarId}/events/{eventId}/instances | Returns instances of the specified recurring event. |
| POST | /calendars/{calendarId}/events/{eventId}/move | Moves an event to another calendar, i.e. changes an event's organizer. |

### channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /channels/stop | Stop watching resources through this channel |

### colors
| Method | Path | Description |
|--------|------|-------------|
| GET | /colors | Returns the color definitions for calendars and events. |

### freeBusy
| Method | Path | Description |
|--------|------|-------------|
| POST | /freeBusy | Returns free/busy information for a set of calendars. |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/me/calendarList | Returns the calendars on the user's calendar list. |
| POST | /users/me/calendarList | Inserts an existing calendar into the user's calendar list. |
| POST | /users/me/calendarList/watch | Watch for changes to CalendarList resources. |
| DELETE | /users/me/calendarList/{calendarId} | Removes a calendar from the user's calendar list. |
| GET | /users/me/calendarList/{calendarId} | Returns a calendar from the user's calendar list. |
| PATCH | /users/me/calendarList/{calendarId} | Updates an existing calendar on the user's calendar list. This method supports patch semantics. |
| PUT | /users/me/calendarList/{calendarId} | Updates an existing calendar on the user's calendar list. |
| GET | /users/me/settings | Returns all user settings for the authenticated user. |
| POST | /users/me/settings/watch | Watch for changes to Settings resources. |
| GET | /users/me/settings/{setting} | Returns a single user setting. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a calendar?" -> POST /calendars
- "Delete a calendar?" -> DELETE /calendars/{calendarId}
- "Get calendar details?" -> GET /calendars/{calendarId}
- "Partially update a calendar?" -> PATCH /calendars/{calendarId}
- "Update a calendar?" -> PUT /calendars/{calendarId}
- "List all acl?" -> GET /calendars/{calendarId}/acl
- "Create a acl?" -> POST /calendars/{calendarId}/acl
- "Create a watch?" -> POST /calendars/{calendarId}/acl/watch
- "Delete a acl?" -> DELETE /calendars/{calendarId}/acl/{ruleId}
- "Get acl details?" -> GET /calendars/{calendarId}/acl/{ruleId}
- "Partially update a acl?" -> PATCH /calendars/{calendarId}/acl/{ruleId}
- "Update a acl?" -> PUT /calendars/{calendarId}/acl/{ruleId}
- "Create a clear?" -> POST /calendars/{calendarId}/clear
- "Search events?" -> GET /calendars/{calendarId}/events
- "Create a event?" -> POST /calendars/{calendarId}/events
- "Create a import?" -> POST /calendars/{calendarId}/events/import
- "Create a quickAdd?" -> POST /calendars/{calendarId}/events/quickAdd
- "Create a watch?" -> POST /calendars/{calendarId}/events/watch
- "Delete a event?" -> DELETE /calendars/{calendarId}/events/{eventId}
- "Get event details?" -> GET /calendars/{calendarId}/events/{eventId}
- "Partially update a event?" -> PATCH /calendars/{calendarId}/events/{eventId}
- "Update a event?" -> PUT /calendars/{calendarId}/events/{eventId}
- "List all instances?" -> GET /calendars/{calendarId}/events/{eventId}/instances
- "Create a move?" -> POST /calendars/{calendarId}/events/{eventId}/move
- "Create a stop?" -> POST /channels/stop
- "List all colors?" -> GET /colors
- "Create a freeBusy?" -> POST /freeBusy
- "List all calendarList?" -> GET /users/me/calendarList
- "Create a calendarList?" -> POST /users/me/calendarList
- "Create a watch?" -> POST /users/me/calendarList/watch
- "Delete a calendarList?" -> DELETE /users/me/calendarList/{calendarId}
- "Get calendarList details?" -> GET /users/me/calendarList/{calendarId}
- "Partially update a calendarList?" -> PATCH /users/me/calendarList/{calendarId}
- "Update a calendarList?" -> PUT /users/me/calendarList/{calendarId}
- "List all settings?" -> GET /users/me/settings
- "Create a watch?" -> POST /users/me/settings/watch
- "Get setting details?" -> GET /users/me/settings/{setting}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
